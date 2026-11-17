"""Probe 2: (D) exact T3a->T3b sequence; (E) instrumented wait_notice_modal on T1."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drive159 as D
from playwright.sync_api import sync_playwright

def snap(pg):
    return pg.evaluate("""() => {
      const vis = b => { const r=b.getBoundingClientRect(); const cs=getComputedStyle(b); return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'; };
      const m = document.querySelector('#modal');
      const mask = document.getElementById('mask');
      const sheet = document.querySelector('#loc-sheet');
      return {
        modal: m ? (m.innerText||'').trim().slice(0,150) : '(no #modal)',
        modalBtns: [...document.querySelectorAll('#modal-btns button')].filter(vis).map(b=>(b.textContent||'').trim().slice(0,20)),
        sheetOpen: !!(sheet && sheet.classList.contains('on')),
        maskOn: !!(mask && mask.classList && mask.classList.contains('on')),
        pending: (window.S && window.S.romance159) ? window.S.romance159.pendingNotice : 'n/a',
        toast: (document.getElementById('toast')||{}).textContent || ''
      };
    }""")

def main():
    srv = D.serve(D.ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 430, "height": 932})
            pg.add_init_script("window.__errs=[]; window.addEventListener('error',e=>window.__errs.push(String(e.message)));")
            pg.on("pageerror", lambda e: pg.evaluate("(m)=>{window.__errs.push(m)}", str(e)))
            D.boot(pg)
            MEET = {"R_hiu_meet": True, "R_choi_meet": True, "R_vera_meet": True,
                    "C1": True, "C2": True, "C3": True, "C4": True, "C5": True}
            MET = {"gift_met_colleague": True, "gift_met_reporter": True, "gift_met_stylist": True}
            LOCNPC = {"tvb_longmen": "colleague", "rec_star": "reporter", "ad_central": "stylist",
                      "tvb_harbour": "colleague", "film_cotton": "reporter", "rec_hk": "colleague"}

            # ---- Phase D: exact T3a -> T3b ----
            print("===== PHASE D: T3a->T3b exact =====", flush=True)
            D.seed(pg, rel={"rel_hiu": 5, "rel_choi": 2, "rel_vera": 1}, done=dict(MEET),
                 flags={"flag_romance_locked": True, "romance_locked_who": "hiu", **MET}, locNpc=dict(LOCNPC),
                 inv={"gift_coffee_beans": 1, "gift_perfume_sample": 1})
            print("open rec_star:", D.open_loc(pg, "rec_star"), flush=True)
            before_inv = D.state(pg)["inv"].get("gift_coffee_beans")
            ok, mt, toast_snap = D.give_gift(pg, "gift_coffee_beans")
            print(f"T3a give ok={ok} inv {before_inv}->{D.state(pg)['inv'].get('gift_coffee_beans')}", flush=True)
            print("D after T3a gift:", json.dumps(snap(pg), ensure_ascii=False), flush=True)
            print("close/cancel/dismiss:", D.click_btn(pg, "關閉") or D.click_btn(pg, "取消") or D.dismiss_once(pg), flush=True)
            pg.wait_for_timeout(500)
            print("D after close:", json.dumps(snap(pg), ensure_ascii=False), flush=True)
            D.reset_travel(pg)
            print("date btn visible:", D.vis_btn(pg, "約周采兒出街"), flush=True)
            print("click date:", D.click_btn(pg, "約周采兒出街"), flush=True)
            pg.wait_for_timeout(150)
            toast_snap = D.toast_now(pg)
            pg.wait_for_timeout(600)
            s = snap(pg)
            print("D at T3b check: toast=", repr(toast_snap), flush=True)
            print("D modal_text=", repr(D.modal_text(pg))[:400], flush=True)
            print("D snap:", json.dumps(s, ensure_ascii=False), flush=True)
            print("D cond: no-約會用一日 =", "約會用一日" not in D.modal_text(pg),
                  "| toast has 鎖定/心入面 =", ("鎖定" in toast_snap or "心入面" in toast_snap), flush=True)

            # ---- Phase E: instrumented wait_notice_modal on T1 ----
            print("===== PHASE E: T1 wait loop instrumented =====", flush=True)
            pg.goto(D.URL); pg.wait_for_timeout(1200); D.boot(pg)
            D.seed(pg, rel={"rel_hiu": 3}, done=dict(MEET), flags=dict(MET), locNpc=dict(LOCNPC), inv={"gift_memo_pad": 1})
            print("open tvb_longmen:", D.open_loc(pg, "tvb_longmen"), flush=True)
            ok, mt, toast_snap = D.give_gift(pg, "gift_memo_pad")
            print("gift ok:", ok, "pending:", D.state(pg)["r159"].get("pendingNotice"), flush=True)
            D.click_btn(pg, "關閉")
            phrases = ["越嚟越近", "你哋越嚟越近"]
            for i in range(30):
                pg.wait_for_timeout(600)
                mt = D.modal_text(pg)
                s = snap(pg)
                hit = any(p in mt for p in phrases)
                print(f"E iter {i}: hit={hit} modal={mt[:70]!r} btns={s['modalBtns']} mask={s['maskOn']} sheet={s['sheetOpen']} pending={s['pending']}", flush=True)
                if hit:
                    print("E: NOTICE MODAL SEEN at iter", i, flush=True)
                    break
                if D.click_btn(pg, "下一句") or D.click_btn(pg, "繼續"):
                    print(f"E iter {i}: clicked 下一句/繼續", flush=True)
                    continue
                clicked = pg.evaluate("""() => {
                  const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
                  if (!bs.length) return false;
                  bs[0].click(); return true;
                }""")
                if clicked:
                    print(f"E iter {i}: clicked first modal-btn", flush=True)
                    continue
                if not mt:
                    pg.evaluate("(a) => { try{ window.__phase2.openLoc(a[0], {travelFree:true}); }catch(e){} }", ["tvb_longmen"])
                    print(f"E iter {i}: re-openLoc", flush=True)
                    continue
            else:
                print("E: loop exhausted, no notice modal", flush=True)
            print("E final snap:", json.dumps(snap(pg), ensure_ascii=False), flush=True)
            print("E errors:", D.state(pg)["errors"], flush=True)
            br.close()
    finally:
        D.stop(srv)

if __name__ == "__main__":
    main()
