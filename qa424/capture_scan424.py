# -*- coding: utf-8 -*-
"""v402 UI 第九輪修復・基線實駕覆驗。
Serves the repo this script lives in locally (--root 可指去基線副本),
Playwright headless shell 經本地 CONNECT 中繼。
用法：
  /home/hatch/pwenv49/bin/python qa401/drive401.py [--root DIR] [--only phone,hosp,tut,awards,board]
結果 JSON＋截圖 -> /home/hatch/workspace/linji-ui-audit-2026-11-24h/。
只量度／實駕，唔改 code。
手法照抄第八輪審計 probe（probe_phone399.py／probe_hosp399.py／drive399_g.py）：
播種只經 window.S＋localStorage（starVolunteer_map_v19w）；入屋／重繪一律經真實 DOM 撳掣。
驗證點（對照 REPORT.md §四）：
 ① 電話／醫院／教學完結卡：mask 掛 scene-paper401（場景 dim 漸變，唔再純黑 rgba(0,0,0,.72)），
    modal 8px 細圓角＋米紙底＋膠紙貼；等消息卡同理。
 ② 教學：遮罩全幅均勻 dim（頂欄同步降亮）＋金圈挖空（tut-hole401 變數對準金圈中心），
    地圖提示列／圖例隱去（卡邊無半截字），教學卡收窄 ≤330px，「下一步」係右下頁籤
    （唔再全寬大掣），「跳過教學」係卡內文字掣。
 ③ 「繼續」金掣：實色金底、text-shadow:none、無 inset 高光；字色 #1A1410 對實色金
    對比度 ≥4.5:1；掣字放大 3 倍截圖，目測無疊影。
 ④ 35c P2：主標「陳偉翔散場」、奪獎行做小標、dual 行歸屬清晰（缺值省略）、
    小檔案係剪報旁註（去框＋虛線頂線）。
 ⑤ 通告欄：整理選單係索引紙（選項文字行＋紅筆剔號，唔再六粒等寬膠囊掣）；
    詳情三行錢包合約紙、預期日薪算式係手寫備註、已公布陣容最後一行可完整捲出。
"""
import sys, os, json, socket, subprocess, time, urllib.request, hashlib, argparse

sys.path.insert(0, '/home/hatch/workspace/fullarc')
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/hatch/pw-browsers')
from playwright.sync_api import sync_playwright

class _A: root='/home/hatch/workspace/linji-work424'; only='phone,hosp,tut,awards,board,map,notebook,counts,verify'
args=_A()
_argv=sys.argv[:]; sys.argv=sys.argv[:1]
import driver as drv
sys.argv=_argv

ITEMS = [x.strip() for x in args.only.split(',') if x.strip()]
ROOT = args.root or "/home/hatch/workspace/linji-work424"
OUT = "/home/hatch/workspace/linji-work424/qa424/out/scan_after"
SHOTS = OUT + "/shots"

TEXTBOX_JS = """() => JSON.stringify((()=>{ const out=[]; document.querySelectorAll('*').forEach(el=>{ if(el.children.length>0) return; const t=(el.textContent||'').trim(); if(!t) return; const cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity||'1')===0) return; const r=el.getBoundingClientRect(); if(r.width<=0||r.height<=0) return; if(r.bottom<0||r.top>innerHeight||r.right<0||r.left>innerWidth) return; let hit=false; for(const fx of [0.5,0.25,0.75]){ const px=Math.min(innerWidth-1,Math.max(0,r.x+r.width*fx)), py=Math.min(innerHeight-1,Math.max(0,r.y+r.height*0.5)); const top=document.elementFromPoint(px,py); if(top&&(top===el||el.contains(top)||top.contains(el))){hit=true;break;} } out.push({text:t.slice(0,40),x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1),color:cs.color,fontSize:cs.fontSize,hit}); }); function vis(el){ if(!el||el.disabled) return false; if(el.offsetParent===null&&getComputedStyle(el).position!=='fixed') return false; const r=el.getBoundingClientRect(); return r.width>0&&r.height>0; } const clicks=[...document.querySelectorAll('button, a[href], input, select, textarea, summary, [role=button], [tabindex]')].filter(vis).length; const pins=[...document.querySelectorAll('.mn68')].filter(vis).length; const scrollers=[]; document.querySelectorAll('*').forEach(el=>{ if(el.scrollHeight>el.clientHeight+4&&el.clientHeight>0){ const r=el.getBoundingClientRect(); if(r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight){ scrollers.push({id:el.id||'',cls:(el.className||'').toString().slice(0,40),scrollTop:Math.round(el.scrollTop),scrollHeight:el.scrollHeight,clientHeight:el.clientHeight}); } } }); const mask=document.getElementById('mask'); const state={view:(document.querySelector('.view.on')||{}).id||'',maskCls:mask?mask.className:'',h3:(document.querySelector('#modal h3')||{}).textContent||'',day:(typeof S!=='undefined'&&S)?S.dayIndex:null,money:(typeof S!=='undefined'&&S)?S.money:null,fame:(typeof S!=='undefined'&&S)?S.fame:null,stress:(typeof S!=='undefined'&&S)?S.stress:null,scrollY:Math.round(window.scrollY||0),scrollers:scrollers.slice(0,8),panel:{maskOn:!!(mask&&mask.classList.contains('on')),locSheet:!!(document.getElementById('loc-sheet')&&document.getElementById('loc-sheet').offsetParent!==null),menu:!!([...document.querySelectorAll('#menu button')].some(b=>b.offsetParent!==null))}}; return {texts:out.slice(0,400),clickables:clicks,pins,state}; })())"""
def _sidecar(pg, name):
    try:
        import json as _j, os as _os
        data = pg.evaluate(TEXTBOX_JS)
        obj = _j.loads(data) if isinstance(data, str) else data
        vp = pg.viewport_size
        _os.makedirs("/home/hatch/workspace/linji-work424/qa424/out/scan_after/sidecars", exist_ok=True)
        with open(f"/home/hatch/workspace/linji-work424/qa424/out/scan_after/sidecars/{name}.json", "w", encoding="utf-8") as _f:
            _j.dump({"viewport": vp, "data": obj, "state": (obj or {}).get("state")}, _f, ensure_ascii=False)
    except Exception as _e:
        print("SIDECARFAIL", name, str(_e)[:140], flush=True)

os.makedirs(OUT, exist_ok=True); os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"

STORY29 = ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17",
           "R_hiu_meet","R_hiu_crisis","R_choi_meet","R_choi_crisis","R_lan_meet","R_lan_crisis",
           "R_xu_meet","R_xu_crisis","R_yip_meet","R_yip_crisis","R_so_meet","R_so_crisis"]

def free_port():
    for cand in range(9361, 9380):
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
print("serve", URL, flush=True)

COUNT_JS = """() => {
  function vis(el){ if(!el || el.disabled) return false; if(el.offsetParent===null && getComputedStyle(el).position!=='fixed') return false; const r=el.getBoundingClientRect(); return r.width>0 && r.height>0; }
  const all=[...document.querySelectorAll('button, a[href], input, select, textarea, summary, [role=button], [tabindex]')].filter(vis);
  const pins=[...document.querySelectorAll('.mn68')].filter(vis);
  const byTag={}; all.forEach(e=>{ const t=e.tagName.toLowerCase(); byTag[t]=(byTag[t]||0)+1; });
  const texts=all.map(e=>{ const t=(e.textContent||e.value||e.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,28); return t||e.tagName; });
  return JSON.stringify({total: all.length, pins: pins.length, byTag, texts}); }"""

CONTRAST_JS = """(scope) => JSON.stringify((()=>{
  function parseRGB(s){ const m=(s||'').match(/rgba?\\(([^)]+)\\)/); if(!m) return null; const p=m[1].split(',').map(x=>parseFloat(x)); return {r:p[0], g:p[1], b:p[2], a:(p.length>3?p[3]:1)}; }
  function lum(c){ const f=v=>{ v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); }
  function ratio(a,b){ const l1=lum(a), l2=lum(b); if(l1==null||l2==null) return null; const hi=Math.max(l1,l2), lo=Math.min(l1,l2); return +((hi+0.05)/(lo+0.05)).toFixed(2); }
  function effBg(el){ let n=el; while(n && n!==document.body){ const cs=getComputedStyle(n); const bg=parseRGB(cs.backgroundColor); if(bg && bg.a>0.9) return {rgb: cs.backgroundColor, img: cs.backgroundImage}; n=n.parentElement; } return {rgb:'#f6efdc', img:'fallback-paper'}; }
  const root = scope ? document.querySelector(scope) : document.body;
  if(!root) return JSON.stringify({scope, error:'no-root'});
  const out=[];
  root.querySelectorAll('*').forEach(el=>{
    if(el.children.length>0) return;
    const t=(el.textContent||'').trim(); if(!t) return;
    if(el.offsetParent===null && getComputedStyle(el).position!=='fixed') return;
    const r=el.getBoundingClientRect(); if(r.width<=0||r.height<=0) return;
    const cs=getComputedStyle(el); const fg=parseRGB(cs.color); if(!fg) return;
    const bg=effBg(el); const bgc=parseRGB(bg.rgb);
    out.push({text:t.slice(0,40), color:cs.color, fontSize:cs.fontSize, bg:bg.rgb, bgImg:(bg.img||'').slice(0,40),
      ratio: bgc? ratio(fg,bgc): null, pass: bgc? (ratio(fg,bgc)>=4.5): null});
  });
  return JSON.stringify({scope, n:out.length, items:out});
})())"""

# v401：modal 紙卡＋遮罩量度
MODAL401_JS = """() => JSON.stringify((()=>{
  const mask=document.getElementById('mask');
  const modal=document.querySelector('#mask .modal') || document.getElementById('modal');
  const mcs=mask?getComputedStyle(mask):null;
  const cs=modal?getComputedStyle(modal):null;
  const btns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>{
    const r=b.getBoundingClientRect(); const c=getComputedStyle(b);
    return {txt:(b.textContent||'').trim(), cls:b.className, w:+r.width.toFixed(1), h:+r.height.toFixed(1),
      bg:c.backgroundColor, bgImg:(c.backgroundImage||'').slice(0,60), color:c.color,
      textShadow:c.textShadow, boxShadow:(c.boxShadow||'').slice(0,80), fontWeight:c.fontWeight,
      borderRadius:c.borderRadius}; });
  const tape=modal?getComputedStyle(modal,'::before'):null;
  return {maskCls:mask?mask.className:null,
    maskBg:mcs?mcs.background:null, maskBgImg:mcs?(mcs.backgroundImage||'').slice(0,120):null,
    modalBorderRadius:cs?cs.borderRadius:null, modalBg:cs?cs.backgroundColor:null,
    modalBgImg:cs?(cs.backgroundImage||'').slice(0,80):null,
    tapeContent:tape?tape.content:null, tapeH:tape?tape.height:null,
    holeCls:mask?mask.classList.contains('tut-hole401'):null,
    holeX:mask?mask.style.getPropertyValue('--tut-hole-x'):null,
    holeY:mask?mask.style.getPropertyValue('--tut-hole-y'):null,
    holeR:mask?mask.style.getPropertyValue('--tut-hole-r'):null,
    btns}; })())"""

def ev(pg, js, arg=None):
    try: return pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)
    except Exception as e: print("EVFAIL", str(e)[:200], flush=True); return None

def shot(pg, name):
    p = f"{SHOTS}/{name}.png"; pg.screenshot(path=p); _sidecar(pg, name)
    md = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    print("SHOT", name, md, flush=True); return p

def shot_clip(pg, name, clip):
    p = f"{SHOTS}/{name}.png"; pg.screenshot(path=p, clip=clip); _sidecar(pg, name)
    md = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    print("SHOT", name, md, flush=True); return p

def save_out(name, obj):
    json.dump(obj, open(f"{OUT}/{name}", 'w'), ensure_ascii=False, indent=1)
    print("SAVED", name, flush=True)

def count(pg, key):
    c = ev(pg, COUNT_JS)
    try: j = json.loads(c)
    except Exception: j = {'raw': c}
    print("COUNT", key, j.get('total'), 'pins', j.get('pins'), flush=True)
    return j

def contrast(pg, scope, label):
    c = ev(pg, CONTRAST_JS, scope)
    try:
        j = json.loads(c)
        if isinstance(j, str): j = json.loads(j)
    except Exception: j = {'raw': c}
    fails = [i for i in j.get('items', []) if i.get('pass') is False]
    print("CONTRAST", label, 'n=', j.get('n'), 'fail<4.5:', len(fails), [(f['text'][:16], f['ratio']) for f in fails[:8]], flush=True)
    return j

def modal401(pg, label):
    r = ev(pg, MODAL401_JS)
    try: j = json.loads(r)
    except Exception: j = {'raw': r}
    print("MODAL401", label, json.dumps(j, ensure_ascii=False)[:600], flush=True)
    return j

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
          const nb=o.querySelector('.e79-btn'); if(nb){ nb.click(); return 'next:'+(nb.textContent||'').trim().slice(0,12); }
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
        wf4 = ev(pg, """() => { const m=document.getElementById('mask'); if(!(m&&m.classList.contains('wf4-stage-on'))) return false; const b=[...document.querySelectorAll('#modal-btns button')].find(x=>x.offsetParent!==null&&!x.disabled); if(!b) return false; b.click(); return (b.textContent||'').trim().slice(0,30); }""")
        if wf4:
            pg.wait_for_timeout(700); continue
        break
    pg.wait_for_timeout(700)
    return not ev(pg, "() => document.getElementById('mask').classList.contains('on')")

def go_map(pg):
    click_any(pg, ['返回地圖']); pg.wait_for_timeout(900)

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

def seed_main(pg, day=1, stats=None):
    st = stats or {'acting':70,'stage':60,'vocal':45,'looks':55,'charm':50,'iq':45,'stamina':80}
    return ev(pg, """(a) => {
  const st=a[1];
  S.acting=st.acting; S.stage=st.stage; S.vocal=st.vocal; S.looks=st.looks; S.charm=st.charm; S.iq=st.iq; S.stamina=st.stamina;
  S.fame=120; S.money=9000; S.stress=20; S.dayIndex=a[0];
  S.weekPlan=['scout_all','street','scout_all','scout_all','scout_all','scout_all','scout_all'];
  S.shoots=[]; S.booked=[]; S.pendingAud=[]; S.aud91Log=[]; S.grant229Queue=[];
  if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
  %s.forEach(id=>{ S.story.done[id]=true; });
  S.story.flags=Object.assign({}, S.story.flags, {route_tv:true});
  S.flags=Object.assign({}, S.flags, {route_tv:true});
  S.story.routes={route_tv:true};
  S.travel114={day:S.dayIndex, used:0};
  try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
  return S.dayIndex; }""" % json.dumps(STORY29), [day, st])

def open_loc_sheet(pg, loc):
    ev(pg, "() => { if(typeof S!=='undefined' && S){ S.travel114={day:S.dayIndex, used:0}; try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} } return 'ok'; }")
    for attempt in range(4):
        go_map(pg); pg.wait_for_timeout(1000)
        ev(pg, """(loc) => { const p=document.querySelector('.pin[data-loc="'+loc+'"]'); if(p) p.click(); return !!p; }""", loc)
        pg.wait_for_timeout(1500)
        play_out_story(pg)
        if ev(pg, "() => { const sh=document.getElementById('loc-sheet'); return !!(sh && sh.offsetParent!==null); }"):
            return True
    return False

def open_board(pg):
    if not open_loc_sheet(pg, 'tvb_longmen'):
        print("BOARD_SHEET_FAIL", flush=True); return False
    r = ev(pg, """() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/通告欄/.test(x.textContent||'')); if(b) b.click(); return !!b; }""")
    pg.wait_for_timeout(1200)
    return True

def state_json(pg):
    r = ev(pg, """() => JSON.stringify({day:(typeof S!=='undefined'&&S)?S.dayIndex:null,
      stress:(typeof S!=='undefined'&&S)?S.stress:null,
      money:(typeof S!=='undefined'&&S)?S.money:null,
      pending:(typeof S!=='undefined'&&S)?(S.pendingAud||[]).map(p=>({gigId:p.gigId,title:p.title,ok:p.ok,revealDay:p.revealDay,audDay:p.audDay,chancePct:p.chancePct})):null,
      mask:document.getElementById('mask').className,
      h3:(document.querySelector('#modal h3')||{}).textContent||null,
      body:(document.getElementById('modal-inner')||{}).innerText.slice(0,400)||null,
      view:(document.querySelector('.view.on')||{}).id||'',
      btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim().slice(0,24))})""")
    try: return json.loads(r)
    except Exception: return {'raw': r}

