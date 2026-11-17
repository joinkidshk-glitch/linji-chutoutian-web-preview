"""Probe for drive run-3 failures: T1/T2 notice modal, T3b picker, T4 talk flow.
Reuses drive159 helpers (import; __main__ guard prevents running the suite)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drive159 as D
from playwright.sync_api import sync_playwright

def dump(pg, tag):
    info = pg.evaluate("""() => {
      const vis = b => { const r=b.getBoundingClientRect(); const cs=getComputedStyle(b); return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'; };
      const btns = sel => [...document.querySelectorAll(sel)].filter(vis).map(b=>(b.textContent||'').trim().slice(0,24));
      const mask = document.getElementById('mask');
      return {
        modal: (document.querySelector('#modal')||{}).innerText ? document.querySelector('#modal').innerText.slice(0,220) : '',
        modalBtns: btns('#modal-btns button'),
        spBtns: btns('.sp-actions button'),
        sheetBtns: btns('#loc-sheet button'),
        maskOn: !!(mask && mask.classList && mask.classList.contains('on')),
        storyActive: (typeof window.__phase2!=='undefined' && window.__phase2.isStoryPlayActive) ? !!window.__phase2.isStoryPlayActive() : 'n/a',
        pending: (window.S && window.S.romance159) ? window.S.romance159.pendingNotice : 'n/a',
        toast: (document.getElementById('toast')||{}).textContent || ''
      };
    }""")
    print(f"--- {tag} ---")
    print(json.dumps(info, ensure_ascii=False, indent=1)[:1800], flush=True)
    return info

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

            # ---- Probe A: T1 flush path ----
            print("===== PROBE A: T1 soft-notice flush =====", flush=True)
            D.seed(pg, rel={"rel_hiu": 3}, done=dict(MEET), flags=dict(MET), locNpc=dict(LOCNPC), inv={"gift_memo_pad": 1})
            print("open_loc:", D.open_loc(pg, "tvb_longmen"), flush=True)
            ok, mt, toast_snap = D.give_gift(pg, "gift_memo_pad")
            print("gift ok:", ok, "rel:", D.state(pg)["rel"], "pending:", D.state(pg)["r159"], flush=True)
            D.click_btn(pg, "關閉")
            for i in range(14):
                pg.wait_for_timeout(1000)
                dump(pg, f"A after-close t={i+1}s")
                # do NOT click anything; just observe what the app does on its own
            # now try re-opening the location once, as wait_notice_modal does
            pg.evaluate("(a) => { try{ window.__phase2.openLoc(a[0], {travelFree:true}); }catch(e){} }", ["tvb_longmen"])
            pg.wait_for_timeout(1000)
            dump(pg, "A after manual re-openLoc")

            # ---- Probe B: T3b locked date button ----
            print("===== PROBE B: T3b locked date button =====", flush=True)
            pg.goto(D.URL); pg.wait_for_timeout(1200); D.boot(pg)
            D.seed(pg, rel={"rel_hiu": 5, "rel_choi": 2, "rel_vera": 1}, done=dict(MEET),
                 flags={"flag_romance_locked": True, "romance_locked_who": "hiu", **MET}, locNpc=dict(LOCNPC),
                 inv={"gift_coffee_beans": 1})
            print("open_loc rec_star:", D.open_loc(pg, "rec_star"), flush=True)
            print("click date btn:", D.click_btn(pg, "約周采兒出街"), flush=True)
            pg.wait_for_timeout(150)
            print("toast@150ms:", repr(D.toast_now(pg)), flush=True)
            pg.wait_for_timeout(600)
            dump(pg, "B after date click")

            # ---- Probe C: T4 talk flow step by step ----
            print("===== PROBE C: T4 talk flow =====", flush=True)
            pg.goto(D.URL); pg.wait_for_timeout(1200); D.boot(pg)
            D.seed(pg, rel={"rel_hiu": 2}, done=dict(MEET), flags=dict(MET), locNpc=dict(LOCNPC), inv={})
            print("open_loc tvb_longmen:", D.open_loc(pg, "tvb_longmen"), flush=True)
            print("click 傾談:", D.click_btn(pg, "傾談"), flush=True)
            for i in range(12):
                pg.wait_for_timeout(700)
                info = dump(pg, f"C talk step {i}")
                mt = info["modal"]
                if "交換電話號碼" in mt or "約佢出街" in mt:
                    print("C: reached result modal at step", i, flush=True)
                    break
                # click first available talk-advance button, preferring 謝謝/再傾兩句/下一句/繼續
                clicked = (D.click_btn(pg, "謝謝，我會去睇") or D.click_btn(pg, "再傾兩句近況")
                           or D.click_btn(pg, "下一句") or D.click_btn(pg, "繼續"))
                print(f"C step {i}: clicked-advance={clicked}", flush=True)
                if not clicked:
                    print("C: no advance button; stop", flush=True)
                    break
            print("C phone exchange click:", D.click_btn(pg, "交換電話號碼"), flush=True)
            pg.wait_for_timeout(500)
            print("C phone state:", D.state(pg)["r159"], flush=True)
            print("C errors:", D.state(pg)["errors"], flush=True)
            br.close()
    finally:
        D.stop(srv)

if __name__ == "__main__":
    main()
