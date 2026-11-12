# -*- coding: utf-8 -*-
"""probe 出沒盤：新遊戲後，逐日（0..11 同 365..376）入一個地點，讀 S.starDay.presence，
睇吓 chai/lok/mak/chung 喺主場出現嘅日子。"""
import sys, os, subprocess, time, signal, json
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8973
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def click_first(pg, texts, wait=800):
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
        for day in [0, 1, 2, 5, 30]:
            pg.evaluate("(d) => { S.dayIndex = d; }", day)
            back = pg.evaluate("() => S.dayIndex")
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 700)
            back2 = pg.evaluate("() => S.dayIndex")
            click_first(pg, ["金龍"], 1200)
            sd = pg.evaluate("() => S.starDay ? {day: S.starDay.day, n: Object.keys(S.starDay.presence||{}).length} : null")
            back3 = pg.evaluate("() => S.dayIndex")
            print(f"set day {day}: readback {back} -> after back_to_map {back2} -> starDay {sd} -> dayIndex now {back3}")
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 700)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE DONE")
