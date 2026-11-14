# -*- coding: utf-8 -*-
"""v20a203 實駕 drive203：WF4 迎新期＋Phase 2＋B3／C1／C2／C3，932／700，LIVE 模式（唔用 ?softPreview=1）。
用法：/home/hatch/pwenv49/bin/python qa203/drive203.py [--only A|B|C|D|E]
Mirror：工作副本 ~/workspace/linji-work203，port 8994，serve repo 原目錄（資產齊全）。
播種：經 new_game 正常開局（slot 1，key starVolunteer_map_v19w），播完 C1 故事返地圖。
Cases（932 同一個 browser 順序行）：
  B 迎新期密度：fresh 局，行到 day 30（每日入 tvb_longmen＋cafe_cha 各一次＋開始今日行程／過一日），
    記錄每次 WF4 modal 標題；斷言 ≥3 單、全部唔同（sim A 路線話 4 單；實玩有巧遇／故事干擾，≥3 收貨）。
  A 場景巡迴（pending-seed 即彈，R5 手法）：15 個目標逐單 seed pending（seen 清空、pendingDay＝當日、
    按 cond 補 day／money／fame／stress），reload＋讀檔＋返地圖即彈 modal；斷言標題啱＋場景圖 URL
    啱（.wf4-scene105 或舞台 .sp-bg-layer 嘅 background-image），圖檔經 HTTP 驗 200。
    目標：day05／07／09／11／14／15（C2 六單）＋st15（C1）＋st17（B3＋C2）＋day17／18／20／24（新 day）
    ＋set17（B3）＋set26／set54（新 loc）。
  C 典禮撞強制播（R4a 播種）：slot 3，day 98，C1–C5 done，pending set17＋C6F 待播；入茶餐廳→閂 sheet→
    晨鏈請柬→出席→典禮播緊嗰陣 JS click 穿透（入地點＋閂 sheet）→斷言故事唔開（冇 .story-play plate、
    story165CanPlay 概念上返 null——IIFE 唔可以直接 call，用行為斷言）、典禮層仲喺度、唔食出行額度；
    撳跳過→典禮完→返地圖→C6F 強制播→播完 isDone('C6F') True。
  D 地點抽乾：seed seen＝全部 113 單除咗 set26（film_lion 剩返呢一單）；入 film_lion 直至 set26 彈出
    一次；之後再入 film_lion 3 次（跨日）→斷言零 WF4 modal（池抽乾後優雅，唔會重出／唔會 crash）。
  E 700 smoke：fresh 局＋pending-seed day05，斷言 modal 標題＋場景圖 bg_loc_cafe_cha.jpg＋圖 200。
量度（DOM 為準，截圖只係記錄）：WF4 modal 以 #modal-inner h3 標題認；場景圖以 background-image URL 認＋HTTP 200；
  pageerror／console error／失敗請求。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, sys, re

ROOT = "/home/hatch/workspace/linji-work203"
HERE = os.path.join(ROOT, "qa203")
SHOTS = os.path.join(HERE, "shots203")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8994
URL = f"http://127.0.0.1:{PORT}/index.html"
REPORT = {"errors": [], "http_fail": [], "cases": {}}

from playwright.sync_api import sync_playwright

# --- 由 index.html 抽 TITLES＋SCENE 表（唔手寫 113 個標題，唔會抄錯） ---
_HTML = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
_ARR = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', _HTML, re.S).group(1)
TITLES = {}
for _chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', _ARR):
    _im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', _chunk)
    _tm = re.search(r'title:"([^"]+)"', _chunk)
    if _im and _tm:
        TITLES[_im.group(1)] = _tm.group(1)
assert len(TITLES) == 113, len(TITLES)
_SCENE = dict(re.findall(r'(wf4_ev_\w+):"([^"]+)"', re.search(r'const WF4_SCENE_OVERRIDE134 = \{(.*?)\};', _HTML, re.S).group(1)))
ALL_IDS = list(TITLES.keys())

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

def http_ok(url_path):
    """場景圖檔經 HTTP 驗 200（去 ?v= 後綴）。"""
    try:
        clean = url_path.split("?")[0].lstrip("/")
        st, _ = http_body(clean)
        return st == 200
    except Exception:
        return False

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
      return { day: S.dayIndex, dateStr: S.dateStr || null,
        money: S.money, stress: S.stress, fame: S.fame,
        seen: (S.wf4 && S.wf4.seen) ? S.wf4.seen : null,
        pending: (S.wf4 && S.wf4.pending) ? S.wf4.pending : null,
        lastDay: (S.wf4) ? S.wf4.lastDay : null,
        locTries: (S.wf4) ? S.wf4.locTries : null }; }""")

