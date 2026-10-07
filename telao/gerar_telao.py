import sys, subprocess
from PIL import Image, ImageDraw, ImageFont

OUT, LOGO, FONTS, IMGS = sys.argv[1:5]
W, H = 1920, 1080
VIN, CORAL, CREME, CARD, GRAY = (75,15,47), (255,111,104), (255,247,242), (255,239,232), (140,110,125)
def F(w, s):
    f = "IntroBold" if w in ("ExtraBold","Bold") else "IntroBook"
    return ImageFont.truetype(f"{FONTS}/{f}.otf", s)

logo_w = Image.open(LOGO).convert("RGBA")
logo = logo_w.copy(); px = logo.load()
for y in range(logo.height):
    for x in range(logo.width):
        r,g,b,a = px[x,y]
        if a > 0 and r > 200 and g > 200 and b > 200: px[x,y] = (43,27,77,a)
def paste_logo(img, width, left=None, right=None, bottom=None, top=None, cx=None, cy=None, white=False):
    src = logo_w if white else logo
    l = src.resize((width, int(src.height*width/src.width)), Image.LANCZOS)
    x = cx - l.width//2 if cx is not None else (left if left is not None else W - right - l.width)
    y = cy - l.height//2 if cy is not None else (top if top is not None else H - bottom - l.height)
    img.paste(l, (x,y), l)

def tw(d, segs, f): return sum(d.textlength(t, font=f) for t,_ in segs)
def block(d, lines, weight, size, y, align="left", x0=130, maxw=1660, gap=1.15):
    while True:
        f = F(weight, size)
        if max(tw(d,l,f) for l in lines) <= maxw or size < 30: break
        size -= 2
    for l in lines:
        w = tw(d,l,f); x = x0 if align=="left" else (W-w)/2
        for t,c in l:
            d.text((x,y), t, font=f, fill=c); x += d.textlength(t, font=f)
        y += int(size*gap)
    return y
def card(d, box, txt, size=44, weight="Medium", color=VIN):
    d.rounded_rectangle(box, radius=40, fill=CARD)
    f = F(weight, size); x0,y0,x1,y1 = box
    d.text((x0+(x1-x0-d.textlength(txt,font=f))/2, y0+(y1-y0-size)/2-6), txt, font=f, fill=color)
def tag(d, n): d.text((130,70), f"[{n:02d}]", font=F("Medium",34), fill=CORAL)
def footer(d, txt): d.text((130,H-70), txt, font=F("Medium",26), fill=GRAY)
def new(): im = Image.new("RGB",(W,H),(255,255,255)); return im, ImageDraw.Draw(im)

