#!/usr/bin/env python3
"""Migra el reproductor de v1 a v2 en un capítulo HTML.

v2 añade respecto a v1:
  - botones de salto ±15s
  - botón toggle del karaoke (persistencia en localStorage)
  - recordar posición de reproducción (localStorage por capítulo)
  - propagación del color "leída" a la puntuación entre palabras (glue)
  - safePlay (atrapa la Promise de audio.play)
  - fetch del alignment sin `cache: 'force-cache'` (Safari file:// lo rechaza)

Es idempotente: si ya está v2 no hace nada. Falla ruidosa si el archivo no
está en el estado v1 esperado.

Uso:
  upgrade_audio_pill_v2.py <capitulo.html> <audio_src> <duration HH:MM> <storage_key>
"""
import re
import sys
from pathlib import Path

# ────────────────────────────────────────────────────────────────
# CSS karaoke v2 (reemplaza el de v1: añade .g + body.karaoke-off)
# ────────────────────────────────────────────────────────────────
CSS_KARAOKE_V2 = """\
.w { cursor: pointer; transition: color 0.25s ease, background-color 0.15s ease; border-radius: 2px; }
.w:hover { color: var(--verde); }
.w.leida { color: var(--ink-soft); opacity: 0.85; }
.w.activa { background-color: rgba(255,122,24,0.18); color: var(--verde); padding: 0 0.12em; }
.g { transition: color 0.25s ease, opacity 0.25s ease; }
.g.leida { color: var(--ink-soft); opacity: 0.85; }
body.karaoke-off .w { cursor: text; }
body.karaoke-off .w:hover { color: inherit; }
body.karaoke-off .w.leida, body.karaoke-off .w.activa,
body.karaoke-off .g.leida { color: inherit; background-color: transparent; opacity: 1; padding: 0; }"""

