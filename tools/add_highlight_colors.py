#!/usr/bin/env python3
"""Convierte el subrayado de un solo color (amarillo) a 4 colores con código:
amarillo (importante · default), naranja (cita/dato), verde (me convence),
coral (dudo/revisar). Funciona en los 3 temas (oscuro/sepia/claro).

Backward compatible:
- Subrayados viejos en localStorage como [3, 7, 12] siguen mostrándose en
  amarillo. El nuevo formato es [3, [7,"v"], 12]: número solo = amarillo,
  [idx, "a|n|v|c"] = color elegido. No requiere migración.
- Cada subrayado guarda SU color (no es global).

Cambios al HTML:
1. CSS: variables --hl-color-* por tema + reglas .hl[data-c=...].
2. JS: el toolbar tiene 4 swatches en vez de un solo botón «Subrayar».
   Click aplica/cambia el color. El botón «Quitar» se mantiene.

Idempotente: si el archivo ya tiene el marcador, no se toca.
Uso: add_highlight_colors.py <archivo.html>
"""
import re
import sys
from pathlib import Path

MARK = "/* hl-colors-v1 */"

# CSS: 4 colores con variantes por tema. El default (oscuro) usa colores
# saturados, sepia/claro usan tonos un poco más profundos para mantener el
# contraste sobre fondos claros. El amarillo default queda como estaba.
CSS_BLOCK = """
""" + MARK + """
:root{
  --hl-color-a: rgba(255,238,0,0.95);   /* amarillo · importante */
  --hl-color-n: rgba(255,150,40,0.95);  /* naranja  · cita/dato */
  --hl-color-v: rgba(120,210,120,0.95); /* verde    · me convence */
  --hl-color-c: rgba(255,128,128,0.95); /* coral    · dudo/revisar */
}
:root[data-theme="sepia"]{
  --hl-color-a: rgba(212,160,0,0.9);
  --hl-color-n: rgba(208,110,30,0.9);
  --hl-color-v: rgba(80,150,80,0.9);
  --hl-color-c: rgba(200,80,80,0.9);
}
:root[data-theme="claro"]{
  --hl-color-a: rgba(218,160,0,0.95);
  --hl-color-n: rgba(214,108,28,0.95);
  --hl-color-v: rgba(64,140,64,0.95);
  --hl-color-c: rgba(204,72,72,0.95);
}
.hl[data-c="a"]{ box-shadow: inset 0 -1.5px 0 var(--hl-color-a) !important; }
.hl[data-c="n"]{ box-shadow: inset 0 -1.5px 0 var(--hl-color-n) !important; }
.hl[data-c="v"]{ box-shadow: inset 0 -1.5px 0 var(--hl-color-v) !important; }
.hl[data-c="c"]{ box-shadow: inset 0 -1.5px 0 var(--hl-color-c) !important; }
.hl[data-c="a"]:hover{ box-shadow: inset 0 -2.5px 0 var(--hl-color-a) !important; }
.hl[data-c="n"]:hover{ box-shadow: inset 0 -2.5px 0 var(--hl-color-n) !important; }
.hl[data-c="v"]:hover{ box-shadow: inset 0 -2.5px 0 var(--hl-color-v) !important; }
.hl[data-c="c"]:hover{ box-shadow: inset 0 -2.5px 0 var(--hl-color-c) !important; }

.hl-swatch{
  width: 22px; height: 22px; border-radius: 50%;
  border: 1.5px solid transparent;
  background: transparent; cursor: pointer; padding: 0;
  display: inline-flex; align-items: center; justify-content: center;
  margin: 0 2px;
  position: relative;
}
.hl-swatch::after{
  content: ""; width: 14px; height: 14px; border-radius: 50%;
  background: var(--sw-color);
  box-shadow: 0 0 0 1px rgba(0,0,0,0.15);
}
.hl-swatch[data-c="a"]{ --sw-color: var(--hl-color-a); }
.hl-swatch[data-c="n"]{ --sw-color: var(--hl-color-n); }
.hl-swatch[data-c="v"]{ --sw-color: var(--hl-color-v); }
.hl-swatch[data-c="c"]{ --sw-color: var(--hl-color-c); }
.hl-swatch:hover{ border-color: var(--rule); }
.hl-swatch.current{ border-color: var(--ink); }
.hl-toolbar .hl-divider{ display:inline-block; width:1px; height:18px; background: var(--rule); margin: 0 4px; vertical-align: middle; }
"""

