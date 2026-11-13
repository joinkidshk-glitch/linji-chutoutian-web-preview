# -*- coding: utf-8 -*-
"""debug：new_game 之後玩家喺邊個畫面？#map-start-today 喺唔喺度？"""
import os, subprocess, time, signal, hashlib, urllib.request, json
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work194"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8995


def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    return p


def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass


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


def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = ctx.new_page(viewport={"width": 932, "height": 700})
            pg.on("pageerror", lambda e: print("PAGEERROR:", e, flush=True))
            pg.goto(f"http://127.0.0.1:{PORT}/index.html"); pg.wait_for_timeout(3000)
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
            pg.wait_for_timeout(1500)
            info = pg.evaluate("""() => {
              const vis = [...document.querySelectorAll('[id^="v-"]')].filter(e => e.offsetParent !== null).map(e => e.id);
              const st = document.getElementById('map-start-today');
              const hbm = document.getElementById('home-back-map');
              const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => ((b.id ? '#' + b.id + ' ' : '') + (b.textContent || '').trim().slice(0, 20)));
              return {visibleViews: vis, hasS: !!window.S, dayIndex: window.S ? S.dayIndex : null,
                      mapStartToday: st ? {visible: st.offsetParent !== null, text: st.textContent} : null,
                      homeBackMap: hbm ? {visible: hbm.offsetParent !== null, text: hbm.textContent, mode: hbm.getAttribute('data-mode')} : null,
                      buttons: btns.slice(0, 40)};
            }""")
            print(json.dumps(info, ensure_ascii=False, indent=1), flush=True)
            pg.screenshot(path="/tmp/dbg194_map.png")
            ctx.close()
    finally:
        stop(srv)


if __name__ == "__main__":
    main()
