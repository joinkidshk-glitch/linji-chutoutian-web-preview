# -*- coding: utf-8 -*-
"""v20a206 C2 實駕 drive206c2：9 單場景重映射逐單截圖核實（7 單任務＋day10／st13 全面掃描追加）。
用法：/home/hatch/pwenv49/bin/python qa206/drive206c2.py
Mirror：工作副本 ~/workspace/linji-work206，port 8997，serve repo 原目錄（資產齊全）。
方法跟 review R1／R1B：new_game 開局一次（slot 1），逐單 pending-seed（localStorage
starVolunteer_map_v19w：seen={}、pending=<id>、pendingDay=<day>、dayIndex=<day>），
reload＋讀檔，晨鏈彈 WF4 modal 即截圖＋讀標題／場景圖 URL。載入日全部避開頒獎日
（100／365／730）；day24  cond yearMin:1992，用 day 731。典禮等待照 R1B 手法
（見 .awd62-stage 就等，唔直接信 #v-map）。
斷言：每單標題啱＋場景圖 URL 啱預期；0 pageerror、0 http fail。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, sys, re

ROOT = "/home/hatch/workspace/linji-work206"
HERE = os.path.join(ROOT, "qa206")
SHOTS = os.path.join(HERE, "shots206c2")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8997
URL = f"http://127.0.0.1:{PORT}/index.html"
REPORT = {"errors": [], "http_fail": [], "cases": {}}

from playwright.sync_api import sync_playwright

_HTML = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
_ARR = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', _HTML, re.S).group(1)
TITLES = {}
for _chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', _ARR):
    _im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', _chunk)
    _tm = re.search(r'title:"([^"]+)"', _chunk)
    if _im and _tm:
        TITLES[_im.group(1)] = _tm.group(1)
assert len(TITLES) == 113, len(TITLES)

# (event id, seed day, expected scene file)
TARGETS = [
    ("wf4_ev_day07", 10, "bg_wf4_market.jpg"),       # 電車上面 → 中性街市街景
    ("wf4_ev_day09", 11, "bg_loc_rec_hk.jpg"),       # 唱片舖 → 唱片舖內景本身
    ("wf4_ev_st17", 12, "bg_wf4_market.jpg"),        # 樓下士多 → 街市街景
    ("wf4_ev_day19", 13, "bg_wf4_market.jpg"),       # 公園晨運 → 戶外街市街景
    ("wf4_ev_day22", 14, "bg_wf4_market.jpg"),       # 地鐵站賣唱 → 中性街市街景
    ("wf4_ev_day24", 731, "bg_loc_tvb_kowloon.jpg"), # 電視台信件房 → 電視台辦公室內景
    ("wf4_ev_day27", 15, "bg_loc_film_harbour.jpg"), # 海邊散步 → 海港景
    ("wf4_ev_day10", 16, "bg_loc_film_harbour.jpg"), # 全面掃描：巴士望海 → 海港景
    ("wf4_ev_st13", 17, "bg_loc_film_harbour.jpg"),  # 全面掃描：渡輪望兩岸 → 海港景
]

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

def click_first(pg, texts, wait=900):
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

def js_click_text(pg, text):
    return pg.evaluate("""(t) => {
      const b = [...document.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)

def modal_click(pg, text):
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)

def read_state(pg):
    return pg.evaluate("""() => {
      if (typeof S === 'undefined' || !S) return null;
      return { day: S.dayIndex,
        pending: (S.wf4 && S.wf4.pending) ? S.wf4.pending : null,
        pendingDay: (S.wf4) ? S.wf4.pendingDay : null }; }""")

def wf4_info(pg):
    return pg.evaluate("""(titles) => {
      const h3 = document.querySelector('#modal-inner h3');
      if (!h3) return null;
      const t = (h3.textContent || '').trim();
      if (titles.indexOf(t) < 0) return null;
      let scene = null;
      const band = document.querySelector('#modal-inner .wf4-scene105');
      if (band) { const m = (band.style.backgroundImage || '').match(/url\\("?([^")]+)"?\\)/); if (m) scene = m[1]; }
      if (!scene) { const bg = document.querySelector('#modal-inner .sp-bg-layer');
        if (bg) { const m = (bg.style.backgroundImage || '').match(/url\\("?([^")]+)"?\\)/); if (m) scene = m[1]; } }
      return { title: t, scene: scene }; }""", list(TITLES.values()))

