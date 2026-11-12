# -*- coding: utf-8 -*-
"""qa131 巧遇攔截診斷 C：播完 A_fong_push1 之後，實際入中環廣告逐日睇 overlay；
同時讀地點 sheet 內文（有冇列出彭少祺在場），分辨 presence 定攔截下游。
"""
import sys, os, json, subprocess, time, signal
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work131"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8965
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
        pg.evaluate("""(a) => {
          S.stars = S.stars || {};
          const st = S.stars[a.star] || (S.stars[a.star] = {});
          st.met = true; st.fav = a.fav; st.beatsDone = {}; st.poolSeen = {};
          st.heartDone = false; st.stage = 0; st.wrapEcho = false; st.capHit = false;
        }""", {"star": "pang_siuki", "fav": 5})
        # 播故事（同 drive131）
        ok = pg.evaluate("""(n) => {
          try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) {}
          return false; }""", "A_fong_push1")
        print("story start:", ok, flush=True)
        pg.wait_for_timeout(1500)
        for _ in range(8):
            clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
              if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
              if (!bs.length) return false; bs[0].click(); return true; }""")
            pg.wait_for_timeout(1500)
            if not clicked:
                break
        pg.wait_for_timeout(800)
        pg.evaluate("""() => { const c = document.querySelector('.sp-choice');
          if (c) { c.click(); return true; } return false; }""")
        pg.wait_for_timeout(1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續", "返回地圖"], 900):
                break
        pg.wait_for_timeout(800)
        print("after story: dayIndex=", pg.evaluate("() => S.dayIndex"), flush=True)
        for day in range(0, 8):
            pg.evaluate("(d) => { S.dayIndex = d; }", day)
            click_first(pg, ["返回地圖"], 700)
            pg.wait_for_timeout(400)
            click_first(pg, ["中環廣告"], 1800)
            pg.wait_for_timeout(1000)
            st = pg.evaluate("""() => {
              const ov = document.getElementById('enc79-overlay');
              const sheet = document.getElementById('loc-sheet');
              const sheetTxt = sheet ? sheet.innerText.slice(0, 400) : '';
              return {enc: !!ov, sheetOn: !!sheet && sheet.classList.contains('on'),
                      pangInSheet: sheetTxt.includes('彭少祺'),
                      sheetHasStar: /彭少祺|少祺/.test(sheetTxt),
                      starDay: (window.S && S.starDay) ? {day: S.starDay.day, triggered: S.starDay.triggered,
                        presAd: (S.starDay.presence||{})['ad_central'] || []} : null}; }""")
            print(f"day {day}:", json.dumps(st, ensure_ascii=False), flush=True)
            if st["enc"]:
                print("  >>> OVERLAY TRIGGERED day", day, flush=True)
                break
            click_first(pg, ["返回地圖"], 700)
            pg.wait_for_timeout(400)
        print("PAGEERRORS:", errs[:5], flush=True)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        pass
