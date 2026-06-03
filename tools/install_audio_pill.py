#!/usr/bin/env python3
"""Instala (o migra) el componente AUDIO PILL en un capítulo HTML.

Es idempotente: si el HTML ya tiene <aside class="audio-pill">, no hace nada.

Casos cubiertos:
  A. HTML con el player viejo (<aside class="audio-player">):
     reemplaza CSS, HTML y JS por la nueva pill.
  B. HTML sin player (e.g. tres-regimenes después del splice): inyecta
     CSS al final del <style>, HTML al final del <body>, JS al final del <body>.

Uso:
  install_audio_pill.py <capitulo.html> <audio_src> <duration HH:MM>
  install_audio_pill.py tres-regimenes.html audio/tres-regimenes.mp3 29:20
"""
import re
import sys
from pathlib import Path


# ────────────────────────────────────────────────────────────────
# Bloque CSS nuevo (se inserta dentro del <style> existente)
# ────────────────────────────────────────────────────────────────
CSS_NEW = """\
/* AUDIO PILL — reproductor flotante, colapsa/expande */
.audio-pill { position: fixed; right: 1.25rem; bottom: 1.25rem; z-index: 100; display: flex; align-items: center; background: rgba(38,38,38,0.92); border: 1px solid var(--rule); border-radius: 28px; box-shadow: 0 12px 36px -14px rgba(0,0,0,0.75), 0 2px 8px -2px rgba(0,0,0,0.25); font-family: var(--font-body); height: 48px; padding: 4px; overflow: hidden; -webkit-backdrop-filter: saturate(180%) blur(20px); backdrop-filter: saturate(180%) blur(20px); transition: width 0.32s cubic-bezier(0.4,0,0.2,1), background 0.2s, box-shadow 0.2s; width: 56px; }
.audio-pill[data-state="expanded"] { width: min(420px, calc(100vw - 2.5rem)); }
.audio-pill:hover { box-shadow: 0 16px 40px -12px rgba(0,0,0,0.85), 0 4px 10px -2px rgba(0,0,0,0.3); }
.ap-play { flex: 0 0 40px; height: 40px; border-radius: 50%; border: none; background: var(--verde); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; transition: background 0.2s, transform 0.1s; }
.ap-play:hover { background: #d96a14; transform: scale(1.04); }
.ap-play:active { transform: scale(0.96); }
.ap-play:focus-visible { outline: 2px solid var(--verde); outline-offset: 3px; }
.ap-play svg { width: 16px; height: 16px; fill: currentColor; pointer-events: none; }
.ap-icon-play { margin-left: 2px; }
.ap-meta { display: flex; align-items: center; gap: 0.55rem; margin-left: 0.65rem; margin-right: 0.25rem; flex: 1; min-width: 0; opacity: 0; transform: translateX(-4px); transition: opacity 0.18s 0.08s, transform 0.28s cubic-bezier(0.4,0,0.2,1); }
.audio-pill[data-state="expanded"] .ap-meta { opacity: 1; transform: translateX(0); }
.audio-pill[data-state="collapsed"] .ap-meta { pointer-events: none; }
.ap-track { flex: 1; min-width: 0; height: 24px; position: relative; cursor: pointer; }
.ap-rail { position: absolute; top: 50%; left: 0; right: 0; height: 2px; background: var(--rule); transform: translateY(-50%); border-radius: 1px; }
.ap-fill { position: absolute; top: 50%; left: 0; height: 2px; width: 0; background: var(--verde); transform: translateY(-50%); border-radius: 1px; transition: width 0.1s linear; }
.ap-thumb { position: absolute; top: 50%; left: 0; width: 10px; height: 10px; border-radius: 50%; background: var(--verde); transform: translate(-50%,-50%); opacity: 0; transition: opacity 0.2s; }
.audio-pill:hover .ap-thumb, .ap-track:focus-visible .ap-thumb { opacity: 1; }
.ap-time { font-size: 0.78rem; color: var(--ink-soft); font-variant-numeric: tabular-nums; letter-spacing: 0.01em; white-space: nowrap; min-width: 36px; text-align: right; }
.audio-pill.playing .ap-time { color: var(--verde); }
.ap-rate { flex: 0 0 auto; background: transparent; border: 1px solid var(--rule); color: var(--ink-soft); border-radius: 12px; height: 24px; padding: 0 9px; font-size: 0.72rem; font-family: inherit; cursor: pointer; font-variant-numeric: tabular-nums; letter-spacing: 0.02em; white-space: nowrap; transition: color 0.2s, border-color 0.2s, background 0.2s; }
.ap-rate:hover { color: var(--ink); border-color: var(--ink-soft); }
.ap-rate:focus-visible { outline: 2px solid var(--verde); outline-offset: 2px; }
.ap-rate.active { color: var(--verde); border-color: var(--verde); }
.ap-close { flex: 0 0 28px; height: 28px; border-radius: 50%; background: transparent; border: none; color: var(--ink-soft); cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; transition: background 0.2s, color 0.2s; }
.ap-close:hover { background: var(--rule); color: var(--ink); }
.ap-close:focus-visible { outline: 2px solid var(--verde); outline-offset: 2px; }
.ap-close svg { width: 12px; height: 12px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; pointer-events: none; }
.audio-pill[data-state="collapsed"]::after { content: attr(data-duration); position: absolute; right: calc(100% + 10px); top: 50%; transform: translateY(-50%); background: var(--surface); border: 1px solid var(--rule); color: var(--ink-soft); padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.72rem; font-variant-numeric: tabular-nums; letter-spacing: 0.04em; white-space: nowrap; opacity: 0; pointer-events: none; transition: opacity 0.2s; }
.audio-pill[data-state="collapsed"]:hover::after, .audio-pill[data-state="collapsed"]:focus-within::after { opacity: 1; }
@media (max-width: 640px) {
  .audio-pill { right: 0.85rem; bottom: 0.85rem; }
  .audio-pill[data-state="expanded"] { left: 0.85rem; right: 0.85rem; width: auto; }
  .audio-pill[data-state="collapsed"]::after { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .audio-pill, .ap-fill, .ap-play, .ap-meta { transition: none; }
}
"""

