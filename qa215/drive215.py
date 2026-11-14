# -*- coding: utf-8 -*-
"""v20a215 實駕：推出日提及（本地鏡像，live 模式）。
重用 qa188/drive188.py 嘅 serve／new_game／modal_info／click helper；
播種直接寫 localStorage（key starVolunteer_map_v19w，slot 1；prefs 指去 1），
reload → 撳「繼續」→ contFromSlot → runScheduleFromToday → 晨鏈 → 朝早報紙。

場次（932）：
  a_release_spring：臨記廣告 春季，59 日朝早晨報有短訊（作品名＋播出資訊、冇玩家名、聲望唔郁）
  b_named_no：配角電影 夏季，151 日朝早冇呢則
  c_wrapped_on_day：臨記廣告 推出日當日先殺青（wrappedDay 59），59 日朝早冇呢則
  d_no_repeat：接 (a)，過一日（day 60）再睇，唔出第二則
  e_merge_award：臨記電影 夏季＋獎項報同一朝到期，併一份報（獎項頭條、推出短訊、聲望只 +2）
每場 0 pageerror。截圖放 qa215/shots215/。
注意：v214 分頁報紙——短訊喺第二版（display:none），modal innerText 只見第一版；
headline 檢查睇埋全版 textContent，短訊喺第二版嗰陣會撳過去核實可見＋截圖。
"""
import json
import os
import sys
import time

QA = "/home/hatch/workspace/linji-work215/qa215"
sys.path.insert(0, "/home/hatch/workspace/linji-work215/qa188")
import drive188 as d

d.ROOT = "/home/hatch/workspace/linji-work215"
d.QA = QA
d.SHOTS = os.path.join(QA, "shots215")
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 21590
os.makedirs(d.SHOTS, exist_ok=True)

from playwright.sync_api import sync_playwright

SEASON_WORD = {"春": "春季", "夏": "夏季", "秋": "秋季", "冬": "冬季"}

JS_SEED = """(o) => {
  const pick = (pred) => { try { return (typeof GIGS !== 'undefined' ? GIGS : []).find(pred) || null; } catch(e){ return null; } };
  const baseAd = pick(g => g.id === "gig_1988_entry_ad_passerby") || pick(g => g.roleScale === "ad_extra_day" && g.season === "春");
  const baseFilm = pick(g => g.id === "gig_1988_film_02") || pick(g => g.season === "夏" && g.type === "電影" && /群戲|武行|特約|臨記/.test(String(g.roleLabel||"")));
  const namedFilm = pick(g => g.id === "gig_1988_rec_02") || pick(g => g.season === "夏" && /男主角|女主角/.test(String(g.roleLabel||"")));
  const gigs = { baseAd, baseFilm, namedFilm };
  const chosen = gigs[o.gig] || null;
  if (!chosen) return { error: "gig not found: " + o.gig };
  const wrap = { gigId: chosen.id, title: chosen.title||chosen.id, type: chosen.type||"",
    workTitle: chosen.workTitle||"", roleLabel: chosen.roleLabel||"", year: chosen.year,
    totalDays: 2, pay: 950, fame: 1, popularity: 0, wrappedDay: o.wrapDay, rating: "順利殺青" };
  S.dayIndex = o.dayIndex;
  S.weekPlan = ["scout_all","scout_all","scout_all","scout_all","scout_all","scout_all","scout_all"];
  S.homeEditable = false;
  S.wrapHistory = [wrap];
  S.newspaperQueue = o.award ? [o.award] : [];
  S.newspaperClippings = [];
  S.pendingMorningPaper = null;
  S.newspaperLastPresentedDay = null;
  S.mockRumors = [];
  S.fame = 5; S.money = 5000; S.stress = 0; S.stage = 60; S.acting = 60;
  S.story = S.story || {}; S.story.done = { C1: 1 }; S.story.flags = {}; S.story.rel = {};
  S.story.gigCount = 1; /* C1 已完成：真玩家到推出日一早做完開局，唔好畀 C1 強制開場搶晨鏈 */
  S.awardsFlags = {};
  ["award_harbour_ad","award_golddisc_music","award_harbour_film","award_singho_tv"].forEach(id => {
    [1990,1991,1992].forEach(y => { S.awardsFlags[y + "/" + id] = "done"; });
  });
  S.pendingAwardPack = null;
  S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
  S.pendingAud = []; S.aud91Log = []; S.shoots = []; S.booked = [];
  if (S.flags) delete S.flags.pendingStoryNudge;
  try {
    localStorage.setItem("starVolunteer_map_v19w", JSON.stringify(S));
    const pk = "starVolunteer_prefs_v19z9";
    const p = JSON.parse(localStorage.getItem(pk) || "{}");
    p.activeSlot = 1; p.lastSlot = 1;
    localStorage.setItem(pk, JSON.stringify(p));
  } catch(e){ return { error: "save failed: " + String(e) }; }
  return { day: S.dayIndex,
    gig: { id: chosen.id, workTitle: chosen.workTitle, type: chosen.type, season: chosen.season,
           year: chosen.year, roleLabel: chosen.roleLabel, roleScale: chosen.roleScale },
    wrapDay: o.wrapDay };
}"""

