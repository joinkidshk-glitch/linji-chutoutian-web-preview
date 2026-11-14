# -*- coding: utf-8 -*-
"""v20a213 星期日典禮針對性檢查：台慶 1991，典禮日 12 月 1 日（星期日，day 699）。
pre-existing v192 C1：舊制典禮日週日，翌日（週一）晨報俾週結算吞咗，週二先出。
v213 唔修呢項，淨係驗證唔惡化：報紙喺邊一日出（700 週一＝改善咗；701 週二＝同舊制一樣）。
用法：/home/hatch/pwenv49/bin/python qa213/drive213_sunday.py [work|pristine]
  work（預設）：~/workspace/linji-work213 port 8914；pristine：~/workspace/linji-pristine213 port 8915。
  work：請柬 11 月 28（696）→ 典禮日 699 晚上播；pristine：請柬 699 當日朝早，撳出席即播。
報紙偵測雙軌：modal 出現嗰陣記 dayIndex；若 settle 食咗個 modal，就用 clippings 增長＋當日 dayIndex 補記。
結果寫入 qa213/drive213_sunday_report_<which>.json；截圖 qa213/shots213/。
"""
import os, sys, json
sys.path.insert(0, "/home/hatch/workspace/linji-work213/qa213")
import drive213 as d
from playwright.sync_api import sync_playwright

WHICH = sys.argv[1] if len(sys.argv) > 1 else "work"
if WHICH == "pristine":
    d.ROOT = "/home/hatch/workspace/linji-pristine213"
    d.PORT = 8915
    INVITE_DAY = 699
    NEED_DAY_RUN = False
else:
    d.ROOT = "/home/hatch/workspace/linji-work213"
    d.PORT = 8914
    INVITE_DAY = 696
    NEED_DAY_RUN = True
OUT = f"/home/hatch/workspace/linji-work213/qa213/drive213_sunday_report_{WHICH}.json"


def paper_watch(pg, timeout_s=15):
    """等報紙 modal；返 (dayIndex|None, text, method)。"""
    for _ in range(int(timeout_s * 2)):
        mt = d.modal_text(pg)
        if mt["visible"] and "收下這份剪報" in mt["btns"]:
            st = d.state(pg)
            return st["day"], mt["text"][:400], "modal"
        pg.wait_for_timeout(500)
    return None, "", ""


