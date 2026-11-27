#!/usr/bin/env python3
"""Voz en off de Sara Vibes: mujer latina, cálida y alegre (Piper es_MX 'claude' high).
Uso: python3 tools/voz.py "<texto>" salida.wav [velocidad]
- Descarga el modelo la primera vez (GitHub release de sherpa-onnx) a ~/.cache/saravibes-voz
- Masteriza: limpia graves, calidez, presencia, compresión suave, sala pequeña, -14 LUFS
Dependencias: pip install --break-system-packages piper-tts ; ffmpeg
"""
import os, subprocess, sys, tarfile, tempfile, urllib.request
V = "es_MX-claude-high"
CACHE = os.path.expanduser("~/.cache/saravibes-voz")
URL = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-{V}.tar.bz2"

def modelo():
    m = f"{CACHE}/vits-piper-{V}/{V}.onnx"
    if not os.path.exists(m):
        os.makedirs(CACHE, exist_ok=True)
        tb = f"{CACHE}/v.tar.bz2"
        urllib.request.urlretrieve(URL, tb)
        tarfile.open(tb).extractall(CACHE, filter="data"); os.remove(tb)
    return m

def voz(texto, out, vel=1.0):
    raw = tempfile.mktemp(suffix=".wav")
    # length_scale <1 = más ágil; noise altos = más expresiva y menos plana
    subprocess.run([sys.executable, "-m", "piper", "-m", modelo(), "-f", raw,
                    "--length-scale", str(round(0.93 / vel, 3)), "--noise-scale", "0.75",
                    "--noise-w-scale", "0.9", "--sentence-silence", "0.18"],
                   input=texto.encode(), check=True, capture_output=True)
    af = ("highpass=f=85,lowpass=f=11500,"
          "asetrate=22050*1.025,aresample=44100,atempo=0.9756,"   # +0,4 semitono: más luminosa y alegre
          "equalizer=f=220:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=3,equalizer=f=7000:t=q:w=2:g=-2,"
          "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,"
          "aecho=0.8:0.35:28|46:0.10|0.06,"
          "loudnorm=I=-14:TP=-1.5:LRA=9,apad=pad_dur=0.25")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", "44100", "-ac", "2", out], check=True)
    os.remove(raw)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                       capture_output=True, text=True).stdout.strip()
    print(out, d); return float(d)

if __name__ == "__main__":
    voz(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
