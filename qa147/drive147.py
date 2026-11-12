#!/usr/bin/env python3
"""v20a147 實駕：頒獎禮整改——D1 旁聽報紙（v136 已做，呢度實駕證實）、D2 安慰場面＋
gallery 宣佈弧做長做實、對手加權（引擎層，見 tests/test_awards63_logic.js §147；實駕唔使再驗分佈）。
Cases（每 case 全新 browser context，免狀態污染）：
  gallery_932   ① 強制 film gallery → 出席 → 全程計時（6 beats，約 9.6s）→ 結果卡 → 翌日晨報有 award_gallery 篇（headline/dek 唔寫入圍／得獎、fameDelta 1）
  gallery_700   ② 同上，430×700（短屏字幕唔被切）
  nominated_932 ③ 強制 film nominated → 出席 → comfort beat（reveal 之後、out 之前）→ 結果卡有 .psr-comfort147 安慰行
  skip_932      ④ 強制 film gallery → 出席 → 1 秒後撳「跳過 ⏩」→ 即入結果卡（跳過掣繼續 work）
  declined_932  ⑤ 強制 film gallery → 推辭 → 翌日晨報有 award_declined 篇（fameDelta 0、唔寫阿偉）
用法：/home/hatch/pwenv49/bin/python qa147/drive147.py [case|all] [932|700]
I/O 防禦：截圖／JSON 寫檔失敗（沙箱寫入攔截）唔會中斷 case，結果照印 stdout。
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work147"
HERE = "/home/hatch/workspace/linji-work147/qa147"
SHOTS = os.path.join(HERE, "shots")
try:
    os.makedirs(SHOTS, exist_ok=True)
except Exception:
    pass
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8971
SAVE_KEY = "starVolunteer_map_v19w"

def shot(pg, name):
    try:
        pg.screenshot(path=os.path.join(SHOTS, name))
        return True
    except Exception:
        return False

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
      const choices = [...document.querySelectorAll('#modal .sp-choice')].map(b => (b.textContent||'').trim()).filter(Boolean);
      const comfort = document.querySelector('#modal .psr-comfort147');
      const body = (m.innerText || '').slice(0, 1200);
      return {visible:true, h3, btns, choices, body,
              comfort: comfort ? comfort.textContent : null};
    }""")

def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            try:
                btn.click(timeout=1000)
            except Exception:
                pass
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

def seed(pg, *, day, fame=40, stage=10, acting=10, credit_delta=0, money=5000, stress=0):
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = o.fame; S.stage = o.stage; S.acting = o.acting;
      S.industryCreditDelta = o.credit_delta;
      S.money = o.money; S.stress = o.stress;
      S.flags = S.flags || {};
      if (typeof BehaviorGate !== "undefined" && BehaviorGate.readCtx) {
        const ctx = BehaviorGate.readCtx({});
        return { day: S.dayIndex, week: ctx.week, year: ctx.year, season: ctx.season, dual: ctx.dual };
      }
      return { day: S.dayIndex };
    }""", {"day": day, "fame": fame, "stage": stage, "acting": acting,
            "credit_delta": credit_delta, "money": money, "stress": stress})

def map_ready(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }") \
        and (not modal_info(pg).get("visible")) and (vis_btn(pg, "過一日") or vis_btn(pg, "開始今日行程"))

def home_on(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")

def pump_to_map(pg, secs=45, stop_on_invite=False):
    seen = []
    t0 = time.time()
    while time.time() - t0 < secs:
        mi = modal_info(pg)
        if mi.get("visible"):
            if stop_on_invite and any("出席" in b for b in mi.get("btns") or []):
                seen.append({"h3": mi.get("h3", ""), "btns": mi.get("btns", []), "body": (mi.get("body", "") or "")[:400]})
                return {"onMap": False, "seen": seen, "invite": mi}
            seen.append({"h3": mi.get("h3", ""), "btns": mi.get("btns", []), "body": (mi.get("body", "") or "")[:400]})
            if not dismiss_once(pg):
                if not click_vis_btn(pg, "返回地圖"):
                    pg.wait_for_timeout(400)
        elif home_on(pg) and vis_btn(pg, "確定本週行程"):
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
      day: S.dayIndex,
      awardsFlags: S.awardsFlags || {},
      pendingAwardPack: S.pendingAwardPack ? { ceremonyId: S.pendingAwardPack.ceremonyId, year: S.pendingAwardPack.year, tier: S.pendingAwardPack.tier, bestOutcome: S.pendingAwardPack.bestOutcome } : null,
      newspaperQueue: (S.newspaperQueue || []).map(q => ({ eventKey: q.eventKey, templateEventKey: q.templateEventKey || null, fameDelta: q.fameDelta, headline: q.headline || '', dek: q.dek || '' })),
      clippings: (S.newspaperClippings || []).flatMap(c => (c && c.eventKeys) || []),
      clipItems: (S.newspaperClippings || []).flatMap(c => (c && c.items) || []).map(i => ({ eventKey: i.eventKey, templateEventKey: i.templateEventKey || null, fameDelta: i.fameDelta, headline: i.headline || '', dek: i.dek || '' })),
    })""")

