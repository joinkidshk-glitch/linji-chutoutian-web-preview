#!/usr/bin/env python3
"""v20a183 實駕：B1–B4＋C1–C9 逐項驗證（932／700）。
沿用 drive176_landed 助手（種子複製／入場／modal），只讀＋真 UI 點擊，唔改 code。
用法：/home/hatch/pwenv49/bin/python qa183/drive183.py [case|all]
"""
import json, subprocess, sys, time, os
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v176")
import drive176_landed as D
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work183"
HERE = "/home/hatch/workspace/linji-work183/qa183"
SHOTS = os.path.join(HERE, "shots183")
os.makedirs(SHOTS, exist_ok=True)
EXE = D.EXE
PORT = 8976
D.PORT = PORT

def shot(pg, name):
    try:
        pg.screenshot(path=os.path.join(SHOTS, name)); return True
    except Exception:
        return False

def seed_day(pg, day):
    return pg.evaluate("""(day) => {
      S.dayIndex = day;
      S.romDay = null; S.starDay = null; S.romWeek = null;
      S.inventory = { gift_pineapple_bun_set: 3, gift_egg_tart_box: 3, gift_thermos: 3,
        gift_hair_clip_set: 3, gift_memo_pad: 3, gift_coffee_beans: 3, gift_cassette_indie: 3,
        gift_handmade_sweet: 3, gift_fashion_mag: 3, gift_perfume_sample: 3 };
      return { day: S.dayIndex };
    }""", day)

def pill(pg):
    return pg.evaluate("""() => {
      const el = document.querySelector('.map-hint-travel');
      return el ? (el.textContent || '').trim() : (document.body.innerText || '').match(/仲可以去 \\d+ 個地方|出行額度已用完/)?.[0] || '';
    }""")

def modal_text(pg):
    mi = D.modal_info(pg)
    return mi

def contrast_in_page(pg):
    return pg.evaluate("""() => {
      const b = document.querySelector('.people-go');
      if (!b) return null;
      const cs = getComputedStyle(b);
      function parse(s){ const m = s.match(/[\\d.]+/g); if (!m) return null;
        return { r:+m[0], g:+m[1], b:+m[2], a:(m.length>3 ? +m[3] : 1) }; }
      function lum(rgb){ function f(c){ c/=255; return c<=0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); }
        return 0.2126*f(rgb[0])+0.7152*f(rgb[1])+0.0722*f(rgb[2]); }
      // 底色：由掣向上收集各層底色，再由底向上逐層 alpha 合成（掣底 rgba .28 金 → 卡紙底 → 白）
      const layers = []; let el = b;
      while (el) { const c = parse(getComputedStyle(el).backgroundColor);
        if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
        el = el.parentElement; }
      let bg = [255,255,255];
      for (let i = layers.length - 1; i >= 0; i--) { const c = layers[i];
        bg = [0,1,2].map(j => Math.round(c.a*[c.r,c.g,c.b][j] + (1-c.a)*bg[j])); }
      const fg = parse(cs.color);
      const L1 = lum([fg.r, fg.g, fg.b]), L2 = lum(bg);
      return { fg: cs.color, bg: 'rgb('+bg.join(',')+')', ratio: Math.round((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)*100)/100 };
    }""")

def new_game_walk_tutorial(pg):
    """新遊戲 → 逐頁行教學（記低每頁文字）→ 停喺屋企 intro modal 之前。回傳 tutorial 文字。"""
    pg.goto(f"http://127.0.0.1:{PORT}/index.html?softPreview=1")
    pg.wait_for_timeout(1500)
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
    pg.wait_for_timeout(1000)
    try:
        pg.locator('[data-slot="3"]').first.click(timeout=1500)
        pg.wait_for_timeout(800)
    except Exception:
        pass
    texts = []
    for _ in range(15):
        mi = D.modal_info(pg)
        if not mi.get("visible"):
            break
        texts.append(mi.get("body") or "")
        if D.click_vis_btn(pg, "下一步", "#modal"):
            pg.wait_for_timeout(700)
            continue
        break
    return texts

