import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np
from collections import deque
IM=sys.argv[1]; OUT=sys.argv[2]
def flood_alpha(im, tol):
    """remove fundo conectado às bordas (cor do canto), com borda suave"""
    a=np.asarray(im.convert("RGB")).astype(int); h,w,_=a.shape
    bg=np.median(np.concatenate([a[0,:],a[-1,:],a[:,0],a[:,-1]]),axis=0)
    d=np.abs(a-bg).max(axis=2)
    cand=d<=tol
    seen=np.zeros((h,w),bool); q=deque()
    for x in range(w):
        for y in (0,h-1):
            if cand[y,x] and not seen[y,x]: seen[y,x]=True;q.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if cand[y,x] and not seen[y,x]: seen[y,x]=True;q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<h and 0<=xx<w and cand[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True;q.append((yy,xx))
    m=Image.fromarray((~seen*255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    o=im.convert("RGBA"); o.putalpha(m); return o
def trim(im):
    bb=im.getchannel("A").point(lambda v:255 if v>20 else 0).getbbox(); return im.crop(bb)
L={}
def load(n): return Image.open(f"{IM}/{n}")
def tile(n,r=30):
    im=load(n).convert("RGBA"); m=Image.new("L",im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+im.size,radius=r,fill=255); im.putalpha(m); return im
def pad_tile(n,pad,r):
    im=load(n).convert("RGB"); bgc=im.getpixel((3,3)); W2,H2=im.width+2*pad,im.height+2*pad
    c=Image.new("RGB",(W2,H2),bgc); c.paste(im,(pad,pad)); c=c.convert("RGBA"); m=Image.new("L",c.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+c.size,radius=r,fill=255); c.putalpha(m); return c
def wtile(n,P,r,crop=False):
    im=load(n).convert("RGB")
    if crop:
        g=np.asarray(im.convert("L")); ys,xs=np.where(g<235); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    t=Image.new("RGB",(im.width+2*P,im.height+2*P),im.getpixel((2,2))); t.paste(im,(P,P)); t=t.convert("RGBA")
    m=Image.new("L",t.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+t.size,radius=r,fill=255); t.putalpha(m); return t
L["Ren9ve Autos"]=pad_tile("51.png",14,18)
L["Rfeitosa Group"]=wtile("52.png",24,26)
L["Sao e Salvo"]=wtile("53.jpg",10,26,crop=True)
L["Sitio do Bosco"]=trim(flood_alpha(load("54.jpg").convert("RGB"),30))
sv=load("55.png").convert("RGBA"); sv=trim(sv); P=40
t=Image.new("RGBA",(sv.width+2*P,sv.height+2*P),(255,255,255,255)); t.alpha_composite(sv,(P,P))
m=Image.new("L",t.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+t.size,radius=36,fill=255); t.putalpha(m); L["Servfort"]=t
base=load("27.jpg").convert("RGB")
CX,CY,MW,MH=994,1038,432,140
import json
for name,lg in L.items():
    if lg is None: continue
    img=base.copy()
    s=min(MW/lg.width,MH/lg.height); lg2=lg.resize((max(1,int(lg.width*s)),max(1,int(lg.height*s))),Image.LANCZOS)
    img.paste(lg2,(CX-lg2.width//2,CY-lg2.height//2),lg2)
    fn=name.lower().replace(" ","_").replace("ç","c").replace("á","a").replace("í","i").replace("ã","a")
    img.save(f"{OUT}/outubro_rosa_{fn}.png"); print(fn,lg2.size)
