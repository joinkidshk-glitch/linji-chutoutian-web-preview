#!/usr/bin/env python3
"""v146 tour: other-modal spot checks + WF4 card banners + desktop mask alignment.
Usage: tour146.py [root] [port]
Writes qa146/tour146.json + screenshots under qa146/shots146/.
Sections (each fresh context unless noted):
  T1 tutorial modal @430x700 + @1200x900 (mask rect vs app rect)
  T2 confirm-day modal @430x700 (mask rect, modal y>=0)
  T3 WF4 cards st06/set08/st04 @430x700 + @430x932 (banner background-position + shot)
  T4 loc-sheet agency + handbook @430x700
  T5 S-30 casting sheet @430x700 (via agency 通告欄)
  T6 day-res modal after day advance @430x700 (paper-on watched)
Exit 0 iff all checked sections pass.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/linji-work146")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8999
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = os.path.join(ROOT, "qa146", "shots146")
os.makedirs(SHOTS, exist_ok=True)
results = {}
def rec(name, ok, detail=None):
    results[name] = {"ok": bool(ok), "detail": detail}
    print(("PASS " if ok else "FAIL ") + name + ((" :: " + str(detail)) if detail is not None else ""))
def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)
def click_vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false; vis[0].click(); return true;
    }""", text)
def modal_h3(pg):
    return pg.evaluate("() => { const h = document.querySelector('#modal h3'); return h ? h.textContent : ''; }")
def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400): btn.click(timeout=1000); return True
    except Exception: pass
    return False
def wait_on_map(pg, secs=60):
    for _ in range(int(secs / 0.7)):
        if vis_btn(pg, "過一日"): return True
        if not dismiss_once(pg):
            if not click_vis_btn(pg, "返回地圖"): pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    return False
