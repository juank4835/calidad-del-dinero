#!/usr/bin/env bash
# Helper de cierre del pipeline: regenera el PDF y el Markdown del libro,
# los agrega al commit del usuario y empuja. Pensado para correrse al final
# de cualquier cambio que modifique el contenido del libro (capítulo nuevo,
# revisión, CSS, índice, etc.).
#
# Uso (dentro del repo):
#   tools/publish.sh "mensaje de commit"
#
# Lo que hace:
#   1. Regenera arregla-el-dinero.pdf con Chrome headless (para imprimir
#      o compartir a lectores humanos)
#   2. Regenera arregla-el-dinero.md (para compartir a IAs en un solo
#      archivo sin contar páginas como imágenes — ideal para Claude/GPT/
#      Gemini que limitan imágenes por chat)
#   3. Hace git add de TODO lo cambiado
#   4. Crea commit con el mensaje recibido
#   5. git push origin main
set -e
cd "$(dirname "$0")/.."

MSG="${1:-Actualización del libro + regeneración del PDF y MD}"

echo "→ Regenerando PDF del libro…"
python3 tools/build_pdf.py

echo "→ Regenerando Markdown del libro…"
python3 tools/build_book_md.py

echo "→ git add + commit + push…"
git add -A
git commit -m "$MSG" 2>&1 | tail -3
git push origin main 2>&1 | tail -3

PDF_KB=$(($(stat -f%z arregla-el-dinero.pdf 2>/dev/null || stat -c%s arregla-el-dinero.pdf) / 1024))
MD_KB=$(($(stat -f%z arregla-el-dinero.md 2>/dev/null || stat -c%s arregla-el-dinero.md) / 1024))
echo ""
echo "✓ PDF en arregla-el-dinero.pdf (${PDF_KB} KB) — para imprimir o compartir a lectores humanos."
echo "✓ MD  en arregla-el-dinero.md  (${MD_KB} KB)  — para subir a IAs (1 archivo, 0 imágenes)."
