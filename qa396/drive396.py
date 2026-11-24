# -*- coding: utf-8 -*-
"""v396 UI fixes (audit round 4, top 5): real-drive verification.
Serves ~/workspace/linji-work396 locally, Playwright headless shell via
local CONNECT relay. Usage:
  /home/hatch/pwenv49/bin/python qa396/drive396.py board|shops|modalbg|rest40|dismiss|awards|menuledger [all]
Results JSON + screenshots -> qa396/verify/ and qa396/shots/.
Only measures / drives; never edits code or MEMORY.md.
"""
import sys, os, json, socket, subprocess, time, urllib.request
sys.path.insert(0, '/home/hatch/workspace/fullarc')
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/hatch/pw-browsers')
from playwright.sync_api import sync_playwright
import driver as drv

ITEMS = sys.argv[1:] or ['board']
ROOT = "/home/hatch/workspace/linji-work396"
OUT = "/home/hatch/workspace/linji-work396/qa396/verify"
SHOTS = "/home/hatch/workspace/linji-work396/qa396/shots"
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
    pg.goto(URL); pg.wait_for_timeout(2500)
    pg.click('#btn-new'); pg.wait_for_timeout(800)
    drv.skip_tutorial(pg)
    drv.click_text_in_modal(pg, r'開始寫手帳')
    pg.wait_for_timeout(1000)
    try: pg.wait_for_function("() => typeof S !== 'undefined' && !!S", timeout=20000)
    except Exception:
        print("NEWGAME_RETRY", flush=True)
        pg.goto(URL); pg.wait_for_timeout(2500)
        pg.click('#btn-new'); pg.wait_for_timeout(800)
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
    All clicks are modal-scoped (see click_modal). Returns True when mask closed."""
    for _ in range(120):
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
        if click_modal(pg, ['下一句', '睇落去', '繼續', '完成', '返回地圖', '離開', '跳過', '關閉', '確定']):
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

# ---------------- probes ----------------
def probe_board(pg):
    new_game(pg)
    seed_main(pg, 1)
    assert open_board(pg), "board open failed"
    res = {}
    res['count'] = count(pg, 'board_peak')
    shot(pg, 'board_peak_396')
    res['head'] = ev(pg, """() => JSON.stringify({
      h3:(document.querySelector('#modal h3')||{}).textContent||null,
      lead:(document.querySelector('.board-lead')||{}).innerText||null,
      sum:(document.querySelector('.board-sum392')||{}).innerText||null,
      sort:(document.querySelector('.board-sort392')||{}).innerText||null,
      filter:(document.querySelector('.board-filter392')||{}).innerText||null,
      nCards: document.querySelectorAll('.gig-teaser').length,
      modalInnerH: (document.getElementById('modal-inner')||{}).clientHeight||null,
      listScrollH: (document.getElementById('gig-board-list')||{}).scrollHeight||null })""")
    res['cards'] = ev(pg, """() => JSON.stringify([...document.querySelectorAll('.gig-teaser')].map(c=>{
      const t=c.querySelector('.gt-title'), s=c.querySelector('.g-seal');
      // text rects (not the element box: padding-right is inside the box, so the
      // element always extends under the seal — measure the actual glyphs)
      let textRight=null, textTop=null, textBottom=null;
      try{
        const range=document.createRange(); range.selectNodeContents(t);
        const rs=[...range.getClientRects()];
        if(rs.length){ textRight=Math.max(...rs.map(r=>r.right)); textTop=Math.min(...rs.map(r=>r.top)); textBottom=Math.max(...rs.map(r=>r.bottom)); }
      }catch(_e){}
      const sr=s?s.getBoundingClientRect():null;
      const gap=(textRight!=null&&sr)? +(sr.left-textRight).toFixed(1) : null;
      const ovY=(textTop!=null&&sr)? Math.max(0, Math.min(textBottom,sr.bottom)-Math.max(textTop,sr.top)) : null;
      return {title:(t?t.textContent:'').trim(), pills:[...c.querySelectorAll('.gt-pill')].map(x=>x.textContent.trim()),
        meta:(c.querySelector('.gt-meta-line')||{}).textContent||null,
        h:+c.getBoundingClientRect().height.toFixed(1),
        textRight: textRight?+textRight.toFixed(1):null, sealLeft: sr?+sr.left.toFixed(1):null,
        gapToSeal: gap, overlapY: ovY?+ovY.toFixed(1):null, featured: c.classList.contains('gt-featured')}; }))""")
    res['first_screen'] = ev(pg, """() => JSON.stringify((()=>{
      const mi=document.getElementById('modal-inner'); if(!mi) return null;
      const mb=mi.getBoundingClientRect().bottom;
      const cards=[...document.querySelectorAll('.gig-teaser')];
      let full=0, partial=null;
      cards.forEach(c=>{ const r=c.getBoundingClientRect();
        if(r.bottom<=mb+0.5) full++;
        else if(partial===null && r.top<mb) partial={title:(c.querySelector('.gt-title')||{}).textContent||'', visiblePx:+(mb-r.top).toFixed(1)}; });
      return {full, partial, modalInnerBottom:+mb.toFixed(1)}; })())""")
    res['board_gigs'] = ev(pg, """() => JSON.stringify((()=>{
      const ids=(S.board&&S.board['tvb_longmen'])||[];
      return ids.map(id=>{ const g=(typeof GIGS!=='undefined'?GIGS:[]).find(x=>x&&x.id===id)||{};
        return {id, type:g.type||null, genre:g.genreLabel||null, coarse:(typeof gigTypeCoarse==='function'?gigTypeCoarse(g):null)}; }); })())""")
    # sort switch: click 總片酬, then filter 電視劇
    btn = ev(pg, """() => { const b=[...document.querySelectorAll('#modal button')].find(x=>/總片酬/.test(x.textContent||'')); if(!b) return null; const r=b.getBoundingClientRect(); return {x:r.x+r.width/2, y:r.y+r.height/2}; }""")
    if btn:
        pg.mouse.click(btn['x'], btn['y']); pg.wait_for_timeout(1000)
        res['after_pay_sort'] = ev(pg, """() => JSON.stringify({sum:(document.querySelector('.board-sum392')||{}).innerText||null,
          firstMeta:(document.querySelector('.gig-teaser .gt-meta-line')||{}).textContent||null,
          firstTitle:(document.querySelector('.gig-teaser .gt-title')||{}).textContent||null})""")
    btn2 = ev(pg, """() => { const b=[...document.querySelectorAll('#modal button')].find(x=>x.textContent.trim()==='電視劇'); if(!b) return null; const r=b.getBoundingClientRect(); return {x:r.x+r.width/2, y:r.y+r.height/2}; }""")
    if btn2:
        pg.mouse.click(btn2['x'], btn2['y']); pg.wait_for_timeout(1000)
        res['after_tv_filter'] = ev(pg, """() => JSON.stringify({sum:(document.querySelector('.board-sum392')||{}).innerText||null,
          n:document.querySelectorAll('.gig-teaser').length,
          pills:[...document.querySelectorAll('.gig-teaser .gt-pill')].map(x=>x.textContent.trim())})""")
        res['count_tv'] = count(pg, 'board_tv_filter')
    shot(pg, 'board_filtered_396')
    save_out('board396.json', res)
    return res

def probe_shops(pg):
    new_game(pg)
    seed_main(pg, 1)
    res = {}
    # gift shop: 廟街禮品 — find its pin by scanning pins for gift loc
    locs = ev(pg, """() => JSON.stringify([...document.querySelectorAll('.pin')].map(p=>p.getAttribute('data-loc')))""")
    print("PINS", locs, flush=True)
    res['pins'] = locs
    for loc, act, key in [('gift_shop', '買禮物', 'gift'), ('temple_gift', '買禮物', 'gift'), ('gift_street', '買禮物', 'gift'),
                          ('clothing_shop', '買衫', 'wardrobe')]:
        if loc not in (locs or []):
            continue
        ok = open_loc_sheet(pg, loc)
        print("SHOP_SHEET", loc, ok, flush=True)
        if not ok:
            continue
        r = ev(pg, """(act) => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>x.textContent.indexOf(act)>=0); if(b) b.click(); return !!b; }""", act)
        pg.wait_for_timeout(1200)
        res[key] = {'act_found': r,
                    'h3': modal_h3(pg),
                    'count': count(pg, f'shop_{key}'),
                    'rows': ev(pg, """() => JSON.stringify([...document.querySelectorAll('#modal [data-buy], #modal [data-buy265]')].map(b=>({tag:b.tagName, id:b.getAttribute('data-buy')||b.getAttribute('data-buy265'), disabled:!!b.disabled, text:(b.textContent||'').trim().slice(0,60)})))"""),
                    'money': ev(pg, "() => (typeof S!=='undefined'&&S)?S.money:null")}
        shot(pg, f'shop_{key}_396')
        # close via 關閉
        click_any(pg, ['關閉']); pg.wait_for_timeout(800)
    # buy-flow verification: gift — select cheapest row, buy, confirm, money drops
    if res.get('gift'):
        ok = open_loc_sheet(pg, 'gift_shop')
        ev(pg, """() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>x.textContent.indexOf('買禮物')>=0); if(b) b.click(); return !!b; }""")
        pg.wait_for_timeout(1200)
        before = ev(pg, "() => S.money")
        ev(pg, """() => { const r=document.querySelector('[data-buy="gift_pineapple_bun_set"]'); if(r) r.click(); return !!r; }""")
        pg.wait_for_timeout(400)
        buy_label = ev(pg, """() => { const b=document.querySelector('#modal-btns .shop-buy396'); return b ? b.textContent : null; }""")
        click_modal(pg, ['購買']); pg.wait_for_timeout(800)
        reconfirm = modal_h3(pg)
        click_modal(pg, ['確定']); pg.wait_for_timeout(1200)
        res['buy_gift'] = {'money_before': before, 'money_after': ev(pg, "() => S.money"),
            'buy_label_after_select': buy_label, 'reconfirm_h3': reconfirm,
            'shop_reopened': ev(pg, "() => !!document.querySelector('#gift-shop-list')"),
            'row_left_now': ev(pg, """() => { const r=document.querySelector('[data-buy="gift_pineapple_bun_set"]'); return r ? r.textContent.replace(/\\s+/g,' ').slice(0,60) : null; }"""),
            'inv': ev(pg, "() => (typeof GiftShop!=='undefined'&&GiftShop.inventoryList) ? JSON.stringify(GiftShop.inventoryList().map(x=>x.itemId||x.id||x.name)) : null")}
        click_any(pg, ['關閉']); pg.wait_for_timeout(800)
    # buy-flow verification: wardrobe — select c1, buy, confirm, money drops, owned
    ok = open_loc_sheet(pg, 'clothing_shop')
    if ok:
        ev(pg, """() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>x.textContent.indexOf('買衫')>=0); if(b) b.click(); return !!b; }""")
        pg.wait_for_timeout(1200)
        before = ev(pg, "() => S.money")
        ev(pg, """() => { const r=document.querySelector('[data-buy265="c1"]'); if(r) r.click(); return !!r; }""")
        pg.wait_for_timeout(400)
        buy_label = ev(pg, """() => { const b=document.querySelector('#modal-btns .shop-buy396'); return b ? b.textContent : null; }""")
        click_modal(pg, ['購買']); pg.wait_for_timeout(800)
        reconfirm = modal_h3(pg)
        click_modal(pg, ['確定']); pg.wait_for_timeout(1200)
        res['buy_wardrobe'] = {'money_before': before, 'money_after': ev(pg, "() => S.money"),
            'buy_label_after_select': buy_label, 'reconfirm_h3': reconfirm,
            'shop_reopened': ev(pg, "() => !!document.querySelector('#clothing-shop265-list')"),
            'row_now': ev(pg, """() => { const r=document.querySelector('[data-buy265="c1"]'); return r ? r.textContent.replace(/\\s+/g,' ').slice(0,60) : null; }""")}
        click_any(pg, ['關閉']); pg.wait_for_timeout(800)
    # buy with nothing selected: toast prompt, modal stays open
    ok = open_loc_sheet(pg, 'gift_shop')
    if ok:
        ev(pg, """() => { const b=[...document.querySelectorAll('#loc-acts .act, #loc-acts button')].find(x=>x.textContent.indexOf('買禮物')>=0); if(b) b.click(); return !!b; }""")
        pg.wait_for_timeout(1200)
        click_modal(pg, ['購買']); pg.wait_for_timeout(600)
        res['buy_nothing'] = {'mask_on': ev(pg, "() => document.getElementById('mask').classList.contains('on')"),
            'h3': modal_h3(pg)}
        click_any(pg, ['關閉']); pg.wait_for_timeout(800)
    save_out('shops396.json', res)
    return res

def probe_modalbg(pg):
    new_game(pg)
    seed_main(pg, 1)
    res = {}
    res['map_count'] = count(pg, 'map_plain')
    # pin position on the plain map BEFORE the modal opens (while hidden the
    # pin has no rect, so the click point must be captured up front)
    go_map(pg)
    pin_xy = ev(pg, """() => { const p=document.querySelector('.pin[data-loc="film_lion"]'); if(!p) return null; const r=p.getBoundingClientRect(); return {x:r.x+r.width/2, y:r.y+r.height/2}; }""")
    res['pin_xy_before'] = pin_xy
    assert open_board(pg), "board open failed"
    res['board_count'] = count(pg, 'board_modal_open')
    res['under'] = ev(pg, """() => JSON.stringify({
      vmapInert: document.getElementById('v-map').hasAttribute('inert'),
      vmapVis: getComputedStyle(document.getElementById('v-map')).visibility,
      vmapPE: getComputedStyle(document.getElementById('v-map')).pointerEvents,
      sheetInert: (document.getElementById('loc-sheet')||{}).hasAttribute ? document.getElementById('loc-sheet').hasAttribute('inert') : null,
      appCls: document.getElementById('app').className,
      pinRect: (()=>{ const p=document.querySelector('.pin[data-loc="film_lion"]'); if(!p) return null; const r=p.getBoundingClientRect(); return {x:+r.x.toFixed(1), y:+r.y.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1), visible: p.offsetParent!==null}; })(),
      pinAtPoint: (()=>{ const p=document.querySelector('.pin[data-loc="film_lion"]'); if(!p) return null; const r=p.getBoundingClientRect(); const el=document.elementFromPoint(r.x+r.width/2, r.y+r.height/2); return el ? (el.id||el.className||el.tagName) : null; })() })""")
    # real mouse click on the pin's (pre-modal) map position while modal open:
    # must NOT open a location — the click lands on the mask (standard dismiss
    # path) or is swallowed; day must not advance, no location modal may open.
    if pin_xy:
        pg.mouse.click(pin_xy['x'], pin_xy['y']); pg.wait_for_timeout(900)
        res['after_pin_click'] = ev(pg, """() => JSON.stringify({maskOn: document.getElementById('mask').classList.contains('on'),
          h3:(document.querySelector('#modal h3')||{}).textContent||null,
          sheetOpen: !!(document.getElementById('loc-sheet')&&document.getElementById('loc-sheet').offsetParent!==null),
          day:(typeof S!=='undefined'&&S)?S.dayIndex:null})""")
        # if the click dismissed the board, reopen for the close test
        if not ev(pg, "() => document.getElementById('mask').classList.contains('on')"):
            open_board(pg)
    click_any(pg, ['返去地點']); pg.wait_for_timeout(1000)
    res['after_close'] = ev(pg, """() => JSON.stringify({
      maskOn: document.getElementById('mask').classList.contains('on'),
      vmapVis: getComputedStyle(document.getElementById('v-map')).visibility,
      vmapInert: document.getElementById('v-map').hasAttribute('inert'),
      appCls: document.getElementById('app').className })""")
    res['map_count_after'] = count(pg, 'map_after_close')
    # pin clickable again after close?
    ok = open_loc_sheet(pg, 'film_lion')
    res['pin_works_after_close'] = ok
    save_out('modalbg396.json', res)
    return res

def seed_day(pg, day, weekplan):
    return ev(pg, """(a) => {
      S.acting=70; S.stage=60; S.vocal=45; S.looks=55; S.charm=50; S.iq=45; S.stamina=80; S.fame=24; S.money=1638; S.stress=20;
      S.dayIndex = a.day;
      S.homeEditable = false;
      S.weekPlanWeek37 = Math.floor(a.day/7)+1;
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ["N1","N2","N3","N4","N5","N6","N6F","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19"].forEach(id=>{ S.story.done[id]=true; });
      S.story.phase='P5';
      S.starDay = {day:a.day, presence:{}, triggered:99, doneToday:{}};
      S.romDay = {day:a.day, presence:{}, triggered:99, doneToday:{}};
      S.travel114 = {day:a.day, used:0};
      S.weekPlan = a.wp.slice();
      try{ if(typeof syncGigsForCalendarYear==='function') syncGigsForCalendarYear(true); }catch(e){}
      return JSON.stringify({date:(typeof fmtDate==='function'?fmtDate():''), plan:S.weekPlan}); }""", {'day': day, 'wp': weekplan})

def run_day_to_card(pg, want_h3_sub, max_steps=60):
    """Click 開始今日行程, then walk modals until a card whose h3 contains want_h3_sub appears."""
    go_map(pg)
    click_any(pg, ['開始今日行程']); pg.wait_for_timeout(1500)
    for step in range(max_steps):
        pg.wait_for_timeout(900)
        h = modal_h3(pg)
        st = ev(pg, """() => JSON.stringify({mask:(document.getElementById('mask')||{}).className||'', day:S.dayIndex,
          modal:(document.getElementById('modal')||{innerText:''}).innerText.slice(0,220).replace(/\\n/g,'|'),
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim().slice(0,24))})""")
        try: j = json.loads(st)
        except Exception: j = {}
        print("STEP", step, "h3=", h, "day=", j.get('day'), "mask=", j.get('mask'), flush=True)
        if h and want_h3_sub in h:
            return True, j
        if 'day-res' in (j.get('mask') or '') and h:
            # a day-end card, but not the one we want: press its primary button to continue
            if not click_modal(pg, ['開始今日行程', '返回地圖', '回家結算', '繼續']):
                pg.mouse.click(195, 120)
            pg.wait_for_timeout(900); continue
        c = click_modal(pg, ['下一句', '繼續', '確定', '收下這份剪報', '跳過', '開始今日行程', '回家結算', '返回地圖'])
        if c: continue
        if ev(pg, "() => document.getElementById('mask').classList.contains('on')"):
            pg.mouse.click(195, 120); pg.wait_for_timeout(700); continue
        if ev(pg, "() => (document.querySelector('.view.on')||{}).id") == 'v-map':
            print("BACK_ON_MAP_NO_CARD", flush=True); return False, j
    return False, {}

def probe_rest40(pg):
    new_game(pg)
    seed_day(pg, 17, ['scout_all', 'scout_all', 'scout_all', 'rest', 'cafe_gig', 'scout_all', 'scout_all'])
    res = {}
    # rest card itself first: is the day-res gradient actually live there?
    ok0, j0 = run_day_to_card(pg, '休息')
    res['rest_card_bg'] = ev(pg, """() => JSON.stringify({
      maskCls: document.getElementById('mask').className,
      bodyCls: document.body.className,
      maskBg: getComputedStyle(document.getElementById('mask')).background,
      maskBgImg: getComputedStyle(document.getElementById('mask')).backgroundImage})""")
    click_modal(pg, ['開始今日行程']); pg.wait_for_timeout(1200)
    ok = ev(pg, "() => (document.querySelector('#modal h3')||{}).textContent||null") == '開始今日行程？'
    res['got40'] = ok
    if ok:
        res['modal40'] = ev(pg, """() => JSON.stringify({
          maskCls: document.getElementById('mask').className,
          bodyCls: document.body.className,
          maskBg: getComputedStyle(document.getElementById('mask')).background,
          maskBgImg: getComputedStyle(document.getElementById('mask')).backgroundImage,
          modalRect: (()=>{ const r=document.getElementById('modal').getBoundingClientRect(); return {x:+r.x.toFixed(1), y:+r.y.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1), bottom:+r.bottom.toFixed(1)}; })(),
          vpH: window.innerHeight,
          text:(document.getElementById('modal-inner')||{}).innerText||null,
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim()) })""")
        shot(pg, '40_start_day_396')
        # dismiss outside (top dim area) -> should return to rest card, day unchanged
        before = ev(pg, "() => JSON.stringify({day:S.dayIndex})")
        pg.mouse.click(195, 120); pg.wait_for_timeout(1500)
        res['dismiss40'] = {'before': before,
          'after': ev(pg, """() => JSON.stringify({day:S.dayIndex, mask:(document.getElementById('mask')||{}).className||'',
            h3:(document.querySelector('#modal h3')||{}).textContent||null,
            modal:(document.getElementById('modal')||{innerText:''}).innerText.slice(0,200).replace(/\\n/g,'|')})""")}
        shot(pg, '86b_rest_dayend_after_cancel_396')
        res['rest_card_dateline'] = ev(pg, """() => JSON.stringify({
          h3:(document.querySelector('#modal h3')||{}).textContent||null,
          dateLine:(document.querySelector('.dayres-date374')||{}).textContent||null,
          nextLine:(document.querySelector('.dayend-next202')||{}).textContent||null,
          body:(document.getElementById('modal-inner')||{}).innerText||null })""")
    save_out('rest40_396.json', res)
    return res

def probe_dismiss(pg):
    new_game(pg)
    res = {}
    # D1: week-end rest card (ended) — Sunday rest, dayIndex 20 (weekdayIdx 6 = 日)
    seed_day(pg, 20, ['scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'rest'])
    ok, j = run_day_to_card(pg, '休息')
    res['D1_rest_ended_found'] = ok
    if ok:
        res['D1_card'] = ev(pg, """() => JSON.stringify({day:S.dayIndex,
          h3:(document.querySelector('#modal h3')||{}).textContent||null,
          dateLine:(document.querySelector('.dayres-date374')||{}).textContent||null,
          nextLine:(document.querySelector('.dayend-next202')||{}).textContent||null,
          gold:(document.querySelector('#modal .gold')||{}).textContent||null,
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim())})""")
        shot(pg, 'dismiss_ended_rest_396')
        before = ev(pg, "() => S.dayIndex")
        pg.mouse.click(195, 120); pg.wait_for_timeout(1500)
        res['D1_after_outside'] = {'day_before': before,
          'state': ev(pg, """() => JSON.stringify({day:S.dayIndex, view:(document.querySelector('.view.on')||{}).id||'',
            maskOn: document.getElementById('mask').classList.contains('on'),
            h3:(document.querySelector('#modal h3')||{}).textContent||null,
            modal:(document.getElementById('modal')||{innerText:''}).innerText.slice(0,160).replace(/\\n/g,'|')})""")}
    # D2: afterDayModal non-rest — training day (reset state in place; do NOT
    # reload the page — the single-threaded test server can stall a 2nd goto)
    seed_day(pg, 17, ['scout_all', 'scout_all', 'scout_all', 'train_acting', 'cafe_gig', 'scout_all', 'scout_all'])
    ok2, j2 = run_day_to_card(pg, '訓練')
    res['D2_training_found'] = ok2
    if not ok2:
        # fall back: accept any day-end card that is not rest
        ok2, j2 = run_day_to_card(pg, '日結')
    if ok2:
        res['D2_card'] = ev(pg, """() => JSON.stringify({day:S.dayIndex,
          h3:(document.querySelector('#modal h3')||{}).textContent||null,
          dateLine:(document.querySelector('.dayres-date374')||{}).textContent||null,
          nextLine:(document.querySelector('.dayend-next202')||{}).textContent||null,
          btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim())})""")
        shot(pg, 'dismiss_afterday_396')
        before = ev(pg, "() => S.dayIndex")
        pg.mouse.click(195, 120); pg.wait_for_timeout(1500)
        res['D2_after_outside'] = {'day_before': before,
          'state': ev(pg, """() => JSON.stringify({day:S.dayIndex, view:(document.querySelector('.view.on')||{}).id||'',
            maskOn: document.getElementById('mask').classList.contains('on'),
            h3:(document.querySelector('#modal h3')||{}).textContent||null,
            modal:(document.getElementById('modal')||{innerText:''}).innerText.slice(0,160).replace(/\\n/g,'|')})""")}
        pg.wait_for_timeout(1500)
        res['D2_after_wait'] = ev(pg, "() => JSON.stringify({day:S.dayIndex, maskOn: document.getElementById('mask').classList.contains('on'), view:(document.querySelector('.view.on')||{}).id||''})")
    save_out('dismiss396.json', res)
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
    print("AWARDS_QUEUE", ev(pg, """() => { try{ const A = window.__awards; if(!A) return 'noA';
        if(A.debugForceSeasonWindow) A.debugForceSeasonWindow();
        if(A.queue) A.queue();
        if(A.present) A.present();
        return 'ok'; }catch(e){ return 'err:'+e.message; } }"""), flush=True)
    pg.wait_for_timeout(1500)
    print("INVITE", modal_h3(pg), flush=True)
    # take the real pack built by the awards system, then present the result card directly
    pack = ev(pg, """() => { try{ const p = (S.pendingAwardPack) || (S.awardBooked213 && S.awardBooked213.pack) || null;
      return p ? JSON.stringify({has: true, keys: Object.keys(p), bestOutcome: p.bestOutcome, displayName: p.displayName, nCats: (p.categories||[]).length, metricEcho: p.metricEcho||null}) : JSON.stringify({has:false}); }catch(e){ return 'err:'+e.message; } }""")
    print("PACK", pack, flush=True)
    # book via invite buttons if present, else close invite by dismiss then use pack
    click_any(pg, ['出席']); pg.wait_for_timeout(900)
    click_any(pg, ['確定']); pg.wait_for_timeout(1500)
    # ceremony plays (canvas stage with a 跳過 button) — skip it, then the
    # result card (presentAwardResult) appears; this is the real flow.
    # Note: the invite only BOOKS the ceremony (S.awardBooked213); it plays
    # on the evening AFTER its ceremonyDay, via playEvening213.
    print("EVENING", ev(pg, """() => { try{ const b=S.awardBooked213; if(!b) return 'no-booked';
      S.dayIndex = (b.ceremonyDay|0) + 1;
      const r = window.__awards.playEvening213 ? window.__awards.playEvening213() : 'no-fn';
      return JSON.stringify({ceremonyDay: b.ceremonyDay, nowDay: S.dayIndex, played: r}); }catch(e){ return 'err:'+e.message; } }"""), flush=True)
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
      outcome: (S.pendingAwardPack||{}).bestOutcome || ((S.awardBooked213||{}).pack||{}).bestOutcome || null,
      h3:(document.querySelector('#modal h3')||{}).textContent||null})""")
    res['sheet'] = ev(pg, """() => JSON.stringify({
      sheetFound: !!document.querySelector('.paper-sheet'),
      maskCls: document.getElementById('mask').className,
      sheetH: (()=>{ const s=document.querySelector('.paper-sheet'); return s?+s.getBoundingClientRect().height.toFixed(1):null; })(),
      body2Cols: (()=>{ const b=document.querySelector('.np214-body2'); return b?getComputedStyle(b).columnCount:null; })(),
      switchPos: (()=>{ const s=document.querySelector('.np214-switchrow'); return s?getComputedStyle(s).position:null; })(),
      switchRect: (()=>{ const s=document.querySelector('.np214-switchrow'); if(!s) return null; const b=s.getBoundingClientRect(); return {y:+b.y.toFixed(1), bottom:+b.bottom.toFixed(1), h:+b.height.toFixed(1)}; })(),
      pagefootRect: (()=>{ const f=document.querySelector('.np214-pagefoot'); if(!f) return null; const b=f.getBoundingClientRect(); return {y:+b.y.toFixed(1), bottom:+b.bottom.toFixed(1)}; })(),
      miH: (document.getElementById('modal-inner')||{}).clientHeight||null,
      miScrollH: (document.getElementById('modal-inner')||{}).scrollHeight||null,
      btns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim()) })""")
    # per-line widths inside body2: detect 逐字斷行 (any rendered line < 40px wide)
    res['lines'] = ev(pg, """() => JSON.stringify((()=>{
      const out=[];
      document.querySelectorAll('.np214-body2 p').forEach(p=>{
        const range=document.createRange(); range.selectNodeContents(p);
        const rects=[...range.getClientRects()].map(r=>({w:+r.width.toFixed(1), h:+r.height.toFixed(1)}));
        out.push({cls:p.className, text:(p.textContent||'').slice(0,40), lines:rects.length, minW: rects.length?Math.min(...rects.map(r=>r.w)):null, rects:rects.slice(0,8)});
      });
      return out; })())""")
    # quote visibility at top + after scrolling to bottom
    res['quote_top'] = ev(pg, """() => JSON.stringify((()=>{ const q=document.querySelector('.np214-quote'); if(!q) return null;
      const mi=document.getElementById('modal-inner'); const mr=mi.getBoundingClientRect(); const r=q.getBoundingClientRect();
      return {text:q.textContent, top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), miTop:+mr.top.toFixed(1), miBottom:+mr.bottom.toFixed(1), fullyVisible: r.top>=mr.top-0.5 && r.bottom<=mr.bottom+0.5}; })())""")
    shot(pg, '35c_top_396')
    ev(pg, "() => { const mi=document.getElementById('modal-inner'); if(mi) mi.scrollTop = mi.scrollHeight; return true; }")
    pg.wait_for_timeout(600)
    res['quote_bottom_scroll'] = ev(pg, """() => JSON.stringify((()=>{ const q=document.querySelector('.np214-quote'); const mi=document.getElementById('modal-inner'); if(!q||!mi) return null;
      const mr=mi.getBoundingClientRect(); const r=q.getBoundingClientRect();
      const last=[...document.querySelectorAll('.paper-sheet .np214-page.on p')].pop();
      const lr=last?last.getBoundingClientRect():null;
      return {quote:{top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), fullyVisible: r.top>=mr.top-0.5 && r.bottom<=mr.bottom+0.5},
        lastP: lr?{text:(last.textContent||'').slice(0,40), bottom:+lr.bottom.toFixed(1)}:null,
        miBottom:+mr.bottom.toFixed(1), scrollTop: mi.scrollTop, scrollH: mi.scrollHeight}; })())""")
    shot(pg, '35c_bottom_396')
    # page 2
    click_any(pg, ['第二版']); pg.wait_for_timeout(900)
    res['page2'] = ev(pg, """() => JSON.stringify({
      page2on: !!(document.querySelector('.np214-page[data-np214-page="2"]')||{}).classList ? document.querySelector('.np214-page[data-np214-page="2"]').classList.contains('on') : null,
      factboxOnP2: (()=>{ const p2=document.querySelector('.np214-page[data-np214-page="2"]'); return p2 ? p2.innerHTML.indexOf('np214-factbox')>=0 : null; })(),
      factboxText: (()=>{ const f=document.querySelector('.np214-page[data-np214-page="2"] .np214-factbox'); return f?f.innerText.slice(0,200):null; })(),
      switchPos: (()=>{ const s=document.querySelector('.np214-page[data-np214-page="2"] .np214-switchrow'); return s?getComputedStyle(s).position:null; })() })""")
    shot(pg, '35c_page2_396')
    save_out('awards35c396.json', res)
    return res

