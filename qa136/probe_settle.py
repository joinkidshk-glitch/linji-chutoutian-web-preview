#!/usr/bin/env python3
"""Probe: after the week-end settlement modal, where does the game land?
Reuses drive136.py helpers. Prints DOM state after each step."""
import sys, time
sys.path.insert(0, "/home/hatch/workspace/linji-work136/qa136")
import drive136 as d
from playwright.sync_api import sync_playwright

def dump(pg, tag):
    st = pg.evaluate("""() => {
      const vis = (sel) => { const el = document.querySelector(sel); if (!el) return null;
        const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return {on: el.classList.contains('on'), w: Math.round(r.width), h: Math.round(r.height), disp: cs.display, vis: cs.visibility}; };
      const btns = [...document.querySelectorAll('button')].filter(b => { const r=b.getBoundingClientRect(); const cs=getComputedStyle(b); return r.width>0 && r.height>0 && cs.visibility!=='hidden' && cs.display!=='none'; }).map(b => (b.textContent||'').trim().slice(0,24));
      const modal = document.querySelector('#modal');
      let modalTxt = '';
      if (modal) { const cs = getComputedStyle(modal); const r = modal.getBoundingClientRect(); modalTxt = (r.width>0 && cs.display!=='none') ? (modal.innerText||'').slice(0,200) : '(hidden)'; }
      return {day: (typeof S!=='undefined'&&S)?S.dayIndex:null, vmap: vis('#v-map'), vhome: vis('#v-home'), btns: btns.slice(0,20), modal: modalTxt};
    }""")
    print(f"--- {tag} ---", flush=True)
    print(f"  day={st['day']} vmap={st['vmap']} vhome={st['vhome']}", flush=True)
    print(f"  btns={st['btns']}", flush=True)
    print(f"  modal={st['modal']!r}", flush=True)

srv = d.subprocess.Popen(["python3", "-m", "http.server", str(d.PORT), "--bind", "127.0.0.1"],
                         cwd=d.ROOT, stdout=d.subprocess.DEVNULL, stderr=d.subprocess.DEVNULL)
time.sleep(1.0)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=d.EXE)
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        ok = d.new_game_to_map(pg)
        print("new_game_to_map:", ok, flush=True)
        dump(pg, "at map after new game")
        ctx2 = d.seed(pg, day=d.day_index(1992, 12, 20), done_ids=d.PRE_C17, award_flag="done",
                      fame=20, stage=0, acting=8, credit_delta=0, money=5000, stress=0, c10_flag=True)
        print("seed:", ctx2, flush=True)
        dump(pg, "after seed (day 1084)")
        # click 過一日 -> confirm modal
        print("click 過一日:", d.click_vis_btn(pg, "過一日"), flush=True)
        pg.wait_for_timeout(800)
        dump(pg, "after 過一日 click (confirm modal?)")
        mi = d.modal_info(pg)
        print("modal_info:", {k: mi.get(k) for k in ("h3", "btns")}, flush=True)
        # pump like advance_day does, but step by step with dumps
        for i in range(6):
            mi = d.modal_info(pg)
            if mi.get("visible"):
                print(f"pump step {i}: modal h3={mi.get('h3')!r} btns={mi.get('btns')}", flush=True)
                r = d.dismiss_once(pg)
                print(f"  dismiss_once -> {r}", flush=True)
                pg.wait_for_timeout(800)
                dump(pg, f"after dismiss step {i}")
            elif d.home_on(pg) and d.vis_btn(pg, "確定本週行程"):
                print(f"pump step {i}: home confirm visible, clicking", flush=True)
                d.click_vis_btn(pg, "確定本週行程")
                pg.wait_for_timeout(800)
                dump(pg, f"after home confirm step {i}")
            elif d.map_ready(pg):
                print(f"pump step {i}: MAP READY", flush=True)
                break
            else:
                print(f"pump step {i}: nothing actionable", flush=True)
                dump(pg, f"stuck step {i}")
                pg.wait_for_timeout(400)
        print("pageerrors:", errs[:5], flush=True)
        b.close()
finally:
    srv.terminate()
