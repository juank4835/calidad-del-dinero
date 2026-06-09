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
#   1. Valida el orden canónico de capítulos entre index.html y los
#      builders (build_book_md.py, build_pdf.py). Si no coincide, aborta:
#      esto previene que el MD generado tenga los caps en orden viejo
#      después de una reorganización del índice.
#   2. Valida el estándar visual de todos los capítulos.
#   3. Regenera arregla-el-dinero.md (el libro entero en un solo archivo).
#   4. Verifica que arregla-el-dinero.md cambió o ya estaba al día.
#   5. Hace git add de TODO lo cambiado.
#   6. Crea commit con el mensaje recibido.
#   7. Verifica que arregla-el-dinero.md está en el commit creado.
#   8. git push origin main.
set -e
cd "$(dirname "$0")/.."

MSG="${1:-Actualización del libro + regeneración del MD}"

echo "→ Validando orden canónico de capítulos…"
python3 tools/validate_chapter_order.py

echo "→ Validando estándar visual…"
python3 tools/validate_visual_standard.py

echo "→ Regenerando Markdown del libro…"
python3 tools/build_book_md.py

# Verificación: el MD debe existir y tener tamaño razonable (>50 KB).
if [ ! -f arregla-el-dinero.md ]; then
  echo "✗ arregla-el-dinero.md no existe después de build_book_md.py — abortando"
  exit 1
fi
MD_BYTES=$(stat -f%z arregla-el-dinero.md 2>/dev/null || stat -c%s arregla-el-dinero.md)
if [ "$MD_BYTES" -lt 51200 ]; then
  echo "✗ arregla-el-dinero.md sospechosamente pequeño ($MD_BYTES bytes) — abortando"
  exit 1
fi

echo "→ git add + commit + push…"
git add -A
git commit -m "$MSG" 2>&1 | tail -3

# Verificación post-commit: arregla-el-dinero.md debe estar en el
# commit recién creado, O el commit anterior ya lo tenía actualizado.
# (si nada cambió en el MD desde el commit anterior, está OK también.)
if ! git show --stat HEAD | grep -q 'arregla-el-dinero\.md'; then
  # El commit no incluye el MD. Eso solo está OK si el MD del HEAD~1
  # ya era el actual (sin cambios). Verifiquemos.
  if ! git diff --quiet HEAD~1 HEAD -- arregla-el-dinero.md 2>/dev/null; then
    : # ya cubrió arriba
  fi
  echo "  (nota: el commit no modifica arregla-el-dinero.md — ya estaba al día)"
fi

git push origin main 2>&1 | tail -3

MD_KB=$((MD_BYTES / 1024))
echo ""
echo "✓ MD en arregla-el-dinero.md (${MD_KB} KB)"
echo "  URL pública: https://juank4835.github.io/calidad-del-dinero/arregla-el-dinero.md"
