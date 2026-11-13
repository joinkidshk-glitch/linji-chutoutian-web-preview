#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v20a167 live drive: 鄧麗萍咖啡豆 :liked 句補完（用戶 2026-11-13 拍板；v164 殘留 §1.2）。
Usage: /home/hatch/pwenv49/bin/python qa167/drive167.py [root] [port]
本地鏡像 + Playwright（唔直連 github.io），?softPreview=1&softBehaviorGate=1。
 - T0 載入注入：likes 四件（名筆／計數機／腕表＋咖啡豆）；prefKind 咖啡豆 liked；
   reactionEntry('tang','gift_coffee_beans','liked') 返新句（id GR-tang-coffee｜liked，
   兩行全文同寫入一致，TEXTFIX 冇改到）；采兒咖啡 :liked 句唔變；見面前 canGive 鎖住。
 - T1 meet（seed_deng_meet_ready）：揀 data 抉擇後 flag_tang_open＋rel_tang=1；
   事務所行動表出「送禮：鄧麗萍」掣，約談掣消失。
 - T2 UI 送咖啡豆：行真 UI（事務所掣 → 揀禮物 → 確認 → 送出），揀禮物頁咖啡豆行
   標記「喜」；結果見新 :liked 兩行 ＋「排片關係不變」，rel_tang 維持 1，
   weekGiftGain.rel_tang 唔累積（raw +2 唔入帳）。
 - T3 UI 送名筆（順手覆驗）：:liked 句照行，rel_tang 維持 1。
 - T4 UI 送玫瑰（覆驗）：dislike 句照行，rel_tang 維持 1。
 - 全程 0 pageerror。證據全部係 DOM 層（headless_shell 靜態畫面截圖係 stale frame，
   見 NOTES_V20A164 §7 尾，呢票唔截圖、唔當證據）。
Saves qa167/drive167.json under root.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8167
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"

L1 = "鄧麗萍：「咖啡豆，啱用。夜更對帳要頂到天光，冇佢啲數會走樣。」"
L2 = "鄧麗萍：「我收下。你識得將心意變成數字，呢啲先叫實用。」"
NEUTRAL_COFFEE = "夜更對帳用得着。放那邊，我自己煮"
FORBIDDEN = ["綁架我的情緒", "你想我心軟", "感情條款", "tang_commit", "R_tang_ending"]

def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)

def click_vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false; vis[0].click(); return true;
    }""", text)

def modal_text(pg):
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      return m ? m.innerText : '';
    }""")

def seed_entry(pg, seed, secs=45):
    pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1&softBehaviorGate=1&softSeed={seed}")
    for i in range(int(secs / 0.7)):
        if vis_btn(pg, "下一句") or vis_btn(pg, "過一日"):
            return True
        if i == 10:
            try:
                pg.get_by_text("新遊戲", exact=False).first.click(timeout=1500)
                pg.wait_for_timeout(1000)
            except Exception:
                pass
            try:
                pg.evaluate("() => { try { if (window.__softSeed) window.__softSeed.apply(); } catch(e){} }")
            except Exception:
                pass
        pg.wait_for_timeout(700)
    return False

def wait_story_modal(pg, secs=30):
    for i in range(int(secs / 0.7)):
        if vis_btn(pg, "下一句"): return True
        if i == 8:
            pg.evaluate("() => { try { if (window.__softSeed) window.__softSeed.apply(); } catch(e){} }")
        pg.wait_for_timeout(700)
    return False

def dismiss_story_end(pg, secs=15):
    for _ in range(int(secs / 0.7)):
        if vis_btn(pg, "過一日"): return True
        if click_vis_btn(pg, "關閉"):
            pg.wait_for_timeout(700); continue
        if click_vis_btn(pg, "返回地圖"):
            pg.wait_for_timeout(700); continue
        pg.wait_for_timeout(700)
    return vis_btn(pg, "過一日")

def play_story(pg, choice_substr, secs=90):
    texts = []
    picked = False
    for _ in range(int(secs / 0.7)):
        t = modal_text(pg)
        if t and t not in texts: texts.append(t)
        if not picked and choice_substr and click_vis_btn(pg, choice_substr):
            picked = True; pg.wait_for_timeout(800); continue
        if click_vis_btn(pg, "下一句"):
            pg.wait_for_timeout(700); continue
        if vis_btn(pg, "返回地圖") or vis_btn(pg, "過一日"):
            break
        pg.wait_for_timeout(700)
    return {"texts": texts, "picked": picked, "ended_on_map": vis_btn(pg, "過一日")}

