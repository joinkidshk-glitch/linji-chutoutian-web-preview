# -*- coding: utf-8 -*-
"""v20a207 驗證 drive：B2／B3／C1–C5 逐項斷言＋截圖。結果寫 qa207/drive207.json，截圖 qa207/shots207/v207_*。
重用 qa188/drive188.py helpers（同 drive204 一樣 import 法）。"""
import json
import os
import sys
import time

from PIL import Image


def slot_cxs(n):
    """draw() 嘅 slotCx：3 slots → [75,240,405]；否則 240＋(i-(n-1)/2)*120。"""
    if n == 3:
        return [75, 240, 405]
    return [round(240 + (i - (n - 1) / 2) * 120) for i in range(n)]


def lum_winner_loser(shot_name, rects, winner_cx=75, loser_cx=240):
    """揭曉截圖：得主（行前 settled 位）vs 落選對手同一框亮度。
    腳底 y ＝ canvas.top ＋ 314/432 × canvas.h；盒 52×115。"""
    try:
        im = Image.open(os.path.join(d.SHOTS, shot_name)).convert("RGB")
        cv = rects["canvas"]; fr = rects["frame"]
        feet = cv["y"] + 314 / 432 * cv["h"]
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
    """由 pack 焦點類別計得主／落選者嘅量度 cx（reveal settled 位）。
    回傳 (winner_cx, loser_cx, info)。slots：fellows 一排，non-gallery 玩家插喺 index 1；
    得主行前 22% 向中央（fwd64，p=1）。"""
    import re as _re
    cats = (fp or {}).get("cats") or []
    # 焦點類別：reveal 字幕講邊個獎（board 會話埋，但呢度用 caption 嘅得主名反查最穩）
    m = _re.search(r"(\S+)憑《", caption or "")
    win_star = m.group(1) if m else None
    focus = None
    for c in cats:
        fws = c.get("fellows") or []
        if win_star and any((f or {}).get("star") == win_star for f in fws):
            focus = c
            break
    if focus is None:
        # won 分支（字幕係「得獎！」無得主名）或搵唔到：用第一個有 fellows 嘅類別
        focus = next((c for c in cats if (c.get("fellows") or [])), None)
    if focus is None:
        return 75, 240, {"note": "no focus cat"}
    fws = focus.get("fellows") or []
    n = len(fws) + (0 if best == "gallery" else 1)
    cxs = slot_cxs(n)
    def slot_of(fellow_idx):
        return fellow_idx if (best == "gallery" or fellow_idx < 1) else fellow_idx + 1
    if best == "won":
        w_slot = 1  # 玩家插喺 index 1
        l_slot = 0  # fellows[0] 係落選對手
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

sys.path.insert(0, "/home/hatch/workspace/linji-work207/qa188")
import drive188 as d

