# -*- coding: utf-8 -*-
"""v20a197 U4 toast 文案即時捕捉（932）：額度用完嗰陣撳星河電視台，
click 後即刻每 100ms 輪詢 #toast（顯示期只得 1800ms，之後 replaceChildren 清空）。
用法：/home/hatch/pwenv49/bin/python qa197/drive197m.py
結果併入 drive197.json -> final5_runs["932m"]。
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (OUT, EXE, serve, stop, snap, click_text, click_first,
                      dismiss_enc3, new_game, ensure_on_map, open_loc, close_loc,
                      STATE_JS, finish_intro, modal_btns)
from drive197h import reset_quota
from playwright.sync_api import sync_playwright

TOAST_JS = """() => { const t=document.getElementById('toast');
  if(!t) return {found:false};
  return {text:(t.textContent||'').trim(), on:t.classList.contains('on'),
    aria:t.getAttribute('aria-hidden'), cls:(t.className||'').toString()}; }"""

def main():
    srv = serve()
    rec = {"height": 932, "probes": {}, "notes": []}
    errs = []
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=EXE)
            ctx = b.new_context(viewport={"width": 430, "height": 932})
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
            # 先清乾淨：確保 mask 閂、冇 story／enc
            st = pg.evaluate(STATE_JS)
            rec["probes"]["clean_check"] = st
            if st["maskOn"] or st["story"] or st["enc"]:
                click_first(pg, ["關閉"], 900); pg.wait_for_timeout(800)
                dismiss_enc3(pg); ensure_on_map(pg)
                st = pg.evaluate(STATE_JS)
                rec["probes"]["clean_check2"] = st
            reset_quota(pg)
            # 用返一次額度（正常入一次地點再返嚟），等 used=1 係真實狀態
            open_loc(pg, "星河電視台")
            pg.wait_for_timeout(700)
            dismiss_enc3(pg); pg.wait_for_timeout(400)
            close_loc(pg); pg.wait_for_timeout(600)
            dismiss_enc3(pg); ensure_on_map(pg)
            pre = {"state": pg.evaluate(STATE_JS),
                   "toast": pg.evaluate(TOAST_JS),
                   "used": pg.evaluate("() => (S.travel114||{}).used"),
                   "hint": pg.evaluate("() => { const h=document.getElementById('map-hint'); return h?(h.textContent||'').trim().slice(0,90):null; }")}
            rec["probes"]["u4_pre"] = pre
            # 設 used=2（額度用完）
            pg.evaluate("() => { try { S.travel114 = {used:2, day:S.dayIndex}; return true; } catch(e){ return String(e); } }")
            pg.wait_for_timeout(200)
            # 即刻撳星河電視台＋即時輪詢 toast
            clicked = click_text(pg, "星河電視台", scope="#v-map", wait=800)
            samples = []
            t0 = time.time()
            while time.time() - t0 < 3.0:
                samples.append({"ms": round((time.time()-t0)*1000), **pg.evaluate(TOAST_JS)})
                pg.wait_for_timeout(100)
            post = {"state": pg.evaluate(STATE_JS),
                    "toast": pg.evaluate(TOAST_JS),
                    "used": pg.evaluate("() => (S.travel114||{}).used"),
                    "locTitle": pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }"),
                    "hint": pg.evaluate("() => { const h=document.getElementById('map-hint'); return h?(h.textContent||'').trim().slice(0,90):null; }")}
            rec["probes"]["u4_toast"] = {"clicked": clicked, "samples": samples, "post": post,
                "seen_texts": sorted({s["text"] for s in samples if s.get("text")})}
            snap(pg, "932_m_u4.png")
            rec["probes"]["pageerrors"] = errs[:10]
            rec["zero_pageerror"] = len(errs) == 0
            ctx.close(); b.close()
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
    finally:
        stop(srv)
    out = json.load(open(os.path.join(OUT, "drive197.json"), encoding="utf-8"))
    out.setdefault("final5_runs", {})["932m"] = rec
    with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("== FINAL5 932m DONE ==", flush=True)

if __name__ == "__main__":
    main()
