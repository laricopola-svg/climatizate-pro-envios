"""Voz en off local (sin internet) con Supertonic 3 — modelo neuronal multilingüe, licencia OpenRAIL-M.

Uso: python3 voz_local.py reels/<ID>/contenido.json reels/<ID>/ [--voz M2] [--velocidad 1.05] [--pasos 10]
Genera reels/<ID>/voz/escena_NN.mp3 + voz.json (mismo formato que voz.py), que kit/reel.py mezcla en el video.

Modelo: carpeta kit/modelos/supertonic3/ (duration_predictor.onnx, text_encoder.onnx, vector_estimator.onnx,
vocoder.onnx, tts.json, unicode_indexer.bin, voice.bin). Si falta, se arma desde npm con:
  python3 kit/voz_local.py --instalar
(descarga los paquetes @3sln/donki-lle-voice-multi*, que redistribuyen los archivos oficiales de Supertone).

Voces: M1–M5 (hombre) y F1–F5 (mujer). Para que suene natural:
- se sintetiza cada escena con su propia frase y una semilla fija (misma voz y timbre en todo el Reel);
- 16 pasos de difusión (más pasos = menos metálico); velocidad 1.08 (ritmo de conversación chilena);
- voz oficial M2 (hombre, grave); pronunciación de términos en inglés corregida (I-Clean → "ai clin", Sleep → "slip").
- texto normalizado: números ya escritos con palabras en el guion, "…" como pausa.
"""
import argparse, json, pathlib, re, subprocess, sys, unicodedata, base64, tarfile, io, urllib.request
import numpy as np

KIT = pathlib.Path(__file__).parent
MOD = KIT / "modelos" / "supertonic3"
VOCES = ["F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"]  # orden dentro de voice.bin (verificado por tono)
PAQ = ["@3sln/donki-lle-voice-multi", "@3sln/donki-lle-voice-multi-2", "@3sln/donki-lle-voice-multi-3"]


def instalar():
    MOD.mkdir(parents=True, exist_ok=True)
    pk = {}
    for p in PAQ:
        meta = json.load(urllib.request.urlopen(f"https://registry.npmjs.org/{p}/0.1.1"))
        tgz = urllib.request.urlopen(meta["dist"]["tarball"]).read()
        pk[f"{p}@0.1.1"] = tarfile.open(fileobj=io.BytesIO(tgz))
    vj = pk[f"{PAQ[0]}@0.1.1"].extractfile("package/voice.js").read().decode()
    cfg = json.loads(vj.split("export default", 1)[1].strip().rstrip(";"))
    for nombre, f in cfg["files"].items():
        datos = b""
        for parte in f["parts"]:
            paquete, resto = parte.rsplit("/c/", 1)
            s = pk[paquete].extractfile(f"package/c/{resto}").read().decode()
            datos += base64.b64decode(s.split('"', 2)[1])
        assert len(datos) == f["size"], nombre
        (MOD / nombre).write_bytes(datos)
    print("OK modelo instalado en", MOD)


