# -*- coding: utf-8 -*-
"""v20a138 實駕 drive138（branch／pristine 兩跑，同一腳本）：
  目標 37 張（v138 全批，生檔先分好）：
  巧遇（真 UI 路徑：seed 星狀態 → 入主場 → ENC79 overlay 逐句行晒，
  揀指定 choice 分支；first／opener tier／heart／stageup／address／beat／pool 各有 seed）：
    chai T0(angry)＋heart(shy)＋beats fav30(chai_intel：shy T2開場＋smile＋think)｜
    chung heart(angry，1991+ 日，T3 開場)｜liu T1 fav15(surprise＋think pool T1[0]，beatsDone 封 foreshadow/tease)｜
    lok T2 fav30(shy)＋beats fav50 vocal40(smile＝lok_help，3 次 visit 輪 beat)｜
    luk first(angry)＋heart(smile)｜mak first(angry)＋heart(smile)｜
    ngai first(smile)＋T0(angry＋addr.extra)＋T0sup fav30 fame30(serious addr.support)
      ＋heart(serious)＋stageup(surprise)＋pool fav30 beatsDone=[ngai_intel](think＝pool T2[1]，2 次 visit)｜
    so T1 fav15(surprise)。
  主線／PACK／LIVE 17 節點合成（StoryPlay.start(id, {force:true})）：
    A_hakfan_ending｜C2｜C19｜A_fong_crisis｜A_tsijun_crisis｜A_tsijun_meet｜
    rumor_mai_zhendong_hide_injury｜F4_stay_mind｜A_ho_meet｜W3_liao_m27｜C12｜
    R_hiu_meet｜R_hiu_ending｜A_lei_ending｜R_xu_meet｜R_xu_ending｜R_vera_meet。
  監察：全程任何 fullbody 404 入 LOG；特別監察 lin_hiu_surprise 有冇被探測。
  用法：pwenv49 python qa138/drive138.py [root] [branch|pristine] [all|enc|story|tag1,tag2,...]
  v138r2 修正（run1 教訓）：
  - WF4 隨機事件會喺入場嗰陣開 modal 遮住地圖（#mask.wf4-stage-on），之後所有 click 失效——
    每次 set_day 後壓住 S.wf4.lastDay=當日＋pending=null（wf4TryLocEvent 即 return false），
    另加 clear_blockers() 兜底行走任何 modal。
  - 計劃錯誤修正（以 index.html 真 DLG／BEATS 為準，唔信 resolver 嘅 section 標籤）：
    liu surprise/think 係 T1／pool T1[0]（唔係 T0／heart）；lok shy 係 T2；chai smile/think 係
    beat chai_intel；lok smile 係 beat lok_help（要 tier≥3＋vocal≥35，beat 次序第 3）；ngai think
    係 pool T2[1]（要 2 次 pool visit）；so surprise 係 T1；chung angry 係 T3 開場。
  - beat sweep：seed 一次，之後逐日只設 dayIndex，beatsDone／poolSeen 自然累積。
  - resume：讀 qa138/drive138_cum.json（seen＋phases），每 phase 完即存。
  - trace：每步 L/R src＋line 寫入 qa138/drive138_trace_<MODE>_<ONLY>.jsonl。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE = sys.argv[2] if len(sys.argv) > 2 else "branch"
ONLY = sys.argv[3] if len(sys.argv) > 3 else "all"
HERE = os.path.join(ROOT, "qa138")
SHOTS = os.path.join(HERE, "shots138")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8971
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
BEATS = json.load(open(os.path.join(HERE, "enc_beats138.json"), encoding="utf-8"))

# v138 fix-up (2026-11-12): classified DEAD by live classifier + probe (see verdict138_addendum.md):
# - lin_hiu_serious.webp: only evidence line is pack R_hiu_meet; runtime swaps to mock (gate C3)
#   whose hiu lines classify neutral/neutral/sad; no live line classifies serious.
# - tsui_poushan_serious.webp: evidence lines are stale pack text; all 17 LIVE tsui lines
#   classify neutral 12 / angry 1 / think 1 / shy 1 / surprise 1 / happy 1; zero serious.
# Both stay in the library (harmless fallback) but are EXCLUDED from the PASS criteria.
DEAD = {"lin_hiu_serious.webp", "tsui_poushan_serious.webp"}
TARGETS = ["chai_zanhoi_angry.webp", "chai_zanhoi_shy.webp", "chai_zanhoi_smile.webp",
           "chai_zanhoi_think.webp", "cheung_hakfan_serious.webp", "cheung_tsijun_sad.webp",
           "cheung_tsijun_think.webp", "chung_choning_angry.webp", "crew_laolinji_serious.webp",
           "extra_ad_fen_sad.webp", "extra_ad_fen_serious.webp", "ho_sang_surprise.webp",
           "ko_chunkit_shy.webp", "ko_chunkit_think.webp", "lin_hiu_serious.webp",
           "lin_hiu_smile.webp", "liu_bingxing_sad.webp", "liu_bingxing_surprise.webp",
           "liu_bingxing_think.webp", "lok_gasing_angry.webp", "lok_gasing_shy.webp",
           "lok_gasing_smile.webp", "lok_gasing_surprise.webp", "lui_ging_serious.webp",
           "luk_baakyin_angry.webp", "luk_baakyin_sad.webp", "luk_baakyin_smile.webp",
           "mak_zhendong_angry.webp", "mak_zhendong_smile.webp", "ngai_wingnaam_angry.webp",
           "ngai_wingnaam_serious.webp", "ngai_wingnaam_smile.webp", "ngai_wingnaam_surprise.webp",
           "ngai_wingnaam_think.webp", "so_jiyan_surprise.webp", "tsui_poushan_serious.webp",
           "vera_serious.webp"]
assert len(TARGETS) == 37
LOG = {"mode": MODE, "phases": {}, "errors": [], "http404": [], "target404": {},
       "rendered": {}, "seen": {}, "lin_hiu_surprise_probe": []}
CUM_PATH = os.path.join(HERE, "drive138_cum.json")
TRACE_PATH = os.path.join(HERE, f"drive138_trace_{MODE}_{ONLY.replace(',', '_')}.jsonl")
if os.path.exists(CUM_PATH):
    try:
        _cum = json.load(open(CUM_PATH, encoding="utf-8"))
        LOG["seen"].update(_cum.get("seen", {}))
        LOG["phases"].update(_cum.get("phases", {}))
        print(f"resume: loaded {len(LOG['seen'])} seen targets from {CUM_PATH}", flush=True)
    except Exception as e:
        print("resume load failed:", e, flush=True)

def save_cum():
    try:
        json.dump({"mode": MODE, "seen": LOG["seen"], "phases": LOG["phases"]},
                  open(CUM_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except Exception as e:
        print("save_cum failed:", e, flush=True)

def trace(rec):
    try:
        with open(TRACE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass

def http_status(path):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
            return r.status, len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, 0
    except Exception:
        return None, 0

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} probably taken)")
    st, body = http_body("index.html")
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

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return { present: false };
  const one = (sel) => { const im = ov.querySelector(sel); if (!im) return null;
    return { src: (im.getAttribute('src')||'').split('/').pop().split('?')[0] }; };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  const chs = [...ov.querySelectorAll('.e79-choice')].map(b => b.textContent.trim());
  return { present: true, L: one('.e79-char-l'), R: one('.e79-char-r'),
           name: name ? name.textContent : null,
           line: line ? line.textContent : null, choices: chs };
}'''

JS_STORY = '''() => {
  const chars = [...document.querySelectorAll('.dlg106-char')].map(im => ({
    id: im.dataset.dlgId, src: (im.getAttribute('src')||'').split('/').pop().split('?')[0] }));
  const sp = document.querySelector('.story-play');
  const speaker = document.querySelector('.story-play .sp-speaker');
  const line = document.querySelector('.story-play .sp-line');
  const choices = [...document.querySelectorAll('.sp-choice')].map(b => b.textContent.trim());
  return { active: !!sp, chars, speaker: speaker ? speaker.textContent : null,
           line: line ? line.textContent : null, choices };
}'''

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

def seed_star(pg, star, met, fav, stage, beats_done=None, heart_done=False, home_visits=0, fame=0, vocal=None, story_done=None):
    pg.evaluate("""(a) => {
      S.stars = S.stars || {};
      const st = S.stars[a.star] || (S.stars[a.star] = {});
      st.met = !!a.met; st.fav = a.fav; st.stage = a.stage;
      st.beatsDone = {}; for (const b of (a.beats_done || [])) st.beatsDone[b] = 1;
      st.poolSeen = {}; st.heartDone = !!a.heart_done; st.wrapEcho = false;
      st.capHit = false; st.lastDay = -99; st.seen = st.seen || 0;
      st.homeVisits = a.home_visits; st.homeVisitDay = -1;
      S.fame = a.fame;
      if (a.vocal !== null && a.vocal !== undefined) S.vocal = a.vocal;
      // story_done：將主線節點標記為已完成——清 enc79StoryPendingAt 壓制
      // （例如 C9 喺 softPreview 下 soft loc 係 rec_star，未做會壓住嗰度嘅巧遇攔截）。
      if (a.story_done && a.story_done.length) {
        S.story = S.story || {}; S.story.done = S.story.done || {};
        for (const id of a.story_done) S.story.done[id] = 1;
      }
      return true;
    }""", {"star": star, "met": met, "fav": fav, "stage": stage,
            "beats_done": beats_done or [], "heart_done": heart_done,
            "home_visits": home_visits, "fame": fame, "vocal": vocal,
            "story_done": story_done or []})

def isolate_star(pg, star):
    """獨佔觸發：除咗目標星，其他 11 星全部 lastDay=當日（冷卻 3 日濾走，唔會搶 pick）；
    目標星 lastDay=-99（sweep 連日 visit 都唔會俾冷卻擋住）。"""
    pg.evaluate("""(a) => {
      S.stars = S.stars || {};
      const day = S.dayIndex|0;
      const ids = ["luk_baakyin","liu_bingxing","ngai_wingnaam","yip_manji","mak_zhendong","lok_gasing","pang_siuki","chung_choning","gu_mingfai","so_jiyan","chai_zanhoi","ching_tinlok"];
      for (const id of ids) {
        const st = S.stars[id] || (S.stars[id] = {});
        st.lastDay = (id === a.star) ? -99 : day;
      }
      return true; }""", {"star": star})

def suppress_wf4(pg):
    """壓住 WF4 隨機事件：lastDay=當日令 wf4TryLocEvent 即回 false；清 pending 防返地圖嗰陣彈出。"""
    pg.evaluate("""() => {
      try { if (typeof wf4Ensure === 'function') { const st = wf4Ensure(); if (st) { st.lastDay = S.dayIndex|0; st.pending = null; } } } catch(_e) {}
      return true; }""")

def clear_blockers(pg):
    """行走任何遮住地圖嘅 modal（WF4 事件 modal #mask.wf4-stage-on／其他 modal）：
    逐個撳 #modal-btns 第一個可見掣，直至遮罩消失。ENC overlay 本身唔喺呢度處理。"""
    for _ in range(15):
        st = pg.evaluate("""() => {
          const mask = document.getElementById('mask');
          const wf4 = mask && mask.classList.contains('wf4-stage-on');
          const row = document.getElementById('modal-btns');
          const vis = row ? [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled) : [];
          return { wf4: !!wf4, nBtns: vis.length,
                   modalOpen: !!(document.querySelector('.modal.open') || (row && vis.length)) }; }""")
        if not st["wf4"] and not st["modalOpen"]:
            return False
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            return True
        pg.wait_for_timeout(400)
    return True

