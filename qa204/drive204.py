# -*- coding: utf-8 -*-
"""v20a204 實駕：補女星入獎池＋提名人性別分流（LIVE 裸 URL，本地鏡像）。
重用 qa188/drive188.py 嘅 new_game／seed／present／watch 等 helper（import module，
覆寫 ROOT／PORT／SHOTS／EXE）；其餘驗證係 v204 專用。

場次：音樂＋電影 × 提名（nominee，男獎類別為主）／旁聽（gallery，全 slate）× 932／700。
每場：debugForceSeasonWindow 建 pack（實路徑，實 GIGS）→ 逐類別驗 fellows 性別：
  女獎類別 fellows 全女＋得主（fellows[0]／winner63）女；男獎全男；
  新人獎（gender ""）混合唔過濾、唔 crash；舊 10 星照常出現。
舞台：出席播典禮，驗 focus 類別嘅提名人喺台上（卡名＋px 圖載到），新星上台要見到 px 圖；
結果卡＋報紙 queue 要正確顯示新星名。0 pageerror。截圖放 qa204/shots204/。
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/linji-work204/qa188")
import drive188 as d

d.ROOT = "/home/hatch/workspace/linji-work204"
d.QA = "/home/hatch/workspace/linji-work204/qa204"
d.SHOTS = "/home/hatch/workspace/linji-work204/qa204/shots204"
d.EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
d.PORT = 20490
os.makedirs(d.SHOTS, exist_ok=True)

from playwright.sync_api import sync_playwright

FEMALE7 = {"so_jiyan", "chung_choning", "ngai_wingnaam", "yip_manji",
           "lan_ruoxi", "shum_yingsuet", "kong_siying"}
NEW3 = {"lan_ruoxi": "藍若曦", "shum_yingsuet": "沈映雪", "kong_siying": "江詩盈"}
OLD10 = {"luk_baakyin", "liu_bingxing", "chai_zanhoi", "mak_zhendong", "lok_gasing",
         "chung_choning", "so_jiyan", "ngai_wingnaam", "gu_mingfai", "yip_manji"}

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
    const table = (window.__awards.table188() || {})[o.id] || [];
    const genderOf = {};
    table.forEach(c => { if (c && c.id) genderOf[c.id] = c.gender || ''; });
    const cats = (p.categories || []).map(c => ({
      id: c.id, label: c.label, outcome: c.outcome, gender: genderOf[c.id] || '',
      fellows: (c.fellows63 || []).map(f => ({ starId: f.starId || '', star: f.star || '', title: f.title || '' })),
      winner: (c.winner63 && c.winner63.star) || ''
    }));
    return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome, tier: p.tier, cats };
  } catch(e) { return { error: String(e) }; }
}"""

JS_STAGE_FELLOWS = """() => {
  const st = document.querySelector('.awd62-stage');
  if (!st) return { present: false };
  // v204：舞台人物係 canvas 畫（drawPx），唔係 <img>——px 圖驗收改用 resource timing
  // （有請求＋200＝載到；截圖再目視核對係邊位企台）。
  const pxReq = performance.getEntriesByType('resource')
    .filter(e => /\\/px_[a-z0-9_]+_(south|east|west)\\.png/.test(e.name))
    .map(e => ({ f: e.name.split('/').pop(), status: e.responseStatus || 0 }));
  const cap = st.querySelector('.awd62-caption');
  return { present: true, pxReq,
           caption: cap ? cap.textContent : '',
           htmlHasNew: ['藍若曦','沈映雪','江詩盈'].filter(n => (st.innerText || '').includes(n)) };
}"""


def force_pack_try(pg, cer, tier, want_female_cat=False, want_gendered_cat=False):
    """建 pack；gallery 嗰陣重試唔同 Math.random seed，直到 pack 有女獎類別；
    nominee 嗰陣重試直到 pack 有性別類別（唔係淨係新人獎），最多 20 次。"""
    for seed in range(1, 21):
        pg.evaluate(JS_SEEDED_RANDOM, seed)
        fp = pg.evaluate(JS_FORCE_PACK, {"id": cer, "tier": tier})
        if "error" in fp:
            return fp, seed
        cats = fp.get("cats") or []
        if want_female_cat and not any(c.get("gender") == "f" for c in cats):
            continue
        if want_gendered_cat and not any((c.get("gender") or "") in ("m", "f") for c in cats):
            continue
        return fp, seed
    return fp, 20


