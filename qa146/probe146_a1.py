#!/usr/bin/env python3
"""v146 A1 probe: WF4 stage modal (day02) geometry, repeated runs.
Usage: probe146_a1.py [root] [port] [runs] [W] [H] [ev] [title-substr]
Dumps modal/h3/stage/plate rects + #app/#mask rects + viewport metrics per run.
Exit 0 iff every run has h3 fully visible (h3.y>=0 and h3.bottom<=vh) and modal.y>=0.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/linji-work146")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8995
RUNS = int(sys.argv[3]) if len(sys.argv) > 3 else 5
W = int(sys.argv[4]) if len(sys.argv) > 4 else 430
H = int(sys.argv[5]) if len(sys.argv) > 5 else 700
EV = sys.argv[6] if len(sys.argv) > 6 else "wf4_ev_day02"
TITLE = sys.argv[7] if len(sys.argv) > 7 else "傳呼台"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"

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
        if btn.is_visible(timeout=400):
            btn.click(timeout=1000); return True
    except Exception:
        pass
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
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height),
                top:Math.round(b.top), bottom:Math.round(b.bottom), display: cs.display, position: cs.position}; };
      const modal = q('#modal'), h3 = q('#modal h3'), sub = q('#modal .sub'),
            stage = q('#modal .sp-bg-layer'), plate = q('#modal .dlg106-plate'),
            app = q('#app'), mask = q('#mask');
      return { vh: window.innerHeight, vw: window.innerWidth, scrollY: Math.round(window.scrollY),
        vvH: Math.round(window.visualViewport ? window.visualViewport.height : -1),
        docScrollH: document.documentElement.scrollHeight, bodyScrollH: document.body.scrollHeight,
        app: r(app), mask: r(mask), modal: r(modal), h3: r(h3), h3text: h3 ? h3.textContent : '',
        sub: r(sub), stage: r(stage), plate: r(plate),
        modalScrollH: modal ? modal.scrollHeight : null, modalClientH: modal ? modal.clientHeight : null };
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
results = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        for run in range(RUNS):
            ctx = b.new_context(viewport={"width": W, "height": H})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            failed = []
            pg.on("requestfailed", lambda r: failed.append(r.url))
            ok = new_game_to_map(pg)
            g = {"run": run, "toMap": ok}
            if ok:
                for _ in range(30):
                    if vis_btn(pg, "過一日"): break
                    if click_vis_btn(pg, "開始今日行程"): pg.wait_for_timeout(1000); continue
                    if not dismiss_once(pg):
                        if not click_vis_btn(pg, "返回地圖"): pg.wait_for_timeout(500)
                    pg.wait_for_timeout(700)
                pg.evaluate("""(ev) => {
                    if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
                    S.wf4.pending = ev; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
                }""", EV)
                click_vis_btn(pg, "過一日")
                found = False
                for _ in range(45):
                    pg.wait_for_timeout(1000)
                    h3 = modal_h3(pg)
                    if TITLE in h3: found = True; break
                    if h3 == "確認過一日？":
                        if click_vis_btn(pg, "確定過一日"): continue
                    dismiss_once(pg)
                pg.wait_for_timeout(800)
                g.update(geo(pg) if found else {})
                g["found"] = found
                g["pageerrors"] = errs; g["failedReq"] = failed
                pg.screenshot(path=f"{ROOT}/qa146/a1_{EV}_{W}x{H}_run{run}.png")
            else:
                g["found"] = False
            results.append(g)
            m = g.get("modal") or {}; h = g.get("h3") or {}
            print(f"run{run} found={g.get('found')} modal y={m.get('y')} h={m.get('h')} h3 y={h.get('y')} bottom={h.get('bottom')} "
                  f"app h={(g.get('app') or {}).get('h')} mask h={(g.get('mask') or {}).get('h')} mask y={(g.get('mask') or {}).get('y')} "
                  f"vh={g.get('vh')} scrollY={g.get('scrollY')} pageerrors={len(errs)} failedReq={len(failed)}")
            ctx.close()
        b.close()
finally:
    srv.terminate()

ok_all = all(r.get("found") and (r.get("h3") or {}).get("y", -1) >= 0
             and (r.get("h3") or {}).get("bottom", 99999) <= r.get("vh", 0)
             and (r.get("modal") or {}).get("y", -1) >= 0
             and not r.get("pageerrors") and not r.get("failedReq") for r in results)
json.dump(results, open(f"{ROOT}/qa146/a1_{EV}_{W}x{H}.json", "w"), ensure_ascii=False, indent=1)
print("A1-ALL-PASS" if ok_all else "A1-FAIL")
sys.exit(0 if ok_all else 1)
