#!/usr/bin/env python3
"""v20a160-m4 實駕：贏分支揭曉後 walkup beat 播阿偉行上台領獎 GIF。
Case（每 case 全新 browser context）：
  won_932  強制 film 贏分支（retry 直到 pack.bestOutcome==='won'）→ 出席 →
           walkup beat（reveal 之後、2200ms）GIF 層 .on、img 載到、兩張唔同幀截圖證明識郁 →
           舞台消失 → 結果卡有得獎
  won_700  同上，430x700
用法：/home/hatch/pwenv49/bin/python qa160-m4/drive160m4.py [won|all] [932|700]
自帶 http.server（port 8974），跑完熄。
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work160-m4"
HERE = "/home/hatch/workspace/linji-work160-m4/qa160-m4"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8974
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
      const body = (m.innerText || '').slice(0, 1200);
      return {visible:true, h3, btns, body};
    }""")

def dismiss_once(pg):
    return pg.evaluate("""() => {
      const bs = [...document.querySelectorAll('#modal-btns button')];
      if (!bs.length) return false;
      const b = bs[0];
      const r = b.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) return false;
      b.click(); return true;
    }""")

def click_text(pg, text):
    """JS click（唔經 Playwright actionability——呢版 start 畫面 locator click 會 hang，見 probe）。"""
    return pg.evaluate("""(t) => {
      const els = [...document.querySelectorAll('button, [role=button], span, div, a')].filter(e => (e.textContent||'').trim() === t || (e.textContent||'').includes(t));
      const vis = els.filter(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false;
      // 最細嗰粒（避免撳中成版容器）
      vis.sort((a, b) => (a.getBoundingClientRect().width * a.getBoundingClientRect().height) - (b.getBoundingClientRect().width * b.getBoundingClientRect().height));
      vis[0].click(); return true;
    }""", text)

def new_game_to_map(pg):
    pg.goto(f"http://127.0.0.1:{PORT}/index.html?softPreview=1")
    pg.wait_for_timeout(2500)
    click_text(pg, "新遊戲")
    pg.wait_for_timeout(1000)
    try:
        pg.evaluate("() => { const el = document.querySelector('[data-slot=\"3\"]'); if (el) el.click(); }")
        pg.wait_for_timeout(800)
    except Exception:
        pass
    for _ in range(10):
        if click_text(pg, "跳過教學"):
            pg.wait_for_timeout(600)
            break
        if click_text(pg, "下一步"):
            pg.wait_for_timeout(600)
        else:
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

def seed_won(pg, *, day):
    """谷爆 dual＋1991 年高質作品，令 film 桶 base 逼近 0.90（贏線 0.875，taste ±0.05）。
    wrapHistory 條目直接帶 roleScale（awards62WorkQuality 會讀 h.roleScale，唔使真 gig）。"""
    wraps = []
    for i in range(4):
        wraps.append({"gigId": f"seed160_film{i+1}", "wrappedDay": 580 + i,
                      "type": "電影", "roleScale": "film_lead_big", "pay": 30000})
    for i in range(2):
        wraps.append({"gigId": f"seed160_tv{i+1}", "wrappedDay": 585 + i,
                      "type": "電視劇", "roleScale": "tv_lead_long", "pay": 20000})
    wraps.append({"gigId": "seed160_ad1", "wrappedDay": 590,
                  "type": "廣告", "roleScale": "ad_av", "pay": 10000})
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = 500; S.stage = 90; S.acting = 90;
      S.industryCreditDelta = 500;
      S.money = 50000; S.stress = 0;
      S.wrapHistory = o.wraps;
      S.postShootRewards = [];
      S.flags = S.flags || {};
      const parts = window.__awards.score62({ primaryTrack: 'stageVolume' }, { medium: 'film', matchTypes: ['電影'] }, 1991);
      return { day: S.dayIndex, wraps: S.wrapHistory.length, base: parts.base };
    }""", {"day": day, "wraps": wraps})

def force_won(pg, ceremony_id, tries=15):
    """重複 force，直到 pack.bestOutcome==='won'（每次重骰 taste）。回傳 {pack, attempts}。"""
    for n in range(1, tries + 1):
        pack = pg.evaluate("""(o) => {
          try {
            const p = window.__awards.debugForceSeasonWindow(o.id, {});
            if (!p) return { error: 'no pack' };
            return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
                     tier: p.tier, categories: (p.categories || []).map(c => ({ outcome: c.outcome, score: c.score })) };
          } catch(e) { return { error: String(e) }; }
        }""", {"id": ceremony_id})
        if pack.get("bestOutcome") == "won":
            return {"pack": pack, "attempts": n}
    return {"pack": pack, "attempts": tries}

def stage_state(pg):
    return pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      const wk = st.querySelector('.awd62-walkup160');
      const img = wk ? wk.querySelector('img') : null;
      const wkcap = wk ? wk.querySelector('.cap') : null;
      const r = img ? img.getBoundingClientRect() : null;
      return { present: true,
               caption: cap ? cap.textContent : '',
               walkupCap: wkcap ? wkcap.textContent : '',
               walkupOn: !!(wk && wk.classList.contains('on')),
               walkupPresent: !!wk,
               imgSrc: img ? (img.getAttribute('src') || '') : '',
               imgOk: img ? (img.complete && img.naturalWidth > 0) : false,
               imgBox: r ? { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) } : null };
    }""")