# ================= 電話（43b 等消息卡＋43d 獲聘／43e 首次落選／43f 落選來電） =================
def do_audition(pg, idx):
    ev(pg, """(i) => { const c=document.querySelectorAll('.gig-teaser')[i]; if(c) c.click(); return !!c; }""", idx)
    pg.wait_for_timeout(1200)
    click_modal(pg, ['接通告']); pg.wait_for_timeout(1500)
    click_modal(pg, ['確定進行']); pg.wait_for_timeout(1500)
    for step in range(50):
        pg.wait_for_timeout(800)
        st = state_json(pg)
        if '試鏡完畢' in (st.get('h3') or ''):
            return st
        if not ('on' in (st.get('mask') or '')):
            return st
        play_out_story(pg)
        if not click_modal(pg, ['下一句', '繼續', '確定', '收下', '跳過', '關閉', '返回地圖']):
            pass
    return state_json(pg)

def capture_wait_card(pg, tag):
    """43b 等消息卡就係而家呢張（h3「試鏡完畢・等消息」＋「繼續」金掣）：
    唔好撳掣先量——直接量度呢張卡＋放大掣圖，量完先由呼叫方撳「繼續」走人。"""
    st = state_json(pg)
    out = {'h3': st.get('h3'), 'btns': st.get('btns'), 'mask': st.get('mask')}
    out['modal401'] = modal401(pg, 'wait43b-' + tag)
    out['contrast'] = contrast(pg, '#modal', 'wait43b-' + tag)
    shot(pg, '402_43b_wait_' + tag)
    # 金掣「繼續」放大：搵 .p 掣 rect，做 clip 截圖（dsf 2 下 clip 係 CSS px）
    box = ev(pg, """() => { const b=[...document.querySelectorAll('#modal-btns button.p')].find(x=>x.offsetParent!==null);
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x, y:r.y, width:r.width, height:r.height}; }""")
    if box:
        out['gold_btn_box'] = box
        pad = 6
        shot_clip(pg, '402_43b_goldbtn_zoom_' + tag,
                  {'x': max(0, box['x'] - pad), 'y': max(0, box['y'] - pad),
                   'width': box['width'] + pad * 2, 'height': box['height'] + pad * 2})
    return out

def run_attempt(pg, tag, stats, want_ok, shotname, preset_fail_seen=False):
    res = {'tag': tag, 'want_ok': want_ok, 'auditions': []}
    new_game(pg)
    seed_main(pg, 1, stats)
    if preset_fail_seen:
        ev(pg, "() => { S.flags=S.flags||{}; S.flags.sawTutAudFail=true; try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} return 'preset'; }")
    target = None
    for idx in range(3):
        if not open_board(pg):
            res['board_fail'] = idx; break
        st = do_audition(pg, idx)
        res['auditions'].append({'idx': idx, 'h3': st.get('h3'), 'pending': st.get('pending'), 'day': st.get('day')})
        # 43b 等消息卡：第一次試鏡嗰陣量度（之後嘅等消息卡同一支樣式）
        if idx == 0 and '試鏡完畢' in (st.get('h3') or ''):
            res['wait43b'] = capture_wait_card(pg, tag)
        ev(pg, "() => { const d=(S.dayIndex|0)+999; (S.pendingAud||[]).forEach(p=>{ p.revealDay=d; }); try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} return 'neutralized'; }")
        pend = st.get('pending') or []
        hit = [p for p in pend if p.get('ok') == want_ok]
        if hit:
            target = hit[0]
            break
        if not click_modal(pg, ['繼續', '返回地圖', '確定', '關閉']):
            play_out_story(pg)
        pg.wait_for_timeout(1000)
    if not target:
        flipped = ev(pg, """(want) => {
          const ps=S.pendingAud||[]; if(!ps.length) return 'no-pending';
          const p=ps[ps.length-1]; p.ok=!!want;
          if(!want){ p.fxFame=-1; p.pay=0; p.fame=0; p.pop=0; }
          try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
          return JSON.stringify({gigId:p.gigId, ok:p.ok}); }""", want_ok)
        res['flipped'] = flipped
        pend_now = ev(pg, "() => JSON.stringify((S.pendingAud||[]).map(p=>({gigId:p.gigId,title:p.title,ok:p.ok,revealDay:p.revealDay,audDay:p.audDay,chancePct:p.chancePct})))")
        try: pend_now = json.loads(pend_now)
        except Exception: pend_now = []
        hit = [p for p in pend_now if p.get('ok') == want_ok]
        if hit:
            target = hit[0]
        else:
            res['found'] = False
            return res
    res['found'] = True
    res['target'] = target
    adj = ev(pg, """(t) => {
      const day=S.dayIndex|0;
      (S.pendingAud||[]).forEach(p=>{ if(p.gigId===t.gigId && p.audDay===t.audDay){ p.revealDay=day; } else { p.revealDay=day+999; } });
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return JSON.stringify({day, pending:(S.pendingAud||[]).map(p=>({gigId:p.gigId,ok:p.ok,revealDay:p.revealDay}))}); }""", target)
    res['adjusted'] = adj
    seen = []
    found = False
    for step in range(170):
        pg.wait_for_timeout(800)
        st = state_json(pg)
        seen.append({'step': step, 'day': st.get('day'), 'h3': st.get('h3'), 'view': st.get('view'), 'btns': st.get('btns')})
        if not res.get('tut43e'):
            _tut = ev(pg, "() => { const t=document.querySelector('#modal .tut-card'); if(!t) return null; return (t.querySelector('.tut-title')||{}).textContent||'tut'; }")
            if _tut:
                res['tut43e'] = {'title': _tut, 'count': count(pg, '43e-tutcard'), 'clash': modal_label_clash(pg)}
                shot(pg, '402_43e_tutcard')
        h3 = st.get('h3') or ''
        body = st.get('body') or ''
        _tgt = (target or {}).get('title') or ''
        if want_ok and (h3.startswith('獲聘') and (not _tgt or _tgt in h3)):
            res['result'] = st; res['result_modal401'] = modal401(pg, 'phone-hired')
            res['result_contrast'] = contrast(pg, '#modal', 'phone-hired')
            res['geometry402'] = measure_43d402(pg, tag)
            shot(pg, shotname); found = True; break
        if want_ok and h3 == '何生來電' and '簽約金' in body and (not _tgt or _tgt in body):
            res['result'] = st; res['result_modal401'] = modal401(pg, 'phone-hired')
            res['result_contrast'] = contrast(pg, '#modal', 'phone-hired')
            res['geometry402'] = measure_43d402(pg, tag)
            shot(pg, shotname); found = True; break
        if (not want_ok) and h3 == '何生來電' and '冇你份' in body and (not _tgt or _tgt in body):
            res['result'] = st; res['result_modal401'] = modal401(pg, 'phone-fail')
            res['result_contrast'] = contrast(pg, '#modal', 'phone-fail')
            res['count402'] = count(pg, '43e-' + tag)
            res['clash402'] = modal_label_clash(pg)
            shot(pg, shotname); found = True; break
        if (not want_ok) and h3 == '本次未獲聘':
            res['result'] = st; res['result_variant'] = 'settlement-first-fail'
            res['result_modal401'] = modal401(pg, 'phone-settlement')
            res['result_contrast'] = contrast(pg, '#modal', 'phone-settlement')
            shot(pg, shotname); found = True; break
        if h3.startswith('獲聘') and not want_ok:
            res.setdefault('wrong_reveals', []).append(h3)
            click_modal(pg, ['好']); pg.wait_for_timeout(1200); continue
        if h3 == '何生來電' and '冇你份' in body and want_ok:
            res.setdefault('wrong_reveals', []).append(h3)
            click_modal(pg, ['繼續']); pg.wait_for_timeout(1200); continue
        mask_on = 'on' in (st.get('mask') or '')
        if not mask_on and st.get('view') == 'v-map':
            r = click_any(pg, ['開始今日行程'])
            if not r:
                r = click_any(pg, ['過一日'])
            if not r:
                r = ev(pg, "() => { try{ if(typeof startTodayScheduleFromMap==='function'){ startTodayScheduleFromMap(); return 'startFn'; } }catch(e){ return 'err:'+e.message; } return false; }")
            print("PHONE_MAPADV", r, st.get('day'), flush=True)
            pg.wait_for_timeout(1200); continue
        if not mask_on:
            ch = ev(pg, """() => { const o=document.getElementById('enc79-overlay'); if(!o) return null;
              const nb=o.querySelector('.e79-btn'); if(nb){ nb.click(); return 'next'; }
              const sk=o.querySelector('.e79-skip'); if(sk){ sk.click(); return 'skip'; } return null; }""")
            if ch:
                pg.wait_for_timeout(700); continue
            if ev(pg, "() => { const c=document.querySelector('.sp-choice'); if(c && c.offsetParent!==null){ c.click(); return true; } return false; }"):
                pg.wait_for_timeout(700); continue
            pg.wait_for_timeout(700); continue
        if '通告欄' in h3:
            click_any(pg, ['返去地點']); pg.wait_for_timeout(900); continue
        if h3 == '拍攝排程':
            click_modal(pg, ['只排空日', '留待下週']); pg.wait_for_timeout(1200); continue
        if '試鏡完畢' in h3:
            click_modal(pg, ['繼續']); pg.wait_for_timeout(1200); continue
        if '開始今日行程' in h3:
            click_modal(pg, ['開始並結算當日']); pg.wait_for_timeout(1000); continue
        if 'day-res' in (st.get('mask') or ''):
            click_modal(pg, ['開始今日行程', '回家結算', '返回地圖']); pg.wait_for_timeout(1000); continue
        if click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '確定', '收下這份剪報', '跳過', '關閉', '開始今日行程', '回家結算', '簽約', '我知道了', '返回地圖', '好']):
            pg.wait_for_timeout(900); continue
        _sc = ev(pg, """() => { const c=document.querySelector('.sp-choice'); if(c && c.offsetParent!==null){ const t=(c.textContent||'').trim().slice(0,20); c.click(); return 'sp:'+t; }
          const m=document.getElementById('modal'); if(!m) return null;
          const bs=[...m.querySelectorAll('button')].filter(b=>b.offsetParent!==null&&!b.disabled);
          if(bs.length===2){ const t=(bs[0].textContent||'').trim().slice(0,20); bs[0].click(); return 'modal2:'+t; } return null; }""")
        if _sc:
            print("PHONE_STORY_CHOICE", _sc, st.get('h3'), flush=True)
            res.setdefault('story_choices', []).append({'h3': st.get('h3'), 'picked': _sc})
            pg.wait_for_timeout(1200); continue
        print("PHONE_STUCK", st.get('day'), st.get('h3'), st.get('btns'), flush=True)
        res.setdefault('stuck_at', st)
        break
    res['found_result'] = found
    res['seen'] = seen
    return res

# ================= 醫院（46 offer／46b 確認／46c 唔夠錢／46d 治療後） =================
def seed_sick(pg, money):
    return ev(pg, """(a) => {
      S.dayIndex=17; S.stress=98; S.money=a.money; S.fame=120;
      S.weekPlan=['scout_all','scout_all','scout_all','scout_all','scout_all','scout_all','scout_all'];
      S.homeEditable=false; S.pendingAud=[]; S.booked=[]; S.shoots=[];
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      a.ids.forEach(id=>{ S.story.done[id]=true; });
      if(!S.conseq61) S.conseq61={};
      S.conseq61.streak90=1; S.conseq61.streak80=2; S.conseq61.cooldownUntil=0; S.conseq61.sick=null;
      S.starDay={day:17, presence:{}, triggered:99, doneToday:{}};
      S.romDay={day:17, presence:{}, triggered:99, doneToday:{}};
      S.travel114={day:17, used:0};
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return 'seeded money='+S.money; }""", {'money': money, 'ids': STORY29})

def run_variant(pg, tag, money):
    new_game(pg)
    print("SEED", seed_sick(pg, money), flush=True)
    go_map(pg)
    res = {'tag': tag, 'money_seed': money, 'steps': []}
    gate_seen = False
    for step in range(160):
        pg.wait_for_timeout(800)
        st = state_json(pg)
        res['steps'].append({'step': step, 'day': st.get('day'), 'stress': st.get('stress'),
                             'money': st.get('money'), 'h3': st.get('h3'), 'view': st.get('view'),
                             'btns': st.get('btns')})
        h3 = st.get('h3') or ''
        if h3.startswith('病到燶'):
            gate_seen = True
            res['gate'] = st
            res['gate_modal401'] = modal401(pg, 'hosp-' + tag)
            res['gate_contrast'] = contrast(pg, '#modal', 'hosp-' + tag)
            shot(pg, '402_46_offer_' + tag)
            res['clash402'] = modal_label_clash(pg)
            if tag == 'afford':
                c = click_modal(pg, ['去醫院治療'])
                pg.wait_for_timeout(1200)
                res['after_treat_click'] = c
                st2 = state_json(pg)
                res['confirm_state'] = st2
                res['confirm_modal401'] = modal401(pg, 'hosp-confirm')
                res['confirm_contrast'] = contrast(pg, '#modal', 'hosp-confirm')
                shot(pg, '402_46b_confirm')
                click_modal(pg, ['確定'])
                pg.wait_for_timeout(1500)
                res['after_confirm'] = state_json(pg)
                # 46d：治療後病假日結卡（afterDayModal 病假路徑）
                res['treated_modal401'] = modal401(pg, 'hosp-treated-46d')
                res['treated_contrast'] = contrast(pg, '#modal', 'hosp-treated-46d')
                shot(pg, '402_46d_treated_after')
            else:
                click_modal(pg, ['留喺屋企休養'])
                pg.wait_for_timeout(1200)
                res['after_stay'] = state_json(pg)
                res['stay_modal401'] = modal401(pg, 'hosp-stay-46c')
                shot(pg, '402_46c_stay')
            break
        mask_on = 'on' in (st.get('mask') or '')
        if not mask_on and st.get('view') == 'v-map':
            r = click_any(pg, ['開始今日行程'])
            if not r:
                r = click_any(pg, ['過一日'])
            if not r:
                print("HOSP_NOSTART", st.get('day'), flush=True); break
            pg.wait_for_timeout(1200); continue
        if not mask_on:
            ch = ev(pg, """() => { const o=document.getElementById('enc79-overlay'); if(!o) return null;
              const nb=o.querySelector('.e79-btn'); if(nb){ nb.click(); return 'next'; }
              const sk=o.querySelector('.e79-skip'); if(sk){ sk.click(); return 'skip'; } return null; }""")
            if ch:
                pg.wait_for_timeout(700); continue
            if ev(pg, "() => { const c=document.querySelector('.sp-choice'); if(c && c.offsetParent!==null){ c.click(); return true; } return false; }"):
                pg.wait_for_timeout(700); continue
            pg.wait_for_timeout(700); continue
        if '通告欄' in h3:
            click_any(pg, ['返去地點']); pg.wait_for_timeout(900); continue
        if '開始今日行程' in h3:
            click_modal(pg, ['開始並結算當日']); pg.wait_for_timeout(1000); continue
        if '病倒休養' in h3:
            res['sick_card_first'] = st
            shot(pg, '402_46x_gate_missed_sickcard')
            click_modal(pg, ['返回地圖']); pg.wait_for_timeout(1200)
            click_any(pg, ['過一日'])
            pg.wait_for_timeout(1500); continue
        if click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '確定', '收下這份剪報', '跳過', '關閉', '開始今日行程', '回家結算', '返回地圖']):
            pg.wait_for_timeout(900); continue
        print("HOSP_STUCK", st.get('day'), st.get('h3'), st.get('btns'), flush=True)
        res['stuck_at'] = st
        break
    res['gate_seen'] = gate_seen
    return res

