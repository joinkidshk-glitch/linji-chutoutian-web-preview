#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v20a169 實駕（只驗證，唔改 game code）。對象：工作副本 linji-work169（分支 v20a169，基底 main 5e6a6b0），port 8169，?softPreview=1。
重點（v164 review B1／B2／C1／C2）：
 - B1：送禮掣費用欄三態——有庫存可送→「免費」（UI105 既有映射）、庫存空→「庫存空」、今日已送→「今日已送」。
 - B2：兩個 push 並存（seed_deng_push_ready → 播 push1「情報」→ 返事務所）：settle 2.5s 後量度幾何——兩卡唔重疊、badge 喺卡內橫排一行、卡高隨內容增長。
 - C1：送名筆結果 modal 見新句「…靠感情、靠人情辦事的人。」、唔見「感人情書」。
 - C2：廟街禮品檔頭 4 位＝名筆／計數機／腕表／玫瑰（置頂），買名筆照行。
完整 Chromium 擷圖（headless_shell 喺靜態 DOM 畫面出殘影，見 v164 NOTES §7 尾）；證據以 DOM 層為主，截圖只作目視輔助（md5 相異先當新鮮幀）。
用法：/home/hatch/pwenv49/bin/python qa169/drive169.py [all|b1|b2|shop]
"""
import glob, hashlib, json, os, subprocess, sys, time
from playwright.sync_api import sync_playwright

HERE = "/home/hatch/workspace/linji-work169/qa169"
ROOT = "/home/hatch/workspace/linji-work169"
SHOTS = os.path.join(HERE, "shots169")
PORT = 8179  # v20a169：唔 reuse 已有 server——上一輪誤 reuse 咗人哋嘅 8169 server（serve 緊 pristine，全部斷言假 FAIL，中途仲斷線）；每次起自己嘅，起完即驗 marker
os.makedirs(SHOTS, exist_ok=True)

def find_exe():
    cands = sorted(glob.glob("/home/hatch/.cache/ms-playwright/chromium-*/chrome-linux64/chrome"))
    cands += sorted(glob.glob("/home/hatch/pw-browsers/chromium-*/chrome-linux/chrome"))
    if cands:
        return cands[-1], "full"
    return "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell", "headless_shell"

EXE, EXE_KIND = find_exe()

def shot(pg, name):
    p = os.path.join(SHOTS, name)
    for _ in range(3):
        try:
            pg.screenshot(path=p)
            return p
        except Exception:
            time.sleep(0.5)
    return None

def shot_md5(p):
    try:
        return hashlib.md5(open(p, "rb").read()).hexdigest()[:12]
    except Exception:
        return None

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
    return pg.evaluate("() => { const m = document.querySelector('#modal'); return m ? m.innerText : ''; }")

def sheet_on(pg):
    return pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }")

def sheet_buttons(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet button, #loc-acts button')]
      .map(b => (b.textContent||'').trim()).filter(Boolean)""")

def overflow_probe(pg):
    return pg.evaluate("""() => ({
      docScrollW: document.documentElement.scrollWidth, innerW: window.innerWidth,
      hOverflow: document.documentElement.scrollWidth > window.innerWidth + 1 })""")

def seed_entry(pg, seed, secs=45):
    for _try in range(2):
        try:
            pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1&softBehaviorGate=1&softSeed={seed}")
            break
        except Exception:
            if _try == 1:
                raise
            pg.wait_for_timeout(1500)
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
        if vis_btn(pg, "下一句"):
            return True
        if i == 8:
            pg.evaluate("() => { try { if (window.__softSeed) window.__softSeed.apply(); } catch(e){} }")
        pg.wait_for_timeout(700)
    return False

def play_story(pg, choice_substr, secs=90):
    texts = []
    picked = False
    for _ in range(int(secs / 0.7)):
        t = modal_text(pg)
        if t and t not in texts:
            texts.append(t)
        if not picked and choice_substr and click_vis_btn(pg, choice_substr):
            picked = True; pg.wait_for_timeout(800); continue
        if click_vis_btn(pg, "下一句"):
            pg.wait_for_timeout(700); continue
        if vis_btn(pg, "返回地圖") or vis_btn(pg, "過一日"):
            break
        pg.wait_for_timeout(700)
    return {"texts": texts, "picked": picked, "ended_on_map": vis_btn(pg, "過一日")}

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
        if sheet_on(pg):
            return ok or True
    return False