def force_award(pg, ceremony_id, tier):
    """強制排一場指定 tier 嘅典禮＋彈請柬。回傳 {pack, invite}。"""
    pack = pg.evaluate("""(o) => {
      try {
        const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
        if (!p) return { error: 'no pack' };
        window.__awards.present();
        return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
                 tier: p.tier, categories: (p.categories || []).map(c => ({ outcome: c.outcome, label: c.label })) };
      } catch(e) { return { error: String(e) }; }
    }""", {"id": ceremony_id, "tier": tier})
    pg.wait_for_timeout(1000)
    inv = modal_info(pg)
    return {"pack": pack, "invite": inv}

def stage_state(pg):
    return pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      const skip = st.querySelector('.awd62-skip');
      const r = cap ? cap.getBoundingClientRect() : null;
      return { present: true,
               caption: cap ? cap.textContent : '',
               skipVisible: !!skip && skip.getBoundingClientRect().width > 0,
               captionBox: r ? { top: Math.round(r.top), bottom: Math.round(r.bottom), h: Math.round(r.height) } : null,
               vh: window.innerHeight };
    }""")

def watch_ceremony(pg, secs=22, shot_at=None):
    """每 90ms 撳 caption，記錄每次轉句嘅時間。shot_at：caption 包含某字就截圖（例：唱名）。"""
    timeline = []
    last = None
    t0 = time.time()
    took = set()
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        cap = st.get("caption") or ""
        now = round((time.time() - t0) * 1000)
        if cap != last:
            timeline.append({"t": now, "caption": cap[:160]})
            last = cap
            if shot_at:
                for key, name in shot_at:
                    if key in cap and name not in took:
                        shot(pg, name)
                        took.add(name)
        pg.wait_for_timeout(90)
    total = round((time.time() - t0) * 1000)
    return {"timeline": timeline, "totalMs": total, "stageGone": not stage_state(pg).get("present")}

def beat_durations(timeline):
    """由 caption 轉換時間推每 beat 時長（最後一段計到 total，喺 watch 回傳嗰度補）。"""
    out = []
    for i, e in enumerate(timeline):
        nxt = timeline[i + 1]["t"] if i + 1 < len(timeline) else None
        out.append({"caption": e["caption"][:60], "startMs": e["t"], "durMs": (nxt - e["t"]) if nxt is not None else None})
    return out

def paper_for_ceremony(st, ceremony_id, year):
    key = f"award:{year}:{ceremony_id}"
    q = [i for i in (st.get("newspaperQueue") or []) if i.get("eventKey") == key]
    c = [i for i in (st.get("clipItems") or []) if i.get("eventKey") == key]
    # 遊戲剪報本體係 S.newspaperClippings[]（每項帶 eventKeys 字串陣列，無 .items），
    # s_state 嘅 clipItems 永遠係空——key 入咗 clippings 就當已剪存（D4 重做實駕修正）。
    if key in (st.get("clippings") or []):
        c = c + [{"eventKey": key, "templateEventKey": None, "fameDelta": None, "headline": "", "dek": ""}]
    return {"key": key, "queued": q, "clipped": c}

# ---------------- cases ----------------
FILM = "award_harbour_film"

def case_gallery(pg, W, H):
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, FILM, "gallery")
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "invite": inv, "checks": {}}
    out["checks"]["pack_is_gallery"] = pack.get("bestOutcome") == "gallery"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_attend"] = any("出席" in b for b in inv.get("btns") or [])
    out["checks"]["invite_has_decline"] = any("推辭" in b for b in inv.get("btns") or [])
    out["checks"]["invite_no_later"] = not any("稍後" in b for b in inv.get("btns") or [])
    shot(pg, f"gallery_invite_{W}x{H}.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    st0 = stage_state(pg)
    out["stage_at_start"] = st0
    out["checks"]["stage_appears"] = bool(st0.get("present"))
    out["checks"]["skip_visible"] = bool(st0.get("skipVisible"))
    w = watch_ceremony(pg, 22, shot_at=[("入圍", f"gallery_names_{W}x{H}.png"), ("得獎者", f"gallery_reveal_{W}x{H}.png")])
    out["watch"] = w
    beats = beat_durations(w["timeline"])
    out["beats"] = beats
    caps = " || ".join(e["caption"] for e in w["timeline"])
    out["checks"]["six_captions_seen"] = len(w["timeline"]) >= 6
    out["checks"]["names_beat_lists_fellows_not_awei"] = ("入圍" in caps) and ("阿偉" not in caps)
    out["checks"]["reveal_names_winner"] = ("得獎者" in caps) or ("得獎" in caps)
    out["checks"]["gallery_copy_no_false_result"] = ("阿偉" not in caps) or ("入圍" not in caps and "得獎" not in caps)
    out["checks"]["total_about_9_6s"] = 8000 <= w["totalMs"] <= 11500
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    out["checks"]["result_card_no_win_claim"] = ("得獎" not in (res.get("body") or "")) or ("阿偉" not in (res.get("body") or ""))
    shot(pg, f"gallery_result_{W}x{H}.png")
    dismiss_once(pg)
    pump_to_map(pg, 30)
    save_slot1(pg)
    # 頒獎報喺典禮完結嗰刻入 queue（publishDay=翌日），advance 之前 snapshot 先攞到
    # 帶 templateEventKey／fameDelta 嘅原物件；advance 之後 queue 已經排走，得返 clippings key。
    st_pre = s_state(pg)
    paper_pre = paper_for_ceremony(st_pre, FILM, 1991)
    adv = advance_day(pg)
    out["next_day"] = adv
    st = s_state(pg)
    out["state_next_day"] = st
    paper = paper_for_ceremony(st, FILM, 1991)
    out["paper"] = paper
    out["paper_pre"] = paper_pre
    gal = (paper_pre["queued"] + paper["queued"] + paper["clipped"])
    out["checks"]["gallery_paper_queued_or_clipped"] = len(gal) > 0
    if gal:
        g0 = gal[0]
        out["checks"]["gallery_paper_template"] = g0.get("templateEventKey") == "award_gallery.film"
        out["checks"]["gallery_paper_fameDelta_1"] = g0.get("fameDelta") == 1
        txt = (g0.get("headline") or "") + (g0.get("dek") or "")
        out["checks"]["gallery_paper_no_nom_win_words"] = not any(k in txt for k in ["入圍", "提名", "得獎", "奪獎"])
        out["gallery_paper_text"] = txt
    shot(pg, f"gallery_nextday_{W}x{H}.png")
    return out

def case_nominated(pg, W, H):
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=120, stage=60, acting=60, credit_delta=80)
    fa = force_award(pg, FILM, "nominee")
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "invite": inv, "checks": {}}
    out["checks"]["pack_is_nominated"] = pack.get("bestOutcome") == "nominated"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    w = watch_ceremony(pg, 22, shot_at=[("拍拍你膊頭", f"nominated_comfort_{W}x{H}.png")])
    out["watch"] = w
    beats = beat_durations(w["timeline"])
    out["beats"] = beats
    caps = [e["caption"] for e in w["timeline"]]
    joined = " || ".join(caps)
    ci = next((i for i, c in enumerate(caps) if "拍拍你膊頭" in c), -1)
    ri = next((i for i, c in enumerate(caps) if "得獎者" in c or "得獎" in c), -1)
    out["checks"]["comfort_beat_seen"] = ci >= 0
    out["checks"]["comfort_after_reveal"] = ci > ri >= 0
    out["checks"]["comfort_has_ho_and_awei"] = ("何生" in joined) and ("阿偉" in joined)
    out["checks"]["comfort_no_win_claim"] = "贏" not in (caps[ci] if ci >= 0 else "")
    out["checks"]["total_about_12s"] = 10000 <= w["totalMs"] <= 14000
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    out["checks"]["result_card_comfort_line"] = (res.get("comfort") or "") == "何生：「差少少啫，唔緊要，下年再嚟過。」"
    out["checks"]["result_card_no_win_claim"] = "得獎" not in (res.get("body") or "") or "阿偉" not in (res.get("body") or "")
    shot(pg, f"nominated_result_{W}x{H}.png")
    return out

def case_skip(pg, W, H):
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, FILM, "gallery")
    out = {"ctx": ctx, "pack": fa["pack"], "checks": {}}
    out["checks"]["invite_shown"] = bool(fa["invite"].get("visible"))
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(1000)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    t0 = time.time()
    clicked = pg.evaluate("""() => { const b = document.querySelector('.awd62-skip'); if (!b) return false; b.click(); return true; }""")
    out["checks"]["skip_clicked"] = bool(clicked)
    pg.wait_for_timeout(800)
    gone_ms = round((time.time() - t0) * 1000)
    out["skip_to_gone_ms"] = gone_ms
    out["checks"]["stage_gone_fast"] = not stage_state(pg).get("present")
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown_after_skip"] = bool(res.get("visible"))
    shot(pg, f"skip_result_{W}x{H}.png")
    return out

def case_declined(pg, W, H):
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, FILM, "gallery")
    out = {"ctx": ctx, "pack": fa["pack"], "checks": {}}
    inv = fa["invite"]
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_decline"] = any("推辭" in b for b in inv.get("btns") or [])
    shot(pg, f"declined_invite_{W}x{H}.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "推辭")
    pg.wait_for_timeout(1200)
    pump_to_map(pg, 30)
    st = s_state(pg)
    out["after_decline"] = st
    out["checks"]["flag_skipped"] = (st.get("awardsFlags") or {}).get("1991/" + FILM) == "skipped"
    out["checks"]["pending_cleared"] = st.get("pendingAwardPack") is None
    out["checks"]["paper_queued_next_day"] = any((q.get("eventKey") == "award:1991:" + FILM) for q in (st.get("newspaperQueue") or []))
    adv = advance_day(pg)
    out["next_day"] = adv
    st2 = s_state(pg)
    out["state_next_day"] = st2
    paper = paper_for_ceremony(st2, FILM, 1991)
    out["paper"] = paper
    paper_pre = paper_for_ceremony(st, FILM, 1991)
    out["paper_pre"] = paper_pre
    dec = (paper_pre["queued"] + paper["queued"] + paper["clipped"])
    out["checks"]["declined_paper_present"] = len(dec) > 0
    if dec:
        d0 = dec[0]
        out["checks"]["declined_paper_template"] = d0.get("templateEventKey") == "award_declined.film"
        out["checks"]["declined_paper_fameDelta_0"] = d0.get("fameDelta") == 0
        txt = (d0.get("headline") or "") + (d0.get("dek") or "")
        out["checks"]["declined_paper_no_awei"] = "阿偉" not in txt
        out["declined_paper_text"] = txt
    shot(pg, f"declined_nextday_{W}x{H}.png")
    return out

CASES = {
    "gallery_932": lambda pg, W, H: case_gallery(pg, W, H),
    "gallery_700": lambda pg, W, H: case_gallery(pg, W, H),
    "nominated_932": lambda pg, W, H: case_nominated(pg, W, H),
    "skip_932": lambda pg, W, H: case_skip(pg, W, H),
    "declined_932": lambda pg, W, H: case_declined(pg, W, H),
}

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    h_arg = sys.argv[2] if len(sys.argv) > 2 else "932"
    sel = list(CASES.keys()) if arg == "all" else [arg]
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    results = {}
    remaining = list(sel)
    for attempt in range(6):
        if not remaining:
            break
        try:
            with sync_playwright() as p:
                b = p.chromium.launch(executable_path=EXE)
                try:
                    _run_with_browser(b, remaining, h_arg, results)
                finally:
                    try:
                        b.close()
                    except Exception:
                        pass
        except Exception as e:
            print(f"  browser attempt {attempt + 1} failed: {e!r}", flush=True)
            time.sleep(15)
        remaining = [n for n in sel if results.get(n, {}).get("verdict") != "PASS"]
        if remaining:
            print(f"  remaining after attempt {attempt + 1}: {remaining}", flush=True)
            time.sleep(10)
    try:
        srv.terminate()
    except Exception:
        pass
    try:
        json.dump(results, open(os.path.join(HERE, "drive147.json"), "w"), ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"NOTE drive147.json write failed: {e!r}", flush=True)
    print("RESULTS_JSON_BEGIN")
    print(json.dumps(results, ensure_ascii=False))
    print("RESULTS_JSON_END")
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    print(f"OVERALL {n_pass}/{len(results)} PASS")
    sys.exit(0 if n_pass == len(results) else 1)

def _run_with_browser(b, sel, h_arg, results):
    for name in sel:
        H = 700 if name == "gallery_700" else int(h_arg)
        key = name
        print(f"== {key} ==", flush=True)
        errs = []
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            if not new_game_to_map(pg):
                results[key] = {"verdict": "ERROR", "checks": {}, "note": "new game did not reach map"}
                print("  ERROR: no map", flush=True)
                continue
            r = CASES[name](pg, 430, H)
            r["pageerrors"] = errs[:8]
            checks = r.get("checks", {})
            r["verdict"] = "PASS" if checks and all(checks.values()) else "FAIL"
            results[key] = r
            print(f"  {r['verdict']} {json.dumps(checks, ensure_ascii=False)}", flush=True)
            if errs:
                print(f"    pageerrors: {errs[:3]}", flush=True)
        except Exception as e:
            results[key] = {"verdict": "ERROR", "checks": {}, "error": repr(e)}
            print(f"  ERROR {e!r}", flush=True)
            try:
                shot(pg, f"err_{key}.png")
            except Exception:
                pass
        finally:
            ctx.close()

if __name__ == "__main__":
    main()
