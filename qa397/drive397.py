# -*- coding: utf-8 -*-
"""v397 UI fixes (audit round 5, top 5): real-drive verification.
Serves the repo this script lives in locally, Playwright headless shell via
local CONNECT relay. Usage:
  /home/hatch/pwenv49/bin/python qa397/drive397.py venue|counts|counts33b|board|awards|dayres|dayres2 [all]
Results JSON + screenshots -> qa397/verify/ and qa397/shots/.
Only measures / drives; never edits code or MEMORY.md.
"""
import sys, os, json, socket, subprocess, time, urllib.request
sys.path.insert(0, '/home/hatch/workspace/fullarc')
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/hatch/pw-browsers')
from playwright.sync_api import sync_playwright
import driver as drv

ITEMS = sys.argv[1:] or ['board']
# Repo root = parent of this script's qa397/ dir (portable across work copies;
# never hardcode a work-copy path — v397 regen lesson: a hardcoded ROOT served
# a deleted directory and every probe measured a 404 page).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "qa397", "verify")
SHOTS = os.path.join(ROOT, "qa397", "shots")
os.makedirs(OUT, exist_ok=True)
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"

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

def ev(pg, js, arg=None):
    try: return pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)
    except Exception as e: print("EVFAIL", str(e)[:300], flush=True); return None

def shot(pg, name):
    p = f"{SHOTS}/{name}.png"; pg.screenshot(path=p); print("SHOT", name, flush=True); return p

def count(pg, key):
    c = ev(pg, COUNT_JS)
    print("COUNT", key, c, flush=True)
    return json.loads(c) if isinstance(c, str) else c

def new_game(pg):
    """Start a fresh game. The #btn-new onclick is attached near the end of
    the ~5MB main script, so a click right after load can land before the
    handler exists and silently do nothing (S stays null) — retry the click
    until the game actually starts (S non-null or a modal/tutorial appears)."""
    pg.goto(URL); pg.wait_for_timeout(2500)
    for _ in range(12):
        pg.click('#btn-new'); pg.wait_for_timeout(1200)
        st = ev(pg, "() => JSON.stringify({s: !!(typeof S!=='undefined'&&S), mask: document.getElementById('mask').classList.contains('on'), view:(document.querySelector('.view.on')||{}).id||''})")
        try: st = json.loads(st)
        except Exception: st = {}
        if st.get('s') or st.get('mask') or st.get('view') != 'v-start':
            break
    # slot picker (only when a save already exists): pick an empty slot.
    if ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button, #slot-list button')].find(x=>x.offsetParent!==null&&/槽 1/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }"):
        pg.wait_for_timeout(1200)
        # overwrite confirm, if any
        click_modal(pg, ['覆蓋開新局', '確定'])
        pg.wait_for_timeout(1000)
    drv.skip_tutorial(pg)
    drv.click_text_in_modal(pg, r'開始寫手帳')
    pg.wait_for_timeout(1000)
    pg.wait_for_function("() => typeof S !== 'undefined' && !!S", timeout=20000)

def seed_main(pg, day=1):
    return ev(pg, """(day) => {
  S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
  S.dayIndex = day;
  S.weekPlan = ['scout_all','street','scout_all','scout_all','scout_all','scout_all','scout_all'];
  S.shoots = []; S.booked = []; S.pendingAud = []; S.aud91Log = [];
  S.grant229Queue = [];
  if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
  ['N1','N2','N3','N4','N5'].forEach(id=>{ S.story.done[id]=true; });
  S.story.flags = Object.assign({}, S.story.flags, {route_tv:true});
  S.flags = Object.assign({}, S.flags, {route_tv:true});
  S.story.routes = {route_tv:true};
  S.travel114 = {day:S.dayIndex, used:0};
  try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
  return S.dayIndex; }""", day)

def click_any(pg, pats):
    return ev(pg, """(pats) => {
      const bs=[...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null&&!b.disabled);
      for(const pat of pats){ const t=bs.find(b=>new RegExp(pat).test(b.textContent||'')); if(t){ t.click(); return (t.textContent||'').trim().slice(0,30); } }
      return null; }""", pats)

def click_modal(pg, pats):
    """Click a button inside #modal only (never a background map/sheet button
    that happens to share the label — e.g. map '返回地圖' behind a story modal)."""
    return ev(pg, """(pats) => {
      const m=document.getElementById('modal'); if(!m) return null;
      const bs=[...m.querySelectorAll('button')].filter(b=>b.offsetParent!==null&&!b.disabled);
      for(const pat of pats){ const t=bs.find(b=>new RegExp(pat).test(b.textContent||'')); if(t){ t.click(); return (t.textContent||'').trim().slice(0,30); } }
      return null; }""", pats)

