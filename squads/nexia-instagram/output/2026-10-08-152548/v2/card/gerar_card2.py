import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BR, FONTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1080, 1350
PURPLE=(49,35,95); WINE=(110,24,66); CORAL=(233,58,82); CREAM=(255,226,206); WHITE=(255,255,255); ROSE=(247,120,170)
def F(kind,size):
    p={"title":f"{FONTS}/fontsource-fredoka/package/files/fredoka-latin-600-normal.woff",
       "body":f"{FONTS}/fontsource-quicksand/package/files/quicksand-latin-700-normal.woff",
       "bodyb":f"{FONTS}/fontsource-nunito/package/files/nunito-latin-800-normal.woff"}[kind]
    return ImageFont.truetype(p,size)

# fundo: degradê diagonal roxo -> vinho, como nos posts do feed
bg=Image.new("RGB",(W,H)); px=bg.load()
for y in range(H):
    for x in range(W):
        t=min(1,max(0,(0.35*x+0.65*y)/(0.35*W+0.65*H)))
        t=t**1.15
        px[x,y]=tuple(int(a+(b-a)*t) for a,b in zip(PURPLE,WINE))
img=bg.convert("RGBA")
# linhas finas decorativas
ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
od.arc((-300,350,900,1500),200,340,fill=(255,255,255,26),width=3)
od.arc((-100,100,1300,1300),20,120,fill=(255,255,255,20),width=3)
img=Image.alpha_composite(img,ov)

# marca grande (ícone do logo) em coral, cortada pela borda, como nos posts
logo=Image.open(f"{BR}/logo-horizontal-nexia-branco-icone-coral.png").convert("RGBA")
icon=logo.crop((995,150,1300,440))
iw=740; ih=int(icon.height*iw/icon.width)
icon=icon.resize((iw,ih),Image.LANCZOS)
img.alpha_composite(icon,(660,880))
d=ImageDraw.Draw(img)

M=84
# título
y=160
for t,c in (("Seu plano tem",CREAM),("clínico geral",CORAL),("24 horas,",CORAL),("todos os dias.",CREAM)):
    d.text((M,y),t,font=F("title",108),fill=c,anchor="la"); y+=116
# apoio
fy=y+36
x=M
for t,c,k in (("Acesse a ",CREAM,"body"),("plataforma completa",CORAL,"bodyb")):
    d.text((x,fy),t,font=F(k,42),fill=c,anchor="la"); x+=d.textlength(t,font=F(k,42))
d.text((M,fy+58),"de saúde da Nexia.",font=F("body",42),fill=CREAM,anchor="la")

# botão
by=fy+190
d.rounded_rectangle((M,by,M+500,by+104),radius=52,fill=CORAL)
d.text((M+250,by+52),"Acesse a plataforma.",font=F("title",40),fill=WHITE,anchor="mm")

# logo no rodapé à esquerda
lg=logo.crop((208,161,1792,429)); lw=400; lh=int(lg.height*lw/lg.width)
lg=lg.resize((lw,lh),Image.LANCZOS)
img.alpha_composite(lg,(M-6,H-100-lh))
img.convert("RGB").save(OUT)
