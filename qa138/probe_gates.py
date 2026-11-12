"""probe7: dump openLoc gate states after new_game + day 400 + fen seed."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game, suppress_wf4, isolate_star, back_to_map = ns['new_game'], ns['suppress_wf4'], ns['isolate_star'], ns['back_to_map']
serve, ROOT, EXE, HERE = ns['serve'], ns['ROOT'], ns['EXE'], ns['HERE']
from playwright.sync_api import sync_playwright
srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        new_game(pg)
        pg.evaluate("() => { const S = window.S; S.dayIndex = 400; S.exodusFenSeeded=true; S.exodusFenFired=false; }")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        gates = pg.evaluate("""() => {
          const out = {};
          out.day = S.dayIndex;
          out.travel114 = S.travel114 || null;
          const fns = ["isStoryPlayActive","todayIsForcedDay","todayPlanId","ending78Gate","travel114Remain","openLoc","StoryPlay"];
          for (const f of fns) { try { out[f] = (typeof window[f] !== 'undefined') ? String(typeof window[f]) : 'undef'; } catch(e){ out[f] = 'err'; } }
          try { out.isStoryPlayActive_v = (typeof isStoryPlayActive==='function') ? isStoryPlayActive() : 'n/a'; } catch(e){ out.isStoryPlayActive_v = 'err:'+e.message; }
          try { out.todayIsForcedDay_v = (typeof todayIsForcedDay==='function') ? todayIsForcedDay() : 'n/a'; } catch(e){ out.todayIsForcedDay_v = 'err:'+e.message; }
          try { out.todayPlanId_v = (typeof todayPlanId==='function') ? todayPlanId() : 'n/a'; } catch(e){ out.todayPlanId_v = 'err:'+e.message; }
          try { out.travelRemain = (typeof travel114Remain==='function') ? travel114Remain() : 'n/a'; } catch(e){ out.travelRemain = 'err:'+e.message; }
          try { out.ending78 = (typeof ending78Gate==='function') ? ending78Gate() : 'n/a'; } catch(e){ out.ending78 = 'err:'+e.message; }
          return out;
        }""")
        print("GATES:", gates)
        # click pin, then read toast text
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"tvb_harbour\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(900)
        toast = pg.evaluate("""() => {
          const t = document.querySelector('.toast') || document.querySelector('[class*="toast"]');
          return t ? t.textContent.trim().slice(0,120) : null;
        }""")
        print("TOAST after pin click:", toast)
        st = pg.evaluate("""() => {
          const sheet = document.getElementById('loc-sheet');
          return { sheetClass: sheet ? sheet.className : 'NO-SHEET', title: (document.getElementById('loc-title')||{}).textContent };
        }""")
        print("SHEET:", st)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE7 DONE")