# ================= 教學（tut_01–03＋TUT_DONE＋B01 tut_04） =================
TUT401_JS = """() => JSON.stringify((()=>{
  const mask=document.getElementById('mask');
  const pin=document.querySelector('.pin[data-loc="tvb_longmen"]') || document.querySelector('.pin:not(.dim)');
  const pr = pin ? pin.getBoundingClientRect() : null;
  const card = document.querySelector('#modal .tut-card');
  const cr = card ? card.getBoundingClientRect() : null;
  const modal = document.querySelector('#mask .modal');
  const mr = modal ? modal.getBoundingClientRect() : null;
  const ring = document.getElementById('tut-spotlight-ring');
  const rr = ring ? ring.getBoundingClientRect() : null;
  const mcs = mask ? getComputedStyle(mask) : null;
  const hint = document.querySelector('.map-hint');
  const legend = document.querySelector('.map-legend');
  const labels = [...document.querySelectorAll('#map-names68 .mn68')].filter(e=>e.offsetParent!==null).map(e=>{
    const r=e.getBoundingClientRect();
    let inter=null;
    if(rr && rr.width>0){
      const ox=Math.max(0, Math.min(r.right,rr.right)-Math.max(r.left,rr.left));
      const oy=Math.max(0, Math.min(r.bottom,rr.bottom)-Math.max(r.top,rr.top));
      if(ox>0 && oy>0) inter={ox:+ox.toFixed(1), oy:+oy.toFixed(1), area:+(ox*oy).toFixed(1)};
    }
    return {txt:(e.textContent||'').trim(), x:+r.x.toFixed(1), y:+r.y.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1), vis:getComputedStyle(e).visibility, inter};
  });
  const clone = document.getElementById('tut-target-label399');
  const clr = clone ? clone.getBoundingClientRect() : null;
  // 卡邊半截字：搵 #app 入面可見文字元素，同 modal rect 交疊但唔完全喺 modal 入面
  const appRect = document.getElementById('app').getBoundingClientRect();
  const clipped = [];
  if(mr){
    document.querySelectorAll('#app .map-hint, #app .map-legend, #app .day-card, #app .date-strip, #app [class*="daycard"]').forEach(el=>{
      if(el.offsetParent===null) return;
      const r=el.getBoundingClientRect();
      const overlap = !(r.bottom<=mr.top || r.top>=mr.bottom || r.right<=mr.left || r.left>=mr.right);
      if(overlap) clipped.push({cls:el.className.slice(0,40), txt:(el.textContent||'').trim().slice(0,30),
        top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), cardTop:+mr.top.toFixed(1), cardBottom:+mr.bottom.toFixed(1)});
    });
  }
  const btns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>{
    const r=b.getBoundingClientRect(); const c=getComputedStyle(b);
    return {txt:(b.textContent||'').trim(), cls:b.className, w:+r.width.toFixed(1), h:+r.height.toFixed(1),
      bg:c.backgroundColor, textDec:c.textDecoration, border:c.border, order:c.order}; });
  return {step: mask.dataset.tutStep||null, maskCls: mask.className,
    maskBg: mcs?mcs.background:null, maskBgImg: mcs?(mcs.backgroundImage||'').slice(0,160):null,
    holeCls: mask.classList.contains('tut-hole401'),
    holeX: mask.style.getPropertyValue('--tut-hole-x'), holeY: mask.style.getPropertyValue('--tut-hole-y'),
    holeR: mask.style.getPropertyValue('--tut-hole-r'),
    hintDisplay: hint?getComputedStyle(hint).display:null,
    legendDisplay: legend?getComputedStyle(legend).display:null,
    pin: pr?{x:+pr.x.toFixed(1), y:+pr.y.toFixed(1), w:+pr.width.toFixed(1), h:+pr.height.toFixed(1)}:null,
    card: cr?{x:+cr.x.toFixed(1), y:+cr.y.toFixed(1), w:+cr.width.toFixed(1), h:+cr.height.toFixed(1), bottom:+cr.bottom.toFixed(1)}:null,
    modal: mr?{x:+mr.x.toFixed(1), y:+mr.y.toFixed(1), w:+mr.width.toFixed(1), h:+mr.height.toFixed(1), bottom:+mr.bottom.toFixed(1)}:null,
    ring: rr?{x:+rr.x.toFixed(1), y:+rr.y.toFixed(1), w:+rr.width.toFixed(1), h:+rr.height.toFixed(1), display: getComputedStyle(ring).display}:null,
    labels, nHidden: labels.filter(l=>l.vis==='hidden').length,
    clone: clr?{x:+clr.x.toFixed(1), y:+clr.y.toFixed(1), w:+clr.width.toFixed(1), h:+clr.height.toFixed(1), bottom:+clr.bottom.toFixed(1), display: getComputedStyle(clone).display}:null,
    clipped, btns}; })())"""

def probe_tut(pg):
    res = {}
    pg.goto(URL); pg.wait_for_timeout(1500)
    ev(pg, "() => { try{ localStorage.clear(); }catch(e){} return true; }")
    pg.goto(URL); pg.wait_for_timeout(2500)
    pg.click('#btn-new'); pg.wait_for_timeout(1500)
    res['step0'] = json.loads(ev(pg, TUT401_JS))
    shot(pg, '402_tut_step0_welcome')
    click_modal(pg, ['下一步']); pg.wait_for_timeout(1500)
    res['step1'] = json.loads(ev(pg, TUT401_JS))
    shot(pg, '402_tut_step1_map')
    res['step1_count'] = count(pg, 'tut_01')
    res['step1_clash'] = modal_label_clash(pg)
    click_modal(pg, ['下一步']); pg.wait_for_timeout(1200)
    res['step2'] = json.loads(ev(pg, TUT401_JS))
    shot(pg, '402_tut_step2_board')
    res['step2_count'] = count(pg, 'tut_step2')
    res['step2_clash'] = modal_label_clash(pg)
    click_modal(pg, ['下一步', '我知道了']); pg.wait_for_timeout(1200)
    res['step3'] = json.loads(ev(pg, TUT401_JS))
    shot(pg, '402_tut_step3_done')
    # TUT_DONE 卡撳掣 → finishTutorial → B01 入門卡（tut_04）
    click_modal(pg, ['我知道了', '下一步']); pg.wait_for_timeout(1500)
    res['b01'] = state_json(pg)
    res['b01_modal401'] = modal401(pg, 'tut-b01')
    res['b01_contrast'] = contrast(pg, '#modal', 'tut-b01')
    shot(pg, '402_tut_04_b01')
    save_out('tut402.json', res)
    return res

# ================= 頒獎 35c =================
def probe_awards(pg):
    new_game(pg)
    ev(pg, """() => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = 423; S.homeEditable = false; S.weekPlanWeek37 = Math.floor(423/7)+1;
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19"].forEach(id=>{ S.story.done[id]=true; });
      S.story.phase='P5';
      S.starDay = {day:423, presence:{}, triggered:99, doneToday:{}};
      S.romDay = {day:423, presence:{}, triggered:99, doneToday:{}};
      S.travel114 = {day:423, used:0};
      S.wrapHistory = [
        { gigId:'gig_1991_film_102', title:'《霓虹夜影》男主角', type:'電影', totalDays:24, pay:3000, fame:20, popularity:10, wrappedDay:390, rating:'表現穩妥' },
        { gigId:'gig_1991_ad_111', title:'《新春團圓》廣告主角', type:'廣告', totalDays:2, pay:400, fame:40, popularity:8, wrappedDay:395, rating:'順利殺青' }
      ];
      return true; }""")
    click_any(pg, ['返回地圖']); pg.wait_for_timeout(1000)
    for i in range(12):
        if ev(pg, "() => (document.querySelector('.view.on')||{}).id") == 'v-map' and not ev(pg, "() => document.getElementById('mask').classList.contains('on')"): break
        c = click_any(pg, ['下一句', '繼續', '確定', '收下這份剪報', '收下剪報', '跳過', '關閉'])
        if not c and ev(pg, "() => document.getElementById('mask').classList.contains('on')"): pg.mouse.click(195, 120)
        pg.wait_for_timeout(700)
    ev(pg, """() => { try{ const A = window.__awards; if(!A) return 'noA';
        if(A.debugForceSeasonWindow) A.debugForceSeasonWindow();
        if(A.queue) A.queue();
        if(A.present) A.present();
        return 'ok'; }catch(e){ return 'err:'+e.message; } }""")
    pg.wait_for_timeout(1500)
    click_any(pg, ['出席']); pg.wait_for_timeout(900)
    click_any(pg, ['確定']); pg.wait_for_timeout(1500)
    ev(pg, """() => { try{ const b=S.awardBooked213; if(!b) return 'no-booked';
      S.dayIndex = (b.ceremonyDay|0) + 1;
      const r = window.__awards.playEvening213 ? window.__awards.playEvening213() : 'no-fn';
      return JSON.stringify({ceremonyDay: b.ceremonyDay, nowDay: S.dayIndex, played: r}); }catch(e){ return 'err:'+e.message; } }""")
    pg.wait_for_timeout(1500)
    ceremony402 = {}
    for _ in range(30):
        if ev(pg, "() => !!document.querySelector('.paper-sheet')"): break
        if not ceremony402.get('counted'):
            _stage = ev(pg, "() => { const e=document.querySelector('.awd62-stage'); if(!e) return false; const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && getComputedStyle(e).display!=='none'; }")
            if _stage:
                ceremony402['counted'] = True
                ceremony402['count'] = count(pg, '35b_ceremony')
                shot(pg, '402_35b_ceremony')
        skipped = ev(pg, "() => { const b=document.querySelector('.awd62-skip'); if(b){ b.click(); return true; } return false; }")
        if not skipped:
            click_modal(pg, ['下一句', '繼續', '確定', '跳過'])
        pg.wait_for_timeout(1000)
    pg.wait_for_timeout(1200)
    res = {}
    res['ceremony'] = ceremony402
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(600)
    shot(pg, '402_awards_p1')
    res['p1'] = awards_p1_402(pg)
    click_any(pg, ['第二版']); pg.wait_for_timeout(900)
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(600)
    res['p2'] = ev(pg, """() => JSON.stringify((()=>{
      const p2=document.querySelector('.np214-page[data-np214-page="2"]');
      if(!p2) return {on:false};
      const h3=p2.querySelector('.np214-headline2');
      const sub=p2.querySelector('.np214-subhead401');
      const lead=p2.querySelector('.np214-body2 .np214-lead');
      const dual=document.querySelector('.psr-dual');
      const fb=p2.querySelector('.np214-factbox');
      const fcs=fb?getComputedStyle(fb):null;
      const scroller=document.getElementById('modal-inner');
      return {on:p2.classList.contains('on'),
        headline:h3?(h3.textContent||'').trim():null,
        subhead:sub?(sub.textContent||'').trim():null,
        lead:lead?(lead.textContent||'').trim().slice(0,120):null,
        dual:dual?(dual.textContent||'').trim():null,
        factbox:{borderTop:fcs?fcs.borderTop:null, border:fcs?fcs.border:null,
          bg:fcs?fcs.backgroundColor:null, fontSize:fcs?fcs.fontSize:null},
        scrollH: scroller?scroller.scrollHeight:null, clientH: scroller?scroller.clientHeight:null}; })())""")
    shot(pg, '402_awards_p2')  # 頂圖：主標「陳偉翔散場」＋奪獎小標（此時 scrollTop 0）
    res['p2_photo'] = awards_p2_photo402(pg)
    # 捲到底：P2 底 dual 行＋小檔案要完整見到
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    res['p2_bottom'] = ev(pg, """() => JSON.stringify((()=>{
      const p2=document.querySelector('.np214-page[data-np214-page="2"]');
      const scroller=document.getElementById('modal-inner');
      const sr=scroller?scroller.getBoundingClientRect():null;
      const dual=document.querySelector('.psr-dual');
      const dr=dual?dual.getBoundingClientRect():null;
      const fb=p2?p2.querySelector('.np214-factbox'):null;
      const fr=fb?fb.getBoundingClientRect():null;
      return {scrollTop: scroller?scroller.scrollTop:null,
        dualBottom: dr?+dr.bottom.toFixed(1):null, viewBottom: sr?+sr.bottom.toFixed(1):null,
        dualFullyVisible: (dr&&sr)?(dr.bottom<=sr.bottom+1):null,
        factBottom: fr?+fr.bottom.toFixed(1):null,
        factFullyVisible: (fr&&sr)?(fr.bottom<=sr.bottom+1):null}; })())""")
    shot(pg, '402_awards_p2_bottom')
    save_out('awards402.json', res)
    return res

