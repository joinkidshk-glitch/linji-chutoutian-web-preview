# -*- coding: utf-8 -*-
"""v20a207 probe（pristine 量度）：B2 框／空帶、B3 跳過掣∩角度 pill、
C1 揭曉得主／落選者亮度、C3 700 結果卡摺疊、C5 中環廣告標籤位置。
只量度，唔改 code。結果寫 qa207/probe207_pristine.json。
重用 qa188/drive188.py helpers（同 drive204 一樣 import 法）。"""
import json
import os
import sys

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


def force_pack_try(pg, cer, tier, want_female_cat=False):
    for seed in range(1, 21):
        pg.evaluate(JS_SEEDED_RANDOM, seed)
        fp = pg.evaluate(JS_FORCE_PACK, {"id": cer, "tier": tier})
        if "error" in fp:
            return fp, seed
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
                   want_f=False):
    print(f"== {name} ==", flush=True)
    out = {"case": name}
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
        fp, seed_used = force_pack_try(pg, cer, tier, want_f)
        out["pack"] = fp
        if "error" in fp:
            out["error"] = fp
            return out
        inv = d.present(pg)
        out["invite_visible"] = bool(inv.get("visible"))
        out["invite_text"] = inv.get("body") or inv.get("text") or ""
        d.shot(pg, f"probe_{name}_invite.png")
        d.click_vis(pg, "出席")
        pg.wait_for_timeout(3900)
        out["rects_names"] = pg.evaluate(JS_RECTS)
        d.shot(pg, f"probe_{name}_stage.png")
        # 揭曉 beat：open1200+pan2000+names2400+suspense1400=7000ms 入揭曉，2100ms 長
        pg.wait_for_timeout(3600)
        out["rects_reveal"] = pg.evaluate(JS_RECTS)
        d.shot(pg, f"probe_{name}_reveal.png")
        w = d.watch(pg, 24)
        out["watch"] = w
        pg.wait_for_timeout(600)
        out["result_rects"] = pg.evaluate(JS_RESULT_RECTS)
        d.shot(pg, f"probe_{name}_result.png")
        out["pageerrors"] = errs[:5]
        return out
    finally:
        try:
            ctx.close()
        except Exception:
            pass
        b.close()


def run_map_case(pw):
    print("== map_932 ==", flush=True)
    out = {"case": "map_932"}
    errs = []
    b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
    try:
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        if not d.new_game(pg):
            out["error"] = "new_game fail"
            return out
        # 過場／開局：第 1 幕播完入地圖（drive204 review 做法：行完第 1 幕關結算卡）
        pg.wait_for_timeout(1500)
        try:
            d.click_vis(pg, "繼續")
        except Exception:
            pass
        pg.wait_for_timeout(2500)
        try:
            d.click_vis(pg, "關閉")
        except Exception:
            pass
        pg.wait_for_timeout(1200)
        out["map_labels"] = pg.evaluate(JS_MAP_LABEL)
        d.shot(pg, "probe_map_932.png")
        out["pageerrors"] = errs[:5]
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
            results["map_932"] = run_map_case(pw)
        with open(os.path.join(d.QA, "probe207_pristine.json"), "w",
                  encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print("== PROBE DONE ==", flush=True)
        for k, v in results.items():
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:600]}", flush=True)
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
