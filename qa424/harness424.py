# -*- coding: utf-8 -*-
"""v424 UI26 實裝量度 harness：serve work424 本地、Playwright 實駕。
輸出 -> qa424/out/（shots + json）。播種只經 S/localStorage starVolunteer_map_v19w。
用法: /home/hatch/pwenv49/bin/python qa424/harness424.py [nb|gigs|n1|sec|map|all] [tag]
tag 用嚟分 before/after（預設 after）。"""
import sys, os, json, socket, subprocess, time, urllib.request, hashlib, io
from PIL import Image

sys.path.insert(0, '/home/hatch/workspace/fullarc')
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/hatch/pw-browsers')
from playwright.sync_api import sync_playwright
import driver as drv

ROOT = '/home/hatch/workspace/linji-work424'
OUT = ROOT + '/qa424/out'
SHOTS = OUT + '/shots'
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
TAG = sys.argv[2] if len(sys.argv) > 2 else 'after'

def free_port():
    for cand in range(9411, 9430):
        s = socket.socket()
        try: s.bind(("127.0.0.1", cand)); return cand
        except OSError: continue
        finally: s.close()
    raise RuntimeError("no free port")
PORT = free_port()
srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(30):
    time.sleep(0.5)
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5).read(); break
    except Exception: continue
URL = f"http://127.0.0.1:{PORT}/index.html"
print("serve", URL, "tag", TAG, flush=True)

R = {}
def rec(k, v):
    R[k] = v
    print("REC", k, json.dumps(v, ensure_ascii=False)[:600] if not isinstance(v, str) else v[:600], flush=True)

def ev(pg, js, arg=None):
    try: return pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)
    except Exception as e: print("EVFAIL", str(e)[:200], flush=True); return None

def shot(pg, name):
    p = f"{SHOTS}/{TAG}_{name}.png"; pg.screenshot(path=p)
    md = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    print("SHOT", TAG, name, md, flush=True); return p

def click_any(pg, pats):
    return ev(pg, """(pats) => {
      const bs=[...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null&&!b.disabled);
      for(const pat of pats){ const t=bs.find(b=>new RegExp(pat).test(b.textContent||'')); if(t){ t.click(); return (t.textContent||'').trim().slice(0,30); } }
      return null; }""", pats)

def click_modal(pg, pats):
    return ev(pg, """(pats) => {
      const m=document.getElementById('modal'); if(!m) return null;
      const bs=[...m.querySelectorAll('button')].filter(b=>b.offsetParent!==null&&!b.disabled);
      for(const pat of pats){ const t=bs.find(b=>new RegExp(pat).test(b.textContent||'')); if(t){ t.click(); return (t.textContent||'').trim().slice(0,30); } }
      return null; }""", pats)

def play_out_story(pg):
    for _ in range(120):
        ov = ev(pg, """() => { const o=document.getElementById('enc79-overlay'); if(!o) return null;
          const ch=o.querySelector('.e79-choice'); if(ch){ ch.click(); return 'choice'; }
          const nb=o.querySelector('.e79-btn'); if(nb){ nb.click(); return 'next'; }
          const sk=o.querySelector('.e79-skip'); if(sk){ sk.click(); return 'skip'; }
          return 'stuck'; }""")
        if ov:
            pg.wait_for_timeout(700); continue
        st = ev(pg, """() => { const m=document.getElementById('mask');
          return JSON.stringify({on: !!(m&&m.classList.contains('on')),
            h3:(document.querySelector('#modal h3')||{}).textContent||null,
            sess: !!(window.StoryPlay && StoryPlay.session),
            reconfirm: !!document.querySelector('.reconfirm236'),
            choice: !!(document.querySelector('.sp-choice')&&document.querySelector('.sp-choice').offsetParent!==null)}); }""")
        try: st = json.loads(st)
        except Exception: break
        if not st.get('on') and not st.get('sess'): return True
        h3 = st.get('h3') or ''
        if '巧遇' in h3:
            if click_modal(pg, ['行開']): pg.wait_for_timeout(700); continue
            break
        if st.get('reconfirm') or h3 == '確認選擇':
            if click_modal(pg, ['確定']): pg.wait_for_timeout(700); continue
            break
        if st.get('choice'):
            ev(pg, "() => { const c=document.querySelector('.sp-choice'); if(c) c.click(); }")
            pg.wait_for_timeout(700); continue
        if click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '完成', '返回地圖', '離開', '跳過', '關閉', '確定', '我知道了']):
            pg.wait_for_timeout(600); continue
        break
    pg.wait_for_timeout(700)
    return not ev(pg, "() => document.getElementById('mask').classList.contains('on')")

