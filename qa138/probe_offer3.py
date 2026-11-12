"""probe3: click button[data-loc=tvb_harbour] directly; dump sheet + story-play + S state."""
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
        pg.on("console", lambda m: print("CONSOLE:", m.type, m.text[:160]) if m.type in ("error", "warning") else None)
        new_game(pg)
        pg.evaluate("() => { const S = window.S; S.dayIndex = 400; S.exodusFenSeeded=true; S.exodusFenFired=false; }")
        suppress_wf4(pg); isolate_star(pg, "__none__"); back_to_map(pg)
        # click the exact map-list button by data-loc
        btn = pg.locator('button[data-loc="tvb_harbour"]')
        print("data-loc btn count:", btn.count(), "visible:", btn.first.is_visible() if btn.count() else None)
        if btn.count():
            btn.first.click(timeout=3000)
        pg.wait_for_timeout(1000)
        st = pg.evaluate("""() => {
          const sheet = document.getElementById('loc-sheet');
          const acts = document.getElementById('loc-acts');
          const sp = document.querySelector('.story-play');
          return { sheetClass: sheet ? sheet.className : 'NO-SHEET',
                   title: (document.getElementById('loc-title')||{}).textContent,
                   acts: acts ? [...acts.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim().slice(0,50)) : 'NO-ACTS',
                   storyActive: !!sp,
                   atLoc: (typeof S!=='undefined' && S) ? (S.atLoc||S.curLoc||null) : null,
                   travel: (typeof S!=='undefined' && S) ? JSON.stringify(S.travel||S.travelUsed||null) : null };
        }""")
        print("STATE:", st)
        pg.screenshot(path=os.path.join(HERE, "qa138", "probe_offer3_sheet.png"))
        b.close()
finally:
    import subprocess, signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE3 DONE")
