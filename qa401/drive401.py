# -*- coding: utf-8 -*-
"""v401 UI401 頭五項・實駕覆驗。
Serves the repo this script lives in locally (--root 可指去基線副本),
Playwright headless shell 經本地 CONNECT 中繼。
用法：
  /home/hatch/pwenv49/bin/python qa401/drive401.py [--root DIR] [--only phone,hosp,tut,awards,board]
結果 JSON＋截圖 -> /home/hatch/workspace/linji-drive401/。
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

ap = argparse.ArgumentParser()
ap.add_argument('--root', default=None)
ap.add_argument('--only', default='phone,hosp,tut,awards,board')
args = ap.parse_args()
sys.argv = sys.argv[:1]
import driver as drv

ITEMS = [x.strip() for x in args.only.split(',') if x.strip()]
ROOT = args.root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/home/hatch/workspace/linji-drive401"
SHOTS = OUT + "/shots"
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
    p = f"{SHOTS}/{name}.png"; pg.screenshot(path=p)
    md = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    print("SHOT", name, md, flush=True); return p

def shot_clip(pg, name, clip):
    p = f"{SHOTS}/{name}.png"; pg.screenshot(path=p, clip=clip)
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
    shot(pg, '401_43b_wait_' + tag)
    # 金掣「繼續」放大：搵 .p 掣 rect，做 clip 截圖（dsf 2 下 clip 係 CSS px）
    box = ev(pg, """() => { const b=[...document.querySelectorAll('#modal-btns button.p')].find(x=>x.offsetParent!==null);
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x, y:r.y, width:r.width, height:r.height}; }""")
    if box:
        out['gold_btn_box'] = box
        pad = 6
        shot_clip(pg, '401_43b_goldbtn_zoom_' + tag,
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
        h3 = st.get('h3') or ''
        body = st.get('body') or ''
        _tgt = (target or {}).get('title') or ''
        if want_ok and (h3.startswith('獲聘') and (not _tgt or _tgt in h3)):
            res['result'] = st; res['result_modal401'] = modal401(pg, 'phone-hired')
            res['result_contrast'] = contrast(pg, '#modal', 'phone-hired')
            shot(pg, shotname); found = True; break
        if want_ok and h3 == '何生來電' and '簽約金' in body and (not _tgt or _tgt in body):
            res['result'] = st; res['result_modal401'] = modal401(pg, 'phone-hired')
            res['result_contrast'] = contrast(pg, '#modal', 'phone-hired')
            shot(pg, shotname); found = True; break
        if (not want_ok) and h3 == '何生來電' and '冇你份' in body and (not _tgt or _tgt in body):
            res['result'] = st; res['result_modal401'] = modal401(pg, 'phone-fail')
            res['result_contrast'] = contrast(pg, '#modal', 'phone-fail')
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
        if click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '確定', '收下這份剪報', '跳過', '關閉', '開始今日行程', '回家結算', '簽約', '我知道了', '返回地圖']):
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
            shot(pg, '401_46_offer_' + tag)
            if tag == 'afford':
                c = click_modal(pg, ['去醫院治療'])
                pg.wait_for_timeout(1200)
                res['after_treat_click'] = c
                st2 = state_json(pg)
                res['confirm_state'] = st2
                res['confirm_modal401'] = modal401(pg, 'hosp-confirm')
                res['confirm_contrast'] = contrast(pg, '#modal', 'hosp-confirm')
                shot(pg, '401_46b_confirm')
                click_modal(pg, ['確定'])
                pg.wait_for_timeout(1500)
                res['after_confirm'] = state_json(pg)
                # 46d：治療後病假日結卡（afterDayModal 病假路徑）
                res['treated_modal401'] = modal401(pg, 'hosp-treated-46d')
                res['treated_contrast'] = contrast(pg, '#modal', 'hosp-treated-46d')
                shot(pg, '401_46d_treated_after')
            else:
                click_modal(pg, ['留喺屋企休養'])
                pg.wait_for_timeout(1200)
                res['after_stay'] = state_json(pg)
                res['stay_modal401'] = modal401(pg, 'hosp-stay-46c')
                shot(pg, '401_46c_stay')
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
            shot(pg, '401_46x_gate_missed_sickcard')
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
    shot(pg, '401_tut_step0_welcome')
    click_modal(pg, ['下一步']); pg.wait_for_timeout(1500)
    res['step1'] = json.loads(ev(pg, TUT401_JS))
    shot(pg, '401_tut_step1_map')
    click_modal(pg, ['下一步']); pg.wait_for_timeout(1200)
    res['step2'] = json.loads(ev(pg, TUT401_JS))
    shot(pg, '401_tut_step2_board')
    click_modal(pg, ['下一步', '我知道了']); pg.wait_for_timeout(1200)
    res['step3'] = json.loads(ev(pg, TUT401_JS))
    shot(pg, '401_tut_step3_done')
    # TUT_DONE 卡撳掣 → finishTutorial → B01 入門卡（tut_04）
    click_modal(pg, ['我知道了', '下一步']); pg.wait_for_timeout(1500)
    res['b01'] = state_json(pg)
    res['b01_modal401'] = modal401(pg, 'tut-b01')
    res['b01_contrast'] = contrast(pg, '#modal', 'tut-b01')
    shot(pg, '401_tut_04_b01')
    save_out('tut401.json', res)
    return res

# ================= 頒獎 35c =================
def probe_awards(pg):
    new_game(pg)
    ev(pg, """() => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = 420; S.homeEditable = false; S.weekPlanWeek37 = Math.floor(420/7)+1;
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19"].forEach(id=>{ S.story.done[id]=true; });
      S.story.phase='P5';
      S.starDay = {day:420, presence:{}, triggered:99, doneToday:{}};
      S.romDay = {day:420, presence:{}, triggered:99, doneToday:{}};
      S.travel114 = {day:420, used:0};
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
    for _ in range(30):
        if ev(pg, "() => !!document.querySelector('.paper-sheet')"): break
        skipped = ev(pg, "() => { const b=document.querySelector('.awd62-skip'); if(b){ b.click(); return true; } return false; }")
        if not skipped:
            click_modal(pg, ['下一句', '繼續', '確定', '跳過'])
        pg.wait_for_timeout(1000)
    pg.wait_for_timeout(1200)
    res = {}
    ev(pg, "() => { const sc=document.getElementById('modal-inner'); if(sc) sc.scrollTop=0; return true; }")
    pg.wait_for_timeout(600)
    shot(pg, '401_awards_p1')
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
    shot(pg, '401_awards_p2')  # 頂圖：主標「陳偉翔散場」＋奪獎小標（此時 scrollTop 0）
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
    shot(pg, '401_awards_p2_bottom')
    save_out('awards401.json', res)
    return res

