# -*- coding: utf-8 -*-
"""v199 WF4 專項實駕（統籌親自跑）：證明 wf4_ev_day02「傳呼台嘅一課」真場景渲染出嚟嘅
.dlg106-char img 帶 onload __dlg108Fit。
關鍵：① 先清場（撳晒 v165 強制播，否則故事 overlay 擋住過一日）；② day02 有 cond tierMax:1，
播種前將 playerTierMax 設為 1；③ 驗日數真係推進咗、pending 清咗、seen 入咗、場景標題係「傳呼台」。
用法：/home/hatch/pwenv49/bin/python qa199/drive199_wf4.py
"""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/linji-work199/qa199")
import drive199 as d
d.URL = "http://127.0.0.1:8998/index.html"

HERE = d.HERE
SHOTS = os.path.join(HERE, "shots_sup")
REPORT = {"errors": [], "http_fail": [], "checks": [], "runs": {}}

def check(name, cond, detail=""):
    REPORT["checks"].append({"name": name, "pass": bool(cond), "detail": detail})
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail else ""), flush=True)
    return bool(cond)

STORY_ON = "() => !!document.querySelector('.story-play')"
SCENE_INFO = """() => {
  const sp = document.querySelector('.story-play');
  const chars = [...document.querySelectorAll('.story-play .dlg106-char, .dlg106-char')].map(im=>({
    id: im.getAttribute('data-dlg-id'), src:(im.getAttribute('src')||'').split('/').pop().split('?')[0],
    onload: im.getAttribute('onload')||'', hasFit: (im.getAttribute('onload')||'').includes('__dlg108Fit')}));
  const txt = sp ? (sp.innerText||'').slice(0,200) : '';
  const wf4 = (typeof S!=='undefined' && S.wf4) ? {pending: S.wf4.pending||null, seen02: !!(S.wf4.seen && S.wf4.seen['wf4_ev_day02'])} : null;
  const day = (typeof S!=='undefined') ? S.dayIndex : '?';
  return {storyOn: !!sp, txt, chars, wf4, day}; }"""