def play_out_story(pg):
    """Play out story/encounter/reconfirm modals until no mask or no progress.
    Handles WF4 choice nodes: pick first option, then 確定 on the reconfirm.
    All clicks are modal-scoped (see click_modal). Returns True when mask closed.
    Also advances the enc79 star-encounter overlay (#enc79-overlay, a
    full-screen div outside #mask): its finish() re-opens the location sheet
    with encDone:true, so the sheet appears once the overlay is played out."""
    for _ in range(120):
        # enc79 overlay first: it is NOT a #mask modal, so the mask checks
        # below would otherwise return True while it is still open.
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
        if click_modal(pg, ['下一句', '下一頁', '睇落去', '繼續', '完成', '返回地圖', '離開', '跳過', '關閉', '確定']):
            pg.wait_for_timeout(600); continue
        # WF4 choice node: the two options are modal buttons with story-specific
        # labels (no generic pattern matches) — pick the first, then 確定.
        wf4 = ev(pg, "() => { const m=document.getElementById('mask'); if(!(m&&m.classList.contains('wf4-stage-on'))) return false; const b=[...document.querySelectorAll('#modal-btns button')].find(x=>x.offsetParent!==null&&!x.disabled); if(!b) return false; b.click(); return (b.textContent||'').trim().slice(0,30); }")
        if wf4:
            print("WF4_PICK", wf4, flush=True)
            pg.wait_for_timeout(700); continue
        break
    pg.wait_for_timeout(700)
    return not ev(pg, "() => document.getElementById('mask').classList.contains('on')")

def go_map(pg):
    click_any(pg, ['返回地圖']); pg.wait_for_timeout(900)

def reset_travel(pg):
    ev(pg, "() => { if(typeof S!=='undefined' && S){ S.travel114={day:S.dayIndex, used:0}; try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){} } return 'ok'; }")

def open_loc_sheet(pg, loc):
    """Click a map pin; play out story/encounter intercepts; True if sheet open.
    Location entry can queue a WF4 stage after an encounter is walked away from,
    so play out after every pin click (not just before the sheet check)."""
    reset_travel(pg)
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
    print("BOARD_OPEN", r, ev(pg, "() => JSON.stringify({n:document.querySelectorAll('.gig-teaser').length, h3:(document.querySelector('#modal h3')||{}).textContent||null})"), flush=True)
    return True

def modal_h3(pg):
    return ev(pg, "() => { const h=document.querySelector('#modal h3'); return h?(h.textContent||'').trim():null; }")

def save_out(name, obj):
    json.dump(obj, open(f"{OUT}/{name}", 'w'), ensure_ascii=False, indent=1)
    print("SAVED", name, flush=True)


def seed_day(pg, day, plan):
    """Set S.dayIndex + S.weekPlan (indexed by weekdayIdx=day%7, 0=Mon) and
    re-show the map so the day card re-renders. (v396 head helper, rebuilt.)"""
    ev(pg, """(a) => { S.dayIndex=a[0]; S.weekPlan=a[1].slice(); S.travel114={day:a[0], used:0};
      S.homeEditable=false; /* fresh start leaves the planner in edit mode, which
        suppresses #map-start-today via todayHasSoftSchedule() */
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return true; }""", [day, plan])
    pg.wait_for_timeout(300)
    # map hint (with #map-start-today) only re-renders when the map view is
    # re-shown: leave for the notebook, then come back.
    click_any(pg, ['手帳']); pg.wait_for_timeout(1000)
    go_map(pg)
    pg.wait_for_timeout(900)

def run_day_to_card(pg, label):
    """Click 開始今日行程 on the map and play through to the day-end card.
    Returns (ok, state): ok True when a day-end card (res-stat374 rows or a
    開始今日行程 button in #modal-btns) is showing."""
    go_map(pg)
    # NOTE: #map-start-today lives in the (position:fixed) map hint, so its
    # offsetParent is null even while visible — do NOT visibility-gate the
    # click; a programmatic .click() fires the handler regardless.
    ev(pg, """() => { const b=document.getElementById('map-start-today')||document.getElementById('map-end-day');
      if(b){ b.click(); return b.id; } return false; }""")
    pg.wait_for_timeout(1200)
    for _ in range(60):
        st = ev(pg, """() => JSON.stringify({on: document.getElementById('mask').classList.contains('on'),
          h3:(document.querySelector('#modal h3')||{}).textContent||null,
          stats: document.querySelectorAll('#modal .res-stat374').length,
          startBtn: [...document.querySelectorAll('#modal-btns button')].some(x=>x.offsetParent!==null&&/開始今日行程/.test(x.textContent||''))})""")
        try: st = json.loads(st)
        except Exception: st = {}
        if st.get('on') and (st.get('stats') or st.get('startBtn')):
            return True, st
        if not st.get('on'):
            return False, st
        # play_out_story may land exactly on the day-end card and return False
        # (no generic button to click) — loop back and re-check state instead
        # of breaking, so the card is recognised on the next pass.
        play_out_story(pg)
        pg.wait_for_timeout(500)
    return False, {}

