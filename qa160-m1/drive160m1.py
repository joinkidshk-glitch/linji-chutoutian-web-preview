#!/usr/bin/env python3
"""v20a160 M1 實駕：會場場景圖做典禮底圖。
Cases（每 case 全新 browser context）：
  won_932     強制 film nominee＋強檔播種 → 贏分支 → 出席 → open beat 取 canvas 像素樣本
              （吊燈／紅幕／講台／白椅／紅地毯五點，證實係會場相唔係舊像素舞台）→ 全程計時約 9.35s
              → reveal 有「得獎」→ 結果卡 → 0 pageerror／0 failed request
  won_700     同上，430×700
  gallery_932 強制 film gallery（旁聽分支）→ 同一個底圖出現（四場＋三分支共用一張底圖）
用法：/home/hatch/pwenv49/bin/python qa160-m1/drive160m1.py [case|all] [932|700]
"""
import json, subprocess, sys, time, os, datetime
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work160-m1"
HERE = "/home/hatch/workspace/linji-work160-m1/qa160-m1"
SHOTS = os.path.join(HERE, "shots")
try:
    os.makedirs(SHOTS, exist_ok=True)
except Exception:
    pass
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8987
SAVE_KEY = "starVolunteer_map_v19w"
BG_URL_PART = "assets/story/awards/bg_awards_ballroom.jpg"
MARKER = "AWARDS62_STAGE_BG"

def start_server():
    """起 http.server 並驗證佢真係 serve 緊呢個工作副本（唔係隔籬 agent 佔咗 port 嘅舊檔）。
    驗唔到就 raise，等 main 唔好靜靜行落去食錯檔。"""
    import urllib.request
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 20
    last_err = None
    while time.time() < deadline:
        if srv.poll() is not None:
            raise RuntimeError(f"http.server on {PORT} exited early (rc={srv.returncode}) — port 已被佔用？")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=3) as r:
                body = r.read().decode("utf-8", "ignore")
            if MARKER in body and "AWARDS62_STAGE_PX" not in body:
                return srv
            last_err = "served index.html missing marker (wrong root?)"
        except Exception as e:
            last_err = repr(e)
        time.sleep(1.0)
    try:
        srv.terminate()
    except Exception:
        pass
    raise RuntimeError(f"server verify failed on {PORT}: {last_err}")

def ensure_server(srv):
    """每 case 前驗一次 server 仲健在＋serve 緊啱嘅檔；死咗就重起。"""
    import urllib.request
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=3) as r:
            body = r.read().decode("utf-8", "ignore")
        if MARKER in body:
            return srv
    except Exception:
        pass
    try:
        srv.terminate()
    except Exception:
        pass
    time.sleep(0.5)
    return start_server()

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
    # no_wait_after：撳「新遊戲」會觸發跳轉，負載重嗰陣等 navigation settle 會超時（v160 實駕見過）；
    # 掣本身已經撳中，之後等畫面轉就得，唔使等 navigation。
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000, no_wait_after=True)
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
    return (datetime.date(y, m, d) - datetime.date(1990, 1, 1)).days

