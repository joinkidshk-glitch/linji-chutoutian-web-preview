# -*- coding: utf-8 -*-
"""v20a109 B 實駕：舊 bust 換新（列表縮圖）。
  A. BEFORE：pristine main（linji-pristine109b，546007d）新遊戲＋定態
     （6 NPCS 好感 55；12 紅星全見過 fav 參差，留程天諾未見過做剪影對照）
     → 人情頁全列表收集（每行名＋圖 src 種類＋naturalWidth）＋全頁截圖。
  B. 舊檔相容：同一 save 標記（money 109109、dayIndex 3、flags.qa109mark）
     → 存槽 3；同一 browser／context／origin（127.0.0.1:8959）換
     v109-bust 鏡像 → 繼續 → 驗證標記還原。
  C. AFTER：同一 state 人情頁全列表再收集＋全頁截圖；新圖必須全部係
     WebP data URI（naturalWidth 240），未見紅星維持剪影。
  D. 頁頭阿偉像跟級數：同一 save 設 tier 2／3／0，逐次重入手帳，
     #home-awi src 解碼後 sha256 對 qa109b/busts/awi[_s2|_s3].webp。
  E. 傾談 modal：人情頁「去找」→ 地點 sheet →「寒暄一下」→
     .dlg-portrait 必須係新 WebP（240 闊）＋截圖；NPC 唔在場就順序試下一個。
  390×844、Playwright、可棄用槽 3。零 pageerror 為 PASS 條件之一。
用法：/home/hatch/pwenv49/bin/python qa109b/drive109.py
"""
import sys, os, json, subprocess, time, signal, hashlib, base64, urllib.request
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
W109 = os.path.dirname(HERE)
PRISTINE = "/home/hatch/workspace/linji-pristine109b"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8959
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107"
LOG = {"before": {}, "compat": {}, "after": {}, "hero": {}, "talk": {},
       "errors": [], "server": {}}

def http_get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} probably taken)")
    st, body = http_get("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    if st != 200 or sha != exp:
        raise RuntimeError(f"served index mismatch: status={st} sha={sha[:12]} expected={exp[:12]}")
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
  S.stars.so_jiyan.met = false;  // 唯一未見：剪影對照（so 有 *_silhouette_far.png）
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
      hasImg: !!img,
      srcKind: !img ? 'none' : s.startsWith('data:image/webp') ? 'webp-data'
        : s.startsWith('data:image/jpeg') ? 'jpeg-data' : s.split('/').pop().split('?')[0],
      nw: img ? img.naturalWidth : null, nh: img ? img.naturalHeight : null,
      complete: img ? img.complete : null,
      opacity: img ? getComputedStyle(img).opacity : null});
  }
  const hero = document.getElementById('home-awi');
  return {rows, heroPrefix: hero ? (hero.getAttribute('src')||'').slice(0,30) : null,
          heroNw: hero ? hero.naturalWidth : null, heroComplete: hero ? hero.complete : null};
}"""

def open_people(pg):
    click_first(pg, ["☰"], 900)
    pg.evaluate("""() => { const b = document.querySelector('[data-m="journal"]');
      if (b) b.click(); }""")
    pg.wait_for_timeout(1200)
    pg.evaluate("""() => { const b = document.getElementById('htab-people');
      if (b) b.click(); }""")
    pg.wait_for_timeout(1200)
    return pg.evaluate(JS_ROWS)

def hero_src_sha(pg):
    """讀 #home-awi 完整 src，解碼後 sha256（data URI）或原字串（資產路徑）。"""
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
    exp = 3 if (n_lead >= 3 and fame >= 70) else (2 if n_lead >= 1 else 0)
    return exp, r

def open_journal(pg):
    click_first(pg, ["☰"], 900)
    pg.evaluate("""() => { const b = document.querySelector('[data-m="journal"]');
      if (b) b.click(); }""")
    pg.wait_for_timeout(1200)

