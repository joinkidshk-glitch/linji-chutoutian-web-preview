# -*- coding: utf-8 -*-
"""v20a144 實駕：紅星巧遇頻率收緊（每日 1 次＋每週 2 次）。
逐點證實：① 同日第二個有星地點唔觸發（每日 1 次）② 同一週第三次唔觸發（每週 2 次）
③ 下一週重置返（又觸發到）④ 正常巧遇流程零回歸（初遇／對白／好感加減）。
方法：Playwright 真 UI（430x932，?softPreview=1，本地 http.server）；出沒盤用 Python
重算日種子（FNV-1a，同 index.html enc79Hash／enc79Rand／enc79PresenceP 一致，1990 春、
冇風聲時 luk／liu／mak p=0.6（伏筆節拍開住 +0.10）、yip p=0.5），再用 live window.S
核對當日 S.starDay.presence（入場嗰刻已計好成盤）。每次入場前 reset live travel114
（drive137 同款 probe 技巧，唔郁存檔），等出行額度唔阻實駕。
用法：/home/hatch/pwenv49/bin/python qa144/drive144.py
輸出：qa144/drive144.json ＋ qa144/shots/*.png
"""
import json, os, subprocess, sys, time, hashlib, urllib.request, socket

ROOT = "/home/hatch/workspace/linji-work144"
HERE = os.path.join(ROOT, "qa144")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8994
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    """起本地 server＋核實 serve 緊嘅確係工作副本（drive141 同款；port 撞咗／serve 錯檔要即刻死，唔好靜靜行錯 code）。"""
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", PORT))
    except OSError as e:
        raise RuntimeError(f"port {PORT} 已被佔用，唔開 drive（驚食錯 server 嘅舊 code）: {e}")
    finally:
        s.close()
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError("http.server died on start")
    st, body = http_body("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    assert st == 200 and sha == exp, f"served index mismatch: {sha[:12]} != {exp[:12]}（可能撞咗其他 server）"
    assert b"ENC79_WEEKLY_CAP" in body, "served index 冇 v144 改動"
    print("serve ok sha", sha[:12], flush=True)
    return p

def stop(p):
    try:
        p.send_signal(__import__("signal").SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

# 試點四星（ENC79_PILOT）：主場／副場
PILOTS = {
    "luk_baakyin": ("film_lion", "rec_star"),
    "liu_bingxing": ("cafe_cha", "film_cotton"),
    "mak_zhendong": ("film_cotton", "film_lion"),
    "yip_manji": ("rec_hk", "tvb_kowloon"),
}
LOC_NAME = {"film_lion": "獅子山製片", "rec_star": "天星音樂", "cafe_cha": "金龍茶餐廳",
            "film_cotton": "紅棉影業", "rec_hk": "香江唱片", "tvb_kowloon": "九龍電視台"}
# 初遇最佳選項關鍵字（enc79ChoiceFx：呢啲 +3）
BEST_CHOICE = {"luk_baakyin": ["雙手", "唔多口"], "liu_bingxing": ["好笑"],
                "mak_zhendong": ["放低"], "yip_manji": ["唔出聲"]}

def fnv1a(s):
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h

def rand(key):
    return (fnv1a(key) % 100000) / 100000

def predict(day, foreshadow_done, whispers):
    """回 {loc: [starIds]}；1990 春、冇季節窗；whispers = {sid: True}。"""
    presence = {}
    for sid, (prim, sec) in PILOTS.items():
        p = 0.6 if (sid != "yip_manji" and sid not in foreshadow_done) else 0.5
        share = 0.65
        if whispers.get(sid):
            p = max(p, 0.80); share = 0.85
        if rand(f"enc79:{day}:{sid}:out") >= p:
            continue
        loc = prim if rand(f"enc79:{day}:{sid}:loc") < share else sec
        presence.setdefault(loc, []).append(sid)
    return presence

# ---------------- playwright helpers（drive137 同款） ----------------
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

def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            btn.click(timeout=1000)
            return True
    except Exception:
        pass
    return False

STATE_JS = """() => {
  const S = window.S || {};
  const q = s => document.querySelector(s);
  const line = q('#enc79-overlay .e79-line');
  const sheet = q('#loc-sheet');
  const stars = {};
  for (const sid of ['luk_baakyin','liu_bingxing','mak_zhendong','yip_manji']) {
    const st = (S.stars||{})[sid] || {};
    stars[sid] = {fav: st.fav||0, met: !!st.met, seen: st.seen||0, lastDay: (st.lastDay===undefined?null:st.lastDay)};
  }
  const wh = {};
  for (const k in (S.starWhispers||{})) wh[k] = !!((S.starWhispers[k]||{}).until >= (S.dayIndex||0));
  return {
    dayIndex: S.dayIndex||0,
    starDay: S.starDay ? {day: S.starDay.day, triggered: S.starDay.triggered||0, presence: S.starDay.presence||{}, doneToday: S.starDay.doneToday||{}} : null,
    starWeek: S.starWeek ? {week: S.starWeek.week, triggered: S.starWeek.triggered||0} : null,
    starFavWeek: S.starFavWeek ? {week: S.starFavWeek.week, gain: S.starFavWeek.gain||0} : null,
    stars, whispers: wh,
    overlay: !!q('#enc79-overlay'),
    overlayLine: line ? (line.textContent||'').trim() : '',
    overlayMeta: (q('#enc79-overlay .e79-meta')||{}).textContent || '',
    sheetOn: !!(sheet && sheet.classList.contains('on')),
    sheetTitle: ((q('#loc-title')||{}).textContent || '').trim(),
    travelUsed: (S.travel114||{}).used,
    homeEditable: !!S.homeEditable,
    homeOn: !!(q('#v-home') && q('#v-home').classList.contains('on')),
    mapOn: !!(q('#v-map') && q('#v-map').classList.contains('on')),
    pins: document.querySelectorAll('.map-pins .pin').length,
    pageErrors: window.__errs || []
  };
}"""

def state(pg):
    return pg.evaluate(STATE_JS)

def reset_travel(pg):
    try:
        pg.evaluate("() => { try{ if(window.S){ window.S.travel114 = {day: Number(window.S.dayIndex)||0, used: 0}; } }catch(e){} }")
    except Exception:
        pass

def goto_map(pg):
    pg.goto(URL)
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
    for _ in range(60):
        st = pg.evaluate("""() => {
          const w = document.querySelector('.map-wrap'); const s = document.querySelector('#loc-sheet');
          const sheetOpen = !!(w && w.classList.contains('sheet-open')) || !!(s && s.classList.contains('on'));
          const storyBtn = [...document.querySelectorAll('#modal-btns button, #enc79-overlay button, .sp-actions button')].some(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
          return {sheetOpen, storyBtn};
        }""")
        if st["sheetOpen"]:
            if not click_vis_btn(pg, "返回地圖"):
                dismiss_once(pg)
            pg.wait_for_timeout(700)
            continue
        if st["storyBtn"]:
            advance_story(pg)
            pg.wait_for_timeout(500)
            continue
        if vis_btn(pg, "過一日"):
            break
        if not dismiss_once(pg):
            pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    pg.wait_for_timeout(800)

ADVANCE_JS = """() => {
  const vis = b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width>0 && r.height>0 && cs.visibility!=='hidden' && cs.display!=='none'; };
  const cands = [...document.querySelectorAll('#modal-btns button, #enc79-overlay button, .sp-actions button, #loc-sheet button')].filter(vis);
  if(!cands.length) return 'none';
  const next = cands.find(b => /下一句|繼續/.test(b.textContent||''));
  const el = next || cands[0];
  const t = (el.textContent||'').trim().slice(0, 12);
  el.click();
  return t;
}"""

def advance_story(pg):
    try:
        return pg.evaluate(ADVANCE_JS)
    except Exception:
        return 'err'

def ensure_on_map(pg, timeout_s=45):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        st = pg.evaluate("""() => {
          const sheet = document.querySelector('#loc-sheet');
          const on = !!(sheet && sheet.classList.contains('on'));
          const endDay = [...document.querySelectorAll('#map-end-day, #map-start-today')].some(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
          const storyBtn = [...document.querySelectorAll('#modal-btns button, #enc79-overlay button, .sp-actions button')].some(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
          const overlay = !!document.querySelector('#enc79-overlay');
          return {on, endDay, storyBtn, overlay};
        }""")
        if st["endDay"] and not st["on"] and not st["storyBtn"] and not st["overlay"]:
            return True
        if st["overlay"]:
            play_encounter(pg)
            continue
        if st["on"]:
            if click_vis_btn(pg, "返回地圖"):
                pg.wait_for_timeout(500)
                continue
        if st["storyBtn"]:
            advance_story(pg)
            pg.wait_for_timeout(450)
            continue
        if dismiss_once(pg):
            pg.wait_for_timeout(400)
            continue
        pg.wait_for_timeout(400)
    return False

def play_encounter(pg, timeout_s=120):
    """播晒成段巧遇對白（唔撳「點頭離開」）；選項揀最佳（+3）嗰個。回 {lines, choices, firstLine}。"""
    lines, choices = [], []
    first_line = None
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        st = state(pg)
        if not st["overlay"]:
            break
        if st["overlayLine"] and (not lines or lines[-1] != st["overlayLine"]):
            lines.append(st["overlayLine"])
            if first_line is None:
                first_line = st["overlayLine"]
        # 選項在位？
        ch = pg.evaluate("""() => {
          const ov = document.querySelector('#enc79-overlay'); if(!ov) return null;
          const btns = [...ov.querySelectorAll('.e79-row .e79-choice')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
          return btns.map(b => (b.textContent||'').trim());
        }""")
        if ch:
            # 邊粒星？由 doneToday／meta 讀
            sid = None
            dt = (st["starDay"] or {}).get("doneToday") or {}
            if dt:
                sid = sorted(dt.keys())[-1]
            pref = BEST_CHOICE.get(sid, [])
            pick = None
            for label in ch:
                if any(k in label for k in pref):
                    pick = label; break
            if pick is None:
                pick = ch[0]
            choices.append(pick)
            pg.evaluate("""(label) => {
              const ov = document.querySelector('#enc79-overlay');
              const b = [...ov.querySelectorAll('.e79-row .e79-choice')].find(x => (x.textContent||'').trim() === label);
              if (b) b.click();
            }""", pick)
            pg.wait_for_timeout(600)
            continue
        # 下一句／完結掣（.e79-row 入面）
        clicked = pg.evaluate("""() => {
          const ov = document.querySelector('#enc79-overlay'); if(!ov) return false;
          const btns = [...ov.querySelectorAll('.e79-row button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
          if(!btns.length) return false;
          btns[0].click(); return (btns[0].textContent||'').trim().slice(0,12);
        }""")
        if clicked is False:
            # 可能係主線式 modal-btns 下一句
            if advance_story(pg) in ('none', 'err'):
                pg.wait_for_timeout(500)
            else:
                pg.wait_for_timeout(450)
        else:
            pg.wait_for_timeout(500)
    st = state(pg)
    return {"lines": lines, "lineCount": len(lines), "choices": choices,
            "firstLine": first_line, "overlayGone": not st["overlay"],
            "sheetOn": st["sheetOn"], "sheetTitle": st["sheetTitle"]}

def confirm_weekly_plan(pg, timeout_s=30):
    """星期一朝早開週計劃（homeEditable）→ 撳確定行程返地圖。回 True/False＋原因。"""
    st = state(pg)
    if not st["homeEditable"]:
        return {"ok": True, "why": "not in planner"}
    ok = pg.evaluate("""() => {
      const b = document.querySelector('#btn-confirm-plan');
      if(!b) return false;
      const r = b.getBoundingClientRect();
      if(r.width<=0 || r.height<=0) return false;
      b.click(); return true;
    }""")
    if not ok:
        return {"ok": False, "why": "no confirm button"}
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        pg.wait_for_timeout(600)
        st = state(pg)
        if not st["homeEditable"] and st["pins"] > 0:
            return {"ok": True, "why": "plan confirmed, back on map"}
        if dismiss_once(pg):
            continue
        adv = advance_story(pg)
        if adv in ('none', 'err'):
            pg.wait_for_timeout(400)
    st = state(pg)
    return {"ok": False, "why": "still in planner", "homeEditable": st["homeEditable"], "pins": st["pins"]}

def click_pin(pg, loc):
    reset_travel(pg)
    pin = pg.evaluate("""(id) => {
      const el = document.querySelector('.map-pins .pin[data-loc="'+id+'"]');
      if(!el) return null; const b = el.getBoundingClientRect();
      return {cx: b.x+b.width/2, cy: b.y+b.height/2};
    }""", loc)
    if not pin:
        return {"ok": False, "why": "no pin element"}
    pg.mouse.click(pin["cx"], pin["cy"])
    return {"ok": True}

def visit(pg, loc, timeout_s=10):
    """入一次地點。回 outcome: 'encounter' | 'sheet' | 'other'，連 state。"""
    r = click_pin(pg, loc)
    if not r["ok"]:
        return {"outcome": "error", "why": r["why"]}
    t0 = time.time()
    outcome = "other"
    while time.time() - t0 < timeout_s:
        pg.wait_for_timeout(400)
        st = state(pg)
        if st["overlay"] and st["overlayLine"]:
            outcome = "encounter"
            break
        if st["sheetOn"] and st["sheetTitle"]:
            outcome = "sheet"
            break
        if dismiss_once(pg):
            continue
    st = state(pg)
    return {"outcome": outcome, "state": st}

def back_to_map(pg):
    for _ in range(8):
        if click_vis_btn(pg, "返回地圖"):
            pg.wait_for_timeout(600)
            return True
        if dismiss_once(pg):
            pg.wait_for_timeout(400)
            continue
        pg.wait_for_timeout(400)
    return False

def end_day(pg, timeout_s=120):
    """過日：自由逛逛日撳「過一日」→ 確認；有 soft 行程嘅日子撳「開始今日行程」執行行程。
    等 dayIndex+1＋返地圖。"""
    before = state(pg)["dayIndex"]
    ensure_on_map(pg, timeout_s=30)
    mode = None
    if click_vis_btn(pg, "過一日"):
        mode = "rest"
        pg.wait_for_timeout(800)
        if not click_vis_btn(pg, "確定過一日"):
            dismiss_once(pg)
    elif click_vis_btn(pg, "開始今日行程"):
        mode = "schedule"
        pg.wait_for_timeout(800)
    else:
        st = state(pg)
        return {"ok": False, "why": "no end-day/start button", "before": before,
                "sheetOn": st["sheetOn"], "sheetTitle": st["sheetTitle"], "overlay": st["overlay"]}
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        pg.wait_for_timeout(600)
        st = state(pg)
        if st["dayIndex"] == before + 1:
            # schedule 執行有機會喺 return 後再 tick 多一日：等 2 秒再讀實數，唔好假設
            pg.wait_for_timeout(2000)
            ensure_on_map(pg, timeout_s=30)
            final_day = state(pg)["dayIndex"]
            return {"ok": final_day == before + 1, "mode": mode, "before": before,
                    "after": final_day, "doubleTick": final_day != before + 1}
        # 朝早 modal／劇情／行程動畫：撳過佢
        if st["overlay"]:
            play_encounter(pg)
            continue
        if dismiss_once(pg):
            continue
        adv = advance_story(pg)
        if adv in ('none', 'err'):
            pg.wait_for_timeout(400)
    return {"ok": False, "why": "day did not advance", "mode": mode, "before": before, "after": state(pg)["dayIndex"]}

def shot(pg, name):
    p = os.path.join(SHOTS, name + ".png")
    pg.screenshot(path=p)
    return p

def main():
    from playwright.sync_api import sync_playwright
    srv = serve(ROOT)
    log = {"checks": {}, "steps": [], "pageErrors": []}
    def note(step, **kw):
        d = {"step": step, **kw}
        log["steps"].append(d)
        print("STEP " + step + " | " + json.dumps(kw, ensure_ascii=False)[:400], flush=True)
        return d
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=EXE)
            ctx = b.new_context(viewport={"width": 430, "height": 932})
            pg = ctx.new_page()
            pg.on("pageerror", lambda e: pg.evaluate("(m)=>{ (window.__errs=window.__errs||[]).push(String(m)); }", str(e)))
            try:
                goto_map(pg)
                st0 = state(pg)
                note("goto_map", dayIndex=st0["dayIndex"], starWeek=st0["starWeek"])
                log["checks"]["goto_map_day0"] = (st0["dayIndex"] == 0)
                foreshadow_done = set()

                # ---------- ① 日 0：第 1 次（應觸發） ----------
                day = 0
                pred = predict(day, foreshadow_done, {})
                note("predict_day0", presence=pred)
                enc1 = None
                tried = []
                for loc in sorted(pred.keys()):
                    v = visit(pg, loc)
                    tried.append({"loc": loc, "outcome": v["outcome"],
                                  "presence": (v.get("state") or {}).get("starDay", {}).get("presence")})
                    if v["outcome"] == "encounter":
                        enc1 = {"loc": loc, "state": v["state"]}
                        break
                    if v["outcome"] == "sheet":
                        back_to_map(pg)
                if enc1 is None:
                    note("enc1_FAIL", tried=tried, livePresence=state(pg)["starDay"])
                    log["checks"]["enc1_trigger"] = False
                else:
                    st = enc1["state"]
                    sid = sorted((st["starDay"]["doneToday"] or {}).keys())
                    sid = sid[-1] if sid else None
                    fav_before = st["stars"][sid]["fav"] if sid else None
                    note("enc1_triggered", loc=enc1["loc"], star=sid, meta=st["overlayMeta"],
                         firstLine=st["overlayLine"], starWeek=st["starWeek"], starDayTrig=st["starDay"]["triggered"])
                    shot(pg, "enc1_dialogue")
                    played = play_encounter(pg)
                    st_after = state(pg)
                    fav_after = st_after["stars"][sid]["fav"] if sid else None
                    note("enc1_played", star=sid, lines=played["lineCount"], choices=played["choices"],
                         favBefore=fav_before, favAfter=fav_after, favDelta=(fav_after - fav_before) if fav_before is not None else None,
                         starWeek=st_after["starWeek"], starDayTrig=st_after["starDay"]["triggered"],
                         sheetTitle=st_after["sheetTitle"])
                    log["checks"]["enc1_trigger"] = True
                    log["checks"]["enc1_dialogue_lines"] = played["lineCount"] >= 5
                    log["checks"]["enc1_fav_up"] = (fav_after is not None and fav_before is not None and fav_after > fav_before)
                    log["checks"]["enc1_counters"] = (st_after["starWeek"] == {"week": 1, "triggered": 1} and st_after["starDay"]["triggered"] == 1)
                    if sid:
                        foreshadow_done.add(sid)
                    shot(pg, "enc1_sheet")
                    back_to_map(pg)

                # ---------- ② 日 0：第二個有星地點（應唔觸發，每日 1 次） ----------
                st_now = state(pg)
                live_pres = (st_now["starDay"] or {}).get("presence") or {}
                # 揀有試點星在場、唔係頭先嗰粒星嘅地點（用 live presence）
                done_sid = None
                if enc1:
                    done_sid = sorted((st_now["starDay"]["doneToday"] or {}).keys())
                    done_sid = done_sid[-1] if done_sid else None
                cand2 = None
                for loc, sids in live_pres.items():
                    others = [s for s in sids if s in PILOTS and s != done_sid]
                    if others:
                        cand2 = (loc, others[0]); break
                if cand2 is None:
                    note("blocked_daily_NO_CANDIDATE", livePresence=live_pres)
                    log["checks"]["blocked_daily"] = False
                else:
                    loc2, sid2 = cand2
                    v2 = visit(pg, loc2)
                    st2 = v2["state"]
                    pres2 = ((st2["starDay"] or {}).get("presence") or {}).get(loc2, [])
                    note("blocked_daily", loc=loc2, starPresent=sid2, outcome=v2["outcome"],
                         presenceAtLoc=pres2, starWeek=st2["starWeek"], starDayTrig=st2["starDay"]["triggered"],
                         overlayLine=st2["overlayLine"])
                    shot(pg, "blocked_daily")
                    log["checks"]["blocked_daily"] = (
                        v2["outcome"] == "sheet" and sid2 in pres2
                        and st2["starWeek"] == {"week": 1, "triggered": 1}
                        and st2["starDay"]["triggered"] == 1)
                    back_to_map(pg)

                # ---------- ③ 日 1：第 2 次（應觸發，每週第 2 次） ----------
                r_end = end_day(pg)
                note("end_day_0_to_1", **r_end)
                log["checks"]["end_day_0_to_1"] = r_end["ok"] and r_end.get("after") == 1
                st_now = state(pg)
                wh = {k: True for k, v in (st_now["whispers"] or {}).items() if v}
                pred1 = predict(1, foreshadow_done, wh)
                note("predict_day1", presence=pred1, whispers=wh)
                enc2 = None
                for loc in sorted(pred1.keys()):
                    v = visit(pg, loc)
                    if v["outcome"] == "encounter":
                        enc2 = {"loc": loc, "state": v["state"]}
                        break
                    if v["outcome"] == "sheet":
                        back_to_map(pg)
                if enc2 is None:
                    # 後備：用 live presence 再試
                    live_pres = ((state(pg)["starDay"] or {}).get("presence") or {})
                    for loc, sids in live_pres.items():
                        if any(s in PILOTS for s in sids):
                            v = visit(pg, loc)
                            if v["outcome"] == "encounter":
                                enc2 = {"loc": loc, "state": v["state"]}
                                break
                            if v["outcome"] == "sheet":
                                back_to_map(pg)
                    note("enc2_retry_live", livePresence=live_pres)
                if enc2 is None:
                    note("enc2_FAIL", livePresence=state(pg)["starDay"])
                    log["checks"]["enc2_trigger"] = False
                else:
                    st = enc2["state"]
                    sid = sorted((st["starDay"]["doneToday"] or {}).keys())
                    sid = sid[-1] if sid else None
                    fav_before = st["stars"][sid]["fav"] if sid else None
                    note("enc2_triggered", loc=enc2["loc"], star=sid, firstLine=st["overlayLine"],
                         starWeek=st["starWeek"], starDayTrig=st["starDay"]["triggered"])
                    shot(pg, "enc2_dialogue")
                    played = play_encounter(pg)
                    st_after = state(pg)
                    fav_after = st_after["stars"][sid]["fav"] if sid else None
                    note("enc2_played", star=sid, lines=played["lineCount"], choices=played["choices"],
                         favBefore=fav_before, favAfter=fav_after,
                         starWeek=st_after["starWeek"], starDayTrig=st_after["starDay"]["triggered"])
                    log["checks"]["enc2_trigger"] = True
                    log["checks"]["enc2_counters"] = (st_after["starWeek"] == {"week": 1, "triggered": 2}
                                                       and st_after["starDay"]["triggered"] == 1)
                    if sid:
                        foreshadow_done.add(sid)
                    shot(pg, "enc2_sheet")
                    back_to_map(pg)

                # ---------- ④ 日 2：第三次（應唔觸發，每週 2 次） ----------
                r_end = end_day(pg)
                note("end_day_1_to_2", **r_end)
                log["checks"]["end_day_1_to_2"] = r_end["ok"] and r_end.get("after") == 2
                st_now = state(pg)
                wh = {k: True for k, v in (st_now["whispers"] or {}).items() if v}
                pred2 = predict(2, foreshadow_done, wh)
                note("predict_day2", presence=pred2, whispers=wh)
                # 搵一個有試點星在場嘅地點：先試預測，唔得就用 live presence
                blocked2 = None
                for loc in sorted(pred2.keys()):
                    v = visit(pg, loc)
                    pres = ((v["state"]["starDay"] or {}).get("presence") or {})
                    if any(s in PILOTS for s in pres.get(loc, [])):
                        blocked2 = {"loc": loc, "state": v["state"], "outcome": v["outcome"]}
                        break
                    if v["outcome"] == "sheet":
                        back_to_map(pg)
                if blocked2 is None:
                    live_pres = ((state(pg)["starDay"] or {}).get("presence") or {})
                    for loc, sids in live_pres.items():
                        if any(s in PILOTS for s in sids):
                            v = visit(pg, loc)
                            blocked2 = {"loc": loc, "state": v["state"], "outcome": v["outcome"]}
                            break
                if blocked2 is None:
                    note("blocked_weekly_NO_CANDIDATE", livePresence=state(pg)["starDay"])
                    log["checks"]["blocked_weekly"] = False
                else:
                    st3 = blocked2["state"]
                    pres3 = ((st3["starDay"] or {}).get("presence") or {}).get(blocked2["loc"], [])
                    note("blocked_weekly", loc=blocked2["loc"], outcome=blocked2["outcome"],
                         presenceAtLoc=pres3, starWeek=st3["starWeek"], starDayTrig=st3["starDay"]["triggered"])
                    shot(pg, "blocked_weekly")
                    log["checks"]["blocked_weekly"] = (
                        blocked2["outcome"] == "sheet"
                        and any(s in PILOTS for s in pres3)
                        and st3["starWeek"] == {"week": 1, "triggered": 2}
                        and st3["starDay"]["triggered"] == 0)
                    back_to_map(pg)

                # ---------- ⑤ 下一週（dayIndex ≥ 7，星期一界）：重置返（應觸發） ----------
                # 唔假設每日只進一日（schedule 執行有機會 double-tick）：推到 week 2 為止，用實際日子計 presence
                ok_days = True
                for _ in range(8):
                    cur = state(pg)["dayIndex"]
                    if cur >= 7:
                        break
                    r_end = end_day(pg)
                    note(f"end_day_{cur}_to_?", **r_end)
                    cur2 = state(pg)["dayIndex"]
                    if cur2 >= 7:
                        break
                    if not r_end["ok"]:
                        ok_days = False
                        break
                day7 = state(pg)["dayIndex"]
                log["checks"]["advance_to_day7"] = day7 >= 7
                # 星期一朝早：週計劃畫面要確定先返到地圖
                r_plan = confirm_weekly_plan(pg)
                note("confirm_weekly_plan", **r_plan)
                log["checks"]["weekly_plan_confirmed"] = r_plan["ok"]
                ensure_on_map(pg, timeout_s=30)
                st_now = state(pg)
                wh = {k: True for k, v in (st_now["whispers"] or {}).items() if v}
                pred7 = predict(day7, foreshadow_done, wh)
                note("predict_day7", presence=pred7, whispers=wh, starWeek=st_now["starWeek"])
                enc3 = None
                for loc in sorted(pred7.keys()):
                    v = visit(pg, loc)
                    if v["outcome"] == "encounter":
                        enc3 = {"loc": loc, "state": v["state"]}
                        break
                    if v["outcome"] == "sheet":
                        back_to_map(pg)
                if enc3 is None:
                    live_pres = ((state(pg)["starDay"] or {}).get("presence") or {})
                    for loc, sids in live_pres.items():
                        if any(s in PILOTS for s in sids):
                            v = visit(pg, loc)
                            if v["outcome"] == "encounter":
                                enc3 = {"loc": loc, "state": v["state"]}
                                break
                            if v["outcome"] == "sheet":
                                back_to_map(pg)
                    note("enc3_retry_live", livePresence=live_pres)
                if enc3 is None:
                    note("enc3_FAIL", livePresence=state(pg)["starDay"])
                    log["checks"]["enc3_trigger_reset"] = False
                else:
                    st = enc3["state"]
                    sid = sorted((st["starDay"]["doneToday"] or {}).keys())
                    sid = sid[-1] if sid else None
                    note("enc3_triggered", loc=enc3["loc"], star=sid, firstLine=st["overlayLine"],
                         starWeek=st["starWeek"], starDayTrig=st["starDay"]["triggered"])
                    shot(pg, "enc3_dialogue")
                    played = play_encounter(pg)
                    st_after = state(pg)
                    note("enc3_played", star=sid, lines=played["lineCount"], choices=played["choices"],
                         starWeek=st_after["starWeek"], starDayTrig=st_after["starDay"]["triggered"])
                    log["checks"]["enc3_trigger_reset"] = True
                    log["checks"]["enc3_counters"] = (st_after["starWeek"] == {"week": 2, "triggered": 1}
                                                       and st_after["starDay"]["triggered"] == 1)
                    shot(pg, "enc3_sheet")
                    back_to_map(pg)

                # ---------- 收尾 ----------
                st_end = state(pg)
                log["checks"]["no_page_errors"] = not st_end["pageErrors"]
                log["pageErrors"] = st_end["pageErrors"]
                log["finalState"] = {"dayIndex": st_end["dayIndex"], "starWeek": st_end["starWeek"],
                                     "starDay": st_end["starDay"], "stars": st_end["stars"]}
                shot(pg, "final_map")
            finally:
                ctx.close()
            b.close()
    finally:
        stop(srv)
    log["verdict"] = "PASS" if all(log["checks"].values()) else "FAIL"
    json.dump(log, open(os.path.join(HERE, "drive144.json"), "w"), ensure_ascii=False, indent=1)
    print("CHECKS " + json.dumps(log["checks"], ensure_ascii=False), flush=True)
    print("OVERALL " + log["verdict"], flush=True)
    sys.exit(0 if log["verdict"] == "PASS" else 1)

if __name__ == "__main__":
    main()
