"""probe11: dump S.weekPlan + computed today plan after new_game (x2 sessions)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game = ns['new_game']
serve, ROOT, EXE, HERE = ns['serve'], ns['ROOT'], ns['EXE'], ns['HERE']
from playwright.sync_api import sync_playwright
srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        for run in (1, 2):
            new_game(pg)
            plan = pg.evaluate("""() => {
              const wd = ((S.dayIndex % 7) + 7) % 7;
              return { day: S.dayIndex, wd, weekPlan: S.weekPlan || null, today: (S.weekPlan && S.weekPlan[wd]) || null };
            }""")
            print(f"run{run} plan:", plan)
            pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"tvb_harbour\"].pin'); if (p) p.click(); return !!p; }")
            pg.wait_for_timeout(900)
            st = pg.evaluate("""() => {
              const sheet = document.getElementById('loc-sheet');
              return { sheetOn: sheet ? sheet.className.includes(' on') : false, title: (document.getElementById('loc-title')||{}).textContent.trim() };
            }""")
            print(f"run{run} tvb_harbour sheet:", st)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE11 DONE")
