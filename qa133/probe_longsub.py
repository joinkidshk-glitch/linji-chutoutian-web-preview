# -*- coding: utf-8 -*-
"""v20a133 探針（唔入 suite）：最長 setting（51 字，wf4_ev_boss01「老闆娘叫霞姐」）
喺 430×700 會唔會令 inner 要捲。做法：開 day02 modal 後，喺頁面將 .sub 換成
51 字 setting，重新量度——sub 只係同一元素嘅文字，幾何問題同真事件一致。
用法：/home/hatch/pwenv49/bin/python qa133/probe_longsub.py
"""
import json, subprocess, sys, time, os
sys.path.insert(0, "/home/hatch/workspace/linji-work133/qa133")
from drive133 import (ROOT, EXE, PORT, SHOTS, vis_btn, click_vis_btn, dismiss_once,
                      modal_h3, MEASURE_JS)
from playwright.sync_api import sync_playwright

LONG_SUB = "金龍茶餐廳，下晝三點幾，落場冇乜人"

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        ctx = b.new_context(viewport={"width": 430, "height": 700})
        pg = ctx.new_page()
        pg.goto(f"http://127.0.0.1:{PORT}/index.html?softPreview=1")
        pg.wait_for_timeout(1500)
        pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
        pg.wait_for_timeout(1000)
        try:
            pg.locator('[data-slot="3"]').first.click(timeout=1500)
            pg.wait_for_timeout(800)
        except Exception:
            pass
        for _ in range(10):
            try:
                pg.get_by_text("跳過教學", exact=True).first.click(timeout=1200)
                pg.wait_for_timeout(600)
                break
            except Exception:
                try:
                    pg.get_by_text("下一步", exact=True).first.click(timeout=1200)
                    pg.wait_for_timeout(600)
                except Exception:
                    break
        pg.wait_for_timeout(1200)
        for _ in range(40):
            if vis_btn(pg, "過一日"):
                break
            if not dismiss_once(pg):
                if not click_vis_btn(pg, "返回地圖"):
                    pg.wait_for_timeout(500)
            pg.wait_for_timeout(700)
        for d in range(3):
            if not click_vis_btn(pg, "過一日"):
                print("no advance btn day", d); sys.exit(2)
            for _ in range(40):
                if vis_btn(pg, "過一日"):
                    break
                dismiss_once(pg)
                pg.wait_for_timeout(700)
        pg.evaluate("""() => {
            if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
            S.wf4.pending = 'wf4_ev_day02'; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
        }""")
        click_vis_btn(pg, "過一日")
        found = False
        for i in range(60):
            pg.wait_for_timeout(1000)
            if "傳呼台" in modal_h3(pg):
                found = True
                break
            dismiss_once(pg)
        print("found day02:", found)
        pg.wait_for_timeout(800)
        before = pg.evaluate(MEASURE_JS)
        print("sub 換前：sub h=%s line=%s inner %s/%s" % (before["sub"]["h"], before["sub"], before["innerScrollH"], before["innerClientH"]))
        pg.evaluate("(t) => { document.querySelector('#modal .sub').textContent = t; }", LONG_SUB)
        pg.wait_for_timeout(400)
        cs = pg.evaluate("""() => { const s = document.querySelector('#modal .sub'); const c = getComputedStyle(s);
          return {text: s.textContent, len: s.textContent.length, ws: c.whiteSpace, ov: c.overflow, to: c.textOverflow,
                  fontSize: c.fontSize, scrollW: s.scrollWidth, clientW: s.clientWidth}; }""")
        print("sub computed:", json.dumps(cs, ensure_ascii=False))
        m = pg.evaluate(MEASURE_JS)
        print("sub 換後（51 字）：sub h=%s （%d 行）" % (m["sub"]["h"], round(m["sub"]["h"] / 20)))
        sp, st, pl, ln, inn = m["storyPlay"], m["stage"], m["plate"], m["line"], m["inner"]
        inner_vis_bottom = inn["y"] + m["innerClientH"]
        checks = {
            "A_stage_le_storyPlay": st["bottom"] <= sp["bottom"] + 1,
            "B_line_le_plate": ln["bottom"] <= pl["bottom"] + 1,
            "C_plate_le_innerVis": pl["bottom"] <= inner_vis_bottom + 1,
            "D_inner_noScroll": m["innerScrollH"] <= m["innerClientH"] + 1,
        }
        print("stage h=%s bottom %s vs sp %s | plate visible=%s line bottom=%s plate bottom=%s | inner %s/%s | overflow=%s -> %s %s"
              % (st["h"], st["bottom"], sp["bottom"], min(pl["bottom"], sp["bottom"]) - pl["y"],
                 ln["bottom"], pl["bottom"], m["innerScrollH"], m["innerClientH"],
                 m["innerScrollH"] - m["innerClientH"], "PASS" if all(checks.values()) else "FAIL", checks))
        pg.screenshot(path=os.path.join(SHOTS, "wf4_longsub_430x700.png"))
        ctx.close()
        b.close()
finally:
    srv.terminate()