def new_game(pg):
    pg.goto(URL); pg.wait_for_timeout(2500)
    for _ in range(12):
        pg.click('#btn-new'); pg.wait_for_timeout(1200)
        st = ev(pg, "() => JSON.stringify({s: !!(typeof S!=='undefined'&&S), mask: document.getElementById('mask').classList.contains('on'), view:(document.querySelector('.view.on')||{}).id||''})")
        try: st = json.loads(st)
        except Exception: st = {}
        if st.get('s') or st.get('mask') or st.get('view') != 'v-start': break
    if ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button, #slot-list button')].find(x=>x.offsetParent!==null&&/槽 1/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }"):
        pg.wait_for_timeout(1200)
        click_modal(pg, ['覆蓋開新局', '確定']); pg.wait_for_timeout(1000)
    drv.skip_tutorial(pg)
    drv.click_text_in_modal(pg, r'開始寫手帳')
    pg.wait_for_timeout(1000)
    pg.wait_for_function("() => typeof S !== 'undefined' && !!S", timeout=20000)

STORY29 = ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17",
           "R_hiu_meet","R_hiu_crisis","R_choi_meet","R_choi_crisis","R_lan_meet","R_lan_crisis",
           "R_xu_meet","R_xu_crisis","R_yip_meet","R_yip_crisis","R_so_meet","R_so_crisis"]

def seed_main(pg, day=1):
    return ev(pg, """(a) => {
  S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80;
  S.fame=120; S.money=9000; S.stress=20; S.dayIndex=a;
  S.weekPlan=['scout_all','street','scout_all','scout_all','scout_all','scout_all','scout_all'];
  S.shoots=[]; S.booked=[]; S.pendingAud=[]; S.aud91Log=[]; S.grant229Queue=[];
  if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
  %s.forEach(id=>{ S.story.done[id]=true; });
  S.story.flags=Object.assign({}, S.story.flags, {route_tv:true});
  S.flags=Object.assign({}, S.flags, {route_tv:true});
  S.story.routes={route_tv:true};
  S.travel114={day:S.dayIndex, used:0};
  try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
  return S.dayIndex; }""" % json.dumps(STORY29), day)

def rich_seed(pg, day=520):
    return ev(pg, """(day) => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = day;
      S.shoots=[]; S.booked=[]; S.pendingAud=[]; S.aud91Log=[]; S.grant229Queue=[];
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19"].forEach(id=>{ S.story.done[id]=true; });
      S.story.flags=Object.assign({}, S.story.flags, {route_tv:true});
      S.flags=Object.assign({}, S.flags, {route_tv:true}); S.story.routes={route_tv:true};
      S.travel114={day:day, used:0};
      try{ if(typeof syncGigsForCalendarYear==='function') syncGigsForCalendarYear(true); }catch(e){}
      try{ if(typeof renderAll==='function') renderAll(); }catch(e){}
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return 'rich'; }""", day)

def open_loc_sheet(pg, loc):
    ev(pg, "() => { if(typeof S!=='undefined' && S){ S.travel114={day:S.dayIndex, used:0}; try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} } return 'ok'; }")
    for attempt in range(4):
        click_any(pg, ['返回地圖']); pg.wait_for_timeout(1000)
        ev(pg, """(loc) => { const p=document.querySelector('.pin[data-loc="'+loc+'"]'); if(p) p.click(); return !!p; }""", loc)
        pg.wait_for_timeout(1500)
        play_out_story(pg)
        if ev(pg, "() => { const sh=document.getElementById('loc-sheet'); return !!(sh && sh.offsetParent!==null); }"):
            return True
    return False

def open_notebook(pg):
    click_any(pg, ['返回地圖']); pg.wait_for_timeout(900)
    for i in range(14):
        if ev(pg, "()=>(document.querySelector('.view.on')||{}).id") == 'v-map' and not ev(pg, "()=>document.getElementById('mask').classList.contains('on')"):
            break
        c = click_any(pg, ['下一句', '繼續', '確定', '收下這份剪報', '收下剪報', '跳過', '關閉', '我知道了'])
        if not c and ev(pg, "()=>document.getElementById('mask').classList.contains('on')"):
            pg.mouse.click(195, 120)
        pg.wait_for_timeout(700)
    pg.wait_for_timeout(1500)
    r = click_any(pg, ['手帳', '行程'])
    pg.wait_for_timeout(1200)
    if ev(pg, "()=>(document.querySelector('.view.on')||{}).id") != 'v-home':
        ev(pg, "() => { const p=document.querySelector('.pin[data-loc=\"home\"]'); if(p) p.click(); return !!p; }")
        pg.wait_for_timeout(1500)
    play_out_story(pg); pg.wait_for_timeout(800)

