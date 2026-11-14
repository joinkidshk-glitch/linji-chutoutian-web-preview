# -*- coding: utf-8 -*-
"""v20a193 Case C 根因 probe（instrumented copy 版）：serve /tmp/wf4probe193（已注入
window.__probe193 entry-log），忠實重跑 drive A→B→C，dump C-load 之後嘅晨鏈 trace。
用法：/home/hatch/pwenv49/bin/python qa193/probe193e.py
"""
import os, json, sys
sys.path.insert(0, os.path.join("/home/hatch/workspace/linji-work193", "qa193"))
import drive193 as D
from playwright.sync_api import sync_playwright

D.ROOT = "/tmp/wf4probe193"
D.PORT = 8994
D.URL = "http://127.0.0.1:8994/index.html"

def dump_probe(pg, tag):
    try:
        rows = pg.evaluate("() => (window.__probe193 || []).slice()")
    except Exception as e:
        print(tag, "dump failed:", e, flush=True)
        return []
    print("=== %s: %d probe entries ===" % (tag, len(rows)), flush=True)
    for r in rows:
        print(json.dumps(r, ensure_ascii=False), flush=True)
    return rows

def main():
    srv = D.serve(D.ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
            assert D.new_game(pg, slot="1"), "new game failed"
            assert D.seed_seen(pg, {"wf4_ev_set03": 1, "wf4_ev_st04": 1, "wf4_ev_cha03": 1, "wf4_ev_day02": 1}), "seed failed"
            resA = D.run_case_a(pg)
            print("A:", resA, flush=True)
            before = D.read_state(pg)
            pg.reload(); pg.wait_for_timeout(2500)
            D.load_slot(pg, "1")
            after = D.read_state(pg)
            print("B before:", before, "after:", after, flush=True)
            r = pg.evaluate("""() => {
              try {
                const raw = localStorage.getItem('starVolunteer_map_v19w');
                if (!raw) return {ok:false, err:'no save'};
                const o = JSON.parse(raw);
                const day = (o.dayIndex|0);
                o.wf4 = { lastDay: day - 5, seen: { 'wf4_ev_set03': 21, 'wf4_ev_st04': 7, 'wf4_ev_cha03': 2, __n: 30 },
                  pending: 'wf4_ev_set03', pendingDay: day, flags: {}, evDay: { 'wf4_ev_set03': day - 5, 'wf4_ev_st04': day - 3 },
                  locDay: -99, locTries: 0, fenFarewellDone: false };
                localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(o));
                return {ok:true, day};
              } catch(e){ return {ok:false, err:String(e)}; } }""")
            print("C seed old save:", r, flush=True)
            pg.reload(); pg.wait_for_timeout(2500)
            res = D.load_slot(pg, "1")
            print("load_slot settle ->", res, flush=True)
            print("state after load:", D.read_state(pg), "map:", D.map_visible(pg), flush=True)
            rows1 = dump_probe(pg, "AFTER-LOAD")
            D.go_map(pg)
            print("after go_map state:", D.read_state(pg), "map:", D.map_visible(pg), flush=True)
            vr = D.visit_loc(pg, 'cafe_cha', "C", [])
            print("visit_loc cafe_cha ->", vr, flush=True)
            stC = D.read_state(pg)
            print("FINAL state:", stC, flush=True)
            rows2 = dump_probe(pg, "FINAL")
            print("pageerrors:", errs, flush=True)
            with open(os.path.join(D.HERE, "probe193e.json"), "w", encoding="utf-8") as f:
                json.dump({"A": resA, "final_state": stC, "probe_after_load": rows1,
                           "probe_final": rows2, "errors": errs}, f, ensure_ascii=False, indent=2)
            br.close()
    finally:
        D.stop(srv)

if __name__ == "__main__":
    main()