def state_probe(pg):
    return pg.evaluate("""() => {
      const out = {};
      try { out.relTang = (typeof S !== 'undefined' && S.story && S.story.rel && S.story.rel.rel_tang); } catch(e){}
      try { out.relTang2 = (typeof S !== 'undefined' && S.rel && S.rel.rel_tang); } catch(e){}
      try { out.flagOpen = (typeof StoryOC !== 'undefined' && StoryOC.getFlag) ? StoryOC.getFlag('flag_tang_open') : null; } catch(e){ out.flagOpen = null; }
      try { out.money = (typeof S !== 'undefined') ? S.money : null; } catch(e){}
      try { out.inv = (typeof S !== 'undefined') ? (S.inventory || {}) : {}; } catch(e){}
      return out;
    }""")

def gift_btn_probe(pg):
    """B1：讀「送禮：鄧麗萍」掣嘅費用欄（.cost）＋描述行（.h）＋全文＋幾何。"""
    return pg.evaluate("""() => {
      const bs = [...document.querySelectorAll('#loc-sheet button, #loc-acts button')];
      const g = bs.find(b => (b.textContent||'').includes('送禮：鄧麗萍'));
      if (!g) return null;
      const r = g.getBoundingClientRect();
      const cost = (g.querySelector('.cost')||{}).textContent || '';
      const hint = (g.querySelector('.act-txt118 .h')||{}).textContent || '';
      return {cost: cost.trim(), hint: hint.trim(), text: (g.textContent||'').trim(),
              x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height)};
    }""")

def push_geom_probe(pg):
    """B2：settle 後量度兩張 push 卡＋各自 .ux68-why badge 嘅幾何（live DOM）。"""
    return pg.evaluate("""() => {
      const bs = [...document.querySelectorAll('#loc-acts .act')];
      const pick = (t) => bs.find(b => (b.textContent||'').includes(t));
      const c1 = pick('午夜場後的試探'), c2 = pick('黃金檔期之爭');
      if (!c1 || !c2) return {found: false, n: bs.length,
        titles: bs.map(b => (b.textContent||'').trim().slice(0, 10))};
      const rect = (el) => { const r = el.getBoundingClientRect();
        return {x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width),
                h: Math.round(r.height), bottom: Math.round(r.bottom), right: Math.round(r.right)}; };
      const card = (el) => {
        const why = el.querySelector('.ux68-why');
        return {rect: rect(el), why: why ? Object.assign(rect(why), {text: (why.textContent||'').trim(),
          inTxt118: !!why.closest('.act-txt118')}) : null,
          cls: el.className, title: (el.querySelector('.n')||{}).textContent || ''};
      };
      const a = card(c1), b = card(c2);
      const overlap = !(a.rect.bottom <= b.rect.y || b.rect.bottom <= a.rect.y);
      // 全版檢查：#loc-acts 內所有可見掣（零尺寸嘅摺疊鎖定掣除外）順序唔重疊
      const vis = bs.filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; })
        .map(el => { const r = el.getBoundingClientRect(); return {y: r.top, bottom: r.bottom}; });
      let allNoOverlap = true;
      for (let i = 1; i < vis.length; i++) { if (vis[i].y < vis[i-1].bottom - 0.5) { allNoOverlap = false; break; } }
      const whyInside = (c) => c.why && c.why.y >= c.rect.y - 1 && c.why.bottom <= c.rect.bottom + 1
        && c.why.x >= c.rect.x - 1 && c.why.right <= c.rect.right + 1;
      return {found: true, card1: a, card2: b, overlap,
        gap: b.rect.y - a.rect.bottom,
        checks: {tallEnough: a.rect.h >= 70 && b.rect.h >= 70,
          whyInside1: !!whyInside(a), whyInside2: !!whyInside(b),
          whyHorizontal1: !!a.why && a.why.h <= 30 && a.why.w >= 100,
          whyHorizontal2: !!b.why && b.why.h <= 30 && b.why.w >= 100,
          whyInTxt118: !!(a.why && a.why.inTxt118) && !!(b.why && b.why.inTxt118),
          whyText: (a.why && a.why.text === '有劇情等你觸發') && (b.why && b.why.text === '有劇情等你觸發'),
          noOverlap: !overlap, gapOk: (b.rect.y - a.rect.bottom) >= 5, allButtonsNoOverlap: allNoOverlap}};
    }""")