def check_pack(fp):
    """逐類別性別斷言。回傳 (checks dict, 新星名單, 舊星名單)。"""
    ck = {}
    new_seen, old_seen = set(), set()
    for c in fp.get("cats") or []:
        g = c.get("gender") or ""
        fl = c.get("fellows") or []
        for f in fl:
            (new_seen if f["starId"] in NEW3 else old_seen).add(f["starId"])
        if g == "f":
            ck[f"{c['id']}_all_female"] = len(fl) > 0 and all(f["starId"] in FEMALE7 for f in fl)
            w = (fl[0]["starId"] if fl else "")
            ck[f"{c['id']}_winner_female"] = w in FEMALE7
        elif g == "m":
            ck[f"{c['id']}_all_male"] = len(fl) > 0 and all(f["starId"] not in FEMALE7 for f in fl)
            w = (fl[0]["starId"] if fl else "")
            ck[f"{c['id']}_winner_male"] = (w not in FEMALE7) and bool(w)
        else:
            ck[f"{c['id']}_newcomer_has_fellows"] = len(fl) > 0
    ck["has_cats"] = len(fp.get("cats") or []) > 0
    return ck, new_seen, old_seen


CASES = [
    # name, ceremony, year, tier, H, fame, credit, roles, want_female_cat, play_stage
    ("music_nom_932", "award_golddisc_music", 1990, "nominee", 932, 25, 0, {"rec": 2}, False, True),
    ("music_nom_700", "award_golddisc_music", 1990, "nominee", 700, 25, 0, {"rec": 2}, False, False),
    ("music_gal_932", "award_golddisc_music", 1991, "gallery", 932, 45, 50, {}, True, True),
    ("music_gal_700", "award_golddisc_music", 1991, "gallery", 700, 45, 50, {}, True, True),
    ("film_nom_932", "award_harbour_film", 1990, "nominee", 932, 25, 0, {"film_lead": 1, "film_sup": 1}, False, True),
    ("film_nom_700", "award_harbour_film", 1990, "nominee", 700, 25, 0, {"film_lead": 1, "film_sup": 1}, False, False),
    ("film_gal_932", "award_harbour_film", 1991, "gallery", 932, 45, 50, {}, True, True),
    ("film_gal_700", "award_harbour_film", 1991, "gallery", 700, 45, 50, {}, True, True),
]


