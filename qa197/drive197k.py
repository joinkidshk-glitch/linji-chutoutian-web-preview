# -*- coding: utf-8 -*-
"""v20a197 700 聚焦再驗證：B1 主線「下一句」＋B4 soft/rest＋C3 sheet 行動掣＋C4 對照。
流程沿用 drive197h（B1）＋drive197j（B4），只改 viewport 做 700。
用法：/home/hatch/pwenv49/bin/python qa197/drive197k.py
結果併入 drive197.json -> final5_runs["700k"]。
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (OUT, EXE, serve, stop, snap, click_text, click_first,
                      dismiss_enc3, new_game, ensure_on_map, open_journal, open_loc, close_loc,
                      SEED_DAYEND_JS, SEED_REST_JS, STATE_JS, finish_intro)
from drive197h import reset_quota, poll_modal
from drive197i import free_day
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
            ok, steps = finish_intro(pg)
            rec["probes"]["intro_finished"] = ok
            rec["probes"]["b1_mainline"] = [
                {"step": s["step"], "kind": s["kind"],
                 "next": [x for x in s["census"]["buttons"] if "下一句" in x["text"]][:2]}
                for s in steps[:8]]
            snap(pg, "700_k_b1_mainline.png")
            dismiss_enc3(pg); ensure_on_map(pg)
            # ---- C3：開茶餐廳 sheet，量行動掣 ----
            r = open_loc(pg, "茶餐廳")
            pg.wait_for_timeout(700)
            st = pg.evaluate(STATE_JS)
            if st["story"]:
                from drive197 import play_story
                play_story(pg, max_steps=30, tag_prefix="dlg_tea700")
                dismiss_enc3(pg); ensure_on_map(pg)
                r = open_loc(pg, "茶餐廳")
                pg.wait_for_timeout(700)
            rec["probes"]["c3_open"] = r
            rec["probes"]["c3_acts"] = pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet .act')]
              .filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
                return {t:(b.textContent||'').trim().slice(0,20), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; })""")
            snap(pg, "700_k_c3_sheet.png")
            close_loc(pg); dismiss_enc3(pg); ensure_on_map(pg)
            # ---- B4 soft ----
            pg.evaluate(SEED_DAYEND_JS, "soft")
            reset_quota(pg)
            open_journal(pg); pg.wait_for_timeout(700)
            click_first(pg, ["返回地圖"], 900); pg.wait_for_timeout(1000)
            m = poll_modal(pg, 8)
            if not m:
                click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
                m = poll_modal(pg, 15)
            rec["probes"]["b4_soft"] = m
            snap(pg, "700_k_b4_soft.png")
            if m:
                click_text(pg, "返回地圖", scope="#modal-btns", wait=1200)
                pg.wait_for_timeout(900)
            dismiss_enc3(pg); ensure_on_map(pg)
            # ---- B4 rest ----
            pg.evaluate(SEED_REST_JS)
            reset_quota(pg)
            open_journal(pg); pg.wait_for_timeout(700)
            click_first(pg, ["返回地圖"], 900); pg.wait_for_timeout(1000)
            m2 = poll_modal(pg, 8)
            if not m2:
                click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
                m2 = poll_modal(pg, 15)
            rec["probes"]["b4_rest"] = m2
            snap(pg, "700_k_b4_rest.png")
            if m2:
                click_text(pg, "返回地圖", scope="#modal-btns", wait=1500)
                pg.wait_for_timeout(1200)
            dismiss_enc3(pg); ensure_on_map(pg)
            if m and m2:
                ys_soft = [x["y"] for x in m["btns"]]
                ys_rest = [x["y"] for x in m2["btns"]]
                rec["probes"]["b4_compare"] = {
                    "soft_modal": {"y": m["modalY"], "h": m["modalH"]},
                    "rest_modal": {"y": m2["modalY"], "h": m2["modalH"]},
                    "soft_btn_ys": ys_soft, "rest_btn_ys": ys_rest,
                    "btn_y_diff": [a - b for a, b in zip(ys_soft, ys_rest)],
                    "identical": ys_soft == ys_rest}
            # ---- C4 對照（非 day-res，應繼續置中） ----
            free_day(pg)
            if click_text(pg, "過一日", scope="#v-map", wait=1200):
                pg.wait_for_timeout(900)
                rec["probes"]["c4_control"] = pg.evaluate("""() => {
                  const mask = document.getElementById('mask');
                  const cs = mask ? getComputedStyle(mask) : null;
                  return {btns: [...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
                    return {t:(b.textContent||'').trim(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; }),
                    maskCls: mask?mask.className:null, maskAI: cs?cs.alignItems:null,
                    modal: (()=>{ const mo=document.querySelector('#mask .modal'); const r=mo?mo.getBoundingClientRect():null;
                      return r?{y:Math.round(r.top), h:Math.round(r.height)}:null; })()}; }""")
                snap(pg, "700_k_c4.png")
                click_first(pg, ["取消"], 900)
                pg.wait_for_timeout(700)
            rec["probes"]["pageerrors"] = errs[:10]
            rec["zero_pageerror"] = len(errs) == 0
            ctx.close(); b.close()
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
    finally:
        stop(srv)
    out = json.load(open(os.path.join(OUT, "drive197.json"), encoding="utf-8"))
    out.setdefault("final5_runs", {})["700k"] = rec
    with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("== FINAL5 700k DONE ==", flush=True)

if __name__ == "__main__":
    main()
