# -*- coding: utf-8 -*-
"""v128 post-change verification: A1 (420x900 + toast-up + chip entry), A3 (D-1/N5/N4/D-7/N16/WF4),
A5 (gift icons live), A6 (settings speed buttons + S-20 top back button).
Reuses probe_a2/a3b patterns (slot 3, ?softPreview=1, window.S seeding only).
No game code changed."""
import sys, os, json
sys.path.insert(0, "/home/hatch/workspace/linji-ui-style-unify")
from drive_lib import EXE
from playwright.sync_api import sync_playwright

PORT = 8952
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
SHOTS = "/home/hatch/workspace/linji-work128/qa128/shots"
os.makedirs(SHOTS, exist_ok=True)
OUT = "/home/hatch/workspace/linji-work128/qa128/verify_a3a6.json"

def click_first(pg, texts, wait=900):
    for t in texts:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

def next_step(pg):
    ok = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")
    pg.wait_for_timeout(900)
    return ok

def story_state(pg):
    return pg.evaluate("""() => {
      const root = document.getElementById('story-play-root');
      if (!root) return {active:false};
      const head = root.querySelector('.sp-head');
      const stage = root.querySelector('.sp-stage');
      const chars = [...root.querySelectorAll('.dlg106-char,.sp-bust')].map(im=>{
        const b = im.getBoundingClientRect();
        return {id: im.dataset.dlgId || im.alt || '', w: Math.round(b.width), h: Math.round(b.height),
          filter: im.style.filter || getComputedStyle(im).filter}; });
      const modalBtns = [...document.querySelectorAll('#modal-btns button')].map(b=>b.textContent.trim());
      const cards = [...root.querySelectorAll('.sp-choice')].map(b=>b.textContent.trim().slice(0,30));
      const mapBar = document.getElementById('map-bar');
      const mapBarVis = mapBar ? getComputedStyle(mapBar).visibility : 'n/a';
      return {active:true, kind: stage ? stage.dataset.spKind : '', head: !!head,
        line: (root.querySelector('.sp-line')||{}).textContent || '',
        speaker: (root.querySelector('.sp-speaker')||{}).textContent || '',
        chars, modalBtns, cards, mapBarVis};
    }""")

def pin_click(pg, loc_id):
    box = pg.evaluate("""(id) => { const b=document.querySelector('.pin[data-loc="'+id+'"]');
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x+r.width/2, y:r.y+r.height/2}; }""", loc_id)
    if not box: return False
    pg.mouse.click(box["x"], box["y"]); pg.wait_for_timeout(1600); return True

def ensure_quota(pg):
    pg.evaluate("""() => { const S = window.S; if(!S) return;
      S.travel114 = { day: S.dayIndex|0, used: 0 }; }""")

STARS12 = ["luk_baakyin","liu_bingxing","ngai_wingnaam","yip_manji","mak_zhendong",
           "lok_gasing","pang_siuki","chung_choning","gu_mingfai","so_jiyan",
           "chai_zanhoi","ching_tinlok"]

def seed_quiet(pg):
    pg.evaluate("""(stars) => { const S = window.S; if(!S) return;
      if(S.starDay && S.starDay.day === S.dayIndex){
        S.starDay.doneToday = S.starDay.doneToday || {};
        stars.forEach(id => S.starDay.doneToday[id] = 1); }
      if(!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = {};
      S.wf4.lastDay = S.dayIndex; }""", STARS12)

def seed_no_encounter(pg):
    """Suppress encounters WITHOUT touching S.wf4 (the loc counter must accumulate across entries)."""
    return pg.evaluate("""() => {
      const S = window.S; if(!S) return 'no S';
      const day = S.dayIndex|0;
      const stars = ["luk_baakyin","liu_bingxing","ngai_wingnaam","yip_manji","mak_zhendong",
        "lok_gasing","pang_siuki","chung_choning","gu_mingfai","so_jiyan","chai_zanhoi","ching_tinlok"];
      if(S.starDay && S.starDay.day === day){
        S.starDay.doneToday = S.starDay.doneToday || {};
        stars.forEach(id => S.starDay.doneToday[id] = 1);
      }
      return 'suppressed'; }""")

