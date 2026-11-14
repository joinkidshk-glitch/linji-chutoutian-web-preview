# -*- coding: utf-8 -*-
"""診斷：星期日典禮後，週一返到地圖，獎報紙點解唔出。
重演 Sunday work 流程到 day 700 地圖，逐步 dump 報紙相關狀態。
用法：/home/hatch/pwenv49/bin/python qa213/drive213_sunday_diag.py
輸出：qa213/drive213_sunday_diag.json
"""
import os, sys, json
sys.path.insert(0, "/home/hatch/workspace/linji-work213/qa213")
import drive213 as d
from playwright.sync_api import sync_playwright

d.ROOT = "/home/hatch/workspace/linji-work213"
d.PORT = 8916
OUT = "/home/hatch/workspace/linji-work213/qa213/drive213_sunday_diag.json"

NP_JS = """() => ({
  day: S.dayIndex,
  lastPresentedDay: S.newspaperLastPresentedDay,
  pendingPaper: S.pendingMorningPaper ? {id: S.pendingMorningPaper.id, dayIndex: S.pendingMorningPaper.dayIndex, headline: S.pendingMorningPaper.headline} : null,
  queue: (S.newspaperQueue || []).map(q => ({eventKey: q.eventKey, publishDay: q.publishDay, enqueuedDay: q.enqueuedDay})),
  clippings: (S.newspaperClippings || []).map(c => ({dayIndex: c.dayIndex, date: c.dateLabel, headline: (c.headline||'').slice(0,40)})),
  paperShowing: !!(window.FREEPLAY_FW && FREEPLAY_FW._paperShowing),
  modal: (document.querySelector('#modal') || {}).innerText ? (document.querySelector('#modal').innerText || '').slice(0,200) : '',
  mapVisible: !!document.querySelector('#v-map:not(.hidden)') && !!(document.querySelector('#v-map') && document.querySelector('#v-map').offsetParent),
})"""


