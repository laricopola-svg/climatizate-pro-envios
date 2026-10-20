"""TeamFS post generator. Usage: python3 tools/make_post.py spec.json OUTDIR
spec: {"slides":[{type:cover|point|cta, photo, fx, fy, ...}]}  -> OUTDIR/slide_01.jpg ...
Run from repo root (photos paths relative to it)."""
import sys,json,os
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance,ImageFilter
import numpy as np
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1080,1350
NAVY=(10,20,46);RED=(230,57,70);WHITE=(255,255,255);GOLD=(242,201,76);SOFT=(225,230,240);DIM=(205,210,225)
P=f"{R}/fonts/Poppins-Bold.ttf";IB=f"{R}/fonts/Inter-ExtraBold.otf";IR=f"{R}/fonts/Inter-Medium.otf"
f=lambda p,s:ImageFont.truetype(p,s)
def enhance(im):
    im=ImageOps.exif_transpose(im).convert("RGB").filter(ImageFilter.MedianFilter(3))
    a=np.asarray(im).astype(np.float32)
    lo=np.percentile(a,0.5,axis=(0,1));hi=np.percentile(a,99.5,axis=(0,1))
    a=0.6*((a-lo)/np.maximum(hi-lo,1)*255)+0.4*a
    im=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.08)).enhance(1.12)
def cover(im,fx=.5,fy=.5,zoom=1.0):
    sc=max(W/im.width,H/im.height)*zoom
    im=im.resize((round(im.width*sc),round(im.height*sc)),Image.LANCZOS)
    x=int((im.width-W)*fx);y=int((im.height-H)*fy)
    return im.crop((x,y,x+W,y+H)).filter(ImageFilter.UnsharpMask(radius=1.2,percent=45,threshold=4))
def gradient(im,start=.4,strength=.94):
    ys=np.arange(H)/H
    b=np.clip((ys-start)/(1-start),0,1)**0.9*255*strength
    t=np.clip(1-np.arange(H)/260,0,1)*150
    g=np.maximum(b,t).astype(np.uint8)[:,None].repeat(W,1)
    return Image.composite(Image.new("RGB",(W,H),NAVY),im,Image.fromarray(g,"L"))
def wrap(d,text,font,maxw):
    out=[]
    for para in text.split("\n"):
        line=""
        for w in para.split():
            t=(line+" "+w).strip()
            if d.textlength(t,font=font)<=maxw: line=t
            else: out.append(line);line=w
        out.append(line)
    return out
def block(d,x,y,text,font,fill,lh,maxw=W-120):
    for ln in wrap(d,text,font,maxw): d.text((x,y),ln,font=font,fill=fill);y+=lh
    return y
def hgt(d,text,font,lh): return len(wrap(d,text,font,W-120))*lh
def header(d,n,tot):
    d.text((60,52),"TEAMFS KENNEL CLUB",font=f(IB,26),fill=WHITE);d.rectangle((60,88,130,93),fill=RED)
    if tot>1:
        s=f"{n}/{tot}";fw=d.textlength(s,font=f(IB,26))
        d.rounded_rectangle((W-60-fw-36,44,W-60,90),radius=23,outline=WHITE,width=2);d.text((W-60-fw-18,52),s,font=f(IB,26),fill=WHITE)
def pill(d,x,y,text,bg,fg=WHITE,size=28):
    fo=f(IB,size);tw=d.textlength(text,font=fo)
    d.rounded_rectangle((x,y,x+tw+44,y+size+26),radius=(size+26)//2,fill=bg);d.text((x+22,y+10),text,font=fo,fill=fg);return y+size+26
def base(s,start,strength):
    return gradient(cover(enhance(Image.open(os.path.join(R,s["photo"]))),s.get("fx",.5),s.get("fy",.5),s.get("zoom",1)),start,strength)
def s_cover(s,n,tot):
    im=base(s,.36,.96);d=ImageDraw.Draw(im);header(d,n,tot)
    ft=f(P,s.get("title_size",150));fs=f(P,54)
    need=54+28+hgt(d,s["title"],ft,int(ft.size*1.2))+hgt(d,s.get("subtitle",""),fs,66)+26+40
    y=H-90-need
    y=pill(d,60,y,s.get("kicker","").upper(),RED)+28
    y=block(d,60,y-20,s["title"],ft,WHITE,int(ft.size*1.2))
    if s.get("subtitle"): y=block(d,60,y,s["subtitle"],fs,WHITE,66)
    if s.get("cta"): d.text((60,y+26),s["cta"],font=f(IB,32),fill=GOLD)
    return im
def s_point(s,n,tot):
    im=base(s,.30,.95);d=ImageDraw.Draw(im);header(d,n,tot)
    fq=f(P,46);fh=f(P,58);fb=f(IR,33)
    q=s.get("quote");need=58+(hgt(d,"“"+q+"”",fq,56)+30 if q else 0)+(58 if s.get("tag") else 0)+hgt(d,s["headline"],fh,68)+18+hgt(d,s.get("body",""),fb,46)
    y=H-80-need
    y=pill(d,60,y,s["label"].upper(),RED,size=26)+14
    if q: y=block(d,60,y,"“"+q+"”",fq,DIM,56)+30
    if s.get("tag"): y=pill(d,60,y,s["tag"].upper(),WHITE,NAVY,26)+14
    y=block(d,60,y,s["headline"],fh,WHITE,68)+18
    block(d,60,y,s.get("body",""),fb,SOFT,46)
    return im
def s_cta(s,n,tot):
    im=base(s,.25,.96);d=ImageDraw.Draw(im);header(d,n,tot)
    fh=f(P,56);fb=f(IR,34);bl=s.get("bullets",[])
    need=hgt(d,s["headline"],fh,68)+8+hgt(d,s.get("highlight",""),fh,68)+36+58*len(bl)+24+50
    y=H-80-need
    y=block(d,60,y,s["headline"],fh,WHITE,68)+8
    y=block(d,60,y,s.get("highlight",""),fh,GOLD,68)+36
    for t in bl: d.ellipse((60,y+12,76,y+28),fill=RED);d.text((96,y),t,font=fb,fill=WHITE);y+=58
    d.text((60,y+24),s.get("handle","@teamfsbull_kennelclub"),font=f(IB,38),fill=WHITE)
    return im
if __name__=="__main__":
    spec=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
    sl=spec["slides"];tot=len(sl)
    for i,s in enumerate(sl,1):
        im={"cover":s_cover,"point":s_point,"cta":s_cta}[s["type"]](s,i,tot)
        im.save(f"{out}/slide_{i:02d}.jpg",quality=90);print(f"{out}/slide_{i:02d}.jpg")