# ────────────────────────────────────────────────────────────────
# CSS pill v2 (reemplaza el de v1)
# ────────────────────────────────────────────────────────────────
CSS_PILL_V2 = """\
/* AUDIO PILL v2 — flotante, colapsa/expande, con skip + toggle karaoke + memoria */
.audio-pill { position: fixed; right: 1.25rem; bottom: 1.25rem; z-index: 100; display: flex; align-items: center; background: rgba(38,38,38,0.92); border: 1px solid var(--rule); border-radius: 28px; box-shadow: 0 12px 36px -14px rgba(0,0,0,0.75), 0 2px 8px -2px rgba(0,0,0,0.25); font-family: var(--font-body); height: 48px; padding: 4px; overflow: hidden; -webkit-backdrop-filter: saturate(180%) blur(20px); backdrop-filter: saturate(180%) blur(20px); transition: width 0.32s cubic-bezier(0.4,0,0.2,1), background 0.2s, box-shadow 0.2s; width: 56px; }
.audio-pill[data-state="expanded"] { width: min(460px, calc(100vw - 2.5rem)); }
.audio-pill:hover { box-shadow: 0 16px 40px -12px rgba(0,0,0,0.85), 0 4px 10px -2px rgba(0,0,0,0.3); }
.ap-play { flex: 0 0 40px; height: 40px; border-radius: 50%; border: none; background: var(--verde); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; transition: background 0.2s, transform 0.1s; }
.ap-play:hover { background: #d96a14; transform: scale(1.04); }
.ap-play:active { transform: scale(0.96); }
.ap-play:focus-visible { outline: 2px solid var(--verde); outline-offset: 3px; }
.ap-play svg { width: 16px; height: 16px; fill: currentColor; pointer-events: none; }
.ap-icon-play { margin-left: 2px; }
.ap-meta { display: flex; align-items: center; gap: 0.35rem; margin-left: 0.4rem; margin-right: 0.2rem; flex: 1; min-width: 0; opacity: 0; transform: translateX(-4px); transition: opacity 0.18s 0.08s, transform 0.28s cubic-bezier(0.4,0,0.2,1); }
.audio-pill[data-state="expanded"] .ap-meta { opacity: 1; transform: translateX(0); }
.audio-pill[data-state="collapsed"] .ap-meta { pointer-events: none; }
.ap-btn { flex: 0 0 28px; height: 28px; border-radius: 50%; background: transparent; border: none; color: var(--ink-soft); cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; transition: background 0.2s, color 0.2s; }
.ap-btn:hover { background: var(--rule); color: var(--ink); }
.ap-btn:focus-visible { outline: 2px solid var(--verde); outline-offset: 2px; }
.ap-btn svg { width: 14px; height: 14px; pointer-events: none; }
.ap-btn.active { color: var(--verde); }
.ap-skip svg { fill: currentColor; stroke: none; }
.ap-skip .skip-label { font: 600 7px/1 ui-monospace, monospace; fill: currentColor; }
.ap-karaoke svg { fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.ap-karaoke .strike { display: none; }
body.karaoke-off .ap-karaoke .strike { display: block; }
.ap-track { flex: 1; min-width: 40px; height: 24px; position: relative; cursor: pointer; }
.ap-rail { position: absolute; top: 50%; left: 0; right: 0; height: 2px; background: var(--rule); transform: translateY(-50%); border-radius: 1px; }
.ap-fill { position: absolute; top: 50%; left: 0; height: 2px; width: 0; background: var(--verde); transform: translateY(-50%); border-radius: 1px; transition: width 0.1s linear; }
.ap-thumb { position: absolute; top: 50%; left: 0; width: 10px; height: 10px; border-radius: 50%; background: var(--verde); transform: translate(-50%,-50%); opacity: 0; transition: opacity 0.2s; }
.audio-pill:hover .ap-thumb, .ap-track:focus-visible .ap-thumb { opacity: 1; }
.ap-time { font-size: 0.78rem; color: var(--ink-soft); font-variant-numeric: tabular-nums; letter-spacing: 0.01em; white-space: nowrap; min-width: 34px; text-align: right; }
.audio-pill.playing .ap-time { color: var(--verde); }
.ap-rate { flex: 0 0 auto; background: transparent; border: 1px solid var(--rule); color: var(--ink-soft); border-radius: 12px; height: 24px; padding: 0 8px; font-size: 0.7rem; font-family: inherit; cursor: pointer; font-variant-numeric: tabular-nums; letter-spacing: 0.02em; white-space: nowrap; transition: color 0.2s, border-color 0.2s, background 0.2s; }
.ap-rate:hover { color: var(--ink); border-color: var(--ink-soft); }
.ap-rate:focus-visible { outline: 2px solid var(--verde); outline-offset: 2px; }
.ap-rate.active { color: var(--verde); border-color: var(--verde); }
.ap-close { flex: 0 0 26px; height: 26px; border-radius: 50%; background: transparent; border: none; color: var(--ink-soft); cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; transition: background 0.2s, color 0.2s; }
.ap-close:hover { background: var(--rule); color: var(--ink); }
.ap-close:focus-visible { outline: 2px solid var(--verde); outline-offset: 2px; }
.ap-close svg { width: 11px; height: 11px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; pointer-events: none; }
.audio-pill[data-state="collapsed"]::after { content: attr(data-duration); position: absolute; right: calc(100% + 10px); top: 50%; transform: translateY(-50%); background: var(--surface); border: 1px solid var(--rule); color: var(--ink-soft); padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.72rem; font-variant-numeric: tabular-nums; letter-spacing: 0.04em; white-space: nowrap; opacity: 0; pointer-events: none; transition: opacity 0.2s; }
.audio-pill[data-state="collapsed"]:hover::after, .audio-pill[data-state="collapsed"]:focus-within::after { opacity: 1; }
.ap-resume-hint { position: absolute; right: calc(100% + 10px); top: 50%; transform: translateY(-50%); background: var(--surface); border: 1px solid var(--verde); color: var(--verde); padding: 0.3rem 0.7rem; border-radius: 12px; font-size: 0.72rem; white-space: nowrap; opacity: 0; pointer-events: none; transition: opacity 0.3s; }
.ap-resume-hint.show { opacity: 1; }
@media (max-width: 640px) {
  .audio-pill { right: 0.85rem; bottom: 0.85rem; }
  .audio-pill[data-state="expanded"] { left: 0.85rem; right: 0.85rem; width: auto; }
  .audio-pill[data-state="collapsed"]::after { display: none; }
  .ap-karaoke { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .audio-pill, .ap-fill, .ap-play, .ap-meta { transition: none; }
}"""

