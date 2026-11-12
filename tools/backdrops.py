"""Original pencil-sketch classical backdrops (code-drawn, sepia). python3 backdrops.py OUTDIR
-> acropolis.svg (temple on the rock + city), columns.svg (close-up Doric ruin). Use at 25-40% multiply over the paper."""
import sys, os, random, math
R=random.Random(5); INK="#4a3526"
def jl(x1,y1,x2,y2,w=2.2,op=.9,passes=2,j=2.2):
    s=''
    for p in range(passes):
        a=(R.uniform(-j,j),R.uniform(-j,j)); b=(R.uniform(-j,j),R.uniform(-j,j))
        mx=(x1+x2)/2+R.uniform(-j,j); my=(y1+y2)/2+R.uniform(-j,j)
        # overshoot a little like a quick pencil stroke
        ox=(x2-x1)*R.uniform(0,.03); oy=(y2-y1)*R.uniform(0,.03)
        s+=f'<path d="M{x1+a[0]-ox:.1f} {y1+a[1]-oy:.1f} Q{mx:.1f} {my:.1f} {x2+b[0]+ox:.1f} {y2+b[1]+oy:.1f}" stroke="{INK}" stroke-width="{w*(1 if p==0 else .6):.2f}" opacity="{op*(1 if p==0 else .55):.2f}" fill="none" stroke-linecap="round"/>'
    return s
def poly(pts,w=2.2,closed=True):
    s=''; n=len(pts)
    for i in range(n if closed else n-1):
        s+=jl(*pts[i],*pts[(i+1)%n],w=w)
    return s
cid=[0]
def hatch(pts,ang=40,gap=9,w=1.2,op=.55):
    cid[0]+=1; c=f'c{cid[0]}'
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    s=f'<clipPath id="{c}"><path d="M'+' L'.join(f'{x} {y}' for x,y in pts)+f' Z"/></clipPath><g clip-path="url(#{c})">'
    t=math.radians(ang); L=(x1-x0)+(y1-y0)+40; cx,cy=(x0+x1)/2,(y0+y1)/2
    k=-L
    while k<L:
        dx,dy=math.cos(t),math.sin(t); nx,ny=-dy,dx
        px,py=cx+nx*k,cy+ny*k
        s+=f'<line x1="{px-dx*L:.0f}" y1="{py-dy*L+R.uniform(-2,2):.0f}" x2="{px+dx*L:.0f}" y2="{py+dy*L+R.uniform(-2,2):.0f}" stroke="{INK}" stroke-width="{w}" opacity="{op*R.uniform(.6,1):.2f}"/>'
        k+=gap*R.uniform(.8,1.2)
    return s+'</g>'
