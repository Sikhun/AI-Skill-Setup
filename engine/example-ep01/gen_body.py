"""Generate src/body.html for EP.01 (Vintage Sketch Studio, Socrates). Edit the SCENES list, then: python3 tools/gen_body.py && python3 tools/build.py"""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD = {"strip": (1000, 420), "mid": (720, 540), "small": (540, 460), "big": (880, 680), "tag": (500, 340), "sq": (440, 440)}

def card(id, kind, x, y, inner, rot=0, scale=1.0):
    w, h = CARD[kind]; w, h = int(w * scale), int(h * scale)
    imgs = "".join(f'<img class="b{i}" src="assets/props/{kind}/f{i}.png" alt="">' for i in range(3))
    return f'<div class="tc" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">{imgs}<div class="ct" style="inset:{int(60*scale)}px">{inner}</div></div>'

def host(n, side, poses):
    """poses: list of (name, mirror)"""
    pz = ""
    for name, m in poses:
        imgs = "".join(f'<img class="b{i}" src="assets/host/{name}/f{i}.png" alt="">' for i in range(3))
        pz += f'<div class="pz{" m" if m else ""}">{imgs}</div>'
    return f'<div class="host {side}" id="s{n:02d}-host"><div class="br">{pz}</div></div>'

def svg(id, name, x, y, w, h, extra=""):
    return f'<div class="svg" id="{id}" data-svg="{name}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}"></div>'

def w(n, text, word=None, cls=""):
    dw = f' data-w="{word}"' if word else ""
    return f'<span class="w {cls}" data-n="{n}"{dw}>{text}</span>'

BD = {"acro": '<img class="bd" src="assets/bd/acropolis.svg" style="left:0;top:{top}px;width:1080px;opacity:{op}">',
      "cols": '<img class="bd" src="assets/bd/columns.svg" style="left:0;top:{top}px;width:1080px;opacity:{op}">'}
def bd(kind, top, op): return BD[kind].format(top=top, op=op)

S = []  # (comment, bg, content)
# 01 hook
S.append(("01 HOOK โสเครตีสคือใคร", "pg", bd("acro", 560, .42) + f'''
  <div class="tz" style="top:250px;height:440px"><div class="lab w" data-t="0.05">LOGOS · I</div><div class="rule" id="s01-rule"><i></i><b></b><i></i></div>
    <div class="h xl">{w(1,"โสเครตีส")}</div><div class="h xl r">{w(1,"คือใคร?","คือใคร")}</div></div>
  {host(1,"C",[("02-questioning",False)])}'''))
# 02 why still talked about
S.append(("02 ผ่านมากว่าสองพันปี คนยังพูดถึงเขา", "pg", f'''
  <div class="tz" style="top:250px;height:400px"><div class="s">{w(2,"ทำไม")} {w(2,"ผ่านมากว่า")} {w(2,"สองพันปี","สองพันปี")}</div>
    <div class="h">{w(2,"คนยัง")}{w(2,"พูดถึงเขา?","พูดถึงเขา","r")}</div></div>
  {svg("s02-b1","bub",560,700,240,185)}{svg("s02-b2","bubq",800,820,220,170)}{svg("s02-b3","bub",640,960,190,146,"transform:scaleX(-1)")}{svg("s02-b4","bubq",520,1060,170,130)}
  {host(2,"L",[("01-thinking",False)])}'''))
# 03 who
S.append(("03 นักปรัชญาชาวกรีก จากเอเธนส์", "pg", bd("acro", 900, .3) + f'''
  <div class="tz" style="top:250px;height:380px"><div class="s">{w(3,"นักปรัชญาชาวกรีก")}</div><div class="h xl">{w(3,"จากกรุง")}{w(3,"เอเธนส์","เอเธนส์","r")}</div></div>
  {card("s03-id","mid",330,660,'<div class="lab" style="font-size:30px">PORTRAIT · I</div><div class="num" style="font-size:84px;color:#3A2A1E;letter-spacing:.06em">SOKRATES</div><div class="rule"><i style="width:120px"></i><b></b><i style="width:120px"></i></div><div class="se" style="font-size:40px">c. 470 – 399 BC</div>',3)}
  {host(3,"L",[("03-explaining",True)])}'''))
# 04 2,400 years ago
S.append(("04 2,400 ปีก่อน", "pg", f'''
  <div class="tz" style="top:250px;height:420px"><div class="s">{w(4,"มีชีวิตอยู่เมื่อประมาณ")}</div><div class="h xl num" style="font-family:Playfair,serif;font-weight:900;font-size:170px"><span class="w" data-n="4" data-w="2,400" id="s04-n">0</span></div><div class="s">{w(4,"ปีก่อน")}</div></div>
  {svg("s04-tl","timeline",110,760,860,140)}
  <div class="se" id="s04-l" style="position:absolute;left:96px;top:900px;font-size:38px;opacity:0">399 BC</div><div class="se" id="s04-r" style="position:absolute;left:840px;top:900px;font-size:38px;opacity:0">TODAY</div>
  {host(4,"R",[("05-surprised",True)])}'''))
