#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v20a173 實駕（只驗證，唔改 game code）。對象：工作副本 linji-work173（分支 v20a173，基底 e8c3a73／v170），port 8183，?softPreview=1。
重點（v171 review C1／C2＋B1／B2 守門）：
 - B1：送禮掣費用欄三態——有庫存可送→「免費」（UI105 既有映射）、庫存空→「庫存空」、今日已送→「今日已送」。
 - B2：兩個 push 並存（seed_deng_push_ready → 播 push1「情報」→ 返事務所）：settle 2.5s 後量度幾何——兩卡唔重疊、badge 喺卡內橫排一行、卡高隨內容增長。
 - C1：送名筆結果 modal 見新句「…靠感情、靠人情辦事的人。」、唔見「感人情書」。
 - C2：廟街禮品檔頭 4 位＝名筆／計數機／腕表／玫瑰（置頂），買名筆照行。
完整 Chromium 擷圖（headless_shell 喺靜態 DOM 畫面出殘影，見 v164 NOTES §7 尾）；證據以 DOM 層為主，截圖只作目視輔助（md5 相異先當新鮮幀）。
用法：/home/hatch/pwenv49/bin/python qa173/drive173.py [all|c1|c2]
"""
import glob, hashlib, json, os, subprocess, sys, time
from playwright.sync_api import sync_playwright

HERE = "/home/hatch/workspace/linji-work173/qa173"
ROOT = "/home/hatch/workspace/linji-work173"
SHOTS = os.path.join(HERE, "shots173")
PORT = 8183  # v20a173：唔 reuse 已有 server——每次起自己嘅，起完即驗 marker
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

def fade_probe(pg):
    """C1：#loc-acts 捲動狀態＋淡出漸變 ::after 計算樣式＋逐掣 fade 區交集。
    v173 新增 rows：每粒可見掣同 30px 淡出區嘅交集（zoneOverlap）、掣喺 acts 可視區
    嘅可見比例（visFrac）、掣底有幾多 px 喺實色線之下（belowSolid——60% stop 嗰陣
    實色線喺淡出區 18px 處，即 actsBottom-12；78% 舊版實色線喺 actsBottom-6.6，
    932「還人情」底 851 到唔到實色線，成個掣只係半透明漸變）。"""
    return pg.evaluate("""() => {
      const acts = document.getElementById('loc-acts');
      if (!acts) return null;
      const cs = getComputedStyle(acts, '::after');
      const r = acts.getBoundingClientRect();
      const btns = [...acts.querySelectorAll('.act')].filter(b => { const q = b.getBoundingClientRect(); return q.width > 0 && q.height > 0; });
      const last = btns[btns.length - 1];
      const lr = last ? last.getBoundingClientRect() : null;
      const fadeTop = r.bottom - 30, solidY = r.bottom - 12;  // 30px 淡出區；60% stop → 實色由 18px 處起
      const rows = btns.map(b => {
        const q = b.getBoundingClientRect();
        const visTop = Math.max(q.top, r.top), visBot = Math.min(q.bottom, r.bottom);
        const visH = Math.max(0, visBot - visTop);
        const zoneOverlap = Math.max(0, Math.min(q.bottom, r.bottom) - Math.max(q.top, fadeTop));
        const belowSolid = Math.max(0, Math.min(q.bottom, r.bottom) - Math.max(q.top, solidY));
        return {title: ((b.querySelector('.n') || {}).textContent || '').trim(),
          top: Math.round(q.top), bottom: Math.round(q.bottom),
          visFrac: +(visH / q.height).toFixed(2),
          zoneOverlap: Math.round(zoneOverlap), belowSolid: Math.round(belowSolid)};
      });
      const mid = document.elementFromPoint(r.left + r.width / 2, r.bottom - 15);
      return {scrollH: acts.scrollHeight, clientH: acts.clientHeight, scrollTop: acts.scrollTop,
        hasMore: acts.classList.contains('loc-acts-more171'),
        afterContent: cs.content, afterPos: cs.position, afterH: cs.height,
        afterBg: (cs.backgroundImage || '').slice(0, 160), afterPE: cs.pointerEvents,
        actsTop: Math.round(r.top), actsBottom: Math.round(r.bottom),
        fadeTop: Math.round(fadeTop), solidY: Math.round(solidY),
        rows: rows, fadeHit: mid ? (mid.closest('.act') ? ((mid.closest('.act').querySelector('.n') || {}).textContent || '').trim() : mid.tagName) : null,
        nBtns: btns.length,
        lastTitle: last ? ((last.querySelector('.n') || {}).textContent || '') : '',
        lastTop: lr ? Math.round(lr.top) : null, lastBottom: lr ? Math.round(lr.bottom) : null,
        lastFullyVisible: lr ? (lr.bottom <= r.bottom + 1 && lr.top >= r.top - 1) : false};
    }""")

def acts_scroll_to(pg, y):
    pg.evaluate("""(y) => { const a = document.getElementById('loc-acts');
      if (a) a.scrollTop = y; }""", y)
    pg.wait_for_timeout(600)

def gift_visual_probe(pg):
    """C2：送禮掣鎖住態視覺區分（class／掣底／費用欄色／標題淡／hint 淡／disabled）。
    v173 新增：hint .h live computed opacity＋color＋混合後對比度（hint 色 #3a2e22，
    priority 掣由 L2040 定；0.72 混合後 #6a6052 on #e6dfcc = 4.63:1）。"""
    return pg.evaluate("""() => {
      const bs = [...document.querySelectorAll('#loc-sheet button, #loc-acts button')];
      const g = bs.find(b => (b.textContent||'').includes('送禮：鄧麗萍'));
      if (!g) return null;
      const cs = getComputedStyle(g);
      const cost = g.querySelector('.cost');
      const n = g.querySelector('.n');
      const h = g.querySelector('.h');
      const ccs = cost ? getComputedStyle(cost) : null;
      const ncs = n ? getComputedStyle(n) : null;
      const hcs = h ? getComputedStyle(h) : null;
      const lum = (rgb) => { const m = rgb.match(/\d+(\.\d+)?/g).map(Number);
        const f = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
        return 0.2126 * f(m[0]) + 0.7152 * f(m[1]) + 0.0722 * f(m[2]); };
      const cr = (a, b) => { const x = lum(a), y = lum(b); const hi = Math.max(x, y), lo = Math.min(x, y); return +((hi + 0.05) / (lo + 0.05)).toFixed(2); };
      let hintCR = null, hintBlend = null;
      if (hcs && cs) {
        const fg = hcs.color.match(/\d+(\.\d+)?/g).map(Number);
        const bg = cs.backgroundColor.match(/\d+(\.\d+)?/g).map(Number);
        const op = parseFloat(hcs.opacity);
        const bl = fg.map((v, i) => Math.round(op * v + (1 - op) * bg[i]));
        hintBlend = 'rgb(' + bl.join(', ') + ')';
        hintCR = cr(hintBlend, cs.backgroundColor);
      }
      return {lockedCls: g.classList.contains('act-locked171'),
        cls: g.className, cost: (cost ? cost.textContent : '').trim(),
        btnBg: cs.backgroundColor, btnOpacity: cs.opacity,
        costColor: ccs ? ccs.color : '', costWeight: ccs ? ccs.fontWeight : '',
        nOpacity: ncs ? ncs.opacity : '', nColor: ncs ? ncs.color : '',
        hOpacity: hcs ? hcs.opacity : '', hColor: hcs ? hcs.color : '',
        hText: h ? (h.textContent || '').trim() : '', hintCR: hintCR, hintBlend: hintBlend,
        disabled: !!g.disabled, ariaDisabled: g.getAttribute('aria-disabled')};
    }""")

