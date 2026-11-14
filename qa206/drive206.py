# -*- coding: utf-8 -*-
"""v20a206 C1 實駕 drive206：迎新期保底（pity timer）＋tick 驗證，932，LIVE 模式（唔用 ?softPreview=1）。
用法：/home/hatch/pwenv49/bin/python qa206/drive206.py [--only T|W]
Mirror：工作副本 ~/workspace/linji-work206，port 8996，serve repo 原目錄（資產齊全）。
播種：經 new_game 正常開局（slot 1，key starVolunteer_map_v19w），播完 C1 故事返地圖。
Cases（932 同一個 browser 順序行，fresh 局各一）：
  T 逐日路線：每日入 tvb_longmen＋cafe_cha 各一次＋「過一日」，行到 day 30。
    （v203 drive B 同款；每日 tick 一次，對得上 sim 逐日模型。）
  W 成週跳日路線：每日入 tvb_longmen＋cafe_cha 各一次＋「開始今日行程」／「過一日」
    （start_today：有行程嗰日跑成週計劃，一次跳 3–4 日；review R2 同款）。
    驗 §14 殘留觀察：中間嗰幾日嘅 tick 係咪只跑落點日嗰次。
Trace（每步 snap 狀態）：dayIndex 序列（有冇跳日）、pending／pendingDay 變化、
seen 數、lastDay；每單 WF4 modal 記低出現嗰陣嘅 day＋標題＋id。
斷言：① dayIndex 由 0 到 30 逐日出現，冇跳號（＋code 事實 advanceDay 係唯一推進
路徑且每次 call wf4DailyTick，即係每日恰好一次 tick）；② 首單 ≤ day 7；
③ 頭 30 日 2–3 單（sim R 路線 3 單、S0 路線 2 單）；④ 全部唔同（once 規則）。
保底識別：sim 預測保底 pick 係 day 7、seen 空嗰陣 wf4_ev_day09「唱片舖試聽嗰首歌」；
正常日骰頭 15 日只得 day 4／day 10 擲中——首單若果係 day09＋pendingDay 7 就係保底派。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, sys, re

ROOT = "/home/hatch/workspace/linji-work206"
HERE = os.path.join(ROOT, "qa206")
SHOTS = os.path.join(HERE, "shots206")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8996
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
ID_BY_TITLE = {v: k for k, v in TITLES.items()}
PITY_PICK = "wf4_ev_day09"  # sim 預測：day 7、seen 空嗰陣保底 pick（見 qa206/sim_output.txt）

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
      const seen = (S.wf4 && S.wf4.seen) ? S.wf4.seen : null;
      let seenN = null, seenIds = null;
      if (seen) { seenIds = Object.keys(seen).filter(k => k !== '__n' && (seen[k] || 0) > 0); seenN = seenIds.length; }
      return { day: S.dayIndex,
        money: S.money, stress: S.stress, fame: S.fame,
        seen: seen, seenN: seenN, seenIds: seenIds,
        pending: (S.wf4 && S.wf4.pending) ? S.wf4.pending : null,
        pendingDay: (S.wf4) ? S.wf4.pendingDay : null,
        lastDay: (S.wf4) ? S.wf4.lastDay : null,
        locTries: (S.wf4) ? S.wf4.locTries : null }; }""")

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
        js_click_text(pg, "返回地圖")
        pg.wait_for_timeout(1200)
        go_map(pg)
    settle(pg, timeout_ms=8000)
    go_map(pg)
    st = read_state(pg)
    print("NEW GAME:", st and st['day'], "map:", map_visible(pg), flush=True)
    return st is not None and map_visible(pg)

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
    click_first(pg, ["讀檔"], 1200)
    pg.evaluate("(s) => { const b = document.querySelector('[data-slot=\"' + s + '\"]'); if (b && b.offsetParent !== null) { b.click(); return true; } return false; }", "1")
    pg.wait_for_timeout(1500)
    click_first(pg, ["覆蓋", "確定", "確認"], 800)
    settle(pg, timeout_ms=15000)
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

