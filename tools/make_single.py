"""Imagen única 1080x1350 (foto real o ilustración IA) con título + pasos + WhatsApp.
Uso: python3 tools/make_single.py spec.json OUT.jpg   (desde la raíz del repo)
spec: {photo, fx, fy, zoom, photo_h (0-1, alto de la foto), kicker, title, steps:[...], dato, ai_label(bool)}"""
import sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from make_post import *
s=json.load(open(sys.argv[1]));out=sys.argv[2]
ph=int(H*s.get("photo_h",.5))
src=Image.open(os.path.join(R,s["photo"]))
src=enhance(src) if not s.get("ai_label") else ImageOps.exif_transpose(src).convert("RGB")
sc=max(W/src.width,ph/src.height)*s.get("zoom",1)
src=src.resize((round(src.width*sc),round(src.height*sc)),Image.LANCZOS)
x=int((src.width-W)*s.get("fx",.5));y=int((src.height-ph)*s.get("fy",.5))
im=Image.new("RGB",(W,H),NAVY);im.paste(src.crop((x,y,x+W,y+ph)),(0,0))
# fundido foto -> azul
g=np.zeros((H,W),np.uint8);fade=160
for yy in range(ph-fade,ph): g[yy,:]=int(255*((yy-(ph-fade))/fade)**1.2)
g[ph:,:]=255
top=np.clip(1-np.arange(H)/200,0,1)*140;g=np.maximum(g,top.astype(np.uint8)[:,None])
im=Image.composite(Image.new("RGB",(W,H),NAVY),im,Image.fromarray(g,"L"));d=ImageDraw.Draw(im)
d.text((60,52),"TEAMFS KENNEL CLUB",font=f(IB,26),fill=WHITE);d.rectangle((60,88,130,93),fill=RED)
if s.get("ai_label"):
    t="Ilustración IA";fo=f(IB,22);tw=d.textlength(t,font=fo)
    d.rounded_rectangle((W-60-tw-30,46,W-60,86),radius=20,fill=(0,0,0));d.text((W-60-tw-15,53),t,font=fo,fill=WHITE)
ft=f(P,s.get("title_size",64));fstep=f(IR,s.get("step_size",31));fn=f(IB,30)
y=ph-120
y=pill(d,60,y,s["kicker"].upper(),RED,size=26)+18
y=block(d,60,y,s["title"],ft,WHITE,int(ft.size*1.15))+14
for i,st in enumerate(s["steps"],1):
    d.ellipse((60,y+2,104,y+46),fill=GOLD);n=str(i);d.text((82-d.textlength(n,font=fn)/2,y+5),n,font=fn,fill=NAVY)
    y=block(d,124,y+4,st,fstep,SOFT,42,maxw=W-124-60)+12
if s.get("dato"):
    y+=4;y=block(d,60,y,"Dato TeamFS: "+s["dato"],f(IB,28),GOLD,38)+8
wa="WhatsApp +56 9 6190 7601";fo=f(IB,30);tw=d.textlength(wa,font=fo)
by=H-92;d.rounded_rectangle((60,by,60+tw+48,by+56),radius=28,fill=(37,211,102));d.text((84,by+11),wa,font=fo,fill=WHITE)
d.text((60+tw+80,by+12),s.get("handle","@teamfsbull_kennelclub"),font=f(IB,28),fill=WHITE)
d.rectangle((0,H-14,W,H),fill=RED)
if y>by-10: print("AVISO: el texto choca con el pie (y=%d)"%y)
im.save(out,quality=88,optimize=True);print(out,os.path.getsize(out)//1024,"KB")