# ---------------- probes (v397 baseline / verification) ----------------
LABELS_JS = """() => JSON.stringify((()=>{
  const stage = document.querySelector('.map-well') || document.getElementById('v-map');
  const sr = stage ? stage.getBoundingClientRect() : null;
  const els = [...document.querySelectorAll('.map-names68 .mn68, #map-districts97 .md97-venue99')].filter(e=>e.offsetParent!==null);
  const items = els.map(e=>{ const r=e.getBoundingClientRect();
    return {txt:(e.textContent||'').trim(), cls:e.className, x:+r.x.toFixed(1), y:+r.y.toFixed(1),
      w:+r.width.toFixed(1), h:+r.height.toFixed(1), right:+(r.right).toFixed(1), bottom:+(r.bottom).toFixed(1)}; });
  const overlaps = [];
  for(let i=0;i<items.length;i++) for(let j=i+1;j<items.length;j++){
    const a=items[i], b=items[j];
    const ox=Math.max(0, Math.min(a.right,b.right)-Math.max(a.x,b.x));
    const oy=Math.max(0, Math.min(a.bottom,b.bottom)-Math.max(a.y,b.y));
    if(ox>0 && oy>0) overlaps.push({a:a.txt, b:b.txt, ox:+ox.toFixed(1), oy:+oy.toFixed(1), area:+(ox*oy).toFixed(1)});
  }
  const rc = items.find(x=>x.txt==='紅棉影業'), gj = items.find(x=>x.txt==='金禧大酒店');
  let pairGap = null;
  if(rc && gj){
    const ox=Math.max(0, Math.min(rc.right,gj.right)-Math.max(rc.x,gj.x));
    const oy=Math.max(0, Math.min(rc.bottom,gj.bottom)-Math.max(rc.y,gj.y));
    const gapX = ox>0 ? 0 : Math.max(rc.x-gj.right, gj.x-rc.right);
    const gapY = oy>0 ? 0 : Math.max(rc.y-gj.bottom, gj.y-rc.bottom);
    pairGap = {ox:+ox.toFixed(1), oy:+oy.toFixed(1), gapX:+gapX.toFixed(1), gapY:+gapY.toFixed(1)};
  }
  const stageBottom = sr ? +sr.bottom.toFixed(1) : null;
  const clipped = items.filter(x=> stageBottom!==null && x.bottom > stageBottom + 0.5)
    .map(x=>({txt:x.txt, bottom:x.bottom, stageBottom, over:+(x.bottom-stageBottom).toFixed(1)}));
  const me = document.querySelector('.map-me363');
  const meR = me ? me.getBoundingClientRect() : null;
  return {n: items.length, stageBottom, items, overlaps, pairGap, clipped,
    me: meR ? {x:+meR.x.toFixed(1), y:+meR.y.toFixed(1)} : null}; })())"""

def probe_venue(pg):
    new_game(pg)
    go_map(pg)
    pg.wait_for_timeout(1200)
    res = {}
    res['844'] = json.loads(ev(pg, LABELS_JS))
    shot(pg, 'venue_844_397')
    pg.set_viewport_size({'width': 390, 'height': 682})
    pg.wait_for_timeout(600)
    ev(pg, "() => { try{ if(typeof drawMap==='function') drawMap(); }catch(e){} try{ if(typeof positionMapLabels137==='function') positionMapLabels137(); }catch(e){} return true; }")
    pg.wait_for_timeout(800)
    res['682'] = json.loads(ev(pg, LABELS_JS))
    shot(pg, 'venue_682_397')
    pg.set_viewport_size({'width': 390, 'height': 844})
    pg.wait_for_timeout(600)
    # seeded tall day-card case (audit 06: day 520, 主線限期 day card shrinks the map).
    # N7 (1991夏) + N8 (1991夏/秋) are in window at day 520 when N1-N6 are done,
    # so the deadline line shows; pendingAud + high stress add two more rows.
    ev(pg, """() => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=60;
      S.dayIndex = 520;
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ['N1','N2','N3','N4','N5','N6','N6F'].forEach(id=>{ S.story.done[id]=true; });
      S.pendingAud=[{gigId:'gig_1991_tv_101', title:'冬日鄰里情'}];
      S.wrapHistory = [
        { gigId:'gig_1991_film_102', title:'《霓虹夜影》男主角', type:'電影', totalDays:24, pay:3000, fame:20, popularity:10, wrappedDay:390, rating:'表現穩妥' },
        { gigId:'gig_1990_film_101', title:'《梭哈》男配角', type:'電影', totalDays:4, pay:1200, fame:5, popularity:5, wrappedDay:230, rating:'表現穩妥' },
        { gigId:'gig_1992_rec_102', title:'《硬漢柔情》新人搖滾主唱', type:'唱片通告', totalDays:2, pay:3000, fame:4, popularity:4, wrappedDay:150, rating:'表現穩妥' },
        { gigId:'gig_1991_ad_111', title:'《新春團圓》廣告主角', type:'廣告', totalDays:2, pay:400, fame:40, popularity:8, wrappedDay:395, rating:'順利殺青' },
        { gigId:'gig_1991_variety_107', title:'《夏日繽紛夜》綜藝晚會主持', type:'綜藝', totalDays:2, pay:460, fame:45, popularity:9, wrappedDay:398, rating:'表現穩妥' }
      ];
      try{ if(typeof syncGigsForCalendarYear==='function') syncGigsForCalendarYear(true); }catch(e){}
      try{ if(typeof renderAll==='function') renderAll(); }catch(e){}
      return true; }""")
    # the map hint only re-renders when the map view is re-shown
    click_any(pg, ['手帳']); pg.wait_for_timeout(1000)
    go_map(pg); pg.wait_for_timeout(1200)
    res['seeded844'] = json.loads(ev(pg, LABELS_JS))
    res['seeded844_hint'] = ev(pg, """() => JSON.stringify({hintH: (document.getElementById('map-hint')||{}).offsetHeight||null,
      hintTxt: (document.getElementById('map-hint')||{}).innerText||null})""")
    shot(pg, 'venue_seeded844_397')
    pg.set_viewport_size({'width': 390, 'height': 682})
    pg.wait_for_timeout(600)
    click_any(pg, ['手帳']); pg.wait_for_timeout(1000)
    go_map(pg); pg.wait_for_timeout(1200)
    # entering the map at day 520 can auto-play the pending N7 node; the
    # v396 unload hides the map behind its modal, so play it out first.
    play_out_story(pg); pg.wait_for_timeout(800)
    res['seeded682'] = json.loads(ev(pg, LABELS_JS))
    shot(pg, 'venue_seeded682_397')
    pg.set_viewport_size({'width': 390, 'height': 844})
    pg.wait_for_timeout(600)
    save_out('venue397.json', res)
    return res

