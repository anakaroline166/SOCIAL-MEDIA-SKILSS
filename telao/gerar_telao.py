import sys, subprocess, os, json
from PIL import Image, ImageDraw, ImageFont

OUT, LOGO, FONTS, IMGS, CUTS = sys.argv[1:6]
NOTEXT = bool(os.environ.get("NOTEXT")); REC=[]; slides=[]
_orig_text = ImageDraw.ImageDraw.text
def _text(self, xy, text, fill=None, font=None, anchor=None, *a, **k):
    REC.append(dict(slide=len(slides)+1, x=float(xy[0]), y=float(xy[1]), text=text, size=font.size, bold=("IntroBold" in font.path), color=list(fill) if isinstance(fill,tuple) else fill))
    if not NOTEXT: _orig_text(self, xy, text, fill=fill, font=font, anchor=anchor, *a, **k)
ImageDraw.ImageDraw.text = _text
W, H = 1920, 1080
M = 110                                   # margem igual nos 4 lados
VIN, CORAL, CREME, CARD, GRAY, NAVY, WHITE = (75,15,47), (255,111,104), (255,247,242), (255,239,232), (140,110,125), (43,27,77), (255,255,255)
LEAD, GAP = 1.12, 40                      # entrelinha e espaço entre blocos, iguais em todos os slides
BOX  = (M, 190, W-M, 890)                   # área útil (acima da faixa do logo)
LEFT = (M, 190, 930, 890)                   # coluna do texto quando há foto
PHOTO= (1110, 190, W-M, 890)                # coluna da foto (760 x 760)

ccx=(PHOTO[0]+PHOTO[2])//2; ccy=(PHOTO[1]+PHOTO[3])//2
def F(w, s):
    return ImageFont.truetype(f"{FONTS}/{'IntroBold' if w in ('ExtraBold','Bold') else 'IntroBook'}.otf", max(int(s),8))

logo_w = Image.open(LOGO).convert("RGBA"); logo = logo_w.copy(); px = logo.load()
for y in range(logo.height):
    for x in range(logo.width):
        r,g,b,a = px[x,y]
        if a > 0 and r > 200 and g > 200 and b > 200: px[x,y] = NAVY+(a,)
