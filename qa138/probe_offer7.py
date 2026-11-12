"""probe8: isolate the variable — click tvb_harbour pin at (a) day 0 no seed, (b) day 400 no seed, (c) day 400 + fen seed."""
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
def sheet_state(pg):
    return pg.evaluate("""() => {
      const sheet = document.getElementById('loc-sheet');
      const acts = document.getElementById('loc-acts');
      return { sheetClass: sheet ? sheet.className : 'NO-SHEET',
               title: (document.getElementById('loc-title')||{}).textContent,
               nActs: acts ? acts.querySelectorAll('button').length : -1 };
    }""")
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        # (a) day 0, no seed
        new_game(pg)
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"tvb_harbour\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(900)
        print("(a) day0 no-seed:", sheet_state(pg))
        # (b) day 400, no seed
        new_game(pg)
        pg.evaluate("() => { S.dayIndex = 400; }")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"tvb_harbour\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(900)
        print("(b) day400 no-seed:", sheet_state(pg))
        # (c) day 400 + fen seed
        new_game(pg)
        pg.evaluate("() => { S.dayIndex = 400; S.exodusFenSeeded=true; S.exodusFenFired=false; }")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"tvb_harbour\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(900)
        print("(c) day400 + fen seed:", sheet_state(pg))
        # (d) control: agency_ho pin at day 400, no seed — does IT open?
        new_game(pg)
        pg.evaluate("() => { S.dayIndex = 400; }")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"agency_ho\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(900)
        print("(d) agency_ho day400 no-seed:", sheet_state(pg))
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE8 DONE")
