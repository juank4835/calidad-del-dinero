#!/usr/bin/env python3
"""Inserta silencio después de cada título de sección (span.section-num) para
darle una pausa clara al narrador, SIN regenerar el audio (cero cuota de TTS).

Cómo funciona:
  1. Localiza los bloques <span class="section-num"> en el HTML (con balanceo
     de <span> anidados) y saca el índice de la ÚLTIMA palabra de cada título.
  2. Para cada título mide el gap actual (fin del título → inicio de la
     siguiente palabra) y calcula cuánto silencio agregar para llegar a TARGET.
  3. Corta el MP3 en el punto medio del gap, intercala un silencio de esa
     duración, y reconcatena (ffmpeg, rutas absolutas).
  4. Recalcula el alignment: cada palabra cuyo índice es mayor que el último
     índice del título se corre por la suma de los silencios insertados antes.

El número de palabras NO cambia → los data-w del HTML siguen calzando 1:1.

Uso:
  insert_title_pauses.py <html> <mp3> <alignment.json> [target_ms]
"""
import json, re, subprocess, sys
from pathlib import Path

TARGET_MS = 1000   # gap total deseado después de cada título
MIN_INSERT_MS = 50 # si ya hay >= TARGET-50, no insertar nada


def section_blocks(html):
    """Devuelve el HTML interior de cada span.section-num, con balanceo."""
    out = []
    for m in re.finditer(r'<span class="section-num">', html):
        i = m.end(); depth = 1
        for t in re.finditer(r'<span\b[^>]*>|</span>', html[i:]):
            depth += 1 if not t.group().startswith('</') else -1
            if depth == 0:
                out.append(html[i:i + t.start()]); break
    return out


def probe_dur(path):
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)]).decode().strip())


def extract(src, t0, t1, dst):
    """Cortar [t0,t1] de src → dst. Si t1 es None corta hasta el final.

    Intenta primero re-encode con libmp3lame (formato uniforme); si falla
    —p.ej. por «inadequate AVFrame plane padding», un bug que se dispara con
    frames mal formateados al final del MP3— cae a -c copy + re-encode en dos
    pasadas, que es robusto al problema.
    """
    base = ["ffmpeg", "-y", "-i", str(src), "-ss", f"{t0:.3f}"]
    if t1 is not None:
        base += ["-to", f"{t1:.3f}"]
    try:
        subprocess.run(
            base + ["-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "1", str(dst)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return
    except subprocess.CalledProcessError:
        pass
    # fallback: cortar con -c copy primero, después re-encodear el bloque ya recortado
    tmp = dst.with_suffix(".copy.mp3")
    subprocess.run(
        base + ["-c", "copy", str(tmp)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(tmp),
         "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "1", str(dst)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    tmp.unlink(missing_ok=True)


def silence(dur, dst):
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
         "-t", f"{dur:.3f}", "-c:a", "libmp3lame", "-b:a", "128k", str(dst)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def concat(parts, dst):
    listfile = dst.parent / "concat_pauses.txt"
    listfile.write_text("\n".join(f"file '{Path(p).resolve()}'" for p in parts) + "\n")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
             "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "1", str(dst)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        listfile.unlink(missing_ok=True)


def main():
    html_path, mp3_path, align_path = map(Path, sys.argv[1:4])
    target = (int(sys.argv[4]) if len(sys.argv) > 4 else TARGET_MS) / 1000.0

    html = html_path.read_text(encoding="utf-8")
    align = json.loads(align_path.read_text())
    words = align["words"]

    # Boundaries: (last_idx, insert_time, insert_dur)
    bounds = []
    for b in section_blocks(html):
        idxs = [int(x) for x in re.findall(r'data-w="(\d+)"', b)]
        if not idxs:
            continue
        last = max(idxs)
        if last + 1 >= len(words):
            continue
        end_t = words[last]["e"]
        nxt_s = words[last + 1]["s"]
        gap = nxt_s - end_t
        add = target - gap
        if add < MIN_INSERT_MS / 1000.0:
            print(f"  · w{last} '{words[last]['t']}' gap={gap*1000:.0f}ms ya OK, sin cambio")
            continue
        # Cortar JUSTO en el onset de la siguiente palabra: así el título queda
        # entero (no se recorta su cola) y la siguiente palabra entra completa.
        t_ins = nxt_s
        bounds.append((last, t_ins, add))
        print(f"  + w{last} '{words[last]['t']}' gap={gap*1000:.0f}ms → +{add*1000:.0f}ms (corte @{t_ins:.2f}s)")

    if not bounds:
        print("Nada que insertar."); return

    bounds.sort(key=lambda x: x[1])
    work = mp3_path.parent / ".pause_work"
    work.mkdir(exist_ok=True)

    # Construir lista de partes: seg0, sil0, seg1, sil1, ..., segN
    total = probe_dur(mp3_path)
    cut_times = [t for _, t, _ in bounds]
    parts = []
    prev = 0.0
    for k, (_, t_ins, add) in enumerate(bounds):
        seg = work / f"seg{k}.mp3"; extract(mp3_path, prev, t_ins, seg); parts.append(seg)
        sil = work / f"sil{k}.mp3"; silence(add, sil); parts.append(sil)
        prev = t_ins
    last_seg = work / f"seg{len(bounds)}.mp3"; extract(mp3_path, prev, None, last_seg); parts.append(last_seg)

    concat(parts, mp3_path)
    new_dur = probe_dur(mp3_path)
    print(f"\naudio: {total:.1f}s → {new_dur:.1f}s (+{new_dur-total:.1f}s)")

    # Recalcular tiempos: shift acumulado por índice
    def shift_for(idx):
        return sum(add for last, _, add in bounds if last < idx)
    for w in words:
        s = shift_for(w["i"])
        w["s"] = round(w["s"] + s, 3)
        w["e"] = round(w["e"] + s, 3)
    align["duration_seconds"] = new_dur
    align_path.write_text(json.dumps(align, ensure_ascii=False, separators=(",", ":")))
    print(f"alignment recalculado: {len(words)} palabras, dur {new_dur:.1f}s")

    # limpiar
    for p in parts:
        p.unlink(missing_ok=True)
    work.rmdir()


if __name__ == "__main__":
    main()
