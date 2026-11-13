# -*- coding: utf-8 -*-
"""v199 診斷：地圖掣文案＋返地圖有兩粒＋WF4 觸發步驟逐格 dump。"""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/linji-work199/qa199")
import drive199 as d
d.URL = "http://127.0.0.1:8998/index.html"

DUMP_BTNS = """() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null)
  .map(b=>({t:(b.textContent||'').trim().slice(0,20), id:b.id||'', cls:(b.className||'').toString().slice(0,40)}))"""
STATE = """() => { const s = (typeof S!=='undefined') ? {day: S.dayIndex, view: (document.querySelector('.view.active')||{}).id || '?',
  homeVis: !!(document.getElementById('v-home') && document.getElementById('v-home').offsetParent!==null),
  mapVis: !!(document.getElementById('v-map') && document.getElementById('v-map').offsetParent!==null),
  modal: (document.getElementById('modal')||{}).innerText ? (document.getElementById('modal').innerText||'').slice(0,80) : '',
  story: !!document.querySelector('.story-play'),
  wf4: S.wf4 ? {pending: S.wf4.pending||null, pendingDay: S.wf4.pendingDay, lastDay: S.wf4.lastDay} : null} : null;
  return s; }"""

def main():
    srv = d.serve(d.REPO, 8998)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 932, "height": 1500})
            pg.on("pageerror", lambda e: print("PAGEERROR:", e, flush=True))
            post = d.load_seeded_save(pg, {"day": 400, "fame": 30, "doneFlags": d.LEAD90_1, "playerTierMax": 2})
            print("load:", post, flush=True)
            print("STATE map:", json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            print("BTNS map:", json.dumps(pg.evaluate(DUMP_BTNS), ensure_ascii=False), flush=True)
            # 撳進度*（偏名匹配）
            ok = pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim().startsWith('進度'));
              if(!b) return false; b.click(); return true; }""")
            pg.wait_for_timeout(1200)
            print("progress click:", ok, flush=True)
            print("STATE home:", json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            print("HOME-AWI:", json.dumps(pg.evaluate("""() => { const im=document.getElementById('home-awi');
              if(!im) return null; const r=im.getBoundingClientRect();
              return {srcHead:(im.getAttribute('src')||'').slice(0,60), complete:!!im.complete, natW:im.naturalWidth,
                rect:{w:Math.round(r.width),h:Math.round(r.height)}}; }"""), ensure_ascii=False), flush=True)
            print("BTNS home:", json.dumps(pg.evaluate(DUMP_BTNS), ensure_ascii=False), flush=True)
            # 返地圖：用 id #home-back-map（如果有）
            back = pg.evaluate("""() => { const b=document.getElementById('home-back-map');
              if(b && b.offsetParent!==null){ b.click(); return 'by-id'; }
              const t=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='返回地圖');
              if(t){ t.click(); return 'by-text'; } return 'none'; }""")
            pg.wait_for_timeout(900)
            print("back:", back, json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            # WF4：播種＋過一日，逐格 dump
            print("seed:", pg.evaluate("""() => { S.wf4=S.wf4||{}; S.wf4.pending='wf4_ev_day02'; S.wf4.pendingDay=S.dayIndex; S.wf4.lastDay=-99;
              return {day:S.dayIndex, wf4:S.wf4}; }"""), flush=True)
            print("click 過一日:", d.js_click_text(pg, "過一日"), flush=True)
            pg.wait_for_timeout(1200)
            print("STATE after 過一日:", json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            print("BTNS:", json.dumps(pg.evaluate(DUMP_BTNS), ensure_ascii=False), flush=True)
            print("modal 確定過一日:", d.modal_click(pg, "確定過一日"), flush=True)
            pg.wait_for_timeout(1500)
            print("STATE after 確定:", json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            print("BTNS:", json.dumps(pg.evaluate(DUMP_BTNS), ensure_ascii=False), flush=True)
            d.dismiss_encounter(pg)
            d.modal_click(pg, "關閉")
            pg.wait_for_timeout(800)
            print("STATE after 關閉:", json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            d.modal_click(pg, "返回地圖")
            pg.wait_for_timeout(1000)
            print("STATE after 返回地圖:", json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            for i in range(10):
                st = pg.evaluate(STATE)
                if st["story"]:
                    break
                pg.wait_for_timeout(500)
                d.dismiss_encounter(pg)
            print("STATE final:", json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)
            print("WF4 chars:", json.dumps(pg.evaluate("""() => [...document.querySelectorAll('.dlg106-char')].map(im=>({id:im.getAttribute('data-dlg-id'),
              src:(im.getAttribute('src')||'').split('/').pop().split('?')[0], onload:(im.getAttribute('onload')||'').slice(0,80)}))"""), ensure_ascii=False), flush=True)
            pg.screenshot(path="/home/hatch/workspace/linji-work199/qa199/shots_sup/diag_wf4.png")
            br.close()
    finally:
        d.stop(srv)

if __name__ == "__main__":
    main()
