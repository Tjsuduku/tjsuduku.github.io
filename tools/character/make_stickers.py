import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from scipy import ndimage as ndi
L=LOGOS; OUT=STK_DIR
POP='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
DJ='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def trim(im): return im.crop(im.getbbox())
def fit(im,long=900):
    s=long/max(im.size); return im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)
def unwhite(im):
    a=np.asarray(im.convert('RGB')).astype(float)
    al=np.clip((765-a.sum(2))/120,0,1)
    c=(a-(1-al[...,None])*255)/np.maximum(al[...,None],1e-3)
    return Image.fromarray(np.dstack([np.clip(c,0,255),al*255]).astype(np.uint8),'RGBA')
def hstack(parts,gap=30,valign='center'):
    H=max(p.height for p in parts); W=sum(p.width for p in parts)+gap*(len(parts)-1)
    o=Image.new('RGBA',(W,H),(0,0,0,0)); x=0
    for p in parts: o.alpha_composite(p,(x,(H-p.height)//2)); x+=p.width+gap
    return o
def vstack(parts,gap=20):
    W=max(p.width for p in parts); H=sum(p.height for p in parts)+gap*(len(parts)-1)
    o=Image.new('RGBA',(W,H),(0,0,0,0)); y=0
    for p in parts: o.alpha_composite(p,((W-p.width)//2,y)); y+=p.height+gap
    return o
def text(s,size,color,font=POP):
    f=ImageFont.truetype(font,size); bb=f.getbbox(s)
    im=Image.new('RGBA',(bb[2]-bb[0]+10,bb[3]-bb[1]+10),(0,0,0,0)); ImageDraw.Draw(im).text((5-bb[0],5-bb[1]),s,font=f,fill=color); return trim(im)
def diecut(art,long=900,border=0.055,fillholes=True):
    a=fit(trim(art),long); w,h=a.size
    bd=int(long*border); m=bd+int(long*0.06)
    cw,ch=w+2*m,h+2*m
    al=np.zeros((ch,cw)); al[m:m+h,m:m+w]=np.asarray(a)[...,3]/255
    core=al>0.15
    dist=ndi.distance_transform_edt(~core)
    sh=dist<bd
    sh=ndi.gaussian_filter(sh.astype(float),bd*0.35)>0.5
    if fillholes: sh=ndi.binary_fill_holes(sh)
    edge=ndi.distance_transform_edt(~sh)<max(2,bd*0.10)
    out=np.zeros((ch,cw,4))
    # soft shadow
    shd=ndi.gaussian_filter(ndi.shift(edge.astype(float),(bd*0.25,bd*0.12)),bd*0.3)*0.28
    out[...,:3]=np.array([60,40,30]); out[...,3]=shd
    def over(rgb,alpha):
        A=alpha[...,None]; out[...,:3]=out[...,:3]*(1-A)*(out[...,3:4])/np.maximum(out[...,3:4]*(1-A)+A,1e-6)+np.array(rgb)*A/np.maximum(out[...,3:4]*(1-A)+A,1e-6)
        out[...,3]=out[...,3]*(1-alpha)+alpha
    edge_s=ndi.gaussian_filter(edge.astype(float),1.0)
    over((178,176,172),edge_s)
    over((236,234,228),ndi.gaussian_filter(sh.astype(float),0.8))
    img=Image.fromarray(np.clip(out*[1,1,1,255],0,255).astype(np.uint8),'RGBA')
    img.alpha_composite(a,(m,m))
    # matte print grain
    g=np.asarray(img).astype(float); n=np.zeros(g.shape[:2])
    g[...,:3]=np.clip(g[...,:3]+n[...,None],0,255)
    return Image.fromarray(g.astype(np.uint8),'RGBA')
def save(n,im):
    im.thumbnail((512,512),Image.LANCZOS); im.save(OUT+n+'.png',optimize=True); print(n,im.size)
# SFU: I <3 + SFU block (like Sen's I love SYSU)
sfu=trim(Image.open(L+'sfu_word.png').convert('RGBA').crop((0,0,240,120)))
sfu=sfu.resize((sfu.width*3,sfu.height*3),Image.LANCZOS)
save('sfu',diecut(sfu,border=0.05))
save('jaalik',diecut(unwhite(Image.open(L+'jaalik.png'))))
save('cloverdale',diecut(Image.open(L+'clov_circle.png').convert('RGBA'),border=0.05))
for n in ['instagram','facebook','linkedin','tiktok']:
    save(n,diecut(Image.open(L+n+'.png').convert('RGBA'),border=0.06))
save('chatgpt',diecut(hstack([trim(Image.open(L+'openai.png').convert('RGBA')).resize((300,300),Image.LANCZOS),text('ChatGPT',190,(20,20,20))],gap=30)))
save('claude',diecut(hstack([trim(Image.open(L+'claude-ai.png').convert('RGBA')).resize((300,300),Image.LANCZOS),text('Claude',200,(25,25,25))],gap=25)))

save('reframes',diecut(Image.open(L+'reframes.png').convert('RGBA'),border=0.05))
_b=Image.open(L+'boopdog_original.png').convert('RGBA'); _b=_b.crop(_b.getbbox()); _b=_b.resize((_b.width*4,_b.height*4),Image.LANCZOS)
_pw,_ph=_b.width+80,_b.height+70; _card=Image.new('RGBA',(_pw,_ph),(0,0,0,0)); ImageDraw.Draw(_card).rounded_rectangle((0,0,_pw-1,_ph-1),radius=_ph//3,fill=(255,255,255,255)); _card.alpha_composite(_b,(40,35))
save('boopdog',diecut(_card,border=0.04))

save('telus',diecut(unwhite(Image.open(L+'telus.png')),border=0.05))
save('skechers',diecut(unwhite(Image.open(L+'skechers.png')),border=0.05))
