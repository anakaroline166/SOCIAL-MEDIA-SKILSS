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
im=load("37.png").convert("RGBA")
if im.getchannel("A").getextrema()[0]>250: im=flood_alpha(im.convert("RGB"),30)
L["Lacliso"]=trim(im)
L["La Pulga"]=tile("38.jpg",22)
_g=np.asarray(load("39.jpg").convert("L")).astype(float); _al=np.clip((255-_g)*1.15,0,255).astype("uint8")
_o=Image.new("RGBA",(150,150),(25,25,25,0)); _o.putalpha(Image.fromarray(_al)); _o=_o.resize((600,600),Image.LANCZOS); L["LA Office"]=trim(_o)
L["IBG Foods"]=tile("41.jpg",22)
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
