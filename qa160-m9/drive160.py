#!/usr/bin/env python3
"""v20a160 M9 實駕：頒獎禮贏分支音效——揭曉嗰刻播 fanfare＋掌聲。
Cases（每 case 全新 browser context，免狀態污染）：
  won_932       ① 強制 film won → 出席 → 全程睇 caption＋window.__awards160Audio 旗標：
                 fanfare 揭曉嗰刻 attempted、掌聲 ~900ms 後 attempted、兩者先後有序；
                 另驗 mp3 真係有經網絡攞（performance resource entries）＋0 pageerror。
  won_skip_932  ② 強制 film won → 出席 → 揭曉前撳「跳過 ⏩」→ 音效旗標維持未觸發（證明只係揭曉觸發）。
  gallery_932   ③ 強制 film gallery → 出席 → 全程睇完 → 音效旗標維持未觸發（證明只限贏分支）。
headless 未必出到聲：本腳本驗觸發邏輯＋檔案攞取＋零 pageerror，唔扮驗到聲；
旗標 playing／blocked 只作觀察記錄，attempted 先係觸發證明。
用法：/home/hatch/pwenv49/bin/python qa160-m9/drive160.py [case|all] [932|700]
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work160-m9"
HERE = "/home/hatch/workspace/linji-work160-m9/qa160-m9"
SHOTS = os.path.join(HERE, "shots")
try:
    os.makedirs(SHOTS, exist_ok=True)
except Exception:
    pass
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8982
SAVE_KEY = "starVolunteer_map_v19w"

def check_served():
    """開 browser 之前先驗：呢個 port 派緊嘅 index.html 係咪我哋工作副本嗰份。
    （教訓：port 8972 俾 M6 兄弟工人嘅 server 佔咗（cwd linji-work160-m6），
    嗰陣 browser 靜默載咗佢哋嗰份——game 照玩、典禮照贏，但完全冇 M9 code，
    旗標永遠唔郁。bind 失敗嗰陣 Popen 唔會出聲（stderr 去咗 DEVNULL），所以一定要驗內容。）
    重試：負載大嗰陣 server 起身慢，1 秒未必 listen 到，唔好一次唔得就判死刑。"""
    import urllib.request
    url = f"http://127.0.0.1:{PORT}/index.html"
    body = None
    last_err = None
    for _ in range(15):
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                body = r.read().decode("utf-8", "replace")
            break
        except Exception as e:
            last_err = e
            time.sleep(1.0)
    if body is None:
        raise RuntimeError(f"served check failed: cannot fetch {url}: {last_err!r}")
    for marker in ("awards160PlayWinAudio", "assets/audio/awards_fanfare.mp3", "assets/audio/awards_applause.mp3"):
        if marker not in body:
            raise RuntimeError(f"served check failed: {url} 冇 {marker}——呢個 port 唔係派緊我哋工作副本！")
    return True

def stop_server(srv):
    """停 server：terminate 之後等一陣，仲未死就 kill。唔可以漏 server 佔住個 port
    （漏咗會令下次 bind 失敗、browser 靜默載錯份——見 check_served 教訓）。"""
    try:
        srv.terminate()
        srv.wait(timeout=5)
    except Exception:
        try:
            srv.kill()
        except Exception:
            pass

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
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=30000)  # timeout 30s：負載大嗰陣 click 後等 navigation 會超過 5s（v160 實駕教訓），click 本身早已完成
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

def seed_strong(pg, day):
    """贏分支種子：雙軌拉滿＋1991 年 4 部電影擔正（q=1.00）＋2 部電視劇擔正（跨桶借分）。
    base = 0.40*1 + 0.42*1 + 0.08 = 0.90，taste ±0.05 → 單類別贏率 75%，兩類別 94%／次。"""
    w530 = day_index(1991, 6, 15)
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = 200; S.stage = 60; S.acting = 60;
      S.industryCreditDelta = 100;
      S.money = 5000; S.stress = 0;
      S.flags = S.flags || {};
      const mk = (type, role) => ({ type: type, roleScale: role, wrappedDay: o.w530, gigId: "", workTitle: "" });
      S.wrapHistory = [mk("電影", "film_lead_big"), mk("電影", "film_lead_big"),
                       mk("電影", "film_lead_big"), mk("電影", "film_lead_big"),
                       mk("電視劇", "tv_lead_long"), mk("電視劇", "tv_lead_long")];
      S.postShootRewards = [];
      try { localStorage.setItem(o.key, JSON.stringify(S)); } catch(e) {}
      return { day: S.dayIndex, fame: S.fame, wraps: S.wrapHistory.length };
    }""", {"day": day, "w530": w530, "key": SAVE_KEY})

