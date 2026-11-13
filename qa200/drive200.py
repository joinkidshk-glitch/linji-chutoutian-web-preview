# -*- coding: utf-8 -*-
"""v20a200 實駕：修 v194 設計 review C1＋C2（＋v192 殘留 nominee 行＋贏獎報紙 live 重驗）。
對象：~/workspace/linji-work200 index.html（工作副本，唯讀 serve，port 20090）。
全部 LIVE 裸 URL，唔准 ?softPreview=1。Playwright venv /home/hatch/pwenv49/bin/python。
helper 照抄獨立 review drive_review192.py（唔係工人舊 drive 嘅覆跑邏輯，但 reuse
佢嘅播種／modal／舞台／晨報函數；new_game／serve 自備，指去本地 PORT 20090）。
Cases（13）：
- c1_ad_gap_932／700：live queue 路徑——上一年 2 部廣告臨記（wrappedDay 1990-09-15），
  1991 春季廣告賞；季前提示＋邀請函 gap 句都要有「今年」，兩邊一致。
- c2_film_gal_932／700：同年 2 部電影臨記位（SEED3），gallery 請柬 rep 行改「入場觀禮」，
  成張請柬零「爭獎」，海報＋同屆提名照留。
- c2_nom_932：對照——電影 nominee 請柬行「你爭嘅獎項」＋rep 行照舊「爭獎」。
- b1_* ×8：贏獎報紙 live 重驗——force won pack → 出席 → 舞台 → 結果卡 → queue
  templateId 對準＋headline／dek 逐字（v192 NP_EXPECT）＋禁字 → 翌朝晨報真實出街
  （廣告 case 播種日係週日，v192 C1 已知遲一日，記 delay_days，兩日內出到即 PASS）。
結果：qa200/drive200.json；截圖 qa200/shots200/。
用法：/home/hatch/pwenv49/bin/python qa200/drive200.py [case ...]
"""
import hashlib, json, os, re, subprocess, sys, time, urllib.request
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v192")
from drive_review192 import (day_idx, parse_ads, parse_gig36, SEED_JS, SEED2_JS,
                             click_btn, click_exact, modal_info, stage_state,
                             watch_stage, result_dom, force_pack, invite_line,
                             newspaper_queue, banned_hits, NP_EXPECT,
                             NP_NOM_HEADLINE, CER_NAME, SLATE, journal_awards, map_check)
from playwright.sync_api import sync_playwright

ROOT = os.environ.get("LINJI200_ROOT", "/home/hatch/workspace/linji-work200")
OUT = "/home/hatch/workspace/linji-work200/qa200"
SHOTS = os.path.join(OUT, "shots200")
PORT = 20090
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
os.makedirs(SHOTS, exist_ok=True)

BANNED = ["三句對白", "茶餐廳食面", "臨記生涯", "不殺之恩", "一句收工了", "綠葉",
          "和音", "合唱單曲", "涼茶", "跌低眼鏡", "特別獎", "臨記組", "最受歡迎"]
GATE_FILM_TV = "嗰年未做過主角／配角級作品，入圍唔到演員獎"
C1_GAP = "今年仲差 1 部廣告作品先夠入圍（而家 0/1）"
C1_HINT = "今季就係「維港街招・年度廣告賞」：今年仲差 1 部廣告作品先夠入圍——呢排接廣告通告要留神。"


