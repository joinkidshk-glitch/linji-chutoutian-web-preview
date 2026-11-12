"""probe2: seed + enter tvb_harbour, dump sheet state + all visible buttons + screenshot."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# import helpers WITHOUT running drive main: load the module source and exec only up to the drive main
import importlib.util
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game, suppress_wf4, isolate_star, back_to_map, click_first = ns['new_game'], ns['suppress_wf4'], ns['isolate_star'], ns['back_to_map'], ns['click_first']
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
        print("click 海港:", click_first(pg, ["海港"], 1200))
        pg.wait_for_timeout(900)
        st = pg.evaluate("""() => {
          const sheet = document.getElementById('loc-sheet');
          const acts = document.getElementById('loc-acts');
          const visBtns = [...document.querySelectorAll('button')].filter(x => x.offsetParent !== null).map(x => (x.textContent||'').trim().slice(0,50));
          return { sheetOn: sheet ? sheet.className : 'NO-SHEET',
                   title: (document.getElementById('loc-title')||{}).textContent,
                   actsHtml: acts ? acts.innerHTML.slice(0, 400) : 'NO-ACTS',
                   nVisBtns: visBtns.length, visBtns: visBtns.slice(0, 30) };
        }""")
        print("sheetOn:", st["sheetOn"])
        print("title:", st["title"])
        print("actsHtml:", st["actsHtml"])
        print("nVisBtns:", st["nVisBtns"])
        for t in st["visBtns"]: print("  BTN:", t)
        pg.screenshot(path=os.path.join(HERE, "qa138", "probe_offer2_sheet.png"))
        b.close()
finally:
    import subprocess, signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE2 DONE")