def wf4_info(pg):
    """而家開緊嘅 modal 係唔係 WF4 事件。返 {title, scene} 或 null。scene 係 background-image URL。"""
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

def story_act191(pg):
    return pg.evaluate("""() => {
      const act = document.querySelector('.sp-act191');
      const plate = document.querySelector('.story-play .dlg106-plate');
      const h3 = document.querySelector('.sp-head-opening h3');
      return { active: !!plate || !!document.querySelector('.sp-head-opening'),
        act191: act ? act.textContent.trim() : null,
        nodeTitle: h3 ? h3.textContent.trim() : null }; }""")

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
        if pg.evaluate("() => { const row = document.getElementById('modal-btns'); if (!row) return false; const bs=[...row.querySelectorAll('button')].filter(x=>x.offsetParent!==null && !x.disabled); if (bs.length) { bs[0].click(); return true; } return false; }"):
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
        if pg.evaluate("() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null); if(c[0]) { c[0].click(); return true; } return false; }"):
            return 'story-choice'
        if pg.evaluate("() => { const row = document.getElementById('modal-btns'); if (!row) return false; const bs=[...row.querySelectorAll('button')].filter(x=>x.offsetParent!==null && !x.disabled); if (bs.length) { bs[0].click(); return true; } return false; }"):
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

def load_slot(pg, slot="1"):
    click_first(pg, ["讀檔"], 1200)
    pg.evaluate("(s) => { const b = document.querySelector('[data-slot=\"' + s + '\"]'); if (b && b.offsetParent !== null) { b.click(); return true; } return false; }", slot)
    pg.wait_for_timeout(1500)
    click_first(pg, ["覆蓋", "確定", "確認"], 800)
    return settle(pg, timeout_ms=15000)

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
        js_click_text(pg, "返回地圖")
        pg.wait_for_timeout(1200)
        go_map(pg)
    settle(pg, timeout_ms=8000)
    go_map(pg)
    st = read_state(pg)
    print("NEW GAME:", st and st['day'], "map:", map_visible(pg), flush=True)
    return st is not None and map_visible(pg)

def persist_wf4(pg, seen=None, pending=None, pending_day=None, day=None, money=None, fame=None, stress=None):
    """直寫 localStorage 存檔（R4a 手法）：saveQ 係 IIFE 內部，頁面 evaluate 叫唔到，唔好靠佢。"""
    return pg.evaluate("""(o) => {
      try {
        const raw = localStorage.getItem('starVolunteer_map_v19w');
        if (!raw) return {ok:false, err:'no save'};
        const sv = JSON.parse(raw);
        if (o.day !== null && o.day !== undefined) sv.dayIndex = o.day;
        if (o.money !== null && o.money !== undefined) sv.money = o.money;
        if (o.fame !== null && o.fame !== undefined) sv.fame = o.fame;
        if (o.stress !== null && o.stress !== undefined) sv.stress = o.stress;
        sv.wf4 = sv.wf4 || {};
        if (o.seen) { sv.wf4.seen = o.seen; sv.wf4.seen.__n = Object.keys(o.seen).filter(k=>k!=='__n').reduce((a,k)=>a+(o.seen[k]||0),0); }
        if (o.pending !== null && o.pending !== undefined) sv.wf4.pending = o.pending;
        if (o.pending_day !== null && o.pending_day !== undefined) sv.wf4.pendingDay = o.pending_day;
        if (o.seen) { sv.wf4.lastDay = (o.day !== null && o.day !== undefined ? o.day : sv.dayIndex) - 3; sv.wf4.locDay = -99; sv.wf4.locTries = 0; }
        sv.weekPlan = []; for (let i=0;i<7;i++) sv.weekPlan[i]='rest';
        localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(sv));
        return {ok:true};
      } catch(e){ return {ok:false, err:String(e)}; } }""",
      {"seen": seen, "pending": pending, "pending_day": pending_day,
       "day": day, "money": money, "fame": fame, "stress": stress})