def click_progress(pg):
    pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim().startsWith('進度'));
      if(b) b.click(); }""")
    pg.wait_for_timeout(1200)
    d.dismiss_encounter(pg)

def back_home(pg):
    pg.evaluate("""() => { const b=document.getElementById('home-back-map-tabs');
      if(b && b.offsetParent!==null){ b.click(); return; }
      const t=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='返回地圖');
      if(t) t.click(); }""")
    pg.wait_for_timeout(900)
    d.dismiss_encounter(pg)

def drain_story(pg, cap=120):
    n = 0
    for _ in range(cap):
        if not pg.evaluate(STORY_ON):
            break
        d.story_next(pg)
        pg.wait_for_timeout(350)
        d.dismiss_encounter(pg)
        n += 1
    pg.wait_for_timeout(500)
    return n, pg.evaluate(STORY_ON)

def main():
    srv = d.serve(d.REPO, 8998)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 932, "height": 1500})
            pg.on("pageerror", lambda e: REPORT["errors"].append(str(e)))
            pg.on("response", lambda r: REPORT["http_fail"].append(f"{r.status} {r.url}") if r.status >= 400 else None)
            post = d.load_seeded_save(pg, {"day": 400, "fame": 30, "doneFlags": d.LEAD90_1, "playerTierMax": 2})
            check("載入 day400 ptm2 stem=s2", post["stem"] == "awi_s2", post)
            # tier 設 1，滿足 day02 cond tierMax:1
            st = d.set_tier(pg, 1)
            check("設 tier=1（day02 cond）stem=awi", st == "awi", st)
            # ---- 清場：來回地圖觸發＋撳晒所有強制播 ----
            total = 0
            for rnd in range(4):
                n, still = drain_story(pg)
                total += n
                if still:
                    print(f"  [清場 round{rnd}: 撳咗 {n} 下仲有故事，繼續]", flush=True)
                click_progress(pg)
                back_home(pg)
                n2, still2 = drain_story(pg)
                total += n2
                if not still2 and not pg.evaluate(STORY_ON):
                    break
            info0 = pg.evaluate(SCENE_INFO)
            check("清場後無故事 overlay", not info0["storyOn"], {"clicks": total, "day": info0["day"]})
            d0 = info0["day"]
            # ---- 播種 WF4 ----
            seed = pg.evaluate("""() => { S.wf4 = S.wf4 || {};
              S.wf4.pending = 'wf4_ev_day02'; S.wf4.pendingDay = S.dayIndex; S.wf4.lastDay = -99;
              return {day: S.dayIndex, pending: S.wf4.pending}; }""")
            print("  wf4 seed:", seed, flush=True)
            pg.evaluate("() => { const b=document.getElementById('map-end-day'); if(b) b.click(); }")
            pg.wait_for_timeout(1200)
            d.dismiss_encounter(pg)
            conf = d.modal_click(pg, "確定過一日")
            print("  確定過一日 modal:", conf, flush=True)
            pg.wait_for_timeout(1500)
            d.dismiss_encounter(pg)
            day_after = pg.evaluate("() => (typeof S!=='undefined') ? S.dayIndex : '?'")
            check("過一日後日數推進 1 日", day_after == d0 + 1, {"dayBefore": d0, "dayNow": day_after})
            # ---- 晨鏈排水：請柬「推辭」→ 報紙「關閉」→ aud91 → WF4；期間如有其他故事，先撳晒佢 ----
            found = None
            for i in range(40):
                info = pg.evaluate(SCENE_INFO)
                # WF4 場景識別：用 beat 原文（標題「傳呼台嘅一課」唔會渲染出嚟）
                if info["storyOn"] and ("Call機響起一串密碼數字" in info["txt"] or "520、3344" in info["txt"]):
                    found = info
                    break
                if info["storyOn"]:
                    n, _ = drain_story(pg, cap=40)
                    print(f"  [poll {i}: 非 WF4 故事，撳咗 {n} 下；txt={info['txt'][:40]!r}]", flush=True)
                    continue
                if d.modal_click(pg, "推辭"):
                    print(f"  [poll {i}: 推辭請柬]", flush=True)
                    pg.wait_for_timeout(900)
                    continue
                if d.modal_click(pg, "關閉"):
                    print(f"  [poll {i}: 關閉報紙／modal]", flush=True)
                    pg.wait_for_timeout(900)
                    continue
                if d.modal_click(pg, "返回地圖"):
                    print(f"  [poll {i}: 返回地圖]", flush=True)
                    pg.wait_for_timeout(900)
                    continue
                pg.wait_for_timeout(500)
                d.dismiss_encounter(pg)
            REPORT["runs"]["wf4"] = found
            check("WF4 場景「傳呼台嘅一課」呈現（beat 原文 Call機／520）", bool(found) and ("Call機響起一串密碼數字" in found["txt"] or "520、3344" in found["txt"]), (found or {}).get("txt", "")[:120])
            check("WF4 pending 已清＋seen 已入", bool(found) and found["wf4"] and found["wf4"]["pending"] is None and found["wf4"]["seen02"],
                  (found or {}).get("wf4"))
            check("WF4 img 全部有 onload __dlg108Fit",
                  bool(found) and bool(found["chars"]) and all(c["hasFit"] for c in found["chars"]),
                  (found or {}).get("chars"))
            # ---- WF4 獨角 fit 實量：撳「繼續」入 beat，量 .dlg106-char 實際渲染高＋fit 有冇落手 ----
            cont = pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='繼續');
              if(b){ b.click(); return true; } return false; }""")
            pg.wait_for_timeout(1200)
            d.dismiss_encounter(pg)
            fit = pg.evaluate("""() => { const im=document.querySelector('.story-play .dlg106-char');
              if(!im) return null;
              const r=im.getBoundingClientRect(); const cs=getComputedStyle(im);
              const ar=(im.naturalWidth||0)/(im.naturalHeight||1);
              const paintedH=Math.min(r.height, r.width/ar);
              const st=document.querySelector('.story-play .sp-stage')||document.querySelector('.story-play');
              const sr=st?st.getBoundingClientRect():null;
              return {id: im.getAttribute('data-dlg-id'), src:(im.getAttribute('src')||'').split('/').pop().split('?')[0],
                w: Math.round(r.width*10)/10, h: Math.round(r.height*10)/10, natW: im.naturalWidth, natH: im.naturalHeight,
                ar: Math.round(ar*10000)/10000, paintedH: Math.round(paintedH*10)/10, inlineH: im.style.height||'',
                cssMaxW: cs.maxWidth, stageH: sr?Math.round(sr.height):null, docScrollW: document.documentElement.scrollWidth, winW: window.innerWidth}; }""")
            check("WF4 獨角撳繼續後 fit 有落手（inline height 已設）＋唔溢出",
                  bool(fit) and bool(fit["inlineH"]) and fit["docScrollW"] <= fit["winW"],
                  {"continued": cont, "fit": fit})
            try:
                pg.screenshot(path=os.path.join(SHOTS, "wf4_day02_beat.png"))
            except Exception:
                pass
            try:
                pg.screenshot(path=os.path.join(SHOTS, "wf4_day02_scene.png"))
            except Exception:
                pass
            br.close()
    finally:
        d.stop(srv)
    with open(os.path.join(HERE, "drive199_wf4_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)
    n = sum(1 for c in REPORT["checks"] if c["pass"])
    print(f"CHECKS {n}/{len(REPORT['checks'])} PASS")
    for c in REPORT["checks"]:
        if not c["pass"]:
            print("  FAIL:", c["name"], c["detail"])
    print("pageerrors:", len(REPORT["errors"]), REPORT["errors"][:5])
    print("http_fail:", len(REPORT["http_fail"]), REPORT["http_fail"][:5])

if __name__ == "__main__":
    main()