# ---------------- trace ----------------
class Trace:
    def __init__(self):
        self.snaps = []          # {step, note, day, pending, pendingDay, seenN, lastDay}
        self.days_seen = []      # 順序去重嘅 dayIndex
        self.pending_obs = []    # 每次見到 pending 非空：{day, pending, pendingDay}
        self.events = []         # {day, title, id}
        self._last = None
        self._step = 0
    def snap(self, pg, note):
        self._step += 1
        st = read_state(pg)
        if not st:
            return None
        key = (st['day'], st['pending'], st['pendingDay'], st['seenN'], st['lastDay'])
        if st['day'] not in self.days_seen:
            self.days_seen.append(st['day'])
        if st['pending']:
            self.pending_obs.append({'day': st['day'], 'pending': st['pending'], 'pendingDay': st['pendingDay']})
        if key != self._last:
            self._last = key
            self.snaps.append({'step': self._step, 'note': note, 'day': st['day'],
                               'pending': st['pending'], 'pendingDay': st['pendingDay'],
                               'seenN': st['seenN'], 'lastDay': st['lastDay']})
        return st
    def drain_titles(self, pg, titles, before_n):
        """將 visit/start/end 期間新出嘅 WF4 標題連同當日 dayIndex 記入 events。"""
        st = read_state(pg)
        day = st['day'] if st else None
        for t in titles[before_n:]:
            self.events.append({'day': day, 'title': t, 'id': ID_BY_TITLE.get(t)})
        return len(titles)

def run_route(pg, mode, trace):
    """mode 'T'：逐日過一日；mode 'W'：開始今日行程（成週跳日）。行到 day 30。"""
    titles = []
    start_day = (read_state(pg) or {}).get('day', 0)
    iters = 0
    while (read_state(pg) or {}).get('day', 99) < 30 and iters < 40:
        iters += 1
        st = read_state(pg)
        if not st:
            break
        trace.snap(pg, 'day-start d%d' % st['day'])
        for loc in ['tvb_longmen', 'cafe_cha']:
            n0 = len(titles)
            visit_loc(pg, loc, f"{mode}_d{st['day']}", titles)
            trace.drain_titles(pg, titles, n0)
            trace.snap(pg, 'after-visit %s d%d' % (loc, st['day']))
        n0 = len(titles)
        if mode == 'T':
            r, day1 = end_day_once(pg, f"{mode}_d{st['day']}", titles)
        else:
            r, day1 = start_today(pg, f"{mode}_d{st['day']}", titles)
        trace.drain_titles(pg, titles, n0)
        trace.snap(pg, 'after-advance -> %s (%s)' % (day1, r))
        print(f"{mode} day {st['day']} -> {day1} ({r}), wf4 so far ({len(trace.events)}): "
              f"{[(e['day'], e['id']) for e in trace.events]}", flush=True)
        if r == 'no-start-btn':
            break
    distinct = len(set(e['id'] for e in trace.events)) == len(trace.events)
    first = trace.events[0] if trace.events else None
    return {"ok": bool(first and first['day'] <= 7 and 2 <= len(trace.events) <= 3 and distinct),
            "events": trace.events, "n": len(trace.events), "distinct": distinct,
            "first": first, "start_day": start_day,
            "end_day": (read_state(pg) or {}).get('day'),
            "days_seen": trace.days_seen,
            "days_complete_0_30": trace.days_seen == list(range(0, max(trace.days_seen) + 1)) if trace.days_seen else False,
            "pending_obs": trace.pending_obs,
            "snaps": trace.snaps}

def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
            pg.on("requestfailed", lambda r: REPORT["http_fail"].append(r.url))
            if not only or "T" in only:
                assert new_game(pg, slot="1"), "new game T failed"
                tr = Trace()
                REPORT["cases"]["T_daily"] = run_route(pg, "T", tr)
                print("T:", json.dumps(REPORT["cases"]["T_daily"], ensure_ascii=False), flush=True)
            if not only or "W" in only:
                assert new_game(pg, slot="1"), "new game W failed"
                tr = Trace()
                REPORT["cases"]["W_weekjump"] = run_route(pg, "W", tr)
                print("W:", json.dumps(REPORT["cases"]["W_weekjump"], ensure_ascii=False), flush=True)
            REPORT["cases"]["errors_932"] = errs
            br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive206_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=2)
    print(json.dumps(REPORT, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
