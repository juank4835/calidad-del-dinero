#!/usr/bin/env bash
# Helper de cierre del pipeline: regenera el Markdown del libro, lo agrega al
# commit del usuario y empuja. Pensado para correrse al final de cualquier
# cambio que modifique el contenido del libro (capítulo nuevo, revisión,
# CSS, índice, etc.).
#
# Por qué solo MD y no PDF:
#   El deliverable principal del libro es la web (GitHub Pages, capítulo
#   por capítulo, con audio karaoke). El MD es el deliverable secundario,
#   pensado para subir el libro entero a IAs (Claude/GPT/Gemini) sin que
#   cuenten cada página como imagen. El PDF se descartó del pipeline
#   porque (1) la web ya cubre el caso de lectura humana, (2) el PDF
#   bloquea a las IAs al consumir su cuota de imágenes.
#
# Si en algún momento se necesita un PDF puntual, correr:
#   python3 tools/build_pdf.py
#
# Uso (dentro del repo):
#   tools/publish.sh "mensaje de commit"
#
# Lo que hace:
#   1. Regenera arregla-el-dinero.md (el libro entero en un solo archivo)
#   2. Hace git add de TODO lo cambiado
#   3. Crea commit con el mensaje recibido
#   4. git push origin main
set -e
cd "$(dirname "$0")/.."

MSG="${1:-Actualización del libro + regeneración del MD}"

echo "→ Validando estándar visual…"
python3 tools/validate_visual_standard.py

echo "→ Regenerando Markdown del libro…"
python3 tools/build_book_md.py

echo "→ git add + commit + push…"
git add -A
git commit -m "$MSG" 2>&1 | tail -3
git push origin main 2>&1 | tail -3

MD_KB=$(($(stat -f%z arregla-el-dinero.md 2>/dev/null || stat -c%s arregla-el-dinero.md) / 1024))
echo ""
echo "✓ MD en arregla-el-dinero.md (${MD_KB} KB)"
echo "  URL pública: https://juank4835.github.io/calidad-del-dinero/arregla-el-dinero.md"
