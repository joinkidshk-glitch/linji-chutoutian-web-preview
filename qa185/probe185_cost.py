#!/usr/bin/env python3
"""debug：右欄卡片 .cost rect 點解 elementFromPoint 命中 BODY。"""
import subprocess, sys, time, os
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v183")
import probe183 as P
from playwright.sync_api import sync_playwright
ROOT = "/home/hatch/workspace/linji-work185"
PORT = 8979
P.ROOT = ROOT; P.PORT = PORT

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
            P.new_game_to_map(pg)
            mi, day, attempts = P.enter_woman(pg, "hiu", "tvb_longmen")
            P.click_vis_btn(pg, "送禮", "#modal")
            pg.wait_for_timeout(1000)
            out = pg.evaluate("""() => [...document.querySelectorAll('#gift-pick-list > *')].map((el, i) => {
              const br = el.getBoundingClientRect();
              const cost = el.querySelector('.cost');
              const cr = cost ? cost.getBoundingClientRect() : null;
              const ccx = cr ? Math.round((cr.left + cr.right) / 2) : null;
              const ccy = cr ? Math.round((cr.top + cr.bottom) / 2) : null;
              const hit = (ccx !== null) ? document.elementFromPoint(ccx, ccy) : null;
              const n = el.querySelector('.n');
              const nr = n ? n.getBoundingClientRect() : null;
              return { i, btn: { l: Math.round(br.left), r: Math.round(br.right), t: Math.round(br.top), b: Math.round(br.bottom), w: Math.round(br.width) },
                cost: cr ? { l: Math.round(cr.left), r: Math.round(cr.right), t: Math.round(cr.top), b: Math.round(cr.bottom), w: Math.round(cr.width), h: Math.round(cr.height), cx: ccx, cy: ccy } : null,
                hitTag: hit ? (hit.tagName + '.' + (hit.className || '').toString().slice(0, 40)) : null,
                nW: nr ? Math.round(nr.width) : null,
                nText: n ? (n.innerText || '').replace(/\\n/g, '|') : null,
                nameSpanW: (() => { const s = el.querySelector('.gift-pick-name'); if (!s) return null; const r2 = s.getBoundingClientRect(); return Math.round(r2.width); })(),
                scrollW: el.scrollWidth, clientW: el.clientWidth };
            })""")
            print(__import__('json').dumps(out, ensure_ascii=False, indent=1))
            print("pageerrors", errs)
            ctx.close(); b.close()
    finally:
        srv.terminate()

if __name__ == "__main__":
    main()
