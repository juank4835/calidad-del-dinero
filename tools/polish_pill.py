#!/usr/bin/env python3
"""Afina la audio-pill y el botón de play para que destaquen bien en los 3
temas (oscuro · sepia · claro), sin cambiar el color naranja del play (que es
el color de marca del libro).

El CSS base de la pill tiene `background: rgba(38,38,38,0.92)` y sombras negras
hardcoded, pensadas para fondo oscuro. En sepia/claro eso se ve como un parche
oscuro sobre fondo crema. Aquí inyectamos un bloque CSS adicional con reglas
`:root[data-theme="..."] .audio-pill` que sobrescriben SOLO en sepia/claro,
preservando el oscuro tal como está.

Cambios por tema:
- Sepia/Claro: pill con fondo `var(--surface)` (tono del libro), sombra más
  suave y cálida, halo naranja sutil bajo el botón de play para que destaque
  sin gritar.
- El naranja del play y el icono blanco quedan iguales — son la marca.

Idempotente vía marcador `/* pill-polish-v1 */`.
Uso: polish_pill.py <archivo.html>
"""
import sys
from pathlib import Path

MARK = "/* pill-polish-v1 */"

CSS_BLOCK = """
""" + MARK + """
:root[data-theme="sepia"] .audio-pill,
:root[data-theme="claro"] .audio-pill {
  background: var(--surface);
  border-color: var(--rule);
  box-shadow:
    0 14px 32px -14px rgba(80, 60, 30, 0.32),
    0 4px 10px -2px rgba(80, 60, 30, 0.12),
    0 0 0 3px rgba(255, 122, 24, 0.06);
}
:root[data-theme="sepia"] .audio-pill:hover,
:root[data-theme="claro"] .audio-pill:hover {
  box-shadow:
    0 18px 40px -12px rgba(80, 60, 30, 0.42),
    0 6px 14px -2px rgba(80, 60, 30, 0.18),
    0 0 0 4px rgba(255, 122, 24, 0.10);
}
:root[data-theme="sepia"] .audio-pill .ap-play,
:root[data-theme="claro"] .audio-pill .ap-play {
  box-shadow:
    0 4px 12px -2px rgba(255, 122, 24, 0.55),
    0 2px 4px -1px rgba(0, 0, 0, 0.15);
}
:root[data-theme="sepia"] .audio-pill .ap-play:hover,
:root[data-theme="claro"] .audio-pill .ap-play:hover {
  box-shadow:
    0 6px 16px -2px rgba(255, 122, 24, 0.7),
    0 3px 6px -1px rgba(0, 0, 0, 0.2);
}
/* En claro/sepia, el texto del rate y los iconos secundarios necesitan tomar
   los colores del tema (algunos estaban hardcoded a tono oscuro). */
:root[data-theme="sepia"] .audio-pill .ap-rate,
:root[data-theme="claro"] .audio-pill .ap-rate { color: var(--ink-soft); border-color: var(--rule); }
:root[data-theme="sepia"] .audio-pill .ap-rate:hover,
:root[data-theme="claro"] .audio-pill .ap-rate:hover { color: var(--ink); border-color: var(--ink-soft); }

/* Pequeño realce permanente del play en oscuro también, para que el botón
   principal sienta más «vivo» en cualquier tema (cambio sutil). */
.audio-pill .ap-play {
  box-shadow: 0 3px 10px -2px rgba(255, 122, 24, 0.35);
}
.audio-pill .ap-play:hover {
  box-shadow: 0 5px 14px -2px rgba(255, 122, 24, 0.5);
}
"""


def patch(html: str) -> str:
    if MARK in html:
        return html
    return html.replace("</style>", CSS_BLOCK + "</style>", 1)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: polish_pill.py <archivo.html>")
    src = Path(sys.argv[1])
    html = src.read_text(encoding="utf-8")
    out = patch(html)
    if out == html:
        print("ya tenía pill-polish-v1:", src)
    else:
        src.write_text(out, encoding="utf-8")
        print("pill-polish-v1 inyectado →", src)


if __name__ == "__main__":
    main()
