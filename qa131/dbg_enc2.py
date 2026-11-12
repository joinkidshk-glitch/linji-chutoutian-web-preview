# -*- coding: utf-8 -*-
"""qa131 巧遇攔截診斷：複製 drive131 流程（新遊戲→手帳→殺青 modal→A_fong_push1→返地圖→seed 彭少祺），
逐日直查 enc79EnsureDay／enc79PresenceAt／enc79StoryPendingAt／enc79TryIntercept。
"""
import sys, os, json, subprocess, time, signal
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work131"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8964
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    return p

def click_first(pg, texts, wait=1000):
    for t in texts:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

JS_DIAG = """(day) => {
  S.dayIndex = day;
  const sd = (typeof enc79EnsureDay === 'function') ? enc79EnsureDay() : null;
  const pres = (typeof enc79PresenceAt === 'function') ? enc79PresenceAt('ad_central') : null;
  const pend = (typeof enc79StoryPendingAt === 'function') ? enc79StoryPendingAt('ad_central') : null;
  const st = (typeof enc79StarState === 'function') ? enc79StarState('pang_siuki') : null;
  const pangDef = (typeof ENC79_STARS !== 'undefined') ? ENC79_STARS.find(s => s.id === 'pang_siuki') : null;
  return {day, starDay: sd ? {day: sd.day, triggered: sd.triggered, presenceAd: sd.presence['ad_central'] || []} : null,
          pres, pend, star: st ? {met: st.met, fav: st.fav, lastDay: st.lastDay} : null,
          def: pangDef ? {primary: pangDef.primary, secondary: pangDef.secondary} : null,
          openNodes: (() => { try { const oc = StoryOC.listOpen({checkNodePhase:true, player:true, ignoreSheetLoc:true}) || {};
            return (oc.open||[]).map(r => r.id); } catch(_e) { return 'err'; } })()};
}"""

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(3000)
        click_first(pg, ["新遊戲"], 1500)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        click_first(pg, ["覆蓋", "確定", "確認"], 900)
        click_first(pg, ["跳過教學"], 1200)
        click_first(pg, ["開始寫手帳"], 1400)
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception:
            pass
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        # 診斷 A：新遊戲狀態（未播故事）逐日 presence
        print("== A: fresh game ==", flush=True)
        pg.evaluate("""(a) => {
          S.stars = S.stars || {};
          const st = S.stars[a.star] || (S.stars[a.star] = {});
          st.met = true; st.fav = a.fav; st.beatsDone = {}; st.poolSeen = {};
          st.heartDone = false; st.stage = 0; st.wrapEcho = false; st.capHit = false;
        }""", {"star": "pang_siuki", "fav": 5})
        for day in range(0, 6):
            print(" day", day, json.dumps(pg.evaluate(JS_DIAG, day), ensure_ascii=False), flush=True)
        # 診斷 B：播 A_fong_push1 之後同樣逐日
        print("== B: after A_fong_push1 ==", flush=True)
        ok = pg.evaluate("""(n) => {
          try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) {}
          return false; }""", "A_fong_push1")
        print(" story start:", ok, flush=True)
        pg.wait_for_timeout(1500)
        for _ in range(8):
            clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
              if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
              if (!bs.length) return false; bs[0].click(); return true; }""")
            pg.wait_for_timeout(1500)
            if not clicked:
                break
        pg.wait_for_timeout(800)
        picked = pg.evaluate("""() => { const c = document.querySelector('.sp-choice');
          if (c) { c.click(); return true; } return false; }""")
        print(" choice picked:", picked, flush=True)
        pg.wait_for_timeout(1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續", "返回地圖"], 900):
                break
        pg.wait_for_timeout(800)
        print(" S.dayIndex now:", pg.evaluate("() => S.dayIndex"), " loc:", pg.evaluate("() => S.loc"), flush=True)
        for day in range(0, 6):
            print(" day", day, json.dumps(pg.evaluate(JS_DIAG, day), ensure_ascii=False), flush=True)
        print("PAGEERRORS:", errs[:5], flush=True)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        pass