def run(pw):
    print(f"\n===== Sunday ceremony ({WHICH}) =====", flush=True)
    ctx = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not d.new_game(pg, f"http://127.0.0.1:{d.PORT}/index.html"):
            res["new_game"] = False; ctx.close(); return res
        d.dismiss_encounter(pg)
        d.settle_to_map(pg)
        picks = pg.evaluate(d.PICK_GIGS_JS)
        pg.evaluate(d.SEED_JS, {"picks": picks, "day": INVITE_DAY, "fame": 30, "credit": 52})
        pr = pg.evaluate(d.PRESENT_JS)
        res["invite"] = pr
        print("invite:", json.dumps(pr, ensure_ascii=False)[:300], flush=True)
        res["clickedAttend"] = d.click_modal(pg, ["出席"], 1200)
        pg.wait_for_timeout(2000)
        res["stageRightAfterAttend"] = d.stage_present(pg)
        if NEED_DAY_RUN:
            d.settle_to_map(pg)
            pg.evaluate("""() => {
              S.dayIndex = 699;  // 1991-12-01 星期日（699%7=6）
              S.weekPlan = S.weekPlan || [];
              while (S.weekPlan.length < 7) S.weekPlan.push('rest');
              S.weekPlan[6] = 'rest'; S.weekPlan[0] = 'rest'; S.weekPlan[1] = 'rest';
              S.stress = 0;
            }""")
            day = d.run_day_via_map(pg)
            res["dayRun"] = day
            tr = d.continue_from_dayend(pg)
            if tr and tr[0].startswith("no-continue-btn"):
                # 週末板：掣係「回家結算」（ended → nextNbReward → 晚間 hook）
                c = d.click_modal(pg, ["回家結算"], 1200)
                tr = [f"回家結算:{c}"]
            res["continueTrace"] = tr
        else:
            pg.evaluate("""() => {
              S.weekPlan = S.weekPlan || [];
              while (S.weekPlan.length < 7) S.weekPlan.push('rest');
              S.weekPlan[6] = 'rest'; S.weekPlan[0] = 'rest'; S.weekPlan[1] = 'rest';
              S.stress = 0;
            }""")
        sk = d.skip_ceremony(pg, f"S_{WHICH}")
        res["ceremony"] = sk
        ok = d.wait_for(lambda: d.modal_text(pg)["visible"] and "收下這晚" in d.modal_text(pg)["text"], 15000)
        res["resultCard"] = ok
        res["clickedResult"] = d.click_modal(pg, ["收下這晚"], 1200) if ok else None
        # 報紙：先等 modal；週末場要先由屋企返地圖（觸發週一晨鏈 → 報紙 step），
        # 再用 clippings 增長補記（settle 有機會先食咗個 modal）。
        clip0 = d.state(pg)["clippings"]
        pday, ptext, method = paper_watch(pg, 10)
        if pday is None:
            pg.evaluate("() => { const b = document.querySelector('#home-back-map-tabs'); if (b) b.click(); }")
            pg.wait_for_timeout(1500)
            d.dismiss_encounter(pg)
            pday, ptext, method = paper_watch(pg, 15)
        if pday is None:
            d.settle_to_map(pg)
            pday, ptext, method = paper_watch(pg, 10)
        if pday is not None:
            res["paperDay"] = pday; res["paperText"] = ptext; res["paperMethod"] = method
            pg.screenshot(path=os.path.join(d.SHOTS, f"S_{WHICH}_paper_day{pday}.png"))
            d.click_modal(pg, ["收下這份剪報"], 1000)
        d.dismiss_modals(pg)
        d.dismiss_encounter(pg)
        st = d.state(pg)
        res["stateAfterResult"] = st
        if pday is None and st["clippings"] > clip0:
            res["paperDay"] = st["day"]; res["paperMethod"] = "clipping"
        print("paper day (after result):", res.get("paperDay"), "state:", json.dumps(st, ensure_ascii=False), flush=True)
        # 未出就逐日行到 701
        for extra_day in (700, 701):
            if res.get("paperDay") is not None:
                break
            clip0 = d.state(pg)["clippings"]
            pg.evaluate(f"() => {{ S.weekPlan = S.weekPlan || []; while (S.weekPlan.length < 7) S.weekPlan.push('rest'); S.weekPlan[{extra_day % 7}] = 'rest'; S.stress = 0; }}")
            d.run_day_via_map(pg)
            d.continue_from_dayend(pg)
            pday, ptext, method = paper_watch(pg, 15)
            if pday is not None:
                res["paperDay"] = pday; res["paperText"] = ptext; res["paperMethod"] = method
                pg.screenshot(path=os.path.join(d.SHOTS, f"S_{WHICH}_paper_day{pday}.png"))
                d.click_modal(pg, ["收下這份剪報"], 1000)
            d.dismiss_modals(pg)
            d.dismiss_encounter(pg)
            st = d.state(pg)
            if pday is None and st["clippings"] > clip0:
                res["paperDay"] = st["day"]; res["paperMethod"] = "clipping"
            print(f"after day {extra_day}: paperDay={res.get('paperDay')} day={st['day']}", flush=True)
        res["paperSeen"] = res.get("paperDay") is not None
        res["stateFinal"] = d.state(pg)
    finally:
        ctx.close()
    return res


def main():
    srv = d.serve(d.ROOT)
    try:
        with sync_playwright() as pw:
            res = run(pw)
    finally:
        d.stop(srv)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print("REPORT WRITTEN", OUT)


if __name__ == "__main__":
    main()
