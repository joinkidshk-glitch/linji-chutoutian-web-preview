# -*- coding: utf-8 -*-
"""v20a193 實駕 case E 單獨重跑：v198×v193 互動（強制播 pending＋stale pending 同時存在嗰陣入茶餐廳）。
重用 drive193.py 嘅 helper（run_case_e 已修正：故事喺閂 sheet 嗰陣先讀）。
用法：/home/hatch/pwenv49/bin/python qa193/drive193e.py
寫 qa193/drive193e_report.json。"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import drive193 as d
from playwright.sync_api import sync_playwright

def main():
    srv = d.serve(d.ROOT)
    rep = {"errors": [], "http_fail": []}
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
            pg.on("requestfailed", lambda r: rep["http_fail"].append(r.url))
            res = d.run_case_e(pg)
            res["errors"] = errs
            rep["E_v198x193"] = res
            print("E:", json.dumps(res, ensure_ascii=False), flush=True)
            br.close()
    finally:
        d.stop(srv)
    with open(os.path.join(d.HERE, "drive193e_report.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print(json.dumps(rep, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