def main():
    srv = serve(PRISTINE)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))

            print("== A. BEFORE (pristine main) ==")
            print("new game:", new_game(pg))
            print("setup state:", pg.evaluate(JS_SETUP_STATE))
            before = open_people(pg)
            LOG["before"] = before
            print(f"before rows: {len(before.get('rows', []))}")
            for r in before.get("rows", []):
                print("  ", r["section"], r["name"], r["srcKind"], r["nw"], "x", r["nh"])
            pg.screenshot(path=f"{SHOTS}/people_before_full.png", full_page=True)
            pg.screenshot(path=f"{SHOTS}/people_before_top.png")

            print("== B. compat: mark + save slot 3 ==")
            ok1 = pg.evaluate("""() => {
              window.S.money = 109109; window.S.dayIndex = 3;
              window.S.flags = window.S.flags || {};
              window.S.flags.qa109mark = 'main-slot3'; return 'marked'; }""")
            click_first(pg, ["☰"], 900)
            pg.evaluate("""() => { const b = document.querySelector('[data-m="save"]'); if (b) b.click(); }""")
            pg.wait_for_timeout(1200)
            saved = pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
              if (!b) return 'nobtn'; b.click(); return 'clicked'; }""")
            pg.wait_for_timeout(1000)
            click_first(pg, ["覆蓋", "確定", "確認"], 900)
            chk = pg.evaluate("""() => { const r = localStorage.getItem('starVolunteer_map_v19w_slot3');
              if (!r) return null; const o = JSON.parse(r);
              return { money: o.money, dayIndex: o.dayIndex, mark: o.flags && o.flags.qa109mark }; }""")
            LOG["compat"]["save"] = {"mark": ok1, "slot_btn": saved, "slot3": chk}
            print("save:", ok1, saved, chk)
            pg.screenshot(path=f"{SHOTS}/compat_before_saved.png")

            print("== swap server -> v109-bust ==")
            stop(srv)
            srv = serve(W109)
            print("== C. continue slot 3 on v109 ==")
            # v107 教訓嘅延續：換 server 後必須用新 query（cache-buster）再入，
            # 否則 Chromium 有機會由 HTTP cache 攞返舊 index.html（同一 URL），
            # localStorage 係按 origin 計，query 唔同唔影響存檔。
            pg.goto(URL + "&nocache=109b"); pg.wait_for_timeout(3000)
            for _ in range(10):
                vis = pg.evaluate("""() => { const b = document.getElementById('btn-cont');
                  return !!(b && b.offsetParent !== null); }""")
                if vis: break
                pg.wait_for_timeout(1000)
            print("continue click:",
                  pg.evaluate("""() => { const b = document.getElementById('btn-cont');
                    if (b && b.offsetParent !== null) { b.click(); return 'btn-cont'; } return null; }""")
                  or click_first(pg, ["繼續"], 1800))
            pg.wait_for_timeout(1200)
            restored = pg.evaluate("""() => {
              if (!(window.S && typeof window.S.dayIndex === 'number')) return null;
              return { money: window.S.money, dayIndex: window.S.dayIndex,
                       mark: window.S.flags && window.S.flags.qa109mark }; }""")
            LOG["compat"]["restored"] = restored
            LOG["compat"]["PASS"] = (restored == {"money": 109109, "dayIndex": 3, "mark": "main-slot3"})
            print("restored:", restored, "PASS:", LOG["compat"]["PASS"])
            pg.screenshot(path=f"{SHOTS}/compat_after_restored.png")

            print("== C2. AFTER people page ==")
            after = open_people(pg)
            LOG["after"] = after
            print(f"after rows: {len(after.get('rows', []))}")
            for r in after.get("rows", []):
                print("  ", r["section"], r["name"], r["srcKind"], r["nw"], "x", r["nh"])
            pg.screenshot(path=f"{SHOTS}/people_after_full.png", full_page=True)
            pg.screenshot(path=f"{SHOTS}/people_after_top.png")

            print("== D. hero tiers ==")
            crop = json.load(open(os.path.join(W109, "qa109b", "crop109.json")))
            for tier, n_lead, fame, stem in [(2, 1, 0, "awi_s2"), (3, 3, 70, "awi_s3"),
                                             (0, 0, 0, "awi")]:
                exp_tier, _r = set_tier(pg, n_lead, fame)
                open_journal(pg)
                sha, nbytes, prefix = hero_src_sha(pg)
                want_sha = None
                for k, v in crop.items():
                    if v["stem"] == stem: want_sha = v["webp_sha256"]
                ok = (sha == want_sha)
                LOG["hero"][f"tier{tier}"] = {"expected_tier": exp_tier, "stem": stem,
                    "sha_match": ok, "prefix": prefix, "bytes": nbytes}
                print(f"hero tier {tier} (exp {exp_tier}) stem={stem} sha_match={ok} prefix={prefix}")
                pg.screenshot(path=f"{SHOTS}/hero_t{tier}.png")

            print("== E. talk modal ==")
            open_people(pg)
            talk = {"tried": [], "found": None}
            for npc in ["agent", "colleague", "reporter", "director", "stylist", "rival"]:
                clicked = pg.evaluate("""(id) => {
                  const b = document.querySelector('.people-go[data-npc="' + id + '"]');
                  if (!b) return false; b.click(); return true; }""", npc)
                talk["tried"].append((npc, clicked))
                if not clicked: continue
                pg.wait_for_timeout(1500)
                talk_btn = click_first(pg, ["寒暄一下"], 1500)
                if not talk_btn:
                    click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
                    open_people(pg)
                    continue
                pg.wait_for_timeout(1200)
                info = pg.evaluate("""() => {
                  const im = document.querySelector('.dlg-portrait');
                  if (!im) return null;
                  const s = im.getAttribute('src') || '';
                  return {srcKind: s.startsWith('data:image/webp') ? 'webp-data'
                      : s.startsWith('data:image/jpeg') ? 'jpeg-data' : s.slice(0,40),
                    nw: im.naturalWidth, nh: im.naturalHeight, complete: im.complete,
                    name: (document.querySelector('.dlg-name')||{}).textContent || ''}; }""")
                print(f"talk {npc}: btn={talk_btn} info={info}")
                talk["found"] = {"npc": npc, "info": info}
                pg.screenshot(path=f"{SHOTS}/talk_after.png")
                click_first(pg, ["關閉", "確定", "知道了"], 900)
                break
            LOG["talk"] = talk

            LOG["errors"] += errs
            b.close()
    finally:
        stop(srv)

    b_rows = LOG["before"].get("rows", [])
    a_rows = LOG["after"].get("rows", [])
    def all_webp(rows, section):
        rs = [r for r in rows if r["section"] == section and r["name"] != "？？？"]
        return bool(rs) and all(r["srcKind"] == "webp-data" and r["nw"] == 240
                                and r["nh"] == 312 and r["complete"] for r in rs)
    before_npc_jpeg = all(r["srcKind"] == "jpeg-data" for r in b_rows if r["section"] == "人脈")
    unmet_after = [r for r in a_rows if r["name"] == "？？？"]
    unmet_ok = (len(unmet_after) == 1 and unmet_after[0]["srcKind"] == "so_jiyan_silhouette_far.png"
                and unmet_after[0]["opacity"] == "0.55")
    LOG["checks"] = {
        "before_npc_all_jpeg": before_npc_jpeg,
        "before_rows_18": len(b_rows) == 18,
        "after_rows_18": len(a_rows) == 18,
        "after_npc_all_webp240": all_webp(a_rows, "人脈"),
        "after_stars_all_webp240": all_webp(a_rows, "紅星"),
        "after_unmet_still_silhouette": unmet_ok,
        "compat": LOG["compat"].get("PASS") is True,
        "hero_all_sha": all(v.get("sha_match") for v in LOG["hero"].values()) and len(LOG["hero"]) == 3,
        "talk_webp240": bool(LOG["talk"].get("found") and LOG["talk"]["found"]["info"]
                             and LOG["talk"]["found"]["info"]["srcKind"] == "webp-data"
                             and LOG["talk"]["found"]["info"]["nw"] == 240),
        "no_pageerrors": not LOG["errors"],
    }
    LOG["PASS"] = all(LOG["checks"].values())
    json.dump(LOG, open(os.path.join(HERE, "drive_log109.json"), "w"), indent=1, ensure_ascii=False)
    print("checks:", json.dumps(LOG["checks"], indent=1, ensure_ascii=False))
    print("pageerrors:", LOG["errors"][:6])
    print("OVERALL PASS:", LOG["PASS"])

if __name__ == "__main__":
    main()
