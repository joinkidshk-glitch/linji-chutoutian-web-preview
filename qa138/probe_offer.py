"""probe: seed exodus flags, enter tvb_harbour, dump S flags + sheet action buttons."""
import sys
sys.path.insert(0, 'qa138')
from drive138 import new_game, suppress_wf4, isolate_star, back_to_map, click_first, serve, ROOT, PORT, EXE
from playwright.sync_api import sync_playwright
srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        new_game(pg)
        print("after new_game:", pg.evaluate("() => ({day: S.dayIndex, seeded: S.exodusFenSeeded, fired: S.exodusFenFired})"))
        pg.evaluate("() => { const S = window.S; S.dayIndex = 400; S.exodusFenSeeded=true; S.exodusFenFired=false; }")
        print("after seed:", pg.evaluate("() => ({day: S.dayIndex, seeded: S.exodusFenSeeded, fired: S.exodusFenFired})"))
        suppress_wf4(pg)
        isolate_star(pg, "__none__")
        back_to_map(pg)
        print("loc click:", click_first(pg, ["海港"], 1200))
        pg.wait_for_timeout(800)
        print("after seed+enter:", pg.evaluate("() => ({day: S.dayIndex, seeded: S.exodusFenSeeded, fired: S.exodusFenFired})"))
        btns = pg.evaluate("""() => {
          const acts = document.getElementById('loc-acts');
          if (!acts) return {noActs: true};
          return [...acts.querySelectorAll('button')].filter(x => x.offsetParent !== null).map(x => x.textContent.trim().slice(0, 60));
        }""")
        print("sheet buttons:", btns)
        print("loc title:", pg.evaluate("() => (document.getElementById('loc-title')||{}).textContent"))
        b.close()
finally:
    stop(srv)