def seed_seen(pg, seen_dict):
    r = pg.evaluate("""(seen) => {
      try {
        if (typeof S === 'undefined' || !S) return {ok:false, err:'no S'};
        if (!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = { lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false };
        for (const k of Object.keys(seen)) S.wf4.seen[k] = seen[k];
        S.wf4.seen.__n = Object.keys(S.wf4.seen).filter(k=>k!=='__n').reduce((a,k)=>a+(S.wf4.seen[k]||0),0);
        S.weekPlan = S.weekPlan || [];
        for (let i=0;i<7;i++) S.weekPlan[i]='rest';
        return {ok:true};
      } catch(e){ return {ok:false, err:String(e)}; } }""", seen_dict)
    print("SEED live:", r, flush=True)
    if not r.get('ok'):
        return False
    r2 = persist_wf4(pg, seen=seen_dict)
    print("SEED persist:", r2, flush=True)
    return r2.get('ok')

def seed_pending(pg, target_id, day, money=None, fame=None, stress=None):
    """pending-seed：直寫存檔（seen 清空＋pending 指目標＋按 cond 補狀態），再 reload＋讀檔。"""
    r = persist_wf4(pg, seen={}, pending=target_id, pending_day=day,
                    day=day, money=money, fame=fame, stress=stress)
    if not r.get('ok'):
        return r
    pg.reload(); pg.wait_for_timeout(2500)
    res = load_slot(pg, "1")
    return {"ok": True, "load": res}

def visit_loc(pg, loc_id, tag, seen_titles):
    if not go_map(pg):
        return ('not-on-map', None)
    ok = pg.evaluate("""(loc) => {
      const b = document.querySelector('button[data-loc="' + loc + '"]');
      if (!b || b.offsetParent === null) return false; b.click(); return true; }""", loc_id)
    pg.wait_for_timeout(1200)
    if not ok:
        return ('no-btn', None)
    t = wf4_info(pg)
    if t:
        info = handle_wf4(pg, tag + '_' + loc_id)
        seen_titles.append(info['title'] if info else t['title'])
        pg.wait_for_timeout(800)
        settle(pg, timeout_ms=8000)
        go_map(pg)
        return ('wf4', t['title'])
    settle(pg, timeout_ms=8000)
    js_click_text(pg, "返回地圖")
    pg.wait_for_timeout(800)
    settle(pg, timeout_ms=8000)
    go_map(pg)
    return ('sheet', None)

def reseed_week_rest(pg):
    pg.evaluate("""() => {
      try {
        S.weekPlan = []; for (let i=0;i<7;i++) S.weekPlan[i]='rest';
        const raw = localStorage.getItem('starVolunteer_map_v19w');
        if (raw) { const sv = JSON.parse(raw); sv.weekPlan = S.weekPlan; localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(sv)); }
        return true; } catch(e){ return false; } }""")
    pg.reload(); pg.wait_for_timeout(2500)
    load_slot(pg, "1")
    go_map(pg)

