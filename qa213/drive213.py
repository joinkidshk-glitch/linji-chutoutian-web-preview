# -*- coding: utf-8 -*-
"""v20a213 實駕：請柬提前 3 日＋典禮改晚上播，LIVE 端到端核實。
用法：/home/hatch/pwenv49/bin/python ~/workspace/linji-work213/qa213/drive213.py
Mirror：工作副本 ~/workspace/linji-work213，port 8913。全部裸 URL，唔准 ?softPreview=1。
播種：經 new_game 正常開局 slot 3，再以真實 gigId 播種 wrapHistory（同 qa194 配方：
  廣告×2、電視×3、綜藝×1、唱片×2、電影×2；雙軌 fame 30／credit 52）。
A. 請柬提前：金碟夜 1990，請柬日 5 月 29（day 148）彈出，寫「典禮夜：6月1日（星期五）」；
   撳出席 → 唔即播（冇 stage）、預約 attend、ceremonyDay 151。
B. 晚間出席（續 A）：典禮日 6 月 1（day 151）休息日結卡先出，之後先播典禮；
   跳過 → 結果卡「收下這晚」→ 翌日晨報（publishDay 152）→ 地圖，dayIndex 152，典禮唔耗日。
C. 推辭電視版（新局）：請柬日推辭 → 預約 decline；典禮日晚上播電視直播版；
   跳過 → 唔出結果卡，log skipped、declined 報紙 publishDay 152。
D. 撞殺青（新局）：典禮日同時係殺青日 → 殺青日結板先，之後先播典禮，兩樣唔吞。
E. 窗口前＋全鏈：day 147 present() 返 false 冇請柬；day 149 經真 UI 鏈（地圖→開始今日行程→
   日結板→返回地圖→晨鏈）彈出請柬。
F. 星期日報紙（新局，台慶 1990）：典禮 12 月 1（星期六）晚上播，報紙翌日 12 月 2
   （星期日）晨報出，唔遲到 12 月 3（pre-existing v192 C1 唔修，淨係唔惡化）。
結果：qa213/drive213_report.json；截圖 qa213/shots213/。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work213"
HERE = "/home/hatch/workspace/linji-work213/qa213"
SHOTS = os.path.join(HERE, "shots213")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8913
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


def click_modal(pg, texts, wait=1000):
    """只撳 #modal / #modal-btns 入面嘅掣（唔會誤撳地圖掣）。"""
    for t in texts:
        try:
            loc = pg.locator("#modal-btns button:has-text('" + t + "'), #modal button:has-text('" + t + "')")
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


def dismiss_modals(pg, rounds=6):
    for _ in range(rounds):
        got = click_first(pg, ["確定", "確認", "好", "知道了", "收到"], 700)
        if not got:
            return


def modal_text(pg):
    return pg.evaluate("""() => {
      const t = (document.querySelector('#modal') || {}).innerText || '';
      const btns = [...document.querySelectorAll('#modal-btns button, #modal button')].map(b => b.innerText.trim()).filter(Boolean);
      return {visible: t.trim().length > 0, text: t.slice(0, 1200), btns: btns};
    }""")


def stage_present(pg):
    return pg.evaluate("() => !!document.querySelector('.awd62-stage, .awd62-frame')")


def state(pg):
    return pg.evaluate("""() => ({
      day: S.dayIndex, date: S.dateStr,
      booked: S.awardBooked213 ? {ceremonyId: S.awardBooked213.ceremonyId, year: S.awardBooked213.year, ceremonyDay: S.awardBooked213.ceremonyDay, decision: S.awardBooked213.decision} : null,
      flags: Object.assign({}, S.awardsFlags || {}),
      log: (S.awardsLog || []).map(e => ({ceremonyId: e.ceremonyId, year: e.year, dayIndex: e.dayIndex, skipped: !!e.skipped, bestOutcome: e.bestOutcome || null})),
      papers: (S.newspaperQueue || []).map(q => ({eventKey: q.eventKey, publishDay: q.publishDay, enqueuedDay: q.enqueuedDay})),
      pending: S.pendingAwardPack ? {ceremonyId: S.pendingAwardPack.ceremonyId, year: S.pendingAwardPack.year} : null,
      clippings: (S.newspaperClippings || []).length,
      wraps: (S.wrapHistory || []).length,
      mapVisible: !!document.querySelector('#v-map:not(.hidden)') && !!(document.querySelector('#v-map') && document.querySelector('#v-map').offsetParent),
    })""")