# ---------- 量度 JS ----------
NB_GEO = """() => JSON.stringify((()=>{
  const vh=innerHeight, vw=innerWidth;
  const Rr=el=>{ if(!el) return null; const b=el.getBoundingClientRect(); return {top:+b.top.toFixed(1),bottom:+b.bottom.toFixed(1),left:+b.left.toFixed(1),right:+b.right.toFixed(1),h:+b.height.toFixed(1),w:+b.width.toFixed(1)}; };
  const vis=r=>r?(r.bottom<=vh+1&&r.top>=-1&&r.left>=-1&&r.right<=vw+1):null;
  const nb=document.getElementById('notebook');
  const conf=document.getElementById('btn-confirm-plan');
  const days=[...document.querySelectorAll('.day-row')].filter(x=>x.offsetParent!==null).map(d=>{ const r=Rr(d); return {t:(d.textContent||'').trim().replace(/\\s+/g,' ').slice(0,20), top:r.top, bottom:r.bottom, h:r.h, w:r.w, fully:vis(r)}; });
  const cats=[...document.querySelectorAll('.cat-tab')].filter(b=>b.offsetParent!==null).map(b=>{ const r=Rr(b); return {t:(b.textContent||'').trim(), top:r.top, bottom:r.bottom, h:r.h, w:r.w, fully:vis(r)}; });
  const acts=[...document.querySelectorAll('.act-item')].filter(b=>b.offsetParent!==null).map(b=>{ const r=Rr(b); return {t:(b.textContent||'').trim().replace(/\\s+/g,' ').slice(0,24), top:r.top, bottom:r.bottom, h:r.h, fully:vis(r), disabled:!!b.disabled}; });
  const title=document.getElementById('nb-right-title');
  const cost=document.getElementById('nb-cost400');
  const range=document.getElementById('nb-range');
  const nbR=Rr(nb);
  const actInPaper = acts.length? (acts[0].bottom <= nbR.bottom+1 && acts[0].top >= nbR.top-1) : null;
  const catInPaper = cats.length? (cats[0].bottom <= nbR.bottom+1) : null;
  const daysInPaper = days.length? days.every(d=>d.bottom<=nbR.bottom+1&&d.top>=nbR.top-1) : null;
  return {vh, vw, nbScroll: nb?{scrollTop:Math.round(nb.scrollTop), scrollH:nb.scrollHeight, clientH:nb.clientHeight}:null,
    nbRect: nbR, confirm: Rr(conf), confirmFully: vis(Rr(conf)), confirmText: conf?(conf.textContent||'').trim():null,
    days, nDays:days.length, daysInPaper, cats, catInPaper, acts:acts.slice(0,6), nActs:acts.length, actInPaper,
    title: title?(title.textContent||'').trim():null, titleRect: Rr(title),
    cost: cost&&!cost.hidden?(cost.textContent||'').trim():null, costRect: Rr(cost),
    range: range?(range.textContent||'').trim():null,
    selDay: (()=>{ const s=document.querySelector('.day-row.on'); return s?(s.textContent||'').trim().replace(/\\s+/g,' ').slice(0,24):null; })(),
    draft: (typeof planDraft!=='undefined')?planDraft.slice():null, planSelDay: (typeof planSelDay!=='undefined')?planSelDay:null,
    activeTag: document.activeElement? (document.activeElement.className||document.activeElement.tagName):null};
})())"""

