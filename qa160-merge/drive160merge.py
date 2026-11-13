#!/usr/bin/env python3
"""v20a160 合併實駕：四項一齊喺贏分支典禮出現，次序正確，0 pageerror。
Cases（每 case 全新 browser context）：
  won_932     強制 film won（真海報 gig 種子，有 glamour）→ 出席 → 全程 poll：
              會場底圖載入、燕尾服繪製、walkup GIF 郁、glamour 喺 walkup 之後、
              fanfare 揭曉嗰刻 attempted＋掌聲跟住 attempted、結果卡、0 pageerror。
  gallery_932 強制 film gallery → 出席 → 睇晒全場：零 audio 請求、燕尾服 0 次、walkup 唔出、底圖照載。
  won_700     won_932 嘅 700 濃縮版（底圖＋燕尾服＋walkup＋音頻 attempted＋0 pageerror）。
用法：/home/hatch/pwenv49/bin/python qa160-merge/drive160merge.py [won_932|gallery_932|won_700|all] [932|700]
注意：port 8985（唔用 8972／8982，嗰啲有其他工用緊）；開 browser 前 check_served() 驗四個標記。
"""
import json, os, subprocess, sys, time, datetime
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work160"
HERE = "/home/hatch/workspace/linji-work160/qa160-merge"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8985
SAVE_KEY = "starVolunteer_map_v19w"
MARKERS = ("AWARDS62_STAGE_BG", "awd_walkup_m4", "AWARDS160_TUXEDO_AWEI", "awards160PlayWinAudio")

def check_served():
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
    for marker in MARKERS:
        if marker not in body:
            raise RuntimeError(f"served check failed: {url} 冇 {marker}")
    return True

def stop_server(srv):
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
      return {visible:true, h3, btns, body: (m.innerText || '').slice(0, 1200)};
    }""")

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
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=30000)
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

def won_wraps():
    d = day_index
    film = [{"gigId": "gig_1988_film_lion_autumn_high", "type": "電影", "pay": 30000,
             "wrappedDay": d(1991, m, 15), "year": 1991} for m in (3, 4, 6, 8)]
    tv = [{"gigId": "fake_tv_lead_%d" % i, "type": "電視劇", "roleScale": "tv_lead_long",
           "pay": 30000, "wrappedDay": d(1991, m, 15), "year": 1991} for i, m in enumerate((5, 7))]
    return film + tv

def seed_won_poster(pg, day):
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
      S.wrapHistory = o.wraps;
      S.postShootRewards = [];
      try { localStorage.setItem(o.key, JSON.stringify(S)); } catch(e) {}
      return { day: S.dayIndex, wraps: S.wrapHistory.length };
    }""", {"day": day, "w530": w530, "wraps": won_wraps(), "key": SAVE_KEY})

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

def install_draw_patch(pg):
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

def force_award(pg, ceremony_id, tier, want_won=False, tries=8):
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
        click_vis_btn(pg, "推辭")
        pg.wait_for_timeout(400)
    return {"pack": last, "attempts": tries, "invite": modal_info(pg), "note": "never won"}

def stage_state(pg):
    return pg.evaluate("""() => {
      // 資源／音頻旗標／燕尾服繪製次數唔依賴舞台元素——典禮播完舞台會拆走，但呢啲證據要留返。
      const audio = window.__awards160Audio || null;
      const res = performance.getEntriesByType('resource').filter(r => /bg_awards_ballroom|awards_fanfare|awards_applause|awd_walkup_m4/.test(r.name))
        .map(r => ({ name: r.name.split('/').slice(-1)[0], transfer: Math.round(r.transferSize || 0) }));
      const tuxDraws = (window.__tuxDraws || []).length;
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false, audio: audio, resources: res, tuxDraws: tuxDraws };
      const cap = st.querySelector('.awd62-caption');
      const glam = st.querySelector('.awd63-glamour');
      const walk = st.querySelector('.awd62-walkup160');
      const wimg = walk ? walk.querySelector('img') : null;
      const cv = st.querySelector('canvas');
      return { present: true,
               caption: cap ? cap.textContent : '',
               glamPresent: !!glam, glamOn: !!(glam && glam.classList.contains('on')),
               walkPresent: !!walk, walkOn: !!(walk && walk.classList.contains('on')),
               walkImg: wimg ? { src: (wimg.getAttribute('src') || ''), complete: !!wimg.complete, w: wimg.naturalWidth, h: wimg.naturalHeight } : null,
               audio: audio, resources: res,
               tuxDraws: tuxDraws };
    }""")

def attend(pg):
    for _ in range(20):
        mi = modal_info(pg)
        if mi.get("visible") and any("出席" in b for b in mi.get("btns", [])):
            if click_vis_btn(pg, "出席"):
                pg.wait_for_timeout(1200)
                return True
        pg.wait_for_timeout(500)
    return False