def gift_via_ui(pg, item_id, shot_base):
    out = {}
    out["gift_btn_hittest"] = pg.evaluate("""() => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes('送禮：鄧麗萍'));
      for (const b of bs) {
        const r = b.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0) continue;
        const el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        if (el === b || b.contains(el)) return true;
      }
      return false; }""")
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
    p = shot(pg, f"{shot_base}_result.png"); out["result_shot_md5"] = shot_md5(p)
    click_vis_btn(pg, "關閉")
    pg.wait_for_timeout(1000)
    out["sheet_back"] = sheet_on(pg)
    return out

def overlay_visible(pg):
    return pg.evaluate("""() => {
      const ov = document.getElementById('enc79-overlay');
      if (!ov) return false;
      const cs = getComputedStyle(ov);
      return cs.display !== 'none' && cs.visibility !== 'hidden' && ov.getBoundingClientRect().width > 0;
    }""")

def clear_encounter_overlay(pg, secs=40):
    clicks = []
    for _ in range(int(secs / 0.7)):
        if not overlay_visible(pg):
            return True, clicks
        hit = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return '';
          const btns = [...ov.querySelectorAll('button')].filter(b => {
            const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
            return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
          const pref = btns.find(b => (b.textContent||'').includes('行開算'))
            || btns.find(b => (b.textContent||'').includes('下一句'))
            || btns.find(b => (b.textContent||'').includes('離開'))
            || btns.find(b => (b.textContent||'').includes('關閉'))
            || btns[0];
          if (!pref) return '';
          pref.click(); return (pref.textContent||'').trim().slice(0, 16);
        }""")
        if hit:
            clicks.append(hit)
        pg.wait_for_timeout(700)
    return (not overlay_visible(pg)), clicks

def modal_visible(pg):
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      if (!m) return false;
      const cs = getComputedStyle(m);
      return cs.display !== 'none' && cs.visibility !== 'hidden' && m.getBoundingClientRect().width > 0;
    }""")

def mask_on(pg):
    return pg.evaluate("""() => {
      const m = document.getElementById('mask');
      return !!m && m.classList.contains('on');
    }""")

def back_to_map(pg, secs=60):
    log = []
    for _ in range(int(secs / 0.7)):
        if overlay_visible(pg):
            ok, clicks = clear_encounter_overlay(pg, secs=10)
            log.append(f"enc:{clicks}")
            pg.wait_for_timeout(500)
            continue
        if modal_visible(pg):
            hit = pg.evaluate("""() => {
              const btns = [...document.querySelectorAll('#modal-btns button')].filter(b => {
                const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
                return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
              const pref = btns.find(b => /關閉|返回地圖|回家結算/.test(b.textContent||''))
                || btns.find(b => /下一句/.test(b.textContent||'')) || btns[0];
              if (!pref) return '';
              pref.click(); return (pref.textContent||'').trim().slice(0, 12);
            }""")
            log.append(f"modal:{hit}")
            pg.wait_for_timeout(700)
            continue
        if mask_on(pg):
            pg.evaluate("() => { try { if (typeof closeModal === 'function') closeModal(); } catch(e){} }")
            log.append("mask:closeModal")
            pg.wait_for_timeout(500)
            continue
        log.append("clean")
        return True, log
        pg.wait_for_timeout(700)
    return False, log

def shop_rows_probe(pg):
    for _ in range(6):
        done = pg.evaluate("""() => {
          const imgs = [...document.querySelectorAll('[data-buy] img.ic112')];
          return imgs.length === 0 || imgs.every(i => i.complete); }""")
        if done:
            break
        pg.wait_for_timeout(500)
    return pg.evaluate("""() => {
      const btns = [...document.querySelectorAll('[data-buy]')];
      return btns.map(b => {
        const img = b.querySelector('img.ic112');
        return {id: b.getAttribute('data-buy'), text: (b.innerText||'').replace(/\\n/g,' | ').slice(0,80),
                imgOk: img ? (img.complete && img.naturalWidth > 0) : null,
                disabled: !!b.disabled};
      });
    }""")

