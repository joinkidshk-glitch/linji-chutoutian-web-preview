# -*- coding: utf-8 -*-
"""v20a108d 最闊配對測試頁實駕：方小龍＋Vera（合計 0.795）喺 390×844 舞台，
   用遊戲本體真 DLG108 模組跑自動收細，量 fitted 高＋淨空＋截圖。
   用法：/home/hatch/pwenv49/bin/python qa108d/fit_drive.py [base_url]"""
import sys, os, json
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8931/"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
HERE = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "qa108d/fit_test.html")
    pg.wait_for_timeout(3000)
    res = pg.evaluate("() => window.__fitResult || null")
    print("fitResult:", json.dumps(res, ensure_ascii=False))
    pg.screenshot(path=os.path.join(HERE, "shots", "post_fit_widest.png"))
    print("pageerrors:", errs[:4])
    b.close()
print("DONE fit")
