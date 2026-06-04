# Operaciones del libro web

Este documento es la memoria operativa del repo. Resume cómo agregar audio + karaoke a un capítulo, cómo actualizar un capítulo cuando solo cambia un párrafo, y los problemas conocidos que ya nos han mordido (con su fix). El objetivo: no volver a tropezar con la misma piedra.

## Estado del libro

- **Voz:** Abel — Reflective, Clear, Expressive (`452WrNT9o8dphaYW5YGU`).
- **Modelo:** `eleven_multilingual_v2`.
- **Voice settings:** `stability=0.65, similarity_boost=0.75, style=0.20, use_speaker_boost=true`.
- **Plan ElevenLabs:** Creator (121k chars/mes). Los audios YA generados están en `audio/` y son tuyos para siempre; cancelar la suscripción no los rompe.
- **Hosting del audio:** dentro del propio repo (carpeta `audio/`), porque GitHub Releases sirve los assets como descarga (`Content-Disposition: attachment`) y eso bloquea la reproducción en navegador.
- **Subrayado y resaltado por palabra:** funcionan en los capítulos con audio. Persistencia local en `localStorage` por capítulo.

## Variables de entorno (archivo `.env`)

```
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxx
```

El `voice_id` y el `model_id` los leen los scripts del entorno:

```bash
export ELEVENLABS_VOICE_ID=452WrNT9o8dphaYW5YGU
export ELEVENLABS_MODEL=eleven_multilingual_v2
```

`.env` está en `.gitignore` — nunca se sube al repo.

## Scripts (en orden de uso típico)

| Script | Para qué |
|---|---|
| `extract_text.py <html>` | Extrae el texto plano de un capítulo HTML (sin tags, sin navs, sin estilos). Es lo que se manda a ElevenLabs. |
| `generate_audio_aligned.py <texto> <salida.mp3>` | Llama al endpoint `/with-timestamps` de ElevenLabs y genera `<salida>.mp3` + `<salida>.alignment.json` con un timestamp por palabra. Si el texto excede 9500 chars, lo parte en chunks y al final corre `ffmpeg -c copy` para que el header del MP3 reporte la duración correcta. |
| `inject_word_spans.py <html>` | Envuelve cada palabra del HTML en `<span class="w" data-w="N">`. El JS de karaoke usa ese índice para resaltar. Tokeniza con regex `\w+(?:[.’']\w+)*` (permite decimales tipo `36.5` y apóstrofes). |
| `splice_audio.py <plan.json>` | Reemplaza un fragmento de audio existente por uno nuevo, sin regenerar todo el capítulo. Útil cuando solo cambian uno o dos párrafos. Mantiene los timestamps del prefix y suffix intactos y re-indexa el alignment. |
| `add_highlights.py <html> [...]` | Aplica el subrayado MVP (amarillo) a uno o varios capítulos. Idempotente (no duplica si ya está aplicado). |
| `install_audio_pill.py`, `upgrade_audio_pill_v2.py` | Scripts que instalaron/actualizaron el reproductor flotante. Ya aplicados a los 3 caps con audio. |

## Flujo A — Agregar audio a un capítulo nuevo

Asumiendo `cap-x.html` ya tiene el contenido del libro listo y vive en la raíz.

```bash
# 1. Extraer texto plano y contar caracteres
python3 tools/extract_text.py cap-x.html > /tmp/cap-x.txt
wc -c /tmp/cap-x.txt   # contar chars antes de gastar créditos

# 2. Generar audio + alineación (ffmpeg auto si hay múltiples chunks)
set -a; source .env; set +a
export ELEVENLABS_VOICE_ID=452WrNT9o8dphaYW5YGU
python3 tools/generate_audio_aligned.py /tmp/cap-x.txt audio/cap-x.mp3

# 3. Limpiar el JSON de alignment con el regex robusto
python3 -c "
import json, re
p = 'audio/cap-x.alignment.json'
d = json.load(open(p))
rx = re.compile(r'\w+(?:[.’\']\w+)*', re.UNICODE)
clean = []
for w in d['words']:
    m = rx.search(w['t'])
    if m:
        clean.append({'i': len(clean), 't': m.group(0), 's': w['s'], 'e': w['e']})
d['words'] = clean
d['word_count'] = len(clean)
open(p,'w',encoding='utf-8').write(json.dumps(d, ensure_ascii=False, separators=(',',':')))
"

# 4. Inyectar spans en el HTML
python3 tools/inject_word_spans.py cap-x.html

# 5. Validar que los conteos cuadran (HTML vs JSON)
words_html=$(grep -oE 'data-w="[0-9]+"' cap-x.html | wc -l)
words_json=$(python3 -c "import json; print(json.load(open('audio/cap-x.alignment.json'))['word_count'])")
echo "$words_html vs $words_json — deben coincidir"

# 6. Instalar la pill (reproductor flotante v2) si el cap no la tiene
#    [usar el patrón de uno de los caps existentes como template]

# 7. Aplicar el subrayado (highlights)
python3 tools/add_highlights.py cap-x.html

# 8. Actualizar audio-manifest.json con hash sha256, word_count, duration

# 9. Commit y push
git add cap-x.html audio/cap-x.mp3 audio/cap-x.alignment.json audio-manifest.json
git commit -m "Agregar audio + karaoke al cap X"
git push origin main
```

