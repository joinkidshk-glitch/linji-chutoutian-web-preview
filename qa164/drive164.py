#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v20a164 live drive: 鄧麗萍送禮補完（v152 殘留）。
Usage: /home/hatch/pwenv49/bin/python qa164/drive164.py [root] [port]
本地鏡像 + Playwright（唔直連 github.io），?softPreview=1&softBehaviorGate=1。
 - T0 載入注入：packs 載入後 prefKind 分流（名筆／計數機／腕表 liked、玫瑰 dislike、
   咖啡豆／拍紙簿 neutral）；四件新貨入咗 items＋shop_street_mk；見面前 canGive 鎖住。
 - T1 meet（seed_deng_meet_ready）：揀 data 抉擇後 flag_tang_open＋rel_tang=1；
   事務所行動表出「送禮：鄧麗萍」掣，約談掣消失。
 - T2 UI 送名筆：行真 UI（事務所掣 → 揀禮物 → 確認 → 送出），見 :liked 專屬句
   ＋「排片關係不變」，rel_tang 維持 1（唔加分）。
 - T3 UI 送玫瑰：見新公事拒收句（「呢度係排片部，唔係花店」），rel_tang 維持 1（−1 唔扣）。
 - T4 UI 送咖啡豆：見 :neutral 專屬句，rel_tang 維持 1。
 - T5 買貨：廟街禮品檔買到名筆（$550），庫存＋1、錢 −550。
 - T6 排片線照行：seed_deng_push_ready，事務所 push2 掣＋送禮掣並存，撳 push2
   播到 crisis 唔撳錯（新掣唔干擾舊掣）。
 - 全程 0 pageerror。
