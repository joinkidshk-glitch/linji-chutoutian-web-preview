"""Focused debug: replicate gift-shop -> back_to_map -> N16 seed -> cafe pin, print state at each step."""
import sys, os, json
sys.path.insert(0, "/home/hatch/workspace/linji-ui-style-unify")
sys.path.insert(0, "qa128")
import verify_a3a6 as V
from drive_lib import EXE
from playwright.sync_api import sync_playwright

def state(pg):
    return pg.evaluate("""() => { const v=document.querySelector('.view.on');
      const sheet=document.getElementById('loc-sheet');
      const modal=document.getElementById('modal');
      const ov=document.querySelector('#enc79-overlay');
      return {view: v?v.id:'none', sheetOn: sheet && (sheet.classList.contains('on')||sheet.classList.contains('sheet-live')),
        modalOn: modal && modal.classList.contains('on'),
        modalDisplay: modal ? getComputedStyle(modal).display : null,
        ov: !!ov, starDay: window.S ? window.S.starDay : null,
        liu: window.S && window.S.stars ? window.S.stars.liu_bingxing : null,
        tips: window.S ? window.S.mapTips : null,
        storyOC: typeof StoryOC !== 'undefined',
        quota: window.S ? window.S.travel114 : null}; }""")

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width":390,"height":844})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(V.URL); pg.wait_for_timeout(3200)
    pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='新遊戲'); if(b) b.click(); }""")
    pg.wait_for_timeout(1200)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]'); if (b && b.offsetParent !== null) b.click(); }""")
    pg.wait_for_timeout(1200)
    for t in ["覆蓋", "確定", "確認"]:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); break
        except Exception: pass
    for t in ["跳過教學", "開始寫手帳"]:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(1200)
        except Exception: pass
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
    except Exception: pass
    V.click_first(pg, ["確定出發"], 1500)
    for _ in range(5):
        hit = False
        for t in ["確定", "確認", "好", "知道了"]:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); hit = True; break
            except Exception: pass
        if not hit: break
    pg.wait_for_timeout(1200)
    V.play_through_dialogue(pg, 40)  # C1
    V.back_to_map(pg)
    print("after C1:", json.dumps(state(pg), ensure_ascii=False), flush=True)
    # gift shop
    V.ensure_quota(pg)
    V.pin_click(pg, "gift_shop"); pg.wait_for_timeout(1500)
    print("after gift pin:", json.dumps(state(pg), ensure_ascii=False), flush=True)
    V.click_first(pg, ["買禮物"], 1200)
    print("after 買禮物:", json.dumps(state(pg), ensure_ascii=False), flush=True)
    print("back_to_map ->", V.back_to_map(pg), flush=True)
    print("after back_to_map:", json.dumps(state(pg), ensure_ascii=False), flush=True)
    # N16
    V.ensure_quota(pg)
    print(V.seed_encounter(pg, "liu_bingxing", "cafe_cha"), flush=True)
    print("after seed:", json.dumps(state(pg), ensure_ascii=False), flush=True)
    print("story:", pg.evaluate("""() => { const oc = StoryOC.listOpen({checkNodePhase:true, player:true, ignoreSheetLoc:true}) || {};
      const ids = (oc.open||[]).map(r=>r.id);
      const locs = {}; for(const id of ids){ try{ locs[id] = (typeof storyNodeLocId==='function') ? storyNodeLocId(StoryOC.findNodeRaw(id)) : '?'; }catch(e){ locs[id]='err'; } }
      return {c1done: StoryOC.isDone ? StoryOC.isDone('C1') : null, open: ids, locs}; }"""), flush=True)
    V.pin_click(pg, "cafe_cha"); pg.wait_for_timeout(1500)
    print("after cafe pin:", json.dumps(state(pg), ensure_ascii=False), flush=True)
    pg.screenshot(path="qa128/shots/dbg_n16.png")
    print("PAGEERRORS:", errs, flush=True)
    br.close()
