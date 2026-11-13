# -*- coding: utf-8 -*-
"""v20a191 實駕：C6F 幕號修復（A 進度頁＋B 場景頂幕號）。
流程沿用調查報告 drive_c6f2.py（已驗證嘅 new_game／C1 真打／播種／強制播路徑）。
Cases（LIVE 模式，唔用 ?softPreview=1）：
  A_film (932)：C1 電影線 → 第 15 週 → 強制播 C6F → 場景頂「第 6 幕・電影線：片場跟班」
                → 播完 → 進度頁「第 6 幕・電影線 ✓ 已完成」，成頁冇「第 20／18／19 幕」。
  B_tv   (932)：C1 電視線 → 第 15 週 → 強制播 C6 → 場景頂「第 6 幕・電視線：飯堂閒角」
                → 播完 → 進度頁「第 6 幕・電視線 ✓ 已完成」。
  C_c18  (932)：C1 電視線 → 播種 C2–C6 done＋第 49 週（1990 冬）→ 強制播 C18
                → 場景頂「番外・1990 冬：上岸路」→ 播完 → 進度頁「番外・1990 冬 ✓ 已完成」。
  D_old  (700)：播種舊存檔（C6F done）寫入 slot 1（key starVolunteer_map_v19w）→ reload
                → 讀檔槽 1 → 進度頁「第 6 幕・電影線 ✓ 已完成」，700 闊驗排版。
用法：/home/hatch/pwenv49/bin/python ~/workspace/linji-work191/qa191/drive191.py
Mirror：工作副本 ~/workspace/linji-work191，port 8981，LIVE 模式。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work198"
HERE = "/home/hatch/workspace/linji-work198/qa198"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8988
URL = f"http://127.0.0.1:{PORT}/index.html"
REPORT = {"errors": [], "http_fail": [], "runs": {}}
FAILS = []


def check(name, cond, detail=""):
    print(("  PASS " if cond else "  FAIL ") + name + ((" :: " + str(detail)[:160]) if detail and not cond else ""), flush=True)
    if not cond:
        FAILS.append(name)
    return cond


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
    print("NEW GAME OK:", ok, pg.evaluate("() => window.S ? (S.dayIndex + ' ' + (S.dateStr||'')) : 'no S'"), flush=True)
    return ok


def dismiss_encounter(pg, max_clicks=16):
    for _ in range(max_clicks):
        if pg.evaluate("() => !document.getElementById('enc79-overlay')"):
            return True
        clicked = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay'); if (!ov) return false;
          const sk = ov.querySelector('.e79-skip'); if (sk && sk.offsetParent !== null) { sk.click(); return true; }
          const ch = ov.querySelector('.e79-choice'); if (ch) { ch.click(); return true; }
          const nb = [...ov.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return true; } return false; }""")
        if not clicked:
            return pg.evaluate("() => !document.getElementById('enc79-overlay')")
        pg.wait_for_timeout(700)
    return pg.evaluate("() => !document.getElementById('enc79-overlay')")


