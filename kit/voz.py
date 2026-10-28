"""Voz en off natural para los Reels (ElevenLabs).

Uso: python3 voz.py reels/<ID>/contenido.json reels/<ID>/
Lee en cada escena el campo "voz" (lo que se dice en esa escena) y genera
reels/<ID>/voz/escena_NN.mp3 + voz.json con la duración de cada audio.
Después, kit/reel.py ajusta la duración de cada escena a su audio y mezcla la voz en el video.

Requiere variables de entorno:
  ELEVENLABS_API_KEY   clave de la cuenta de ElevenLabs (plan con uso comercial)
  ELEVENLABS_VOICE_ID  opcional; por defecto "Adam" (pNInz6obpgDQGcFmaJgB)
Si falta la clave o la API no responde, termina con código 2 y el Reel sale sin voz.

Para que suene real (ajustes probados para narración corta en español):
  - modelo eleven_multilingual_v2; stability 0.42 (más variación = menos robótico),
    similarity 0.80, style 0.30, speaker boost, velocidad 1.05;
  - se envía el texto de la escena anterior y la siguiente (previous_text / next_text)
    para que la entonación fluya entre escenas como una sola locución;
  - guion hablado, no leído: frases cortas, comas donde se respira, palabras de Chile
    ("depa", "la cuenta de la luz", "harto"), números escritos como se dicen ("dieciocho grados").
"""
import json, os, sys, pathlib, subprocess, urllib.request

VOZ_ADAM = "pNInz6obpgDQGcFmaJgB"
AJUSTES = {"stability": 0.42, "similarity_boost": 0.80, "style": 0.30, "use_speaker_boost": True, "speed": 1.05}


def duracion(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def tts(texto, prev, sig, key, voz, destino):
    cuerpo = {"text": texto, "model_id": "eleven_multilingual_v2", "voice_settings": AJUSTES,
              "previous_text": prev or None, "next_text": sig or None}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voz}?output_format=mp3_44100_128",
        data=json.dumps(cuerpo).encode(), method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=90) as r:
        destino.write_bytes(r.read())


def main(spec_path, out):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    key = os.environ.get("ELEVENLABS_API_KEY")
    voz = os.environ.get("ELEVENLABS_VOICE_ID") or spec.get("voz_id") or VOZ_ADAM
    if not key:
        print("SIN_VOZ: falta ELEVENLABS_API_KEY")
        sys.exit(2)
    d = pathlib.Path(out) / "voz"
    d.mkdir(parents=True, exist_ok=True)
    textos = [e.get("voz", "") for e in spec["escenas"]]
    res = []
    try:
        for i, t in enumerate(textos):
            if not t.strip():
                res.append(None)
                continue
            f = d / f"escena_{i + 1:02d}.mp3"
            tts(t, " ".join(textos[:i])[-300:], " ".join(textos[i + 1:])[:300], key, voz, f)
            res.append({"archivo": f.name, "dur": round(duracion(f), 3)})
    except Exception as e:  # red bloqueada, cuota, clave inválida
        print(f"SIN_VOZ: {e}")
        sys.exit(2)
    (d / "voz.json").write_text(json.dumps({"voz_id": voz, "ajustes": AJUSTES, "escenas": res}, indent=1))
    print("OK voz", [r and r["dur"] for r in res])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
