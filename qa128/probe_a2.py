# -*- coding: utf-8 -*-
"""v128 A2 probe v2: open location boards via map label buttons, play through
any encounter dialogue, retry the pin if the board did not open.
Measures N13 geometry, S-26 flag, N2 nameplate, N3 desc."""
import sys, os, json
sys.path.insert(0, "/home/hatch/workspace/linji-ui-style-unify")
from drive_lib import EXE
from playwright.sync_api import sync_playwright

PORT = 8952
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
SHOTS = "/home/hatch/workspace/linji-work128/qa128/shots"
os.makedirs(SHOTS, exist_ok=True)

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

def play_through_dialogue(pg, max_steps=40):
    """Click through any dialogue: .story-play OR .enc79-overlay.
    Mirrors drive_d play_story: choices first, then #modal-btns, then 下一句."""
    for _ in range(max_steps):
        st = pg.evaluate("""() => {
          const sp = document.querySelector('.story-play');
          const ov = document.querySelector('.enc79-overlay');
          const host = sp || ov;
          if (!host) return {active:false};
          return {active:true, kind: sp ? 'story' : 'enc79',
            choices:[...host.querySelectorAll('.sp-choice')].map(b=>b.textContent.trim().slice(0,20))};
        }""")
        if not st["active"]:
            return True
        if st["choices"]:
            pg.evaluate("""() => { const c=document.querySelector('.sp-choice'); if(c) c.click(); }""")
            pg.wait_for_timeout(900)
            continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if clicked:
            pg.wait_for_timeout(800)
            continue
        hit = click_first(pg, ["下一句", "繼續", "下一步", "好", "知道了"], 700)
        if not hit:
            pg.evaluate("""() => { const sp=document.querySelector('.story-play,.enc79-overlay'); if(sp) sp.click(); }""")
            pg.wait_for_timeout(700)
    return pg.evaluate("() => !document.querySelector('.story-play,.enc79-overlay')")

def sheet_open(pg):
    return pg.evaluate("""() => {
      const s = document.getElementById('loc-sheet');
      return s && (s.classList.contains('on') || s.classList.contains('sheet-live')) &&
             (document.getElementById('loc-title')||{}).textContent !== '地點';
    }""")

STARS12 = ["luk_baakyin", "liu_bingxing", "ngai_wingnaam", "yip_manji", "mak_zhendong",
           "lok_gasing", "pang_siuki", "chung_choning", "gu_mingfai", "so_jiyan",
           "chai_zanhoi", "ching_tinlok"]

def seed_quiet(pg):
    """Probe-only: mark all of today's encounters done + WF4 done, so openLoc
    opens the board directly instead of intercepting. Does NOT touch game code.
    (Without this, a present star's enc79 intercept fires but the overlay
    never appears — pre-existing silent swallow, v126 same — and the board
    never opens while the travel quota is still spent.)"""
    return pg.evaluate("""(stars) => {
      const S = window.S; if(!S) return 'no S';
      if(S.starDay && S.starDay.day === S.dayIndex){
        S.starDay.doneToday = S.starDay.doneToday || {};
        stars.forEach(id => S.starDay.doneToday[id] = 1);
      }
      if(!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = {};
      S.wf4.lastDay = S.dayIndex;
      return 'seeded';
    }""", STARS12)

def ensure_quota(pg):
    """Probe-only: reset today's travel quota via window.S (the 過一日 flow
    triggers the morning briefing/plan editor and stalls on later days).
    The quota is a game mechanic, not what this probe measures."""
    pg.evaluate("""() => {
      const S = window.S; if(!S) return;
      S.travel114 = { day: S.dayIndex|0, used: 0 };
    }""")

def pin_click(pg, loc_id):
    """Mouse click at the pin centre (drive_d click_pin method)."""
    box = pg.evaluate("""(id) => { const b=document.querySelector('.pin[data-loc="'+id+'"]');
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x+r.width/2, y:r.y+r.height/2}; }""", loc_id)
    if not box:
        return False
    pg.mouse.click(box["x"], box["y"])
    pg.wait_for_timeout(1600)
    return True