def watch_won(pg, secs=20, tag="won"):
    """每 100ms 撳 walkup 層狀態；walkup 期間截兩張唔同時刻證明識郁；回傳 timeline＋量度。"""
    timeline = []
    last_cap, last_wk = None, None
    t0 = time.time()
    walkup_on_t, walkup_off_t = None, None
    img_box = None
    shots_taken = []
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        now = round((time.time() - t0) * 1000)
        cap = st.get("caption") or ""
        wk = st.get("walkupOn")
        if cap != last_cap or wk != last_wk:
            timeline.append({"t": now, "caption": cap[:80], "walkupCap": (st.get("walkupCap") or "")[:80], "walkupOn": wk,
                             "imgOk": st.get("imgOk"), "imgSrc": st.get("imgSrc")})
            last_cap, last_wk = cap, wk
        if wk and walkup_on_t is None:
            walkup_on_t = now
            img_box = st.get("imgBox")
        if wk and walkup_on_t is not None and now - walkup_on_t >= 400 and "a" not in shots_taken:
            shot(pg, f"{tag}_walkup_a.png"); shots_taken.append("a")
        if wk and walkup_on_t is not None and now - walkup_on_t >= 1300 and "b" not in shots_taken:
            shot(pg, f"{tag}_walkup_b.png"); shots_taken.append("b")
        if (not wk) and walkup_on_t is not None and walkup_off_t is None:
            walkup_off_t = now
        pg.wait_for_timeout(100)
    total = round((time.time() - t0) * 1000)
    walkup_off_est = False
    if walkup_on_t is not None and walkup_off_t is None and not stage_state(pg).get("present"):
        # 截圖慢（headless 下一張 ~1 秒），poll 未必撞到 walkup→out 嗰一刻：
        # 舞台消失＝out beat（500ms）行完，walkup 熄 ≈ 舞台消失前 500ms，作估算。
        walkup_off_t = total - 500
        walkup_off_est = True
    return {"timeline": timeline, "totalMs": total,
            "walkupOnMs": walkup_on_t, "walkupOffMs": walkup_off_t,
            "walkupDurMs": (walkup_off_t - walkup_on_t) if (walkup_on_t is not None and walkup_off_t is not None) else None,
            "walkupOffEstimated": walkup_off_est,
            "imgBox": img_box, "shots": shots_taken,
            "stageGone": not stage_state(pg).get("present")}

