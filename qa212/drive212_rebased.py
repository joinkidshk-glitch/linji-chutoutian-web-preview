# -*- coding: utf-8 -*-
"""v20a212 落地重驗：喺 rebase 後嘅分支（main b1ca47a＋v212）全套重跑 drive212
全部 7 場，寫入 drive212_rebased.json（唔覆蓋原本 drive212.json 舊基底證據）。"""
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/linji-work212/qa212")
import drive212 as t
from playwright.sync_api import sync_playwright


def main():
    srv = t.d.serve()
    results = {}
    try:
        with sync_playwright() as pw:
            for cfg in t.CASES:
                t.run_case(pw, cfg, results)
            results["map_932"] = t.run_map_case(pw)
        with open(os.path.join(t.QA, "drive212_rebased.json"), "w",
                  encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        npass = 0
        for k, v in results.items():
            bad = {kk: vv for kk, vv in (v.get("checks") or {}).items()
                   if not vv}
            ok = not bad and not v.get("error")
            npass += 1 if ok else 0
            print(f"  {k}: {'PASS' if ok else 'FAIL'} "
                  f"bad={json.dumps(bad, ensure_ascii=False)} "
                  f"errs={v.get('pageerrors')}", flush=True)
        print(f"== REBASED DRIVE SUMMARY {npass}/{len(results)} cases PASS ==",
              flush=True)
        for k in ("film_nom_932", "film_won_932", "film_won_700",
                  "music_gal_932", "ad_dec_932"):
            o = results[k]
            pack = o.get("pack") or {}
            wins = []
            for c in pack.get("cats") or []:
                w = c.get("winner") or {}
                if isinstance(w, dict):
                    wins.append(f"{c.get('label')}:{w.get('star','')}"
                                f"《{w.get('title','')}》")
                else:
                    wins.append(f"{c.get('label')}:{w}")
            print(k, "| winners:", " / ".join(wins), flush=True)
            print("   c5:", o.get("c5_figure_centers"),
                  "c1last:", o.get("c1_lastcat_cards_bright"),
                  "c1cat2:", o.get("c1_cat_title_cards_bright"), flush=True)
    finally:
        t.d.stop(srv)


if __name__ == "__main__":
    main()
