#!/usr/bin/env python3
"""
Toma el cap 1 actual y lo transforma al estilo Audio First:
  - inyecta el CSS del hero, waveform, tabs y mini-bar
  - inserta el hero player justo después de <body class="mode-both">
  - oculta el nav-top original y la pill flotante (siguen existiendo
    para que el JS de karaoke/audio funcione)
  - agrega un mini-bar sticky al final con su propio JS de sync
  - conecta el botón gigante del hero al .ap-play de la pill original
"""
import re
from pathlib import Path

SRC = Path("../dinero-como-informacion.html")
DST = Path("cap1-audio-first.html")

src = SRC.read_text(encoding="utf-8")

# CSS adicional, antes de </style>
EXTRA_CSS = """
/* ===== Audio First — hero, tabs, waveform, mini-bar ===== */
.hero-player {
  background: linear-gradient(180deg, #161618 0%, var(--bg) 100%);
  border-bottom: 1px solid var(--rule);
  padding: 4rem 2rem 3rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.hero-player::before {
  content: ""; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%,-50%);
  width: 700px; height: 700px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,122,24,0.18) 0%, transparent 60%);
  z-index: 0; pointer-events: none;
}
.hero-player > * { position: relative; z-index: 1; }
.hero-player .ch-num {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.78rem; letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--verde); margin-bottom: 1.4rem;
}
.hero-player .ch-title {
  font-size: 2.6rem; line-height: 1.12; letter-spacing: -0.02em;
  font-weight: 400; margin: 0 auto 0.7rem; max-width: 30rem; color: var(--ink);
}
.hero-player .ch-sub {
  font-style: italic; color: var(--ink-soft);
  font-size: 1.06rem; margin: 0 auto 2.5rem; max-width: 30rem;
}
.big-play {
  width: 84px; height: 84px; border-radius: 50%;
  background: var(--verde); border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1.2rem;
  box-shadow: 0 12px 36px -10px rgba(255,122,24,0.6);
  transition: transform 0.15s, box-shadow 0.15s;
}
.big-play:hover {
  transform: scale(1.05);
  box-shadow: 0 18px 44px -10px rgba(255,122,24,0.75);
}
.big-play svg { width: 26px; height: 26px; fill: white; margin-left: 3px; }
.big-play.playing svg.play-icon { display: none; }
.big-play.playing svg.pause-icon { display: block; margin-left: 0; }
.big-play svg.pause-icon { display: none; }
.audio-meta {
  display: flex; justify-content: center; gap: 2rem; align-items: center;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.84rem; color: var(--ink-soft); letter-spacing: 0.02em;
}
.audio-meta .narrator { color: var(--ink); }
.audio-meta .dur { font-variant-numeric: tabular-nums; }
.audio-meta #heroCur { transition: color 0.2s ease; }
body.audio-playing .audio-meta #heroCur { color: var(--verde); }
.audio-meta .speed {
  padding: 0.3rem 0.7rem; border: 1px solid var(--rule);
  border-radius: 12px; cursor: pointer; user-select: none;
}
.waveform {
  display: flex; gap: 2px; justify-content: center; align-items: end;
  height: 36px; margin: 2rem auto 0; max-width: 480px; padding: 0 1rem;
}
.waveform { cursor: pointer; }
.waveform.dragging { cursor: grabbing; }
.waveform span {
  flex: 1; background: #5e5a57; border-radius: 1px; min-width: 2px;
  transition: background 0.15s, height 0.2s;
  pointer-events: none;
}
.waveform:hover span { background: #7a7672; }
.waveform.dragging span { transition: none; }
.waveform span.played { background: var(--verde) !important; }
.waveform span.current {
  background: var(--verde) !important;
  box-shadow: 0 0 8px var(--verde);
}

/* Tabs de modo */
.reader-toggle {
  display: flex; justify-content: center; gap: 0.5rem;
  padding: 1.5rem; border-bottom: 1px solid var(--rule);
  background: var(--bg);
}
.reader-toggle button {
  background: transparent; border: 1px solid var(--rule); color: var(--ink-soft);
  padding: 0.55rem 1.4rem; border-radius: 22px; cursor: pointer;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.83rem; letter-spacing: 0.05em;
  transition: all 0.15s;
}
.reader-toggle button.active {
  background: var(--ink); color: var(--bg); border-color: var(--ink);
}
.reader-toggle button:not(.active):hover {
  color: var(--ink); border-color: var(--ink-soft);
}

/* Cuando el modo es "audio-only", ocultar el prose */
body.mode-audio-only .page .prose,
body.mode-audio-only .page .ornament,
body.mode-audio-only .page .chapter-eyebrow,
body.mode-audio-only .page .chapter-title,
body.mode-audio-only .page .chapter-subtitle {
  display: none;
}

/* Cuando el modo es solo lectura, ocultar partes del audio */
body.mode-read-only .hero-player .waveform,
body.mode-read-only .hero-player .audio-meta { display: none; }

/* Ocultar la pill flotante original y el nav-top (los reemplaza el hero + mini-bar) */
.audio-pill { display: none !important; }
.nav-top { display: none !important; }

/* Quitar el chapter-eyebrow + title + subtitle del article (ya están en el hero) */
.page .chapter-eyebrow,
.page .chapter-title,
.page .chapter-subtitle,
.page > .ornament:first-of-type { display: none; }

/* Mini-bar abajo */
.mini-bar {
  position: fixed; bottom: 0; left: 0; right: 0; height: 70px;
  background: rgba(14,14,16,0.96);
  -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px);
  border-top: 1px solid var(--rule);
  display: flex; align-items: center; gap: 1rem; padding: 0 1.5rem;
  z-index: 50; opacity: 0; transform: translateY(100%);
  transition: opacity 0.3s, transform 0.3s;
}
.mini-bar.show { opacity: 1; transform: translateY(0); }
.mini-bar .mb-play {
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--verde); border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.mini-bar .mb-play svg { width: 14px; height: 14px; fill: white; }
.mini-bar .mb-play.playing svg.play-icon { display: none; }
.mini-bar .mb-play.playing svg.pause-icon { display: block; }
.mini-bar .mb-play svg.pause-icon { display: none; }
.mini-bar .mb-info { flex: 1; font-family: 'Inter', system-ui, sans-serif; min-width: 0; }
.mini-bar .mb-info .mb-title { font-size: 0.86rem; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mini-bar .mb-info .mb-meta { font-size: 0.74rem; color: var(--ink-soft); letter-spacing: 0.02em; }
.mini-bar .mb-progress {
  flex: 1; height: 4px; background: var(--rule); border-radius: 2px;
  max-width: 320px; cursor: pointer; position: relative;
}
/* área de toque invisible más grande (12px arriba y abajo) para agarrar fácil */
.mini-bar .mb-progress::after {
  content: ""; position: absolute; left: 0; right: 0; top: -12px; bottom: -12px;
}
.mini-bar .mb-progress.dragging { cursor: grabbing; }
.mini-bar .mb-progress-fill {
  height: 100%; width: 0%; background: var(--verde); border-radius: 2px;
  position: relative; pointer-events: none;
}
.mini-bar .mb-progress-fill::after {
  content: ""; position: absolute; right: -6px; top: 50%;
  width: 12px; height: 12px; border-radius: 50%; background: var(--verde);
  transform: translateY(-50%) scale(0.6); opacity: 0;
  transition: opacity 0.15s, transform 0.15s; pointer-events: none;
}
.mini-bar:hover .mb-progress-fill::after,
.mini-bar .mb-progress.dragging .mb-progress-fill::after {
  opacity: 1; transform: translateY(-50%) scale(1);
}
.mini-bar .mb-time {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.78rem; color: var(--ink-soft);
  font-variant-numeric: tabular-nums; min-width: 100px; text-align: right; flex-shrink: 0;
}

/* Más aire para la pagina porque ya no hay nav-top y el hero ocupa */
.page { padding-top: 2rem !important; padding-bottom: 9rem !important; }

/* ===== Píldoras de modo: barra fija arriba ===== */
.reader-toggle {
  position: fixed; top: 0; left: 0; right: 0; z-index: 95;
  padding: 0.7rem 1rem; border-bottom: 1px solid var(--rule);
  background: rgba(14,14,16,0.9);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
}
.reader-toggle button { padding: 0.45rem 1.1rem; font-size: 0.78rem; }
/* el hero baja para no quedar tapado por la barra fija */
.hero-player { padding-top: 4.5rem; }

/* ===== Hero adaptativo según el modo ===== */
/* LEER + AUDIO (default): hero compacto, el texto asoma pronto */
body.mode-both .hero-player { padding-bottom: 2rem; }
body.mode-both .hero-player::before { width: 440px; height: 440px; }
body.mode-both .hero-player .ch-title { font-size: 2rem; margin-bottom: 0.5rem; }
body.mode-both .hero-player .ch-sub { font-size: 1.02rem; margin-bottom: 1.4rem; }
body.mode-both .big-play { width: 58px; height: 58px; margin-bottom: 0.8rem; }
body.mode-both .big-play svg { width: 19px; height: 19px; }
body.mode-both .waveform { height: 28px; margin-top: 1.1rem; }

/* SOLO ESCUCHAR: hero protagonista, centrado y alto (el texto está oculto) */
body.mode-audio-only .hero-player {
  min-height: calc(100vh - 52px);
  display: flex; flex-direction: column; justify-content: center;
}

/* SOLO LEER: sin controles de audio, el texto manda */
body.mode-read-only .hero-player .big-play,
body.mode-read-only .hero-player .audio-meta,
body.mode-read-only .hero-player .waveform { display: none; }
body.mode-read-only .hero-player::before { display: none; }
body.mode-read-only .hero-player { padding-top: 4.8rem; padding-bottom: 1.5rem; }

/* ===== Responsive móvil — Audio First compacto ===== */
@media (max-width: 640px) {
  .hero-player { padding: 3.6rem 1.1rem 1.4rem; }
  .reader-toggle { padding: 0.6rem 0.6rem; }
  .hero-player::before { width: 420px; height: 420px; }
  .hero-player .ch-num { font-size: 0.68rem; letter-spacing: 0.18em; margin-bottom: 0.9rem; }
  .hero-player .ch-title { font-size: 1.85rem; line-height: 1.12; margin-bottom: 0.5rem; }
  .hero-player .ch-sub { font-size: 0.98rem; margin-bottom: 1.4rem; }
  .big-play { width: 62px; height: 62px; margin-bottom: 1rem; }
  .big-play svg { width: 20px; height: 20px; }
  .audio-meta { gap: 0.9rem; font-size: 0.78rem; flex-wrap: wrap; row-gap: 0.5rem; }
  .audio-meta > span:first-child { flex-basis: 100%; text-align: center; }
  .waveform { height: 28px; margin-top: 1.2rem; max-width: 100%; }
  .reader-toggle { padding: 0.9rem 0.6rem; gap: 0.35rem; }
  .reader-toggle button { padding: 0.55rem 0.5rem; font-size: 0.7rem; letter-spacing: 0.01em; flex: 1; text-align: center; white-space: nowrap; }
  .mini-bar { gap: 0.7rem; padding: 0 0.9rem; }
  .mini-bar .mb-info { display: none; }
  .mini-bar .mb-progress { max-width: none; }
  .mini-bar .mb-time { min-width: 84px; font-size: 0.74rem; }
}
"""