def seed_plain(pg, day):
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = 40; S.stage = 10; S.acting = 10;
      S.industryCreditDelta = 0;
      S.money = 5000; S.stress = 0;
      S.flags = S.flags || {};
      S.wrapHistory = [];
      S.postShootRewards = [];
      try { localStorage.setItem(o.key, JSON.stringify(S)); } catch(e) {}
      return { day: S.dayIndex };
    }""", {"day": day, "key": SAVE_KEY})

def force_award(pg, ceremony_id, tier):
    pack = pg.evaluate("""(o) => {
      try {
        const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
        if (!p) return { error: 'no pack' };
        window.__awards.present();
        return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
                 tier: p.tier, categories: (p.categories || []).map(c => ({ outcome: c.outcome, label: c.label, score: (c.score != null ? Math.round(c.score * 1000) / 1000 : null) })) };
      } catch(e) { return { error: String(e) }; }
    }""", {"id": ceremony_id, "tier": tier})
    pg.wait_for_timeout(1000)
    inv = modal_info(pg)
    return {"pack": pack, "invite": inv}

def force_won(pg, ceremony_id, tries=6):
    """重骰直至 bestOutcome==="won"（每試重骰類別＋taste；理論上每試 ~94%）。"""
    attempts = []
    for _ in range(tries):
        fa = force_award(pg, ceremony_id, "nominee")
        attempts.append(fa["pack"])
        if fa["pack"].get("bestOutcome") == "won":
            return {"pack": fa["pack"], "invite": fa["invite"], "attempts": len(attempts), "tried": attempts}
        # 唔可以用 dismiss_once：請柬第一個掣係「出席」，撳錯會開咗唔贏嗰場典禮。
        # 撳「推辭」安全（debugForceSeasonWindow 下次會清 flag 再排隊）。
        click_vis_btn(pg, "推辭")
        pg.wait_for_timeout(400)
    return {"pack": attempts[-1], "invite": modal_info(pg), "attempts": len(attempts), "tried": attempts}

def stage_state(pg):
    return pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      const skip = st.querySelector('.awd62-skip');
      return { present: true,
               caption: cap ? cap.textContent : '',
               skipVisible: !!skip && skip.getBoundingClientRect().width > 0 };
    }""")

def audio_flag(pg):
    return pg.evaluate("() => (window.__awards160Audio ? { fanfare: window.__awards160Audio.fanfare, applause: window.__awards160Audio.applause } : null)")

def audio_resources(pg):
    return pg.evaluate("""() => {
      const es = performance.getEntriesByType('resource') || [];
      return es.filter(e => (e.name || '').indexOf('awards_') >= 0 && (e.name || '').indexOf('.mp3') >= 0)
               .map(e => ({ url: e.name.split('/').slice(-1)[0], transferSize: e.transferSize || 0, duration: Math.round(e.duration || 0) }));
    }""")

def watch_ceremony_audio(pg, secs=18, shot_at=None):
    """每 90ms 撳 caption＋audio 旗標，記錄每次轉變嘅時間。"""
    timeline = []
    audio_log = []
    last_cap = None
    last_flag = None
    t0 = time.time()
    took = set()
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        cap = st.get("caption") or ""
        now = round((time.time() - t0) * 1000)
        if cap != last_cap:
            timeline.append({"t": now, "caption": cap[:160]})
            last_cap = cap
            if shot_at:
                for key, name in shot_at:
                    if key in cap and name not in took:
                        shot(pg, name)
                        took.add(name)
        fl = audio_flag(pg)
        fl_key = json.dumps(fl, sort_keys=True) if fl else "null"
        if fl_key != last_flag:
            audio_log.append({"t": now, "flag": fl})
            last_flag = fl_key
        pg.wait_for_timeout(90)
    total = round((time.time() - t0) * 1000)
    return {"timeline": timeline, "audioLog": audio_log, "totalMs": total,
            "stageGone": not stage_state(pg).get("present"),
            "finalFlag": audio_flag(pg), "resources": audio_resources(pg)}

# ---------------- cases ----------------
FILM = "award_harbour_film"