def seed_encounter(pg, star_id, loc_id):
    return pg.evaluate("""(a) => { const sid=a[0], loc=a[1]; const S = window.S; if(!S) return 'no S';
      const day = S.dayIndex;
      S.starDay = { day, presence: {}, triggered: 0, doneToday: {} };
      S.starDay.presence[loc] = [sid];
      if(!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = {};
      S.wf4.lastDay = day;
      return 'seeded ' + sid + ' @ ' + loc + ' day ' + day; }""", [star_id, loc_id])

def play_through_dialogue(pg, max_steps=40):
    for _ in range(max_steps):
        st = pg.evaluate("""() => {
          const sp = document.querySelector('.story-play');
          const ov = document.querySelector('.enc79-overlay');
          const host = sp || ov;
          if (!host) return {active:false};
          return {active:true, choices:[...host.querySelectorAll('.sp-choice')].map(b=>b.textContent.trim().slice(0,20))}; }""")
        if not st["active"]: return True
        if st["choices"]:
            pg.evaluate("""() => { const c=document.querySelector('.sp-choice'); if(c) c.click(); }""")
            pg.wait_for_timeout(900); continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if clicked: pg.wait_for_timeout(800); continue
        hit = click_first(pg, ["下一句", "繼續", "下一步", "好", "知道了"], 700)
        if not hit:
            pg.evaluate("""() => { const sp=document.querySelector('.story-play,.enc79-overlay'); if(sp) sp.click(); }""")
            pg.wait_for_timeout(700)
    return pg.evaluate("() => !document.querySelector('.story-play,.enc79-overlay')")

def sheet_open(pg):
    return pg.evaluate("""() => { const s = document.getElementById('loc-sheet');
      return s && (s.classList.contains('on') || s.classList.contains('sheet-live')) &&
             (document.getElementById('loc-title')||{}).textContent !== '地點'; }""")

def back_to_map(pg):
    # modal visibility lives on #mask.on, NOT #modal.on; the gift purchase modal's
    # dismiss button is 返去地點 (reopens the sheet via forceRestore), then 返回地圖 closes it.
    for _ in range(6):
        st = pg.evaluate("""() => { const v=document.getElementById('v-map');
          const sheet=document.getElementById('loc-sheet');
          const mask=document.getElementById('mask');
          return {onMap: v && v.classList.contains('on'),
            sheetOn: sheet && (sheet.classList.contains('on') || sheet.classList.contains('sheet-live')),
            modalOn: mask && mask.classList.contains('on')}; }""")
        if st["onMap"] and not st["sheetOn"] and not st["modalOn"]:
            return st
        click_first(pg, ["返去地點", "返回地圖", "返地圖", "關閉"], 900)
        pg.wait_for_timeout(700)
    return pg.evaluate("""() => { const v=document.getElementById('v-map');
      const sheet=document.getElementById('loc-sheet');
      const mask=document.getElementById('mask');
      return {onMap: v && v.classList.contains('on'),
        sheetOn: sheet && (sheet.classList.contains('on') || sheet.classList.contains('sheet-live')),
        modalOn: mask && mask.classList.contains('on')}; }""")

def map_measure(pg):
    return pg.evaluate("""() => { const de = document.documentElement;
      const hint = document.getElementById('map-hint');
      const hb = hint ? hint.getBoundingClientRect() : null;
      const chip = document.getElementById('chip-story');
      return {vh: window.innerHeight, docScrollH: de.scrollHeight, scrollY: window.scrollY,
        hintVisible: hint ? getComputedStyle(hint).visibility : 'n/a',
        hintOpacity: hint ? getComputedStyle(hint).opacity : 'n/a',
        hintBottom: hb ? Math.round(hb.bottom) : null,
        chipTag: chip ? chip.tagName : null,
        chipText: chip ? chip.textContent.trim().slice(0,12) : null,
        floatProg: !!document.getElementById('map-progress-btn')}; }""")

