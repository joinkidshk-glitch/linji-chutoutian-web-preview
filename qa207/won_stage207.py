# -*- coding: utf-8 -*-
"""v207 landing won-stage 驗證：用 v208 式強 seed 跑 music won 全場，
驗 C1 spotlight／veil 喺 won 揭曉嗰陣（亮度差）＋B2／B3。
結果寫 qa207/won_stage207.json；截圖 qa207/shots207/v207_won_*。"""
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/linji-work207/qa207")
import drive207 as d207

sys.path.insert(0, "/home/hatch/workspace/linji-work207/qa188")
import drive188 as d

from playwright.sync_api import sync_playwright

def main():
    srv = d.serve()
    results = {}
    try:
        with sync_playwright() as pw:
            results["music_won_932"] = d207.run_stage_case(
                pw, "music_won_932", "award_golddisc_music", 1990, "nominee",
                932, 80, 60, {"rec": 3, "film_lead": 2, "tv_lead": 2, "ad_lead": 1},
                want_outcome="won")
        with open(os.path.join(d207.d.QA, "won_stage207.json"), "w",
                  encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        for k, v in results.items():
            bad = {kk: vv for kk, vv in (v.get("checks") or {}).items() if not vv}
            print(f"  {k}: {'PASS' if not bad and not v.get('error') else 'FAIL'} "
                  f"bad={json.dumps(bad, ensure_ascii=False)} errs={v.get('pageerrors')}",
                  flush=True)
    finally:
        d.stop(srv)

if __name__ == "__main__":
    main()