N1_MEASURE = """() => JSON.stringify((()=>{
  const Rr=el=>{ if(!el) return null; const b=el.getBoundingClientRect(); return {top:+b.top.toFixed(1),bottom:+b.bottom.toFixed(1),left:+b.left.toFixed(1),right:+b.right.toFixed(1),h:+b.height.toFixed(1),w:+b.width.toFixed(1)}; };
  const sp=document.querySelector('.sp-speaker');
  const line=document.querySelector('.sp-line');
  let nameTextW=null, plate=null, lineRect=null;
  if(sp){ plate=Rr(sp);
    try{ const rg=document.createRange(); rg.selectNodeContents(sp); const rr=rg.getBoundingClientRect(); nameTextW=+rr.width.toFixed(1); }catch(e){}
  }
  if(line) lineRect=Rr(line);
  const imgs=[...document.querySelectorAll('img.dlg106-char')].map(im=>{ const cs=getComputedStyle(im); return {src:im.getAttribute('src'), r:Rr(im), filter:cs.filter, brightVar: im.style.getPropertyValue('--speaker-brightness')||null, natW:im.naturalWidth, natH:im.naturalHeight, flip: im.className.includes('dlg106-flip')}; });
  const stage=document.querySelector('.sp-stage');
  const bg=document.querySelector('.sp-bg-layer');
  const fg=document.querySelector('.sp-fg424');
  const grade=document.querySelector('.sp-grade424');
  const plateEl=document.querySelector('.dlg106-plate');
  const csPlate=plateEl?getComputedStyle(plateEl):null;
  const counter=(document.querySelector('.sp-prog362')||{}).textContent||null;
  return {vw:innerWidth, vh:innerHeight, counter: counter?counter.trim():null,
    dlgText: line?(line.textContent||'').trim():null,
    speakerText: sp?(sp.textContent||'').trim():null,
    nameTextW, plate, lineRect,
    plateMinusText: (plate&&nameTextW!=null)? +(plate.w-nameTextW).toFixed(1):null,
    leftEdgeDiff: (plate&&lineRect)? +(plate.left-lineRect.left).toFixed(1):null,
    imgs, stageRect: Rr(stage),
    bgImg: bg?getComputedStyle(bg).backgroundImage:null,
    fg: fg?{rect:Rr(fg), clip:getComputedStyle(fg).clipPath, bgSize:getComputedStyle(fg).backgroundSize, bgPos:getComputedStyle(fg).backgroundPosition, bgImg:getComputedStyle(fg).backgroundImage}:null,
    grade: grade?{bg:getComputedStyle(grade).backgroundImage.slice(0,120)}:null,
    plateShadow: csPlate?csPlate.boxShadow:null};
})())"""

CONTRAST_JS = """(scope) => JSON.stringify((()=>{
  function parseRGB(s){ const m=(s||'').match(/rgba?\\(([^)]+)\\)/); if(!m) return null; const p=m[1].split(',').map(x=>parseFloat(x)); return {r:p[0], g:p[1], b:p[2], a:(p.length>3?p[3]:1)}; }
  function lum(c){ const f=v=>{ v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); }
  function ratio(a,b){ const l1=lum(a), l2=lum(b); if(l1==null||l2==null) return null; const hi=Math.max(l1,l2), lo=Math.min(l1,l2); return +((hi+0.05)/(lo+0.05)).toFixed(2); }
  function blend(fg,bg){ const a=fg.a; return {r:fg.r*a+bg.r*(1-a), g:fg.g*a+bg.g*(1-a), b:fg.b*a+bg.b*(1-a), a:1}; }
  function effBg(el){
    // 由下而上合成：收集祖先背景色（半透明逐層合成），圖片底標記
    let layers=[], n=el, img=false;
    while(n && n!==document.documentElement){ const cs=getComputedStyle(n);
      if(cs.backgroundImage && cs.backgroundImage!=='none') img=true; /* 圖層喺不透明底色之前先要像素量度 */
      const bg=parseRGB(cs.backgroundColor); if(bg && bg.a>0){ layers.push(bg); if(bg.a>0.98) break; }
      n=n.parentElement; }
    let base={r:246,g:239,b:220,a:1};
    for(let i=layers.length-1;i>=0;i--){ base=blend(layers[i], base); }
    return {rgb:base, img};
  }
  function groupOpacity(el){ let o=1, n=el; while(n && n!==document.documentElement){ o*=parseFloat(getComputedStyle(n).opacity||'1'); n=n.parentElement; } return o; }
  const root = scope ? document.querySelector(scope) : document.body;
  if(!root) return JSON.stringify({scope, error:'no-root'});
  const out=[];
  root.querySelectorAll('*').forEach(el=>{
    if(el.children.length>0) return;
    if(el.closest('[aria-hidden="true"]')) return; /* 裝飾字形唔入語義對比 */
    const t=(el.textContent||'').trim(); if(!t) return;
    const cs=getComputedStyle(el);
    if(cs.visibility==='hidden'||cs.display==='none') return;
    const r=el.getBoundingClientRect(); if(r.width<=0||r.height<=0) return;
    if(r.bottom>innerHeight+1||r.top<-1||r.right>innerWidth+1||r.left<-1) return; /* 折位半截／被遮文字唔入量度 */
    // hit-test：中心點要打中自己或子孫先算可見
    let hit=false;
    for(const fx of [0.5,0.3,0.7]){ const px=Math.min(innerWidth-1,Math.max(0,r.x+r.width*fx)), py=Math.min(innerHeight-1,Math.max(0,r.y+r.height*0.5)); const top=document.elementFromPoint(px,py); if(top&&(top===el||el.contains(top)||top.contains(el))){hit=true;break;} }
    if(!hit) return;
    const fg0=parseRGB(cs.color); if(!fg0) return;
    const bg=effBg(el);
    const go=groupOpacity(el);
    const fg=blend({r:fg0.r,g:fg0.g,b:fg0.b,a:fg0.a*go}, bg.rgb);
    const fs=parseFloat(cs.fontSize)||0;
    out.push({text:t.slice(0,40), cls:(el.className||'').toString().slice(0,50), color:cs.color, fontSize:+fs.toFixed(1), fontWeight:cs.fontWeight,
      bgImg:bg.img, ratio: ratio(fg,bg.rgb), fgRaw:{r:fg0.r,g:fg0.g,b:fg0.b,a:fg0.a}, go:+go.toFixed(3),
      rect:{x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)},
      disabled: !!el.disabled || !!el.closest('button:disabled')});
  });
  return JSON.stringify({scope, n:out.length, items:out});
})())"""