src = src.replace("</style>", EXTRA_CSS + "\n</style>")

# HTML: insertar el hero JUSTO antes del <article class="page">
HERO_HTML = """
<section class="hero-player">
  <div class="ch-num">Capítulo 1 · Bloque I</div>
  <h1 class="ch-title">El dinero como sistema que transmite información</h1>
  <p class="ch-sub">Por qué una ciudad se alimenta cada mañana sin que nadie lo ordene</p>

  <button class="big-play" id="bigPlay" aria-label="Reproducir capítulo">
    <svg class="play-icon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
    <svg class="pause-icon" viewBox="0 0 24 24"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>
  </button>

  <div class="audio-meta">
    <span>Escrito por <span class="narrator">Juan Camilo Álvarez Ramírez</span></span>
    <span class="dur"><span id="heroCur">0:00</span> / <span id="heroDur">14:20</span></span>
    <span class="speed" id="heroSpeed">1×</span>
  </div>

  <div class="waveform" id="waveform"></div>
</section>

<div class="reader-toggle">
  <button data-mode="both" class="active">Leer + audio</button>
  <button data-mode="audio-only">Solo escuchar</button>
  <button data-mode="read-only">Solo leer</button>
</div>

"""
src = src.replace('<article class="page">', HERO_HTML + '<article class="page">', 1)