def seed(pg, *, day, fame=40, stage=10, acting=10, credit_delta=0, money=5000, stress=0, wraps=None):
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
      S.wrapHistory = o.wraps || [];
      S.postShootRewards = [];
      return { day: S.dayIndex, wraps: (S.wrapHistory||[]).length };
    }""", {"day": day, "fame": fame, "stage": stage, "acting": acting,
            "credit_delta": credit_delta, "money": money, "stress": stress,
            "wraps": wraps or []})

def seed_won_wraps():
    """強檔：3 部 1991 電影主角作（roleScale film_lead_big，q=1.0）＋2 部 1991 電視主角作
    （跨媒介借分＋repPower），令 base ≈ 0.40＋0.42＋0.08 = 0.90，taste ±0.05 下贏面高。"""
    film_days = [day_index(1991, 3, 10), day_index(1991, 6, 15), day_index(1991, 9, 5)]
    tv_days = [day_index(1991, 4, 20), day_index(1991, 8, 12)]
    wraps = []
    for i, d in enumerate(film_days):
        wraps.append({"gigId": "seed160_film_%d" % i, "type": "電影", "wrappedDay": d,
                      "year": 1991, "pay": 50000, "roleScale": "film_lead_big",
                      "workTitle": "龍城歲月%d" % (i + 1)})
    for i, d in enumerate(tv_days):
        wraps.append({"gigId": "seed160_tv_%d" % i, "type": "電視劇", "wrappedDay": d,
                      "year": 1991, "pay": 30000, "roleScale": "tv_lead_long",
                      "workTitle": "屋企人%d" % (i + 1)})
    return wraps

def force_award(pg, ceremony_id, tier):
    pack = pg.evaluate("""(o) => {
      try {
        const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
        if (!p) return { error: 'no pack' };
        window.__awards.present();
        return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
                 tier: p.tier, categories: (p.categories || []).map(c => ({ outcome: c.outcome, label: c.label, score: c.score })) };
      } catch(e) { return { error: String(e) }; }
    }""", {"id": ceremony_id, "tier": tier})
    pg.wait_for_timeout(1000)
    inv = modal_info(pg)
    return {"pack": pack, "invite": inv}

def force_won(pg, ceremony_id, tries=8):
    """重試 force 直到 bestOutcome === 'won'（每 attempt 重抽 taste＋類別；debugForce 每次清 flag）。"""
    attempts = []
    for _ in range(tries):
        fa = force_award(pg, ceremony_id, "nominee")
        attempts.append(fa["pack"])
        if fa["pack"].get("bestOutcome") == "won":
            return {"pack": fa["pack"], "invite": fa["invite"], "attempts": len(attempts)}
    return {"pack": attempts[-1] if attempts else {}, "invite": modal_info(pg), "attempts": len(attempts)}

def stage_state(pg):
    return pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      const skip = st.querySelector('.awd62-skip');
      const cv = st.querySelector('canvas');
      const r = cap ? cap.getBoundingClientRect() : null;
      const cr = cv ? cv.getBoundingClientRect() : null;
      return { present: true,
               caption: cap ? cap.textContent : '',
               skipVisible: !!skip && skip.getBoundingClientRect().width > 0,
               captionBox: r ? { top: Math.round(r.top), bottom: Math.round(r.bottom), h: Math.round(r.height) } : null,
               canvasBox: cr ? { x: Math.round(cr.x), y: Math.round(cr.y), w: Math.round(cr.width), h: Math.round(cr.height) } : null,
               vh: window.innerHeight };
    }""")

def sample_canvas(pg):
    """open beat（未有人仔、遮罩已退）取 5 點 canvas 像素。舊像素舞台係深紫 #241736＋黑地板，
    會場相係光吊燈／紅幕／白椅／紅地毯——亮度同色相完全唔同級。"""
    return pg.evaluate("""() => {
      const cv = document.querySelector('.awd62-stage canvas');
      if (!cv) return { error: 'no canvas' };
      const ctx = cv.getContext('2d');
      const pts = { chandelier: [212, 30], curtain: [212, 80], podium: [212, 130], chairs: [100, 210], carpet: [212, 225] };
      const out = {};
      for (const [k, p] of Object.entries(pts)) {
        const d = ctx.getImageData(p[0], p[1], 1, 1).data;
        const lum = Math.round(0.299 * d[0] + 0.587 * d[1] + 0.114 * d[2]);
        out[k] = { rgb: [d[0], d[1], d[2]], lum };
      }
      const lums = Object.values(out).map(v => v.lum);
      out.meanLum = Math.round(lums.reduce((a, b) => a + b, 0) / lums.length);
      return out;
    }""")