# 05 talks in public, asks questions
S.append(("05 พูดคุยกับผู้คนในที่สาธารณะ / ตั้งคำถาม", "pg", bd("cols", 380, .26) + f'''
  <div class="tz" style="top:240px;height:420px">
    <div class="sw" id="s05-a"><div class="s">{w(5,"เขามักพูดคุยกับผู้คน")}</div><div class="h">{w(5,"ในที่สาธารณะ")}</div></div>
    <div class="sw" id="s05-b" style="opacity:0"><div class="h xl r">{w(5,"ตั้งคำถาม")}</div><div class="s">{w(5,"เกี่ยวกับเรื่องสำคัญในชีวิต")}</div></div></div>
  {svg("s05-b1","bub",600,700,250,192)}{svg("s05-b2","bub",820,860,200,154,"transform:scaleX(-1)")}{svg("s05-b3","bubq",560,930,230,177)}
  {svg("s05-q","qmark",700,660,230,326)}
  {host(5,"L",[("02-questioning",True)])}'''))
# 06 examples: goodness, justice
S.append(("06 เช่น ความดีคืออะไร ความยุติธรรมคืออะไร", "pg", f'''
  <div class="tz" style="top:240px;height:200px"><div class="lab" style="font-size:40px">{w(6,"เช่น")}</div></div>
  {card("s06-c1","strip",30,430,'<div class="tt" style="font-size:78px">ความดี<span style="color:#A8432A">คืออะไร?</span></div>',-2,0.9)}
  {card("s06-c2","strip",90,780,'<div class="tt" style="font-size:66px">ความยุติธรรม<span style="color:#A8432A">คืออะไร?</span></div>',1.5,0.95)}
  {svg("s06-ht","heart",800,410,150,135)}{svg("s06-sc","scales",780,1060,240,240)}
  {host(6,"L",[("01-thinking",False)])}'''))
# 07 how sure
S.append(("07 มั่นใจได้อย่างไร ว่าที่เชื่อถูกต้อง", "pg", f'''
  <div class="tz" style="top:250px;height:420px"><div class="s">{w(9,"และเรามั่นใจได้อย่างไร")}</div><div class="h">{w(9,"ว่าสิ่งที่เชื่อ")}</div><div class="h xl r">{w(9,"ถูกต้อง?","ถูกต้อง")}</div></div>
  {card("s07-c","sq",600,700,'<div class="lab" style="font-size:28px">VERUM ?</div>',4,0.9)}
  {svg("s07-ck","check",660,780,250,200)}{svg("s07-q","qmark",770,720,160,226)}
  {host(7,"L",[("04-skeptical",False)])}'''))
# 08 examine own thinking
S.append(("08 กลับมาตรวจสอบความคิดของตัวเอง", "pg", f'''
  <div class="tz" style="top:250px;height:420px"><div class="s">{w(10,"การสนทนาแบบนี้")} {w(10,"ทำให้ผู้คนต้องกลับมา")}</div><div class="h xl">{w(10,"ตรวจสอบ","ตรวจสอบ","r")}</div><div class="s">{w(10,"ความคิดของตัวเอง")}</div></div>
  {card("s08-c","mid",60,700,'<div class="tt" style="font-size:96px">ความคิด</div><div class="se" style="font-size:34px;margin-top:6px">fig. 1 — what I believe</div>',-3,0.95)}
  {svg("s08-mg","magni",420,700,300,300)}
  {host(8,"R",[("01-thinking",True)])}'''))
# 09 thought you knew -> can't explain
S.append(("09 ที่เคยคิดว่ารู้ กลับยังอธิบายไม่ได้", "pg", f'''
  <div class="tz" style="top:250px;height:420px">
    <div class="sw" id="s09-a"><div class="s">{w(11,"และบางครั้งก็พบว่า")}</div><div class="h">{w(12,"สิ่งที่เคยคิดว่า")}<span class="w" data-n="12" data-w="รู้">รู้</span></div></div>
    <div class="sw" id="s09-b" style="opacity:0"><div class="s">{w(12,"กลับยัง")}</div><div class="h xl r">{w(12,"อธิบายไม่ได้")}</div></div></div>
  {card("s09-c","small",470,700,'<div class="tt" style="font-size:88px">"รู้แล้ว"</div>',3)}
  {svg("s09-x","strike",500,820,480,96)}
  {host(9,"L",[("01-thinking",False),("05-surprised",False)])}'''))
