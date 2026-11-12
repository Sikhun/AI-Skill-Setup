"""Torn-paper stickers with a stop-motion "boiling" edge (Vintage Sketch Studio).
  python3 torn.py host IN.png OUTDIR [frames=3]   -> OUTDIR/f0.png.. (figure on a torn cream-paper cut-out)
  python3 torn.py rect W H OUTDIR [frames=3]      -> OUTDIR/f0.png.. (blank torn-paper card W x H for props)
Each frame re-tears the edge with a new noise seed; play the frames on a loop at 8 fps (hold each 3 frames @24fps)."""
import sys, os, numpy as np
from PIL import Image, ImageFilter, ImageDraw
import random

PAPER=np.array([248,244,234])/255; FIBER=np.array([226,220,207])/255
def blur(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)/255
def dilate(a,r):
    m=Image.fromarray((a*255).astype(np.uint8)); s=4
    sm=m.resize((m.width//s,m.height//s),Image.BILINEAR)
    k=max(3,(r//s)*2+1); sm=sm.filter(ImageFilter.MaxFilter(k if k<=31 else 31))
    if k>31: sm=sm.filter(ImageFilter.MaxFilter(k-30 if (k-30)%2 else k-29))
    return np.asarray(sm.resize(m.size,Image.BILINEAR)).astype(np.float32)/255
def noise(h,w,seed):
    rng=np.random.default_rng(seed); n=np.zeros((h,w),np.float32)
    for sc,amp in ((90,1.0),(30,.6),(9,.45),(3,.3)):
        g=rng.random((h//sc+2,w//sc+2)).astype(np.float32)
        n+=amp*(np.asarray(Image.fromarray((g*255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(np.float32)/255-.5)
    return n
def paper_tex(h,w,seed):
    rng=np.random.default_rng(seed+99); g=rng.random((h,w)).astype(np.float32)
    g=blur(g,0.8)*.6+blur(rng.random((h,w)),6)*.4
    return (g-.5)*.08

def tear(base_mask, seed, pad_r):
    """base_mask: float 0..1 shape to surround. returns (paper_alpha, fiber_alpha)."""
    h,w=base_mask.shape
    d=blur(dilate(base_mask,pad_r),pad_r*0.35)
    n=noise(h,w,seed)
    paper=np.clip((d+0.30*n-0.5)*14,0,1)                    # ragged outer edge
    fib_out=np.clip((d+0.30*n+0.05*noise(h,w,seed+7)-0.40)*14,0,1)  # a bit further out: white torn fibres
    inner=np.clip((d+0.30*n-0.62)*14,0,1)
    fiber=np.clip(fib_out-inner,0,1)*(0.6+0.4*(noise(h,w,seed+3)>-.05))
    return np.maximum(paper,fib_out), fiber


# ---- angular (faceted) tear: straight torn segments ----
def trace(mask):
    """outer contour of the largest blob (Moore tracing) on a small boolean grid"""
    h,w=mask.shape; m=np.zeros((h+2,w+2),bool); m[1:-1,1:-1]=mask
    ys,xs=np.nonzero(m); i=np.argmin(ys*10000+xs); start=(ys[i],xs[i])
    nb=[(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    cur=start; d=6; pts=[cur]
    for _ in range(200000):
        for k in range(8):
            dd=(d+k)%8; ny,nx=cur[0]+nb[dd][0],cur[1]+nb[dd][1]
            if m[ny,nx]: cur=(ny,nx); d=(dd+5)%8; break
        if cur==start: break
        pts.append(cur)
    return [(x-1,y-1) for y,x in pts]
def dp(pts,eps):
    if len(pts)<3: return pts
    (x1,y1),(x2,y2)=pts[0],pts[-1]; L=max(np.hypot(x2-x1,y2-y1),1e-6)
    d=[abs((y2-y1)*x-(x2-x1)*y+x2*y1-y2*x1)/L for x,y in pts[1:-1]]
    i=int(np.argmax(d))+1
    if d[i-1]>eps: return dp(pts[:i+1],eps)[:-1]+dp(pts[i:],eps)
    return [pts[0],pts[-1]]
def facet_poly(base_mask,pad,eps):
    s=4; h,w=base_mask.shape
    sm=np.asarray(Image.fromarray((base_mask*255).astype(np.uint8)).resize((w//s,h//s),Image.BILINEAR))>100
    big=dilate(sm.astype(np.float32),pad//s*2)>0.5 if False else None
    d=np.asarray(Image.fromarray((sm*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(min(31,(pad//s)*2+1))))>0
    d=np.asarray(Image.fromarray((d*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(pad/s*0.6)))>90
    c=trace(d); n=len(c); a=dp(c[:n//2+1],eps/s); b=dp(c[n//2:]+[c[0]],eps/s)
    return [(x*s+s/2,y*s+s/2) for x,y in a[:-1]+b[:-1]]
def tear_facet(poly,shape,seed,jit=4,micro=1.0):
    rnd=random.Random(seed); h,w=shape
    pts=[]
    for i in range(len(poly)):                      # split long edges so tears stay angular but irregular
        x1,y1=poly[i]; x2,y2=poly[(i+1)%len(poly)]; L=np.hypot(x2-x1,y2-y1); k=max(1,int(L//rnd.uniform(70,130)))
        for j in range(k):
            t=j/k; off=rnd.uniform(-jit,jit) if j else 0
            nx,ny=-(y2-y1)/max(L,1),(x2-x1)/max(L,1)
            pts.append((x1+(x2-x1)*t+nx*off+rnd.uniform(-jit,jit)*.5,y1+(y2-y1)*t+ny*off+rnd.uniform(-jit,jit)*.5))
    im=Image.new('L',(w,h),0); ImageDraw.Draw(im).polygon(pts,fill=255)
    a=np.asarray(im).astype(np.float32)/255
    n=noise(h,w,seed)
    hi=np.random.default_rng(seed).random((h,w)).astype(np.float32)
    edge=blur(a,2.2)
    paper=np.clip((edge+0.10*micro*n+0.10*micro*(blur(hi,0.7)-.5)*2-0.5)*9,0,1)   # small jagged tooth on straight cuts
    outer=np.clip((blur(a,6)+0.12*n+0.22*(blur(hi,0.6)-.5)*2-0.36)*6,0,1)
    fiber=np.clip(outer-paper,0,1)*(0.75+0.25*(hi>0.5))
    return np.maximum(paper,outer), fiber

def shifted(x,dy,dx):
    o=np.zeros_like(x); o[dy:,dx:]=x[:x.shape[0]-dy,:x.shape[1]-dx]; return o
def compose(paper_a, fiber_a, figure=None, seed=0, shift=(0,0)):
    h,w=paper_a.shape
    rgb=np.ones((h,w,3),np.float32)*PAPER+paper_tex(h,w,seed)[...,None]
    # light from top-left: rim facing the light is bright white fibre, rim facing away is grey/darker (gives thickness)
    b=blur(paper_a,3); gy,gx=np.gradient(b); facing=np.clip((gx+gy)*-6,-1,1)   # >0 faces top-left
    rim=fiber_a
    lit=np.array([1.0,0.995,0.98]); dark=np.array([0.80,0.76,0.69])
    rimc=np.where((facing>0)[...,None],lit,dark)
    rgb=rgb*(1-rim[...,None])+rimc*rim[...,None]
    # paper slightly darker toward its edge (soft curl)
    inner=np.clip(1-blur(paper_a,9),0,1)*paper_a
    rgb=rgb*(1-0.10*inner[...,None])
    a=paper_a.copy()
    if figure is not None:
        fa=figure[...,3]
        cs=shifted(blur(fa,3),4,3)*0.35*(1-fa)      # figure casts a small shadow on its paper
        rgb=rgb*(1-cs[...,None])
        rgb=rgb*(1-fa[...,None])+figure[...,:3]*fa[...,None]; a=np.maximum(a,fa)
    out=np.dstack([np.clip(rgb,0,1),a])
    # two-layer drop shadow: tight contact + soft ambient
    sh=np.maximum(shifted(blur(a,2.5),4,3)*0.6, shifted(blur(a,12),14,9)*0.38)
    final_a=a+sh*(1-a)
    final_rgb=(out[...,:3]*a[...,None]+np.array([.20,.14,.09])*(sh*(1-a))[...,None])/np.maximum(final_a,1e-4)[...,None]
    img=Image.fromarray((np.dstack([np.clip(final_rgb,0,1),final_a])*255).astype(np.uint8),'RGBA')
    if shift!=(0,0) or seed%3:
        ang=[0,0.7,-0.6][seed%3]; img=img.rotate(ang,resample=Image.BICUBIC,translate=shift)
    return img

def clean_figure(path,pad):
    im=np.asarray(Image.open(path).convert('RGBA')).astype(np.float32)/255
    a=im[...,3]; a=np.where(a>0.9,1,np.where(a<0.1,0,a))
    rgb=im[...,:3]
    # kill coloured fringes from background removal: desaturate a rim band
    core=blur((a>0.5).astype(np.float32),3)>0.97
    lum=(rgb@[0.299,0.587,0.114])[...,None]
    marble=lum*np.array([1.0,0.98,0.94])
    rgb=np.where(core[...,None],rgb,marble)
    a=a*(blur((a>0.5).astype(np.float32),1.2)>0.5)
    fig=np.dstack([rgb,a]); H,W=a.shape
    big=np.zeros((H+2*pad,W+2*pad,4),np.float32); big[pad:pad+H,pad:pad+W]=fig
    return big

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='host':
        src,out=sys.argv[2],sys.argv[3]; n=int(sys.argv[4]) if len(sys.argv)>4 else 3
        os.makedirs(out,exist_ok=True); pad=70
        fig=clean_figure(src,pad); m=(fig[...,3]>0.5).astype(np.float32)
        poly=facet_poly(m,24,16)
        for i in range(n):
            pa,fa=tear_facet(poly,m.shape,1000+i*17)
            compose(pa,fa,fig,seed=i,shift=[(0,0),(2,-1),(-1,2)][i%3]).save(f'{out}/f{i}.png')
    else:
        W,H,out=int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]; n=int(sys.argv[5]) if len(sys.argv)>5 else 3
        os.makedirs(out,exist_ok=True); pad=60
        m=np.zeros((H+2*pad,W+2*pad),np.float32); m[pad+18:pad+H-18,pad+18:pad+W-18]=1
        poly=[(pad+6,pad+6),(pad+W-6,pad+6),(pad+W-6,pad+H-6),(pad+6,pad+H-6)]
        for i in range(n):
            pa,fa=tear_facet(poly,m.shape,500+i*31,jit=7)
            compose(pa,fa,None,seed=i,shift=[(0,0),(1,-1),(-1,1)][i%3]).save(f'{out}/f{i}.png')
    print('ok')