# ────────────────────────────────────────────────────────────────
# HTML pill v2 (templates {src}, {duration}, {key})
# ────────────────────────────────────────────────────────────────
HTML_PILL_V2 = """\
<aside class="audio-pill" data-state="collapsed" data-duration="{duration}" data-storage-key="{key}" aria-label="Reproductor de audio del capítulo">
  <audio class="ap-audio" preload="metadata" src="{src}"></audio>
  <button class="ap-play" type="button" aria-label="Reproducir capítulo">
    <svg class="ap-icon-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
    <svg class="ap-icon-pause" viewBox="0 0 24 24" aria-hidden="true" style="display:none"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>
  </button>
  <div class="ap-resume-hint" aria-hidden="true"></div>
  <div class="ap-meta">
    <button class="ap-btn ap-skip ap-skip-back" type="button" aria-label="Retroceder 15 segundos" title="Retroceder 15 s (J)">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M11 6V3L6 7l5 4V8c3.3 0 6 2.7 6 6s-2.7 6-6 6-6-2.7-6-6H3c0 4.4 3.6 8 8 8s8-3.6 8-8-3.6-8-8-8z"/>
        <text class="skip-label" x="11" y="17" text-anchor="middle">15</text>
      </svg>
    </button>
    <button class="ap-btn ap-skip ap-skip-fwd" type="button" aria-label="Avanzar 15 segundos" title="Avanzar 15 s (L)">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M13 6V3l5 4-5 4V8c-3.3 0-6 2.7-6 6s2.7 6 6 6 6-2.7 6-6h2c0 4.4-3.6 8-8 8s-8-3.6-8-8 3.6-8 8-8z"/>
        <text class="skip-label" x="13" y="17" text-anchor="middle">15</text>
      </svg>
    </button>
    <div class="ap-track" role="slider" tabindex="0" aria-label="Posición del audio" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
      <div class="ap-rail"></div>
      <div class="ap-fill"></div>
      <div class="ap-thumb"></div>
    </div>
    <div class="ap-time"><span class="ap-current">0:00</span></div>
    <button class="ap-btn ap-karaoke" type="button" aria-label="Resaltado palabra por palabra (toggle)" title="Karaoke (K)">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 18 L8 7 L12 18 M5.5 14 L10.5 14"/>
        <path d="M19 18 V11.5 a3 3 0 0 0 -6 0 a3 3 0 0 0 3 3 a3 3 0 0 0 3 -3"/>
        <line class="strike" x1="3" y1="20" x2="21" y2="4"/>
      </svg>
    </button>
    <button class="ap-rate" type="button" aria-label="Velocidad de reproducción" title="Velocidad">1×</button>
    <button class="ap-close" type="button" aria-label="Minimizar reproductor" title="Minimizar (Esc)">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6 L18 18 M18 6 L6 18"/></svg>
    </button>
  </div>
</aside>"""

