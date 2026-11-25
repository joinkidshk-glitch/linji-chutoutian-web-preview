# -*- coding: utf-8 -*-
"""probe: confirm week1 -> watch what blocks day advance. Logs to qa400/verify/probe400.log."""
import sys, time, json, subprocess
sys.path.insert(0, '/home/hatch/workspace/fullarc')
from playwright.sync_api import sync_playwright
import driver as drv
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
ROOT = "/home/hatch/workspace/linji-work400"
LOG = open(f"{ROOT}/qa400/verify/probe400.log", "w", encoding="utf-8")
def lg(*a):
    print(*a, flush=True); print(*a, file=LOG, flush=True)
srv = subprocess.Popen(["python3","-m","http.server","19395","--bind","127.0.0.1"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
URL = "http://127.0.0.1:19395/index.html"
def ev(pg, js):
    try: return pg.evaluate(js)
    except Exception as e: return "EVFAIL:"+str(e)[:200]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox','--proxy-server=http://127.0.0.1:18081','--ignore-certificate-errors'])
    pg = b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2).new_page()
    pg.set_default_timeout(10000)
    pg.goto(URL); pg.wait_for_timeout(2500)
    for _ in range(12):
        pg.click('#btn-new'); pg.wait_for_timeout(1200)
        st = json.loads(ev(pg, "() => JSON.stringify({s: !!(typeof S!=='undefined'&&S), mask: document.getElementById('mask').classList.contains('on'), view:(document.querySelector('.view.on')||{}).id||''})"))
        if st.get('s') or st.get('mask') or st.get('view') != 'v-start': break
    drv.skip_tutorial(pg)
    drv.click_text_in_modal(pg, r'開始寫手帳')
    pg.wait_for_timeout(1200)
    ev(pg, "() => { const b=document.getElementById('btn-confirm-plan'); if(b) b.click(); return true; }")
    pg.wait_for_timeout(1500)
    for i in range(60):
        pg.wait_for_timeout(1000)
        st = ev(pg, """() => JSON.stringify({day:S.dayIndex, ed:S.homeEditable,
          view:(document.querySelector('.view.on')||{}).id||'',
          mask:document.getElementById('mask').classList.contains('on'),
          maskHtml: (document.getElementById('mask')||{innerText:''}).innerText.slice(0,120),
          modalBtns:[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim()),
          modalHead:((document.querySelector('#modal-inner h3')||{}).textContent||'').slice(0,50),
          modalText:((document.querySelector('#modal-inner')||{innerText:''}).innerText||'').slice(0,200),
          storyBtns:[...document.querySelectorAll('#story-btns button, #story-box button, #story button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim()),
          sheet: (document.getElementById('loc-sheet')||{classList:{contains:()=>false}}).classList.contains('on')})""")
        lg(i, st)
        if '"mask":false' in st:
            lg("MASK CLOSED"); break
        hit = ev(pg, """() => {
          const all=[...document.querySelectorAll('#modal-btns button, #story-btns button, #story-box button, #story button, #mask button')].filter(x=>x.offsetParent!==null&&!x.disabled);
          const t=all.find(x=>/下一句|跳至選項|繼續|確定|開始|收到|我知道了/.test(x.textContent||''))||all[0];
          if(!t) return null; t.click(); return (t.textContent||'').trim(); }""")
        lg("  clicked:", hit)
    pg.screenshot(path=f"{ROOT}/qa400/shots/probe_stuck2.png")
    b.close()
srv.terminate()
lg("DONE")
