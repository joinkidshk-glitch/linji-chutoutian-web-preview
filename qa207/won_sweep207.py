# -*- coding: utf-8 -*-
"""v207 landing won-seed sweep：用 v208 式跨媒介強 seed，搵一個 music won pack，
再跑完整舞台驗 C1 spotlight／veil 喺 won 揭曉嗰陣。
結果寫 qa207/won_sweep207.json；成功嗰陣截圖 qa207/shots207/v207_won_*。
"""
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/linji-work207/qa188")
import drive188 as d

d.ROOT = "/home/hatch/workspace/linji-work207"
d.QA = "/home/hatch/workspace/linji-work207/qa207"
d.SHOTS = "/home/hatch/workspace/linji-work207/qa207/shots207"
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 20791
os.makedirs(d.SHOTS, exist_ok=True)

sys.path.insert(0, "/home/hatch/workspace/linji-work207/qa207")
from drive207 import JS_SEEDED_RANDOM, JS_FORCE_PACK, JS_RECTS, force_pack_try

from playwright.sync_api import sync_playwright

# v208 式強 seed：跨媒介作品＋高 fame／credit（舊 seed base 0.82 贏唔到 0.875 贏線）
SEED_SETS = [
    # (ceremony, year, tier, fame, credit, roles)
    ("award_golddisc_music", 1990, "nominee", 80, 60,
     {"rec": 3, "film_lead": 2, "tv_lead": 2, "ad_lead": 1}),
    ("award_golddisc_music", 1991, "nominee", 80, 60,
     {"rec": 3, "film_lead": 2, "tv_lead": 2, "ad_lead": 1}),
    ("award_harbour_film", 1990, "nominee", 80, 60,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2, "tv_sup": 1, "ad_lead": 1}),
    ("award_harbour_film", 1991, "nominee", 80, 60,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2, "tv_sup": 1, "ad_lead": 1}),
]

def main():
    srv = d.serve()
    out = {"tried": [], "won": None}
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            try:
                pg = b.new_page(viewport={"width": 430, "height": 932})
                d.new_game(pg)
                for (cer, year, tier, fame, credit, roles) in SEED_SETS:
                    sd = d.seed(pg, {"year": year, "fame": fame, "credit": credit,
                                     "roles": roles, "payOverride": None}, [])
                    # sweep seeds 1..60
                    found = None
                    for seed in range(1, 61):
                        pg.evaluate(JS_SEEDED_RANDOM, seed)
                        fp = pg.evaluate(JS_FORCE_PACK, {"id": cer, "tier": tier})
                        if fp.get("bestOutcome") == "won":
                            found = (seed, fp)
                            break
                    rec = {"cer": cer, "year": year, "tier": tier, "fame": fame,
                           "credit": credit, "roles": roles,
                           "won_seed": found[0] if found else None,
                           "bestOutcome": (found[1] or {}).get("bestOutcome")}
                    out["tried"].append(rec)
                    print(rec, flush=True)
                    if found and out["won"] is None:
                        out["won"] = {"cer": cer, "year": year, "tier": tier,
                                      "seed": found[0], "roles": roles, "fame": fame,
                                      "credit": credit}
            finally:
                b.close()
    finally:
        d.stop(srv)
    with open(os.path.join(d.QA, "won_sweep207.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("WON:", out["won"], flush=True)

if __name__ == "__main__":
    main()
