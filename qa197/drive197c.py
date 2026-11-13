# -*- coding: utf-8 -*-
"""v20a197 診斷＋重點重驗（932／700）：reload 行為、B7 遮擋 DIV、U6 逐日複製、
地點 sheet（C3／B5）、B1 巧遇（quota reset）、C6、U4、B4 soft／rest、U1、C2／C4。
用法：/home/hatch/pwenv49/bin/python qa197/drive197c.py [932|700]
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (ROOT, OUT, SHOTS, URL, EXE, serve, stop, snap, census, rect,
                      modal_btns, click_text, click_first, dismiss_enc3, play_story,
                      new_game, ensure_on_map, open_loc, close_loc, open_journal,
                      SEED_DAYEND_JS, SEED_REST_JS, STATE_JS, wait_for_S, finish_intro)
from playwright.sync_api import sync_playwright

def vis_btns(pg, n=14):
    return pg.evaluate("""(n) => [...document.querySelectorAll('button')]
      .filter(b=>b.offsetParent!==null).slice(0,n).map(b=>{ const r=b.getBoundingClientRect();
        return {t:(b.textContent||'').trim().slice(0,24), id:b.id||'', x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; })""", n)

def reset_quota(pg):
    return pg.evaluate("""() => { try { S.travel114 = {used:0, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")

def continue_if_title(pg):
    st = pg.evaluate(STATE_JS)
    if st["mapVisible"]:
        return "already_map"
    ok = click_text(pg, "繼續", wait=1500)
    pg.wait_for_timeout(800)
    return "clicked_continue" if ok else "no_continue_btn"

def run(pw, H, label):
    print(f"===== DIAG {label} =====", flush=True)
    rec = {"height": H, "probes": {}, "notes": []}
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        # ---- Phase A：開局＋journal（可編輯態）----
        if not new_game(pg, confirm_plan=False):
            rec["notes"].append("new_game FAILED"); return rec
        pg.wait_for_timeout(600)
        # B7：遮擋 DIV 真身＋真 mouse click
        rec["probes"]["b7_hitchain"] = pg.evaluate("""() => {
          const tabs = document.getElementById('cat-tabs');
          if (!tabs) return {found:false};
          return [...tabs.querySelectorAll('button')].filter(x=>x.offsetParent!==null).slice(0,2).map(x=>{
            const r=x.getBoundingClientRect(); const cx=r.left+r.width/2, cy=r.top+r.height/2;
            const hit=document.elementFromPoint(cx, cy);
            const chain=[]; let el=hit;
            while (el && chain.length<6) { const rr=el.getBoundingClientRect();
              chain.push({tag:el.tagName, id:el.id||'', cls:(el.className||'').toString().slice(0,60),
                pe:getComputedStyle(el).pointerEvents, x:Math.round(rr.left), y:Math.round(rr.top), w:Math.round(rr.width), h:Math.round(rr.height)});
              el=el.parentElement; }
            return {t:(x.textContent||'').trim(), hitIsBtn: hit===x, chain}; }); }""")
        # 真 mouse click：撳「工作」分類掣中心，睇下 .on 會唔會轉過去
        before_on = pg.evaluate("() => { const o=document.querySelector('#cat-tabs button.on'); return o?(o.textContent||'').trim():null; }")
        tab = pg.evaluate("""() => { const x=[...document.querySelectorAll('#cat-tabs button')].find(b=>(b.textContent||'').includes('工作'));
          if(!x) return null; const r=x.getBoundingClientRect(); return {x:r.left+r.width/2, y:r.top+r.height/2}; }""")
        clicked = False
        if tab:
            pg.mouse.click(tab["x"], tab["y"]); pg.wait_for_timeout(900); clicked = True
        after_on = pg.evaluate("() => { const o=document.querySelector('#cat-tabs button.on'); return o?(o.textContent||'').trim():null; }")
        rec["probes"]["b7_real_click"] = {"before_on": before_on, "tab": tab, "clicked": clicked, "after_on": after_on}
        # U6：逐粒 .day-row .cp 試
        u6 = []
        n_cp = pg.evaluate("() => document.querySelectorAll('.day-row .cp').length")
        for i in range(n_cp):
            r = pg.evaluate("""(i) => {
              const cps=[...document.querySelectorAll('.day-row .cp')];
              const cp=cps[i]; if(!cp) return null;
              const row=cp.closest('.day-row');
              const locked = row ? row.classList.contains('locked') : null;
              const dayName = row ? (row.textContent||'').slice(0,12) : '';
              cp.click();
              const w=document.getElementById('nb-copy-wrap');
              const toast=[...document.querySelectorAll('.toast, #toast')].filter(e=>e.offsetParent!==null).map(e=>(e.textContent||'').trim()).slice(0,2);
              return {i, dayName, locked, panelOpen: w?w.classList.contains('open'):null,
                panelDisplay: w?getComputedStyle(w).display:null, selDay:(typeof planSelDay!=='undefined')?planSelDay:null, toast}; }""", i)
            pg.wait_for_timeout(500)
            if r: u6.append(r)
            pg.evaluate("() => { try { toggleCopyPanel(false); } catch(e){} return true; }")
            pg.wait_for_timeout(300)
        rec["probes"]["u6_per_day"] = u6
        # ---- Phase B：確認＋出發＋intro 診斷 ----
        click_text(pg, "確定本週行程", scope="#nb-actions", wait=1200)
        pg.wait_for_timeout(600)
        dep_ok = click_text(pg, "確定出發", wait=1500)
        rec["probes"]["depart"] = {"clicked": dep_ok, "state": pg.evaluate(STATE_JS), "vis": vis_btns(pg)}
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        rec["probes"]["after_confirm_loop"] = {"state": pg.evaluate(STATE_JS), "vis": vis_btns(pg)}
        ok, steps = finish_intro(pg)
        rec["probes"]["intro_finished"] = ok
        rec["probes"]["b1_mainline"] = [
            {"step": s["step"], "kind": s["kind"],
             "next": [x for x in s["census"]["buttons"] if "下一句" in x["text"]][:2],
             "choices": [x for x in s["census"]["buttons"] if "sp-choice" in x["cls"]][:3]}
            for s in steps[:8]]
        rec["probes"]["after_intro"] = {"state": pg.evaluate(STATE_JS), "vis": vis_btns(pg)}
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- Phase C：B6＋C3＋B5（播晒故事先量 sheet）----
        reset_quota(pg)
        r = open_loc(pg, "茶餐廳")
        pg.wait_for_timeout(700)
        st = pg.evaluate(STATE_JS)
        story_played = False
        if st["story"]:
            story_played = True
            play_story(pg, max_steps=60, tag_prefix="dlg_tea2")
            dismiss_enc3(pg); ensure_on_map(pg)
            reset_quota(pg)
            r = open_loc(pg, "茶餐廳")
            pg.wait_for_timeout(900)
        st = pg.evaluate(STATE_JS)
        rec["probes"]["sheet_state"] = {"open_loc": r, "story_played": story_played, "state": st}
        # 將 sheet 捲入 viewport（如果佢喺下面）
        pg.evaluate("""() => { const s=document.getElementById('loc-sheet');
          if (s) s.scrollIntoView({block:'end'}); return true; }""")
        pg.wait_for_timeout(600)
        rec["probes"]["b6_sheet_open"] = {
            "end_day": rect(pg, "#map-end-day"), "hint": rect(pg, "#map-hint"),
            "sheet": rect(pg, "#loc-sheet"),
            "appScrollTop": pg.evaluate("() => document.getElementById('app').scrollTop"),
            "wrapScrollTop": pg.evaluate("() => { const w=document.querySelector('.map-wrap'); return w ? w.scrollTop : null; }")}
        rec["probes"]["b5_loc_close"] = pg.evaluate("""() => { const b=document.getElementById('loc-close');
          if (!b) return {found:false};
          const r=b.getBoundingClientRect();
          return {tag:b.tagName, offsetW:b.offsetWidth, offsetH:b.offsetHeight,
            bbox:{x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)},
            text:(b.textContent||'').trim()}; }""")
        rec["probes"]["c3_acts"] = pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet .act')]
          .filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
            return {t:(b.textContent||'').trim().slice(0,20), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; })""")
        snap(pg, f"{label}_c_sheet.png")
        close_loc(pg)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- Phase D：B1 巧遇（每次 reset 額度）----
        enc = None
        for loc in ["茶餐廳", "星河電視台", "廟街", "清水灣片場", "啟德機場", "中環", "尖沙咀", "旺角", "銅鑼灣", "油麻地", "九龍城", "深水埗"]:
            reset_quota(pg)
            r = open_loc(pg, loc)
            pg.wait_for_timeout(700)
            st = pg.evaluate(STATE_JS)
            if st["enc"]:
                enc = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                  if (!ov) return null;
                  const nb=[...ov.querySelectorAll('.e79-btn:not(.e79-choice)')].find(x=>x.offsetParent!==null);
                  const r=nb?nb.getBoundingClientRect():null;
                  const line=(ov.querySelector('.e79-line')||{}).textContent||'';
                  return {nb: r?{x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height),
                    offsetW: nb.offsetWidth, offsetH: nb.offsetHeight, text:(nb.textContent||'').trim()} : null,
                    line: line.slice(0,30)}; }""")
                snap(pg, f"{label}_c_b1_enc.png")
                before = enc["line"] if enc else ""
                pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                  const nb=[...ov.querySelectorAll('.e79-btn:not(.e79-choice)')].find(x=>x.offsetParent!==null);
                  if (nb) nb.click(); }""")
                pg.wait_for_timeout(900)
                after = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                  return ov ? ((ov.querySelector('.e79-line')||{}).textContent||'').slice(0,30) : 'CLOSED'; }""")
                enc["advance"] = {"before": before, "after": after, "advanced": before != after}
                enc["loc"] = loc
                break
            if st["story"]:
                play_story(pg, max_steps=40, tag_prefix="dlg_encloc2")
            if st["locSheet"]:
                close_loc(pg)
            dismiss_enc3(pg); ensure_on_map(pg)
        rec["probes"]["b1_encounter"] = enc
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- Phase E：C6 通告板 ----
        reset_quota(pg)
        open_loc(pg, "星河電視台")
        pg.wait_for_timeout(700)
        dismiss_enc3(pg)
        pg.wait_for_timeout(500)
        if click_text(pg, "通告欄", scope="#loc-acts", wait=1500):
            pg.wait_for_timeout(900)
            rec["probes"]["c6_board"] = pg.evaluate("""() => {
              const cards=[...document.querySelectorAll('#modal-inner .gig-teaser, #modal-inner .gig-card')].filter(e=>e.offsetParent!==null)
                .map(e=>{ const r=e.getBoundingClientRect(); return {y:Math.round(r.top), bottom:Math.round(r.bottom), h:Math.round(r.height)}; });
              const det=document.querySelector('#modal-inner details.gig-locked108');
              const sum=det?det.querySelector('summary'):null;
              const sr=sum?sum.getBoundingClientRect():null;
              const scs=sum?getComputedStyle(sum):null;
              return {cards, n: cards.length,
                gaps: cards.slice(1).map((c,i)=>Math.round(c.y-cards[i].bottom)),
                summary: sr?{x:Math.round(sr.left), y:Math.round(sr.top), w:Math.round(sr.width), h:Math.round(sr.height),
                  bg: scs.backgroundColor, fontSize: scs.fontSize, fontWeight: scs.fontWeight,
                  text:(sum.textContent||'').trim().slice(0,44)} : null}; }""")
            snap(pg, f"{label}_c_c6_board.png")
            opened = pg.evaluate("""() => {
              const cards = [...document.querySelectorAll('#modal-inner button')].filter(b=>b.offsetParent!==null && (b.textContent||'').includes('可接通告'));
              if (!cards.length) return null;
              cards[0].click(); return (cards[0].textContent||'').trim().slice(0,30); }""")
            pg.wait_for_timeout(1200)
            rec["probes"]["u2_detail"] = {"opened": opened, "census": census(pg, "casting_detail")}
            snap(pg, f"{label}_c_u2_detail.png")
            click_first(pg, ["返回", "關閉"], 900)
            pg.wait_for_timeout(800)
            click_first(pg, ["返去地點", "返回地圖"], 900)
            pg.wait_for_timeout(800)
        close_loc(pg)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- Phase F：U4 額度擋 TVB ----
        reset_quota(pg)
        ensure_on_map(pg)
        pg.evaluate("""() => { try { S.travel114 = {used:2, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")
        pg.wait_for_timeout(400)
        before = pg.evaluate(STATE_JS)
        toast_before = pg.evaluate("() => [...document.querySelectorAll('.toast, #toast')].filter(e=>e.offsetParent!==null).map(e=>(e.textContent||'').trim())")
        open_loc(pg, "星河電視台")
        pg.wait_for_timeout(900)
        after = pg.evaluate(STATE_JS)
        toast_after = pg.evaluate("() => [...document.querySelectorAll('.toast, #toast')].filter(e=>e.offsetParent!==null).map(e=>(e.textContent||'').trim())")
        rec["probes"]["u4_quota"] = {"before": before, "after": after,
            "sheet_opened": after["locSheet"], "locTitle": after["locTitle"],
            "toast_before": toast_before, "toast_after": toast_after}
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- Phase G：B4 soft 日結 ----
        pg.evaluate(SEED_DAYEND_JS, "soft")
        pg.evaluate("""() => { try { S.travel114 = {used:0, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        rec["probes"]["b4_reload"] = {"continued": continue_if_title(pg), "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg); ensure_on_map(pg)
        reset_quota(pg)
        open_loc(pg, "茶餐廳")
        pg.wait_for_timeout(700)
        st = pg.evaluate(STATE_JS)
        if st["story"]:
            play_story(pg, max_steps=40, tag_prefix="dlg_dayend2")
        close_loc(pg)
        # 等日結 modal（poll 12 秒）
        modal = None
        for _ in range(24):
            pg.wait_for_timeout(500)
            m = pg.evaluate("""() => {
              const btns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null);
              if (!btns.length) return null;
              const mask=document.getElementById('mask');
              const modalEl = document.querySelector('#mask .modal') || document.querySelector('.modal');
              const r = modalEl ? modalEl.getBoundingClientRect() : null;
              return {maskCls: mask?mask.className:null,
                modalH: r?Math.round(r.height):null, modalY: r?Math.round(r.top):null,
                title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h?(h.textContent||'').trim():null; })(),
                btns: btns.map(b=>{ const rr=b.getBoundingClientRect();
                  return {t:(b.textContent||'').trim().slice(0,16), x:Math.round(rr.left), y:Math.round(rr.top), w:Math.round(rr.width), h:Math.round(rr.height)}; })}; }""")
            if m:
                modal = m; break
        rec["probes"]["b4_soft"] = modal
        snap(pg, f"{label}_c_b4_soft.png")
        if modal and click_text(pg, "返回地圖", scope="#modal-btns", wait=1200):
            pg.wait_for_timeout(900)
            rec["probes"]["b4_soft_after_back"] = pg.evaluate(STATE_JS)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- Phase H：B4 rest 日結（U1）----
        pg.evaluate(SEED_REST_JS)
        pg.evaluate("""() => { try { S.travel114 = {used:0, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        rec["probes"]["b4_rest_reload"] = {"continued": continue_if_title(pg), "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg); ensure_on_map(pg)
        if click_text(pg, "開始今日行程", scope="#v-map", wait=1200):
            pg.wait_for_timeout(1200)
            modal2 = None
            for _ in range(12):
                m = pg.evaluate("""() => {
                  const btns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null);
                  if (!btns.length) return null;
                  const modalEl = document.querySelector('#mask .modal') || document.querySelector('.modal');
                  const r = modalEl ? modalEl.getBoundingClientRect() : null;
                  return {modalH: r?Math.round(r.height):null, modalY: r?Math.round(r.top):null,
                    title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h?(h.textContent||'').trim():null; })(),
                    btns: btns.map(b=>{ const rr=b.getBoundingClientRect();
                      return {t:(b.textContent||'').trim().slice(0,16), x:Math.round(rr.left), y:Math.round(rr.top), w:Math.round(rr.width), h:Math.round(rr.height)}; })}; }""")
                if m:
                    modal2 = m; break
                pg.wait_for_timeout(500)
            rec["probes"]["b4_rest"] = modal2
            snap(pg, f"{label}_c_b4_rest.png")
            ok = click_text(pg, "返回地圖", scope="#modal-btns", wait=1500)
            pg.wait_for_timeout(1200)
            rec["probes"]["u1_rest_back"] = {"clicked": ok, "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- Phase I：C2／C4 過一日確認 ----
        pg.evaluate("""() => { try { S.weekPlan = S.weekPlan || []; for(let i=0;i<7;i++) S.weekPlan[i]='rest'; S.homeEditable=false; S.travel114={used:0, day:S.dayIndex}; saveQ(); } catch(e){} return true; }""")
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        continue_if_title(pg)
        dismiss_enc3(pg); ensure_on_map(pg)
        rec["probes"]["c2_end_day"] = {"end_day": rect(pg, "#map-end-day"), "start_today": rect(pg, "#map-start-today")}
        if click_text(pg, "過一日", scope="#v-map", wait=1200):
            pg.wait_for_timeout(900)
            rec["probes"]["c4_overday"] = {"btns": modal_btns(pg), "title": pg.evaluate(STATE_JS)["title"],
                "dom_order": pg.evaluate("() => [...document.querySelectorAll('#modal-btns button')].map(b=>(b.textContent||'').trim())")}
            snap(pg, f"{label}_c_c4_overday.png")
            click_first(pg, ["取消", "唔好", "返回"], 900)
            pg.wait_for_timeout(700)
        rec["probes"]["pageerrors"] = errs[:10]
        rec["zero_pageerror"] = len(errs) == 0
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
        try: snap(pg, f"{label}_c_ERR.png")
        except Exception: pass
    finally:
        ctx.close(); b.close()
    return rec

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "932"
    H = int(which)
    label = which
    srv = serve()
    try:
        with sync_playwright() as pw:
            rec = run(pw, H, label)
        out = json.load(open(os.path.join(OUT, "drive197.json"), encoding="utf-8"))
        out.setdefault("diag_runs", {})[label] = rec
        with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f"== DIAG {label} DONE ==", flush=True)
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