def open_loc(pg, loc_id, tries=3):
    """Click the map pin, play through any encounter overlay, confirm the sheet opened."""
    for _ in range(tries):
        ensure_quota(pg)
        seed_quiet(pg)
        if not pin_click(pg, loc_id):
            print(f"  no pin for {loc_id}", flush=True)
            return False
        play_through_dialogue(pg, 40)
        pg.wait_for_timeout(900)
        if sheet_open(pg):
            return True
        # encounter played; the board should now open on a second click
        seed_quiet(pg)
        pin_click(pg, loc_id)
        pg.wait_for_timeout(900)
        if sheet_open(pg):
            return True
    return sheet_open(pg)

def back_to_map(pg):
    click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
    pg.wait_for_timeout(700)
    # verify the map is actually showing; retry once if a sheet is still up
    on_map = pg.evaluate("() => { const v=document.getElementById('v-map'); return v && v.classList.contains('on'); }")
    if not on_map:
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
        pg.wait_for_timeout(700)

MEASURE_BOARD = """() => {
  const r = s => { const el = document.querySelector(s); if(!el) return null;
    const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            bottom: Math.round(b.bottom), top: Math.round(b.top),
            display: cs.display, position: cs.position, order: cs.order, overflow: cs.overflow}; };
  const who = document.getElementById('loc-who');
  const line = document.querySelector('.pres105-line');
  const lineBox = line ? (()=>{ const b=line.getBoundingClientRect();
    return {x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height),bottom:Math.round(b.bottom),
            scrollH: line.scrollHeight, text: line.textContent}; })() : null;
  return {
    sheetOn: !!document.querySelector('#loc-sheet.on, #loc-sheet.sheet-live'),
    title: (document.getElementById('loc-title')||{}).textContent||'',
    desc: (document.getElementById('loc-desc')||{}).textContent||'',
    whoText: who ? who.textContent : null,
    whoBox: r('#loc-who'), pres105: r('.pres105'), presLine: lineBox,
    quota: r('#loc-quota118'), tagrow: r('#loc-tagrow118'),
    tagrowText: (document.getElementById('loc-tagrow-tag118')||{}).textContent||'',
    ownerHidden: (document.getElementById('loc-owner118')||{}).hidden,
    flag26: !!(window.S && window.S.flags && window.S.flags.seenLocWhoHint26),
    sheetCls: (document.getElementById('loc-sheet')||{}).className||''
  };
}"""

def main():
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
        # C1 first (drive_d): agency board -> 播劇情 -> play through -> back to map.
        # Without C1, star-location pins are silently swallowed (enc79 gate).
        print("== C1 via agency ==", flush=True)
        pin_click(pg, "agency_ho")
        print("agency sheet:", pg.evaluate("""() => (document.getElementById('loc-title')||{}).textContent||''"""), flush=True)
        print("播劇情:", click_first(pg, ["播劇情"], 1800), flush=True)
        pg.wait_for_timeout(800)
        print("C1 cleared:", play_through_dialogue(pg, 30), flush=True)
        back_to_map(pg)
        pg.wait_for_timeout(600)

        out = {}
        for label, key, shot in [
            ("cafe_cha", "cafe", "a2_cafe_390x844.png"),
            ("tvb_longmen", "tv", None),
            ("film_lion", "lion", None),
            ("hospital", "hospital", "a2_hospital_390x844.png"),
            ("gift_shop", "gift", "a2_gift_390x844.png"),
        ]:
            ok = open_loc(pg, label)
            print(f"== {key} open={ok} ==", flush=True)
            m = pg.evaluate(MEASURE_BOARD)
            out[key] = m
            print(json.dumps(m, ensure_ascii=False, indent=1))
            if shot:
                pg.screenshot(path=os.path.join(SHOTS, shot))
            back_to_map(pg)
        out["pageerrors"] = errs
        print("PAGEERRORS:", errs)
        with open("/home/hatch/workspace/linji-work128/qa128/a2_probe.json", "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        br.close()

if __name__ == "__main__":
    main()