def sample_canvas_multi(pg):
    """open beat 取三次樣本（即刻／＋300ms／＋250ms，遮罩由 0.44→0.22→0），取較光嗰組——
    遮罩只會壓暗，較光嗰組先係底圖真身；樣本點全部喺人仔企位之外（人仔佔 y≈144–194，
    樣本點係 30／80／130／210／225），就算滑入 enter beat 都唔會俾人仔遮住。"""
    sets = []
    for wait in (0, 300, 250):
        pg.wait_for_timeout(wait)
        s = sample_canvas(pg)
        if isinstance(s, dict) and "meanLum" in s:
            sets.append(s)
    if not sets:
        return {"error": "no sample"}
    return max(sets, key=lambda s: s.get("meanLum", 0))

def bg_resource(pg):
    return pg.evaluate("""(part) => {
      const rs = performance.getEntriesByType('resource').filter(e => (e.name || '').includes(part));
      return rs.map(e => ({ name: (e.name || '').slice(-60), transferSize: e.transferSize || 0, duration: Math.round(e.duration || 0) }));
    }""", BG_URL_PART)

def watch_ceremony(pg, secs=22, shot_at=None):
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
    out = []
    for i, e in enumerate(timeline):
        nxt = timeline[i + 1]["t"] if i + 1 < len(timeline) else None
        out.append({"caption": e["caption"][:60], "startMs": e["t"], "durMs": (nxt - e["t"]) if nxt is not None else None})
    return out

FILM = "award_harbour_film"

def case_won(pg, W, H):
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=150, stage=60, acting=60,
               credit_delta=80, wraps=seed_won_wraps())
    fw = force_won(pg, FILM)
    pack, inv = fw["pack"], fw["invite"]
    out = {"ctx": ctx, "pack": pack, "forceAttempts": fw["attempts"], "invite": inv, "checks": {}}
    out["checks"]["pack_is_won"] = pack.get("bestOutcome") == "won"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_attend"] = any("出席" in b for b in inv.get("btns") or [])
    shot(pg, f"won_invite_{W}x{H}.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    st0 = stage_state(pg)
    out["stage_at_start"] = st0
    out["checks"]["stage_appears"] = bool(st0.get("present"))
    out["checks"]["skip_visible"] = bool(st0.get("skipVisible"))
    # open beat（遮罩已退、未有人仔）：取兩次像素樣本，取較光嗰組＋截圖
    smp = sample_canvas_multi(pg)
    out["canvas_samples"] = smp
    out["checks"]["bg_is_photo_not_pixel_stage"] = (
        isinstance(smp, dict) and smp.get("meanLum", 0) > 60
        and smp.get("chandelier", {}).get("lum", 0) > 100
        and smp.get("chairs", {}).get("lum", 0) > 120
        and smp.get("curtain", {}).get("lum", 0) > 20)
    shot(pg, f"won_open_{W}x{H}.png")
    res = bg_resource(pg)
    out["bg_resource"] = res
    out["checks"]["bg_file_loaded_200"] = len(res) > 0 and (res[0].get("transferSize") or 0) > 0
    w = watch_ceremony(pg, 22, shot_at=[("入圍", f"won_names_{W}x{H}.png"), ("得獎", f"won_reveal_{W}x{H}.png")])
    out["watch"] = w
    out["beats"] = beat_durations(w["timeline"])
    caps = " || ".join(e["caption"] for e in w["timeline"])
    out["checks"]["reveal_names_win"] = "得獎" in caps
    out["checks"]["total_about_9_35s"] = 7000 <= w["totalMs"] <= 14000
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    pg.wait_for_timeout(600)
    res2 = modal_info(pg)
    out["result_card"] = res2
    out["checks"]["result_card_shown"] = bool(res2.get("visible"))
    shot(pg, f"won_result_{W}x{H}.png")
    return out

def case_gallery(pg, W, H):
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, FILM, "gallery")
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "invite": inv, "checks": {}}
    out["checks"]["pack_is_gallery"] = pack.get("bestOutcome") == "gallery"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    st0 = stage_state(pg)
    out["checks"]["stage_appears"] = bool(st0.get("present"))
    smp = sample_canvas_multi(pg)
    out["canvas_samples"] = smp
    out["checks"]["bg_is_photo_not_pixel_stage"] = (
        isinstance(smp, dict) and smp.get("meanLum", 0) > 60
        and smp.get("chandelier", {}).get("lum", 0) > 100
        and smp.get("chairs", {}).get("lum", 0) > 120)
    shot(pg, f"gallery_open_{W}x{H}.png")
    w = watch_ceremony(pg, 22, shot_at=[("入圍", f"gallery_names_{W}x{H}.png"), ("得獎者", f"gallery_reveal_{W}x{H}.png")])
    out["watch"] = w
    out["checks"]["total_about_9_6s"] = 7000 <= w["totalMs"] <= 14000
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    pg.wait_for_timeout(600)
    res2 = modal_info(pg)
    out["checks"]["result_card_shown"] = bool(res2.get("visible"))
    shot(pg, f"gallery_result_{W}x{H}.png")
    return out