def back_to_map(pg):
    click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
    pg.wait_for_timeout(700)

def record(pg, tag, targets, srcs, line, step):
    """srcs 出現目標檔即記低（連同當時對白行）；回傳新見嘅目標。"""
    global LOG
    newly = []
    for s in srcs:
        if s in targets and s not in LOG["seen"]:
            LOG["seen"][s] = {"phase": tag, "step": step, "line": (line or "")[:70]}
            newly.append(s)
            pg.screenshot(path=f"{SHOTS}/{MODE}_{tag}_{s.replace('.webp', '')}.png")
            print(f"  >> {tag}[{step}] TARGET {s} :: {(line or '')[:60]}", flush=True)
    return newly

def step_overlay(pg, targets, tag, wanted, attempt, max_steps=60):
    """行一個 ENC79 overlay；wanted = 想揀嘅 choice label 子串清單。
    冇 wanted 命中就按 attempt 輪換揀 choice。"""
    seen_here = set()
    for i in range(max_steps):
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            break
        srcs = [c["src"] for c in (info["L"], info["R"]) if c and c.get("src")]
        trace({"phase": tag, "attempt": attempt, "step": i, "kind": "enc",
               "L": (info["L"] or {}).get("src"), "R": (info["R"] or {}).get("src"),
               "name": info.get("name"), "line": (info.get("line") or "")[:80],
               "choices": info.get("choices")})
        for s in record(pg, tag, targets, srcs, info.get("line"), i):
            seen_here.add(s)
        if seen_here == set(targets):
            # 行埋落去都得，但目標齊晒就停，慳時間
            pass
        clicked = pg.evaluate("""(a) => {
          const chs = [...document.querySelectorAll('.e79-choice')].filter(b => b.offsetParent !== null);
          if (chs.length) {
            let t = null;
            for (const w of a.wanted) {
              const m = chs.find(b => (b.textContent||'').indexOf(w) >= 0);
              if (m) { t = m; break; }
            }
            if (!t) t = chs[a.attempt % chs.length];
            t.click(); return 'choice:' + (t.textContent||'').trim().slice(0,24);
          }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null && !b.classList.contains('e79-skip'));
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""", {"wanted": wanted, "attempt": attempt})
        if not clicked:
            break
        pg.wait_for_timeout(420)
    return seen_here

