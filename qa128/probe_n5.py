# -*- coding: utf-8 -*-
"""v128 A3 N5 probe: list every element intersecting the top 24px of the
viewport during C1 step 0, to identify the two clipped gold pills."""
import sys, os
sys.path.insert(0, "/home/hatch/workspace/linji-ui-style-unify")
from drive_lib import EXE
from playwright.sync_api import sync_playwright

PORT = 8952
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def click_first(pg, texts, wait=900):
    for t in texts:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

def pin_click(pg, loc_id):
    box = pg.evaluate("""(id) => { const b=document.querySelector('.pin[data-loc="'+id+'"]');
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x+r.width/2, y:r.y+r.height/2}; }""", loc_id)
    if not box:
        return False
    pg.mouse.click(box["x"], box["y"])
    pg.wait_for_timeout(1600)
    return True

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                         user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(3200)
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
    click_first(pg, ["確定出發"], 1500)
    for _ in range(5):
        hit = False
        for t in ["確定", "確認", "好", "知道了"]:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); hit = True; break
            except Exception: pass
        if not hit: break
    pg.wait_for_timeout(1200)
    pin_click(pg, "agency_ho")
    print("播劇情:", click_first(pg, ["播劇情"], 1800), flush=True)
    pg.wait_for_timeout(1000)
    res = pg.evaluate("""() => {
      const out = [];
      document.querySelectorAll('body *').forEach(el=>{
        const b = el.getBoundingClientRect();
        if(b.width===0 || b.height===0) return;
        if(b.top < 24 && b.bottom > 0 && b.right > 250){
          const cs = getComputedStyle(el);
          out.push({tag: el.tagName, id: el.id||'', cls: String(el.className).slice(0,50),
            txt: (el.textContent||'').trim().slice(0,24),
            x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            z: cs.zIndex, pos: cs.position, vis: cs.visibility, op: cs.opacity,
            parent: el.parentElement ? (el.parentElement.tagName+'.'+String(el.parentElement.className).slice(0,30)) : ''});
        }
      });
      return out;
    }""")
    for r in res:
        print(r)
    print("PAGEERRORS:", errs)
    br.close()
