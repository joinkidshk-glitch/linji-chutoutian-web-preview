# -*- coding: utf-8 -*-
"""B3 聚焦探針：逐 beat 同時量 skip／canvaswrap／frame／stage 四個 rect，
判斷跳過掣係咪釘死喺 canvaswrap 上（skip.y - wrap.y 恆定＝修好）。"""
import json, sys, time
sys.path.insert(0, "/home/hatch/workspace/linji-work197/qa197")
import drive197
from playwright.sync_api import sync_playwright

TRACK_JS = """() => {
  const q = s => document.querySelector(s);
  const r = el => { if(!el) return null; const b=el.getBoundingClientRect();
    return {x:Math.round(b.left), y:Math.round(b.top), w:Math.round(b.width), h:Math.round(b.height)}; };
  const skip = [...document.querySelectorAll('button')].find(b => b.offsetParent!==null && /跳過/.test(b.textContent||''));
  const st = q('.awd62-stage'), fr = q('.awd62-frame'), wrap = q('.awd62-canvaswrap');
  const cap = st ? st.querySelector('.awd62-caption') : null;
  return {stage: r(st), frame: r(fr), wrap: r(wrap), skip: skip ? r(skip) : null,
    skipParent: skip && skip.parentElement ? skip.parentElement.className : null,
    caption: cap ? (cap.textContent||'').slice(0,24) : ''};
}"""

srv = drive197.serve()
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=drive197.EXE)
        try:
            ctx = b.new_context(viewport={"width": 430, "height": 932})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(drive197.URL + "?softPreview=1")
            pg.wait_for_timeout(3000)
            if not drive197.new_game(pg):
                print("new_game FAILED"); sys.exit(1)
            st = pg.evaluate(drive197.STATE_JS)
            if st["story"] or st["choices"]:
                drive197.play_story(pg, max_steps=60, tag_prefix="dlg_b3")
            st = pg.evaluate(drive197.STATE_JS)
            if st["maskOn"]:
                drive197.click_first(pg, ["關閉"], 900); pg.wait_for_timeout(800)
            drive197.dismiss_enc3(pg)
            drive197.ensure_on_map(pg)
            drive197.dismiss_enc3(pg)
            pg.evaluate("""() => {
              try {
                S.dayIndex = 292; S.fame = 45; S.industryCreditDelta = 50; S.stage = 60; S.acting = 60;
                S.awardsFlags = {}; S.pendingAwardPack = null; S.newspaperQueue = []; S.news = S.news || [];
                S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
                const g = (typeof GIGS !== 'undefined' ? GIGS.filter(x=>x && x.type==='電影' && /男主角/.test(String(x.roleLabel||''))) : []);
                const pick = g.slice(0, 2);
                S.wrapHistory = pick.map(x => ({ gigId: x.id, title: x.title||x.id, type: '電影', workTitle: x.workTitle||'',
                  roleLabel: x.roleLabel||'', roleScale: x.roleScale||'', year: 1990, totalDays: 2,
                  pay: 20000, fame: 0, popularity: 0, wrappedDay: 250, rating: '順利殺青' }));
                S.story = S.story || {}; S.story.done = {}; S.story.flags = S.story.flags || {}; S.story.rel = S.story.rel || {};
              } catch(e){} }""")
            pg.evaluate("() => { try { window.__awards.debugForceSeasonWindow('award_harbour_film', {}); } catch(e){} }")
            pg.evaluate("() => { try { window.__awards.present(); } catch(e){} }")
            pg.wait_for_timeout(1200)
            drive197.click_text(pg, "出席", wait=1000)
            rows = []
            t0 = time.time()
            while time.time() - t0 < 26:
                m = pg.evaluate(TRACK_JS)
                m["t"] = round((time.time()-t0)*1000)
                rows.append(m)
                if not m.get("stage"):
                    break
                pg.wait_for_timeout(500)
            print(json.dumps({"rows": rows, "pageerrors": errs}, ensure_ascii=False))
        finally:
            ctx.close(); b.close()
finally:
    drive197.stop(srv)