# HTML: insertar el mini-bar justo antes del primer <script>
MINI_BAR_HTML = """
<div class="mini-bar" id="miniBar">
  <button class="mb-play" id="mbPlay" aria-label="Reproducir/Pausar">
    <svg class="play-icon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
    <svg class="pause-icon" viewBox="0 0 24 24"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>
  </button>
  <div class="mb-info">
    <div class="mb-title">El dinero como sistema que transmite información</div>
  </div>
  <div class="mb-progress" id="mbProgress">
    <div class="mb-progress-fill" id="mbFill"></div>
  </div>
  <div class="mb-time"><span id="mbCur">0:00</span> / <span id="mbDur">14:20</span></div>
</div>

<script>
/* Audio First — conecta el hero player + mini-bar + tabs con el audio existente */
document.addEventListener('DOMContentLoaded', function(){
  var audio = document.querySelector('.ap-audio');
  if (!audio) return;

  var bigPlay = document.getElementById('bigPlay');
  var heroDur = document.getElementById('heroDur');
  var heroCur = document.getElementById('heroCur');
  var waveform = document.getElementById('waveform');
  var miniBar = document.getElementById('miniBar');
  var heroSpeed = document.getElementById('heroSpeed');

  // Velocidad de reproducción: ciclo 1× → 1.25× → 1.5× → 2× → 1×
  var SPEEDS = [1, 1.25, 1.5, 2];
  var SPEED_KEY = 'audio-speed:dinero-como-informacion';
  function applySpeed(rate){
    audio.playbackRate = rate;
    if (heroSpeed) heroSpeed.textContent = (rate % 1 === 0 ? rate.toFixed(0) : rate.toString()) + '×';
    try { localStorage.setItem(SPEED_KEY, String(rate)); } catch(e){}
  }
  // Cargar velocidad guardada (o 1× por defecto)
  var savedSpeed = 1;
  try {
    var s = parseFloat(localStorage.getItem(SPEED_KEY));
    if (!isNaN(s) && SPEEDS.indexOf(s) !== -1) savedSpeed = s;
  } catch(e){}
  applySpeed(savedSpeed);

  if (heroSpeed) heroSpeed.addEventListener('click', function(){
    var cur = audio.playbackRate;
    var idx = SPEEDS.indexOf(cur);
    if (idx === -1) idx = 0;
    var next = SPEEDS[(idx + 1) % SPEEDS.length];
    applySpeed(next);
  });
  var mbPlay = document.getElementById('mbPlay');
  var mbFill = document.getElementById('mbFill');
  var mbCur = document.getElementById('mbCur');
  var mbDur = document.getElementById('mbDur');
  var mbProgress = document.getElementById('mbProgress');
  var heroPlayer = document.querySelector('.hero-player');

  // Construir 40 barras de waveform decorativo (alturas pseudoaleatorias)
  for (var i = 0; i < 40; i++) {
    var h = 30 + ((i * 37) % 60); // 30-90%
    var s = document.createElement('span');
    s.style.height = h + '%';
    waveform.appendChild(s);
  }
  var bars = waveform.querySelectorAll('span');

  // Click + drag sobre el waveform para saltar el audio (como Soundcloud)
  var wfDragging = false, wfWasPlaying = false;
  function wfSeek(clientX){
    if (!audio.duration) return;
    var r = waveform.getBoundingClientRect();
    var pct = Math.max(0, Math.min(1, (clientX - r.left) / r.width));
    audio.currentTime = pct * audio.duration;
  }
  function wfDown(e){
    if (!audio.duration) return;
    wfDragging = true;
    wfWasPlaying = !audio.paused;
    if (wfWasPlaying) audio.pause();
    waveform.classList.add('dragging');
    var x = (e.touches && e.touches[0]) ? e.touches[0].clientX : e.clientX;
    wfSeek(x);
    e.preventDefault();
  }
  function wfMove(e){
    if (!wfDragging) return;
    var x = (e.touches && e.touches[0]) ? e.touches[0].clientX : e.clientX;
    wfSeek(x);
    e.preventDefault();
  }
  function wfUp(){
    if (!wfDragging) return;
    wfDragging = false;
    waveform.classList.remove('dragging');
    if (wfWasPlaying) { var p = audio.play(); if (p && typeof p.catch === 'function') p.catch(function(){}); }
  }
  waveform.addEventListener('mousedown', wfDown);
  waveform.addEventListener('touchstart', wfDown, { passive: false });
  window.addEventListener('mousemove', wfMove);
  window.addEventListener('touchmove', wfMove, { passive: false });
  window.addEventListener('mouseup', wfUp);
  window.addEventListener('touchend', wfUp);
  window.addEventListener('touchcancel', wfUp);


  function fmt(t){
    if (!isFinite(t)) return '--:--';
    var m = Math.floor(t / 60), s = Math.floor(t % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function togglePlay(){
    if (audio.paused) {
      var p = audio.play();
      if (p && typeof p.catch === 'function') p.catch(function(){});
    } else {
      audio.pause();
    }
  }

  bigPlay.addEventListener('click', togglePlay);
  mbPlay.addEventListener('click', togglePlay);

  audio.addEventListener('play', function(){
    bigPlay.classList.add('playing');
    mbPlay.classList.add('playing');
    document.body.classList.add('audio-playing');
  });
  audio.addEventListener('pause', function(){
    bigPlay.classList.remove('playing');
    mbPlay.classList.remove('playing');
    document.body.classList.remove('audio-playing');
  });

  audio.addEventListener('loadedmetadata', function(){
    var d = fmt(audio.duration);
    heroDur.textContent = d;
    mbDur.textContent = d;
  });

  audio.addEventListener('timeupdate', function(){
    if (!audio.duration) return;
    var pct = audio.currentTime / audio.duration;
    mbFill.style.width = (pct * 100) + '%';
    var curStr = fmt(audio.currentTime);
    mbCur.textContent = curStr;
    if (heroCur) heroCur.textContent = curStr;

    // Pintar waveform: barras "leídas" en naranja
    var n = bars.length;
    var idx = Math.floor(pct * n);
    for (var i = 0; i < n; i++) {
      bars[i].classList.toggle('played', i < idx);
      bars[i].classList.toggle('current', i === idx);
    }
  });

  // mb-progress: click + drag para saltar/scrubbing (mouse + touch)
  (function(){
    var dragging = false, wasPlaying = false;
    function seekAt(clientX){
      if (!audio.duration) return;
      var r = mbProgress.getBoundingClientRect();
      var pct = Math.max(0, Math.min(1, (clientX - r.left) / r.width));
      audio.currentTime = pct * audio.duration;
    }
    function down(e){
      if (!audio.duration) return;
      dragging = true; wasPlaying = !audio.paused;
      if (wasPlaying) audio.pause();
      mbProgress.classList.add('dragging');
      var x = (e.touches && e.touches[0]) ? e.touches[0].clientX : e.clientX;
      seekAt(x); e.preventDefault();
    }
    function move(e){
      if (!dragging) return;
      var x = (e.touches && e.touches[0]) ? e.touches[0].clientX : e.clientX;
      seekAt(x); e.preventDefault();
    }
    function up(){
      if (!dragging) return;
      dragging = false; mbProgress.classList.remove('dragging');
      if (wasPlaying) { var pr = audio.play(); if (pr && typeof pr.catch === 'function') pr.catch(function(){}); }
    }
    mbProgress.addEventListener('mousedown', down);
    mbProgress.addEventListener('touchstart', down, { passive: false });
    window.addEventListener('mousemove', move);
    window.addEventListener('touchmove', move, { passive: false });
    window.addEventListener('mouseup', up);
    window.addEventListener('touchend', up);
  })();

  // Mini-bar visible si: el audio está sonando (control persistente desde el
  // inicio) O el hero ya salió de viewport (navegación mientras lees).
  function updateMiniBar(){
    var heroOut = heroPlayer.getBoundingClientRect().bottom < 60;
    var playing = !audio.paused && !audio.ended;
    if (heroOut || playing) miniBar.classList.add('show');
    else miniBar.classList.remove('show');
  }
  window.addEventListener('scroll', updateMiniBar, { passive: true });
  audio.addEventListener('play', updateMiniBar);
  audio.addEventListener('pause', updateMiniBar);
  audio.addEventListener('ended', updateMiniBar);
  updateMiniBar();

  // Tabs de modo
  document.querySelectorAll('.reader-toggle button').forEach(function(btn){
    btn.addEventListener('click', function(){
      document.querySelectorAll('.reader-toggle button').forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      document.body.classList.remove('mode-audio-only', 'mode-read-only', 'mode-both');
      document.body.classList.add('mode-' + btn.dataset.mode);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
});
</script>

"""

# Lo inyectamos justo antes del primer <script> del archivo original (línea ~242 aprox)
# pero más seguro: justo antes del PRIMER script que ya está en el body.
# Vamos a inyectarlo justo después del </article> de nuestro article.
src = src.replace('</article>\n', '</article>\n' + MINI_BAR_HTML, 1)

DST.write_text(src, encoding="utf-8")
print(f"OK → {DST}")
print(f"Tamaño: {len(src)} chars")
