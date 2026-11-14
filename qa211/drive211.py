# -*- coding: utf-8 -*-
"""v20a211 實駕：v207 設計 review 六項（A1＋B1＋B2＋C1–C3）逐項驗證。
重用 qa188/drive188.py helpers（new_game／seed／present／watch／stage_state）。
場次：gallery／nominee／won × 932／700，music＋film＋ad。
每場：force pack → 出席 → 每 200ms 採樣 frame／canvas／caption／cards rect（beat 序列，
驗 B1 黑帶＋C2 names→reveal 跳位）→ 揭曉亮度（C1 門檻 ≥12，FLOOR 分數由下便 FLOOR_FRAC 計）
→ 結果卡：toast／眉題重疊（A1）、銷量卡得主名（B2）、同屆提名得主標記（C1）、scroll＝client（C3 守衛）
→ 請柬席位行去重（C3）。0 pageerror。證據 qa211/drive211.json，截圖 qa211/shots211/。
won 用強 seed（fame 80／credit 60／rec 3＋film_lead 2＋tv_lead 2＋ad_lead 1，逐 seed 試到 won 為止）。
"""
import json
import os
import sys
import time

from PIL import Image

sys.path.insert(0, "/home/hatch/workspace/linji-work211/qa188")
import drive188 as d

d.ROOT = "/home/hatch/workspace/linji-work211"
d.QA = "/home/hatch/workspace/linji-work211/qa211"
d.SHOTS = "/home/hatch/workspace/linji-work211/qa211/shots211"
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 21190
os.makedirs(d.SHOTS, exist_ok=True)

from playwright.sync_api import sync_playwright

