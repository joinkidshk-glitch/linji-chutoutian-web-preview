# -*- coding: utf-8 -*-
"""重跑 drive212 嘅兩場失敗場次（music_gal_932、ad_dec_932），用已修正嘅探針
（fresh-frame 補影＋C1 dim_pct 閾值＋C5 幕布 edge 過濾），結果合併入 drive212.json。"""
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/linji-work212/qa212")
import drive212 as t

d = t.d
from playwright.sync_api import sync_playwright


def main():
    srv = d.serve()
    results = {}
    try:
        with sync_playwright() as pw:
            for cfg in t.CASES:
                if cfg[0] not in ("music_gal_932", "ad_dec_932"):
                    continue
                t.run_case(pw, cfg, results)
        old = {}
        p = os.path.join(t.QA, "drive212.json")
        if os.path.exists(p):
            old = json.load(open(p, encoding="utf-8"))
        old.update(results)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(old, f, ensure_ascii=False, indent=1)
        npass = 0
        for k, v in old.items():
            bad = {kk: vv for kk, vv in (v.get("checks") or {}).items() if not vv}
            ok = not bad and not v.get("error")
            npass += 1 if ok else 0
            print(f"  {k}: {'PASS' if ok else 'FAIL'} bad={json.dumps(bad, ensure_ascii=False)} errs={v.get('pageerrors')}")
        print(f"== RERUN SUMMARY {npass}/{len(old)} cases PASS ==", flush=True)
        for k in ("music_gal_932", "ad_dec_932"):
            o = old[k]
            print(k, "c5:", o.get("c5_figure_centers"), "c1last:", o.get("c1_lastcat_cards_bright"),
                  "c1cat2:", o.get("c1_cat_title_cards_bright"), flush=True)
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
