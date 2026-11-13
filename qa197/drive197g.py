# -*- coding: utf-8 -*-
"""v20a197 最終驗證輪（932／700）：B4 in-memory seed 唔 reload、U6 UI 驅動合成態、
B7 可編輯態、C3／B5／B6 乾淨 sheet、B1 跨日搵巧遇、U2、U4、C2／C4。
關鍵教訓：saveQ／renderNotebook／toggleCopyPanel／openCopyFromDay 唔係 global，
seed 入面嘅 saveQ() 會靜默失敗——B4 唔可以靠 reload，一定要 live seed。
用法：/home/hatch/pwenv49/bin/python qa197/drive197g.py [932|700]
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from drive197 import (OUT, SHOTS, URL, EXE, serve, stop, snap, census, rect,
                      modal_btns, click_text, click_first, dismiss_enc3, play_story,
                      new_game, ensure_on_map, open_loc, close_loc, open_journal,
                      SEED_DAYEND_JS, SEED_REST_JS, STATE_JS, finish_intro)
from playwright.sync_api import sync_playwright

def reset_quota(pg):
    return pg.evaluate("""() => { try { S.travel114 = {used:0, day:S.dayIndex}; return true; } catch(e){ return String(e); } }""")

def poll_modal(pg, secs=15):
    for _ in range(int(secs * 2)):
        m = pg.evaluate("""() => {
          const btns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null);
          if (!btns.length) return null;
          const mask=document.getElementById('mask');
          const modalEl = document.querySelector('#mask .modal') || document.querySelector('.modal');
          const r = modalEl ? modalEl.getBoundingClientRect() : null;
          const inner = document.getElementById('modal-inner');
          return {maskCls: mask?mask.className:null,
            modalH: r?Math.round(r.height):null, modalY: r?Math.round(r.top):null, modalW: r?Math.round(r.width):null,
            innerScroll: inner?{sh:inner.scrollHeight, ch:inner.clientHeight, st:inner.scrollTop}:null,
            title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h?(h.textContent||'').trim():null; })(),
            btns: btns.map(b=>{ const rr=b.getBoundingClientRect();
              return {t:(b.textContent||'').trim().slice(0,16), cls:(b.className||'').toString(), x:Math.round(rr.left), y:Math.round(rr.top), w:Math.round(rr.width), h:Math.round(r.height)}; })}; }""")
        if m:
            return m
        pg.wait_for_timeout(500)
    return None

def run(pw, H, label):
    print(f"===== FINAL4 {label} =====", flush=True)
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
        # ---- U6 UI 驅動合成態：S.homeEditable=true → 撳 day-row（內部 renderNotebook）→ 撳 ⧉ 複製 ----
        rec["probes"]["u6_synth"] = pg.evaluate("""() => {
          const out = {};
          try { S.homeEditable = true; } catch(e){ out.setErr = String(e); }
          const row = document.querySelector('.day-row');
          if (row) row.click();
          out.afterRowClick = {cpCount: document.querySelectorAll('.day-row .cp').length,
            homeEditable: S.homeEditable};
          const cp = document.querySelector('.day-row .cp');
          out.rowBtn = cp ? (cp.textContent||'').trim() : null;
          if (cp) cp.click();
          const w=document.getElementById('nb-copy-wrap');
          out.afterRowCopy = {open: w?w.classList.contains('open'):null, display: w?getComputedStyle(w).display:null};
          out.toast = (document.getElementById('toast')||{}).textContent || '';
          return out; }""")
        pg.wait_for_timeout(600)
        # 快捷列對照（同一 panel）
        rec["probes"]["u6_quick"] = pg.evaluate("""() => {
          const q=document.getElementById('nb-q-copy');
          if (q) q.click();
          const w=document.getElementById('nb-copy-wrap');
          return {panelOpen: w?w.classList.contains('open'):null, panelDisplay: w?getComputedStyle(w).display:null}; }""")
        pg.wait_for_timeout(500)
        pg.evaluate("""() => { const q=document.getElementById('nb-q-copy'); if (q) q.click(); return true; }""")
        pg.wait_for_timeout(400)
        # ---- B7 可編輯態：分類掣撳落去 .on 轉＋elementFromPoint ----
        rec["probes"]["b7_editable"] = pg.evaluate("""() => {
          const before = (()=>{ const o=document.querySelector('#cat-tabs button.on'); return o?(o.textContent||'').trim():null; })();
          const b=[...document.querySelectorAll('#cat-tabs button')].find(x=>(x.textContent||'').includes('訓練'));
          if (b) b.click();
          const after = (()=>{ const o=document.querySelector('#cat-tabs button.on'); return o?(o.textContent||'').trim():null; })();
          const bar = document.getElementById('nb-actions');
          const br = bar ? bar.getBoundingClientRect() : null;
          const nb = document.getElementById('notebook');
          const tabs=[...document.querySelectorAll('#cat-tabs button')].map(x=>{ const r=x.getBoundingClientRect();
            const hit=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
            return {t:(x.textContent||'').trim(), y:Math.round(r.top), bottom:Math.round(r.bottom),
              hitIsBtn: hit===x, hitIsChild: hit?x.contains(hit):null,
              hitCls: hit?(hit.className||'').toString().slice(0,40):null}; });
          return {before, after, barTop: br?Math.round(br.top):null, scrollTop: nb?nb.scrollTop:null,
            homeEditable: S.homeEditable, tabs}; }""")
        # ---- 確認＋播 intro ----
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
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- B4 soft：LIVE seed（唔 reload）→ 開始今日行程 ----
        seed_ret = pg.evaluate(SEED_DAYEND_JS, "soft")
        reset_quota(pg)
        rec["probes"]["b4_seed"] = {"ret": seed_ret,
            "state": pg.evaluate("() => ({weekPlan: S.weekPlan, shoots: (S.shoots||[]).map(x=>x.id)})")}
        rec["probes"]["b4_map_btns"] = pg.evaluate("""() => ({
          startToday: (()=>{ const e=document.getElementById('map-start-today'); if(!e) return null;
            const r=e.getBoundingClientRect(); return {t:(e.textContent||'').trim(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), vis:e.offsetParent!==null}; })(),
          endDay: (()=>{ const e=document.getElementById('map-end-day'); if(!e) return null;
            const r=e.getBoundingClientRect(); return {t:(e.textContent||'').trim(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), vis:e.offsetParent!==null}; })()})""")
        st_ok = click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
        rec["probes"]["b4_start_clicked"] = st_ok
        modal = poll_modal(pg, 15)
        rec["probes"]["b4_soft"] = modal
        snap(pg, f"{label}_g_b4_soft.png")
        if modal and click_text(pg, "返回地圖", scope="#modal-btns", wait=1200):
            pg.wait_for_timeout(900)
            rec["probes"]["b4_soft_after_back"] = pg.evaluate(STATE_JS)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- B4 rest：LIVE seed（唔 reload）→ 開始今日行程 ----
        seed_ret2 = pg.evaluate(SEED_REST_JS)
        reset_quota(pg)
        rec["probes"]["b4_rest_seed"] = {"ret": seed_ret2,
            "state": pg.evaluate("() => ({weekPlan: S.weekPlan})")}
        st_ok2 = click_text(pg, "開始今日行程", scope="#v-map", wait=1500)
        rec["probes"]["b4_rest_start_clicked"] = st_ok2
        modal2 = poll_modal(pg, 15)
        rec["probes"]["b4_rest"] = modal2
        snap(pg, f"{label}_g_b4_rest.png")
        if modal2:
            ok2 = click_text(pg, "返回地圖", scope="#modal-btns", wait=1500)
            pg.wait_for_timeout(1200)
            rec["probes"]["u1_rest_back"] = {"clicked": ok2, "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- C2／C4：過一日確認（自由日）----
        pg.evaluate("""() => { try { S.weekPlan = S.weekPlan || []; for(let i=0;i<7;i++) S.weekPlan[i]='rest'; S.homeEditable=false; S.travel114={used:0, day:S.dayIndex}; } catch(e){} return true; }""")
        dismiss_enc3(pg); ensure_on_map(pg)
        rec["probes"]["c2_end_day"] = {"end_day": rect(pg, "#map-end-day"), "start_today": rect(pg, "#map-start-today")}
        if click_text(pg, "過一日", scope="#v-map", wait=1200):
            pg.wait_for_timeout(900)
            rec["probes"]["c4_overday"] = {"btns": modal_btns(pg), "title": pg.evaluate(STATE_JS)["title"],
                "dom_order": pg.evaluate("() => [...document.querySelectorAll('#modal-btns button')].map(b=>(b.textContent||'').trim())")}
            snap(pg, f"{label}_g_c4_overday.png")
            click_first(pg, ["取消", "唔好", "返回"], 900)
            pg.wait_for_timeout(700)
        # ---- C3／B5／B6 乾淨 sheet ----
        reset_quota(pg)
        clean = None
        for attempt in range(3):
            r = open_loc(pg, "茶餐廳")
            pg.wait_for_timeout(800)
            st = pg.evaluate(STATE_JS)
            if st["story"]:
                play_story(pg, max_steps=60, tag_prefix="dlg_sheet4")
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
            snap(pg, f"{label}_g_sheet.png")
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
                    snap(pg, f"{label}_g_b1_enc.png")
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
                    play_story(pg, max_steps=40, tag_prefix="dlg_enchunt3")
                if st["locSheet"]:
                    close_loc(pg)
                dismiss_enc3(pg); ensure_on_map(pg)
            if enc: break
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
            snap(pg, f"{label}_g_u2_detail.png")
            click_first(pg, ["返回", "關閉"], 900)
            pg.wait_for_timeout(800)
            click_first(pg, ["返去地點", "返回地圖"], 900)
            pg.wait_for_timeout(800)
        close_loc(pg)
        dismiss_enc3(pg); ensure_on_map(pg)
        # ---- U4：額度擋 TVB ----
        reset_quota(pg)
        ensure_on_map(pg)
        pg.evaluate("""() => { try { S.travel114 = {used:2, day:S.dayIndex}; return true; } catch(e){ return String(e); } }""")
        pg.wait_for_timeout(400)
        before = {"state": pg.evaluate(STATE_JS),
            "locTitle": pg.evaluate("() => { const t=document.getElementById('loc-title'); return t?(t.textContent||'').trim():null; }"),
            "hint": pg.evaluate("() => { const h=document.getElementById('map-hint'); return h?(h.textContent||'').trim().slice(0,80):null; }"),
            "toast": pg.evaluate("() => (document.getElementById('toast')||{}).textContent || ''"),
            "used": pg.evaluate("() => (S.travel114||{}).used")}
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
        try: snap(pg, f"{label}_g_ERR.png")
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
        out.setdefault("final4_runs", {})[label] = rec
        with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f"== FINAL4 {label} DONE ==", flush=True)
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
