# -*- coding: utf-8 -*-
"""Probe: case (e) 合併場 — 推出短訊喺 v214 分頁報紙入面去咗邊。
重用 drive215 嘅播種＋場次設定，只係加 dump 全個 #modal innerHTML（包埋隱藏嘅第二版）
同撳「第二版 →」之後嘅可見文字。
"""
import json, os, sys
QA = "/home/hatch/workspace/linji-work215/qa215"
sys.path.insert(0, "/home/hatch/workspace/linji-work215/qa188")
sys.path.insert(0, QA)
import drive188 as d
import drive215 as d15
from playwright.sync_api import sync_playwright

d.ROOT = "/home/hatch/workspace/linji-work215"
d.QA = QA
d.SHOTS = os.path.join(QA, "shots215")
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 21591

AWARD = {"eventKey": "award:1990:award_harbour_film", "source": "award",
         "enqueuedDay": 150, "publishDay": 151, "fameDelta": 2,
         "paperName": "娛樂快報", "headline": "頒獎見報",
         "dek": "維港影藝獎之夜結果出爐。",
         "clipLabel": "娛樂快報・頒獎夜", "rumorEcho": "",
         "medium": "film", "workTitle": "維港影藝獎"}
TARGET = "《孤劍破陣》夏季上映"

srv = d.serve()
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=d.EXE)
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        assert d.new_game(pg), "new_game failed"
        sd = pg.evaluate(d15.JS_SEED, {"gig": "baseFilm", "dayIndex": 151, "wrapDay": 100, "award": AWARD})
        print("seed:", json.dumps(sd, ensure_ascii=False))
        clicked, modal = d15.continue_and_wait(pg)
        print("modal h3:", modal.get("h3"), "| btns:", modal.get("btns"))
        html = pg.evaluate("() => document.querySelector('#modal').innerHTML")
        print("TARGET in full modal HTML:", TARGET in html)
        print("TARGET in visible innerText p1:", TARGET in (modal.get("body") or ""))
        # 搵短訊渲染位置：邊個 np214 page 容器有 TARGET
        loc = pg.evaluate("""(t) => {
          const out = [];
          document.querySelectorAll('#modal [class*="np214"], #modal [data-page], #modal section, #modal div').forEach(el => {
            if (el.textContent && el.textContent.includes(t)) {
              const cls = (el.className||'').toString().slice(0,80);
              const cs = getComputedStyle(el);
              out.push({tag: el.tagName, cls, display: cs.display, vis: cs.visibility,
                        text: (el.textContent||'').slice(0,60)});
            }
          });
          return out.slice(0, 8);
        }""", TARGET)
        print("containers holding TARGET:", json.dumps(loc, ensure_ascii=False, indent=1))
        # 撳第二版
        clicked2 = d.click_text(pg, ["第二版"], 1200)
        print("clicked 第二版:", clicked2)
        modal2 = d.modal_info(pg)
        print("p2 visible TARGET:", TARGET in (modal2.get("body") or ""))
        print("p2 body:", (modal2.get("body") or "")[:900])
        d.shot(pg, "e_probe_p2.png")
        print("pageerrors:", errs)
        b.close()
finally:
    d.stop(srv)
