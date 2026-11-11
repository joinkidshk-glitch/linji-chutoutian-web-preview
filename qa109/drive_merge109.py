# -*- coding: utf-8 -*-
"""v20a109 合併版額外檢查：同一 save 先後行 B 線（人情頁＋hero tier 切換）
再入 A 線（C1 對話舞台），確認 bust109HeroSrc() tier 切換唔干擾
dlg108FitApply 身高比。另補：人情頁全列表分段截圖、404 URL 實名記錄。
用法：/home/hatch/pwenv49/bin/python qa109/drive_merge109.py
產出：qa109/shots/merge_*.png ＋ qa109/merge_check109.json
"""
import sys, os, json, subprocess, time, signal, hashlib, base64, urllib.request
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8963
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107&nocache=109m"
LOG = {"errors": [], "failed_requests": [], "hero": {}, "people": {}, "c1": {}, "hero_after": {}}

def http_get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} taken?)")
    st, body = http_get("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    if st != 200 or sha != exp:
        raise RuntimeError(f"served index mismatch: {st} sha={sha[:12]} expected={exp[:12]}")
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
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

JS_SETUP_STATE = """() => {
  S.npcs = S.npcs || {};
  for (const id of ["colleague","director","stylist","rival","reporter","agent"]) S.npcs[id] = 55;
  S.stars = S.stars || {};
  const favs = {luk_baakyin:0, liu_bingxing:15, ngai_wingnaam:30, yip_manji:50,
    mak_zhendong:80, lok_gasing:5, pang_siuki:25, chung_choning:45, gu_mingfai:70,
    so_jiyan:10, chai_zanhoi:35, ching_tinlok:60};
  for (const [id, fav] of Object.entries(favs))
    S.stars[id] = {fav, met:true, seen:1, lastDay:-999, stage:0, beatsDone:{},
                   poolSeen:{}, workedWith:false, homeVisits:0, homeVisitDay:-1};
  S.stars.so_jiyan.met = false;
  return true;
}"""

JS_ROWS = """() => {
  const box = document.getElementById('people-list');
  if (!box) return {error:'no people-list'};
  const rows = [];
  let section = '';
  for (const el of box.children) {
    if (el.tagName === 'H3') { section = el.textContent.trim(); continue; }
    if (!el.classList || !el.classList.contains('people-row')) continue;
    const img = el.querySelector('img');
    const b = el.querySelector('b');
    const s = img ? (img.getAttribute('src')||'') : '';
    rows.push({section, name: b ? b.textContent.trim() : '',
      srcKind: !img ? 'none' : s.startsWith('data:image/webp') ? 'webp-data'
        : s.startsWith('data:image/jpeg') ? 'jpeg-data' : s.split('/').pop().split('?')[0],
      nw: img ? img.naturalWidth : null, nh: img ? img.naturalHeight : null});
  }
  return {rows};
}"""

def hero_src_sha(pg):
    src = pg.evaluate("""() => { const im = document.getElementById('home-awi');
      return im ? (im.getAttribute('src')||'') : ''; }""")
    if src.startswith("data:"):
        raw = base64.b64decode(src.split(",", 1)[1])
        return hashlib.sha256(raw).hexdigest(), len(raw), src[:30]
    return src, 0, src[:30]

def set_tier(pg, n_lead, fame):
    r = pg.evaluate("""(arg) => {
      const leads = (typeof GIGS !== 'undefined' ? GIGS : [])
        .filter(g => g && /lead/.test(String(g.roleScale || ''))).slice(0, 3).map(g => g.id);
      S.flags = S.flags || {};
      for (const k of Object.keys(S.flags)) if (k.indexOf('done_') === 0) delete S.flags[k];
      for (let i = 0; i < arg.n; i++) S.flags['done_' + leads[i]] = 1;
      S.fame = arg.fame;
      return { leads }; }""", {"n": n_lead, "fame": fame})
    return (3 if (n_lead >= 3 and fame >= 70) else (2 if n_lead >= 1 else 0)), r

def open_journal(pg):
    click_first(pg, ["☰"], 900)
    pg.evaluate("""() => { const b = document.querySelector('[data-m="journal"]');
      if (b) b.click(); }""")
    pg.wait_for_timeout(1200)

def open_people(pg):
    open_journal(pg)
    pg.evaluate("""() => { const b = document.getElementById('htab-people');
      if (b) b.click(); }""")
    pg.wait_for_timeout(1200)
    return pg.evaluate(JS_ROWS)

JS_STORY = '''() => {
  const sp = document.querySelector('.story-play');
  if (!sp) return { active: false };
  const speaker = document.querySelector('.story-play .sp-speaker');
  const line = document.querySelector('.story-play .sp-line');
  const stage = document.querySelector('.story-play .sp-stage');
  return { active: true, speaker: speaker ? speaker.textContent : null,
    charHVar: stage ? (getComputedStyle(stage).getPropertyValue('--dlg108-char-h') || '').trim() : null,
    line: line ? line.textContent : null };
}'''

JS_MEASURE_IMG = '''(sel) => {
  const out = [];
  document.querySelectorAll(sel).forEach(im => {
    const r = im.getBoundingClientRect();
    out.push({ id: im.dataset.dlgId || im._sid106 || null,
      src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
      top: +(r.top.toFixed(1)), bottom: +(r.bottom.toFixed(1)), height: +(r.height.toFixed(1)),
      inlineH: im.style.height || null,
      nat: (im.naturalWidth||0) + 'x' + (im.naturalHeight||0) });
  });
  return out;
}'''

def next_step(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: LOG["errors"].append("pageerror: " + str(e)))
        pg.on("console", lambda m: LOG["errors"].append("console.error: " + m.text) if m.type == "error" else None)
        pg.on("response", lambda r: LOG["failed_requests"].append(f"{r.status} {r.url.split('/127.0.0.1:8963/')[-1]}") if r.status >= 400 else None)
        pg.on("requestfailed", lambda r: LOG["failed_requests"].append("FAILED " + r.url.split('/127.0.0.1:8963/')[-1]))

        print("new game:", new_game(pg))
        print("setup state:", pg.evaluate(JS_SETUP_STATE))

        # ---- B 線先行：hero tier 2 ----
        exp_tier, _ = set_tier(pg, 1, 0)
        open_journal(pg)
        sha, nbytes, prefix = hero_src_sha(pg)
        crop = json.load(open(os.path.join(ROOT, "qa109b", "crop109.json")))
        want = next(v["webp_sha256"] for v in crop.values() if v["stem"] == "awi_s2")
        LOG["hero"] = {"tier_set": 2, "expected_tier": exp_tier, "sha_match_s2": sha == want,
                       "prefix": prefix, "bytes": nbytes}
        print(f"hero tier2: exp={exp_tier} sha_match_s2={sha == want} prefix={prefix}")
        pg.screenshot(path=f"{SHOTS}/merge_hero_t2.png")

        # ---- B 線：人情頁全列表（分段截圖）----
        people = open_people(pg)
        LOG["people"] = people
        rows = people.get("rows", [])
        print(f"people rows: {len(rows)} webp={sum(1 for r in rows if r['srcKind']=='webp-data')}")
        pg.screenshot(path=f"{SHOTS}/merge_people_full.png", full_page=True)
        total_h = pg.evaluate("() => document.documentElement.scrollHeight")
        for i, frac in enumerate([0, 0.38, 0.76]):
            pg.evaluate("(y) => window.scrollTo(0, y)", int(total_h * frac))
            pg.wait_for_timeout(400)
            pg.screenshot(path=f"{SHOTS}/merge_people_seg{i+1}.png")
        pg.evaluate("() => window.scrollTo(0, 0)")

        # ---- A 線：同一 save 入 C1 對話（hero 仍係 tier 2 狀態）----
        print("back to map:", click_first(pg, ["返回地圖"], 1200))
        print("enter agency:", click_first(pg, ["何生事務所"], 1800))
        pg.wait_for_timeout(800)
        st = pg.evaluate(JS_STORY)
        if not st["active"]:
            pg.evaluate("() => { const b = document.getElementById('map-progress-btn'); if (b) b.click(); }")
            pg.wait_for_timeout(1200)
            print("C1 play button:", pg.evaluate('''() => { const b = document.querySelector('[data-prog77-play="C1"]');
              if (b) { b.click(); return true; } return false; }'''))
            pg.wait_for_timeout(1500)
        c1 = {"found": False}
        for step in range(15):
            info = pg.evaluate(JS_STORY)
            chars = pg.evaluate(JS_MEASURE_IMG, ".dlg106-char") if info["active"] else []
            if info["active"] and len(chars) == 2:
                awi = chars[0]
                c1 = {"found": True, "step": step, "speaker": info.get("speaker"),
                      "line": (info.get("line") or "")[:60], "charHVar": info.get("charHVar"),
                      "chars": chars,
                      "awi_declared_scale": pg.evaluate("() => (window.DLG109 && typeof window.DLG109.scale==='function') ? window.DLG109.scale('awi') : null"),
                      "ho_declared_scale": pg.evaluate("() => (window.DLG109 && typeof window.DLG109.scale==='function') ? window.DLG109.scale('ho_sang') : null"),
                      "awi_height_ratio_vs_baseline487": round(awi["height"] / 487.2, 3)}
                print(f" C1[{step}] spk={info.get('speaker')} charHVar={info.get('charHVar')} chars={[(c['id'], c['src'], c['height'], c['top'], c['inlineH']) for c in chars]} awi_scale={c1['awi_declared_scale']} ratio={c1['awi_height_ratio_vs_baseline487']}")
                pg.screenshot(path=f"{SHOTS}/merge_c1_awixho_t2.png")
                break
            if info.get("choices"):
                print(" C1 choices hit before 2-char step, stop"); break
            if not next_step(pg):
                print(" C1 no next button, stop"); break
            pg.wait_for_timeout(500)
        LOG["c1"] = c1

        # ---- 對話後 hero 仲係唔係 tier 2 ----
        for _ in range(20):
            st = pg.evaluate(JS_STORY)
            if not st["active"]:
                break
            if not next_step(pg):
                break
            pg.wait_for_timeout(500)
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 1200)
        open_journal(pg)
        sha2, _, prefix2 = hero_src_sha(pg)
        LOG["hero_after"] = {"sha_match_s2": sha2 == want, "prefix": prefix2}
        print(f"hero after dialogue: sha_match_s2={sha2 == want}")
        b.close()
