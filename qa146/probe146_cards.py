#!/usr/bin/env python3
"""Capture WF4 card screenshots for given events on a given root (for before/after compare).
Usage: probe146_cards.py [root] [port] [ev:title:tag ...]  (viewport fixed 430x700)
Saves qa146/shots146/cmp_<tag>_430x700.png under root.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1]
PORT = int(sys.argv[2])
SPECS = [s.split(":") for s in sys.argv[3:]]
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = os.path.join(ROOT, "qa146", "shots146")
os.makedirs(SHOTS, exist_ok=True)
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
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        for ev, title, tag in SPECS:
            ctx = b.new_context(viewport={"width": 430, "height": 700})
            pg = ctx.new_page()
            ok = new_game_to_map(pg)
            found = False
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
                }""", ev)
                click_vis_btn(pg, "過一日")
                for _ in range(45):
                    pg.wait_for_timeout(1000)
                    h3 = modal_h3(pg)
                    if title in h3: found = True; break
                    if h3 == "確認過一日？":
                        if click_vis_btn(pg, "確定過一日"): continue
                    dismiss_once(pg)
                pg.wait_for_timeout(600)
                if found:
                    pg.screenshot(path=f"{SHOTS}/cmp_{tag}_430x700.png")
            print(tag, "found:", found)
            ctx.close()
        b.close()
finally:
    srv.terminate()