JS_STATE = """() => {
  const S = window.S || {};
  const q = (S.newspaperQueue || []).map(it => ({ key: it.eventKey, src: it.source, pub: it.publishDay, enq: it.enqueuedDay }));
  const clips = (S.newspaperClippings || []).map(c => ({ keys: c.eventKeys || [], head: c.headline || "", fame: c.fameDelta }));
  return { day: S.dayIndex, fame: S.fame, queue: q, clips,
           pend: S.pendingMorningPaper ? { head: S.pendingMorningPaper.headline, keys: S.pendingMorningPaper.eventKeys } : null };
}"""

JS_MAP_VISIBLE = """() => {
  const m = document.querySelector('#v-map');
  if (!m) return false;
  const cs = getComputedStyle(m);
  return cs.display !== 'none' && m.getBoundingClientRect().width > 0;
}"""


def verb_of(t):
    if t == "電影":
        return "上映"
    if t in ("電視劇", "綜藝"):
        return "播出"
    return "推出"


def expected_headline(gig):
    return "《%s》%s%s" % (gig["workTitle"], SEASON_WORD[gig["season"]], verb_of(gig["type"]))


def continue_and_wait(pg, secs=5):
    """reload 後等 packs → 撳「繼續」→ 等晨鏈 modal／地圖，回傳 modal_info。"""
    pg.reload()
    pg.wait_for_timeout(2500)
    for _ in range(10):
        try:
            n = pg.evaluate("() => (typeof GIGS !== 'undefined' ? GIGS.length : 0)")
        except Exception:
            n = 0
        if n > 50:
            break
        pg.wait_for_timeout(500)
    clicked = d.click_text(pg, ["繼續"], 1200)
    last = d.modal_info(pg)
    for _ in range(6):
        if last.get("visible"):
            break
        pg.wait_for_timeout(700)
        last = d.modal_info(pg)
    return clicked, last


def collect_paper(pg):
    d.click_text(pg, ["收下這份剪報"], 1200)
    pg.wait_for_timeout(800)
    return pg.evaluate(JS_STATE)