def _lum(rgb):
    def f(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2])

def _ratio(fg, bg):
    l1, l2 = _lum(fg), _lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)

def contrast(pg, scope, label):
    c = ev(pg, CONTRAST_JS, scope)
    try:
        j = json.loads(c)
        if isinstance(j, str): j = json.loads(j)
    except Exception as e:
        print("CONTRASTFAIL", label, str(e)[:150], flush=True); return None
    items = j.get('items') or []
    # 圖片底：用截圖像素量文字外圈背景（最差一成亮度），唔用祖先底色估算
    img_items = [i for i in items if i.get('bgImg') and i.get('rect')]
    if img_items:
        try:
            im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
            vp = pg.viewport_size or {'width': im.width // 2, 'height': im.height // 2}
            sx, sy = im.width / float(vp['width']), im.height / float(vp['height'])
            for i in img_items:
                r = i['rect']
                fg0 = i.get('fgRaw') or {'r': 0, 'g': 0, 'b': 0, 'a': 1}
                fgc = (fg0['r'], fg0['g'], fg0['b'])
                x0 = max(0, int((r['x'] - 1) * sx)); x1 = min(im.width - 1, int((r['x'] + r['w'] + 1) * sx))
                y0 = max(0, int((r['y'] - 1) * sy)); y1 = min(im.height - 1, int((r['y'] + r['h'] + 1) * sy))
                def _dist(px):
                    return ((px[0] - fgc[0]) ** 2 + (px[1] - fgc[1]) ** 2 + (px[2] - fgc[2]) ** 2) ** 0.5
                fgmask = set()
                for yy in range(y0, y1 + 1):
                    for xx in range(x0, x1 + 1):
                        if _dist(im.getpixel((xx, yy))) <= 70:
                            fgmask.add((xx, yy))
                pts = []
                for yy in range(y0, y1 + 1):
                    for xx in range(x0, x1 + 1):
                        if (xx, yy) in fgmask:
                            continue
                        near = any((xx + dx, yy + dy) in fgmask for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2))
                        if near:
                            pts.append(im.getpixel((xx, yy)))
                if len(pts) < 8:
                    pts = [im.getpixel((xx, yy)) for yy in range(y0, y1 + 1, 2) for xx in range(x0, x1 + 1, 2) if (xx, yy) not in fgmask]
                if not pts:
                    continue
                pts.sort(key=_lum)
                dark_text = _lum(fgc) < 0.35
                bg = pts[int(0.5 * (len(pts) - 1))]  # 鄰近背景中位（紋理／邊框離群像素唔代表文字底）
                a = float(fg0.get('a', 1)) * float(i.get('go', 1))
                fg = tuple(fg0[k] * a + bg[n] * (1 - a) for n, k in enumerate(('r', 'g', 'b')))
                i['ratioCss'] = i.get('ratio')
                i['ratio'] = _ratio(fg, bg)
                i['bgSample'] = list(bg)
        except Exception as e:
            print("CONTRASTIMGFAIL", label, str(e)[:150], flush=True)
    fails = [i for i in items if i.get('ratio') is not None and i['ratio'] < 4.5 and not i.get('disabled')]
    small = [i for i in items if i.get('fontSize') and i['fontSize'] < 12]
    under14 = [{'text': i['text'], 'cls': i['cls'], 'fontSize': i['fontSize'], 'ratio': i.get('ratio')} for i in items if i.get('fontSize') and i['fontSize'] < 14]
    print("CONTRAST", label, 'n=', len(items), 'fail<4.5:', len(fails), 'small<12:', len(small), 'under14:', len(under14),
          [(f['text'][:14], f['ratio'], f['fontSize']) for f in fails[:10]], flush=True)
    rec('contrast_' + label, {'n': len(items), 'fails': fails[:40], 'small': small[:40], 'under14': under14[:80]})
    return j

