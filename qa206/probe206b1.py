# -*- coding: utf-8 -*-
"""v20a206 B1 實駕抽查（rebase 後重驗）：seed 兩單重寫事件，核實新標題＋新 beat 文案真係上台。
用法：/home/hatch/pwenv49/bin/python qa206/probe206b1.py
重用 drive206c2 嘅 new_game／seed_pending／wf4_info／handle_wf4（port 改 8998）。"""
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import drive206c2 as d
from playwright.sync_api import sync_playwright

d.PORT = 8998
d.URL = "http://127.0.0.1:8998/index.html"
SHOTS = os.path.join(d.HERE, "shots206b1")
os.makedirs(SHOTS, exist_ok=True)
d.SHOTS = SHOTS

TARGETS = [
    ("wf4_ev_set32", 10, "外景小巴嗰個暈車", "暈車"),
    ("wf4_ev_set35", 11, "海邊嗰場晨戲", "潮水一路漲"),
]
REPORT = {"cases": {}, "errors": [], "http_fail": []}

def modal_text(pg):
    return pg.evaluate("""() => { const m = document.querySelector('#modal-inner'); return m ? m.innerText : ''; }""")

def main():
    srv = d.serve(d.ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
            pg.on("requestfailed", lambda r: REPORT["http_fail"].append(r.url))
            assert d.new_game(pg, slot="1"), "new game failed"
            for (eid, day, expect_title, phrase) in TARGETS:
                r = d.seed_pending(pg, eid, day)
                info = None
                t0 = time.time()
                while time.time() - t0 < 60:
                    if d.ceremony_active(pg):
                        pg.wait_for_timeout(1500)
                        continue
                    info = d.wf4_info(pg)
                    if info:
                        break
                    rr = d.dismiss_once(pg)
                    if rr:
                        pg.wait_for_timeout(700)
                        continue
                    if d.map_visible(pg):
                        pg.wait_for_timeout(1000)
                        if not d.ceremony_active(pg) and not d.wf4_info(pg):
                            break
                text = modal_text(pg) if info else ""
                ok = bool(info and info["title"] == expect_title and phrase in text)
                if info:
                    d.handle_wf4(pg, "B1_" + eid.replace("wf4_ev_", ""))
                    d.settle(pg, timeout_ms=8000)
                    d.go_map(pg)
                REPORT["cases"][eid] = {"ok": ok, "seed_day": day, "title": info["title"] if info else None,
                                        "expect_title": expect_title, "phrase": phrase,
                                        "phrase_in_modal": phrase in text}
                print("B1", eid, REPORT["cases"][eid], flush=True)
            REPORT["cases"]["errors_932"] = errs
            br.close()
    finally:
        d.stop(srv)
    with open(os.path.join(d.HERE, "probe206b1_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=2)
    n_ok = sum(1 for k, v in REPORT["cases"].items() if isinstance(v, dict) and v.get("ok"))
    print(f"RESULT {n_ok}/{len(TARGETS)} ok, pageerrors={len(REPORT['cases']['errors_932'])}, http_fail={len(REPORT['http_fail'])}")

if __name__ == "__main__":
    main()