# ────────────────────────────────────────────────────────────────
# JS pill v2
# ────────────────────────────────────────────────────────────────
JS_PILL_V2 = """\
<script>
/* AUDIO PILL controller v2 */
(function(){
  var pill = document.querySelector('.audio-pill');
  if (!pill) return;
  var a = pill.querySelector('.ap-audio');
  var b = pill.querySelector('.ap-play');
  var pi = pill.querySelector('.ap-icon-play');
  var ps = pill.querySelector('.ap-icon-pause');
  var tr = pill.querySelector('.ap-track');
  var fi = pill.querySelector('.ap-fill');
  var th = pill.querySelector('.ap-thumb');
  var cu = pill.querySelector('.ap-current');
  var rateBtn = pill.querySelector('.ap-rate');
  var closeBtn = pill.querySelector('.ap-close');
  var skipBackBtn = pill.querySelector('.ap-skip-back');
  var skipFwdBtn  = pill.querySelector('.ap-skip-fwd');
  var karaokeBtn  = pill.querySelector('.ap-karaoke');
  var hint        = pill.querySelector('.ap-resume-hint');
  var STORAGE_KEY = pill.getAttribute('data-storage-key') || 'default';
  var POS_KEY = 'audio-pill:pos:' + STORAGE_KEY;
  var KARAOKE_KEY = 'audio-pill:karaoke';
  var RATES = [1, 1.25, 1.5, 0.8];
  var rateIdx = 0, lastSaveAt = 0;
  function fmt(t){ if(!isFinite(t)) return '0:00'; var m=Math.floor(t/60), s=Math.floor(t%60); return m+':'+(s<10?'0':'')+s; }
  function expand(){ pill.setAttribute('data-state','expanded'); }
  function collapse(){ pill.setAttribute('data-state','collapsed'); }
  function setPlayIcon(playing){
    if (playing) { pi.style.display='none'; ps.style.display=''; b.setAttribute('aria-label','Pausar'); }
    else         { pi.style.display=''; ps.style.display='none'; b.setAttribute('aria-label','Reproducir'); }
  }
  function safePlay(){
    var p = a.play();
    if (p && typeof p.catch === 'function') p.catch(function(){});
  }
  function savePos(){
    if (!a.duration || !isFinite(a.duration)) return;
    var t = a.currentTime;
    if (t > a.duration - 8) { try { localStorage.removeItem(POS_KEY); } catch(e){} return; }
    if (t < 3) return;
    try { localStorage.setItem(POS_KEY, String(Math.floor(t))); } catch(e){}
  }
  function loadPos(){
    try { var v = localStorage.getItem(POS_KEY); var t = parseFloat(v); return isFinite(t) && t > 0 ? t : 0; }
    catch(e){ return 0; }
  }
  function showResumeHint(s){
    if (!hint) return;
    hint.textContent = '↻ ' + fmt(s);
    hint.classList.add('show');
    setTimeout(function(){ hint.classList.remove('show'); }, 2200);
  }
  a.addEventListener('loadedmetadata', function(){
    if (isFinite(a.duration)) pill.setAttribute('data-duration', fmt(a.duration));
    var saved = loadPos();
    if (saved > 0 && saved < a.duration - 8) {
      a.currentTime = saved;
      showResumeHint(saved);
    }
  });
  a.addEventListener('timeupdate', function(){
    var pct = a.duration ? (a.currentTime/a.duration)*100 : 0;
    fi.style.width = pct+'%'; th.style.left = pct+'%';
    cu.textContent = fmt(a.currentTime);
    tr.setAttribute('aria-valuenow', Math.round(pct));
    if (!a.paused) {
      var now = (typeof performance !== 'undefined' && performance.now) ? performance.now() : 0;
      if (now - lastSaveAt > 3000) { savePos(); lastSaveAt = now; }
    }
  });
  a.addEventListener('pause', function(){ savePos(); });
  window.addEventListener('beforeunload', savePos);
  document.addEventListener('visibilitychange', function(){ if (document.hidden) savePos(); });
  a.addEventListener('play',  function(){ pill.classList.add('playing'); setPlayIcon(true); expand(); });
  a.addEventListener('pause', function(){ pill.classList.remove('playing'); setPlayIcon(false); });
  a.addEventListener('ended', function(){ pill.classList.remove('playing'); setPlayIcon(false); try { localStorage.removeItem(POS_KEY); } catch(e){} });
  b.addEventListener('click', function(e){ e.stopPropagation(); if (a.paused) safePlay(); else a.pause(); });
  closeBtn.addEventListener('click', function(e){ e.stopPropagation(); a.pause(); collapse(); });
  rateBtn.addEventListener('click', function(e){
    e.stopPropagation();
    rateIdx = (rateIdx+1) % RATES.length;
    var r = RATES[rateIdx];
    a.playbackRate = r;
    rateBtn.textContent = (r % 1 === 0 ? r.toFixed(0) : r) + '×';
    rateBtn.classList.toggle('active', r !== 1);
    rateBtn.setAttribute('aria-label', 'Velocidad: ' + rateBtn.textContent + '. Tocar para cambiar.');
  });
  function skip(secs){ if (!a.duration) return; a.currentTime = Math.max(0, Math.min(a.duration, a.currentTime + secs)); }
  if (skipBackBtn) skipBackBtn.addEventListener('click', function(e){ e.stopPropagation(); skip(-15); });
  if (skipFwdBtn)  skipFwdBtn.addEventListener('click',  function(e){ e.stopPropagation(); skip(+15); });
  function applyKaraokePref(){
    var off = false;
    try { off = localStorage.getItem(KARAOKE_KEY) === 'off'; } catch(e){}
    document.body.classList.toggle('karaoke-off', off);
    if (karaokeBtn) {
      karaokeBtn.classList.toggle('active', !off);
      karaokeBtn.setAttribute('aria-pressed', String(!off));
      karaokeBtn.setAttribute('aria-label', off ? 'Activar resaltado palabra por palabra' : 'Desactivar resaltado palabra por palabra');
    }
  }
  applyKaraokePref();
  if (karaokeBtn) karaokeBtn.addEventListener('click', function(e){
    e.stopPropagation();
    var current = document.body.classList.contains('karaoke-off');
    try { localStorage.setItem(KARAOKE_KEY, current ? 'on' : 'off'); } catch(e){}
    applyKaraokePref();
  });
  tr.addEventListener('click', function(e){
    if (!a.duration) return;
    var r = tr.getBoundingClientRect();
    var pct = Math.max(0, Math.min(1, (e.clientX-r.left)/r.width));
    a.currentTime = pct*a.duration;
  });
  tr.addEventListener('keydown', function(e){
    if (!a.duration) return;
    if      (e.key==='ArrowRight'){ a.currentTime = Math.min(a.duration, a.currentTime+5); e.preventDefault(); }
    else if (e.key==='ArrowLeft') { a.currentTime = Math.max(0, a.currentTime-5);          e.preventDefault(); }
  });
  document.addEventListener('keydown', function(e){
    if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    if (e.target && e.target.isContentEditable) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key.toLowerCase();
    if (k === ' ' && !(/^(BUTTON|A)$/.test(e.target.tagName))) {
      if (!pill.contains(document.activeElement)) return;
      e.preventDefault();
      if (a.paused) safePlay(); else a.pause();
    } else if (k === 'j') { skip(-15); e.preventDefault(); }
      else if (k === 'l') { skip(+15); e.preventDefault(); }
      else if (k === 'k' && karaokeBtn) { karaokeBtn.click(); e.preventDefault(); }
      else if (e.key === 'Escape' && pill.getAttribute('data-state') === 'expanded') { a.pause(); collapse(); }
  });
})();
</script>"""

