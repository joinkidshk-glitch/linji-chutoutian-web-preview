# -*- coding: utf-8 -*-
"""v20a198 實駕：B1 強制播優先於 WF4 boss01＋C1 死 code 清除＋C2 鎖住插入行＋C3 場景行唔重複路線名。
LIVE 模式，唔用 ?softPreview=1。播種用 S 直接寫（沿用 qa191／review drive 嘅 SEED_JS）。
觸發路徑用 reviewer 嘅真玩家路徑：地圖掣直接入茶餐廳，唔 pre-click「返回地圖」
（qa191 嘅 open_loc_sheet pre-click 係 drive artifact，會令強制播喺入場前已經播咗）。
Cases（932，除 D_old 700）：
  FRESH：新遊戲→播完 C1→進度頁：鎖住插入行見到＋兩段合併＋C6F 講「行電影線」；
         地圖卡冇 .map-hint-story（C1 死 code 玩家面零殘留）。
  A_film：C1 電影線→第 15 週→首次入茶餐廳：強制播 C6F 即出（boss01 唔打尖，locTries 仲係 0）；
          播完 C6F→再入茶餐廳：boss01 即出（霞姐 modal＋wf4 seen／flags）；C3 場景行冇「電影線：」。
  B_tv：C1 電視線→第 15 週→首次入茶餐廳：強制播 C6 即出；C3 場景行冇「電視線：」。
  C_c18：C1 電視線→播種 C2–C6 done＋第 49 週（1990 冬）→首次入茶餐廳：強制播 C18 即出；
         播完→進度頁 C19 鎖行＋「先完成番外・1990 冬〈上岸路〉」＋C7 緊貼插入行之後。
  D_old (700)：A_film 留低嘅 C6F-done 真存檔寫入 slot 1→reload→讀檔→進度頁 700 闊驗。
用法：/home/hatch/pwenv49/bin/python ~/workspace/linji-work198/qa198/drive198.py
Mirror：工作副本 ~/workspace/linji-work198，port 8988，LIVE 模式。
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
REP = {"errors": [], "http_fail": [], "runs": {}}
FAILS = []


def note(name, cond, detail=""):
    print(("  PASS " if cond else "  FAIL ") + name + ((" :: " + str(detail)[:220]) if detail and not cond else ""), flush=True)
    if not cond:
        FAILS.append(name)
    return cond


def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=ROOT,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest()
    assert sha == exp, "served sha mismatch"
    print("serve ok sha", sha[:12], "bytes", len(body), flush=True)
    return p


def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass


def tap(pg, texts, wait=1000):
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


def js_tap_exact(pg, text):
    return pg.evaluate("""(t) => {
      const b = [...document.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent||'').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def modal_tap(pg, text):
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent||'').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def modal_click_any(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return null; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return null; const t = (bs[0].textContent||'').trim(); bs[0].click(); return t; }""")


def new_game(pg):
    pg.goto(URL); pg.wait_for_timeout(3000)
    tap(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    tap(pg, ["覆蓋", "確定", "確認"], 900)
    tap(pg, ["跳過教學"], 1200)
    tap(pg, ["開始寫手帳"], 1400)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
    except Exception:
        pass
    tap(pg, ["確定出發"], 1500)
    for _ in range(4):
        if not tap(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    ok = pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")
    print("NEW GAME OK:", ok, flush=True)
    return ok


def clear_enc(pg, rounds=16):
    for _ in range(rounds):
        if pg.evaluate("() => !document.getElementById('enc79-overlay')"):
            return True
        hit = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay'); if (!ov) return false;
          const sk = ov.querySelector('.e79-skip'); if (sk && sk.offsetParent !== null) { sk.click(); return true; }
          const ch = ov.querySelector('.e79-choice'); if (ch) { ch.click(); return true; }
          const nb = [...ov.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return true; } return false; }""")
        if not hit:
            return pg.evaluate("() => !document.getElementById('enc79-overlay')")
        pg.wait_for_timeout(700)
    return pg.evaluate("() => !document.getElementById('enc79-overlay')")


