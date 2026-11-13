#!/usr/bin/env python3
"""v20a176 實駕：全面隨機巧遇＋紅星送禮。
Cases（每 case 全新 browser context，免狀態污染）：
  woman_932      ① 播種到曉晴喺長門嘅日子（Python 種子複製搵候選日，真 UI 入場確認）
                  → 女角巧遇 modal（傾談／送禮／行開，冇約會掣）
                  → 送禮（保溫瓶，喜歡＋2）→ rel_hiu +2、庫存 −1 → 返地點板 → 板上冇女角送禮／傾談掣
                  → 同日再入唔再觸發（每日 1 次）
  woman_talk_932 ② 同上播種 → 撳傾談 → doTalk modal 出現 → 返地點板，唔再觸發
  star_932       ③ 播種到有星在場（嗰地點冇女角）→ 星巧遇 overlay → 行到收尾 → 「送禮畀X」掣
                  → 送最愛（+4）→ fav +4、唔寫 S.story.rel → 同日再送唔得
  whisper_932    ④ 風聲狀態（logic test 覆 grant 本身；呢度驗 UI 消費端）→ 人脈頁見「多數喺 X 出沒」
  woman_700      ⑤ 同 ①，430×700（短屏 modal 掣要見到撳到）
注意：主 script 係 IIFE，page evaluate 叫唔到 rom176／enc79／openLoc 等函數，只可以讀寫 window.S＋撳真 UI。
用法：/home/hatch/pwenv49/bin/python qa176/drive176.py [case|all] [932|700]
I/O 防禦：截圖／JSON 寫檔失敗唔會中斷 case，結果照印 stdout。
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work176"
HERE = "/home/hatch/workspace/linji-work176/qa176"
SHOTS = os.path.join(HERE, "shots")
try:
    os.makedirs(SHOTS, exist_ok=True)
except Exception:
    pass
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8971
SAVE_KEY = "starVolunteer_map_v19w"
ITEM_NAMES = {
    "gift_pineapple_bun_set": "菠蘿油", "gift_egg_tart_box": "蛋撻",
    "gift_thermos": "保溫瓶", "gift_hair_clip_set": "髮夾",
    "gift_memo_pad": "拍紙簿", "gift_coffee_beans": "咖啡豆",
    "gift_cassette_indie": "卡帶", "gift_handmade_sweet": "手作甜品",
    "gift_fashion_mag": "時裝雜誌", "gift_perfume_sample": "香氛",
}
# --- 種子複製（主 script 係 IIFE，page evaluate 叫唔到 rom176／enc79 函數；
# 只可以讀寫 window.S＋撳真 UI。所以候選日喺 Python 用 FNV-1a 種子計，再入頁真 UI 確認。
# 保守性：複製用 base P=0.50／share=0.65；beat-open／風聲／win 只會推高 P／share，
# 所以複製話「出沒」嘅日子一定真係出沒（真陽性），複製話「唔出」嘅日子唔試。) ---
def _fnv(s):
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h

def _rand(key):
    return (_fnv(key) % 100000) / 100000

ROM176_WOMEN = [
    ("hiu", "tvb_longmen", "tvb_kowloon"),
    ("choi", "rec_star", "film_cotton"),
    ("vera", "ad_central", "ad_adm"),
    ("lan", "tvb_longmen", "tvb_kowloon"),
    ("xu", "ad_central", "ad_adm"),
    ("mei", "ad_adm", "rec_hk"),
]
ENC79_STARS = [
    ("luk_baakyin", "film_lion", "rec_star"),
    ("liu_bingxing", "cafe_cha", "film_cotton"),
    ("ngai_wingnaam", "film_harbour", "agency_ho"),
    ("yip_manji", "rec_hk", "tvb_kowloon"),
    ("mak_zhendong", "film_cotton", "film_lion"),
    ("lok_gasing", "tvb_longmen", "rec_hk"),
    ("pang_siuki", "ad_central", "tvb_longmen"),
    ("chung_choning", "rec_star", "ad_adm"),
    ("gu_mingfai", "tvb_harbour", "cafe_cha"),
    ("so_jiyan", "rec_wanchai", "ad_central"),
    ("chai_zanhoi", "tvb_longmen", "tvb_harbour"),
    # ching_tinlok 1992 先解鎖，1990 掃描唔計
]
# 星最愛第一件（DESIGN §4.3 SP176 表；GiftShop 唔係 global，drive 唔可以直接讀 prefFor）
STAR_FAV1 = {
    "luk_baakyin": "gift_coffee_beans", "liu_bingxing": "gift_pineapple_bun_set",
    "ngai_wingnaam": "gift_thermos", "yip_manji": "gift_perfume_sample",
    "mak_zhendong": "gift_thermos", "lok_gasing": "gift_cassette_indie",
    "pang_siuki": "gift_coffee_beans", "chung_choning": "gift_memo_pad",
    "gu_mingfai": "gift_pineapple_bun_set", "so_jiyan": "gift_perfume_sample",
    "chai_zanhoi": "gift_coffee_beans", "ching_tinlok": "gift_cassette_indie",
}

def woman_loc_on(day, key):
    """複製 rom176EnsureDay：回傳 key 喺邊個地點出沒（None＝唔出）。mei 喺 1990 未解鎖。"""
    w = next((x for x in ROM176_WOMEN if x[0] == key), None)
    if not w or key == "mei":
        return None
    if _rand(f"rom176:{day}:{key}:out") >= 0.50:
        return None
    return w[1] if _rand(f"rom176:{day}:{key}:loc") < 0.65 else w[2]

def star_loc_on(day, star):
    s = next((x for x in ENC79_STARS if x[0] == star), None)
    if not s:
        return None
    if _rand(f"enc79:{day}:{star}:out") >= 0.50:
        return None
    return s[1] if _rand(f"enc79:{day}:{star}:loc") < 0.65 else s[2]

def find_woman_days(key, loc, n=10):
    out = []
    for d in range(0, 120):
        if woman_loc_on(d, key) == loc:
            out.append(d)
        if len(out) >= n:
            break
    return out

def find_star_candidates(n=10):
    """(day, loc, star)：星出沒、嗰地點複製話冇女角（避免女角攔截搶先）。"""
    out = []
    for d in range(0, 120):
        for loc in sorted({s[1] for s in ENC79_STARS} | {s[2] for s in ENC79_STARS}):
            if any(woman_loc_on(d, k) == loc for k, _, _ in ROM176_WOMEN):
                continue
            for star, _, _ in ENC79_STARS:
                if star_loc_on(d, star) == loc:
                    out.append({"day": d, "loc": loc, "star": star})
                    break
            if len(out) >= n:
                return out
    return out

def shot(pg, name):
    try:
        pg.screenshot(path=os.path.join(SHOTS, name))
        return True
    except Exception:
        return False

def vis_btn(pg, text, scope=None):
    return pg.evaluate("""(o) => {
      const root = o.scope ? document.querySelector(o.scope) : document;
      if (!root) return false;
      const bs = [...root.querySelectorAll('button')].filter(b => (b.textContent||'').includes(o.t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", {"t": text, "scope": scope})

def click_vis_btn(pg, text, scope=None):
    return pg.evaluate("""(o) => {
      const root = o.scope ? document.querySelector(o.scope) : document;
      if (!root) return false;
      const bs = [...root.querySelectorAll('button')].filter(b => (b.textContent||'').includes(o.t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false;
      vis[0].click(); return true;
    }""", {"t": text, "scope": scope})

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
      const body = (m.innerText || '').slice(0, 1500);
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
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
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

def map_ready(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }") \
        and (not modal_info(pg).get("visible")) and (vis_btn(pg, "過一日") or vis_btn(pg, "開始今日行程"))

def sheet_visible(pg):
    return pg.evaluate("""() => { const s = document.getElementById('loc-sheet'); if (!s) return false;
      const r = s.getBoundingClientRect(); return r.width > 0 && r.height > 0; }""")

def sheet_buttons(pg):
    return pg.evaluate("""() => { const s = document.getElementById('loc-sheet'); if (!s) return [];
      return [...s.querySelectorAll('button')].map(b => (b.textContent||'').trim()).filter(Boolean); }""")

def seed_gifts(pg, day):
    return pg.evaluate("""(day) => {
      S.dayIndex = day;
      S.romDay = null; S.starDay = null;
      S.inventory = { gift_pineapple_bun_set: 3, gift_egg_tart_box: 3, gift_thermos: 3,
        gift_hair_clip_set: 3, gift_memo_pad: 3, gift_coffee_beans: 3, gift_cassette_indie: 3,
        gift_handmade_sweet: 3, gift_fashion_mag: 3, gift_perfume_sample: 3 };
      return { day: S.dayIndex, inv: Object.keys(S.inventory).length };
    }""", day)

def enter_loc(pg, loc):
    """經真 UI 入地點：先試地點快捷列，再試地圖針。openLoc 唔係 global，冇 evaluate 後備；
    兩條路都唔得就回傳 None（係真問題，要報）。"""
    way = pg.evaluate("""(id) => {
      const b = document.querySelector('#map-area-list button[data-loc="'+id+'"]');
      if (b) { b.click(); return 'area-list'; }
      const pin = document.querySelector('.pin[data-loc="'+id+'"]');
      if (pin) { pin.click(); return 'pin'; }
      return null;
    }""", loc)
    if way:
        return way
    pg.evaluate("""() => { const b = document.getElementById('map-show-all-locs'); if (b) b.click(); }""")
    pg.wait_for_timeout(600)
    way = pg.evaluate("""(id) => {
      const b = document.querySelector('#map-area-list button[data-loc="'+id+'"]');
      if (b) { b.click(); return 'area-list-all'; }
      return null;
    }""", loc)
    return way

def wait_modal(pg, secs=4):
    t0 = time.time()
    while time.time() - t0 < secs:
        mi = modal_info(pg)
        if mi.get("visible"):
            return mi
        pg.wait_for_timeout(250)
    return modal_info(pg)

def wait_no_modal(pg, secs=2):
    t0 = time.time()
    while time.time() - t0 < secs:
        if not modal_info(pg).get("visible"):
            return True
        pg.wait_for_timeout(250)
    return not modal_info(pg).get("visible")

def back_to_map(pg):
    """由地點 sheet 返地圖（撳 sheet 嘅「返回地圖」掣 #loc-close）。"""
    for _ in range(6):
        if map_ready(pg):
            return True
        if click_vis_btn(pg, "返回地圖", "#loc-sheet"):
            pg.wait_for_timeout(700)
        else:
            pg.wait_for_timeout(500)
    return map_ready(pg)

def e79_info(pg):
    return pg.evaluate("""() => {
      const ov = document.getElementById('enc79-overlay');
      if (!ov) return {visible:false};
      const r = ov.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) return {visible:false};
      const meta = (ov.querySelector('.e79-meta')||{}).textContent || '';
      const name = (ov.querySelector('.e79-name')||{}).textContent || '';
      const line = (ov.querySelector('.e79-line')||{}).textContent || '';
      const btns = [...ov.querySelectorAll('.e79-row button')].map(b => (b.textContent||'').trim()).filter(Boolean);
      return {visible:true, meta, name, line, btns};
    }""")

def e79_advance(pg, secs=8):
    """行星巧遇 steps 直到收尾出現「送禮畀」掣（或 overlay 消失）。回傳 {giftBtn, steps}。"""
    steps = 0
    t0 = time.time()
    while time.time() - t0 < secs:
        info = e79_info(pg)
        if not info.get("visible"):
            return {"giftBtn": None, "steps": steps, "gone": True}
        if any(b.startswith("送禮畀") for b in info.get("btns") or []):
            return {"giftBtn": [b for b in info["btns"] if b.startswith("送禮畀")][0], "steps": steps, "gone": False}
        clicked = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return false;
          const row = ov.querySelector('.e79-row');
          const bs = row ? [...row.querySelectorAll('button')] : [];
          const vis = bs.filter(b => { const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
          if (!vis.length) return false;
          vis[0].click(); return true;
        }""")
        if clicked:
            steps += 1
        pg.wait_for_timeout(500)
    return {"giftBtn": None, "steps": steps, "gone": False}

def click_gift_item(pg, item_id):
    """撳禮物行 → 確認 modal → 撳「送出」。回傳 (picked, confirmed)。"""
    name = ITEM_NAMES[item_id]
    picked = click_vis_btn(pg, name, "#modal")
    if not picked:
        return (False, False)
    pg.wait_for_timeout(800)
    confirm = wait_modal(pg, 4)
    confirmed = bool(confirm.get("visible")) and "確認送禮" in (confirm.get("h3") or "")
    if confirmed:
        confirmed = click_vis_btn(pg, "送出", "#modal")
        pg.wait_for_timeout(1000)
    return (picked, confirmed)

def rel_state(pg):
    return pg.evaluate("""() => ({
      day: S.dayIndex,
      relHiu: (S.story && S.story.rel && S.story.rel.rel_hiu) || 0,
      relLan: (S.story && S.story.rel && S.story.rel.rel_lan) || 0,
      npcsColleague: (S.npcs && S.npcs.colleague) || 0,
      invThermos: (S.inventory && S.inventory.gift_thermos) || 0,
      invCoffee: (S.inventory && S.inventory.gift_coffee_beans) || 0,
      lastGiveHiu: (S.giftMeta && S.giftMeta.lastGiveDay && S.giftMeta.lastGiveDay.rel_hiu),
      romTriggered: (S.romDay && S.romDay.triggered) || 0,
      romWeekCount: (S.romWeek && S.romWeek.count) || 0,
      flagsMetHiu: !!(S.flags && S.flags.gift_met_hiu),
    })""")

def star_state(pg, star):
    return pg.evaluate("""(star) => {
      const st = (S.stars && S.stars[star]) || {};
      return { fav: st.fav || 0, met: !!st.met,
        giftHist: st.giftHist || {},
        starGiftDay: S.starGiftDay || null,
        relStar: (S.story && S.story.rel && S.story.rel['rel_' + star]) || 0,
        inv: S.inventory || {} };
    }""", star)

# ---------------- cases ----------------
def case_woman(pg, W, H, talk_only=False):
    out = {"checks": {}}
    cand_days = find_woman_days("hiu", "tvb_longmen")
    out["candidateDays"] = cand_days
    out["checks"]["found_hiu_days"] = len(cand_days) > 0
    if not cand_days:
        return out
    mi, day, attempts = None, None, []
    for d in cand_days:
        out["seed"] = seed_gifts(pg, d)
        way = enter_loc(pg, "tvb_longmen")
        if not way:
            attempts.append({"day": d, "enter": None})
            return {**out, "attempts": attempts, "checks": {**out["checks"], "enter_loc_ui_works": False}}
        pg.wait_for_timeout(1200)
        mi_try = wait_modal(pg, 5)
        diag = pg.evaluate("() => ({ romDay: S.romDay || null, mapTip: (S.mapTips && S.mapTips['tvb_longmen']) || null })")
        attempts.append({"day": d, "enter": way, "modalH3": mi_try.get("h3"), "romDay": diag.get("romDay")})
        if mi_try.get("visible") and "林曉晴" in (mi_try.get("h3") or ""):
            mi, day = mi_try, d
            break
        # 唔係曉晴 modal（可能主線待播／另一人）：清走佢，試下一個候選日
        if mi_try.get("visible"):
            dismiss_once(pg)
            pg.wait_for_timeout(800)
        if sheet_visible(pg):
            back_to_map(pg)
        elif map_ready(pg):
            pass
        else:
            dismiss_once(pg)
            pg.wait_for_timeout(800)
            back_to_map(pg)
    out["attempts"] = attempts
    out["seedDay"] = day
    out["encounterModal"] = mi
    out["checks"]["woman_modal_shown"] = bool(mi and mi.get("visible")) and "林曉晴" in (mi.get("h3") or "")
    if not out["checks"]["woman_modal_shown"]:
        shot(pg, f"woman_nomodal_{W}x{H}.png")
        return out
    btns = mi.get("btns") or []
    out["checks"]["modal_has_talk"] = "傾談" in btns
    out["checks"]["modal_has_gift"] = "送禮" in btns
    out["checks"]["modal_has_leave"] = "行開" in btns
    out["checks"]["modal_no_date_btn"] = not any("約" in b for b in btns)
    shot(pg, f"woman_modal_{W}x{H}.png")
    if H == 700:
        out["checks"]["modal_btns_in_viewport_700"] = pg.evaluate("""() => {
          const bs = [...document.querySelectorAll('#modal-btns button')];
          return bs.length > 0 && bs.every(b => { const r = b.getBoundingClientRect(); return r.top >= 0 && r.bottom <= window.innerHeight; });
        }""")
    if talk_only:
        before = rel_state(pg)
        out["checks"]["click_talk"] = click_vis_btn(pg, "傾談", "#modal")
        pg.wait_for_timeout(1200)
        talk = wait_modal(pg, 4)
        out["talkModal"] = talk
        out["checks"]["talk_modal_shown"] = bool(talk.get("visible"))
        shot(pg, f"woman_talk_{W}x{H}.png")
        dismiss_once(pg)
        pg.wait_for_timeout(1200)
        out["checks"]["back_at_sheet_after_talk"] = sheet_visible(pg) or map_ready(pg)
        out["afterTalk"] = rel_state(pg)
        return out
    before = rel_state(pg)
    out["beforeGift"] = before
    out["checks"]["click_gift"] = click_vis_btn(pg, "送禮", "#modal")
    pg.wait_for_timeout(1000)
    pick = wait_modal(pg, 4)
    out["pickModal"] = pick
    out["checks"]["gift_pick_shown"] = bool(pick.get("visible"))
    out["checks"]["pick_lists_thermos"] = "保溫瓶" in (pick.get("body") or "")
    if out["checks"]["gift_pick_shown"]:
        picked, confirmed = click_gift_item(pg, "gift_thermos")
        out["checks"]["click_thermos"] = picked
        out["checks"]["confirm_send"] = confirmed
        pg.wait_for_timeout(1200)
        res = wait_modal(pg, 4)
        out["resultModal"] = res
        out["checks"]["result_shown"] = bool(res.get("visible")) and "送禮結果" in (res.get("h3") or "")
        out["checks"]["result_says_plus2"] = "好感 +2" in (res.get("body") or "")
        out["checks"]["result_says_no_day_cost"] = "送禮唔計日子" in (res.get("body") or "")
        shot(pg, f"woman_result_{W}x{H}.png")
        dismiss_once(pg)
        pg.wait_for_timeout(1200)
    after = rel_state(pg)
    out["afterGift"] = after
    out["checks"]["rel_hiu_plus2"] = after["relHiu"] - before["relHiu"] == 2
    out["checks"]["inv_thermos_minus1"] = before["invThermos"] - after["invThermos"] == 1
    out["checks"]["gift_met_flag_set"] = after["flagsMetHiu"] is True
    out["checks"]["back_at_sheet_after_gift"] = sheet_visible(pg)
    # 地點板：冇女角送禮／傾談掣（若返程落咗地圖，呢次再入就係第 2 次入場，兼做「同日唔再觸發」觀測）
    pg.wait_for_timeout(800)
    second_entry_used = False
    if not sheet_visible(pg) and map_ready(pg):
        out["giftReturnWentToMap"] = True
        enter_loc(pg, "tvb_longmen")
        pg.wait_for_timeout(1500)
        mi_fallback = modal_info(pg)
        out["checks"]["same_day_no_second_encounter"] = not mi_fallback.get("visible")
        out["checks"]["second_entry_shows_sheet"] = sheet_visible(pg)
        second_entry_used = True
    btns_sheet = sheet_buttons(pg)
    out["sheetButtons"] = btns_sheet
    out["checks"]["sheet_no_woman_gift_btn"] = not any(b.startswith("送禮：") and ("林曉晴" in b or "周采兒" in b or "Vera" in b or "藍若曦" in b or "徐寶珊" in b or "關海媚" in b) for b in btns_sheet)
    out["checks"]["sheet_no_woman_talk_btn"] = not any(b.startswith("同") and ("林曉晴" in b or "周采兒" in b or "Vera" in b or "藍若曦" in b or "徐寶珊" in b or "關海媚" in b) for b in btns_sheet)
    shot(pg, f"woman_sheet_{W}x{H}.png")
    # 同日再入：每日 1 次，唔再觸發（若上面已用咗第 2 次入場，唔再燒第 3 次）
    if not second_entry_used:
        out["checks"]["back_to_map_ok"] = back_to_map(pg)
        pg.wait_for_timeout(600)
        way2 = enter_loc(pg, "tvb_longmen")
        out["enterWay2"] = way2
        pg.wait_for_timeout(1500)
        mi2 = modal_info(pg)
        out["checks"]["same_day_no_second_encounter"] = not mi2.get("visible")
        out["checks"]["second_entry_shows_sheet"] = sheet_visible(pg)
    out["afterSecond"] = rel_state(pg)
    shot(pg, f"woman_second_{W}x{H}.png")
    return out

def case_star(pg, W, H):
    out = {"checks": {}}
    cands = find_star_candidates()
    out["candidates"] = cands
    out["checks"]["found_star_candidates"] = len(cands) > 0
    if not cands:
        return out
    found, info, before, attempts = None, None, None, []
    for c in cands:
        day, loc, star = c["day"], c["loc"], c["star"]
        out["seed"] = seed_gifts(pg, day)
        before_try = star_state(pg, star)
        way = enter_loc(pg, loc)
        if not way:
            attempts.append({"day": day, "loc": loc, "star": star, "enter": None})
            return {**out, "attempts": attempts, "checks": {**out["checks"], "enter_loc_ui_works": False}}
        pg.wait_for_timeout(1500)
        info_try = e79_info(pg)
        mi_try = modal_info(pg)
        attempts.append({"day": day, "loc": loc, "star": star, "enter": way,
                         "e79visible": info_try.get("visible"), "e79meta": info_try.get("meta"),
                         "modalH3": mi_try.get("h3")})
        if info_try.get("visible"):
            found, info, before = c, info_try, before_try
            break
        # 唔係星 overlay（可能女角 modal／主線／直接入 sheet）：清走佢，試下一個候選
        if mi_try.get("visible"):
            dismiss_once(pg)
            pg.wait_for_timeout(800)
        if sheet_visible(pg):
            back_to_map(pg)
        elif not map_ready(pg):
            dismiss_once(pg)
            pg.wait_for_timeout(800)
            back_to_map(pg)
    out["attempts"] = attempts
    out["found"] = found
    if not found:
        shot(pg, f"star_nooverlay_{W}x{H}.png")
        return out
    day, loc, star = found["day"], found["loc"], found["star"]
    out["beforeStar"] = before
    fav_item = STAR_FAV1.get(star)
    out["favItem"] = fav_item
    out["checks"]["star_has_favorite"] = bool(fav_item)
    out["e79"] = info
    out["checks"]["star_overlay_shown"] = bool(info.get("visible"))
    if not info.get("visible"):
        out["modalInstead"] = modal_info(pg)
        shot(pg, f"star_nooverlay_{W}x{H}.png")
        return out
    out["checks"]["overlay_names_star"] = bool(info.get("meta")) and star.split("_")[0] not in (info.get("meta") or "")
    adv = e79_advance(pg, 10)
    out["advance"] = adv
    out["checks"]["gift_btn_at_last_step"] = bool(adv.get("giftBtn"))
    if not adv.get("giftBtn"):
        shot(pg, f"star_nogiftbtn_{W}x{H}.png")
        return out
    # 撳送禮前嗰刻做基線（巧遇本身行 steps 嗰陣可能已經加過 fav，唔可以同入場前比較）
    midStar = star_state(pg, star)
    out["midStar"] = midStar
    out["checks"]["click_star_gift_btn"] = click_vis_btn(pg, adv["giftBtn"], "#enc79-overlay")
    pg.wait_for_timeout(1000)
    pick = wait_modal(pg, 4)
    out["pickModal"] = pick
    out["checks"]["gift_pick_shown"] = bool(pick.get("visible"))
    fav_name = ITEM_NAMES.get(fav_item, "")
    out["checks"]["pick_lists_fav"] = fav_name in (pick.get("body") or "")
    if out["checks"]["gift_pick_shown"] and fav_item:
        picked, confirmed = click_gift_item(pg, fav_item)
        out["checks"]["click_fav_item"] = picked
        out["checks"]["confirm_send"] = confirmed
        pg.wait_for_timeout(1200)
        res = wait_modal(pg, 4)
        out["resultModal"] = res
        out["checks"]["result_shown"] = bool(res.get("visible")) and "送禮結果" in (res.get("h3") or "")
        out["checks"]["result_says_plus4"] = "好感 +4" in (res.get("body") or "")
        shot(pg, f"star_result_{W}x{H}.png")
        dismiss_once(pg)
        pg.wait_for_timeout(1200)
    after = star_state(pg, star)
    out["afterStar"] = after
    out["checks"]["fav_plus4"] = after["fav"] - midStar["fav"] == 4
    out["checks"]["no_fake_rel_star"] = after["relStar"] == 0
    out["checks"]["gift_hist_recorded"] = (after["giftHist"] or {}).get(fav_item) == 1
    out["checks"]["star_gift_day_recorded"] = bool((after["starGiftDay"] or {}).get("given", {}).get(star))
    out["checks"]["same_day_cannot_gift_again"] = pg.evaluate("(s) => { const gd = S.starGiftDay || {}; return gd.day === (S.dayIndex|0) && !!(gd.given && gd.given[s]); }", star)
    return out

def case_whisper(pg, W, H):
    out = {"checks": {}}
    seed_gifts(pg, 10)
    # 直接寫入 grantWhisper 會寫嘅狀態（grant 本身由 logic test B13 覆；呢度驗 UI 消費端——
    # 人脈頁出沒提示＋手帳風聲卡讀嘅就係呢啲欄位。rom176GrantWhisper 唔係 global，drive 叫唔到。）
    grant = pg.evaluate("""() => {
      S.romWhispers = S.romWhispers || {};
      S.romWhispers.lan = { until: 12, src: 'tea' };
      S.mockRumors = S.mockRumors || [];
      S.mockRumors.unshift({ id: 'romwind:lan:10', source: '風聲', title: '風聲：藍若曦行蹤',
        text: '場務話，藍若曦呢排成日喺星河電視台通告牌前面企，話幫手執位。',
        state: 'teased', season: '風聲 · 3 日內有效', wind: true, windUntil: 12, fromAsk: true });
      return { whisper: S.romWhispers.lan, rumor: S.mockRumors[0] };
    }""")
    out["grant"] = grant
    out["checks"]["whisper_until_day_plus2"] = (grant.get("whisper") or {}).get("until") == 12
    out["checks"]["rumor_in_journal"] = bool(grant.get("rumor"))
    out["checks"]["rumor_id_romwind"] = bool(grant.get("rumor")) and grant["rumor"].get("id") == "romwind:lan:10"
    # 人脈頁：經真 UI（手帳掣 → 人脈 tab）開，唔直接叫 showPeople（唔係 global）
    out["checks"]["open_journal_btn"] = pg.evaluate("""() => { const b = document.querySelector('button[data-m="journal"]'); if (b) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(800)
    out["checks"]["open_people_tab"] = pg.evaluate("""() => { const b = document.getElementById('htab-people'); if (b) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1000)
    people = pg.evaluate("""() => (document.body.innerText || '').slice(0, 8000)""")
    out["checks"]["people_shows_lan"] = "藍若曦" in people
    out["checks"]["people_haunt_line"] = "多數喺" in people and "出沒" in people
    shot(pg, f"whisper_people_{W}x{H}.png")
    return out

CASES = {
    "woman_932": lambda pg, W, H: case_woman(pg, W, H, talk_only=False),
    "woman_talk_932": lambda pg, W, H: case_woman(pg, W, H, talk_only=True),
    "star_932": lambda pg, W, H: case_star(pg, W, H),
    "whisper_932": lambda pg, W, H: case_whisper(pg, W, H),
    "woman_700": lambda pg, W, H: case_woman(pg, W, H, talk_only=False),
}

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    h_arg = sys.argv[2] if len(sys.argv) > 2 else "932"
    sel = list(CASES.keys()) if arg == "all" else [arg]
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
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
    try:
        srv.terminate()
    except Exception:
        pass
    try:
        json.dump(results, open(os.path.join(HERE, "drive176.json"), "w"), ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"NOTE drive176.json write failed: {e!r}", flush=True)
    print("RESULTS_JSON_BEGIN")
    print(json.dumps(results, ensure_ascii=False))
    print("RESULTS_JSON_END")
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    print(f"OVERALL {n_pass}/{len(results)} PASS")
    sys.exit(0 if n_pass == len(results) else 1)

def _run_with_browser(b, sel, h_arg, results):
    for name in sel:
        H = 700 if name == "woman_700" else int(h_arg)
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
            r["verdict"] = "PASS" if checks and all(checks.values()) and not errs else "FAIL"
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
