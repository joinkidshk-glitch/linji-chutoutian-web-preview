"""probe5: click the pin's inner image/head (not the button center); dump sheet state."""
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
        box = pg.evaluate("""() => {
          const pin = document.querySelector('button[data-loc="tvb_harbour"].pin');
          if (!pin) return null;
          const inner = pin.querySelector('.pin-img') || pin.querySelector('.pin-head') || pin.querySelector('.dot');
          const r = (inner || pin).getBoundingClientRect();
          const pr = pin.getBoundingClientRect();
          return { innerSel: inner ? inner.className : 'NONE', x: r.x + r.width/2, y: r.y + r.height/2,
                   w: r.width, h: r.height, pinBox: {x: pr.x, y: pr.y, w: pr.width, h: pr.height},
                   innerPE: inner ? getComputedStyle(inner).pointerEvents : null,
                   pinPE: getComputedStyle(pin).pointerEvents };
        }""")
        print("BOX:", box)
        if box:
            pg.mouse.click(box["x"], box["y"])
            pg.wait_for_timeout(1000)
            st = pg.evaluate("""() => {
              const sheet = document.getElementById('loc-sheet');
              const acts = document.getElementById('loc-acts');
              return { sheetClass: sheet ? sheet.className : 'NO-SHEET',
                       title: (document.getElementById('loc-title')||{}).textContent,
                       acts: acts ? [...acts.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim().slice(0,45)) : 'NO-ACTS' };
            }""")
            print("AFTER inner click:", st)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE5 DONE")