def dismiss_to_map(pg, tries=30):
    for _ in range(tries):
        if D.map_ready(pg):
            return True
        if not D.dismiss_once(pg):
            if not D.click_vis_btn(pg, "返回地圖"):
                pg.wait_for_timeout(500)
        pg.wait_for_timeout(600)
    return D.map_ready(pg)

def enter_woman(pg, key, loc, max_days=10):
    """播種搵 key 喺 loc 嘅日子，逐日試入場，直到撞到 key 嘅 modal。回傳 (mi, day, attempts)。"""
    cands = D.find_woman_days(key, loc, n=max_days)
    attempts = []
    for d in cands:
        seed_day(pg, d)
        way = D.enter_loc(pg, loc)
        if not way:
            attempts.append({"day": d, "enter": None})
            return None, None, attempts
        pg.wait_for_timeout(1200)
        mi = D.wait_modal(pg, 5)
        attempts.append({"day": d, "enter": way, "h3": mi.get("h3")})
        name = {"hiu": "林曉晴", "xu": "徐寶珊", "mei": "關海媚", "choi": "周采兒", "vera": "Vera", "lan": "藍若曦"}[key]
        if mi.get("visible") and name in (mi.get("h3") or ""):
            return mi, d, attempts
        if mi.get("visible"):
            D.dismiss_once(pg)
            pg.wait_for_timeout(800)
        if D.sheet_visible(pg):
            D.back_to_map(pg)
        elif D.map_ready(pg):
            pass
        else:
            D.dismiss_once(pg)
            pg.wait_for_timeout(800)
            D.back_to_map(pg)
    return None, None, attempts

def mei_days(n=10):
    out = []
    for d in range(0, 150):
        if D._rand(f"rom176:{d}:mei:out") >= 0.50:
            continue
        out.append((d, "ad_adm" if D._rand(f"rom176:{d}:mei:loc") < 0.65 else "rec_hk"))
        if len(out) >= n:
            break
    return out