def try_days_enc(pg, loc_label, days, targets, tag, seed, wanted, max_attempts=4, sweep=False):
    """逐日試：每日重設 seed → 入場 → 有 overlay 就行晒佢。attempt 輪換 choice。
    sweep=True：只喺第一日 seed，之後逐日只設 dayIndex（beatsDone／poolSeen 自然累積，逐個 beat／pool 輪住出）。
    回傳 (seen, overlay_days)。"""
    seen_all = set()
    overlay_days = []
    attempts = 0
    seeded = False
    for day in days:
        if seen_all == set(targets) or attempts >= max_attempts:
            break
        if not sweep or not seeded:
            seed_star(pg, **seed)
            seeded = True
        pg.evaluate("(d) => { S.dayIndex = d; }", day)
        suppress_wf4(pg)
        isolate_star(pg, seed["star"])
        back_to_map(pg)
        clear_blockers(pg)
        clicked = click_first(pg, [loc_label], 1800)
        pg.wait_for_timeout(900)
        clear_blockers(pg)
        info = pg.evaluate(JS_ENC)
        trace({"phase": tag, "day": day, "kind": "day_attempt", "clicked": clicked,
               "overlay": info["present"],
               "presence": pg.evaluate("() => (S.starDay && S.starDay.presence) || {}"),
               "wf4": pg.evaluate("() => !!(document.getElementById('mask')||{}).classList && document.getElementById('mask').classList.contains('wf4-stage-on')")})
        if not info["present"]:
            back_to_map(pg)
            clear_blockers(pg)
            continue
        # 錯星守衛：overlay 嘅星唔係目標星（L/R 圖檔唔以目標星 id 開頭）→ skip 佢，唔計 attempt
        star_ok = pg.evaluate("""(a) => {
          const ov = document.getElementById('enc79-overlay'); if (!ov) return false;
          const srcs = [...ov.querySelectorAll('img')].map(im => (im.getAttribute('src')||'').split('/').pop().split('?')[0]);
          return srcs.some(x => x.indexOf(a.star + '_') === 0); }""", {"star": seed["star"]})
        if not star_ok:
            print(f"  [{tag}] day {day}: WRONG STAR overlay, skipping", flush=True)
            pg.evaluate("""() => { const sk = document.querySelector('.e79-skip'); if (sk) sk.click(); return true; }""")
            pg.wait_for_timeout(600)
            back_to_map(pg)
            clear_blockers(pg)
            continue
        overlay_days.append(day)
        print(f"  [{tag}] day {day}: overlay (attempt {attempts})", flush=True)
        seen = step_overlay(pg, targets, tag, wanted, attempts)
        seen_all |= seen
        print(f"  [{tag}] day {day}: seen={sorted(seen)}", flush=True)
        attempts += 1
        back_to_map(pg)
        clear_blockers(pg)
    return seen_all, overlay_days

