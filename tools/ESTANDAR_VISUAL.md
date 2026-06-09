# Estándar visual del libro

Documento de referencia normativo para todos los capítulos de
«Arregla el dinero, arregla el mundo». Las reglas aquí están
consolidadas a partir de los capítulos 1, 2 y 3 (de referencia,
ya conformes). El validador `tools/validate_visual_standard.py`
verifica que cada capítulo cumpla estas reglas y aborta el
`publish.sh` si un cap del allowlist no las cumple.

---

## 1. Header del capítulo (obligatorio, mismo orden siempre)

```html
<article class="page" id="contenido" tabindex="-1">
  <div class="chapter-eyebrow">Bloque N · NombreBloque</div>
  <h1 class="chapter-title">Título del capítulo</h1>
  <p class="chapter-subtitle">Subtítulo o ancla del cap</p>
  <div class="ornament">• • •</div>
  <div class="prose">
    …
  </div>
</article>
```

### Reglas
- El orden eyebrow → h1 → subtitle → ornament → prose es **obligatorio**.
- Eyebrow es libre en convención (el libro usa varias formas válidas):
  - `Bloque I · Fundamentos`
  - `Primera pieza · gravedad crítica` / `Tercera pieza · gravedad alta`
  - `Antes de seguir · La pregunta inevitable`
  - `Cuarta consecuencia · lo más visible`
  - `La pieza que las sostiene a todas` (auditabilidad, sin numeración)
- **Prohibido**: sufijos de trabajo en curso. El eyebrow no puede contener
  las palabras: `corrección`, `revisión`, `borrador`, `wip`, `draft`, `todo`
  (case-insensitive).
- El `<h1>` debe ser el ÚNICO `<h1>` del cap (no usar h1 en el cuerpo).
- El subtítulo es un único `<p>`, no múltiples.

---

## 2. Epígrafe (opcional — cita inicial del cap)

Si el cap abre con una cita ajena (ej.: Hayek, Mises, Rothbard), va
**dentro del `<div class="prose">`**, antes del lead.

```html
<blockquote class="epigrafe">
  <p>«Texto de la cita…»</p>
  <cite class="no-audio">Autor, <em>Obra</em> (año)</cite>
</blockquote>
```

### Reglas
- Va dentro del prose, antes del `<p class="lead">`.
- El texto del `<p>` SÍ se narra (entra al karaoke).
- La atribución `<cite>` NO se narra: debe llevar `class="no-audio"`.
- Cap puede tener máximo **uno** epígrafe.
- El CSS de `.prose .epigrafe` vive **local en el `<style>` del cap** (NO en el esqueleto).

### CSS canónico
```css
.prose .epigrafe {
  margin: 0 0 3.5rem;
  padding: 0 1.5rem;
  border-left: none;
}
.prose .epigrafe p {
  font-size: 1rem; font-style: italic; line-height: 1.6;
  color: var(--ink-soft); margin: 0 0 0.8rem;
}
.prose .epigrafe cite {
  display: block; text-align: right; font-style: italic;
  font-size: 0.85rem; color: var(--ink-soft); margin-top: 0.4rem;
}
.prose .epigrafe cite::before { content: "— "; }
```

---

## 3. Máxima del autor (frase rectora destacada)

Frase corta, en voz del autor, que captura una idea-eje del cap.

```html
<blockquote class="lema">El dinero no se crea de la nada: se produce.</blockquote>
```

### Reglas
- Cap puede tener **0, 1 o más** máximas.
- Se narra completa.
- NO lleva `<cite>` (no es una cita ajena).
- El CSS de `blockquote.lema` vive **local en el `<style>` del cap**, NO en el esqueleto (decisión consolidada del autor).

### CSS canónico
```css
blockquote.lema {
  margin: 2.8rem 0; padding: 1.4rem 1rem;
  border-left: none;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
  text-align: center; font-style: italic;
  font-size: 1.18rem; line-height: 1.5; color: var(--ink);
}
```

---

## 4. Cita de autor (cita intermedia en la prosa)

Citas de Hayek, Mises, Rothbard u otros, intercaladas en el cuerpo
del cap como evidencia argumentativa.

```html
<blockquote class="pull-quote">
  <p>«Texto de la cita…»</p>
  <cite class="no-audio">Autor, <em>Obra</em> (año)</cite>
</blockquote>
```

### Reglas
- El texto SÍ se narra (entra al karaoke).
- La atribución `<cite>` puede narrarse o no, según decisión editorial del cap:
  - Si la atribución se narra → tiene spans `<span class="w" data-w="N">` adentro y **NO** lleva `class="no-audio"`.
  - Si la atribución NO se narra → **DEBE** llevar `class="no-audio"` (para que el inyector la salte y el alignment no se rompa).