# ────────────────────────────────────────────────────────────────
# Markup nuevo (placeholders {src} y {duration})
# ────────────────────────────────────────────────────────────────
HTML_NEW = """\
<aside class="audio-pill" data-state="collapsed" data-duration="{duration}" aria-label="Reproductor de audio del capítulo">
  <audio class="ap-audio" preload="metadata" src="{src}"></audio>
  <button class="ap-play" type="button" aria-label="Reproducir capítulo">
    <svg class="ap-icon-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
    <svg class="ap-icon-pause" viewBox="0 0 24 24" aria-hidden="true" style="display:none"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>
  </button>
  <div class="ap-meta">
    <div class="ap-track" role="slider" tabindex="0" aria-label="Posición del audio" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
      <div class="ap-rail"></div>
      <div class="ap-fill"></div>
      <div class="ap-thumb"></div>
    </div>
    <div class="ap-time"><span class="ap-current">0:00</span></div>
    <button class="ap-rate" type="button" aria-label="Velocidad de reproducción">1×</button>
    <button class="ap-close" type="button" aria-label="Minimizar reproductor">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6 L18 18 M18 6 L6 18"/></svg>
    </button>
  </div>
</aside>"""

# ────────────────────────────────────────────────────────────────
# JS nuevo
# ────────────────────────────────────────────────────────────────
JS_NEW = """\
<script>
/* AUDIO PILL controller */
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
  var RATES = [1, 1.25, 1.5, 0.8];
  var rateIdx = 0;
  function fmt(t){ if(!isFinite(t)) return '0:00'; var m=Math.floor(t/60), s=Math.floor(t%60); return m+':'+(s<10?'0':'')+s; }
  function expand(){ pill.setAttribute('data-state','expanded'); }
  function collapse(){ pill.setAttribute('data-state','collapsed'); }
  function setPlayIcon(playing){
    if (playing) { pi.style.display='none'; ps.style.display=''; b.setAttribute('aria-label','Pausar'); }
    else         { pi.style.display=''; ps.style.display='none'; b.setAttribute('aria-label','Reproducir'); }
  }
  a.addEventListener('loadedmetadata', function(){
    if (isFinite(a.duration)) pill.setAttribute('data-duration', fmt(a.duration));
  });
  a.addEventListener('timeupdate', function(){
    var pct = a.duration ? (a.currentTime/a.duration)*100 : 0;
    fi.style.width = pct+'%'; th.style.left = pct+'%';
    cu.textContent = fmt(a.currentTime);
    tr.setAttribute('aria-valuenow', Math.round(pct));
  });
  a.addEventListener('play',  function(){ pill.classList.add('playing'); setPlayIcon(true); expand(); });
  a.addEventListener('pause', function(){ pill.classList.remove('playing'); setPlayIcon(false); });
  a.addEventListener('ended', function(){ pill.classList.remove('playing'); setPlayIcon(false); });
  b.addEventListener('click', function(e){ e.stopPropagation(); if (a.paused) a.play(); else a.pause(); });
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
  pill.addEventListener('keydown', function(e){
    if (e.key !== ' ' && e.key !== 'Spacebar') return;
    if (e.target === rateBtn || e.target === closeBtn) return;
    e.preventDefault();
    if (a.paused) a.play(); else a.pause();
  });
})();
</script>"""

