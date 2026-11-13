# -*- coding: utf-8 -*-
"""v199 補測 drive v2（統籌親自跑）：
修正：①「進度」掣實際文案係「進度2」（chip-story，帶計數）→ 用 startsWith 撳；
② 返地圖用 #home-back-map-tabs（id），唔用文案（地圖有兩粒同名掣）；
③ 先清場：開一次屋企返地圖觸發 v165 強制播（F4 上岸路），撳晒佢先做 C1／WF4，否則故事 overlay 會擋住之後所有掣。
用法：/home/hatch/pwenv49/bin/python qa199/drive199_sup.py
"""
import json, os, re, sys
sys.path.insert(0, "/home/hatch/workspace/linji-work199/qa199")
import drive199 as d
d.URL = "http://127.0.0.1:8998/index.html"

REPO = d.REPO
HERE = d.HERE
SHOTS = os.path.join(HERE, "shots_sup")
os.makedirs(SHOTS, exist_ok=True)
REPORT = {"errors": [], "http_fail": [], "checks": [], "runs": {}}

def check(name, cond, detail=""):
    REPORT["checks"].append({"name": name, "pass": bool(cond), "detail": detail})
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail else ""), flush=True)
    return bool(cond)

html = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()
CANDS = {}
for k in ("hero_awi", "awi_s2", "awi_s3"):
    m = re.search(r'"%s":\s*"(data:image/webp;base64,[A-Za-z0-9+/=]{180})' % k, html)
    CANDS[k] = m.group(1)[:200] if m else ""

MEASURE_HOME = """() => { const im=document.getElementById('home-awi');
  const v=document.getElementById('v-home');
  if(!im) return null;
  const r=im.getBoundingClientRect();
  return {srcHead:(im.getAttribute('src')||'').slice(0,200), complete: !!im.complete, natW: im.naturalWidth||0,
          homeVisible: !!(v && v.offsetParent!==null),
          rect: {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}}; }"""
STORY_ON = "() => !!document.querySelector('.story-play')"

def click_progress(pg):
    ok = pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim().startsWith('進度'));
      if(!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1200)
    d.dismiss_encounter(pg)
    return ok

def back_home(pg):
    pg.evaluate("""() => { const b=document.getElementById('home-back-map-tabs');
      if(b && b.offsetParent!==null){ b.click(); return; }
      const t=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='返回地圖');
      if(t) t.click(); }""")
    pg.wait_for_timeout(900)
    d.dismiss_encounter(pg)

def drain_story(pg, cap=80):
    """撳晒強制播故事（下一句／選項首選），直至 .story-play 消失。回撳咗幾多下。"""
    n = 0
    for _ in range(cap):
        if not pg.evaluate(STORY_ON):
            break
        d.story_next(pg)
        pg.wait_for_timeout(400)
        d.dismiss_encounter(pg)
        n += 1
    pg.wait_for_timeout(600)
    return n, pg.evaluate(STORY_ON)