def run_case(pw, name, height, want_won, tier, seed_fn):
    out = {"case": name, "checks": {}, "errors": []}
    errs = []
    pg = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"]).new_page(viewport={"width": 430, "height": height})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    try:
        assert new_game_to_map(pg), "去唔到地圖"
        install_draw_patch(pg)
        day = day_index(1991, 10, 20)
        seed_fn(pg, day)
        fa = force_award(pg, "award_harbour_film", tier, want_won=want_won)
        out["pack"] = fa["pack"]
        out["attempts"] = fa["attempts"]
        if want_won:
            assert fa["pack"].get("bestOutcome") == "won", "重骰 %d 次都唔贏：%s" % (fa["attempts"], fa["pack"])
        assert attend(pg), "請柬出席撳唔到"
        t0 = time.time()
        timeline = []
        walk_shots = []
        while time.time() - t0 < 22:
            st = stage_state(pg)
            timeline.append({"t": round(time.time() - t0, 2), "cap": (st.get("caption") or "")[:40],
                             "walkOn": st.get("walkOn"), "glamOn": st.get("glamOn"),
                             "audio": st.get("audio"), "tux": st.get("tuxDraws")})
            if st.get("walkOn") and len(walk_shots) < 3:
                shot(pg, f"{name}_walkup_{len(walk_shots)}.png")
                walk_shots.append(time.time())
                if len(walk_shots) < 3:
                    pg.wait_for_timeout(350)  # 350ms ≈ 2.9 幀，唔係 1080ms loop 嘅倍數，兩張唔會撞返同一幀
            if st.get("glamOn"):
                shot(pg, f"{name}_glamour.png")
            # 結果卡出現＝典禮播完
            if pg.evaluate("() => !!(document.querySelector('.awd62-result') || [...document.querySelectorAll('button')].some(b => (b.textContent||'').includes('返回地圖')))") and time.time() - t0 > 8:
                if st.get("glamOn") or time.time() - t0 > 14:
                    break
            pg.wait_for_timeout(150)
        out["timeline"] = timeline
        final = stage_state(pg)
        out["final"] = final
        shot(pg, f"{name}_result.png")
        # ---- 斷言 ----
        c = out["checks"]
        res_names = [r["name"] for r in final.get("resources", [])]
        c["bg_loaded"] = "bg_awards_ballroom.jpg" in res_names and any(r["transfer"] > 0 for r in final.get("resources", []) if r["name"] == "bg_awards_ballroom.jpg")
        c["tux_drawn"] = final.get("tuxDraws", 0) > 0
        c["walkup_seen"] = any(t.get("walkOn") for t in timeline)
        c["walkup_img_ok"] = bool(final.get("walkImg") and final["walkImg"]["complete"] and final["walkImg"]["w"] == 144)
        if len(walk_shots) >= 2:
            import hashlib
            hashes = []
            for k in range(len(walk_shots)):
                p = os.path.join(SHOTS, f"{name}_walkup_{k}.png")
                hashes.append(hashlib.md5(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None)
            c["walkup_animates"] = len(set(h for h in hashes if h)) > 1
        else:
            c["walkup_animates"] = False
        walk_first = next((t["t"] for t in timeline if t.get("walkOn")), None)
        glam_first = next((t["t"] for t in timeline if t.get("glamOn")), None)
        c["glamour_seen"] = glam_first is not None
        c["walkup_before_glamour"] = (walk_first is not None and glam_first is not None and walk_first < glam_first)
        c["fanfare_attempted"] = bool(final.get("audio") and final["audio"].get("fanfare") not in (None, "idle"))
        c["applause_attempted"] = bool(final.get("audio") and final["audio"].get("applause") not in (None, "idle"))
        c["fanfare_mp3_fetched"] = "awards_fanfare.mp3" in res_names
        c["applause_mp3_fetched"] = "awards_applause.mp3" in res_names
        c["result_shown"] = pg.evaluate("""(won) => {
          const txt = document.body.innerText || '';
          if (won) return txt.includes('得獎');
          return !!document.querySelector('.awd62-result') || txt.includes('頒獎');
        }""", want_won)
        if not want_won:
            # 對照組：乜都唔應該觸發（音頻用成條 timeline 判斷，唔用 final——舞台拆走之後 final 冇 audio）。
            tl_audio = [t.get("audio") for t in timeline if t.get("audio")]
            c["bg_loaded"] = c["bg_loaded"]
            c["tux_drawn"] = final.get("tuxDraws", 0) == 0
            c["walkup_seen"] = not any(t.get("walkOn") for t in timeline)
            c["walkup_img_ok"] = True
            c["walkup_animates"] = True
            c["glamour_seen"] = True  # gallery 唔要求 glamour
            c["walkup_before_glamour"] = True
            c["fanfare_attempted"] = not any(a.get("fanfare") not in (None, "idle") for a in tl_audio)
            c["applause_attempted"] = not any(a.get("applause") not in (None, "idle") for a in tl_audio)
            c["fanfare_mp3_fetched"] = "awards_fanfare.mp3" not in res_names
            c["applause_mp3_fetched"] = "awards_applause.mp3" not in res_names
        out["pass"] = all(c.values())
    except Exception as e:
        out["pass"] = False
        out["error"] = str(e)
    finally:
        out["pageerrors"] = errs
        out["checks"]["zero_pageerror"] = len(errs) == 0
        out["pass"] = out.get("pass", False) and len(errs) == 0
        try:
            pg.close()
        except Exception:
            pass
    return out

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        check_served()
        results = {}
        with sync_playwright() as pw:
            if which in ("all", "won_932"):
                results["won_932"] = run_case(pw, "won_932", 932, True, "nominee", seed_won_poster)
            if which in ("all", "gallery_932"):
                results["gallery_932"] = run_case(pw, "gallery_932", 932, False, "gallery", seed_plain)
            if which in ("all", "won_700"):
                results["won_700"] = run_case(pw, "won_700", 700, True, "nominee", seed_won_poster)
        json.dump(results, open(os.path.join(HERE, "drive160merge.json"), "w"), ensure_ascii=False, indent=1)
        for name, r in results.items():
            print(f"{name}: {'PASS' if r.get('pass') else 'FAIL'} checks={r.get('checks')} pageerrors={len(r.get('pageerrors', []))} attempts={r.get('attempts')} pack={str(r.get('pack', {}).get('bestOutcome'))}")
            if r.get("error"):
                print("  ERROR:", r["error"])
        ok = all(r.get("pass") for r in results.values())
        print("OVERALL", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    finally:
        stop_server(srv)

if __name__ == "__main__":
    sys.exit(main())