# 10 known through others' writings
S.append(("10 รู้จักเขาผ่านงานเขียนของผู้อื่น", "pg", f'''
  <div class="tz" style="top:250px;height:420px"><div class="s">{w(13,"เรารู้จักเรื่องราวของเขาผ่าน")}</div><div class="h xl">{w(13,"งานเขียน")}</div><div class="h r">{w(13,"ของผู้อื่น")}</div></div>
  {svg("s10-sc","scroll",500,720,460,362)}
  {host(10,"L",[("03-explaining",True)])}'''))
# 11 Plato
S.append(("11 โดยเฉพาะเพลโต ได้รับอิทธิพลจากเขา", "pg", f'''
  <div class="tz" style="top:250px;height:420px">
    <div class="sw" id="s11-a"><div class="s">{w(14,"โดยเฉพาะ")}</div><div class="h xl r">{w(14,"เพลโต")}</div></div>
    <div class="sw" id="s11-b" style="opacity:0"><div class="s">{w(15,"ได้รับอิทธิพลจากเขา")}</div><div class="h xl">{w(15,"อย่างมาก")}</div></div></div>
  {card("s11-a1","tag",20,700,'<div class="num" style="font-size:58px;color:#3A2A1E">SOKRATES</div>',-4,0.9)}
  {svg("s11-ar","arrow",380,700,280,130)}
  {card("s11-a2","tag",560,760,'<div class="num" style="font-size:66px;color:#A8432A">PLATO</div><div class="tt" style="font-size:40px">เพลโต</div>',3,0.9)}
  {host(11,"R",[("03-explaining",False)])}'''))
# 12 age 70, sentenced to death
S.append(("12 อายุราว 70 ปี ถูกตัดสินประหารชีวิต", "pg dk", f'''
  <div class="tz" style="top:250px;height:420px">
    <div class="sw" id="s12-a"><div class="s">{w(16,"เมื่ออายุราว")}</div><div class="h xl"><span class="w num" data-n="16" data-w="70" style="font-family:Playfair,serif;font-weight:900;font-size:150px">70</span> {w(16,"ปี")}</div></div>
    <div class="sw" id="s12-b" style="opacity:0"><div class="s">{w(17,"โสเครตีสถูกตัดสิน")}</div><div class="h xl r">{w(17,"ประหารชีวิต")}</div></div></div>
  <div class="seal" id="s12-seal" style="left:690px;top:680px;width:250px;height:250px"><span>ประหาร</span></div>
  {host(12,"R",[("01-thinking",True),("05-surprised",True)])}'''))
# 13 charges
S.append(("13 ข้อหา: ทำให้เยาวชนเสื่อมเสีย / ไม่เคารพเทพเจ้า", "pg dk", f'''
  <div class="tz" style="top:240px;height:300px"><div class="h">{w(17,"ในข้อหา")}</div></div>
  {card("s13-c","big",160,520,'<div class="lab" style="font-size:30px;margin-bottom:18px">KATEGORIA · 399 BC</div><div class="tt" id="s13-i1" style="font-size:54px;opacity:0;text-align:left;width:100%;padding:0 30px 0 50px"><span class="num" style="color:#A8432A">I.</span> ทำให้เยาวชนเสื่อมเสีย</div><div class="tt" id="s13-i2" style="font-size:54px;opacity:0;text-align:left;width:100%;padding:0 30px 0 50px;margin-top:14px"><span class="num" style="color:#A8432A">II.</span> ไม่เคารพเทพเจ้าของนคร</div>',-1.5)}
  {host(13,"L",[("04-skeptical",False)])}'''))
# 14 hemlock
S.append(("14 เสียชีวิตด้วยการดื่มยาพิษ", "pg dk", bd("cols", 600, .16) + f'''
  <div class="tz" style="top:250px;height:420px"><div class="s">{w(18,"เขาเสียชีวิตด้วยการ")}</div><div class="h xl r">{w(18,"ดื่มยาพิษ")}</div><div class="s">{w(18,"ตามคำตัดสิน")}</div></div>
  {svg("s14-cup","cup",240,820,600,533)}'''))
# 15 his life ended
S.append(("15 ชีวิตของเขาจบลง", "pg dk", f'''
  <div class="tz" style="top:560px;height:500px"><div class="s">{w(19,"ชีวิตของเขา")}</div><div class="h xl">{w(19,"จบลง")}</div></div>
  {svg("s15-lr","laurel",330,1060,420,330)}'''))
