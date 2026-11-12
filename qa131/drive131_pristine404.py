# -*- coding: utf-8 -*-
"""qa131 pristine 對照：同一合成 StoryPlay.start(A_fong_push1) 喺 pristine main 跑，
數 arc_fong_push1.* 404——核實 drive131 嘅 12 個 404 係 pre-existing（抉擇屏 artId
fallback probing，arc art 根本未出過），唔係 B 批改動引起。
用法：/home/hatch/pwenv49/bin/python qa131/drive131_pristine404.py
"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/pristine131-worktree"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8963
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    return p

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        http404 = []
        def on_resp(resp):
            try:
                if resp.status >= 400:
                    http404.append(resp.url)
            except Exception:
                pass
        pg.on("response", on_resp)
        pg.goto(URL); pg.wait_for_timeout(3000)
        # 新遊戲（同 drive131 流程簡化版）
        def click_first(texts, wait=1000):
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
        click_first(["新遊戲"], 1500)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        click_first(["覆蓋", "確定", "確認"], 900)
        click_first(["跳過教學"], 1200)
        click_first(["開始寫手帳"], 1400)
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception:
            pass
        click_first(["確定出發"], 1500)
        for _ in range(4):
            if not click_first(["確定", "確認", "好", "知道了"], 900):
                break
        ok = pg.evaluate("""(n) => {
          try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) {}
          return false; }""", "A_fong_push1")
        print("pristine StoryPlay.start:", ok, flush=True)
        pg.wait_for_timeout(1500)
        # 行晒 6 句 → 抉擇屏（artId probing 喺呢度發生）
        for _ in range(8):
            clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
              if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
              if (!bs.length) return false; bs[0].click(); return true; }""")
            pg.wait_for_timeout(2200)
            if not clicked:
                break
        pg.wait_for_timeout(1000)
        print("PRISTINE pageerrors:", errs, flush=True)
        print("PRISTINE http404 count:", len(http404), flush=True)
        for u in http404:
            print("  404:", u, flush=True)
        json.dump({"pageerrors": errs, "http404": http404},
                  open("/home/hatch/workspace/linji-work131/qa131/drive131_pristine404.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        pass
