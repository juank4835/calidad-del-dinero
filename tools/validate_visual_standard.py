#!/usr/bin/env python3
"""Valida que cada capítulo cumpla el estándar visual del libro.

Reglas codificadas: ver tools/ESTANDAR_VISUAL.md

Modo de operación:
  - Caps en STANDARD_ALLOWLIST → modo STRICT (errores hacen fail).
  - Resto → modo SOFT (errores se reportan pero NO hacen fail).

Uso:
  validate_visual_standard.py                 → valida todos los caps
  validate_visual_standard.py archivo.html    → valida solo ese archivo
  validate_visual_standard.py --strict-all    → strict para TODOS los caps
                                                (para CI/auditoría)

Exit codes:
  0 → todo OK (o solo warnings en caps soft)
  1 → al menos un cap del allowlist falló

Diseñado para integrarse a tools/publish.sh ANTES del build_book_md y
del git commit. Si un cap del allowlist falla, el push se aborta.
"""
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────────────
# ALLOWLIST: capítulos al estándar (modo strict)
# ──────────────────────────────────────────────────────────────────────
STANDARD_ALLOWLIST = {
    # Bloque I
    "dinero-como-informacion.html",
    "criterio-de-evaluacion.html",
    "tres-formas-organizar-dinero.html",
    # Bloque II
    "preferencia-temporal.html",
    "ahorro-real.html",
    "cuando-un-precio-dice-la-verdad.html",
    # Bloque III
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
    "deforestacion.html",
    "degradacion-alimentaria.html",
}

# Todos los caps del libro (orden canónico) — usado para validar TODO
ALL_CHAPTERS = [
    "dinero-como-informacion.html",
    "criterio-de-evaluacion.html",
    "tres-formas-organizar-dinero.html",
    "preferencia-temporal.html",
    "ahorro-real.html",
    "cuando-un-precio-dice-la-verdad.html",
    "tasa-de-interes.html",
    "asignacion-intertemporal.html",
    "deteccion-mala-inversion.html",
    "precios-relativos.html",
    "predictibilidad-estructural.html",
    "poder-adquisitivo.html",
    "asignacion-credito.html",
    "auditabilidad.html",
    "por-que-no-volver-al-oro.html",
    "el-horizonte-se-acorta.html",
    "deforestacion.html",
    "degradacion-alimentaria.html",
]

# ──────────────────────────────────────────────────────────────────────
# Eyebrow: palabras prohibidas (sufijos de trabajo en curso)
# ──────────────────────────────────────────────────────────────────────
# El eyebrow del libro tiene convenciones ricas por cap:
#   "Bloque I · Fundamentos"
#   "Primera pieza · gravedad crítica"
#   "Antes de seguir · La pregunta inevitable"
#   "Cuarta consecuencia · lo más visible"
# Todas son válidas. Solo prohibimos sufijos que indiquen trabajo
# pendiente o estado provisional que no debería llegar a publicación.
EYEBROW_FORBIDDEN = (
    "corrección",
    "revisión",
    "borrador",
    "wip",
    "draft",
    "todo",
)


