#!/usr/bin/env python3
"""量度 700 下每件禮物名 span 係咪被 ellipsis 截斷（scrollWidth vs clientWidth）。"""
import subprocess, sys, time, json
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v183")
import probe183 as P
from playwright.sync_api import sync_playwright
ROOT = "/home/hatch/workspace/linji-work185"
PORT = 8980
P.ROOT = ROOT; P.PORT = PORT

def run(pg):
    P.new_game_to_map(pg)
    mi, day, attempts = P.enter_woman(pg, "hiu", "tvb_longmen")
    P.click_vis_btn(pg, "送禮", "#modal")
    pg.wait_for_timeout(1000)
    return pg.evaluate("""() => [...document.querySelectorAll('#gift-pick-list > *')].map(el => {
      const s = el.querySelector('.gift-pick-name');
      const n = el.querySelector('.n');
      // 可見文字：用 Range 量度第一行實際渲染文字（ellipsis 會令 textContent 長過可見）
      let visible = null;
      try { const range = document.createRange(); range.selectNodeContents(s);
        const rects = [...range.getClientRects()].map(r => Math.round(r.width));
        visible = { rects, text: s.textContent }; } catch(e) { visible = { err: String(e) }; }
      return { full: s.textContent, clientW: s.clientWidth, scrollW: s.scrollWidth,
               truncated: s.scrollWidth > s.clientWidth + 1,
               nH: Math.round(n.getBoundingClientRect().height),
               computed: getComputedStyle(s).textOverflow };
    })""")

def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=P.EXE)
            ctx = b.new_context(viewport={"width": 430, "height": 700})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            out = run(pg)
            print(json.dumps(out, ensure_ascii=False, indent=1))
            print("pageerrors", errs)
            ctx.close(); b.close()
    finally:
        srv.terminate()

if __name__ == "__main__":
    main()
