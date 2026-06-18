#!/usr/bin/env python3
"""Genera un PDF del libro completo concatenando todos los capítulos.

Estrategia:
  1. Toma el orden de capítulos del orden canónico del libro.
  2. De cada HTML extrae solo el <article class="page"> (el contenido).
  3. Reúne todo en un book.html con:
     - portada (extraída de index.html)
     - índice / tabla de contenidos
     - cada capítulo, con salto de página antes
     - umbral de cierre (cap 19 pendiente)
  4. Aplica CSS de impresión: tema claro forzado, sin UI flotante (pill,
     gear, panel ajustes, barra de progreso, etc.), sin spans karaoke
     interfiriendo en la tipografía.
  5. Llama a Chrome headless para imprimir a PDF.

Uso:
  build_pdf.py           → genera ./arregla-el-dinero.pdf
  build_pdf.py salida.pdf
"""
import re
import subprocess
import sys
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Orden canónico del libro
CHAPTERS = [
    # Bloque I · Fundamentos
    "dinero-como-informacion.html",
    "criterio-de-evaluacion.html",
    "tres-formas-organizar-dinero.html",
    # Bisagra entre Bloque I y Bloque II
    "cuando-un-precio-dice-la-verdad.html",
    # Bloque II · Los cimientos
    "preferencia-temporal.html",
    "ahorro-real.html",
    # Bloque III · La anatomía
    "tasa-de-interes.html",
    "asignacion-intertemporal.html",
    "deteccion-mala-inversion.html",
    "precios-relativos.html",
    "predictibilidad-estructural.html",
    "poder-adquisitivo.html",
    "asignacion-credito.html",
    "auditabilidad.html",
    # Bisagra
    "por-que-no-volver-al-oro.html",
    # Bloque IV
    "el-horizonte-se-acorta.html",
]


def extract_article(html: str) -> str:
    """Saca solo el <article class="page">..</article> del capítulo."""
    m = re.search(r'<article class="page"[^>]*>.*?</article>', html, re.DOTALL)
    if not m:
        raise RuntimeError("no encontré <article class=page>")
    art = m.group(0)
    # Quitar el id="contenido" (no aporta en PDF, podría chocar entre artículos)
    art = re.sub(r'\sid="contenido"', '', art)
    art = re.sub(r'\stabindex="-1"', '', art)
    return art


def extract_cover(index_html: str) -> str:
    """Saca la portada del index."""
    m = re.search(r'<header class="cover">.*?</header>', index_html, re.DOTALL)
    if not m:
        return ''
    return m.group(0)


def extract_toc(index_html: str) -> str:
    """Saca el índice/bloques del index para hacer una TOC al inicio."""
    # Capturar todo desde <!-- BLOQUE I --> hasta el cierre del último elemento
    m = re.search(
        r'<!-- BLOQUE I -->.*?</section>\s*(?=<!-- UMBRAL DE CIERRE|</div>)',
        index_html,
        re.DOTALL,
    )
    if not m:
        return ''
    toc = m.group(0)
    # Incluir también la bisagra del oro y el umbral de cierre
    m2 = re.search(r'<!-- BISAGRA.*?</div>\s*\n', index_html, re.DOTALL)
    m3 = re.search(r'<!-- UMBRAL DE CIERRE.*?</div>', index_html, re.DOTALL)
    return toc + ('\n' + m2.group(0) if m2 else '') + ('\n' + m3.group(0) if m3 else '')