def start_today(pg, tag, seen_titles):
    day0 = (read_state(pg) or {}).get('day')
    clicked = pg.evaluate("""() => {
      const b = document.getElementById('map-start-today');
      if (b && b.offsetParent !== null) { b.click(); return 'start'; }
      const e = document.getElementById('map-end-day');
      if (e && e.offsetParent !== null) { e.click(); return 'endday'; }
      return false; }""")
    pg.wait_for_timeout(1000)
    if not clicked:
        reseed_week_rest(pg)
        clicked = pg.evaluate("""() => {
          const b = document.getElementById('map-start-today');
          if (b && b.offsetParent !== null) { b.click(); return 'start'; }
          const e = document.getElementById('map-end-day');
          if (e && e.offsetParent !== null) { e.click(); return 'endday'; }
          return false; }""")
        pg.wait_for_timeout(1000)
    if not clicked:
        return ('no-start-btn', day0)
    t0 = time.time()
    while time.time() - t0 < 45:
        t = wf4_info(pg)
        if t:
            info = handle_wf4(pg, tag + '_day')
            seen_titles.append(info['title'] if info else t['title'])
            pg.wait_for_timeout(700)
            continue
        r = dismiss_once(pg)
        if r:
            pg.wait_for_timeout(700)
            continue
        st = read_state(pg)
        if st and day0 is not None and st['day'] != day0 and map_visible(pg):
            return ('advanced', st['day'])
        pg.wait_for_timeout(600)
    st = read_state(pg)
    return ('timeout', st and st['day'])