TOUCH_JS = """() => JSON.stringify((()=>{
  const out=[];
  document.querySelectorAll('button, a[href], summary, [role=button]').forEach(el=>{
    if(el.disabled) return;
    if(el.offsetParent===null && getComputedStyle(el).position!=='fixed') return;
    const r=el.getBoundingClientRect(); if(r.width<=0||r.height<=0) return;
    if(r.bottom<0||r.top>innerHeight) return;
    if(r.width<44||r.height<44) out.push({t:(el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,24), cls:(el.className||'').toString().slice(0,40), w:+r.width.toFixed(1), h:+r.height.toFixed(1)});
  });
  return out;
})())"""

# ---------- 焦點流程 ----------
def focus_nb(pg):
    for (vw, vh, tag) in [(430, 707, '430x707'), (390, 844, '390x844'), (430, 932, '430x932')]:
        pg.set_viewport_size({'width': vw, 'height': vh})
        new_game(pg); pg.wait_for_timeout(1000)
        shot(pg, f'nb_{tag}_top')
        rec(f'nb_{tag}_top', json.loads(ev(pg, NB_GEO)))
        contrast(pg, '#home-pane-plan', f'nb_{tag}')
        rec(f'touch_nb_{tag}', json.loads(ev(pg, TOUCH_JS)))
        # 撳週二改活動（休息->街頭表演 之類），再撳週一揀活動：防誤改流程
        ev(pg, "() => { const r=[...document.querySelectorAll('.day-row')].find(x=>/週二/.test(x.textContent||'')); if(r) r.click(); return !!r; }")
        pg.wait_for_timeout(900)
        g1 = json.loads(ev(pg, NB_GEO)); rec(f'nb_{tag}_click_tue', g1)
        shot(pg, f'nb_{tag}_click_tue')
        ev(pg, "() => { const b=[...document.querySelectorAll('.cat-tab')].find(x=>/表演/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(800)
        picked = ev(pg, "() => { const items=[...document.querySelectorAll('.act-item')].filter(x=>x.offsetParent!==null&&!x.disabled); const it=items.find(x=>/街頭表演/.test(x.textContent||''))||items[0]; if(it){ const t=(it.textContent||'').trim().slice(0,24); const r=it.getBoundingClientRect(); it.click(); return JSON.stringify({t, top:+r.top.toFixed(1)}); } return null; }")
        pg.wait_for_timeout(900)
        g2 = json.loads(ev(pg, NB_GEO)); g2['picked'] = picked; rec(f'nb_{tag}_pick_tue', g2)
        shot(pg, f'nb_{tag}_pick_tue')
        # 轉週一再揀活動
        ev(pg, "() => { const r=[...document.querySelectorAll('.day-row')].find(x=>/週一/.test(x.textContent||'')); if(r) r.click(); return !!r; }")
        pg.wait_for_timeout(900)
        g3 = json.loads(ev(pg, NB_GEO)); rec(f'nb_{tag}_click_mon', g3)
        shot(pg, f'nb_{tag}_click_mon')
        ev(pg, "() => { const c=[...document.querySelectorAll('.cat-tab')].find(x=>/表演/.test(x.textContent||'')); if(c) c.click(); return !!c; }")
        picked2 = ev(pg, "() => { const items=[...document.querySelectorAll('.act-item')].filter(x=>x.offsetParent!==null&&!x.disabled); const it=items.find(x=>/咖啡店/.test(x.textContent||''))||items[0]; if(it){ const t=(it.textContent||'').trim().slice(0,24); const r=it.getBoundingClientRect(); it.click(); return JSON.stringify({t, top:+r.top.toFixed(1)}); } return null; }")
        pg.wait_for_timeout(900)
        g4 = json.loads(ev(pg, NB_GEO)); g4['picked'] = picked2; rec(f'nb_{tag}_pick_mon', g4)
        shot(pg, f'nb_{tag}_pick_mon')
    pg.set_viewport_size({'width': 390, 'height': 844})

def focus_gigs(pg):
    pg.set_viewport_size({'width': 390, 'height': 844})
    new_game(pg); seed_main(pg, 1); pg.wait_for_timeout(800)
    boards = [('film_lion', 'film'), ('tvb_longmen', 'tv'), ('ad_central', 'ad'), ('rec_hk', 'rec')]
    for loc, tag in boards:
        if not open_loc_sheet(pg, loc):
            rec(f'board_{tag}', 'sheet-fail'); continue
        r = ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/通告欄/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1400)
        shot(pg, f'board_{tag}')
        info = ev(pg, """() => JSON.stringify((()=>{
          const cards=[...document.querySelectorAll('.gig-teaser')];
          const Rr=el=>{ const b=el.getBoundingClientRect(); return {top:+b.top.toFixed(1),bottom:+b.bottom.toFixed(1),h:+b.height.toFixed(1),w:+b.width.toFixed(1)}; };
          const vis = cards.filter(c=>{ const r=c.getBoundingClientRect(); return r.bottom>0&&r.top<innerHeight; });
          const first = cards[0]? {cls:cards[0].className, text:(cards[0].innerText||'').slice(0,400), r:Rr(cards[0])}:null;
          const locked = cards.find(c=>c.dataset.boardState==='locked');
          const head = document.querySelector('.board-head392');
          const lead = document.querySelector('.board-lead');
          const list = document.querySelector('.gig-board-list');
          const listR = list?Rr(list):null;
          const comparable = cards.filter(c=>{ const t=c.innerText||''; const r=c.getBoundingClientRect(); return /片酬/.test(t)&&/要求/.test(t)&&/檔期/.test(t)&&listR&&r.bottom<=listR.bottom+1&&r.top>=listR.top-1; }).length;
          return {nCards:cards.length, nVis:vis.length, comparable, first,
            lockedText: locked?(locked.innerText||'').slice(0,300):null,
            headText: head?(head.innerText||'').slice(0,200):null, headR: head?Rr(head):null,
            leadText: lead?(lead.innerText||'').slice(0,200):null, leadR: lead?Rr(lead):null,
            cardTexts: cards.slice(0,4).map(c=>(c.innerText||'').replace(/\\n+/g,' | ').slice(0,260))};
        })())""")
        rec(f'board_{tag}', json.loads(info) if info else None)
        contrast(pg, '#modal-inner', f'board_{tag}')
        rec(f'touch_board_{tag}', json.loads(ev(pg, TOUCH_JS)))
        # 開第一張卡詳情
        ev(pg, "() => { const c=document.querySelector('.gig-teaser'); if(c) c.click(); return !!c; }")
        pg.wait_for_timeout(1400)
        shot(pg, f'gig_{tag}_detail')
        det = ev(pg, """() => JSON.stringify((()=>{
          const root=document.getElementById('modal-inner');
          const txt=root?(root.innerText||''):'' ;
          const secs=[...root.querySelectorAll('.cn-lab')].map(e=>(e.textContent||'').trim());
          const rows=[...root.querySelectorAll('.cn-sum-row')].map(e=>(e.innerText||'').replace(/\\n/g,' ').trim().slice(0,60));
          return {secs, rows, txt: txt.slice(0,1600)};
        })())""")
        rec(f'gig_{tag}_detail', json.loads(det) if det else None)
        contrast(pg, '#modal-inner', f'gig_{tag}_detail')
        ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button')].find(x=>/返回|離開|關閉/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1000)
        play_out_story(pg)
    # 鎖定卡：低數值開板
    new_game(pg); pg.wait_for_timeout(800)
    if open_loc_sheet(pg, 'film_lion'):
        ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/通告欄/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1400)
        ev(pg, "() => { const d=document.querySelector('.gig-locked108'); if(d) d.open=true; return !!d; }")
        pg.wait_for_timeout(800)
        shot(pg, 'board_locked')
        info = ev(pg, """() => JSON.stringify((()=>{
          const cards=[...document.querySelectorAll('.gig-teaser')];
          const locked=cards.filter(c=>c.dataset.boardState==='locked');
          return {n:cards.length, nLocked:locked.length, lockedTexts: locked.slice(0,3).map(c=>(c.innerText||'').replace(/\\n+/g,' | ').slice(0,300))};
        })())""")
        rec('board_locked', json.loads(info) if info else None)
        contrast(pg, '#modal-inner', 'board_locked')