def main():
    srv = d.serve(REPO, 8998)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            for vp in [{"width": 932, "height": 1500}, {"width": 700, "height": 1400}]:
                tag = str(vp["width"])
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=tag: REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=tag: REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                post = d.load_seeded_save(pg, {"day": 400, "fame": 30, "doneFlags": d.LEAD90_1, "playerTierMax": 2})
                check(f"{tag} 載入 day400 ptm2 stem=s2", post["stem"] == "awi_s2", post)
                # ---- 清場：觸發並撳晒 v165 強制播 ----
                click_progress(pg)
                back_home(pg)
                n, still = drain_story(pg)
                check(f"{tag} 清場：強制播故事撳晒（{n} 下）", not still, {"clicks": n, "storyStillOn": still})
                # ---- C1：三 tier 屋企 bust ----
                homes = {}
                for tier, key in [(1, "hero_awi"), (2, "awi_s2"), (3, "awi_s3")]:
                    st = d.set_tier(pg, tier)
                    ok = click_progress(pg)
                    home = pg.evaluate(MEASURE_HOME)
                    homes[tier] = {"stem": st, "progressClicked": ok, "measure": home}
                    if home and home.get("homeVisible"):
                        try:
                            el = pg.query_selector("#home-awi")
                            if el:
                                el.screenshot(path=os.path.join(SHOTS, f"sup_{tag}_t{tier}_bust.png"))
                        except Exception:
                            pass
                        try:
                            pg.screenshot(path=os.path.join(SHOTS, f"sup_{tag}_t{tier}_home.png"))
                        except Exception:
                            pass
                    back_home(pg)
                    n2, still2 = drain_story(pg, cap=10)
                    if still2:
                        print(f"  [warn t{tier}: story still on after back]", flush=True)
                REPORT["runs"][f"{tag}_home"] = homes
                rects = [homes[t]["measure"]["rect"] if homes[t]["measure"] else None for t in (1, 2, 3)]
                check(f"{tag} C1 屋企 bust 三 tier rect 一致 56x74",
                      all(r and r["w"] == 56 and r["h"] == 74 for r in rects), rects)
                check(f"{tag} C1 屋企 bust 全部 complete+natW 240",
                      all(homes[t]["measure"] and homes[t]["measure"]["complete"] and homes[t]["measure"]["natW"] == 240 for t in (1, 2, 3)),
                      {t: homes[t]["measure"] for t in (1, 2, 3)})
                check(f"{tag} C1 屋企 bust src 跟 tier",
                      all(homes[t]["measure"] and homes[t]["measure"]["srcHead"] == CANDS[k] for t, k in [(1, "hero_awi"), (2, "awi_s2"), (3, "awi_s3")]),
                      {t: (homes[t]["measure"] or {}).get("srcHead", "")[:40] for t in (1, 2, 3)})
                # ---- WF4：播種 pending＋過一日，讀 DOM onload ----
                seeded = pg.evaluate("""() => { try {
                    S.wf4 = S.wf4 || {};
                    S.wf4.pending = 'wf4_ev_day02';
                    S.wf4.pendingDay = S.dayIndex;
                    S.wf4.lastDay = -99;
                    return 'seeded day ' + S.dayIndex;
                  } catch(e){ return 'err:'+e; } }""")
                print(f"  wf4 seed: {seeded}", flush=True)
                pg.evaluate("() => { const b=document.getElementById('map-end-day'); if(b) b.click(); }")
                pg.wait_for_timeout(1200)
                d.dismiss_encounter(pg)
                d.modal_click(pg, "確定過一日")
                pg.wait_for_timeout(1500)
                d.dismiss_encounter(pg)
                d.modal_click(pg, "關閉")
                pg.wait_for_timeout(800)
                d.dismiss_encounter(pg)
                d.modal_click(pg, "返回地圖")
                pg.wait_for_timeout(1000)
                d.dismiss_encounter(pg)
                found = None
                for _ in range(20):
                    found = pg.evaluate("""() => {
                      const imgs=[...document.querySelectorAll('.story-play .dlg106-char, .dlg106-char')];
                      if(!imgs.length) return null;
                      return imgs.map(im=>({id: im.getAttribute('data-dlg-id'), src:(im.getAttribute('src')||'').split('/').pop().split('?')[0],
                        onload: im.getAttribute('onload')||'', hasFit: (im.getAttribute('onload')||'').includes('__dlg108Fit')})); }""")
                    if found:
                        break
                    pg.wait_for_timeout(500)
                    d.dismiss_encounter(pg)
                day_now = pg.evaluate("() => (typeof S!=='undefined') ? S.dayIndex : '?'")
                check(f"{tag} WF4 場景呈現＋img 有 onload __dlg108Fit",
                      bool(found) and all(x["hasFit"] for x in found),
                      {"day": day_now, "chars": found})
                try:
                    pg.screenshot(path=os.path.join(SHOTS, f"sup_{tag}_wf4.png"))
                except Exception:
                    pass
                pg.close()
            br.close()
    finally:
        d.stop(srv)
    with open(os.path.join(HERE, "drive199_sup_report.json"), "w", encoding="utf-8") as f:
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
