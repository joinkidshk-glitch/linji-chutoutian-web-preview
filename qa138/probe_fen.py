"""probe_fen: replicate play_offer('海港', day 400) step by step, dump state after each step."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game, suppress_wf4, isolate_star, back_to_map, seed_star, click_first, sheet_open = ns['new_game'], ns['suppress_wf4'], ns['isolate_star'], ns['back_to_map'], ns['seed_star'], ns['click_first'], ns['sheet_open']
serve, ROOT, EXE, HERE = ns['serve'], ns['ROOT'], ns['EXE'], ns['HERE']
from playwright.sync_api import sync_playwright
srv = serve(ROOT)
def dump(pg, label):
    st = pg.evaluate("""() => {
      const t = (document.getElementById('loc-title')||{}).textContent || '';
      const sheet = document.getElementById('loc-sheet');
      const pins = [...document.querySelectorAll('button[data-loc="tvb_harbour"]')].map(b => ({cls: b.className.slice(0,60), vis: b.offsetParent!==null, w: b.offsetWidth, h: b.offsetHeight, txt: (b.textContent||'').trim().slice(0,20)}));
      const haiBtns = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes('海港')).map(b => ({cls: b.className.slice(0,40), vis: b.offsetParent!==null, w: b.offsetWidth}));
      const modal = !!document.querySelector('.modal.open');
      const ov = !!document.getElementById('enc79-overlay');
      const acts = [...document.querySelectorAll('#loc-acts button')].map(b => (b.textContent||'').trim().slice(0,30));
      return { title: t.trim(), sheetOn: sheet ? sheet.className.includes(' on') : false, pins, haiBtns, modal, ov, acts };
    }""")
    print(label, st, flush=True)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        new_game(pg)
        dump(pg, "after new_game:")
        pg.evaluate("""() => { S.dayIndex = 400; S.exodusFenSeeded = true; S.exodusFenFired = false; return true; }""")
        suppress_wf4(pg); isolate_star(pg, "__none__")
        dump(pg, "after seed+suppress+isolate:")
        back_to_map(pg)
        dump(pg, "after back_to_map:")
        r = click_first(pg, ["海港"], 1200)
        print("click_first returned:", r, flush=True)
        pg.wait_for_timeout(700)
        dump(pg, "after click 海港:")
        print("sheet_open:", sheet_open(pg), flush=True)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE_FEN DONE")
