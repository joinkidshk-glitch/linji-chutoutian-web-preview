"""probe_fen3: exact play_offer sequence for s_fen_intro, dump title+acts after sheet opens."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game, suppress_wf4, isolate_star, back_to_map, open_loc_retry, sheet_open = ns['new_game'], ns['suppress_wf4'], ns['isolate_star'], ns['back_to_map'], ns['open_loc_retry'], ns['sheet_open']
serve, ROOT, EXE, HERE = ns['serve'], ns['ROOT'], ns['EXE'], ns['HERE']
from playwright.sync_api import sync_playwright
srv = serve(ROOT)
def dump(pg, label):
    st = pg.evaluate("""() => {
      const t = (document.getElementById('loc-title')||{}).textContent || '';
      const acts = [...document.querySelectorAll('#loc-acts button')].map(b => (b.textContent||'').trim().slice(0,45));
      const fen = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes('芬姐')).map(b => ({txt:(b.textContent||'').trim().slice(0,45), vis: b.offsetParent!==null}));
      return { title: t.trim(), acts, fen, flags: {seeded: S.exodusFenSeeded, fired: S.exodusFenFired, introDone: (S.story&&S.story.done&&S.story.done['WF4_fen_intro'])||false, day: S.dayIndex} };
    }""")
    print(label, st, flush=True)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        new_game(pg)
        pg.evaluate("""() => { const S = window.S; S.dayIndex = 400; S.exodusFenSeeded=true;S.exodusFenFired=false; }""")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        ok = open_loc_retry(pg, "海港")
        print("open_loc_retry:", ok, flush=True)
        pg.wait_for_timeout(600)
        dump(pg, "after open:")
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE_FEN3 DONE")
