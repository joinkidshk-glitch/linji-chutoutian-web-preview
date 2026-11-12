# -*- coding: utf-8 -*-
"""v20a141 BOOK141 實駕 drive141：手帳去網頁感（B 式文件夾 tab＋備忘紙＋吊牌＋印章）。
用法：/home/hatch/pwenv49/bin/python qa141/drive141.py
Mirror：工作副本 ~/workspace/linji-work141，port 8962，430x932＋430x700，?softPreview=1。
流程：UI 新遊戲 → 手帳（editable：無印章）→ 五 tab 逐個撳 → 進度／行程切換（圈跟住郁）
→ 確定行程 → 返地圖 → 再入手帳（locked：印章出）→ 返回地圖。
量度：tab 幾何／色、備忘紙三行 vs live S 值、吊牌幾何、印章計算樣式、六日可見數。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work141"
HERE = os.path.join(ROOT, "qa141")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8962
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"errors": [], "http404": [], "phases": {}}

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError("http.server died on start")
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
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

def click_exact(pg, text, wait=1200):
    ok = pg.evaluate("""(t) => {
      const els=[...document.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()===t;});
      if(!els.length) return false; els[0].click(); return true; }""", text)
    pg.wait_for_timeout(wait)
    return ok

def new_game_to_handbook(pg):
    """drive131 同款新遊戲流程，停喺手帳 editable（未確定行程）。"""
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    pg.wait_for_timeout(1000)
    on = pg.evaluate("() => { const v=document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")
    print("handbook open (editable):", on, flush=True)
    return on

def open_handbook_via_menu(pg):
    pg.locator("button:has-text('☰')").first.click(timeout=3000); pg.wait_for_timeout(900)
    ok = click_first(pg, ["手帳"], 1400)
    pg.wait_for_timeout(1000)
    on = pg.evaluate("() => { const v=document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")
    print("handbook open via menu:", ok, on, flush=True)
    return on

JS_MEASURE = """() => {
  const cs = (el, pseudo) => el ? getComputedStyle(el, pseudo || null) : null;
  const rect = el => { if(!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const S = window.S || {};
  let dual = null;
  try { dual = (typeof syncDualTracks === 'function') ? syncDualTracks(S) : null; } catch(_e) {}
  const tabs = [...document.querySelectorAll('#home-tabs .home-tab')].map(el => {
    const c = cs(el); const after = cs(el, '::after');
    return {id: el.id, text: el.textContent.trim(), on: el.classList.contains('on'),
      aria: el.getAttribute('aria-selected'), rect: rect(el),
      bg: c.backgroundColor, color: c.color, height: c.height, width: c.width,
      afterContent: after.content, afterH: after.height}; });
  const planSubs = [...document.querySelectorAll('.hsub-group[data-hsubgroup="plan"] .home-tab')].map(el => {
    const c = cs(el); const after = cs(el, '::after');
    return {id: el.id, text: el.textContent.trim(), on: el.classList.contains('on'),
      rect: rect(el), color: c.color, font: c.fontFamily.slice(0, 40), fontSize: c.fontSize,
      afterBg: (after.backgroundImage || '').slice(0, 60), afterW: after.width, afterH: after.height}; });
  const memo = document.getElementById('home-stats');
  const conf = document.getElementById('btn-confirm-plan');
  const reset = document.getElementById('btn-reset-plan');
  const tag = document.getElementById('home-back-map-tabs');
  const nb = document.getElementById('notebook');
  const days = [...document.querySelectorAll('#nb-days .day-row')].map(el => {
    const b = el.getBoundingClientRect();
    return {top: Math.round(b.top), bottom: Math.round(b.bottom),
            visibleFull: b.bottom <= window.innerHeight && b.top >= 0}; });
  const cc = conf ? cs(conf) : null;
  return {
    vh: window.innerHeight, vw: window.innerWidth,
    money: S.money, dual,
    memoText: memo ? memo.textContent.replace(/\\s+/g, ' ').trim() : null,
    memoRect: rect(memo),
    memoBg: memo ? cs(memo).backgroundImage.slice(0, 60) : null,
    chop: (()=>{ const c = document.querySelector('.memo141-chop'); return c ? {text: c.textContent, rect: rect(c)} : null; })(),
    tabs, planSubs,
    subtabGroupsOn: [...document.querySelectorAll('.hsub-group')].map(g => ({g: g.getAttribute('data-hsubgroup'), on: g.classList.contains('on')})),
    paneOn: (()=>{ const p = document.querySelector('.home-pane.on'); return p ? p.id : null; })(),
    tag: tag ? {text: tag.textContent.trim(), rect: rect(tag), bg: cs(tag).backgroundColor,
                clip: cs(tag).clipPath.slice(0, 60), visible: !!tag.offsetParent} : null,
    confirm: conf ? {text: conf.textContent.trim(), disabled: conf.disabled, locked: conf.classList.contains('is-locked'),
      rect: rect(conf), color: cc.color, fontSize: cc.fontSize, borderTop: cc.borderTopWidth + ' ' + cc.borderTopStyle + ' ' + cc.borderTopColor,
      letterSpacing: cc.letterSpacing, transform: cc.transform, bg: cc.backgroundColor} : null,
    resetVisible: reset ? (getComputedStyle(reset).display !== 'none' && !!reset.offsetParent) : null,
    geometry: {memoBottom: memo ? Math.round(memo.getBoundingClientRect().bottom) : null,
      tabsRect: rect(document.getElementById('home-tabs')),
      subtabsRect: rect(document.getElementById('home-subtabs')),
      notebookTop: nb ? Math.round(nb.getBoundingClientRect().top) : null,
      nbActionsRect: rect(document.getElementById('nb-actions'))},
    days: {count: days.length, fullVisible: days.filter(d => d.visibleFull).length, rows: days},
    homeTop: rect(document.querySelector('.home-top'))
  };
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
    pg.on("response", lambda r: http404.append({"url": r.url.split("/")[-1][:60], "status": r.status}) if r.status >= 400 else None)
    out = {}
    try:
        # ---- editable ----
        assert new_game_to_handbook(pg), "handbook did not open"
        m = pg.evaluate(JS_MEASURE)
        out["editable"] = m
        pg.screenshot(path=os.path.join(SHOTS, f"141_{tag}_editable.png"))
        print(f"[{tag}] editable memo={m['memoText']} money={m['money']} dual={m['dual']}", flush=True)
        print(f"[{tag}] tabs={[(t['text'], t['rect']['w'], t['rect']['h'], t['on']) for t in m['tabs']]}", flush=True)
        print(f"[{tag}] planSubs={[(s['text'], s['on'], s['afterBg'][:20]) for s in m['planSubs']]} days full={m['days']['fullVisible']}/{m['days']['count']}", flush=True)
        print(f"[{tag}] tag={m['tag']} confirm={m['confirm']['text']} locked={m['confirm']['locked']} resetVisible={m['resetVisible']}", flush=True)
        print(f"[{tag}] geometry={m['geometry']}", flush=True)
        # ---- 五 tab 逐個撳 ----
        tab_checks = {}
        for gid, name in [("hgroup-plan", "行程"), ("hgroup-career", "事業"), ("hgroup-status", "近況"),
                          ("hgroup-news", "消息"), ("hgroup-favor", "人情")]:
            pg.locator("#" + gid).click(timeout=3000); pg.wait_for_timeout(900)
            pane = pg.evaluate("() => { const p=document.querySelector('.home-pane.on'); return p ? p.id : null; }")
            tab_checks[name] = pane
            print(f"[{tag}] tab {name} -> pane {pane}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"141_{tag}_tab_career.png")) if False else None
        out["tabChecks"] = tab_checks
        # 返行程 tab，驗進度／行程切換（圈跟住郁）
        pg.locator("#hgroup-plan").click(timeout=3000); pg.wait_for_timeout(900)
        pg.locator("#htab-progress").click(timeout=3000); pg.wait_for_timeout(900)
        m_prog = pg.evaluate(JS_MEASURE)
        out["progressSubtab"] = {"pane": m_prog["paneOn"],
                                 "subs": [(s["text"], s["on"], bool(s["afterBg"] and s["afterBg"] != "none")) for s in m_prog["planSubs"]]}
        print(f"[{tag}] progress subtab: pane={m_prog['paneOn']} subs={out['progressSubtab']['subs']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"141_{tag}_progress.png"))
        pg.locator("#htab-plan").click(timeout=3000); pg.wait_for_timeout(900)
        m_plan = pg.evaluate(JS_MEASURE)
        out["planSubtabBack"] = [(s["text"], s["on"], bool(s["afterBg"] and s["afterBg"] != "none")) for s in m_plan["planSubs"]]
        print(f"[{tag}] back to plan subtab: {out['planSubtabBack']}", flush=True)
        # ---- 確定行程 → locked ----
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        pg.wait_for_timeout(800)
        assert open_handbook_via_menu(pg), "handbook did not reopen"
        m2 = pg.evaluate(JS_MEASURE)
        out["locked"] = m2
        pg.screenshot(path=os.path.join(SHOTS, f"141_{tag}_locked.png"))
        print(f"[{tag}] locked memo={m2['memoText']} confirm={m2['confirm']} resetVisible={m2['resetVisible']} days full={m2['days']['fullVisible']}/{m2['days']['count']}", flush=True)
        # ---- 返回地圖（吊牌） ----
        pg.locator("#home-back-map-tabs").click(timeout=3000); pg.wait_for_timeout(1200)
        back = pg.evaluate("() => { const v=document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }")
        out["backToMap"] = back
        print(f"[{tag}] back to map via tag: {back}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"141_{tag}_map.png"))
        out["errors"] = errs
        out["http404"] = http404
        print(f"[{tag}] PAGEERRORS: {errs[:5]} HTTP404: {http404[:5]}", flush=True)
    finally:
        ctx.close()
    return out

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        LOG["phases"]["932"] = run_viewport(pw, 430, 932, "932")
        LOG["phases"]["700"] = run_viewport(pw, 430, 700, "700")
    json.dump(LOG, open(os.path.join(HERE, "drive141.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("LOG qa141/drive141.json", flush=True)
finally:
    stop(srv)
