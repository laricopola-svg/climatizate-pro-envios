#!/usr/bin/env python3
"""Voz en off de Sara Vibes: mujer, natural y fluida (Supertonic 3, multilingüe, vía sherpa-onnx).
Uso: python3 tools/voz.py "<texto>" salida.wav [velocidad] [voz]
- voz = id de hablante 0-4 (mujeres). Por defecto VOZ_SARA (env) o 1.
- Descarga el modelo la primera vez (GitHub release de sherpa-onnx) a ~/.cache/saravibes-voz
- "Sara Vibes" se pronuncia en inglés: el texto se adapta solo ("Sara Vaibs").
- Mezcla mínima (sin efectos que la hagan sonar metálica): limpieza de graves, compresión suave y -14 LUFS.
Dependencias: pip install --break-system-packages sherpa-onnx soundfile ; ffmpeg
"""
import os, re, subprocess, sys, tarfile, tempfile, urllib.request
M = "sherpa-onnx-supertonic-3-tts-int8-2026-05-11"
CACHE = os.path.expanduser("~/.cache/saravibes-voz")
URL = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/{M}.tar.bz2"

def carpeta():
    d = f"{CACHE}/{M}"
    if not os.path.exists(f"{d}/voice.bin"):
        os.makedirs(CACHE, exist_ok=True); tb = f"{CACHE}/m.tar.bz2"
        urllib.request.urlretrieve(URL, tb); tarfile.open(tb).extractall(CACHE, filter="data"); os.remove(tb)
    return d

def preparar(t):
    t = re.sub(r"Sara Vibes", "Sara Vaibs", t, flags=re.I)
    t = t.replace("WhatsApp", "guasap").replace("pyme", "pyme").replace("…", ",")
    return t

def deps():
    try:
        import sherpa_onnx, soundfile  # noqa
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "sherpa-onnx", "soundfile"], check=True)

def voz(texto, out, vel=1.0, sid=None):
    deps()
    import sherpa_onnx, soundfile as sf
    sid = int(sid if sid is not None else os.environ.get("VOZ_SARA", 1))
    d = carpeta()
    tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        supertonic=sherpa_onnx.OfflineTtsSupertonicModelConfig(
            duration_predictor=f"{d}/duration_predictor.int8.onnx", text_encoder=f"{d}/text_encoder.int8.onnx",
            vector_estimator=f"{d}/vector_estimator.int8.onnx", vocoder=f"{d}/vocoder.int8.onnx",
            tts_json=f"{d}/tts.json", unicode_indexer=f"{d}/unicode_indexer.bin", voice_style=f"{d}/voice.bin"),
        num_threads=4, provider="cpu")))
    g = sherpa_onnx.GenerationConfig(); g.sid = sid; g.num_steps = 16; g.speed = vel; g.extra["lang"] = "es"
    a = tts.generate(preparar(texto), g)
    raw = tempfile.mktemp(suffix=".wav"); sf.write(raw, a.samples, samplerate=a.sample_rate)
    af = "highpass=f=70,acompressor=threshold=-22dB:ratio=2:attack=10:release=150:makeup=1,loudnorm=I=-14:TP=-1.5:LRA=11,apad=pad_dur=0.25"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", "44100", "-ac", "2", out], check=True)
    os.remove(raw)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                         capture_output=True, text=True).stdout.strip()
    print(out, dur); return float(dur)

if __name__ == "__main__":
    a = sys.argv
    voz(a[1], a[2], float(a[3]) if len(a) > 3 else 1.0, a[4] if len(a) > 4 else None)
