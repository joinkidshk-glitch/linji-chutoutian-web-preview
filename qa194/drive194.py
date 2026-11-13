# -*- coding: utf-8 -*-
"""v20a194 實駕：頒獎禮拆 soft 閘之後，LIVE 裸 URL 端到端核實。
用法：/home/hatch/pwenv49/bin/python ~/workspace/linji-work194/qa194/drive194.py
Mirror：工作副本 ~/workspace/linji-work194，port 8994。全部裸 URL，唔准 ?softPreview=1。
播種：同調查報告一致（經 new_game 正常開局 slot 3，再以真實 gigId 播種 wrapHistory）：
  1990：廣告×2、電視×3、唱片×2、電影×2；1991：廣告×1、唱片×1。
  雙軌：1990 春 fame 26／credit 49（用戶第 15 週截圖數值），之後緩升。
A. 六窗（day 60／160／250／335／425／525）：queue() 返 1、請柬 modal → 出席 → 典禮 frame
   → 完成（flag done），每窗記 check()（ok／fails／softStatus）＋hints。
B. 朝早鏈：返地圖嗰條真路 goToMapForBrowse() 會唔會彈請柬（獨立 run，唔污染六窗）。
C. 季前提示對得上：近 miss 玩家 hints 話「仲差 N 部」→ 補返 N 部殺青 → 同窗 queue() 返 1。
D. C17：1992 冬台慶有結果 → flag done，awardResolved 條件成立（唔靠 backstop）。
E. 舊存檔：soft 模式玩過嘅 save（invited 旗標＋pendingAwardPack）載入唔 crash，請柬還原到。
結果：qa194/drive194_report.json；截圖 qa194/shots/。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work194"
HERE = "/home/hatch/workspace/linji-work194/qa194"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8994
REPORT = {"errors": [], "http_fail": [], "runs": {}}


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


def new_game(pg, url):
    pg.goto(url); pg.wait_for_timeout(3000)
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


def dismiss_modals(pg, rounds=6):
    for _ in range(rounds):
        got = click_first(pg, ["確定", "確認", "好", "知道了", "收到"], 700)
        if not got:
            return


def wait_fw(pg):
    for _ in range(30):
        try:
            r = pg.evaluate("() => { try { const c = window.__awards.check(); return c; } catch(e){ return {fails:['no-awards']}; } }")
            if r and "schema" not in (r.get("fails") or []) and "stub" not in (r.get("fails") or []):
                return r
        except Exception:
            pass
        pg.wait_for_timeout(500)
    return pg.evaluate("() => { try { return window.__awards.check(); } catch(e){ return {fails:['timeout']}; } }")


PICK_GIGS_JS = """() => {
  const out = {};
  const want = {"廣告":2, "唱片通告":2, "電影":2, "電視劇":3, "綜藝":1};
  const gigs = (window.GIGS || []);
  for (const t of Object.keys(want)) {
    out[t] = gigs.filter(g => g && g.type === t).slice(0, want[t])
      .map(g => ({id: g.id, type: g.type, title: g.title || g.id,
                  role: g.role || g.castRole || g.cast || null,
                  tier: g.tier || null}));
  }
  return out;
}"""

SEED_JS = """(args) => {
  const picks = args.picks;
  const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type,
    totalDays: 3, pay: 1000, fame: 2, popularity: 0, wrappedDay: day, rating: "順利殺青"});
  const wraps = [];
  const take = (t, days) => { (picks[t]||[]).slice(0, days.length).forEach((g,i)=> wraps.push(mk(g, days[i]))); };
  take("廣告", [30, 45]);
  take("電視劇", [20, 100]);
  take("綜藝", [300]);
  take("唱片通告", [120, 140]);
  take("電影", [200, 230]);
  S.dayIndex = args.day;
  S.fame = args.fame;
  S.industryCredit = args.credit;
  S.wrapHistory = wraps;
  S.postShootRewards = [];
  if (S.story) S.story.gigCount = wraps.length;
  S.awardsFlags = {};
  S.pendingAwardPack = null;
  if (S.awardsLog) S.awardsLog = [];
  return {wraps: wraps.length, byType: wraps.reduce((a,w)=>{a[w.type]=(a[w.type]||0)+1;return a;},{})};
}"""

ADD_WRAPS_JS = """(args) => {
  const picks = args.picks;
  const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type,
    totalDays: 3, pay: 1000, fame: 2, popularity: 0, wrappedDay: day, rating: "順利殺青"});
  const add = [];
  if (args.year === 1991) {
    (picks["廣告"]||[]).slice(0,1).forEach(g=> add.push(mk(g, 400)));
    (picks["唱片通告"]||[]).slice(0,1).forEach(g=> add.push(mk(g, 480)));
  }
  S.wrapHistory = (S.wrapHistory||[]).concat(add);
  if (S.story) S.story.gigCount = S.wrapHistory.length;
  return {added: add.length, total: S.wrapHistory.length};
}"""

PROBE_JS = """(day) => {
  S.dayIndex = day;
  let flag = null, lsFlag = null, check = null, hints = null, qErr = null, queued = null;
  try { flag = (typeof BehaviorGate !== "undefined") ? BehaviorGate.featureFlag_softBehaviorGatePreview() : "no-BehaviorGate"; } catch(e){ flag = "err:" + e.message; }
  try { lsFlag = localStorage.getItem("starVolunteer_softBehaviorGatePreview"); } catch(e){ lsFlag = "err"; }
  try { check = window.__awards.check(); } catch(e){ check = {fails: ["err:"+e.message]}; }
  try { hints = window.__awards.hints62(S, 0); } catch(e){ hints = "err:" + e.message; }
  try { queued = window.__awards.queue(); } catch(e){ qErr = String(e && e.message || e); }
  let present = null, presentErr = null;
  try { present = window.__freeplay.presentAward(); } catch(e){ presentErr = String(e && e.message || e); }
  const modal = !!document.querySelector(".awd-sheet, .awd62-frame, [class*='award-invite'], [class*='awd-invite']");
  return {
    day: day,
    softFlag: flag, lsFlag: lsFlag,
    check: check,
    hints: hints,
    queueLen: Array.isArray(queued) ? queued.length : null,
    queueErr: qErr,
    queueIds: Array.isArray(queued) ? queued.map(p => (p && (p.ceremonyId || p.id)) || "?") : null,
    queueTiers: Array.isArray(queued) ? queued.map(p => (p && (p.bestOutcome || p.tierLabel)) || "?") : null,
    present: present, presentErr: presentErr, modalVisible: modal,
    flags: Object.assign({}, S.awardsFlags || {}),
    pending: S.pendingAwardPack ? {ceremonyId: S.pendingAwardPack.ceremonyId, year: S.pendingAwardPack.year, bestOutcome: S.pendingAwardPack.bestOutcome} : null,
    fame: S.fame, credit: S.industryCredit,
    wraps: (S.wrapHistory||[]).length,
  };
}"""

WINDOWS = [
    ("1990-春 廣告賞", 60, 26, 49),
    ("1990-夏 金碟夜", 160, 30, 52),
    ("1990-秋 影藝獎", 250, 34, 55),
    ("1990-冬 台慶", 335, 38, 58),
    ("1991-春 廣告賞", 425, 45, 62),
    ("1991-夏 金碟夜", 525, 52, 66),
]


def attend_ceremony(pg, day, tag):
    """modal 已經彈出：撳出席 → 等典禮 frame → 截圖 → 跳過 → 等 frame 消失 → 記 flag。"""
    out = {"attended": False, "frame": False, "skipped": None, "flagsAfter": None}
    pg.screenshot(path=os.path.join(SHOTS, f"LIVE_invite_{day}.png"))
    clicked = click_first(pg, ["出席", "去現場", "參加"], 1500)
    out["attended"] = clicked
    print(f"    clicked attend ({tag}):", clicked, flush=True)
    frame = False
    for _ in range(10):
        pg.wait_for_timeout(500)
        frame = pg.evaluate("() => !!document.querySelector('.awd62-frame')")
        if frame:
            break
    out["frame"] = frame
    print("    ceremony frame visible:", frame, flush=True)
    if frame:
        pg.screenshot(path=os.path.join(SHOTS, f"LIVE_ceremony_{day}.png"))
        sk = click_first(pg, ["跳過", "跳過典禮"], 1000)
        out["skipped"] = sk
        for _ in range(30):
            pg.wait_for_timeout(500)
            if not pg.evaluate("() => !!document.querySelector('.awd62-frame')"):
                break
        out["frameGone"] = not pg.evaluate("() => !!document.querySelector('.awd62-frame')")
        print("    skipped:", sk, "| frame gone:", out.get("frameGone"), flush=True)
    dismiss_modals(pg)
    dismiss_encounter(pg)
    out["flagsAfter"] = pg.evaluate("() => Object.assign({}, S.awardsFlags || {})")
    out["logLen"] = pg.evaluate("() => (S.awardsLog || []).length")
    return out


def run_six_windows(pw):
    print("\n===== A: LIVE 六窗 =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"windows": [], "pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False
            REPORT["runs"]["six_windows"] = res
            ctx.close(); return res
        dismiss_encounter(pg)
        chk = wait_fw(pg)
        res["awardsCheckAtBoot"] = chk
        print("awardsCheck at boot:", json.dumps(chk, ensure_ascii=False), flush=True)
        picks = pg.evaluate(PICK_GIGS_JS)
        res["picks"] = picks
        seed = pg.evaluate(SEED_JS, {"picks": picks, "day": 60, "fame": 26, "credit": 49})
        res["seed"] = seed
        print("seed:", seed, flush=True)
        added91 = False
        for label, day, fame, credit in WINDOWS:
            if day >= 400 and not added91:
                r91 = pg.evaluate(ADD_WRAPS_JS, {"picks": picks, "year": 1991})
                print("1991 wraps added:", r91, flush=True)
                added91 = True
            pg.evaluate("(a)=>{ S.fame=a[0]; S.industryCredit=a[1]; }", [fame, credit])
            dismiss_encounter(pg)
            probe = pg.evaluate(PROBE_JS, day)
            probe["label"] = label
            res["windows"].append(probe)
            print(f"--- {label} day={day} fame={fame} credit={credit}", flush=True)
            print("    softFlag:", probe["softFlag"], "| queueLen:", probe["queueLen"],
                  "| queueIds:", probe["queueIds"], "| tiers:", probe["queueTiers"],
                  "| present:", probe["present"], "| modal:", probe["modalVisible"],
                  "| flags:", probe["flags"], "| pending:", probe["pending"], flush=True)
            print("    check:", json.dumps(probe["check"], ensure_ascii=False)[:300], flush=True)
            print("    hints:", json.dumps(probe["hints"], ensure_ascii=False)[:400], flush=True)
            if probe["modalVisible"]:
                att = attend_ceremony(pg, day, label)
                probe["attend"] = att
            else:
                pg.screenshot(path=os.path.join(SHOTS, f"LIVE_nomodal_{day}.png"))
                dismiss_modals(pg)
    finally:
        ctx.close()
    REPORT["runs"]["six_windows"] = res
    return res


def run_morning_chain(pw):
    print("\n===== B: 朝早鏈 goToMapForBrowse() =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False
            REPORT["runs"]["morning_chain"] = res
            ctx.close(); return res
        dismiss_encounter(pg)
        wait_fw(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        pg.evaluate(SEED_JS, {"picks": picks, "day": 60, "fame": 26, "credit": 49})
        dismiss_encounter(pg)
        # 真路兩步：(1) 手帳恆常出口「返回地圖」#home-back-map-tabs → 顯示地圖；
        # (2) 地圖底部「過一日」掣 #map-start-today → startTodayScheduleFromMap
        # （今日無計劃）→ goToMapForBrowse() 晨鏈 → queue＋presentPendingAward 彈請柬。
        # 註：book70ExitHome 本身唔行晨鏈（純 show 地圖），晨鏈係第二步嗰粒掣觸發。
        clicked_map = pg.evaluate("""() => {
          const b = document.getElementById('home-back-map-tabs');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false;
        }""")
        res["clickedBackToMap"] = clicked_map
        pg.wait_for_timeout(2000)
        res["onMap"] = pg.evaluate("() => { const m = document.getElementById('v-map'); return !!(m && m.offsetParent !== null); }")
        clicked = pg.evaluate("""() => {
          const b = document.getElementById('map-start-today');
          if (b && b.offsetParent !== null) { b.click(); return '#map-start-today'; }
          return null;
        }""")
        if not clicked:
            clicked = click_first(pg, ["過一日"], 1500)
        res["clickedStartToday"] = clicked
        pg.wait_for_timeout(2500)
        # #map-start-today 嗰粒係「開始今日行程」——行完今日行程出日結板；
        # 日結板「返回地圖」先至係 goToMapForBrowse 晨鏈（v189：soft 日真返地圖）。
        res["dayAfterSchedule"] = pg.evaluate("() => window.S ? S.dayIndex : null")
        clicked_end = click_first(pg, ["返回地圖"], 1500)
        res["clickedDayEndBackToMap"] = clicked_end
        pg.wait_for_timeout(2500)
        res["modalAfterChain"] = pg.evaluate("() => !!document.querySelector(\".awd-sheet, .awd62-frame, [class*='award-invite'], [class*='awd-invite']\")")
        res["modalText"] = pg.evaluate("() => { const el = document.querySelector('.awd-sheet'); return el ? el.textContent.slice(0, 200) : null; }")
        print("morning chain modal:", res["modalAfterChain"], "| clicked start-today:", res.get("clickedStartToday"), flush=True)
        print("modal text:", res["modalText"], flush=True)
        pg.screenshot(path=os.path.join(SHOTS, "LIVE_morning_chain_60.png"))
        if res["modalAfterChain"]:
            att = attend_ceremony(pg, 60, "morning-chain")
            res["attend"] = att
        res["flagsAfter"] = pg.evaluate("() => Object.assign({}, S.awardsFlags || {})")
    finally:
        ctx.close()
    REPORT["runs"]["morning_chain"] = res
    return res


def run_hints_probe(pw):
    print("\n===== C: 季前提示 vs 派柬 =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False
            REPORT["runs"]["hints"] = res
            ctx.close(); return res
        dismiss_encounter(pg)
        wait_fw(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        # 近 miss 玩家（調查報告原 seed）：fame 8／credit 10、電視×2，其他媒介 0 殺青
        pg.evaluate("""(picks) => {
          const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type,
            totalDays: 3, pay: 1000, fame: 2, popularity: 0, wrappedDay: day, rating: "順利殺青"});
          const wraps = [];
          (picks["電視劇"]||[]).slice(0,2).forEach((g,i)=> wraps.push(mk(g, 20+i*10)));
          S.wrapHistory = wraps;
          S.postShootRewards = [];
          S.awardsFlags = {}; S.pendingAwardPack = null;
          if (S.awardsLog) S.awardsLog = [];
          S.fame = 8; S.industryCredit = 10;
          window.__picks194 = picks;
        }""", picks)
        for day, season in [(60, "春"), (250, "秋")]:
            # 先問提示，唔 call queue——queue 會即刻落 invited 旗標，之後再問就唔係同一個狀態
            h = pg.evaluate("(d) => { S.dayIndex = d; try { return window.__awards.hints62(S, 0); } catch(e){ return 'err:' + e.message; } }", day)
            print(f"  day {day} ({season}) near-miss hints:", json.dumps(h, ensure_ascii=False)[:300], flush=True)
            res[f"nearmiss_{day}"] = {"hints": h}
        # 補返缺少嘅殺青 → 同窗應該派到柬（提示同派柬對得上）；每窗只 queue 一次
        r = pg.evaluate("""() => {
          const picks = window.__picks194;
          const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type,
            totalDays: 3, pay: 1000, fame: 2, popularity: 0, wrappedDay: day, rating: "順利殺青"});
          (picks["廣告"]||[]).slice(0,1).forEach(g=> S.wrapHistory.push(mk(g, 45)));
          S.fame = 26; S.industryCredit = 49;
          S.dayIndex = 60;
          let q = null, qErr = null;
          try { q = window.__awards.queue(); } catch(e){ qErr = String(e.message); }
          return {queueLen: Array.isArray(q) ? q.length : null, queueErr: qErr,
                  queueIds: Array.isArray(q) ? q.map(p => p.ceremonyId) : null,
                  hintsAfter: (() => { try { return window.__awards.hints62(S, 0); } catch(e){ return 'err'; } })()};
        }""")
        print("  after topping up ad wrap (day 60):", json.dumps(r, ensure_ascii=False)[:400], flush=True)
        res["topped_up_60"] = r
        # 秋窗同樣：補 2 部電影殺青 → 影藝獎派柬（提示話「仲差 2 部」）
        r2 = pg.evaluate("""() => {
          const picks = window.__picks194;
          const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type,
            totalDays: 3, pay: 1000, fame: 2, popularity: 0, wrappedDay: day, rating: "順利殺青"});
          S.awardsFlags = {}; S.pendingAwardPack = null;
          (picks["電影"]||[]).slice(0,2).forEach((g,i)=> S.wrapHistory.push(mk(g, 200+i*30)));
          S.fame = 34; S.industryCredit = 55;
          S.dayIndex = 250;
          let q = null, qErr = null;
          try { q = window.__awards.queue(); } catch(e){ qErr = String(e.message); }
          return {queueLen: Array.isArray(q) ? q.length : null, queueErr: qErr,
                  queueIds: Array.isArray(q) ? q.map(p => p.ceremonyId) : null,
                  tiers: Array.isArray(q) ? q.map(p => p.bestOutcome || p.tierLabel) : null};
        }""")
        print("  after topping up 2 film wraps (day 250):", json.dumps(r2, ensure_ascii=False)[:400], flush=True)
        res["topped_up_250"] = r2
    finally:
        ctx.close()
    REPORT["runs"]["hints"] = res
    return res


def run_c17_probe(pw):
    print("\n===== D: C17 awardResolved（1992 冬台慶） =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False
            REPORT["runs"]["c17"] = res
            ctx.close(); return res
        dismiss_encounter(pg)
        wait_fw(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        # 1992 年電視殺青 ×2（wrappedDay 800／900），day 1065 = 1992-12-01（第 153 週）。
        # C10 讓路：12 月係年內第 49 週，C10 未完成嗰陣台慶會延期——播種 C10 已完成，
        # 等冬台慶照常排（模擬一個行到 1992 冬、做完 C10 嘅玩家；C10 未完成者行 backstop，見 NOTES）。
        pg.evaluate("""(picks) => {
          const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type,
            totalDays: 3, pay: 1000, fame: 2, popularity: 0, wrappedDay: day, rating: "順利殺青"});
          const wraps = [];
          (picks["電視劇"]||[]).slice(0,2).forEach((g,i)=> wraps.push(mk(g, 800 + i*100)));
          S.wrapHistory = wraps;
          S.postShootRewards = [];
          S.awardsFlags = {}; S.pendingAwardPack = null;
          if (S.awardsLog) S.awardsLog = [];
          S.flags = Object.assign({}, S.flags, {C10: true, done_C10: true});
          S.fame = 60; S.industryCredit = 70;
          S.dayIndex = 1065;
          window.__picks194 = picks;
        }""", picks)
        before = pg.evaluate("""() => {
          let flags = null;
          try { flags = window.__awards.flags(); } catch(e){ flags = 'err'; }
          return {flagBefore: (flags && flags["1992/award_singho_tv"]) || "", dayIndex: S.dayIndex};
        }""")
        res["before"] = before
        print("  before:", before, flush=True)
        probe = pg.evaluate(PROBE_JS, 1065)
        res["probe"] = {k: probe[k] for k in ("queueLen", "queueIds", "queueTiers", "present", "modalVisible", "flags", "check")}
        print("  queue:", probe["queueLen"], probe["queueIds"], "| present:", probe["present"], "| modal:", probe["modalVisible"], flush=True)
        if probe["modalVisible"]:
            att = attend_ceremony(pg, 1065, "c17-tv1992")
            res["attend"] = att
        after = pg.evaluate("""() => {
          let flags = null;
          try { flags = window.__awards.flags(); } catch(e){ flags = {}; }
          const flag = (flags && flags["1992/award_singho_tv"]) || "";
          // C17 閘條件（storyLockMeta 嗰段邏輯）：done／skipped 先計
          const gate = (flag === 'done' || flag === 'skipped');
          return {flagAfter: flag, awardResolvedSatisfied: gate,
                  backstopDay: 1096, dayIndex: S.dayIndex};
        }""")
        res["after"] = after
        print("  after:", after, flush=True)
    finally:
        ctx.close()
    REPORT["runs"]["c17"] = res
    return res


def run_old_save_probe(pw):
    print("\n===== E: 舊存檔（soft 模式玩過）載入 =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False
            REPORT["runs"]["old_save"] = res
            ctx.close(); return res
        dismiss_encounter(pg)
        wait_fw(pg)
        # 扮一個 soft 模式玩過嘅 save：invited 旗標＋pendingAwardPack。
        # saveQ() 係 IIFE 私有，唔可以直接 call——照佢嘅寫法直接寫 localStorage
        #（saveKeyForSlot：slot 1 = SAVE 本身，slot n = SAVE+"_slot"+n；開局用 slot 3）。
        # 兩個槽都寫同一份，等「繼續」無論讀邊個槽都係呢份 crafted save。
        crafted = pg.evaluate("""() => {
          const pack = window.__awards.build({ceremonyId: "award_harbour_ad", year: 1990, forceTier: "gallery"});
          S.awardsFlags = {"1990/award_harbour_ad": "invited"};
          S.pendingAwardPack = pack;
          S.dayIndex = 60; S.fame = 26; S.industryCredit = 49;
          try {
            const raw = JSON.stringify(S);
            localStorage.setItem("starVolunteer_map_v19w_slot3", raw);
            localStorage.setItem("starVolunteer_map_v19w", raw);
            return {saved: true, packId: pack.ceremonyId, packYear: pack.year};
          } catch(e){ return {saved: false, err: String(e.message)}; }
        }""")
        res["crafted"] = crafted
        print("  crafted soft-mode save:", crafted, flush=True)
        pg.reload()
        pg.wait_for_timeout(3000)
        btns = pg.evaluate("""() => [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => (b.textContent || '').trim()).slice(0, 30)""")
        res["titleButtons"] = btns
        print("  title buttons:", btns, flush=True)
        clicked = click_first(pg, ["繼續", "繼續遊戲", "載入", "讀取"], 1500)
        res["clickedContinue"] = clicked
        if not clicked:
            # 冇「繼續」掣：試下撳 slot 3 載入
            clicked2 = pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
              if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
            pg.wait_for_timeout(1500)
            res["clickedSlot3"] = clicked2
            click_first(pg, ["載入", "讀檔", "確定", "確認"], 1200)
        pg.wait_for_timeout(1500)
        loaded = pg.evaluate("""() => {
          try {
            return {hasS: !!(window.S && typeof window.S.dayIndex === 'number'),
                    dayIndex: window.S ? S.dayIndex : null,
                    flags: window.S ? Object.assign({}, S.awardsFlags || {}) : null,
                    hasPendingPack: !!(window.S && S.pendingAwardPack)};
          } catch(e){ return {hasS: false, err: String(e.message)}; }
        }""")
        res["loaded"] = loaded
        print("  loaded:", loaded, flush=True)
        if loaded.get("hasS"):
            wait_fw(pg)
            pres = pg.evaluate("""() => {
              let present = null, err = null;
              try { present = window.__freeplay.presentAward(); } catch(e){ err = String(e.message); }
              const modal = !!document.querySelector(".awd-sheet, .awd62-frame, [class*='award-invite'], [class*='awd-invite']");
              return {present: present, err: err, modalVisible: modal,
                      flags: Object.assign({}, S.awardsFlags || {})};
            }""")
            res["presentAfterLoad"] = pres
            print("  present after load:", pres, flush=True)
            pg.screenshot(path=os.path.join(SHOTS, "LIVE_old_save_invite.png"))
            if pres.get("modalVisible"):
                att = attend_ceremony(pg, 60, "old-save")
                res["attend"] = att
    finally:
        ctx.close()
    REPORT["runs"]["old_save"] = res
    return res


def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            run_six_windows(pw)
            run_morning_chain(pw)
            run_hints_probe(pw)
            run_c17_probe(pw)
            run_old_save_probe(pw)
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive194_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)
    print("\nDONE. result ->", os.path.join(HERE, "drive194_report.json"), flush=True)


if __name__ == "__main__":
    main()
