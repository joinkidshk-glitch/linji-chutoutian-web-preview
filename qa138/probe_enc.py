# -*- coding: utf-8 -*-
"""診斷 probe：重演 e_chai_T0（chai @ 星河，met/fav0），每步 dump 狀態：
  S.starDay（出沒盤＋triggered＋doneToday）、S.stars.chai_zanhoi、
  當前面板（邊個掣可見）、overlay 有冇。"""
import sys, os, subprocess, time, signal, json
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8972
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

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

def dump(pg, tag):
    st = pg.evaluate("""() => {
      const vis = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null)
        .map(b => (b.textContent||'').trim().slice(0, 18)).slice(0, 25);
      return {
        day: S.dayIndex, starDay: S.starDay || null,
        chai: (S.stars||{}).chai_zanhoi || null,
        overlay: !!document.getElementById('enc79-overlay'),
        title: (document.querySelector('#loc-title')||{}).textContent || null,
        visBtns: vis,
      };
    }""")
    print(f"--- {tag} ---")
    print(json.dumps(st, ensure_ascii=False, indent=1)[:1800])

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=ROOT,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
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
        print("new game ok:", pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"))
        dump(pg, "after new_game")
        # seed chai met/fav0
        pg.evaluate("""() => {
          S.stars = S.stars || {};
          const st = S.stars.chai_zanhoi || (S.stars.chai_zanhoi = {});
          st.met = true; st.fav = 0; st.stage = 0; st.beatsDone = {}; st.poolSeen = {};
          st.heartDone = false; st.wrapEcho = false; st.capHit = false; st.lastDay = -99;
          st.homeVisits = 0; st.homeVisitDay = -1; S.fame = 0; return true; }""")
        for day in [0, 1, 2]:
            pg.evaluate("(d) => { S.dayIndex = d; }", day)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
            pg.wait_for_timeout(500)
            r = click_first(pg, ["星河"], 1800)
            pg.wait_for_timeout(900)
            dump(pg, f"day {day} after click 星河 -> {r}")
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
            pg.wait_for_timeout(500)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE DONE")
