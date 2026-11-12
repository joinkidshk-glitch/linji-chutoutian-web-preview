# -*- coding: utf-8 -*-
"""B1 debug 2：睇金龍茶餐廳掣嘅 HTML＋撳完之後嘅完整狀態。"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work131"
HERE = os.path.join(ROOT, "qa131")
SHOTS = os.path.join(HERE, "shots")
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8966
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
        # 睇金龍茶餐廳掣嘅 HTML
        html = pg.evaluate("""() => {
          const btns=[...document.querySelectorAll('button')].filter(b=> (b.textContent||'').includes('金龍'));
          return btns.map(b => ({tag: b.tagName, cls: b.className, id: b.id,
            onclick: (b.getAttribute('onclick')||'').slice(0,120),
            rect: (()=>{const r=b.getBoundingClientRect(); return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];})(),
            html: b.outerHTML.slice(0,300)}));
        }""")
        print("金龍掣:", json.dumps(html, ensure_ascii=False), flush=True)
        # 用 Playwright locator 撳佢
        loc = pg.locator("button:has-text('金龍茶餐廳')")
        print("locator count:", loc.count(), flush=True)
        loc.first.click(timeout=3000)
        pg.wait_for_timeout(2500)
        st = pg.evaluate("""() => {
          const q = s => { const e = document.querySelector(s); return e ? {cls: e.className, on: e.classList.contains('on'), txt: (e.textContent||'').slice(0,120)} : null; };
          return {sheet: q('#loc-sheet'), owner: q('#loc-owner118'),
                  ownerImg: (()=>{const i=document.getElementById('loc-owner-img118'); return i ? {src: i.getAttribute('src'), loaded: i.complete && i.naturalWidth>0, nat: [i.naturalWidth, i.naturalHeight]} : null;})(),
                  ownerTag: (()=>{const t=document.getElementById('loc-owner-tag118'); return t ? t.textContent : null;})(),
                  modal: q('#modal'), mask: q('#mask'),
                  enc: q('#enc79-overlay'),
                  toast: (()=>{const t=document.querySelector('.toast'); return t ? t.textContent.slice(0,100) : null;})(),
                  travel: (window.S && S.travel114) ? S.travel114 : null};
        }""")
        print("撳完金龍:", json.dumps(st, ensure_ascii=False), flush=True)
        pg.screenshot(path=os.path.join(SHOTS, "dbg_b1_cafe2.png"))
        print("SHOT dbg_b1_cafe2.png", flush=True)
        b.close()
finally:
    stop(srv)
