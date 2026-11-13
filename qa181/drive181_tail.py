# -*- coding: utf-8 -*-
"""v181 黃字 fix 尾段補拍：主 drive181 取樣時鐘漂移 ~2 秒，每 run 最尾 1–2 個 beat
（won glamour／nominated comfort／gallery reveal）嗰陣舞台已拆走，截圖＋DOM 證據缺失；
700_won walkup 截圖亦失敗，檔仲係上一輪（修前）舊圖。
本腳本每場只取一個尾段 beat（截圖先、DOM 證據後），唔做前面 beats，唔累積漂移，
補齊 7 張修後截圖＋幾何證據。報告寫 qa181/drive181_tail_report.json。"""
import os, sys, time, json
sys.path.insert(0, "/home/hatch/workspace/linji-work181/qa181")
import drive181 as d
from playwright.sync_api import sync_playwright

TAIL = {"won": [("walkup", 10000), ("glamour", 11500)],
        "nominated": [("comfort", 10000)], "gallery": [("reveal", 8000)]}
REPORT = {"runs": {}}


def run_tail(pg, vp, outcome, first=False):
    key = f"{vp}_{outcome}"
    tails = TAIL[outcome]
    print(f"== {key} tails {[b for b, _ in tails]} ==", flush=True)
    if not d.trigger_invite(pg, outcome, first=first):
        print("  !! 等唔到請柬 modal", flush=True)
        REPORT["runs"][key] = {"invite": False}
        return False
    if not d.modal_click(pg, d.ATTEND[outcome]):
        print(f"  !! 撳唔到{d.ATTEND[outcome]}", flush=True)
        REPORT["runs"][key] = {"invite": True, "attend": False}
        return False
    t0 = None
    for _ in range(10):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => !!document.querySelector('.awd62-stage')"):
            t0 = time.time()
            break
    if t0 is None:
        print("  !! 撳完冇舞台", flush=True)
        REPORT["runs"][key] = {"invite": True, "attend": True, "stage": False}
        return False
    samples = []
    all_ok = True
    for beat, target in tails:
        wait_ms = max(0, int((target - 300) - (time.time() - t0) * 1000))
        pg.wait_for_timeout(wait_ms)
        shot_path = os.path.join(d.SHOTS, f"{key}_{beat}.png")
        shot_ok = True
        try:
            pg.locator(".awd62-frame").screenshot(path=shot_path, timeout=5000)
        except Exception as e:
            shot_ok = False
            print(f"  shot {beat} failed: {str(e)[:80]}", flush=True)
        ev = pg.evaluate(d.EVIDENCE_JS)
        g = ev.get("geom") or {}
        ok = shot_ok and bool(g.get("subInsideBoard")) and bool(g.get("subAboveHeads")) and bool(g.get("boardAboveGlyph"))
        all_ok = all_ok and ok
        print(f"  [{beat}] shot={shot_ok} board={ev['board']!r} cap={(ev['caption'] or '')[:40]!r} "
              f"geomIn={g.get('subInsideBoard')} aboveHead={g.get('subAboveHeads')} "
              f"aboveGlyph={g.get('boardAboveGlyph')} lines={g.get('subLines')}", flush=True)
        samples.append({"beat": beat, "shot": shot_ok, "ev": ev})
    stage_gone = False
    for _ in range(20):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => !document.querySelector('.awd62-stage')"):
            stage_gone = True
            break
    pg.wait_for_timeout(800)
    d.modal_click(pg, "收下這晚")
    pg.wait_for_timeout(1200)
    d.dismiss_encounter(pg)
    REPORT["runs"][key] = {"invite": True, "attend": True, "stage": True,
                           "samples": samples, "stage_gone": stage_gone}
    return all_ok and stage_gone


def main():
    srv = d.serve(d.ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            for vp in (932, 700):
                pg = br.new_page(viewport={"width": vp, "height": 844})
                pg.on("pageerror", lambda e: REPORT.setdefault("errors", []).append(f"{vp}: {e}"))
                pg.on("response", lambda r: REPORT.setdefault("http_fail", []).append(f"{vp} {r.status} {r.url}") if r.status >= 400 else None)
                pg.on("requestfailed", lambda r: REPORT.setdefault("http_fail", []).append(f"{vp} REQFAIL {r.url}"))
                assert d.new_game(pg), "new game failed"
                d.dismiss_encounter(pg)
                for i, outcome in enumerate(("won", "nominated", "gallery")):
                    ok = run_tail(pg, vp, outcome, first=(i == 0))
                    print(f"  tail {vp}_{outcome}: {'OK' if ok else 'CHECK'}", flush=True)
                    pg.wait_for_timeout(600)
                pg.close()
            br.close()
    finally:
        d.stop(srv)
    with open(os.path.join(d.HERE, "drive181_tail_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)
    print("errors:", REPORT.get("errors", []))
    print("http_fail:", REPORT.get("http_fail", []))
    print("runs:", {k: (v.get("shot"), v.get("stage_gone")) for k, v in REPORT["runs"].items()})


if __name__ == "__main__":
    main()
