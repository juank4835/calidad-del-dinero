#!/usr/bin/env bash
# Helper de cierre del pipeline: regenera el PDF del libro, lo agrega al
# commit del usuario y empuja. Pensado para correrse al final de cualquier
# cambio que modifique el contenido del libro (capítulo nuevo, revisión,
# CSS, índice, etc.).
#
# Uso (dentro del repo):
#   tools/publish.sh "mensaje de commit"
#
# Lo que hace:
#   1. Regenera arregla-el-dinero.pdf con Chrome headless
#   2. Hace git add de TODO lo cambiado (incluido el PDF)
#   3. Crea commit con el mensaje recibido
#   4. git push origin main
set -e
cd "$(dirname "$0")/.."

MSG="${1:-Actualización del libro + regeneración del PDF}"

echo "→ Regenerando PDF del libro…"
python3 tools/build_pdf.py

echo "→ git add + commit + push…"
git add -A
git commit -m "$MSG" 2>&1 | tail -3
git push origin main 2>&1 | tail -3

KB=$(($(stat -f%z arregla-el-dinero.pdf 2>/dev/null || stat -c%s arregla-el-dinero.pdf) / 1024))
echo ""
echo "✓ PDF en arregla-el-dinero.pdf (${KB} KB) — listo para compartir."