PILL_MARKER = '<aside class="audio-pill"'


def install(html_path: Path, audio_src: str, duration: str):
    html = html_path.read_text(encoding="utf-8")
    if PILL_MARKER in html:
        print(f"[skip] {html_path.name}: ya tiene <aside class='audio-pill'>")
        return

    has_old = '<aside class="audio-player"' in html

    # ──────── 1. quitar CSS viejo del player ────────
    if has_old:
        # Bloque de líneas consecutivas con selectores .audio-player / .ap-*
        # Las reglas viejas vienen todas pegadas (una por línea) entre línea 55-69
        # aprox. Eliminamos el rango contiguo.
        css_old_re = re.compile(
            r"\.audio-player\s*\{[^}]*\}(?:\s*\.(?:audio-player|ap-)[^}]*\{[^}]*\})+"
        )
        html, n = css_old_re.subn("", html, count=1)
        if n == 0:
            raise RuntimeError(f"no encontré CSS viejo del player en {html_path}")
        # En la media query (max-width 640px) había:
        #   .ap-time { min-width: 64px; font-size: 0.75rem; } .audio-player { padding: 1.1rem 1.2rem; }
        # eliminar ambas declaraciones (no aplican a la pill).
        media_old_re = re.compile(
            r"\s*\.ap-time\s*\{[^}]*\}\s*\.audio-player\s*\{[^}]*\}"
        )
        html = media_old_re.sub("", html, count=1)

    # ──────── 2. quitar JS viejo del player ────────
    if has_old:
        js_old_re = re.compile(
            r"<script>\s*\(function\(\)\{\s*document\.querySelectorAll\('\.audio-player'\)[\s\S]*?\}\)\(\);\s*</script>"
        )
        html, n = js_old_re.subn("", html, count=1)
        if n == 0:
            raise RuntimeError(f"no encontré JS viejo del player en {html_path}")

    # ──────── 3. quitar markup viejo ────────
    if has_old:
        aside_old_re = re.compile(
            r'<aside class="audio-player"[^>]*>[\s\S]*?</aside>\s*'
        )
        html, n = aside_old_re.subn("", html, count=1)
        if n == 0:
            raise RuntimeError(f"no encontré <aside audio-player> en {html_path}")

    # ──────── 4. inyectar CSS nuevo al final del <style> ────────
    style_close = re.search(r"</style>", html)
    if not style_close:
        raise RuntimeError(f"no hay </style> en {html_path}")
    html = (
        html[: style_close.start()]
        + CSS_NEW
        + "\n"
        + html[style_close.start():]
    )

    # ──────── 5. inyectar markup nuevo justo antes de </body> ────────
    pill_markup = HTML_NEW.format(src=audio_src, duration=duration)
    body_close = re.search(r"</body>", html)
    if not body_close:
        raise RuntimeError(f"no hay </body> en {html_path}")
    html = (
        html[: body_close.start()]
        + pill_markup
        + "\n\n"
        + JS_NEW
        + "\n"
        + html[body_close.start():]
    )

    html_path.write_text(html, encoding="utf-8")
    print(f"[OK]  {html_path.name}: instalada pill ({duration})")


def main():
    if len(sys.argv) != 4:
        raise SystemExit("uso: install_audio_pill.py <capitulo.html> <audio_src> <duration HH:MM>")
    install(Path(sys.argv[1]), sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
