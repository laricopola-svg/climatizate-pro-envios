"""TeamFS Reel/TikTok video generator (1080x1920, 30fps, H.264 + silent AAC).
Usage: python3 tools/make_reel.py spec.json out.mp4   (run from repo root)
spec: {"clips":[{"photo":"banco/...jpg","text":"Texto grande","sub":"texto chico opcional","dur":2.5,"fy":0.5}],
       "end":{"title":"TeamFS Kennel Club","sub":"Cane Corso KCC · American Bully ABKC"}}
First clip = hook (1.5–2.5 s). Keep total 8–25 s. Text is baked into frames (Reels/TikTok are watched muted).
Voz en off (opcional): agrega "vo":"texto hablado" a cada clip. La duración del clip se alarga para que calce la voz.
  Motor (vo_engine "auto"): Edge TTS chilena es-CL-CatalinaNeural si hay acceso a speech.platform.bing.com; si no, Piper offline latino es_MX-claude-high.
  Opcional en spec: "edge_voice":"es-CL-LorenzoNeural", "edge_rate":"+8%", "piper_voice":"es_MX-ald-medium", "vo_speed":0.92, "vo_file":"audio.mp3" (voz grabada por el dueño, reemplaza la TTS)."""
import sys,json,os,subprocess,tempfile
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter,ImageEnhance
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1080,1920;FPS=30
P=f"{R}/fonts/Poppins-Bold.ttf";IB=f"{R}/fonts/Inter-ExtraBold.otf";IR=f"{R}/fonts/Inter-Medium.otf"
NAVY=(10,20,46);GREEN=(37,211,102)
def wrap(d,t,fo,mw):
    out=[];line=""
    for w in t.split():
        s=(line+" "+w).strip()
        if d.textlength(s,font=fo)<=mw: line=s
        else: out.append(line);line=w
    return out+[line]
def stroke_text(d,y,text,fo,lh,fill=(255,255,255)):
    for ln in wrap(d,text,fo,W-140):
        tw=d.textlength(ln,font=fo);d.text(((W-tw)/2,y),ln,font=fo,fill=fill,stroke_width=7,stroke_fill=(0,0,0));y+=lh
    return y
