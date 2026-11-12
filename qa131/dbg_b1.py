# -*- coding: utf-8 -*-
"""B1 debug：逐步截圖＋dump 狀態，睇下「全部地點」→ 金龍茶餐廳 點解開唔到 sheet。"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work131"
HERE = os.path.join(ROOT, "qa131")
SHOTS = os.path.join(HERE, "shots")
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8965
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    st, body = http_body("index.html")
    assert st == 200
    print("serve ok", flush=True)
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

def dump(pg, tag):
    st = pg.evaluate("""() => {
      const vis = sel => { const e = document.querySelector(sel); return e ? {cls: e.className, hidden: e.hidden, txt: (e.textContent||'').slice(0,80)} : null; };
      const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null)
        .map(b => (b.textContent||'').trim()).filter(Boolean).slice(0, 40);
      return {sheet: vis('#loc-sheet'), owner: vis('#loc-owner118'),
              allLocBtn: btns.filter(t => t.includes('全部地點')),
              mapOn: !!document.getElementById('v-map')?.classList.contains('on'),
              visibleBtns: btns};
    }""")
    print(f"--- {tag} ---", json.dumps(st, ensure_ascii=False)[:1200], flush=True)
    pg.screenshot(path=os.path.join(SHOTS, f"dbg_b1_{tag}.png"))
    return st

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e, flush=True))
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
        dump(pg, "map")
        # 撳「全部地點」
        r = pg.evaluate("""() => {
          const els=[...document.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
            const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()==='全部地點';});
          if(!els.length) return 'NOT FOUND';
          els[0].click(); return 'clicked'; }""")
        print("全部地點 click:", r, flush=True)
        pg.wait_for_timeout(1200)
        dump(pg, "allloc")
        # 列出「全部地點」list 入面嘅掣
        lst = pg.evaluate("""() => {
          const els=[...document.querySelectorAll('button')].filter(b => b.offsetParent !== null)
            .map(b => (b.textContent||'').trim()).filter(Boolean);
          return els; }""")
        print("visible buttons after 全部地點:", lst, flush=True)
        # 撳金龍茶餐廳
        r2 = pg.evaluate("""() => {
          const els=[...document.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
            const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').includes('金龍');});
          if(!els.length) return 'NOT FOUND';
          els[0].click(); return 'clicked: ' + els[0].innerText.slice(0,40); }""")
        print("金龍 click:", r2, flush=True)
        pg.wait_for_timeout(2000)
        dump(pg, "cafe")
        b.close()
finally:
    stop(srv)