Saves qa164/shots164/*.png + qa164/drive164.json under root.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8164
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = os.path.join(ROOT, "qa164", "shots164")
os.makedirs(SHOTS, exist_ok=True)

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

def page_text(pg):
    return pg.evaluate("() => document.body.innerText || ''")

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

def wait_packs(pg, secs=20):
    """等 packs 載入＋applyTangGift164 行完（likes 有 3 件）"""
    for _ in range(int(secs / 0.7)):
        try:
            got = pg.evaluate("""() => { try {
              const t = GiftShop.prefFor('tang');
              return t && t.likes ? t.likes.slice() : null; } catch(e){ return null; } }""")
            if got and len(got) == 3:
                return got
        except Exception:
            pass
        pg.wait_for_timeout(700)
    return None

def gift_via_ui(pg, item_id, shot):
    """喺已開嘅事務所 sheet 撳送禮掣 → 揀貨 → 確認 → 送出；回傳 pick／result 文字。"""
    out = {}
    out["clicked_gift_btn"] = click_vis_btn(pg, "送禮：鄧麗萍")
    pg.wait_for_timeout(1000)
    out["pick_text"] = modal_text(pg)
    out["clicked_item"] = pg.evaluate("""(id) => {
      const b = document.querySelector('[data-give="' + id + '"]');
      if (!b) return false; b.click(); return true; }""", item_id)
    pg.wait_for_timeout(900)
    out["confirm_text"] = modal_text(pg)
    out["clicked_send"] = click_vis_btn(pg, "送出")
    pg.wait_for_timeout(1200)
    out["result_text"] = modal_text(pg)
    pg.screenshot(path=f"{SHOTS}/{shot}.png")
    # 閂結果 modal：go() 會 travelFree 重開事務所 sheet
    click_vis_btn(pg, "關閉")
    pg.wait_for_timeout(1000)
    out["sheet_back"] = sheet_on(pg)
    return out

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
        rec["shop_items"] = pg.evaluate("""() => { try {
          return GiftShop.shopList('shop_street_mk').map(r => r.itemId); } catch(e){ return ['err:'+e.message]; } }""")
        rec["can_give_before_meet"] = pg.evaluate("() => { try { return GiftShop.canGive('tang'); } catch(e){ return {ok:false, reason:'err:'+e.message}; } }")
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"] and rec["likes"] == ["gift_fountain_pen", "gift_desk_calculator", "gift_dress_watch"]
                           and rec["prefkinds"].get("pen") == "liked" and rec["prefkinds"].get("calc") == "liked"
                           and rec["prefkinds"].get("watch") == "liked" and rec["prefkinds"].get("rose") == "dislike"
                           and rec["prefkinds"].get("coffee") == "neutral" and rec["prefkinds"].get("memo") == "neutral"
                           and all(x in (rec["shop_items"] or []) for x in
                                   ["gift_fountain_pen", "gift_desk_calculator", "gift_dress_watch", "gift_rose_premium"])
                           and rec["can_give_before_meet"].get("ok") is False
                           and "院線那邊" in str(rec["can_give_before_meet"].get("reason", "")))
        results.append(rec)
        print("T0", rec["pass"], "likes:", rec["likes"], "prefkinds:", rec["prefkinds"], "canGive:", rec["can_give_before_meet"])
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
        pg.screenshot(path=f"{SHOTS}/t1_agency.png")
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

        # ---------- T2：UI 送名筆（liked） ----------
        rec = {"test": "T2_ui_gift_pen", "pageerrors": 0}
        g = gift_via_ui(pg, "gift_fountain_pen", "t2_gift_pen")
        rec.update(g)
        st = state_probe(pg)
        rec["rel_tang_after"] = st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")
        rec["pen_left"] = (st.get("inv") or {}).get("gift_fountain_pen")
        rec["has_pen_line"] = "名筆。簽名、批檔期、改數字，都用得著。" in (g.get("result_text") or "")  # live 經 TEXTFIX55：着→著
        rec["has_rel_unchanged"] = "排片關係不變" in (g.get("result_text") or "")
        rec["pick_subtitle_ok"] = "唔會改變排片關係" in (g.get("pick_text") or "")
        rec["pick_tag_liked"] = "喜" in (g.get("pick_text") or "")
        rec["forbidden"] = [w for w in FORBIDDEN if w in (g.get("result_text") or "")]
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(g.get("clicked_gift_btn") and g.get("clicked_item") and g.get("clicked_send")
                           and rec["has_pen_line"] and rec["has_rel_unchanged"] and rec["pick_subtitle_ok"]
                           and rec["rel_tang_after"] == 1 and rec["pen_left"] == 1 and not rec["forbidden"]
                           and g.get("sheet_back"))
        results.append(rec)
        print("T2", rec["pass"], "pen_line:", rec["has_pen_line"], "rel:", rec["rel_tang_after"], "left:", rec["pen_left"])
        pg.screenshot(path=f"{SHOTS}/t2_after.png")

        # ---------- T3：UI 送玫瑰（dislike） ----------
        pg.evaluate("() => { try { S.dayIndex = (S.dayIndex|0) + 1; if (S.giftMeta) { S.giftMeta.lastGiveDay = {}; S.giftMeta.weekGiftGain = {}; } } catch(e){} }")
        pg.wait_for_timeout(600)
        rec = {"test": "T3_ui_gift_rose", "pageerrors": 0}
        g = gift_via_ui(pg, "gift_rose_premium", "t3_gift_rose")
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
        print("T3", rec["pass"], "rose_line:", rec["has_rose_line"], "rel:", rec["rel_tang_after"])
        pg.screenshot(path=f"{SHOTS}/t3_after.png")

        # ---------- T4：UI 送咖啡豆（neutral） ----------
        pg.evaluate("() => { try { S.dayIndex = (S.dayIndex|0) + 1; if (S.giftMeta) { S.giftMeta.lastGiveDay = {}; S.giftMeta.weekGiftGain = {}; } } catch(e){} }")
        pg.wait_for_timeout(600)
        rec = {"test": "T4_ui_gift_coffee", "pageerrors": 0}
        g = gift_via_ui(pg, "gift_coffee_beans", "t4_gift_coffee")
        rec.update(g)
        st = state_probe(pg)
        rec["rel_tang_after"] = st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")
        rec["has_coffee_line"] = "咖啡豆" in (g.get("result_text") or "") and "夜更對帳用得著" in (g.get("result_text") or "")  # live 經 TEXTFIX55：着→著
        rec["has_rel_unchanged"] = "排片關係不變" in (g.get("result_text") or "")
        rec["forbidden"] = [w for w in FORBIDDEN if w in (g.get("result_text") or "")]
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(g.get("clicked_gift_btn") and g.get("clicked_item") and g.get("clicked_send")
                           and rec["has_coffee_line"] and rec["has_rel_unchanged"]
                           and rec["rel_tang_after"] == 1 and not rec["forbidden"] and g.get("sheet_back"))
        results.append(rec)
        print("T4", rec["pass"], "coffee_line:", rec["has_coffee_line"], "rel:", rec["rel_tang_after"])
        ctx.close()

        # ---------- T5：廟街禮品檔買名筆 ----------
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        rec = {"test": "T5_shop_buy_pen", "pageerrors": 0}
        rec["on_map"] = seed_entry(pg, "seed_deng_meet_ready")
        pg.evaluate("() => { try { S.money = 10000; S.inventory = {}; } catch(e){} }")
        pg.wait_for_timeout(800)
        # 種子會自動播 meet 劇情：正規播完佢（揀 data 抉擇），再去禮品檔（買貨唔使見過面，但要返到地圖）
        if wait_story_modal(pg, secs=15):
            play_story(pg, "遞上")
        dismiss_story_end(pg)
        rec["shop_open"] = open_loc(pg, "gift_shop")
        rec["buy_btn_present"] = False
        if rec["shop_open"]:
            rec["buy_btn_present"] = click_vis_btn(pg, "買禮物")
            pg.wait_for_timeout(1000)
            rec["shop_text"] = modal_text(pg)
            rec["pen_row"] = pg.evaluate("""() => {
              const b = document.querySelector('[data-buy="gift_fountain_pen"]');
              return b ? b.innerText : ''; }""")
            before = state_probe(pg)
            rec["money_before"] = before.get("money")
            rec["clicked_buy"] = pg.evaluate("""() => {
              const b = document.querySelector('[data-buy="gift_fountain_pen"]');
              if (!b || b.disabled) return false; b.click(); return true; }""")
            pg.wait_for_timeout(1000)
            after = state_probe(pg)
            rec["money_after"] = after.get("money")
            rec["pen_inv"] = (after.get("inv") or {}).get("gift_fountain_pen")
        pg.screenshot(path=f"{SHOTS}/t5_shop.png")
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"] and rec.get("shop_open") and rec.get("buy_btn_present")
                           and rec.get("clicked_buy") and rec.get("pen_inv") == 1
                           and rec.get("money_before") is not None
                           and rec.get("money_after") == rec["money_before"] - 550
                           and "名筆" in (rec.get("pen_row") or ""))
        results.append(rec)
        print("T5", rec["pass"], "pen_inv:", rec.get("pen_inv"), "money:", rec.get("money_before"), "->", rec.get("money_after"))
        ctx.close()

        # ---------- T6：排片線照行（push2 掣＋送禮掣並存，唔撳錯） ----------
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        rec = {"test": "T6_push_line_intact", "pageerrors": 0}
        rec["on_map"] = seed_entry(pg, "seed_deng_push_ready")
        rec["story_modal"] = wait_story_modal(pg)
        if rec["story_modal"]:
            play = play_story(pg, "情報")
            rec["push1_picked"] = play["picked"]
        pg.wait_for_timeout(1200)
        dismiss_story_end(pg)
        rec["agency_open"] = open_loc(pg, "agency_ho")
        if rec["agency_open"]:
            btns = sheet_buttons(pg)
            rec["agency_buttons"] = btns
            rec["push2_present"] = any("午夜場後的試探" in t for t in btns)
            rec["gift_button_present"] = any("送禮：鄧麗萍" in t for t in btns)
            if rec["push2_present"]:
                rec["clicked_push2"] = click_vis_btn(pg, "午夜場後的試探")
                pg.wait_for_timeout(800)
                play = play_story(pg, "齋講檔期")
                rec["push2_picked"] = play["picked"]
                rec["push2_text"] = "\n---\n".join(play["texts"])
        pg.wait_for_timeout(1200)
        st = state_probe(pg)
        rec["done"] = {"push1": None, "push2": None}
        try:
            rec["done"] = pg.evaluate("""() => { try { return {
              push1: StoryOC.isDone('R_tang_push1'), push2: StoryOC.isDone('R_tang_push2') }; }
              catch(e){ return {}; } }""")
        except Exception:
            pass
        pg.screenshot(path=f"{SHOTS}/t6_push2.png")
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"] and rec["story_modal"] and rec.get("push1_picked")
                           and rec.get("agency_open") and rec.get("push2_present") and rec.get("gift_button_present")
                           and rec.get("clicked_push2") and rec.get("push2_picked")
                           and rec["done"].get("push2") is True)
        results.append(rec)
        print("T6", rec["pass"], "push2:", rec.get("push2_picked"), "done:", rec["done"])
        ctx.close()
        b.close()
finally:
    srv.terminate()
with open(os.path.join(ROOT, "qa164", "drive164.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
n_pass = sum(1 for r in results if r.get("pass") and r.get("pageerrors") == 0)
print(f"OVERALL {n_pass}/{len(results)}")
