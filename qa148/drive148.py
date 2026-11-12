#!/usr/bin/env python3
"""v20a148 live drive: WF4 card banner background-position per event.
Usage: drive148.py [root] [port]
Specs: (ev, title, tag, viewport_h, dayIndex_or_None)
 - st08 @700+@932 with dayIndex=365 (1991-01-01, cond yearMin:1991): expect bg_wf4_taxi.jpg, pos 50% 20%
 - st06 @700+@932: expect bg_wf4_market.jpg, pos 50% 75% (v146 B2 unchanged)
 - st05 @700, set08 @700, st04 @700: expect pos 50% 50% (shared rule unchanged)
Saves qa148/shots148/card_<tag>_<h>.png + qa148/drive148.json under root.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1]
PORT = int(sys.argv[2])
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = os.path.join(ROOT, "qa148", "shots148")
os.makedirs(SHOTS, exist_ok=True)
SPECS = [
    ("wf4_ev_st08", "的士佬送機有感", "st08", 700, 365),
    ("wf4_ev_st08", "的士佬送機有感", "st08", 932, 365),
    ("wf4_ev_st06", "魚檔阿姐認得你", "st06", 700, None),
    ("wf4_ev_st06", "魚檔阿姐認得你", "st06", 932, None),
    ("wf4_ev_st05", "K房霸咪嗰晚", "st05", 700, None),
    ("wf4_ev_set08", "派錯更去錯廠", "set08", 700, None),
    ("wf4_ev_st04", "最後一杯紅豆冰", "st04", 700, None),
]
def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)
def click_vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false; vis[0].click(); return true;
    }""", text)
def modal_h3(pg):
    return pg.evaluate("() => { const h = document.querySelector('#modal h3'); return h ? h.textContent : ''; }")
def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400): btn.click(timeout=1000); return True
    except Exception: pass
    return False
def wait_on_map(pg, secs=60):
    for _ in range(int(secs / 0.7)):
        if vis_btn(pg, "過一日"): return True
        if not dismiss_once(pg):
            if not click_vis_btn(pg, "返回地圖"): pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    return False
def new_game_to_map(pg):
    pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1")
    pg.wait_for_timeout(1500)
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
    pg.wait_for_timeout(1000)
    try:
        pg.locator('[data-slot="3"]').first.click(timeout=1500); pg.wait_for_timeout(800)
    except Exception: pass
    for _ in range(10):
        try:
            pg.get_by_text("跳過教學", exact=True).first.click(timeout=1200); pg.wait_for_timeout(600); break
        except Exception:
            try:
                pg.get_by_text("下一步", exact=True).first.click(timeout=1200); pg.wait_for_timeout(600)
            except Exception: break
    pg.wait_for_timeout(1200)
    return wait_on_map(pg)

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
results = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        for ev, title, tag, vh, day_idx in SPECS:
            ctx = b.new_context(viewport={"width": 430, "height": vh})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            rec = {"tag": tag, "vh": vh, "ev": ev, "found": False, "pageerrors": 0}
            ok = new_game_to_map(pg)
            if ok:
                for _ in range(30):
                    if vis_btn(pg, "過一日"): break
                    if click_vis_btn(pg, "開始今日行程"): pg.wait_for_timeout(1000); continue
                    if not dismiss_once(pg):
                        if not click_vis_btn(pg, "返回地圖"): pg.wait_for_timeout(500)
                    pg.wait_for_timeout(700)
                pg.evaluate("""([ev, dayIdx]) => {
                    if (dayIdx !== null && typeof S !== 'undefined') S.dayIndex = dayIdx;
                    if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
                    S.wf4.pending = ev; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
                }""", [ev, day_idx])
                click_vis_btn(pg, "過一日")
                for _ in range(45):
                    pg.wait_for_timeout(1000)
                    h3 = modal_h3(pg)
                    if title in h3: rec["found"] = True; break
                    if h3 == "確認過一日？":
                        if click_vis_btn(pg, "確定過一日"): continue
                    dismiss_once(pg)
                pg.wait_for_timeout(600)
                if rec["found"]:
                    rec["banner"] = pg.evaluate("""() => {
                      const el = document.querySelector('.wf4-scene105');
                      if (!el) return null;
                      const cs = getComputedStyle(el);
                      const r = el.getBoundingClientRect();
                      return {bg: cs.backgroundImage, pos: cs.backgroundPosition,
                              size: cs.backgroundSize, x: Math.round(r.x), y: Math.round(r.y),
                              w: Math.round(r.width), h: Math.round(r.height)};
                    }""")
                    rec["year"] = pg.evaluate("() => (typeof S !== 'undefined' && S.dayIndex !== undefined) ? S.dayIndex : null")
                    pg.screenshot(path=f"{SHOTS}/card_{tag}_{vh}.png")
            rec["pageerrors"] = len(errs)
            rec["errors"] = errs[:3]
            results.append(rec)
            print(tag, vh, "found:", rec["found"], "banner:", rec.get("banner"))
            ctx.close()
        b.close()
finally:
    srv.terminate()
with open(os.path.join(ROOT, "qa148", "drive148.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
n_pass = sum(1 for r in results if r["found"] and r.get("banner") and r["pageerrors"] == 0)
print(f"OVERALL {n_pass}/{len(results)}")
