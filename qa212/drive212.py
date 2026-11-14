# -*- coding: utf-8 -*-
"""v20a212 實駕：v208 review 七項修復覆驗（LIVE 裸 URL，本地鏡像）。
重用常駐 clone qa188/drive188.py 嘅 new_game／seed／present 等 helper；
改編自 linji-design-review-v208/drive208_review.py（timeline／探針／亮度）。

場次：
  1. film_nom_932：電影 1990 nominated，4 格全晚（B1 去重＋懸念輪換＋C1／C2／C3）。
  2. film_won_932：電影 won（強 seed，seed 1 即 won；A1 glamour＋C4 walkup）。
  3. film_won_700：電影 won 700（A1 glamour 700 版）。
  4. music_gal_932：音樂 1991 gallery，3 格（C5 兩人置中＋C1／C2）。
  5. ad_dec_932：廣告推辭，全晚多格＋declined 報紙（B1 去重）。
  6. film_skip_700：第 2 格撳跳過 → 成晚即完 → 結果卡（跳過掣本身未壞）。
  7. map_932：主畫面抽查。
每場 0 pageerror。截圖放 qa212/shots212/。
"""
import json
import os
import sys
import time

from PIL import Image

QA = "/home/hatch/workspace/linji-work212/qa212"
sys.path.insert(0, "/home/hatch/workspace/linji-work212/qa188")
import drive188 as d

d.ROOT = "/home/hatch/workspace/linji-work212"
d.QA = QA
d.SHOTS = os.path.join(QA, "shots212")
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 21290
os.makedirs(d.SHOTS, exist_ok=True)

from playwright.sync_api import sync_playwright