# ──────────────────────────────────────────────────────────────────────
# Validador individual de un capítulo
# ──────────────────────────────────────────────────────────────────────
def validate_chapter(html_path: Path) -> tuple[list[str], list[str], dict]:
    """Devuelve (errors, warnings, stats) para un capítulo."""
    errors = []
    warnings = []
    stats = {}

    if not html_path.exists():
        errors.append(f"archivo no existe: {html_path.name}")
        return errors, warnings, stats

    html = html_path.read_text(encoding="utf-8")

    # ── 1. HTML parseable ─────────────────────────────────────────
    class V(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ok = True
            self.errstr = ""
        def error(self, message):
            self.ok = False
            self.errstr = message
    v = V()
    try:
        v.feed(html)
        if not v.ok:
            errors.append(f"HTML inválido: {v.errstr}")
    except Exception as e:
        errors.append(f"HTML inválido: {e}")

    # ── 2. Header del capítulo (orden y unicidad) ─────────────────
    article_m = re.search(r'<article class="page"[^>]*>(.*?)</article>',
                           html, re.DOTALL)
    if not article_m:
        errors.append("no encontré <article class='page'>")
        return errors, warnings, stats
    article = article_m.group(1)

    eyebrow_m = re.search(r'<div class="chapter-eyebrow">(.*?)</div>',
                          article, re.DOTALL)
    title_m = re.search(r'<h1 class="chapter-title">(.*?)</h1>',
                        article, re.DOTALL)
    subtitle_m = re.search(r'<p class="chapter-subtitle">(.*?)</p>',
                            article, re.DOTALL)
    ornament_m = re.search(r'<div class="ornament">', article)
    prose_m = re.search(r'<div class="prose">', article)

    if not eyebrow_m:
        errors.append("falta <div class='chapter-eyebrow'>")
    if not title_m:
        errors.append("falta <h1 class='chapter-title'>")
    if not subtitle_m:
        errors.append("falta <p class='chapter-subtitle'>")
    if not ornament_m:
        errors.append("falta <div class='ornament'>")
    if not prose_m:
        errors.append("falta <div class='prose'>")

    # Solo un h1
    h1_count = len(re.findall(r'<h1\b', article))
    if h1_count > 1:
        errors.append(f"hay {h1_count} <h1>, debe haber exactamente 1")

    # ── 3. Eyebrow sin sufijos de trabajo en curso ─────────────────
    if eyebrow_m:
        eyebrow_text = re.sub(r'<[^>]+>', '', eyebrow_m.group(1)).strip()
        lower = eyebrow_text.lower()
        bad = [w for w in EYEBROW_FORBIDDEN if w in lower]
        if bad:
            errors.append(
                f"eyebrow contiene sufijo prohibido {bad}: '{eyebrow_text}'"
            )
        # Debe tener al menos un caracter
        if not eyebrow_text:
            errors.append("eyebrow está vacío")

    # ── 4. Spans karaoke calzan con alignment ──────────────────────
    slug = html_path.stem
    mp3 = ROOT / "audio" / f"{slug}.mp3"
    json_path = ROOT / "audio" / f"{slug}.alignment.json"

    if json_path.exists():
        try:
            a = json.loads(json_path.read_text())
            align_count = a.get("word_count", 0)
            all_ws = [int(m.group(1))
                      for m in re.finditer(r'data-w="(\d+)"', html)]
            stats["audio_words"] = align_count
            stats["audio_duration_s"] = a.get("duration_seconds", 0)
            stats["html_spans"] = len(all_ws)

            if len(all_ws) != align_count:
                errors.append(
                    f"spans karaoke ({len(all_ws)}) ≠ "
                    f"alignment word_count ({align_count})"
                )
            if all_ws and (min(all_ws) != 0
                           or max(all_ws) != len(all_ws) - 1):
                errors.append(
                    f"data-w no es correlativo desde 0: "
                    f"rango {min(all_ws)}..{max(all_ws)}"
                )
        except Exception as e:
            warnings.append(f"no pude validar alignment: {e}")
    else:
        warnings.append(f"sin alignment JSON ({json_path.name})")

    # ── 5. Coherencia <cite> ↔ no-audio ────────────────────────────
    # Cada <cite> dentro de un blockquote (pull-quote/epigrafe) debe
    # ser coherente con sus spans karaoke:
    #   - Si tiene spans <span class="w" data-w="N"> dentro → se narra,
    #     NO debe tener class="no-audio".
    #   - Si NO tiene spans → no se narra, DEBE tener class="no-audio".
    for m in re.finditer(
        r'<blockquote class="(pull-quote|epigrafe)"[^>]*>(.*?)</blockquote>',
        html, re.DOTALL,
    ):
        bq_cls = m.group(1)
        bq_inner = m.group(2)
        cite_m = re.search(r'<cite\b([^>]*)>(.*?)</cite>',
                           bq_inner, re.DOTALL)
        if cite_m:
            cite_attrs = cite_m.group(1)
            cite_inner = cite_m.group(2)
            has_noaudio = 'no-audio' in cite_attrs
            has_spans = bool(re.search(r'<span class="w" data-w="', cite_inner))
            if has_spans and has_noaudio:
                errors.append(
                    f"<cite> en blockquote.{bq_cls} con spans karaoke "
                    f"PERO también con class='no-audio' (contradictorio)"
                )
            elif not has_spans and not has_noaudio:
                errors.append(
                    f"<cite> en blockquote.{bq_cls} sin spans karaoke "
                    f"NI class='no-audio' (el inyector la procesará "
                    f"como audio pero el alignment no tiene esas palabras)"
                )

    # ── 6. CSS local — blockquote.lema ─────────────────────────────
    has_lema_use = 'class="lema"' in html
    has_lema_css = re.search(r'\bblockquote\.lema\s*\{', html)
    if has_lema_use and not has_lema_css:
        errors.append(
            "usa <blockquote class='lema'> pero NO tiene "
            "CSS local de blockquote.lema (debe vivir en el <style> del cap)"
        )
    stats["lemas"] = len(re.findall(r'<blockquote class="lema"', html))

    # ── 7. CSS local — .prose .epigrafe ────────────────────────────
    has_epig_use = 'class="epigrafe"' in html
    has_epig_css = re.search(r'\.prose\s+\.epigrafe\s*\{', html)
    if has_epig_use and not has_epig_css:
        errors.append(
            "usa <blockquote class='epigrafe'> pero NO tiene "
            "CSS local de .prose .epigrafe"
        )
    stats["epigrafes"] = len(re.findall(r'<blockquote class="epigrafe"', html))

    # ── 8. CSS local — .prose .recuadro (variante hairlines) ───────
    has_recu_use = 'aside class="recuadro"' in html
    has_recu_css = re.search(r'\.prose\s+\.recuadro\s*\{', html)
    if has_recu_use and not has_recu_css:
        errors.append(
            "usa <aside class='recuadro'> pero NO tiene "
            "CSS local de .prose .recuadro"
        )
    if has_recu_use and has_recu_css:
        # Validar que sea variante hairlines (border-top + border-bottom)
        # y NO la variante caja (background var(--surface), border-radius)
        css_block_m = re.search(
            r'\.prose\s+\.recuadro\s*\{([^}]*)\}', html
        )
        if css_block_m:
            css_body = css_block_m.group(1)
            if 'border-radius' in css_body:
                errors.append(
                    "recuadro usa border-radius — debe ser variante "
                    "hairlines (sin caja, sin radius)"
                )
            if 'background: var(--surface)' in css_body or \
               'background:var(--surface)' in css_body:
                errors.append(
                    "recuadro tiene background var(--surface) — debe ser "
                    "variante hairlines (background: none)"
                )
            if 'border-top' not in css_body or 'border-bottom' not in css_body:
                errors.append(
                    "recuadro debe tener border-top + border-bottom "
                    "(variante hairlines)"
                )
    stats["recuadros"] = len(re.findall(r'<aside class="recuadro"', html))

    # ── 9. Sin resaltados de color en palabras del cuerpo ───────────
    # Las clases pueden estar DEFINIDAS en el CSS del esqueleto (no
    # estorban), pero NO deben USARSE en el cuerpo del cap. Filtramos
    # el <style> antes de buscar.
    style_re = re.compile(r'<style[^>]*>.*?</style>', re.DOTALL)
    body_only = style_re.sub('', html)
    term_uses = re.findall(r'<span class="term-(verde|rojo)"', body_only)
    if term_uses:
        errors.append(
            f"usa <span class='term-*'> en el cuerpo ({len(term_uses)} "
            f"ocurrencias) — el estándar no permite resaltado de color "
            f"en palabras"
        )

    # ── 10. pull-quotes — stats ─────────────────────────────────────
    stats["pull_quotes"] = len(re.findall(
        r'<blockquote class="pull-quote"', html
    ))

    return errors, warnings, stats


# ──────────────────────────────────────────────────────────────────────
# Reporte
# ──────────────────────────────────────────────────────────────────────
def format_report(filename: str, errors: list[str], warnings: list[str],
                  stats: dict, strict: bool) -> tuple[str, bool]:
    """Formatea reporte. Devuelve (texto, hizo_fail)."""
    if not errors and not warnings:
        meta_parts = []
        if "audio_words" in stats:
            meta_parts.append(f"{stats['audio_words']} palabras")
            meta_parts.append(f"{stats['audio_duration_s']:.0f}s audio")
        meta = ", ".join(meta_parts) if meta_parts else ""
        marker = "✓" if strict else "·"
        return f"  {marker} {filename}  ({meta})", False

    lines = []
    if errors:
        marker = "✗" if strict else "⚠"
        mode = "FAIL" if strict else "warn"
        lines.append(f"  {marker} {filename}  [{mode}]")
        for e in errors:
            lines.append(f"      ✗ {e}")
        for w in warnings:
            lines.append(f"      · {w}")
        return "\n".join(lines), strict  # fail solo si strict

    if warnings:
        lines.append(f"  · {filename}  (warnings)")
        for w in warnings:
            lines.append(f"      · {w}")
        return "\n".join(lines), False

    return "", False


def main():
    args = sys.argv[1:]
    strict_all = "--strict-all" in args
    args = [a for a in args if a != "--strict-all"]

    if args:
        targets = [Path(a).name for a in args]
    else:
        targets = ALL_CHAPTERS

    print("Validando estándar visual del libro…")
    print(f"  allowlist (strict): {len(STANDARD_ALLOWLIST)} caps")
    if strict_all:
        print("  modo: STRICT-ALL (todos los caps deben pasar)")
    print()

    any_fail = False
    standard_count = 0
    soft_warn_count = 0
    strict_count = 0

    for fname in targets:
        path = ROOT / fname
        is_strict = strict_all or (fname in STANDARD_ALLOWLIST)
        errors, warnings, stats = validate_chapter(path)

        report, fails = format_report(fname, errors, warnings, stats, is_strict)
        print(report)

        if fails:
            any_fail = True
            strict_count += 1
        elif errors or warnings:
            soft_warn_count += 1
        else:
            standard_count += 1

    print()
    print(f"Resumen: {standard_count} OK, "
          f"{soft_warn_count} con avisos (soft), "
          f"{strict_count} fallos (strict)")

    if any_fail:
        print("\n✗ FAIL: al menos un cap del allowlist no cumple "
              "el estándar. Aborto.")
        sys.exit(1)
    else:
        print("\n✓ Validación OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
