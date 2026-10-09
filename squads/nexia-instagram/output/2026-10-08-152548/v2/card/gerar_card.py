import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC, OUT = sys.argv[1], sys.argv[2]
W, H = 1080, 1440
MAG=(232,33,94); NAVY=(48,16,98); PINK_FOOT=(252,180,200); WHITE=(255,255,255)
F="/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(w,s): return ImageFont.truetype(F%w,s)

# fundo em degradê rosa
bg=Image.new("RGB",(W,H))
px=bg.load()
for y in range(H):
    t=y/H
    c=tuple(int(a+(b-a)*t) for a,b in zip((255,232,238),(251,196,213)))
    for x in range(W): px[x,y]=c
img=bg.convert("RGBA"); d=ImageDraw.Draw(img)

# laço decorativo suave (curvas translúcidas)
ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
od.ellipse((620,-260,1260,420),outline=(240,90,140,110),width=70)
ov=ov.filter(ImageFilter.GaussianBlur(3)); img=Image.alpha_composite(img,ov); d=ImageDraw.Draw(img)

M=80
# selo
d.rounded_rectangle((M,90,M+360,160),radius=35,fill=MAG)
f=font("Medium",30); txt="O U T U B R O   R O S A"
d.text((M+180,125),txt,font=font("Medium",26),fill=WHITE,anchor="mm")

# título
y=200
for t,c in (("Você tem",NAVY),("ginecologia e",MAG),("psicologia",MAG),("no seu plano.",NAVY)):
    d.text((M,y),t,font=font("ExtraBold",88),fill=c,anchor="la"); y+=100
# apoio
d.text((M,y+25),"Consulta por telemedicina,",font=font("Medium",40),fill=NAVY,anchor="la")
d.text((M,y+78),"agendada pela Nexia Saúde.",font=font("Medium",40),fill=NAVY,anchor="la")

# foto recortada da arte de parceria já existente
src=Image.open(SRC).convert("RGB")
ph=src.crop((740,190,1374,930)).resize((400,468),Image.LANCZOS)  # só a mulher e o notebook
m=Image.new("L",ph.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+ph.size,radius=44,fill=255)
img.paste(ph,(W-M-400,770),m)

# cartões de benefício à esquerda da foto
def chip(y0,title,sub):
    d.rounded_rectangle((M,y0,M+470,y0+170),radius=34,fill=(255,240,245))
    d.ellipse((M+22,y0+30,M+132,y0+140),fill=MAG)
    return y0
chip(780,"","")
chip(960,"","")
# ícone ginecologista recortado da arte existente
ic=src.crop((135,610,245,720)).resize((110,110),Image.LANCZOS)
cm=Image.new("L",ic.size,0); ImageDraw.Draw(cm).ellipse((0,0)+ic.size,fill=255)
img.paste(ic,(M+22,810),cm)
# ícone psicologia: coração dentro de balão de fala
cx,cy=M+77,1025
d.rounded_rectangle((cx-28,cy-24,cx+28,cy+14),radius=12,fill=WHITE)
d.polygon([(cx-14,cy+12),(cx-4,cy+12),(cx-18,cy+30)],fill=WHITE)
d.ellipse((cx-15,cy-16,cx,cy-2),fill=MAG); d.ellipse((cx,cy-16,cx+15,cy-2),fill=MAG)
d.polygon([(cx-15,cy-8),(cx+15,cy-8),(cx,cy+8)],fill=MAG)
d.text((M+150,832),"Ginecologia",font=font("ExtraBold",38),fill=NAVY,anchor="la")
d.text((M+150,880),"por telemedicina",font=font("Medium",30),fill=NAVY,anchor="la")
d.text((M+150,1012),"Psicologia",font=font("ExtraBold",38),fill=NAVY,anchor="la")
d.text((M+150,1060),"no seu plano",font=font("Medium",30),fill=NAVY,anchor="la")

# botão
d.rounded_rectangle((M,1160,M+470,1260),radius=50,fill=MAG)
d.text((M+235,1210),"Agende pelo link.",font=font("ExtraBold",40),fill=WHITE,anchor="mm")

# rodapé com logo da Nexia (recortado da arte existente)
d.rectangle((0,1320,W,H),fill=PINK_FOOT)
logo=src.crop((160,992,620,1092))
img.paste(logo.convert("RGBA"),(W//2-logo.width//2,1320+(H-1320-logo.height)//2))
img.convert("RGB").save(OUT)
