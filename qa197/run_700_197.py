# -*- coding: utf-8 -*-
"""v197 700 run：預載舊 drive197.json 再跑 run_viewport(700)，唔洗走 932＋awards 結果。"""
import json, sys
sys.path.insert(0, "/home/hatch/workspace/linji-work197/qa197")
import drive197
from playwright.sync_api import sync_playwright
OUT = "/home/hatch/workspace/linji-work197/qa197/drive197.json"
with open(OUT, encoding="utf-8") as f:
    old = json.load(f)
drive197.R.clear(); drive197.R.update(old)
srv = drive197.serve()
try:
    with sync_playwright() as pw:
        drive197.run_viewport(pw, 700, "700")
finally:
    drive197.stop(srv)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(drive197.R, f, ensure_ascii=False, indent=1)
print("== 700 merged into drive197.json ==", flush=True)
