# -*- coding: utf-8 -*-
"""v20a143 B3 對照 probe：鎖定態 scrollTop=0 嗰陣，700px 一屏真見幾多日。
clip-aware 可見定義：一行真見＝rect.top >= notebook 頂 ＋ rect.bottom <= nb-actions 頂
（唔計俾 sticky footer 遮住／俾 notebook 捲走嗰啲）。跑兩次：工作副本 vs pristine main，
差值就係 B3 慳位嘅實效。
用法：/home/hatch/pwenv49/bin/python qa143/probe143_b3.py <root> <port>
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = sys.argv[1]
PORT = int(sys.argv[2])
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    st, body = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5).read(), None
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def click_first(pg, texts, wait=1000):
    for t in texts:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

JS = """() => {
  const nb = document.getElementById('notebook');
  nb.scrollTop = 0;
  const nbR = nb.getBoundingClientRect();
  const actR = document.getElementById('nb-actions').getBoundingClientRect();
  const conf = document.getElementById('btn-confirm-plan');
  const c = getComputedStyle(conf);
  const rows = [...document.querySelectorAll('#nb-days .day-row')].map(el => {
    const b = el.getBoundingClientRect();
    return {text: (el.textContent||'').replace(/\\s+/g,' ').trim().slice(0,12),
      top: Math.round(b.top), bottom: Math.round(b.bottom),
      trulyVisible: b.top >= Math.round(nbR.top) && b.bottom <= Math.round(actR.top),
      partiallyVisible: b.bottom > Math.round(nbR.top) && b.top < Math.round(actR.top)}; });
  return {vh: window.innerHeight, notebookTop: Math.round(nbR.top),
    nbActionsTop: Math.round(actR.top), nbActionsH: Math.round(actR.height),
    stamp: {text: conf.textContent.trim(), fontSize: c.fontSize, h: Math.round(conf.getBoundingClientRect().height),
      top: Math.round(conf.getBoundingClientRect().top), bottom: Math.round(conf.getBoundingClientRect().bottom)},
    rows, fullCount: rows.filter(r => r.trulyVisible).length,
    partialCount: rows.filter(r => r.partiallyVisible && !r.trulyVisible).length};
}"""

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        for (w, h, tag) in [(430, 932, "932"), (430, 700, "700")]:
            ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"]).new_context(
                viewport={"width": w, "height": h}, device_scale_factor=2,
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(URL); pg.wait_for_timeout(3000)
            click_first(pg, ["新遊戲"], 1500)
            pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
              if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
            pg.wait_for_timeout(1200)
            click_first(pg, ["覆蓋", "確定", "確認"], 900)
            click_first(pg, ["跳過教學"], 1200)
            click_first(pg, ["開始寫手帳"], 1400)
            pg.wait_for_timeout(1000)
            # editable 先量一次（scrollTop=0）
            ed = pg.evaluate(JS)
            # 確定行程 → locked，經 menu 重入
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
            click_first(pg, ["確定出發"], 1500)
            for _ in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                    break
            pg.wait_for_timeout(800)
            pg.locator("button:has-text('☰')").first.click(timeout=3000); pg.wait_for_timeout(900)
            click_first(pg, ["手帳"], 1400)
            pg.wait_for_timeout(1000)
            lk = pg.evaluate(JS)
            print(f"[{tag}] ROOT={ROOT}", flush=True)
            print(f"[{tag}] editable: full={ed['fullCount']} partial={ed['partialCount']} rows={[(r['text'], r['top'], r['bottom'], r['trulyVisible']) for r in ed['rows']]}", flush=True)
            print(f"[{tag}] locked: full={lk['fullCount']} partial={lk['partialCount']} stamp={lk['stamp']} nbActionsH={lk['nbActionsH']} rows={[(r['text'], r['top'], r['bottom'], r['trulyVisible']) for r in lk['rows']]}", flush=True)
            print(f"[{tag}] errors={errs}", flush=True)
            ctx.close()
finally:
    stop(srv)
