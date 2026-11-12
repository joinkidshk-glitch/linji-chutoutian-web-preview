# -*- coding: utf-8 -*-
"""v20a145 pre-fix probe：量度現況（改之前）——700 鎖定態幾何＋各 pane 底色。
用法：/home/hatch/pwenv49/bin/python qa145/probe145_pre.py
Mirror：工作副本 ~/workspace/linji-work145，port 8965，430x932＋430x700，?softPreview=1。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work145"
HERE = os.path.join(ROOT, "qa145")
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
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    assert st == 200 and sha == exp, "served index mismatch"
    print("serve ok sha", sha[:12], flush=True)
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
                        el.scroll_into_view_if_needed(timeout=2000)
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

def new_game_to_handbook(pg):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    pg.wait_for_timeout(1000)
    return pg.evaluate("() => { const v=document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")

def open_handbook_via_menu(pg):
    pg.locator("button:has-text('☰')").first.click(timeout=3000); pg.wait_for_timeout(900)
    ok = click_first(pg, ["手帳"], 1400)
    pg.wait_for_timeout(1000)
    on = pg.evaluate("() => { const v=document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")
    return ok and on

JS_LOCKED = """() => {
  const rect = el => { if(!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const cs = el => el ? getComputedStyle(el) : null;
  const nb = document.getElementById('notebook');
  const nbR = nb ? nb.getBoundingClientRect() : null;
  const actR = document.getElementById('nb-actions').getBoundingClientRect();
  const vis = el => !!el && !!el.offsetParent;
  const dayRows = [...document.querySelectorAll('#nb-days .day-row')].map(el => {
    const b = el.getBoundingClientRect();
    return {text: (el.textContent||'').replace(/\\s+/g,' ').trim().slice(0,28),
            top: Math.round(b.top), bottom: Math.round(b.bottom),
            full: nbR && b.top >= Math.round(nbR.top) && b.bottom <= Math.round(actR.top)}; });
  const conf = document.getElementById('btn-confirm-plan');
  const cc = cs(conf);
  const parts = {};
  for (const [k, sel] of [['title','#nb-plan-title'],['mode','#nb-plan-mode'],['range','#nb-range'],
      ['quick','#nb-quick'],['days','#nb-days'],['stress','#nb-live-stress'],
      ['teach','#plan-teach105'],['right','#nb-right'],['actions','#nb-actions']]) {
    const el = document.querySelector(sel);
    parts[k] = el ? {rect: rect(el), display: cs(el).display, visible: vis(el),
      text: (el.textContent||'').replace(/\\s+/g,' ').trim().slice(0,40)} : null;
  }
  return {vh: window.innerHeight, notebookTop: nbR ? Math.round(nbR.top) : null,
    nbActionsTop: Math.round(actR.top), nbActionsH: Math.round(actR.height),
    stamp: conf ? {text: conf.textContent.trim(), fontSize: cc.fontSize, rect: rect(conf),
      borderTop: cc.borderTopWidth+' '+cc.borderTopStyle+' '+cc.borderTopColor} : null,
    parts, days: dayRows, fullCount: dayRows.filter(d=>d.full).length};
}"""

JS_PANE_BG = """() => {
  const out = {};
  for (const p of document.querySelectorAll('.home-pane')) {
    const js = p.querySelector('.journal-scroll, .ledger-wrap');
    const b = js ? js.getBoundingClientRect() : p.getBoundingClientRect();
    out[p.id] = {on: p.classList.contains('on'),
      bg: js ? getComputedStyle(js).backgroundColor : getComputedStyle(p).backgroundColor,
      bgImage: js ? (getComputedStyle(js).backgroundImage||'').slice(0,60) : '',
      rect: {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)},
      text: (p.textContent||'').replace(/\\s+/g,' ').trim().slice(0,60)};
  }
  return out;
}"""

def run_viewport(pw, width, height, tag):
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"]).new_context(
        viewport={"width": width, "height": height}, device_scale_factor=2,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
    http404 = []
    pg.on("response", lambda r: http404.append(r.url.split("/")[-1][:60]) if r.status >= 400 else None)
    out = {}
    try:
        assert new_game_to_handbook(pg), "handbook did not open"
        # 鎖定：確定行程
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        pg.wait_for_timeout(800)
        assert open_handbook_via_menu(pg), "handbook did not reopen"
        pg.evaluate("() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=0; }")
        pg.wait_for_timeout(300)
        m = pg.evaluate(JS_LOCKED)
        out["locked"] = m
        print(f"[{tag}] LOCKED vh={m['vh']} nbTop={m['notebookTop']} actTop={m['nbActionsTop']} actH={m['nbActionsH']} full={m['fullCount']}/7 stamp={m['stamp']}", flush=True)
        for k, v in m["parts"].items():
            print(f"[{tag}]   {k}: {v}", flush=True)
        for d in m["days"]:
            print(f"[{tag}]   day {d['text'][:12]:14s} top={d['top']} bottom={d['bottom']} full={d['full']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"pre_{tag}_locked.png"))
        # 各 pane 底色：逐個大 tab＋subtab 切過去量 computed bg
        panes = {}
        for gid, subs in [("hgroup-plan", ["htab-plan", "htab-progress"]),
                          ("hgroup-career", ["htab-works", "htab-awards", "htab-memory"]),
                          ("hgroup-status", ["htab-ledger", "htab-inv"]),
                          ("hgroup-news", ["htab-rumor", "htab-clippings"]),
                          ("hgroup-favor", ["htab-debt", "htab-people"])]:
            pg.locator("#" + gid).click(timeout=3000); pg.wait_for_timeout(800)
            for bid in subs:
                try:
                    pg.locator("#" + bid).click(timeout=3000)
                except Exception:
                    print(f"[{tag}]   subtab {bid} click FAIL (hidden?)", flush=True); continue
                pg.wait_for_timeout(700)
                bg = pg.evaluate(JS_PANE_BG)
                on = [k for k, v in bg.items() if v["on"]]
                panes[bid] = {k: v for k, v in bg.items() if v["on"]}
                print(f"[{tag}] PANE {bid}: on={on} bg={panes[bid]}", flush=True)
                pg.screenshot(path=os.path.join(SHOTS, f"pre_{tag}_pane_{bid}.png"))
        out["panes"] = panes
        out["errors"] = errs; out["http404"] = http404
        print(f"[{tag}] PAGEERRORS: {errs[:5]} HTTP404: {http404[:5]}", flush=True)
    finally:
        ctx.close()
    return out

LOG = {"phases": {}}
srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        LOG["phases"]["932"] = run_viewport(pw, 430, 932, "932")
        LOG["phases"]["700"] = run_viewport(pw, 430, 700, "700")
    json.dump(LOG, open(os.path.join(HERE, "probe145_pre.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("LOG qa145/probe145_pre.json", flush=True)
finally:
    stop(srv)