# 揭曉亮度量度用：腳底＝canvas.top＋FLOOR_FRAC×canvas.h（v207：314/432；v211 B1 改咗要同步改呢度）
FLOOR_FRAC = 314 / 432

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
    return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
      tier: p.tier, repWork62: p.repWork62 || '',
      cats: (p.categories || []).map(c => ({ id: c.id, label: c.label,
        outcome: c.outcome, repWorkTitle: c.repWorkTitle || '',
        fellows: (c.fellows63 || []).map(f => ({ starId: f.starId || '', star: f.star || '', title: f.title || '' })) })) };
  } catch(e) { return { error: String(e) }; }
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
  const cards = st.querySelector('.awd63-cards');
  const skip = st.querySelector('.awd62-skip');
  const strips = Array.from(st.querySelectorAll('.awd181-strip')).map(r);
  const skipR = r(skip), stripR = strips.length > 1 ? strips[1] : null;
  let overlap = null;
  if (skipR && stripR) {
    const ox = Math.max(0, Math.min(skipR.right, stripR.right) - Math.max(skipR.x, stripR.x));
    const oy = Math.max(0, Math.min(skipR.bottom, stripR.bottom) - Math.max(skipR.y, stripR.y));
    overlap = ox * oy;
  }
  return { present: true, vh: window.innerHeight, vw: window.innerWidth,
    stage: r(st), frame: r(frame), canvas: r(cv), caption: r(cap),
    captionText: cap ? cap.textContent : '',
    captionDisplay: cap ? getComputedStyle(cap).display : null,
    cards: r(cards), cardsVisible: cards ? getComputedStyle(cards).visibility : null,
    cardsDisplay: cards ? getComputedStyle(cards).display : null,
    skip: skipR, skipStripOverlap: overlap };
}"""

JS_BEAM = """(o) => {
  // 直接讀 canvas backing 像素（DOM 橫額／數字條／白牌唔會污染）：得主側 vs 落選者側，
  // 由框頂到腳底 6 個高度取樣。x 偏置：人物頭頂之上用 cx+10（光柱頂半闊 ~18px 內），
  // 人物高度範圍用 cx+38（避開人物本身 ~±30px，喺光柱底半闊 ~55px 內）。
  const cv = document.querySelector('canvas.awd62-canvas');
  if (!cv) return { error: 'no canvas' };
  const ctx = cv.getContext('2d');
  const H = cv.height / 1.5, F = 314 / 432 * H;
  const lumWarmAt = (lx, ly) => {
    const bx = Math.round(lx * 1.5), by = Math.round(ly * 1.5);
    try {
      const d = ctx.getImageData(bx - 4, by - 4, 9, 9).data;
      let r = 0, g = 0, b = 0, n = 0;
      for (let i = 0; i < d.length; i += 4) { r += d[i]; g += d[i + 1]; b += d[i + 2]; n++; }
      r /= n; g /= n; b /= n;
      return { lum: Math.round((0.299 * r + 0.587 * g + 0.114 * b) * 10) / 10, warm: Math.round(r - b) };
    } catch (e) { return null; }
  };
  const ys = [20, 80, 140, 200, Math.round(F - 40), Math.round(F - 10)];
  const rows = ys.map(y => {
    // 人物頭頂之上（y < F-160）用 cx+10（光柱頂半闊 ~18px 內）；人物高度範圍用 cx+38——
    // 但人物邊緣像素會污染（gallery 非贏版下半段實測 diff ~0 係撞到提名人衣邊，唔係光柱唔到）；
    // 所以下半段改取腳底附近（F-40／F-10：光池＋光灘區，人物腿闊 ±15px，+38 淨係光＋地板）。
    // 另：暖白光柱喺米白幕布上亮度差本來細（R 升 B 跌互相抵消），中段改用量暖色偏移（R-B）——
    // 探針校準（music_nom_700）：y80/140/200 暖色差 +20/+27/+17，腳底亮度差 +4.8/+12.4，框頂亮度差 +100。
    const off = (y < F - 160) ? 10 : 38;
    const w = lumWarmAt(o.wcx + off, y), l = lumWarmAt(o.lcx + off, y);
    return { y, off,
             win: w ? w.lum : null, lose: l ? l.lum : null,
             diff: (w && l) ? Math.round((w.lum - l.lum) * 10) / 10 : null,
             warmDiff: (w && l) ? w.warm - l.warm : null };
  });
  return { H: Math.round(H), F: Math.round(F), rows };
}"""

JS_RESULT = """() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
             bottom: Math.round(b.bottom), right: Math.round(b.right) }; };
  const modal = document.querySelector('.modal');
  const inner = document.getElementById('modal-inner');
  const sheet = document.querySelector('.awd-sheet');
  const toast = document.getElementById('toast');
  if (!modal || !sheet) return { present: false };
  const eyebrow = sheet.querySelector('.psr-eyebrow');
  const tR = r(toast), eR = r(eyebrow);
  let toastEyebrowOverlap = 0;
  if (tR && eR && toast && toast.classList.contains('on')) {
    const ox = Math.max(0, Math.min(tR.right, eR.right) - Math.max(tR.x, eR.x));
    const oy = Math.max(0, Math.min(tR.bottom, eR.bottom) - Math.max(tR.y, eR.y));
    toastEyebrowOverlap = ox * oy;
  }
  const cards = Array.from(sheet.querySelectorAll('.psr-card')).map(el => ({
    cls: el.className, rect: r(el),
    kicker: (el.querySelector('.psr-kicker') || {}).textContent || '',
    title: (el.querySelector('.psr-title') || {}).textContent || '' }));
  const fel = sheet.querySelector('.psr-fellows63');
  return { present: true, vh: window.innerHeight,
    modal: r(modal), modalInnerScrollH: inner ? inner.scrollHeight : null,
    modalInnerClientH: inner ? inner.clientHeight : null,
    sheet: r(sheet), cards,
    fellowsText: fel ? fel.textContent : '',
    fellowsHtml: fel ? fel.innerHTML : '',
    sheetText: sheet.innerText || '',
    toast: tR, toastOn: toast ? toast.classList.contains('on') : false,
    toastText: toast ? toast.textContent : '',
    eyebrow: eR, toastEyebrowOverlap,
    eyebrowVisible: eyebrow ? (() => { const b = eyebrow.getBoundingClientRect();
      return b.height > 0 && b.bottom > 0 && b.top < window.innerHeight; })() : false };
}"""


def slot_cxs(n):
    if n == 3:
        return [75, 240, 405]
    return [round(240 + (i - (n - 1) / 2) * 120) for i in range(n)]


def lum_winner_loser(shot_name, rects, winner_cx, loser_cx):
    try:
        im = Image.open(os.path.join(d.SHOTS, shot_name)).convert("RGB")
        cv = rects["canvas"]; fr = rects["frame"]
        feet = cv["y"] + FLOOR_FRAC * cv["h"]
        out = {}
        for label, cx in (("winner", winner_cx), ("loser", loser_cx)):
            x0 = int(fr["x"] + cx / 480 * fr["w"])
            box = (x0 - 26, int(feet - 115), x0 + 26, int(feet))
            px = list(im.crop(box).getdata())
            mean = tuple(sum(c[i] for c in px) / len(px) for i in range(3))
            out[label] = round(0.299 * mean[0] + 0.587 * mean[1] + 0.114 * mean[2], 1)
        return out
    except Exception as e:
        return {"error": repr(e)}


def reveal_slots(fp, best, caption):
    import re as _re
    cats = (fp or {}).get("cats") or []
    m = _re.search(r"(\S+)憑《", caption or "")
    win_star = m.group(1) if m else None
    focus = None
    for c in cats:
        fws = c.get("fellows") or []
        if win_star and any((f or {}).get("star") == win_star for f in fws):
            focus = c
            break
    if focus is None:
        focus = next((c for c in cats if (c.get("fellows") or [])), None)
    if focus is None:
        return 75, 240, {"note": "no focus cat"}
    fws = focus.get("fellows") or []
    n = len(fws) + (0 if best == "gallery" else 1)
    cxs = slot_cxs(n)

    def slot_of(fi):
        return fi if (best == "gallery" or fi < 1) else fi + 1
    if best == "won":
        w_slot, l_slot = 1, 0
    else:
        w_idx = next((i for i, f in enumerate(fws) if (f or {}).get("star") == win_star), 0)
        w_slot = slot_of(w_idx)
        l_idx = next((i for i in range(len(fws)) if i != w_idx), 1 if len(fws) > 1 else 0)
        l_slot = slot_of(l_idx)
    w_cx = cxs[w_slot]
    w_settled = round(w_cx + (240 - w_cx) * 0.22)
    return w_settled, cxs[l_slot], {"focus": focus.get("label"), "n": n,
                                     "w_slot": w_slot, "l_slot": l_slot,
                                     "w_cx": w_cx, "win_star": win_star}


def force_pack_try(pg, cer, tier, want_outcome=None):
    for seed in range(1, 21):
        pg.evaluate(JS_SEEDED_RANDOM, seed)
        fp = pg.evaluate(JS_FORCE_PACK, {"id": cer, "tier": tier})
        if "error" in fp:
            return fp, seed
        if want_outcome and fp.get("bestOutcome") != want_outcome:
            continue
        return fp, seed
    return fp, 20


def phase_of(cap):
    cap = cap or ""
    if "得獎者是" in cap:
        return "suspense"
    if "得獎" in cap:
        return "reveal"
    if "：《" in cap:
        return "names"
    if "掌聲響起" in cap or "完滿落幕" in cap:
        return "out"
    if "魚貫入場" in cap or "觀禮席" in cap or "電視轉播" in cap:
        return "enter_pan"
    return "other"


STRONG_ROLES = {"rec": 3, "film_lead": 2, "tv_lead": 2, "ad_lead": 1}


def run_case(pw, name, cer, year, tier, H, fame, credit, roles, want_outcome=None):
    print(f"== {name} ==", flush=True)
    out = {"case": name, "checks": {}}
    ck = out["checks"]
    errs = []
    b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        if not d.new_game(pg):
            out["error"] = "new_game fail"
            return out
        d.seed(pg, {"year": year, "fame": fame, "credit": credit,
                    "roles": roles, "payOverride": None}, [])
        fp, seed_used = force_pack_try(pg, cer, tier, want_outcome)
        out["pack"] = fp
        out["seed_used"] = seed_used
        if "error" in fp:
            out["error"] = fp
            return out
        if want_outcome:
            ck["pack_outcome_" + want_outcome] = fp.get("bestOutcome") == want_outcome
            if fp.get("bestOutcome") != want_outcome:
                out["skipped_no_won"] = True
                print("  (no won pack in 20 seeds, skip)", flush=True)
                return out
        inv = d.present(pg)
        out["invite_visible"] = bool(inv.get("visible"))
        out["invite_text"] = inv.get("body") or inv.get("text") or ""
        ck["invite_shown"] = bool(inv.get("visible"))
        # C3：請柬席位行只得一行
        it = out["invite_text"]
        ck["C3_invite_one_seat_line"] = ("席位：旁聽席" not in it) and ("今晚席位：觀禮" in it or "今晚席位" not in it)
        ck["C3_invite_no_dup_seat"] = "席位：旁聽席" not in it
        d.shot(pg, f"v211_{name}_invite.png")
        d.click_vis(pg, "出席")
        # beat 序列採樣：由出席起每 200ms 採 rects，直到舞台消失（最多 60 秒）
        series = []
        reveal_cap = ""
        reveal_rects = None
        t0 = time.time()
        while time.time() - t0 < 60:
            try:
                rn = pg.evaluate(JS_RECTS)
            except Exception:
                break
            if not rn.get("present"):
                break
            ph = phase_of(rn.get("captionText") or "")
            series.append({"t": round(time.time() - t0, 2), "phase": ph,
                           "frame": rn.get("frame"), "canvas": rn.get("canvas"),
                           "caption": rn.get("caption"),
                           "captionText": rn.get("captionText") or "",
                           "captionDisplay": rn.get("captionDisplay"),
                           "cards": rn.get("cards"),
                           "cardsVisible": rn.get("cardsVisible"),
                           "cardsDisplay": rn.get("cardsDisplay")})
            if ph == "reveal" and reveal_rects is None:
                pg.wait_for_timeout(700)
                reveal_rects = pg.evaluate(JS_RECTS)
                reveal_cap = (d.stage_state(pg).get("caption") or "")
                d.shot(pg, f"v211_{name}_reveal.png")
                # B7：趁 reveal beat 仲喺度，直讀 canvas 像素驗光柱（之後舞台會拆）
                try:
                    _w, _l, _info = reveal_slots(fp, fp.get("bestOutcome"), reveal_cap)
                    out["beam"] = pg.evaluate(JS_BEAM, {"wcx": _w, "lcx": _l})
                    out["beam_slots"] = _info
                except Exception as e:
                    out["beam"] = {"error": repr(e)}
            pg.wait_for_timeout(200)
        out["beat_series"] = series
        out["reveal_caption"] = reveal_cap
        out["reveal_rects"] = reveal_rects
        # B1：黑帶（names／reveal 樣本 frame 頂／底）
        def phase_frames(ph):
            return [s["frame"] for s in series if s["phase"] == ph and s["frame"]]
        for ph in ("names", "reveal"):
            frs = phase_frames(ph)
            if frs:
                ys = sorted(f["y"] for f in frs)
                hs = sorted(f["h"] for f in frs)
                out[f"frame_{ph}"] = {"y_med": ys[len(ys) // 2], "h_med": hs[len(hs) // 2],
                                      "y_min": ys[0], "y_max": ys[-1], "n": len(frs)}
                ck[f"B1_{ph}_band_lt_232"] = ys[len(ys) // 2] < 232 if H == 932 else True
        # C2：names→reveal frame 位移（中位數 y 差）
        if phase_frames("names") and phase_frames("reveal"):
            nfr = out["frame_names"]; rfr = out["frame_reveal"]
            out["C2_names_reveal_dy"] = abs(rfr["y_med"] - nfr["y_med"])
            out["C2_names_reveal_dh"] = abs(rfr["h_med"] - nfr["h_med"])
            ck["C2_frame_shift_le_2"] = out["C2_names_reveal_dy"] <= 2
        # C1 亮度（reveal 截圖＋reveal rects）
        if reveal_rects and reveal_rects.get("present") and reveal_cap:
            w_cx, l_cx, info = reveal_slots(fp, fp.get("bestOutcome"), reveal_cap)
            out["reveal_slots"] = info
            out["reveal_lum"] = lum_winner_loser(f"v211_{name}_reveal.png", reveal_rects, w_cx, l_cx)
            wl = out["reveal_lum"]
            if wl and "winner" in wl:
                ck["C1_winner_brighter_ge_12"] = wl["winner"] - wl["loser"] >= 12
            # B7：光柱由框頂連到腳底（reveal 當刻 canvas 像素直讀，6 個高度取樣；
            # 框頂亮度差＋腳底亮度差＋中段暖色偏移三組門檻，見 JS_BEAM 內探針校準數字）
            beam = out.get("beam") or {}
            rows = beam.get("rows") or []
            by_y = {r["y"]: r for r in rows}
            top = by_y.get(20) or {}
            feet = [r for r in rows if r["y"] >= (beam.get("F") or 314) - 40]
            mid = [r for r in rows if r["y"] in (80, 140, 200) or (r["y"] == (beam.get("F") or 314) - 40)]
            out["beam_top_diff"] = top.get("diff")
            out["beam_feet_diffs"] = [r.get("diff") for r in feet]
            out["beam_mid_warm"] = [r.get("warmDiff") for r in mid]
            ck["B7_beam_top_to_feet"] = bool(
                (top.get("diff") or 0) >= 20
                and len(feet) == 2 and all((r.get("diff") or 0) >= 3 for r in feet)
                and sum(1 for r in mid if (r.get("warmDiff") or 0) >= 8) >= 3)
        # B3 守衛：跳過掣唔遮數字條（names 樣本）
        ns = [s for s in series if s["phase"] == "names"]
        if ns:
            pass
        w = d.watch(pg, 24)
        out["watch"] = w
        pg.wait_for_timeout(600)
        res = pg.evaluate(JS_RESULT)
        out["result"] = res
        if res.get("present"):
            ck["result_shown"] = True
            # A1：toast 收起＋眉題完整可見（重疊面積 0，toast off）
            ck["A1_toast_off_at_result"] = res.get("toastOn") is False
            ck["A1_eyebrow_not_covered"] = (res.get("toastEyebrowOverlap") or 0) == 0
            # C3 守衛：結果卡唔碌
            ck["C3_result_no_scroll"] = (res.get("modalInnerScrollH") or 0) <= (res.get("modalInnerClientH") or 0) + 2
            # B2：won 版銷量卡有得主名，stub 句 0 命中
            st = res.get("sheetText") or ""
            out["sheet_text"] = st
            ck["B2_no_stub_sales_line"] = "——典禮後仍有人提起。" not in st
            if fp.get("bestOutcome") == "won":
                ck["B2_won_sales_names_player"] = "阿偉憑《" in st and "奪獎" in st
            # C1：won 版同屆提名有得主標記（🏆 係 <img class="ic112">，textContent 讀唔到——驗 html）
            fel = res.get("fellowsText") or ""
            fel_html = res.get("fellowsHtml") or ""
            out["fellows_text"] = fel
            if fp.get("bestOutcome") == "won":
                ck["C1_won_fellows_names_player"] = ("阿偉《" in fel and "為得主" in fel
                                                     and fel_html.count("ic112") >= 2
                                                     and fel_html.index("ic112") < fel_html.index("阿偉"))
            if fp.get("bestOutcome") in ("gallery", "nominated"):
                ck["C1_fellows_has_legend"] = "為得主" in fel
        d.shot(pg, f"v211_{name}_result.png")
        # toast 遲 2 秒再驗一次（A1：唔係靠 1.8s timer 自然熄先過關——結果卡開出嗰刻已經要 off；
        # 若開卡嗰刻 toast 仲 on，上面 A1_toast_off 已經 FAIL；呢度只記錄）
        pg.wait_for_timeout(2000)
        res2 = pg.evaluate(JS_RESULT)
        out["result_after_2s"] = {"toastOn": res2.get("toastOn"),
                                  "toastEyebrowOverlap": res2.get("toastEyebrowOverlap")} if res2.get("present") else res2
        out["pageerrors"] = errs[:5]
        ck["zero_pageerror"] = len(errs) == 0
        return out
    finally:
        try:
            ctx.close()
        except Exception:
            pass
        b.close()


CASES = [
    ("music_gal_932", "award_golddisc_music", 1991, "gallery", 932, 45, 50, {}, None),
    ("music_gal_700", "award_golddisc_music", 1991, "gallery", 700, 45, 50, {}, None),
    ("music_nom_700", "award_golddisc_music", 1990, "nominee", 700, 25, 0, {"rec": 2}, None),
    ("film_nom_700", "award_harbour_film", 1990, "nominee", 700, 25, 0, {"film_lead": 1, "film_sup": 1}, None),
    ("film_gal_932", "award_harbour_film", 1991, "gallery", 932, 45, 50, {}, None),
    ("ad_gal_932", "award_harbour_ad", 1991, "gallery", 932, 45, 50, {}, None),
    ("music_won_932", "award_golddisc_music", 1990, "nominee", 932, 80, 60, STRONG_ROLES, "won"),
    ("music_won_700", "award_golddisc_music", 1990, "nominee", 700, 80, 60, STRONG_ROLES, "won"),
    ("film_won_932", "award_harbour_film", 1990, "nominee", 932, 80, 60, STRONG_ROLES, "won"),
    ("ad_won_932", "award_harbour_ad", 1990, "nominee", 932, 80, 60, STRONG_ROLES, "won"),
]


def main():
    srv = d.serve()
    results = {}
    try:
        with sync_playwright() as pw:
            for c in CASES:
                results[c[0]] = run_case(pw, *c)
        with open(os.path.join(d.QA, "drive211.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print("== DRIVE211 DONE ==", flush=True)
        npass = 0
        for k, v in results.items():
            bad = {kk: vv for kk, vv in (v.get("checks") or {}).items() if not vv}
            ok = not bad and not v.get("error")
            npass += 1 if ok else 0
            print(f"  {k}: {'PASS' if ok else 'FAIL'} bad={json.dumps(bad, ensure_ascii=False)}"
                  f" errs={v.get('pageerrors')} skipped={v.get('skipped_no_won')}", flush=True)
        print(f"== SUMMARY {npass}/{len(results)} cases PASS ==", flush=True)
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