# 16 legacy
S.append(("16 แต่วิธีตั้งคำถามยังมีอิทธิพลถึงทุกวันนี้", "pg", bd("acro", 640, .32) + f'''
  <div class="tz" style="top:240px;height:440px">
    <div class="sw" id="s16-a"><div class="s">{w(20,"แต่")}</div><div class="h xl r">{w(20,"วิธีตั้งคำถาม")}</div><div class="s">{w(20,"ของเขา")}</div></div>
    <div class="sw" id="s16-b" style="opacity:0"><div class="s">{w(20,"ยังคงมีอิทธิพลต่อปรัชญา")}</div><div class="h xl">{w(20,"จนถึงทุกวันนี้","จนถึงทุกวันนี้")}</div></div></div>
  {svg("s16-q","qmark",720,700,230,326)}
  {svg("s16-tl","timeline",110,1010,860,140)}
  <div class="se" id="s16-l" style="position:absolute;left:96px;top:1150px;font-size:38px;opacity:0">399 BC</div><div class="se" id="s16-r" style="position:absolute;left:840px;top:1150px;font-size:38px;opacity:0">TODAY</div>
  {host(16,"L",[("03-explaining",True)])}'''))
# 17 CTA
S.append(("17 CTA ไลก์และติดตาม", "pg", f'''
  <div class="tz" style="top:250px;height:420px">
    <div class="sw" id="s17-a"><div class="s">{w(21,"ถ้าชอบ")}</div><div class="h xl">{w(21,"แนวนี้")}</div></div>
    <div class="sw" id="s17-b" style="opacity:0"><div class="s">{w(21,"อย่าลืมกด")}</div><div class="h xl r">{w(21,"ไลก์")}</div><div class="h">{w(21,"และติดตาม")}</div></div>
    <div class="sw" id="s17-c" style="opacity:0"><div class="s">{w(22,"แล้วเราจะได้")}</div><div class="h xl">{w(22,"เจอกันอีก")}</div><div class="lab" style="margin-top:10px">{w(22,"ครับ")}</div></div></div>
  {card("s17-lk","sq",560,690,'<div style="width:190px;height:170px" class="svg" data-svg="heart" id="s17-ht"></div>',-4,0.85)}
  {card("s17-fl","sq",760,860,'<div style="width:180px;height:180px" class="svg" data-svg="plus" id="s17-pl"></div>',5,0.75)}
  {host(17,"L",[("02-questioning",True)])}'''))

out = ['  <body>\n    <!-- EP.01: Vintage Sketch Studio "โสเครตีสคือใคร". Generated by tools/gen_body.py -->',
       '    <svg width="0" height="0" style="position:absolute"><defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="2"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>'
       '<filter id="chalkf"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="5" result="t"/><feColorMatrix in="t" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1.6 1.25" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in" result="c"/><feDisplacementMap in="c" in2="t" scale="4"/></filter></defs></svg>',
       '    <div id="root" data-f="0" data-composition-id="main" data-start="0" data-duration="@DUR" data-width="1080" data-height="1920">',
       '      <div id="ground" class="clip full" style="background:#EFE4CC" data-start="0" data-duration="@DUR" data-track-index="0"></div>']
for i, (c, bg, content) in enumerate(S, 1):
    out.append(f'\n      <!-- {c} -->\n      <section id="s{i:02d}" class="clip scene" data-start="@S{i:02d}" data-duration="@D{i:02d}" data-track-index="@K{i:02d}"><div class="inner"><div class="{bg}"></div><svg class="scrib" data-seed="{i*13+7}"></svg><div class="cam">{content}\n      </div></div></section>')
out.append('''
      <!-- global overlays -->
      <div id="fiber" class="clip full" data-layout-allow-occlusion="" data-start="0" data-duration="@DUR" data-track-index="4"></div>
      <div id="blot" class="clip full" data-layout-allow-occlusion="" data-start="0" data-duration="@DUR" data-track-index="5"></div>
      <div id="grain" class="clip full" data-layout-allow-occlusion="" data-start="0" data-duration="@DUR" data-track-index="6"><i></i></div>
      <div id="burnedge" class="clip full" data-layout-allow-occlusion="" data-start="0" data-duration="@DUR" data-track-index="7"></div>
      <div id="sepia" class="clip" data-layout-allow-occlusion="" data-start="0" data-duration="@DUR" data-track-index="8"></div>
      <div id="flash" class="clip" data-layout-allow-occlusion="" data-start="0" data-duration="@DUR" data-track-index="9"></div>
      <audio id="soundtrack" src="assets/audio/derived/soundtrack.wav" data-start="0" data-duration="@DUR" data-track-index="10" data-volume="1"></audio>
    </div>''')
open(os.path.join(R, "src", "body.html"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(S), "scenes")
