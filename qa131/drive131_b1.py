# -*- coding: utf-8 -*-
"""v20a131 B1 實駕 drive131_b1：霞姐／禮品老闆娘企立圖＋名牌（地點面板）。
用法：/home/hatch/pwenv49/bin/python qa131/drive131_b1.py
Mirror：工作副本 ~/workspace/linji-work131，port 8964，390x844，?softPreview=1。
流程：新遊戲 → 地圖 → 「全部地點」→ 金龍茶餐廳 → 核 owner img src＋名牌＋截圖
→ 返回地圖 → 「全部地點」→ 廟街禮品 → 同樣核對 → 截圖。
已知 pre-existing 404（唔計入失敗）：arc_fong_push1.*（pristine 一樣有）、
pang_siuki_sad.*（v127 表情補圖未入庫，main 都冇呢張圖）。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work131"
HERE = os.path.join(ROOT, "qa131")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8964
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"errors": [], "http404": [], "phases": {}}
PREEXIST_404 = ("arc_fong_push1", "pang_siuki_sad")

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

def new_game(pg):
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
    ok = pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")
    print("NEW GAME OK:", ok, pg.evaluate("() => window.S ? (S.dayIndex + ' ' + S.dateStr) : 'no S'"), flush=True)
    return ok

JS_OWNER = """() => {
  const img = document.getElementById('loc-owner-img118');
  const tag = document.getElementById('loc-owner-tag118');
  const sheet = document.getElementById('loc-sheet');
  const owner = document.getElementById('loc-owner118');
  return {
    sheetOn: !!sheet && sheet.classList.contains('on'),
    ownerHidden: owner ? owner.hidden : null,
    imgSrc: img ? (img.getAttribute('src') || '') : null,
    imgLoaded: img ? (img.complete && img.naturalWidth > 0) : null,
    imgNat: img ? [img.naturalWidth, img.naturalHeight] : null,
    tagText: tag ? tag.textContent : null,
    tagHidden: tag ? tag.hidden : null,
    ownerFn: (typeof locpanel118OwnerFor === 'function') ? 'fn' : (typeof window.locpanel118OwnerFor)
  };
}"""

JS_OWNER_FN = """(locId) => {
  try {
    const fn = (typeof locpanel118OwnerFor === 'function') ? locpanel118OwnerFor : null;
    if (!fn) return {ok: false, why: 'no fn'};
    return {ok: true, o: fn(locId)};
  } catch (e) { return {ok: false, why: String(e)}; }
}"""

def open_location(pg, name):
    """經「全部地點」開指定地點；如遇巧遇 overlay，先撳完佢再睇 sheet。"""
    click_first(pg, ["返回地圖"], 800)
    pg.wait_for_timeout(600)
    got = click_exact(pg, "全部地點", 1200)
    if not got:
        # 可能已經喺地圖，直接搵地點掣
        got = click_first(pg, [name], 1500)
        if got:
            return True
        return False
    pg.wait_for_timeout(800)
    got = click_first(pg, [name], 1800)
    return bool(got)

def clear_encounter(pg, max_steps=40):
    """如果有 enc79 巧遇（以 .e79-line 有文字為準，唔靠 'on' class——實測 overlay
    class 可能係空但內容已出），撳到佢消失為止；回傳有冇處理過。"""
    handled = False
    for _ in range(max_steps):
        present = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return false;
          const line = ov.querySelector('.e79-line');
          return !!(line && (line.textContent||'').trim()); }""")
        if not present:
            return handled
        handled = True
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""")
        pg.wait_for_timeout(700)
        if not clicked:
            break
    return handled

def check_owner(pg, loc_id, expect_src, expect_name, expect_sub, shot):
    # 撳入地點可能先觸發巧遇（openLoc 要等 ENC79 播完先放行）：循環清巧遇直至 sheet 開
    for _ in range(6):
        pg.wait_for_timeout(1000)
        clear_encounter(pg)
        pg.wait_for_timeout(600)
        info = pg.evaluate(JS_OWNER)
        if info['sheetOn']:
            break
    fn = None
    print(f"  {loc_id}: sheetOn={info['sheetOn']} imgSrc={info['imgSrc']} loaded={info['imgLoaded']} nat={info['imgNat']} tag={info['tagText']!r}", flush=True)
    pg.screenshot(path=os.path.join(SHOTS, shot))
    print("  SHOT", shot, flush=True)
    ok = (info['sheetOn'] and info['imgSrc'] and expect_src in info['imgSrc']
          and info['imgLoaded'] and info['tagText'] and expect_name in info['tagText']
          and expect_sub in info['tagText'])
    return {"ui": info, "fn": fn, "ok": ok}

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
        http404 = []
        def on_resp(resp):
            try:
                if resp.status >= 400:
                    http404.append({"url": resp.url.split("/")[-1][:60], "status": resp.status})
            except Exception:
                pass
        pg.on("response", on_resp)

        print("== B1 ==", flush=True)
        assert new_game(pg)
        # 圖檔直連 200＋byte 對數（先確認伺服器派得出新圖）
        for f, exp_bytes in [("assets/story/fullbody/xia_jie_base.webp", 104362),
                             ("assets/story/fullbody/gift_lady_base.webp", 151314)]:
            st, body = http_body(f)
            print(f"  file {f}: {st} {len(body)} bytes (expect {exp_bytes})", flush=True)
            assert st == 200 and len(body) == exp_bytes, f

        # 金龍茶餐廳
        assert open_location(pg, "金龍茶餐廳"), "open cafe_cha failed"
        r1 = check_owner(pg, "cafe_cha", "xia_jie_base.webp", "霞姐", "金龍茶餐廳老闆娘", "b1_cafe_cha.png")
        LOG["phases"]["B1_cafe"] = r1
        # 廟街禮品（第 2 個地點，當日額度 2/2）
        assert open_location(pg, "廟街禮品"), "open gift_shop failed"
        r2 = check_owner(pg, "gift_shop", "gift_lady_base.webp", "老闆娘", "廟街禮品檔", "b1_gift_shop.png")
        LOG["phases"]["B1_gift"] = r2

        LOG["errors"] = errs
        LOG["http404"] = http404
        new404 = [h for h in http404 if not any(p in h["url"] for p in PREEXIST_404)]
        print("PAGEERRORS:", errs, flush=True)
        print("HTTP404 all:", http404, flush=True)
        print("HTTP404 new (excl pre-existing):", new404, flush=True)
        print("B1 cafe ok:", r1["ok"], "gift ok:", r2["ok"], flush=True)
        json.dump(LOG, open(os.path.join(HERE, "drive131_b1.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("LOG qa131/drive131_b1.json", flush=True)
        b.close()
finally:
    stop(srv)
