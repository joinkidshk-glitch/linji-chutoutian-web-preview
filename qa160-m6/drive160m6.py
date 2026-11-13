#!/usr/bin/env python3
"""v20a160 M6 實駕：燕尾服阿偉只喺典禮贏分支上台。
Cases（每 case 全新 browser context）：
  won_932       ① 強檔 seed（fame 200／credit 210／4 部電影 q0.78 有海報＋2 部電視 q1.0）→
                強制 film nominee、重骰到 bestOutcome==="won" → 出席 → reveal＋glamour 期間
                drawImage 監測到 awei_tuxedo 繪製（64x64）＋截圖目視燕尾服＋結果卡講得獎
  nominated_932 ② 弱檔 seed（drive147 同款）→ 強制 nominee → 落選＋comfort beat → 全程
                零 awei_tuxedo 繪製（輸分支唔著燕尾服，對照組）
用法：/home/hatch/pwenv49/bin/python qa160-m6/drive160m6.py [case|all] [932|700]
I/O 防禦：截圖／JSON 寫檔失敗唔會中斷 case，結果照印 stdout。
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work160-m6"
HERE = "/home/hatch/workspace/linji-work160-m6/qa160-m6"
SHOTS = os.path.join(HERE, "shots")
try:
    os.makedirs(SHOTS, exist_ok=True)
except Exception:
    pass
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8972
SAVE_KEY = "starVolunteer_map_v19w"

def ensure_server(srv):
    """探測 http.server 仲生唔生；死咗就重開（實駕見過 server 喺 case 之間無故死咗，之後全數 ERR_CONNECTION_REFUSED）。"""
    import urllib.request
    for _ in range(3):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=3) as resp:
                if resp.status == 200:
                    return srv
        except Exception:
            pass
        try:
            if srv is not None:
                srv.terminate()
        except Exception:
            pass
        srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                               cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5)
    return srv

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
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=15000)
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

def seed(pg, *, day, fame=40, stage=10, acting=10, credit_delta=0, money=5000, stress=0, wraps=None):
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.story.gigCount = 6;
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = o.fame; S.stage = o.stage; S.acting = o.acting;
      S.industryCreditDelta = o.credit_delta;
      S.money = o.money; S.stress = o.stress;
      S.flags = S.flags || {};
      S.wrapHistory = o.wraps || [];
      S.postShootRewards = [];
      if (typeof BehaviorGate !== "undefined" && BehaviorGate.readCtx) {
        const ctx = BehaviorGate.readCtx({});
        return { day: S.dayIndex, week: ctx.week, year: ctx.year, season: ctx.season, dual: ctx.dual };
      }
      return { day: S.dayIndex };
    }""", {"day": day, "fame": fame, "stage": stage, "acting": acting,
            "credit_delta": credit_delta, "money": money, "stress": stress,
            "wraps": wraps or []})

def won_wraps():
    d = day_index
    # 4 部電影全部用有海報嘅 gig_1988_film_lion_autumn_high（gig roleScale film_support_main -> q 0.78，
    # poster59Path 回 assets/posters/...webp，repGigId63 係佢先有 glamour beat；wsum 0.78*2.1=1.64 -> worksScore 1.0）
    # ＋2 部電視假 lead（q 1.0，跨媒介借分＋repPower 0.08）-> base 0.40+0.42+0.08=0.90，taste +-0.05，重骰贏面高。
    film = [{"gigId": "gig_1988_film_lion_autumn_high", "type": "電影", "pay": 30000,
             "wrappedDay": d(1991, m, 15), "year": 1991} for m in (3, 4, 6, 8)]
    tv = [{"gigId": "fake_tv_lead_%d" % i, "type": "電視劇", "roleScale": "tv_lead_long",
           "pay": 30000, "wrappedDay": d(1991, m, 15), "year": 1991} for i, m in enumerate((5, 7))]
    return film + tv

def map_ready(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }") \
        and (not modal_info(pg).get("visible")) and (vis_btn(pg, "過一日") or vis_btn(pg, "開始今日行程"))