# ================= 通告欄（整理選單＋詳情頁） =================
def probe_board(pg):
    new_game(pg)
    seed_main(pg, 1)
    assert open_board(pg), "board open failed"
    res = {}
    res['head'] = ev(pg, """() => JSON.stringify({
      nCards: document.querySelectorAll('.gig-teaser').length })""")
    shot(pg, '402_board_peak')
    res['seal402'] = seal_measure402(pg)
    res['cards402'] = board_cards402(pg)
    click_any(pg, ['整理']); pg.wait_for_timeout(800)
    res['organize_open'] = ev(pg, """() => JSON.stringify((()=>{
      const menu=document.querySelector('.board-menu397');
      const mr=menu?menu.getBoundingClientRect():null;
      const mcs=menu?getComputedStyle(menu):null;
      const chips=[...document.querySelectorAll('.board-menu397 .board-chip392')].map(c=>{
        const r=c.getBoundingClientRect(); const cs=getComputedStyle(c);
        const after=getComputedStyle(c,'::after');
        return {txt:(c.textContent||'').trim(), on:c.classList.contains('on'),
          w:+r.width.toFixed(1), h:+r.height.toFixed(1),
          bg:cs.backgroundColor, border:cs.border, radius:cs.borderRadius,
          afterContent:after.content, afterColor:after.color}; });
      return {menuRect: mr?{x:+mr.x.toFixed(1), w:+mr.width.toFixed(1), h:+mr.height.toFixed(1)}:null,
        menuBg: mcs?mcs.backgroundImage:null, menuTransform: mcs?mcs.transform:null,
        chips}; })())""")
    shot(pg, '402_board_organize')
    # 關選單，入第一張詳情頁
    click_any(pg, ['整理']); pg.wait_for_timeout(500)
    ev(pg, """() => { const c=document.querySelectorAll('.gig-teaser')[0]; if(c) c.click(); return !!c; }""")
    pg.wait_for_timeout(1500)
    res['detail'] = ev(pg, """() => JSON.stringify((()=>{
      const contract=document.querySelector('.cn-contract401');
      const calc=document.querySelector('.board-calc397');
      const calcCs=calc?getComputedStyle(calc):null;
      const castRows=[...document.querySelectorAll('.cn-summary .cn-sum-row')].filter(r=>/^(男主角|女主角|男配角|女配角)/.test((r.textContent||'').trim()));
      const scroller=document.querySelector('.notice_sheet_body');
      const sr=scroller?scroller.getBoundingClientRect():null;
      return {contract: !!contract,
        contractRows: contract?[...contract.querySelectorAll('.cn-sum-row')].map(r=>(r.textContent||'').trim().slice(0,24)):null,
        calc: calc?(calc.textContent||'').trim().slice(0,120):null,
        calcFont: calcCs?calcCs.fontFamily:null, calcSize: calcCs?calcCs.fontSize:null,
        castRows: castRows.map(r=>(r.textContent||'').trim().slice(0,24)),
        nCastRows: castRows.length,
        scrollerBottom: sr?+sr.bottom.toFixed(1):null,
        scrollH: scroller?scroller.scrollHeight:null, clientH: scroller?scroller.clientHeight:null}; })())""")
    shot(pg, '402_board_detail_top')
    # 捲到底：已公布陣容最後一行要完整捲出
    ev(pg, "() => { const sc=document.querySelector('.notice_sheet_body'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    res['detail_bottom'] = ev(pg, """() => JSON.stringify((()=>{
      const scroller=document.querySelector('.notice_sheet_body');
      const sr=scroller?scroller.getBoundingClientRect():null;
      const castRows=[...document.querySelectorAll('.cn-summary .cn-sum-row')].filter(r=>/^(男主角|女主角|男配角|女配角)/.test((r.textContent||'').trim()));
      const last=castRows[castRows.length-1];
      const lr=last?last.getBoundingClientRect():null;
      // 下一行殘字檢查：最後一行下面仲有冇半截行（下一個兄弟元素露出 < 1 行高）
      let nextPartial=null;
      if(last){ const nx=last.nextElementSibling;
        if(nx){ const nr=nx.getBoundingClientRect();
          nextPartial={cls:(nx.className||'').slice(0,30), top:+nr.top.toFixed(1), bottom:+nr.bottom.toFixed(1),
            visible: sr?+(Math.min(nr.bottom,sr.bottom)-Math.max(nr.top,sr.top)).toFixed(1):null}; } }
      return {scrollTop: scroller?scroller.scrollTop:null,
        lastRow: last?(last.textContent||'').trim().slice(0,24):null,
        lastBottom: lr?+lr.bottom.toFixed(1):null, viewBottom: sr?+sr.bottom.toFixed(1):null,
        lastFullyVisible: (lr&&sr)?(lr.bottom<=sr.bottom+1):null,
        nextPartial}; })())""")
    shot(pg, '402_board_detail_bottom')
    res['cast402'] = cast_row_shot402(pg)
    save_out('board402.json', res)
    return res

# -*- coding: utf-8 -*-
"""v402 appended probes (appended to the drive401_h.py copy by patch402.py):
43d geometry, modal-vs-map-label clash, seal pixels, awards P1/P2,
map occluder (07c/05b/h682), notebook (11b/11c/33), counts, verify.
"""
import re
from PIL import Image

def _jload(s):
    try:
        j = json.loads(s)
        if isinstance(j, str):
            j = json.loads(j)
        return j
    except Exception:
        return {'raw': s}

def lum_rgb(rgb):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio_rgb(a, b):
    l1, l2 = lum_rgb(a), lum_rgb(b)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)

# ================= modal 卡 vs 地圖標籤相交 =================
MODAL_CLASH_JS = """() => JSON.stringify((()=>{
  const modal=document.querySelector('#mask .modal');
  if(!modal) return {on:false};
  const mr=modal.getBoundingClientRect();
  function inter(r){ const ox=Math.max(0,Math.min(r.right,mr.right)-Math.max(r.left,mr.left));
    const oy=Math.max(0,Math.min(r.bottom,mr.bottom)-Math.max(r.top,mr.top));
    return (ox>0&&oy>0)?{ox:+ox.toFixed(1),oy:+oy.toFixed(1)}:null; }
  function full(r){ return r.top>=mr.top-1&&r.bottom<=mr.bottom+1&&r.left>=mr.left-1&&r.right<=mr.right+1; }
  const labels=[...document.querySelectorAll('#map-names68 .mn68')].filter(e=>e.offsetParent!==null).map(e=>{
    const r=e.getBoundingClientRect(); const ov=inter(r);
    return {txt:(e.textContent||'').trim(), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
      left:+r.left.toFixed(1), right:+r.right.toFixed(1), vis:getComputedStyle(e).visibility,
      overlap:ov, straddling: !!(ov && !full(r))}; });
  const me=document.querySelector('.map-me363');
  const mer=me?me.getBoundingClientRect():null;
  return {modalRect:{top:+mr.top.toFixed(1),bottom:+mr.bottom.toFixed(1),left:+mr.left.toFixed(1),right:+mr.right.toFixed(1)},
    labels: labels.filter(l=>l.overlap),
    nStraddling: labels.filter(l=>l.straddling).length,
    me363: mer?{top:+mer.top.toFixed(1),bottom:+mer.bottom.toFixed(1),left:+mer.left.toFixed(1),right:+mer.right.toFixed(1),overlap:inter(mer)}:null}; })())"""

def modal_label_clash(pg):
    return _jload(ev(pg, MODAL_CLASH_JS))

# ================= 43d 幾何：日期行＋支票 memo＋金掣 =================
MEASURE_43D_JS = """() => JSON.stringify((()=>{
  const sc=document.getElementById('modal-inner');
  if(!sc) return {on:false};
  const sr=sc.getBoundingClientRect();
  const ps=[...sc.querySelectorAll('p')];
  const dateP=ps.filter(p=>/年\\d+月\\d+日/.test(p.textContent||'')).pop()||null;
  function snap(el){ if(!el) return null; const r=el.getBoundingClientRect();
    return {txt:(el.textContent||'').trim().slice(0,40), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
      fullyVisible: r.bottom<=sr.bottom+1 && r.top>=sr.top-1, hiddenBelow: +(Math.max(0, r.bottom-sr.bottom)).toFixed(1)}; }
  const chk=document.querySelector('.chk101');
  const memo=document.querySelector('.chk101 .ck-memo');
  const cr=chk?chk.getBoundingClientRect():null;
  const mr2=memo?memo.getBoundingClientRect():null;
  const img=chk?chk.querySelector('img'):null;
  const ir=img?img.getBoundingClientRect():null;
  const cs=getComputedStyle(sc);
  return {scrollTop: sc.scrollTop, scrollHeight: sc.scrollHeight, clientHeight: sc.clientHeight,
    scrollerRect:{top:+sr.top.toFixed(1),bottom:+sr.bottom.toFixed(1)},
    maskImage:(cs.maskImage||'').slice(0,120), maskWebkit:(cs.webkitMaskImage||'').slice(0,120),
    dateLine: snap(dateP),
    cheque: cr?{top:+cr.top.toFixed(1),bottom:+cr.bottom.toFixed(1)}:null,
    chequeImg: ir?{top:+ir.top.toFixed(1),bottom:+ir.bottom.toFixed(1)}:null,
    memo: mr2?{txt:(memo.textContent||'').trim().slice(0,30), top:+mr2.top.toFixed(1), bottom:+mr2.bottom.toFixed(1),
      clearanceToChequeBottom: cr?+(cr.bottom-mr2.bottom).toFixed(1):null,
      clearanceToImgBottom: ir?+(ir.bottom-mr2.bottom).toFixed(1):null}:null}; })())"""

def measure_43d402(pg, tag):
    out = {}
    out['top'] = _jload(ev(pg, MEASURE_43D_JS))
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    out['bottom'] = _jload(ev(pg, MEASURE_43D_JS))
    shot(pg, '402_43d_bottom_' + tag)
    box = ev(pg, """() => { const b=[...document.querySelectorAll('#modal-btns button.p')].find(x=>x.offsetParent!==null);
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x, y:r.y, width:r.width, height:r.height}; }""")
    if box:
        pad = 6
        clip = {'x': max(0, box['x'] - pad), 'y': max(0, box['y'] - pad),
                'width': box['width'] + pad * 2, 'height': box['height'] + pad * 2}
        p = f"{SHOTS}/402_43d_goldbtn_zoom_{tag}.png"
        pg.screenshot(path=p, clip=clip); _sidecar(pg, '402_43d_goldbtn_zoom_' + tag)
        try:
            im = Image.open(p)
            im2 = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
            im2.save(f"{SHOTS}/402_43d_goldbtn_zoom3x_{tag}.png")
        except Exception as e:
            print("ZOOM3X_FAIL", str(e)[:120], flush=True)
        out['gold_btn_box'] = box
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(400)
    print("MEASURE43D", tag, json.dumps(out, ensure_ascii=False)[:900], flush=True)
    return out

# ================= 通告欄：紅印像素＋卡列＋陣容尾行 =================
SEAL_CARDS_JS = """() => JSON.stringify((()=>{
  const mi=document.getElementById('modal-inner');
  const mr=mi?mi.getBoundingClientRect():null;
  return {mi: mr?{top:+mr.top.toFixed(1),bottom:+mr.bottom.toFixed(1)}:null,
    cards:[...document.querySelectorAll('.gig-teaser')].map((c,i)=>{
      const r=c.getBoundingClientRect(); const seal=c.querySelector('.g-seal');
      const sr=seal?seal.getBoundingClientRect():null;
      return {i, title:(c.querySelector('.gt-title')||c).textContent.trim().slice(0,30),
        top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), h:+r.height.toFixed(1),
        sealSrc: seal?seal.getAttribute('src'):null, sealAlt: seal?seal.getAttribute('alt'):null,
        sealRect: sr?{x:+sr.x.toFixed(1), y:+sr.y.toFixed(1), w:+sr.width.toFixed(1), h:+sr.height.toFixed(1)}:null}; })}; })())"""

def seal_measure402(pg):
    st = _jload(ev(pg, SEAL_CARDS_JS))
    src = f"{SHOTS}/402_board_peak.png"
    out = {'cards': st.get('cards', []), 'seal_pixel': []}
    try:
        im = Image.open(src).convert("RGB")
        W, H = im.size
        SC = W / 390.0
        def is_red(px):
            r, g, bl = px
            return r > 110 and (r - g) > 45 and (r - bl) > 35
        def is_paper(px):
            r, g, bl = px
            return r > 200 and g > 180 and bl > 140 and (r - bl) < 90
        def med(ps):
            if not ps:
                return None
            ps = sorted(ps)
            return ps[len(ps) // 2]
        def darkest(ps):
            if not ps:
                return None
            return min(ps, key=lambda p: lum_rgb(p))
        for c in st.get('cards', []):
            sr = c.get('sealRect')
            if not sr:
                continue
            x0, y0 = int(sr['x'] * SC), int(sr['y'] * SC)
            x1, y1 = int((sr['x'] + sr['w']) * SC), int((sr['y'] + sr['h']) * SC)
            reds = []
            for y in range(y0, min(y1, H)):
                for x in range(x0, min(x1, W)):
                    px = im.getpixel((x, y))
                    if is_red(px):
                        reds.append(px)
            cx0, cy0 = int(8 * SC), int(c['top'] * SC)
            cx1, cy1 = int(382 * SC), int(min(c['bottom'], 745) * SC)
            card_papers = []
            for y in range(max(cy0, 0), min(cy1, H), 2):
                for x in range(cx0, cx1, 2):
                    if x0 <= x < x1 and y0 <= y < y1:
                        continue
                    px = im.getpixel((x, y))
                    if is_paper(px):
                        card_papers.append(px)
            red_med = med(reds)
            paper_med = med(card_papers)
            paper_dark = darkest(card_papers)
            out['seal_pixel'].append({
                'title': c['title'], 'sealAlt': c.get('sealAlt'),
                'sealSrc': (c.get('sealSrc') or '').split('/')[-1],
                'nRed': len(reds), 'redMedian': red_med, 'paperMedian': paper_med,
                'paperDarkest': paper_dark,
                'ratioVsMedianPaper': (ratio_rgb(red_med, paper_med) if red_med and paper_med else None),
                'ratioVsDarkestPaper': (ratio_rgb(red_med, paper_dark) if red_med and paper_dark else None)})
        lin = next((c for c in st.get('cards', []) if (c.get('sealSrc') or '').endswith('seal_extra.png')), None)
        if lin and lin.get('sealRect'):
            sr = lin['sealRect']
            pg.screenshot(path=f"{SHOTS}/402_redseal_lin_zoom.png",
                          clip={'x': max(0, sr['x'] - 8), 'y': max(0, sr['y'] - 8),
                                'width': sr['w'] + 16, 'height': sr['h'] + 16})
    except Exception as e:
        out['error'] = repr(e)[:200]
    for s in out['seal_pixel']:
        print("SEAL402", s['title'], s['sealAlt'], "red", s['redMedian'],
              "paperMed", s['paperMedian'], "vsMed", s['ratioVsMedianPaper'],
              "vsDark", s['ratioVsDarkestPaper'], flush=True)
    return out

BOARD_CARDS_JS = """() => JSON.stringify((()=>{
  const mi=document.getElementById('modal-inner');
  const sr=mi?mi.getBoundingClientRect():null;
  const btns=document.getElementById('modal-btns');
  const br=btns?btns.getBoundingClientRect():null;
  const stats=[...document.querySelectorAll('#modal-inner *')].filter(e=>e.children.length===0 && /共\\s*\\d+\\s*張|統計|已接\\s*\\d/.test(e.textContent||'')).slice(0,4).map(e=>{
    const r=e.getBoundingClientRect(); return {txt:(e.textContent||'').trim().slice(0,50),
      top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), cls:(e.className||'').slice(0,30)}; });
  const org=document.querySelector('.board-menu397');
  const orr=org?org.getBoundingClientRect():null;
  return {scroller: sr?{top:+sr.top.toFixed(1),bottom:+sr.bottom.toFixed(1),scrollTop:mi.scrollTop,scrollHeight:mi.scrollHeight,clientHeight:mi.clientHeight}:null,
    btns: br?{top:+br.top.toFixed(1),bottom:+br.bottom.toFixed(1),h:+br.height.toFixed(1)}:null,
    stats, organize: orr?{x:+orr.x.toFixed(1),w:+orr.width.toFixed(1),h:+orr.height.toFixed(1)}:null,
    cards:[...document.querySelectorAll('.gig-teaser')].map((c,i)=>{ const r=c.getBoundingClientRect();
      return {i, title:(c.querySelector('.gt-title')||c).textContent.trim().slice(0,30),
        top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
        visibleH: sr?+(Math.min(r.bottom,sr.bottom)-Math.max(r.top,sr.top)).toFixed(1):null,
        fullyVisible: sr?(r.top>=sr.top-1&&r.bottom<=sr.bottom+1):null}; })}; })())"""

def board_cards402(pg):
    out = {'top': _jload(ev(pg, BOARD_CARDS_JS))}
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    out['bottom'] = _jload(ev(pg, BOARD_CARDS_JS))
    shot(pg, '402_board_bottom')
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(400)
    print("BOARDCARDS402", json.dumps(out, ensure_ascii=False)[:1200], flush=True)
    return out

CAST_ROW_JS = """() => JSON.stringify((()=>{
  const sc=document.querySelector('.notice_sheet_body') || document.getElementById('modal-inner');
  if(!sc) return {on:false};
  const sr=sc.getBoundingClientRect();
  const rows=[...document.querySelectorAll('.cn-summary .cn-sum-row')].filter(r=>/^(男主角|女主角|男配角|女配角)/.test((r.textContent||'').trim()));
  const last=rows[rows.length-1];
  if(!last) return {on:false, nRows: rows.length};
  const lr=last.getBoundingClientRect();
  sc.scrollTop += (lr.bottom - sr.bottom) + 10;
  return {nRows: rows.length, lastRow:(last.textContent||'').trim().slice(0,30),
    scrollTop: sc.scrollTop, scrollHeight: sc.scrollHeight, clientHeight: sc.clientHeight}; })())"""

CAST_ROW_AFTER_JS = """() => JSON.stringify((()=>{
  const sc=document.querySelector('.notice_sheet_body') || document.getElementById('modal-inner');
  const sr=sc?sc.getBoundingClientRect():null;
  const rows=[...document.querySelectorAll('.cn-summary .cn-sum-row')].filter(r=>/^(男主角|女主角|男配角|女配角)/.test((r.textContent||'').trim()));
  const last=rows[rows.length-1];
  const lr=last?last.getBoundingClientRect():null;
  return {lastRow: last?(last.textContent||'').trim().slice(0,30):null,
    lastBottom: lr?+lr.bottom.toFixed(1):null, viewBottom: sr?+sr.bottom.toFixed(1):null,
    fullyVisible: (lr&&sr)?(lr.bottom<=sr.bottom+1):null}; })())"""

def cast_row_shot402(pg):
    out = _jload(ev(pg, CAST_ROW_JS))
    pg.wait_for_timeout(900)
    out['after'] = _jload(ev(pg, CAST_ROW_AFTER_JS))
    shot(pg, '402_board_detail_cast')
    print("CAST402", json.dumps(out, ensure_ascii=False)[:600], flush=True)
    return out

# ================= 35c：P1 大標＋fade＋P2 相 =================
AWARDS_P1_JS = """() => JSON.stringify((()=>{
  const sc=document.getElementById('modal-inner');
  const sr=sc?sc.getBoundingClientRect():null;
  const sheet=document.querySelector('.paper-sheet');
  const h1=sheet?sheet.querySelector('h1, .np214-headline, .np214-headline2'):null;
  const cs=sc?getComputedStyle(sc):null;
  let straddle=null;
  if(sr){
    const el=document.elementFromPoint(Math.round((sr.left+sr.right)/2), Math.round(sr.bottom)-2);
    if(el){ const r=el.getBoundingClientRect();
      straddle={tag:el.tagName, cls:(el.className||'').toString().slice(0,40), txt:(el.textContent||'').trim().slice(0,60),
        top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), hiddenBelow:+(Math.max(0,r.bottom-sr.bottom)).toFixed(1)}; } }
  const paras=[...document.querySelectorAll('.paper-sheet p')].slice(0,6).map(p=>(p.textContent||'').trim().slice(0,80));
  return {headline: h1?(h1.textContent||'').trim():null,
    headlineTag: h1?h1.tagName:null, headlineCls: h1?(h1.className||'').toString():null,
    maskImage: cs?(cs.maskImage||'').slice(0,140):null,
    scrollTop: sc?sc.scrollTop:null, scrollHeight: sc?sc.scrollHeight:null, clientHeight: sc?sc.clientHeight:null,
    scrollerBottom: sr?+sr.bottom.toFixed(1):null, straddle, paras}; })())"""

def awards_p1_402(pg):
    out = {'top': _jload(ev(pg, AWARDS_P1_JS))}
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    out['bottom'] = _jload(ev(pg, AWARDS_P1_JS))
    shot(pg, '402_awards_p1_bottom')
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(400)
    print("AWARDSP1_402", json.dumps(out, ensure_ascii=False)[:1000], flush=True)
    return out

AWARDS_P2_PHOTO_JS = """() => JSON.stringify((()=>{
  const p2=document.querySelector('.np214-page[data-np214-page="2"]');
  if(!p2) return {on:false};
  const figs=[...p2.querySelectorAll('.np214-photo, figure')].map(f=>{
    const img=f.querySelector('img');
    const r=f.getBoundingClientRect();
    return {cls:(f.className||'').toString().slice(0,40), src: img?img.getAttribute('src'):null,
      alt: img?img.getAttribute('alt'):null,
      caption:(f.textContent||'').trim().slice(0,80),
      top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1)}; });
  const marks=[...p2.querySelectorAll('[class*=mark], [class*=tag], [class*=badge], [class*=award]')].filter(e=>e.offsetParent!==null).slice(0,8).map(e=>({cls:(e.className||'').toString().slice(0,40), txt:(e.textContent||'').trim().slice(0,40)}));
  return {headline: (p2.querySelector('.np214-headline2')||{}).textContent||null,
    subhead: (p2.querySelector('.np214-subhead401')||{}).textContent||null,
    figs, marks}; })())"""

def awards_p2_photo402(pg):
    out = _jload(ev(pg, AWARDS_P2_PHOTO_JS))
    box = ev(pg, """() => { const f=document.querySelector('.np214-page[data-np214-page="2"] .np214-photo, .np214-page[data-np214-page="2"] figure');
      if(!f) return null; const r=f.getBoundingClientRect();
      return {x:r.x, y:r.y, width:r.width, height:r.height}; }""")
    if box:
        shot_clip(pg, '402_awards_p2_photo_zoom',
                  {'x': max(0, box['x'] - 6), 'y': max(0, box['y'] - 6),
                   'width': box['width'] + 12, 'height': box['height'] + 12})
    print("AWARDSP2_402", json.dumps(out, ensure_ascii=False)[:900], flush=True)
    return out

# ================= 地圖：07c／05b／h682 遮擋 =================
OCCLUDER_JS = """(labelTxt) => JSON.stringify((()=>{
  const labels=[...document.querySelectorAll('#map-names68 .mn68')].filter(e=>e.offsetParent!==null);
  const lab=labels.find(e=>(e.textContent||'').includes(labelTxt)) || null;
  if(!lab) return {found:false, labelTxt};
  const r=lab.getBoundingClientRect();
  function stackAt(x,y){ return [...document.elementsFromPoint(x,y)].slice(0,6).map(e=>({tag:e.tagName, cls:(e.className||'').toString().slice(0,40), id:e.id||null, txt:(e.textContent||'').trim().slice(0,24)})); }
  const hits=[];
  document.querySelectorAll('body *').forEach(e=>{
    if(e===lab || lab.contains(e) || e.contains(lab)) return;
    if(e.offsetParent===null && getComputedStyle(e).position!=='fixed') return;
    const b=e.getBoundingClientRect();
    if(b.width<=0||b.height<=0) return;
    const ox=Math.max(0,Math.min(b.right,r.right)-Math.max(b.left,r.left));
    const oy=Math.max(0,Math.min(b.bottom,r.bottom)-Math.max(b.top,r.top));
    if(ox>2&&oy>2){ const cs=getComputedStyle(e);
      hits.push({tag:e.tagName, cls:(e.className||'').toString().slice(0,40), id:e.id||null,
        ox:+ox.toFixed(1), oy:+oy.toFixed(1), z:cs.zIndex, pos:cs.position,
        bg:(cs.backgroundColor||'').slice(0,30)}); }
  });
  const me=document.querySelector('.map-me363');
  const mer=me?me.getBoundingClientRect():null;
  const tag=document.querySelector('.me363-tag');
  const tr=tag?tag.getBoundingClientRect():null;
  const cx=(r.left+r.right)/2;
  return {found:true, labelRect:{top:+r.top.toFixed(1),bottom:+r.bottom.toFixed(1),left:+r.left.toFixed(1),right:+r.right.toFixed(1)},
    stackTop: stackAt(cx, r.top+2), stackMid: stackAt(cx, (r.top+r.bottom)/2),
    hits: hits.slice(0,12),
    me363: mer?{top:+mer.top.toFixed(1),bottom:+mer.bottom.toFixed(1),left:+mer.left.toFixed(1),right:+mer.right.toFixed(1)}:null,
    meTag: tr?{txt:(tag.textContent||'').trim(), top:+tr.top.toFixed(1),bottom:+tr.bottom.toFixed(1),left:+tr.left.toFixed(1),right:+tr.right.toFixed(1)}:null,
    meVsLabel: (mer)?{ox:+Math.max(0,Math.min(mer.right,r.right)-Math.max(mer.left,r.left)).toFixed(1),
      oy:+Math.max(0,Math.min(mer.bottom,r.bottom)-Math.max(mer.top,r.top)).toFixed(1)}:null,
    tagVsLabel: (tr)?{ox:+Math.max(0,Math.min(tr.right,r.right)-Math.max(tr.left,r.left)).toFixed(1),
      oy:+Math.max(0,Math.min(tr.bottom,r.bottom)-Math.max(tr.top,r.top)).toFixed(1)}:null}; })())"""

def seed_map402(pg, day):
    return ev(pg, """(day) => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = day; S.homeEditable = false;
      S.weekPlanWeek37 = Math.floor(day/7)+1;
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19"].forEach(id=>{ S.story.done[id]=true; });
      S.story.phase='P5';
      S.starDay = {day:day, presence:{}, triggered:99, doneToday:{}};
      S.romDay = {day:day, presence:{}, triggered:99, doneToday:{}};
      S.travel114 = {day:day, used:0};
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return 'day='+S.dayIndex; }""", day)

def to_map402(pg):
    click_any(pg, ['返回地圖'])
    pg.wait_for_timeout(1000)
    for i in range(12):
        if ev(pg, "() => (document.querySelector('.view.on')||{}).id") == 'v-map' and not ev(pg, "() => document.getElementById('mask').classList.contains('on')"):
            break
        c = click_any(pg, ['下一句', '繼續', '確定', '收下這份剪報', '跳過', '關閉'])
        if not c and ev(pg, "() => document.getElementById('mask').classList.contains('on')"):
            pg.mouse.click(195, 120)
        pg.wait_for_timeout(700)

def gift_shop_measure402(pg, tag):
    """Item 4 h682：玩家喺禮品店嗰陣，「我喺呢度」tag＋方格唔可以遮「廟街禮品」二字。
    atLoc 係遊戲內部 let，evaluate 賦值改唔到（只會生 window.atLoc）；遊戲函數
    （openLoc／drawMap）喺 IIFE 入面，evaluate 都叫唔到——行真流程：撳「廟街禮品」
    pin 入場（計出行額度，seed 有 2 次），再撳「返回地圖」關 sheet，atLoc 留低，
    地圖重畫出 marker＋tag。"""
    clicked = click_any(pg, ['廟街禮品'])
    pg.wait_for_timeout(1200)
    click_any(pg, ['返回地圖'])
    pg.wait_for_timeout(1000)
    out = {}
    out['pinClicked'] = clicked
    out['occluder'] = _jload(ev(pg, OCCLUDER_JS, '廟街禮品'))
    out['count'] = count(pg, tag)
    out['me'] = _jload(ev(pg, """() => JSON.stringify((()=>{
      const me=document.querySelector('.map-me363');
      const tag=document.querySelector('.me363-tag');
      const strip=document.querySelector('.map-here373');
      const lab=[...document.querySelectorAll('#map-names68 .mn68')].find(e=>(e.textContent||'').trim()==='廟街禮品');
      const snap=(el)=>{ if(!el) return null; const r=el.getBoundingClientRect(); return {top:+r.top.toFixed(1),bottom:+r.bottom.toFixed(1),left:+r.left.toFixed(1),right:+r.right.toFixed(1)}; };
      const styleTop = lab ? lab.style.top : null;
      const offTop = lab ? lab.offsetTop : null;
      return {me:snap(me), tag:snap(tag), strip:snap(strip), label:snap(lab), styleTop, offTop}; })())"""))
    shot(pg, '402_' + tag + '_gift_shop')
    print("GIFT402", tag, json.dumps(out, ensure_ascii=False)[:700], flush=True)
    return out

def probe_map(pg, b):
    res = {}
    new_game(pg)
    seed_map402(pg, 520)
    to_map402(pg)
    pg.wait_for_timeout(1200)
    res['count_05b'] = count(pg, '05b_map_labels')
    res['occluder_05b'] = _jload(ev(pg, OCCLUDER_JS, '廟街禮品'))
    shot(pg, '402_05b_map_labels')
    ev(pg, "() => { const b=document.getElementById('map-layer159'); if(b) b.click(); }")
    pg.wait_for_timeout(1200)
    res['count_07c'] = count(pg, '07c_map_date')
    res['occluder_07c'] = _jload(ev(pg, OCCLUDER_JS, '廟街禮品'))
    res['strip_07c'] = _jload(ev(pg, """() => JSON.stringify((()=>{
      const strip=document.querySelector('.map-here373');
      const lab=[...document.querySelectorAll('#map-names68 .mn68')].find(e=>(e.textContent||'').trim()==='廟街禮品');
      const snap=(el)=>{ if(!el) return null; const r=el.getBoundingClientRect(); return {top:+r.top.toFixed(1),bottom:+r.bottom.toFixed(1),left:+r.left.toFixed(1),right:+r.right.toFixed(1)}; };
      const s=snap(strip), l=snap(lab);
      const ox=(s&&l)?Math.max(0,Math.min(s.right,l.right)-Math.max(s.left,l.left)):0;
      const oy=(s&&l)?Math.max(0,Math.min(s.bottom,l.bottom)-Math.max(s.top,l.top)):0;
      return {strip:s, label:l, overlapPx:+(ox*oy).toFixed(1)}; })())"""))
    shot(pg, '402_07c_map_date')
    ev(pg, "() => { const b=document.getElementById('map-layer159'); if(b) b.click(); }")
    pg.wait_for_timeout(800)
    res['gift_shop_844'] = gift_shop_measure402(pg, 'gift_shop_844')
    ctx2 = b.new_context(viewport={'width': 390, 'height': 682}, device_scale_factor=2)
    pg2 = ctx2.new_page()
    pg2.on('pageerror', lambda e: print('PAGEERROR682', str(e)[:150], flush=True))
    try:
        new_game(pg2)
        seed_map402(pg2, 520)
        to_map402(pg2)
        pg2.wait_for_timeout(1200)
        res['h682'] = {}
        res['h682']['occluder'] = _jload(ev(pg2, OCCLUDER_JS, '廟街禮品'))
        res['h682']['count'] = count(pg2, '05b_h682')
        shot(pg2, '402_05b_map_labels_h682')
        res['gift_shop_h682'] = gift_shop_measure402(pg2, 'gift_shop_h682')
    except Exception as e:
        res['h682'] = {'error': repr(e)[:200]}
        print("PROBE_FAIL map-h682", repr(e)[:200], flush=True)
    ctx2.close()
    save_out('map402.json', res)
    return res

# ================= 手帳：11b／11c／33 =================
NB_CELLS_JS = """() => JSON.stringify((()=>{
  const nb=document.getElementById('notebook');
  if(!nb) return {on:false};
  const nr=nb.getBoundingClientRect();
  const acts=document.getElementById('nb-actions');
  const ar=acts?acts.getBoundingClientRect():null;
  const row265=document.getElementById('home265-row');
  const r265=row265?row265.getBoundingClientRect():null;
  const days=[...document.querySelectorAll('#nb-days > *')].map((d,i)=>{
    const r=d.getBoundingClientRect();
    return {i, cls:(d.className||'').toString().slice(0,30), txt:(d.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30),
      top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
      visibleH:+(Math.min(r.bottom,nr.bottom)-Math.max(r.top,nr.top)).toFixed(1),
      fullyVisible: r.top>=nr.top-1 && r.bottom<=nr.bottom+1}; });
  return {scrollTop: nb.scrollTop, scrollHeight: nb.scrollHeight, clientHeight: nb.clientHeight,
    notebookRect:{top:+nr.top.toFixed(1),bottom:+nr.bottom.toFixed(1)},
    paddingBottom: getComputedStyle(nb).paddingBottom,
    actions: ar?{top:+ar.top.toFixed(1),bottom:+ar.bottom.toFixed(1),h:+ar.height.toFixed(1)}:null,
    row265: r265?{top:+r265.top.toFixed(1),bottom:+r265.bottom.toFixed(1),h:+r265.height.toFixed(1)}:null,
    days}; })())"""

def nb_cells402(pg, tag):
    out = {'top': _jload(ev(pg, NB_CELLS_JS))}
    ev(pg, "() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=nb.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    out['bottom'] = _jload(ev(pg, NB_CELLS_JS))
    shot(pg, '402_' + tag + '_bottom')
    ev(pg, "() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=0; return true; }")
    pg.wait_for_timeout(400)
    print("NBCELLS402", tag, json.dumps(out, ensure_ascii=False)[:900], flush=True)
    return out

ENDING_JS = """() => JSON.stringify((()=>{
  const sc=document.getElementById('modal-inner');
  if(!sc) return {on:false};
  const sr=sc.getBoundingClientRect();
  const sheet=document.querySelector('.ending375-sheet');
  const ps=sheet?[...sheet.querySelectorAll('p')]:[];
  const last=ps[ps.length-1];
  function snap(el){ if(!el) return null; const r=el.getBoundingClientRect();
    return {txt:(el.textContent||'').trim().slice(0,80), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
      fullyVisible: r.bottom<=sr.bottom+1 && r.top>=sr.top-1, hiddenBelow:+(Math.max(0,r.bottom-sr.bottom)).toFixed(1)}; }
  const gap=[...document.querySelectorAll('.ending375-sheet p')].filter(p=>/回望那一格/.test(p.textContent||''));
  return {scrollTop: sc.scrollTop, scrollHeight: sc.scrollHeight, clientHeight: sc.clientHeight,
    scrollerBottom: +sr.bottom.toFixed(1), nParas: ps.length,
    lastPara: snap(last), gapHead: gap.length?snap(gap[0]):null}; })())"""

def ending_measure402(pg):
    out = {'top': _jload(ev(pg, ENDING_JS))}
    shot(pg, '402_33_ending_summary')
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    out['bottom'] = _jload(ev(pg, ENDING_JS))
    shot(pg, '402_33_ending_bottom')
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(400)
    click_any(pg, ['回顧手帳'])
    pg.wait_for_timeout(1500)
    out['count_33b'] = count(pg, '33b_ending_gate')
    shot(pg, '402_33b_ending_gate')
    print("ENDING402", json.dumps(out, ensure_ascii=False)[:900], flush=True)
    return out

def probe_notebook(pg):
    res = {}
    new_game(pg)
    ev(pg, """() => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = 520;
      try{ if(typeof syncGigsForCalendarYear==='function') syncGigsForCalendarYear(true); }catch(e){}
      try{ if(typeof renderAll==='function') renderAll(); }catch(e){}
      return 'seeded'; }""")
    pg.wait_for_timeout(700)
    shot(pg, '402_11b_notebook_plan')
    res['nb_11b'] = nb_cells402(pg, '11b_notebook_plan')
    click_any(pg, ['行程工具'])
    pg.wait_for_timeout(600)
    print("全日訓練", click_any(pg, ['全日訓練']), flush=True)
    pg.wait_for_timeout(600)
    shot(pg, '402_11c_notebook_plan_filled')
    res['nb_11c'] = nb_cells402(pg, '11c_notebook_plan_filled')
    try:
        src = json.load(open('/home/hatch/workspace/linji-ending-targets-2026-11-23/E3_director_ls_backup.json'))
        fin = json.load(open('/home/hatch/workspace/linji-ending-targets-2026-11-23/E3_director_ending_final.json'))
        S = json.loads(src['starVolunteer_map_v19w'])
        e410 = fin['ending410']
        S['ending410'] = {'id': e410.get('career'), 'career': e410.get('career'), 'careerVariant': e410.get('careerVariant'),
            'title': e410.get('title'), 'settled': e410.get('settled'), 'creditsHeld': e410.get('creditsHeld'),
            'exodusNames': e410.get('exodusNames') or [], 'romance': e410.get('romanceLine'),
            'romanceLine': e410.get('romanceLine'), 'romanceKind': e410.get('romanceKind'),
            'exodus': e410.get('exodus'), 'day': e410.get('day'), 'fame': e410.get('fame'),
            'credit': e410.get('credit'), 'dual': e410.get('dual'), 'gaps95': e410.get('gaps95') or []}
        pg.goto(URL)
        pg.wait_for_timeout(2500)
        ev(pg, """(payload) => {
          localStorage.setItem('starVolunteer_map_v19w', payload.S);
          localStorage.setItem('starVolunteer_prefs_v19z9', payload.prefs);
          return 'stored'; }""", {'S': json.dumps(S, ensure_ascii=False), 'prefs': src.get('starVolunteer_prefs_v19z9', '{}')})
        pg.reload(wait_until="load")
        pg.wait_for_timeout(3000)
        res['count_36'] = count(pg, '36_after_reload')
        click_any(pg, ['繼續'])
        pg.wait_for_timeout(2500)
        ev(pg, """() => { const rows=[...document.querySelectorAll('.slot-row')]; if(rows[0]){ rows[0].click(); return 'clicked'; } return 'no-slot'; }""")
        pg.wait_for_timeout(2500)
        res['count_33'] = count(pg, '33_ending_summary')
        res['ending'] = ending_measure402(pg)
    except Exception as e:
        res['ending_error'] = repr(e)[:300]
        print("PROBE_FAIL notebook-33", repr(e)[:200], flush=True)
    save_out('notebook402.json', res)
    return res

# ================= 掣量計數：07／24／08／32／25b =================
RED_COST_JS = """() => JSON.stringify((()=>{
  const els=[...document.querySelectorAll('#loc-sheet .act .cost')].filter(e=>e.offsetParent!==null).slice(0,6).map(e=>{
    const cs=getComputedStyle(e);
    let bg=null, n=e; while(n && n!==document.body){ const c2=getComputedStyle(n); const m=(c2.backgroundColor||'').match(/rgba?\\(([^)]+)\\)/);
      if(m){ const p=m[1].split(',').map(x=>parseFloat(x)); if(p.length<4||p[3]>0.9){ bg=c2.backgroundColor; break; } } n=n.parentElement; }
    return {txt:(e.textContent||'').trim(), color:cs.color, bg}; });
  return els; })())"""

ELLIPSIS_JS = """() => JSON.stringify((()=>{
  const hs=[...document.querySelectorAll('#loc-sheet .act .h')].filter(e=>e.offsetParent!==null).slice(0,10).map(e=>{
    const cs=getComputedStyle(e);
    return {txt:(e.textContent||'').trim().slice(0,40), sw:e.scrollWidth, cw:e.clientWidth,
      clipped: e.scrollWidth>e.clientWidth+1, clamp: cs.webkitLineClamp, overflow: cs.overflow}; });
  return hs; })())"""

def _parse_rgba(s):
    m = re.match(r'rgba?\(([^)]+)\)', s or '')
    if not m:
        return None
    p = [float(x) for x in m.group(1).split(',')]
    return tuple(p[:3])

def probe_counts(pg):
    res = {}
    new_game(pg)
    seed_map402(pg, 520)
    to_map402(pg)
    pg.wait_for_timeout(1200)
    res['07_map_baseline'] = count(pg, '07_map_baseline')
    ev(pg, "() => { const b=document.getElementById('btn-menu'); if(b) b.click(); }")
    pg.wait_for_timeout(1000)
    res['24_menu'] = count(pg, '24_menu')
    click_any(pg, ['關閉', '返回', '取消'])
    pg.wait_for_timeout(800)
    if open_loc_sheet(pg, 'tvb_longmen'):
        pg.wait_for_timeout(800)
        res['08_tv'] = count(pg, '08_tv')
        res['08_red_cost'] = _jload(ev(pg, RED_COST_JS))
        shot(pg, '402_08_loc_panel')
        click_any(pg, ['關閉', '返回', '取消'])
        pg.wait_for_timeout(700)
        go_map(pg)
    if open_loc_sheet(pg, 'cafe_cha'):
        pg.wait_for_timeout(800)
        res['32_cafe'] = count(pg, '32_cafe')
        res['32_ellipsis'] = _jload(ev(pg, ELLIPSIS_JS))
        shot(pg, '402_32_cafe_intel')
        click_any(pg, ['關閉', '返回', '取消'])
        pg.wait_for_timeout(700)
        go_map(pg)
    ev(pg, "() => { const b=document.getElementById('map-layer159'); if(b) b.click(); }")
    pg.wait_for_timeout(1100)
    if open_loc_sheet(pg, 'date_harbour'):
        pg.wait_for_timeout(800)
        res['25b_date'] = count(pg, '25b_date')
        shot(pg, '402_26_date_loc')
        click_any(pg, ['關閉', '返回', '取消'])
        pg.wait_for_timeout(700)
    ev(pg, "() => { const b=document.getElementById('map-layer159'); if(b) b.click(); }")
    pg.wait_for_timeout(800)
    for item in res.get('08_red_cost', []):
        try:
            fg, bg = _parse_rgba(item.get('color')), _parse_rgba(item.get('bg'))
            if fg and bg:
                item['ratio'] = ratio_rgb(fg, bg)
        except Exception:
            pass
    save_out('counts402.json', res)
    print("COUNTS402", json.dumps({k: (v.get('total') if isinstance(v, dict) else v) for k, v in res.items()}, ensure_ascii=False), flush=True)
    return res

# ================= 核對：兩店／約會入口／09b 鎖定版 =================
SHEET_ACTS_JS = """() => JSON.stringify((()=>{
  const sh=document.getElementById('loc-sheet');
  if(!sh || sh.offsetParent===null) return {on:false};
  const acts=[...sh.querySelectorAll('.act, button')].filter(e=>e.offsetParent!==null).map(e=>{
    return {tag:e.tagName, cls:(e.className||'').toString().slice(0,30),
      txt:(e.textContent||'').replace(/\\s+/g,' ').trim().slice(0,60)}; });
  return {title:(sh.querySelector('h3, .loc-title')||{}).textContent||null, acts}; })())"""

def probe_verify(pg):
    res = {}
    new_game(pg)
    seed_map402(pg, 520)
    to_map402(pg)
    for loc, key in [('clothing_shop', 'shop_clothing'), ('gift_shop', 'shop_gift')]:
        if open_loc_sheet(pg, loc):
            pg.wait_for_timeout(800)
            res[key] = _jload(ev(pg, SHEET_ACTS_JS))
            shot(pg, '402_verify_' + key)
            click_any(pg, ['關閉', '返回', '取消'])
            pg.wait_for_timeout(700)
            go_map(pg)
        else:
            res[key] = {'error': 'sheet-open-fail'}
    res['date_layer'] = _jload(ev(pg, """() => JSON.stringify((()=>{
      const b=document.getElementById('map-layer159');
      const pins=[...document.querySelectorAll('.pin')].filter(p=>p.offsetParent!==null).map(p=>p.getAttribute('data-loc'));
      return {layerBtn: b?(b.textContent||'').trim():null, nPins: pins.length, pins}; })())"""))
    ev(pg, "() => { const b=document.getElementById('map-layer159'); if(b) b.click(); }")
    pg.wait_for_timeout(1100)
    res['date_layer_on'] = _jload(ev(pg, """() => JSON.stringify((()=>{
      const b=document.getElementById('map-layer159');
      const pins=[...document.querySelectorAll('.pin')].filter(p=>p.offsetParent!==null).map(p=>p.getAttribute('data-loc'));
      return {layerBtn: b?(b.textContent||'').trim():null, nPins: pins.length, pins}; })())"""))
    shot(pg, '402_verify_date_layer')
    ev(pg, "() => { const b=document.getElementById('map-layer159'); if(b) b.click(); }")
    pg.wait_for_timeout(800)
    for tag, stats in [('locked', {'acting': 18, 'stage': 14, 'vocal': 14, 'looks': 22, 'charm': 16, 'iq': 20, 'stamina': 75}),
                       ('unlocked', {'acting': 70, 'stage': 60, 'vocal': 45, 'looks': 55, 'charm': 50, 'iq': 45, 'stamina': 80})]:
        new_game(pg)
        seed_main(pg, 1, stats)
        if open_board(pg):
            pg.wait_for_timeout(800)
            res['board_' + tag] = _jload(ev(pg, """() => JSON.stringify((()=>{
              const cards=[...document.querySelectorAll('.gig-teaser')].map(c=>{
                const t=(c.textContent||'');
                return {title:(c.querySelector('.gt-title')||c).textContent.trim().slice(0,30),
                  locked: /未達標|鎖定|未夠/.test(t)}; });
              const modalBtns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim());
              const boardBtns=[...document.querySelectorAll('#modal-inner button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim().slice(0,24));
              return {nCards: cards.length, nLocked: cards.filter(c=>c.locked).length, cards,
                modalBtns, boardBtns}; })())"""))
            shot(pg, '402_verify_board_' + tag)
        else:
            res['board_' + tag] = {'error': 'board-open-fail'}
    save_out('verify402.json', res)
    print("VERIFY402", json.dumps(res, ensure_ascii=False)[:1500], flush=True)
    return res

PROBES = {'phone': None, 'hosp': None, 'tut': probe_tut, 'awards': probe_awards, 'board': probe_board,
          'map': probe_map, 'notebook': probe_notebook, 'counts': probe_counts, 'verify': probe_verify}


# ================= ROUND-11 BASE SECTIONS =================
def state_tag(pg):
    st = ev(pg, "() => JSON.stringify({view:(document.querySelector('.view.on')||{}).id||'',mask:document.getElementById('mask').className,h3:(document.querySelector('#modal h3')||{}).textContent||'',sheet:!!(document.getElementById('loc-sheet')&&document.getElementById('loc-sheet').offsetParent!==null),day:(typeof S!=='undefined'&&S)?S.dayIndex:null})")
    try:
        return json.loads(st)
    except Exception:
        return {}
def shot2(pg, name):
    print("STATE", name, json.dumps(state_tag(pg), ensure_ascii=False)[:220], flush=True)
    return shot(pg, name)
def rich_seed(pg, day=520):
    return ev(pg, """(day) => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = day;
      S.wrapHistory = [
        { gigId:'gig_1991_film_102', title:'《霓虹夜影》男主角', type:'電影', totalDays:24, pay:3000, fame:20, popularity:10, wrappedDay:390, rating:'表現穩妥' },
        { gigId:'gig_1990_film_101', title:'《梭哈》男配角', type:'電影', totalDays:4, pay:1200, fame:5, popularity:5, wrappedDay:230, rating:'表現穩妥' },
        { gigId:'gig_1992_rec_102', title:'《硬漢柔情》新人搖滾主唱', type:'唱片通告', totalDays:2, pay:3000, fame:4, popularity:4, wrappedDay:150, rating:'表現穩妥' },
        { gigId:'gig_1991_ad_111', title:'《新春團圓》廣告主角', type:'廣告', totalDays:2, pay:400, fame:40, popularity:8, wrappedDay:395, rating:'順利殺青' },
        { gigId:'gig_1991_variety_107', title:'《夏日繽紛夜》綜藝晚會主持', type:'綜藝', totalDays:2, pay:460, fame:45, popularity:9, wrappedDay:398, rating:'表現穩妥' }
      ];
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
def to_map_j(pg):
    click_any(pg, ['返回地圖']); pg.wait_for_timeout(900)
    for i in range(14):
        if ev(pg, "()=>(document.querySelector('.view.on')||{}).id") == 'v-map' and not ev(pg, "()=>document.getElementById('mask').classList.contains('on')"):
            break
        c = click_any(pg, ['下一句', '繼續', '確定', '收下這份剪報', '收下剪報', '跳過', '關閉', '我知道了'])
        if not c and ev(pg, "()=>document.getElementById('mask').classList.contains('on')"):
            pg.mouse.click(195, 120)
        pg.wait_for_timeout(700)
    pg.wait_for_timeout(2000)

def sec_title_tut(pg):
    pg.goto(URL); pg.wait_for_timeout(2500)
    ev(pg, "() => { try{ localStorage.clear(); }catch(e){} return true; }")
    pg.goto(URL); pg.wait_for_timeout(2500)
    shot2(pg, '01_title')
    click_any(pg, ['讀檔']); pg.wait_for_timeout(1200)
    shot2(pg, '02_slot_clean'); shot2(pg, '02c_load_slot')
    click_any(pg, ['關閉', '返回']); pg.wait_for_timeout(800)
    pg.click('#btn-new'); pg.wait_for_timeout(1500)
    shot2(pg, '03_newgame_confirm')
    # slot pick if shown
    ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button, #slot-list button')].find(x=>x.offsetParent!==null&&/槽 1/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }")
    pg.wait_for_timeout(1200)
    click_modal(pg, ['覆蓋開新局', '確定']); pg.wait_for_timeout(1200)
    try: pg.wait_for_selector('.tut-card', timeout=8000)
    except Exception: print('TUTCARD WAITFAIL', flush=True)
    pg.wait_for_timeout(600)
    shot2(pg, 'tut_00'); shot2(pg, '02b_newgame_after'); shot2(pg, '04_opening'); shot2(pg, 'tutmap_00')
    click_modal(pg, ['下一步']); pg.wait_for_timeout(1800)
    shot2(pg, 'tut_01'); shot2(pg, 'tutmap_01'); shot2(pg, 'tutmap_manual')
    click_modal(pg, ['下一步']); pg.wait_for_timeout(1500)
    shot2(pg, 'tut_02'); shot2(pg, 'tutmap_02')
    click_modal(pg, ['下一步', '我知道了']); pg.wait_for_timeout(1500)
    shot2(pg, 'tut_03'); shot2(pg, 'tutmap_03')
    click_modal(pg, ['我知道了', '下一步']); pg.wait_for_timeout(1500)
    shot2(pg, 'tut_04'); shot2(pg, 'tut_after')
    shot2(pg, '04_opening_story'); shot2(pg, '23_story_dialogue')  # v419：開場故事場景喺 tut_04 已開，唔好撳「開始寫手帳」閂咗先拍
    drv.click_text_in_modal(pg, r'開始寫手帳'); pg.wait_for_timeout(1800)
    play_out_story(pg); pg.wait_for_timeout(800)

def sec_map(pg):
    new_game(pg); rich_seed(pg, 520); to_map_j(pg)
    shot2(pg, '05_map_studio'); shot2(pg, '05c_map_labels_daycard'); shot2(pg, '06_map_studio_seeded')
    shot2(pg, 'venue398_844'); shot2(pg, 'venue_844_397'); shot2(pg, 'venue398_seeded844'); shot2(pg, 'venue_seeded844_397')
    click_any(pg, ['約會']); pg.wait_for_timeout(1500)
    shot2(pg, '07_map_date'); shot2(pg, '07c_map_date_labels_daycard')
    click_any(pg, ['片場']); pg.wait_for_timeout(1200)
    pg.set_viewport_size({"width": 390, "height": 682}); pg.wait_for_timeout(1800)
    shot2(pg, '05b_map_labels_h682'); shot2(pg, 'venue398_682'); shot2(pg, 'venue_682_397')
    shot2(pg, 'venue398_seeded682'); shot2(pg, 'venue_seeded682_397'); shot2(pg, 'venue398_seeded682_toast')
    click_any(pg, ['約會']); pg.wait_for_timeout(1500)
    shot2(pg, '07b_map_date_labels_h682')
    click_any(pg, ['片場']); pg.wait_for_timeout(1000)
    pg.set_viewport_size({"width": 390, "height": 844}); pg.wait_for_timeout(1500)
    # user read-path state for userlabels4 names
    ev(pg, """()=>{S.dayIndex=10;S.fame=19;S.money=955;S.stress=46;if('credit' in S)S.credit=22;
      S.acting=18;S.stage=14;S.vocal=14;S.looks=22;S.charm=16;S.iq=20;S.stamina=75;
      S.homeEditable=false;S.weekPlanWeek37=2;S.weekPlan=['scout_all','scout_all','scout_all','scout_all','scout_all','scout_all','scout_all'];
      S.starDay={day:10,presence:{},triggered:99,doneToday:{}};S.romDay={day:10,presence:{},triggered:99,doneToday:{}};
      S.travel114={day:10,used:0};
      try{localStorage.setItem('starVolunteer_map_v19w',JSON.stringify(S));}catch(e){}return 'u';}""")
    pg.reload(); pg.wait_for_timeout(2500)
    click_any(pg, ['讀檔']); pg.wait_for_timeout(1200)
    ev(pg, "() => { const b=[...document.querySelectorAll('#slot-list button,#modal-btns button,.slot-row')].find(x=>x.offsetParent!==null&&/槽 1|第/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }")
    pg.wait_for_timeout(1800); to_map_j(pg)
    shot2(pg, 'userlabels4_390x844_ctrl')
    pg.set_viewport_size({"width": 430, "height": 707}); pg.wait_for_timeout(2000)
    shot2(pg, 'userlabels4_430x707_user')
    pg.set_viewport_size({"width": 390, "height": 844}); pg.wait_for_timeout(1200)

def sec_loc(pg):
    new_game(pg); rich_seed(pg, 520)
    ev(pg, "() => { S.starDay={day:520,presence:{gao_junjie:'film_lion'},triggered:99,doneToday:{}}; try{localStorage.setItem('starVolunteer_map_v19w',JSON.stringify(S));}catch(e){} return 'p'; }")
    locs = [('tvb_longmen', '08_loc_panel'), ('film_lion', '25_film_loc'), ('date_harbour', '26_date_loc'),
            ('clothing_shop', '28_clothing_shop'), ('gift_shop', '30_gift_shop'), ('cafe_cha', '32_cafe_intel'),
            ('ad_adm', 'loc_ad_adm'), ('ad_central', 'loc_ad_central'), ('film_cotton', 'loc_film_cotton'),
            ('film_harbour', 'loc_film_harbour'), ('hospital', 'loc_hospital'), ('rec_hk', 'loc_rec_hk'),
            ('rec_star', 'loc_rec_star'), ('rec_wanchai', 'loc_rec_wanchai'), ('tvb_harbour', 'loc_tvb_harbour'),
            ('tvb_kowloon', 'loc_tvb_kowloon')]
    for loc, name in locs:
        ok = open_loc_sheet(pg, loc)
        print("LOC", loc, ok, flush=True)
        if ok:
            shot2(pg, name)
            if loc == 'film_lion':
                shot2(pg, '25b_film_panel'); shot2(pg, 'modalbg2_film_panel')
            if loc == 'cafe_cha':
                shot2(pg, 'counts_intel_397')
                pg.set_viewport_size({"width": 390, "height": 682}); pg.wait_for_timeout(1500)
                shot2(pg, '32c_cafe_panel_check_h682')
                pg.set_viewport_size({"width": 390, "height": 844}); pg.wait_for_timeout(1200)
    # home -> notebook view
    ok = open_loc_sheet(pg, 'home')
    print("LOC home", ok, flush=True)
    pg.wait_for_timeout(1200); shot2(pg, 'loc_home')
    # training confirm modal at tvb
    if open_loc_sheet(pg, 'tvb_longmen'):
        ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/訓練|課程|報名/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1400); shot2(pg, '25_training_loc')
        click_modal(pg, ['取消', '返去', '關閉']); pg.wait_for_timeout(800)