def paste_logo(img, white=False, width=220):
    src = logo_w if white else logo
    l = src.resize((width, int(src.height*width/src.width)), Image.LANCZOS)
    img.paste(l, (W//2 - l.width//2, H - 80 - l.height), l)

def cutout(name):
    im = Image.open(f"{CUTS}/{name}").convert("RGBA")
    return im.crop(im.getchannel("A").point(lambda v:255 if v>20 else 0).getbbox())
def grad(w,h,c0=(75,15,47),c1=(49,35,95),dx=0.5,dy=0.5):
    g = Image.new("RGB",(w,h)); p=g.load()
    for yy in range(h):
        for xx in range(w):
            t=xx/w*dx+yy/h*dy; p[xx,yy]=tuple(int(c0[i]+(c1[i]-c0[i])*t) for i in range(3))
    return g
def photo_card(img, name, box, focus=(0.5,0.5), tint=115, radius=50):
    x0,y0,x1,y1 = box; bw,bh = x1-x0, y1-y0
    im = Image.open(f"{IMGS}/{name}").convert("RGB")
    s = max(bw/im.width, bh/im.height)
    im = im.resize((int(im.width*s)+1, int(im.height*s)+1), Image.LANCZOS)
    cx,cy = int(focus[0]*im.width), int(focus[1]*im.height)
    l = min(max(cx-bw//2,0), im.width-bw); t = min(max(cy-bh//2,0), im.height-bh)
    im = Image.alpha_composite(im.crop((l,t,l+bw,t+bh)).convert("RGBA"), Image.new("RGBA",(bw,bh),VIN+(tint,)))
    mask = Image.new("L",(bw,bh),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,bw,bh), radius=radius, fill=255)
    img.paste(im.convert("RGB"), (x0,y0), mask)

# ---------- motor de layout ----------
_probe = ImageDraw.Draw(Image.new("RGB",(10,10)))
def tmetrics(lines, weight, size):
    f=F(weight,size); lh=size*LEAD; tops=[];bots=[];ws=[]
    for l in lines:
        t=1e9; b=-1e9; w=0
        for txt,c in l:
            bb=_probe.textbbox((0,0),txt,font=f,anchor="ls"); t=min(t,bb[1]); b=max(b,bb[3]); w+=_probe.textlength(txt,font=f)
        tops.append(-t); bots.append(b); ws.append(w)
    return f,lh,tops,bots,ws, tops[0]+(len(lines)-1)*lh+bots[-1]
def T(lines, weight="Bold", size=100):  return dict(k="text", lines=lines, w=weight, size=size)
def CARDI(txt, size=44, weight="Medium", color=VIN, fill=CARD): return dict(k="card", txt=txt, size=size, w=weight, color=color, fill=fill)
def PILLS(txts, size=34):  return dict(k="pills", txts=txts, size=size)
def CUSTOM(h, fn):         return dict(k="custom", h=h, fn=fn)

def prep(it, s, boxw):
    if it["k"]=="text":
        size=it["size"]*s
        while True:
            m=tmetrics(it["lines"], it["w"], size)
            if max(m[4])<=boxw or size<24: break
            size-=2
        it["_m"]=m; it["_size"]=size; it["_h"]=m[5]
    elif it["k"]=="card":
        size=it["size"]*s
        while True:
            m=tmetrics([[(it["txt"],it["color"])]], it["w"], size)
            if m[4][0]+140<=boxw or size<20: break
            size-=2
        it["_m"]=m; it["_size"]=size; it["_h"]=max(m[5]+2*34, 40)
    elif it["k"]=="pills":
        ph=int(84*s); it["_ph"]=ph; it["_h"]=len(it["txts"])*ph+(len(it["txts"])-1)*int(22*s)
    else: it["_h"]=it["h"]
def stack(img, d, items, box, bg_dark=False, cap=0.9, align='center'):
    x0,y0,x1,y1 = box; bw,bh = x1-x0, y1-y0; cx=(x0+x1)/2
    s=1.0
    while True:
        for it in items: prep(it, s, bw)
        total=sum(it["_h"] for it in items)+GAP*(len(items)-1)
        if total<=bh*cap or s<0.45: break
        s-=0.02
    y=y0+(bh-total)/2
    for it in items:
        if it["k"]=="text":
            f,lh,tops,bots,ws,h=it["_m"]
            for i,l in enumerate(it["lines"]):
                x=(x0 if align=='left' else cx-ws[i]/2); by=y+tops[0]+i*lh
                for txt,c in l:
                    d.text((x,by),txt,font=f,fill=c,anchor="ls"); x+=d.textlength(txt,font=f)
        elif it["k"]=="card":
            f,lh,tops,bots,ws,h=it["_m"]; w=ws[0]+140; cl=(x0 if align=='left' else cx-w/2)
            d.rounded_rectangle((cl,y,cl+w,y+it["_h"]), radius=int(it["_h"]/2) if it["_h"]<140 else 40, fill=it["fill"])
            d.text((cl+70, y+it["_h"]/2-(tops[0]+bots[0])/2+tops[0]), it["txt"], font=f, fill=it["color"], anchor="ls")
        elif it["k"]=="pills":
            f=F("Bold",it["size"]*s); ph=it["_ph"]; yy=y
            for t in it["txts"]:
                w=d.textlength(t,font=f)+130; px0=(x0 if align=='left' else cx-w/2)
                d.rounded_rectangle((px0,yy,px0+w,yy+ph), radius=ph//2, fill=CARD)
                d.ellipse((px0+34,yy+ph/2-14,px0+62,yy+ph/2+14), fill=CORAL)
                bb=d.textbbox((0,0),t,font=f,anchor="ls")
                d.text((px0+86, yy+ph/2-(bb[1]+bb[3])/2), t, font=f, fill=VIN, anchor="ls")
                yy+=ph+int(22*s)
        else:
            it["fn"](img,d,x0,y,bw)
        y+=it["_h"]+GAP
def new(dark=False):
    im = grad(W,H,dx=0.6,dy=0.4) if dark else Image.new("RGB",(W,H),WHITE)
    return im, ImageDraw.Draw(im)
def footnote(txt): return T([[(txt,GRAY)]],"Medium",30)

# 1
img,d=new(); stack(img,d,[T([[("Quanto ",VIN),("custa",CORAL),(" para sua",VIN)],[("empresa um funcionário",VIN)],[("não conseguir trabalhar?",VIN)]],"Bold",150)],BOX)
paste_logo(img); slides.append((img,9))
# 2
img,d=new(); stack(img,d,[T([[("Agora multiplique por",VIN)]],"Medium",70),T([[("×100",CORAL)]],"Bold",380),T([[("funcionários.",VIN)]],"Bold",110)],LEFT,cap=1.0,align='left')
photo_card(img,"16.jpg",PHOTO,(0.5,0.45)); paste_logo(img); slides.append((img,6))
# 3
img,d=new(); stack(img,d,[T([[("Um dia de falta não custa",VIN)]],"Bold",112),T([[("R$ 54.",CORAL)]],"Bold",310),T([[("Custa muito mais.",VIN)]],"Bold",136),CARDI("O salário é só a ponta do custo.",54)],BOX,cap=1.0)
d.text((M,H-80),"Base: salário mínimo 2026 (R$ 1.621 ÷ 30 dias)",font=F("Medium",28),fill=GRAY,anchor="ls")
paste_logo(img); slides.append((img,9))
# 4
img,d=new(); stack(img,d,[T([[("“",CORAL)]],"Bold",300),T([[("A falta aparece no ponto.",VIN)],[("O prejuízo aparece no ",VIN),("resultado.",CORAL)]],"Bold",110)],BOX)
paste_logo(img); slides.append((img,6))
# A
img,d=new(); stack(img,d,[T([[("Você sabe quanto custa",VIN)],[("1 dia de ausência",CORAL)],[("na sua empresa?",VIN)]],"Bold",130)],BOX)
paste_logo(img); slides.append((img,7))
# C
img,d=new(); stack(img,d,[T([[("Seu funcionário faltou 1 dia.",VIN)]],"Bold",96),T([[("Quanto sua empresa",VIN)],[("realmente perdeu?",CORAL)]],"Bold",130)],BOX)
paste_logo(img); slides.append((img,7))
# 5
img,d=new(); stack(img,d,[T([[("546 mil",CORAL)]],"Bold",250),T([[("afastamentos por saúde",VIN)],[("mental no Brasil em 2025.",VIN)]],"Bold",96),CARDI("+15% em um ano",52,"Bold",CORAL),footnote("Fonte: Ministério da Previdência Social")],BOX)
paste_logo(img); slides.append((img,9))
# 6
img,d=new(); stack(img,d,[T([[("4,1 milhões",CORAL)]],"Bold",230),T([[("de afastamentos temporários",VIN)],[("do trabalho em 2025.",VIN)]],"Bold",90),CARDI("+17% em um ano",52,"Bold",CORAL),footnote("Fonte: Ministério da Previdência Social")],BOX)
paste_logo(img); slides.append((img,9))
# B
img,d=new(); stack(img,d,[T([[("Estresse, afastamento e",VIN)],[("presenteísmo têm um preço.",VIN)]],"Bold",100),T([[("Você sabe qual?",CORAL)]],"Bold",130)],BOX)
paste_logo(img); slides.append((img,7))
# 7
img,d=new(); stack(img,d,[T([[("NR-1",CORAL)]],"Bold",220),T([[("não é só obrigação.",VIN)],[("É gestão de um risco",VIN)],[("que custa dinheiro.",CORAL)]],"Bold",90),CARDI("Risco psicossocial também aparece no caixa.",42)],BOX)
paste_logo(img); slides.append((img,9))
# 8 NR-1 UAU
img,d=new(True)
stack(img,d,[CARDI("NR-1  ·  RISCOS PSICOSSOCIAIS",34,"Bold",WHITE,CORAL),
  T([[("Sua empresa está",CREME)],[("pronta para a",CREME)]],"Bold",96),
  T([[("NR-1?",CORAL)]],"Bold",260),
  T([[("A Nexia faz grande parte desse caminho,",CREME)],[("com suporte e pós-venda.",CREME)]],"Medium",40),
  CARDI("Entre e converse com a gente  →",44,"Bold",VIN,CREME)],LEFT,cap=1.0,align='left')
photo_card(img,"15.jpg",PHOTO,(0.56,0.5),tint=70); paste_logo(img,white=True); slides.append((img,9,True))
# 12a e 12b: médico (mesmo recorte nas duas, só o texto troca)
def slide_doctor(items,dur):
    img,d=new(); stack(img,d,items,LEFT,cap=1.0,align="left")
    cx0,cy0,cx1,cy1 = PHOTO; ccx=(cx0+cx1)//2; ccy=(cy0+cy1)//2
    d.ellipse(PHOTO, fill=CORAL)
    doc=cutout("medico_birefnet-general-lite.png"); w=680; h=int(doc.height*w/doc.width); doc=doc.resize((w,h),Image.LANCZOS)
    layer=Image.new("RGBA",(W,H),(0,0,0,0)); layer.paste(doc,(ccx-w//2, cy1-h),doc)
    clip=Image.new("L",(W,H),0); cd=ImageDraw.Draw(clip); cd.ellipse(PHOTO,fill=255); cd.rectangle((0,0,W,ccy),fill=255)
    al=layer.getchannel("A"); layer.putalpha(Image.composite(al,Image.new("L",(W,H),0),clip))
    img.paste(layer,(0,0),layer); paste_logo(img); slides.append((img,dur))
slide_doctor([T([[("Cuidar da saúde",VIN)],[("pode ser caro.",VIN)]],"Bold",84),T([[("Não cuidar é",VIN)]],"Bold",84),T([[("mais caro",CORAL)]],"Bold",190),T([[("ainda.",VIN)]],"Bold",84)],8)
# 10 médica no celular
img,d=new()
stack(img,d,[T([[("Saúde na palma",VIN)],[("da mão.",VIN)],[("Sem deslocamento.",CORAL)]],"Bold",100),PILLS(["Clínico geral 24h","Mais de 12 especialidades","Psicologia e nutrição","Clubes de benefícios nacional e regional"],32)],LEFT,cap=1.0,align="left")
d.ellipse(PHOTO, fill=CORAL)
PX0,PX1,PY0,PY1 = ccx-210, ccx+210, PHOTO[1]+70, PHOTO[3]
mask=Image.new("L",(PX1-PX0,PY1-PY0),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,PX1-PX0,PY1-PY0),radius=70,fill=255)
img.paste(grad(PX1-PX0,PY1-PY0,dx=0.4,dy=0.6),(PX0,PY0),mask)
frame=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(frame).rounded_rectangle((PX0,PY0,PX1,PY1),radius=70,outline=NAVY+(255,),width=16)
img.paste(frame,(0,0),frame)
doc=cutout("medica_birefnet-general-lite.png"); BOT=PY1-16; hh=BOT-PHOTO[1]; w=int(doc.width*hh/doc.height); doc=doc.resize((w,hh),Image.LANCZOS)
layer=Image.new("RGBA",(W,H),(0,0,0,0)); layer.paste(doc,(ccx-w//2,PHOTO[1]),doc)
al=layer.getchannel("A"); ad=ImageDraw.Draw(al); ad.rectangle((0,BOT,W,H),fill=0); ad.rectangle((0,BOT-45,PX0+20,BOT),fill=0); ad.rectangle((PX1-20,BOT-45,W,BOT),fill=0); layer.putalpha(al)
img.paste(layer,(0,0),layer)
strip=frame.crop((0,BOT-6,W,PY1+2)); img.paste(strip,(0,BOT-6),strip)
paste_logo(img); slides.append((img,9))
# 11
def numbers(img,d,x0,y,bw):
    cols=[("+50","empresas clientes"),("+2.000","pessoas beneficiadas"),("+200","profissionais parceiros")]
    cw,gap=500,40; start=x0+(bw-(3*cw+2*gap))/2
    for i,(n,t) in enumerate(cols):
        xx=start+i*(cw+gap); d.rounded_rectangle((xx,y,xx+cw,y+400),radius=50,fill=CARD)
        nf=F("Bold",150 if len(n)<5 else 122); tf=F("Bold",38)
        d.text((xx+cw/2-d.textlength(n,font=nf)/2,y+205),n,font=nf,fill=CORAL,anchor="ls")
        d.text((xx+cw/2-d.textlength(t,font=tf)/2,y+310),t,font=tf,fill=VIN,anchor="ls")
img,d=new(); stack(img,d,[T([[("Quem já escolheu cuidar da equipe",VIN)]],"Bold",84),CUSTOM(400,numbers),footnote("No Ceará, Rio Grande do Norte e Maranhão.")],BOX)
paste_logo(img); slides.append((img,9))
# 12
img,d=new(); stack(img,d,[T([[("Cuidar de pessoas",VIN)],[("é fazer negócios",VIN)],[("ir ",VIN),("mais longe.",CORAL)]],"Bold",104)],(M,190,830,890),cap=1.0,align='left')
photo_card(img,"19.jpg",(870,190,W-M,890),(0.38,0.5)); paste_logo(img); slides.append((img,9))
# 13
img,d=new(); stack(img,d,[T([[("Vamos conversar",VIN)],[("sobre o futuro",VIN)],[("da ",VIN),("sua equipe?",CORAL)]],"Bold",104),CARDI("@nexiasaude  |  (88) 8191-1058",38,"Bold")],LEFT,cap=1.0,align='left')
photo_card(img,"18.jpg",PHOTO,(0.36,0.45)); paste_logo(img); slides.append((img,9))

if NOTEXT:
    json.dump(dict(texts=REC, durs=[sl[1] for sl in slides]), open(f"{OUT}/texto.json","w"), ensure_ascii=False)
paths=[];durs=[];anim=[]
for i,sl in enumerate(slides,1):
    p=f"{OUT}/slides/tela_{i:02d}.png"; sl[0].save(p); paths.append(p); durs.append(sl[1]); anim.append(len(sl)>2)
if NOTEXT: print('base ok', len(slides)); sys.exit(0)
FADE=0.6; FPS=30; cmd=["ffmpeg","-y"]
for p,dur,a in zip(paths,durs,anim): cmd += ["-i",p] if a else ["-loop","1","-t",str(dur),"-framerate",str(FPS),"-i",p]
fc=[];labels=[]
for k,a in enumerate(anim):
    fc.append(f"[{k}:v]scale=3840:2160,zoompan=z='1+0.03*on/{durs[k]*FPS}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={durs[k]*FPS}:s=1920x1080:fps={FPS},setsar=1[a{k}]" if a else f"[{k}:v]fps={FPS},setsar=1[a{k}]"); labels.append(f"[a{k}]")
prev=labels[0]; acc=durs[0]
for k in range(1,len(paths)):
    fc.append(f"{prev}{labels[k]}xfade=transition=fade:duration={FADE}:offset={round(acc-k*FADE,3)}[v{k}]"); prev=f"[v{k}]"; acc+=durs[k]
cmd+=["-filter_complex",";".join(fc),"-map",prev,"-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-r",str(FPS),f"{OUT}/telao_connect_valley_rascunho.mp4"]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
print("ok", sum(durs)-FADE*(len(paths)-1), len(paths),"telas")