def close_loc_sheet(pg):
    hit = pg.evaluate("""() => {
      const sh = document.getElementById('loc-sheet'); if (!sh) return false;
      const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent||'').trim() === '返回地圖');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    return hit

# ---------------- Cases ----------------

# A：15 個目標（id, day, money, fame, stress, 預期場景檔名或 None=地點預設圖）
TARGETS_A = [
    ("wf4_ev_day05", 10, None, None, None, "bg_loc_cafe_cha.jpg"),
    ("wf4_ev_day07", 10, None, None, None, "bg_wf4_taxi.jpg"),
    ("wf4_ev_day09", 10, None, None, None, "bg_loc_gift_shop.jpg"),
    ("wf4_ev_day11", 365, None, None, None, "bg_loc_cafe_cha.jpg"),
    ("wf4_ev_day14", 365, None, None, None, "bg_loc_film_lion.jpg"),
    ("wf4_ev_day15", 10, 150, None, None, "bg_loc_cafe_cha.jpg"),
    ("wf4_ev_st15", 10, None, None, None, "bg_wf4_taxi.jpg"),
    ("wf4_ev_st17", 10, None, None, 60, "bg_loc_gift_shop.jpg"),
    ("wf4_ev_day17", 20, None, None, None, "bg_wf4_home.jpg"),
    ("wf4_ev_day18", 70, None, None, None, "bg_wf4_market.jpg"),
    ("wf4_ev_day20", 20, None, None, None, "bg_loc_gift_shop.jpg"),
    ("wf4_ev_day24", 730, None, 26, None, "bg_wf4_home.jpg"),
    ("wf4_ev_set17", 365, None, 26, None, None),
    ("wf4_ev_set26", 10, None, None, None, None),
    ("wf4_ev_set54", 730, None, None, None, None),
]

def run_case_a(pg):
    results = {}
    for (tid, day, money, fame, stress, expect_scene) in TARGETS_A:
        r = seed_pending(pg, tid, day, money, fame, stress)
        if not r.get('ok'):
            results[tid] = {"ok": False, "why": "seed-failed", "seed": r}
            print("A", tid, "SEED FAIL", r, flush=True)
            continue
        # 晨鏈可能播緊典禮（day 730 撞星河台慶，舞台 ~10 秒＋結果卡）：等舞台拆走＋碌埋結果卡先讀 WF4 modal。
        # settle 會喺 #v-map 見到嗰陣即刻返 'map'（地圖喺 fixed overlay 下面 offsetParent 照樣可見），所以唔可以直接信佢。
        info = None
        t0 = time.time()
        while time.time() - t0 < 45:
            if ceremony_active(pg):
                pg.wait_for_timeout(1500)
                continue
            info = wf4_info(pg)
            if info:
                break
            r = dismiss_once(pg)
            if r:
                pg.wait_for_timeout(700)
                continue
            if map_visible(pg):
                pg.wait_for_timeout(1000)
                if not ceremony_active(pg) and not wf4_info(pg):
                    break
        title_ok = bool(info) and info['title'] == TITLES[tid]
        scene_ok = None
        scene_url = info['scene'] if info else None
        if expect_scene:
            scene_ok = bool(scene_url) and expect_scene in scene_url and http_ok(scene_url)
        else:
            scene_ok = bool(scene_url) and http_ok(scene_url)
        # 額外核對：覆寫表話係邊張（防 drive 手寫錯）
        table_ok = (expect_scene is None) or (tid in _SCENE and expect_scene in _SCENE[tid])
        if info:
            handle_wf4(pg, "A_" + tid.replace("wf4_ev_", ""))
            settle(pg, timeout_ms=8000)
            go_map(pg)
        results[tid] = {"ok": bool(title_ok and scene_ok and table_ok),
                        "title": info['title'] if info else None, "expect_title": TITLES[tid],
                        "scene": scene_url, "expect_scene": expect_scene,
                        "scene_ok": scene_ok, "table_ok": table_ok}
        print("A", tid, results[tid], flush=True)
    ok = all(v["ok"] for v in results.values())
    return {"ok": ok, "results": results}

def end_day_once(pg, tag, seen_titles):
    """撳「過一日」行一日（唔行成週行程）：逐日推進，等 daily tick 每日都跑一次，對得上 sim 嘅逐日模型。"""
    day0 = (read_state(pg) or {}).get('day')
    clicked = pg.evaluate("""() => {
      // #map-end-day 有兩個（重複 id）：第一個係隱藏嗰粒，getElementById 會攞錯——要搵可見嗰粒
      const e = [...document.querySelectorAll('#map-end-day')].find(x => x.offsetParent !== null);
      if (e) { e.click(); return 'endday'; }
      return false; }""")
    pg.wait_for_timeout(1000)
    if not clicked:
        return start_today(pg, tag, seen_titles)
    t0 = time.time()
    while time.time() - t0 < 45:
        t = wf4_info(pg)
        if t:
            info = handle_wf4(pg, tag + '_day')
            seen_titles.append(info['title'] if info else t['title'])
            pg.wait_for_timeout(700)
            continue
        r = dismiss_once(pg)
        if r:
            pg.wait_for_timeout(700)
            continue
        st = read_state(pg)
        if st and day0 is not None and st['day'] != day0 and map_visible(pg):
            return ('advanced', st['day'])
        pg.wait_for_timeout(600)
    st = read_state(pg)
    return ('timeout', st and st['day'])

def run_case_b(pg, single_day=True):
    titles = []
    start_day = (read_state(pg) or {}).get('day', 0)
    days = 0
    while (read_state(pg) or {}).get('day', 99) < 30 and days < 32:
        st = read_state(pg)
        if not st:
            break
        for loc in ['tvb_longmen', 'cafe_cha']:
            visit_loc(pg, loc, f"B_d{st['day']}", titles)
        if single_day:
            r, day1 = end_day_once(pg, f"B_d{st['day']}", titles)
        else:
            r, day1 = start_today(pg, f"B_d{st['day']}", titles)
        days += 1
        print(f"B day {st['day']} -> {day1} ({r}), wf4 so far ({len(titles)}): {titles}", flush=True)
        if r == 'no-start-btn':
            break
    distinct = len(set(titles)) == len(titles)
    return {"ok": len(titles) >= 3 and distinct, "titles": titles, "n": len(titles),
            "distinct": distinct, "start_day": start_day,
            "end_day": (read_state(pg) or {}).get('day')}

def run_case_c(pg):
    """C3：R4a 播種＋典禮穿透探針。"""
    assert new_game(pg, slot="1", pick="接電影散工賺快錢"), "new game C failed"
    click_first(pg, ["關閉"], 800)
    go_map(pg); settle(pg, timeout_ms=8000); go_map(pg)
    ok_copy = pg.evaluate("""() => {
      try {
        const raw = localStorage.getItem('starVolunteer_map_v19w');
        if (!raw) return {ok:false, err:'no slot1 save'};
        const o = JSON.parse(raw);
        o.dayIndex = 98;
        o.story = o.story || {}; o.story.done = Object.assign({}, o.story.done, { C1: true, C2: true, C3: true, C4: true, C5: true });
        o.story.lastMainDoneDay = 90;
        o.fame = 26; o.industryCredit = 49; o.money = 14936;
        o.wf4 = o.wf4 || {};
        o.wf4.seen = {}; o.wf4.pending = 'wf4_ev_set17'; o.wf4.pendingDay = 98;
        o.wf4.lastDay = 95; o.wf4.locDay = -99; o.wf4.locTries = 0;
        localStorage.setItem('starVolunteer_map_v19w_slot3', JSON.stringify(o));
        return {ok:true};
      } catch(e){ return {ok:false, err:String(e)}; } }""")
    print("C copy to slot3:", ok_copy, flush=True)
    if not ok_copy.get('ok'):
        return {"ok": False, "why": "copy-failed", "copy": ok_copy}
    pg.goto(URL); pg.wait_for_timeout(2500)
    ld = load_slot(pg, "3")
    print("C load slot3:", ld, flush=True)
    st = read_state(pg)
    if not st or st.get('day') != 98:
        return {"ok": False, "why": "load-state-wrong", "state": st}
    go_map(pg)
    ok = pg.evaluate("""() => {
      const b = document.querySelector('button[data-loc="cafe_cha"]');
      if (!b || b.offsetParent === null) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    print("C entered cafe:", ok, "state:", read_state(pg), flush=True)
    closed = close_loc_sheet(pg)
    print("C closed sheet:", closed, flush=True)
    # 晨鏈：請柬 modal（出席／推辭）→ 出席 → 典禮舞台。poll 30 秒處理三種狀態。
    ceremony_seen = False
    invite_clicked = False
    t0 = time.time()
    while time.time() - t0 < 40:
        if ceremony_active(pg):
            ceremony_seen = True
            break
        if pg.evaluate("""() => { const row = document.getElementById('modal-btns');
            if (!row) return false;
            const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent||'').trim() === '出席');
            if (!b) return false; b.click(); return true; }"""):
            invite_clicked = True
            pg.wait_for_timeout(1500)
            continue
        if story_active(pg):
            break
        r = dismiss_once(pg)
        if r:
            pg.wait_for_timeout(700)
            continue
        pg.wait_for_timeout(700)
    print("C ceremony seen:", ceremony_seen, "invite clicked:", invite_clicked, "story active:", story_active(pg), flush=True)
    pg.screenshot(path=os.path.join(SHOTS, "C_ceremony.png"))
    if not ceremony_seen:
        # 典禮冇出：可能鏈直接行咗強制播（唔係撞期嗰日）——記錄，唔當 C3 失敗，但要講明
        sp = story_act191(pg)
        return {"ok": False, "why": "no-ceremony-this-run", "ceremony_seen": False,
                "invite_clicked": invite_clicked, "story": sp}
    # --- 典禮進行中：穿透探針（真人玩家撳唔穿，review R4a 手法） ---
    before = read_state(pg)
    penetrated = pg.evaluate("""() => {
      const out = { locBtn: false, closeBtn: false };
      const b = document.querySelector('button[data-loc="cafe_cha"]');
      if (b) { b.click(); out.locBtn = true; }
      return out; }""")
    pg.wait_for_timeout(1500)
    penetrated['closeBtn'] = pg.evaluate("""() => {
      const sh = document.getElementById('loc-sheet');
      if (!sh) return 'no-sheet';
      const b = [...sh.querySelectorAll('button')].find(x => (x.textContent||'').trim() === '返回地圖');
      if (!b) return 'no-btn';
      b.click(); return 'clicked'; }""")
    pg.wait_for_timeout(2000)
    story_during = story_active(pg)
    ceremony_still = ceremony_active(pg)
    after = read_state(pg)
    print("C penetration:", penetrated, "story during ceremony:", story_during,
          "ceremony still:", ceremony_still, "before:", before, "after:", after, flush=True)
    pg.screenshot(path=os.path.join(SHOTS, "C_penetration.png"))
    # --- 撳跳過，典禮完，返地圖 → C6F 強制播 ---
    skipped = pg.evaluate("""() => {
      const b = document.querySelector('.awd62-skip');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(2000)
    print("C skipped:", skipped, "ceremony gone:", not ceremony_active(pg), flush=True)
    go_map(pg)
    t0 = time.time()
    sp = story_act191(pg)
    while time.time() - t0 < 60 and not sp.get('active'):
        # 典禮完之後晨鏈會先呈現 WF4 pending（set17 仲未播）——要撳埋佢，強制播先輪到
        if wf4_info(pg):
            handle_wf4(pg, "C_pending")
            pg.wait_for_timeout(700)
            sp = story_act191(pg)
            continue
        r = dismiss_once(pg)
        if r:
            pg.wait_for_timeout(700)
        sp = story_act191(pg)
        if map_visible(pg) and not sp.get('active'):
            # 再返一次地圖觸發晨鏈尾段（強制播掛返地圖路徑）
            go_map(pg)
            pg.wait_for_timeout(1500)
            sp = story_act191(pg)
        pg.wait_for_timeout(700)
    print("C after ceremony story:", sp, flush=True)
    pg.screenshot(path=os.path.join(SHOTS, "C_story_open.png"))
    c6f_done = None
    if sp.get('active'):
        play_story(pg, max_steps=90)
        pg.wait_for_timeout(800)
        click_first(pg, ["關閉"], 800)
        c6f_done = pg.evaluate("() => { try { return StoryOC.isDone('C6F'); } catch(e){ return 'err:'+String(e); } }")
    print("C C6F done:", c6f_done, flush=True)
    ok = (ceremony_seen and not story_during and ceremony_still
          and sp.get('act191') == "第 6 幕・電影線：片場跟班" and c6f_done is True)
    return {"ok": ok, "ceremony_seen": ceremony_seen, "invite_clicked": invite_clicked,
            "penetration": penetrated, "story_during_ceremony": story_during,
            "ceremony_still_after_probe": ceremony_still,
            "quota_before": before, "quota_after": after,
            "story": sp, "c6f_done": c6f_done}

def run_case_d(pg):
    """D：film_lion 池抽乾。seed 全部 113 單除咗 set26。"""
    except_id = "wf4_ev_set26"
    seen = {i: 1 for i in ALL_IDS if i != except_id}
    assert seed_seen(pg, seen), "seed D failed"
    titles = []
    fired = None
    attempts = 0
    # 每日入 film_lion 兩次（出行額度每日 2 次；locTriesPerDay=3，但 try 1 嘅 roll 喺 day 0–59
    # 對 film_lion 系統性偏高——hash 實測 try 1 零中、try 2 中 day 4／31／36／57；
    # 淨入一次要行到 day 31 先中，兩次就 day 4 有機會中）。
    for attempts in range(1, 36):
        for v in range(2):
            r, t = visit_loc(pg, 'film_lion', f"D_a{attempts}v{v}", titles)
            if r == 'wf4':
                fired = t
                break
        if fired:
            break
        r2, _ = start_today(pg, f"D_a{attempts}", titles)
        if r2 == 'no-start-btn':
            break
        print(f"D attempt {attempts}: visit {r}, advance {r2}", flush=True)
    print("D fired:", fired, "after attempts:", attempts, "titles:", titles, flush=True)
    pg.screenshot(path=os.path.join(SHOTS, "D_fired.png"))
    # 抽乾後再入 3 次（跨日）→ 零 WF4 modal
    extra = []
    for k in range(3):
        r, t = visit_loc(pg, 'film_lion', f"D_x{k}", extra)
        print(f"D extra {k}: {r} {t}", flush=True)
        if k < 2:
            start_today(pg, f"D_x{k}", extra)
    ok = (fired == TITLES[except_id] and len(titles) == 1 and len(extra) == 0)
    return {"ok": ok, "fired": fired, "expect": TITLES[except_id],
            "attempts": attempts, "titles": titles, "extra_after_exhaust": extra}

def run_case_e(pg):
    """E 700：pending-seed day05，斷言標題＋場景圖＋圖 200。"""
    assert new_game(pg, slot="1"), "new game E failed"
    r = seed_pending(pg, "wf4_ev_day05", 10)
    if not r.get('ok'):
        return {"ok": False, "why": "seed-failed", "seed": r}
    info = wf4_info(pg)
    if not info:
        go_map(pg)
        st = settle(pg, timeout_ms=8000)
        info = st[1] if st[0] == 'wf4' else wf4_info(pg)
    title_ok = bool(info) and info['title'] == TITLES["wf4_ev_day05"]
    scene_ok = bool(info and info['scene']) and "bg_loc_cafe_cha.jpg" in info['scene'] and http_ok(info['scene'])
    pg.screenshot(path=os.path.join(SHOTS, "E_700_day05.png"))
    if info:
        handle_wf4(pg, "E_day05")
        settle(pg, timeout_ms=8000)
        go_map(pg)
    return {"ok": bool(title_ok and scene_ok), "title": info['title'] if info else None,
            "scene": info['scene'] if info else None, "map": map_visible(pg)}

def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
    if "--targets" in sys.argv:
        _want = sys.argv[sys.argv.index("--targets") + 1].split(",")
        globals()['TARGETS_A'] = [t for t in TARGETS_A if t[0] in _want]
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
            pg.on("requestfailed", lambda r: REPORT["http_fail"].append(r.url))
            if not only or "B" in only:
                assert new_game(pg, slot="1"), "new game B failed"
                REPORT["cases"]["B_welcome"] = run_case_b(pg)
                print("B:", json.dumps(REPORT["cases"]["B_welcome"], ensure_ascii=False), flush=True)
            if not only or "A" in only:
                if not read_state(pg):
                    assert new_game(pg, slot="1"), "new game A failed"
                REPORT["cases"]["A_scene_tour"] = run_case_a(pg)
                print("A:", json.dumps(REPORT["cases"]["A_scene_tour"], ensure_ascii=False), flush=True)
            if not only or "C" in only:
                REPORT["cases"]["C_ceremony"] = run_case_c(pg)
                print("C:", json.dumps(REPORT["cases"]["C_ceremony"], ensure_ascii=False), flush=True)
            if not only or "D" in only:
                if not read_state(pg):
                    assert new_game(pg, slot="1"), "new game D failed"
                REPORT["cases"]["D_exhaust"] = run_case_d(pg)
                print("D:", json.dumps(REPORT["cases"]["D_exhaust"], ensure_ascii=False), flush=True)
            REPORT["cases"]["errors_932"] = errs
            br.close()
            if not only or "E" in only:
                br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
                pg = br.new_page(viewport={"width": 390, "height": 700})
                errs7 = []
                pg.on("pageerror", lambda e: errs7.append(str(e)))
                pg.on("console", lambda m: errs7.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
                pg.on("requestfailed", lambda r: REPORT["http_fail"].append(r.url))
                REPORT["cases"]["E_700"] = run_case_e(pg)
                print("E:", json.dumps(REPORT["cases"]["E_700"], ensure_ascii=False), flush=True)
                REPORT["cases"]["errors_700"] = errs7
                br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive203_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=2)
    print(json.dumps(REPORT, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
