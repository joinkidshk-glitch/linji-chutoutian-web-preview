#!/usr/bin/env python3
"""v20a136 實駕：結局閘搬去 1992 年 12 月（C17 weekMin 153＋等冬台慶＋backstop 1096）。
Cases（每 case 全新 browser context，免狀態污染）：
  gate_nov      ① 1992-11-15（week 151）C13 done、台慶未解決 → C17 唔開（weekMin 擋）
  gate_dec_open ① 1992-12-05（week 153）C13 done、台慶未解決 → C17 唔開（awardResolved 擋）
  play_c17      ①正／③ 1992-12-05＋台慶 done → C17 開→播呢幕→播完即結局（S.ending410＋地圖鎖死）
  backstop      ② 1993-01-05、C13 未做、台慶未解決 → C17 無條件開
  decline       ④ 推辭：請柬只得 出席／推辭（無稍後）→ flag skipped → 翌日報紙有結果
  reload        ⑤ reload 後請柬再出現（S.pendingAwardPack 持久化）
  c10_defer     ⑥ C10 未做：12 月 TV 典禮讓路（無請柬）；1 月排到（有請柬）
  review        ⑦ 12 月 20 日起：week 155 強警告（floor 155）→ week 156 邊界判收場（pendingEnding review）
play_c17 另行 430×700 viewport 做對話框唔被切量度。
用法：/home/hatch/pwenv49/bin/python qa136/drive136.py [case|all] [932|700]
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work136"
HERE = "/home/hatch/workspace/linji-work136/qa136"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8969
SAVE_KEY = "starVolunteer_map_v19w"

def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)

def click_vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false;
      vis[0].click(); return true;
    }""", text)

def modal_info(pg):
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      if (!m) return {visible:false};
      const cs = getComputedStyle(m);
      const r = m.getBoundingClientRect();
      const vis = r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden';
      if (!vis) return {visible:false};
      const h3 = (document.querySelector('#modal h3')||{}).textContent || '';
      const btns = [...document.querySelectorAll('#modal-btns button')].map(b => (b.textContent||'').trim()).filter(Boolean);
      // 抉擇唔喺 #modal-btns，係 .sp-choice 按鈕（StoryPlay choices layout）
      const choices = [...document.querySelectorAll('#modal .sp-choice')].map(b => (b.textContent||'').trim()).filter(Boolean);
      const body = (m.innerText || '').slice(0, 900);
      return {visible:true, h3, btns, choices, body};
    }""")

def click_sp_choice(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('#modal .sp-choice')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false;
      vis[0].click(); return true;
    }""", text)

def dismiss_once(pg):
    """撳 #modal-btns 第一個掣。注意：掣一撳 modal 即關，元素 detach 會令 click() 擲錯——
    嗰陣 click 其實已落地，唔可以回 False（pump 會誤撳「返回地圖」走人，致全跑間歇性卡住）。
    所以：掣可見＋click 已發出就回 True；只有搵唔到掣先回 False。"""
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            try:
                btn.click(timeout=1000)
            except Exception:
                pass  # click 已發出、modal 關咗令元素 detach —— 當成功
            return True
    except Exception:
        pass
    return False

def new_game_to_map(pg):
    pg.goto(f"http://127.0.0.1:{PORT}/index.html?softPreview=1")
    pg.wait_for_timeout(1500)
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
    pg.wait_for_timeout(1000)
    try:
        pg.locator('[data-slot="3"]').first.click(timeout=1500)
        pg.wait_for_timeout(800)
    except Exception:
        pass
    for _ in range(10):
        try:
            pg.get_by_text("跳過教學", exact=True).first.click(timeout=1200)
            pg.wait_for_timeout(600)
            break
        except Exception:
            try:
                pg.get_by_text("下一步", exact=True).first.click(timeout=1200)
                pg.wait_for_timeout(600)
            except Exception:
                break
    pg.wait_for_timeout(1200)
    for _ in range(40):
        # 先驗 modal（地圖掣喺 modal 背後仍量度為 visible）
        if not modal_info(pg).get("visible") and vis_btn(pg, "過一日"):
            return True
        if not dismiss_once(pg):
            if not click_vis_btn(pg, "返回地圖"):
                pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    return False

def day_index(y, m, d):
    import datetime
    return (datetime.date(y, m, d) - datetime.date(1990, 1, 1)).days

PRE_C17 = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16"]

