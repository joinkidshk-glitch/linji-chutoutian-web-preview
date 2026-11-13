# -*- coding: utf-8 -*-
"""v20a197 B4 再驗證（932）：B4 補丁（固定高度＋底錨統一）之後，
soft 板 vs rest 板掣列 y 應該完全一致；C4 過一日確認（非 day-res）做對照。
用法：/home/hatch/pwenv49/bin/python qa197/drive197j.py
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (OUT, EXE, serve, stop, snap, click_text, click_first,
                      dismiss_enc3, new_game, ensure_on_map, open_journal,
                      SEED_DAYEND_JS, SEED_REST_JS, STATE_JS, finish_intro)
from drive197h import reset_quota, poll_modal
from drive197i import free_day
from playwright.sync_api import sync_playwright

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
            new_game(pg, confirm_plan=False)
            pg.wait_for_timeout(600)
            click_text(pg, "確定本週行程", scope="#nb-actions", wait=1200)
            pg.wait_for_timeout(600)
            click_text(pg, "確定出發", wait=1200)
            for _ in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                    break
            finish_intro(pg)
            dismiss_enc3(pg); ensure_on_map(pg)
            # soft 板
            pg.evaluate(SEED_DAYEND_JS, "soft")
            reset_quota(pg)
            open_journal(pg); pg.wait_for_timeout(700)
            click_first(pg, ["返回地圖"], 900); pg.wait_for_timeout(1000)
            m = poll_modal(pg, 8)
            if not m:
                click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
                m = poll_modal(pg, 15)
            rec["probes"]["b4_soft_v2"] = m
            snap(pg, "932_j_b4_soft.png")
            if m:
                click_text(pg, "返回地圖", scope="#modal-btns", wait=1200)
                pg.wait_for_timeout(900)
            dismiss_enc3(pg); ensure_on_map(pg)
            # rest 板
            pg.evaluate(SEED_REST_JS)
            reset_quota(pg)
            open_journal(pg); pg.wait_for_timeout(700)
            click_first(pg, ["返回地圖"], 900); pg.wait_for_timeout(1000)
            m2 = poll_modal(pg, 8)
            if not m2:
                click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
                m2 = poll_modal(pg, 15)
            rec["probes"]["b4_rest_v2"] = m2
            snap(pg, "932_j_b4_rest.png")
            if m2:
                click_text(pg, "返回地圖", scope="#modal-btns", wait=1500)
                pg.wait_for_timeout(1200)
            dismiss_enc3(pg); ensure_on_map(pg)
            # 對照：掣列 y 差
            if m and m2:
                ys_soft = [x["y"] for x in m["btns"]]
                ys_rest = [x["y"] for x in m2["btns"]]
                rec["probes"]["b4_compare"] = {
                    "soft_modal": {"y": m["modalY"], "h": m["modalH"]},
                    "rest_modal": {"y": m2["modalY"], "h": m2["modalH"]},
                    "soft_btn_ys": ys_soft, "rest_btn_ys": ys_rest,
                    "btn_y_diff": [a - b for a, b in zip(ys_soft, ys_rest)],
                    "identical": ys_soft == ys_rest}
            # C4 對照（非 day-res，應繼續置中）
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
                snap(pg, "932_j_c4.png")
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
    out.setdefault("final5_runs", {})["932j"] = rec
    with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("== FINAL5 932j DONE ==", flush=True)

if __name__ == "__main__":
    main()