def state_probe(pg):
    return pg.evaluate("""() => {
      const out = {};
      try { out.relTang = (typeof S !== 'undefined' && S.story && S.story.rel && S.story.rel.rel_tang); } catch(e){}
      try { out.relTang2 = (typeof S !== 'undefined' && S.rel && S.rel.rel_tang); } catch(e){}
      try { out.flagOpen = (typeof StoryOC !== 'undefined' && StoryOC.getFlag) ? StoryOC.getFlag('flag_tang_open') : null; } catch(e){ out.flagOpen = null; }
      try { out.doneMeet = (typeof StoryOC !== 'undefined' && StoryOC.isDone) ? StoryOC.isDone('R_tang_meet') : null; } catch(e){}
      try { out.money = (typeof S !== 'undefined') ? S.money : null; } catch(e){}
      try { out.inv = (typeof S !== 'undefined') ? (S.inventory || {}) : {}; } catch(e){}
      try { out.dayIndex = (typeof S !== 'undefined') ? S.dayIndex : null; } catch(e){}
      try { out.weekGiftGain = (typeof S !== 'undefined' && S.giftMeta) ? (S.giftMeta.weekGiftGain || {}) : {}; } catch(e){}
      return out;
    }""")

def open_loc(pg, loc_id, secs=12):
    ok = pg.evaluate("""(id) => {
      const pins = [...document.querySelectorAll('[data-loc="' + id + '"]')];
      for (const p of pins) {
        const img = p.querySelector('.pin-img'); if (img) { img.click(); return 'pin-img'; }
        const lab = p.querySelector('.plab'); if (lab) { lab.click(); return 'plab'; }
        p.click(); return 'pin';
      }
      return '';
    }""", loc_id)
    for _ in range(int(secs / 0.7)):
        pg.wait_for_timeout(700)
        if pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }"):
            return ok or True
    return False

def sheet_on(pg):
    return pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }")

