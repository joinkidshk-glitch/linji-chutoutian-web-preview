"""probe6: DOM .click() on the pin; if that fails, scroll list button into view and click it."""
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
               acts: acts ? [...acts.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim().slice(0,45)) : 'NO-ACTS' };
    }""")
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        new_game(pg)
        pg.evaluate("() => { const S = window.S; S.dayIndex = 400; S.exodusFenSeeded=true; S.exodusFenFired=false; }")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        # attempt 1: DOM .click() on the pin
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"tvb_harbour\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(900)
        print("AFTER dom-click pin:", sheet_state(pg))
        if sheet_state(pg)["title"] == "地點":
            # attempt 2: scroll the list button into view and click it
            pg.evaluate("() => { const l = document.querySelector('#map-area-list button[data-loc=\"tvb_harbour\"]'); if (l) l.scrollIntoView({block:'center'}); return !!l; }")
            pg.wait_for_timeout(600)
            btn = pg.locator('#map-area-list button[data-loc="tvb_harbour"]')
            print("list btn visible after scroll:", btn.is_visible() if btn.count() else "no btn")
            if btn.count():
                btn.click(timeout=3000)
                pg.wait_for_timeout(900)
                print("AFTER list-btn click:", sheet_state(pg))
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE6 DONE")
