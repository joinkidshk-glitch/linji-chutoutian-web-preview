# -*- coding: utf-8 -*-
"""v20a215 實駕探針：boot → new_game → reload → 印標題畫面按鈕，確認讀檔路徑。"""
import os, sys
sys.path.insert(0, "/home/hatch/workspace/linji-work215/qa188")
import drive188 as d
d.ROOT = "/home/hatch/workspace/linji-work215"
d.QA = "/home/hatch/workspace/linji-work215/qa215"
d.SHOTS = "/home/hatch/workspace/linji-work215/qa215/shots215"
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 21590
os.makedirs(d.SHOTS, exist_ok=True)
from playwright.sync_api import sync_playwright

srv = d.serve()
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=d.EXE)
        pg = b.new_page(viewport={"width": 430, "height": 932})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        print("new_game:", d.new_game(pg))
        print("S day:", pg.evaluate("() => (window.S||{}).dayIndex"))
        pg.evaluate("() => { try { saveQ(); } catch(e){} return true; }")
        pg.reload()
        pg.wait_for_timeout(3000)
        btns = pg.evaluate("""() => [...document.querySelectorAll('button')].filter(b => {
          const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0;
        }).map(b => (b.textContent||'').trim()).filter(Boolean).slice(0, 30)""")
        print("buttons after reload:", btns)
        print("GIGS len:", pg.evaluate("() => (typeof GIGS!=='undefined' ? GIGS.length : -1)"))
        print("pageerrors:", errs)
        b.close()
finally:
    d.stop(srv)