def svg(w,h,body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'

PAPER="#F3EAD6"
def temple(x,y,W,H,cols=8):
    base=y+H; e2=base-36-H*0.62-8
    s=f'<path d="M{x-16} {base} L{x+W+16} {base} L{x+W+14} {e2-48} L{x+W/2} {e2-48-W*0.13} L{x-14} {e2-48} Z" fill="{PAPER}"/>'
    # steps
    for i in range(3): s+=poly([(x-14+i*6,base-i*12),(x+W+14-i*6,base-i*12),(x+W+14-i*6,base-(i+1)*12),(x-14+i*6,base-(i+1)*12)],w=1.8)
    top=base-36; colH=H*0.62; ent=top-colH
    cw=W/(cols*1.55); gap=(W-cw*cols)/(cols-1)
    for i in range(cols):
        cx=x+i*(cw+gap)
        s+=jl(cx,top,cx+cw*.06,ent,w=2)+jl(cx+cw,top,cx+cw*.94,ent,w=2)
        for f in range(1,4): s+=jl(cx+cw*f/4,top-2,cx+cw*f/4,ent+4,w=.9,op=.5,passes=1)
        s+=poly([(cx-5,ent),(cx+cw+5,ent),(cx+cw+3,ent-8),(cx-3,ent-8)],w=1.6)
        s+=hatch([(cx,top),(cx+cw*.35,top),(cx+cw*.35,ent),(cx,ent)],70,6,1,.4)
    # entablature + frieze triglyphs
    e2=ent-8; s+=poly([(x-8,e2),(x+W+8,e2),(x+W+8,e2-22),(x-8,e2-22)],w=2)
    s+=poly([(x-8,e2-22),(x+W+8,e2-22),(x+W+8,e2-48),(x-8,e2-48)],w=2)
    for i in range(int(W/26)): s+=jl(x+i*26+8,e2-24,x+i*26+8,e2-46,w=1.2,op=.7,passes=1)
    # pediment
    s+=poly([(x-14,e2-48),(x+W+14,e2-48),(x+W/2,e2-48-W*0.13)],w=2.2)
    s+=hatch([(x+10,e2-52),(x+W-10,e2-52),(x+W/2,e2-44-W*0.12)],-30,10,1,.35)
    return s

def acropolis():
    W,H=1080,1200; b=''
    # distant hills
    b+=poly([(0,430),(140,380),(260,400),(380,350),(520,390),(640,330),(760,300),(850,250),(930,300),(1080,340)],w=1.6,closed=False)
    b+=hatch([(780,300),(850,250),(930,300),(960,330),(800,330)],80,7,1,.35)
    # rock
    rock=[(40,760),(110,640),(210,600),(300,560),(800,560),(900,590),(990,660),(1060,760)]
    b+='<path d="M'+' L'.join(f'{x} {y}' for x,y in rock+[(1060,820),(40,820)])+f' Z" fill="{PAPER}"/>'
    b+=poly(rock,w=2.4,closed=False)
    b+=hatch(rock+[(1060,820),(40,820)],88,8,1.2,.5)
    for x in range(140,980,55): b+=jl(x,600+R.uniform(-20,10),x+R.uniform(-12,12),780,w=1.1,op=.5,passes=1)
    # Parthenon + small temple
    b+=temple(340,370,420,190,8)
    b+=temple(800,470,120,90,4)
    # city blocks below
    for i in range(26):
        x=R.uniform(20,1000); y=R.uniform(800,1120); w=R.uniform(50,130); h=R.uniform(30,70)
        b+=poly([(x,y),(x+w,y),(x+w,y-h),(x,y-h)],w=1.4)
        b+=jl(x-6,y-h,x+w/2,y-h-18,w=1.2)+jl(x+w/2,y-h-18,x+w+6,y-h,w=1.2)
        for k in range(int(w//28)): b+=poly([(x+10+k*28,y-12),(x+20+k*28,y-12),(x+20+k*28,y-28),(x+10+k*28,y-28)],w=1,closed=True)
        if R.random()<.5: b+=hatch([(x,y),(x+w*.3,y),(x+w*.3,y-h),(x,y-h)],60,6,1,.4)
    # cypress trees
    for x,y in [(120,880),(560,960),(930,900),(300,1080)]:
        b+=poly([(x,y),(x-16,y-40),(x-8,y-100),(x,y-130),(x+8,y-100),(x+16,y-40)],w=1.6)
        b+=hatch([(x,y),(x-16,y-40),(x-8,y-100),(x,y-130),(x+8,y-100),(x+16,y-40)],50,5,1,.6)
    # loose scribbles in the sky
    for i in range(8):
        x=R.uniform(40,1000); y=R.uniform(80,300); b+=jl(x,y,x+R.uniform(80,200),y+R.uniform(-30,30),w=1,op=.4,passes=1)
    return svg(W,H,b)

def columns():
    W,H=1080,1500; b=''
    # broken entablature
    top=260
    b+=poly([(60,top),(1000,top),(1030,top-60),(880,top-80),(820,top-150),(560,top-120),(420,top-170),(180,top-150),(80,top-70)],w=2.4)
    b+=poly([(40,top),(1040,top),(1040,top+70),(40,top+70)],w=2.2)
    for i in range(8): b+=poly([(90+i*120,top+70),(130+i*120,top+70),(130+i*120,top+150),(90+i*120,top+150)],w=1.6)
    b+=poly([(40,top+150),(1040,top+150),(1040,top+190),(40,top+190)],w=2)
    b+=hatch([(40,top+150),(1040,top+150),(1040,top+190),(40,top+190)],20,8,1.2,.6)
    b+=hatch([(80,top-70),(180,top-150),(420,top-170),(420,top),(60,top)],45,10,1,.35)
    # three Doric columns
    for cx in (150,470,790):
        y0=top+190; y1=1180; w=170
        b+=poly([(cx-14,y0),(cx+w+14,y0),(cx+w+4,y0+34),(cx-4,y0+34)],w=2)
        b+=jl(cx,y0+34,cx-6,y1,w=2.4)+jl(cx+w,y0+34,cx+w+6,y1,w=2.4)
        for f in range(1,8): b+=jl(cx+w*f/8,y0+40,cx+w*f/8+(f-4)*1.2,y1-4,w=1,op=.55,passes=1)
        for yy in range(y0+150,y1,150): b+=jl(cx-4,yy,cx+w+4,yy+R.uniform(-4,4),w=1,op=.5,passes=1)
        b+=hatch([(cx,y0+34),(cx+w*.32,y0+34),(cx+w*.32,y1),(cx-6,y1)],65,6,1.1,.55)
    # crack
    b+=poly([(330,520),(318,640),(338,760),(322,900)],w=1.6,closed=False)
    # steps / stones
    for i,y in enumerate((1180,1250,1320,1400)):
        b+=jl(20+i*20,y,1060-i*40,y,w=2)
        for k in range(7): x=R.uniform(40,1000); b+=jl(x,y,x+R.uniform(-6,6),y+70,w=1.4,op=.7)
    b+=hatch([(20,1180),(1060,1180),(1020,1250),(40,1250)],30,9,1,.35)
    # side shadow
    b+=hatch([(0,top+190),(150,top+190),(150,1180),(0,1180)],60,10,1,.35)
    return svg(W,H,b)

if __name__=='__main__':
    o=sys.argv[1]; os.makedirs(o,exist_ok=True)
    open(f'{o}/acropolis.svg','w').write(acropolis()); open(f'{o}/columns.svg','w').write(columns()); print('ok')
