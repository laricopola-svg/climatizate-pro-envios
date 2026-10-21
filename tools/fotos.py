"""Rotación de fotos TeamFS. Uso (desde la raíz del repo):
  python3 tools/fotos.py sugerir cane-corso 6      -> fotos menos usadas de esa carpeta de banco
  python3 tools/fotos.py revisar spec.json FECHA   -> avisa si alguna foto del spec se usó hace < 14 días (portada < 30 días)
  python3 tools/fotos.py registrar spec.json FECHA CARPETA -> anota las fotos usadas en state/fotos_usadas.json
Reglas: ninguna foto se repite en 14 días; la foto de portada no se repite en 30 días; nunca la misma foto en 2 publicaciones del mismo día."""
import sys,json,os,glob,datetime as dt
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));LOG=f"{R}/state/fotos_usadas.json"
def load(): return json.load(open(LOG)) if os.path.exists(LOG) else {}
def photos(spec):
    s=json.load(open(spec));items=s.get("slides") or s.get("clips") or []
    return [(c["photo"],i==0) for i,c in enumerate(items) if c.get("photo")]
def days(a,b): return (dt.date.fromisoformat(b)-dt.date.fromisoformat(a)).days
if __name__=="__main__":
    cmd=sys.argv[1];log=load()
    if cmd=="sugerir":
        fs=sorted(glob.glob(f"{R}/banco/{sys.argv[2]}/*.jpg"))+(sorted(glob.glob(f"{R}/banco/{sys.argv[2]}/**/*.jpg")))
        fs=sorted(set(os.path.relpath(f,R) for f in fs))
        last=lambda f: max([u["fecha"] for u in log.get(f,[])] or ["2000-01-01"])
        for f in sorted(fs,key=lambda f:(last(f),len(log.get(f,[]))))[:int(sys.argv[3]) if len(sys.argv)>3 else 8]: print(f,"última:",last(f) if last(f)!="2000-01-01" else "nunca")
    elif cmd=="revisar":
        fecha=sys.argv[3];bad=0
        for p,cov in photos(sys.argv[2]):
            if p.startswith("marca/"): continue
            for u in log.get(p,[]):
                d=days(u["fecha"],fecha);lim=30 if (cov or u.get("portada")) else 14
                if 0<=d<lim: print(f"REPETIDA: {p} usada {u['fecha']} en {u['carpeta']} ({d} días; mínimo {lim})");bad=1
        print("OK: sin repeticiones" if not bad else "Cambia las fotos marcadas");sys.exit(bad)
    elif cmd=="registrar":
        fecha,carp=sys.argv[3],sys.argv[4]
        for p,cov in photos(sys.argv[2]):
            log.setdefault(p,[]).append({"fecha":fecha,"carpeta":carp,"portada":cov})
        json.dump(log,open(LOG,"w"),ensure_ascii=False,indent=1);print("registrado",carp)