SUSPENSE212 = ["得獎者是……", "今晚呢個獎，屬於……", "結果揭曉——得獎者是……"]

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
               fellows: (n.fellows || []).map(f => ({ star: f.star || '', title: f.title || '' })),
               winner: (n.winner && { star: n.winner.star || '', title: n.winner.title || '' }) || null })) : null,
             beatsTotal: beats ? beats.reduce((a, b) => a + (b.ms || 0), 0) : null,
             beatsN: beats ? beats.length : 0,
             suspense: beats ? beats.filter(b => b.id === 'suspense').map(b => b.caption) : null };
  } catch(e) { return { error: String(e) }; }
}"""

JS_STAGE_FULL = """() => {
  const st = document.querySelector('.awd62-stage');
  if (!st) return { present: false };
  const cap = st.querySelector('.awd62-caption');
  const board = st.querySelector('.awd181-board .awd181-t');
  const sub = st.querySelector('.awd181-board .awd181-sub, .awd181-sub');
  const shown = st.querySelectorAll('.awd63-card.show').length;
  const total = st.querySelectorAll('.awd63-card').length;
  const glam = st.querySelector('.awd63-glamour');
  const cards = st.querySelector('.awd63-cards');
  const skip = st.querySelector('.awd62-skip');
  const glamCap = st.querySelector('.awd63-glamour .cap');
  let cardsVis = '', cardsPrev = false, cardsOn = false;
  if (cards) { const cs = getComputedStyle(cards); cardsVis = cs.visibility; cardsPrev = cards.classList.contains('preview212'); cardsOn = cards.classList.contains('on'); }
  let skipDisp = '', skipVis = false;
  if (skip) { skipDisp = getComputedStyle(skip).display; skipVis = skip.offsetParent !== null && skipDisp !== 'none'; }
  return { present: true, caption: cap ? cap.textContent : '', board: board ? board.textContent : '',
           boardSub: sub ? sub.textContent : '',
           shownCards: shown, totalCards: total,
           glamOn: !!(glam && glam.classList.contains('on')),
           glamCap: glamCap ? glamCap.textContent.replace(/\\s+/g, ' ').trim() : '',
           cardsVis, cardsPrev, cardsOn, skipDisp, skipVis };
}"""

JS_RECTS = """() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
             bottom: Math.round(b.bottom), right: Math.round(b.right) }; };
  const st = document.querySelector('.awd62-stage');
  if (!st) return { present: false };
  const frame = st.querySelector('.awd62-frame');
  const cv = st.querySelector('canvas.awd62-canvas');
  const cap = st.querySelector('.awd62-caption');
  const skip = st.querySelector('.awd62-skip');
  const cards = st.querySelector('.awd63-cards');
  const glamCap = st.querySelector('.awd63-glamour .cap');
  return { present: true, vh: window.innerHeight, vw: window.innerWidth,
    stage: r(st), frame: r(frame), canvas: r(cv), caption: r(cap), skip: r(skip),
    cards: r(cards), glamCapRect: r(glamCap),
    glamCapText: glamCap ? glamCap.textContent.replace(/\\s+/g, ' ').trim() : '',
    skipDisp: skip ? getComputedStyle(skip).display : '',
    skipVisible: skip ? (skip.offsetParent !== null && getComputedStyle(skip).display !== 'none') : false,
    captionText: cap ? cap.textContent : '' };
}"""

JS_RESULT_TOAST = """() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
             bottom: Math.round(b.bottom), right: Math.round(b.right) }; };
  const modal = document.querySelector('#modal');
  const inner = document.getElementById('modal-inner');
  const sheet = document.querySelector('.awd-sheet');
  if (!modal || !sheet) return { present: false };
  return { present: true, vh: window.innerHeight,
    modal: r(modal), sheet: r(sheet),
    modalInnerScrollH: inner ? inner.scrollHeight : null,
    modalInnerClientH: inner ? inner.clientHeight : null,
    sheetText: (sheet.innerText || '').slice(0, 1500) };
}"""

JS_MAP_LABEL = """() => {
  const els = Array.from(document.querySelectorAll('#map-names68 .mn68'));
  const out = els.map(el => { const b = el.getBoundingClientRect();
    return { text: el.textContent, x: Math.round(b.x), y: Math.round(b.y),
             w: Math.round(b.width), h: Math.round(b.height) }; });
  const wrap = document.querySelector('#map-names68');
  const wb = wrap ? wrap.getBoundingClientRect() : null;
  return { labels: out, wrap: wb ? { x: Math.round(wb.x), y: Math.round(wb.y),
    w: Math.round(wb.width), h: Math.round(wb.height) } : null };
}"""


def force_pack_try(pg, cer, tier, want_outcome=None, max_seed=30):
    fp = {"error": "no try"}
    for seed in range(1, max_seed + 1):
        pg.evaluate(JS_SEEDED_RANDOM, seed)
        fp = pg.evaluate(JS_FORCE_PACK, {"id": cer, "tier": tier})
        if "error" in fp:
            return fp, seed
        if want_outcome is None or fp.get("bestOutcome") == want_outcome:
            return fp, seed
    return fp, max_seed


def classify(cap):
    if cap.startswith("—— ") and cap.endswith(" ——"):
        return "catTitle"
    if "入圍名單" in cap:
        return "nominee"
    if cap in SUSPENSE212:
        return "suspense"
    if "得獎" in cap:
        return "reveal"
    if "接過獎盃" in cap:
        return "walkup"
    if "差少少啫" in cap or "下年，我要自己行上台" in cap:
        return "comfort"
    if cap.startswith("—— ") or "維港影藝獎" in cap or "金碟夜" in cap:
        return "open"
    return "other"


def watch_beats(pg, secs=75, shots=None, name=""):
    """每 ~60ms 採樣：caption／board／出卡數／卡列 preview／跳過掣可見／glamour。
    C2：記低每句提名字幕第一次見到嗰刻＋同一句第一次 shown>=1 嗰刻，計 lag。
    glamour 第一次見到嗰陣等 900ms 影 glamour 探針＋量 skip／cap。
    walkup 第一次見到「接過獎盃」嗰陣等 450ms／1400ms 各影一張。"""
    samples = []
    boards = []
    board_subs = []
    cap_max = {}
    cap_first_seen = {}
    cap_first_shown = {}
    beat_rects = {}
    glam_seen = False
    glam_probe = None
    shot_done = set()
    last_key = None
    walkup_shots = []
    t0 = time.time()
    gone_at = None
    shots = shots or []
    while time.time() - t0 < secs:
        st = pg.evaluate(JS_STAGE_FULL)
        if not st.get("present"):
            gone_at = round((time.time() - t0) * 1000)
            break
        now_ms = round((time.time() - t0) * 1000)
        cap = st.get("caption") or ""
        shown = st.get("shownCards") or 0
        if st.get("glamOn"):
            glam_seen = True
            if glam_probe is None:
                pg.wait_for_timeout(900)
                d.shot(pg, f"r212_{name}_glamour.png")
                glam_probe = pg.evaluate(JS_RECTS)
                glam_probe["t_ms"] = round((time.time() - t0) * 1000)
        if "接過獎盃" in cap and len(walkup_shots) < 2:
            if not walkup_shots:
                pg.wait_for_timeout(450)
                d.shot(pg, f"r212_{name}_walkup_mid.png")
                walkup_shots.append({"at": "mid450", "rects": pg.evaluate(JS_RECTS)})
            elif len(walkup_shots) == 1:
                pg.wait_for_timeout(950)
                d.shot(pg, f"r212_{name}_walkup_late.png")
                walkup_shots.append({"at": "late1400", "rects": pg.evaluate(JS_RECTS)})
        if cap not in cap_max or shown > cap_max[cap]:
            cap_max[cap] = shown
        if cap and cap not in cap_first_seen:
            cap_first_seen[cap] = now_ms
        if cap and shown >= 1 and cap not in cap_first_shown:
            cap_first_shown[cap] = now_ms
        key = (cap, st.get("board") or "", shown)
        if key != last_key:
            samples.append({"t": now_ms, "caption": cap[:160],
                            "board": key[1], "boardSub": st.get("boardSub") or "",
                            "shown": shown, "total": st.get("totalCards"),
                            "cardsPrev": st.get("cardsPrev"), "cardsVis": st.get("cardsVis"),
                            "skipVis": st.get("skipVis"), "kind": classify(cap)})
            last_key = key
            bt = classify(cap)
            if bt not in beat_rects:
                try:
                    beat_rects[bt] = pg.evaluate(JS_RECTS)
                except Exception:
                    pass
        for substr, fname in shots:
            if substr not in shot_done and substr in cap:
                shot_done.add(substr)
                pg.wait_for_timeout(350)
                d.shot(pg, fname)
                # v20a212 探針修正：headless_shell 截圖有機會攞到 stale frame（DOM 已
                # preview 但畫面仲係舊幀；實測第一次截圖卡列區 mean 17.6／max 19，同
                # 全空一樣）。等多 150ms、caption 仲係同一句先補影多一張覆蓋，確保係新幀。
                try:
                    st2 = pg.evaluate(JS_STAGE_FULL)
                    if (st2.get("caption") or "") == cap:
                        pg.wait_for_timeout(150)
                        d.shot(pg, fname)
                except Exception:
                    pass
                try:
                    beat_rects["shot_" + fname] = pg.evaluate(JS_RECTS)
                except Exception:
                    pass
        b = st.get("board") or ""
        if b and b not in boards:
            boards.append(b)
        bs = st.get("boardSub") or ""
        if bs and bs not in board_subs:
            board_subs.append(bs)
        pg.wait_for_timeout(60)
    nom_lag = {}
    for c, t0c in cap_first_seen.items():
        if "入圍名單" in c:
            nom_lag[c[:80]] = (cap_first_shown.get(c) - t0c) if c in cap_first_shown else None
    return {"samples": samples, "boards": boards, "boardSubs": board_subs,
            "cap_max_shown": cap_max, "beatRects": beat_rects,
            "glamSeen": glam_seen, "glamProbe": glam_probe, "walkupShots": walkup_shots,
            "nomLagMs": nom_lag,
            "totalMs": gone_at if gone_at is not None else round((time.time() - t0) * 1000),
            "stageGone": gone_at is not None}


def wait_board(pg, label, timeout_ms=90000):
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout_ms:
        st = pg.evaluate(JS_STAGE_FULL)
        if not st.get("present"):
            return False
        if (st.get("board") or "") == label:
            return True
        pg.wait_for_timeout(60)
    return False


def analyse_timeline(w, night_labels, night):
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
    rev_caps = [s["caption"] for s in samples if "得獎" in s["caption"] and s["caption"] not in SUSPENSE212]
    ck["reveal_beats_seen"] = len(rev_caps) == len(night_labels)
    sus_caps = [s["caption"] for s in samples if s["caption"] in SUSPENSE212]
    ck["suspense_beats_seen"] = len(sus_caps) == len(night_labels)
    open_caps = [s["caption"] for s in samples if s["kind"] == "open"]
    ck["open_beat_once"] = len(open_caps) == 1

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
            ck["player_nominee_beats_n"] = True
            ck["player_first_nominee_is_awei"] = True
            ck["cards_one_by_one_focus_cat"] = stepwise_for(fl["label"], nom_n(fl))
    # C1：格標題嗰陣卡列預覽（preview212＋visible），唔再全空
    title_samples = [s for s in samples if s["caption"].startswith("—— ") and s["caption"].endswith(" ——")]
    ck["cards_preview_at_cat_title"] = bool(title_samples) and all(
        s.get("cardsPrev") and s.get("cardsVis") == "visible" for s in title_samples)
    # C2：提名 beat 字幕→卡片 lag（同一句第一次見到 → 第一次 shown>=1）
    lags = [v for v in (w.get("nomLagMs") or {}).values() if v is not None]
    ck["nominee_card_lag_max_le_250ms"] = bool(lags) and max(lags) <= 250
    ck["nominee_card_lag_all_seen"] = len(lags) == len(nom_caps)
    return ck


def slot_cxs(n):
    if n == 3:
        return [75, 240, 405]
    if n == 2:
        return [200, 280]
    return [round(240 + (i - (n - 1) / 2) * 120) for i in range(n)]


def side_band_lum(shot_name, rects, cxs):
    """C3：宣佈嗰位身邊光柱帶亮度——人物左邊 14px 闊背景帶（腳底上 115px 高），
    唔計人物本身，淨量光柱有冇照亮背景。"""
    try:
        im = Image.open(os.path.join(d.SHOTS, shot_name)).convert("RGB")
        cv = rects["canvas"]; fr = rects["frame"]
        feet = cv["y"] + 314 / 432 * cv["h"]
        out = {}
        for i, cx in enumerate(cxs):
            x0 = int(fr["x"] + cx / 480 * fr["w"])
            box = (x0 - 40, int(feet - 115), x0 - 26, int(feet))
            px = list(im.crop(box).getdata())
            mean = tuple(sum(c[j] for c in px) / len(px) for j in range(3))
            out[f"slot{i}"] = round(0.299 * mean[0] + 0.587 * mean[1] + 0.114 * mean[2], 1)
        return out
    except Exception as e:
        return {"error": repr(e)}


def figure_centers(shot_name, rects):
    """C5：台上人物左右中心（邏輯座標）——figure band 逐欄平均亮度，人物欄明顯暗過背景簾／地板。"""
    try:
        im = Image.open(os.path.join(d.SHOTS, shot_name)).convert("RGB")
        cv = rects["canvas"]; fr = rects["frame"]
        feet = cv["y"] + 314 / 432 * cv["h"]
        top = int(feet - 115)
        bot = int(feet)
        x0 = fr["x"]; x1 = fr["x"] + fr["w"]
        cols = []
        for x in range(x0, x1):
            px = list(im.crop((x, top, x + 1, bot)).getdata())
            m = sum(0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in px) / len(px)
            cols.append(m)
        base = sorted(cols)[int(len(cols) * 0.8)]
        dark = [i for i, m in enumerate(cols) if m < base - 25]
        groups = []
        for i in dark:
            if groups and i - groups[-1][-1] <= 4:
                groups[-1].append(i)
            else:
                groups.append([i])
        groups = [g for g in groups if len(g) >= 8]
        # v20a212 探針修正：左右紅幕布係暗欄，會喺 frame 邊緣生出假 group——
        # 掟走掂住 frame 左右邊嘅 group（真人唔會企到貼邊；figures 實測 199／278）。
        edge_dropped = [g for g in groups if g[0] != 0 and g[-1] != len(cols) - 1]
        if edge_dropped:
            groups = edge_dropped
        centers = [round((fr["x"] + (g[0] + g[-1]) / 2 - fr["x"]) / fr["w"] * 480) for g in groups]
        return {"centers_logical": centers, "base": round(base, 1), "groups_px": [[g[0], g[-1]] for g in groups]}
    except Exception as e:
        return {"error": repr(e)}


def cards_zone_bright(shot_name, rects):
    """C1：卡列區亮像素比例（對照 v208：全空 ~2.5%，有卡 13–22%，>120 閾值）。
    v20a212 探針修正：preview 卡係 opacity 0.22 dimmed，亮度上限 ~66，>120 永遠 0%——
    改用 >50 閾值（實測 preview ≈31.7%，全空 0.0%，full 卡 12–15%）。"""
    try:
        im = Image.open(os.path.join(d.SHOTS, shot_name)).convert("RGB")
        cd = rects["cards"]
        if not cd:
            return {"error": "no cards rect"}
        box = (cd["x"], cd["y"], cd["x"] + cd["w"], cd["y"] + cd["h"])
        px = list(im.crop(box).getdata())
        bright = sum(1 for c in px if 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] > 120)
        dim = sum(1 for c in px if 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] > 50)
        return {"bright_pct": round(100.0 * bright / max(1, len(px)), 2),
                "dim_pct": round(100.0 * dim / max(1, len(px)), 2)}
    except Exception as e:
        return {"error": repr(e)}


CASES = [
    ("film_nom_932", "award_harbour_film", 1990, "nominee", 932, 25, 0,
     {"film_lead": 1, "film_sup": 1}, "nominated", "attend"),
    ("film_won_932", "award_harbour_film", 1990, "nominee", 932, 80, 60,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2, "tv_sup": 1, "ad_lead": 1}, "won", "attend"),
    ("film_won_700", "award_harbour_film", 1990, "nominee", 700, 80, 60,
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
            # B1：同一晚得主組合唔重複（玩家格 won 除外，得主係阿偉）
            win_keys = []
            for n in night:
                w = n.get("winner")
                if w:
                    win_keys.append((w.get("star") or "") + "|" + (w.get("title") or ""))
            out["winner_keys"] = win_keys
            out["checks"]["b1_winners_distinct"] = len(win_keys) == len(set(win_keys))
            sus = fp.get("suspense") or []
            out["suspense_caps"] = sus
            out["checks"]["b1_suspense_not_all_same"] = len(sus) >= 2 and len(set(sus)) >= 2
            focus = [n for n in night if n.get("isFocus")]
            focus_label = focus[0]["label"] if focus else ""
            out["focus_label"] = focus_label
            inv = d.present(pg)
            out["invite"] = inv
            out["checks"]["invite_shown"] = bool(inv.get("visible"))
            d.shot(pg, f"r212_{name}_invite.png")
            if not inv.get("visible"):
                out["pageerrors"] = errs[:8]
                out["checks"]["zero_pageerror"] = len(errs) == 0
                out["verdict"] = "FAIL"
                results[name] = out
                print("  FAIL no invite", flush=True)
                return
            if mode == "decline":
                d.click_vis(pg, "推辭")
                pg.wait_for_timeout(400)
                out["checks"]["stage_appears"] = bool(d.stage_state(pg).get("present"))
                w = watch_beats(pg, 75, [("—— 最佳廣告女主角 ——", f"r212_{name}_cat2.png"),
                                         ("2/3 · 最佳廣告女主角", f"r212_{name}_nom.png")], name)
                out["watch"] = w
                out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
                out["checks"].update(analyse_timeline(w, night_labels, night))
                out["checks"]["boards_in_order"] = w["boards"] == EXPECTED_BOARDS.get(cer, [])
                exp_total = fp.get("beatsTotal")
                out["expected_total_ms"] = exp_total
                out["checks"]["total_duration_close"] = (
                    exp_total is not None and abs(w["totalMs"] - exp_total) <= 5000)
                # C1：格標題截圖卡列區亮像素
                r2 = w["beatRects"].get("shot_r212_ad_dec_932_cat2.png") or {}
                if r2.get("present"):
                    out["c1_cat_title_cards_bright"] = cards_zone_bright(f"r212_{name}_cat2.png", r2)
                    out["checks"]["c1_cat_title_not_empty"] = (out["c1_cat_title_cards_bright"].get("dim_pct") or 0) > 5
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
                d.shot(pg, f"r212_{name}_after.png")
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
                    d.shot(pg, f"r212_{name}_cat2_title.png")
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
                d.shot(pg, f"r212_{name}_result.png")
                out["result_toast"] = pg.evaluate(JS_RESULT_TOAST)
            else:  # attend
                d.click_vis(pg, "出席")
                pg.wait_for_timeout(400)
                out["checks"]["stage_appears"] = bool(d.stage_state(pg).get("present"))
                shots = []
                if name == "film_nom_932":
                    shots = [("入圍名單 1/4", f"r212_{name}_nom1.png"),
                             ("入圍名單 2/4", f"r212_{name}_nom2.png"),
                             ("差少少", f"r212_{name}_reveal.png"),
                             ("差少少啫", f"r212_{name}_comfort.png")]
                elif name in ("film_won_932", "film_won_700"):
                    shots = [("入圍名單 1/4", f"r212_{name}_nom1.png"),
                             ("得獎！", f"r212_{name}_reveal.png")]
                elif name == "music_gal_932":
                    shots = [("· 最佳女歌手", f"r212_{name}_nom.png"),
                             ("—— 最佳男歌手 ——", f"r212_{name}_lastcat.png"),
                             ("得獎", f"r212_{name}_reveal.png")]
                w = watch_beats(pg, 75, shots, name)
                out["watch"] = w
                out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
                out["checks"].update(analyse_timeline(w, night_labels, night))
                out["checks"]["boards_in_order"] = w["boards"] == EXPECTED_BOARDS.get(cer, [])
                exp_total = fp.get("beatsTotal")
                out["expected_total_ms"] = exp_total
                out["checks"]["total_duration_close"] = (
                    exp_total is not None and abs(w["totalMs"] - exp_total) <= 5000)
                # A1：glamour 探針——跳過掣收起＋cap 全文
                if w.get("glamSeen"):
                    gp = w.get("glamProbe") or {}
                    out["glam_probe"] = gp
                    out["checks"]["a1_skip_hidden_during_glamour"] = gp.get("skipVisible") is False
                    out["checks"]["a1_skip_display_none"] = gp.get("skipDisp") == "none"
                    cap = gp.get("glamCapText") or ""
                    out["checks"]["a1_glam_cap_full"] = "《新春大吉》" in cap and "最佳男配角" in cap
                    # glamour 完咗之後跳過掣返嚟（下一格 catTitle／out 嗰陣再探）
                    after = pg.evaluate("""() => {
                      const s = document.querySelector('.awd62-stage');
                      return { stageGone: !s }; }""")
                    out["checks"]["a1_stage_ended_normally"] = bool(w.get("stageGone"))
                if mode == "attend" and want_outcome == "won":
                    caps = [s["caption"] for s in w["samples"]]
                    out["checks"]["walkup_caption_seen"] = any("接過獎盃" in c for c in caps)
                    out["checks"]["glamour_overlay_seen"] = bool(w.get("glamSeen"))
                    audio = pg.evaluate("() => window.__awards160Audio || null")
                    out["audio_flag"] = audio
                    out["checks"]["fanfare_attempted"] = bool(audio) and audio.get("fanfare") in ("attempted", "playing", "blocked")
                    # C4：walkup 兩張截圖齊（mid／late），目視＋量度留畀分析
                    out["checks"]["c4_walkup_shots_taken"] = len(w.get("walkupShots") or []) == 2
                if mode == "attend" and want_outcome == "nominated":
                    caps = [s["caption"] for s in w["samples"]]
                    out["checks"]["comfort_caption_seen"] = any("差少少啫" in c for c in caps)
                pg.wait_for_timeout(600)
                res = d.modal_info(pg)
                out["result_card"] = res
                out["checks"]["result_card_shown"] = bool(res.get("visible"))
                if res.get("visible") and focus_label:
                    out["checks"]["result_card_names_focus_cat"] = focus_label in (res.get("body") or "")
                d.shot(pg, f"r212_{name}_result.png")
                out["result_toast"] = pg.evaluate(JS_RESULT_TOAST)
                # C3：提名 spotlight 光柱帶亮度（nom1 阿偉 slot1 宣佈 vs nom2 陸柏言 slot0 宣佈）
                if name == "film_nom_932":
                    cxs = slot_cxs(4)
                    r1 = w["beatRects"].get("shot_r212_film_nom_932_nom1.png") or {}
                    r2 = w["beatRects"].get("shot_r212_film_nom_932_nom2.png") or {}
                    out["c3_sideband_nom1"] = side_band_lum("r212_film_nom_932_nom1.png", r1, cxs) if r1.get("present") else {"error": "no rects"}
                    out["c3_sideband_nom2"] = side_band_lum("r212_film_nom_932_nom2.png", r2, cxs) if r2.get("present") else {"error": "no rects"}
                    l1 = out["c3_sideband_nom1"]; l2 = out["c3_sideband_nom2"]
                    try:
                        # 同一 slot：宣佈嗰陣 vs 未宣佈嗰陣——光柱帶應該光啲
                        out["checks"]["c3_spotlight_brighter_when_announced"] = (
                            l2.get("slot0", 0) > l1.get("slot0", 0) and l1.get("slot1", 0) > l2.get("slot1", 0))
                    except Exception:
                        out["checks"]["c3_spotlight_brighter_when_announced"] = False
                # C5：音樂女歌手格 2 位提名人置中（figure centers ≈ 200／280）
                if name == "music_gal_932":
                    rn = w["beatRects"].get("shot_r212_music_gal_932_nom.png") or {}
                    if rn.get("present"):
                        out["c5_figure_centers"] = figure_centers("r212_music_gal_932_nom.png", rn)
                        cs5 = (out["c5_figure_centers"] or {}).get("centers_logical") or []
                        out["checks"]["c5_two_figures_centered"] = (
                            len(cs5) == 2 and abs(cs5[0] - 200) <= 25 and abs(cs5[1] - 280) <= 25)
                # C1：格標題截圖卡列區亮像素（music 尾格）
                if name == "music_gal_932":
                    rl = w["beatRects"].get("shot_r212_music_gal_932_lastcat.png") or {}
                    if rl.get("present"):
                        out["c1_lastcat_cards_bright"] = cards_zone_bright("r212_music_gal_932_lastcat.png", rl)
                        out["checks"]["c1_lastcat_not_empty"] = (out["c1_lastcat_cards_bright"].get("dim_pct") or 0) > 5
                if res.get("visible"):
                    d.click_vis(pg, "收下這晚")
                    pg.wait_for_timeout(900)
                    nq = d.newspaper_award(pg)
                    out["newspaper"] = nq
                    aw = [n for n in nq if "award" in (n.get("source") or "").lower()
                          or "頒獎" in (n.get("headline") or "")]
                    out["checks"]["newspaper_has_award"] = len(aw) >= 1
                    d.shot(pg, f"r212_{name}_paper.png")
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


def run_map_case(pw):
    print("== map_932 ==", flush=True)
    out = {"case": "map_932", "checks": {}}
    errs = []
    b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
    try:
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        if not d.new_game(pg):
            out["error"] = "new_game fail"
            return out
        d.click_vis(pg, "返回地圖")
        pg.wait_for_timeout(800)
        for _ in range(60):
            act = pg.evaluate("""() => {
              const nxt = [...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='下一句' && e.offsetParent);
              if (nxt) { nxt.click(); return 'next'; }
              const ch = [...document.querySelectorAll('*')].filter(e=>e.children.length===0 && e.offsetParent && getComputedStyle(e).cursor==='pointer').find(e=>/跟張子駿|接電影散工/.test(e.textContent));
              if (ch) { ch.click(); return 'choice'; }
              const cl = [...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='關閉' && e.offsetParent);
              if (cl) { cl.click(); return 'close'; }
              return 'none'; }""")
            if act == 'none':
                break
            pg.wait_for_timeout(450)
        pg.wait_for_timeout(1000)
        out["map_labels"] = pg.evaluate(JS_MAP_LABEL)
        out["story_overlay_gone"] = pg.evaluate(
            "() => ![...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='下一句' && e.offsetParent)")
        d.shot(pg, "r212_map_932.png")
        labs = (out["map_labels"] or {}).get("labels") or []
        out["checks"]["map_has_15_labels"] = len(labs) == 15
        out["checks"]["no_story_overlay"] = bool(out.get("story_overlay_gone"))
        out["pageerrors"] = errs[:5]
        out["checks"]["zero_pageerror"] = len(errs) == 0
        return out
    finally:
        try:
            ctx.close()
        except Exception:
            pass
        b.close()


def main():
    srv = d.serve()
    results = {}
    try:
        with sync_playwright() as pw:
            for cfg in CASES:
                run_case(pw, cfg, results)
            results["map_932"] = run_map_case(pw)
        with open(os.path.join(QA, "drive212.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print("== DRIVE212 DONE ==", flush=True)
        npass = 0
        for k, v in results.items():
            bad = {kk: vv for kk, vv in (v.get("checks") or {}).items() if not vv}
            ok = not bad and not v.get("error")
            npass += 1 if ok else 0
            print(f"  {k}: {'PASS' if ok else 'FAIL'} bad={json.dumps(bad, ensure_ascii=False)}"
                  f" errs={v.get('pageerrors')}", flush=True)
        print(f"== SUMMARY {npass}/{len(results)} cases PASS ==", flush=True)
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