def step_story(pg, targets, tag, wanted, attempt, max_steps=90):
    found = set()
    for step in range(max_steps):
        info = pg.evaluate(JS_STORY)
        srcs = [c["src"] for c in info["chars"]]
        for s in record(pg, tag, targets, srcs, info.get("line"), step):
            found.add(s)
        trace({"phase": tag, "attempt": attempt, "step": step, "kind": "story",
               "L": srcs[0] if srcs else None, "R": srcs[1] if len(srcs) > 1 else None,
               "line": (info.get("line") or "")[:80]})
        if found == set(targets):
            return found, step + 1
        if not info["active"]:
            break
        if info["choices"]:
            # 揀 wanted 先，否則輪換
            pick = None
            for w in wanted:
                for c in info["choices"]:
                    if w in c:
                        pick = c
                        break
                if pick:
                    break
            if not pick:
                pick = info["choices"][attempt % len(info["choices"])]
            click_first(pg, [pick[:8]], 1500)
            pg.wait_for_timeout(1200)
            for _ in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續"], 900):
                    break
            continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            break
        pg.wait_for_timeout(500)
    return found, max_steps

def play_story(pg, node, targets, tag, wanted, max_attempts=3):
    found_all = set()
    for attempt in range(max_attempts):
        if found_all == set(targets):
            break
        ok = pg.evaluate("""(n) => {
          try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) {}
          return false; }""", node)
        print(f"  [{tag}] StoryPlay.start({node}) attempt {attempt}: {ok}", flush=True)
        if not ok:
            break
        pg.wait_for_timeout(1500)
        found, n = step_story(pg, targets, tag, wanted, attempt)
        found_all |= found
        print(f"  [{tag}] attempt {attempt}: found={sorted(found)} steps={n}", flush=True)
        back_to_map(pg)
        pg.wait_for_timeout(600)
    return found_all

def sheet_open(pg):
    """地點 sheet 是否已開（標題唔係預設「地點」）。"""
    try:
        return pg.evaluate("""() => {
          const t = (document.getElementById('loc-title')||{}).textContent || '';
          return t.trim() !== '' && t.trim() !== '地點'; }""")
    except Exception:
        return False