def map_visible(pg):
    return pg.evaluate("() => { const v = document.querySelector('#v-map'); return !!v && v.offsetParent !== null; }")

def ceremony_active(pg):
    return pg.evaluate("() => !!document.querySelector('.awd62-stage')")

def story_active(pg):
    return pg.evaluate("""() => {
      const plate = document.querySelector('.story-play .dlg106-plate');
      const choice = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
      return !!plate || choice.length > 0; }""")

def play_story(pg, max_steps=80, pick=None):
    for _ in range(max_steps):
        if not story_active(pg):
            return True
        if pg.evaluate("""(kw) => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
            if (!c.length) return false;
            let i = 0;
            if (kw) { for (let j=0;j<c.length;j++) if ((c[j].textContent||'').indexOf(kw) >= 0) { i = j; break; } }
            c[i].click(); return true; }""", pick):
            pg.wait_for_timeout(1000)
            continue
        if pg.evaluate("""() => { const row = document.getElementById('modal-btns'); if (!row) return false; const bs=[...row.querySelectorAll('button')].filter(x=>x.offsetParent!==null && !x.disabled); if (bs.length) { bs[0].click(); return true; } return false; }"""):
            pg.wait_for_timeout(900)
            continue
        pg.wait_for_timeout(800)
    return not story_active(pg)

