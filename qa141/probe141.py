# probe141：只探印章 border＋吊牌尺寸嘅 computed style／matched rules。
import os, subprocess, time, signal, hashlib, urllib.request, json
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work141"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8963
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=ROOT,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        pg = b.new_context(viewport={"width": 430, "height": 932}, device_scale_factor=2).new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR", e))
        def click_first(texts, wait=1000):
            for t in texts:
                loc = pg.locator("button:has-text('" + t + "')")
                for i in range(loc.count()):
                    el = loc.nth(i)
                    try:
                        if el.is_visible() and el.is_enabled():
                            el.click(timeout=900); pg.wait_for_timeout(wait); return t
                    except Exception:
                        pass
            return None
        pg.goto(URL); pg.wait_for_timeout(3000)
        click_first(["新遊戲"], 1500)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        click_first(["覆蓋", "確定", "確認"], 900)
        click_first(["跳過教學"], 1200)
        click_first(["開始寫手帳"], 1400)
        pg.wait_for_timeout(1000)
        tag_probe = pg.evaluate("""() => {
          const el = document.getElementById('home-back-map-tabs');
          const cs = getComputedStyle(el);
          return {cls: el.className, w: cs.width, h: cs.height, minH: cs.minHeight,
                  pad: cs.padding, boxSizing: cs.boxSizing, flex: cs.flex,
                  rect: (()=>{const b=el.getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)];})()}; }""")
        print("TAG editable:", json.dumps(tag_probe, ensure_ascii=False), flush=True)
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        click_first(["確定出發"], 1500)
        for _ in range(4):
            if not click_first(["確定", "確認", "好", "知道了"], 900):
                break
        pg.wait_for_timeout(800)
        pg.locator("button:has-text('☰')").first.click(timeout=3000); pg.wait_for_timeout(900)
        click_first(["手帳"], 1400); pg.wait_for_timeout(1000)
        out = pg.evaluate("""() => {
          const el = document.getElementById('btn-confirm-plan');
          const cs = getComputedStyle(el);
          const rules = [];
          for (const sheet of document.styleSheets) {
            let rs; try { rs = sheet.cssRules; } catch(_e) { continue; }
            for (const r of rs) {
              try {
                if (r.selectorText && el.matches(r.selectorText) && /border|#btn-confirm-plan|button\\.ink/.test(r.cssText))
                  rules.push(r.selectorText + ' :: ' + r.style.getPropertyValue('border') + ' / ' + r.style.getPropertyValue('border-top'));
              } catch(_e) {}
            }
          }
          return {cls: el.className, border: cs.border, borderTop: cs.borderTop,
                  borderTopWidth: cs.borderTopWidth, borderTopStyle: cs.borderTopStyle,
                  borderTopColor: cs.borderTopColor, color: cs.color, fontSize: cs.fontSize,
                  matchedBorderRules: rules}; }""")
        print("STAMP locked:", json.dumps(out, ensure_ascii=False, indent=1), flush=True)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