def probe_counts(pg):
    res = {}
    pg.goto(URL); pg.wait_for_timeout(2500)
    # audit flow: store E3 save, load-mini, close slot screen, clear save, then 新遊戲
    src = json.load(open('/home/hatch/workspace/linji-ending-targets-2026-11-23/E3_director_ls_backup.json'))
    ev(pg, """(payload) => {
      localStorage.setItem('starVolunteer_map_v19w', payload.S);
      localStorage.setItem('starVolunteer_prefs_v19z9', payload.prefs || '{}');
      return 'stored'; }""", {'S': src['starVolunteer_map_v19w'], 'prefs': src.get('starVolunteer_prefs_v19z9', '{}')})
    ev(pg, "() => { const b=document.getElementById('btn-load-mini'); if(b){ b.click(); return 'clicked'; } return 'missing'; }")
    pg.wait_for_timeout(1500)
    click_any(pg, ['關閉', '返回', '取消']); pg.wait_for_timeout(800)
    ev(pg, "() => { localStorage.removeItem('starVolunteer_map_v19w'); return 'cleared'; }")
    pg.click('#btn-new'); pg.wait_for_timeout(1200)
    res['02b'] = count(pg, '02b')
    ev(pg, "() => { const b=Array.from(document.querySelectorAll('button')).find(x=>/槽|Slot/.test(x.textContent)&&x.offsetParent!==null); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(1200)
    res['03'] = count(pg, '03')
    drv.skip_tutorial(pg)
    drv.click_text_in_modal(pg, r'開始寫手帳')
    pg.wait_for_timeout(1000)
    ev(pg, """() => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=120; S.money=9000; S.stress=20;
      S.dayIndex = 1; S.homeEditable = true;
      S.weekPlan = ['train_acting','street','rest','train_vocal','cafe_gig','shoot:dummy','scout_all'];
      try{ if(typeof renderNotebook==='function') renderNotebook(); }catch(e){}
      return true; }""")
    pg.wait_for_timeout(900)
    res['11d'] = count(pg, '11d')
    res['11d_tools'] = ev(pg, """() => JSON.stringify({
      quick:[...document.querySelectorAll('#nb-quick button')].filter(x=>x.offsetParent!==null).map(x=>x.id||x.textContent.trim()),
      toolsMenu: !!document.getElementById('nb-tools397-menu'),
      resetVisible: !!(document.getElementById('btn-reset-plan')&&document.getElementById('btn-reset-plan').offsetParent!==null),
      catTabs:[...document.querySelectorAll('#cat-tabs button')].filter(x=>x.offsetParent!==null).map(x=>x.textContent.trim()) })""")
    shot(pg, 'counts_11d_397')
    go_map(pg)
    ev(pg, "() => { const b=document.getElementById('btn-menu'); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(900)
    res['24_menu'] = count(pg, '24_menu')
    res['menu_btns'] = ev(pg, """() => JSON.stringify([...document.querySelectorAll('#menu button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim()))""")
    shot(pg, 'counts_menu_397')
    ev(pg, "() => { const b=document.getElementById('btn-menu'); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(600)
    ev(pg, """() => {
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ['R_hiu_meet','R_choi_meet','R_lan_meet','R_xu_meet','R_yip_meet','R_so_meet'].forEach(id=>{ S.story.done[id]=true; });
      S.travel114={day:S.dayIndex, used:0};
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return true; }""")
    ok = open_loc_sheet(pg, 'cafe_cha')
    res['intel_sheet'] = ok
    res['intel_count'] = count(pg, 'intel')
    res['intel_acts'] = ev(pg, """() => JSON.stringify([...document.querySelectorAll('#loc-acts .act')].map(x=>({t:(x.querySelector('.n')||x).textContent.trim().slice(0,30), h:(x.querySelector('.h')||{}).textContent||''})))""")
    shot(pg, 'counts_intel_397')
    save_out('counts397.json', res)
    return res

def probe_counts33b(pg):
    res = {}
    src = json.load(open('/home/hatch/workspace/linji-ending-targets-2026-11-23/E3_director_ls_backup.json'))
    pg.goto(URL); pg.wait_for_timeout(2500)
    ev(pg, """(payload) => {
      localStorage.setItem('starVolunteer_map_v19w', payload.S);
      localStorage.setItem('starVolunteer_prefs_v19z9', payload.prefs || '{}');
      return 'stored'; }""", {'S': src['starVolunteer_map_v19w'], 'prefs': src.get('starVolunteer_prefs_v19z9', '{}')})
    ev(pg, "() => { const b=document.getElementById('btn-load-mini'); if(b){ b.click(); return 'clicked'; } return 'missing'; }")
    pg.wait_for_timeout(2000)
    # btn-load-mini opens the slot picker; load the E3 save in slot 1 first.
    ev(pg, """() => { const b=[...document.querySelectorAll('#slot-list [data-slot="1"]')].find(x=>x.offsetParent!==null); if(b){ b.click(); return 'slot1'; } return 'noslot'; }""")
    pg.wait_for_timeout(2000)
    res['after_load'] = ev(pg, """() => JSON.stringify({view:(document.querySelector('.view.on')||{}).id||'',
      h3:(document.querySelector('#modal h3')||{}).textContent||null,
      btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim()),
      body:(document.getElementById('modal-inner')||{}).innerText.slice(0,200)||null})""")
    # the E3 save opens with a pending multi-page newspaper modal; page
    # through it (下一頁) until 收下這份剪報 appears, then dismiss.
    for _ in range(8):
        if click_modal(pg, ['收下這份剪報', '收下剪報']):
            pg.wait_for_timeout(800); break
        if not click_modal(pg, ['下一頁']):
            break
        pg.wait_for_timeout(700)
    play_out_story(pg)
    res['after_paper'] = ev(pg, """() => JSON.stringify({mask:document.getElementById('mask').className,
      h3:(document.querySelector('#modal h3')||{}).textContent||null,
      btns:[...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim().slice(0,16))})""")
    r33 = click_any(pg, ['睇手帳總結'])
    print('REVIEW_BTN', r33, flush=True)
    pg.wait_for_timeout(1200)
    r33b = click_any(pg, ['回顧手帳'])
    print('REVIEW_BTN2', r33b, flush=True)
    pg.wait_for_timeout(1200)
    res['33b'] = count(pg, '33b')
    res['33b_state'] = ev(pg, """() => JSON.stringify({view:(document.querySelector('.view.on')||{}).id||'',
      editable: (typeof S!=='undefined'&&S)?!!S.homeEditable:null,
      catTabsVisible: [...document.querySelectorAll('#cat-tabs button')].filter(x=>x.offsetParent!==null).length,
      dayRows: [...document.querySelectorAll('#nb-days button')].filter(x=>x.offsetParent!==null).length,
      intelVisible: !!(document.getElementById('btn-intel381')&&document.getElementById('btn-intel381').offsetParent!==null)})""")
    shot(pg, 'counts_33b_397')
    save_out('counts33b397.json', res)
    return res

def probe_intel_date(pg):
    """v397-5c: 約人出街入口端到端——入內揀人 → 開日期地點 picker → 返回返地點面板。"""
    new_game(pg)
    ev(pg, """() => {
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ['R_hiu_meet','R_choi_meet','R_lan_meet','R_xu_meet','R_yip_meet','R_so_meet'].forEach(id=>{ S.story.done[id]=true; });
      S.travel114={day:S.dayIndex, used:0};
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return true; }""")
    ok = open_loc_sheet(pg, 'cafe_cha')
    res = {'sheet': ok}
    if ok:
        clicked = click_any(pg, ['約人出街'])
        pg.wait_for_timeout(1000)
        res['who_picker'] = ev(pg, """() => JSON.stringify({h3:(document.querySelector('#modal h3')||{}).textContent||null,
          whos:[...document.querySelectorAll('[data-date-who]')].map(x=>x.textContent.trim().slice(0,24)),
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim())})""")
        shot(pg, 'intel_who_397')
        # pick the first woman -> date-spot picker should open
        ev(pg, """() => { const b=document.querySelector('[data-date-who]'); if(b){ b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1000)
        res['spot_picker'] = ev(pg, """() => JSON.stringify({h3:(document.querySelector('#modal h3')||{}).textContent||null,
          spots:[...document.querySelectorAll('[data-date-spot]')].map(x=>x.textContent.trim().slice(0,30)),
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim())})""")
        shot(pg, 'intel_spot_397')
        # cancel back to the location sheet
        click_modal(pg, ['取消'])
        pg.wait_for_timeout(1200)
        res['back_to_sheet'] = ev(pg, """() => JSON.stringify({sheetTitle:(document.querySelector('#loc-sheet .loc-title')||document.querySelector('#loc-sheet h3')||{}).textContent||null,
          acts:[...document.querySelectorAll('#loc-acts .act')].map(x=>(x.querySelector('.n')||x).textContent.trim().slice(0,20))})""")
    save_out('intel_date397.json', res)
    return res

def probe_board_low(pg):
    """v397-3d 低 stats：驗證鎖定摘要移去可接清單最尾（修前基線排第 2）。"""
    new_game(pg)
    ev(pg, """() => {
      S.acting=10; S.stage=10; S.vocal=10; S.looks=10; S.charm=10; S.iq=10; S.stamina=40; S.fame=5; S.money=1200; S.stress=20;
      S.dayIndex = 1;
      S.weekPlan = ['scout_all','street','scout_all','scout_all','scout_all','scout_all','scout_all'];
      S.shoots = []; S.booked = []; S.pendingAud = []; S.aud91Log = [];
      S.grant229Queue = [];
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ['N1','N2','N3','N4','N5'].forEach(id=>{ S.story.done[id]=true; });
      S.story.flags = Object.assign({}, S.story.flags, {route_tv:true});
      S.flags = Object.assign({}, S.flags, {route_tv:true});
      S.story.routes = {route_tv:true};
      S.travel114 = {day:S.dayIndex, used:0};
      return true;
    }""")
    assert open_board(pg), "board open failed"
    res = ev(pg, """() => JSON.stringify({
      sum:(document.querySelector('.board-sum392')||{}).innerText||null,
      listOrder: [...document.querySelectorAll('#gig-board-list > *')].map(x=> x.classList.contains('gig-locked108') ? 'LOCKED-DETAILS' : ((x.querySelector('.gt-title')||{}).textContent||x.tagName).slice(0,20)),
      lockedIdx: [...document.querySelectorAll('#gig-board-list > *')].findIndex(x=>x.classList.contains('gig-locked108')),
      nChildren: document.querySelectorAll('#gig-board-list > *').length,
      lockedSummary:(document.querySelector('.gig-locked108 summary')||{}).textContent||null })""")
    save_out('board_low397.json', res)
    return res

def probe_board(pg):
    new_game(pg)
    seed_main(pg, 1)
    assert open_board(pg), "board open failed"
    res = {}
    res['count'] = count(pg, 'board_peak')
    res['head'] = ev(pg, """() => JSON.stringify({
      lead:(document.querySelector('.board-lead')||{}).innerText||null,
      sum:(document.querySelector('.board-sum392')||{}).innerText||null,
      sortBtns:[...document.querySelectorAll('.board-sort392 button')].map(x=>x.textContent.trim()),
      filterBtns:[...document.querySelectorAll('.board-filter392 button')].map(x=>x.textContent.trim()),
      headH: (()=>{ const h=document.querySelector('.board-head392'); if(!h) return null; const r=h.getBoundingClientRect(); return +r.height.toFixed(1); })(),
      nCards: document.querySelectorAll('.gig-teaser').length,
      listOrder: [...document.querySelectorAll('#gig-board-list > *')].map(x=> x.classList.contains('gig-locked108') ? 'LOCKED-DETAILS' : ((x.querySelector('.gt-title')||{}).textContent||x.tagName).slice(0,20)),
      lockedSummary:(document.querySelector('.gig-locked108 summary')||{}).textContent||null })""")
    res['exp82'] = ev(pg, """() => JSON.stringify((()=>{
      const cards=[...document.querySelectorAll('.gig-teaser')];
      const c=cards.find(x=>/預期 \\$82／日/.test(x.textContent||''));
      if(!c) return {found:false, metas:cards.slice(0,4).map(x=>(x.querySelector('.gt-meta-line')||{}).textContent||null)};
      return {found:true, gid:c.dataset.gid, title:(c.querySelector('.gt-title')||{}).textContent||null,
        meta:(c.querySelector('.gt-meta-line')||{}).textContent||null,
        boardIds:(S.board&&S.board['tvb_longmen'])||[]}; })())""")
    ev(pg, """() => { const c=document.querySelector('.gig-teaser'); if(c) c.click(); return !!c; }""")
    pg.wait_for_timeout(1200)
    res['detail'] = ev(pg, """() => JSON.stringify({h3:(document.querySelector('#modal h3')||{}).textContent||null,
      hasCalc: /預期日薪/.test((document.getElementById('modal-inner')||{}).innerText||''),
      calcLine: (()=>{ const el=document.querySelector('.board-expcalc397'); return el?el.textContent:null; })(),
      bodyHas: ((document.getElementById('modal-inner')||{}).innerText||'').slice(0,600) })""")
    shot(pg, 'board_detail_397')
    save_out('board397.json', res)
    return res

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
    res['present'] = ev(pg, """() => JSON.stringify({sheetFound: !!document.querySelector('.paper-sheet'),
      outcome: (S.pendingAwardPack||{}).bestOutcome || ((S.awardBooked213||{}).pack||{}).bestOutcome || null})""")
    res['p1_first'] = ev(pg, """() => JSON.stringify((()=>{
      const mi=document.getElementById('modal-inner'); const mr=mi.getBoundingClientRect();
      const cap=document.querySelector('.np214-page.on .np214-caption');
      const cr=cap?cap.getBoundingClientRect():null;
      const sb=document.querySelector('.np214-page.on .np214-sidebar');
      const sbr=sb?sb.getBoundingClientRect():null;
      const sbP=sb?sb.querySelector('p'):null;
      const sbPr=sbP?sbP.getBoundingClientRect():null;
      const mast=document.querySelector('.np214-page.on .np214-masthead');
      const mstR=mast?mast.getBoundingClientRect():null;
      return {miTop:+mr.top.toFixed(1), miBottom:+mr.bottom.toFixed(1), miH:mi.clientHeight, miScrollH:mi.scrollHeight,
        mastH: mstR?+mstR.height.toFixed(1):null,
        caption: cr?{top:+cr.top.toFixed(1), bottom:+cr.bottom.toFixed(1), fullyVisible: cr.bottom<=mr.bottom+0.5, text:cap.textContent.slice(0,60)}:null,
        sidebar: sbr?{top:+sbr.top.toFixed(1), bottom:+sbr.bottom.toFixed(1)}:null,
        sidebarP: sbPr?{top:+sbPr.top.toFixed(1), bottom:+sbPr.bottom.toFixed(1), text:(sbP.textContent||'').slice(0,60)}:null,
        fillerV: !!document.querySelector('.np214-page.on .np214-filler-v'),
        sbMark: !!document.querySelector('.np214-page.on .np214-sb-mark397')}; })())""")
    shot(pg, '35c_top_397')
    ev(pg, "() => { const mi=document.getElementById('modal-inner'); if(mi) mi.scrollTop = mi.scrollHeight; return true; }")
    pg.wait_for_timeout(600)
    res['p1_bottom'] = ev(pg, """() => JSON.stringify((()=>{
      const mi=document.getElementById('modal-inner'); const mr=mi.getBoundingClientRect();
      const ps=[...document.querySelectorAll('.np214-page.on .np214-sidebar p')].map(p=>{ const r=p.getBoundingClientRect();
        return {text:(p.textContent||'').slice(0,50), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
          fullyVisible: r.top>=mr.top-0.5 && r.bottom<=mr.bottom+0.5}; });
      const last=[...document.querySelectorAll('.paper-sheet .np214-page.on p')].pop();
      const lr=last?last.getBoundingClientRect():null;
      return {miBottom:+mr.bottom.toFixed(1), sidebarPs:ps,
        lastP: lr?{text:(last.textContent||'').slice(0,40), bottom:+lr.bottom.toFixed(1)}:null,
        scrollTop: mi.scrollTop, scrollH: mi.scrollHeight}; })())""")
    shot(pg, '35c_bottom_397')
    click_any(pg, ['第二版']); pg.wait_for_timeout(900)
    res['p2'] = ev(pg, """() => JSON.stringify((()=>{
      const p2=document.querySelector('.np214-page[data-np214-page="2"]');
      if(!p2) return {on:false};
      const dek=(p2.querySelector('.np214-dek')||{}).textContent||null;
      const lead=(p2.querySelector('.np214-body2 .np214-lead')||{}).textContent||null;
      const cap=(p2.querySelector('.np214-caption')||{}).textContent||null;
      const head=(p2.querySelector('.np214-headline2')||{}).textContent||null;
      const mi=document.getElementById('modal-inner'); const mr=mi.getBoundingClientRect();
      const capEl=p2.querySelector('.np214-caption'); const cr=capEl?capEl.getBoundingClientRect():null;
      return {on:p2.classList.contains('on'), head, dek, lead, cap,
        captionFirst: cr?{top:+cr.top.toFixed(1), bottom:+cr.bottom.toFixed(1), fullyVisible: cr.bottom<=mr.bottom+0.5}:null,
        miBottom:+mr.bottom.toFixed(1)}; })())""")
    shot(pg, '35c_page2_397')
    ev(pg, "() => { const mi=document.getElementById('modal-inner'); if(mi) mi.scrollTop = mi.scrollHeight; return true; }")
    pg.wait_for_timeout(600)
    res['p2_bottom'] = ev(pg, """() => JSON.stringify((()=>{
      const mi=document.getElementById('modal-inner'); const mr=mi.getBoundingClientRect();
      const p2=document.querySelector('.np214-page[data-np214-page="2"]');
      const fb=p2?p2.querySelector('.np214-factbox'):null;
      const fr=fb?fb.getBoundingClientRect():null;
      const sbPs=[...document.querySelectorAll('.np214-page[data-np214-page="2"] .np214-sidebar p')].map(p=>{ const r=p.getBoundingClientRect();
        return {text:(p.textContent||'').slice(0,50), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
          fullyVisible: r.top>=mr.top-0.5 && r.bottom<=mr.bottom+0.5}; });
      return {miBottom:+mr.bottom.toFixed(1), factbox: fr?{bottom:+fr.bottom.toFixed(1), fullyVisible: fr.bottom<=mr.bottom+0.5}:null, sidebarPs:sbPs}; })())""")
    shot(pg, '35c_page2_bottom_397')
    save_out('awards35c397.json', res)
    return res

def probe_dayres(pg):
    new_game(pg)
    res = {}
    seed_day(pg, 17, ['scout_all', 'scout_all', 'scout_all', 'rest', 'cafe_gig', 'scout_all', 'scout_all'])
    ok0, j0 = run_day_to_card(pg, '休息')
    res['rest_found'] = ok0
    res['rest_card'] = ev(pg, """() => JSON.stringify({
      maskCls: document.getElementById('mask').className,
      maskBgImg: getComputedStyle(document.getElementById('mask')).backgroundImage,
      appCls: document.getElementById('app').className,
      vmapVisible: !!(document.getElementById('v-map')&&document.getElementById('v-map').offsetParent!==null),
      pinsVisible: [...document.querySelectorAll('.pin')].filter(x=>x.offsetParent!==null).length,
      mapImgVisible: (()=>{ const im=document.getElementById('map-img'); if(!im) return null; const r=im.getBoundingClientRect(); return {w:+r.width.toFixed(0), h:+r.height.toFixed(0), vis: im.offsetParent!==null}; })(),
      dateLine:(document.querySelector('.dayres-date374')||{}).textContent||null,
      btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>({t:(x.textContent||'').trim(), cls:x.className})) })""")
    shot(pg, 'dayres_rest_397')
    click_modal(pg, ['開始今日行程']); pg.wait_for_timeout(1200)
    res['got40'] = ev(pg, "() => (document.querySelector('#modal h3')||{}).textContent||null") == '開始今日行程？'
    if res['got40']:
        res['modal40'] = ev(pg, """() => JSON.stringify({
          maskCls: document.getElementById('mask').className,
          appCls: document.getElementById('app').className,
          maskBgImg: getComputedStyle(document.getElementById('mask')).backgroundImage,
          vmapVisible: !!(document.getElementById('v-map')&&document.getElementById('v-map').offsetParent!==null),
          pinsVisible: [...document.querySelectorAll('.pin')].filter(x=>x.offsetParent!==null).length,
          modalRect: (()=>{ const r=document.getElementById('modal').getBoundingClientRect(); return {y:+r.y.toFixed(1), h:+r.height.toFixed(1), bottom:+r.bottom.toFixed(1)}; })(),
          text:(document.getElementById('modal-inner')||{}).innerText||null,
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>({t:(x.textContent||'').trim(), cls:x.className})) })""")
        shot(pg, 'dayres_40_397')
        pg.mouse.click(195, 120); pg.wait_for_timeout(1500)
        res['after_dismiss40'] = ev(pg, """() => JSON.stringify({day:S.dayIndex,
          h3:(document.querySelector('#modal h3')||{}).textContent||null})""")
    save_out('dayres40_397.json', res)
    return res

def probe_dayres2(pg):
    # Two fresh games: D1 (week-end card) first, then a NEW game for D2.
    # Chaining D2 after D1 in one game breaks (backward time jump downgrades
    # the training act to 小休); chaining D1 after D2 breaks the same way
    # (the open D2 card blocks the re-seed).
    new_game(pg)
    res = {}
    seed_day(pg, 20, ['scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'rest'])
    ok, j = run_day_to_card(pg, '休息')
    res['D1_found'] = ok
    if ok:
        res['D1_card'] = ev(pg, """() => JSON.stringify({day:S.dayIndex,
          h3:(document.querySelector('#modal h3')||{}).textContent||null,
          dateLine:(document.querySelector('.dayres-date374')||{}).textContent||null,
          gold:(document.querySelector('#modal .gold')||{}).textContent||null,
          stamp:(document.querySelector('#modal .dayres-stamp397')||{}).textContent||null,
          bodyHasHomeSettle: (document.getElementById('modal-inner')||{}).innerText.indexOf('回家結算')>=0,
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim())})""")
        shot(pg, 'dayres_86c_397')
    new_game(pg)
    seed_day(pg, 17, ['scout_all', 'scout_all', 'scout_all', 'train_acting', 'cafe_gig', 'scout_all', 'scout_all'])
    ok2, j2 = run_day_to_card(pg, '訓練')
    res['D2_found'] = ok2
    if ok2:
        res['D2_card'] = ev(pg, """() => JSON.stringify({day:S.dayIndex,
          h3:(document.querySelector('#modal h3')||{}).textContent||null,
          dateLine:(document.querySelector('.dayres-date374')||{}).textContent||null,
          statRows: document.querySelectorAll('#modal .res-stat374').length,
          ledger:(document.querySelector('#modal .dayres-ledger397')||{}).textContent||null,
          text:(document.getElementById('modal-inner')||{}).innerText||null,
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim())})""")
        shot(pg, 'dayres_27c_397')
    save_out('dayres2_397.json', res)
    return res


PROBES = {'venue': probe_venue, 'counts': probe_counts, 'counts33b': probe_counts33b,
          'board': probe_board, 'board_low': probe_board_low, 'awards': probe_awards, 'dayres': probe_dayres,
          'dayres2': probe_dayres2, 'intel_date': probe_intel_date}

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox',
        '--proxy-server=http://127.0.0.1:18081', '--ignore-certificate-errors'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: print('PAGEERR', str(e)[:200], flush=True))
    todo = ['venue', 'counts', 'counts33b', 'board', 'awards', 'dayres', 'dayres2'] if 'all' in ITEMS else ITEMS
    for name in todo:
        print("===== PROBE", name, "=====", flush=True)
        try:
            PROBES[name](pg)
        except Exception as e:
            print("PROBE_FAIL", name, repr(e)[:400], flush=True)
        try:
            pg.goto(URL); pg.wait_for_timeout(800)
        except Exception:
            pass
    b.close()
srv.terminate()
print("DONE", flush=True)
