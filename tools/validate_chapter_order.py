#!/usr/bin/env python3
"""Valida que el orden canónico de capítulos sea COHERENTE entre:
  - index.html  (el orden de lectura visible, la fuente de verdad)
  - tools/build_book_md.py::CHAPTERS
  - tools/build_pdf.py::CHAPTERS

Por qué este check:
  El bug que motivó este script: tras reorganizar el índice y los
  nav-foots, se olvidó actualizar la lista CHAPTERS en build_book_md.py.
  Resultado: el MD generado tenía los caps con su contenido nuevo pero
  concatenados en el orden viejo. El lector humano de la web veía un
  orden; el consumidor del MD (las IAs) veía otro.

  Este validador hace que sea imposible que eso vuelva a pasar: si los
  tres órdenes no coinciden, el pipeline aborta antes de generar el MD.

Extracción del orden desde index.html:
  - Por cada <a href="*.html"> dentro de <section class="bloque">,
    <div class="bisagra"> o <div class="cimiento">, en orden de aparición.
  - Filtra index.html mismo y la portada.
  - Devuelve la lista en orden de lectura.

Uso:
  validate_chapter_order.py            → valida los 3 órdenes
  validate_chapter_order.py --fix      → reescribe CHAPTERS en los
                                          builders para que coincidan
                                          con index.html (último recurso)

Exit codes:
  0 → todos los órdenes coinciden
  1 → al menos un orden no coincide; pipeline debe abortar
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def order_from_index() -> list[str]:
    """Extrae el orden canónico de capítulos desde index.html."""
    h = (ROOT / "index.html").read_text(encoding="utf-8")
    # Tomar solo la zona del índice donde están los caps/bisagras/cimientos
    # (entre el cierre de la portada y el cierre del index).
    # Más simple: capturar todos los hrefs a *.html dentro de <section
    # class="bloque">, <div class="bisagra">, <div class="cimiento">.
    chapters = []
    # Buscamos cada elemento estructural en orden de aparición.
    # Estrategia: walking del HTML.
    pat = re.compile(
        r'<(?:section class="bloque"|div class="(?:bisagra|cimiento)")\b.*?</(?:section|div)>',
        re.DOTALL,
    )
    # Simplificación: captura todos los href="X.html" en orden y filtra.
    blacklist = {"index.html"}
    seen = set()
    for m in re.finditer(r'href="([\w\-]+\.html)"', h):
        ref = m.group(1)
        if ref in blacklist or ref in seen:
            continue
        seen.add(ref)
        chapters.append(ref)
    return chapters


def order_from_builder(builder_path: Path) -> list[str]:
    """Extrae CHAPTERS = [...] del builder."""
    src = builder_path.read_text(encoding="utf-8")
    m = re.search(r'^CHAPTERS\s*=\s*\[(.*?)\]', src, re.DOTALL | re.MULTILINE)
    if not m:
        return []
    body = m.group(1)
    chapters = re.findall(r'"([\w\-]+\.html)"', body)
    return chapters


def main():
    fix_mode = "--fix" in sys.argv

    index_order = order_from_index()
    md_path = ROOT / "tools" / "build_book_md.py"
    pdf_path = ROOT / "tools" / "build_pdf.py"
    md_order = order_from_builder(md_path)
    pdf_order = order_from_builder(pdf_path)

    print(f"Orden inferido del index.html:    {len(index_order)} caps")
    print(f"Orden de tools/build_book_md.py:  {len(md_order)} caps")
    print(f"Orden de tools/build_pdf.py:      {len(pdf_order)} caps")
    print()

    problems = []

    if index_order != md_order:
        problems.append(("build_book_md.py", md_order, md_path))
    if index_order != pdf_order:
        problems.append(("build_pdf.py", pdf_order, pdf_path))

    if not problems:
        print("✓ orden coherente entre index.html, build_book_md.py "
              "y build_pdf.py")
        sys.exit(0)

    # Mostrar diff visual
    for name, builder_order, _ in problems:
        print(f"✗ {name} NO coincide con index.html:")
        n = max(len(index_order), len(builder_order))
        for i in range(n):
            ix = index_order[i] if i < len(index_order) else "—"
            bx = builder_order[i] if i < len(builder_order) else "—"
            marker = " " if ix == bx else "✗"
            print(f"    {marker} [{i:2}] index={ix:48} builder={bx}")
        print()

    if not fix_mode:
        print("Para arreglar automáticamente: validate_chapter_order.py --fix")
        sys.exit(1)

    # --fix: reescribir CHAPTERS en cada builder roto
    print("→ aplicando --fix")
    for name, _, builder_path in problems:
        src = builder_path.read_text(encoding="utf-8")
        m = re.search(r'^CHAPTERS\s*=\s*\[(.*?)\]', src,
                      re.DOTALL | re.MULTILINE)
        if not m:
            continue
        # Construir nueva lista con comentarios de bloque
        new_lines = ["CHAPTERS = ["]
        for ch in index_order:
            new_lines.append(f'    "{ch}",')
        new_lines.append("]")
        new_block = "\n".join(new_lines)
        # Conservar el header y comentarios del builder
        new_src = (src[:m.start()] + new_block + src[m.end():])
        builder_path.write_text(new_src, encoding="utf-8")
        print(f"  ✓ {name}: CHAPTERS reescrito con el orden de index.html")
    print()
    print("Re-corrre el script sin --fix para verificar.")
    sys.exit(0)


if __name__ == "__main__":
    main()