def toast_probe(pg):
    return pg.evaluate("""() => { const t = document.getElementById('toast');
      if (!t) return null;
      const cs = getComputedStyle(t);
      return {text: (t.innerText || t.textContent || '').trim(),
        visible: cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0.5,
        ariaHidden: t.getAttribute('aria-hidden')}; }""")

def click_locked_gift(pg):
    ok = click_vis_btn(pg, "送禮：鄧麗萍")
    pg.wait_for_timeout(900)
    return ok, toast_probe(pg)

def run_c1(pw, height):
    tag = f"c1_fade_{height}"
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
        pg.wait_for_timeout(2500)
        top = fade_probe(pg)
        out["fade_top"] = top
        out["checks"]["scrollable"] = top and top["scrollH"] > top["clientH"] + 4
        out["checks"]["has_more_at_top"] = top and top["hasMore"] is True
        out["checks"]["after_is_sticky_30px"] = top and top["afterPos"] == "sticky" and top["afterH"] == "30px"
        out["checks"]["after_is_gradient"] = top and "linear-gradient" in (top["afterBg"] or "")
        out["checks"]["after_click_through"] = top and top["afterPE"] == "none"
        out["checks"]["last_btn_is_talk_ho"] = top and "同何生傾談" in (top["lastTitle"] or "")
        out["checks"]["last_btn_below_fold_at_top"] = top and top["lastBottom"] > top["actsBottom"]
        out["checks"]["nine_buttons"] = top and top["nBtns"] == 8  # #loc-acts 內 8 粒＋footer「返回地圖」＝review 講嘅 9 個掣
        out["checks"]["scrollH_814"] = top and top["scrollH"] == 814  # 更正數字：唔係 v171 NOTES 嘅 821
        out["checks"]["after_stop_60pct"] = top and "60%" in (top["afterBg"] or "")
        row = lambda t: next((x for x in (top.get("rows") or []) if t in x["title"]), None)
        if height == 932:
            rh = row("還人情")
            out["fade_row_repay"] = rh
            out["checks"]["c1_932_repay_in_fade"] = rh and rh["zoneOverlap"] >= 20  # review：底 22px
            out["checks"]["c1_932_repay_below_solid"] = rh and rh["belowSolid"] > 0  # 掣底過咗 60% 實色線，完全溶入底色
            out["checks"]["c1_932_listen_1px"] = (lambda x: x is None or x["zoneOverlap"] <= 2)(row("聽風聲"))
        else:
            rs = row("送禮")
            out["fade_row_gift"] = rs
            out["checks"]["c1_700_gift_cut"] = rs and rs["zoneOverlap"] >= 29 and rs["visFrac"] < 1  # review：成 30px，visFrac 0.84
        out["checks"]["fade_click_through"] = top and top.get("fadeHit") and top["fadeHit"] not in ("DIV", "SECTION", "")
        p = shot(pg, f"{tag}_top.png"); out["top_shot_md5"] = shot_md5(p)
        # B2 守門：兩張 push 卡幾何不變（各 h115、gap 7、零重疊）
        geom = push_geom_probe(pg)
        out["geom"] = geom
        if geom.get("found"):
            for k, v in (geom.get("checks") or {}).items():
                out["checks"]["b2_" + k] = bool(v)
            out["checks"]["b2_cards_h115"] = geom["card1"]["rect"]["h"] == 115 and geom["card2"]["rect"]["h"] == 115
            out["checks"]["b2_gap7"] = geom["gap"] == 7
        # 捲到底：提示消失、最尾掣全見、scrollH 不變（::after 唔佔位）
        acts_scroll_to(pg, 100000)
        bot = fade_probe(pg)
        out["fade_bottom"] = bot
        out["checks"]["no_more_at_bottom"] = bot and bot["hasMore"] is False
        out["checks"]["last_btn_visible_at_bottom"] = bot and bot["lastFullyVisible"] is True
        out["checks"]["scrollH_stable"] = top and bot and top["scrollH"] == bot["scrollH"]
        p = shot(pg, f"{tag}_scrolled.png"); out["scrolled_shot_md5"] = shot_md5(p)
        # 捲返頂：提示返嚟
        acts_scroll_to(pg, 0)
        top2 = fade_probe(pg)
        out["fade_top2"] = top2
        out["checks"]["has_more_again_at_top"] = top2 and top2["hasMore"] is True
        # resize 兜底：切另一高度再量，sync 照跟住重計
        pg.set_viewport_size({"width": 430, "height": 700 if height == 932 else 932})
        pg.wait_for_timeout(800)
        rsz = fade_probe(pg)
        out["fade_resized"] = rsz
        out["checks"]["resize_has_more"] = rsz and rsz["hasMore"] is True
        out["checks"]["resize_scrollH_814"] = rsz and rsz["scrollH"] == 814
        pg.set_viewport_size({"width": 430, "height": height})
        pg.wait_for_timeout(600)
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