def probe_lockedboard(pg):
    """24 vs 25 verification: opening stats so some gigs lock. Foreground
    count should be ready cards + 1 locked <summary> + 3 sort + 3 filter + 1 back."""
    new_game(pg)
    ev(pg, """() => {
      S.acting=18; S.stage=14; S.vocal=14; S.looks=22; S.charm=16; S.iq=20; S.stamina=75; S.fame=5; S.money=1200; S.stress=20;
      S.dayIndex = 1;
      S.weekPlan = ['scout_all','street','scout_all','scout_all','scout_all','scout_all','scout_all'];
      S.shoots=[]; S.booked=[]; S.pendingAud=[]; S.aud91Log=[]; S.grant229Queue=[];
      if(!S.story) S.story={done:{},flags:{},rel:{},routes:{},phase:'P5'};
      ['N1','N2','N3','N4','N5'].forEach(id=>{ S.story.done[id]=true; });
      S.story.flags = Object.assign({}, S.story.flags, {route_tv:true});
      S.flags = Object.assign({}, S.flags, {route_tv:true});
      S.story.routes = {route_tv:true};
      S.travel114 = {day:S.dayIndex, used:0};
      try{ localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S)); }catch(e){}
      return true; }""")
    assert open_board(pg), "board open failed"
    res = {}
    res['count'] = count(pg, 'board_locked')
    res['head'] = ev(pg, """() => JSON.stringify({
      sum:(document.querySelector('.board-sum392')||{}).innerText||null,
      nCards: document.querySelectorAll('.gig-teaser').length,
      nSummary: document.querySelectorAll('.gig-locked108 summary').length,
      summaryText:(document.querySelector('.gig-locked108 summary')||{}).textContent||null,
      nReady: document.querySelectorAll('.gig-teaser[data-board-state="ready"]').length,
      nLocked: document.querySelectorAll('.gig-teaser[data-board-state="locked"]').length,
      featured: (document.querySelector('.gig-teaser.gt-featured .gt-title')||{}).textContent||null})""")
    shot(pg, 'board_locked_396')
    save_out('lockedboard396.json', res)
    return res