## Flujo B — Actualizar un capítulo (uno o dos párrafos cambiaron)

Si el cambio es pequeño, **no regenerar todo el audio**: empalmar solo el fragmento cambiado con `splice_audio.py`. Ahorra ~80–90% de créditos.

1. Diff el texto plano viejo vs nuevo para identificar el rango.
2. Encontrar los índices de palabras en el alignment (la palabra inmediatamente antes del cambio y la inmediatamente después).
3. Armar un `plan.json` con:
   ```json
   {
     "in_mp3":         "audio/cap-x.mp3",
     "in_alignment":   "audio/cap-x.alignment.json",
     "out_mp3":        "audio/cap-x-new.mp3",
     "out_alignment":  "audio/cap-x-new.alignment.json",
     "old_start_idx":  N,
     "old_end_idx":    M,
     "cut_start_seconds": T1,
     "cut_end_seconds":   T2,
     "old_duration_seconds": D,
     "new_fragment_text": "Texto del fragmento nuevo...",
     "previous_text": "≈500 chars de contexto antes",
     "next_text":     "≈500 chars de contexto después"
   }
   ```
4. `python3 tools/splice_audio.py plan.json`
5. Sanity check de las costuras (lo imprime el script).
6. Mover `*-new.{mp3,json}` sobre los originales.
7. En el HTML: quitar los spans `.w` viejos, insertar el párrafo nuevo donde corresponde, re-inyectar spans con `inject_word_spans.py`. Validar que el conteo cuadre con el alignment nuevo.

## Flujo C — Regenerar todo el audio del capítulo

Cuando el cambio es muy grande (más del 30 %), regenerar todo sale más simple que parchar. Sigue el Flujo A reemplazando `audio/cap-x.mp3` (ffmpeg auto en `generate_audio_aligned.py` arregla headers si hay chunks).

## Problemas conocidos y sus fixes (lecciones aprendidas)

### 1. Duración del MP3 reportada incorrectamente cuando hay varios chunks

**Síntoma:** la barra de progreso llega al 100 % a la mitad real del audio. El karaoke deja de avanzar. La duración del `<audio>` que reporta el navegador es menor a la real.

**Causa:** la concatenación binaria con `cat` deja solo el header del primer chunk; el resto de los frames MP3 son auto-descriptivos pero el header global subreporta la duración total.

**Fix permanente:** `generate_audio_aligned.py` corre `ffmpeg -c copy` automáticamente cuando hay más de un chunk (re-empaca el contenedor sin re-codificar, fix instantáneo).

### 2. Click en palabra no salta el audio

**Síntoma:** Click humano en una palabra no cambia el `currentTime` del audio, aunque programáticamente `audio.currentTime = X` sí funcione.

**Causa:** la pill v2 introdujo un wrapper `<span class="g">` (glue) dentro de cada `<span class="w">` para extender el área de selección a la puntuación. El click cae en el `.g`, no en el `.w`. El handler antiguo verificaba `target.classList.contains('w')` y abortaba.

**Fix permanente:** usar `e.target.closest('.w')` en lugar de la verificación directa. Sube por el DOM hasta encontrar el `.w` ancestro.

### 3. `:has()` no funciona consistentemente para CSS de continuidad

**Síntoma:** el subrayado se ve como rectángulos sueltos en vez de una banda continua.

**Causa:** CSS `:has()` aún tiene comportamiento inconsistente en algunos navegadores. La regla `.w.hl:has(+ .w.hl)` no se aplica.

**Fix permanente:** usar padding fijo (`padding: 0 0.5em; margin: 0 -0.5em;`) en todos los `.w.hl`. Cubre el espacio entre palabras y signos de puntuación cortos (`,`, `.`, `:`, `;`, `?`).

### 4. Tokenizer divide `36.5°` en `36` y `5`