def js_click_text(pg, text):
    return pg.evaluate("""(t) => {
      const b = [...document.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def modal_click(pg, text):
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def story_state(pg):
    return pg.evaluate("""() => {
      const plate = document.querySelector('.story-play .dlg106-plate');
      const choices = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
      const mi = document.getElementById('modal-inner');
      const txt = mi ? (mi.textContent || '') : '';
      const act = document.querySelector('.sp-act191');
      const meta = document.querySelector('.sp-head-opening .sp-meta');
      const h3 = document.querySelector('.sp-head-opening h3');
      return { active: !!plate || choices.length > 0, choices: choices.length,
        choiceLabels: choices.map(c => (c.textContent || '').trim().slice(0, 60)),
        snippet: txt.replace(/\\s+/g, ' ').trim().slice(0, 200),
        act191: act ? act.textContent.trim() : null,
        meta: meta ? meta.textContent.trim() : null,
        nodeTitle: h3 ? h3.textContent.trim() : null }; }""")


def play_through_story(pg, pick_keyword=None, max_steps=100):
    picked = None
    for _ in range(max_steps):
        st = story_state(pg)
        if not st["active"]:
            return picked
        if st["choices"]:
            idx = 0
            if pick_keyword:
                for i, lab in enumerate(st["choiceLabels"]):
                    if pick_keyword in lab:
                        idx = i; break
            picked = st["choiceLabels"][idx] if st["choiceLabels"] else "?"
            pg.evaluate("""(i) => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
              if (c[i]) c[i].click(); }""", idx)
            pg.wait_for_timeout(1200)
            continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            return picked
        pg.wait_for_timeout(900)
    return picked


def open_loc_sheet(pg, name):
    js_click_text(pg, "返回地圖")
    pg.wait_for_timeout(1200)
    opened = pg.evaluate("""(nm) => {
      const root = document.querySelector('#v-map'); if (!root) return false;
      const b = [...root.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').includes(nm));
      if (!b) return false; b.click(); return true; }""", name)
    pg.wait_for_timeout(1500)
    dismiss_encounter(pg)
    return opened


def close_loc_sheet(pg):
    hit = pg.evaluate("""() => {
      const sh = document.getElementById('loc-sheet'); if (!sh) return false;
      const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === '返回地圖');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    return hit


SEED_JS = """(arg) => {
  const done = arg.done || {};
  S.dayIndex = arg.day;
  if (arg.fame) S.fame = arg.fame;
  if (arg.credit) S.industryCredit = arg.credit;
  if (arg.money) S.money = arg.money;
  S.story.done = Object.assign({}, S.story.done, done);
  S.story.lastMainDoneDay = arg.lastDoneDay;
  try { StoryOC.syncPhaseFromProgress(); } catch(e){}
  const oc = StoryOC.listOpen({checkNodePhase:true, player:true, ignoreSheetLoc:true});
  return {
    day: S.dayIndex, week: Math.floor(S.dayIndex/7)+1, phase: S.story.phase,
    routeFilm: StoryOC.getFlag('route_film'), routeTv: StoryOC.getFlag('route_tv'),
    open: (oc.open||[]).map(r=>r.id), done: (oc.done||[]).map(r=>r.id),
    lastMainDoneDay: S.story.lastMainDoneDay,
  };
}"""

PROGRESS_JS = """() => {
  const el = document.getElementById('progress-list');
  if (!el) return {found:false};
  const rows = [...el.querySelectorAll('.prog71-row')].map(r => {
    const act = r.querySelector('.prog71-act');
    const b = r.querySelector('b');
    const tag = r.querySelector('.prog71-tag');
    const items = [...r.querySelectorAll('.prog71-items li')].map(li => (li.textContent||'').trim());
    return { act: act ? act.textContent.trim() : '', title: b ? b.textContent.trim() : '',
      tag: tag ? tag.textContent.trim() : '', items };
  });
  return {found:true, rows, raw: (el.textContent||'').replace(/\\s+/g,' ').trim()};
}"""

DONE_JS = """() => ({ c6f: StoryOC.isDone('C6F'), c6: StoryOC.isDone('C6'),
  c18: StoryOC.isDone('C18'), c19: StoryOC.isDone('C19'),
  done: Object.keys(S.story.done||{}).filter(k => S.story.done[k]) })"""


def open_progress(pg):
    pg.evaluate("""() => { const cs = document.getElementById('chip-story');
      if (cs) cs.click(); return !!cs; }""")
    pg.wait_for_timeout(1200)
    pg.evaluate("""() => {
      const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null && (b.textContent||'').trim() === '進度');
      if (btns[0]) btns[0].click(); return btns.length; }""")
    pg.wait_for_timeout(900)
    return pg.evaluate(PROGRESS_JS)


def trigger_forced(pg):
    """閂地點 sheet 觸發 v165 強制播；唔得就過一日行晨鏈。"""
    print("  open 茶餐廳 sheet:", open_loc_sheet(pg, "茶餐廳"), flush=True)
    print("  close sheet:", close_loc_sheet(pg), flush=True)
    st = story_state(pg)
    print("  sheet-close 後 story:", json.dumps(st, ensure_ascii=False), flush=True)
    if st["active"]:
        return st, "sheet-close"
    js_click_text(pg, "過一日")
    for _ in range(120):
        pg.wait_for_timeout(500)
        st = story_state(pg)
        if st["active"]:
            break
        if pg.evaluate("() => !!document.getElementById('enc79-overlay')"):
            dismiss_encounter(pg); continue
        if modal_click(pg, "收下這份剪報"): continue
        if modal_click(pg, "返回地圖"): continue
        if modal_click(pg, "開始今日行程"): continue
        if modal_click(pg, "確定過一日"): continue
        if modal_click(pg, "關閉"): continue
        if modal_click(pg, "知道了"): continue
        if js_click_text(pg, "開始今日行程"): continue
    print("  morning 後 story:", json.dumps(st, ensure_ascii=False), flush=True)
    return st, "morning"


def play_c1_and_seed(pg, c1_keyword, seed_arg):
    """真打 C1（揀路線）→ 播種。回傳 seed 報告。"""
    assert new_game(pg), "new game failed"
    dismiss_encounter(pg)
    st = story_state(pg)
    print("  new_game 後 story active:", st["active"], flush=True)
    if not st["active"]:
        print("  open 茶餐廳觸發 C1:", open_loc_sheet(pg, "茶餐廳"), flush=True)
        close_loc_sheet(pg)
        st = story_state(pg)
        print("  觸發後 story active:", st["active"], flush=True)
    assert st["active"], "C1 未彈出，無法繼續"
    picked_c1 = play_through_story(pg, pick_keyword=c1_keyword)
    print("  C1 揀咗:", picked_c1, flush=True)
    pg.wait_for_timeout(800)
    modal_click(pg, "關閉")
    pg.wait_for_timeout(800)
    dismiss_encounter(pg)
    seed = pg.evaluate(SEED_JS, seed_arg)
    print("  seed:", json.dumps(seed, ensure_ascii=False), flush=True)
    return picked_c1, seed


def check_progress_no_bad_numbers(prog, tag):
    raw = prog.get("raw") or ""
    check(tag + "：進度頁冇「第 20 幕」", "第 20 幕" not in raw, raw[:200])
    check(tag + "：進度頁冇「第 18 幕」", "第 18 幕" not in raw, raw[:200])
    check(tag + "：進度頁冇「第 19 幕」", "第 19 幕" not in raw, raw[:200])


WF4_DUMP_JS = """() => {
  const st = (window.S && S.wf4) || null;
  const can = (typeof story165CanPlay === 'function') ? story165CanPlay() : 'n/a';
  const pend = (typeof enc79StoryPendingAt === 'function') ? enc79StoryPendingAt('cafe_cha') : 'n/a';
  const forced = (typeof todayIsForcedDay === 'function') ? todayIsForcedDay() : 'n/a';
  const sheet = document.getElementById('loc-sheet');
  const mi = document.getElementById('modal-inner');
  const mask = document.getElementById('mask');
  return { day: S ? S.dayIndex : null, wf4: st,
    canPlay: can ? can.id : null, pendingAtCafe: pend, forcedDay: forced,
    weekPlan: S ? S.weekPlan : null, todayPlan: (typeof todayPlanId === 'function') ? todayPlanId() : 'n/a',
    sheetOn: !!(sheet && sheet.classList.contains('on')),
    sheetVisible: !!(sheet && sheet.offsetParent !== null),
    maskOn: !!(mask && mask.classList.contains('on')),
    maskCls: mask ? mask.className : null,
    modalText: mi ? (mi.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 160) : null,
    encOverlay: !!document.getElementById('enc79-overlay') };
}"""

def dump(pg, tag):
    d = pg.evaluate(WF4_DUMP_JS)
    print(f"  [{tag}]", json.dumps(d, ensure_ascii=False), flush=True)
    return d

def modal_click_any(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return null; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return null; const t = bs[0].textContent.trim(); bs[0].click(); return t; }""")

def run_probe(pg, name):
    print(f"== PROBE {name} ==", flush=True)
    picked, seed = play_c1_and_seed(pg, "接電影散工賺快錢",
        {"day": 98, "done": {"C2": True, "C3": True, "C4": True, "C5": True},
         "lastDoneDay": 90, "fame": 26, "credit": 49, "money": 14936})
    print("  C1 picked:", picked, flush=True)
    dump(pg, "after-seed day98")
    print("  open 茶餐廳 sheet:", open_loc_sheet(pg, "茶餐廳"), flush=True)
    dump(pg, "after-open-cafe")
    print("  close sheet:", close_loc_sheet(pg), flush=True)
    dump(pg, "after-close-sheet")
    st = story_state(pg)
    print("  story_state:", json.dumps(st, ensure_ascii=False), flush=True)
    # If a WF4 modal is open (no .sp-act191), play it through via modal buttons
    for i in range(12):
        st = story_state(pg)
        if st.get("act191"):
            print("  TARGET STORY ACTIVE act191:", st.get("act191"), flush=True)
            break
        t = modal_click_any(pg)
        print(f"  modal click #{i}: {t!r}", flush=True)
        pg.wait_for_timeout(900)
        d = dump(pg, f"after-modal-click-{i}")
        if t is None:
            break
    st = story_state(pg)
    print("  final story_state:", json.dumps(st, ensure_ascii=False), flush=True)
    dump(pg, "final")
    return True

def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            for name in ["P1", "P2"]:
                pg = br.new_page(viewport={"width": 932, "height": 1500})
                pg.on("pageerror", lambda e, n=name: REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=name: REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    run_probe(pg, name)
                except Exception as e:
                    print(f"  !! {name} exception: {e}", flush=True)
                    REPORT["runs"][name] = {"error": str(e)}
                pg.close()
    finally:
        stop(srv)
    print("ERRORS:", json.dumps(REPORT["errors"], ensure_ascii=False), flush=True)
    print("HTTP_FAIL:", json.dumps(REPORT["http_fail"], ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
