# -*- coding: utf-8 -*-
"""v20a132 回歸 drive：S-30 通告詳情卡標題被切（v128 回歸）。
修法：.cn-issuer30v2 height:auto → 240px（還原 v116 胸口以上 crop）。
斷言（每 case）：h2 完全可見（h2 bottom ≤ frame bottom，即 clippedByFrame ≤ 0）
＋sheet body 高度 ≥120px。短 viewport 430×700＋390×700 係主戰場（真機條件），
430×932 做對照。用法：/home/hatch/pwenv49/bin/python qa132/drive132.py
[ROOT 預設工作副本；設 LINJI132_ROOT 可指去 pristine worktree 做反證]
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request

ROOT = os.environ.get("LINJI132_ROOT", "/home/hatch/workspace/linji-work132")
HERE = "/home/hatch/workspace/linji-work132/qa132"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8965
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"errors": [], "http404": [], "cases": {}}

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
    print("serve ok", cwd, "sha", sha[:12], flush=True)
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
    print("NEW GAME OK:", ok, flush=True)
    return ok

def clear_encounter(pg, max_steps=40):
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

def open_location(pg, name):
    click_first(pg, ["返回地圖"], 800)
    pg.wait_for_timeout(600)
    got = click_exact(pg, "全部地點", 1200)
    if not got:
        return bool(click_first(pg, [name], 1500))
    pg.wait_for_timeout(800)
    return bool(click_first(pg, [name], 1800))

JS_PICKS = """(locId) => {
  const gs = (window.GIGS||[]).filter(g => g && g.loc === locId);
  return gs.slice(0, 10).map(g => ({id: g.id, title: g.title}));
}"""

JS_DETAIL_OPEN = """() => {
  const m = document.getElementById('mask');
  return !!(m && m.className.includes('casting-sheet-on') && document.querySelector('.cn-issuer30v2'));
}"""

def open_gig_detail(pg, picks):
    """逐張試通告行，直至詳情卡開咗（.cn-issuer30v2 出現）。"""
    for _ in range(6):
        pg.wait_for_timeout(1000)
        clear_encounter(pg)
        pg.wait_for_timeout(600)
        sheet_on = pg.evaluate("() => { const s = document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }")
        if sheet_on:
            break
    for p in picks:
        # fragment＝《》內嘅書名（唔可以橫跨 》取 6 字，否則 "街景臨記》臨時" 對唔上）
        frag = p["title"].split("》")[0].replace("《", "")
        hit = pg.evaluate("""(frag) => {
          const els=[...document.querySelectorAll('#loc-sheet button, #loc-acts button, #loc-sheet [role=button]')].filter(e=>{
            const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').includes(frag);});
          if(!els.length) return false; els[0].click(); return true; }""", frag)
        pg.wait_for_timeout(1200)
        if hit and pg.evaluate(JS_DETAIL_OPEN):
            print("  OPENED GIG:", p["title"], flush=True)
            return p
        # 撳咗但唔係詳情卡（可能係其他 modal），撳返走再試下一張
        pg.evaluate("""() => { const b=[...document.querySelectorAll('#modal-btns button')].find(x=>(x.innerText||'').trim()==='離開'); if(b) b.click(); return true; }""")
        pg.wait_for_timeout(800)
    return None

JS_MEASURE = """() => {
  const r = s => { const el = document.querySelector(s); if(!el) return null;
    const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), bottom: Math.round(b.bottom)}; };
  const img = document.querySelector('.cn-issuer-img30v2');
  const hero = document.querySelector('.cn-issuer30v2');
  const frame = document.querySelector('.notice_sheet_frame');
  const h2 = document.querySelector('.cn-work');
  const body = document.querySelector('.notice_sheet_body');
  const fb = frame ? frame.getBoundingClientRect() : null;
  const hb = h2 ? h2.getBoundingClientRect() : null;
  return {
    vw: window.innerWidth, vh: window.innerHeight,
    modal: r('#modal'), hero: r('.cn-issuer30v2'),
    heroCssH: hero ? getComputedStyle(hero).height : null,
    img: img ? {w: Math.round(img.getBoundingClientRect().width),
                h: Math.round(img.getBoundingClientRect().height),
                src: (img.getAttribute('src')||'').split('/').pop().slice(0,40)} : null,
    cap: r('.cn-issuer-cap30v2'),
    frame: r('.notice_sheet_frame'),
    header: r('.notice_header_orange'),
    h2: h2 ? {txt: (h2.textContent||'').trim(),
              bottom: Math.round(hb.bottom),
              clippedByFrame: fb ? Math.round(hb.bottom - fb.bottom) : null} : null,
    body: body ? {h: Math.round(body.getBoundingClientRect().height),
                  scrollH: body.scrollHeight} : null,
    btnLabels: [...document.querySelectorAll('#modal-btns button')].map(b => (b.innerText||'').trim()),
  };
}"""

def check_case(pg, name, tag):
    m = pg.evaluate(JS_MEASURE)
    clip = (m.get("h2") or {}).get("clippedByFrame")
    body_h = (m.get("body") or {}).get("h")
    hero_h = (m.get("hero") or {}).get("h")
    ok = (clip is not None and clip <= 0 and body_h is not None and body_h >= 120)
    LOG["cases"][tag] = {"measure": m, "pass": ok}
    print(f"  [{tag}] heroH={hero_h} clip={clip} bodyH={body_h} -> {'PASS' if ok else 'FAIL'}", flush=True)
    pg.screenshot(path=os.path.join(SHOTS, f"132_{tag}.png"))
    return ok

def run_session(pw, vw, vh, loc_id, loc_name, tag700):
    """一個 session：開新遊戲 → 入指定地點 → 開通告詳情 → 700 高量度 → 改 932 高再量度（只限 ad_adm session）。"""
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": vw, "height": vh})
    pg.on("console", lambda m: LOG["errors"].append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: LOG["errors"].append("PAGEERROR: " + str(e)))
    pg.on("response", lambda r: LOG["http404"].append(r.url) if r.status == 404 else None)
    results = {}
    try:
        assert new_game(pg), "new game failed"
        pg.evaluate("""() => { if (window.S) { S.fame = 30; S.acting = 60; S.vocal = 60;
          S.stage = 60; S.charm = 100; S.looks = 100; S.stamina = 110; S.iq = 60;
          S.industryCredit = 21; } return true; }""")
        assert open_location(pg, loc_name), f"open loc {loc_name} failed"
        picks = pg.evaluate(JS_PICKS, loc_id)
        print(f"  {loc_id} picks:", json.dumps(picks, ensure_ascii=False), flush=True)
        assert picks, f"no gigs for {loc_id}"
        opened = open_gig_detail(pg, picks)
        assert opened, f"could not open any {loc_id} gig detail"
        results[tag700] = check_case(pg, opened["title"], tag700)
        return pg, br, results
    except Exception:
        br.close()
        raise

def main():
    from playwright.sync_api import sync_playwright
    srv = serve(ROOT)
    all_ok = True
    try:
        with sync_playwright() as pw:
            # Case A: 430×700 方樂怡（ad_adm）＋ resize 430×932 對照
            pg, br, res = run_session(pw, 430, 700, "ad_adm", "金鐘創意", "430x700_adm")
            all_ok &= all(res.values())
            pg.set_viewport_size({"width": 430, "height": 932})
            pg.wait_for_timeout(800)
            all_ok &= check_case(pg, "control", "430x932_adm")
            br.close()
            # Case B: 390×700 沈卓衡（tvb_longmen）
            pg, br, res = run_session(pw, 390, 700, "tvb_longmen", "星河電視台", "390x700_tvb")
            all_ok &= all(res.values())
            br.close()
    finally:
        stop(srv)
    print("ERRORS:", json.dumps(LOG["errors"][:10], ensure_ascii=False), flush=True)
    print("404:", json.dumps(LOG["http404"][:10], ensure_ascii=False), flush=True)
    json.dump(LOG, open(os.path.join(HERE, "drive132.json"), "w"), ensure_ascii=False, indent=1)
    print("DRIVE132", "PASS" if all_ok else "FAIL", flush=True)
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