def new_context(pw, height):
    ctx = pw.chromium.launch(executable_path=EXE, headless=False, args=["--no-sandbox"]).new_context(viewport={"width": 430, "height": height})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    return ctx, pg, errs

def meet_and_back(pg):
    """seed meet → 播 meet（揀 data 抉擇）→ 返地圖。回傳 checks dict。"""
    out = {}
    out["on_map"] = seed_entry(pg, "seed_deng_meet_ready")
    out["story_modal"] = wait_story_modal(pg)
    play = play_story(pg, "遞上")
    out["picked_data"] = play["picked"]
    out["back_to_map"], _back_log = back_to_map(pg)
    st = state_probe(pg)
    out["flag_open"] = bool(st.get("flagOpen"))
    out["rel_tang_1"] = (st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")) == 1
    return out

def run_b1(pw):
    out = {"case": "b1_states", "errors": [], "checks": {}}
    errs = []
    # --- OK 態 → 送筆 → SENT 態（同一 context，932） ---
    ctx, pg, errs = new_context(pw, 932)
    pg.on("response", lambda r: out["errors"].append(f"http{r.status}: {r.url}") if r.status >= 400 else None)
    try:
        out["checks"].update(meet_and_back(pg))
        pg.evaluate("""() => { try {
          S.inventory = S.inventory || {};
          ['gift_fountain_pen','gift_desk_calculator','gift_dress_watch','gift_coffee_beans','gift_rose_premium','gift_memo_pad']
            .forEach(id => { S.inventory[id] = 2; });
          S.money = 10000;
        } catch(e){} }""")
        out["checks"]["agency_open"] = bool(open_loc(pg, "agency_ho"))
        pg.wait_for_timeout(2500)
        ok_probe = gift_btn_probe(pg)
        out["ok_probe"] = ok_probe
        out["checks"]["ok_cost_free"] = ok_probe and ok_probe["cost"] == "免費"
        out["checks"]["ok_hint_no_day"] = ok_probe and "不耗日" in ok_probe["hint"]
        p = shot(pg, "b1_ok_932.png"); out["ok_shot_md5"] = shot_md5(p)
        g = gift_via_ui(pg, "gift_fountain_pen", "b1_pen")
        out["pen"] = g
        out["checks"]["pen_line1"] = "名筆。簽名、批檔期、改數字，都用得著。" in (g.get("result_text") or "")
        out["checks"]["pen_line2_new"] = "靠感情、靠人情辦事的人" in (g.get("result_text") or "")
        out["checks"]["pen_typo_gone"] = "感人情書" not in (g.get("result_text") or "")
        out["checks"]["pen_rel_unchanged"] = "排片關係不變" in (g.get("result_text") or "")
        st = state_probe(pg)
        out["checks"]["pen_rel_still_1"] = (st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")) == 1
        out["checks"]["pen_left_1"] = (st.get("inv") or {}).get("gift_fountain_pen") == 1
        out["checks"]["sheet_back"] = bool(g.get("sheet_back"))
        sent_probe = gift_btn_probe(pg)
        out["sent_probe"] = sent_probe
        out["checks"]["sent_cost_today"] = sent_probe and sent_probe["cost"] == "今日已送"
        p = shot(pg, "b1_sent_932.png"); out["sent_shot_md5"] = shot_md5(p)
        out["pass_ok_sent"] = all(v is True for k, v in out["checks"].items() if k in (
            "on_map", "story_modal", "picked_data", "back_to_map", "flag_open", "rel_tang_1",
            "agency_open", "ok_cost_free", "ok_hint_no_day", "pen_line1", "pen_line2_new",
            "pen_typo_gone", "pen_rel_unchanged", "pen_rel_still_1", "pen_left_1", "sheet_back",
            "sent_cost_today"))
    except Exception as e:
        out["pass_ok_sent"] = False
        out["error"] = repr(e)
    finally:
        out["pageerrors_ok_sent"] = errs
        try: ctx.close()
        except Exception: pass
    # --- EMPTY 態（新 context，932） ---
    errs2 = []
    ctx2, pg2, errs2 = new_context(pw, 932)
    pg2.on("response", lambda r: out["errors"].append(f"http{r.status}: {r.url}") if r.status >= 400 else None)
    try:
        out["checks"].update({("empty_" + k): v for k, v in meet_and_back(pg2).items()})
        pg2.evaluate("() => { try { S.inventory = {}; S.money = 10000; } catch(e){} }")
        out["checks"]["empty_agency_open"] = bool(open_loc(pg2, "agency_ho"))
        pg2.wait_for_timeout(2500)
        empty_probe = gift_btn_probe(pg2)
        out["empty_probe"] = empty_probe
        out["checks"]["empty_cost_stock"] = empty_probe and empty_probe["cost"] == "庫存空"
        out["checks"]["empty_hint"] = empty_probe and "庫存空空" in empty_probe["hint"]
        out["checks"]["empty_cost_not_free"] = empty_probe and empty_probe["cost"] != "免費"
        p = shot(pg2, "b1_empty_932.png"); out["empty_shot_md5"] = shot_md5(p)
        out["pass_empty"] = all(v is True for k, v in out["checks"].items() if k.startswith("empty_") or k in (
            "empty_cost_stock", "empty_hint", "empty_cost_not_free"))
    except Exception as e:
        out["pass_empty"] = False
        out["error_empty"] = repr(e)
    finally:
        out["pageerrors_empty"] = errs2
        try: ctx2.close()
        except Exception: pass
    out["pass"] = bool(out.get("pass_ok_sent")) and bool(out.get("pass_empty")) \
        and not out.get("pageerrors_ok_sent") and not out.get("pageerrors_empty")
    out["checks"]["zero_pageerror"] = not out.get("pageerrors_ok_sent") and not out.get("pageerrors_empty")
    return out

def run_b2(pw, height):
    tag = f"b2_push_{height}"
    out = {"case": tag, "height": height, "errors": [], "checks": {}}
    ctx, pg, errs = new_context(pw, height)
    pg.on("response", lambda r: out["errors"].append(f"http{r.status}: {r.url}") if r.status >= 400 else None)
    try:
        out["checks"]["on_map"] = seed_entry(pg, "seed_deng_push_ready")
        out["checks"]["story_modal"] = wait_story_modal(pg)
        play = play_story(pg, "情報")
        out["checks"]["push1_picked"] = play["picked"]
        out["back_to_map"], out["back_log"] = back_to_map(pg)
        out["checks"]["back_to_map"] = bool(out["back_to_map"])
        out["checks"]["agency_open"] = bool(open_loc(pg, "agency_ho"))
        # settle：等 sheet 滑入動畫停（review 要求重驗嗰陣喺返得嘅環境跑呢個探針）
        pg.wait_for_timeout(2500)
        geom1 = push_geom_probe(pg)
        out["geom_settle"] = geom1
        pg.wait_for_timeout(1000)
        geom2 = push_geom_probe(pg)
        out["geom_settle_plus1s"] = geom2
        out["checks"]["two_cards"] = bool(geom1.get("found")) and bool(geom2.get("found"))
        if geom1.get("found"):
            for k, v in (geom1.get("checks") or {}).items():
                out["checks"]["settle_" + k] = bool(v)
            out["checks"]["stable_geom"] = geom1.get("card1") == geom2.get("card1") and geom1.get("card2") == geom2.get("card2")
        # 順手：呢個 state 庫存空，送禮掣費用欄應為「庫存空」（B1 附帶）
        gp = gift_btn_probe(pg)
        out["gift_probe_push_state"] = gp
        out["checks"]["push_state_gift_cost_stock"] = gp and gp["cost"] == "庫存空"
        p = shot(pg, f"{tag}_agency.png"); out["agency_shot_md5"] = shot_md5(p)
        out["pass"] = all(v is True for v in out["checks"].values())
    except Exception as e:
        out["pass"] = False
        out["error"] = repr(e)
    finally:
        out["pageerrors"] = errs
        out["checks"]["zero_pageerror"] = len(errs) == 0
        out["pass"] = out.get("pass", False) and len(errs) == 0
        try: ctx.close()
        except Exception: pass
    return out

def run_shop(pw):
    out = {"case": "shop_top", "errors": [], "checks": {}}
    ctx, pg, errs = new_context(pw, 932)
    pg.on("response", lambda r: out["errors"].append(f"http{r.status}: {r.url}") if r.status >= 400 else None)
    try:
        out["checks"].update(meet_and_back(pg))
        pg.evaluate("() => { try { S.money = 10000; S.inventory = {}; } catch(e){} }")
        out["checks"]["shop_open"] = bool(open_loc(pg, "gift_shop"))
        out["checks"]["buy_btn"] = click_vis_btn(pg, "買禮物")
        pg.wait_for_timeout(1000)
        out["shop_text"] = modal_text(pg)
        rows = shop_rows_probe(pg)
        out["shop_rows"] = rows
        ids = [r["id"] for r in rows]
        new4 = ["gift_fountain_pen", "gift_desk_calculator", "gift_dress_watch", "gift_rose_premium"]
        out["checks"]["rows_14"] = len(ids) == 14
        out["checks"]["new4_first4"] = ids[:4] == new4
        out["checks"]["fifth_is_mvp"] = len(ids) > 4 and ids[4] not in new4
        out["checks"]["new4_icons_ok"] = all((rows[i].get("imgOk") for i in range(4)))
        p = shot(pg, "shop_932.png"); out["shop_shot_md5"] = shot_md5(p)
        before = state_probe(pg)
        out["checks"]["clicked_buy_pen"] = pg.evaluate("""() => {
          const b = document.querySelector('[data-buy="gift_fountain_pen"]');
          if (!b || b.disabled) return false; b.click(); return true; }""")
        pg.wait_for_timeout(1000)
        after = state_probe(pg)
        out["checks"]["pen_bought"] = (after.get("inv") or {}).get("gift_fountain_pen") == 1
        out["checks"]["money_minus_550"] = after.get("money") == (before.get("money") or 0) - 550
        out["pass"] = all(v is True for v in out["checks"].values())
    except Exception as e:
        out["pass"] = False
        out["error"] = repr(e)
    finally:
        out["pageerrors"] = errs
        out["checks"]["zero_pageerror"] = len(errs) == 0
        out["pass"] = out.get("pass", False) and len(errs) == 0
        try: ctx.close()
        except Exception: pass
    return out

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("EXE:", EXE, "kind:", EXE_KIND)
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    # 驗明正身：呢個 server 必須 serve 緊工作副本（有 v169 marker），唔係就即停，唔好測錯 build
    import urllib.request
    served = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5).read().decode("utf-8")
    for marker in ("applyTangGift169", "flex-shrink:0", "今日已送"):
        assert marker in served, f"server on {PORT} is NOT work169 (missing {marker})"
    print(f"serving work169 on {PORT} (markers ok)")
    results = {}
    try:
        with sync_playwright() as pw:
            if which in ("all", "b1"):
                results["b1"] = run_b1(pw)
            if which in ("all", "b2"):
                results["b2_932"] = run_b2(pw, 932)
                results["b2_700"] = run_b2(pw, 700)
            if which in ("all", "shop"):
                results["shop"] = run_shop(pw)
        json.dump(results, open(os.path.join(HERE, "drive169.json"), "w"), ensure_ascii=False, indent=1)
        for name, r in results.items():
            print(f"{name}: {'PASS' if r.get('pass') else 'FAIL'}")
            for k, v in (r.get("checks") or {}).items():
                if v is not True:
                    print(f"   check FAIL: {k} = {v!r}")
            if r.get("error"):
                print("   ERROR:", r["error"])
            if r.get("pageerrors"):
                print("   pageerrors:", r["pageerrors"][:3])
        ok = all(r.get("pass") for r in results.values())
        print("OVERALL", "PASS" if ok else "FAIL", "| EXE kind:", EXE_KIND)
        return 0 if ok else 1
    finally:
        if srv:
            srv.terminate()

if __name__ == "__main__":
    sys.exit(main())
