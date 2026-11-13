# -*- coding: utf-8 -*-
"""v20a197 聚焦探針（932）：B4 兩板幾何隨時間採樣、C4 過一日確認、B6 自由日、
U4 乾淨態、B1 跨日 hunt（自由日推進）。
用法：/home/hatch/pwenv49/bin/python qa197/drive197i.py
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (OUT, SHOTS, URL, EXE, serve, stop, snap, census, rect,
                      modal_btns, click_text, click_first, dismiss_enc3, play_story,
                      new_game, ensure_on_map, open_loc, close_loc, open_journal,
                      SEED_DAYEND_JS, SEED_REST_JS, STATE_JS, finish_intro)
from drive197h import wf4rand, day_plan, LOCS, NAME, reset_quota, poll_modal, measure_enc
from playwright.sync_api import sync_playwright

SAMPLE_JS = """() => {
  const mask = document.getElementById('mask');
  const modal = document.querySelector('#mask .modal');
  const cs = (el, p) => el ? getComputedStyle(el)[p] : null;
  const inner = document.getElementById('modal-inner');
  const r = modal ? modal.getBoundingClientRect() : null;
  return {
    maskCls: mask ? mask.className : null,
    maskChildren: mask ? [...mask.children].map(c => (c.tagName + '.' + (c.className || '').toString().split(' ').slice(0, 3).join('.')).slice(0, 60)) : [],
    maskCS: mask ? {ai: cs(mask, 'alignItems'), jc: cs(mask, 'justifyContent'), fd: cs(mask, 'flexDirection'), pad: cs(mask, 'padding'), h: Math.round(mask.getBoundingClientRect().height)} : null,
    modal: r ? {x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height)} : null,
    modalCS: modal ? {mt: cs(modal, 'marginTop'), mb: cs(modal, 'marginBottom'), trans: cs(modal, 'transition'), anim: cs(modal, 'animation'), maxH: cs(modal, 'maxHeight'), h: cs(modal, 'height'), pos: cs(modal, 'position')} : null,
    modalParent: modal && modal.parentElement ? (modal.parentElement.tagName + '#' + (modal.parentElement.id || '') + '.' + (modal.parentElement.className || '').toString().split(' ').slice(0, 2).join('.')) : null,
    innerScroll: inner ? {sh: inner.scrollHeight, ch: inner.clientHeight} : null,
    title: (() => { const h = document.querySelector('#modal-inner h3'); return h ? (h.textContent || '').trim() : null; })(),
    btns: [...document.querySelectorAll('#modal-btns button')].filter(b => b.offsetParent !== null).map(b => { const rr = b.getBoundingClientRect(); return {t: (b.textContent || '').trim().slice(0, 14), x: Math.round(rr.left), y: Math.round(rr.top), w: Math.round(rr.width), h: Math.round(rr.height)}; })
  }; }"""

def sample_modal(pg, secs=3.0):
    out = []
    t0 = time.time()
    while time.time() - t0 < secs:
        out.append(pg.evaluate(SAMPLE_JS))
        pg.wait_for_timeout(500)
    return out

def free_day(pg):
    """將今日格清做自由日（weekPlan[dayIndex%7]=null），再經手帳來回重繪地圖。"""
    pg.evaluate("""() => { try { S.weekPlan[weekdayIdx2()] = null; } catch(e){}
      return true; }""".replace("weekdayIdx2()", "S.dayIndex % 7"))
    open_journal(pg)
    pg.wait_for_timeout(600)
    click_first(pg, ["返回地圖"], 900)
    pg.wait_for_timeout(900)
    dismiss_enc3(pg)
    return pg.evaluate(STATE_JS)

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
            pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
            new_game(pg, confirm_plan=False)
            pg.wait_for_timeout(600)
            click_text(pg, "確定本週行程", scope="#nb-actions", wait=1200)
            pg.wait_for_timeout(600)
            click_text(pg, "確定出發", wait=1200)
            for _ in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                    break
            ok, steps = finish_intro(pg)
            dismiss_enc3(pg); ensure_on_map(pg)
            # ---- Part A1：soft 板幾何隨時間 ----
            pg.evaluate(SEED_DAYEND_JS, "soft")
            reset_quota(pg)
            open_journal(pg); pg.wait_for_timeout(700)
            click_first(pg, ["返回地圖"], 900); pg.wait_for_timeout(1000)
            m = poll_modal(pg, 8)
            if not m:
                click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
                m = poll_modal(pg, 15)
            rec["probes"]["b4_soft_samples"] = sample_modal(pg, 3.0) if m else None
            snap(pg, "932_i_b4_soft.png")
            if m:
                click_text(pg, "返回地圖", scope="#modal-btns", wait=1200)
                pg.wait_for_timeout(900)
            dismiss_enc3(pg); ensure_on_map(pg)
            # ---- Part A2：rest 板幾何隨時間 ----
            pg.evaluate(SEED_REST_JS)
            reset_quota(pg)
            open_journal(pg); pg.wait_for_timeout(700)
            click_first(pg, ["返回地圖"], 900); pg.wait_for_timeout(1000)
            m2 = poll_modal(pg, 8)
            if not m2:
                click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
                m2 = poll_modal(pg, 15)
            rec["probes"]["b4_rest_samples"] = sample_modal(pg, 3.0) if m2 else None
            snap(pg, "932_i_b4_rest.png")
            if m2:
                click_text(pg, "返回地圖", scope="#modal-btns", wait=1500)
                pg.wait_for_timeout(1200)
            dismiss_enc3(pg); ensure_on_map(pg)
            rec["probes"]["after_rest_day"] = pg.evaluate(STATE_JS)
            # ---- Part B：B6 自由日 ----
            st = free_day(pg)
            rec["probes"]["b6_free_day_state"] = st
            clean_end = rect(pg, "#map-end-day")
            clean_hint = rect(pg, "#map-hint")
            rec["probes"]["b6_clean"] = {"end_day": clean_end, "hint": clean_hint}
            opened = None
            for attempt in range(3):
                r = open_loc(pg, "茶餐廳")
                pg.wait_for_timeout(800)
                st2 = pg.evaluate(STATE_JS)
                if st2["story"]:
                    play_story(pg, max_steps=60, tag_prefix="dlg_sheet_i")
                    dismiss_enc3(pg); ensure_on_map(pg); reset_quota(pg); continue
                if st2["enc"]:
                    dismiss_enc3(pg); ensure_on_map(pg); reset_quota(pg); continue
                opened = {"attempt": attempt, "state": st2}
                break
            rec["probes"]["b6_sheet_opened"] = opened
            if opened:
                rec["probes"]["b6_sheet_open"] = {
                    "end_day_count": pg.evaluate("() => document.querySelectorAll('#map-end-day').length"),
                    "end_day": rect(pg, "#map-end-day"), "hint": rect(pg, "#map-hint"),
                    "sheet": rect(pg, "#loc-sheet"),
                    "appScrollTop": pg.evaluate("() => document.getElementById('app').scrollTop")}
                snap(pg, "932_i_b6_sheet.png")
                close_loc(pg)
                pg.wait_for_timeout(800)
                rec["probes"]["b6_after_close"] = {"end_day": rect(pg, "#map-end-day"), "hint": rect(pg, "#map-hint")}
            dismiss_enc3(pg); ensure_on_map(pg)
            # ---- Part C：C4 過一日確認（自由日）----
            rec["probes"]["c4_before"] = pg.evaluate(STATE_JS)
            if click_text(pg, "過一日", scope="#v-map", wait=1200):
                pg.wait_for_timeout(900)
                rec["probes"]["c4_overday"] = pg.evaluate("""() => {
                  const mask = document.getElementById('mask');
                  return {btns: [...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
                    return {t:(b.textContent||'').trim(), cls:(b.className||'').toString(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; }),
                    dom_order: [...document.querySelectorAll('#modal-btns button')].map(b=>(b.textContent||'').trim()),
                    maskCls: mask?mask.className:null,
                    modal: (()=>{ const m=document.querySelector('#mask .modal'); const r=m?m.getBoundingClientRect():null;
                      return r?{x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}:null; })(),
                    title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h?(h.textContent||'').trim():null; })()}; }""")
                snap(pg, "932_i_c4_overday.png")
                click_first(pg, ["取消"], 900)
                pg.wait_for_timeout(700)
                rec["probes"]["c4_after_cancel_day"] = pg.evaluate("() => (typeof S!=='undefined' && S) ? S.dayIndex : null")
            # ---- Part D：U4 乾淨態 ----
            reset_quota(pg)
            open_loc(pg, "星河電視台")
            pg.wait_for_timeout(700)
            dismiss_enc3(pg); pg.wait_for_timeout(500)
            if click_text(pg, "通告欄", scope="#loc-acts", wait=1500):
                pg.wait_for_timeout(900)
                pg.evaluate("""() => { const card=[...document.querySelectorAll('#modal-inner .gig-card, #modal-inner .gig-teaser')].find(e=>e.offsetParent!==null);
                  if (card) card.click(); }""")
                pg.wait_for_timeout(1200)
                rec["probes"]["u2_detail_again"] = {"btns": modal_btns(pg)}
                click_first(pg, ["離開"], 900); pg.wait_for_timeout(800)
                # 通告欄 modal 用「返去地點」閂
                closed = click_first(pg, ["返去地點"], 900); pg.wait_for_timeout(800)
                rec["probes"]["u4_close_giglist"] = {"clicked_back": closed, "state": pg.evaluate(STATE_JS)}
            close_loc(pg)
            dismiss_enc3(pg); ensure_on_map(pg)
            pg.wait_for_timeout(600)
            pre = {"state": pg.evaluate(STATE_JS),
                "locTitle": pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }"),
                "hint": pg.evaluate("() => { const h=document.getElementById('map-hint'); return h?(h.textContent||'').trim().slice(0,90):null; }"),
                "toast": pg.evaluate("() => (document.getElementById('toast')||{}).textContent || ''"),
                "used": pg.evaluate("() => (S.travel114||{}).used")}
            pg.evaluate("""() => { try { S.travel114 = {used:2, day:S.dayIndex}; return true; } catch(e){ return String(e); } }""")
            pg.wait_for_timeout(400)
            open_loc(pg, "星河電視台")
            pg.wait_for_timeout(1000)
            post = {"state": pg.evaluate(STATE_JS),
                "locTitle": pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }"),
                "hint": pg.evaluate("() => { const h=document.getElementById('map-hint'); return h?(h.textContent||'').trim().slice(0,90):null; }"),
                "toast": pg.evaluate("() => (document.getElementById('toast')||{}).textContent || ''"),
                "used": pg.evaluate("() => (S.travel114||{}).used")}
            rec["probes"]["u4_quota"] = {"before": pre, "after": post}
            snap(pg, "932_i_u4.png")
            dismiss_enc3(pg); ensure_on_map(pg)
            # ---- Part E：B1 hunt（自由日推進，daily gate 過嘅日子優先）----
            enc = None
            hunt_log = []
            for _n in range(5):
                if enc: break
                day = pg.evaluate("() => (typeof S!=='undefined' && S) ? S.dayIndex : null")
                if day is None: break
                st = pg.evaluate(STATE_JS)
                if st["enc"]:
                    enc = measure_enc(pg)
                    if enc:
                        enc["via"] = "morning_pending"; enc["day"] = day
                        snap(pg, "932_i_b1_enc.png")
                        hunt_log.append({"day": day, "via": "morning_pending", "fired": True})
                        break
                plan = day_plan(day)
                entry = {"day": day, "plan": {str(k): (NAME[v] if v else None) for k, v in plan.items()},
                         "daily_gate": round(wf4rand(f"wf4day:{day}"), 4)}
                for t in (1, 2, 3):
                    if enc: break
                    loc = plan.get(t)
                    if not loc: continue
                    reset_quota(pg)
                    open_loc(pg, NAME[loc])
                    pg.wait_for_timeout(700)
                    st2 = pg.evaluate(STATE_JS)
                    entry[f"try{t}_{NAME[loc]}"] = {"enc": st2["enc"], "story": st2["story"], "sheet": st2["locSheet"]}
                    if st2["enc"]:
                        enc = measure_enc(pg)
                        if enc:
                            enc["via"] = f"loc_try{t}"; enc["loc"] = NAME[loc]; enc["day"] = day
                            snap(pg, "932_i_b1_enc.png")
                        break
                    if st2["story"]:
                        play_story(pg, max_steps=40, tag_prefix="dlg_hunt_i")
                    if st2["locSheet"]:
                        close_loc(pg)
                    dismiss_enc3(pg); ensure_on_map(pg)
                hunt_log.append(entry)
                if enc: break
                # 自由日推進：清今日格 → 過一日 → 確認
                free_day(pg)
                if click_text(pg, "過一日", scope="#v-map", wait=1200):
                    pg.wait_for_timeout(800)
                    click_first(pg, ["確定過一日"], 900)
                    pg.wait_for_timeout(1500)
                    dismiss_enc3(pg); ensure_on_map(pg)
                else:
                    hunt_log.append({"advance_failed_day": day})
                    break
            rec["probes"]["b1_hunt_log"] = hunt_log
            rec["probes"]["b1_encounter"] = enc
            rec["probes"]["pageerrors"] = errs[:10]
            rec["zero_pageerror"] = len(errs) == 0
            ctx.close(); b.close()
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
    finally:
        stop(srv)
    out = json.load(open(os.path.join(OUT, "drive197.json"), encoding="utf-8"))
    out.setdefault("final5_runs", {})["932i"] = rec
    with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("== FINAL5 932i DONE ==", flush=True)

if __name__ == "__main__":
    main()
