"""Explore the linji game page: load ?softPreview=1, dump start state."""
import sys, time
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8123/index.html?softPreview=1"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/explore118"

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell",
                          args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 390, "height": 844})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: errors.append("CONSOLE-" + m.type + ": " + m.text) if m.type in ("error",) else None)
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(2500)
    pg.screenshot(path=OUT + "_start.png")
    state = pg.evaluate("""() => {
      const vis = (el) => el && el.offsetParent !== null;
      const btns = Array.from(document.querySelectorAll('button')).filter(vis).slice(0, 60)
        .map(b => (b.id ? '#' + b.id : '') + ' :: ' + (b.textContent || '').trim().slice(0, 40));
      const views = Array.from(document.querySelectorAll('section.view, .view')).map(v => v.id + ':' + (v.classList.contains('on') ? 'on' : 'off'));
      return { title: document.title, views, btns,
        bodyText: (document.body.innerText || '').slice(0, 600),
        hasS: typeof S !== 'undefined', dayIndex: (typeof S !== 'undefined' && S) ? S.dayIndex : null,
        atLoc: (typeof atLoc !== 'undefined') ? atLoc : null };
    }""")
    print(state)
    print("ERRORS:", errors[:10])
    b.close()