def focus_n1(pg):
    new_game(pg)
    r = ev(pg, "() => { try{ return JSON.stringify({ok: StoryPlay.start('N1', {force:true})}); }catch(e){ return 'err:'+e.message; } }")
    rec('n1_start', r)
    pg.wait_for_timeout(2200)
    for step in range(12):
        m = json.loads(ev(pg, N1_MEASURE))
        rec(f'n1_step{step}', {'counter': m.get('counter'), 'dlg': m.get('dlgText')})
        if (m.get('counter') and m['counter'].replace(' ', '') == '5/16') or (m.get('dlgText') and '另一份係去電影片場做散工' in m['dlgText']):
            break
        if not click_any(pg, ['下一句']):
            ev(pg, "() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null&&/下一句/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1500)
    for (vw, vh, tag) in [(390, 844, '390x844'), (430, 707, '430x707'), (430, 932, '430x932')]:
        pg.set_viewport_size({'width': vw, 'height': vh}); pg.wait_for_timeout(1800)
        shot(pg, f'n1_5of16_{tag}')
        rec(f'n1_{tag}', json.loads(ev(pg, N1_MEASURE)))
    # 講者切換：下一句（阿偉講）再截
    pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(800)
    click_any(pg, ['下一句']); pg.wait_for_timeout(1600)
    shot(pg, 'n1_next_390x844')
    rec('n1_next', json.loads(ev(pg, N1_MEASURE)))
    play_out_story(pg)

def focus_sec(pg):
    pg.set_viewport_size({'width': 390, 'height': 844})
    new_game(pg); rich_seed(pg, 520)
    ev(pg, "() => { S.weekPlanWeek37=75; S.weekPlan=['scout_all','rest','scout_all','scout_all','street','cafe_gig','rest']; S.homeEditable=false; try{ if(typeof renderAll==='function') renderAll(); }catch(e){} try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} return 'w'; }")
    open_notebook(pg)
    for tab, name in [('plan', 'sec_nb_plan'), ('works', 'sec_works'), ('ledger', 'sec_ledger'), ('stats389', 'sec_stats')]:
        ev(pg, "(t) => { const b=document.querySelector('[data-htab=\"'+t+'\"]'); if(b) b.click(); return !!b; }", tab)
        pg.wait_for_timeout(1100)
        shot(pg, name)
        contrast(pg, '#v-home', name)
    # 地點面板（入場可能撞巧遇 modal：揀第一個選項播完再開面板）
    opened = False
    for _attempt in range(6):
        if not open_loc_sheet(pg, 'tvb_longmen'):
            continue
        if ev(pg, "() => document.getElementById('mask').classList.contains('on')"):
            ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button')].find(x=>x.offsetParent!==null&&!x.disabled); if(b) b.click(); return !!b; }")
            pg.wait_for_timeout(1200)
            play_out_story(pg)
            continue
        opened = True
        break
    if opened:
        shot(pg, 'sec_loc_panel')
        contrast(pg, '#loc-sheet', 'sec_loc_panel')
        rec('touch_sec_loc_panel', json.loads(ev(pg, TOUCH_JS)))
    else:
        rec('sec_loc_panel', 'sheet-fail')

def focus_map(pg):
    for (vw, vh, tag) in [(390, 844, '390x844'), (430, 707, '430x707')]:
        pg.set_viewport_size({'width': vw, 'height': vh})
        new_game(pg); rich_seed(pg, 520); pg.wait_for_timeout(1000)
        click_any(pg, ['返回地圖']); pg.wait_for_timeout(1200)
        shot(pg, f'map_{tag}')
        info = ev(pg, """() => JSON.stringify((()=>{
          const els=[...document.querySelectorAll('.mn68')].filter(e=>e.offsetParent!==null&&getComputedStyle(e).visibility!=='hidden');
          const items=els.map(e=>{ const r=e.getBoundingClientRect(); return {t:(e.textContent||'').trim(), x:+r.x.toFixed(1), y:+r.y.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1)}; });
          const coll=[];
          for(let i=0;i<items.length;i++) for(let j=i+1;j<items.length;j++){
            const a=items[i], b=items[j];
            const ox=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x), oy=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y);
            if(ox>0&&oy>0) coll.push({a:a.t,b:b.t,ox:+ox.toFixed(1),oy:+oy.toFixed(1)});
          }
          return {n:items.length, nColl:coll.length, coll:coll.slice(0,10)};
        })())""")
        rec(f'map_{tag}', json.loads(info) if info else None)

def main():
    want = sys.argv[1] if len(sys.argv) > 1 else 'all'
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox", "--proxy-server=http://127.0.0.1:18081", "--ignore-certificate-errors"])
        ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERR", str(e)[:200], flush=True))
        fns = {'nb': focus_nb, 'gigs': focus_gigs, 'n1': focus_n1, 'sec': focus_sec, 'map': focus_map}
        names = list(fns.keys()) if want == 'all' else [want]
        for name in names:
            print("=== FOCUS", name, "===", flush=True)
            try: fns[name](pg)
            except Exception as e: print("FOCUS_FAIL", name, repr(e)[:400], flush=True)
            pg.set_viewport_size({"width": 390, "height": 844})
        br.close()
    json.dump(R, open(f"{OUT}/measure_{TAG}.json", 'w'), ensure_ascii=False, indent=1)
    print("DONE", TAG, flush=True)

if __name__ == '__main__':
    main()