# ================= 通告欄（整理選單＋詳情頁） =================
def probe_board(pg):
    new_game(pg)
    seed_main(pg, 1)
    assert open_board(pg), "board open failed"
    res = {}
    res['head'] = ev(pg, """() => JSON.stringify({
      nCards: document.querySelectorAll('.gig-teaser').length })""")
    shot(pg, '401_board_peak')
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
    shot(pg, '401_board_organize')
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
    shot(pg, '401_board_detail_top')
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
    shot(pg, '401_board_detail_bottom')
    save_out('board401.json', res)
    return res

PROBES = {'phone': None, 'hosp': None, 'tut': probe_tut, 'awards': probe_awards, 'board': probe_board}

def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox',
            '--proxy-server=http://127.0.0.1:18081', '--ignore-certificate-errors'])
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: print('PAGEERROR', str(e)[:200], flush=True))
        out = {}
        if 'phone' in ITEMS:
            print('=== PROBE phone', flush=True)
            ph = {}
            try:
                ph['hired'] = run_attempt(pg, 'hired',
                    {'acting':70,'stage':60,'vocal':45,'looks':55,'charm':50,'iq':45,'stamina':80},
                    True, '401_43d_phone_hired')
            except Exception as e: print('PROBE_FAIL phone-hired', repr(e)[:300], flush=True)
            try:
                ph['fail'] = run_attempt(pg, 'fail',
                    {'acting':18,'stage':14,'vocal':14,'looks':22,'charm':16,'iq':20,'stamina':75},
                    False, '401_43e_phone_fail')
            except Exception as e: print('PROBE_FAIL phone-fail', repr(e)[:300], flush=True)
            try:
                ph['failcall'] = run_attempt(pg, 'failcall',
                    {'acting':18,'stage':14,'vocal':14,'looks':22,'charm':16,'iq':20,'stamina':75},
                    False, '401_43f_phone_fail_call', preset_fail_seen=True)
            except Exception as e: print('PROBE_FAIL phone-failcall', repr(e)[:300], flush=True)
            out['phone'] = ph
            save_out('phone401.json', ph)
        if 'hosp' in ITEMS:
            print('=== PROBE hosp', flush=True)
            hp = {}
            try: hp['afford'] = run_variant(pg, 'afford', 9000)
            except Exception as e: print('PROBE_FAIL hosp-afford', repr(e)[:300], flush=True)
            try: hp['nomoney'] = run_variant(pg, 'nomoney', 10)
            except Exception as e: print('PROBE_FAIL hosp-nomoney', repr(e)[:300], flush=True)
            out['hosp'] = hp
            save_out('hosp401.json', hp)
        for name in ('tut', 'awards', 'board'):
            if name in ITEMS:
                print('=== PROBE', name, flush=True)
                try: out[name] = PROBES[name](pg)
                except Exception as e: print('PROBE_FAIL', name, repr(e)[:300], flush=True)
        save_out('drive401.json', out)
        print("DONE drive401", flush=True)
        b.close()

if __name__ == '__main__':
    main()
srv.terminate()
