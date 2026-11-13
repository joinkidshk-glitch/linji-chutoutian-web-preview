#!/usr/bin/env python3
"""v20a161 probe: measure .start-intro vs #start-standee face geometry on the start screen.
Usage: probe161.py [root] [port] [tag]
Loads ?softPreview=1, waits for the standee image, measures rects of the start-screen
elements at 390x844 / 390x932 / 390x700, screenshots full page + standee element.
Saves qa161/probe_<tag>.json + qa161/shots161/*_<tag>.png under root.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1]
PORT = int(sys.argv[2])
TAG = sys.argv[3] if len(sys.argv) > 3 else "pristine"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = os.path.join(ROOT, "qa161", "shots161")
os.makedirs(SHOTS, exist_ok=True)
VIEWPORTS = [(390, 844), (390, 932), (390, 700)]
MEASURE_JS = """() => {
  const r = (sel) => { const el = document.querySelector(sel);
    if (!el) return null;
    const b = el.getBoundingClientRect();
    return {x: Math.round(b.x*10)/10, y: Math.round(b.y*10)/10,
            w: Math.round(b.width*10)/10, h: Math.round(b.height*10)/10,
            right: Math.round(b.right*10)/10, bottom: Math.round(b.bottom*10)/10}; };
  const intro = document.querySelector('.start-intro');
  let textBox = null;
  if (intro) {
    // glyph-level box: union of text-node ranges (excludes padding / fog halo)
    const range = document.createRange(); range.selectNodeContents(intro);
    const rs = [...range.getClientRects()].map(b => ({x: Math.round(b.x*10)/10, y: Math.round(b.y*10)/10,
      w: Math.round(b.width*10)/10, h: Math.round(b.height*10)/10,
      right: Math.round(b.right*10)/10, bottom: Math.round(b.bottom*10)/10}));
    textBox = rs;
    const cs = getComputedStyle(intro);
    var introStyle = {maxWidth: cs.maxWidth, marginLeft: cs.marginLeft, marginRight: cs.marginRight,
      textAlign: cs.textAlign, padding: cs.padding};
  }
  const st = document.querySelector('#start-standee');
  return {
    intro: r('.start-intro'), introText: textBox, introStyle: (typeof introStyle !== 'undefined' ? introStyle : null),
    standee: r('#start-standee'),
    standeeNat: st ? {w: st.naturalWidth, h: st.naturalHeight} : null,
    title: r('.start-title'), sub: r('.start-sub'),
    head: r('.start-head'), menu: r('.start-menu'),
    btnNew: r('#btn-new'), softTip: r('#start-soft-tip'),
    inner: r('.start-inner'), viewH: window.innerHeight, viewW: window.innerWidth,
    scrollH: document.querySelector('.start-inner') ? document.querySelector('.start-inner').scrollHeight : null,
    clientH: document.querySelector('.start-inner') ? document.querySelector('.start-inner').clientHeight : null,
  };
}"""
srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
results = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        for w, h in VIEWPORTS:
            ctx = b.new_context(viewport={"width": w, "height": h})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1")
            pg.wait_for_timeout(1500)
            # wait for standee image to load
            try:
                pg.wait_for_function("() => { const s = document.querySelector('#start-standee'); return s && s.naturalWidth > 0; }", timeout=8000)
            except Exception:
                pass
            pg.wait_for_timeout(500)
            rec = {"viewport": [w, h], "pageerrors": errs}
            rec["geom"] = pg.evaluate(MEASURE_JS)
            pg.screenshot(path=f"{SHOTS}/start_{w}x{h}_{TAG}.png")
            try:
                pg.locator("#start-standee").screenshot(path=f"{SHOTS}/standee_{w}x{h}_{TAG}.png")
            except Exception as e:
                rec["standeeShotErr"] = str(e)
            results.append(rec)
            print(w, h, json.dumps(rec["geom"], ensure_ascii=False))
            ctx.close()
        b.close()
finally:
    srv.terminate()
with open(os.path.join(ROOT, "qa161", f"probe_{TAG}.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("saved qa161/probe_%s.json" % TAG)