def home_on(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")

def pump_to_map(pg, secs=45):
    t0 = time.time()
    while time.time() - t0 < secs:
        mi = modal_info(pg)
        if mi.get("visible"):
            if not dismiss_once(pg):
                if not click_vis_btn(pg, "返回地圖"):
                    pg.wait_for_timeout(400)
        elif home_on(pg) and vis_btn(pg, "確定本週行程"):
            click_vis_btn(pg, "確定本週行程")
            pg.wait_for_timeout(800)
        elif map_ready(pg):
            return {"onMap": True}
        else:
            pg.wait_for_timeout(400)
        pg.wait_for_timeout(300)
    return {"onMap": map_ready(pg)}

def install_draw_patch(pg):
    """監測 canvas drawImage：只記低 src 含 awei_tuxedo 嘅呼叫（來源＋落點＋尺寸）。"""
    return pg.evaluate("""() => {
      window.__tuxDraws = [];
      if (!window.__tuxPatched) {
        window.__tuxPatched = true;
        const _di = CanvasRenderingContext2D.prototype.drawImage;
        CanvasRenderingContext2D.prototype.drawImage = function(img, ...rest) {
          try {
            const s = img && img.src ? String(img.src) : '';
            if (s.indexOf('awei_tuxedo') >= 0) {
              window.__tuxDraws.push({src: s.slice(-45), dx: rest[0], dy: rest[1], dw: rest[2], dh: rest[3]});
            }
          } catch(e) {}
          return _di.apply(this, [img, ...rest]);
        };
      }
      return { patched: true };
    }""")

def tux_draws(pg):
    return pg.evaluate("() => (window.__tuxDraws || [])")

def force_award(pg, ceremony_id, tier, want_won=False, tries=8):
    """強制排一場指定 tier 嘅典禮。want_won 就重骰到 bestOutcome==="won" 先彈請柬。"""
    last = None
    for attempt in range(1, tries + 1):
        pack = pg.evaluate("""(o) => {
          try {
            const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
            if (!p) return { error: 'no pack' };
            return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
                     tier: p.tier, repGigId63: p.repGigId63 || '',
                     categories: (p.categories || []).map(c => ({ outcome: c.outcome, label: c.label, score: (c.score != null ? +c.score.toFixed(3) : null) })) };
          } catch(e) { return { error: String(e) }; }
        }""", {"id": ceremony_id, "tier": tier})
        last = pack
        if pack.get("error"):
            return {"pack": pack, "attempts": attempt, "invite": modal_info(pg)}
        if (not want_won) or pack.get("bestOutcome") == "won":
            pg.evaluate("() => { try { window.__awards.present(); } catch(e) {} }")
            pg.wait_for_timeout(1000)
            return {"pack": pack, "attempts": attempt, "invite": modal_info(pg)}
    return {"pack": last, "attempts": tries, "invite": modal_info(pg), "note": "never won in %d tries" % tries}

def stage_state(pg):
    return pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      const glam = st.querySelector('.awd63-glamour');
      const cv = st.querySelector('canvas');
      const r = cv ? cv.getBoundingClientRect() : null;
      return { present: true,
               caption: cap ? cap.textContent : '',
               glamPresent: !!glam,
               glamOn: !!(glam && glam.classList.contains('on')),
               canvasBox: r ? { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) } : null };
    }""")

def watch_ceremony(pg, secs=22, shot_at=None):
    """每 90ms 撳 caption＋glamour 狀態，記錄每次轉句。shot_at：(caption 關鍵字, 檔名, 延遲ms)。"""
    timeline = []
    last = None
    last_glam = False
    t0 = time.time()
    took = set()
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        cap = st.get("caption") or ""
        now = round((time.time() - t0) * 1000)
        if cap != last:
            timeline.append({"t": now, "caption": cap[:160], "glamOn": bool(st.get("glamOn"))})
            last = cap
            if shot_at:
                for key, name, delay in shot_at:
                    if key in cap and name not in took:
                        took.add(name)
                        pg.wait_for_timeout(delay)
                        shot(pg, name)
        if st.get("glamOn") and not last_glam:
            timeline.append({"t": now, "caption": "[glamour on]", "glamOn": True})
            if shot_at:
                for key, name, delay in shot_at:
                    if key == "[glamour]" and name not in took:
                        took.add(name)
                        pg.wait_for_timeout(delay)
                        shot(pg, name)
        last_glam = bool(st.get("glamOn"))
        pg.wait_for_timeout(90)
    total = round((time.time() - t0) * 1000)
    return {"timeline": timeline, "totalMs": total, "stageGone": not stage_state(pg).get("present")}

def beat_durations(timeline):
    out = []
    for i, e in enumerate(timeline):
        nxt = timeline[i + 1]["t"] if i + 1 < len(timeline) else None
        out.append({"caption": e["caption"][:60], "startMs": e["t"], "durMs": (nxt - e["t"]) if nxt is not None else None})
    return out

# ---------------- cases ----------------
FILM = "award_harbour_film"

def case_won(pg, W, H):
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=200, stage=60, acting=60,
               credit_delta=200, wraps=won_wraps())
    fa = force_award(pg, FILM, "nominee", want_won=True, tries=8)
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "attempts": fa.get("attempts"), "invite": inv, "checks": {}}
    out["checks"]["pack_is_won"] = pack.get("bestOutcome") == "won"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_attend"] = any("出席" in b for b in inv.get("btns") or [])
    shot(pg, f"won_invite_{W}x{H}.png")
    if not out["checks"]["invite_shown"] or not out["checks"]["pack_is_won"]:
        return out
    install_draw_patch(pg)
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    st0 = stage_state(pg)
    out["stage_at_start"] = st0
    out["checks"]["stage_appears"] = bool(st0.get("present"))
    out["checks"]["glamour_el_present"] = bool(st0.get("glamPresent"))
    w = watch_ceremony(pg, 24, shot_at=[("得獎！", f"won_reveal_{W}x{H}.png", 900),
                                        ("[glamour]", f"won_glamour_{W}x{H}.png", 600)])
    out["watch"] = w
    out["beats"] = beat_durations(w["timeline"])
    caps = " || ".join(e["caption"] for e in w["timeline"])
    out["checks"]["reveal_caption_has_win"] = "得獎" in caps
    out["checks"]["glamour_beat_seen"] = any(e.get("glamOn") for e in w["timeline"])
    out["checks"]["total_about_11s"] = 10000 <= w["totalMs"] <= 14000
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    draws = tux_draws(pg)
    out["tux_draws"] = draws[:5]
    out["tux_draw_count"] = len(draws)
    out["checks"]["tuxedo_drawn"] = len(draws) >= 1
    out["checks"]["tuxedo_draw_64x64"] = any(d.get("dw") == 64 and d.get("dh") == 64 for d in draws)
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    out["checks"]["result_card_says_won"] = "得獎" in (res.get("body") or "")
    shot(pg, f"won_result_{W}x{H}.png")
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
    install_draw_patch(pg)
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    w = watch_ceremony(pg, 22, shot_at=[("拍拍你膊頭", f"nominated_comfort_{W}x{H}.png", 400)])
    out["watch"] = w
    caps = [e["caption"] for e in w["timeline"]]
    joined = " || ".join(caps)
    out["checks"]["comfort_beat_seen"] = "拍拍你膊頭" in joined
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    draws = tux_draws(pg)
    out["tux_draws"] = draws[:5]
    out["tux_draw_count"] = len(draws)
    out["checks"]["tuxedo_NOT_drawn_losing_branch"] = len(draws) == 0
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    shot(pg, f"nominated_result_{W}x{H}.png")
    return out

CASES = {
    "won_932": lambda pg, W, H: case_won(pg, W, H),
    "nominated_932": lambda pg, W, H: case_nominated(pg, W, H),
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
        srv = ensure_server(srv)
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
        json.dump(results, open(os.path.join(HERE, "drive160m6.json"), "w"), ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"NOTE drive160m6.json write failed: {e!r}", flush=True)
    print("RESULTS_JSON_BEGIN")
    print(json.dumps(results, ensure_ascii=False))
    print("RESULTS_JSON_END")
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    print(f"OVERALL {n_pass}/{len(results)} PASS")
    sys.exit(0 if n_pass == len(results) else 1)

def _run_with_browser(b, sel, h_arg, results):
    for name in sel:
        H = int(h_arg)
        key = name
        print(f"== {key} ==", flush=True)
        errs = []
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120] + " :: " + str(r.failure)))
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
