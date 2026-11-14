# -*- coding: utf-8 -*-
"""v20a208 實駕：頒獎禮逐格宣佈（LIVE 裸 URL，本地鏡像）。
重用 qa188/drive188.py 嘅 new_game／seed／present／watch 等 helper（import module，
覆寫 ROOT／PORT／SHOTS／EXE）；驗證係 v208 專用。

場次（932 高為主，跳過場用 700）：
  1. film_nom_932：電影 1990 nominated——全晚 4 格，格次序／逐位提名／卡片逐張出／
     每格揭曉／成晚總時長／結果卡＋報紙。
  2. film_won_932：電影 won（重試 seed 直到 pack.bestOutcome == "won"）——walkup／glamour
     喺玩家格揭曉之後、下一格之前；fanfare 觸發（__awards160Audio）。
  3. music_gal_932：音樂 1991 gallery——全晚 3 格（新人獎→女歌手→男歌手），冇 enter／walkup。
  4. ad_dec_932：廣告推辭——電視轉播版全晚多格，播完 log 標 skipped＋報紙 declined 版，冇結果卡。
  5. film_skip_700：電影 nominated，第 2 格嗰陣撳跳過 → 成晚即刻完 → 結果卡即刻出。
每場：0 pageerror／0 requestfailed。截圖放 qa208/shots208/。
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/linji-work208/qa188")
import drive188 as d

d.ROOT = "/home/hatch/workspace/linji-work208"
d.QA = "/home/hatch/workspace/linji-work208/qa208"
d.SHOTS = "/home/hatch/workspace/linji-work208/qa208/shots208"
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 20890
os.makedirs(d.SHOTS, exist_ok=True)

from playwright.sync_api import sync_playwright

JS_SEEDED_RANDOM = """(seed) => {
  let a = seed >>> 0 || 1;
  Math.random = () => {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  return true;
}"""

JS_FORCE_PACK = """(o) => {
  try {
    const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
    if (!p) return { error: 'no pack' };
    let night = null;
    try { night = window.__awards.night208(p) || null; } catch(e) {}
    let beats = null;
    try { beats = window.__awards.beats62(p) || null; } catch(e) {}
    const cats = (p.categories || []).map(c => ({
      id: c.id, label: c.label, outcome: c.outcome,
      fellows: (c.fellows63 || []).map(f => ({ starId: f.starId || '', star: f.star || '', title: f.title || '' })),
      winner: (c.winner63 && c.winner63.star) || ''
    }));
    return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome, tier: p.tier, cats,
             night: night ? night.map(n => ({ id: n.id, label: n.label, outcome: n.outcome, isFocus: !!n.isFocus,
               fellows: (n.fellows || []).map(f => f.star || ''), winner: (n.winner && n.winner.star) || '' })) : null,
             beatsTotal: beats ? beats.reduce((a, b) => a + (b.ms || 0), 0) : null,
             beatsN: beats ? beats.length : 0 };
  } catch(e) { return { error: String(e) }; }
}"""

JS_STAGE_FULL = """() => {
  const st = document.querySelector('.awd62-stage');
  if (!st) return { present: false };
  const cap = st.querySelector('.awd62-caption');
  const board = st.querySelector('.awd181-board .awd181-t');
  const shown = st.querySelectorAll('.awd63-card.show').length;
  const total = st.querySelectorAll('.awd63-card').length;
  const glam = st.querySelector('.awd63-glamour');
  return { present: true, caption: cap ? cap.textContent : '', board: board ? board.textContent : '',
           shownCards: shown, totalCards: total,
           glamOn: !!(glam && glam.classList.contains('on')) };
}"""


def force_pack_try(pg, cer, tier, want_outcome=None, max_seed=30):
    """建 pack；want_outcome 唔啱就重試唔同 Math.random seed（最多 max_seed 次）。"""
    fp = {"error": "no try"}
    for seed in range(1, max_seed + 1):
        pg.evaluate(JS_SEEDED_RANDOM, seed)
        fp = pg.evaluate(JS_FORCE_PACK, {"id": cer, "tier": tier})
        if "error" in fp:
            return fp, seed
        if want_outcome is None or fp.get("bestOutcome") == want_outcome:
            return fp, seed
    return fp, max_seed


def watch_beats(pg, secs=75, shots=None):
    """每 ~120ms 採樣：caption／board／已出卡數。回傳 samples＋boards＋總時長＋每句字幕見過嘅最大出卡數。
    shots：[(字幕子字串, 檔名)]，第一次見到嗰句即影（關鍵畫面用）。"""
    samples = []
    boards = []
    cap_max = {}
    glam_seen = False
    shot_done = set()
    last_key = None
    t0 = time.time()
    gone_at = None
    shots = shots or []
    while time.time() - t0 < secs:
        st = pg.evaluate(JS_STAGE_FULL)
        if not st.get("present"):
            gone_at = round((time.time() - t0) * 1000)
            break
        cap = st.get("caption") or ""
        shown = st.get("shownCards") or 0
        if st.get("glamOn"):
            glam_seen = True
        if cap not in cap_max or shown > cap_max[cap]:
            cap_max[cap] = shown
        key = (cap, st.get("board") or "", shown)
        if key != last_key:
            samples.append({"t": round((time.time() - t0) * 1000), "caption": cap[:160],
                            "board": key[1], "shown": shown, "total": st.get("totalCards")})
            last_key = key
        for substr, fname in shots:
            if substr not in shot_done and substr in cap:
                shot_done.add(substr)
                d.shot(pg, fname)
        b = st.get("board") or ""
        if b and b not in boards:
            boards.append(b)
        pg.wait_for_timeout(120)
    return {"samples": samples, "boards": boards, "cap_max_shown": cap_max,
            "glamSeen": glam_seen,
            "totalMs": gone_at if gone_at is not None else round((time.time() - t0) * 1000),
            "stageGone": gone_at is not None}


def wait_caption(pg, substr, timeout_ms=90000):
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout_ms:
        st = pg.evaluate(JS_STAGE_FULL)
        if not st.get("present"):
            return False
        if substr in (st.get("caption") or ""):
            return True
        pg.wait_for_timeout(120)
    return False


def wait_board(pg, label, timeout_ms=90000):
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout_ms:
        st = pg.evaluate(JS_STAGE_FULL)
        if not st.get("present"):
            return False
        if (st.get("board") or "") == label:
            return True
        pg.wait_for_timeout(120)
    return False


def analyse_timeline(w, night_labels, night):
    """由採樣 timeline＋每句字幕最大出卡數驗：格標題次序／提名 beat 數／揭曉數／卡片逐張出。
    night：in-page night208 清單（每格 isFocus＋fellows 數，計期望提名總數用）。"""
    samples = w["samples"]
    cap_max = w.get("cap_max_shown") or {}
    ck = {}
    want_titles = ["—— " + lb + " ——" for lb in night_labels]
    titles = [s["caption"] for s in samples if s["caption"] in want_titles]
    ck["cat_titles_in_order"] = titles == want_titles
    ck["cat_titles_n"] = len(titles)
    nom_caps = [c for c in cap_max if "入圍名單" in c]
    exp_nom = sum((4 if (n.get("isFocus") and n.get("outcome") != "gallery") else len(n.get("fellows") or []) or 1)
                  for n in night)
    ck["nominee_beats_total"] = len(nom_caps) == exp_nom
    rev_caps = [s["caption"] for s in samples if "得獎" in s["caption"] and "得獎者是" not in s["caption"]]
    ck["reveal_beats_seen"] = len(rev_caps) == len(night_labels)
    # 卡片逐張出：第 1 格＋玩家格（如有）逐位提名嗰陣，已出卡數要 1→2→3（→4）。
    def stepwise_for(label, n_nom):
        caps = [c for c in cap_max if ("入圍名單" in c and ("· " + label) in c)]
        caps.sort(key=lambda c: c.split("入圍名單 ")[1].split("/")[0] if "入圍名單 " in c else "")
        if len(caps) != n_nom:
            return False
        return all(cap_max[c] == i + 1 for i, c in enumerate(caps))
    def nom_n(n):
        return 4 if (n.get("isFocus") and n.get("outcome") != "gallery") else (len(n.get("fellows") or []) or 1)
    ck["cards_one_by_one_first_cat"] = stepwise_for(night_labels[0], nom_n(night[0])) if night else False
    focus = [n for n in night if n.get("isFocus")]
    if focus:
        fl = focus[0]
        if fl.get("outcome") in ("won", "nominated"):
            ck["player_nominee_beats_n"] = len([c for c in cap_max if "入圍名單" in c and ("· " + fl["label"]) in c]) == 4
            first_nom = [c for c in cap_max if "入圍名單 1/4 · " + fl["label"] in c]
            ck["player_first_nominee_is_awei"] = bool(first_nom) and "阿偉：《" in first_nom[0]
            ck["cards_one_by_one_focus_cat"] = stepwise_for(fl["label"], 4)
        else:
            # gallery 夜：focus 只係 categories[0] 兜底，唔係玩家格——玩家檢查不適用，淨驗嗰格逐張出卡
            ck["player_nominee_beats_n"] = True
            ck["player_first_nominee_is_awei"] = True
            ck["cards_one_by_one_focus_cat"] = stepwise_for(fl["label"], nom_n(fl))
    # 格標題嗰陣卡片要收起（上一格 reveal 嗰陣全出，轉格即刻拎走）。
    title_shown = [s["shown"] for s in samples if s["caption"].startswith("—— ")]
    ck["cards_hidden_at_cat_title"] = all(v == 0 for v in title_shown)
    return ck


CASES = [
    # name, ceremony, year, tier, H, fame, credit, roles, want_outcome, mode
    ("film_nom_932", "award_harbour_film", 1990, "nominee", 932, 25, 0,
     {"film_lead": 1, "film_sup": 1}, "nominated", "attend"),
    ("film_won_932", "award_harbour_film", 1990, "nominee", 932, 80, 60,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2, "tv_sup": 1, "ad_lead": 1}, "won", "attend"),
    ("music_gal_932", "award_golddisc_music", 1991, "gallery", 932, 45, 50,
     {}, None, "attend"),
    ("ad_dec_932", "award_harbour_ad", 1990, "gallery", 932, 25, 0,
     {}, None, "decline"),
    ("film_skip_700", "award_harbour_film", 1990, "nominee", 700, 25, 0,
     {"film_lead": 1, "film_sup": 1}, "nominated", "skip2nd"),
]

EXPECTED_BOARDS = {
    "award_harbour_film": ["最佳男配角", "最佳女配角", "最佳女主角", "最佳男主角"],
    "award_singho_tv": ["最佳男配角", "最佳女配角", "最佳女主角", "最佳男主角"],
    "award_harbour_ad": ["最佳廣告男配角", "最佳廣告女配角", "最佳廣告女主角", "最佳廣告男主角"],
    "award_golddisc_music": ["最佳新人獎", "最佳女歌手", "最佳男歌手"],
}


def run_case(pw, cfg, results):
    name, cer, year, tier, H, fame, credit, roles, want_outcome, mode = cfg
    print(f"== {name} ({cer} {year} {tier} {mode}) ==", flush=True)
    out = {"case": name, "ceremony": cer, "year": year, "tier": tier, "mode": mode, "checks": {}}
    errs = []
    b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            if not d.new_game(pg):
                out["checks"]["new_game"] = False
                out["verdict"] = "ERROR"
                results[name] = out
                print("  ERROR new_game", flush=True)
                return
            out["checks"]["new_game"] = True
            sd = d.seed(pg, {"year": year, "fame": fame, "credit": credit,
                             "roles": roles, "payOverride": None}, [])
            out["seed"] = sd
            fp, seed_used = force_pack_try(pg, cer, tier, want_outcome)
            out["pack"] = fp
            out["seed_used"] = seed_used
            out["checks"]["pack_built"] = "error" not in fp
            if "error" in fp:
                out["verdict"] = "ERROR"
                results[name] = out
                print("  ERROR pack", fp, flush=True)
                return
            if want_outcome is not None:
                out["checks"]["pack_outcome_" + want_outcome] = fp.get("bestOutcome") == want_outcome
            night = fp.get("night") or []
            night_labels = [n["label"] for n in night]
            out["checks"]["night_labels_in_order"] = night_labels == EXPECTED_BOARDS.get(cer, [])
            focus = [n for n in night if n.get("isFocus")]
            focus_label = focus[0]["label"] if focus else ""
            out["focus_label"] = focus_label
            inv = d.present(pg)
            out["invite"] = inv
            out["checks"]["invite_shown"] = bool(inv.get("visible"))
            d.shot(pg, f"{name}_invite.png")
            if not inv.get("visible"):
                out["pageerrors"] = errs[:8]
                out["checks"]["zero_pageerror"] = len(errs) == 0
                out["verdict"] = "FAIL"
                results[name] = out
                print(f"  FAIL no invite", flush=True)
                return
            if mode == "decline":
                d.click_vis(pg, "推辭")
                pg.wait_for_timeout(400)
                out["checks"]["stage_appears"] = bool(d.stage_state(pg).get("present"))
                w = watch_beats(pg, 75, [("—— 最佳廣告女主角 ——", f"{name}_cat2.png"),
                                         ("2/3 · 最佳廣告女主角", f"{name}_nom.png")])
                out["watch"] = w
                out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
                out["checks"].update(analyse_timeline(w, night_labels, night))
                out["checks"]["boards_in_order"] = w["boards"] == EXPECTED_BOARDS.get(cer, [])
                exp_total = fp.get("beatsTotal")
                out["expected_total_ms"] = exp_total
                out["checks"]["total_duration_close"] = (
                    exp_total is not None and abs(w["totalMs"] - exp_total) <= 5000)
                pg.wait_for_timeout(800)
                res = d.modal_info(pg)
                out["checks"]["no_result_card_after_decline"] = not (bool(res.get("visible")) and "結果" in (res.get("h3") or ""))
                log = pg.evaluate("""() => {
                  const lg = (typeof S !== 'undefined' && S && S.awardsLog) || [];
                  const nq = (typeof S !== 'undefined' && S && S.newspaperQueue) || [];
                  return { skipped: lg.length ? !!lg[0].skipped : null,
                           nqAward: nq.filter(n => (n.source || '') === 'award').length,
                           nqHeadlines: nq.map(n => n.headline || '') }; }""")
                out["decline_log"] = log
                out["checks"]["log_marked_skipped"] = log.get("skipped") is True
                out["checks"]["newspaper_has_award"] = (log.get("nqAward") or 0) >= 1
                d.shot(pg, f"{name}_after.png")
            elif mode == "skip2nd":
                d.click_vis(pg, "出席")
                pg.wait_for_timeout(400)
                t_stage0 = time.time()
                out["checks"]["stage_appears"] = bool(d.stage_state(pg).get("present"))
                second_label = night_labels[1] if len(night_labels) > 1 else ""
                ok_board = wait_board(pg, second_label, 60000)
                out["checks"]["reached_2nd_cat"] = ok_board
                skip_t = None
                if ok_board:
                    # 第 2 格格標題嗰陣影一張，再撳跳過
                    d.shot(pg, f"{name}_cat2_title.png")
                    skip_t = round((time.time() - t_stage0) * 1000)
                    clicked = pg.evaluate("""() => {
                      const b = document.querySelector('.awd62-skip');
                      if (!b) return false; b.click(); return true; }""")
                    out["checks"]["skip_clicked"] = bool(clicked)
                    pg.wait_for_timeout(1500)
                out["skip_at_ms"] = skip_t
                out["checks"]["stage_gone_after_skip"] = not d.stage_state(pg).get("present")
                pg.wait_for_timeout(600)
                res = d.modal_info(pg)
                out["result_card"] = res
                out["checks"]["result_card_shown_immediately"] = bool(res.get("visible"))
                out["checks"]["skip_was_early"] = skip_t is not None and skip_t < 30000
                d.shot(pg, f"{name}_result.png")
            else:  # attend
                d.click_vis(pg, "出席")
                pg.wait_for_timeout(400)
                out["checks"]["stage_appears"] = bool(d.stage_state(pg).get("present"))
                # 關鍵畫面：每場按字幕觸發影相（watch_beats 第一次見到嗰句即影）
                shots = []
                if name == "film_nom_932":
                    shots = [("2/4 · ", f"{name}_nom2.png"), ("差少少", f"{name}_reveal.png")]
                elif name == "film_won_932":
                    shots = [("得獎！", f"{name}_reveal.png"), ("接過獎盃", f"{name}_walkup.png")]
                elif name == "music_gal_932":
                    # 女歌手嗰格得 2 位 fellows，字幕係「1/2 ·」唔係「1/3 ·」
                    shots = [("· 最佳女歌手", f"{name}_nom.png"), ("—— 最佳男歌手 ——", f"{name}_lastcat.png")]
                w = watch_beats(pg, 75, shots)
                out["watch"] = w
                out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
                out["checks"].update(analyse_timeline(w, night_labels, night))
                out["checks"]["boards_in_order"] = w["boards"] == EXPECTED_BOARDS.get(cer, [])
                exp_total = fp.get("beatsTotal")
                out["expected_total_ms"] = exp_total
                out["checks"]["total_duration_close"] = (
                    exp_total is not None and abs(w["totalMs"] - exp_total) <= 5000)
                if mode == "attend" and want_outcome == "won":
                    caps = [s["caption"] for s in w["samples"]]
                    out["checks"]["walkup_caption_seen"] = any("接過獎盃" in c for c in caps)
                    out["checks"]["glamour_overlay_seen"] = bool(w.get("glamSeen"))
                    audio = pg.evaluate("() => window.__awards160Audio || null")
                    out["audio_flag"] = audio
                    out["checks"]["fanfare_attempted"] = bool(audio) and audio.get("fanfare") in ("attempted", "playing", "blocked")
                pg.wait_for_timeout(600)
                res = d.modal_info(pg)
                out["result_card"] = res
                out["checks"]["result_card_shown"] = bool(res.get("visible"))
                if res.get("visible") and focus_label:
                    out["checks"]["result_card_names_focus_cat"] = focus_label in (res.get("body") or "")
                d.shot(pg, f"{name}_result.png")
                if res.get("visible"):
                    d.click_vis(pg, "收下這晚")
                    pg.wait_for_timeout(900)
                    nq = d.newspaper_award(pg)
                    out["newspaper"] = nq
                    aw = [n for n in nq if "award" in (n.get("source") or "").lower()
                          or "頒獎" in (n.get("headline") or "")]
                    out["checks"]["newspaper_has_award"] = len(aw) >= 1
            out["pageerrors"] = errs[:8]
            out["checks"]["zero_pageerror"] = len(errs) == 0
            out["verdict"] = "PASS" if all(out["checks"].values()) else "FAIL"
            results[name] = out
            print(f"  {out['verdict']} {json.dumps(out['checks'], ensure_ascii=False)}", flush=True)
            if errs:
                print(f"    pageerrors: {errs[:3]}", flush=True)
        except Exception as e:
            out["error"] = repr(e)
            out["verdict"] = "ERROR"
            out["pageerrors"] = errs[:8]
            results[name] = out
            print(f"  ERROR {e!r}", flush=True)
            try:
                d.shot(pg, f"err_{name}.png")
            except Exception:
                pass
        finally:
            ctx.close()
    finally:
        b.close()


def main():
    srv = d.serve()
    try:
        results = {}
        with sync_playwright() as pw:
            for cfg in CASES:
                run_case(pw, cfg, results)
        with open(os.path.join(d.QA, "drive208.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        npass = sum(1 for r in results.values() if r.get("verdict") == "PASS")
        print(f"== SUMMARY {npass}/{len(results)} PASS ==", flush=True)
        for k, r in results.items():
            bad = {kk: vv for kk, vv in (r.get("checks") or {}).items() if not vv}
            print(f"  {k}: {r.get('verdict')} {json.dumps(bad, ensure_ascii=False)}"
                  f" expected_total={r.get('expected_total_ms')} measured={((r.get('watch') or {}).get('totalMs'))}", flush=True)
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
