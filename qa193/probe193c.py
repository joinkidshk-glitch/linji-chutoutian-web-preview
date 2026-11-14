# -*- coding: utf-8 -*-
"""v20a193 Case C 根因 probe：舊 save pending=set03(見過 21 次) 點解 load 後仲喺度。

做法：new_game → 寫入同 drive Case C 一模一樣形狀嘅舊 save（day 當刻值、
lastDay=day-5、seen set03:21、pending=set03、pendingDay=day）→ reload 前先
wrap 晨鏈／WF4 相關函數（計 call 數＋返值＋關鍵謂詞快照）→ load_slot →
go_map → visit_loc cafe_cha → 讀 state＋dump __probe193。

用法：/home/hatch/pwenv49/bin/python qa193/probe193c.py
"""
import os, json, sys
sys.path.insert(0, os.path.join("/home/hatch/workspace/linji-work193", "qa193"))
import drive193 as D
from playwright.sync_api import sync_playwright

WRAP_JS = r"""
() => {
  window.__probe193 = [];
  const log = (fn, ret, extra) => {
    let snap = {};
    try {
      snap = { day: (typeof S !== 'undefined' && S) ? (S.dayIndex|0) : null,
        pending: (S && S.wf4) ? S.wf4.pending : null,
        lastDay: (S && S.wf4) ? S.wf4.lastDay : null,
        seenPend: (S && S.wf4 && S.wf4.pending) ? (S.wf4.seen[S.wf4.pending]||0) : null,
        plan: (typeof todayPlanId === 'function') ? String(todayPlanId()) : null };
    } catch(e) { snap = { err: String(e) }; }
    window.__probe193.push(Object.assign({ fn, ret: (typeof ret === 'boolean' || typeof ret === 'number' || ret === null) ? ret : String(ret).slice(0, 80), t: Date.now() }, snap, extra || {}));
  };
  const wrap = (name, extraFn) => {
    const orig = window[name];
    if (typeof orig !== 'function') { window.__probe193.push({ fn: 'WRAP-MISSING', name }); return; }
    window[name] = function(...args) {
      let ret, err = null;
      try { ret = orig.apply(this, args); } catch(e) { err = String(e); }
      let extra = {};
      try { if (extraFn) extra = extraFn(ret) || {}; } catch(e) { extra = { extraErr: String(e) }; }
      if (err) extra.threw = err;
      log(name, ret, extra);
      if (err) throw err;
      return ret;
    };
  };
  const predSnap = () => {
    const o = {};
    try { o.baseOk = (typeof wf4BaseOk === 'function') ? wf4BaseOk() : 'n/a'; } catch(e) { o.baseOk = 'ERR:' + e; }
    try { o.newsDay = (typeof wf4NewsDay === 'function' && S) ? wf4NewsDay(S.dayIndex|0) : 'n/a'; } catch(e) { o.newsDay = 'ERR:' + e; }
    try { o.forced = (typeof todayIsForcedDay === 'function') ? todayIsForcedDay() : 'n/a'; } catch(e) { o.forced = 'ERR:' + e; }
    try { o.sick = (typeof conseq61IsSickToday === 'function') ? conseq61IsSickToday() : 'n/a'; } catch(e) { o.sick = 'ERR:' + e; }
    try { o.ending = (typeof ending78Locked === 'function') ? ending78Locked() : 'n/a'; } catch(e) { o.ending = 'ERR:' + e; }
    try { o.fen = (typeof wf4PresentFenFarewell === 'function') ? 'fn-exists' : 'n/a'; } catch(e) {}
    return o;
  };
  wrap('goToMapForBrowse');
  wrap('runScheduleFromToday');
  wrap('resolvePlannedDay');
  wrap('wf4PresentPending', (ret) => ({ preds: predSnap() }));
  wrap('wf4BaseOk');
  wrap('wf4DailyTick');
  wrap('wf4TryLocEvent');
  wrap('wf4PresentFenFarewell');
  wrap('presentDueMorningPaper');
  wrap('aud91PresentDue');
  wrap('presentPendingAward');
  window.__probe193Preds = predSnap;
  return window.__probe193.length;
}
"""

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
            assert D.seed_seen(pg, {"wf4_ev_set03": 1}), "seed failed"
            # 同 drive Case C 一樣寫舊 save（day 用當刻 localStorage 嘅 dayIndex）
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
            # reload 後、撳讀檔之前 wrap（title 畫面，page script 已跑，函數喺 window）
            n = pg.evaluate(WRAP_JS)
            print("wrapped fns, probe entries:", n, flush=True)
            print("preds before load:", pg.evaluate("() => { try { return window.__probe193Preds(); } catch(e) { return String(e); } }"), flush=True)
            res = D.load_slot(pg, "1")
            print("load_slot settle ->", res, flush=True)
            print("state after load:", D.read_state(pg), "map:", D.map_visible(pg), flush=True)
            print("preds after load:", pg.evaluate("() => { try { return window.__probe193Preds(); } catch(e) { return String(e); } }"), flush=True)
            D.go_map(pg)
            print("after go_map state:", D.read_state(pg), "map:", D.map_visible(pg), flush=True)
            vr = D.visit_loc(pg, 'cafe_cha', "C", [])
            print("visit_loc cafe_cha ->", vr, flush=True)
            stC = D.read_state(pg)
            print("FINAL state:", stC, flush=True)
            print("preds final:", pg.evaluate("() => { try { return window.__probe193Preds(); } catch(e) { return String(e); } }"), flush=True)
            # 直接叫 wf4PresentPending 睇吓喺呢個 live state 下會點（對照）
            direct = pg.evaluate("""() => {
              try {
                const before = S.wf4.pending;
                const ret = wf4PresentPending();
                return { before, ret, after: S.wf4.pending, wf4title: (document.querySelector('#modal-inner h3')||{}).textContent || null };
              } catch(e) { return { err: String(e) }; } }""")
            print("DIRECT wf4PresentPending call:", direct, flush=True)
            pg.wait_for_timeout(800)
            D.settle(pg, timeout_ms=8000)
            print("state after direct+settle:", D.read_state(pg), flush=True)
            probe = pg.evaluate("() => window.__probe193 || []")
            print("=== PROBE LOG (%d entries) ===" % len(probe), flush=True)
            for e in probe:
                print(json.dumps(e, ensure_ascii=False), flush=True)
            print("pageerrors:", errs, flush=True)
            with open(os.path.join(D.HERE, "probe193c.json"), "w", encoding="utf-8") as f:
                json.dump({"final_state": stC, "direct": direct, "probe": probe, "errors": errs}, f, ensure_ascii=False, indent=2)
            br.close()
    finally:
        D.stop(srv)

if __name__ == "__main__":
    main()
