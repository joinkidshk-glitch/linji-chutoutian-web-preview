import sys, os
sys.path.insert(0, "/home/hatch/workspace/linji-ui-style-unify")
sys.path.insert(0, "qa128")
import verify_a3a6 as V
from drive_lib import EXE
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width":390,"height":844})
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
    # C1 plays then lands on home; click through to home view
    V.play_through_dialogue(pg, 40)
    pg.wait_for_timeout(1000)
    print("view:", pg.evaluate("() => { const v=document.querySelector('.view.on'); return v?v.id:'none'; }"))
    # enter home via the 進度 chip, then measure the top area
    pg.evaluate("() => { const c=document.getElementById('chip-story'); if(c) c.click(); }")
    pg.wait_for_timeout(1200)
    print("view after chip:", pg.evaluate("() => { const v=document.querySelector('.view.on'); return v?v.id:'none'; }"))
    # go to home via chip if on map
    st = pg.evaluate("""() => { const ex=document.getElementById('home-tab-exit');
      const tabs=document.querySelector('.home-tabs');
      const r1=ex?ex.getBoundingClientRect():null, r2=tabs?tabs.getBoundingClientRect():null;
      const btn=document.getElementById('home-back-map-tabs');
      const rb=btn?btn.getBoundingClientRect():null;
      const reset=document.getElementById('btn-reset-plan');
      const rr=reset?reset.getBoundingClientRect():null;
      return {exitY: r1?Math.round(r1.y):null, tabsY: r2?Math.round(r2.y):null,
        backBtn: rb?{x:Math.round(rb.x),y:Math.round(rb.y),w:Math.round(rb.width),h:Math.round(rb.height),txt:btn.textContent.trim()}:null,
        reset: rr?{y:Math.round(rr.y),h:Math.round(rr.height),vis:getComputedStyle(reset).display}:null}; }""")
    print(st)
    pg.screenshot(path="qa128/shots/v128_home_top2.png")
    br.close()