PICK_GIGS_JS = """() => {
  const out = {};
  const want = {"廣告":2, "唱片通告":2, "電影":2, "電視劇":3, "綜藝":1};
  const gigs = (window.GIGS || []);
  for (const t of Object.keys(want)) {
    out[t] = gigs.filter(g => g && g.type === t).slice(0, want[t])
      .map(g => ({id: g.id, type: g.type, title: g.title || g.id}));
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
  S.newspaperQueue = [];
  S.stress = 0;
  S.wf4 = {lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true};
  return {wraps: wraps.length};
}"""

PRESENT_JS = """() => {
  let r = null, err = null;
  try { r = window.__freeplay.presentAward(); } catch(e){ err = String(e && e.message || e); }
  const t = (document.querySelector('#modal') || {}).innerText || '';
  return {ret: r, err: err, modalVisible: !!document.querySelector('#modal'),
    hasNightLine: t.indexOf('典禮夜：') >= 0, nightLine: (t.match(/典禮夜：[^\\n]*/) || [''])[0],
    hasInvite: t.indexOf('請柬') >= 0 || t.indexOf('頒獎') >= 0,
    textHead: t.slice(0, 300)};
}"""


def wait_for(fn, timeout_ms=15000, step=500):
    for _ in range(int(timeout_ms / step)):
        try:
            if fn():
                return True
        except Exception:
            pass
        time.sleep(step / 1000.0)
    return False


def settle_to_map(pg, timeout_s=90):
    """撳走途中一切（C1 強制劇情「下一句」／抉擇／日結板／確認），直至地圖可見或超時。
    返 (mapVisible, trace)。注意：日結板冇「返回地圖」嗰陣撳「開始今日行程」會續跑下一日，
    係預期內嘅（實駕其後會再 set dayIndex／weekPlan）。"""
    trace = []
    for _ in range(int(timeout_s * 2)):
        dismiss_encounter(pg)
        st = state(pg)
        if st["mapVisible"] and not modal_text(pg)["visible"]:
            return True, trace
        mt = modal_text(pg)
        if mt["visible"]:
            if "跳至選項" in mt["btns"]:
                c = click_modal(pg, ["跳至選項"], 500)
                trace.append("story:跳至選項"); continue
            if "下一句" in mt["btns"]:
                c = click_modal(pg, ["下一句"], 500)
                trace.append("story:下一句"); continue
            if "返回地圖" in mt["btns"]:
                c = click_modal(pg, ["返回地圖"], 800)
                trace.append("board:返回地圖:" + mt["text"][:110].replace("\n", " / ")); continue
            if "開始今日行程" in mt["btns"]:
                c = click_modal(pg, ["開始今日行程"], 800)
                trace.append("board:開始今日行程:" + mt["text"][:110].replace("\n", " / "))
                mt2 = modal_text(pg)
                if mt2["visible"] and "開始" in mt2["btns"]:
                    c2 = click_modal(pg, ["開始"], 800)
                    trace.append("confirm:開始")
                continue
            c = click_modal(pg, ["確定", "確認", "好", "知道了", "收到", "關閉"], 600)
            if c:
                trace.append("modal:" + c); continue
            # 抉擇掣：撳第一粒可見掣——但永不撳頒獎決定掣（出席／推辭／收下這晚），
            # 等測試本身觀察／決定；撞到就停低回報，唔好食咗佢。
            got = pg.evaluate("""() => {
              const ban = ["出席", "推辭", "收下這晚"];
              const btns = [...document.querySelectorAll('#modal-btns button, #modal button')].filter(b => b.offsetParent !== null && !b.disabled);
              const ok = btns.filter(b => !ban.some(x => (b.innerText || "").indexOf(x) >= 0));
              if (!ok.length) return null;
              const t = ok[0].innerText.trim(); ok[0].click(); return t;
            }""")
            if got:
                trace.append("choice:" + got); pg.wait_for_timeout(600); continue
            trace.append("modal-stuck:" + mt["text"][:80]); return False, trace
        time.sleep(0.5)
    return False, trace