def main():
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                             user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
        pg.goto(URL); pg.wait_for_timeout(3200)
        pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='新遊戲'); if(b) b.click(); }""")
        pg.wait_for_timeout(1200)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]'); if (b && b.offsetParent !== null) b.click(); }""")
        pg.wait_for_timeout(1200)
        for t in ["覆蓋", "確定", "確認"]:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); break
            except Exception: pass
        for t in ["跳過教學", "開始寫手帳"]:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(1200)
            except Exception: pass
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception: pass
        click_first(pg, ["確定出發"], 1500)
        for _ in range(5):
            hit = False
            for t in ["確定", "確認", "好", "知道了"]:
                try:
                    loc = pg.locator("button:has-text('" + t + "')")
                    if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); hit = True; break
                except Exception: pass
            if not hit: break
        pg.wait_for_timeout(1200)

        # ---- C1: D-1 / N5 / D-7 / N4 ----
        print("== C1 ==", flush=True)
        pin_click(pg, "agency_ho")
        print("播劇情:", click_first(pg, ["播劇情"], 1800), flush=True)
        c1 = []
        for i in range(30):
            st = story_state(pg)
            c1.append(st)
            print(f"step{i}: kind={st.get('kind')} head={st.get('head')} speaker={st.get('speaker')!r} chars={[(c['id'],c['w'],c['h']) for c in st.get('chars',[])]} mapBarVis={st.get('mapBarVis')} modalBtns={st.get('modalBtns')} cards={len(st.get('cards',[]))}", flush=True)
            if i == 2:
                pg.screenshot(path=os.path.join(SHOTS, "v128_c1_step2.png"))
            if st.get("kind") == "choices" or not st.get("active"):
                break
            if pg.evaluate("() => !!document.querySelector('.sp-choice')"):
                break
            next_step(pg)
        out["c1"] = c1
        # choices screen: verify paper cards only, no head, then click a card
        choice_info = pg.evaluate("""() => {
          const root = document.getElementById('story-play-root');
          if(!root) return {active:false};
          const cards = [...root.querySelectorAll('.sp-choice')];
          const pe = cards.length ? getComputedStyle(cards[0]).pointerEvents : 'n/a';
          return {active:true, head: !!root.querySelector('.sp-head'),
            modalBtns: [...document.querySelectorAll('#modal-btns button')].map(b=>b.textContent.trim()),
            nCards: cards.length, cardPointerEvents: pe,
            cardDisabled: cards.length ? cards[0].disabled : null}; }""")
        print("CHOICES:", json.dumps(choice_info, ensure_ascii=False), flush=True)
        out["choices"] = choice_info
        pg.screenshot(path=os.path.join(SHOTS, "v128_c1_choices.png"))
        # click first paper card -> should advance (pickChoice runs)
        clicked = pg.evaluate("""() => { const c=document.querySelector('.sp-choice'); if(!c) return false;
          c.click(); return true; }""")
        pg.wait_for_timeout(1500)
        after_click = pg.evaluate("""() => { const root = document.getElementById('story-play-root');
          return {stillChoices: !!document.querySelector('.sp-choice'),
                  result: !!document.querySelector('.sp-result, .story-play'),
                  modalBtns: [...document.querySelectorAll('#modal-btns button')].map(b=>b.textContent.trim())}; }""")
        print("after paper-card click:", clicked, json.dumps(after_click, ensure_ascii=False), flush=True)
        out["choice_click"] = {"clicked": clicked, "after": after_click}
        play_through_dialogue(pg, 30)
        pg.wait_for_timeout(900)
        click_first(pg, ["好", "知道了", "完成"], 900)
        back_to_map(pg)

        # ---- A1 map: 390x844 one-screen + toast-up + chip entry ----
        print("== A1 map 390x844 ==", flush=True)
        m390 = map_measure(pg)
        print("map390:", json.dumps(m390, ensure_ascii=False), flush=True)
        out["map390"] = m390
        pg.screenshot(path=os.path.join(SHOTS, "v128_map_390x844.png"))
        # toast-up: force the class (toast() is IIFE-scoped, not global) and check hint stays visible
        pg.evaluate("""() => { const app = document.getElementById('app'); if(app) app.classList.add('toast-up'); }""")
        pg.wait_for_timeout(400)
        toast_state = pg.evaluate("""() => { const app = document.getElementById('app');
          const hint = document.getElementById('map-hint');
          return {toastUp: app ? app.classList.contains('toast-up') : null,
                  hintVis: hint ? getComputedStyle(hint).visibility : 'n/a',
                  hintOpacity: hint ? getComputedStyle(hint).opacity : 'n/a'}; }""")
        print("toast-up:", json.dumps(toast_state, ensure_ascii=False), flush=True)
        out["toast_up"] = toast_state
        pg.evaluate("""() => { const app = document.getElementById('app'); if(app) app.classList.remove('toast-up'); }""")
        pg.wait_for_timeout(300)
        # chip click -> progress page
        chip_go = pg.evaluate("""() => { const c=document.getElementById('chip-story');
          if(!c) return 'no chip'; c.click(); return 'clicked'; }""")
        pg.wait_for_timeout(1200)
        chip_dest = pg.evaluate("""() => { const v=document.getElementById('v-home');
          const pane = document.getElementById('home-pane-progress');
          return {homeOn: v ? v.classList.contains('on') : null,
                  progressOn: pane ? pane.classList.contains('on') : null}; }""")
        print("chip:", chip_go, json.dumps(chip_dest, ensure_ascii=False), flush=True)
        out["chip"] = {"click": chip_go, "dest": chip_dest}
        pg.screenshot(path=os.path.join(SHOTS, "v128_chip_progress.png"))
        back_to_map(pg)

        # ---- A6 S-20: 手帳頂部返回掣 ----
        print("== A6 S-20 ==", flush=True)
        pg.evaluate("""() => { try{ enterHome(null, false, 'plan'); }catch(e){} }""")
        pg.wait_for_timeout(1200)
        s20 = pg.evaluate("""() => {
          const exit = document.getElementById('home-tab-exit');
          const tabs = document.getElementById('home-tabs');
          const home = document.querySelector('.home');
          const kids = home ? [...home.children].map(el=>el.id||el.className.slice(0,20)) : [];
          const reset = document.getElementById('btn-reset-plan');
          const confirm = document.getElementById('btn-confirm-plan');
          const rb = reset ? reset.getBoundingClientRect() : null;
          const cb = confirm ? confirm.getBoundingClientRect() : null;
          const eb = exit ? exit.getBoundingClientRect() : null;
          const tb = tabs ? tabs.getBoundingClientRect() : null;
          return {exitBeforeTabs: !!(exit && tabs && (exit.compareDocumentPosition(tabs) & 4)),
                  homeKids: kids.slice(0,6),
                  exitY: eb ? Math.round(eb.y) : null, tabsY: tb ? Math.round(tb.y) : null,
                  resetH: rb ? Math.round(rb.height) : null,
                  resetVisible: reset ? getComputedStyle(reset).display : 'n/a',
                  confirmText: confirm ? confirm.textContent.trim() : null}; }""")
        print("S-20:", json.dumps(s20, ensure_ascii=False), flush=True)
        out["s20"] = s20
        pg.screenshot(path=os.path.join(SHOTS, "v128_home_top.png"))

        # ---- A6 settings: speed paper buttons ----
        print("== A6 settings ==", flush=True)
        pg.evaluate("""() => { const b=document.getElementById('btn-menu'); if(b) b.click(); }""")
        pg.wait_for_timeout(800)
        click_first(pg, ["設定"], 1200)
        pg.wait_for_timeout(800)
        spd = pg.evaluate("""() => {
          const btns = [...document.querySelectorAll('.set-speed128 .set-speed-btn')];
          const hid = document.getElementById('set-speed');
          const sel = document.querySelector('select#set-speed');
          return {nBtns: btns.length, labels: btns.map(b=>b.textContent.trim()),
                  onLabel: (btns.find(b=>b.classList.contains('on'))||{}).textContent || null,
                  hiddenVal: hid ? hid.value : null, hasSelect: !!sel}; }""")
        print("speed before:", json.dumps(spd, ensure_ascii=False), flush=True)
        # click 慢 -> hidden value should become slow
        pg.evaluate("""() => { const b=[...document.querySelectorAll('.set-speed128 .set-speed-btn')].find(x=>x.textContent.trim()==='慢'); if(b) b.click(); }""")
        pg.wait_for_timeout(600)
        spd2 = pg.evaluate("""() => { const hid = document.getElementById('set-speed');
          const on = document.querySelector('.set-speed128 .set-speed-btn.on');
          return {hiddenVal: hid ? hid.value : null, onLabel: on ? on.textContent.trim() : null}; }""")
        print("speed after click 慢:", json.dumps(spd2, ensure_ascii=False), flush=True)
        out["speed"] = {"before": spd, "after": spd2}
        pg.screenshot(path=os.path.join(SHOTS, "v128_settings_speed.png"))
        click_first(pg, ["關閉"], 900)
        back_to_map(pg)

        # ---- A5: gift shop icons render as img (retry: encounter may swallow the pin) ----
        print("== A5 gift shop ==", flush=True)
        gift = {"sheetOpen": False, "nIc112": 0, "giftImgs": []}
        for attempt in range(3):
            ensure_quota(pg); seed_quiet(pg)
            pin_click(pg, "gift_shop")
            pg.wait_for_timeout(1200)
            play_through_dialogue(pg, 15)
            pg.wait_for_timeout(900)
            if sheet_open(pg):
                break
            seed_quiet(pg); pin_click(pg, "gift_shop"); pg.wait_for_timeout(1200)
            if sheet_open(pg):
                break
        gift = pg.evaluate("""() => {
          const imgs = [...document.querySelectorAll('#loc-sheet img.ic112')].map(im=>im.getAttribute('src'));
          const giftImgs = imgs.filter(s=>s && s.includes('icon_gift_'));
          return {sheetOpen: !!document.querySelector('#loc-sheet.on, #loc-sheet.sheet-live'),
                  nIc112: imgs.length, giftImgs}; }""")
        print("gift shop board:", json.dumps(gift, ensure_ascii=False), flush=True)
        # gift icons live in the purchase list: open 買禮物 and re-check
        click_first(pg, ["買禮物"], 1200)
        gift2 = pg.evaluate("""() => {
          const imgs = [...document.querySelectorAll('#loc-sheet img.ic112, #modal-inner img.ic112')].map(im=>im.getAttribute('src'));
          const giftImgs = imgs.filter(s=>s && s.includes('icon_gift_'));
          return {nIc112: imgs.length, giftImgs}; }""")
        print("gift purchase list:", json.dumps(gift2, ensure_ascii=False), flush=True)
        gift["purchaseList"] = gift2
        print("gift shop:", json.dumps(gift, ensure_ascii=False), flush=True)
        out["gift_shop"] = gift
        pg.screenshot(path=os.path.join(SHOTS, "v128_gift_shop.png"))
        print("back to map:", back_to_map(pg), flush=True)

        # ---- N16: encounter third party ----
        print("== N16 ==", flush=True)
        ensure_quota(pg)
        print(seed_encounter(pg, "liu_bingxing", "cafe_cha"), flush=True)
        pin_click(pg, "cafe_cha")
        pg.wait_for_timeout(1500)
        enc = []
        for i in range(10):
            st = pg.evaluate("""() => { const ov = document.querySelector('#enc79-overlay');
              if(!ov) return {active:false};
              const m = ov.querySelector('.e79-char3');
              const mh = ov.querySelector('.e79-char3-halo');
              const mb = m ? m.getBoundingClientRect() : null;
              const chars=[...ov.querySelectorAll('.e79-char')].map(im=>{ const b=im.getBoundingClientRect();
                return {sid: im._sid106||'', w: Math.round(b.width), h: Math.round(b.height), filter: im.style.filter}; });
              return {active:true, name: (ov.querySelector('.e79-name')||{}).textContent||'',
                line: (ov.querySelector('.e79-line')||{}).textContent||'',
                char3: m ? {shown: m.classList.contains('on'), src: (m.getAttribute('src')||'').slice(0,60),
                            w: mb ? Math.round(mb.width) : 0, h: mb ? Math.round(mb.height) : 0,
                            filter: m.style.filter} : null,
                haloShown: mh ? mh.classList.contains('on') : null, chars}; }""")
            enc.append(st)
            print(f"enc{i}: name={st.get('name')!r} line={st.get('line','')[:40]!r} char3={st.get('char3')} chars={[(c['sid'],c['w'],c['filter']) for c in st.get('chars',[])]}", flush=True)
            if "副導" in st.get("line", "") or (st.get("char3") or {}).get("shown"):
                pg.screenshot(path=os.path.join(SHOTS, "v128_enc_fudao.png"))
                break
            pg.evaluate("""() => { const b=[...document.querySelectorAll('#enc79-overlay .e79-btn')].find(x=>x.textContent.trim()==='下一句'); if(b) b.click(); }""")
            pg.wait_for_timeout(900)
        out["enc"] = enc
        # close encounter (probe_a3b loop): choices first, then 下一句/返去, then skip
        for _ in range(16):
            still = pg.evaluate("() => !!document.querySelector('#enc79-overlay')")
            if not still:
                break
            pg.evaluate("""() => {
              const ov = document.querySelector('#enc79-overlay'); if(!ov) return;
              const ch = ov.querySelector('.e79-choice');
              if(ch){ ch.click(); return; }
              const b=[...ov.querySelectorAll('.e79-btn')].find(x=>/下一句|返去/.test(x.textContent));
              if(b) b.click(); }""")
            pg.wait_for_timeout(700)
        pg.evaluate("""() => { const s=document.querySelector('#enc79-overlay .e79-skip'); if(s) s.click(); }""")
        pg.wait_for_timeout(900)
        print("after enc close:", back_to_map(pg), flush=True)

        # ---- WF4: boss01 stage (probe_a3b recipe: reset gate ONCE, enter cafe 3x, 3rd fires) ----
        print("== WF4 ==", flush=True)
        print("day/wf4:", pg.evaluate("() => ({day: window.S.dayIndex, wf4: window.S.wf4})"), flush=True)
        pg.evaluate("""() => { const S = window.S; if(!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = {};
          S.wf4.lastDay = -99; S.wf4.locDay = -99; S.wf4.locTries = 0; S.wf4.pending = null;
          S.wf4.seen = S.wf4.seen || {}; S.wf4.seen.__n = 3; /* pick hash -> boss01 (has 阿偉) */
          return 'reset'; }""")
        wf = None
        for entry in range(1, 4):
            seed_no_encounter(pg)
            ensure_quota(pg)
            pin_click(pg, "cafe_cha")
            pg.wait_for_timeout(1200)
            wf = pg.evaluate("""() => { const st = document.querySelector('#modal-inner .sp-stage');
              const sheet = document.getElementById('loc-sheet');
              const sheetOn = sheet && (sheet.classList.contains('on') || sheet.classList.contains('sheet-live'));
              const mask = document.getElementById('mask');
              if(!st) return {stage:false, sheetOn: !!sheetOn, wf4on: mask ? mask.classList.contains('wf4-stage-on') : null,
                modalText: (document.getElementById('modal-inner')||{}).textContent.slice(0,60)};
              const b = st.getBoundingClientRect();
              const chars=[...st.querySelectorAll('.dlg106-char')].map(im=>{ const r=im.getBoundingClientRect();
                return {sid: im.dataset.dlgId||'', w: Math.round(r.width), h: Math.round(r.height)}; });
              const modal = document.getElementById('modal-inner').getBoundingClientRect();
              const title = (document.querySelector('#modal-inner h3')||{}).textContent||'';
              return {stage:true, title, wf4on: mask ? mask.classList.contains('wf4-stage-on') : null,
                stage:{w:Math.round(b.width),h:Math.round(b.height)},
                modal:{w:Math.round(modal.width),h:Math.round(modal.height)}, chars}; }""")
            print(f"entry{entry}:", json.dumps(wf, ensure_ascii=False), flush=True)
            print("  wf4state:", pg.evaluate("() => ({day: window.S.dayIndex, lastDay: window.S.wf4.lastDay, locDay: window.S.wf4.locDay, locTries: window.S.wf4.locTries})"), flush=True)
            if wf.get("stage"):
                pg.screenshot(path=os.path.join(SHOTS, "v128_wf4.png"))
                break
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
            pg.wait_for_timeout(700)
        out["wf4"] = wf

        # ---- A1 420x900 ----
        print("== A1 map 420x900 ==", flush=True)
        pg.set_viewport_size({"width": 420, "height": 900})
        pg.wait_for_timeout(1200)
        back_to_map(pg)
        pg.wait_for_timeout(800)
        m420 = map_measure(pg)
        print("map420:", json.dumps(m420, ensure_ascii=False), flush=True)
        out["map420"] = m420
        pg.screenshot(path=os.path.join(SHOTS, "v128_map_420x900.png"))

        out["pageerrors"] = errs
        print("PAGEERRORS:", errs, flush=True)
        with open(OUT, "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        br.close()

if __name__ == "__main__":
    main()