def run_case(pw, cfg, results):
    name, cer, year, tier, H, fame, credit, roles, want_f, play_stage = cfg
    print(f"== {name} ({cer} {year} {tier}) ==", flush=True)
    out = {"case": name, "ceremony": cer, "year": year, "tier": tier, "checks": {}}
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
            fp, seed_used = force_pack_try(pg, cer, tier, want_f,
                                           want_gendered_cat=(tier == "nominee"))
            out["pack"] = fp
            out["seed_used"] = seed_used
            out["checks"]["pack_built"] = "error" not in fp
            if "error" in fp:
                out["verdict"] = "ERROR"
                results[name] = out
                print("  ERROR pack", fp, flush=True)
                return
            out["checks"]["tier_is_" + tier] = fp.get("tier") == tier
            pck, new_seen, old_seen = check_pack(fp)
            out["checks"].update(pck)
            out["new_stars_in_pack"] = sorted(new_seen)
            out["old_stars_in_pack"] = sorted(old_seen)
            if want_f:
                out["checks"]["pack_has_female_cat"] = any(
                    c.get("gender") == "f" for c in fp.get("cats") or [])
            inv = d.present(pg)
            out["invite"] = inv
            out["checks"]["invite_shown"] = bool(inv.get("visible"))
            d.shot(pg, f"{name}_invite.png")
            if not inv.get("visible") or not play_stage:
                out["pageerrors"] = errs[:8]
                out["checks"]["zero_pageerror"] = len(errs) == 0
                out["verdict"] = "PASS" if all(out["checks"].values()) else "FAIL"
                results[name] = out
                print(f"  {out['verdict']} {json.dumps(out['checks'], ensure_ascii=False)}", flush=True)
                return
            d.click_vis(pg, "出席")
            pg.wait_for_timeout(400)
            out["checks"]["stage_appears"] = bool(d.stage_state(pg).get("present"))
            # 唱名 beat（約 2–4 秒入場後）影一張＋讀卡名／px
            pg.wait_for_timeout(3500)
            st = pg.evaluate(JS_STAGE_FELLOWS)
            out["stage_mid"] = st
            d.shot(pg, f"{name}_stage.png")
            focus = (fp.get("cats") or [{}])[0]
            focus_fellows = [f["star"] for f in (focus.get("fellows") or [])]
            # 舞台唱名：字幕要唱出 focus 類別嘅提名人（逐句唱，3.5 秒嗰陣至少見到一位）
            out["checks"]["stage_caption_names_fellow"] = bool(focus_fellows) and any(
                n in (st.get("caption") or "") for n in focus_fellows)
            # px 圖：focus 類別每位提名人嘅 south 幀都要有請求＋200（canvas 畫用）
            px_files = {(p.get("f") or "") for p in (st.get("pxReq") or [])}
            px_ok = all((p.get("status") in (200, 304)) for p in (st.get("pxReq") or []))
            out["checks"]["stage_px_all_loaded"] = px_ok and bool(px_files)
            out["stage_px_files"] = sorted(px_files)
            out["checks"]["stage_px_covers_focus_fellows"] = bool(focus_fellows) and all(
                f"px_{f['starId']}_south.png" in px_files for f in (focus.get("fellows") or []))
            new_on_stage = [n for n in NEW3.values() if n in (st.get("htmlHasNew") or [])]
            out["new_stars_on_stage"] = new_on_stage
            w = d.watch(pg, 24)
            out["watch"] = w
            out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
            pg.wait_for_timeout(600)
            res = d.modal_info(pg)
            out["result_card"] = res
            out["checks"]["result_card_shown"] = bool(res.get("visible"))
            rbody = res.get("body") or ""
            for sid, nm in NEW3.items():
                if sid in new_seen:
                    out["checks"][f"result_names_{sid}"] = nm in rbody
            d.shot(pg, f"{name}_result.png")
            d.click_vis(pg, "收下這晚")
            pg.wait_for_timeout(900)
            nq = d.newspaper_award(pg)
            out["newspaper"] = nq
            aw = [n for n in nq if "award" in (n.get("source") or "").lower()
                  or "頒獎" in (n.get("headline") or "")]
            out["checks"]["newspaper_has_award"] = len(aw) >= 1
            # 報紙：gallery／won 印得主名；提名（入圍未得獎）印嘅係入圍名單——玩家名，唔印對手得主
            nq_text = json.dumps(nq, ensure_ascii=False)
            if tier == "gallery":
                focus0 = (((fp.get("cats") or [{}])[0].get("fellows") or [{}])[0].get("star")) or ""
                out["checks"]["newspaper_names_winner"] = bool(focus0) and focus0 in nq_text
            else:
                out["checks"]["newspaper_names_player_nominee"] = "阿偉" in nq_text and "入圍" in nq_text
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
        with open(os.path.join(d.QA, "drive204.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        npass = sum(1 for r in results.values() if r.get("verdict") == "PASS")
        print(f"== SUMMARY {npass}/{len(results)} PASS ==", flush=True)
        for k, r in results.items():
            bad = {kk: vv for kk, vv in (r.get("checks") or {}).items() if not vv}
            print(f"  {k}: {r.get('verdict')} {json.dumps(bad, ensure_ascii=False)}"
                  f" new={r.get('new_stars_in_pack')} old_n={len(r.get('old_stars_in_pack') or [])}", flush=True)
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
