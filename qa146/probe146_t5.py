#!/usr/bin/env python3
"""v146 T5 retry: open agency loc-sheet, dump visible buttons, click 只查看通告欄, measure board modal."""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/linji-work146")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8996
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
out = {}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        ctx = b.new_context(viewport={"width": 430, "height": 700})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        ok = new_game_to_map(pg)
        out["toMap"] = ok
        if ok:
            opened = pg.evaluate("""() => {
              const btns = [...document.querySelectorAll('#map-area-list button, .map-area-list button, #v-map button')];
              const t = btns.find(x => (x.textContent||'').includes('電視台'));
              if (t) { t.click(); return true; } return false;
            }""")
            pg.wait_for_timeout(1500)
            # entry may intercept with a WF4/encounter modal; dismiss it to reach the sheet
            for _ in range(6):
                if not pg.evaluate("() => document.getElementById('mask').classList.contains('on')"):
                    break
                dismiss_once(pg)
                pg.wait_for_timeout(800)
            btns = pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet button, #loc-acts button, #loc-acts .act')].map(x => {
              const r = x.getBoundingClientRect(); const cs = getComputedStyle(x);
              return { t: (x.textContent||'').trim().slice(0, 30), vis: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' };
            }).filter(x => x.t);""")
            out["sheetOpened"] = opened
            out["sheetButtons"] = btns
            print("sheet buttons:", json.dumps(btns, ensure_ascii=False))
            board = click_vis_btn(pg, "只查看通告欄")
            pg.wait_for_timeout(1500)
            g = pg.evaluate("""() => {
              const q = s => document.querySelector(s);
              const r = el => { if(!el) return null; const b = el.getBoundingClientRect();
                return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height)}; };
              const mask = q('#mask'), modal = q('#modal'), h3 = q('#modal h3');
              return { maskOn: mask.classList.contains('on'), maskCls: [...mask.classList].join(' '),
                modal: r(modal), h3: h3 ? h3.textContent : '', modalMaxH: getComputedStyle(modal).maxHeight };
            }""")
            out["boardClicked"] = board
            out["boardModal"] = g
            print("board clicked:", board, "modal:", json.dumps(g, ensure_ascii=False))
            pg.screenshot(path=f"{ROOT}/qa146/shots146/t5_casting_retry_430x700.png")
            out["ok"] = bool(board and g["maskOn"] and g["modal"] and g["modal"]["y"] >= 0 and not errs)
        out["pageerrors"] = errs
        b.close()
finally:
    srv.terminate()
json.dump(out, open(f"{ROOT}/qa146/t5_retry.json", "w"), ensure_ascii=False, indent=1)
print("T5-RETRY " + ("PASS" if out.get("ok") else "FAIL"))
sys.exit(0 if out.get("ok") else 1)