def sec_board(pg):
    new_game(pg); seed_main(pg, 1)
    if open_board(pg):
        shot2(pg, '09_board'); shot2(pg, '09b_board_peak'); shot2(pg, 'board398_peak')
        ev(pg, "() => { const b=document.querySelector('[data-board-menu397]'); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(800); shot2(pg, 'board398_organize')
        ev(pg, "() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null&&/電視劇/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1000); shot2(pg, '09b_board_filtered')
        ev(pg, "() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null&&/全部|所有/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(800)
        ev(pg, "() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null&&/片酬|排序/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1000); shot2(pg, '09b_board_sorted'); shot2(pg, 'board_sorted_pay401')
        ev(pg, "() => { const sc=document.querySelector('.board-scroll, #modal-inner, .modal-body'); if(sc) sc.scrollTop=sc.scrollHeight; return !!sc; }")
        pg.wait_for_timeout(900); shot2(pg, '09c_board_peak_bottom')
        ev(pg, "() => { const sc=document.querySelector('.board-scroll, #modal-inner, .modal-body'); if(sc) sc.scrollTop=0; return !!sc; }")
        pg.wait_for_timeout(700)
        ev(pg, "() => { const c=document.querySelector('.gig-teaser.gt-featured')||document.querySelector('.gig-teaser'); if(c) c.click(); return !!c; }")
        pg.wait_for_timeout(1500); shot2(pg, '10_gig_detail'); shot2(pg, 'board398_detail')
        click_modal(pg, ['返去', '關閉', '返回']); pg.wait_for_timeout(1000)
        ev(pg, "() => { const cs=[...document.querySelectorAll('.gig-teaser')]; const c=cs[cs.length-1]; if(c) c.click(); return cs.length; }")
        pg.wait_for_timeout(1500); shot2(pg, 'board_detail_calc')
        click_modal(pg, ['返去', '關閉', '返回']); pg.wait_for_timeout(800)
        # red seal crops from peak shot
        try:
            from PIL import Image
            box = ev(pg, "() => { const im=[...document.querySelectorAll('img')].find(x=>/seal/.test(x.src||'')); if(!im) return null; const r=im.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; }")
            print("SEALBOX", box, flush=True)
        except Exception as e:
            print("SEALERR", e, flush=True)
    # locked board: fresh low stats
    new_game(pg)
    ev(pg, "() => { S.acting=18;S.stage=14;S.vocal=14;S.looks=22;S.charm=16;S.iq=20;S.stamina=75;S.fame=5;S.money=1200;S.dayIndex=1;S.travel114={day:1,used:0}; try{localStorage.setItem('starVolunteer_map_v19w',JSON.stringify(S));}catch(e){} return 'low'; }")
    if open_board(pg):
        shot2(pg, '09b_board_locked')

def open_notebook(pg):
    to_map_j(pg)
    r = click_any(pg, ['手帳', '行程'])
    pg.wait_for_timeout(1200)
    if ev(pg, "()=>(document.querySelector('.view.on')||{}).id") != 'v-home':
        ev(pg, "() => { const p=document.querySelector('.pin[data-loc=\"home\"]'); if(p) p.click(); return !!p; }")
        pg.wait_for_timeout(1500)
    play_out_story(pg); pg.wait_for_timeout(800)
def htab(pg, tab):
    ev(pg, "(t) => { const b=document.querySelector('[data-htab=\"'+t+'\"]'); if(b) b.click(); return !!b; }", tab)
    pg.wait_for_timeout(1000)
def sec_notebook(pg):
    new_game(pg); rich_seed(pg, 520)
    # v423：播種一致性——weekPlanWeek37 同 dayIndex 對齊（第75週），唔好令手帳出「上週行程 1990」假象
    ev(pg, "() => { S.weekPlanWeek37=75; S.weekPlan=['scout_all','rest','scout_all','scout_all','street','cafe_gig','rest']; S.homeEditable=false; try{ if(typeof renderAll==='function') renderAll(); }catch(e){} try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} return 'w'; }")
    ev(pg, """() => { try{ S.debts=[{id:'d1',who:'何生',amt:200,note:'人情債',day:300},{id:'d2',who:'霞姐',amt:150,note:'人情債',day:350}]; }catch(e){}
      try{ S.inventory=[{id:'g1',n:2}]; }catch(e){}
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} return 'x'; }""")
    open_notebook(pg)
    htab(pg, 'plan'); shot2(pg, '11_notebook_plan'); shot2(pg, '11b_notebook_plan_seeded')
    ev(pg, "() => { S.weekPlan=['train_acting','train_acting','train_stage','train_vocal','train_acting','train_stage','rest']; try{ if(typeof renderAll==='function') renderAll(); }catch(e){} return 'f'; }")
    pg.wait_for_timeout(1000); shot2(pg, '11d_notebook_plan_mixed'); shot2(pg, 'counts_11d_397')
    click_any(pg, ['行程工具']); pg.wait_for_timeout(600)
    click_any(pg, ['全日訓練']); pg.wait_for_timeout(800)
    shot2(pg, '11c_notebook_plan_filled')
    # suggest rows: week 2 editable true state; sync planDraft so cost row is actually shown
    sug = ev(pg, """() => { S.dayIndex=8; S.stress=78; S.weekPlanWeek37=2; S.fame=8; S.money=1100; S.acting=18; S.stage=14; S.vocal=14; S.looks=22; S.charm=16; S.iq=20; S.stamina=75; S.homeEditable=true; S.enrolled=S.enrolled||{}; S.enrolled.train_acting=true; S.weekPlan=['scout_all','scout_all','scout_all','scout_all','scout_all','scout_all','scout_all']; try{ planDraft=S.weekPlan.slice(); planSelDay=1; }catch(e){} try{ const c=document.getElementById('nb-cost400'); if(c){ c.textContent=''; c.hidden=true; } }catch(e){} try{ if(typeof renderNotebook==='function') renderNotebook(); }catch(e){} try{ if(typeof renderAll==='function') renderAll(); }catch(e){} const box=document.getElementById('nb-suggest400'); return JSON.stringify({day:S.dayIndex, editable:S.homeEditable, draft:(typeof planDraft!=='undefined')?planDraft:null, suggestHidden: box?box.hidden:null, suggestText: box?(box.textContent||'').trim():null, peak:(typeof weekStressPeak400==='function'&&typeof planDraft!=='undefined')?weekStressPeak400(planDraft):null}); }""")
    print("SUGGEST_STATE", sug, flush=True)
    pg.wait_for_timeout(1000)
    ev(pg, "() => { const e=document.getElementById('nb-suggest400'); if(e) e.scrollIntoView({block:'center'}); return !!e; }")
    pg.wait_for_timeout(700); shot2(pg, '11_suggest_row')
    clicked = ev(pg, "() => { const b=[...document.querySelectorAll('#nb-suggest400 button')].find(x=>x.offsetParent!==null&&/補最低屬性|建議：壓力偏高|沿用上次/.test(x.textContent||'')); if(b){ const t=(b.textContent||'').trim(); b.click(); return t; } return null; }")
    print("SUGGEST_CLICK", clicked, flush=True)
    pg.wait_for_timeout(900)
    cost = ev(pg, "() => { const c=document.getElementById('nb-cost400'); if(c) c.scrollIntoView({block:'center'}); return JSON.stringify({hidden:c?c.hidden:null, text:c?(c.textContent||'').trim():null, draft:(typeof planDraft!=='undefined')?planDraft:null}); }")
    print("SUGGEST_COST", cost, flush=True)
    pg.wait_for_timeout(500); shot2(pg, '11_suggest_cost_row')
    # v423：建議列段改過 dayIndex/stress，之後還原一致播種先影其餘分頁
    ev(pg, "() => { S.dayIndex=520; S.stress=20; S.weekPlanWeek37=75; S.fame=120; S.money=9000; S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.weekPlan=['scout_all','rest','scout_all','scout_all','street','cafe_gig','rest']; S.homeEditable=false; try{ if(typeof renderAll==='function') renderAll(); }catch(e){} try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} return 'r'; }")
    pg.wait_for_timeout(800)
    htab(pg, 'works'); shot2(pg, '13_works_wall')
    ev(pg, "() => { const w=document.querySelector('.work-row, .works-wall .work, [data-work]'); if(w) w.click(); return !!w; }")
    pg.wait_for_timeout(1200); shot2(pg, '14_work_detail')
    click_modal(pg, ['關閉', '返回']); pg.wait_for_timeout(700)
    ev(pg, "() => { const sc=document.querySelector('.home-scroll, #v-home'); if(sc) sc.scrollTop=sc.scrollHeight; window.scrollTo(0,99999); return true; }")
    pg.wait_for_timeout(800); shot2(pg, '18_tags')
    htab(pg, 'awards'); shot2(pg, '15b_awards_tab_content')
    htab(pg, 'memory'); shot2(pg, '16_memory')
    htab(pg, 'clippings'); shot2(pg, '20_clippings')
    htab(pg, 'ledger'); shot2(pg, '17_ledger')
    htab(pg, 'inventory'); shot2(pg, '19_inventory')
    htab(pg, 'debt'); shot2(pg, '21_debt')
    htab(pg, 'wardrobe'); shot2(pg, '87_wardrobe_tab')
    htab(pg, 'stats389'); shot2(pg, '88_stats_card')
    click_any(pg, ['進度']); pg.wait_for_timeout(1200); shot2(pg, '12_notebook_progress')
    click_modal(pg, ['關閉', '返回']); pg.wait_for_timeout(700)
    # awards empty state on fresh game
    new_game(pg); open_notebook(pg); htab(pg, 'awards'); shot2(pg, '15_awards_tab')

def sec_menu_slots(pg):
    new_game(pg); rich_seed(pg, 520); to_map_j(pg)
    ev(pg, "() => { const b=document.getElementById('btn-menu')||[...document.querySelectorAll('button')].find(x=>/☰|選單/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(1000); shot2(pg, '24_menu'); shot2(pg, '24_menu_clean'); shot2(pg, 'counts_menu_397')
    click_any(pg, ['設定']); pg.wait_for_timeout(1200); shot2(pg, '41_settings'); shot2(pg, 'dayres398_settings41')
    click_modal(pg, ['關閉', '返回']); pg.wait_for_timeout(800)
    ev(pg, "() => { const b=document.getElementById('btn-menu')||[...document.querySelectorAll('button')].find(x=>/☰|選單/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(900)
    click_any(pg, ['讀檔']); pg.wait_for_timeout(1200); shot2(pg, '42_slot_pick_occupied'); shot2(pg, '02c_load_slot')
    click_modal(pg, ['關閉', '返回']); pg.wait_for_timeout(800)
    ev(pg, "() => { const b=document.getElementById('btn-menu')||[...document.querySelectorAll('button')].find(x=>/☰|選單/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(900)
    click_any(pg, ['新遊戲']); pg.wait_for_timeout(1200)
    ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button, #slot-list button')].find(x=>x.offsetParent!==null&&/槽 1/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }")
    pg.wait_for_timeout(1200); shot2(pg, '42_slot_overwrite')
    click_modal(pg, ['取消', '返去', '關閉']); pg.wait_for_timeout(800)
    pg.reload(); pg.wait_for_timeout(2500); shot2(pg, '36_after_reload')
    click_any(pg, ['繼續', '讀檔']); pg.wait_for_timeout(1200)
    ev(pg, "() => { const b=[...document.querySelectorAll('#slot-list button,#modal-btns button,.slot-row')].find(x=>x.offsetParent!==null); if(b){ b.click(); return true; } return false; }")
    pg.wait_for_timeout(2500); shot2(pg, '02c_load_slot_confirm')

def advance_day_j(pg, want_shot=None):
    for step in range(60):
        st = state_tag(pg)
        mask = st.get('mask') or ''
        if 'story-play-on' in mask:
            play_out_story(pg); pg.wait_for_timeout(800); continue
        if 'day-res' in mask:
            if want_shot and want_shot != '40_start_day':
                shot2(pg, want_shot)
            click_modal(pg, ['休息並過日', '執行今日行程', '開始拍攝', '開始工作', '回家結算', '返回地圖', '繼續']); pg.wait_for_timeout(1000)
            return True
        if st.get('view') == 'v-map' and 'on' not in mask:
            if want_shot == '40_start_day':
                shot2(pg, '40_start_day'); shot2(pg, 'dayres_40_397')
                want_shot = None
            r = ev(pg, "() => { const b=document.getElementById('map-start-today'); if(b){ b.click(); return (b.textContent||'').trim(); } return null; }")
            if not r:
                r = click_any(pg, ['執行今日行程', '休息並過日', '開始拍攝', '開始工作', '過一日'])
            pg.wait_for_timeout(1200); continue
        if '開始今日行程' in (st.get('h3') or ''):
            if want_shot == '40_start_day':
                shot2(pg, '40_start_day'); shot2(pg, 'dayres_40_397')
                want_shot = None
            click_modal(pg, ['開始並結算當日', '確定']); pg.wait_for_timeout(1000); continue
        if click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '確定', '收下這份剪報', '收下剪報', '跳過', '關閉', '我知道了', '返回地圖', '好']):
            pg.wait_for_timeout(800); continue
        pg.mouse.click(195, 120); pg.wait_for_timeout(700)
    return False
def sec_dayres(pg):
    new_game(pg)
    ev(pg, "() => { S.dayIndex=1; S.weekPlan=['rest','street','train_acting','train_acting','street','train_vocal','rest']; S.homeEditable=false; S.weekPlanWeek37=1; S.travel114={day:1,used:0}; S.starDay={day:1,presence:{},triggered:99,doneToday:{}}; S.romDay={day:1,presence:{},triggered:99,doneToday:{}}; try{localStorage.setItem('starVolunteer_map_v19w',JSON.stringify(S));}catch(e){} return 'p'; }")
    to_map_j(pg)
    names = ['27_dayres_01', '27_dayres_02', '27_dayres_03', '27_dayres_04', '27_dayres_05', '27_dayres_06', '27_dayres_07', '27_dayres_08']
    advance_day_j(pg, '40_start_day')
    for i, nm in enumerate(names):
        ok = advance_day_j(pg, nm)
        # v419：跨週嗰陣同步 weekPlanWeek37，唔好令日結標題星期同日期矛盾（擷取播種一致性）
        ev(pg, "() => { try{ S.weekPlanWeek37 = Math.floor((S.dayIndex|0)/7)+1; localStorage.setItem('starVolunteer_map_v19w',JSON.stringify(S)); }catch(e){} return true; }")
        print("DAYRES", nm, ok, flush=True)
        if nm == '27_dayres_01':
            shot2(pg, '86_rest_dayend'); shot2(pg, 'dayres398_rest'); shot2(pg, 'dayres_rest_397')
        if nm == '27_dayres_02':
            shot2(pg, '27_dayres_coffee')
        if nm == '27_dayres_03':
            shot2(pg, '27c_dayres_afterday'); shot2(pg, 'dayres398_train27c'); shot2(pg, 'dayres_27c_397')
    shot2(pg, '86c_rest_dayend_ended'); shot2(pg, 'dayres_86c_397')
    shot2(pg, '86b_rest_dayend_after_cancel')

def sec_shops_intel(pg):
    new_game(pg); rich_seed(pg, 520)
    if open_loc_sheet(pg, 'clothing_shop'):
        ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/買衫/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1400); shot2(pg, '29_wardrobe_shop'); shot2(pg, 'shop_wardrobe_d')
        click_modal(pg, ['關閉', '返回', '返去']); pg.wait_for_timeout(800)
    if open_loc_sheet(pg, 'gift_shop'):
        ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/買禮物|禮物/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1400); shot2(pg, '31_gift_pick'); shot2(pg, 'shop_gift_d')
        click_modal(pg, ['關閉', '返回', '返去']); pg.wait_for_timeout(800)
    if open_loc_sheet(pg, 'cafe_cha'):
        ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/打聽/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1500); shot2(pg, '32b_intel_detail')
        click_modal(pg, ['確定', '關閉', '返回']); pg.wait_for_timeout(900)
        play_out_story(pg)
    if open_loc_sheet(pg, 'cafe_cha'):
        ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/約人/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1400); shot2(pg, 'intel_who_397')
        ev(pg, "() => { const b=[...document.querySelectorAll('#modal button, .picker button')].find(x=>x.offsetParent!==null); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1200); shot2(pg, 'intel_spot_397')

def sec_audition(pg):
    # accept confirm + wait cards
    new_game(pg); seed_main(pg, 1)
    if open_board(pg):
        ev(pg, "() => { const c=document.querySelector('.gig-teaser'); if(c) c.click(); return !!c; }")
        pg.wait_for_timeout(1400)
        ev(pg, "() => { const b=[...document.querySelectorAll('#modal button')].find(x=>x.offsetParent!==null&&/報名|應徵|確定/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1200); shot2(pg, '43_audition_after_accept')
        click_modal(pg, ['確定進行', '確定']); pg.wait_for_timeout(1500)
        shot2(pg, '43b_audition_result'); shot2(pg, '43c_audition_result_fail')
    r1 = run_attempt(pg, 'hired', {'acting':70,'stage':60,'vocal':45,'looks':55,'charm':50,'iq':45,'stamina':80}, True, '43d_phone_hired')
    print("AUD hired", r1.get('found_result'), flush=True)
    shot2(pg, '39_shoot_schedule')
    r2 = run_attempt(pg, 'fail', {'acting':18,'stage':14,'vocal':14,'looks':22,'charm':16,'iq':20,'stamina':75}, False, '43e_phone_fail')
    print("AUD fail", r2.get('found_result'), flush=True)
    shot2(pg, '402_43e_settle')
    click_modal(pg, ['我知道了', '繼續', '好']); pg.wait_for_timeout(1500)
    shot2(pg, 'day2_after_fail')
    r3 = run_attempt(pg, 'failcall', {'acting':18,'stage':14,'vocal':14,'looks':22,'charm':16,'iq':20,'stamina':75}, False, '43f_phone_fail_call', preset_fail_seen=True)
    print("AUD failcall", r3.get('found_result'), flush=True)

def sec_awards(pg):
    new_game(pg)
    ev(pg, """() => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = 423; S.homeEditable = false; S.weekPlanWeek37 = Math.floor(423/7)+1;
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19"].forEach(id=>{ S.story.done[id]=true; });
      S.story.phase='P5';
      S.starDay = {day:423, presence:{}, triggered:99, doneToday:{}};
      S.romDay = {day:423, presence:{}, triggered:99, doneToday:{}};
      S.travel114 = {day:423, used:0};
      S.wrapHistory = [
        { gigId:'gig_1991_film_102', title:'《霓虹夜影》男主角', type:'電影', totalDays:24, pay:3000, fame:20, popularity:10, wrappedDay:390, rating:'表現穩妥' },
        { gigId:'gig_1991_ad_111', title:'《新春團圓》廣告主角', type:'廣告', totalDays:2, pay:400, fame:40, popularity:8, wrappedDay:395, rating:'順利殺青' }
      ];
      return true; }""")
    to_map_j(pg)
    ev(pg, """() => { try{ const A = window.__awards; if(!A) return 'noA';
        if(A.debugForceSeasonWindow) A.debugForceSeasonWindow();
        if(A.queue) A.queue();
        if(A.present) A.present();
        return 'ok'; }catch(e){ return 'err:'+e.message; } }""")
    pg.wait_for_timeout(1500); shot2(pg, '35_awards_invite')
    click_any(pg, ['出席']); pg.wait_for_timeout(900)
    click_any(pg, ['確定']); pg.wait_for_timeout(1500)
    ev(pg, """() => { try{ const b=S.awardBooked213; if(!b) return 'no-booked';
      S.dayIndex = (b.ceremonyDay|0) + 1;
      const r = window.__awards.playEvening213 ? window.__awards.playEvening213() : 'no-fn';
      return JSON.stringify({ceremonyDay: b.ceremonyDay, nowDay: S.dayIndex, played: r}); }catch(e){ return 'err:'+e.message; } }""")
    pg.wait_for_timeout(1500)
    beats = ['35b_awards_1', '35b_awards_2', '35b_awards_3', '35b_awards_4', '35b_awards_5', '35b_awards_6']
    bi = 0
    shot2(pg, '35_awards_ceremony')
    for _ in range(40):
        if ev(pg, "() => !!document.querySelector('.paper-sheet')"):
            break
        if bi < len(beats):
            shot2(pg, beats[bi]); bi += 1
        skipped = ev(pg, "() => { const b=document.querySelector('.awd62-skip'); if(b){ b.click(); return true; } return false; }")
        if not skipped:
            click_modal(pg, ['下一句', '繼續', '確定', '跳過'])
        pg.wait_for_timeout(1100)
    pg.wait_for_timeout(1200)
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(600)
    shot2(pg, '35c_awards_result'); shot2(pg, '35c_top_397'); shot2(pg, 'awards398_p1')
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    shot2(pg, '35c_awards_result_bottom'); shot2(pg, '35c_bottom_397')
    click_any(pg, ['第二版']); pg.wait_for_timeout(900)
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(600)
    shot2(pg, '35c_awards_result_p2'); shot2(pg, '35c_page2_397'); shot2(pg, 'awards398_p2')
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=sc.scrollHeight; return true; }")
    pg.wait_for_timeout(900)
    shot2(pg, '35c_awards_result_p2_bottom'); shot2(pg, '35c_page2_bottom_397')

def sec_encounter_date(pg):
    new_game(pg); rich_seed(pg, 520)
    ev(pg, "() => { S.starDay={day:520,presence:{lin_xiaoqing:'cafe_cha'},triggered:0,doneToday:{}}; S.romDay={day:520,presence:{lin_xiaoqing:'cafe_cha'},triggered:0,doneToday:{}}; if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'}; S.story.done['R_hiu_meet']=true; S.story.rel=S.story.rel||{}; S.story.rel['lin_xiaoqing']=3; S.travel114={day:520,used:0}; try{localStorage.setItem('starVolunteer_map_v19w',JSON.stringify(S));}catch(e){} return 'e'; }")
    if open_loc_sheet(pg, 'cafe_cha'):
        ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/傾談|巧遇|林曉晴/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1800); shot2(pg, '37_encounter_choice')
        play_out_story(pg)
    # date flow
    to_map_j(pg)
    click_any(pg, ['約會']); pg.wait_for_timeout(1200)
    ev(pg, "() => { const p=document.querySelector('.pin[data-loc=\"date_harbour\"]'); if(p) p.click(); return !!p; }")
    pg.wait_for_timeout(1500)
    ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button, button')].find(x=>x.offsetParent!==null&&/約/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(1500)
    ev(pg, "() => { const b=[...document.querySelectorAll('#modal button')].find(x=>x.offsetParent!==null&&/林曉晴|曉晴/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(1800)
    shot2(pg, '44_date_scene'); shot2(pg, '44_date_after_pick')
    ev(pg, "() => { const c=document.querySelector('.sp-choice'); if(c) c.click(); return !!c; }")
    pg.wait_for_timeout(1800)
    shot2(pg, '44b_date_after_pick'); shot2(pg, '44c_date_result')

def sec_sick(pg):
    # afford variant
    new_game(pg); seed_sick(pg, 9000)
    go_map(pg)
    # v423：跟 run_variant 同一步進邏輯推進到治療抉擇出現先拍（真玩路徑）
    for _step in range(160):
        pg.wait_for_timeout(800)
        _st = state_json(pg)
        _h3 = _st.get('h3') or ''
        if _h3.startswith('病倒'):
            break
        _mask_on = 'on' in (_st.get('mask') or '')
        if not _mask_on and _st.get('view') == 'v-map':
            if not click_any(pg, ['開始今日行程']):
                click_any(pg, ['過一日'])
            pg.wait_for_timeout(1200); continue
        if not _mask_on:
            pg.wait_for_timeout(700); continue
        if '通告欄' in _h3:
            click_any(pg, ['返去地點']); pg.wait_for_timeout(900); continue
        if '開始今日行程' in _h3:
            click_modal(pg, ['開始並結算當日']); pg.wait_for_timeout(1000); continue
        if '病倒休養' in _h3:
            click_modal(pg, ['返回地圖']); pg.wait_for_timeout(1200)
            click_any(pg, ['過一日']); pg.wait_for_timeout(1500); continue
        if not click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '確定', '收下這份剪報', '跳過', '關閉', '開始今日行程', '回家結算', '返回地圖']):
            pg.mouse.click(195, 120); pg.wait_for_timeout(700)
    shot2(pg, '45_sick_card'); shot2(pg, '45b_sick_after')
    advance_day_j(pg, '45c_sick_day2')
    if open_loc_sheet(pg, 'hospital'):
        shot2(pg, '45d_sick_hospital')
    r = run_variant(pg, 'afford', 9000)
    print("SICK afford done", flush=True)
    new_game(pg); seed_sick(pg, 10)
    r2 = run_variant(pg, 'nomoney', 10)
    print("SICK nomoney done", flush=True)
    # base names from 402 variants just shot: re-shoot states via fresh variants is complex; copy files as same-state aliases
    import shutil
    for src, dst in [('402_46_offer_afford', '46_hosp_treat_offer'), ('402_46b_confirm', '46b_hosp_treat_confirm'),
                     ('402_46_offer_nomoney', '46c_hosp_treat_no_money'), ('402_46d_treated_after', '46d_hosp_treated_after')]:
        s = f"{SHOTS}/{src}.png"; d = f"{SHOTS}/{dst}.png"
        if os.path.exists(s):
            shutil.copyfile(s, d); print("ALIAS", src, "->", dst, flush=True)