def run_day_via_map(pg):
    """喺地圖撳「開始今日行程」，等日結板出現。返日結板文字。
    強制劇情（C1/C2…）會喺返地圖嗰陣自動彈出：每次撳掣前後都 settle，撳唔到就 settle 再試。"""
    trace = []
    dismiss_encounter(pg)
    for attempt in range(3):
        ok, tr = settle_to_map(pg)
        trace.extend(tr)
        if not ok:
            return {"clickedStartToday": False, "boardVisible": True, "board": modal_text(pg), "settleTrace": trace, "settleOk": False}
        pg.evaluate("() => { const b = document.querySelector('#home-back-map-tabs'); if (b) b.click(); }")
        pg.wait_for_timeout(1500)
        dismiss_encounter(pg)
        if modal_text(pg)["visible"]:
            # 返地圖觸發晨鏈 → 強制劇情彈出：播埋佢再試
            trace.append("story-after-home-tabs")
            continue
        try:
            btn = pg.locator("#map-start-today")
            if btn.count() and btn.first.is_visible():
                btn.first.click(timeout=1500)
                trace.append("clicked-start-today")
                pg.wait_for_timeout(1200)
            else:
                trace.append("no-start-today-btn")
                continue
        except Exception as e:
            trace.append("start-today-click-fail:" + str(e)[:60])
            continue
        # 等日結板出現（休息 FX／結算有少少延遲）
        if wait_for(lambda: modal_text(pg)["visible"], 15000):
            return {"clickedStartToday": True, "boardVisible": True, "board": modal_text(pg), "settleTrace": trace}
        # 撳完冇板：可能又彈劇情，settle 再試
        trace.append("no-board-after-start")
    return {"clickedStartToday": False, "boardVisible": modal_text(pg)["visible"], "board": modal_text(pg), "settleTrace": trace}


def continue_from_dayend(pg):
    """日結板撳「返回地圖」或「開始今日行程」（後者有確認就撳開始）。返 trace。
    全部撳掣限定 #modal 範圍，唔會誤撳地圖掣。"""
    trace = []
    c = click_modal(pg, ["返回地圖"], 1200)
    if c:
        trace.append("返回地圖"); return trace
    c = click_modal(pg, ["開始今日行程"], 1200)
    if c:
        trace.append("開始今日行程")
        # v20a45 確認 modal：「開始」／「取消（返去休息卡）」
        mt = modal_text(pg)
        if mt["visible"] and "開始今日行程？" in mt["text"]:
            c2 = click_modal(pg, ["開始"], 1000)
            trace.append("confirm:" + str(c2))
        return trace
    trace.append("no-continue-btn:" + str(modal_text(pg)["btns"]))
    return trace


def skip_ceremony(pg, tag):
    """等 stage 出現 → 截圖 → 撳跳過 → 等 stage 消失。返結果。"""
    out = {"stageSeen": False, "skipped": None, "stageGone": False}
    ok = wait_for(lambda: stage_present(pg), 20000)
    out["stageSeen"] = ok
    if ok:
        pg.screenshot(path=os.path.join(SHOTS, f"{tag}_stage.png"))
        out["skipped"] = click_first(pg, ["跳過", "跳過典禮"], 1000)
        out["stageGone"] = wait_for(lambda: not stage_present(pg), 20000)
    return out