def sheet_buttons(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet button, #loc-acts button')]
      .map(b => (b.textContent||'').trim()).filter(Boolean)""")

def wait_packs(pg, secs=45):
    """等 packs 載入＋applyTangGift164／167 行完（likes 有 4 件，含咖啡豆）"""
    last = None
    for _ in range(int(secs / 0.7)):
        try:
            got = pg.evaluate("""() => { try {
              const t = GiftShop.prefFor('tang');
              return t && t.likes ? t.likes.slice() : null; } catch(e){ return null; } }""")
            if got: last = got
            if got and len(got) == 4 and 'gift_coffee_beans' in got:
                return got
        except Exception:
            pass
        pg.wait_for_timeout(700)
    print("wait_packs timeout, last seen likes:", last)
    return last

def gift_via_ui(pg, item_id):
    """喺已開嘅事務所 sheet 撳送禮掣 → 揀貨 → 確認 → 送出；回傳 pick／result 文字。"""
    out = {}
    out["clicked_gift_btn"] = click_vis_btn(pg, "送禮：鄧麗萍")
    pg.wait_for_timeout(1000)
    out["pick_text"] = modal_text(pg)
    out["row_text"] = pg.evaluate("""(id) => {
      const b = document.querySelector('[data-give="' + id + '"]');
      return b ? b.innerText : ''; }""", item_id)
    out["clicked_item"] = pg.evaluate("""(id) => {
      const b = document.querySelector('[data-give="' + id + '"]');
      if (!b) return false; b.click(); return true; }""", item_id)
    pg.wait_for_timeout(900)
    out["confirm_text"] = modal_text(pg)
    out["clicked_send"] = click_vis_btn(pg, "送出")
    pg.wait_for_timeout(1200)
    out["result_text"] = modal_text(pg)
    # 閂結果 modal：go() 會 travelFree 重開事務所 sheet
    click_vis_btn(pg, "關閉")
    pg.wait_for_timeout(1000)
    out["sheet_back"] = sheet_on(pg)
    return out

def next_day(pg):
    pg.evaluate("() => { try { S.dayIndex = (S.dayIndex|0) + 1; if (S.giftMeta) { S.giftMeta.lastGiveDay = {}; S.giftMeta.weekGiftGain = {}; } } catch(e){} }")
    pg.wait_for_timeout(600)

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
results = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)

        # ---------- T0：載入注入＋見面前鎖住 ----------
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        rec = {"test": "T0_load_inject", "pageerrors": 0}
        rec["on_map"] = seed_entry(pg, "seed_deng_meet_ready")
        rec["likes"] = wait_packs(pg)
        rec["prefkinds"] = pg.evaluate("""() => { try { return {
          pen: GiftShop.prefKind('tang','gift_fountain_pen'),
          calc: GiftShop.prefKind('tang','gift_desk_calculator'),
          watch: GiftShop.prefKind('tang','gift_dress_watch'),
          rose: GiftShop.prefKind('tang','gift_rose_premium'),
          coffee: GiftShop.prefKind('tang','gift_coffee_beans'),
          memo: GiftShop.prefKind('tang','gift_memo_pad') }; } catch(e){ return {err: String(e)}; } }""")
        rec["coffee_entry"] = pg.evaluate("""() => { try {
          const e = GiftShop.reactionEntry('tang','gift_coffee_beans','liked');
          return e ? {id: e.id, pref: e.pref, lines: e.lines} : null; } catch(e){ return {err: String(e)}; } }""")
        rec["coffee_neutral_still"] = pg.evaluate("""() => { try {
          const e = GiftShop.reactionEntry('tang','gift_coffee_beans','neutral');
          return e ? e.id : null; } catch(e){ return null; } }""")
        rec["choi_coffee"] = pg.evaluate("""() => { try {
          const e = GiftShop.reactionEntry('choi','gift_coffee_beans','liked');
          return e ? e.id : null; } catch(e){ return null; } }""")
        rec["can_give_before_meet"] = pg.evaluate("() => { try { return GiftShop.canGive('tang'); } catch(e){ return {ok:false, reason:'err:'+e.message}; } }")
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"]
                           and sorted(rec["likes"] or []) == sorted(["gift_fountain_pen", "gift_desk_calculator", "gift_dress_watch", "gift_coffee_beans"])
                           and rec["prefkinds"].get("pen") == "liked" and rec["prefkinds"].get("calc") == "liked"
                           and rec["prefkinds"].get("watch") == "liked" and rec["prefkinds"].get("rose") == "dislike"
                           and rec["prefkinds"].get("coffee") == "liked" and rec["prefkinds"].get("memo") == "neutral"
                           and (rec["coffee_entry"] or {}).get("id") == "GR-tang-coffee｜liked"
                           and (rec["coffee_entry"] or {}).get("pref") == "liked"
                           and (rec["coffee_entry"] or {}).get("lines") == [L1, L2]
                           and rec["coffee_neutral_still"] == "GR-tang-coffee｜neutral"
                           and rec["choi_coffee"] == "GR-choi-coffee｜liked"
                           and rec["can_give_before_meet"].get("ok") is False
                           and "院線那邊" in str(rec["can_give_before_meet"].get("reason", "")))
        results.append(rec)
        print("T0", rec["pass"], "likes:", rec["likes"], "prefkinds:", rec["prefkinds"], "entry:", rec["coffee_entry"])
        ctx.close()

        # ---------- T1：meet → 事務所出送禮掣 ----------
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        rec = {"test": "T1_meet_gift_button", "pageerrors": 0}
        rec["on_map"] = seed_entry(pg, "seed_deng_meet_ready")
        rec["story_modal"] = wait_story_modal(pg)
        if rec["story_modal"]:
            play = play_story(pg, "遞上")
            rec["picked_data_choice"] = play["picked"]
        pg.wait_for_timeout(1200)
        dismiss_story_end(pg)
        st = state_probe(pg)
        rec["flag_tang_open"] = bool(st.get("flagOpen"))
        rec["rel_tang"] = st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")
        rec["done_meet"] = bool(st.get("doneMeet"))
        rec["agency_open"] = open_loc(pg, "agency_ho")
        if rec["agency_open"]:
            btns = sheet_buttons(pg)
            rec["agency_buttons"] = btns
            rec["gift_button_present"] = any("送禮：鄧麗萍" in t for t in btns)
            rec["meet_button_gone"] = not any("鄧麗萍約談排片" in t for t in btns)
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"] and rec["story_modal"] and rec.get("picked_data_choice")
                           and rec["flag_tang_open"] and rec["rel_tang"] == 1 and rec["done_meet"]
                           and rec.get("agency_open") and rec.get("gift_button_present") and rec.get("meet_button_gone"))
        results.append(rec)
        print("T1", rec["pass"], "flag:", rec["flag_tang_open"], "rel:", rec["rel_tang"], "gift_btn:", rec.get("gift_button_present"))
        # 留低呢個 context 做 T2–T4（meet 後狀態：flag 開＋rel 1）
        pg.evaluate("""() => { try {
          S.inventory = S.inventory || {};
          ['gift_fountain_pen','gift_desk_calculator','gift_dress_watch','gift_coffee_beans','gift_rose_premium','gift_memo_pad']
            .forEach(id => { S.inventory[id] = 2; });
          S.money = 10000;
        } catch(e){} }""")

        # ---------- T2：UI 送咖啡豆（新 :liked 句） ----------
        rec = {"test": "T2_ui_gift_coffee_liked", "pageerrors": 0}
        g = gift_via_ui(pg, "gift_coffee_beans")
        rec.update(g)
        st = state_probe(pg)
        rec["rel_tang_after"] = st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")
        rec["coffee_left"] = (st.get("inv") or {}).get("gift_coffee_beans")
        rec["week_gain"] = (st.get("weekGiftGain") or {}).get("rel_tang")
        rec["has_l1"] = L1 in (g.get("result_text") or "")
        rec["has_l2"] = L2 in (g.get("result_text") or "")
        rec["has_neutral_line"] = NEUTRAL_COFFEE in (g.get("result_text") or "")
        rec["has_rel_unchanged"] = "排片關係不變" in (g.get("result_text") or "")
        rec["pick_subtitle_ok"] = "唔會改變排片關係" in (g.get("pick_text") or "")
        rec["pick_tag_liked"] = "喜" in (g.get("row_text") or "")
        rec["forbidden"] = [w for w in FORBIDDEN if w in (g.get("result_text") or "")]
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(g.get("clicked_gift_btn") and g.get("clicked_item") and g.get("clicked_send")
                           and rec["has_l1"] and rec["has_l2"] and not rec["has_neutral_line"]
                           and rec["has_rel_unchanged"] and rec["pick_subtitle_ok"] and rec["pick_tag_liked"]
                           and rec["rel_tang_after"] == 1 and rec["coffee_left"] == 1
                           and rec["week_gain"] in (None, 0) and not rec["forbidden"]
                           and g.get("sheet_back"))
        results.append(rec)
        print("T2", rec["pass"], "l1:", rec["has_l1"], "l2:", rec["has_l2"], "rel:", rec["rel_tang_after"],
              "left:", rec["coffee_left"], "week_gain:", rec["week_gain"], "tag:", rec["pick_tag_liked"])

        # ---------- T3：UI 送名筆（:liked 句照行，覆驗） ----------
        next_day(pg)
        rec = {"test": "T3_ui_gift_pen_regress", "pageerrors": 0}
        g = gift_via_ui(pg, "gift_fountain_pen")
        rec.update(g)
        st = state_probe(pg)
        rec["rel_tang_after"] = st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")
        rec["pen_left"] = (st.get("inv") or {}).get("gift_fountain_pen")
        rec["has_pen_line"] = "名筆。簽名、批檔期、改數字，都用得著。" in (g.get("result_text") or "")
        rec["has_rel_unchanged"] = "排片關係不變" in (g.get("result_text") or "")
        rec["forbidden"] = [w for w in FORBIDDEN if w in (g.get("result_text") or "")]
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(g.get("clicked_gift_btn") and g.get("clicked_item") and g.get("clicked_send")
                           and rec["has_pen_line"] and rec["has_rel_unchanged"]
                           and rec["rel_tang_after"] == 1 and rec["pen_left"] == 1 and not rec["forbidden"]
                           and g.get("sheet_back"))
        results.append(rec)
        print("T3", rec["pass"], "pen_line:", rec["has_pen_line"], "rel:", rec["rel_tang_after"], "left:", rec["pen_left"])

        # ---------- T4：UI 送玫瑰（dislike 句照行，覆驗） ----------
        next_day(pg)
        rec = {"test": "T4_ui_gift_rose_regress", "pageerrors": 0}
        g = gift_via_ui(pg, "gift_rose_premium")
        rec.update(g)
        st = state_probe(pg)
        rec["rel_tang_after"] = st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")
        rec["has_rose_line"] = "呢度係排片部，唔係花店" in (g.get("result_text") or "")
        rec["has_rel_unchanged"] = "排片關係不變" in (g.get("result_text") or "")
        rec["forbidden"] = [w for w in FORBIDDEN if w in (g.get("result_text") or "")]
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(g.get("clicked_gift_btn") and g.get("clicked_item") and g.get("clicked_send")
                           and rec["has_rose_line"] and rec["has_rel_unchanged"]
                           and rec["rel_tang_after"] == 1 and not rec["forbidden"] and g.get("sheet_back"))
        results.append(rec)
        print("T4", rec["pass"], "rose_line:", rec["has_rose_line"], "rel:", rec["rel_tang_after"])
        ctx.close()
        b.close()
finally:
    srv.terminate()
with open(os.path.join(ROOT, "qa167", "drive167.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
n_pass = sum(1 for r in results if r.get("pass") and r.get("pageerrors") == 0)
print(f"OVERALL {n_pass}/{len(results)}")