def seed(pg, *, day, done_ids=(), award_flag="", fame=40, stage=10, acting=10,
         credit_delta=0, money=5000, stress=0, c10_flag=None):
    return pg.evaluate("""(o) => {
      const done = {};
      (o.done_ids || []).forEach(id => { done[id] = true; });
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = done;
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = o.award_flag ? { "1992/award_singho_tv": o.award_flag } : {};
      S.pendingAwardPack = null;
      // 1992 年尾存檔：芬姐送別戲（1990 春）理應已發生，唔好俾 wf4PresentPending 喺晨鏈自動播出嚟擋路
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = o.fame; S.stage = o.stage; S.acting = o.acting;
      S.industryCreditDelta = o.credit_delta;
      S.money = o.money; S.stress = o.stress;
      S.flags = S.flags || {};
      if (o.c10_flag === true) { S.flags.C10 = true; S.flags.done_C10 = true; S.flags["story_C10"] = true; }
      if (o.c10_flag === false) { delete S.flags.C10; delete S.flags.done_C10; delete S.flags["story_C10"]; }
      if (typeof BehaviorGate !== "undefined" && BehaviorGate.readCtx) {
        const ctx = BehaviorGate.readCtx({});
        return { day: S.dayIndex, week: ctx.week, year: ctx.year, season: ctx.season, dual: ctx.dual };
      }
      return { day: S.dayIndex };
    }""", {"day": day, "done_ids": list(done_ids), "award_flag": award_flag,
            "fame": fame, "stage": stage, "acting": acting, "credit_delta": credit_delta,
            "money": money, "stress": stress, "c10_flag": c10_flag})

def gate_c17(pg):
    return pg.evaluate("""() => {
      try {
        const r = BehaviorGate.evalGate3Y('C17', {});
        let open = null;
        try { open = (StoryOC.listOpen({player:true}).open || []).map(x => x.id); } catch(_e) {}
        return { ok: r.ok, reasons: r.reasons || [], openIds: open };
      } catch(e) { return { error: String(e) }; }
    }""")

def open_progress(pg):
    pg.evaluate("() => { const c = document.querySelector('#chip-story'); if(c) c.click(); }")
    pg.wait_for_timeout(1200)
    return pg.evaluate("""() => {
      const rows = [...document.querySelectorAll('.prog71-row')];
      const c17 = rows.find(x => (x.textContent||'').includes('三年收科'));
      const all = rows.map(r => (r.textContent||'').slice(0, 90));
      return { c17: c17 ? c17.textContent.slice(0, 600) : null,
               hasPlayBtn: c17 ? !!c17.querySelector('[data-prog77-play]') : false,
               rows: all };
    }""")

def close_progress(pg):
    # 進度頁係手帳 tab：撳返地圖 tab／返回地圖
    if click_vis_btn(pg, "返回地圖"):
        pg.wait_for_timeout(800)
        return
    pg.evaluate("() => { const b = [...document.querySelectorAll('button')].find(x => (x.textContent||'').trim() === '地圖'); if (b) b.click(); }")
    pg.wait_for_timeout(800)

def goto_tv_location(pg):
    """撳地圖星河電視台掣入地點；途中可能觸發巧遇（下一句泵走），再返地圖觸發
    goToMapForBrowse 鏈（頒獎請柬／晨報）。回傳 {sheetOpened, invite}。"""
    ok = pg.evaluate("""() => {
      const b = document.querySelector('[data-loc="tvb_longmen"]');
      if (!b) return false; b.click(); return true;
    }""")
    pg.wait_for_timeout(1000)
    sheet = vis_btn(pg, "返回地圖")
    invite = None
    for _ in range(50):
        mi = modal_info(pg)
        if mi.get("visible") and any("出席" in b for b in mi.get("btns") or []):
            invite = mi
            break
        if vis_btn(pg, "下一句"):
            click_vis_btn(pg, "下一句")
            pg.wait_for_timeout(700)
            continue
        if vis_btn(pg, "返回地圖"):
            click_vis_btn(pg, "返回地圖")
            pg.wait_for_timeout(1200)
            mi2 = modal_info(pg)
            if mi2.get("visible") and any("出席" in b for b in mi2.get("btns") or []):
                invite = mi2
            break
        pg.wait_for_timeout(500)
    return {"clicked": ok, "sheetOpened": sheet, "invite": invite}

def map_ready(pg):
    """返到地圖：v-map on、無 modal ＋ 過一日或開始今日行程（晨鏈後地圖主掣係後者，過一日收喺計劃表入面）。"""
    return pg.evaluate("() => { const v = document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }") \
        and (not modal_info(pg).get("visible")) and (vis_btn(pg, "過一日") or vis_btn(pg, "開始今日行程"))

