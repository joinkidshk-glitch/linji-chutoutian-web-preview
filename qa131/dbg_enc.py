# -*- coding: utf-8 -*-
"""qa131 巧遇觸發診斷：新遊戲 → seed 彭少祺 → 逐日入中環廣告，dump 當時畫面狀態。"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
sys.path.insert(0, "/home/hatch/workspace/linji-work131/qa131")
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work131"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8962
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    return p

def click_first(pg, texts, wait=1000):
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

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(3000)
        click_first(pg, ["新遊戲"], 1500)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        click_first(pg, ["覆蓋", "確定", "確認"], 900)
        click_first(pg, ["跳過教學"], 1200)
        click_first(pg, ["開始寫手帳"], 1400)
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception:
            pass
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        print("S:", pg.evaluate("() => window.S ? (S.dayIndex + ' ' + S.dateStr + ' loc=' + (S.loc||'')) : 'no S'"), flush=True)
        pg.evaluate("""(a) => {
          S.stars = S.stars || {};
          const st = S.stars[a.star] || (S.stars[a.star] = {});
          st.met = true; st.fav = a.fav; st.beatsDone = {}; st.poolSeen = {};
          st.heartDone = false; st.stage = 0; st.wrapEcho = false; st.capHit = false;
        }""", {"star": "pang_siuki", "fav": 5})
        # 睇下地圖有咩掣
        dump = pg.evaluate("""() => {
          const vis = el => { const r = el.getBoundingClientRect(); return r.width>0 && r.height>0; };
          const btns = [...document.querySelectorAll('button')].filter(vis)
            .map(e => (e.innerText||e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,30));
          const views = [...document.querySelectorAll('.view')].map(v => v.id + ':' + (v.classList.contains('on')?'on':'off'));
          return {btns: btns.slice(0,40), views};
        }""")
        print("MAP BTNS:", json.dumps(dump, ensure_ascii=False), flush=True)
        for day in [0, 1, 2, 3]:
            pg.evaluate("(d) => { S.dayIndex = d; }", day)
            r = click_first(pg, ["中環廣告"], 1800)
            pg.wait_for_timeout(1000)
            st = pg.evaluate("""() => {
              const ov = document.getElementById('enc79-overlay');
              const sheet = document.getElementById('loc-sheet');
              return {clicked: true, enc: !!ov, locSheet: !!sheet && sheet.classList.contains('on'),
                      S_loc: (window.S||{}).loc, travel: JSON.stringify((window.S||{}).travel||null),
                      toast: (document.querySelector('.toast')||{textContent:''}).textContent.slice(0,80)}; }""")
            print(f"day {day} click={r} state:", json.dumps(st, ensure_ascii=False), flush=True)
            pg.screenshot(path=f"/home/hatch/workspace/linji-work131/qa131/shots/dbg_enc_day{day}.png")
            click_first(pg, ["返回地圖"], 700)
            pg.wait_for_timeout(500)
        print("PAGEERRORS:", errs[:5], flush=True)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        pass