CASES = {
    "won_932": lambda pg, W, H: case_won(pg, W, H),
    "won_700": lambda pg, W, H: case_won(pg, W, H),
    "gallery_932": lambda pg, W, H: case_gallery(pg, W, H),
}

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    h_arg = sys.argv[2] if len(sys.argv) > 2 else "932"
    sel = list(CASES.keys()) if arg == "all" else [arg]
    srv = start_server()
    print(f"server verified on {PORT} (serves this work copy)", flush=True)
    time.sleep(0.5)
    results = {}
    remaining = list(sel)
    for attempt in range(4):
        if not remaining:
            break
        try:
            with sync_playwright() as p:
                b = p.chromium.launch(executable_path=EXE)
                try:
                    _run_with_browser(b, remaining, h_arg, results, srv)
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
        json.dump(results, open(os.path.join(HERE, "drive160m1.json"), "w"), ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"NOTE drive160m1.json write failed: {e!r}", flush=True)
    print("RESULTS_JSON_BEGIN")
    print(json.dumps(results, ensure_ascii=False))
    print("RESULTS_JSON_END")
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    print(f"OVERALL {n_pass}/{len(results)} PASS")
    sys.exit(0 if n_pass == len(results) else 1)

def _run_with_browser(b, sel, h_arg, results, srv):
    for name in sel:
        H = 700 if name == "won_700" else int(h_arg)
        key = name
        print(f"== {key} ==", flush=True)
        errs = []
        try:
            srv = ensure_server(srv)
        except Exception as e:
            results[key] = {"verdict": "ERROR", "checks": {}, "error": f"server: {e!r}"}
            print(f"  ERROR server {e!r}", flush=True)
            continue
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            if not new_game_to_map(pg):
                _keep(results, key, {"verdict": "ERROR", "checks": {}, "note": "new game did not reach map"})
                print("  ERROR: no map", flush=True)
                continue
            r = CASES[name](pg, 430, H)
            r["pageerrors"] = errs[:8]
            checks = r.get("checks", {})
            r["verdict"] = "PASS" if checks and all(checks.values()) else "FAIL"
            _keep(results, key, r)
            print(f"  {r['verdict']} {json.dumps(checks, ensure_ascii=False)}", flush=True)
            if errs:
                print(f"    pageerrors: {errs[:3]}", flush=True)
        except Exception as e:
            _keep(results, key, {"verdict": "ERROR", "checks": {}, "error": repr(e)})
            print(f"  ERROR {e!r}", flush=True)
            try:
                shot(pg, f"err_{key}.png")
            except Exception:
                pass
        finally:
            ctx.close()

def _keep(results, key, new):
    """重試唔好用 ERROR 蓋過已有嘅 FAIL（有 checks）／PASS——環境死 server 唔係遊戲問題。"""
    old = results.get(key)
    if not old:
        results[key] = new
        return
    rank = {"ERROR": 0, "FAIL": 1, "PASS": 2}
    if rank.get(new.get("verdict"), 0) > rank.get(old.get("verdict"), 0):
        results[key] = new

if __name__ == "__main__":
    main()