def run_case(pw, cfg, results):
    name = cfg["name"]
    print(f"== {name} ==", flush=True)
    out = {"case": name, "checks": {}}
    errs = []
    b = pw.chromium.launch(executable_path=d.EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        if not d.new_game(pg):
            out["checks"]["new_game"] = False
            out["verdict"] = "ERROR"
            results[name] = out
            print("  ERROR new_game", flush=True)
            return
        out["checks"]["new_game"] = True
        sd = pg.evaluate(JS_SEED, {"gig": cfg["gig"], "dayIndex": cfg["day"], "wrapDay": cfg["wrapDay"],
                                   "award": cfg.get("award")})
        out["seed"] = sd
        if "error" in sd:
            out["verdict"] = "ERROR"
            results[name] = out
            print("  ERROR seed", sd, flush=True)
            return
        exp = expected_headline(sd["gig"])
        out["expected_headline"] = exp
        clicked, modal = continue_and_wait(pg)
        out["continue_clicked"] = clicked
        out["modal"] = modal
        body = modal.get("body") or ""
        if cfg.get("expect_paper"):
            out["checks"]["paper_modal_shown"] = bool(modal.get("visible"))
            # v214 分頁報紙：短訊（同版短訊）喺第二版（display:none），innerText 睇唔到；
            # headline 檢查要睇埋全版 textContent，仲要記低係邊一版。
            full = pg.evaluate("() => (document.querySelector('#modal')||{}).textContent || ''")
            out["checks"]["headline_present"] = exp in body or exp in full
            out["headline_page"] = 1 if exp in body else (2 if exp in full else 0)
            seg_src = body if exp in body else full
            seg = seg_src[seg_src.find(exp):seg_src.find(exp) + 300] if exp in seg_src else ""
            out["checks"]["no_player_name_near"] = ("阿偉" not in seg and "陳偉翔" not in seg)
            if cfg.get("expect_head") is not None:
                out["checks"]["head_is_award"] = (cfg["expect_head"] in body and exp in full
                                                   and full.find(cfg["expect_head"]) < full.find(exp))
            if cfg.get("expect_fame_line"):
                out["checks"]["fame_line"] = cfg["expect_fame_line"] in body
            d.shot(pg, name + "_paper.png")
            if out["headline_page"] == 2:
                d.click_text(pg, ["第二版"], 1200)
                modal2 = d.modal_info(pg)
                out["checks"]["headline_visible_p2"] = exp in (modal2.get("body") or "")
                d.shot(pg, name + "_paper_p2.png")
            st = collect_paper(pg)
            out["state_after"] = st
            out["checks"]["fame_unchanged_or_expected"] = (st["fame"] == cfg.get("fame_after", 5))
            out["checks"]["clipping_has_release"] = any(
                ("release:" + sd["gig"]["id"]) in (c.get("keys") or []) for c in st["clips"])
            out["checks"]["queue_empty"] = len(st["queue"]) == 0
            if cfg.get("expect_merge"):
                out["checks"]["one_clipping_only"] = len(st["clips"]) == 1
                out["checks"]["merged_keys_both"] = (
                    len(st["clips"]) == 1
                    and ("release:" + sd["gig"]["id"]) in (st["clips"][0].get("keys") or [])
                    and "award:1990:award_harbour_film" in (st["clips"][0].get("keys") or []))
        else:
            # 「冇呢則報紙」＝冇收下剪報掣嘅晨報 modal；C2 強制劇情等其他 modal 唔計
            #（晨鏈次序：報紙行先過強制播，見到劇情 modal 即係報紙嗰環已經行完且無嘢出）
            out["checks"]["no_paper_modal"] = "收下這份剪報" not in (modal.get("btns") or [])
            out["other_modal_h3"] = modal.get("h3")
            out["checks"]["map_visible"] = pg.evaluate(JS_MAP_VISIBLE)
            st = pg.evaluate(JS_STATE)
            out["state_after"] = st
            out["checks"]["queue_empty"] = len(st["queue"]) == 0
            out["checks"]["no_clippings"] = len(st["clips"]) == 0
            d.shot(pg, name + "_map.png")
        # (d) 延續 (a)：過一日再睇
        if cfg.get("follow_day"):
            pg.evaluate("""(day) => {
              S.dayIndex = day; S.newspaperLastPresentedDay = day - 1;
              try { localStorage.setItem("starVolunteer_map_v19w", JSON.stringify(S)); } catch(e){}
              return true; }""", cfg["follow_day"])
            clicked2, modal2 = continue_and_wait(pg)
            out["follow_modal"] = modal2
            out["checks"]["follow_no_paper"] = "收下這份剪報" not in (modal2.get("btns") or [])
            out["follow_modal_h3"] = modal2.get("h3")
            st2 = pg.evaluate(JS_STATE)
            out["follow_state"] = st2
            out["checks"]["follow_still_one_clipping"] = len(st2["clips"]) == 1
            out["checks"]["follow_queue_empty"] = len(st2["queue"]) == 0
            d.shot(pg, name + "_follow.png")
        out["pageerrors"] = errs
        out["checks"]["zero_pageerror"] = len(errs) == 0
        failed = [k for k, v in out["checks"].items() if v is not True]
        out["verdict"] = "PASS" if not failed else "FAIL"
        print(f"  verdict={out['verdict']} failed={failed} errs={errs}", flush=True)
        results[name] = out
    finally:
        b.close()


def main():
    srv = d.serve()
    results = {}
    try:
        with sync_playwright() as pw:
            run_case(pw, {"name": "a_release_spring", "gig": "baseAd", "day": 59, "wrapDay": 30,
                          "expect_paper": True, "expect_fame_line": "聲望未有變動", "fame_after": 5,
                          "follow_day": 60}, results)
            run_case(pw, {"name": "b_named_no", "gig": "namedFilm", "day": 151, "wrapDay": 100}, results)
            run_case(pw, {"name": "c_wrapped_on_day", "gig": "baseAd", "day": 59, "wrapDay": 59}, results)
            run_case(pw, {"name": "e_merge_award", "gig": "baseFilm", "day": 151, "wrapDay": 100,
                          "expect_paper": True, "expect_head": "頒獎見報", "expect_fame_line": "聲望 +2",
                          "fame_after": 7, "expect_merge": True,
                          "award": {"eventKey": "award:1990:award_harbour_film", "source": "award",
                                    "enqueuedDay": 150, "publishDay": 151, "fameDelta": 2,
                                    "paperName": "娛樂快報", "headline": "頒獎見報",
                                    "dek": "維港影藝獎之夜結果出爐。",
                                    "clipLabel": "娛樂快報・頒獎夜", "rumorEcho": "",
                                    "medium": "film", "workTitle": "維港影藝獎"}}, results)
    finally:
        d.stop(srv)
    with open(os.path.join(QA, "drive215.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    n_pass = sum(1 for r in results.values() if r.get("verdict") == "PASS")
    print(f"\n==== v215 實駕：{n_pass}/{len(results)} PASS ====")
    for k, r in results.items():
        print(f"  {k}: {r.get('verdict')}")


if __name__ == "__main__":
    main()
