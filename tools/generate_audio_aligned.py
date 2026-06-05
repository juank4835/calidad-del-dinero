#!/usr/bin/env python3
"""
Genera audio TTS + alineación por palabra para un capítulo.
Usa el endpoint /with-timestamps de ElevenLabs.

Si el texto excede el límite de la API (~10k chars), parte en chunks
y compone tanto el audio (cat binario) como los timestamps (offseteando
el tiempo del 2º chunk por la duración del 1º).

Output:
  - <salida.mp3>
  - <salida.alignment.json>   con lista de palabras y sus tiempos

Variables de entorno:
  ELEVENLABS_API_KEY
  ELEVENLABS_VOICE_ID
  ELEVENLABS_MODEL  (default: eleven_multilingual_v2)
"""
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

MAX_CHARS = 6000
CTX_CHARS = 500


def split_text(text: str, limit: int = MAX_CHARS) -> list[str]:
    if len(text) <= limit:
        return [text]
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for p in paragraphs:
        candidate = (current + "\n\n" + p) if current else p
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(p) <= limit:
                current = p
            else:
                sentences = re.split(r"(?<=[\.\!\?])\s+", p)
                buf = ""
                for s in sentences:
                    cand = (buf + " " + s) if buf else s
                    if len(cand) <= limit:
                        buf = cand
                    else:
                        if buf:
                            chunks.append(buf)
                        buf = s
                if buf:
                    current = buf
                else:
                    current = ""
    if current:
        chunks.append(current)
    return chunks


def tts_with_timestamps(text, voice_id, api_key, model, prev_text="", next_text=""):
    body = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.65,
            "similarity_boost": 0.75,
            "style": 0.20,
            "use_speaker_boost": True,
        },
    }
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text

    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"ElevenLabs error {e.code}: {e.read().decode()}")


def chars_to_words(characters, starts, ends):
    """Agrupa caracteres en palabras. Una palabra es una secuencia
    contigua de caracteres no-whitespace. Devuelve [{text, start, end}]."""
    words = []
    buf_chars = []
    buf_starts = []
    buf_ends = []

    def flush():
        if not buf_chars:
            return
        word_text = "".join(buf_chars)
        if word_text.strip():
            words.append({
                "text": word_text,
                "start": buf_starts[0],
                "end": buf_ends[-1],
            })
        buf_chars.clear()
        buf_starts.clear()
        buf_ends.clear()

    for ch, s, e in zip(characters, starts, ends):
        if ch.isspace() or ch == "\n":
            flush()
        else:
            buf_chars.append(ch)
            buf_starts.append(s)
            buf_ends.append(e)
    flush()
    return words


def main():
    if len(sys.argv) < 3:
        print("uso: generate_audio_aligned.py <texto.txt> <salida.mp3>", file=sys.stderr)
        sys.exit(1)
    text_path = Path(sys.argv[1])
    mp3_path = Path(sys.argv[2])
    json_path = mp3_path.with_suffix(".alignment.json")
    mp3_path.parent.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
    model = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
    if not api_key or not voice_id:
        raise SystemExit("Faltan ELEVENLABS_API_KEY o ELEVENLABS_VOICE_ID")

    text = text_path.read_text(encoding="utf-8").strip()
    chunks = split_text(text)
    print(f"Texto: {len(text)} chars en {len(chunks)} chunk(s).")
    for i, c in enumerate(chunks, 1):
        print(f"  chunk {i}: {len(c)} chars")

    all_audio_bytes = b""
    all_words = []
    time_offset = 0.0

    for i, chunk in enumerate(chunks):
        prev = chunks[i - 1][-CTX_CHARS:] if i > 0 else ""
        nxt = chunks[i + 1][:CTX_CHARS] if i < len(chunks) - 1 else ""
        print(f"Llamando ElevenLabs (with-timestamps) {i+1}/{len(chunks)}...")
        resp = tts_with_timestamps(chunk, voice_id, api_key, model, prev, nxt)

        audio_bytes = base64.b64decode(resp["audio_base64"])
        all_audio_bytes += audio_bytes

        align = resp["alignment"]
        words = chars_to_words(
            align["characters"],
            align["character_start_times_seconds"],
            align["character_end_times_seconds"],
        )
        # offsetear tiempos por la duración acumulada de chunks anteriores
        for w in words:
            w["start"] += time_offset
            w["end"] += time_offset
        all_words.extend(words)

        # avanzar offset por la duración del audio de este chunk
        # (último end_time del alignment es una buena aproximación)
        if align["character_end_times_seconds"]:
            time_offset += align["character_end_times_seconds"][-1]

    # Guardar MP3 (concatenación binaria)
    with open(mp3_path, "wb") as f:
        f.write(all_audio_bytes)

    # Si hubo múltiples chunks, el header del MP3 concatenado reporta
    # mal la duración (solo cuenta el primer chunk). Re-empacar con
    # ffmpeg (sin recodificar) arregla los headers.
    if len(chunks) > 1 and shutil.which("ffmpeg"):
        tmp_out = mp3_path.with_suffix(".tmp.mp3")
        subprocess.run(
            ["ffmpeg", "-i", str(mp3_path), "-c", "copy", "-y", str(tmp_out)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        tmp_out.replace(mp3_path)
        print(f"(headers re-empacados con ffmpeg, duración correcta)")

    # Guardar alignment JSON
    out = {
        "duration_seconds": time_offset,
        "word_count": len(all_words),
        "words": [
            {"i": idx, "t": w["text"], "s": round(w["start"], 3), "e": round(w["end"], 3)}
            for idx, w in enumerate(all_words)
        ],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    print(f"OK: {mp3_path} ({mp3_path.stat().st_size // 1024} KB)")
    print(f"OK: {json_path} ({json_path.stat().st_size // 1024} KB, {len(all_words)} palabras)")


if __name__ == "__main__":
    main()