# CSS para PDF: tema claro forzado, sin UI flotante, saltos de página
PRINT_CSS = """
:root {
  --bg: #fbf9f5; --surface: #eeeae3; --ink: #1a1916;
  --ink-soft: #5d584f; --rule: #e2ddd3; --verde: #FF7A18;
  --rojo: #E8552D; --font-scale: 1;
  --font-body: 'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
body {
  background: var(--bg); color: var(--ink); font-family: var(--font-body);
  line-height: 1.7; margin: 0; padding: 0; position: relative; overflow-x: hidden;
}

/* === OCULTAR TODA LA UI flotante (no aplica en papel) === */
.audio-pill, .nav-top, .nav-foot, .read-progress, .ui-settings,
.resume-read, .next-card, .skip-link, .hl-toolbar, .ap-resume-hint,
.audio-only { display: none !important; }
/* Quitar el glow naranja del fondo (en papel se ve raro) */
body::before { display: none !important; }
.audio-only { display: none !important; }

/* === Portada del libro === */
.cover { text-align: center; margin: 0 auto; max-width: 760px; padding: 8rem 1.5rem 4rem; page-break-after: always; }
.cover .kicker {
  font-size: 0.78rem; letter-spacing: 0.24em; text-transform: uppercase;
  color: var(--verde); margin-bottom: 1.4rem;
}
.cover h1 {
  font-size: 3rem; font-weight: 400; line-height: 1.1;
  letter-spacing: -0.015em; margin-bottom: 0.8rem;
}
.cover .sub {
  font-size: 1.2rem; font-style: italic; color: var(--ink-soft);
  max-width: 30rem; margin: 0 auto;
}
.cover .autor {
  margin-top: 2rem;
  font-size: 0.78rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--ink-soft);
}
.cover .autor em { font-style: normal; color: var(--ink); }

/* === Índice / TOC === */
.toc-wrap { max-width: 760px; margin: 0 auto; padding: 4rem 1.5rem; page-break-after: always; }
.toc-title { font-size: 0.78rem; letter-spacing: 0.24em; text-transform: uppercase; color: var(--verde); margin-bottom: 2rem; text-align: center; }
.toc-wrap .bloque { margin-bottom: 2.5rem; }
.toc-wrap .bloque-tit {
  font-size: 0.78rem; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--ink-soft); border-bottom: 1px solid var(--rule);
  padding-bottom: 0.6rem; margin-bottom: 1rem;
}
.toc-wrap .bloque-desc { font-size: 0.95rem; font-style: italic; color: var(--ink-soft); margin-bottom: 1rem; margin-top: -0.5rem; }
.toc-wrap .cap { display: flex; align-items: baseline; gap: 0.9rem; padding: 0.35rem 0; }
.toc-wrap .cap .num { font-size: 0.85rem; color: var(--ink-soft); min-width: 1.6rem; font-variant-numeric: tabular-nums; }
.toc-wrap .cap .titulo, .toc-wrap .cap a { color: var(--ink); text-decoration: none; }
.toc-wrap .cap.pend .titulo, .toc-wrap .cap.pend a { color: var(--ink-soft); opacity: 0.65; }
.toc-wrap .cap .estado { display: none; }
.toc-wrap .cimiento { margin-top: 1.5rem; padding-top: 1rem; border-top: 1px dashed var(--rule); }
.toc-wrap .cimiento .cim-tag { display: block; font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--verde); margin-bottom: 0.4rem; }
.toc-wrap .cimiento .cim-cap a { color: var(--ink); text-decoration: none; font-size: 1.05rem; }
.toc-wrap .cimiento .cim-desc { font-size: 0.9rem; font-style: italic; color: var(--ink-soft); margin-top: 0.3rem; }
.toc-wrap .cimiento .estado { display: none; }
.toc-wrap .bisagra { margin: 2rem 0; padding: 1.4rem; text-align: center; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); }
.toc-wrap .bisagra .bis-tag { display: block; font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--ink-soft); margin-bottom: 0.6rem; }
.toc-wrap .bisagra a, .toc-wrap .bisagra .bis-titulo { color: var(--ink); text-decoration: none; font-size: 1.2rem; font-style: italic; }
.toc-wrap .bisagra .bis-estado { display: none; }
.toc-wrap .bisagra.cierre { margin-top: 3rem; border-bottom: none; }
.toc-wrap .bisagra.cierre .bis-titulo { font-size: 1.3rem; }

/* === Cada capítulo: salto de página antes === */
article.page {
  max-width: 760px; margin: 0 auto; padding: 4rem 1.5rem;
  page-break-before: always;
}
article.page:first-of-type { page-break-before: avoid; }

.chapter-eyebrow {
  font-size: 0.78rem; letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--verde); margin-bottom: 1.4rem;
}
.chapter-title {
  font-size: 2.3rem; font-weight: 400; line-height: 1.15;
  letter-spacing: -0.015em; margin-bottom: 0.8rem;
}
.chapter-subtitle {
  font-size: 1.05rem; font-style: italic; color: var(--ink-soft);
  max-width: 32rem; margin-bottom: 1rem;
}
.ornament { text-align: center; color: var(--verde); letter-spacing: 0.5em; margin: 2.5rem 0 3rem; }

/* Prosa */
.prose p { font-size: 1.05rem; line-height: 1.75; margin-bottom: 1.4rem; }
.prose p.lead { font-size: 1.18rem; line-height: 1.65; color: var(--ink); margin-bottom: 1.6rem; }
.prose .lead::first-letter { font-size: 3.2rem; font-weight: 600; float: left; line-height: 0.82; margin: 0.08em 0.12em -0.1em 0; color: var(--verde); }
.prose em { font-style: italic; }
.prose strong { font-weight: 600; color: var(--ink); }
.prose .section-num {
  display: block; font-size: 0.78rem; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--verde); margin-bottom: 0.6rem; margin-top: 2.5rem;
}

/* Cita en bloque (Hayek, Mises, Rothbard) */
.prose .pull-quote {
  margin: 2rem 0; padding: 0.3rem 0 0.3rem 1.5rem;
  border-left: 2px solid var(--rule);
}
.prose .pull-quote p {
  font-size: 1.02rem; font-style: italic; line-height: 1.7; color: var(--ink); margin: 0 0 0.7rem;
}
.prose .pull-quote cite {
  display: block; font-style: italic; font-size: 0.86rem; line-height: 1.5; color: var(--ink-soft);
}

/* Recuadros (capítulo del oro) */
.prose .recuadro {
  margin: 2rem 0; padding: 1.3rem 1.5rem;
  background: var(--surface); border: 1px solid var(--rule); border-radius: 6px;
  page-break-inside: avoid;
}
.prose .recuadro .recuadro-tag {
  display: block; font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--ink-soft); margin-bottom: 0.8rem;
}
.prose .recuadro p {
  font-size: 0.95rem; line-height: 1.7; color: var(--ink-soft); margin: 0 0 0.7rem;
}
.prose .recuadro p:last-child { margin-bottom: 0; }
.prose .recuadro em { font-style: italic; color: var(--ink); }
.prose .recuadro strong { font-weight: 600; color: var(--ink); }

/* Figura (auditabilidad: BlockClock) */
.figura-foto { margin: 2.5rem 0 1.5rem; text-align: center; page-break-inside: avoid; }
.figura-foto img { max-width: 100%; height: auto; border-radius: 6px; border: 1px solid var(--rule); }
.figura-foto figcaption { margin-top: 0.8rem; font-size: 0.88rem; font-style: italic; color: var(--ink-soft); }

/* Limpiar el resaltado de karaoke en papel — los spans .w no aportan visualmente */
.w { background: none !important; box-shadow: none !important; color: inherit !important; }
.w.activa, .w.leida, .w.hl { background: none !important; box-shadow: none !important; color: inherit !important; }

@page { size: A4; margin: 0; }
@media print {
  article.page { page-break-before: always; }
  article.page:first-of-type { page-break-before: avoid; }
  .cover, .toc-wrap { page-break-after: always; }
}
"""


