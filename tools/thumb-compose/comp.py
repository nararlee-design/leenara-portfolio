import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
SRC=sys.argv[1]; OUT=sys.argv[2]
W,H=2560,1440
def bg():
    y,x=np.mgrid[0:H,0:W].astype(np.float32)
    base=np.zeros((H,W,3),np.float32); base[:]=(17,18,20)
    d=np.sqrt(((x-W*0.92)/(W*0.55))**2+((y-H*0.02)/(H*0.75))**2)
    g=np.clip(1-d,0,1)**1.6*0.42
    teal=np.array([31,143,132],np.float32)
    base=base*(1-g[...,None])+teal*g[...,None]
    d2=np.sqrt(((x-W*0.05)/(W*0.5))**2+((y-H*1.05)/(H*0.7))**2)
    g2=np.clip(1-d2,0,1)**2*0.12
    base=base*(1-g2[...,None])+teal*g2[...,None]
    rng=np.random.default_rng(3); base+=rng.normal(0,2.2,(H,W,1))
    return Image.fromarray(np.clip(base,0,255).astype(np.uint8)).convert('RGBA')
def rounded(im,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.size[0]-1,im.size[1]-1),r,fill=255)
    o=im.convert('RGBA'); o.putalpha(m); return o
def shadow(canvas,box,r,blur=40,off=(0,24),alpha=150):
    x,y,w,h=box
    s=Image.new('RGBA',canvas.size,(0,0,0,0)); ImageDraw.Draw(s).rounded_rectangle((x+off[0],y+off[1],x+w+off[0],y+h+off[1]),r,fill=(0,0,0,alpha))
    canvas.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))
def place(canvas,im,x,y,w,r=16,sh=True,blur=40,alpha=150):
    h=round(im.size[1]*w/im.size[0]); im=im.convert('RGB').resize((w,h),Image.LANCZOS)
    if sh: shadow(canvas,(x,y,w,h),r,blur,(0,int(blur*0.6)),alpha)
    canvas.alpha_composite(rounded(im,r),(x,y)); return h
def browser(im,w,crop=None):
    if crop: im=im.crop(crop)
    im=im.convert('RGB'); scale=w/im.size[0]; im=im.resize((w,round(im.size[1]*scale)),Image.LANCZOS)
    bar=44; frame=Image.new('RGB',(w,im.size[1]+bar),(28,29,33)); d=ImageDraw.Draw(frame)
    for i,c in enumerate([(255,95,87),(254,188,46),(40,200,64)]): d.ellipse((22+i*26,bar//2-7,36+i*26,bar//2+7),fill=c)
    d.rounded_rectangle((w*0.3,10,w*0.7,bar-10),8,fill=(42,44,49))
    frame.paste(im,(0,bar)); return frame
def S(n): return Image.open(SRC+'/'+n)
mode=sys.argv[3]
c=bg()
if mode=='mockup':
    back=browser(S('리스트_공동구매(3개).png'),1500,(0,0,1680,1200))
    front=browser(S('상세_옵션(선택 후).png'),1560,(0,0,1680,1180))
    place(c,back,250,150,1500,r=18,blur=50,alpha=170)
    # dim back slightly
    ov=Image.new('RGBA',c.size,(0,0,0,0)); 
    place(c,front,760,330,1560,r=18,blur=60,alpha=190)
elif mode=='collage':
    det=S('상세_옵션(선택 후).png').crop((300,270,1380,880))
    order=S('주문-결제_scroll.png').crop((470,155,1199,1045))
    lst=S('마이페이지_리스트.png').crop((640,480,1380,1110))
    done=S('주문-결제  결제완료 팝업.png').crop((554,400,1150,606))
    cancel=S('마이페이지  취소-교환-반품 요청  확인 팝업.png').crop((542,179,1138,385))
    place(c,det,200,250,900,r=16,blur=50,alpha=150)
    place(c,lst,1530,330,820,r=16,blur=50,alpha=150)
    place(c,order,860,110,840,r=18,blur=70,alpha=200)
    place(c,done,1580,180,560,r=14,blur=40,alpha=180)
    place(c,cancel,330,830,560,r=14,blur=40,alpha=180)
c.convert('RGB').save(OUT,quality=88)
