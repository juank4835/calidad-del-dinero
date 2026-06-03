#!/usr/bin/env python3
"""
Genera el audio TTS de un capítulo del libro.
- Lee el texto plano ya extraído (por extract_text.py).
- Si pasa de ~9500 caracteres, lo parte en chunks cortando en
  finales de párrafo y luego de oración, sin partir palabras.
- Llama a ElevenLabs por cada chunk, pasando previous_text/next_text
  para preservar entonación entre cortes.
- Concatena los MP3s resultantes.

Uso:
  generate_audio.py <texto.txt> <salida.mp3>

Variables de entorno:
  ELEVENLABS_API_KEY   (requerida)
  ELEVENLABS_VOICE_ID  (requerida)
  ELEVENLABS_MODEL     (opcional, default eleven_multilingual_v2)
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

MAX_CHARS = 9500   # margen bajo el límite de 10000 de la API
CTX_CHARS = 500    # cuánto contexto pasamos como previous/next


def split_text(text: str, limit: int = MAX_CHARS) -> list[str]:
    """Parte el texto en chunks de máximo `limit` caracteres, cortando
    en final de párrafo (\\n\\n) primero y de oración después."""
    if len(text) <= limit:
        return [text]

    # paso 1: por párrafos
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
            # si un solo párrafo excede el límite, dividir por oraciones
            if len(p) <= limit:
                current = p
            else:
                # split por puntos seguidos de espacio (heurística simple)
                sentences = []
                buf = ""
                for tok in p.replace("? ", "?|SPLIT|").replace("! ", "!|SPLIT|").replace(". ", ".|SPLIT|").split("|SPLIT|"):
                    cand = (buf + " " + tok) if buf else tok
                    if len(cand) <= limit:
                        buf = cand
                    else:
                        if buf:
                            sentences.append(buf)
                        buf = tok
                if buf:
                    sentences.append(buf)
                chunks.extend(sentences[:-1])
                current = sentences[-1] if sentences else ""
    if current:
        chunks.append(current)
    return chunks


def tts(text: str, voice_id: str, api_key: str, model: str,
        previous_text: str = "", next_text: str = "") -> bytes:
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
    if previous_text:
        body["previous_text"] = previous_text
    if next_text:
        body["next_text"] = next_text

    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        raise SystemExit(f"ElevenLabs error {e.code}: {err_body}")


def main():
    if len(sys.argv) < 3:
        print("uso: generate_audio.py <texto.txt> <salida.mp3>", file=sys.stderr)
        sys.exit(1)
    text_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
    model = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
    if not api_key or not voice_id:
        raise SystemExit("Faltan ELEVENLABS_API_KEY o ELEVENLABS_VOICE_ID")

    text = text_path.read_text(encoding="utf-8").strip()
    chunks = split_text(text)
    total_chars = sum(len(c) for c in chunks)
    print(f"Texto: {len(text)} caracteres, partido en {len(chunks)} chunk(s).")
    for i, c in enumerate(chunks, 1):
        print(f"  chunk {i}: {len(c)} chars")

    # Generar cada chunk con contexto
    audio_pieces = []
    for i, chunk in enumerate(chunks):
        prev = chunks[i - 1][-CTX_CHARS:] if i > 0 else ""
        nxt = chunks[i + 1][:CTX_CHARS] if i < len(chunks) - 1 else ""
        print(f"Llamando ElevenLabs para chunk {i+1}/{len(chunks)}...")
        audio_pieces.append(tts(chunk, voice_id, api_key, model, prev, nxt))

    # Concatenar
    with open(out_path, "wb") as out:
        for piece in audio_pieces:
            out.write(piece)
    size_kb = out_path.stat().st_size / 1024
    print(f"OK → {out_path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