def dismiss_once(pg):
    if wf4_info(pg):
        return False
    r = pg.evaluate("""() => {
      const ov = document.getElementById('enc79-overlay'); if (ov) {
        const sk = ov.querySelector('.e79-skip'); if (sk && sk.offsetParent !== null) { sk.click(); return 'enc-skip'; }
        const ch = ov.querySelector('.e79-choice'); if (ch) { ch.click(); return 'enc-choice'; }
        const nb = [...ov.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
        if (nb) { nb.click(); return 'enc-btn'; } }
      return false; }""")
    if r:
        return r
    if story_active(pg):
        if pg.evaluate("""() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null); if(c[0]) { c[0].click(); return true; } return false; }"""):
            return 'story-choice'
        if pg.evaluate("""() => { const row = document.getElementById('modal-btns'); if (!row) return false; const bs=[...row.querySelectorAll('button')].filter(x=>x.offsetParent!==null && !x.disabled); if (bs.length) { bs[0].click(); return true; } return false; }"""):
            return 'story-next'
        return False
    r = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return 'modal-btn:' + (bs[0].textContent || '').trim().slice(0,12); }""")
    return r or False

def settle(pg, timeout_ms=15000):
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout_ms:
        t = wf4_info(pg)
        if t:
            return ('wf4', t)
        r = dismiss_once(pg)
        if r:
            pg.wait_for_timeout(700)
            continue
        if map_visible(pg):
            return ('map', None)
        pg.wait_for_timeout(600)
    return ('timeout', wf4_info(pg))

def handle_wf4(pg, tag):
    info = wf4_info(pg)
    if not info:
        return None
    pg.screenshot(path=os.path.join(SHOTS, f"{tag}_wf4.png"))
    for _ in range(14):
        if not wf4_info(pg):
            break
        clicked = (modal_click(pg, "繼續") or modal_click(pg, "睇落去")
                   or pg.evaluate("""() => { const row = document.getElementById('modal-btns');
                     if (!row) return false;
                     const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
                     if (!bs.length) return false; bs[0].click(); return true; }"""))
        pg.wait_for_timeout(700)
        if not clicked:
            break
    return info

def go_map(pg):
    if map_visible(pg):
        return True
    pg.evaluate("() => { const b=document.getElementById('home-back-map'); if(b && b.offsetParent!==null) b.click(); }")
    pg.wait_for_timeout(1200)
    if map_visible(pg):
        return True
    js_click_text(pg, "返回地圖")
    pg.wait_for_timeout(1200)
    return map_visible(pg)

def new_game(pg, slot="1", pick=None):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("(s) => { const b = document.querySelector('[data-slot=\"' + s + '\"]'); if (b && b.offsetParent !== null) { b.click(); return true; } return false; }", slot)
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
    if not play_story(pg, max_steps=80, pick=pick):
        print("WARN: story not cleared", flush=True)
    pg.wait_for_timeout(1500)
    if not go_map(pg):
        js_click_text(pg, "返回地圖"); pg.wait_for_timeout(1200); go_map(pg)
    settle(pg, timeout_ms=8000)
    go_map(pg)
    st = read_state(pg)
    print("NEW GAME:", st and st['day'], "map:", map_visible(pg), flush=True)
    return st is not None and map_visible(pg)

def load_slot(pg, slot="1"):
    click_first(pg, ["讀檔"], 1200)
    pg.evaluate("(s) => { const b = document.querySelector('[data-slot=\"' + s + '\"]'); if (b && b.offsetParent !== null) { b.click(); return true; } return false; }", slot)
    pg.wait_for_timeout(1500)
    click_first(pg, ["覆蓋", "確定", "確認"], 800)
    return settle(pg, timeout_ms=15000)

def seed_pending(pg, target_id, day):
    r = pg.evaluate("""(o) => {
      try {
        const raw = localStorage.getItem('starVolunteer_map_v19w');
        if (!raw) return {ok:false, err:'no save'};
        const sv = JSON.parse(raw);
        sv.dayIndex = o.day;
        sv.wf4 = sv.wf4 || {};
        sv.wf4.seen = {}; sv.wf4.seen.__n = 0;
        sv.wf4.pending = o.pending; sv.wf4.pendingDay = o.day;
        sv.wf4.lastDay = o.day - 3; sv.wf4.locDay = -99; sv.wf4.locTries = 0;
        sv.weekPlan = []; for (let i=0;i<7;i++) sv.weekPlan[i]='rest';
        localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(sv));
        return {ok:true};
      } catch(e){ return {ok:false, err:String(e)}; } }""",
      {"pending": target_id, "day": day})
    if not r.get('ok'):
        return r
    pg.reload(); pg.wait_for_timeout(2500)
    res = load_slot(pg, "1")
    return {"ok": True, "load": res}

def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
            pg.on("requestfailed", lambda r: REPORT["http_fail"].append(r.url))
            assert new_game(pg, slot="1"), "new game failed"
            for (eid, day, expect_file) in TARGETS:
                r = seed_pending(pg, eid, day)
                info = None
                t0 = time.time()
                while time.time() - t0 < 60:
                    if ceremony_active(pg):
                        pg.wait_for_timeout(1500)
                        continue
                    info = wf4_info(pg)
                    if info:
                        break
                    rr = dismiss_once(pg)
                    if rr:
                        pg.wait_for_timeout(700)
                        continue
                    if map_visible(pg):
                        pg.wait_for_timeout(1000)
                        if not ceremony_active(pg) and not wf4_info(pg):
                            break
                if info:
                    info = handle_wf4(pg, "C2_" + eid.replace("wf4_ev_", ""))
                    settle(pg, timeout_ms=8000)
                    go_map(pg)
                ok = bool(info and info['title'] == TITLES[eid]
                          and info['scene'] and expect_file in info['scene'])
                REPORT["cases"][eid] = {"ok": ok, "seed_day": day,
                                        "title": info['title'] if info else None,
                                        "expect_title": TITLES[eid],
                                        "scene": info['scene'] if info else None,
                                        "expect_scene": expect_file}
                print("C2", eid, REPORT["cases"][eid], flush=True)
            REPORT["cases"]["errors_932"] = errs
            br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive206c2_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=2)
    n_ok = sum(1 for k, v in REPORT["cases"].items() if isinstance(v, dict) and v.get("ok"))
    print(f"RESULT {n_ok}/{len(TARGETS)} ok, pageerrors={len(REPORT['cases']['errors_932'])}, http_fail={len(REPORT['http_fail'])}")

if __name__ == "__main__":
    main()