def on_map(pg):
    return pg.evaluate("""() => {
      const m = document.getElementById('v-map');
      return !!(m && m.offsetParent !== null && !document.getElementById('enc79-overlay')
        && !document.querySelector('.story-play .dlg106-plate')
        && !document.querySelector('.sp-head-opening')); }""")


def back_to_map(pg):
    for _ in range(8):
        if on_map(pg):
            return True
        js_tap_exact(pg, "返回地圖")
        pg.wait_for_timeout(900)
        modal_tap(pg, "返回地圖")
        pg.wait_for_timeout(600)
        clear_enc(pg)
    return on_map(pg)


SP_STATE = """() => {
  const plate = document.querySelector('.story-play .dlg106-plate');
  const choices = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
  const mi = document.getElementById('modal-inner');
  const act = document.querySelector('.sp-act191');
  const h3 = document.querySelector('.sp-head-opening h3');
  const meta = document.querySelector('.sp-head-opening .sp-meta');
  const setting = document.querySelector('.sp-setting');
  return { active: !!plate || choices.length > 0 || !!document.querySelector('.sp-head-opening'),
    choices: choices.length,
    choiceLabels: choices.map(c => (c.textContent||'').trim().slice(0, 60)),
    snippet: mi ? (mi.textContent||'').replace(/\\s+/g,' ').trim().slice(0, 200) : '',
    act191: act ? act.textContent.trim() : null,
    meta: meta ? meta.textContent.trim() : null,
    setting: setting ? setting.textContent.trim() : null,
    nodeTitle: h3 ? h3.textContent.trim() : null }; }"""


def play_story(pg, pick=None, max_steps=110):
    picked = None
    for _ in range(max_steps):
        st = pg.evaluate(SP_STATE)
        if not st["active"]:
            return picked
        if st["choices"]:
            idx = 0
            if pick:
                for i, lab in enumerate(st["choiceLabels"]):
                    if pick in lab:
                        idx = i; break
            picked = st["choiceLabels"][idx] if st["choiceLabels"] else "?"
            pg.evaluate("""(i) => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
              if (c[i]) c[i].click(); }""", idx)
            pg.wait_for_timeout(1200)
            continue
        hit = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not hit:
            return picked
        pg.wait_for_timeout(900)
    return picked


PROG_JS = """() => {
  const el = document.getElementById('progress-list');
  if (!el) return {found:false};
  const rows = [...el.querySelectorAll('.prog71-row')].map(r => {
    const act = r.querySelector('.prog71-act');
    const b = r.querySelector('b');
    const tag = r.querySelector('.prog71-tag');
    const items = [...r.querySelectorAll('.prog71-items li')].map(li => (li.textContent||'').trim());
    return { cls: r.className, act: act ? act.textContent.trim() : '',
      title: b ? b.textContent.trim() : '', tag: tag ? tag.textContent.trim() : '', items };
  });
  return {found:true, rows, raw: (el.textContent||'').replace(/\\s+/g,' ').trim()}; }"""


def open_progress(pg):
    pg.evaluate("""() => { const cs = document.getElementById('chip-story');
      if (cs) cs.click(); return !!cs; }""")
    pg.wait_for_timeout(1200)
    pg.evaluate("""() => {
      const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null && (b.textContent||'').trim() === '進度');
      if (btns[0]) btns[0].click(); return btns.length; }""")
    pg.wait_for_timeout(900)
    return pg.evaluate(PROG_JS)


def open_loc_map_button(pg, name):
    """真玩家路徑：地圖掣直接入地點，唔 pre-click「返回地圖」。"""
    ok = pg.evaluate("""(nm) => {
      const root = document.querySelector('#v-map'); if (!root) return false;
      const b = [...root.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent||'').includes(nm));
      if (!b) return false; b.click(); return true; }""", name)
    pg.wait_for_timeout(1500)
    clear_enc(pg)
    return ok