**Síntoma:** la validación de conteo HTML vs JSON falla porque el texto plano que mandamos a ElevenLabs trata `36.5` como una palabra, pero el inyector lo dividía.

**Fix permanente:** el regex de `inject_word_spans.py` es `\w+(?:[.’']\w+)*`, que permite punto entre dígitos y apóstrofes internos.

### 5. Palabras con tags inline (`<em>`, `<strong>`, `<span class="term-verde">`)

**Síntoma:** se rompía el HTML con nesting cruzado cuando una palabra estaba parcialmente dentro y parcialmente fuera de un tag inline (ej. `mienten,` donde `mienten` está en `<span class="term-rojo">` y la `,` afuera).

**Fix permanente:** el tokenizer no envuelve palabras cuyo rango contendría un tag completo (`if "<" in content: continue`). La parte alfanumérica sí se envuelve, la puntuación queda sin envolver. Los timestamps siguen siendo consistentes porque el JSON también ignora puntuación adyacente.

### 6. `sed` para modificar JavaScript es peligroso

**Síntoma:** un `sed` mal escrito dejó una línea de JS sintácticamente inválida que rompió todo el karaoke (no solo lo que intentaba cambiar).

**Fix:** para cambios en JS o HTML que involucren patrones complejos, usar **Python con string replacement exacto** en lugar de `sed`. Si hay duda, ejecutar primero con un dry-run que muestre el diff.

### 7. Concat demuxer de ffmpeg con paths relativos

**Síntoma:** `splice_audio.py` falla con `No such file or directory` aunque los archivos existan.

**Causa:** el concat demuxer interpreta los paths del archivo de lista como **relativos al archivo de lista**, no al cwd.

**Fix permanente:** `ffmpeg_concat()` ahora convierte todos los paths a absolutos antes de escribir el archivo de lista.

### 8. Símbolos `°` y `%` no se pronuncian al narrar

**Síntoma:** Abel lee "treinta y seis coma cinco" pero se salta el "°" (en `36.5°`) o el `%` (en `2%`). El audio dice menos de lo que el lector ve.

**Fix permanente:** insertar `<span class="audio-only"> grados</span>` después de `°` y `<span class="audio-only"> por ciento</span>` después de `%`. El CSS oculta visualmente esos spans (`position: absolute; left: -10000px`) pero el extractor sí los lee y los manda a ElevenLabs. Cuando vuelves a inyectar spans, los `<span class="w">` envuelven la palabra "grados"/"por ciento" como cualquier otra palabra, así que el karaoke las resalta brevemente cuando suenan.

### 9. La pill v2 contamina el texto plano con `15`, `0`, `1×`

**Síntoma:** después de extraer el texto plano, el final del archivo trae números sueltos como `15` (botones de skip), `0:00` (tiempo) y `1×` (velocidad). El JSON acaba con esas "palabras" extras y descuadra contra el HTML.

**Fix permanente:** `extract_text.py` ahora elimina cualquier `<aside class="audio-pill">...</aside>` y `<div class="hl-toolbar">` antes de tokenizar. El texto plano queda solo con el contenido del libro.

### 10. Barra de progreso solo permite tap, no drag

**Síntoma:** click en cualquier punto de la barra salta, pero no se puede agarrar el thumb y arrastrarlo.

**Fix permanente:** reemplazar el listener `click` por un bloque que escucha `mousedown` + `mousemove`/`mouseup` en `window` (no en la propia track, para que el drag sobreviva al cursor saliendo de la barra). Soporte `touchstart/move/end` para móvil. Mientras se arrastra, pausar el audio y reanudar al soltar. El thumb se agranda 1.3x con la clase `.dragging` para feedback visual.

## Checklist antes de subir un cambio con audio

- [ ] El conteo HTML (`grep -oE 'data-w="[0-9]+"' cap.html | wc -l`) coincide con el `word_count` del `*.alignment.json`.
- [ ] `afinfo audio/cap.mp3` reporta la duración esperada (no "menor de lo que debería").
- [ ] El HTML es válido (`python3 -c "from html.parser import HTMLParser; ..."`).
- [ ] El audio funciona local: doble click en el MP3, escucharlo.
- [ ] `audio-manifest.json` está actualizado.
- [ ] El click en una palabra al azar en el sitio publicado salta al tiempo correcto.

## URLs útiles

- Sitio: <https://juank4835.github.io/calidad-del-dinero/>
- Repo: <https://github.com/juank4835/calidad-del-dinero>
- ElevenLabs voz Abel: <https://elevenlabs.io/app/voice-library?search=Abel>
- Cuota mensual de la cuenta: <https://elevenlabs.io/app/subscription>
