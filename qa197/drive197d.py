# -*- coding: utf-8 -*-
"""v20a197 最終重點探針（932／700）：U6 直 call、B7 播完 intro 再量、B4 經「開始今日行程」、
C3／B5 乾淨 sheet、B1 跨日搵巧遇、U2 撳卡片、U4（#toast＋locTitle＋quota）。
用法：/home/hatch/pwenv49/bin/python qa197/drive197d.py [932|700]
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (OUT, SHOTS, URL, EXE, serve, stop, snap, census, rect,
                      modal_btns, click_text, click_first, dismiss_enc3, play_story,
                      new_game, ensure_on_map, open_loc, close_loc, open_journal,
                      SEED_DAYEND_JS, SEED_REST_JS, STATE_JS, wait_for_S, finish_intro)
from playwright.sync_api import sync_playwright

def reset_quota(pg):
    return pg.evaluate("""() => { try { S.travel114 = {used:0, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")

def continue_if_title(pg):
    st = pg.evaluate(STATE_JS)
    if st["mapVisible"]:
        return "already_map"
    ok = click_text(pg, "繼續", wait=1500)
    pg.wait_for_timeout(800)
    return "clicked_continue" if ok else "no_continue_btn"

def poll_modal(pg, secs=15):
    for _ in range(int(secs * 2)):
        m = pg.evaluate("""() => {
          const btns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null);
          if (!btns.length) return null;
          const mask=document.getElementById('mask');
          const modalEl = document.querySelector('#mask .modal') || document.querySelector('.modal');
          const r = modalEl ? modalEl.getBoundingClientRect() : null;
          return {maskCls: mask?mask.className:null,
            modalH: r?Math.round(r.height):null, modalY: r?Math.round(r.top):null, modalX: r?Math.round(r.left):null, modalW: r?Math.round(r.width):null,
            title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h?(h.textContent||'').trim():null; })(),
            btns: btns.map(b=>{ const rr=b.getBoundingClientRect();
              return {t:(b.textContent||'').trim().slice(0,16), cls:(b.className||'').toString(), x:Math.round(rr.left), y:Math.round(rr.top), w:Math.round(rr.width), h:Math.round(rr.height)}; })}; }""")
        if m:
            return m
        pg.wait_for_timeout(500)
    return None

def run(pw, H, label):
    print(f"===== FINAL {label} =====", flush=True)
    rec = {"height": H, "probes": {}, "notes": []}
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        if not new_game(pg, confirm_plan=False):
            rec["notes"].append("new_game FAILED"); return rec
        pg.wait_for_timeout(600)
        # ---- U6 直 call：homeEditable＋openCopyFromDay(0)＋toast ----
        rec["probes"]["u6_direct"] = pg.evaluate("""() => {
          const out = {homeEditable: (typeof S!=='undefined' && S) ? S.homeEditable : null,
            planSelDay: (typeof planSelDay!=='undefined') ? planSelDay : 'undef',
            toastBefore: (document.getElementById('toast')||{}).textContent || ''};
          try { openCopyFromDay(0); } catch(e){ out.err = String(e); }
          const w=document.getElementById('nb-copy-wrap');
          out.after = {panelOpen: w?w.classList.contains('open'):null, panelDisplay: w?getComputedStyle(w).display:null,
            selDay: (typeof planSelDay!=='undefined') ? planSelDay : 'undef',
            toastAfter: (document.getElementById('toast')||{}).textContent || ''};
          out.dayLocked = [];
          try { for(let i=0;i<7;i++) out.dayLocked.push(dayPlanLocked(planDraft && planDraft[i])); } catch(e){ out.dayLockedErr=String(e); }
          return out; }""")
        pg.wait_for_timeout(500)
        # 快捷列嗰組做對照
        rec["probes"]["u6_quick_direct"] = pg.evaluate("""() => {
          try { toggleCopyPanel(false); } catch(e){}
          const q=document.getElementById('nb-q-copy'); if (q) q.click();
          const w=document.getElementById('nb-copy-wrap');
          return {panelOpen: w?w.classList.contains('open'):null, panelDisplay: w?getComputedStyle(w).display:null,
            selDay: (typeof planSelDay!=='undefined') ? planSelDay : 'undef'}; }""")
        pg.evaluate("() => { try { toggleCopyPanel(false); } catch(e){} return true; }")
        # ---- 確認＋播 intro ----
        click_text(pg, "確定本週行程", scope="#nb-actions", wait=1200)
        pg.wait_for_timeout(600)
        click_text(pg, "確定出發", wait=1200)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        ok, steps = finish_intro(pg)
        rec["probes"]["intro_finished"] = ok
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- B7 播完 intro 再入行手帳：elementFromPoint＋真 click ----
        open_journal(pg)
        pg.wait_for_timeout(700)
        rec["probes"]["b7_post_intro"] = pg.evaluate("""() => {
          const tabs = document.getElementById('cat-tabs');
          const nb = document.getElementById('notebook');
          if (!tabs) return {found:false};
          const bar = document.getElementById('nb-actions');
          const br = bar ? bar.getBoundingClientRect() : null;
          return {scrollTop: nb?nb.scrollTop:null,
            barTop: br?Math.round(br.top):null,
            tabs: [...tabs.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>{
              const r=x.getBoundingClientRect(); const cx=r.left+r.width/2, cy=r.top+r.height/2;
              const hit=document.elementFromPoint(cx, cy);
              return {t:(x.textContent||'').trim(), y:Math.round(r.top), bottom:Math.round(r.bottom),
                hitIsBtn: hit===x, hitCls: hit?(hit.className||'').toString().slice(0,40):null}; })}; }""")
        before_on = pg.evaluate("() => { const o=document.querySelector('#cat-tabs button.on'); return o?(o.textContent||'').trim():null; }")
        tab = pg.evaluate("""() => { const x=[...document.querySelectorAll('#cat-tabs button')].find(b=>(b.textContent||'').includes('工作'));
          if(!x) return null; const r=x.getBoundingClientRect(); return {x:r.left+r.width/2, y:r.top+r.height/2}; }""")
        if tab:
            pg.mouse.click(tab["x"], tab["y"]); pg.wait_for_timeout(900)
        after_on = pg.evaluate("() => { const o=document.querySelector('#cat-tabs button.on'); return o?(o.textContent||'').trim():null; }")
        rec["probes"]["b7_post_intro_click"] = {"before_on": before_on, "tab": tab, "after_on": after_on}
        snap(pg, f"{label}_d_b7_journal.png")
        click_first(pg, ["返回地圖"], 900)
        pg.wait_for_timeout(800)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- B4 soft：seed → reload → 繼續 → 開始今日行程 ----
        pg.evaluate(SEED_DAYEND_JS, "soft")
        pg.evaluate("""() => { try { S.travel114 = {used:0, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        rec["probes"]["b4_seed_state"] = pg.evaluate("""() => ({dayIndex: S.dayIndex,
          weekPlan: S.weekPlan, shoots: (S.shoots||[]).map(x=>({id:x.id, doneDays:x.doneDays, totalDays:x.totalDays})),
          todayPlan: (typeof todayPlanId==='function') ? todayPlanId() : null})""")
        rec["probes"]["b4_reload"] = {"continued": continue_if_title(pg), "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg); ensure_on_map(pg)
        rec["probes"]["b4_map_btns"] = pg.evaluate("""() => ({
          startToday: (()=>{ const e=document.getElementById('map-start-today'); if(!e) return null;
            const r=e.getBoundingClientRect(); return {t:(e.textContent||'').trim(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), vis:e.offsetParent!==null}; })(),
          endDay: (()=>{ const e=document.getElementById('map-end-day'); if(!e) return null;
            const r=e.getBoundingClientRect(); return {t:(e.textContent||'').trim(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), vis:e.offsetParent!==null}; })(),
          todayPlan: (typeof todayPlanId==='function') ? todayPlanId() : null})""")
        st_ok = click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
        rec["probes"]["b4_start_clicked"] = st_ok
        modal = poll_modal(pg, 15)
        rec["probes"]["b4_soft"] = modal
        snap(pg, f"{label}_d_b4_soft.png")
        if modal and click_text(pg, "返回地圖", scope="#modal-btns", wait=1200):
            pg.wait_for_timeout(900)
            rec["probes"]["b4_soft_after_back"] = pg.evaluate(STATE_JS)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- B4 rest：seed → reload → 繼續 → 開始今日行程 ----
        pg.evaluate(SEED_REST_JS)
        pg.evaluate("""() => { try { S.travel114 = {used:0, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        rec["probes"]["b4_rest_reload"] = {"continued": continue_if_title(pg), "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg); ensure_on_map(pg)
        rec["probes"]["b4_rest_map_btns"] = pg.evaluate("""() => ({
          startToday: (()=>{ const e=document.getElementById('map-start-today'); if(!e) return null;
            const r=e.getBoundingClientRect(); return {t:(e.textContent||'').trim(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), vis:e.offsetParent!==null}; })(),
          todayPlan: (typeof todayPlanId==='function') ? todayPlanId() : null})""")
        st_ok2 = click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
        rec["probes"]["b4_rest_start_clicked"] = st_ok2
        modal2 = poll_modal(pg, 15)
        rec["probes"]["b4_rest"] = modal2
        snap(pg, f"{label}_d_b4_rest.png")
        if modal2:
            ok2 = click_text(pg, "返回地圖", scope="#modal-btns", wait=1500)
            pg.wait_for_timeout(1200)
            rec["probes"]["u1_rest_back"] = {"clicked": ok2, "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- C3／B5／B6 乾淨 sheet：開地點，有故事／巧遇就清咗佢再開 ----
        reset_quota(pg)
        clean = None
        for attempt in range(3):
            r = open_loc(pg, "茶餐廳")
            pg.wait_for_timeout(800)
            st = pg.evaluate(STATE_JS)
            if st["story"]:
                play_story(pg, max_steps=60, tag_prefix="dlg_sheet2")
                dismiss_enc3(pg); ensure_on_map(pg); reset_quota(pg); continue
            if st["enc"]:
                dismiss_enc3(pg); ensure_on_map(pg); reset_quota(pg); continue
            clean = {"attempt": attempt, "open_loc": r, "state": st}
            break
        rec["probes"]["sheet_clean"] = clean
        if clean:
            rec["probes"]["b6_sheet_open"] = {
                "end_day": rect(pg, "#map-end-day"), "hint": rect(pg, "#map-hint"),
                "sheet": rect(pg, "#loc-sheet"),
                "appScrollTop": pg.evaluate("() => document.getElementById('app').scrollTop")}
            rec["probes"]["c3_acts"] = pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet .act')]
              .filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
                return {t:(b.textContent||'').trim().slice(0,24), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; })""")
            rec["probes"]["b5_loc_close"] = pg.evaluate("""() => { const b=document.getElementById('loc-close');
              if (!b) return {found:false};
              const r=b.getBoundingClientRect();
              return {tag:b.tagName, offsetW:b.offsetWidth, offsetH:b.offsetHeight,
                bbox:{x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)},
                text:(b.textContent||'').trim()}; }""")
            rec["probes"]["loc_title"] = pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }")
            snap(pg, f"{label}_d_sheet.png")
            close_loc(pg)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- B1 跨日搵巧遇 ----
        enc = None
        for day in range(6):
            if enc: break
            for loc in ["茶餐廳", "星河電視台", "廟街", "清水灣片場"]:
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
                    snap(pg, f"{label}_d_b1_enc.png")
                    before = enc["line"] if enc else ""
                    pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                      const nb=[...ov.querySelectorAll('.e79-btn:not(.e79-choice)')].find(x=>x.offsetParent!==null);
                      if (nb) nb.click(); }""")
                    pg.wait_for_timeout(900)
                    after = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                      return ov ? ((ov.querySelector('.e79-line')||{}).textContent||'').slice(0,30) : 'CLOSED'; }""")
                    enc["advance"] = {"before": before, "after": after, "advanced": before != after}
                    enc["loc"] = loc; enc["day"] = day
                    break
                if st["story"]:
                    play_story(pg, max_steps=40, tag_prefix="dlg_enchunt")
                if st["locSheet"]:
                    close_loc(pg)
                dismiss_enc3(pg); ensure_on_map(pg)
            if enc: break
            # 過一日去下一日
            if click_text(pg, "過一日", scope="#v-map", wait=1200):
                pg.wait_for_timeout(900)
                click_first(pg, ["確定過一日", "確定"], 900)
                pg.wait_for_timeout(1500)
                dismiss_enc3(pg); ensure_on_map(pg)
            else:
                break
        rec["probes"]["b1_encounter"] = enc
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- U2：通告板 → 撳第一張卡 ----
        reset_quota(pg)
        open_loc(pg, "星河電視台")
        pg.wait_for_timeout(700)
        dismiss_enc3(pg)
        pg.wait_for_timeout(500)
        if click_text(pg, "通告欄", scope="#loc-acts", wait=1500):
            pg.wait_for_timeout(900)
            opened = pg.evaluate("""() => {
              const card=[...document.querySelectorAll('#modal-inner .gig-card, #modal-inner .gig-teaser')].find(e=>e.offsetParent!==null);
              if (!card) return null;
              card.click();
              return {cls:(card.className||'').toString().slice(0,40), text:(card.textContent||'').trim().slice(0,30)}; }""")
            pg.wait_for_timeout(1200)
            rec["probes"]["u2_detail"] = {"opened": opened,
                "state": pg.evaluate(STATE_JS),
                "census": census(pg, "casting_detail")}
            snap(pg, f"{label}_d_u2_detail.png")
            click_first(pg, ["返回", "關閉"], 900)
            pg.wait_for_timeout(800)
            click_first(pg, ["返去地點", "返回地圖"], 900)
            pg.wait_for_timeout(800)
        close_loc(pg)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- U4：額度擋 TVB（#toast＋locTitle＋hint）----
        reset_quota(pg)
        ensure_on_map(pg)
        pg.evaluate("""() => { try { S.travel114 = {used:2, day:S.dayIndex}; saveQ(); return true; } catch(e){ return String(e); } }""")
        pg.wait_for_timeout(400)
        before = {"state": pg.evaluate(STATE_JS),
            "locTitle": pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }"),
            "hint": pg.evaluate("() => { const h=document.getElementById('map-hint'); return h?(h.textContent||'').trim().slice(0,80):null; }"),
            "toast": pg.evaluate("() => (document.getElementById('toast')||{}).textContent || ''")}
        open_loc(pg, "星河電視台")
        pg.wait_for_timeout(1000)
        after = {"state": pg.evaluate(STATE_JS),
            "locTitle": pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }"),
            "hint": pg.evaluate("() => { const h=document.getElementById('map-hint'); return h?(h.textContent||'').trim().slice(0,80):null; }"),
            "toast": pg.evaluate("() => (document.getElementById('toast')||{}).textContent || ''"),
            "used": pg.evaluate("() => (S.travel114||{}).used")}
        rec["probes"]["u4_quota"] = {"before": before, "after": after}
        dismiss_enc3(pg); ensure_on_map(pg)
        rec["probes"]["pageerrors"] = errs[:10]
        rec["zero_pageerror"] = len(errs) == 0
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
        try: snap(pg, f"{label}_d_ERR.png")
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
        out.setdefault("final_runs", {})[label] = rec
        with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f"== FINAL {label} DONE ==", flush=True)
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