# ────────────────────────────────────────────────────────────────
# JS karaoke v2 (template {align_url})
# ────────────────────────────────────────────────────────────────
JS_KARAOKE_V2 = """\
<script>
/* Karaoke v2: carga alignment y resalta palabra + puntuación. Respeta body.karaoke-off. */
(function(){
  var ALIGN_URL = '{align_url}';
  var audio = document.querySelector('.ap-audio');
  if (!audio) return;
  var words = null, wordEls = [], glueEls = [], lastIdx = -1, lastScrollAt = 0;
  document.querySelectorAll('.w').forEach(function(el){
    var i = parseInt(el.getAttribute('data-w'), 10);
    if (!isNaN(i)) wordEls[i] = el;
  });
  try {
    var allW = document.querySelectorAll('.w');
    var rootEls = [];
    allW.forEach(function(w){
      var p = w.parentNode;
      while (p && p !== document.body && !/^(P|H1|H2|H3|DIV|LI|BLOCKQUOTE)$/.test(p.tagName)) p = p.parentNode;
      if (p && rootEls.indexOf(p) < 0) rootEls.push(p);
    });
    rootEls.forEach(function(root){
      var walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, null);
      var seq = [], n;
      while ((n = walker.nextNode())) {
        if (n.nodeType === 3) { if (n.textContent) seq.push(n); }
        else if (n.nodeType === 1 && n.classList && n.classList.contains('w')) seq.push(n);
      }
      var currentIdx = -1;
      seq.forEach(function(node){
        if (node.nodeType === 1) {
          var i = parseInt(node.getAttribute('data-w'), 10);
          if (!isNaN(i)) currentIdx = i;
        } else if (node.nodeType === 3 && currentIdx >= 0 && node.parentNode) {
          var g = document.createElement('span');
          g.className = 'g';
          g.textContent = node.textContent;
          node.parentNode.replaceChild(g, node);
          if (!glueEls[currentIdx]) glueEls[currentIdx] = [];
          glueEls[currentIdx].push(g);
        }
      });
    });
  } catch (err) { /* el karaoke base sigue funcionando sin glue */ }
  fetch(ALIGN_URL)
    .then(function(r){ return r.ok ? r.json() : null; })
    .then(function(data){
      if (!data || !data.words) return;
      words = data.words;
      audio.addEventListener('timeupdate', tick);
      audio.addEventListener('seeked', function(){ resetState(); tick(); });
    })
    .catch(function(){});
  function findIdx(t){
    if (!words || !words.length) return -1;
    var lo = 0, hi = words.length - 1, ans = -1;
    while (lo <= hi) { var mid = (lo + hi) >> 1; if (words[mid].s <= t) { ans = mid; lo = mid + 1; } else { hi = mid - 1; } }
    return ans;
  }
  function setGlue(i, add){
    var arr = glueEls[i]; if (!arr) return;
    for (var k = 0; k < arr.length; k++) arr[k].classList[add ? 'add' : 'remove']('leida');
  }
  function resetState(){
    for (var k = 0; k < wordEls.length; k++) {
      if (wordEls[k]) wordEls[k].classList.remove('activa','leida');
      setGlue(k, false);
    }
    lastIdx = -1;
  }
  function tick(){
    if (!words) return;
    var idx = findIdx(audio.currentTime);
    if (idx === lastIdx) return;
    if (idx < lastIdx) {
      for (var i = idx + 1; i <= lastIdx; i++) {
        if (wordEls[i]) wordEls[i].classList.remove('leida','activa');
        setGlue(i, false);
      }
    } else {
      for (var j = Math.max(0, lastIdx); j < idx; j++) {
        if (wordEls[j]) { wordEls[j].classList.remove('activa'); wordEls[j].classList.add('leida'); }
        setGlue(j, true);
      }
    }
    if (idx >= 0 && wordEls[idx]) {
      wordEls[idx].classList.remove('leida');
      wordEls[idx].classList.add('activa');
      var rect = wordEls[idx].getBoundingClientRect();
      var vh = window.innerHeight;
      if (rect.top < vh*0.22 || rect.bottom > vh*0.72) {
        var now = (typeof performance !== 'undefined' && performance.now) ? performance.now() : 0;
        if (now - lastScrollAt > 600) {
          wordEls[idx].scrollIntoView({behavior:'smooth', block:'center'});
          lastScrollAt = now;
        }
      }
    }
    lastIdx = idx;
  }
  document.addEventListener('click', function(e){
    var t = e.target;
    if (!(t && t.classList && t.classList.contains('w'))) return;
    var i = parseInt(t.getAttribute('data-w'), 10);
    if (isNaN(i) || !words || !words[i]) return;
    audio.currentTime = words[i].s;
    if (audio.paused) { var p = audio.play(); if (p && typeof p.catch === 'function') p.catch(function(){}); }
  });
})();
</script>"""

