"""probe15: control — seed LUK at film_lion day 0 (known-good loc), DOM .click() pin. Does intercept fire?"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game, suppress_wf4, isolate_star, back_to_map, seed_star = ns['new_game'], ns['suppress_wf4'], ns['isolate_star'], ns['back_to_map'], ns['seed_star']
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
        seed_star(pg, "luk_baakyin", True, 50, 3, beats_done=[], heart_done=False)
        pg.evaluate("(d) => { S.dayIndex = d; }", 0)
        suppress_wf4(pg); isolate_star(pg, "luk_baakyin"); back_to_map(pg)
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"film_lion\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(1200)
        st = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          const sheet = document.getElementById('loc-sheet');
          return { overlay: !!ov, overlayName: ov ? ((ov.querySelector('.e79-name')||{}).textContent||'').trim() : null,
                   sheetOn: sheet ? sheet.className.includes(' on') : false,
                   title: (document.getElementById('loc-title')||{}).textContent.trim(),
                   presence: (S.starDay && S.starDay.presence) || {},
                   triggered: (S.starDay && S.starDay.triggered) || 0 };
        }""")
        print("LUK at film_lion day0 (DOM click):", st)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE15 DONE")
