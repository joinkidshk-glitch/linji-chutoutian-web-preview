"""probe_fen2: DOM-click the hidden map-area-list button for tvb_harbour; dump title + acts."""
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
        pg.evaluate("""() => { S.dayIndex = 400; S.exodusFenSeeded = true; S.exodusFenFired = false; return true; }""")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        r = pg.evaluate("""() => {
          const listBtn = document.querySelector('#map-area-list button[data-loc="tvb_harbour"]');
          const pin = document.querySelector('button.pin[data-loc="tvb_harbour"]');
          const info = { listBtn: !!listBtn, pin: !!pin,
                         listOnclick: listBtn ? (listBtn.getAttribute('onclick')||'').slice(0,60) : null,
                         pinOnclick: pin ? (pin.getAttribute('onclick')||'').slice(0,60) : null };
          if (listBtn) listBtn.click();
          return info;
        }""")
        print("clicked list btn:", r, flush=True)
        pg.wait_for_timeout(900)
        st = pg.evaluate("""() => {
          const t = (document.getElementById('loc-title')||{}).textContent || '';
          const acts = [...document.querySelectorAll('#loc-acts button')].map(b => (b.textContent||'').trim().slice(0,40));
          const allBtns = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes('芬姐')).map(b => (b.textContent||'').trim().slice(0,40));
          return { title: t.trim(), acts, fenBtns: allBtns, visited: S.visited };
        }""")
        print("after list-btn click:", st, flush=True)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE_FEN2 DONE")