# JS nuevo que reemplaza el bloque del subrayado. Mantiene la interfaz pero
# soporta los 4 colores y el formato extendido del localStorage.
NEW_JS = '''<script>
/* Subrayado con colores — instalado por tools/add_highlight_colors.py */
(function(){
  var STORAGE_KEY = 'highlights:' + (location.pathname.split('/').pop() || 'doc');
  var prose = document.querySelector('.prose');
  if (!prose) return;
  var COLORS = ['a','n','v','c'];
  var LAST_COLOR_KEY = 'highlights:last-color';
  var DEFAULT_COLOR = 'a';
  var lastColor;
  try { lastColor = localStorage.getItem(LAST_COLOR_KEY) || DEFAULT_COLOR; } catch(e){ lastColor = DEFAULT_COLOR; }
  if (COLORS.indexOf(lastColor) === -1) lastColor = DEFAULT_COLOR;

  // saved: arreglo donde cada item es Number (=amarillo, compat) o [idx, color].
  var saved;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch(e){ saved = []; }
  if (!Array.isArray(saved)) saved = [];
  // mapa idx → color para pintar
  function buildMap(){
    var m = {};
    saved.forEach(function(it){
      if (typeof it === 'number') m[it] = 'a';
      else if (Array.isArray(it) && it.length >= 2) m[it[0]] = COLORS.indexOf(it[1]) !== -1 ? it[1] : 'a';
    });
    return m;
  }
  function paintAll(){
    var m = buildMap();
    prose.querySelectorAll('.w.hl').forEach(function(el){
      el.classList.remove('hl'); el.removeAttribute('data-c');
    });
    Object.keys(m).forEach(function(idx){
      var el = prose.querySelector('.w[data-w="'+idx+'"]');
      if (el){ el.classList.add('hl'); el.setAttribute('data-c', m[idx]); }
    });
  }
  paintAll();

  function setColor(idx, color){
    // quitar entry previa
    for (var i = saved.length - 1; i >= 0; i--){
      var it = saved[i];
      var k = typeof it === 'number' ? it : (Array.isArray(it) ? it[0] : -1);
      if (k === idx) saved.splice(i, 1);
    }
    // guardar (forma compacta para amarillo)
    if (color === 'a') saved.push(idx);
    else saved.push([idx, color]);
  }
  function removeIdx(idx){
    for (var i = saved.length - 1; i >= 0; i--){
      var it = saved[i];
      var k = typeof it === 'number' ? it : (Array.isArray(it) ? it[0] : -1);
      if (k === idx) saved.splice(i, 1);
    }
  }
  function save(){
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(saved)); } catch(e){}
  }

  var toolbar = document.createElement('div');
  toolbar.className = 'hl-toolbar';
  toolbar.setAttribute('role','toolbar');
  toolbar.setAttribute('aria-label','Acciones de subrayado');
  document.body.appendChild(toolbar);

  var selectedIdxs = [];
  function hideToolbar(){ toolbar.classList.remove('show'); selectedIdxs = []; }

  function getSelectedWordIdxs(){
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount || sel.toString().trim() === '') return [];
    var range = sel.getRangeAt(0);
    if (!prose.contains(range.commonAncestorContainer) && !range.intersectsNode(prose)) return [];
    var idxs = [];
    var allWords = prose.querySelectorAll('.w');
    for (var i = 0; i < allWords.length; i++){
      if (range.intersectsNode(allWords[i])){
        var idx = parseInt(allWords[i].getAttribute('data-w'), 10);
        if (!isNaN(idx)) idxs.push(idx);
      }
    }
    return idxs;
  }

  function applyColor(color){
    selectedIdxs.forEach(function(i){ setColor(i, color); });
    try { localStorage.setItem(LAST_COLOR_KEY, color); } catch(e){}
    lastColor = color;
    save(); paintAll(); hideToolbar();
    var sel = window.getSelection(); if (sel) sel.removeAllRanges();
  }
  function removeAll(){
    selectedIdxs.forEach(function(i){ removeIdx(i); });
    save(); paintAll(); hideToolbar();
    var sel = window.getSelection(); if (sel) sel.removeAllRanges();
  }

  var COLOR_LABEL = { a: 'Amarillo · importante', n: 'Naranja · cita o dato', v: 'Verde · me convence', c: 'Coral · dudo' };

  function showToolbar(x, y, currentColor){
    toolbar.innerHTML = '';
    COLORS.forEach(function(c){
      var sw = document.createElement('button');
      sw.type = 'button'; sw.className = 'hl-swatch';
      sw.setAttribute('data-c', c);
      sw.setAttribute('aria-label', COLOR_LABEL[c]);
      sw.title = COLOR_LABEL[c];
      if (currentColor === c) sw.classList.add('current');
      sw.addEventListener('mousedown', function(e){ e.preventDefault(); });
      sw.addEventListener('click', function(e){ e.stopPropagation(); applyColor(c); });
      toolbar.appendChild(sw);
    });
    if (currentColor){
      var div = document.createElement('span'); div.className = 'hl-divider';
      toolbar.appendChild(div);
      var rm = document.createElement('button');
      rm.type = 'button'; rm.className = 'hl-btn hl-btn-rm';
      rm.textContent = 'Quitar';
      rm.addEventListener('mousedown', function(e){ e.preventDefault(); });
      rm.addEventListener('click', function(e){ e.stopPropagation(); removeAll(); });
      toolbar.appendChild(rm);
    }
    toolbar.classList.add('show');
    var w = toolbar.offsetWidth, h = toolbar.offsetHeight;
    var vw = window.innerWidth;
    var left = Math.max(8, Math.min(vw - w - 8, x - w/2));
    var top = Math.max(window.scrollY + 8, y - h - 8);
    toolbar.style.left = left + 'px';
    toolbar.style.top = top + 'px';
  }

  function onSelection(e){
    if (e && e.target && toolbar.contains(e.target)) return;
    if (e && e.target && e.target.closest && e.target.closest('.audio-pill')) return;
    setTimeout(function(){
      var idxs = getSelectedWordIdxs();
      if (idxs.length === 0){ hideToolbar(); return; }
      var sel = window.getSelection();
      var range = sel.getRangeAt(0);
      var rect = range.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0){ hideToolbar(); return; }
      var x = rect.left + window.scrollX + rect.width/2;
      var y = rect.top + window.scrollY;
      var m = buildMap();
      // color "actual" de la selección: si todas las palabras subrayadas comparten color, ese; si no, ninguno
      var present = idxs.map(function(i){ return m[i]; }).filter(Boolean);
      var allSame = present.length === idxs.length && present.every(function(c){ return c === present[0]; });
      var currentColor = allSame && present.length ? present[0] : null;
      selectedIdxs = idxs;
      showToolbar(x, y, currentColor);
    }, 10);
  }

  document.addEventListener('mouseup', onSelection);
  document.addEventListener('touchend', onSelection);
  document.addEventListener('mousedown', function(e){
    if (toolbar.contains(e.target)) return;
    hideToolbar();
  });
  window.addEventListener('scroll', hideToolbar, { passive: true });
  window.addEventListener('resize', hideToolbar);
})();
</script>'''


def patch(html: str) -> str:
    if MARK in html:
        return html
    # 1) inyectar CSS antes de </style>
    html = html.replace("</style>", CSS_BLOCK + "</style>", 1)
    # 2) reemplazar el bloque del highlighter viejo por el nuevo. El bloque viejo
    #    empieza con "/* Subrayado (highlights)" y termina en "</script>".
    pat = re.compile(
        r'<script>\s*/\* Subrayado \(highlights\).*?</script>',
        re.DOTALL,
    )
    new_html, n = pat.subn(NEW_JS, html, count=1)
    if n == 0:
        raise RuntimeError("no se encontró el bloque del highlighter viejo")
    return new_html


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: add_highlight_colors.py <archivo.html>")
    src = Path(sys.argv[1])
    html = src.read_text(encoding="utf-8")
    out = patch(html)
    if out == html and MARK in html:
        print("ya tenía hl-colors-v1:", src)
    else:
        src.write_text(out, encoding="utf-8")
        print("hl-colors-v1 inyectado →", src)


if __name__ == "__main__":
    main()
