import os
from playwright.sync_api import sync_playwright
ROOT = "/home/hatch/workspace/linji-work170"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
OUT = os.path.join(ROOT, "samples170")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    for name, h in [("sample_liao_card_932", 932), ("sample_liao_card_700", 700)]:
        pg = b.new_page(viewport={"width": 430, "height": h})
        pg.goto("file://" + os.path.join(ROOT, "sample_liao_card.html"))
        pg.wait_for_timeout(600)
        pg.screenshot(path=os.path.join(OUT, name + ".png"), full_page=True)
        print(name, "ok")
    b.close()
