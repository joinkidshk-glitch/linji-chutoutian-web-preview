# -*- coding: utf-8 -*-
"""v20a197 C3 700 專用探針：clean-sheet loop（drive197h 做法）開茶餐廳真 sheet，量行動掣高度。
用法：/home/hatch/pwenv49/bin/python qa197/drive197l.py
結果併入 drive197.json -> final5_runs["700l"]。
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (OUT, EXE, serve, stop, snap, click_text, click_first,
                      dismiss_enc3, new_game, ensure_on_map, open_loc, close_loc,
                      STATE_JS, finish_intro, play_story, rect)
from drive197h import reset_quota
from playwright.sync_api import sync_playwright

def main():
    srv = serve()
    rec = {"height": 700, "probes": {}, "notes": []}
    errs = []
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=EXE)
            ctx = b.new_context(viewport={"width": 430, "height": 700})
            pg = ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e)))
            if not new_game(pg, confirm_plan=False):
                rec["notes"].append("new_game FAILED"); return
            pg.wait_for_timeout(600)
            click_text(pg, "確定本週行程", scope="#nb-actions", wait=1200)
            pg.wait_for_timeout(600)
            click_text(pg, "確定出發", wait=1200)
            for _ in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                    break
            finish_intro(pg)
            dismiss_enc3(pg); ensure_on_map(pg)
            clean = None
            for attempt in range(3):
                r = open_loc(pg, "茶餐廳")
                pg.wait_for_timeout(800)
                st = pg.evaluate(STATE_JS)
                if st["story"]:
                    play_story(pg, max_steps=60, tag_prefix="dlg_sheet700")
                    dismiss_enc3(pg); ensure_on_map(pg); reset_quota(pg); continue
                if st["enc"]:
                    dismiss_enc3(pg); ensure_on_map(pg); reset_quota(pg); continue
                clean = {"attempt": attempt, "open_loc": r, "state": st}
                break
            rec["probes"]["sheet_clean"] = clean
            if clean:
                rec["probes"]["c3_acts"] = pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet .act')]
                  .filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
                    return {t:(b.textContent||'').trim().slice(0,24), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; })""")
                rec["probes"]["loc_title"] = pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }")
                snap(pg, "700_l_c3_sheet.png")
                close_loc(pg)
            rec["probes"]["pageerrors"] = errs[:10]
            rec["zero_pageerror"] = len(errs) == 0
            ctx.close(); b.close()
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
    finally:
        stop(srv)
    out = json.load(open(os.path.join(OUT, "drive197.json"), encoding="utf-8"))
    out.setdefault("final5_runs", {})["700l"] = rec
    with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("== FINAL5 700l DONE ==", flush=True)

if __name__ == "__main__":
    main()