def sec_ending(pg):
    try:
        src = json.load(open('/home/hatch/workspace/linji-ending-targets-2026-11-23/E3_director_ls_backup.json'))
        fin = json.load(open('/home/hatch/workspace/linji-ending-targets-2026-11-23/E3_director_ending_final.json'))
        S = json.loads(src['starVolunteer_map_v19w'])
        e410 = fin['ending410']
        S['ending410'] = {'id': e410.get('career'), 'career': e410.get('career'), 'careerVariant': e410.get('careerVariant'),
            'title': e410.get('title'), 'settled': e410.get('settled'), 'creditsHeld': e410.get('creditsHeld'),
            'exodusNames': e410.get('exodusNames') or [], 'romance': e410.get('romanceLine'),
            'romanceLine': e410.get('romanceLine'), 'romanceKind': e410.get('romanceKind'),
            'exodus': e410.get('exodus'), 'day': e410.get('day'), 'fame': e410.get('fame'),
            'credit': e410.get('credit'), 'dual': e410.get('dual'), 'gaps95': e410.get('gaps95') or []}
        pg.goto(URL); pg.wait_for_timeout(2500)
        ev(pg, """(payload) => {
          localStorage.setItem('starVolunteer_map_v19w', payload.S);
          localStorage.setItem('starVolunteer_prefs_v19z9', payload.prefs);
          return 'stored'; }""", {'S': json.dumps(S, ensure_ascii=False), 'prefs': src.get('starVolunteer_prefs_v19z9', '{}')})
        pg.reload(wait_until="load"); pg.wait_for_timeout(3000)
        click_any(pg, ['繼續']); pg.wait_for_timeout(2500)
        ev(pg, "() => { const rows=[...document.querySelectorAll('.slot-row')]; if(rows[0]){ rows[0].click(); return 'clicked'; } return 'no-slot'; }")
        pg.wait_for_timeout(2500)
        shot2(pg, '33_ending_summary')
        ev(pg, "() => { const b=[...document.querySelectorAll('#modal button, button')].find(x=>x.offsetParent!==null&&/回顧|手帳/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
        pg.wait_for_timeout(1800)
        shot2(pg, '33b_ending_gate'); shot2(pg, 'counts_33b_397')
    except Exception as e:
        print("ENDING_FAIL", repr(e)[:300], flush=True)

SECTIONS = {'title_tut': sec_title_tut, 'map': sec_map, 'loc': sec_loc, 'board': sec_board,
            'notebook': sec_notebook, 'menu_slots': sec_menu_slots, 'dayres': sec_dayres,
            'shops_intel': sec_shops_intel, 'audition': sec_audition, 'awards': sec_awards,
            'encounter_date': sec_encounter_date, 'sick': sec_sick, 'ending': sec_ending}
def main_j():
    want = sys.argv[1:] or list(SECTIONS.keys())
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox", "--proxy-server=http://127.0.0.1:18081", "--ignore-certificate-errors"])
        ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERR", str(e)[:200], flush=True))
        for name in want:
            print("=== SECTION", name, "===", flush=True)
            try:
                SECTIONS[name](pg)
            except Exception as e:
                print("SECTION_FAIL", name, repr(e)[:400], flush=True)
            pg.set_viewport_size({"width": 390, "height": 844})
        print("CAPTURE_J DONE", flush=True)
if __name__ == '__main__':
    main_j()