# ────────────────────────────────────────────────────────────────
# Patrones de los bloques v1 a reemplazar
# ────────────────────────────────────────────────────────────────

# 1. CSS karaoke v1: desde `.w {` hasta `.w.activa {…}` (capturando reglas .w… intermedias)
RE_CSS_KARAOKE_V1 = re.compile(
    r"\.w \{[\s\S]*?\.w\.activa \{[^}]*\}"
)

# 2. CSS pill v1 (desde "/* AUDIO PILL" hasta inmediatamente antes de "</style>")
RE_CSS_PILL_V1 = re.compile(
    r"/\* AUDIO PILL [\s\S]*?(?=</style>)"
)

# 3. HTML pill v1
RE_HTML_PILL_V1 = re.compile(
    r'<aside class="audio-pill"[\s\S]*?</aside>'
)

# 4. JS pill v1
RE_JS_PILL_V1 = re.compile(
    r"<script>\s*/\* AUDIO PILL controller \*/[\s\S]*?\}\)\(\);\s*</script>"
)

# 5. JS karaoke v1
RE_JS_KARAOKE_V1 = re.compile(
    r"<script>\s*/\* Karaoke[\s\S]*?\}\)\(\);\s*</script>"
)


def upgrade(html_path: Path, audio_src: str, duration: str, storage_key: str):
    html = html_path.read_text(encoding="utf-8")

    # Detectar si ya está v2 — buscar marcador único v2
    if "AUDIO PILL controller v2" in html or "Karaoke v2" in html:
        print(f"[skip] {html_path.name}: ya está en v2")
        return

    # Sanity: que esté en v1
    missing = []
    for label, rx in [
        ("CSS karaoke", RE_CSS_KARAOKE_V1),
        ("CSS pill", RE_CSS_PILL_V1),
        ("HTML pill", RE_HTML_PILL_V1),
        ("JS pill", RE_JS_PILL_V1),
        ("JS karaoke", RE_JS_KARAOKE_V1),
    ]:
        if not rx.search(html):
            missing.append(label)
    if missing:
        raise RuntimeError(f"{html_path.name}: falta(n) bloque(s) v1: {missing}")

    align_url = audio_src.rsplit(".mp3", 1)[0] + ".alignment.json"

    # Reemplazos en orden inverso de tamaño (para mantener regex válidos)
    html = RE_JS_KARAOKE_V1.sub(JS_KARAOKE_V2.replace("{align_url}", align_url), html, count=1)
    html = RE_JS_PILL_V1.sub(JS_PILL_V2, html, count=1)
    html = RE_HTML_PILL_V1.sub(
        HTML_PILL_V2.format(src=audio_src, duration=duration, key=storage_key),
        html, count=1,
    )
    html = RE_CSS_PILL_V1.sub(CSS_PILL_V2 + "\n", html, count=1)
    html = RE_CSS_KARAOKE_V1.sub(CSS_KARAOKE_V2, html, count=1)

    html_path.write_text(html, encoding="utf-8")
    print(f"[OK]  {html_path.name}: migrado a v2")


def main():
    if len(sys.argv) != 5:
        raise SystemExit("uso: upgrade_audio_pill_v2.py <html> <audio_src> <duration> <storage_key>")
    upgrade(Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    main()