- Convención por defecto: si el párrafo de la prosa ANTES de la cita ya nombra al autor y la obra, la atribución va `no-audio` para no repetir. Si no los nombra, se narra.
- El CSS de `blockquote.pull-quote` vive en el **esqueleto** (`tres-regimenes.html`), heredado por todos los caps.
- **Audio**: cuando se regenera la cita con `splice_audio.py`, usar `voice_settings` ajustados:
  - `stability`: 0.80 (más sereno, pausado)
  - `style`: 0.40 (más enfático, presencia interpretativa)
  - `similarity_boost`: 0.75 (sin cambio — preserva timbre)
  - Esto da la cadencia de «alguien que baja el ritmo para citar» sin cambiar de voz.

---

## 5. Recuadro de resumen / síntesis

Caja de cierre del cap (o de una sección) con un resumen sintético.

```html
<aside class="recuadro">
  <span class="recuadro-tag">En síntesis</span>
  <p>Intro del recuadro…</p>
  <p><strong>Término 1</strong> — descripción.<br>
     <strong>Término 2</strong> — descripción.<br>
     <strong>Término 3</strong> — descripción.</p>
</aside>
```

### Reglas
- Se narra completo (tag, intro y líneas).
- Términos clave en `<strong>` para énfasis visual.
- Líneas separadas con `<br>` (no múltiples `<p>` para las opciones).
- Cap puede tener máximo **uno** recuadro de cierre (no se duplica).
- El CSS de `.prose .recuadro` vive **local en el `<style>` del cap**.
- **Estilo obligatorio**: variante hairlines (border-top + border-bottom, sin background).

### CSS canónico
```css
.prose .recuadro {
  margin: 3rem 0 1rem; padding: 1.5rem 0;
  background: none;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
.prose .recuadro .recuadro-tag {
  display: block; text-align: center;
  font-size: 0.68rem; letter-spacing: 0.28em;
  text-transform: uppercase; color: var(--ink-soft);
  margin-bottom: 1rem;
}
.prose .recuadro p { margin: 0 0 0.7rem; }
.prose .recuadro p:last-child { margin: 0; }
```

---

## 6. Palabras en el cuerpo: SIN resaltados de color

**Regla**: en la prosa narrativa del libro NO se usan resaltados de
color en palabras individuales. Esto incluye específicamente:

- `<span class="term-verde">…</span>` (color naranja `#FF7A18`)
- `<span class="term-rojo">…</span>` (gris)
- Cualquier otra clase `term-*` con color

Estas clases pueden quedar **definidas en el CSS** del esqueleto
(no estorban si no se usan), pero **no deben aparecer en el cuerpo
de ningún cap**. La razón: en los caps 1–3 (referencia) se decidió
que el énfasis se logra con la voz del texto, no con marcas
tipográficas que rompen el flujo lector.

Para énfasis legítimos siguen disponibles:
- `<em>` → cursiva
- `<strong>` → negrita

Pero úsalos sólo cuando aclaran; no para decorar.

---

## 7. Audio y karaoke (sin excepciones)

### Reglas
- Cada cap tiene MP3 (`audio/<slug>.mp3`) + alignment JSON (`audio/<slug>.alignment.json`).
- Cada palabra narrada va envuelta en `<span class="w" data-w="N">palabra</span>`.
- Los `data-w` son **correlativos** desde 0 sin saltos.
- El **conteo de spans** del cap = **word_count del alignment JSON**.
- Bloques no narrados (`<cite>` con atribución, asides técnicos como `<aside class="audio-pill">`) llevan `class="no-audio"` para que el inyector los salte.

---

## 8. CSS — qué vive dónde

| Regla | Vive en | Notas |
|---|---|---|
| `chapter-eyebrow`, `chapter-title`, `chapter-subtitle`, `ornament` | Esqueleto | Heredado por todos los caps |
| `blockquote.pull-quote` | Esqueleto | Heredado |
| `blockquote.lema` | **Local** en cada cap que lo use | Decisión consolidada |
| `.prose .epigrafe` | **Local** en cada cap que lo use | |
| `.prose .recuadro` | **Local** en cada cap que lo use | Variante hairlines obligatoria |

El esqueleto canónico es `tres-regimenes.html`. Cualquier regla
añadida al esqueleto se hereda automáticamente por todos los caps
generados con los builders.

---

## 9. Capítulos de referencia (allowlist)

Los siguientes caps están al estándar y **el validador los chequea
en modo strict**: si fallan, el `publish.sh` aborta.

- `dinero-como-informacion.html` (cap 1)
- `criterio-de-evaluacion.html` (cap 2)
- `tres-formas-organizar-dinero.html` (cap 3)

Los caps **fuera** de la allowlist se chequean en modo soft (warnings
en pantalla, sin abortar). A medida que homogeneicemos un cap, se
agrega a esta lista.

La allowlist está hard-coded en `tools/validate_visual_standard.py`
(constante `STANDARD_ALLOWLIST`). Para agregar un cap, editar la
constante y correr el validador para confirmar que pasa.
