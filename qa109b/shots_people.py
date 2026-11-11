# -*- coding: utf-8 -*-
"""v20a109 B 補拍：人情頁全列表分段截圖（full_page 捉唔到內部捲動容器，
故逐段捲動 scroll container 再逐 viewport 截圖，務求 18 行全部入鏡）。
用法：/home/hatch/pwenv49/bin/python qa109b/shots_people.py [before|after]
  before → pristine main；after → v109-bust（預設 after）。
"""
import sys, os, subprocess, time, signal, hashlib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive109 import serve, stop, click_first, new_game, open_people, JS_SETUP_STATE, PORT, URL, SHOTS
from playwright.sync_api import sync_playwright

MODE = sys.argv[1] if len(sys.argv) > 1 else "after"
CWD = "/home/hatch/workspace/linji-pristine109b" if MODE == "before" else "/home/hatch/workspace/linji-work109b"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"

JS_SCROLL_INFO = """() => {
  const box = document.getElementById('people-list');
  if (!box) return null;
  let el = box;
  while (el) {
    if (el.scrollHeight > el.clientHeight + 10) {
      return {tag: el.tagName, cls: (el.className||'').toString().slice(0,80),
              id: el.id, sh: el.scrollHeight, ch: el.clientHeight};
    }
    el = el.parentElement;
  }
  return {tag: 'window', sh: document.documentElement.scrollHeight,
          ch: window.innerHeight};
}"""

srv = serve(CWD)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        print("new game:", new_game(pg))
        print("setup:", pg.evaluate(JS_SETUP_STATE))
        rows = open_people(pg)
        print("rows:", len(rows.get("rows", [])))
        info = pg.evaluate(JS_SCROLL_INFO)
        print("scroll container:", info)
        # 逐段捲動：每段捲 (viewport 高 - 120px)，直至底部；每段截一張。
        for step in range(6):
            top = pg.evaluate("""() => {
              const box = document.getElementById('people-list');
              let el = box;
              while (el) {
                if (el.scrollHeight > el.clientHeight + 10) {
                  el.scrollTop = Math.min(el.scrollHeight - el.clientHeight,
                    el.scrollTop + (el.clientHeight - 120));
                  return {scrollTop: el.scrollTop, max: el.scrollHeight - el.clientHeight};
                }
                el = el.parentElement;
              }
              window.scrollBy(0, window.innerHeight - 120);
              return {scrollTop: window.scrollY, max: document.documentElement.scrollHeight - window.innerHeight};
            }""")
            pg.wait_for_timeout(600)
            pg.screenshot(path=f"{SHOTS}/people_{MODE}_s{step}.png")
            print(f"step {step}: {top}")
            if top["scrollTop"] >= top["max"] - 2:
                print("reached bottom at step", step)
                break
        print("pageerrors:", errs)
        b.close()
finally:
    stop(srv)
print("done")