def home_on(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")

def pump_to_map(pg, secs=45, stop_on_invite=False):
    """撳走途中 modal 直到返地圖（見到 過一日），回傳途中見過嘅 modal 文字清單。
    stop_on_invite：見到頒獎請柬（有 出席 掣）即停，唔好撳走佢，回傳 invite。
    另快照 S.weekBoundary105.html（週結算 flavor：評核警告／結果行文只寫入呢度，enterHome 唔 render，
    要喺入屋清旗之前攞走）。"""
    seen = []
    wb_html = None
    t0 = time.time()
    while time.time() - t0 < secs:
        try:
            wb = pg.evaluate("() => (typeof S !== 'undefined' && S && S.weekBoundary105) ? (S.weekBoundary105.html || '') : ''")
            if wb:
                wb_html = wb
        except Exception:
            pass
        # 先驗 modal：地圖掣喺 modal 背後仍然量度為 visible，唔可以先驗佢
        mi = modal_info(pg)
        if mi.get("visible"):
            if stop_on_invite and any("出席" in b for b in mi.get("btns") or []):
                seen.append({"h3": mi.get("h3", ""), "btns": mi.get("btns", []), "body": (mi.get("body", "") or "")[:400]})
                return {"onMap": False, "seen": seen, "invite": mi, "weekBoundaryHtml": wb_html}
            seen.append({"h3": mi.get("h3", ""), "btns": mi.get("btns", []), "body": (mi.get("body", "") or "")[:400]})
            if not dismiss_once(pg):
                if not click_vis_btn(pg, "返回地圖"):
                    pg.wait_for_timeout(400)
        elif home_on(pg) and vis_btn(pg, "確定本週行程"):
            # 週日結算後屋企畫面：先記低週結算文字（評核警告／結果行文經 S.weekBoundary105 喺呢度顯示），再確定本週行程開週，晨鏈（報紙／請柬）喺開週前彈出
            seen.append({"h3": "屋企（週結算）", "btns": [], "body": pg.evaluate("() => { const v = document.getElementById('v-home'); return v ? v.innerText.slice(0, 1500) : ''; }")})
            click_vis_btn(pg, "確定本週行程")
            pg.wait_for_timeout(800)
        elif map_ready(pg):
            return {"onMap": True, "seen": seen, "weekBoundaryHtml": wb_html}
        else:
            pg.wait_for_timeout(400)
        pg.wait_for_timeout(300)
    return {"onMap": map_ready(pg), "seen": seen, "weekBoundaryHtml": wb_html}

def pump_story_to_map(pg, secs=90):
    """撳走途中 modal／劇情（下一句／抉擇揀第一個）直到返地圖，回傳見過嘅 modal 清單。"""
    seen = []
    t0 = time.time()
    while time.time() - t0 < secs:
        mi = modal_info(pg)
        if mi.get("visible"):
            seen.append({"h3": mi.get("h3", ""), "btns": mi.get("btns", []),
                         "choices": mi.get("choices", []), "body": (mi.get("body", "") or "")[:300]})
            btns = mi.get("btns") or []
            if any("下一句" in b for b in btns):
                click_vis_btn(pg, "下一句")
                pg.wait_for_timeout(600)
                continue
            if mi.get("choices"):
                pg.evaluate("""() => { const b = document.querySelector('#modal .sp-choice'); if (b) b.click(); }""")
                pg.wait_for_timeout(800)
                continue
            if not dismiss_once(pg):
                if not click_vis_btn(pg, "返回地圖"):
                    pg.wait_for_timeout(400)
        elif home_on(pg) and vis_btn(pg, "確定本週行程"):
            # 週日結算後屋企畫面：先記低週結算文字（評核警告／結果行文經 S.weekBoundary105 喺呢度顯示），再確定本週行程開週，晨鏈（報紙／請柬）喺開週前彈出
            seen.append({"h3": "屋企（週結算）", "btns": [], "body": pg.evaluate("() => { const v = document.getElementById('v-home'); return v ? v.innerText.slice(0, 1500) : ''; }")})
            click_vis_btn(pg, "確定本週行程")
            pg.wait_for_timeout(800)
        elif map_ready(pg):
            return {"onMap": True, "seen": seen}
        else:
            pg.wait_for_timeout(400)
        pg.wait_for_timeout(300)
    return {"onMap": map_ready(pg), "seen": seen}

def advance_day(pg, stop_on_invite=False):
    if vis_btn(pg, "過一日"):
        click_vis_btn(pg, "過一日")
    elif vis_btn(pg, "開始今日行程"):
        # 晨鏈後地圖主掣係開始今日行程：撳開計劃表，週日會彈休息提示（回家結算＝瞓一日過日）
        click_vis_btn(pg, "開始今日行程")
        pg.wait_for_timeout(1000)
        mi = modal_info(pg)
        if mi.get("visible") and any("回家結算" in b for b in mi.get("btns") or []):
            click_vis_btn(pg, "回家結算")
        elif vis_btn(pg, "過一日"):
            click_vis_btn(pg, "過一日")
        else:
            return {"advanced": False, "seen": []}
    else:
        return {"advanced": False, "seen": []}
    pg.wait_for_timeout(800)
    return {"advanced": True, **pump_to_map(pg, 45, stop_on_invite=stop_on_invite)}

def save_slot1(pg):
    return pg.evaluate("""(key) => {
      try { localStorage.setItem(key, JSON.stringify(S)); return { saved: true, day: S.dayIndex, hasPending: !!S.pendingAwardPack }; }
      catch(e) { return { saved: false, error: String(e) }; }
    }""", SAVE_KEY)

def s_state(pg):
    return pg.evaluate("""() => ({
      day: S.dayIndex, ending410: !!S.ending410,
      awardsFlags: S.awardsFlags || {},
      pendingAwardPack: S.pendingAwardPack ? { ceremonyId: S.pendingAwardPack.ceremonyId, year: S.pendingAwardPack.year, tier: S.pendingAwardPack.tier } : null,
      newspaperQueue: (S.newspaperQueue || []).map(q => q.eventKey),
      clippings: (S.newspaperClippings || []).flatMap(c => (c && c.eventKeys) || []),
      conseq61: S.conseq61 ? { reviews: S.conseq61.reviews || {}, pendingEnding: S.conseq61.pendingEnding || null } : null,
      storyDoneC17: !!(S.story && S.story.done && S.story.done.C17),
    })""")

# ---------------- cases ----------------
def case_gate_nov(pg):
    ctx = seed(pg, day=day_index(1992, 11, 22), done_ids=PRE_C17, award_flag="")
    g = gate_c17(pg)
    pr = open_progress(pg)
    checks = {
        "ctx_week_151": ctx.get("week") == 151,
        "ctx_season_autumn": ctx.get("season") == "秋",
        "gate_closed": g.get("ok") is False,
        "gate_weekMin_blocks": "weekMin:153" in (g.get("reasons") or []),
        "listOpen_no_C17": g.get("openIds") is not None and "C17" not in g["openIds"],
        "progress_C17_locked": pr.get("c17") is not None and "已開放" not in pr["c17"],
        "progress_shows_award_item": pr.get("c17") is not None and "等冬台慶有結果" in pr["c17"],
        "progress_no_play_btn": pr.get("hasPlayBtn") is False,
    }
    return {"checks": checks, "ctx": ctx, "gate": g, "c17row": pr.get("c17")}

def case_gate_dec_open(pg):
    ctx = seed(pg, day=day_index(1992, 12, 5), done_ids=PRE_C17, award_flag="")
    g = gate_c17(pg)
    pr = open_progress(pg)
    checks = {
        "ctx_week_153plus": (ctx.get("week") or 0) >= 153,
        "gate_closed": g.get("ok") is False,
        "gate_only_award_blocks": g.get("reasons") == ["awardResolved:1992/award_singho_tv"],
        "listOpen_no_C17": g.get("openIds") is not None and "C17" not in g["openIds"],
        "progress_C17_locked": pr.get("c17") is not None and "已開放" not in pr["c17"],
        "progress_no_play_btn": pr.get("hasPlayBtn") is False,
        "progress_displays_1992_winter": pr.get("c17") is not None and "1992 年冬" in pr["c17"] and "1994" not in pr["c17"],
    }
    return {"checks": checks, "ctx": ctx, "gate": g, "c17row": pr.get("c17")}

def case_play_c17(pg, W, H):
    ctx = seed(pg, day=day_index(1992, 12, 5), done_ids=PRE_C17, award_flag="done", c10_flag=True)
    g = gate_c17(pg)
    out = {"ctx": ctx, "gate": g, "checks": {}, "story": []}
    out["checks"]["gate_open"] = g.get("ok") is True
    out["checks"]["listOpen_has_C17"] = g.get("openIds") is not None and "C17" in g["openIds"]
    # 入星河電視台（可能即場觸發 C17），否則經進度頁 播呢幕
    clicked = pg.evaluate("() => { const b = document.querySelector('[data-loc=\"tvb_longmen\"]'); if (!b) return false; b.click(); return true; }")
    pg.wait_for_timeout(1200)
    mi = modal_info(pg)
    started = False
    if mi.get("visible") and ("三年收科" in (mi.get("body") or "") or "頒獎禮" in (mi.get("body") or "")):
        started = True
        out["entry"] = "auto_on_enter_location"
    if not started:
        # 返地圖→進度頁→播呢幕
        pump_to_map(pg, 20)
        pr = open_progress(pg)
        out["progress_c17"] = pr.get("c17")
        out["checks"]["progress_open_with_play"] = pr.get("hasPlayBtn") is True
        if pr.get("hasPlayBtn"):
            pg.evaluate("() => { const b = document.querySelector('[data-prog77-play=\"C17\"]'); if (b) b.click(); }")
            pg.wait_for_timeout(1200)
            started = True
            out["entry"] = "progress_play_button"
    out["checks"]["story_started"] = started
    if not started:
        pg.screenshot(path=os.path.join(SHOTS, f"play_c17_{W}x{H}_nostart.png"))
        return out
    pg.wait_for_timeout(800)
    # 量度對話框（第一拍）
    measure = pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); return {bottom: Math.round(b.bottom), h: Math.round(b.height)}; };
      const sp = q('#modal .story-play'), plate = q('#modal .dlg106-plate'), line = q('#modal .dlg106-plate .sp-line'), inner = q('#modal-inner');
      return { storyPlay: r(sp), plate: r(plate), line: r(line),
               innerScrollH: inner ? inner.scrollHeight : null, innerClientH: inner ? inner.clientHeight : null,
               firstLine: line ? line.textContent : '' };
    }""")
    out["first_measure"] = measure
    fl = measure.get("firstLine") or ""
    out["checks"]["first_line_post_ceremony"] = ("散場" in fl) and ("1992" in fl) and ("1994" not in fl)
    out["checks"]["header_displays_1992_winter"] = bool(out["story"] and False)  # 佔位，下一步泵完再驗（見 story[0]）
    out["checks"]["dialog_not_clipped"] = bool(measure.get("line") and measure.get("plate") and measure["line"]["bottom"] <= measure["plate"]["bottom"] + 1)
    pg.screenshot(path=os.path.join(SHOTS, f"c17_play_{W}x{H}.png"))
    # 逐句泵：下一句 → 抉擇 → 揀「順其自然」→ 繼續 下一句 直到 S.ending410
    picked = False
    for i in range(60):
        st = s_state(pg)
        if st.get("ending410"):
            break
        mi = modal_info(pg)
        out["story"].append({"i": i, "h3": mi.get("h3", ""), "btns": mi.get("btns", []),
                             "choices": mi.get("choices", []),
                             "body": (mi.get("body", "") or "")[:220]})
        btns = mi.get("btns") or []
        chs = mi.get("choices") or []
        if not picked and any("順其自然" in c for c in chs):
            click_sp_choice(pg, "順其自然")
            picked = True
            pg.wait_for_timeout(900)
            continue
        if any("下一句" in b for b in btns):
            click_vis_btn(pg, "下一句")
            pg.wait_for_timeout(700)
            continue
        if btns:
            # 結局總結頁掣（例：睇總結／完成）——撳第一個繼續
            dismiss_once(pg)
            pg.wait_for_timeout(900)
            continue
        pg.wait_for_timeout(500)
    # 頁首年份：第一拍 body 應寫「主線 · 1992冬」（walk 將源頭 1990 顯示做 1992），唔係 1994
    first_body = (out["story"][0].get("body", "") if out["story"] else "")
    out["checks"]["header_displays_1992_winter"] = ("1992冬" in first_body) and ("1994" not in first_body)
    st = s_state(pg)
    out["picked_choice"] = picked
    out["final_state"] = st
    out["checks"]["choice_picked"] = picked
    out["checks"]["ending410_written"] = st.get("ending410") is True
    out["checks"]["story_C17_done"] = st.get("storyDoneC17") is True
    pg.screenshot(path=os.path.join(SHOTS, f"c17_ending_{W}x{H}.png"))
    # 地圖鎖死：進度頁／過一日唔應再出現；返地圖應出結局總結
    end_modal = modal_info(pg)
    out["ending_modal"] = {"h3": end_modal.get("h3", ""), "btns": end_modal.get("btns", []),
                           "body": (end_modal.get("body", "") or "")[:400]}
    if click_vis_btn(pg, "返回地圖"):
        pg.wait_for_timeout(1000)
    mi2 = modal_info(pg)
    out["after_return"] = {"h3": mi2.get("h3", ""), "btns": mi2.get("btns", []), "body": (mi2.get("body", "") or "")[:300]}
    out["checks"]["map_locked_no_advance"] = vis_btn(pg, "過一日") is False
    pg.screenshot(path=os.path.join(SHOTS, f"c17_locked_{W}x{H}.png"))
    return out

def case_backstop(pg):
    ctx = seed(pg, day=day_index(1993, 1, 5), done_ids=(), award_flag="")
    g = gate_c17(pg)
    pr = open_progress(pg)
    checks = {
        "ctx_day_ge_1096": ctx.get("day", 0) >= 1096,
        "gate_open_unconditional": g.get("ok") is True,
        "gate_no_reasons": (g.get("reasons") or []) == [],
        "listOpen_has_C17": g.get("openIds") is not None and "C17" in g["openIds"],
    }
    return {"checks": checks, "ctx": ctx, "gate": g, "progress_rows": pr.get("rows")}

def case_decline(pg):
    # 12 月 5 日＋C10 已做 → 過一日（晨鏈 goToMapForBrowse 排請柬）→ 請柬彈出
    ctx = seed(pg, day=day_index(1992, 12, 5), done_ids=PRE_C17, award_flag="", c10_flag=True)
    adv0 = advance_day(pg, stop_on_invite=True)
    inv = adv0.get("invite") or {}
    checks = {
        "invite_shown": bool(inv.get("visible")),
        "invite_is_tv": "台慶" in (inv.get("body") or "") or "星河台慶" in (inv.get("h3") or "") or "頒獎" in (inv.get("body") or ""),
        "invite_has_attend": any("出席" in b for b in inv.get("btns") or []),
        "invite_has_decline": any("推辭" in b for b in inv.get("btns") or []),
        "invite_no_later": not any("稍後" in b for b in inv.get("btns") or []),
    }
    out = {"checks": checks, "ctx": ctx, "invite": inv, "morning_seen": adv0.get("seen", [])}
    pg.screenshot(path=os.path.join(SHOTS, "invite_decline.png"))
    if not checks["invite_shown"]:
        return out
    click_vis_btn(pg, "推辭")
    pg.wait_for_timeout(1200)
    # 推辭後晨鏈可能自動播其他待播劇情（例：啟德送芬姐）——先行完佢哋先返地圖
    pumped = pump_story_to_map(pg, 90)
    out["post_decline_pump"] = pumped
    st = s_state(pg)
    out["after_decline"] = st
    checks["flag_skipped"] = (st.get("awardsFlags") or {}).get("1992/award_singho_tv") == "skipped"
    checks["pending_cleared"] = st.get("pendingAwardPack") is None
    checks["paper_queued_next_day"] = "award:1992:award_singho_tv" in (st.get("newspaperQueue") or [])
    # 翌日：過一日 → 晨報應講台慶結果
    adv = advance_day(pg)
    papers = [s for s in adv.get("seen", []) if "報" in s.get("h3", "") or "剪報" in (s.get("body") or "") or "台慶" in (s.get("body") or "")]
    out["next_day_modals"] = adv.get("seen", [])
    out["paper_modals"] = papers
    st2 = s_state(pg)
    out["after_next_day"] = st2
    checks["paper_next_day"] = len(papers) > 0
    checks["clip_recorded"] = "award:1992:award_singho_tv" in (st2.get("clippings") or [])
    if papers:
        body = papers[0].get("body", "")
        checks["paper_mentions_ceremony"] = ("台慶" in body) or ("頒獎" in body)
        checks["paper_no_false_win"] = ("阿偉" not in body) or ("得獎" not in body and "奪獎" not in body)
    pg.screenshot(path=os.path.join(SHOTS, "decline_nextday.png"))
    return out

def case_reload(pg):
    ctx = seed(pg, day=day_index(1992, 12, 5), done_ids=PRE_C17, award_flag="", c10_flag=True)
    adv0 = advance_day(pg, stop_on_invite=True)
    inv = adv0.get("invite") or {}
    out = {"ctx": ctx, "invite_before": inv, "checks": {}}
    out["checks"]["invite_shown_before"] = bool(inv.get("visible"))
    if not inv.get("visible"):
        return out
    st0 = s_state(pg)
    out["state_before_reload"] = st0
    out["checks"]["pack_persisted_in_S"] = (st0.get("pendingAwardPack") or {}).get("ceremonyId") == "award_singho_tv"
    sv = save_slot1(pg)
    out["save"] = sv
    pg.reload()
    pg.wait_for_timeout(1500)
    # 標題畫面：搵 繼續／讀檔
    title_btns = pg.evaluate("""() => [...document.querySelectorAll('button')].filter(b=>{const r=b.getBoundingClientRect(); return r.width>0&&r.height>0;}).map(b=>(b.textContent||'').trim()).slice(0,15)""")
    out["title_btns"] = title_btns
    continued = False
    for label in ["繼續", "讀檔", "載入"]:
        if click_vis_btn(pg, label):
            continued = True
            pg.wait_for_timeout(1000)
            break
    out["continued_via"] = continued
    if continued:
        # 讀檔槽 1
        if pg.evaluate("() => { const b=[...document.querySelectorAll('[data-slot=\"1\"]')]; if(b.length){b[0].click(); return true;} return false; }"):
            pg.wait_for_timeout(1200)
        # 可能彈「讀取槽 1？」確認
        if click_vis_btn(pg, "讀取") or click_vis_btn(pg, "確認"):
            pg.wait_for_timeout(1200)
    # 讀檔後、未行任何晨鏈之前，即刻驗還原嘅 day（應＝存檔嗰陣 1070）
    out["state_right_after_continue"] = s_state(pg)
    pump = pump_to_map(pg, 30, stop_on_invite=True)
    out["pump_after_reload"] = pump
    st1 = s_state(pg)
    out["state_after_reload"] = st1
    # 存檔寫嗰陣 day 1070（12 月 6 日，週日）；撳「繼續」載入嗰陣 pending 嘅週日結算即刻行（1070→1071），係遊戲本身行為——還原成功即 day 係 1070 或 1071
    out["checks"]["save_restored_day"] = out.get("state_right_after_continue", {}).get("day") in (day_index(1992, 12, 6), day_index(1992, 12, 7))
    out["checks"]["pack_survived_reload"] = (st1.get("pendingAwardPack") or {}).get("ceremonyId") == "award_singho_tv"
    # 請柬應重現：可能已經喺 continue 後嘅晨鏈出咗，否則過一日再觸發
    inv2 = pump.get("invite") or {}
    if not inv2.get("visible"):
        adv1 = advance_day(pg, stop_on_invite=True)
        out["advance_after_reload"] = adv1
        inv2 = adv1.get("invite") or {}
    out["invite_after"] = inv2
    out["checks"]["invite_shown_after_reload"] = bool(inv2.get("visible"))
    out["checks"]["invite_after_no_later"] = not any("稍後" in b for b in (inv2.get("btns") or []))
    pg.screenshot(path=os.path.join(SHOTS, "invite_reload.png"))
    return out

def case_c10_defer(pg):
    # 12 月 5 日（第 153 週，年內第 49 週）＋C10 未做（其餘主線做晒，免自動播放鏈擋路）→ 過一日，TV 讓路，唔應有請柬
    no_c10 = [c for c in PRE_C17 if c != "C10"]
    ctx1 = seed(pg, day=day_index(1992, 12, 5), done_ids=no_c10, award_flag="", c10_flag=False)
    adv1 = advance_day(pg, stop_on_invite=True)
    inv1 = adv1.get("invite")
    on_map1 = map_ready(pg)
    st1 = s_state(pg)
    checks = {
        "dec_week49": (ctx1.get("week") or 0) == 153 and ((ctx1.get("week") - 1) % 52) + 1 == 49,
        "dec_no_invite": not (inv1 or {}).get("visible"),
        "dec_still_on_map": on_map1 is True,
        "dec_flag_still_empty": (st1.get("awardsFlags") or {}).get("1992/award_singho_tv") in (None, ""),
        "dec_no_pending_pack": st1.get("pendingAwardPack") is None,
    }
    # 1 月 5 日（年內第 2 週）→ C10 窗口已過，同一屆應排到
    ctx2 = seed(pg, day=day_index(1993, 1, 5), done_ids=no_c10, award_flag="", c10_flag=False)
    adv2 = advance_day(pg, stop_on_invite=True)
    inv2 = adv2.get("invite") or {}
    st2 = s_state(pg)
    checks["jan_invite_shown"] = bool(inv2.get("visible"))
    checks["jan_invite_is_tv"] = ("台慶" in (inv2.get("body") or "")) or ("頒獎" in (inv2.get("body") or ""))
    checks["jan_edition_1992"] = "1992" in (inv2.get("body") or "")
    pg.screenshot(path=os.path.join(SHOTS, "c10_defer_jan.png"))
    return {"checks": checks, "ctx_dec": ctx1, "ctx_jan": ctx2,
            "dec_invite": inv1, "jan_invite": inv2, "state_jan": st2}

def case_review(pg):
    # 12 月 20 日（week 155 尾日），dual 低（fame 20/stage 0/acting 8/delta 0 → dual 32）
    ctx = seed(pg, day=day_index(1992, 12, 20), done_ids=PRE_C17, award_flag="done",
               fame=20, stage=0, acting=8, credit_delta=0, money=5000, stress=0, c10_flag=True)
    out = {"ctx": ctx, "checks": {}}
    out["checks"]["seed_week_155"] = ctx.get("week") == 155
    out["checks"]["seed_dual_low"] = (ctx.get("dual") or 999) < 155
    adv1 = advance_day(pg)  # → 12 月 21 日，結算 week 155：強警告
    out["advance1"] = adv1
    # 警告行文唔喺 modal，喺 S.weekBoundary105.html（pump 快照，未入屋清旗之前攞走）
    wb1 = adv1.get("weekBoundaryHtml") or ""
    out["warn_week_boundary_html"] = wb1
    out["checks"]["warn_mentions_1992_review"] = "1992" in wb1 and "評核" in wb1
    out["checks"]["warn_shows_floor_155"] = "155" in wb1
    out["checks"]["warn_shows_dual"] = str(ctx.get("dual")) in wb1
    pg.screenshot(path=os.path.join(SHOTS, "review_warn.png"))
    # 行到 12 月 28 日（day 1092）：結算 week 156 邊界
    boundary = []
    boundary_wb = []
    for d in range(7):
        adv = advance_day(pg)
        boundary.extend(adv.get("seen", []))
        if adv.get("weekBoundaryHtml"):
            boundary_wb.append(adv.get("weekBoundaryHtml"))
        st = s_state(pg)
        if (st.get("conseq61") or {}).get("reviews", {}).get("1992"):
            break
    out["boundary_modals"] = boundary
    out["boundary_week_boundary_html"] = boundary_wb
    st2 = s_state(pg)
    out["state_after_boundary"] = st2
    rev = ((st2.get("conseq61") or {}).get("reviews") or {}).get("1992") or {}
    pe = ((st2.get("conseq61") or {}).get("pendingEnding") or {})
    out["checks"]["review_1992_recorded"] = bool(rev)
    out["checks"]["review_floor_155"] = rev.get("floor") == 155
    out["checks"]["review_failed_low_dual"] = rev.get("passed") is False and (rev.get("dual") or 999) < 155
    # pendingEnding 係過渡值：強制收場呈現嗰陣被消耗（寫入 ending410）——驗呈現本身：評核場面＋提早收科總結出過
    btext = " ".join(s.get("body", "") for s in boundary)
    bh3 = " ".join(s.get("h3", "") for s in boundary)
    out["checks"]["forced_ending_presented"] = ("事務所評核" in bh3) and ("提早收科" in bh3)
    # 結算行文原文（「1992 年尾評核結果出咗」）由 conseq61SettleEval 生成，喺單元測試直接驗（test_conseq61_1992_logic.js）；
    # 實駕層驗玩家面可見嘅強制收場呈現（評核場面＋提早收科總結）同紀錄數字
    pg.screenshot(path=os.path.join(SHOTS, "review_boundary.png"))
    return out

CASES = {
    "gate_nov": lambda pg, W, H: case_gate_nov(pg),
    "gate_dec_open": lambda pg, W, H: case_gate_dec_open(pg),
    "play_c17": case_play_c17,
    "backstop": lambda pg, W, H: case_backstop(pg),
    "decline": lambda pg, W, H: case_decline(pg),
    "reload": lambda pg, W, H: case_reload(pg),
    "c10_defer": lambda pg, W, H: case_c10_defer(pg),
    "review": lambda pg, W, H: case_review(pg),
}

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    h_arg = sys.argv[2] if len(sys.argv) > 2 else "932"
    sel = list(CASES.keys()) if arg == "all" else [arg]
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    results = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=EXE)
            for name in sel:
                heights = [932, 700] if (name == "play_c17" and h_arg == "all") else [int(h_arg)]
                for H in heights:
                    key = f"{name}_{430}x{H}" if len(heights) > 1 else name
                    print(f"== {key} ==", flush=True)
                    errs = []
                    ctx = b.new_context(viewport={"width": 430, "height": H})
                    pg = ctx.new_page()
                    pg.on("pageerror", lambda e: errs.append(str(e)))
                    try:
                        if not new_game_to_map(pg):
                            results[key] = {"verdict": "ERROR", "checks": {}, "note": "new game did not reach map"}
                            print("  ERROR: no map", flush=True)
                            continue
                        r = CASES[name](pg, 430, H)
                        r["pageerrors"] = errs[:5]
                        checks = r.get("checks", {})
                        r["verdict"] = "PASS" if checks and all(checks.values()) else "FAIL"
                        results[key] = r
                        print(f"  {r['verdict']} {json.dumps(checks, ensure_ascii=False)}", flush=True)
                        for k in ("gate", "ctx"):
                            if k in r:
                                print(f"    {k}: {json.dumps(r[k], ensure_ascii=False)[:300]}", flush=True)
                    except Exception as e:
                        results[key] = {"verdict": "ERROR", "checks": {}, "error": repr(e)}
                        print(f"  ERROR {e!r}", flush=True)
                        try:
                            pg.screenshot(path=os.path.join(SHOTS, f"err_{key}.png"))
                        except Exception:
                            pass
                    finally:
                        ctx.close()
            b.close()
    finally:
        srv.terminate()
    out = os.path.join(HERE, "drive136.json")
    json.dump(results, open(out, "w"), ensure_ascii=False, indent=1)
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    print(f"OVERALL {n_pass}/{len(results)} PASS | {out}")
    sys.exit(0 if n_pass == len(results) else 1)

if __name__ == "__main__":
    main()