class Supertonic:
    def __init__(self):
        import onnxruntime as ort
        o = ort.SessionOptions()
        o.intra_op_num_threads = 4
        s = lambda n: ort.InferenceSession(str(MOD / f"{n}.onnx"), o, providers=["CPUExecutionProvider"])
        self.dp, self.te, self.ve, self.vo = s("duration_predictor"), s("text_encoder"), s("vector_estimator"), s("vocoder")
        cfg = json.loads((MOD / "tts.json").read_text())
        self.sr = cfg["ae"]["sample_rate"]
        self.chunk = cfg["ae"]["base_chunk_size"] * cfg["ttl"]["chunk_compress_factor"]
        self.ldim = cfg["ttl"]["latent_dim"] * cfg["ttl"]["chunk_compress_factor"]
        self.ix = np.fromfile(MOD / "unicode_indexer.bin", dtype=np.int32)
        b = (MOD / "voice.bin").read_bytes()
        h = np.frombuffer(b[:48], dtype=np.int64)
        n, a, c, _, d, e = h
        off = 48
        self.ttl = np.frombuffer(b, np.float32, n * a * c, off).reshape(n, a, c)
        off += n * a * c * 4
        self.dps = np.frombuffer(b, np.float32, n * d * e, off).reshape(n, d, e)

    PRON = [(r"\bI-?CLEAN\b", "ai clin"), (r"\bECO\s?\+", "eco plus"), (r"\bSLEEP\b", "slip"),
            (r"\bWI-?FI\b", "uai fai"), (r"\bBTU\b", "be te u"), (r"\bTURBO\b", "turbo"),
            (r"\bFOLLOW ME\b", "fólou mi"), (r"\bGOLDEN FIN\b", "góulden fin"), (r"\bAPP\b", "app"),
            (r"\+56 9 6190 7601", "más cincuenta y seis, nueve, sesenta y uno, noventa, setenta y seis, cero uno")]

    def texto(self, t, lang):
        for pat, rep in self.PRON:  # cómo se dice en Chile, no cómo se escribe
            t = re.sub(pat, rep, t, flags=re.I)
        t = t.replace("…", "...").replace("“", '"').replace("”", '"').replace("’", "'")
        t = re.sub(r"[\U0001F000-\U0001FAFF☀-➿]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        if t and t[-1] not in ".!?…":
            t += "."
        t = unicodedata.normalize("NFKD", f"<{lang}>{t}</{lang}>")
        ids = np.array([self.ix[ord(ch)] if ord(ch) < len(self.ix) else -1 for ch in t], dtype=np.int64)
        ids = ids[ids >= 0]
        return ids[None, :], np.ones((1, 1, ids.size), np.float32)

    def decir(self, t, voz="M2", lang="es", velocidad=1.08, pasos=16, semilla=7):
        k = VOCES.index(voz)
        ttl, dp = self.ttl[k:k + 1].copy(), self.dps[k:k + 1].copy()
        ids, m = self.texto(t, lang)
        dur = self.dp.run(None, {"text_ids": ids, "style_dp": dp, "text_mask": m})[0] / velocidad
        emb = self.te.run(None, {"text_ids": ids, "style_ttl": ttl, "text_mask": m})[0]
        n_wav = int(dur[0] * self.sr)
        L = (n_wav + self.chunk - 1) // self.chunk
        rng = np.random.default_rng(semilla)
        x = rng.standard_normal((1, self.ldim, L)).astype(np.float32)
        lm = np.ones((1, 1, L), np.float32)
        tot = np.array([pasos], np.float32)
        for i in range(pasos):
            x = self.ve.run(None, {"noisy_latent": x, "text_emb": emb, "style_ttl": ttl, "latent_mask": lm,
                                   "text_mask": m, "current_step": np.array([i], np.float32), "total_step": tot})[0]
        wav = self.vo.run(None, {"latent": x})[0][0][:n_wav]
        return wav.astype(np.float32)


def a_mp3(wav, sr, destino):
    fade = int(0.02 * sr)
    wav = wav.copy()
    wav[:fade] *= np.linspace(0, 1, fade)
    wav[-fade:] *= np.linspace(1, 0, fade)
    p = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                        "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                        "-c:a", "libmp3lame", "-b:a", "160k", str(destino)], input=wav.tobytes())
    if p.returncode:
        raise RuntimeError("ffmpeg mp3")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--voz", default="M2", choices=VOCES)  # voz oficial de Climatízate Pro: M2 (hombre, grave)
    ap.add_argument("--velocidad", type=float, default=1.08)
    ap.add_argument("--pasos", type=int, default=16)
    ap.add_argument("--instalar", action="store_true")
    a = ap.parse_args()
    if a.instalar or not (MOD / "vocoder.onnx").exists():
        instalar()
        if not a.spec:
            return
    spec = json.loads(pathlib.Path(a.spec).read_text())
    tts = Supertonic()
    d = pathlib.Path(a.out) / "voz"
    d.mkdir(parents=True, exist_ok=True)
    res = []
    for i, e in enumerate(spec["escenas"]):
        t = (e.get("voz") or "").strip()
        if not t:
            res.append(None)
            continue
        f = d / f"escena_{i + 1:02d}.mp3"
        a_mp3(tts.decir(t, a.voz, "es", a.velocidad, a.pasos), tts.sr, f)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                   capture_output=True, text=True).stdout)
        res.append({"archivo": f.name, "dur": round(dur, 3)})
    (d / "voz.json").write_text(json.dumps({"motor": "supertonic3", "voz_id": a.voz, "velocidad": a.velocidad,
                                            "pasos": a.pasos, "escenas": res}, indent=1))
    print("OK voz", a.voz, [r and r["dur"] for r in res])


if __name__ == "__main__":
    main()
