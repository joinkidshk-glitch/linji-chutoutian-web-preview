# -*- coding: utf-8 -*-
"""v199 WF4 診斷 v2：逐格 dump 過一日後嘅狀態，搵出 wf4PresentPending 冇觸發嘅原因。"""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/linji-work199/qa199")
import drive199 as d
d.URL = "http://127.0.0.1:8998/index.html"

STATE = """() => { const out = {};
  out.day = (typeof S!=='undefined') ? S.dayIndex : '?';
  out.storyOn = !!document.querySelector('.story-play');
  out.modalTxt = (document.getElementById('modal') ? (document.getElementById('modal').innerText||'').slice(0,120) : '');
  out.btns = [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim().slice(0,14)).slice(0,20);
  try { out.wf4 = S.wf4 ? {pending: S.wf4.pending||null, pendingDay: S.wf4.pendingDay, lastDay: S.wf4.lastDay, seen02: !!(S.wf4.seen && S.wf4.seen['wf4_ev_day02'])} : null; } catch(e){ out.wf4 = 'err'; }
  try { out.baseOk = (typeof wf4BaseOk==='function') ? wf4BaseOk() : 'n/a'; } catch(e){ out.baseOk = 'err:'+e; }
  try { out.forcedDay = (typeof todayIsForcedDay==='function') ? todayIsForcedDay() : 'n/a'; } catch(e){ out.forcedDay = 'err:'+e; }
  try { out.newsDay = (typeof wf4NewsDay==='function') ? wf4NewsDay(out.day) : 'n/a'; } catch(e){ out.newsDay = 'err:'+e; }
  try { out.sick = (typeof conseq61IsSickToday==='function') ? conseq61IsSickToday() : 'n/a'; } catch(e){ out.sick = 'err:'+e; }
  try { out.ending = (typeof ending78Locked==='function') ? ending78Locked() : 'n/a'; } catch(e){ out.ending = 'err:'+e; }
  return out; }"""

def dump(pg, label):
    print(f"--- {label}", flush=True)
    print("   " + json.dumps(pg.evaluate(STATE), ensure_ascii=False), flush=True)

def drain_story(pg, cap=120):
    n = 0
    for _ in range(cap):
        if not pg.evaluate("() => !!document.querySelector('.story-play')"):
            break
        d.story_next(pg)
        pg.wait_for_timeout(350)
        d.dismiss_encounter(pg)
        n += 1
    pg.wait_for_timeout(500)
    return n

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
            d.set_tier(pg, 1)
            total = 0
            for rnd in range(4):
                total += drain_story(pg)
                pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim().startsWith('進度')); if(b) b.click(); }""")
                pg.wait_for_timeout(1200)
                d.dismiss_encounter(pg)
                pg.evaluate("""() => { const b=document.getElementById('home-back-map-tabs'); if(b && b.offsetParent!==null){ b.click(); return; }
                  const t=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='返回地圖'); if(t) t.click(); }""")
                pg.wait_for_timeout(900)
                d.dismiss_encounter(pg)
                total += drain_story(pg)
                if not pg.evaluate("() => !!document.querySelector('.story-play')"):
                    break
            print(f"清場撳咗 {total} 下", flush=True)
            dump(pg, "清場後")
            print("seed:", pg.evaluate("""() => { S.wf4 = S.wf4 || {}; S.wf4.pending='wf4_ev_day02'; S.wf4.pendingDay=S.dayIndex; S.wf4.lastDay=-99;
              return {day:S.dayIndex, pending:S.wf4.pending}; }"""), flush=True)
            pg.evaluate("() => { const b=document.getElementById('map-end-day'); if(b) b.click(); }")
            pg.wait_for_timeout(1200)
            dump(pg, "撳過一日後")
            print("確定過一日:", d.modal_click(pg, "確定過一日"), flush=True)
            pg.wait_for_timeout(1500)
            dump(pg, "確定過一日後")
            d.dismiss_encounter(pg)
            print("關閉 modal:", d.modal_click(pg, "關閉"), flush=True)
            pg.wait_for_timeout(800)
            dump(pg, "關閉後")
            d.dismiss_encounter(pg)
            print("返回地圖 modal:", d.modal_click(pg, "返回地圖"), flush=True)
            pg.wait_for_timeout(1000)
            dump(pg, "返回地圖後")
            for i in range(6):
                pg.wait_for_timeout(1000)
                d.dismiss_encounter(pg)
                dump(pg, f"等候 {i+1}s")
                if pg.evaluate("() => !!document.querySelector('.story-play')"):
                    break
            print("直接 call wf4PresentPending:", pg.evaluate("() => { try { return wf4PresentPending(); } catch(e){ return 'err:'+e; } }"), flush=True)
            pg.wait_for_timeout(1500)
            dump(pg, "直接 call 之後")
            print("WF4 chars:", json.dumps(pg.evaluate("""() => [...document.querySelectorAll('.dlg106-char')].map(im=>({id:im.getAttribute('data-dlg-id'),
              src:(im.getAttribute('src')||'').split('/').pop().split('?')[0], onload:(im.getAttribute('onload')||'').slice(0,60)}))"""), ensure_ascii=False), flush=True)
            pg.screenshot(path="/home/hatch/workspace/linji-work199/qa199/shots_sup/diag2_wf4.png")
            br.close()
    finally:
        d.stop(srv)

if __name__ == "__main__":
    main()