def photo_card(img, name, box, focus=(0.5,0.5), tint=115, radius=50):
    x0,y0,x1,y1 = box; bw,bh = x1-x0, y1-y0
    im = Image.open(f"{IMGS}/{name}").convert("RGB")
    s = max(bw/im.width, bh/im.height)
    im = im.resize((int(im.width*s)+1, int(im.height*s)+1), Image.LANCZOS)
    cx = int(focus[0]*im.width); cy = int(focus[1]*im.height)
    l = min(max(cx-bw//2,0), im.width-bw); t = min(max(cy-bh//2,0), im.height-bh)
    im = im.crop((l,t,l+bw,t+bh)).convert("RGBA")
    im = Image.alpha_composite(im, Image.new("RGBA",(bw,bh),VIN+(tint,)))
    mask = Image.new("L",(bw,bh),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,bw,bh), radius=radius, fill=255)
    img.paste(im.convert("RGB"), (x0,y0), mask)

slides = []
PH = (1030,110,1790,930)
# 1
img,d = new(); tag(d,1)
block(d, [[("Quanto ",VIN),("custa",CORAL),(" para",VIN)],[("sua empresa um",VIN)],[("funcionário não",VIN)],[("conseguir trabalhar?",VIN)]], "Bold", 108, 190, maxw=880)
photo_card(img,"17.jpg",PH,(0.40,0.5))
paste_logo(img, 260, right=100, bottom=60); slides.append((img,9))
# 2
img,d = new(); tag(d,2)
block(d, [[("Agora multiplique por",VIN)]], "Medium", 76, 190, maxw=880)
block(d, [[("×100",CORAL)]], "Bold", 430, 270, maxw=880)
block(d, [[("funcionários.",VIN)]], "Bold", 120, 650, maxw=880)
photo_card(img,"16.jpg",PH,(0.5,0.38))
paste_logo(img, 260, right=100, bottom=60); slides.append((img,6))
# 3
img,d = new(); tag(d,3)
block(d, [[("Um dia de falta não custa",VIN)]], "Bold", 96, 170)
block(d, [[("R$ 54.",CORAL)]], "Bold", 380, 260)
block(d, [[("Custa muito mais.",VIN)]], "Bold", 120, 680)
card(d,(130,860,1250,980),"O salário é só a ponta do custo.",46)
footer(d,"Base: salário mínimo 2026 (R$ 1.621 ÷ 30 dias)")
paste_logo(img, 260, right=100, bottom=70); slides.append((img,9))
# 4
img,d = new(); tag(d,4)
d.text((130,150),"“",font=F("Bold",420),fill=CORAL)
block(d, [[("A falta aparece no ponto.",VIN)]], "Bold", 120, 470)
block(d, [[("O prejuízo aparece no ",VIN),("resultado.",CORAL)]], "Bold", 120, 640)
paste_logo(img, 260, right=100, bottom=70); slides.append((img,6))
# 5
img,d = new(); tag(d,5)
block(d, [[("546 mil",CORAL)]], "Bold", 380, 150)
block(d, [[("afastamentos por saúde mental",VIN)],[("no Brasil em 2025.",VIN)]], "Bold", 100, 600)
card(d,(130,850,720,970),"+15% em um ano",52,"Bold",CORAL)
footer(d,"Fonte: Ministério da Previdência Social")
paste_logo(img, 260, right=100, bottom=70); slides.append((img,9))
# 6
img,d = new(); tag(d,6)
block(d, [[("4,1 milhões",CORAL)]], "Bold", 330, 160)
block(d, [[("de afastamentos temporários do trabalho",VIN)],[("em 2025.",VIN)]], "Bold", 92, 590)
card(d,(130,850,720,970),"+17% em um ano",52,"Bold",CORAL)
footer(d,"Fonte: Ministério da Previdência Social")
paste_logo(img, 260, right=100, bottom=70); slides.append((img,9))
# 7
img,d = new(); tag(d,7)
block(d, [[("NR-1",CORAL)]], "Bold", 300, 130)
block(d, [[("não é só obrigação.",VIN)],[("É gestão de um risco que",VIN)],[("custa dinheiro.",CORAL)]], "Bold", 100, 470)
card(d,(130,880,1300,990),"Risco psicossocial também aparece no caixa.",44)
paste_logo(img, 260, right=100, bottom=70); slides.append((img,9))
# 8 NR-1 UAU
grad = Image.new("RGB",(W,H)); gp = grad.load()
for yy in range(H):
    for xx in range(W):
        t = (xx/W*0.6 + yy/H*0.4)
        gp[xx,yy] = (int(75+(49-75)*t), int(15+(35-15)*t), int(47+(95-47)*t))
img = grad; d = ImageDraw.Draw(img)
pf = F("Bold",36); ptxt = "NR-1  ·  RISCOS PSICOSSOCIAIS"
pw = int(d.textlength(ptxt,font=pf))+90
d.rounded_rectangle((130,90,130+pw,170), radius=40, fill=CORAL)
d.text((175,108),ptxt,font=pf,fill=(255,255,255))
block(d, [[("Sua empresa está",CREME)],[("pronta para a",CREME)]], "Bold", 104, 205, maxw=840, gap=1.08)
block(d, [[("NR-1?",CORAL)]], "Bold", 300, 425, maxw=840)
block(d, [[("A Nexia faz grande parte desse caminho,",CREME)],[("com suporte e pós-venda.",CREME)]], "Medium", 42, 760, maxw=860, gap=1.3)
d.rounded_rectangle((130,880,970,990), radius=55, fill=CREME)
d.text((180,904),"Entre e converse com a gente  →", font=F("Bold",46), fill=VIN)
photo_card(img,"15.jpg",(1030,190,1790,990),(0.58,0.62),tint=70)
paste_logo(img, 300, right=130, top=62, white=True)
slides.append((img,9,True))
# 9
img,d = new(); tag(d,9)
block(d, [[("Cuidar da saúde pode ser caro.",VIN)]], "Bold", 96, 190)
block(d, [[("Não cuidar é",VIN)]], "Bold", 96, 340)
block(d, [[("mais caro",CORAL)]], "Bold", 330, 440)
block(d, [[("ainda.",VIN)]], "Bold", 120, 800)
paste_logo(img, 260, right=100, bottom=70); slides.append((img,9))
# 10
img,d = new(); tag(d,10)
block(d, [[("Saúde na palma",VIN)],[("da mão.",VIN)],[("Sem deslocamento.",CORAL)]], "Bold", 120, 230, maxw=800)
d.rounded_rectangle((1000,190,1800,800), radius=50, fill=CARD)
items = ["Clínico geral 24h","Mais de 12 especialidades","Psicologia e nutrição","Clubes de benefícios","nacional e regional"]
y=250
for i,t in enumerate(items):
    if i<4: d.ellipse((1050,y+16,1078,y+44), fill=CORAL)
    d.text((1100, y), t, font=F("Bold" if i<4 else "Medium",46), fill=VIN)
    y += 120 if i!=3 else 62
paste_logo(img, 260, right=100, bottom=70); slides.append((img,9))
# 11
img,d = new(); tag(d,11)
block(d, [[("Quem já escolheu cuidar da equipe",VIN)]], "Bold", 80, 160)
cols = [("+50","empresas clientes"),("+2.000","pessoas beneficiadas"),("+200","profissionais parceiros")]
for i,(n,t) in enumerate(cols):
    x0 = 130 + i*570
    d.rounded_rectangle((x0,330,x0+520,780), radius=50, fill=CARD)
    d.text((x0+40,360), f"[{i+1:02d}]", font=F("Medium",30), fill=CORAL)
    d.text((x0+40,470), n, font=F("Bold",150 if len(n)<5 else 118), fill=CORAL)
    d.text((x0+40,680), t, font=F("Bold",40), fill=VIN)
d.text((130,830),"No Ceará, Rio Grande do Norte e Maranhão.", font=F("Medium",40), fill=GRAY)
paste_logo(img, 260, right=100, bottom=70); slides.append((img,9))
# 12
img,d = new()
block(d, [[("Cuidar de pessoas",VIN)],[("é fazer negócios",VIN)],[("ir ",VIN),("mais longe.",CORAL)]], "Bold", 112, 200, maxw=880)
photo_card(img,"19.jpg",PH,(0.5,0.45))
paste_logo(img, 520, left=130, bottom=80); slides.append((img,9))
# 13
img,d = new()
block(d, [[("Vamos conversar",VIN)],[("sobre o futuro",VIN)],[("da ",VIN),("sua equipe?",CORAL)]], "Bold", 112, 140, maxw=880)
card(d,(130,640,960,760),"@nexiasaude  |  (88) 8191-1058",42,"Bold")
photo_card(img,"18.jpg",PH,(0.30,0.45))
paste_logo(img, 520, left=130, bottom=80); slides.append((img,9))

paths=[]; durs=[]; anim=[]
for i,sl in enumerate(slides,1):
    p=f"{OUT}/slides/tela_{i:02d}.png"; sl[0].save(p); paths.append(p); durs.append(sl[1]); anim.append(len(sl)>2)
FADE=0.6; FPS=30
cmd=["ffmpeg","-y"]
for p,dur,a in zip(paths,durs,anim):
    cmd += ["-i",p] if a else ["-loop","1","-t",str(dur),"-framerate",str(FPS),"-i",p]
fc=[]; labels=[]
for k,a in enumerate(anim):
    if a: fc.append(f"[{k}:v]scale=3840:2160,zoompan=z='1+0.06*on/{durs[k]*FPS}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={durs[k]*FPS}:s=1920x1080:fps={FPS},setsar=1[a{k}]")
    else: fc.append(f"[{k}:v]fps={FPS},setsar=1[a{k}]")
    labels.append(f"[a{k}]")
prev=labels[0]; acc=durs[0]
for k in range(1,len(paths)):
    off=round(acc-k*FADE,3); fc.append(f"{prev}{labels[k]}xfade=transition=fade:duration={FADE}:offset={off}[v{k}]"); prev=f"[v{k}]"; acc+=durs[k]
cmd+=["-filter_complex",";".join(fc),"-map",prev,"-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-r",str(FPS),f"{OUT}/telao_connect_valley_rascunho.mp4"]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
print("ok", sum(durs)-FADE*(len(paths)-1), len(paths),"telas")