def open_loc_retry(pg, loc_sub, max_tries=3):
    """撳地點針開 sheet（新遊戲後第一次撳針間歇性靜默失效——開唔到就重撳）。
    只喺 sheet 未開嗰陣重試；開咗就唔再撳（免浪費出行額度）。
    用 DOM .click() 而唔係 Playwright click——海港針中心俾嘢遮住，
    Playwright hit-test 會 timeout（probe_fen 證實：pin 可見 52×52 但
    click_first 回 None），DOM click 繞過 hit-testing（probe10/12 證實開到）。"""
    for i in range(max_tries):
        clicked = pg.evaluate("""(sub) => {
          const pins = [...document.querySelectorAll('button.pin[data-loc]')];
          const p = pins.find(b => (b.textContent||'').includes(sub));
          if (!p) return false;
          p.click(); return true;
        }""", loc_sub)
        if not clicked:
            print(f"  [open_loc_retry] {loc_sub} try {i}: pin not found", flush=True)
            back_to_map(pg)
            pg.wait_for_timeout(400)
            continue
        pg.wait_for_timeout(700)
        if sheet_open(pg):
            return True
        print(f"  [open_loc_retry] {loc_sub} try {i}: sheet not open, retry", flush=True)
        back_to_map(pg)
        pg.wait_for_timeout(400)
    return sheet_open(pg)

def play_offer(pg, loc_sub, day, action, seed_expr, targets, tag, wanted, max_attempts=2):
    """真 UI 路徑：地點 sheet 入面嘅 action 掣（choice47ActionsAt／wf4FenActionsAt 渲染）。
    StoryPlay.start 搵唔到 CHOICE47／WF4 節點，所以唔可以用 synthetic route。
    seed_expr 係直接寫入 S 嘅 JS 陳述（例如 exodusFenSeeded=true）。"""
    found_all = set()
    for attempt in range(max_attempts):
        if found_all == set(targets):
            break
        new_game(pg)
        pg.evaluate(f"""() => {{ const S = window.S; S.dayIndex = {day}; {seed_expr} }}""")
        suppress_wf4(pg)
        isolate_star(pg, "__none__")  # 全部 12 星 lastDay=當日，ENC 唔會搶
        back_to_map(pg)
        if not open_loc_retry(pg, loc_sub):
            print(f"  [{tag}] offer: loc '{loc_sub}' sheet never opened", flush=True)
            continue
        pg.wait_for_timeout(1000)
        # DOM .click() 撳 action 掣——Playwright click 喺滑入中嘅 sheet 上間歇性
        # actionability timeout（fix-up 兩次都係呢度跌），DOM click 繞過佢。
        act_ok = pg.evaluate("""(a) => {
          const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(a));
          const vis = bs.find(b => b.offsetParent !== null) || bs[0];
          if (!vis) return false;
          vis.click(); return true;
        }""", action)
        if not act_ok:
            dbg = pg.evaluate("""() => {
              const t = (document.getElementById('loc-title')||{}).textContent || '';
              const acts = [...document.querySelectorAll('#loc-acts button')].map(b => (b.textContent||'').trim().slice(0,40));
              return { title: t.trim(), acts }; }""")
            print(f"  [{tag}] offer: action '{action}' not found; sheet={dbg}", flush=True)
            back_to_map(pg)
            continue
        pg.wait_for_timeout(1500)
        found, n = step_story(pg, targets, tag, wanted, attempt)
        found_all |= found
        print(f"  [{tag}] offer attempt {attempt}: found={sorted(found)} steps={n}", flush=True)
        back_to_map(pg)
        pg.wait_for_timeout(600)
    return found_all

def play_farewell(pg, targets, tag, wanted, max_attempts=2):
    """芬姐送別：seed arm → 撳「過一日」→ 日結流程返地圖（goToMapForBrowse →
    wf4PresentPending → wf4PresentFenFarewell 優先）。注意：地點 sheet 嘅「返回地圖」
    只係 closeSheet，唔會行 goToMapForBrowse，所以一定要經「過一日」。"""
    found_all = set()
    for attempt in range(max_attempts):
        if found_all == set(targets):
            break
        new_game(pg)
        pg.evaluate("""() => {
          const S = window.S;
          S.exodusFenFired = true; S.wf4FenFarewell = null;
          try { const st = wf4Ensure(); if (st) { st.fenFarewellDone = false; st.pending = null; st.lastDay = S.dayIndex|0; } } catch(_e) {}
          return true; }""")
        suppress_wf4(pg)
        isolate_star(pg, "__none__")
        back_to_map(pg)
        if not click_first(pg, ["過一日"], 1500):
            print(f"  [{tag}] farewell: '過一日' click failed", flush=True)
            continue
        pg.wait_for_timeout(1200)
        # 返地圖流程可能先彈晨報／請柬／日結 modal，逐個行走直至 story-play 出現
        for _ in range(8):
            st = pg.evaluate(JS_STORY)
            if st["active"]:
                break
            if not clear_blockers(pg):
                break
            pg.wait_for_timeout(700)
        found, n = step_story(pg, targets, tag, wanted, attempt)
        found_all |= found
        print(f"  [{tag}] farewell attempt {attempt}: found={sorted(found)} steps={n}", flush=True)
        back_to_map(pg)
        pg.wait_for_timeout(600)
    return found_all