finally:
    stop(srv)

rows = LOG["people"].get("rows", [])
LOG["checks"] = {
    "hero_tier2_sha": LOG["hero"].get("sha_match_s2") is True,
    "people_rows_18": len(rows) == 18,
    "people_all_webp_or_silhouette": all(
        (r["srcKind"] == "webp-data" and r["nw"] == 240) or r["srcKind"] == "so_jiyan_silhouette_far.png"
        for r in rows),
    "c1_found": LOG["c1"].get("found") is True,
    "c1_awi_scale_1.00": LOG["c1"].get("awi_declared_scale") == 1,
    "c1_awi_height_487.2": bool(LOG["c1"].get("chars") and LOG["c1"]["chars"][0]["height"] == 487.2),
    "c1_awi_inlineH_60pct": bool(LOG["c1"].get("chars") and LOG["c1"]["chars"][0]["inlineH"] == "60%"),
    "c1_ho_same_height": bool(LOG["c1"].get("chars") and len(LOG["c1"]["chars"]) == 2
                              and LOG["c1"]["chars"][0]["height"] == LOG["c1"]["chars"][1]["height"]
                              and LOG["c1"]["chars"][0]["top"] == LOG["c1"]["chars"][1]["top"]),
    "hero_still_t2_after_dialogue": LOG["hero_after"].get("sha_match_s2") is True,
    "no_pageerrors": not [e for e in LOG["errors"] if e.startswith("pageerror")],
}
LOG["PASS"] = all(LOG["checks"].values())
json.dump(LOG, open(os.path.join(HERE, "merge_check109.json"), "w"), indent=1, ensure_ascii=False)
print("checks:", json.dumps(LOG["checks"], indent=1, ensure_ascii=False))
print("console errors:", len([e for e in LOG["errors"] if e.startswith("console")]))
print("failed requests:", json.dumps(LOG["failed_requests"], indent=1, ensure_ascii=False))
print("OVERALL PASS:", LOG["PASS"])