def run(pw):
    ctx = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs, "steps": []}
    def snap(label):
        s = pg.evaluate(NP_JS)
        res["steps"].append({"label": label, "state": s})
        print(f"--- {label} ---", json.dumps(s, ensure_ascii=False)[:600], flush=True)
        return s
    try:
        assert d.new_game(pg, f"http://127.0.0.1:{d.PORT}/index.html")
        d.dismiss_encounter(pg)
        d.settle_to_map(pg)
        picks = pg.evaluate(d.PICK_GIGS_JS)
        pg.evaluate(d.SEED_JS, {"picks": picks, "day": 696, "fame": 30, "credit": 52})
        snap("seeded-696")
        pg.evaluate(d.PRESENT_JS)
        d.click_modal(pg, ["出席"], 1200)
        pg.wait_for_timeout(2000)
        d.settle_to_map(pg)
        snap("after-attend-settled")
        pg.evaluate("""() => {
          S.dayIndex = 699;
          S.weekPlan = S.weekPlan || [];
          while (S.weekPlan.length < 7) S.weekPlan.push('rest');
          S.weekPlan[6] = 'rest'; S.weekPlan[0] = 'rest'; S.weekPlan[1] = 'rest';
          S.stress = 0;
        }""")
        day = d.run_day_via_map(pg)
        snap("after-run-day (board should be rest-Sunday)")
        tr = d.continue_from_dayend(pg)
        if tr and tr[0].startswith("no-continue-btn"):
            c = d.click_modal(pg, ["回家結算"], 1200)
            tr = [f"回家結算:{c}"]
        print("continue:", tr, flush=True)
        sk = d.skip_ceremony(pg, "DIAG")
        print("ceremony:", sk, flush=True)
        ok = d.wait_for(lambda: d.modal_text(pg)["visible"] and "收下這晚" in d.modal_text(pg)["text"], 15000)
        print("resultCard:", ok, flush=True)
        d.click_modal(pg, ["收下這晚"], 1200)
        pg.wait_for_timeout(2000)
        snap("after-result-card (should be home, day 700)")
        # 返地圖：撳 home-back-map-tabs
        r = pg.evaluate("""() => {
          const b = document.querySelector('#home-back-map-tabs');
          if (!b) return 'no-btn';
          if (!b.offsetParent) return 'btn-hidden';
          b.click(); return 'clicked';
        }""")
        print("home-back-map-tabs:", r, flush=True)
        pg.wait_for_timeout(3000)
        snap("after-home-tabs (Monday chain should have run)")
        # 再等一陣，睇報紙 modal 會唔會出
        pg.wait_for_timeout(5000)
        snap("after-wait-5s")
        # 週一要先確認新一週計劃先開日：dump planning 狀態，撳確認
        plan = pg.evaluate("""() => ({
          homeEditable: !!S.homeEditable,
          weekPlan: S.weekPlan,
          todayPlan: (typeof todayPlanId === 'function') ? todayPlanId() : null,
          confirmBtn: (() => { const b = document.querySelector('#btn-confirm-plan'); return b ? {visible: !!b.offsetParent, text: b.innerText} : null; })(),
          startBtn: (() => { const b = document.querySelector('#map-start-today'); return b ? {visible: !!b.offsetParent} : null; })(),
          endBtn: (() => { const b = document.querySelector('#map-end-day'); return b ? {visible: !!b.offsetParent} : null; })(),
        })""")
        print("planning:", json.dumps(plan, ensure_ascii=False), flush=True)
        res["planning"] = plan
        if plan.get("confirmBtn") and plan["confirmBtn"]["visible"]:
            pg.evaluate("() => document.querySelector('#btn-confirm-plan').click()")
            pg.wait_for_timeout(2000)
            snap("after-confirm-plan")
            # 確認後可能出「確定出發」之類
            d.click_first(pg, ["確定出發", "確定", "確認"], 1200)
            pg.wait_for_timeout(2000)
            snap("after-confirm-depart")
        # 開手帳 → 行程頁 → 確認本週行程 → 開始週一
        pg.evaluate("() => document.querySelector('#btn-menu').click()")
        pg.wait_for_timeout(800)
        d.click_first(pg, ["手帳"], 1000)
        pg.wait_for_timeout(1200)
        pg.evaluate("""() => {
          const t = document.querySelector('[data-htab="plan"]');
          if (t) t.click();
        }""")
        pg.wait_for_timeout(1200)
        snap("plan-pane-open")
        cb = pg.evaluate("() => { const b = document.querySelector('#btn-confirm-plan'); return b ? {visible: !!b.offsetParent, text: b.innerText, disabled: b.disabled} : null; }")
        print("confirmBtn now:", cb, flush=True)
        if cb and cb["visible"] and not cb["disabled"]:
            pg.evaluate("() => document.querySelector('#btn-confirm-plan').click()")
            pg.wait_for_timeout(1500)
            snap("after-confirm-plan2")
            d.click_first(pg, ["確定出發", "確定", "確認"], 1200)
            pg.wait_for_timeout(1500)
            snap("after-depart2")
        # 試行一日（週一休息 → 週二鏈）
        day2 = d.run_day_via_map(pg)
        print("run day2:", json.dumps(day2, ensure_ascii=False)[:300], flush=True)
        snap("after-run-day2")
        tr2 = d.continue_from_dayend(pg)
        print("continue2:", tr2, flush=True)
        pg.wait_for_timeout(3000)
        snap("after-continue2 (Tuesday chain should have run)")
        # 報紙 modal 有冇出（publishDay 700，應喺週一鏈出；若週二先出即係遲一日）
        for _ in range(20):
            mt = d.modal_text(pg)
            if mt["visible"] and "收下這份剪報" in mt["btns"]:
                st = d.state(pg)
                res["paperDay2"] = st["day"]
                res["paperText2"] = mt["text"][:300]
                print("PAPER FOUND day", st["day"], mt["text"][:200], flush=True)
                break
            pg.wait_for_timeout(500)
        else:
            print("no paper modal after continue2", flush=True)
            res["paperDay2"] = None
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