ALL_BEATS = lambda star: BEATS.get(star, [])
# chung_farewell 唔可以入 beatsDone：enc79PresenceP 有離港閘——beatsDone.chung_farewell 成立
# 即當佢已離港，p=0 永遠唔出沒（1991 年佢個 farewell beat 本身未開閘，唔入亦唔會搶 heart）。
ALL_BEATS_MINUS = lambda star, *excl: [b for b in BEATS.get(star, []) if b not in excl]
# (tag, star, loc_label, seed_kwargs, days, targets, wanted, max_attempts, sweep)
# 修正依據（index.html 真數據，見 drive138 檔頭）：
#  - T0/T1/T2/T3 開場按 enc79TierOf(fav)：0→T0，10–24→T1，25–44→T2，45–69→T3
#  - pool：冇開 beat＋（tier<3 或 heartDone）先行，band tier≤1→T1／2→T2／≥3→T3，逐次輪最少見嗰段
#  - beat：enc79PickBeat 取表頭第一個 when 開＋未做；heart 要 tier≥3＋冇 beat 開＋!heartDone
ENC_PHASES = [
    ("e_chai_T0", "chai_zanhoi", "星河", dict(met=True, fav=0, stage=0), list(range(0, 12)),
     {"chai_zanhoi_angry.webp"}, [], 4, False),
    ("e_chai_heart", "chai_zanhoi", "星河", dict(met=True, fav=50, stage=3, beats_done=ALL_BEATS("chai_zanhoi"), heart_done=False), list(range(0, 12)),
     {"chai_zanhoi_shy.webp"},
     ["安慰佢：一哥地位邊有咁易動搖", "唔出聲，佢大佬嚟，自己會諗", "勸佢停一停，唔好接呢套"], 4, False),
    ("e_chai_beats", "chai_zanhoi", "星河", dict(met=True, fav=30, stage=2), list(range(0, 12)),
     {"chai_zanhoi_shy.webp", "chai_zanhoi_smile.webp", "chai_zanhoi_think.webp"}, [], 3, False),
    # chung angry = pool T3[0]（「有天份冇用功…」），唔係 T3 opener 亦唔係 heart。
    # heartDone=True 先去到 pool（否則 heart 線搶先播晒成個 visit）。
    ("e_chung_heart", "chung_choning", "天星", dict(met=True, fav=50, stage=3, beats_done=ALL_BEATS_MINUS("chung_choning", "chung_farewell"), heart_done=True, story_done=["C9"]), list(range(365, 377)),
     {"chung_choning_angry.webp"}, ["問佢會唔會返嚟"], 4, False),
    ("e_liu_T1", "liu_bingxing", "金龍", dict(met=True, fav=15, stage=1, beats_done=["liu_foreshadow", "liu_tease"]), list(range(0, 12)),
     {"liu_bingxing_think.webp"}, [], 4, False),
    ("e_lok_T2", "lok_gasing", "星河", dict(met=True, fav=30, stage=2), list(range(0, 12)),
     {"lok_gasing_shy.webp"}, [], 4, False),
    ("e_lok_beats", "lok_gasing", "星河", dict(met=True, fav=50, stage=3, vocal=40), list(range(0, 41)),
     {"lok_gasing_smile.webp"}, [], 6, True),
    ("e_mak_heart", "mak_zhendong", "紅棉", dict(met=True, fav=50, stage=3, beats_done=ALL_BEATS("mak_zhendong"), heart_done=False), list(range(0, 12)),
     {"mak_zhendong_smile.webp"}, [], 4, False),
    ("e_ngai_first", "ngai_wingnaam", "維港", dict(met=False, fav=0, stage=0, home_visits=5), list(range(0, 12)),
     {"ngai_wingnaam_smile.webp"}, ["放低包紙巾就走，唔打擾"], 4, False),
    ("e_ngai_T0", "ngai_wingnaam", "維港", dict(met=True, fav=0, stage=0, fame=0), list(range(0, 12)),
     {"ngai_wingnaam_angry.webp"}, [], 4, False),
    ("e_ngai_T0sup", "ngai_wingnaam", "維港", dict(met=True, fav=30, stage=2, fame=30), list(range(0, 12)),
     {"ngai_wingnaam_serious.webp"}, [], 4, False),
    ("e_ngai_heart", "ngai_wingnaam", "維港", dict(met=True, fav=50, stage=3, beats_done=ALL_BEATS("ngai_wingnaam"), heart_done=False), list(range(0, 12)),
     {"ngai_wingnaam_serious.webp"},
     ["笑住話怕自己學唔嚟", "買杯熱茶畀佢暖下手", "笑住話下次先慢慢學"], 4, False),
    ("e_ngai_stageup", "ngai_wingnaam", "維港", dict(met=True, fav=15, stage=0), list(range(0, 12)),
     {"ngai_wingnaam_surprise.webp"}, [], 4, False),
    ("e_ngai_pool", "ngai_wingnaam", "維港", dict(met=True, fav=30, stage=2, beats_done=["ngai_intel"]), list(range(0, 12)),
     {"ngai_wingnaam_think.webp"}, [], 6, True),
    ("e_so_T1", "so_jiyan", "灣仔", dict(met=True, fav=15, stage=1), list(range(0, 12)),
     {"so_jiyan_surprise.webp"}, [], 4, False),
    # 以下已見晒，resume 會自動跳過（留低做完整清單對照）
    ("e_liu_heart", "liu_bingxing", "金龍", dict(met=True, fav=50, stage=3, beats_done=ALL_BEATS("liu_bingxing"), heart_done=False), list(range(0, 12)),
     {"liu_bingxing_sad.webp"}, ["用笑話接住"], 4, False),
    ("e_lok_first", "lok_gasing", "星河", dict(met=False, fav=0, stage=0, home_visits=5), list(range(0, 12)),
     {"lok_gasing_angry.webp"}, ["笑佢脾氣咁大，抵佢冇運行"], 4, False),
    ("e_lok_stageup", "lok_gasing", "星河", dict(met=True, fav=15, stage=0), list(range(0, 12)),
     {"lok_gasing_surprise.webp"}, [], 4, False),
    ("e_luk_first", "luk_baakyin", "獅子山", dict(met=False, fav=0, stage=0, home_visits=5), list(range(0, 12)),
     {"luk_baakyin_angry.webp"}, ["趁機介紹自己"], 4, False),
    ("e_luk_heart", "luk_baakyin", "獅子山", dict(met=True, fav=50, stage=3, beats_done=ALL_BEATS("luk_baakyin"), heart_done=False), list(range(0, 12)),
     {"luk_baakyin_smile.webp"}, ["靜靜聽落去", "講句安慰話", "笑住帶過"], 4, False),
    ("e_mak_first", "mak_zhendong", "紅棉", dict(met=False, fav=0, stage=0, home_visits=5), list(range(0, 12)),
     {"mak_zhendong_angry.webp"}, ["開口問佢傷勢"], 4, False),
]
STORY_PHASES = [
    ("s_hakfan_end", "A_hakfan_ending", {"cheung_hakfan_serious.webp"}, []),
    ("s_c2", "C2", {"crew_laolinji_serious.webp"}, []),
    ("s_c19", "C19", {"crew_laolinji_serious.webp"}, []),
    ("s_fong_crisis", "A_fong_crisis", {"cheung_hakfan_serious.webp", "ko_chunkit_think.webp"}, []),
    ("s_tsijun_crisis", "A_tsijun_crisis", {"cheung_tsijun_sad.webp"}, []),
    ("s_tsijun_meet", "A_tsijun_meet", {"cheung_tsijun_think.webp"}, []),
    # fix-up：offer／farewell 真 UI 路徑（StoryPlay.start 搵唔到 CHOICE47／WF4 節點；
    # 唯一活路係地點 sheet action 掣／過一日返地圖流程；見 verdict138_addendum.md）
    ("s_fen_intro", "WF4_fen_intro", {"extra_ad_fen_sad.webp", "extra_ad_fen_serious.webp"}, [],
     "offer:海港:400:芬姐喺茶水帳揚手叫你:S.exodusFenSeeded=true;S.exodusFenFired=false;"),
    ("s_fen_farewell", "WF4_fen_farewell", {"extra_ad_fen_serious.webp"}, [], "farewell"),
    ("s_f4", "F4_stay_mind", {"ho_sang_surprise.webp"}, [],
     "offer:事務所:920:何生有句說話想同你講:"),
    ("s_ho_meet", "A_ho_meet", {"ko_chunkit_shy.webp"}, []),
    ("s_w3_liao", "W3_liao_m27", {"liu_bingxing_sad.webp"}, []),
    ("s_c12", "C12", {"luk_baakyin_sad.webp"}, []),
    # s_hiu_meet 已刪：lin_hiu_serious 判死（見 verdict138_addendum.md）——
    # pack R_hiu_meet 唯一 serious 句永遠播唔到（mock 換走＋閘），唔跑
    ("s_hiu_end", "R_hiu_ending", {"lin_hiu_smile.webp"}, []),
    ("s_lei_end", "A_lei_ending", {"lui_ging_serious.webp"}, []),
    # s_xu_meet／s_xu_end 已刪：tsui_poushan_serious 判死（見 verdict138_addendum.md）——
    # 17 句 live 徐寶珊句零 serious，pack 兩句係舊版文本，唔跑
    ("s_vera_meet", "R_vera_meet", {"vera_serious.webp"}, []),
]

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        def on_resp(resp):
            try:
                u = resp.url
                if "assets/story/fullbody/" in u and resp.status >= 400:
                    fn = u.split("/").pop().split("?")[0]
                    LOG["http404"].append({"file": fn, "status": resp.status})
                    if fn in TARGETS:
                        LOG["target404"][fn] = LOG["target404"].get(fn, 0) + 1
                    if fn == "lin_hiu_surprise.webp":
                        LOG["lin_hiu_surprise_probe"].append({"status": resp.status, "url": u})
            except Exception:
                pass
        pg.on("response", on_resp)
        if MODE == "branch":
            chk = {}
            for n in TARGETS:
                st, ln = http_status("assets/story/fullbody/" + n)
                chk[n] = (st == 200 and ln == os.path.getsize(os.path.join(ROOT, "assets", "story", "fullbody", n)))
            print("server check all 37 ok:", all(chk.values()), flush=True)
            assert all(chk.values()), "server check failed — abort"

        WANT_TAGS = None if ONLY in ("all", "enc", "story") else set(ONLY.split(","))
        if ONLY in ("all", "enc") or WANT_TAGS:
            for tag, star, loc, kw, days, tgts, wanted, max_att, sweep in ENC_PHASES:
                if WANT_TAGS and tag not in WANT_TAGS:
                    continue
                pending = {t for t in tgts if t not in LOG["seen"]}
                if not pending:
                    print(f"== {tag}: targets already seen, skip ==", flush=True)
                    continue
                print(f"== {tag} ({star} @ {loc}) targets={sorted(pending)} ==", flush=True)
                new_game(pg)
                seed = dict(kw)
                seed["star"] = star
                seen, odays = try_days_enc(pg, loc, days, pending, tag, seed, wanted,
                                            max_attempts=max_att, sweep=sweep)
                LOG["phases"][tag] = {"seen": sorted(seen), "overlay_days": odays,
                                       "missing": sorted(pending - seen)}
                save_cum()
                print(f"  {tag} DONE seen={sorted(seen)} missing={sorted(pending - seen)}", flush=True)

        if ONLY in ("all", "story") or WANT_TAGS:
            print("== story synthetic (one game) ==", flush=True)
            new_game(pg)
            for ph in STORY_PHASES:
                tag, node, tgts, wanted = ph[0], ph[1], ph[2], ph[3]
                route = ph[4] if len(ph) > 4 else ""
                if WANT_TAGS and tag not in WANT_TAGS:
                    continue
                pending = {t for t in tgts if t not in LOG["seen"]}
                if not pending:
                    print(f"== {tag}: targets already seen, skip ==", flush=True)
                    continue
                print(f"== {tag} ({node}) route={route or 'synthetic'} targets={sorted(pending)} ==", flush=True)
                if route.startswith("offer:"):
                    _, loc_sub, day_s, action, seed_expr = route.split(":", 4)
                    found = play_offer(pg, loc_sub, int(day_s), action, seed_expr, pending, tag, wanted)
                    rname = "offer"
                elif route == "farewell":
                    found = play_farewell(pg, pending, tag, wanted)
                    rname = "farewell"
                else:
                    found = play_story(pg, node, pending, tag, wanted)
                    rname = "synthetic"
                LOG["phases"][tag] = {"route": rname, "found": sorted(found),
                                       "missing": sorted(pending - found)}
                save_cum()
                print(f"  {tag} DONE found={sorted(found)} missing={sorted(pending - found)}", flush=True)

        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

missing = sorted(set(TARGETS) - set(LOG["seen"]) - DEAD)
LOG["missing"] = missing
LOG["dead_excluded"] = sorted(DEAD)
LOG["PASS"] = bool(not missing and not LOG["target404"] and not LOG["errors"])
print("seen:", sorted(LOG["seen"]), flush=True)
print("missing:", missing, flush=True)
print("target404:", LOG["target404"], flush=True)
print("all404:", LOG["http404"][:12], flush=True)
print("lin_hiu_surprise probes:", LOG["lin_hiu_surprise_probe"], flush=True)
print("pageerrors:", LOG["errors"][:6], flush=True)
print("OVERALL PASS:", LOG["PASS"], flush=True)
with open(os.path.join(HERE, f"drive138_{MODE}_{ONLY}.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