def frame(c):
    im=ImageOps.exif_transpose(Image.open(os.path.join(R,c["photo"]))).convert("RGB")
    im=ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.06)).enhance(1.1)
    bg=im.resize((W,int(im.height*W/im.width)) if im.width/im.height<W/H else (int(im.width*H/im.height),H))
    sc=max(W/im.width,H/im.height);bg=im.resize((int(im.width*sc)+2,int(im.height*sc)+2))
    fy=c.get("fy",.5);fx=c.get("fx",.5)
    x=int((bg.width-W)*fx);y=int((bg.height-H)*fy)
    if c.get("fit")=="contain":
        b=bg.crop((x,y,x+W,y+H)).filter(ImageFilter.GaussianBlur(40));b=ImageEnhance.Brightness(b).enhance(.55)
        fg=im.copy();fg.thumbnail((W-80,1150));b.paste(fg,((W-fg.width)//2,200));out=b
    else: out=bg.crop((x,y,x+W,y+H))
    d=ImageDraw.Draw(out)
    d.text((60,90),"TEAMFS KENNEL CLUB",font=ImageFont.truetype(IB,32),fill=(255,255,255),stroke_width=4,stroke_fill=(0,0,0))
    yy=c.get("text_y",1400 if c.get("fit")=="contain" else 300)
    if c.get("text"): yy=stroke_text(d,yy,c["text"],ImageFont.truetype(P,c.get("size",84)),int(c.get("size",84)*1.18))
    if c.get("sub"): stroke_text(d,yy+20,c["sub"],ImageFont.truetype(IB,58),70,(242,201,76))
    return out
def endcard(e):
    out=Image.new("RGB",(W,H),NAVY);d=ImageDraw.Draw(out)
    logo=e.get("logo","marca/logo_001.jpg")
    if os.path.exists(os.path.join(R,logo)):
        lg=Image.open(os.path.join(R,logo)).convert("RGB");lg.thumbnail((700,900));out.paste(lg,((W-lg.width)//2,220))
    y=1200;y=stroke_text(d,y,e.get("title","TeamFS Kennel Club"),ImageFont.truetype(P,70),84)
    y=stroke_text(d,y+10,e.get("sub","Cane Corso KCC · American Bully ABKC"),ImageFont.truetype(IR,44),56,(220,226,240))
    fo=ImageFont.truetype(IB,50);t=e.get("whatsapp","WhatsApp +56 9 6190 7601");tw=d.textlength(t,font=fo)
    d.rounded_rectangle(((W-tw)/2-40,y+50,(W+tw)/2+40,y+150),radius=50,fill=GREEN);d.text(((W-tw)/2,y+70),t,font=fo,fill=(255,255,255))
    return out
# Voz: 1) Edge TTS es-CL (chilena, natural) si el dominio speech.platform.bing.com está permitido;
#      2) si no, Piper offline latino (es_MX-claude-high, descargado de GitHub sherpa-onnx a tools/voices/).
EDGE_VOICE="es-CL-CatalinaNeural"   # alternativa masculina: es-CL-LorenzoNeural
PIPER_DEFAULT="es_MX-claude-high"
PIPER_URL="https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-{n}.tar.bz2"
def ensure_voice(s):
    v=s.get("voice_model")
    if v: return v
    n=s.get("piper_voice",PIPER_DEFAULT);d=f"{R}/tools/voices";v=f"{d}/vits-piper-{n}/{n}.onnx"
    if not os.path.exists(v):
        os.makedirs(d,exist_ok=True);tg=f"{d}/v.tar.bz2"
        subprocess.run(["curl","-sSL","-o",tg,PIPER_URL.format(n=n)],check=True);subprocess.run(["tar","xjf",tg,"-C",d],check=True);os.remove(tg)
    return v
def dur_of(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout.strip())
def edge_tts(text,out,voice,rate):
    try:
        import edge_tts,asyncio
        px=os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        async def go(): await edge_tts.Communicate(text,voice,rate=rate,proxy=px).save(out+".mp3")
        asyncio.run(go());subprocess.run(["ffmpeg","-v","error","-y","-i",out+".mp3",out],check=True);return True
    except Exception as e:
        print("Edge TTS no disponible, uso Piper:",str(e)[:80]);return False
ENGINE={"edge":None}
def tts(text,s,out):
    if s.get("vo_engine","auto") in ("auto","edge") and ENGINE["edge"] is not False:
        ok=edge_tts(text,out,s.get("edge_voice",EDGE_VOICE),s.get("edge_rate","+8%"))
        ENGINE["edge"]=ok
        if ok: return dur_of(out)
    model=ensure_voice(s)
    raw=out+".raw.wav"
    subprocess.run([sys.executable,"-m","piper","-m",model,"-f",raw,"--length-scale",str(s.get("vo_speed",0.92)),"--noise-scale","0.75","--sentence-silence","0.15"],input=text.encode(),check=True,capture_output=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",raw,"-af","highpass=f=80,acompressor=threshold=-18dB:ratio=3","-ar","44100",out],check=True)
    return dur_of(out)
def main(spec,out):
    s=json.load(open(spec));tmp=tempfile.mkdtemp();parts=[]
    clips=s["clips"]+[{"_end":True,"dur":s.get("end",{}).get("dur",2.5),"vo":s.get("end",{}).get("vo")}]
    vo_on=any(c.get("vo") for c in clips) and not s.get("vo_file");vos=[]
    if vo_on:
        for i,c in enumerate(clips):
            if c.get("vo"):
                w=f"{tmp}/vo{i}.wav";d=tts(c["vo"],s,w);c["dur"]=max(c.get("dur",2.5),d+0.6);vos.append((i,w))
    for i,c in enumerate(clips):
        img=endcard(s.get("end",{})) if c.get("_end") else frame(c)
        p=f"{tmp}/f{i}.png";img.save(p);n=int(c.get("dur",2.5)*FPS)
        z="1.0" if c.get("_end") else f"min(1+0.10*on/{n},1.10)"
        v=f"{tmp}/c{i}.mp4"
        subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",p,"-vf",f"scale=1188:2112,zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={n}:s={W}x{H}:fps={FPS},format=yuv420p","-frames:v",str(n),"-c:v","libx264","-preset","veryfast","-crf","20",v],check=True)
        parts.append((v,c.get("dur",2.5)))
    # crossfade chain
    inputs=[];fil=[];last="0:v";off=0.0;xf=0.35
    for i,(v,dur) in enumerate(parts): inputs+=["-i",v]
    acc=parts[0][1]
    for i in range(1,len(parts)):
        off=acc-xf;lab=f"v{i}";fil.append(f"[{last}][{i}:v]xfade=transition=fade:duration={xf}:offset={off:.2f}[{lab}]");last=lab;acc+=parts[i][1]-xf
    if vo_on or s.get("vo_file"):
        # build voice track aligned to clip starts
        starts=[];t=0.0
        for i,(v,dur) in enumerate(parts): starts.append(t);t+=dur-xf
        if s.get("vo_file"): af=[s["vo_file"]];dl=[0]
        else: af=[w for i,w in vos];dl=[int((starts[i]+0.25)*1000) for i,w in vos]
        ain=[];fl=[]
        for k,(f_,d_) in enumerate(zip(af,dl)): ain+=["-i",f_];fl.append(f"[{k}:a]aresample=44100,adelay={d_}|{d_},apad[a{k}]")
        fl.append("".join(f"[a{k}]" for k in range(len(af)))+f"amix=inputs={len(af)}:normalize=0,atrim=0:{acc:.2f},volume=0.85[out]")
        voice=f"{tmp}/voice.wav";subprocess.run(["ffmpeg","-v","error","-y"]+ain+["-filter_complex",";".join(fl),"-map","[out]","-ac","2",voice],check=True)
        audio_in=["-i",voice]
    else: audio_in=["-f","lavfi","-t",f"{acc:.2f}","-i","anullsrc=r=44100:cl=stereo"]
    cmd=["ffmpeg","-v","error","-y"]+inputs+audio_in
    cmd+=["-filter_complex",";".join(fil),"-map",f"[{last}]","-map",f"{len(parts)}:a","-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-shortest","-movflags","+faststart",out] if fil else ["-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest",out]
    subprocess.run(cmd,check=True);print(out,f"{acc:.1f}s")
if __name__=="__main__": main(sys.argv[1],sys.argv[2])