def probe_menuledger(pg):
    new_game(pg)
    seed_main(pg, 1)
    go_map(pg)
    res = {}
    # real menu: #btn-menu opens the #menu dropdown PANEL (not a modal)
    ev(pg, "() => { const b=document.getElementById('btn-menu'); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(1000)
    res['menu'] = ev(pg, """() => JSON.stringify({menuOn: document.getElementById('menu').classList.contains('on'),
      menuVisible: document.getElementById('menu').offsetParent!==null,
      btns:[...document.querySelectorAll('#menu button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim())})""")
    shot(pg, 'retake_24_menu_396')
    click_any(pg, ['關閉', '返回', '取消']); pg.wait_for_timeout(800)
    # real ledger: home notebook -> 帳本 group -> 帳目 sub-tab
    ev(pg, "() => { const h=document.getElementById('book389-handle'); if(h) h.click(); return !!h; }")
    pg.wait_for_timeout(1200)
    ev(pg, """() => { const b=[...document.querySelectorAll('button')].find(x=>/帳本/.test(x.textContent||'')); if(b) b.click(); return !!b; }""")
    pg.wait_for_timeout(800)
    ev(pg, "() => { const b=document.getElementById('htab-ledger'); if(b) b.click(); return !!b; }")
    pg.wait_for_timeout(900)
    res['ledger'] = ev(pg, """() => JSON.stringify({view:(document.querySelector('.view.on')||{}).id||'',
      ledgerVisible: !!(document.getElementById('ledger-list')&&document.getElementById('ledger-list').offsetParent!==null),
      text:(document.getElementById('ledger-list')||{}).innerText.slice(0,300)||null,
      htab: (document.getElementById('htab-ledger')||{}).textContent||null})""")
    shot(pg, 'retake_17_ledger_396')
    save_out('menuledger396.json', res)
    return res

PROBES = {'board': probe_board, 'shops': probe_shops, 'modalbg': probe_modalbg,
          'rest40': probe_rest40, 'dismiss': probe_dismiss, 'awards': probe_awards,
          'menuledger': probe_menuledger, 'lockedboard': probe_lockedboard}

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox',
        '--proxy-server=http://127.0.0.1:18081', '--ignore-certificate-errors'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: print('PAGEERR', str(e)[:200], flush=True))
    todo = ['board', 'shops', 'modalbg', 'rest40', 'dismiss', 'awards', 'menuledger'] if 'all' in ITEMS else ITEMS
    for name in todo:
        print("===== PROBE", name, "=====", flush=True)
        try:
            PROBES[name](pg)
        except Exception as e:
            print("PROBE_FAIL", name, repr(e)[:300], flush=True)
        try:
            pg.goto(URL); pg.wait_for_timeout(800)
        except Exception:
            pass
    b.close()
srv.terminate()
print("DONE", flush=True)