def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    assert hashlib.sha256(body).hexdigest() == hashlib.sha256(
        open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest(), "served sha mismatch"
    print("serve ok sha", hashlib.sha256(body).hexdigest()[:12], flush=True)
    return p


def stop(p):
    try:
        p.send_signal(subprocess.signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass


def snap(pg, name):
    try: pg.screenshot(path=os.path.join(SHOTS, name)); return True
    except Exception: return False


def new_game(pg):
    pg.goto(f"http://127.0.0.1:{PORT}/index.html")
    pg.wait_for_timeout(3000)
    click_btn(pg, "新遊戲", 1500); pg.wait_for_timeout(600)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) b.click(); }""")
    pg.wait_for_timeout(1000)
    for t in ["覆蓋", "確定", "確認"]:
        click_btn(pg, t, 700)
    click_btn(pg, "跳過教學", 1200)
    click_btn(pg, "開始寫手帳", 1200)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1000)
    except Exception: pass
    click_btn(pg, "確定出發", 1200)
    for _ in range(4):
        if not click_btn(pg, "確定", 700) and not click_btn(pg, "確認", 700) \
           and not click_btn(pg, "好", 700) and not click_btn(pg, "知道了", 700):
            break
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")


# C1 播種：上一年 2 部廣告臨記位（wrappedDay 1990-09-15＝day 257），
# 1991 春季廣告賞窗 day 425；fame／credit 照 v194 §4 近 miss 玩家（8／10）。
SEED_C1_JS = """(o) => {
  const picks = o.picks["廣告"] || [];
  const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type, workTitle: g.workTitle,
    roleLabel: g.roleLabel, roleScale: g.roleScale, year: 1990, totalDays: 2,
    pay: 1000, fame: 0, popularity: 0, wrappedDay: day, rating: '順利殺青'});
  const wraps = picks.slice(0, 2).map(g => mk(g, o.wrapDay));
  S.dayIndex = o.dayIndex;
  S.story = S.story || {}; S.story.done = {}; S.story.flags = S.story.flags || {}; S.story.rel = S.story.rel || {};
  S.awardsFlags = {}; S.pendingAwardPack = null;
  S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
  S.fame = o.fame; S.industryCredit = o.credit; S.stage = 10; S.acting = 10;
  S.money = 5000; S.stress = 0; S.flags = S.flags || {};
  S.wrapHistory = wraps; S.newspaperQueue = []; S.news = S.news || [];
  S.story.gigCount = wraps.length;
  return { day: S.dayIndex, wraps: wraps.length };
}"""

# C2 播種：同年 2 部電影臨記位（照抄 qa192 SEED3_JS）。
SEED3_JS = """(o) => {
  const mk = (g) => ({ gigId: g.id, title: g.title, type: g.type, workTitle: g.workTitle,
    roleLabel: g.roleLabel, roleScale: g.roleScale, year: o.year, totalDays: 2,
    pay: g.pay, fame: 0, popularity: 0, wrappedDay: o.wrapDay, rating: '順利殺青' });
  const wraps = [
    mk({ id:'gig_exodus_film_hand', title:'《江邊小鎮》動作組熟手（急聘）', type:'電影',
         workTitle:'江邊小鎮', roleLabel:'動作組熟手臨記', roleScale:'film_action_extra', pay:2900 }),
    mk({ id:'gig_br89_stunt_ngai', title:'情報通告：《鐵血柔情》替身缺位', type:'電影',
         workTitle:'鐵血柔情', roleLabel:'情報通告・替身位', roleScale:'film_stunt', pay:1000 })
  ];
  S.dayIndex = o.dayIndex;
  S.story = S.story || {}; S.story.done = {}; S.story.flags = S.story.flags || {}; S.story.rel = S.story.rel || {};
  S.awardsFlags = {}; S.pendingAwardPack = null;
  S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
  S.fame = 45; S.stage = 60; S.acting = 60; S.industryCreditDelta = 50;
  S.money = 5000; S.stress = 0; S.flags = S.flags || {};
  S.wrapHistory = wraps; S.newspaperQueue = []; S.news = S.news || [];
  S.story.gigCount = wraps.length;
  return { day: S.dayIndex, wraps: wraps.length };
}"""

LIVE_PROBE_JS = """() => {
  let hints = null, hintsErr = null, queued = null, qErr = null, present = null, presentErr = null;
  try { hints = window.__awards.hints62(S, 0); } catch(e){ hintsErr = String(e && e.message || e); }
  try { queued = window.__awards.queue(); } catch(e){ qErr = String(e && e.message || e); }
  try { present = window.__freeplay.presentAward(); } catch(e){ presentErr = String(e && e.message || e); }
  const modal = !!document.querySelector(".awd-sheet");
  return { hints: hints, hintsErr: hintsErr,
    queueLen: Array.isArray(queued) ? queued.length : null, queueErr: qErr,
    queueIds: Array.isArray(queued) ? queued.map(p => (p && (p.ceremonyId || p.id)) || "?") : null,
    queueTiers: Array.isArray(queued) ? queued.map(p => (p && p.tier) || "?") : null,
    present: present, presentErr: presentErr, modalVisible: modal,
    flags: Object.assign({}, S.awardsFlags || {}),
    pending: S.pendingAwardPack ? {ceremonyId: S.pendingAwardPack.ceremonyId, year: S.pendingAwardPack.year} : null };
}"""

# name, ceremony, year, H, fame, credit, roles, payOverride, rand, mode
# mode: c1_live | c2_gal | c2_nom | won
CASES = [
    ("c1_ad_gap_932", "award_harbour_ad", 1991, 932, 8, 10, None, None, 0.4, "c1_live"),
    ("c1_ad_gap_700", "award_harbour_ad", 1991, 700, 8, 10, None, None, 0.4, "c1_live"),
    ("c2_film_gal_932", "award_harbour_film", 1990, 932, 45, 50, None, None, 0.4, "c2_gal"),
    ("c2_film_gal_700", "award_harbour_film", 1990, 700, 45, 50, None, None, 0.4, "c2_gal"),
    ("c2_nom_932", "award_harbour_film", 1990, 932, 45, 50,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2}, None, 0.4, "c2_nom"),
    ("b1_film_01_932", "award_harbour_film", 1990, 932, 45, 50,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2}, None, 0.4, "won"),
    ("b1_film_02_932", "award_harbour_film", 1990, 932, 45, 50,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2}, None, 0.7, "won"),
    ("b1_tv_01_932", "award_singho_tv", 1990, 932, 45, 50,
     {"tv_lead": 2, "tv_sup": 1, "film_lead": 2}, None, 0.4, "won"),
    ("b1_tv_02_932", "award_singho_tv", 1990, 932, 45, 50,
     {"tv_lead": 2, "tv_sup": 1, "film_lead": 2}, None, 0.7, "won"),
    ("b1_music_01_932", "award_golddisc_music", 1990, 932, 45, 50,
     {"rec": 4, "film_lead": 2}, None, 0.4, "won"),
    ("b1_music_02_700", "award_golddisc_music", 1990, 700, 45, 50,
     {"rec": 4, "film_lead": 2}, None, 0.7, "won"),
    ("b1_ad_01_932", "award_harbour_ad", 1991, 932, 45, 50,
     {"ad_lead": 2, "ad_sup": 1, "film_lead": 2}, 25000, 0.4, "won"),
    ("b1_ad_02_932", "award_harbour_ad", 1991, 932, 45, 50,
     {"ad_lead": 2, "ad_sup": 1, "film_lead": 2}, 25000, 0.7, "won"),
]


def morning_paper(pg, name, want_h, out, c):
    """翌日晨報（真實呈現）：返回地圖 → 選單 → 過一日 → 確定過一日 →
    小休日結 →（週日：回家結算）→ 晨報 modal 應見 win headline。
    典禮日係週日嗰陣要多一日先出（v192 C1 已知，唔係 fail），最多試兩日。"""
    paper = {"shown": False}
    found_day = None
    all_steps = []
    try:
        for attempt in (1, 2):
            click_btn(pg, "返回地圖", 700)
            pg.wait_for_timeout(800)
            if attempt == 1:
                for _round in range(3):
                    for _ in range(40):
                        if click_btn(pg, "下一句", 500):
                            continue
                        break
                    pg.wait_for_timeout(1200)
                    if not pg.evaluate("""() => [...document.querySelectorAll('button')].some(b => {
                      const r = b.getBoundingClientRect();
                      return r.width > 0 && (b.textContent||'').trim() === '下一句'; })"""):
                        break
            menu_opened = False
            try:
                pg.locator("#btn-menu").click(timeout=3000); menu_opened = True
            except Exception:
                pg.evaluate("() => { const b = document.querySelector('#btn-menu'); if (b) b.click(); }")
                menu_opened = pg.evaluate("() => { const m = document.querySelector('#menu'); return !!(m && m.getBoundingClientRect().width > 0); }")
            pg.wait_for_timeout(800)
            c["morning_menu_opened"] = bool(menu_opened)
            if not click_btn(pg, "過一日", 1200):
                c["morning_nextday_clicked"] = False
                break
            pg.wait_for_timeout(600)
            c["morning_nextday_clicked"] = click_btn(pg, "確定過一日", 1200)
            pg.wait_for_timeout(3000)
            steps = []
            for _step in range(6):
                m = modal_info(pg)
                if not m.get("visible"):
                    break
                h3 = m.get("h3") or ""; btns = m.get("btns") or []
                steps.append({"h3": h3, "btns": btns})
                body = m.get("body") or ""
                if want_h and want_h in body:
                    break
                if "收下這份剪報" in btns:
                    break
                if "出席" in btns and "推辭" in btns:
                    # 另一場典禮嘅請柬擋路（返地圖嗰陣 presentPendingAward 彈出）：
                    # 推辭，等典禮播完再繼續搵晨報（唔係 game bug，係 drive 要識行呢條路）。
                    click_btn(pg, "推辭", 1200)
                    pg.wait_for_timeout(500)
                    w = watch_stage(pg, 30)
                    steps.append({"h3": "declined-invite-stage", "boards": w.get("boards")})
                    pg.wait_for_timeout(600)
                    for _ in range(3):
                        mm = modal_info(pg)
                        if not mm.get("visible"):
                            break
                        b2 = mm.get("btns") or []
                        if "知道了" in b2:
                            click_btn(pg, "知道了", 900)
                        elif "確定" in b2:
                            click_btn(pg, "確定", 900)
                        elif "返回地圖" in b2:
                            click_btn(pg, "返回地圖", 1200)
                        else:
                            break
                        pg.wait_for_timeout(1200)
                    pg.wait_for_timeout(1000)
                    continue
                if "小休" in h3 and "返回地圖" in btns:
                    click_btn(pg, "返回地圖", 1200)
                elif "小休" in h3 and "回家結算" in btns:
                    click_btn(pg, "回家結算", 1200)
                elif "知道了" in btns:
                    click_btn(pg, "知道了", 900)
                elif "確定" in btns:
                    click_btn(pg, "確定", 900)
                elif "返回地圖" in btns:
                    click_btn(pg, "返回地圖", 1200)
                else:
                    break
                pg.wait_for_timeout(2000)
            all_steps.append({"day": attempt, "steps": steps})
            m = modal_info(pg)
            paper = {"shown": bool(m.get("visible")), "h3": m.get("h3") or "",
                     "btns": m.get("btns") or [], "body_head": (m.get("body") or "")[:800],
                     "overflow": m.get("overflow")}
            if want_h and want_h in (m.get("body") or ""):
                found_day = attempt
                break
            click_btn(pg, "收下這份剪報", 900) or click_btn(pg, "知道了", 900) or click_btn(pg, "確定", 900)
            pg.wait_for_timeout(800)
        out["morning_steps"] = all_steps
        out["morning_paper"] = paper
        out["morning_paper_delay_days"] = found_day
        snap(pg, f"{name}_paper.png")
        if want_h:
            c["morning_paper_shows_headline"] = found_day is not None
            if paper.get("overflow"):
                ov = paper["overflow"]
                c["morning_paper_no_overflow"] = ov.get("bodyScrollH", 0) <= ov.get("bodyClientH", 0) + 1
        click_btn(pg, "收下這份剪報", 900) or click_btn(pg, "知道了", 900) or click_btn(pg, "確定", 900)
        pg.wait_for_timeout(800)
    except Exception as e:
        out["morning_paper_error"] = repr(e)
        c["morning_paper_step_ok"] = False


def run_case(pw, cfg, ads, extra, results):
    name, cer, year, H, fame, credit, roles, payov, rnd, mode = cfg
    print(f"== {name} ({cer} {year} rand={rnd} mode={mode}) ==", flush=True)
    out = {"case": name, "ceremony": cer, "year": year, "mode": mode, "rand": rnd, "checks": {}}
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            c = out["checks"]
            if not new_game(pg):
                c["new_game"] = False; out["verdict"] = "ERROR"; results[name] = out; return
            c["new_game"] = True
            if mode == "c1_live":
                picks = pg.evaluate("""() => {
                  const out = {};
                  const gigs = (window.GIGS || []);
                  out["廣告"] = gigs.filter(g => g && g.type === "廣告").slice(0, 2)
                    .map(g => ({id: g.id, type: g.type, title: g.title || g.id,
                      roleLabel: g.roleLabel || null, roleScale: g.roleScale || null,
                      workTitle: g.workTitle || g.title || g.id}));
                  return out; }""")
                sd = pg.evaluate(SEED_C1_JS, {"dayIndex": 425, "wrapDay": day_idx(1990, 9, 15),
                                               "fame": fame, "credit": credit, "picks": picks})
                out["seed"] = sd
                c["seed_2_ad_prev_year"] = sd.get("wraps") == 2
                probe = pg.evaluate(LIVE_PROBE_JS)
                out["probe"] = probe
                c["hint_has_this_year"] = C1_HINT in (probe.get("hints") or "")
                c["live_queue_1_gallery"] = probe.get("queueLen") == 1 and probe.get("queueTiers") == ["gallery"]
                c["invite_presented_live"] = bool(probe.get("present"))
                pg.wait_for_timeout(1000)
                inv = modal_info(pg)
                out["invite"] = inv
                body = inv.get("body") or ""
                c["invite_shown"] = bool(inv.get("visible"))
                c["invite_gap_has_this_year"] = C1_GAP in body
                c["invite_gap_no_old_wording"] = "觀禮。仲差 1 部" not in body
                c["invite_no_contest_wording"] = "爭獎" not in body
                ov = inv.get("overflow") or {}
                c["invite_no_overflow"] = ov.get("bodyScrollH", 0) <= ov.get("bodyClientH", 0) + 1
                out["invite_overflow"] = ov
                snap(pg, f"{name}_invite.png")
            elif mode in ("c2_gal", "c2_nom"):
                if mode == "c2_gal":
                    sd = pg.evaluate(SEED3_JS, {"dayIndex": day_idx(year, 10, 20),
                                                 "wrapDay": day_idx(year, 9, 15), "year": year})
                    c["seed_roles_found"] = sd.get("wraps") == 2
                else:
                    sd = pg.evaluate(SEED_JS, {"dayIndex": day_idx(year, 10, 20),
                                                "wrapDay": day_idx(year, 9, 15), "year": year,
                                                "fame": fame, "credit": credit, "roles": roles,
                                                "ads": ads, "payOverride": payov})
                    c["seed_roles_found"] = all(len(sd["picked"].get(k, [])) == n for k, n in roles.items())
                out["seed"] = sd
                pg.evaluate("(v) => { Math.random = () => v; return true; }", rnd)
                pack = force_pack(pg, cer)
                out["pack"] = pack
                c["pack_built"] = "error" not in pack
                if "error" in pack:
                    out["verdict"] = "ERROR"; results[name] = out; print("  ERROR pack", pack, flush=True); return
                pg.evaluate("() => { try { window.__awards.present(); } catch(e){} }")
                pg.wait_for_timeout(1000)
                inv = modal_info(pg)
                out["invite"] = inv
                body = inv.get("body") or ""
                c["invite_shown"] = bool(inv.get("visible"))
                ov = inv.get("overflow") or {}
                c["invite_no_overflow"] = ov.get("bodyScrollH", 0) <= ov.get("bodyClientH", 0) + 1
                out["invite_overflow"] = ov
                snap(pg, f"{name}_invite.png")
                if mode == "c2_gal":
                    c["c2_rep_says_observe"] = "你今年憑《江邊小鎮》入場觀禮。" in body
                    c["c2_invite_zero_contest"] = "爭獎" not in body
                    c["c2_gate_role_line"] = GATE_FILM_TV in body
                    c["c2_full_slate"] = invite_line(body) == SLATE[cer]
                    c["c2_gallery_seat"] = "旁聽席" in body
                else:
                    c["c2_nom_label_contested"] = "你爭嘅獎項：最佳男主角、最佳男配角" in body
                    c["c2_nom_no_tonight_label"] = "今晚獎項" not in body
                    c["c2_nom_rep_still_contests"] = "你今年憑《新春大吉》爭獎。" in body
                    c["c2_nom_seat"] = "入圍／提名" in body
            else:  # won
                sd = pg.evaluate(SEED_JS, {"dayIndex": day_idx(year, 10, 20),
                                            "wrapDay": day_idx(year, 9, 15), "year": year,
                                            "fame": fame, "credit": credit, "roles": roles,
                                            "ads": ads, "payOverride": payov})
                c["seed_roles_found"] = all(len(sd["picked"].get(k, [])) == n for k, n in roles.items())
                out["seed"] = sd
                pg.evaluate("(v) => { Math.random = () => v; return true; }", rnd)
                pack = force_pack(pg, cer)
                out["pack"] = pack
                c["pack_built"] = "error" not in pack
                if "error" in pack:
                    out["verdict"] = "ERROR"; results[name] = out; print("  ERROR pack", pack, flush=True); return
                pg.evaluate("() => { try { window.__awards.present(); } catch(e){} }")
                pg.wait_for_timeout(1000)
                inv = modal_info(pg)
                out["invite"] = inv
                body = inv.get("body") or ""
                c["invite_shown"] = bool(inv.get("visible"))
                ov = inv.get("overflow") or {}
                c["invite_no_overflow"] = ov.get("bodyScrollH", 0) <= ov.get("bodyClientH", 0) + 1
                snap(pg, f"{name}_invite.png")
                if not click_btn(pg, "出席", 900):
                    c["attend_clicked"] = False; out["verdict"] = "FAIL"; results[name] = out; return
                c["attend_clicked"] = True
                pg.wait_for_timeout(400)
                c["stage_appears"] = bool(stage_state(pg).get("present"))
                w = watch_stage(pg, 26)
                out["watch"] = w
                c["stage_gone_after"] = bool(w.get("gone"))
                pg.wait_for_timeout(600)
                res = modal_info(pg)
                out["result_modal"] = {k: v for k, v in res.items() if k != "overflow"}
                c["result_shown"] = bool(res.get("visible"))
                snap(pg, f"{name}_result.png")
                click_btn(pg, "收下這晚", 900)
                pg.wait_for_timeout(900)
                nq = newspaper_queue(pg)
                out["newspaper"] = nq
                aw = [n for n in nq if n.get("templateId", "").startswith("np_win_")]
                out["newspaper_win_items"] = aw
                c["newspaper_has_win"] = len(aw) >= 1
                if aw:
                    item = aw[0]
                    exp = NP_EXPECT.get(item.get("templateId") or "")
                    out["newspaper_template"] = item.get("templateId")
                    if exp:
                        c["b1_headline_verbatim"] = item.get("headline") == exp[0]
                        c["b1_dek_verbatim"] = item.get("dek") == exp[1]
                    else:
                        c["b1_headline_verbatim"] = False
                        c["b1_dek_verbatim"] = False
                    c["b1_no_banned"] = not any(x in (item.get("headline") or "") or x in (item.get("dek") or "") for x in BANNED)
                    if item.get("templateId") == "np_win_music_01":
                        c["b1_music01_no_newcomer_word"] = "新人" not in (item.get("headline") or "") and "新人" not in (item.get("dek") or "")
                else:
                    c["b1_headline_verbatim"] = False
                    c["b1_dek_verbatim"] = False
                    c["b1_no_banned"] = False
                want_h = aw[0].get("headline") if aw else None
                out["morning_paper_want"] = want_h
                morning_paper(pg, name, want_h, out, c)
                jn = journal_awards(pg)
                out["journal"] = jn
                jtxt = jn.get("text") or ""
                c["journal_shown"] = bool(jn.get("present")) and not jn.get("error")
                c["journal_has_ceremony"] = CER_NAME[cer] in jtxt
                c["journal_has_badge"] = ("得獎" in jtxt) or ("入圍" in jtxt) or ("觀禮" in jtxt)
                snap(pg, f"{name}_journal.png")
                click_btn(pg, "關閉", 700) or click_btn(pg, "返回", 700) or click_btn(pg, "地圖", 700)
                pg.wait_for_timeout(900)
                mc = map_check(pg)
                out["map_check"] = mc
                c["map_no_h_overflow"] = not mc.get("hOverflow")
                snap(pg, f"{name}_map.png")
            out["pageerrors"] = errs[:8]
            c["zero_pageerror"] = len(errs) == 0
            out["verdict"] = "PASS" if all(c.values()) else "FAIL"
            results[name] = out
            print(f"  {out['verdict']} fail={json.dumps({k:v for k,v in c.items() if not v}, ensure_ascii=False)}", flush=True)
            if errs: print(f"    pageerrors: {errs[:3]}", flush=True)
        except Exception as e:
            out["error"] = repr(e); out["verdict"] = "ERROR"; out["pageerrors"] = errs[:8]
            results[name] = out; print(f"  ERROR {e!r}", flush=True)
            try: snap(pg, f"err_{name}.png")
            except Exception: pass
        finally:
            ctx.close()
    finally:
        b.close()


def main():
    srv = serve()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
            src = r.read().decode("utf-8", "replace")
        ads = parse_ads(src)
        extra = parse_gig36(src, {"tv_regular_extra"})
        i = src.find('id:"gig_exodus_film_hand"')
        blk = src[i:i+2200]
        def fld(p):
            m = re.search(p, blk); return m.group(1) if m else ""
        pm = re.search(r"pay:\s*\[(\d+)\s*,\s*(\d+)\]", blk)
        extra.append({"id": "gig_exodus_film_hand", "type": "電影", "roleScale": "film_action_extra",
                      "roleLabel": fld(r"roleLabel:\s*\"([^\"]*)\""),
                      "pay": [int(pm.group(1)), int(pm.group(2))] if pm else None,
                      "title": fld(r"title:\s*\"([^\"]*)\""),
                      "workTitle": fld(r"workTitle:\s*\"([^\"]*)\""), "stars": 1, "year": 1990})
        print("ad gigs parsed:", len(ads), "extra gigs:", len(extra), flush=True)
        results = {}
        only = set(sys.argv[1:])
        cases = [cfg for cfg in CASES if not only or cfg[0] in only]
        with sync_playwright() as pw:
            for cfg in cases:
                run_case(pw, cfg, ads, extra, results)
        with open(os.path.join(OUT, "drive200.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        npass = sum(1 for r in results.values() if r.get("verdict") == "PASS")
        print(f"== SUMMARY {npass}/{len(results)} PASS ==", flush=True)
        for k, r in results.items():
            print(f"  {k}: {r.get('verdict')} fail={json.dumps({kk:vv for kk,vv in (r.get('checks') or {}).items() if not vv}, ensure_ascii=False)}", flush=True)
    finally:
        stop(srv)


if __name__ == "__main__":
    main()
