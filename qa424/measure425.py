# -*- coding: utf-8 -*-
"""v425 UI26 GPT評級修復量度：板頭篩選態三視口、詳情首屏、鎖定日格、日期行。
用法: /home/hatch/pwenv49/bin/python qa424/measure425.py
輸出 -> qa424/out/（fix425_*.png + measure_fix425.json）。只量度，唔改 code。"""
import sys, os, json, socket, subprocess, time, urllib.request, hashlib

sys.path.insert(0, '/home/hatch/workspace/fullarc')
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/hatch/pw-browsers')
from playwright.sync_api import sync_playwright
import driver as drv

ROOT = '/home/hatch/workspace/linji-work424'
OUT = ROOT + '/qa424/out'
SHOTS = OUT + '/shots'
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"

def free_port():
    for cand in range(9451, 9470):
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

R = {}
def rec(k, v):
    R[k] = v
    print("REC", k, json.dumps(v, ensure_ascii=False)[:700] if not isinstance(v, str) else v[:700], flush=True)

def ev(pg, js, arg=None):
    try: return pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)
    except Exception as e: print("EVFAIL", str(e)[:200], flush=True); return None

def shot(pg, name):
    p = f"{SHOTS}/fix425_{name}.png"; pg.screenshot(path=p)
    md = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    print("SHOT", name, md, flush=True); return p

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
            choice: !!(document.querySelector('.sp-choice')&&document.querySelector('.sp-choice').offsetParent!==null)}); }""")
        try: st = json.loads(st)
        except Exception: break
        if not st.get('on') and not st.get('sess'): return True
        if '巧遇' in (st.get('h3') or ''):
            if click_modal(pg, ['行開']): pg.wait_for_timeout(700); continue
            break
        if st.get('choice'):
            ev(pg, "() => { const c=document.querySelector('.sp-choice'); if(c) c.click(); }")
            pg.wait_for_timeout(700); continue
        if click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '完成', '返回地圖', '離開', '跳過', '關閉', '確定', '我知道了']):
            pg.wait_for_timeout(600); continue
        # 抉擇型 modal（無標準掣名）：撳最後一粒推進，唔好卡死
        fb = ev(pg, "() => { const bs=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null&&!b.disabled); if(bs.length){ bs[bs.length-1].click(); return (bs[bs.length-1].textContent||'').trim().slice(0,20); } return null; }")
        if fb:
            pg.wait_for_timeout(800); continue
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

def open_board(pg, loc='tvb_longmen'):
    if not open_loc_sheet(pg, loc):
        return False
    r = ev(pg, "() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>/通告欄/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(1400)
    return True

HEAD_JS = """() => JSON.stringify((()=>{
  const Rr=el=>{ if(!el) return null; const b=el.getBoundingClientRect(); return {top:+b.top.toFixed(1),bottom:+b.bottom.toFixed(1),left:+b.left.toFixed(1),right:+b.right.toFixed(1),h:+b.height.toFixed(1),w:+b.width.toFixed(1)}; };
  const inter=(a,b)=>{ if(!a||!b) return null; const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left), oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top); return (ox>0&&oy>0)?+(ox*oy).toFixed(1):0; };
  const sum=document.querySelector('.board-sum392');
  const formula=document.querySelector('.board-formula424');
  const ctl=document.querySelector('.board-ctl397');
  const segs=sum?[...sum.querySelectorAll('.bc-seg417')].map(s=>({t:(s.textContent||'').trim(), r:Rr(s)})):[];
  const sumR=Rr(sum), fR=Rr(formula), cR=Rr(ctl);
  // 「張」字可見：最後一段右緣 hit-test
  let zhangHit=null;
  if(segs.length){ const s0=sum.querySelector('.bc-seg417'); const r=s0.getBoundingClientRect();
    const top=document.elementFromPoint(Math.min(innerWidth-1,r.right-3), r.top+r.height/2);
    zhangHit = !!(top && (top===s0 || s0.contains(top) || top.contains(s0))); }
  const cards=[...document.querySelectorAll('.gig-teaser')];
  const bands=cards.slice(0,4).map(c=>{ const band=c.querySelector('.gt-band424'); const cols=band?[...band.querySelectorAll('.gt-col424')].map(x=>+x.getBoundingClientRect().left.toFixed(1)):[]; return {featured:c.classList.contains('gt-featured'), cols, cardLeft:+c.getBoundingClientRect().left.toFixed(1)}; });
  const segs425=[...document.querySelectorAll('.gt-seg425')].slice(0,12).map(s=>{ const r=s.getBoundingClientRect(); const lh=parseFloat(getComputedStyle(s).lineHeight)||19; return {t:(s.textContent||'').trim(), h:+r.height.toFixed(1), lines:Math.max(1,Math.round(r.height/lh))}; });
  return {vw:innerWidth, vh:innerHeight, sumText:sum?(sum.innerText||'').replace(/\\n/g,' '):null, sumR, fR, cR,
    sumFormulaOverlap:inter(sumR,fR), sumCtlOverlap:inter(sumR,cR), segs, zhangHit,
    formulaText:formula?(formula.querySelector('summary')||{}).textContent:null,
    bands, segs425};
})())"""

DET_JS = """() => JSON.stringify((()=>{
  const Rr=el=>{ if(!el) return null; const b=el.getBoundingClientRect(); return {top:+b.top.toFixed(1),bottom:+b.bottom.toFixed(1),left:+b.left.toFixed(1),right:+b.right.toFixed(1),h:+b.height.toFixed(1),w:+b.width.toFixed(1)}; };
  const body=document.querySelector('.notice_sheet_body');
  const bR=Rr(body);
  const secs=[...document.querySelectorAll('.cn-sec424')];
  const secOf=t=>secs.find(s=>(s.textContent||'').trim()===t);
  const reqGrid=document.querySelector('.cn-req-grid30v2');
  const contract=document.querySelector('.cn-contract401');
  const schedSec=secOf('檔期');
  const audSec=secOf('試鏡與接單');
  // 檔期段容器底（v425 cn-sched425 包裝）
  const schedLast=document.querySelector('.cn-sched425');
  const btns=document.getElementById('modal-btns');
  const accept=[...document.querySelectorAll('#modal-btns button')].find(b=>/接通告/.test(b.textContent||''));
  const varNote=document.querySelector('.cn-summary .var-note');
  const calc=document.querySelector('.board-calc397');
  const inBody=r=>r&&bR?(r.bottom<=bR.bottom+1&&r.top>=bR.top-1):null;
  return {vw:innerWidth, vh:innerHeight, bodyR:bR, bodyScrollTop:body?body.scrollTop:null,
    contractR:Rr(contract), contractIn:inBody(Rr(contract)),
    reqR:Rr(reqGrid), reqIn:inBody(Rr(reqGrid)),
    schedSecR:Rr(schedSec), schedLastR:Rr(schedLast), schedLastText:schedLast?(schedLast.innerText||'').replace(/\\n/g,' '):null,
    schedIn:inBody(Rr(schedLast)), schedSecIn:inBody(Rr(schedSec)),
    audSecR:Rr(audSec), btnsR:Rr(btns), acceptText:accept?(accept.textContent||'').trim():null,
    varNoteR:Rr(varNote), varNoteText:varNote?(varNote.innerText||'').replace(/\\n/g,' '):null,
    calcR:Rr(calc), calcInBody: calc? !!calc.closest('.notice_sheet_body') : null,
    calcText:calc?(calc.innerText||'').replace(/\\n/g,' '):null,
    heroR:Rr(document.querySelector('.cn-issuer30v2'))};
})())"""

NB_JS = """() => JSON.stringify((()=>{
  const Rr=el=>{ if(!el) return null; const b=el.getBoundingClientRect(); return {top:+b.top.toFixed(1),bottom:+b.bottom.toFixed(1),left:+b.left.toFixed(1),right:+b.right.toFixed(1),h:+b.height.toFixed(1),w:+b.width.toFixed(1)}; };
  const rows=[...document.querySelectorAll('.day-row')].filter(x=>x.offsetParent!==null);
  const cells=rows.map(d=>{ const main=d.querySelector('.plan-main'); const hint=d.querySelector('.plan-hint');
    const lh=main?(parseFloat(getComputedStyle(main).lineHeight)||19):19;
    const mR=Rr(main);
    return {t:(d.innerText||'').replace(/\\n/g,' | ').slice(0,60), locked:d.classList.contains('locked'),
      mainText:main?(main.textContent||'').trim():null, mainLines:mR?Math.max(1,Math.round(mR.h/lh)):null,
      hintSegs:hint?[...hint.querySelectorAll('.hint-seg414')].map(s=>({t:(s.textContent||'').trim(), top:+s.getBoundingClientRect().top.toFixed(1)})):[],
      aria:d.getAttribute('aria-label'), r:Rr(d)}; });
  const range=document.getElementById('nb-range');
  const rangeSegs=range?[...range.querySelectorAll('.nb-seg425')].map(s=>({t:(s.textContent||'').trim(), top:+s.getBoundingClientRect().top.toFixed(1), h:+s.getBoundingClientRect().height.toFixed(1)})):[];
  const lhR=range?(parseFloat(getComputedStyle(range).lineHeight)||20):20;
  const rangeR=Rr(range);
  const title=document.getElementById('nb-right-title');
  const nb=document.getElementById('notebook');
  const acts=[...document.querySelectorAll('.act-item')].filter(b=>b.offsetParent!==null);
  const nbR=Rr(nb);
  return {vw:innerWidth, vh:innerHeight, cells, rangeText:range?(range.innerText||''):null, rangeSegs,
    rangeLines:rangeR?Math.max(1,Math.round(rangeR.h/lhR)):null,
    titleText:title?(title.textContent||'').trim():null,
    editTags:document.querySelectorAll('.edit-tag414').length,
    nbScroll:nb?Math.round(nb.scrollTop):null,
    firstActBottom:acts.length?+acts[0].getBoundingClientRect().bottom.toFixed(1):null, nbBottom:nbR?nbR.bottom:null};
})())"""

def main():
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox", "--proxy-server=http://127.0.0.1:18081", "--ignore-certificate-errors"])
        ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERR", str(e)[:200], flush=True))

        # ---- 板頭篩選態三視口 + 未捲態覆核 ----
        for (vw, vh, tag) in [(390, 844, '390x844'), (430, 707, '430x707'), (430, 932, '430x932')]:
            pg.set_viewport_size({'width': vw, 'height': vh})
            new_game(pg); seed_main(pg, 1); pg.wait_for_timeout(800)
            if not open_board(pg):
                rec(f'head_{tag}', 'board-fail'); continue
            shot(pg, f'board_peak_{tag}')
            rec(f'head_default_{tag}', json.loads(ev(pg, HEAD_JS)))
            ev(pg, "() => { const b=document.querySelector('[data-board-menu397]'); if(b) b.click(); return !!b; }")
            pg.wait_for_timeout(700)
            ev(pg, "() => { const b=[...document.querySelectorAll('[data-filter392]')].find(x=>x.dataset.filter392==='電視劇'); if(b) b.click(); return !!b; }")
            pg.wait_for_timeout(1000)
            shot(pg, f'board_filtered_{tag}')
            rec(f'head_filtered_{tag}', json.loads(ev(pg, HEAD_JS)))

        # ---- 詳情首屏（電影／廣告） ----
        for (vw, vh, tag) in [(390, 844, '390x844'), (430, 707, '430x707')]:
            pg.set_viewport_size({'width': vw, 'height': vh})
            new_game(pg); seed_main(pg, 1); pg.wait_for_timeout(800)
            for loc, ltag in [('film_lion', 'film'), ('ad_central', 'ad')]:
                if not open_board(pg, loc):
                    rec(f'det_{ltag}_{tag}', 'board-fail'); continue
                ev(pg, "() => { const c=document.querySelector('.gig-teaser[data-board-state=\"ready\"]')||document.querySelector('.gig-teaser'); if(c) c.click(); return !!c; }")
                pg.wait_for_timeout(1500)
                shot(pg, f'gig_{ltag}_detail_{tag}')
                rec(f'det_{ltag}_{tag}', json.loads(ev(pg, DET_JS)))
                ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button')].find(x=>/離開|返回/.test(x.textContent||'')); if(b) b.click(); return !!b; }")
                pg.wait_for_timeout(1000)
                play_out_story(pg)

        # ---- 手帳鎖定日格（唯讀週：拍攝中《電視一族》Mon-Wed） ----
        pg.set_viewport_size({'width': 390, 'height': 844})
        new_game(pg); pg.wait_for_timeout(800)
        # 鎖定週播種：寫存檔後重載（planDraft/enterHome 喺 IIFE 內，唔可直接 evaluate）
        ev(pg, """() => {
          S.dayIndex=7; S.weekPlanWeek37=2; S.homeEditable=false;
          S.shoots=[{id:'sh425', title:'《電視一族》', gigId:'gig425', totalDays:3, doneDays:0, daysLeft:3, type:'電視劇', shootWeekdays:[1,2,3], hiredAtDay:7, deadlineDays:14, deadlineDay:21, pay:300, fame:5, popularity:3, locId:'tvb_longmen'}];
          S.weekPlan=['shoot:sh425','shoot:sh425','shoot:sh425','rest','street','scout_all','rest'];
          S.travel114={day:7,used:0};
          S.starDay={day:7,presence:{},triggered:99,doneToday:{}}; S.romDay={day:7,presence:{},triggered:99,doneToday:{}};
          try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
          return 'seeded'; }""")
        pg.reload(); pg.wait_for_timeout(3000)
        click_any(pg, ['繼續']); pg.wait_for_timeout(2000)
        try: pg.wait_for_function("() => typeof S !== 'undefined' && !!S", timeout=15000)
        except Exception: pass
        play_out_story(pg); pg.wait_for_timeout(800)
        # 經 UI 入手帳（唯讀）
        for _try in range(6):
            if ev(pg, "()=>(document.querySelector('.view.on')||{}).id") == 'v-home' and not ev(pg, "()=>document.getElementById('mask').classList.contains('on')"):
                break
            r = click_any(pg, ['手帳', '行程'])
            if not r:
                ev(pg, "() => { const p=document.querySelector('.pin[data-loc=\"home\"]'); if(p) p.click(); return !!p; }")
            pg.wait_for_timeout(1200)
            play_out_story(pg); pg.wait_for_timeout(600)
        rec('nb_locked_seed_state', ev(pg, "() => JSON.stringify({editable:S.homeEditable, weekPlan:S.weekPlan, day:S.dayIndex, mask:document.getElementById('mask').className, view:(document.querySelector('.view.on')||{}).id})"))
        ev(pg, "() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=0; return true; }")
        pg.wait_for_timeout(600)
        shot(pg, 'nb_locked_390x844')
        rec('nb_locked_390x844', json.loads(ev(pg, NB_JS)))
        # 撳鎖定日格：摘要全名可達
        ev(pg, "() => { const r=document.querySelector('.day-row.locked'); if(r) r.click(); return !!r; }")
        pg.wait_for_timeout(800)
        rec('nb_locked_selected', json.loads(ev(pg, NB_JS)))

        # ---- 手帳編輯態（日期行＋去重＋首屏） ----
        pg.set_viewport_size({'width': 430, 'height': 707})
        new_game(pg); pg.wait_for_timeout(800)
        shot(pg, 'nb_edit_430x707')
        rec('nb_edit_430x707', json.loads(ev(pg, NB_JS)))
        pg.set_viewport_size({'width': 390, 'height': 844})
        new_game(pg); pg.wait_for_timeout(800)
        shot(pg, 'nb_edit_390x844')
        rec('nb_edit_390x844', json.loads(ev(pg, NB_JS)))

        br.close()
    json.dump(R, open(f"{OUT}/measure_fix425.json", 'w'), ensure_ascii=False, indent=1)
    print("DONE", flush=True)

if __name__ == '__main__':
    main()