def run_c2(pw):
    out = {"case": "c2_locked_visual", "errors": [], "checks": {}}
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
        okv = gift_visual_probe(pg)
        out["ok_visual"] = okv
        out["checks"]["ok_cost_free"] = okv and okv["cost"] == "免費"
        out["checks"]["ok_not_locked"] = okv and okv["lockedCls"] is False
        out["checks"]["ok_cost_red"] = okv and okv["costColor"] == "rgb(196, 60, 42)"
        out["checks"]["ok_btn_bg_priority"] = okv and okv["btnBg"] == "rgb(245, 230, 192)"
        out["checks"]["ok_hint_opacity_1"] = okv and okv["hOpacity"] == "1"  # 可送態唔鎖，舊 rule opacity 1
        out["checks"]["ok_title_opacity_1"] = okv and okv["nOpacity"] == "1"
        p = shot(pg, "c2_ok_932.png"); out["ok_shot_md5"] = shot_md5(p)
        g = gift_via_ui(pg, "gift_fountain_pen", "c2_pen")
        out["pen"] = g
        out["checks"]["pen_sent_ok"] = "排片關係不變" in (g.get("result_text") or "")
        out["checks"]["sheet_back"] = bool(g.get("sheet_back"))
        sent = gift_visual_probe(pg)
        out["sent_visual"] = sent
        out["checks"]["sent_cost_today"] = sent and sent["cost"] == "今日已送"
        out["checks"]["sent_locked_cls"] = sent and sent["lockedCls"] is True
        out["checks"]["sent_cost_grey"] = sent and sent["costColor"] == "rgb(107, 86, 54)"
        out["checks"]["sent_btn_bg_grey"] = sent and sent["btnBg"] == "rgb(230, 223, 204)"
        out["checks"]["sent_title_dimmed"] = sent and float(sent["nOpacity"] or 1) < 0.8
        out["checks"]["sent_title_opacity_072"] = sent and sent["nOpacity"] == "0.72"
        out["checks"]["sent_hint_opacity_072"] = sent and sent["hOpacity"] == "0.72"  # v173 C2：live 斷言
        out["checks"]["sent_hint_readable"] = sent and sent["hintCR"] is not None and sent["hintCR"] >= 4.5
        out["checks"]["sent_hint_color_3a2e22"] = sent and sent["hColor"] == "rgb(58, 46, 34)"
        out["checks"]["sent_not_disabled"] = sent and sent["disabled"] is False
        p = shot(pg, "c2_sent_932.png"); out["sent_shot_md5"] = shot_md5(p)
        clicked, toast = click_locked_gift(pg)
        out["sent_toast"] = toast
        out["checks"]["sent_click_toasts"] = clicked is True and toast and toast["visible"] is True and len(toast["text"] or "") > 0
        out["checks"]["sent_click_no_gift_modal"] = modal_visible(pg) is False  # 鎖住態撳落去唔開揀禮物 modal
        out["pass_ok_sent"] = all(v is True for k, v in out["checks"].items() if k in (
            "on_map", "story_modal", "picked_data", "back_to_map", "flag_open", "rel_tang_1",
            "agency_open", "ok_cost_free", "ok_not_locked", "ok_cost_red", "ok_btn_bg_priority",
            "ok_hint_opacity_1", "ok_title_opacity_1",
            "pen_sent_ok", "sheet_back", "sent_cost_today", "sent_locked_cls", "sent_cost_grey",
            "sent_btn_bg_grey", "sent_title_dimmed", "sent_title_opacity_072",
            "sent_hint_opacity_072", "sent_hint_readable", "sent_hint_color_3a2e22",
            "sent_not_disabled", "sent_click_toasts", "sent_click_no_gift_modal"))
    except Exception as e:
        out["pass_ok_sent"] = False
        out["error"] = repr(e)
    finally:
        out["pageerrors_ok_sent"] = errs
        try: ctx.close()
        except Exception: pass
    # --- EMPTY 態（新 context，932） ---
    ctx2, pg2, errs2 = new_context(pw, 932)
    pg2.on("response", lambda r: out["errors"].append(f"http{r.status}: {r.url}") if r.status >= 400 else None)
    try:
        out["checks"].update({("empty_" + k): v for k, v in meet_and_back(pg2).items()})
        pg2.evaluate("() => { try { S.inventory = {}; S.money = 10000; } catch(e){} }")
        out["checks"]["empty_agency_open"] = bool(open_loc(pg2, "agency_ho"))
        pg2.wait_for_timeout(2500)
        emp = gift_visual_probe(pg2)
        out["empty_visual"] = emp
        out["checks"]["empty_cost_stock"] = emp and emp["cost"] == "庫存空"
        out["checks"]["empty_locked_cls"] = emp and emp["lockedCls"] is True
        out["checks"]["empty_cost_grey"] = emp and emp["costColor"] == "rgb(107, 86, 54)"
        out["checks"]["empty_btn_bg_grey"] = emp and emp["btnBg"] == "rgb(230, 223, 204)"
        out["checks"]["empty_not_disabled"] = emp and emp["disabled"] is False
        out["checks"]["empty_hint_opacity_072"] = emp and emp["hOpacity"] == "0.72"
        out["checks"]["empty_hint_readable"] = emp and emp["hintCR"] is not None and emp["hintCR"] >= 4.5
        p = shot(pg2, "c2_empty_932.png"); out["empty_shot_md5"] = shot_md5(p)
        clicked2, toast2 = click_locked_gift(pg2)
        out["empty_toast"] = toast2
        out["checks"]["empty_click_toasts"] = clicked2 is True and toast2 and toast2["visible"] is True and "庫存空空" in (toast2["text"] or "")
        out["checks"]["empty_click_no_gift_modal"] = modal_visible(pg2) is False
        out["pass_empty"] = all(v is True for k, v in out["checks"].items() if k.startswith("empty_") or k in (
            "empty_cost_stock", "empty_locked_cls", "empty_cost_grey", "empty_btn_bg_grey",
            "empty_not_disabled", "empty_click_toasts", "empty_click_no_gift_modal",
            "empty_hint_opacity_072", "empty_hint_readable"))
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

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("EXE:", EXE, "kind:", EXE_KIND)
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    import urllib.request
    served = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5).read().decode("utf-8")
    for marker in ("applyTangGift169", "syncLocActsFade171", "act-locked171", "loc-acts-more171", "#f8f1de 60%", "opacity:.72 !important"):
        assert marker in served, f"server on {PORT} is NOT work171 (missing {marker})"
    print(f"serving work173 on {PORT} (markers ok)")
    results = {}
    try:
        with sync_playwright() as pw:
            if which in ("all", "c1"):
                results["c1_932"] = run_c1(pw, 932)
                results["c1_700"] = run_c1(pw, 700)
            if which in ("all", "c2"):
                results["c2"] = run_c2(pw)
        json.dump(results, open(os.path.join(HERE, "drive173.json"), "w"), ensure_ascii=False, indent=1)
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
