#!/usr/bin/env python3
"""v146 A1 mechanism probe: with the WF4 stage modal open, set #app.scrollTop=216
and re-measure. Pristine (absolute mask inside #app) should shift modal y 149 -> -67
(the v134 review bad state). Fixed (position:fixed mask) must stay at y=149.
Usage: probe146_scroll.py [root] [port] [W] [H]
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/linji-work146")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8997
W = int(sys.argv[3]) if len(sys.argv) > 3 else 430
H = int(sys.argv[4]) if len(sys.argv) > 4 else 700
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# reuse flow helpers from probe146_a1 by importing is awkward (it runs on import);
# duplicate the small flow here.
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
def geo(pg):
    return pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect();
        return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height)}; };
      const app = q('#app'), mask = q('#mask'), modal = q('#modal'), h3 = q('#modal h3');
      return { appScrollTop: app ? app.scrollTop : null, appScrollH: app ? app.scrollHeight : null,
        appClientH: app ? app.clientHeight : null, maskPos: mask ? getComputedStyle(mask).position : null,
        modal: r(modal), h3: r(h3), h3text: h3 ? h3.textContent : '', mask: r(mask) };
    }""")
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
out = {}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        ctx = b.new_context(viewport={"width": W, "height": H})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        ok = new_game_to_map(pg)
        out["toMap"] = ok
        if ok:
            for _ in range(30):
                if vis_btn(pg, "過一日"): break
                if click_vis_btn(pg, "開始今日行程"): pg.wait_for_timeout(1000); continue
                if not dismiss_once(pg):
                    if not click_vis_btn(pg, "返回地圖"): pg.wait_for_timeout(500)
                pg.wait_for_timeout(700)
            pg.evaluate("""() => {
                if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
                S.wf4.pending = 'wf4_ev_day02'; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
            }""")
            click_vis_btn(pg, "過一日")
            found = False
            for _ in range(45):
                pg.wait_for_timeout(1000)
                h3 = modal_h3(pg)
                if "傳呼台" in h3: found = True; break
                if h3 == "確認過一日？":
                    if click_vis_btn(pg, "確定過一日"): continue
                dismiss_once(pg)
            pg.wait_for_timeout(800)
            out["found"] = found
            if found:
                out["before"] = geo(pg)
                set_ok = pg.evaluate("() => { const a = document.getElementById('app'); a.scrollTop = 216; return a.scrollTop; }")
                out["scrollTopSet"] = set_ok
                pg.wait_for_timeout(400)
                out["after"] = geo(pg)
                pg.screenshot(path=f"{ROOT}/qa146/scroll_after.png")
                print("before modal y=%s h3 y=%s appScrollTop=%s scrollH=%s" % (
                    out["before"]["modal"]["y"], out["before"]["h3"]["y"],
                    out["before"]["appScrollTop"], out["before"]["appScrollH"]))
                print("set scrollTop -> %s" % set_ok)
                print("after  modal y=%s h3 y=%s appScrollTop=%s" % (
                    out["after"]["modal"]["y"], out["after"]["h3"]["y"], out["after"]["appScrollTop"]))
        out["pageerrors"] = errs
        b.close()
finally:
    srv.terminate()
json.dump(out, open(f"{ROOT}/qa146/scroll_{W}x{H}.json", "w"), ensure_ascii=False, indent=1)
print("done", ROOT)
