# -*- coding: utf-8 -*-
"""v20a197 rebase spot re-verification（932 viewport）：預載舊 drive197.json，
只重跑 drive197.run_viewport(932)，merge 返（唔洗走舊結果）。
用法：/home/hatch/pwenv49/bin/python qa197/run_rebase932.py
覆蓋：B1 主線「下一句」、B2、 B5、 B6（placeholder sheet）、B7、C1–C3、C6、U1、U2、U4、U6。
B1 巧遇／B4／B3／C4 請柬由 drive197i／j／run_awards197／probe_awards_b3 另行覆驗。
"""
import json, os, sys
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
        drive197.run_viewport(pw, 932, "932")
finally:
    drive197.stop(srv)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(drive197.R, f, ensure_ascii=False, indent=1)
print("== viewport 932 merged into drive197.json ==", flush=True)