def build_book_html(out_path: Path):
    repo = Path('.')
    index_html = (repo / 'index.html').read_text(encoding='utf-8')
    cover = extract_cover(index_html)
    toc = extract_toc(index_html)

    parts = ['<!DOCTYPE html>\n<html lang="es"><head><meta charset="UTF-8">',
             '<title>Arregla el dinero, arregla el mundo</title>',
             '<style>', PRINT_CSS, '</style></head><body>']
    if cover:
        parts.append(cover)
    if toc:
        parts.append('<div class="toc-wrap">')
        parts.append('<div class="toc-title">Índice</div>')
        parts.append(toc)
        parts.append('</div>')
    for ch in CHAPTERS:
        path = repo / ch
        if not path.exists():
            print(f"  (saltado, no existe: {ch})")
            continue
        html = path.read_text(encoding='utf-8')
        try:
            parts.append(extract_article(html))
        except Exception as e:
            print(f"  ERROR en {ch}: {e}")
    parts.append('</body></html>')
    out_path.write_text(''.join(parts), encoding='utf-8')


def html_to_pdf(html_path: Path, pdf_path: Path):
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.absolute()}",
        f"file://{html_path.absolute()}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    pdf_path = Path(sys.argv[1]) if len(sys.argv) >= 2 else Path('arregla-el-dinero.pdf')
    book_html = Path('.book.html')  # temporal
    print("Construyendo book.html…")
    build_book_html(book_html)
    chars = book_html.stat().st_size
    print(f"  book.html: {chars} bytes ({chars // 1024} KB)")
    print(f"Renderizando con Chrome headless → {pdf_path}…")
    html_to_pdf(book_html, pdf_path)
    book_html.unlink(missing_ok=True)
    size = pdf_path.stat().st_size
    print(f"OK: {pdf_path} ({size // 1024} KB)")


if __name__ == "__main__":
    main()