def case_won(pg, W, H):
    ctx = seed_strong(pg, day_index(1991, 10, 20))
    fw = force_won(pg, FILM)
    pack, inv = fw["pack"], fw["invite"]
    out = {"ctx": ctx, "pack": pack, "forceAttempts": fw["attempts"], "invite": inv, "checks": {}}
    out["checks"]["pack_is_won"] = pack.get("bestOutcome") == "won"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_attend"] = any("出席" in b for b in inv.get("btns") or [])
    shot(pg, f"won_invite_{W}x{H}.png")
    if not out["checks"]["invite_shown"] or not out["checks"]["pack_is_won"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    st0 = stage_state(pg)
    out["stage_at_start"] = st0
    out["checks"]["stage_appears"] = bool(st0.get("present"))
    w = watch_ceremony_audio(pg, 18, shot_at=[("得獎", f"won_reveal_{W}x{H}.png")])
    out["watch"] = w
    caps = " || ".join(e["caption"] for e in w["timeline"])
    out["checks"]["reveal_caption_won"] = ("得獎" in caps) and ("阿偉" in caps or "得獎！" in caps)
    out["checks"]["total_about_9_3s"] = 8000 <= w["totalMs"] <= 12000
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    fl = w.get("finalFlag") or {}
    out["checks"]["fanfare_attempted"] = fl.get("fanfare") in ("attempted", "playing", "blocked")
    out["checks"]["applause_attempted"] = fl.get("applause") in ("attempted", "playing", "blocked")
    # 時序：fanfare 先於掌聲 attempted；掌聲唔早過 fanfare＋500ms（規格 900ms，量度容差）。
    alog = w.get("audioLog") or []
    t_fan = next((e["t"] for e in alog if (e.get("flag") or {}).get("fanfare") in ("attempted", "playing", "blocked")), None)
    t_app = next((e["t"] for e in alog if (e.get("flag") or {}).get("applause") in ("attempted", "playing", "blocked")), None)
    out["audio_first_times"] = {"fanfareMs": t_fan, "applauseMs": t_app}
    out["checks"]["fanfare_before_applause"] = (t_fan is not None and t_app is not None and t_app >= t_fan)
    out["checks"]["applause_delay_ge_500ms"] = (t_fan is not None and t_app is not None and (t_app - t_fan) >= 500)
    out["checks"]["fanfare_state_observed"] = fl.get("fanfare") in ("playing", "blocked")
    out["checks"]["applause_state_observed"] = fl.get("applause") in ("playing", "blocked")
    # mp3 真係有經網絡攞（唔係 404／冇請求）
    res = w.get("resources") or []
    out["checks"]["fanfare_mp3_fetched"] = any(r.get("url") == "awards_fanfare.mp3" and (r.get("transferSize") or 0) > 0 for r in res)
    out["checks"]["applause_mp3_fetched"] = any(r.get("url") == "awards_applause.mp3" and (r.get("transferSize") or 0) > 0 for r in res)
    pg.wait_for_timeout(600)
    res_modal = modal_info(pg)
    out["result_card"] = res_modal
    out["checks"]["result_card_shown"] = bool(res_modal.get("visible"))
    shot(pg, f"won_result_{W}x{H}.png")
    return out

def case_won_skip(pg, W, H):
    ctx = seed_strong(pg, day_index(1991, 10, 20))
    fw = force_won(pg, FILM)
    out = {"ctx": ctx, "pack": fw["pack"], "forceAttempts": fw["attempts"], "checks": {}}
    out["checks"]["pack_is_won"] = fw["pack"].get("bestOutcome") == "won"
    out["checks"]["invite_shown"] = bool(fw["invite"].get("visible"))
    if not out["checks"]["invite_shown"] or not out["checks"]["pack_is_won"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(1000)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    clicked = pg.evaluate("""() => { const b = document.querySelector('.awd62-skip'); if (!b) return false; b.click(); return true; }""")
    out["checks"]["skip_clicked"] = bool(clicked)
    pg.wait_for_timeout(800)
    out["checks"]["stage_gone_fast"] = not stage_state(pg).get("present")
    out["finalFlag"] = audio_flag(pg)
    out["checks"]["audio_never_attempted"] = audio_flag(pg) is None
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown_after_skip"] = bool(res.get("visible"))
    shot(pg, f"won_skip_result_{W}x{H}.png")
    return out

def case_gallery(pg, W, H):
    ctx = seed_plain(pg, day_index(1991, 10, 20))
    fa = force_award(pg, FILM, "gallery")
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "invite": inv, "checks": {}}
    out["checks"]["pack_is_gallery"] = pack.get("bestOutcome") == "gallery"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    w = watch_ceremony_audio(pg, 18)
    out["watch"] = w
    out["checks"]["total_about_9_6s"] = 8000 <= w["totalMs"] <= 12000
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    out["checks"]["audio_never_attempted"] = audio_flag(pg) is None
    out["checks"]["no_audio_resources"] = len(w.get("resources") or []) == 0
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    shot(pg, f"gallery_result_{W}x{H}.png")
    return out

CASES = {
    "won_932": lambda pg, W, H: case_won(pg, W, H),
    "won_skip_932": lambda pg, W, H: case_won_skip(pg, W, H),
    "gallery_932": lambda pg, W, H: case_gallery(pg, W, H),
}

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    h_arg = sys.argv[2] if len(sys.argv) > 2 else "932"
    sel = list(CASES.keys()) if arg == "all" else [arg]
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    try:
        check_served()
    except Exception as e:
        print(f"FATAL served check: {e!r}", flush=True)
        stop_server(srv)
        sys.exit(2)
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
    stop_server(srv)
    try:
        json.dump(results, open(os.path.join(HERE, "drive160.json"), "w"), ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"NOTE drive160.json write failed: {e!r}", flush=True)
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