def close_loc(pg):
    hit = pg.evaluate("""() => {
      const sh = document.getElementById('loc-sheet'); if (!sh) return false;
      const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent||'').trim() === '返回地圖');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    return hit


WF4_JS = """() => {
  const st = (window.S && S.wf4) || null;
  const mi = document.getElementById('modal-inner');
  return { day: S ? S.dayIndex : null,
    wf4: st ? { lastDay: st.lastDay, locDay: st.locDay, locTries: st.locTries,
      seen: st.seen, flags: st.flags, evDay: st.evDay } : null,
    modalText: mi ? (mi.textContent||'').replace(/\\s+/g,' ').trim().slice(0, 300) : null,
    modalVisible: !!(mi && mi.offsetParent !== null) }; }"""


MAP_HINT_JS = """() => {
  const hint = document.getElementById('map-hint');
  return { hintStoryEl: !!document.querySelector('.map-hint-story'),
    hintStoryIn128: !!document.querySelector('.map-hint-story-in128'),
    hintText: hint ? (hint.textContent||'').replace(/\\s+/g,' ').trim().slice(0, 300) : null,
    chipStory: !!document.getElementById('chip-story') }; }"""


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
  return { day: S.dayIndex, week: Math.floor(S.dayIndex/7)+1, phase: S.story.phase,
    open: (oc.open||[]).map(r=>r.id), done: (oc.done||[]).map(r=>r.id) }; }"""


def play_c1_seed(pg, keyword, seed_arg):
    assert new_game(pg), "new game failed"
    clear_enc(pg)
    st = pg.evaluate(SP_STATE)
    if not st["active"]:
        open_loc_map_button(pg, "茶餐廳")
        close_loc(pg)
        st = pg.evaluate(SP_STATE)
    assert st["active"], "C1 未彈出"
    picked = play_story(pg, pick=keyword)
    print("  C1 揀咗:", picked, flush=True)
    pg.wait_for_timeout(800)
    modal_tap(pg, "關閉")
    pg.wait_for_timeout(800)
    clear_enc(pg)
    seed = pg.evaluate(SEED_JS, seed_arg)
    print("  seed:", json.dumps(seed, ensure_ascii=False), flush=True)
    return picked, seed


def no_bad_numbers(prog, tag):
    raw = prog.get("raw") or ""
    note(tag + "：進度頁冇「第 20 幕」", "第 20 幕" not in raw, raw[:160])
    note(tag + "：進度頁冇「第 18 幕」", "第 18 幕" not in raw, raw[:160])
    note(tag + "：進度頁冇「第 19 幕」", "第 19 幕" not in raw, raw[:160])


def check_c3(st, tag, route_word):
    """場景頂：路線名只出現一次（幕號行有，場景行冇）。"""
    head = ((st.get("act191") or "") + " | " + (st.get("setting") or ""))
    n = head.count(route_word)
    note(tag + f"：場景頂「{route_word}」只出現一次（幕號行，場景行已剝走）",
         n == 1, head)
    note(tag + "：場景行唔再有「" + route_word + "：」",
         (route_word + "：") not in (st.get("setting") or ""), st.get("setting"))


def run_forced_case(pg, name, keyword, seed_arg, expect_act, expect_title, expect_node,
                    route_word, expect_setting, check_boss01):
    print(f"== {name}（預期 {expect_act}：{expect_title}）==", flush=True)
    picked_c1, seed = play_c1_seed(pg, keyword, seed_arg)
    wf4_before = pg.evaluate(WF4_JS)
    print("  wf4 before trigger:", json.dumps(wf4_before, ensure_ascii=False), flush=True)
    note(name + "：播種後 WF4 仲係 pristine（locTries 0）",
         (wf4_before.get("wf4") or {}).get("locTries") == 0, json.dumps(wf4_before, ensure_ascii=False))
    # --- B1 主修：首次入茶餐廳，強制播即出 ---
    open_loc_map_button(pg, "茶餐廳")
    wf4_entry = pg.evaluate(WF4_JS)
    print("  wf4 after entry:", json.dumps(wf4_entry, ensure_ascii=False), flush=True)
    note(name + "：入茶餐廳嗰刻 boss01 冇打尖（modal 唔係霞姐）",
         "霞姐" not in (wf4_entry.get("modalText") or ""), wf4_entry.get("modalText"))
    close_loc(pg)
    st = pg.evaluate(SP_STATE)
    print("  first trigger story:", json.dumps(st, ensure_ascii=False), flush=True)
    pg.screenshot(path=os.path.join(SHOTS, f"{name}_story_open.png"))
    note(name + "：首次觸發即出目標主線幕（唔使等下一次）",
         st.get("act191") == expect_act + "：" + expect_title, json.dumps(st, ensure_ascii=False)[:300])
    note(name + "：節點標題仍係「" + expect_node + "」",
         st.get("nodeTitle") == expect_node, json.dumps(st, ensure_ascii=False)[:200])
    if expect_setting:
        note(name + "：場景行＝「" + expect_setting + "」",
             st.get("setting") == expect_setting, st.get("setting"))
    if route_word:
        check_c3(st, name, route_word)
    else:
        head = ((st.get("act191") or "") + " | " + (st.get("setting") or ""))
        note(name + "：場景頂冇「電影線／電視線」", "電影線" not in head and "電視線" not in head, head)
    picked = play_story(pg)
    print("  揀咗:", picked, flush=True)
    pg.wait_for_timeout(800)
    modal_tap(pg, "關閉")
    pg.wait_for_timeout(800)
    clear_enc(pg)
    done = pg.evaluate("() => ({ c6f: StoryOC.isDone('C6F'), c6: StoryOC.isDone('C6'), c18: StoryOC.isDone('C18'), c19: StoryOC.isDone('C19') })")
    print("  done:", json.dumps(done, ensure_ascii=False), flush=True)
    note(name + "：目標幕播完 mark done", done.get({"第 6 幕・電影線": "c6f", "第 6 幕・電視線": "c6", "番外・1990 冬": "c18"}[expect_act]) is True, json.dumps(done, ensure_ascii=False))
    back_to_map(pg)
    # --- B1 去向：boss01 之後喺邊度出 ---
    if check_boss01:
        wf4_pre2 = pg.evaluate(WF4_JS)
        open_loc_map_button(pg, "茶餐廳")
        wf4_after2 = pg.evaluate(WF4_JS)
        print("  wf4 2nd entry:", json.dumps(wf4_after2, ensure_ascii=False), flush=True)
        note(name + "：boss01 之後仲出——播完主線幕再入茶餐廳就出霞姐",
             "霞姐" in (wf4_after2.get("modalText") or ""), wf4_after2.get("modalText"))
        note(name + "：boss01 嗰次 locTries 係 1（defer 嗰次冇計數）",
             (wf4_after2.get("wf4") or {}).get("locTries") == 1, json.dumps(wf4_after2.get("wf4"), ensure_ascii=False))
        note(name + "：boss01 已見（seen／boss_met）",
             ((wf4_after2.get("wf4") or {}).get("seen") or {}).get("wf4_ev_boss01") == 1
             and ((wf4_after2.get("wf4") or {}).get("flags") or {}).get("boss_met") is True,
             json.dumps(wf4_after2.get("wf4"), ensure_ascii=False))
        btn = modal_click_any(pg)
        print("  boss01 modal 撳咗:", btn, flush=True)
        pg.wait_for_timeout(900)
        clear_enc(pg)
        back_to_map(pg)
    prog = open_progress(pg)
    pg.screenshot(path=os.path.join(SHOTS, f"{name}_progress.png"))
    rows = prog.get("rows") or []
    acts = [r["act"] for r in rows]
    print("  progress acts:", acts, flush=True)
    row = next((r for r in rows if r.get("act") == expect_act), None)
    note(name + "：進度頁有「" + expect_act + "」行", row is not None, str(acts))
    if row:
        note(name + "：嗰行標題＝「" + expect_title + "」", row.get("title") == expect_title, json.dumps(row, ensure_ascii=False))
        note(name + "：嗰行 ✓ 已完成", row.get("tag") == "✓ 已完成", json.dumps(row, ensure_ascii=False))
    no_bad_numbers(prog, name)
    REP["runs"][name] = {"c1": picked_c1, "seed": seed, "act191": st.get("act191"),
                         "setting": st.get("setting"), "picked": picked, "done": done,
                         "acts": acts, "row": row,
                         "wf4_before": wf4_before, "wf4_entry": wf4_entry}
    return rows, done


def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])

            # --- FRESH：新遊戲→播完 C1→進度頁鎖住插入行＋兩段合併；地圖卡冇 hint ---
            pg = br.new_page(viewport={"width": 932, "height": 1500})
            pg.on("pageerror", lambda e: REP["errors"].append("FRESH: " + str(e)))
            pg.on("response", lambda r: REP["http_fail"].append(f"FRESH {r.status} {r.url}") if r.status >= 400 else None)
            print("== FRESH_932（新遊戲→C1→進度頁＋地圖卡）==", flush=True)
            assert new_game(pg)
            clear_enc(pg)
            st = pg.evaluate(SP_STATE)
            if st["active"]:
                play_story(pg, pick="接電影散工賺快錢")
                pg.wait_for_timeout(800)
                modal_tap(pg, "關閉")
                pg.wait_for_timeout(800)
                clear_enc(pg)
            note("FRESH：播完 C1 後返到真地圖", back_to_map(pg), "")
            hint = pg.evaluate(MAP_HINT_JS)
            print("  map hint:", json.dumps(hint, ensure_ascii=False), flush=True)
            pg.screenshot(path=os.path.join(SHOTS, "fresh_map_932.png"))
            note("FRESH C1：地圖卡冇 .map-hint-story 元素（死 code 玩家面零殘留）",
                 hint.get("hintStoryEl") is False and hint.get("hintStoryIn128") is False, json.dumps(hint, ensure_ascii=False))
            note("FRESH C1：地圖卡仲有合併行（計劃＋出行，冇回歸）",
                 "仲可以去" in (hint.get("hintText") or ""), hint.get("hintText"))
            note("FRESH C1：頂欄進度 chip 仲喺度（進度入口）", hint.get("chipStory") is True, "")
            prog0 = open_progress(pg)
            pg.screenshot(path=os.path.join(SHOTS, "fresh_progress_932.png"))
            rows0 = prog0.get("rows") or []
            acts0 = [r["act"] for r in rows0]
            print("  fresh acts:", acts0, flush=True)
            print("  fresh rows:", json.dumps(rows0, ensure_ascii=False)[:1200], flush=True)
            no_bad_numbers(prog0, "FRESH")
            note("FRESH C2：鎖住插入行見到（C6F／C18／C19 標題＋未開放）",
                 all(a in acts0 for a in ["第 6 幕・電影線", "番外・1990 冬", "番外・1991 春"]), str(acts0))
            note("FRESH C2：插入行帶 prog71-insert 標記",
                 any("prog71-insert" in (r.get("cls") or "") for r in rows0), str([r.get("cls") for r in rows0]))
            c6f = next((r for r in rows0 if r.get("act") == "第 6 幕・電影線"), None)
            note("FRESH C2：C6F 鎖行講啱條件（行電影線，唔係行電視線）",
                 bool(c6f) and any("行電影線" in i for i in c6f.get("items", []))
                 and not any("行電視線" in i for i in c6f.get("items", [])), json.dumps(c6f, ensure_ascii=False))
            c19 = next((r for r in rows0 if r.get("act") == "番外・1991 春"), None)
            note("FRESH C2：C19 鎖行有前置句「先完成番外・1990 冬〈上岸路〉」",
                 bool(c19) and any("先完成番外・1990 冬〈上岸路〉" in i for i in c19.get("items", [])), json.dumps(c19, ensure_ascii=False))
            note("FRESH C2：遠幕按段合併兩行「第 4–6 幕」＋「第 7–17 幕」（C2／C3 係鎖住 detail，far 由 C4 起）",
                 "第 4–6 幕" in acts0 and "第 7–17 幕" in acts0 and "第 4–17 幕" not in acts0, str(acts0))
            i_ins = max([acts0.index(a) for a in ["第 6 幕・電影線", "番外・1990 冬", "番外・1991 春"] if a in acts0], default=-1)
            i_m7 = acts0.index("第 7–17 幕") if "第 7–17 幕" in acts0 else -1
            note("FRESH C2：「第 7–17 幕」合併行緊貼插入行之後", 0 <= i_ins < i_m7, str(acts0))
            REP["runs"]["FRESH"] = {"acts": acts0, "mapHint": hint}
            pg.close()

            # --- A_film / B_tv / C_c18 ---
            saved_slot_value = None
            saved_slot_key = None
            for name, kw, seed_arg, eact, etitle, enode, rword, esetting, boss in [
                ("A_film", "接電影散工賺快錢",
                 {"day": 98, "done": {"C2": True, "C3": True, "C4": True, "C5": True},
                  "lastDoneDay": 90, "fame": 26, "credit": 49, "money": 14936},
                 "第 6 幕・電影線", "片場跟班", "角落嗰張枱",
                 "電影線", "獅子山製片廠 · 1990 年 · 佈景板後面嗰個位", True),
                ("B_tv", "跟張子駿班底學動作戲",
                 {"day": 98, "done": {"C2": True, "C3": True, "C4": True, "C5": True},
                  "lastDoneDay": 90, "fame": 26, "credit": 49, "money": 14936},
                 "第 6 幕・電視線", "飯堂閒角", "角落嗰張枱",
                 "電視線", "星河電視台飯堂 · 1990 年 · 角落嗰張枱", False),
                ("C_c18", "跟張子駿班底學動作戲",
                 {"day": 336, "done": {"C2": True, "C3": True, "C4": True, "C5": True, "C6": True},
                  "lastDoneDay": 330, "fame": 60, "credit": 60, "money": 30000},
                 "番外・1990 冬", "上岸路", "上岸路",
                 None, None, False),
            ]:
                pg = br.new_page(viewport={"width": 932, "height": 1500})
                pg.on("pageerror", lambda e, n=name: REP["errors"].append(n + ": " + str(e)))
                pg.on("response", lambda r, n=name: REP["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    rows, done = run_forced_case(pg, name, kw, seed_arg, eact, etitle, enode, rword, esetting, boss)
                    if name == "A_film":
                        acts = [r["act"] for r in rows]
                        i6 = acts.index("第 6 幕・電視線") if "第 6 幕・電視線" in acts else -1
                        i6f = acts.index("第 6 幕・電影線") if "第 6 幕・電影線" in acts else -1
                        i7 = acts.index("第 7 幕") if "第 7 幕" in acts else -1
                        note("A_film：次序 C6 ＜ C6F ＜ C7", 0 <= i6 < i6f < i7, str(acts))
                        slots = pg.evaluate("""() => {
                          const out = {};
                          for (let i = 0; i < localStorage.length; i++) {
                            const k = localStorage.key(i);
                            if (k && k.indexOf('starVolunteer_map_v19w') === 0) out[k] = localStorage.getItem(k);
                          }
                          return out; }""")
                        print("  save keys:", [(k, len(v or "")) for k, v in slots.items()], flush=True)
                        for k, v in slots.items():
                            try:
                                j = json.loads(v)
                                d = (j.get("story") or {}).get("done") or j.get("done") or {}
                                if d.get("C6F"):
                                    saved_slot_value, saved_slot_key = v, k
                                    print("  C6F-done save found in:", k, flush=True)
                                    break
                            except Exception as e:
                                print("  parse fail", k, e, flush=True)
                        note("A_film：搵到 C6F done 嘅真存檔值", saved_slot_value is not None, str(list(slots.keys())))
                    if name == "C_c18":
                        acts = [r["act"] for r in rows]
                        c19 = next((r for r in rows if r.get("act") == "番外・1991 春"), None)
                        note("C_c18：播完 C18 後 C19 鎖行見到＋前置句在位",
                             bool(c19) and any("先完成番外・1990 冬〈上岸路〉" in i for i in c19.get("items", [])), json.dumps(c19, ensure_ascii=False))
                        i19 = acts.index("番外・1991 春") if "番外・1991 春" in acts else -1
                        i7 = acts.index("第 7 幕") if "第 7 幕" in acts else -1
                        note("C_c18：第 7 幕緊貼插入行之後搵得到", 0 <= i19 < i7, str(acts))
                        note("C_c18：合併行「第 9–17 幕」仲喺度（C7／C8 係 detail，far 由 C9 起）", "第 9–17 幕" in acts, str(acts))
                except Exception as e:
                    print(f"  !! {name} exception: {e}", flush=True)
                    REP["runs"][name] = {"error": str(e)}
                    FAILS.append(name + " exception: " + str(e))
                pg.close()

            # --- D_old (700)：舊存檔 slot 1 載入 ---
            print("== D_old_700（舊存檔直接寫 slot 1 載入）==", flush=True)
            pg = br.new_page(viewport={"width": 700, "height": 1500})
            pg.on("pageerror", lambda e: REP["errors"].append("D_old: " + str(e)))
            pg.on("response", lambda r: REP["http_fail"].append(f"D_old {r.status} {r.url}") if r.status >= 400 else None)
            try:
                assert saved_slot_value, "A_film 未留低 C6F-done 存檔值"
                print("  source key:", saved_slot_key, "len:", len(saved_slot_value), flush=True)
                pg.goto(URL); pg.wait_for_timeout(2500)
                pg.evaluate("""(v) => { localStorage.setItem('starVolunteer_map_v19w', v); return true; }""", saved_slot_value)
                pg.goto(URL); pg.wait_for_timeout(2500)
                note("D_old：撳到「讀檔」", js_tap_exact(pg, "讀檔"), "")
                pg.wait_for_timeout(1000)
                slot1 = pg.evaluate("""() => { const b = document.querySelector('[data-slot="1"]');
                  if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
                note("D_old：撳到槽 1", slot1, "")
                pg.wait_for_timeout(1000)
                modal_tap(pg, "讀取")
                pg.wait_for_timeout(1500)
                clear_enc(pg)
                loaded = pg.evaluate("""() => ({ hasS: !!(window.S && typeof window.S.dayIndex === 'number'),
                  day: window.S ? S.dayIndex : null, c6f: window.S ? StoryOC.isDone('C6F') : null,
                  done: window.S ? Object.keys(S.story.done||{}).filter(k => S.story.done[k]) : [] })""")
                print("  loaded:", json.dumps(loaded, ensure_ascii=False), flush=True)
                note("D_old：reload＋讀檔後 C6F 仲係 done", loaded.get("c6f") is True, json.dumps(loaded, ensure_ascii=False))
                prog = open_progress(pg)
                pg.screenshot(path=os.path.join(SHOTS, "D_old_progress.png"))
                rows = prog.get("rows") or []
                acts = [r["act"] for r in rows]
                row = next((r for r in rows if r.get("act") == "第 6 幕・電影線"), None)
                note("D_old：700 闊進度頁有「第 6 幕・電影線」行", row is not None, str(acts))
                if row:
                    note("D_old：嗰行 ✓ 已完成", row.get("tag") == "✓ 已完成", json.dumps(row, ensure_ascii=False))
                c6 = next((r for r in rows if r.get("act") == "第 6 幕・電視線"), None)
                note("D_old：C6 行喺 C6F 行之前", bool(c6 and row and acts.index(c6["act"]) < acts.index(row["act"])), str(acts))
                note("D_old：鎖住嘅 C18／C19 行 700 闊都見到",
                     "番外・1990 冬" in acts and "番外・1991 春" in acts, str(acts))
                no_bad_numbers(prog, "D_old")
                REP["runs"]["D_old"] = {"loaded": loaded, "acts": acts, "row": row}
            except Exception as e:
                print(f"  !! D_old exception: {e}", flush=True)
                REP["runs"]["D_old"] = {"error": str(e)}
                FAILS.append("D_old exception: " + str(e))
            pg.close()
            br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive198_report.json"), "w", encoding="utf-8") as f:
        json.dump(REP, f, ensure_ascii=False, indent=1)
    print("pageerrors:", len(REP["errors"]), REP["errors"][:5], flush=True)
    print("http_fail:", len(REP["http_fail"]), REP["http_fail"][:5], flush=True)
    print("DRIVE198 FAILS: " + (" | ".join(FAILS) if FAILS else "NONE — ALL PASS"), flush=True)


if __name__ == "__main__":
    main()