def run_AB(pw):
    print("\n===== A+B: 金碟夜 1990 請柬提前＋晚間出席 =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False; REPORT["runs"]["AB"] = res; ctx.close(); return res
        dismiss_encounter(pg)
        res["settleAfterNewGame"] = settle_to_map(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        res["seed"] = pg.evaluate(SEED_JS, {"picks": picks, "day": 148, "fame": 30, "credit": 52})
        # --- A: 請柬 ---
        pr = pg.evaluate(PRESENT_JS)
        res["invite"] = pr
        print("invite present:", json.dumps(pr, ensure_ascii=False)[:400], flush=True)
        pg.screenshot(path=os.path.join(SHOTS, "A_invite_148.png"))
        clicked = click_modal(pg, ["出席"], 1200)
        res["clickedAttend"] = clicked
        pg.wait_for_timeout(3000)
        res["stageRightAfterAttend"] = stage_present(pg)
        res["settleAfterAttend"] = settle_to_map(pg)
        res["stateAfterAttend"] = state(pg)
        print("after attend:", json.dumps(res["stateAfterAttend"], ensure_ascii=False), flush=True)
        # --- B: 典禮日晚上 ---
        pg.evaluate("""() => {
          S.dayIndex = 151;
          S.weekPlan = S.weekPlan || [];
          while (S.weekPlan.length < 7) S.weekPlan.push('rest');
          S.weekPlan[4] = 'rest'; S.weekPlan[5] = 'rest';
          S.stress = 0;
        }""")
        day = run_day_via_map(pg)
        res["dayRun"] = day
        print("day run:", json.dumps(day, ensure_ascii=False)[:300], flush=True)
        pg.screenshot(path=os.path.join(SHOTS, "B_dayend_151.png"))
        res["boardSawStageBefore"] = stage_present(pg)  # 日結板嗰陣應未播典禮
        res["continueTrace"] = continue_from_dayend(pg)
        sk = skip_ceremony(pg, "B")
        res["ceremony"] = sk
        print("ceremony:", sk, flush=True)
        # 結果卡
        ok = wait_for(lambda: modal_text(pg)["visible"] and "收下這晚" in modal_text(pg)["text"], 15000)
        res["resultCard"] = ok
        pg.screenshot(path=os.path.join(SHOTS, "B_result.png"))
        res["resultCardText"] = modal_text(pg)["text"][:300]
        c = click_modal(pg, ["收下這晚"], 1200)
        res["clickedResult"] = c
        # 之後應係翌日晨報（publishDay 152）
        ok = wait_for(lambda: modal_text(pg)["visible"], 10000)
        res["paperAfterResult"] = ok
        res["paperText"] = modal_text(pg)["text"][:300] if ok else ""
        pg.screenshot(path=os.path.join(SHOTS, "B_paper_152.png"))
        click_modal(pg, ["收下這份剪報"], 1000)
        dismiss_modals(pg)
        dismiss_encounter(pg)
        res["stateFinal"] = state(pg)
        print("final:", json.dumps(res["stateFinal"], ensure_ascii=False), flush=True)
    finally:
        REPORT["runs"]["AB"] = res
        ctx.close()
    return res


def run_C(pw):
    print("\n===== C: 推辭 → 電視直播版 =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False; REPORT["runs"]["C"] = res; ctx.close(); return res
        dismiss_encounter(pg)
        res["settleAfterNewGame"] = settle_to_map(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        pg.evaluate(SEED_JS, {"picks": picks, "day": 148, "fame": 30, "credit": 52})
        pr = pg.evaluate(PRESENT_JS)
        res["invite"] = pr
        clicked = click_modal(pg, ["推辭"], 1200)
        res["clickedDecline"] = clicked
        pg.wait_for_timeout(3000)
        res["stageRightAfterDecline"] = stage_present(pg)
        res["settleAfterDecline"] = settle_to_map(pg)
        res["stateAfterDecline"] = state(pg)
        pg.evaluate("""() => {
          S.dayIndex = 151;
          S.weekPlan = S.weekPlan || [];
          while (S.weekPlan.length < 7) S.weekPlan.push('rest');
          S.weekPlan[4] = 'rest'; S.weekPlan[5] = 'rest';
          S.stress = 0;
        }""")
        day = run_day_via_map(pg)
        res["dayRun"] = day
        res["continueTrace"] = continue_from_dayend(pg)
        sk = skip_ceremony(pg, "C")
        res["ceremony"] = sk
        # 推辭版唔出結果卡
        pg.wait_for_timeout(2500)
        mt = modal_text(pg)
        res["resultCardShown"] = ("收下這晚" in mt["text"]) if mt["visible"] else False
        res["afterSkipModal"] = mt["text"][:300]
        pg.screenshot(path=os.path.join(SHOTS, "C_after_skip.png"))
        # 之後應係 declined 晨報
        ok = wait_for(lambda: modal_text(pg)["visible"], 10000)
        res["paperAfter"] = ok
        res["paperText"] = modal_text(pg)["text"][:300] if ok else ""
        pg.screenshot(path=os.path.join(SHOTS, "C_paper_152.png"))
        click_modal(pg, ["收下這份剪報"], 1000)
        dismiss_modals(pg)
        dismiss_encounter(pg)
        res["stateFinal"] = state(pg)
        print("final:", json.dumps(res["stateFinal"], ensure_ascii=False), flush=True)
    finally:
        REPORT["runs"]["C"] = res
        ctx.close()
    return res


def run_D(pw):
    print("\n===== D: 撞殺青 =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False; REPORT["runs"]["D"] = res; ctx.close(); return res
        dismiss_encounter(pg)
        res["settleAfterNewGame"] = settle_to_map(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        pg.evaluate(SEED_JS, {"picks": picks, "day": 148, "fame": 30, "credit": 52})
        pr = pg.evaluate(PRESENT_JS)
        res["invite"] = pr
        res["clickedAttend"] = click_modal(pg, ["出席"], 1200)
        pg.wait_for_timeout(2000)
        res["settleAfterAttend"] = settle_to_map(pg)
        # 播種一單電影拍攝，典禮日（151）殺青：totalDays 2，doneDays 1
        seed_shoot = pg.evaluate("""(args) => {
          const g = (args.picks["電影"] || [])[0];
          S.shoots = [{id: "sh213", gigId: g.id, title: g.title, type: "電影",
            totalDays: 2, doneDays: 1, pay: 1500, fame: 2, popularity: 0}];
          S.dayIndex = 151;
          S.weekPlan = S.weekPlan || [];
          while (S.weekPlan.length < 7) S.weekPlan.push('rest');
          S.weekPlan[4] = 'shoot:sh213'; S.weekPlan[5] = 'rest';
          S.stress = 0;
          return {gigId: g.id, title: g.title, shoots: S.shoots.length};
        }""", {"picks": picks})
        res["seedShoot"] = seed_shoot
        day = run_day_via_map(pg)
        res["dayRun"] = day
        res["wrapBoardSeen"] = ("殺青" in day["board"]["text"])
        pg.screenshot(path=os.path.join(SHOTS, "D_wrapboard_151.png"))
        res["stageBeforeWrapBoard"] = stage_present(pg)
        res["continueTrace"] = continue_from_dayend(pg)
        # 殺青獎勵 sheet 可能出現
        mt = modal_text(pg)
        if mt["visible"] and "殺青獎勵" in mt["text"]:
            res["wrapRewardSheet"] = True
            res["clickedWrapReward"] = click_modal(pg, ["收下這份反響"], 1000)
        else:
            res["wrapRewardSheet"] = False
        sk = skip_ceremony(pg, "D")
        res["ceremony"] = sk
        ok = wait_for(lambda: modal_text(pg)["visible"] and "收下這晚" in modal_text(pg)["text"], 15000)
        res["resultCard"] = ok
        res["clickedResult"] = click_modal(pg, ["收下這晚"], 1200) if ok else None
        ok = wait_for(lambda: modal_text(pg)["visible"], 10000)
        res["paperAfterResult"] = ok
        res["paperText"] = modal_text(pg)["text"][:300] if ok else ""
        click_modal(pg, ["收下這份剪報"], 1000)
        dismiss_modals(pg)
        dismiss_encounter(pg)
        res["stateFinal"] = state(pg)
        print("final:", json.dumps(res["stateFinal"], ensure_ascii=False), flush=True)
    finally:
        REPORT["runs"]["D"] = res
        ctx.close()
    return res


def run_E(pw):
    print("\n===== E: 窗口前＋全鏈請柬 =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False; REPORT["runs"]["E"] = res; ctx.close(); return res
        dismiss_encounter(pg)
        res["settleAfterNewGame"] = settle_to_map(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        pg.evaluate(SEED_JS, {"picks": picks, "day": 147, "fame": 30, "credit": 52})
        pr = pg.evaluate(PRESENT_JS)
        res["beforeWindow"] = pr
        print("day147 present:", json.dumps(pr, ensure_ascii=False)[:300], flush=True)
        # 全鏈：day 149 經真 UI 鏈彈請柬
        pg.evaluate("() => { S.dayIndex = 149; S.weekPlan = S.weekPlan || []; while (S.weekPlan.length < 7) S.weekPlan.push('rest'); S.weekPlan[2] = 'rest'; S.stress = 0; }")
        day = run_day_via_map(pg)
        res["dayRun"] = day
        res["continueTrace"] = continue_from_dayend(pg)
        # 晨鏈應彈請柬
        ok = wait_for(lambda: modal_text(pg)["visible"] and ("請柬" in modal_text(pg)["text"] or "典禮夜" in modal_text(pg)["text"]), 15000)
        res["inviteViaChain"] = ok
        res["chainModal"] = modal_text(pg)["text"][:400] if ok else modal_text(pg)["text"][:200]
        pg.screenshot(path=os.path.join(SHOTS, "E_invite_chain_149.png"))
        if ok:
            res["clickedAttend"] = click_modal(pg, ["出席"], 1200)
            pg.wait_for_timeout(2000)
            res["stageRightAfterAttend"] = stage_present(pg)
            res["stateAfterAttend"] = state(pg)
        dismiss_modals(pg)
        dismiss_encounter(pg)
    finally:
        REPORT["runs"]["E"] = res
        ctx.close()
    return res


def run_F(pw):
    print("\n===== F: 星期日報紙（台慶 1990） =====", flush=True)
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 932, "height": 700})
    errs = []
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
    res = {"pageerrors": errs}
    try:
        if not new_game(pg, f"http://127.0.0.1:{PORT}/index.html"):
            res["new_game"] = False; REPORT["runs"]["F"] = res; ctx.close(); return res
        dismiss_encounter(pg)
        res["settleAfterNewGame"] = settle_to_map(pg)
        picks = pg.evaluate(PICK_GIGS_JS)
        pg.evaluate(SEED_JS, {"picks": picks, "day": 331, "fame": 30, "credit": 52})
        pr = pg.evaluate(PRESENT_JS)
        res["invite"] = pr
        print("invite 331:", json.dumps(pr, ensure_ascii=False)[:300], flush=True)
        res["clickedAttend"] = click_modal(pg, ["出席"], 1200)
        pg.wait_for_timeout(2000)
        res["settleAfterAttend"] = settle_to_map(pg)
        res["stateAfterAttend"] = state(pg)
        pg.evaluate("""() => {
          S.dayIndex = 334;  // 1990-12-01 星期六（334%7=5），翌日 335 星期日（%7=6）
          S.weekPlan = S.weekPlan || [];
          while (S.weekPlan.length < 7) S.weekPlan.push('rest');
          S.weekPlan[5] = 'rest'; S.weekPlan[6] = 'rest';
          S.stress = 0;
        }""")
        day = run_day_via_map(pg)
        res["dayRun"] = day
        res["continueTrace"] = continue_from_dayend(pg)
        sk = skip_ceremony(pg, "F")
        res["ceremony"] = sk
        ok = wait_for(lambda: modal_text(pg)["visible"] and "收下這晚" in modal_text(pg)["text"], 15000)
        res["resultCard"] = ok
        res["clickedResult"] = click_modal(pg, ["收下這晚"], 1200) if ok else None
        # 翌日 12 月 2（星期日）晨報應即刻出
        ok = wait_for(lambda: modal_text(pg)["visible"], 10000)
        res["paperDay335"] = ok
        res["paperText335"] = modal_text(pg)["text"][:300] if ok else ""
        pg.screenshot(path=os.path.join(SHOTS, "F_paper_sunday.png"))
        click_modal(pg, ["收下這份剪報"], 1000)
        dismiss_modals(pg)
        dismiss_encounter(pg)
        st = state(pg)
        res["stateAfterPaper"] = st
        print("after paper:", json.dumps(st, ensure_ascii=False), flush=True)
        # 再跑一日（12 月 2 休息 → 12 月 3 晨鏈），確認獎報唔再重出
        pg.evaluate("() => { S.weekPlan[0] = 'rest'; S.stress = 0; }")
        day2 = run_day_via_map(pg)
        res["dayRun2"] = day2
        res["continueTrace2"] = continue_from_dayend(pg)
        pg.wait_for_timeout(3000)
        mt = modal_text(pg)
        res["day336Modal"] = mt["text"][:300] if mt["visible"] else ""
        res["awardPaperAgainDay336"] = ("台慶" in mt["text"] or "頒獎" in mt["text"]) if mt["visible"] else False
        dismiss_modals(pg)
        dismiss_encounter(pg)
        res["stateFinal"] = state(pg)
    finally:
        REPORT["runs"]["F"] = res
        ctx.close()
    return res


def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            run_AB(pw)
            run_C(pw)
            run_D(pw)
            run_E(pw)
            run_F(pw)
    finally:
        stop(srv)
        with open(os.path.join(HERE, "drive213_report.json"), "w", encoding="utf-8") as f:
            json.dump(REPORT, f, ensure_ascii=False, indent=2)
        print("REPORT WRITTEN")


if __name__ == "__main__":
    main()