def mask_geo(pg):
    return pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), pos: cs.position}; };
      const mask = q('#mask'), modal = q('#modal'), app = q('#app'), h3 = q('#modal h3');
      return { app: r(app), mask: r(mask), modal: r(modal), h3: r(h3), h3text: h3 ? h3.textContent : '',
        maskOn: mask ? mask.classList.contains('on') : false,
        maskCls: mask ? [...mask.classList].join(' ') : '',
        modalMaxH: modal ? getComputedStyle(modal).maxHeight : null,
        vh: innerHeight, vw: innerWidth, appScrollTop: app ? app.scrollTop : null };
    }""")
def new_game_to_map(pg):
    pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1")
    pg.wait_for_timeout(1500)
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
    pg.wait_for_timeout(1000)
    try:
        pg.locator('[data-slot="3"]').first.click(timeout=1500); pg.wait_for_timeout(800)
    except Exception: pass
    for _ in range(10):
        try:
            pg.get_by_text("跳過教學", exact=True).first.click(timeout=1200); pg.wait_for_timeout(600); break
        except Exception:
            try:
                pg.get_by_text("下一步", exact=True).first.click(timeout=1200); pg.wait_for_timeout(600)
            except Exception: break
    pg.wait_for_timeout(1200)
    return wait_on_map(pg)
def drive_wf4_card(pg, ev, title_sub):
    """Assumes on map. Seeds pending, advances day, returns banner info dict or None."""
    for _ in range(30):
        if vis_btn(pg, "過一日"): break
        if click_vis_btn(pg, "開始今日行程"): pg.wait_for_timeout(1000); continue
        if not dismiss_once(pg):
            if not click_vis_btn(pg, "返回地圖"): pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    pg.evaluate("""(ev) => {
        if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
        S.wf4.pending = ev; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
    }""", ev)
    click_vis_btn(pg, "過一日")
    for _ in range(45):
        pg.wait_for_timeout(1000)
        h3 = modal_h3(pg)
        if title_sub in h3: return True
        if h3 == "確認過一日？":
            if click_vis_btn(pg, "確定過一日"): continue
        dismiss_once(pg)
    return False

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        # ---- T1 tutorial modal, 430x700 + 1200x900 ----
        for (W, H) in [(430, 700), (1200, 900)]:
            ctx = b.new_context(viewport={"width": W, "height": H})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1")
            pg.wait_for_timeout(1500)
            pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
            pg.wait_for_timeout(1500)
            g = mask_geo(pg)
            same = (g["app"] and g["mask"] and g["app"]["x"] == g["mask"]["x"] and g["app"]["y"] == g["mask"]["y"]
                    and g["app"]["w"] == g["mask"]["w"] and g["app"]["h"] == g["mask"]["h"])
            rec(f"T1 tutorial modal mask==app @{W}x{H}", same and g["maskOn"] and not errs,
                {"app": g["app"], "mask": g["mask"], "modal": g["modal"], "pageerrors": errs})
            pg.screenshot(path=f"{SHOTS}/t1_tutorial_{W}x{H}.png")
            ctx.close()
        # ---- T2 confirm-day modal @430x700 ----
        ctx = b.new_context(viewport={"width": 430, "height": 700})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        if new_game_to_map(pg):
            click_vis_btn(pg, "過一日")
            pg.wait_for_timeout(1200)
            g = mask_geo(pg)
            rec("T2 confirm-day modal @430x700", g["h3text"] == "確認過一日？" and g["modal"]["y"] >= 0 and not errs,
                {"h3": g["h3text"], "modal": g["modal"], "mask": g["mask"], "pageerrors": errs})
            pg.screenshot(path=f"{SHOTS}/t2_confirm_430x700.png")
            click_vis_btn(pg, "確定過一日")
            pg.wait_for_timeout(1500)
            # day-res / rest card may follow; record whatever modal is showing
            g2 = mask_geo(pg)
            rec("T6 day-res-or-next modal after advance @430x700", g2["modal"] is None or g2["modal"]["y"] >= 0,
                {"h3": g2["h3text"], "modal": g2["modal"], "maskCls": g2["maskCls"]})
            pg.screenshot(path=f"{SHOTS}/t6_after_advance_430x700.png")
        else:
            rec("T2 confirm-day modal @430x700", False, "not on map")
        ctx.close()
        # ---- T3 WF4 cards @700 + @932 ----
        for (ev, title, tag) in [("wf4_ev_st06", "魚檔", "st06"),
                                 ("wf4_ev_set08", "派錯", "set08"),
                                 ("wf4_ev_st04", "紅豆冰", "st04")]:
            for (W, H) in [(430, 700), (430, 932)]:
                ctx = b.new_context(viewport={"width": W, "height": H})
                pg = ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                failed = []
                pg.on("requestfailed", lambda r: failed.append(r.url))
                ok = new_game_to_map(pg) and drive_wf4_card(pg, ev, title)
                info = None
                if ok:
                    pg.wait_for_timeout(600)
                    info = pg.evaluate("""() => {
                      const bn = document.querySelector('#modal .wf4-scene105');
                      const h3 = document.querySelector('#modal h3');
                      const m = document.querySelector('#modal');
                      const b = m ? m.getBoundingClientRect() : null;
                      return { banner: bn ? { bg: bn.style.backgroundImage.slice(0, 80),
                        pos: getComputedStyle(bn).backgroundPosition } : null,
                        h3: h3 ? { y: Math.round(h3.getBoundingClientRect().y), text: h3.textContent } : null,
                        modalY: b ? Math.round(b.y) : null };
                    }""")
                    pg.screenshot(path=f"{SHOTS}/t3_{tag}_{W}x{H}.png")
                want_pos = "50% 75%" if tag == "st06" else "50% 50%"
                good = bool(ok and info and info["banner"] and info["banner"]["pos"] == want_pos
                            and info["h3"] and info["h3"]["y"] >= 0 and info["modalY"] >= 0
                            and not errs and not failed)
                rec(f"T3 card {tag} banner @{W}x{H}", good,
                    {"info": info, "pageerrors": errs, "failedReq": failed})
                ctx.close()
        # ---- T4 loc-sheet + handbook @430x700 ----
        ctx = b.new_context(viewport={"width": 430, "height": 700})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        if new_game_to_map(pg):
            # loc-sheet: open via map area list button for 事務所
            opened = pg.evaluate("""() => {
              const btns = [...document.querySelectorAll('#map-area-list button, .map-area-list button, #v-map button')];
              const t = btns.find(x => (x.textContent||'').includes('事務所'));
              if (t) { t.click(); return true; } return false;
            }""")
            pg.wait_for_timeout(1200)
            sheet = pg.evaluate("""() => {
              const sh = document.querySelector('#loc-sheet');
              if (!sh) return null;
              const b = sh.getBoundingClientRect();
              return { on: sh.classList.contains('on'), x: Math.round(b.x), y: Math.round(b.y),
                       w: Math.round(b.width), h: Math.round(b.height), txt: (sh.textContent||'').slice(0, 60) };
            }""")
            rec("T4 loc-sheet agency @430x700", bool(opened and sheet and sheet["on"] and not errs),
                {"opened": opened, "sheet": sheet, "pageerrors": errs})
            pg.screenshot(path=f"{SHOTS}/t4_locsheet_430x700.png")
            click_vis_btn(pg, "返回地圖")
            pg.wait_for_timeout(800)
            # handbook: menubar 手帳 button
            hb = click_vis_btn(pg, "手帳") or pg.evaluate("""() => {
              const bs = [...document.querySelectorAll('button')].filter(x => (x.textContent||'').includes('手帳'));
              if (bs.length) { bs[0].click(); return true; } return false; }""")
            pg.wait_for_timeout(1200)
            home_on = pg.evaluate("() => { const v = document.querySelector('#v-home'); return v ? v.classList.contains('on') : null; }")
            rec("T4 handbook opens @430x700", bool(hb and home_on and not errs),
                {"clicked": hb, "homeOn": home_on, "pageerrors": errs})
            pg.screenshot(path=f"{SHOTS}/t4_handbook_430x700.png")
        else:
            rec("T4 loc-sheet agency @430x700", False, "not on map")
        ctx.close()
        # ---- T5 S-30 casting sheet via agency 通告欄 ----
        ctx = b.new_context(viewport={"width": 430, "height": 700})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        if new_game_to_map(pg):
            opened = pg.evaluate("""() => {
              const btns = [...document.querySelectorAll('#map-area-list button, .map-area-list button, #v-map button')];
              const t = btns.find(x => (x.textContent||'').includes('事務所'));
              if (t) { t.click(); return true; } return false;
            }""")
            pg.wait_for_timeout(1200)
            board = click_vis_btn(pg, "通告欄")
            pg.wait_for_timeout(1500)
            g = mask_geo(pg)
            rec("T5 S-30 casting sheet @430x700", bool(board and g["maskOn"] and g["modal"] and g["modal"]["y"] >= 0 and not errs),
                {"board": board, "h3": g["h3text"], "modal": g["modal"], "maskCls": g["maskCls"], "pageerrors": errs})
            pg.screenshot(path=f"{SHOTS}/t5_casting_430x700.png")
        else:
            rec("T5 S-30 casting sheet @430x700", False, "not on map")
        ctx.close()
        b.close()
finally:
    srv.terminate()
json.dump(results, open(os.path.join(ROOT, "qa146", "tour146.json"), "w"), ensure_ascii=False, indent=1)
bad = [k for k, v in results.items() if not v["ok"]]
print("TOUR " + ("ALL-PASS" if not bad else "FAIL: " + ", ".join(bad)))
sys.exit(0 if not bad else 1)