def open_people(pg):
    ok1 = pg.evaluate("""() => { const b = document.querySelector('button[data-m="journal"]'); if (b) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(800)
    ok2 = pg.evaluate("""() => { const b = document.getElementById('htab-people'); if (b) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1000)
    return ok1 and ok2

# ---------------- cases ----------------
def case_c6c9(pg, W, H):
    out = {"checks": {}}
    tut = new_game_walk_tutorial(pg)
    out["tutSteps"] = len(tut)
    out["tutSample"] = (tut[0][:200] if tut else "")
    joined = "\n".join(tut)
    out["checks"]["c6_tut_mentions_encounter"] = "撞到" in joined
    out["checks"]["c6_tut_has_steps"] = len(tut) >= 2
    # 跳過教學，停喺 intro modal
    D.click_vis_btn(pg, "跳過教學", "#modal")
    pg.wait_for_timeout(1200)
    out["pill_before_intro"] = pill(pg)
    out["checks"]["c9_pill_before_intro_2"] = "仲可以去 2 個地方" in (out["pill_before_intro"] or "")
    out["checks"]["c9_intro_btn_present"] = D.vis_btn(pg, "睇劇情", "#modal")
    shot(pg, f"c9_intro_{W}x{H}.png")
    clicked = D.click_vis_btn(pg, "睇劇情", "#modal")
    out["checks"]["c9_intro_btn_clickable"] = clicked
    pg.wait_for_timeout(1500)
    out["pill_after_intro"] = pill(pg)
    out["checks"]["c9_pill_after_intro_still_2"] = "仲可以去 2 個地方" in (out["pill_after_intro"] or "")
    dismiss_to_map(pg)
    way = D.enter_loc(pg, "cafe_cha")
    pg.wait_for_timeout(1200)
    out["enter_cafe"] = way
    out["pill_after_manual"] = pill(pg)
    out["checks"]["c9_manual_entry_costs_1"] = "仲可以去 1 個地方" in (out["pill_after_manual"] or "")
    return out

def case_people(pg, W, H):
    out = {"checks": {}}
    out["checks"]["new_game_to_map"] = D.new_game_to_map(pg)
    pg.evaluate("""() => { S.story.rel = { rel_hiu: 2, rel_choi: 1 }; S.story.done = {}; return true; }""")
    out["checks"]["open_people"] = open_people(pg)
    txt = pg.evaluate("""() => (document.getElementById('people-list') || {}).innerText || ''""")
    out["peopleText"] = txt[:1500]
    out["checks"]["b1_rel_line_hiu"] = "感情：好感 2／5" in txt
    out["checks"]["b1_rel_line_choi"] = "感情：好感 1／5" in txt
    out["checks"]["b4_mei_locked_note"] = "主線再行前啲先撞到佢" in txt
    btns = pg.evaluate("""() => [...document.querySelectorAll('#people-list .people-go')].map(b => (b.textContent||'').trim())""")
    out["goBtns"] = btns
    out["checks"]["b4_mei_no_go_btn"] = not any("金鐘創意" in b for b in btns)
    out["checks"]["c8_no_go_find_word"] = not any("去找" in b for b in btns)
    out["checks"]["c8_go_btn_says_walk"] = any("行下" in b for b in btns)
    out["contrast"] = contrast_in_page(pg)
    out["checks"]["c5_contrast_ge_4_5"] = bool(out["contrast"]) and out["contrast"]["ratio"] >= 4.5
    shot(pg, f"people_{W}x{H}.png")
    return out

def case_woman(pg, W, H):
    out = {"checks": {}}
    out["checks"]["new_game_to_map"] = D.new_game_to_map(pg)
    pg.evaluate("""() => { S.story.rel = { rel_hiu: 2 }; return true; }""")
    mi, day, attempts = enter_woman(pg, "hiu", "tvb_longmen")
    out["attempts"] = attempts
    out["seedDay"] = day
    out["encounterModal"] = mi
    out["checks"]["woman_modal_shown"] = bool(mi and mi.get("visible")) and "林曉晴" in (mi.get("h3") or "")
    if not out["checks"]["woman_modal_shown"]:
        return out
    body = mi.get("body") or ""
    out["checks"]["c1_greet_cantonese"] = "咁啱嘅，喺呢度撞到你" in body
    out["checks"]["c1_no_mandarin_greet"] = "今天在星河電視台廠房碰到你" not in body
    out["checks"]["b1_modal_rel_line"] = "而家好感 2／5" in body
    shot(pg, f"woman_modal_{W}x{H}.png")
    # B2：送禮選擇器
    out["checks"]["click_gift"] = D.click_vis_btn(pg, "送禮", "#modal")
    pg.wait_for_timeout(1000)
    pick = D.wait_modal(pg, 4)
    out["pickModal"] = pick
    out["checks"]["gift_pick_shown"] = bool(pick.get("visible"))
    rows = pg.evaluate("""() => [...document.querySelectorAll('#gift-pick-list > *')].map(r => ({
      t: (r.innerText || '').replace(/\\n/g, ' | ').slice(0, 90),
      bottom: Math.round(r.getBoundingClientRect().bottom) }))""")
    out["pickRows"] = rows
    fav_rows = [r for r in rows if "★ 最愛" in r["t"]]
    like_rows = [r for r in rows if "喜" in r["t"] and "★" not in r["t"]]
    # 女角 gift_prefs.json 無 favorites 欄（得星先有）——女角 picker 預期冇 ★ 行；★ 分辨由 star_b2 case 驗
    out["checks"]["b2_women_no_fav_rows_expected"] = len(fav_rows) == 0
    out["checks"]["b2_has_like_tag"] = len(like_rows) >= 1
    if H == 700:
        out["checks"]["c7_all_rows_in_viewport"] = len(rows) == 10 and all(r["bottom"] <= 700 for r in rows)
        cancel = pg.evaluate("""() => { const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => (b.textContent||'').includes('取消'));
          if (!bs.length) return null; const r = bs[0].getBoundingClientRect(); return { bottom: Math.round(r.bottom), top: Math.round(r.top) }; }""")
        out["cancelGeom"] = cancel
        out["checks"]["c7_cancel_pinned_visible"] = bool(cancel) and cancel["bottom"] <= 700
        shot(pg, f"picker_700_{W}x{H}.png")
    # 撳最愛行 → 確認 modal 寫明最愛
    fav_name = None
    if fav_rows:
        fav_name = pg.evaluate("""() => { const rs = [...document.querySelectorAll('#gift-pick-list > *')];
          const f = rs.find(r => (r.innerText||'').includes('★ 最愛')); if (!f) return null;
          const b = f.querySelector('button') || f; b.click(); return (f.innerText||'').slice(0, 60); }""")
        pg.wait_for_timeout(900)
        conf = D.wait_modal(pg, 4)
        out["favConfirm"] = conf
        out["checks"]["b2_confirm_says_fav"] = "★ 最愛：佢最鍾意呢樣禮物" in (conf.get("body") or "")
        shot(pg, f"confirm_fav_{W}x{H}.png")
        D.click_vis_btn(pg, "取消", "#modal") or D.dismiss_once(pg)
        pg.wait_for_timeout(900)
    # 送保溫瓶（喜歡）→ C3 反應句
    picked, confirmed = D.click_gift_item(pg, "gift_thermos")
    out["checks"]["click_thermos"] = picked
    out["checks"]["confirm_send"] = confirmed
    pg.wait_for_timeout(1200)
    res = D.wait_modal(pg, 4)
    out["resultModal"] = res
    rbody = res.get("body") or ""
    out["checks"]["c3_thermos_cantonese"] = "係咪見到我冬天抱住紙杯震" in rbody
    out["checks"]["c3_no_mandarin_words"] = "是不是" not in rbody and "什麼" not in rbody
    out["checks"]["result_plus2"] = "好感 +2" in rbody
    D.dismiss_once(pg)
    pg.wait_for_timeout(1000)
    after = D.rel_state(pg)
    out["checks"]["rel_hiu_2_to_4"] = after["relHiu"] == 4
    return out

def case_b3(pg, W, H):
    out = {"checks": {}}
    out["checks"]["new_game_to_map"] = D.new_game_to_map(pg)
    mi, day, attempts = enter_woman(pg, "hiu", "tvb_longmen")
    out["attempts"] = attempts
    out["checks"]["encounter_first"] = bool(mi and mi.get("visible"))
    if not out["checks"]["encounter_first"]:
        return out
    out["checks"]["click_leave"] = D.click_vis_btn(pg, "行開", "#modal")
    pg.wait_for_timeout(1000)
    out["checks"]["sheet_after_leave"] = D.sheet_visible(pg)
    out["checks"]["back_to_map"] = D.back_to_map(pg)
    way2 = D.enter_loc(pg, "tvb_longmen")
    pg.wait_for_timeout(1200)
    out["enterWay2"] = way2
    # 再入場可能彈隨機劇情 modal（例如「飛紙仔殺到埋身」）冚住地點板——清晒啲 modal 先讀板
    for _ in range(10):
        mi2 = D.modal_info(pg)
        if not mi2.get("visible"):
            break
        D.dismiss_once(pg)
        pg.wait_for_timeout(800)
    sheet = pg.evaluate("""() => { const s = document.getElementById('loc-sheet'); return s ? s.innerText.slice(0, 1200) : ''; }""")
    out["sheetText"] = sheet
    out["checks"]["b3_who_line_names_hiu"] = "曉晴" in sheet
    out["checks"]["b3_who_line_says_met_today"] = "今日已經撞過佢" in sheet
    out["checks"]["b3_who_line_not_lan"] = "藍若曦" not in sheet.split("在場")[1][:120] if "在場" in sheet else True
    shot(pg, f"b3_sheet_{W}x{H}.png")
    return out

def case_xu(pg, W, H):
    out = {"checks": {}}
    out["checks"]["new_game_to_map"] = D.new_game_to_map(pg)
    mi, day, attempts = enter_woman(pg, "xu", "ad_central")
    out["attempts1"] = attempts
    out["checks"]["xu_first_encounter"] = bool(mi and mi.get("visible"))
    if not out["checks"]["xu_first_encounter"]:
        return out
    body1 = mi.get("body") or ""
    out["checks"]["c2_first_no_chunming"] = "春茗" not in body1
    out["checks"]["c2_first_is_fresh"] = "啱啱先撞到" in body1
    shot(pg, f"xu_first_{W}x{H}.png")
    D.click_vis_btn(pg, "行開", "#modal")
    pg.wait_for_timeout(900)
    D.back_to_map(pg)
    pg.evaluate("""() => { S.flags = S.flags || {}; S.flags.gift_met_xu = 1; S.romDay = null; S.romWeek = null; return true; }""")
    # 第二日再撞（唔同日，同一地點）
    cands = [d for d in D.find_woman_days("xu", "ad_central", n=10) if d != day]
    mi2 = None
    for d in cands:
        seed_day(pg, d)
        way = D.enter_loc(pg, "ad_central")
        if not way:
            break
        pg.wait_for_timeout(1200)
        m = D.wait_modal(pg, 5)
        if m.get("visible") and "徐寶珊" in (m.get("h3") or ""):
            mi2 = m
            out["day2"] = d
            break
        if m.get("visible"):
            D.dismiss_once(pg)
            pg.wait_for_timeout(800)
        if D.sheet_visible(pg):
            D.back_to_map(pg)
    out["checks"]["xu_second_encounter"] = bool(mi2 and mi2.get("visible"))
    if mi2:
        body2 = mi2.get("body") or ""
        out["checks"]["c2_second_has_chunming"] = "春茗" in body2
        shot(pg, f"xu_second_{W}x{H}.png")
    return out

def case_mei(pg, W, H):
    out = {"checks": {}}
    out["checks"]["new_game_to_map"] = D.new_game_to_map(pg)
    pg.evaluate("""() => { S.story.done = Object.assign({}, S.story.done, { C9: 1 }); return true; }""")
    mi = None
    attempts = []
    for d, loc in mei_days(10):
        seed_day(pg, d)
        way = D.enter_loc(pg, loc)
        if not way:
            attempts.append({"day": d, "loc": loc, "enter": None})
            break
        pg.wait_for_timeout(1200)
        m = D.wait_modal(pg, 5)
        attempts.append({"day": d, "loc": loc, "h3": m.get("h3")})
        if m.get("visible") and "關海媚" in (m.get("h3") or ""):
            mi = m
            out["day"] = d
            break
        if m.get("visible"):
            D.dismiss_once(pg)
            pg.wait_for_timeout(800)
        if D.sheet_visible(pg):
            D.back_to_map(pg)
        elif D.map_ready(pg):
            pass
        else:
            D.dismiss_once(pg)
            pg.wait_for_timeout(800)
            D.back_to_map(pg)
    out["attempts"] = attempts
    out["checks"]["mei_encounter"] = bool(mi and mi.get("visible"))
    if mi:
        body = mi.get("body") or ""
        out["checks"]["c4_no_stage_direction"] = "（佢望咗你一眼" not in body and "冇即刻行開" not in body
        out["checks"]["c4_greet_cantonese"] = "咁啱，喺呢度撞到你" in body
        shot(pg, f"mei_modal_{W}x{H}.png")
    return out

def case_star_b2(pg, W, H):
    """B2 live：星送禮選擇器要一眼分到最愛 vs 喜歡（女角 picker 冇 favorites 數據，唔係 B2 目標）。"""
    out = {"checks": {}}
    out["checks"]["new_game_to_map"] = D.new_game_to_map(pg)
    cands = D.find_star_candidates()
    out["candidates"] = cands[:3]
    out["checks"]["found_star_candidates"] = len(cands) > 0
    if not cands:
        return out
    found, info = None, None
    for c in cands:
        day, loc, star = c["day"], c["loc"], c["star"]
        seed_day(pg, day)
        way = D.enter_loc(pg, loc)
        if not way:
            return {**out, "checks": {**out["checks"], "enter_loc_ui_works": False}}
        pg.wait_for_timeout(1500)
        info_try = D.e79_info(pg)
        mi_try = D.modal_info(pg)
        if info_try.get("visible"):
            found, info = c, info_try
            break
        if mi_try.get("visible"):
            D.dismiss_once(pg)
            pg.wait_for_timeout(800)
        if D.sheet_visible(pg):
            D.back_to_map(pg)
        elif not D.map_ready(pg):
            D.dismiss_once(pg)
            pg.wait_for_timeout(800)
            D.back_to_map(pg)
    out["found"] = found
    out["checks"]["star_overlay_shown"] = bool(found and info.get("visible"))
    if not found:
        return out
    day, loc, star = found["day"], found["loc"], found["star"]
    fav_item = D.STAR_FAV1.get(star)
    out["star"] = star
    out["favItem"] = fav_item
    adv = D.e79_advance(pg, 10)
    out["checks"]["gift_btn_at_last_step"] = bool(adv.get("giftBtn"))
    if not adv.get("giftBtn"):
        return out
    out["checks"]["click_star_gift_btn"] = D.click_vis_btn(pg, adv["giftBtn"], "#enc79-overlay")
    pg.wait_for_timeout(1000)
    pick = D.wait_modal(pg, 4)
    out["checks"]["gift_pick_shown"] = bool(pick.get("visible"))
    rows = pg.evaluate("""() => [...document.querySelectorAll('#gift-pick-list > *')].map(r => ({
      t: (r.innerText || '').replace(/\\n/g, ' | ').slice(0, 90) }))""")
    out["pickRows"] = rows
    fav_rows = [r for r in rows if "★ 最愛" in r["t"]]
    like_rows = [r for r in rows if "喜" in r["t"] and "★" not in r["t"]]
    out["checks"]["b2_star_has_fav_tag"] = len(fav_rows) >= 1
    out["checks"]["b2_star_has_like_tag"] = len(like_rows) >= 1
    out["checks"]["b2_fav_row_is_fav_item"] = bool(fav_item) and any(D.ITEM_NAMES.get(fav_item, "") in r["t"] for r in fav_rows)
    if fav_rows:
        pg.evaluate("""() => { const rs = [...document.querySelectorAll('#gift-pick-list > *')];
          const f = rs.find(r => (r.innerText||'').includes('★ 最愛')); if (f) { const b = f.querySelector('button') || f; b.click(); } return !!f; }""")
        pg.wait_for_timeout(900)
        conf = D.wait_modal(pg, 4)
        out["favConfirm"] = conf
        out["checks"]["b2_confirm_says_fav"] = "★ 最愛：佢最鍾意呢樣禮物" in (conf.get("body") or "")
        shot(pg, f"star_confirm_fav_{W}x{H}.png")
        # 送出最愛，驗 +4（drive176 已覆數值，呢度順手確認條路行得通）
        out["checks"]["click_send"] = D.click_vis_btn(pg, "送出", "#modal")
        pg.wait_for_timeout(1200)
        res = D.wait_modal(pg, 4)
        out["resultModal"] = res
        out["checks"]["star_fav_plus4"] = "好感 +4" in (res.get("body") or "")
    return out

CASES = {
    "c6c9_932": (case_c6c9, 430, 932),
    "people_932": (case_people, 430, 932),
    "woman_932": (case_woman, 430, 932),
    "woman_700": (case_woman, 430, 700),
    "star_b2_932": (case_star_b2, 430, 932),
    "b3_932": (case_b3, 430, 932),
    "xu_932": (case_xu, 430, 932),
    "mei_932": (case_mei, 430, 932),
}

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    results = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=EXE)
            for name, (fn, W, H) in CASES.items():
                if only != "all" and only != name:
                    continue
                ctx = b.new_context(viewport={"width": W, "height": H})
                pg = ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                out = {"checks": {}}
                try:
                    out = fn(pg, W, H)
                except Exception as e:
                    out["exception"] = repr(e)
                out["pageerrors"] = errs
                ch = out.get("checks", {})
                out["verdict"] = "PASS" if ch and all(ch.values()) and not errs else "FAIL"
                results[name] = out
                print(f"== {name}: {out['verdict']} ({sum(1 for v in ch.values() if v)}/{len(ch)} checks, {len(errs)} pageerrors)")
                for k, v in ch.items():
                    if not v:
                        print(f"   FAIL check: {k}")
                ctx.close()
            b.close()
    finally:
        srv.terminate()
    with open(os.path.join(HERE, "drive183.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v["verdict"] for k, v in results.items()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
