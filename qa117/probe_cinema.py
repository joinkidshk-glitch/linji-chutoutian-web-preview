# 探查：入維港電影嗰陣彈出嘅事件鏈有幾多步、每步掣係咩。
import sys, os, subprocess, time, signal, hashlib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
PORT = 8991
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107"

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
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

def dom_click(pg, sub, selector="button"):
    return pg.evaluate("""([sub, sel]) => {
      const els=[...document.querySelectorAll(sel)].filter(x=>x.offsetParent!==null);
      const hit=els.find(x=>(x.textContent||'').includes(sub));
      if(!hit) return {found:false};
      hit.click(); return {found:true, text:hit.textContent.trim().replace(/\\s+/g,' ').slice(0,70)}; }""",
      [sub, selector])

JS_MODAL = '''() => {
  const mi = document.getElementById('modal-inner');
  const mask = document.getElementById('mask');
  const btns = [...document.querySelectorAll('#modal-btns button, #mask button')].filter(x=>x.offsetParent!==null).map(x=>x.textContent.trim());
  return { modalText: mi ? mi.innerText.slice(0, 300) : null,
    maskVisible: mask ? getComputedStyle(mask).display : null, btns };
}'''

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        pg.goto(URL); pg.wait_for_timeout(3000)
        click_first(pg, ["新遊戲"], 1500)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        click_first(pg, ["覆蓋", "確定", "確認"], 900)
        click_first(pg, ["跳過教學"], 1200)
        click_first(pg, ["開始寫手帳"], 1400)
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception:
            pass
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        print("enter:", dom_click(pg, "維港電影"))
        pg.wait_for_timeout(1200)
        for step in range(10):
            st = pg.evaluate(JS_MODAL)
            print(f"--- step {step} btns={st['btns']}")
            print("  text:", (st['modalText'] or '').replace('\n', ' | ')[:220])
            if any('只查看通告欄' in x for x in st['btns']):
                print("BOARD REACHED at step", step)
                break
            hit = pg.evaluate("""() => {
              const btns=[...document.querySelectorAll('#modal-btns button, #mask button')].filter(x=>x.offsetParent!==null);
              if(!btns.length) return null;
              const b=btns[0]; const t=(b.textContent||'').trim(); b.click(); return t; }""")
            print("  clicked first modal btn:", hit)
            if not hit:
                print("NO MODAL BTN — stop"); break
            pg.wait_for_timeout(900)
        pg.screenshot(path="qa117/shots/probe_cinema_final.png")
        b.close()
finally:
    stop(srv)
