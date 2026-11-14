# probe193：開局後畫面狀態探測（唔做斷言，只印 DOM／S 狀態）
import os, subprocess, time, signal, hashlib, urllib.request, sys
ROOT = "/home/hatch/workspace/linji-work193"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8994
URL = f"http://127.0.0.1:{PORT}/index.html"
from playwright.sync_api import sync_playwright

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    return p

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

JS_STATE = "() => (typeof S==='undefined') ? 'no S' : ({day:S.dayIndex, plan:S.weekPlan})"
JS_VIEWS = "() => ['#v-map','#v-home'].map(s=>{const e=document.querySelector(s); return s+':'+(e?(e.offsetParent!==null):'null')}).join(' ')"
JS_BTNS = "() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim()).slice(0,25)"
JS_STORY = """() => {
  const plate = document.querySelector('.story-play .dlg106-plate');
  const choice = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
  return {plate: !!plate, choices: choice.length}; }"""
JS_STORY_NEXT = """() => { const row = document.getElementById('modal-btns');
  if (!row) return false; const bs=[...row.querySelectorAll('button')].filter(x=>x.offsetParent!==null && !x.disabled);
  if (bs.length) { bs[0].click(); return true; } return false; }"""
JS_STORY_CHOICE = """() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null); if(c[0]) { c[0].click(); return true; } return false; }"""

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        pg = br.new_page(viewport={"width": 390, "height": 844})
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        pg.goto(URL); pg.wait_for_timeout(3000)
        click_first(pg, ["新遊戲"], 1500)
        pg.evaluate("() => { const b = document.querySelector('[data-slot=\"1\"]'); if (b) b.click(); }")
        pg.wait_for_timeout(1200)
        click_first(pg, ["覆蓋", "確定", "確認"], 900)
        click_first(pg, ["跳過教學"], 1200)
        click_first(pg, ["開始寫手帳"], 1400)
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception as e:
            print("confirm-plan fail:", e)
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        pg.wait_for_timeout(1500)
        print("S:", pg.evaluate(JS_STATE))
        print("story:", pg.evaluate(JS_STORY))
        for i in range(60):
            st = pg.evaluate(JS_STORY)
            if not st['plate'] and not st['choices']:
                print("story done after", i, "steps")
                break
            if st['choices']:
                pg.evaluate(JS_STORY_CHOICE)
            else:
                pg.evaluate(JS_STORY_NEXT)
            pg.wait_for_timeout(900)
        pg.wait_for_timeout(1200)
        print("after story:", pg.evaluate(JS_STORY), "S:", pg.evaluate(JS_STATE))
        print("views:", pg.evaluate(JS_VIEWS))
        print("buttons:", pg.evaluate(JS_BTNS))
        pg.evaluate("() => { const b=document.getElementById('home-back-map'); if(b) b.click(); }")
        pg.wait_for_timeout(1500)
        print("after 返回地圖 views:", pg.evaluate(JS_VIEWS))
        print("map-start-today:", pg.evaluate("() => { const b=document.getElementById('map-start-today'); return b ? (b.offsetParent!==null)+' text='+(b.textContent||'').trim() : 'absent'; }"))
        print("data-loc tvb_longmen:", pg.evaluate("() => { const b=document.querySelector('button[data-loc=\"tvb_longmen\"]'); return b ? (b.offsetParent!==null) : 'absent'; }"))
        print("data-loc cafe_cha:", pg.evaluate("() => { const b=document.querySelector('button[data-loc=\"cafe_cha\"]'); return b ? (b.offsetParent!==null) : 'absent'; }"))
        print("S:", pg.evaluate(JS_STATE))
        pg.screenshot(path="/tmp/probe193_map.png")
        br.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        pass
