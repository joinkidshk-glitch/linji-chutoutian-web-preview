# -*- coding: utf-8 -*-
"""最小探針：global 可見性＋seed 返值＋seed 後即時狀態＋reload 後狀態。"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import OUT, EXE, serve, stop, new_game, STATE_JS, SEED_DAYEND_JS
from playwright.sync_api import sync_playwright

def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=EXE)
            ctx = b.new_context(viewport={"width": 430, "height": 932})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("http://127.0.0.1:18997/index.html")
            pg.wait_for_timeout(3000)
            print("TYPEOF:", json.dumps(pg.evaluate("""() => ({
              S: typeof S, GIGS: typeof GIGS, saveQ: typeof saveQ,
              toggleCopyPanel: typeof toggleCopyPanel, renderNotebook: typeof renderNotebook,
              openCopyFromDay: typeof openCopyFromDay, planSelDay: typeof planSelDay,
              dayPlanLocked: typeof dayPlanLocked, todayPlanId: typeof todayPlanId,
              runScheduleFromToday: typeof runScheduleFromToday, startTodayScheduleFromMap: typeof startTodayScheduleFromMap
            })"""), ensure_ascii=False))
            print("new_game:", new_game(pg, confirm_plan=False))
            pg.wait_for_timeout(800)
            print("SEED_RET:", json.dumps(pg.evaluate(SEED_DAYEND_JS, "soft"), ensure_ascii=False))
            print("POST_SEED:", json.dumps(pg.evaluate("""() => ({dayIndex: S.dayIndex, weekPlan: S.weekPlan,
              shoots: (S.shoots||[]).map(x=>x.id), todayPlan: (typeof todayPlanId==='function') ? todayPlanId() : null})"""), ensure_ascii=False))
            print("SAVE:", pg.evaluate("() => { try { saveQ(); return 'ok'; } catch(e){ return String(e); } }"))
            pg.wait_for_timeout(1500)
            pg.reload()
            pg.wait_for_timeout(2500)
            print("AFTER_RELOAD_STATE:", json.dumps(pg.evaluate(STATE_JS), ensure_ascii=False))
            print("AFTER_RELOAD_S:", pg.evaluate("() => (typeof S!=='undefined' && S!==null) ? 'S exists' : 'S null/undef'"))
            # 撳繼續
            ok = pg.evaluate("""() => { const bs=[...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null && (b.textContent||'').includes('繼續'));
              if (!bs.length) return false; bs[0].click(); return true; }""")
            print("CLICK_CONTINUE:", ok)
            pg.wait_for_timeout(2000)
            print("POST_CONTINUE:", json.dumps(pg.evaluate("""() => ({dayIndex: (typeof S!=='undefined' && S) ? S.dayIndex : null,
              weekPlan: (typeof S!=='undefined' && S) ? S.weekPlan : null,
              shoots: (typeof S!=='undefined' && S) ? (S.shoots||[]).map(x=>x.id) : null,
              todayPlan: (typeof todayPlanId==='function') ? todayPlanId() : null})"""), ensure_ascii=False))
            print("PAGEERRORS:", errs)
            ctx.close(); b.close()
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