d.ROOT = "/home/hatch/workspace/linji-work207"
d.QA = "/home/hatch/workspace/linji-work207/qa207"
d.SHOTS = "/home/hatch/workspace/linji-work207/qa207/shots207"
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 20790
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
    return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
      tier: p.tier,
      cats: (p.categories || []).map(c => ({ id: c.id, label: c.label,
        outcome: c.outcome,
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
  const skip = st.querySelector('.awd62-skip');
  const strips = Array.from(st.querySelectorAll('.awd181-strip')).map(r);
  const tap = st.querySelector('.awd62-tap');
  const cards = st.querySelector('.awd63-cards');
  const skipR = r(skip), stripR = strips.length > 1 ? strips[1] : null;
  let overlap = null;
  if (skipR && stripR) {
    const ox = Math.max(0, Math.min(skipR.right, stripR.right) - Math.max(skipR.x, stripR.x));
    const oy = Math.max(0, Math.min(skipR.bottom, stripR.bottom) - Math.max(skipR.y, stripR.y));
    overlap = { ox, oy, area: ox * oy };
  }
  return { present: true, vh: window.innerHeight, vw: window.innerWidth,
    stage: r(st), frame: r(frame), canvas: r(cv), caption: r(cap), skip: skipR,
    strips, stripRight: stripR, skipStripOverlap: overlap, tap: r(tap),
    cards: r(cards), cardsVisible: cards ? getComputedStyle(cards).visibility : null,
    captionText: cap ? cap.textContent : '' };
}"""

JS_RESULT_RECTS = """() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
             bottom: Math.round(b.bottom), right: Math.round(b.right) }; };
  const modal = document.querySelector('.modal');
  const inner = document.getElementById('modal-inner');
  const sheet = document.querySelector('.awd-sheet');
  if (!modal || !sheet) return { present: false };
  const cards = Array.from(sheet.querySelectorAll('.psr-card')).map(el => ({
    cls: el.className, rect: r(el),
    kicker: (el.querySelector('.psr-kicker') || {}).textContent || '' }));
  const dual = sheet.querySelector('.psr-dual');
  const btns = document.getElementById('modal-btns');
  return { present: true, vh: window.innerHeight,
    modal: r(modal), modalInnerScrollH: inner ? inner.scrollHeight : null,
    modalInnerClientH: inner ? inner.clientHeight : null,
    sheet: r(sheet), cards, dual: r(dual),
    dualText: dual ? dual.textContent : '',
    btns: r(btns),
    fellows: r(sheet.querySelector('.psr-fellows63')) };
}"""

JS_MAP_LABEL = """() => {
  const els = Array.from(document.querySelectorAll('#map-names68 .mn68'));
  const out = els.map(el => { const b = el.getBoundingClientRect();
    return { text: el.textContent, x: Math.round(b.x), y: Math.round(b.y),
             w: Math.round(b.width), h: Math.round(b.height),
             left: el.style.left, top: el.style.top }; });
  const wrap = document.querySelector('#map-names68');
  const wb = wrap ? wrap.getBoundingClientRect() : null;
  return { labels: out, wrap: wb ? { x: Math.round(wb.x), y: Math.round(wb.y),
    w: Math.round(wb.width), h: Math.round(wb.height) } : null };
}"""


def force_pack_try(pg, cer, tier, want_female_cat=False, want_outcome=None):
    for seed in range(1, 21):
        pg.evaluate(JS_SEEDED_RANDOM, seed)
        fp = pg.evaluate(JS_FORCE_PACK, {"id": cer, "tier": tier})
        if "error" in fp:
            return fp, seed
        if want_outcome and fp.get("bestOutcome") != want_outcome:
            continue
        cats = fp.get("cats") or []
        if want_female_cat and not any(
                (c.get("fellows") or []) and c["fellows"][0].get("starId") in
                {"so_jiyan", "chung_choning", "ngai_wingnaam", "yip_manji",
                 "lan_ruoxi", "shum_yingsuet", "kong_siying"}
                for c in cats):
            continue
        return fp, seed
    return fp, 20


def run_stage_case(pw, name, cer, year, tier, H, fame, credit, roles,
                   want_f=False, want_outcome=None):
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
        fp, seed_used = force_pack_try(pg, cer, tier, want_f, want_outcome)
        out["pack"] = fp
        out["seed_used"] = seed_used
        if "error" in fp:
            out["error"] = fp
            return out
        if want_outcome:
            ck["pack_outcome_" + want_outcome] = fp.get("bestOutcome") == want_outcome
            if fp.get("bestOutcome") != want_outcome:
                out["skipped_won"] = True
                print("  (no won pack in 20 seeds, skip stage)", flush=True)
                return out
        inv = d.present(pg)
        out["invite_visible"] = bool(inv.get("visible"))
        out["invite_text"] = inv.get("body") or inv.get("text") or ""
        ck["invite_shown"] = bool(inv.get("visible"))
        # C4：影藝獎／廣告獎請柬唔再有「旁聽／入圍席位信」
        if cer in ("award_harbour_film", "award_harbour_ad"):
            ck["C4_no_slash_dek"] = "旁聽／入圍席位信" not in out["invite_text"]
            ck["C4_has_seat_letter"] = "你收到一張席位信" in out["invite_text"]
        d.shot(pg, f"v207_{name}_invite.png")
        d.click_vis(pg, "出席")
        pg.wait_for_timeout(3900)
        rn = pg.evaluate(JS_RECTS)
        out["rects_names"] = rn
        # B2：canvas 高咗（307→~367），框唔出 viewport；B3：跳過掣唔遮數字條
        if rn.get("present"):
            cv = rn["canvas"]; fr = rn["frame"]
            ck["B2_canvas_taller"] = 355 <= cv["h"] <= 380
            ck["B2_frame_in_viewport"] = fr["y"] >= 0 and fr["bottom"] <= H
            ck["B2_top_band_narrower"] = fr["y"] < (259 if H == 932 else 143)
            ov = rn.get("skipStripOverlap") or {}
            ck["B3_skip_not_covering_strip"] = (ov.get("area") or 0) == 0
            sk = rn.get("skip") or {}
            ck["B3_skip_bottom_half"] = sk.get("y", 0) > cv["y"] + cv["h"] / 2
        d.shot(pg, f"v207_{name}_stage.png")
        # 揭曉 beat：等真正 reveal 字幕（唔係 suspense 嗰句「得獎者是……」）再影；
        # 等 700ms 等得主行前企定（fwd64 p=1）先量亮度。
        shot_reveal = False
        cap = ""
        t0 = time.time()
        while time.time() - t0 < 12:
            try:
                cap = (d.stage_state(pg).get("caption") or "")
            except Exception:
                cap = ""
            if "得獎" in cap and cap.strip() != "得獎者是……":
                pg.wait_for_timeout(700)
                shot_reveal = True
                break
            pg.wait_for_timeout(250)
        rr = pg.evaluate(JS_RECTS)
        out["rects_reveal"] = rr
        out["reveal_shot"] = shot_reveal
        out["reveal_caption"] = cap
        d.shot(pg, f"v207_{name}_reveal.png")
        # C1：得主／落選者亮度差（slot 位由 pack 焦點類別計，唔寫死 cx75／cx240）
        if rr.get("present") and shot_reveal:
            w_cx, l_cx, info = reveal_slots(fp, fp.get("bestOutcome"), cap)
            out["reveal_slots"] = info
            out["reveal_lum"] = lum_winner_loser(f"v207_{name}_reveal.png", rr, w_cx, l_cx)
            wl = out["reveal_lum"]
            if wl:
                ck["C1_winner_brighter"] = wl["winner"] - wl["loser"] >= 12
        w = d.watch(pg, 24)
        out["watch"] = w
        pg.wait_for_timeout(600)
        res = pg.evaluate(JS_RESULT_RECTS)
        out["result_rects"] = res
        if res.get("present"):
            # C3：700 高三格＋聲望行唔使碌（scroll <= client）；932 照舊唔碌
            ck["C3_result_no_scroll"] = (res.get("modalInnerScrollH") or 0) <= (res.get("modalInnerClientH") or 0) + 2
            cards = res.get("cards") or []
            metric = [c for c in cards if "銷量" in (c.get("kicker") or "") or "票房" in (c.get("kicker") or "")]
            if metric:
                out["metric_bottom"] = metric[0]["rect"]["bottom"]
                ck["C3_metric_visible"] = metric[0]["rect"]["bottom"] <= (res["modal"]["bottom"] if res.get("modal") else 9999)
            if res.get("dual"):
                ck["C3_dual_visible"] = res["dual"]["bottom"] <= (res["modal"]["bottom"] if res.get("modal") else 9999)
        d.shot(pg, f"v207_{name}_result.png")
        out["pageerrors"] = errs[:5]
        ck["zero_pageerror"] = len(errs) == 0
        return out
    finally:
        try:
            ctx.close()
        except Exception:
            pass
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
        # new_game 落喺手帳頁（地圖未開，labels 0×0）：撳「返回地圖」先量標籤
        d.click_vis(pg, "返回地圖")
        pg.wait_for_timeout(800)
        # 開場 C1 會自動全屏播（遮住地圖）：撳「下一句」播完，抉擇揀第一個，
        # 結算撳「關閉」，地圖先真係見到。唔播完，量度到嘅 label rect 只係 DOM 數字，
        # 截圖會係劇情畫面（v207 第一版 drive 就係咁，map 截圖影住何生事務所）。
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
        d.shot(pg, "v207_map_932.png")
        labs = (out["map_labels"] or {}).get("labels") or []
        central = [x for x in labs if x.get("text") == "中環廣告"]
        if central:
            c = central[0]
            out["checks"]["C5_label_has_size"] = c["w"] > 0 and c["h"] > 0
            # game JS 開地圖後會將 inline left 寫成 px（'192.956px'），唔再係 '51%'——
            # 用 wrap 闊度計中心位比率驗（inline 51% 本身由 ui142／ux68 靜態釘死）。
            wrap = (out["map_labels"] or {}).get("wrap") or {}
            ww = wrap.get("w") or 0
            ratio = ((c["x"] + c["w"] / 2 - wrap.get("x", 0)) / ww) if ww else -1
            out["checks"]["C5_label_at_51pct"] = 0.41 <= ratio <= 0.61
            out["checks"]["C5_label_inside_map"] = (
                c["x"] >= wrap.get("x", 0) and c["x"] + c["w"] <= wrap.get("x", 0) + ww)
            out["checks"]["C5_no_story_overlay"] = bool(out.get("story_overlay_gone"))
            out["central_label"] = c
            out["central_ratio"] = round(ratio, 3)
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
            results["music_gal_932"] = run_stage_case(
                pw, "music_gal_932", "award_golddisc_music", 1991, "gallery",
                932, 45, 50, {}, want_f=True)
            results["music_gal_700"] = run_stage_case(
                pw, "music_gal_700", "award_golddisc_music", 1991, "gallery",
                700, 45, 50, {}, want_f=True)
            results["music_nom_700"] = run_stage_case(
                pw, "music_nom_700", "award_golddisc_music", 1990, "nominee",
                700, 25, 0, {"rec": 2})
            results["film_gal_932"] = run_stage_case(
                pw, "film_gal_932", "award_harbour_film", 1991, "gallery",
                932, 45, 50, {}, want_f=True)
            results["music_won_932"] = run_stage_case(
                pw, "music_won_932", "award_golddisc_music", 1990, "nominee",
                932, 80, 0, {"rec": 3}, want_outcome="won")
            results["map_932"] = run_map_case(pw)
        with open(os.path.join(d.QA, "drive207.json"), "w",
                  encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print("== DRIVE207 DONE ==", flush=True)
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