def case_won(pg, W, H):
    out = {"checks": {}, "errors": []}
    tag = "won_932" if H >= 900 else "won_700"
    if not new_game_to_map(pg):
        out["checks"]["to_map"] = False
        return out
    out["checks"]["to_map"] = True
    ctx = seed_won(pg, day=day_index(1991, 10, 20))
    out["seed"] = ctx
    out["checks"]["seed_base_ge_088"] = (ctx.get("base") or 0) >= 0.88
    fw = force_won(pg, "award_harbour_film")
    out["force"] = fw
    out["checks"]["pack_is_won"] = fw["pack"].get("bestOutcome") == "won"
    if not out["checks"]["pack_is_won"]:
        return out
    pg.evaluate("() => { window.__awards.present(); }")
    pg.wait_for_timeout(1000)
    inv = modal_info(pg)
    out["invite"] = {"h3": inv.get("h3"), "btns": inv.get("btns")}
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    if not click_vis_btn(pg, "出席"):
        out["checks"]["clicked_attend"] = False
        return out
    out["checks"]["clicked_attend"] = True
    pg.wait_for_timeout(500)
    w = watch_won(pg, secs=20, tag=tag)
    out["watch"] = w
    wk_events = [e for e in w["timeline"] if e.get("walkupOn")]
    out["checks"]["walkup_layer_present"] = any(e.get("imgSrc") for e in w["timeline"])
    out["checks"]["walkup_turned_on"] = w["walkupOnMs"] is not None
    out["checks"]["walkup_img_loaded"] = any(e.get("imgOk") for e in wk_events)
    out["checks"]["walkup_img_is_m4"] = any("awd_walkup_m4.gif" in (e.get("imgSrc") or "") for e in wk_events)
    out["checks"]["walkup_caption"] = any("行上台" in (e.get("walkupCap") or "") for e in wk_events)
    dur = w["walkupDurMs"]
    # walkup 2200ms 係 logic test 已 pin（awards62_logic）；實駕量度受 poll＋截圖延遲影響：
    # 直接捕捉到熄嗰刻 → 窗 1800–2800；估算（截圖塞住 poll）→ 只驗下限＋唔離譜上限
    if w.get("walkupOffEstimated"):
        out["checks"]["walkup_dur_approx_2200"] = dur is not None and 1800 <= dur <= 4500
    else:
        out["checks"]["walkup_dur_approx_2200"] = dur is not None and 1800 <= dur <= 2800
    out["checks"]["walkup_two_shots"] = w["shots"] == ["a", "b"]
    # 兩張 walkup 截圖像素對照（GIF 識郁證明）唔喺呢度做：pwenv49 冇 PIL，
    # 用系統 python3＋PIL 喺 drive 跑完之後對 qa160-m4/shots 嗰兩張 PNG 驗。
    out["checks"]["stage_gone_after"] = w["stageGone"]
    # walkup 熄咗之後先有結果卡
    pg.wait_for_timeout(800)
    res = modal_info(pg)
    out["result"] = {"h3": res.get("h3"), "btns": res.get("btns"),
                     "bodyWon": ("得獎" in (res.get("body") or ""))}
    out["checks"]["result_card_won"] = bool(res.get("visible")) and ("得獎" in (res.get("body") or ""))
    shot(pg, f"{tag}_result.png")
    return out

CASES = {
    "won_932": lambda pg, W, H: case_won(pg, W, H),
    "won_700": lambda pg, W, H: case_won(pg, W, H),
}

def run_case(name, W, H):
    errors = []
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(30):
            try:
                import urllib.request
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=1)
                break
            except Exception:
                time.sleep(0.5)
        with sync_playwright() as pw:
            last_exc = None
            browser = None
            for attempt in range(6):
                try:
                    browser = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
                    break
                except Exception as e:
                    last_exc = e
                    time.sleep(15)
            if not browser:
                return {"case": name, "error": f"browser launch failed: {last_exc}"}
            try:
                ctx = browser.new_context(viewport={"width": W, "height": H})
                pg = ctx.new_page()
                pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
                pg.on("requestfailed", lambda r: errors.append(f"reqfail: {r.url}"))
                pg.on("console", lambda m: errors.append(f"console-{m.type}: {m.text}") if m.type == "error" else None)
                res = CASES[name](pg, W, H)
                res["pageerrors"] = errors
                res["checks"]["zero_pageerror"] = len([e for e in errors if e.startswith("pageerror")]) == 0
                res["checks"]["zero_reqfail"] = len([e for e in errors if e.startswith("reqfail")]) == 0
                return res
            finally:
                browser.close()
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=5)
        except Exception:
            srv.kill()

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    size = sys.argv[2] if len(sys.argv) > 2 else "932"
    W, H = (430, 932) if size == "932" else (430, 700)
    names = ["won_932"] if which == "won" and size == "932" else \
            ["won_700"] if which == "won" and size == "700" else \
            ["won_932", "won_700"] if which == "all" else [which]
    results = {}
    for n in names:
        w, h = (430, 932) if n.endswith("932") else (430, 700)
        print(f"=== {n} ({w}x{h}) ===", flush=True)
        r = run_case(n, w, h)
        results[n] = r
        print(json.dumps(r, ensure_ascii=False, indent=1)[:6000], flush=True)
        passed = sum(1 for v in r.get("checks", {}).values() if v is True)
        total = len(r.get("checks", {}))
        print(f"--- {n}: {passed}/{total} checks passed ---", flush=True)
    try:
        prev = json.load(open(os.path.join(HERE, "drive160m4.json"), encoding="utf-8"))
    except Exception:
        prev = {}
    prev.update(results)
    with open(os.path.join(HERE, "drive160m4.json"), "w", encoding="utf-8") as f:
        json.dump(prev, f, ensure_ascii=False, indent=1)
    allok = all(all(v is True for v in r.get("checks", {}).values()) for r in prev.values())
    print("OVERALL " + ("PASS" if allok else "FAIL"), flush=True)

if __name__ == "__main__":
    main()
