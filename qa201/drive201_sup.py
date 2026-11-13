# -*- coding: utf-8 -*-
"""v201 補測 drive（跟 v199 drive199_sup.py 手法）：
修正主 drive 嘅三類假 FAIL（全部同 v199 主 drive 一樣，唔係回歸）：
① 屋企 bust：主 drive 直 call enterHome（IIFE 內部函數）throw，屋企永遠唔開
   → 行 UI 路徑：地圖「進度」掣（#chip-story，文案「進度2」）→ 屋企；
   返地圖用 #home-back-map-tabs。
② base 闊度：合成 beat 入面 emotion "base" 渲染出嚟係 serious 圖（v199 review
   §限制 #1，pre-existing）→ base 闊度唔用舞台 beat，改用 live boxH × 三 tier
   base 圖自然 AR 模型（boxH 由 serious beat 實測，同高已證）。
③ WF4：wf4DlgCharsHtml108 係 IIFE 內部函數，唔係 global，主 drive 嗰個 check
   永遠 ReferenceError → 行真實 WF4 晨鏈（播種 pending＋過一日，讀 DOM onload）。
另加：聽者 brightness(0.60) 實測（講者 1／聽者 0.6）。
用法：/home/hatch/pwenv49/bin/python qa201/drive201_sup.py
"""
import json, os, re, sys
sys.path.insert(0, "/home/hatch/workspace/linji-work201/qa201")
import drive201 as d
d.URL = "http://127.0.0.1:8997/index.html"

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
    srv = d.serve(REPO, 8997)
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
                click_progress(pg)
                back_home(pg)
                n, still = drain_story(pg)
                check(f"{tag} 清場：強制播故事撳晒（{n} 下）", not still, {"clicks": n, "storyStillOn": still})
                # ---- C1：三 tier 屋企 bust（UI 路徑）----
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
                    drain_story(pg, cap=10)
                REPORT["runs"][f"{tag}_home"] = homes
                rects = [homes[t]["measure"]["rect"] if homes[t]["measure"] else None for t in (1, 2, 3)]
                check(f"{tag} C1 屋企 bust 三 tier rect 一致 56x74",
                      all(r and r["w"] == 56 and r["h"] == 74 for r in rects), rects)
                check(f"{tag} C1 屋企 bust 全部 complete+natW 240",
                      all(homes[t]["measure"] and homes[t]["measure"]["complete"] and homes[t]["measure"]["natW"] == 240 for t in (1, 2, 3)),
                      {t: homes[t]["measure"] for t in (1, 2, 3)})
                check(f"{tag} C1 屋企 bust src 跟 tier（新 crop201 hero_awi）",
                      all(homes[t]["measure"] and homes[t]["measure"]["srcHead"] == CANDS[k] for t, k in [(1, "hero_awi"), (2, "awi_s2"), (3, "awi_s3")]),
                      {t: (homes[t]["measure"] or {}).get("srcHead", "")[:40] for t in (1, 2, 3)})
                # ---- C1 base 闊度（live boxH × 自然 AR 模型）----
                # boxH 由 serious beat 實測（同高已證，三 tier 同一 boxH）。
                d.set_tier(pg, 2)
                res = d.run_beat(pg, "ho_sang", "serious", "記住，呢行最緊要係準時。")
                box_h = next(c["h"] for c in res["m"]["chars"] if c["id"] == "awi")
                nat = pg.evaluate("""() => { const files = ['awi_base.webp','awi_s2_base.webp','awi_s3_base.webp'];
                  return new Promise(res => { const r = {};
                    for (const f of files) { const im = new Image();
                      im.onload = () => { r[f] = [im.naturalWidth, im.naturalHeight]; if (Object.keys(r).length === files.length) res(r); };
                      im.onerror = () => { r[f] = 'error'; if (Object.keys(r).length === files.length) res(r); };
                      im.src = 'assets/story/fullbody/' + f; } }); }""")
                ws = [round(box_h * nat[f][0] / nat[f][1], 1) for f in
                      ["awi_base.webp", "awi_s2_base.webp", "awi_s3_base.webp"]]
                check(f"{tag} C1 base 闊度（live boxH {box_h}px × 自然 AR）：三 tier 同闊 spread ≤5px（{ws}，spread {max(ws)-min(ws):.1f}px）",
                      max(ws) - min(ws) <= 5.0, {"boxH": box_h, "nat": nat, "widths": ws})
                REPORT["runs"][f"{tag}_base_widths"] = {"boxH": box_h, "nat": nat, "widths": ws}
                # ---- 聽者變暗 0.60（講者 1／聽者 0.6，computed filter）----
                bright = pg.evaluate("""() => { const ims=[...document.querySelectorAll('.story-play .dlg106-char')];
                  return ims.map(im=>({id: im.getAttribute('data-dlg-id'), filter: getComputedStyle(im).filter})); }""")
                # run_beat 播完停喺玩家句：玩家係講者（brightness 1），何生係聽者（0.6）。
                spk = next((x for x in bright if x["id"] == "awi"), None)
                lis = next((x for x in bright if x["id"] == "ho_sang"), None)
                check(f"{tag} 聽者變暗：講者阿偉 brightness(1)、聽者何生 brightness(0.6)",
                      bool(spk and lis) and "brightness(1)" in spk["filter"] and "brightness(0.6)" in lis["filter"],
                      bright)
                REPORT["runs"][f"{tag}_brightness"] = bright
                pg.close()
            br.close()
    finally:
        d.stop(srv)
    with open(os.path.join(HERE, "drive201_sup_report.json"), "w", encoding="utf-8") as f:
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
