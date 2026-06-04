#!/usr/bin/env python3
"""
Agrega el subsistema de subrayado al capítulo HTML:
  1. CSS: estilos para .w.hl (palabra subrayada) y .hl-toolbar (botones flotantes)
  2. JS: aborta el click del karaoke cuando hay selección de texto activa
  3. JS: bloque nuevo al final del body que maneja la selección, la toolbar
     y persiste las palabras subrayadas en localStorage por capítulo.

Idempotente: si el archivo ya tiene los cambios, no los duplica.

Uso:
  add_highlights.py <archivo.html> [otro.html ...]
"""
import re
import sys
from pathlib import Path

CSS_BLOCK = """\
.w.hl { background-color: rgba(255,224,102,0.45); border-radius: 2px; }
.w.hl:hover { background-color: rgba(255,224,102,0.6); }
.w.activa.hl { background-color: rgba(255,122,24,0.35); }
.w.leida.hl { opacity: 1; }
body.karaoke-off .w.hl { background-color: rgba(255,224,102,0.45) !important; color: inherit; }
.hl-toolbar { position: absolute; display: none; background: var(--surface); border: 1px solid var(--rule); border-radius: 6px; padding: 3px; box-shadow: 0 4px 16px -4px rgba(0,0,0,0.6); z-index: 200; font-family: var(--font-body); white-space: nowrap; -webkit-backdrop-filter: saturate(180%) blur(20px); backdrop-filter: saturate(180%) blur(20px); }
.hl-toolbar.show { display: block; }
.hl-btn { background: transparent; border: none; color: var(--ink); padding: 0.42rem 0.85rem; cursor: pointer; border-radius: 4px; font-family: inherit; font-size: 0.84rem; letter-spacing: 0.02em; }
.hl-btn:hover { background: var(--rule); }
.hl-btn-rm { color: var(--ink-soft); }
"""

JS_BLOCK = """\
<script>
/* Subrayado (highlights) — selecciona texto y aparece toolbar; se guarda en localStorage por capítulo */
(function(){
  var STORAGE_KEY = 'highlights:' + (location.pathname.split('/').pop() || 'doc');
  var prose = document.querySelector('.prose');
  if (!prose) return;

  var saved;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch(e){ saved = []; }
  if (!Array.isArray(saved)) saved = [];
  saved.forEach(function(idx){
    var el = prose.querySelector('.w[data-w="'+idx+'"]');
    if (el) el.classList.add('hl');
  });

  var toolbar = document.createElement('div');
  toolbar.className = 'hl-toolbar';
  toolbar.setAttribute('role', 'toolbar');
  toolbar.setAttribute('aria-label', 'Acciones de subrayado');
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
      if (range.intersectsNode(allWords[i])) {
        var idx = parseInt(allWords[i].getAttribute('data-w'), 10);
        if (!isNaN(idx)) idxs.push(idx);
      }
    }
    return idxs;
  }

  function save(){
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(saved)); } catch(e){}
  }

  function apply(){
    selectedIdxs.forEach(function(i){
      var el = prose.querySelector('.w[data-w="'+i+'"]');
      if (el) el.classList.add('hl');
      if (saved.indexOf(i) === -1) saved.push(i);
    });
    save(); hideToolbar();
    var sel = window.getSelection(); if (sel) sel.removeAllRanges();
  }
  function remove(){
    selectedIdxs.forEach(function(i){
      var el = prose.querySelector('.w[data-w="'+i+'"]');
      if (el) el.classList.remove('hl');
      var k = saved.indexOf(i); if (k !== -1) saved.splice(k, 1);
    });
    save(); hideToolbar();
    var sel = window.getSelection(); if (sel) sel.removeAllRanges();
  }

  function showToolbar(x, y, anyHl){
    toolbar.innerHTML = '';
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'hl-btn';
    btn.textContent = anyHl ? 'Subrayar todo' : 'Subrayar';
    btn.addEventListener('mousedown', function(e){ e.preventDefault(); });
    btn.addEventListener('click', function(e){ e.stopPropagation(); apply(); });
    toolbar.appendChild(btn);
    if (anyHl) {
      var rm = document.createElement('button');
      rm.type = 'button'; rm.className = 'hl-btn hl-btn-rm';
      rm.textContent = 'Quitar';
      rm.addEventListener('mousedown', function(e){ e.preventDefault(); });
      rm.addEventListener('click', function(e){ e.stopPropagation(); remove(); });
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
      if (idxs.length === 0) { hideToolbar(); return; }
      var sel = window.getSelection();
      var range = sel.getRangeAt(0);
      var rect = range.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) { hideToolbar(); return; }
      var x = rect.left + window.scrollX + rect.width / 2;
      var y = rect.top + window.scrollY;
      var anyHl = idxs.some(function(i){ return saved.indexOf(i) !== -1; });
      selectedIdxs = idxs;
      showToolbar(x, y, anyHl);
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
</script>
"""

MARK = "/* highlights MVP — instalado por tools/add_highlights.py */"

def patch(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    if MARK in src:
        print(f"= {path.name}: ya tiene highlights, omito")
        return False

    # 1) Insertar CSS antes del último @media. Marcamos con un comentario.
    css_marker = f"\n{MARK}\n{CSS_BLOCK}"
    # buscamos la línea que abre @media (max-width: 640px) y la dejamos intacta;
    # el CSS nuevo va inmediatamente antes
    pattern_media = re.compile(r"(@media \(max-width: 640px\))")
    src2, n = pattern_media.subn(css_marker + r"\1", src, count=1)
    if n != 1:
        print(f"✗ {path.name}: no encontré @media para insertar CSS")
        return False

    # 2) Modificar el handler click .w: abortar si hay selección de texto
    handler_pattern = re.compile(
        r"(document\.addEventListener\('click', function\(e\)\{\s*var t = e\.target;\s*"
        r"if \(!\(t && t\.classList && t\.classList\.contains\('w'\)\)\) return;)"
    )
    src3, n = handler_pattern.subn(
        r"\1\n    if (window.getSelection && window.getSelection().toString().length > 0) return;",
        src2, count=1
    )
    if n != 1:
        print(f"! {path.name}: no encontré el handler click .w (sigo con CSS+JS)")
        src3 = src2

    # 3) Insertar el bloque JS de highlights justo antes de </body>
    if "</body>" in src3:
        src3 = src3.replace("</body>", JS_BLOCK + "\n</body>", 1)
    else:
        print(f"✗ {path.name}: no encontré </body>")
        return False

    path.write_text(src3, encoding="utf-8")
    print(f"✓ {path.name}: highlights agregados")
    return True


def main():
    if len(sys.argv) < 2:
        print("uso: add_highlights.py <archivo.html> [...]", file=sys.stderr)
        sys.exit(1)
    changed = 0
    for arg in sys.argv[1:]:
        if patch(Path(arg)):
            changed += 1
    print(f"\nTotal modificados: {changed}")


if __name__ == "__main__":
    main()
