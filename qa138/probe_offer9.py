"""probe9: click tvb_harbour pin; dump overlay + S.visited + plan keys + starDay + gu state."""
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
        pg.evaluate("() => { S.dayIndex = 400; S.exodusFenSeeded=true; S.exodusFenFired=false; }")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        pre = pg.evaluate("""() => ({ visited: S.visited || {}, planKeys: Object.keys(S).filter(k=>/plan|today|schedule|travel/i.test(k)),
          travel114: S.travel114 || null })""")
        print("PRE:", pre)
        pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"tvb_harbour\"].pin'); if (p) p.click(); return !!p; }")
        pg.wait_for_timeout(1000)
        post = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          const sheet = document.getElementById('loc-sheet');
          return { overlay: !!ov, overlayText: ov ? (ov.textContent||'').trim().slice(0,80) : null,
                   sheetClass: sheet ? sheet.className : 'NO-SHEET',
                   title: (document.getElementById('loc-title')||{}).textContent,
                   visited: S.visited || {},
                   starDay: (S.starDay && S.starDay.presence) || {},
                   gu: (S.stars && S.stars.gu_mingfai) || null,
                   atLoc: (typeof atLoc!=='undefined') ? atLoc : 'undef-var' };
        }""")
        print("POST:", post)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE9 DONE")
