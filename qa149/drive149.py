#!/usr/bin/env python3
"""v20a147 設計 review 實駕（只擷圖＋量度，唔改 game code）。
Mirror：~/workspace/linji-design-review-v147/mirror-main（worktree，HEAD a3a0ac1），port 8981，?softPreview=1。
沿用 linji-work147/qa147/drive147.py 模式（new_game_to_map / seed / modal_info / forceTier
"gallery"/"nominee" / 報紙 queue 用 eventKey / 剪報物件只有 eventKeys），再加：
  - 每 beat 逐個截圖（按 __awards.beats62(pack) 預期時長分段）＋每 beat 時長量度
  - 晨報 modal 實景截圖＋全文 dump＋溢出量度（唔再盲 dismiss）
  - 剪報頁（手帳「剪報」tab）實景截圖
  - 真實路徑入圍對照（seed 兩部 1991 電影 wrap，唔用 forceTier）
  - B 主畫面抽查（地圖／手帳／進度／S-30／對話舞台，932＋700）
用法：/home/hatch/pwenv49/bin/python drive147r.py [case|all]
I/O 防禦：截圖／JSON 寫檔失敗 retry 3 次，失敗記低、結果照印 stdout。
"""
import json, subprocess, sys, time, os, datetime
from playwright.sync_api import sync_playwright
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v142")
import drive142r_base as B

HERE = "/home/hatch/workspace/linji-work149/qa149"
ROOT = os.environ.get("DRIVE149_ROOT", "/home/hatch/workspace/linji-work149")
SHOTS = os.path.join(HERE, "shots")
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = int(os.environ.get("DRIVE149_PORT", "8983"))
SAVE_KEY = "starVolunteer_map_v19w"
FILM = "award_harbour_film"
TV = "award_singho_tv"
os.makedirs(SHOTS, exist_ok=True)

def shot(pg, name):
    for i in range(3):
        try:
            pg.screenshot(path=os.path.join(SHOTS, name))
            return True
        except Exception as e:
            if i == 2:
                print(f"  SHOT FAIL {name}: {e!r}", flush=True)
                return False
            time.sleep(1.0)

def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)

def click_vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false;
      vis[0].click(); return true;
    }""", text)

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
      const choices = [...document.querySelectorAll('#modal .sp-choice')].map(b => (b.textContent||'').trim()).filter(Boolean);
      const comfort = document.querySelector('#modal .psr-comfort147');
      const body = (m.innerText || '').slice(0, 3000);
      return {visible:true, h3, btns, choices, body,
              comfort: comfort ? comfort.textContent : null};
    }""")

def modal_overflow(pg):
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      if (!m) return null;
      const mi = document.getElementById('modal-inner');
      const bad = [];
      m.querySelectorAll('*').forEach(el => {
        if (el.scrollWidth > el.clientWidth + 2 && el.children.length === 0) {
          const t = (el.textContent||'').trim().slice(0, 40);
          if (t) bad.push({tag: el.tagName, cls: (el.className||'').toString().slice(0,40), sw: el.scrollWidth, cw: el.clientWidth, txt: t});
        }
      });
      return {modalScrollH: m.scrollHeight, modalClientH: m.clientHeight,
              innerScrollH: mi ? mi.scrollHeight : null, innerClientH: mi ? mi.clientHeight : null,
              innerScrollTop: mi ? mi.scrollTop : null, hOverflow: bad.slice(0, 6)};
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

def day_index(y, m, d):
    return (datetime.date(y, m, d) - datetime.date(1990, 1, 1)).days

def seed(pg, *, day, fame=40, stage=10, acting=10, credit_delta=0, money=5000, stress=0, wraps=None):
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = o.fame; S.stage = o.stage; S.acting = o.acting;
      S.industryCreditDelta = o.credit_delta;
      S.money = o.money; S.stress = o.stress;
      S.flags = S.flags || {};
      if (o.wraps) S.wrapHistory = o.wraps;
      if (typeof BehaviorGate !== "undefined" && BehaviorGate.readCtx) {
        const ctx = BehaviorGate.readCtx({});
        return { day: S.dayIndex, week: ctx.week, year: ctx.year, season: ctx.season, dual: ctx.dual };
      }
      return { day: S.dayIndex };
    }""", {"day": day, "fame": fame, "stage": stage, "acting": acting,
            "credit_delta": credit_delta, "money": money, "stress": stress, "wraps": wraps})

def map_ready(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }") \
        and (not modal_info(pg).get("visible")) and (vis_btn(pg, "過一日") or vis_btn(pg, "開始今日行程"))

def home_on(pg):
    return pg.evaluate("() => { const v = document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")

def pump_to_map(pg, secs=45, stop_on_invite=False):
    seen = []
    t0 = time.time()
    while time.time() - t0 < secs:
        mi = modal_info(pg)
        if mi.get("visible"):
            if stop_on_invite and any("出席" in b for b in mi.get("btns") or []):
                seen.append({"h3": mi.get("h3", ""), "btns": mi.get("btns", []), "body": (mi.get("body", "") or "")[:400]})
                return {"onMap": False, "seen": seen, "invite": mi}
            seen.append({"h3": mi.get("h3", ""), "btns": mi.get("btns", []), "body": (mi.get("body", "") or "")[:400]})
            if not dismiss_once(pg):
                if not click_vis_btn(pg, "返回地圖"):
                    pg.wait_for_timeout(400)
        elif home_on(pg) and vis_btn(pg, "確定本週行程"):
            seen.append({"h3": "屋企（週結算）", "btns": [], "body": pg.evaluate("() => { const v = document.getElementById('v-home'); return v ? v.innerText.slice(0, 1500) : ''; }")})
            click_vis_btn(pg, "確定本週行程")
            pg.wait_for_timeout(800)
        elif map_ready(pg):
            return {"onMap": True, "seen": seen}
        else:
            pg.wait_for_timeout(400)
        pg.wait_for_timeout(300)
    return {"onMap": map_ready(pg), "seen": seen}

def advance_day_capture_paper(pg, prefix, secs=60):
    """撳「過一日」，途中如有晨報 modal 就截圖＋dump 全文＋量溢出，先至 dismiss；回傳 paper modal 紀錄。"""
    papers = []
    if vis_btn(pg, "過一日"):
        click_vis_btn(pg, "過一日")
    elif vis_btn(pg, "開始今日行程"):
        click_vis_btn(pg, "開始今日行程")
        pg.wait_for_timeout(1000)
        mi = modal_info(pg)
        if mi.get("visible") and any("回家結算" in b for b in mi.get("btns") or []):
            click_vis_btn(pg, "回家結算")
        elif vis_btn(pg, "過一日"):
            click_vis_btn(pg, "過一日")
        else:
            return {"advanced": False, "papers": papers}
    else:
        return {"advanced": False, "papers": papers}
    pg.wait_for_timeout(800)
    t0 = time.time()
    while time.time() - t0 < secs:
        mi = modal_info(pg)
        if mi.get("visible"):
            body = mi.get("body") or ""
            is_paper = any(k in body for k in ["報紙", "娛樂快報", "剪報", "晨報", "頭版"]) or any(k in (mi.get("h3") or "") for k in ["報紙", "晨報"])
            if is_paper and not any(p.get("body") == body for p in papers):
                rec = {"h3": mi.get("h3", ""), "btns": mi.get("btns", []), "body": body,
                       "overflow": modal_overflow(pg), "tail": paper_tail_check(pg)}
                papers.append(rec)
                shot(pg, f"{prefix}_paper.png")
                print(f"  [paper] h3={rec['h3']!r} btns={rec['btns']}", flush=True)
            if not dismiss_once(pg):
                if not click_vis_btn(pg, "返回地圖"):
                    pg.wait_for_timeout(400)
        elif home_on(pg) and vis_btn(pg, "確定本週行程"):
            click_vis_btn(pg, "確定本週行程")
            pg.wait_for_timeout(800)
        elif map_ready(pg):
            return {"advanced": True, "papers": papers, "onMap": True}
        else:
            pg.wait_for_timeout(400)
        pg.wait_for_timeout(300)
    return {"advanced": True, "papers": papers, "onMap": map_ready(pg)}

def save_slot1(pg):
    return pg.evaluate("""(key) => {
      try { localStorage.setItem(key, JSON.stringify(S)); return { saved: true, day: S.dayIndex, hasPending: !!S.pendingAwardPack }; }
      catch(e) { return { saved: false, error: String(e) }; }
    }""", SAVE_KEY)

def s_state(pg):
    return pg.evaluate("""() => ({
      day: S.dayIndex,
      awardsFlags: S.awardsFlags || {},
      pendingAwardPack: S.pendingAwardPack ? { ceremonyId: S.pendingAwardPack.ceremonyId, year: S.pendingAwardPack.year, tier: S.pendingAwardPack.tier, bestOutcome: S.pendingAwardPack.bestOutcome } : null,
      newspaperQueue: (S.newspaperQueue || []).map(q => ({ eventKey: q.eventKey, templateEventKey: q.templateEventKey || null, fameDelta: q.fameDelta, headline: q.headline || '', dek: q.dek || '' })),
      clippings: (S.newspaperClippings || []).flatMap(c => (c && c.eventKeys) || []),
      clipItems: (S.newspaperClippings || []).flatMap(c => (c && c.items) || []).map(i => ({ eventKey: i.eventKey, templateEventKey: i.templateEventKey || null, fameDelta: i.fameDelta, headline: i.headline || '', dek: i.dek || '' })),
    })""")

def force_award(pg, ceremony_id, tier=None):
    """強制排一場典禮＋彈請柬。tier=None 時唔傳 forceTier（真實判定）。"""
    pack = pg.evaluate("""(o) => {
      try {
        const args = o.tier ? { forceTier: o.tier } : {};
        const p = window.__awards.debugForceSeasonWindow(o.id, args);
        if (!p) return { error: 'no pack' };
        window.__awards.present();
        return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
                 tier: p.tier, categories: (p.categories || []).map(c => ({ outcome: c.outcome, label: c.label })) };
      } catch(e) { return { error: String(e) }; }
    }""", {"id": ceremony_id, "tier": tier})
    pg.wait_for_timeout(1000)
    inv = modal_info(pg)
    # 請柬完整 body（modal_info 只截 3000 字，呢度再攞全文＋gate 行）
    full = pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      if (!m) return null;
      const gate = m.querySelector('.psr-gate62');
      const sheet = m.querySelector('.psr-sheet');
      return { fullText: (m.innerText || ''), gateLine: gate ? gate.textContent : null,
               gateClass: gate ? gate.className : null,
               standing: (() => { try { const p = window.__awards.pending(); return p && p.standing62 ? { tier: p.standing62.tier, wraps: p.standing62.wraps, wrapMin: p.standing62.wrapMin, gapWorks: p.standing62.gapWorks, dualOk: p.standing62.dualOk, bestBase: p.standing62.bestBase } : null; } catch(e) { return null; } })() };
    }""")
    return {"pack": pack, "invite": inv, "invite_full": full}

def stage_state(pg):
    return pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      const skip = st.querySelector('.awd62-skip');
      const frame = st.querySelector('.awd62-frame');
      const cv = st.querySelector('canvas.awd62-canvas');
      const audClassCount = st.querySelectorAll('[class*="aud"]').length; // 反向探針：觀眾帶已剔走應為 0（class 名拆開查，唔寫全名）
      const stageBg = getComputedStyle(st).backgroundColor; // F1：frame 上下剩餘空間底色
      const conf = [...st.querySelectorAll('.awd62-m5fx149')].map(im => ({on: im.classList.contains('on'), vis: getComputedStyle(im).display !== 'none', w: Math.round(im.getBoundingClientRect().width), h: Math.round(im.getBoundingClientRect().height)}));
      const cards = [...st.querySelectorAll('.awd63-card')].map(c => {
        const css = c.querySelector('.awd63-csscard');
        const img = c.querySelector('img');
        return { cls: (c.className||'').toString(), text: (c.innerText||'').replace(/\\n/g,' / ').slice(0,60),
                 hasImg: !!img, imgSrc: img ? (img.getAttribute('src')||'').slice(0,60) : null,
                 cssText: css ? (css.innerText||'').replace(/\\n/g,' / ').slice(0,60) : null,
                 cssHasIcon: css ? !!css.querySelector('img, .awd63-cssicon') : null,
                 titleCount: ((c.innerText||'').match(/《/g)||[]).length };
      });
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); return {top: Math.round(b.top), bottom: Math.round(b.bottom), h: Math.round(b.height), w: Math.round(b.width), left: Math.round(b.left), right: Math.round(b.right)}; };
      return { present: true,
               caption: cap ? cap.textContent : '',
               captionHtml: cap ? cap.innerHTML.slice(0, 300) : '',
               skipVisible: !!skip && skip.getBoundingClientRect().width > 0,
               skipBox: r(skip), frameBox: r(frame), audClassCount, stageBg, confetti: conf,
               canvasBacking: cv ? {w: cv.width, h: cv.height} : null,
               canvasBox: r(cv),
               captionBox: r(cap), vh: window.innerHeight, vw: window.innerWidth,
               captionOverflowsBottom: cap ? (cap.getBoundingClientRect().bottom > window.innerHeight + 1) : null,
               cards };
    }""")

def paper_tail_check(pg):
    """B4：報紙 modal 第一眼（唔碌）尾句「下期。」可見否——尾句 rect 底唔可以俾「收下這份剪報」掣遮住。"""
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      if (!m) return {paper: false};
      const btns = [...document.querySelectorAll('#modal-btns button')].filter(b => b.getBoundingClientRect().width > 0);
      const btnTop = btns.length ? Math.min(...btns.map(b => b.getBoundingClientRect().top)) : null;
      const mi = document.getElementById('modal-inner');
      let tail = null;
      m.querySelectorAll('.paper-sheet p, .paper-sheet h4, .paper-sheet .paper-short p').forEach(el => {
        const t = (el.textContent||'').trim();
        if (t.includes('下期')) { const b = el.getBoundingClientRect(); tail = {txt: t.slice(-20), top: Math.round(b.top), bottom: Math.round(b.bottom)}; }
      });
      return {paper: true, btnTop: btnTop === null ? null : Math.round(btnTop),
              innerScrollH: mi ? mi.scrollHeight : null, innerClientH: mi ? mi.clientHeight : null,
              innerScrollTop: mi ? mi.scrollTop : null, tail,
              tailAboveBtn: !!(tail && btnTop !== null && tail.bottom <= btnTop),
              tailInViewport: !!(tail && tail.bottom <= window.innerHeight)};
    }""")


def expected_beats(pg, pack):
    try:
        return pg.evaluate("""(p) => {
          try { const pk = window.__awards.pending() || p; return window.__awards.beats62(pk).map(b => ({ id: b.id, ms: b.ms, caption: (b.caption||'').slice(0,80), lines: (b.lines||[]).slice() })); }
          catch(e) { return { error: String(e) }; }
        }""", pack)
    except Exception as e:
        return {"error": repr(e)}

def beat_id_for_caption(cap):
    """按字幕內容對應 beat id（實測每 beat 比預期 ms 早約 300ms，唔可以用預期時間邊界分段）。"""
    c = cap or ""
    if "拍拍你膊頭" in c:
        return "comfort"
    if "掌聲響起" in c:
        return "out"
    if "得獎者是" in c:
        return "suspense"
    if "入圍名單" in c:
        return "names"
    if "魚貫入場" in c:
        return "enter"
    if "觀禮席" in c:
        return "pan"
    if "得獎" in c:
        return "reveal"
    if c.strip().startswith("——"):
        return "open"
    return None

def watch_ceremony(pg, prefix, exp_beats, secs=25):
    """按 caption 變化＋內容對應 beat 分段；每段入段後 ~350ms 截一張（names 另加中段一張）。
    exp_beats 只用嚟計預期總長（必須喺撳「出席」前經 __awards.beats62(pending pack) 攞，開場後 pending 已清）。"""
    timeline = []
    beats_seen = []
    probes = {}
    last = None
    t0 = time.time()
    exp = exp_beats or []
    expected_total = sum((b.get("ms") or 0) for b in exp)
    cur_seg = None
    seg_start = None
    names_mid_taken = False
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        cap = st.get("caption") or ""
        now = round((time.time() - t0) * 1000)
        seg = beat_id_for_caption(cap)
        if seg and seg != cur_seg:
            if cur_seg is not None and seg_start is not None:
                beats_seen.append({"id": cur_seg, "startMs": seg_start, "durMs": now - seg_start,
                                   "firstCaption": next((e["caption"] for e in timeline if e.get("seg") == cur_seg), "")})
            cur_seg = seg
            seg_start = now
            names_mid_taken = False
            pg.wait_for_timeout(350)
            shot(pg, f"{prefix}_beat_{seg}.png")
            st2 = stage_state(pg)
            if seg in ("reveal", "comfort") and seg not in probes:
                probes[seg] = st2
            if st2.get("present"):
                cap = st2.get("caption") or ""
                now = round((time.time() - t0) * 1000)
        if cur_seg == "names" and not names_mid_taken and seg_start is not None and now - seg_start >= 1400:
            shot(pg, f"{prefix}_beat_names_mid.png")
            names_mid_taken = True
        if cap != last:
            timeline.append({"t": now, "seg": beat_id_for_caption(cap), "caption": cap[:200]})
            last = cap
        pg.wait_for_timeout(70)
    total = round((time.time() - t0) * 1000)
    if cur_seg is not None and seg_start is not None:
        beats_seen.append({"id": cur_seg, "startMs": seg_start, "durMs": total - seg_start,
                           "firstCaption": next((e["caption"] for e in timeline if e.get("seg") == cur_seg), "")})
    return {"timeline": timeline, "beats": beats_seen, "expectedBeats": exp,
            "expectedTotalMs": expected_total, "totalMs": total,
            "stageGone": not stage_state(pg).get("present"), "probes": probes}

def paper_for_ceremony(st, ceremony_id, year):
    key = f"award:{year}:{ceremony_id}"
    q = [i for i in (st.get("newspaperQueue") or []) if i.get("eventKey") == key]
    c = [i for i in (st.get("clipItems") or []) if i.get("eventKey") == key]
    if key in (st.get("clippings") or []):
        c = c + [{"eventKey": key, "templateEventKey": None, "fameDelta": None, "headline": "", "dek": ""}]
    return {"key": key, "queued": q, "clipped": c}

def open_clippings(pg, prefix):
    """手帳 → 剪報 tab，截圖＋量度剪報卡溢出。回傳 {ok, text, overflow}。"""
    try:
        if not B.open_notebook(pg):
            return {"ok": False, "why": "open notebook failed"}
        if not B.click_nb_button(pg, "剪報"):
            # 後備：tab 掣 id htab-clippings（click_nb_button 要求 innerText 完全等於「剪報」）
            hit = pg.evaluate("""() => { const el = document.getElementById('htab-clippings'); if (!el) return false; el.click(); return true; }""")
            pg.wait_for_timeout(900)
            if not hit:
                return {"ok": False, "why": "clippings tab btn not found (nb_button + #htab-clippings)"}
        pg.wait_for_timeout(900)
        shot(pg, f"{prefix}_clippings.png")
        m = pg.evaluate("""() => {
          const list = document.querySelector('#clippings-list');
          const bad = [];
          if (list) list.querySelectorAll('*').forEach(el => {
            if (el.scrollWidth > el.clientWidth + 2 && el.children.length === 0) {
              const t = (el.textContent||'').trim().slice(0, 40);
              if (t) bad.push({tag: el.tagName, sw: el.scrollWidth, cw: el.clientWidth, txt: t});
            }
          });
          return {text: list ? list.innerText.slice(0, 1200) : null,
                  hOverflow: bad.slice(0, 6),
                  listScrollH: list ? list.scrollHeight : null, listClientH: list ? list.clientHeight : null};
        }""")
        m["ok"] = True
        return m
    except Exception as e:
        return {"ok": False, "why": repr(e)}

# ---------------- cases ----------------
def pending_winner(pg):
    """由 pending pack 取期望得主（focus cat fellows[0]；won 類別回 None）。"""
    return pg.evaluate("""() => {
      try {
        const p = window.__awards.pending();
        if (!p) return null;
        const cats = p.categories || [];
        const f = cats.find(c => c && c.outcome === 'nominated') || cats.find(c => c && c.outcome === 'gallery') || cats[0];
        if (!f) return null;
        if (f.outcome === 'won') return null;
        const w = f.winner63 || ((f.fellows63 || [])[0] || null);
        return w ? {star: w.star || '', title: w.title || ''} : null;
      } catch(e) { return {error: String(e)}; }
    }""")

def case_gallery(pg, W, H):
    tag = f"gallery_{W}x{H}"
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, FILM, "gallery")
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "invite": inv, "invite_full": fa.get("invite_full"), "checks": {},
           "expected_winner": pending_winner(pg)}
    out["expected_beats"] = expected_beats(pg, pack)
    out["checks"]["pack_is_gallery"] = pack.get("bestOutcome") == "gallery"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_attend"] = any("出席" in b for b in inv.get("btns") or [])
    out["checks"]["invite_has_decline"] = any("推辭" in b for b in inv.get("btns") or [])
    out["checks"]["invite_no_later"] = not any("稍後" in b for b in inv.get("btns") or [])
    shot(pg, f"{tag}_invite.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    st0 = stage_state(pg)
    out["stage_at_start"] = st0
    out["checks"]["stage_appears"] = bool(st0.get("present"))
    out["checks"]["skip_visible"] = bool(st0.get("skipVisible"))
    w = watch_ceremony(pg, tag, out["expected_beats"], 25)
    out["watch"] = w
    # --- B1（reveal probe） ---
    rp = (w.get("probes") or {}).get("reveal") or {}
    out["reveal_probe"] = rp
    fb = rp.get("frameBox") or {}
    vh = rp.get("vh") or H
    sk = rp.get("skipBox") or {}
    out["checks"]["b1_no_aud_bands"] = rp.get("audClassCount", -1) == 0
    out["f1"] = {"frameTop": fb.get("top"), "frameBottom": fb.get("bottom"), "vh": vh,
                 "topGap": fb.get("top"), "botGap": (vh - fb.get("bottom")) if fb.get("bottom") is not None else None,
                 "stageBg": rp.get("stageBg")}
    out["checks"]["b1_frame_vertically_centred"] = bool(fb) and abs((fb.get("top", 0) or 0) - (vh - (fb.get("bottom", 0) or 0))) <= 6
    out["checks"]["b1_canvas_backing_636x360"] = (rp.get("canvasBacking") or {}) == {"w": 636, "h": 360}
    out["checks"]["b1_confetti_m5_visible_at_reveal"] = any(c.get("vis") for c in (rp.get("confetti") or []))
    out["checks"]["b1_skip_inside_frame"] = bool(sk) and bool(fb) and sk.get("top", -999) >= fb.get("top", 0) and sk.get("right", 9999) <= fb.get("right", 0)
    caps = " || ".join(e["caption"] for e in w["timeline"])
    out["checks"]["six_beats_seen"] = len(w["beats"]) >= 6
    out["checks"]["beat_ids"] = [b["id"] for b in w["beats"]]
    out["checks"]["names_beat_lists_fellows_not_awei"] = ("入圍" in caps) and ("阿偉" not in caps)
    out["checks"]["reveal_names_winner"] = ("得獎者" in caps) or ("得獎" in caps)
    out["checks"]["total_about_9_6s"] = 8000 <= w["totalMs"] <= 11500
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    out["checks"]["caption_never_overflows_bottom"] = all(
        (e.get("caption") is not None) for e in w["timeline"])
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    shot(pg, f"{tag}_result.png")
    dismiss_once(pg)
    pump_to_map(pg, 30)
    save_slot1(pg)
    st_pre = s_state(pg)
    paper_pre = paper_for_ceremony(st_pre, FILM, 1991)
    adv = advance_day_capture_paper(pg, tag)
    out["next_day"] = adv
    st = s_state(pg)
    out["state_next_day"] = st
    paper = paper_for_ceremony(st, FILM, 1991)
    out["paper"] = paper
    out["paper_pre"] = paper_pre
    gal = (paper_pre["queued"] + paper["queued"] + paper["clipped"])
    out["checks"]["gallery_paper_queued_or_clipped"] = len(gal) > 0
    if gal:
        g0 = gal[0]
        out["checks"]["gallery_paper_template"] = g0.get("templateEventKey") == "award_gallery.film"
        out["checks"]["gallery_paper_fameDelta_1"] = g0.get("fameDelta") == 1
        txt = (g0.get("headline") or "") + (g0.get("dek") or "")
        w149 = out.get("expected_winner") or {}
        out["checks"]["b2_gallery_paper_names_winner"] = bool(w149.get("star")) and (w149["star"] in txt) and (w149.get("title", "") in txt) and ("奪獎" in txt)
        out["gallery_paper_text"] = txt
    out["checks"]["morning_paper_shown"] = len(adv.get("papers") or []) > 0
    # B2 結果卡：同屆提名有 🏆 標記＋metricLine 寫實內容（唔再係 stub）
    res_body = (res.get("body") or "") if isinstance(res, dict) else ""
    w149 = out.get("expected_winner") or {}
    out["checks"]["b2_result_fellows_marks_winner"] = ("為得主" in res_body) and bool(w149.get("star")) and (w149["star"] in res_body)
    out["checks"]["b2_result_metricline_real"] = bool(w149.get("star")) and (w149["star"] in res_body) and ("奪獎" in res_body) and ("典禮後仍有人提起" in res_body)
    # B4：700 報紙尾句第一眼可見
    tails = [pp.get("tail") or {} for pp in (adv.get("papers") or [])]
    out["checks"]["b4_tail_first_view"] = any(t.get("tailAboveBtn") for t in tails) if tails else False
    out["paper_tails"] = tails
    clip = open_clippings(pg, tag)
    out["clippings"] = clip
    out["checks"]["clippings_ok"] = bool(clip.get("ok"))
    return out

def case_nominated(pg, W, H, real=False):
    tag = ("nominated_real" if real else "nominated") + f"_{W}x{H}"
    if real:
        # 真實路徑：1991 年兩部電影 wrap（type 須 match ceremony matchTypes；先探一次 standing）
        probe = pg.evaluate("""() => {
          try { const c = awardsCeremonyById('award_harbour_film'); return { matchTypes: c.matchTypes, medium: c.medium }; }
          catch(e) { return { error: String(e) }; }
        }""")
        wraps = [{"wrappedDay": day_index(1991, 3, 10), "type": "電影", "dayIndex": day_index(1991, 3, 10)},
                 {"wrappedDay": day_index(1991, 7, 20), "type": "電影", "dayIndex": day_index(1991, 7, 20)}]
        ctx = seed(pg, day=day_index(1991, 10, 20), fame=120, stage=60, acting=60, credit_delta=80, wraps=wraps)
        standing = pg.evaluate("""() => { try { const c = awardsCeremonyById('award_harbour_film'); return window.__awards.standing62(c, 1991); } catch(e) { return { error: String(e) }; } }""")
        fa = force_award(pg, FILM, None)
        out_probe = {"ceremony_probe": probe, "standing_before_force": standing}
    else:
        ctx = seed(pg, day=day_index(1991, 10, 20), fame=120, stage=60, acting=60, credit_delta=80)
        fa = force_award(pg, FILM, "nominee")
        out_probe = {}
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "invite": inv, "invite_full": fa.get("invite_full"), "checks": {}, **out_probe}
    out["expected_beats"] = expected_beats(pg, pack)
    out["checks"]["pack_is_nominated"] = pack.get("bestOutcome") == "nominated"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    gate = ((fa.get("invite_full") or {}).get("gateLine") or "")
    standing_tier = ((fa.get("invite_full") or {}).get("standing") or {}).get("tier")
    if real:
        # 真實路徑：門檻行必須係「入圍門檻已達標」，唔可以有「仲差 N 部…先夠入圍」
        out["checks"]["invite_gate_correct_nominee"] = gate.startswith("入圍門檻已達標") and "先夠入圍" not in gate
    else:
        # 強制路徑：gate 行跟 standing62（真實判定，唔跟 forceTier），tier label 跟強制 tier——
        # 兩者唔一致係 debug-force 產物，唔係玩家路徑 bug；呢度只驗 gate 行忠實反映真實 standing
        out["checks"]["invite_gate_reflects_real_standing"] = ("先夠入圍" in gate) and standing_tier == "gallery"
    shot(pg, f"{tag}_invite.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    w = watch_ceremony(pg, tag, out["expected_beats"], 25)
    out["watch"] = w
    caps = [e["caption"] for e in w["timeline"]]
    joined = " || ".join(caps)
    ci = next((i for i, c in enumerate(caps) if "拍拍你膊頭" in c), -1)
    ri = next((i for i, c in enumerate(caps) if "得獎者" in c or "得獎" in c), -1)
    comfort_beat = next((b for b in w["beats"] if b["id"] == "comfort"), None)
    out["comfort_beat"] = comfort_beat
    # --- B3（comfort probe 卡片） ---
    cp = (w.get("probes") or {}).get("comfort") or {}
    out["comfort_probe"] = cp
    cards149 = cp.get("cards") or []
    out["checks"]["b3_cards_present"] = len(cards149) >= 2
    out["checks"]["b3_no_poster_card_is_icon_not_title"] = all(
        (c.get("hasImg") or (c.get("cssText") is not None and "《" not in (c.get("cssText") or "") and c.get("cssHasIcon")))
        for c in cards149)
    out["checks"]["b3_title_only_once_per_card"] = all((c.get("titleCount") or 0) <= 1 for c in cards149)
    out["checks"]["b3_winner_card_has_trophy_badge"] = any("win" in (c.get("cls") or "") for c in cards149)
    out["checks"]["comfort_beat_seen"] = ci >= 0
    out["checks"]["comfort_after_reveal"] = ci > ri >= 0
    out["checks"]["comfort_has_ho_and_awei"] = ("何生" in joined) and ("阿偉" in joined)
    out["checks"]["comfort_dur_about_2600"] = comfort_beat is not None and 2000 <= (comfort_beat.get("durMs") or 0) <= 3400
    out["checks"]["total_about_12s"] = 10000 <= w["totalMs"] <= 14500
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    out["checks"]["result_card_comfort_line"] = (res.get("comfort") or "") == "何生：「差少少啫，唔緊要，下年再嚟過。」"
    shot(pg, f"{tag}_result.png")
    return out

def case_skip(pg, W, H):
    tag = f"skip_{W}x{H}"
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, FILM, "gallery")
    out = {"ctx": ctx, "pack": fa["pack"], "checks": {}}
    out["checks"]["invite_shown"] = bool(fa["invite"].get("visible"))
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(1000)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    t0 = time.time()
    clicked = pg.evaluate("""() => { const b = document.querySelector('.awd62-skip'); if (!b) return false; b.click(); return true; }""")
    out["checks"]["skip_clicked"] = bool(clicked)
    pg.wait_for_timeout(800)
    out["skip_to_gone_ms"] = round((time.time() - t0) * 1000)
    out["checks"]["stage_gone_fast"] = not stage_state(pg).get("present")
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown_after_skip"] = bool(res.get("visible"))
    shot(pg, f"{tag}_result.png")
    return out

def case_declined(pg, W, H):
    tag = f"declined_{W}x{H}"
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, FILM, "gallery")
    out = {"ctx": ctx, "pack": fa["pack"], "invite": fa["invite"], "checks": {},
           "expected_winner": pending_winner(pg)}
    inv = fa["invite"]
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_decline"] = any("推辭" in b for b in inv.get("btns") or [])
    shot(pg, f"{tag}_invite.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "推辭")
    pg.wait_for_timeout(1200)
    pump_to_map(pg, 30)
    st = s_state(pg)
    out["after_decline"] = st
    out["checks"]["flag_skipped"] = (st.get("awardsFlags") or {}).get("1991/" + FILM) == "skipped"
    out["checks"]["pending_cleared"] = st.get("pendingAwardPack") is None
    out["checks"]["paper_queued_next_day"] = any((q.get("eventKey") == "award:1991:" + FILM) for q in (st.get("newspaperQueue") or []))
    paper_pre = paper_for_ceremony(st, FILM, 1991)
    out["paper_pre"] = paper_pre
    adv = advance_day_capture_paper(pg, tag)
    out["next_day"] = adv
    st2 = s_state(pg)
    out["state_next_day"] = st2
    paper = paper_for_ceremony(st2, FILM, 1991)
    out["paper"] = paper
    dec = (paper_pre["queued"] + paper["queued"] + paper["clipped"])
    out["checks"]["declined_paper_present"] = len(dec) > 0
    if dec:
        d0 = dec[0]
        out["checks"]["declined_paper_template"] = d0.get("templateEventKey") == "award_declined.film"
        out["checks"]["declined_paper_fameDelta_0"] = d0.get("fameDelta") == 0
        txt = (d0.get("headline") or "") + (d0.get("dek") or "")
        w149 = out.get("expected_winner") or {}
        out["checks"]["b2_declined_paper_names_winner"] = bool(w149.get("star")) and (w149["star"] in txt) and ("奪獎" in txt)
        out["checks"]["declined_paper_no_awei"] = "阿偉" not in txt
        out["declined_paper_text"] = txt
    out["checks"]["morning_paper_shown"] = len(adv.get("papers") or []) > 0
    tails = [pp.get("tail") or {} for pp in (adv.get("papers") or [])]
    out["checks"]["b4_tail_first_view"] = any(t.get("tailAboveBtn") for t in tails) if tails else False
    out["paper_tails"] = tails
    clip = open_clippings(pg, tag)
    out["clippings"] = clip
    out["checks"]["clippings_ok"] = bool(clip.get("ok"))
    return out

def case_gallery_tv(pg, W, H):
    """換 ceremony（TV 台慶）＋同一年：得主唔同，頭版／結果卡要跟實際得主，唔係寫死廖炳星。"""
    tag = f"gallery_tv_{W}x{H}"
    ctx = seed(pg, day=day_index(1991, 10, 20), fame=40, stage=10, acting=10)
    fa = force_award(pg, TV, "gallery")
    pack, inv = fa["pack"], fa["invite"]
    out = {"ctx": ctx, "pack": pack, "invite": inv, "invite_full": fa.get("invite_full"), "checks": {},
           "expected_winner": pending_winner(pg)}
    out["checks"]["pack_is_gallery"] = pack.get("bestOutcome") == "gallery"
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    if not out["checks"]["invite_shown"]:
        return out
    click_vis_btn(pg, "出席")
    pg.wait_for_timeout(400)
    w = watch_ceremony(pg, tag, expected_beats(pg, pack), 25)
    out["watch"] = w
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    dismiss_once(pg)
    pump_to_map(pg, 30)
    save_slot1(pg)
    adv = advance_day_capture_paper(pg, tag)
    out["next_day"] = adv
    st = s_state(pg)
    paper = paper_for_ceremony(st, TV, 1991)
    out["paper"] = paper
    gal = (paper["queued"] + paper["clipped"])
    out["checks"]["gallery_tv_paper_present"] = len(gal) > 0
    w149 = out.get("expected_winner") or {}
    if gal:
        txt = (gal[0].get("headline") or "") + (gal[0].get("dek") or "")
        out["checks"]["b2_tv_paper_names_its_winner"] = bool(w149.get("star")) and (w149["star"] in txt) and ("奪獎" in txt)
        out["checks"]["b2_tv_paper_not_film_headline"] = "維港影藝獎之夜" not in txt
        out["gallery_tv_paper_text"] = txt
    res_body = (res.get("body") or "")
    out["checks"]["b2_tv_result_marks_winner"] = ("為得主" in res_body) and bool(w149.get("star")) and (w149["star"] in res_body)
    return out

# ---------------- B：主畫面抽查 ----------------
ADVANCE_JS = """() => {
  const vis = b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width>0 && r.height>0 && cs.visibility!=='hidden' && cs.display!=='none'; };
  const cands = [...document.querySelectorAll('#modal-btns button, #enc79-overlay button, .sp-actions button, #loc-sheet button')].filter(vis);
  if(!cands.length) return 'none';
  const next = cands.find(b => /下一句|繼續/.test(b.textContent||''));
  const el = next || cands[0];
  const t = (el.textContent||'').trim().slice(0, 12);
  el.click();
  return t;
}"""

def js_click_text(pg, text):
    """JS .click()（繞過 Playwright hit-test；loc-sheet #loc-bg 遮住 #btn-menu 時用）。"""
    ok = pg.evaluate("""(t) => {
      const els=[...document.querySelectorAll('button')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()===t;});
      if(!els.length) return false; els[0].click(); return true; }""", text)
    pg.wait_for_timeout(800)
    return ok

def open_notebook_js(pg):
    """開手帳（JS click，唔經 Playwright hit-test）。"""
    if not pg.evaluate("() => { const b = document.getElementById('btn-menu'); if (!b) return false; b.click(); return true; }"):
        return False
    pg.wait_for_timeout(800)
    if not pg.evaluate("() => { const b = document.querySelector('[data-m=\"journal\"]'); if (!b) return false; b.click(); return true; }"):
        return False
    pg.wait_for_timeout(1200)
    return pg.evaluate("() => !!document.querySelector('#v-home')")

def case_spot(pg, W, H):
    tag = f"spot_{W}x{H}"
    out = {"checks": {}}
    # 開局新遊戲會自動彈何生事務所 loc-sheet（首日引導），先閂咗佢先見到地圖
    js_click_text(pg, "返回地圖")
    B.clear_encounter(pg)
    pg.wait_for_timeout(600)
    out["sheet_closed"] = pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !(s && s.classList.contains('on')); }")
    out["checks"]["opening_sheet_closed"] = bool(out["sheet_closed"])
    out["map"] = pg.evaluate(B.JS_MAP_MEASURE)
    labels = [l["text"] for l in out["map"]["labels"]]
    out["checks"]["map_15_labels"] = len(labels) == 15
    out["map_labels"] = labels
    out["map_label_clashes"] = []
    labs = out["map"]["labels"]
    def overlap(a, b):
        return a["x"] < b["x"] + b["w"] and a["x"] + a["w"] > b["x"] and a["y"] < b["y"] + b["h"] and a["y"] + a["h"] > b["y"]
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            if overlap(labs[i]["rect"], labs[j]["rect"]):
                out["map_label_clashes"].append((labs[i]["text"], labs[j]["text"]))
    out["checks"]["map_no_label_clash"] = len(out["map_label_clashes"]) == 0
    out["map_labels_overflow"] = [l for l in labs if l["rect"]["right"] > 430 or l["rect"]["x"] < 0]
    out["checks"]["map_labels_inside_viewport"] = len(out["map_labels_overflow"]) == 0
    shot(pg, f"{tag}_map.png")
    # 進度頁：幕次序＋星途寄語（「進度」掣喺行程 pane，必須喺撳「事業」之前撳）
    assert open_notebook_js(pg), "open notebook failed"
    assert B.click_nb_button(pg, "進度"), "progress btn failed"
    pg.wait_for_timeout(800)
    out["progress"] = pg.evaluate("""() => {
      const el = document.querySelector('#home-pane-progress');
      const txt = el ? el.innerText : '';
      const acts = [...document.querySelectorAll('#home-pane-progress [class*=act], #home-pane-progress h3, #home-pane-progress h4')].map(e => (e.textContent||'').trim()).filter(Boolean).slice(0, 30);
      const msg = document.querySelector('.prog71-next142');
      return {text: txt.slice(0, 1500), actHeads: acts,
              next142: msg ? msg.innerText.trim().slice(0, 200) : null,
              next142Rect: (()=>{ if(!msg) return null; const b = msg.getBoundingClientRect(); return {y: Math.round(b.y), bottom: Math.round(b.bottom), vh: window.innerHeight}; })()};
    }""")
    # 星途寄語摺線量度（已知 v142 B2：932 橫跨摺線，要碌先見晒——只記錄，唔當 FAIL）
    _r142 = out["progress"]["next142Rect"]
    out["progress_fold_overflow_px"] = (max(0, (_r142 or {}).get("bottom", 0) - H) if _r142 else None)
    shot(pg, f"{tag}_progress.png")
    # 對話舞台：去何生事務所撳「播劇情」卡播 C1（進度頁「播呢幕」掣只喺現場先出，屋企唔出）
    story_started = False
    if B.open_location(pg, "何生事務所"):
        B.clear_encounter(pg)
        pg.wait_for_timeout(600)
        story_started = pg.evaluate("""() => {
          const els=[...document.querySelectorAll('#loc-sheet button, #loc-sheet [role=button], #loc-acts button')].filter(e=>{
            const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').includes('播劇情');});
          if(!els.length) return false; els[0].click(); return true; }""")
        pg.wait_for_timeout(1200)
    out["story_play"] = story_started
    out["checks"]["story_started"] = bool(story_started)
    if story_started:
        pg.wait_for_timeout(1000)
        for i in range(6):
            pg.evaluate(ADVANCE_JS)
            pg.wait_for_timeout(500)
        out["story_mid"] = pg.evaluate("""() => {
          const box = document.querySelector('.sp-plate');
          const imgs = [...document.querySelectorAll('#modal img')].filter(im => im.getBoundingClientRect().height > 200).map(im => { const b = im.getBoundingClientRect(); return {src: (im.getAttribute('src')||'').split('/').pop(), y: Math.round(b.y), bottom: Math.round(b.bottom), h: Math.round(b.height), dim: getComputedStyle(im).opacity}; }).slice(0, 6);
          const dlg = document.querySelector('.sp-plate');
          const dr = dlg ? dlg.getBoundingClientRect() : null;
          const spk = document.querySelector('.sp-speaker');
          return {text: box ? (box.innerText||'').slice(0, 200) : null,
                  speaker: spk ? spk.textContent.trim() : null,
                  imgs,
                  dialogBox: dr ? {top: Math.round(dr.top), bottom: Math.round(dr.bottom), h: Math.round(dr.height)} : null,
                  vh: window.innerHeight};
        }""")
        shot(pg, f"{tag}_story.png")
        # 對話框遮腿：框頂低過人物圖底（人物伸入框後面）
        sm = out["story_mid"] or {}
        imgs = sm.get("imgs") or []
        dlg = sm.get("dialogBox")
        out["checks"]["story_dialog_covers_legs"] = bool(dlg and imgs and any(im["bottom"] > dlg["top"] for im in imgs))
    js_click_text(pg, "返回地圖")
    pg.wait_for_timeout(700)
    # 手帳：紙面 tab＋一組 pane（事業）
    assert open_notebook_js(pg), "reopen notebook failed"
    B.click_nb_button(pg, "事業")
    pg.wait_for_timeout(800)
    out["nb_career"] = pg.evaluate("""() => { const v = document.querySelector('#v-home'); return v ? v.innerText.slice(0, 600) : null; }""")
    shot(pg, f"{tag}_nb_career.png")
    # S-30：手帳事業 → 去通告欄 → 列表＋第一張詳情（老闆 bust 髮頂）
    B.click_nb_button(pg, "事業")
    pg.wait_for_timeout(800)
    found = click_vis_btn(pg, "去通告欄")
    out["s30_entry"] = found
    pg.wait_for_timeout(900)
    out["s30_list"] = pg.evaluate("""() => { const m = document.querySelector('#modal'); return m ? m.innerText.slice(0, 800) : null; }""")
    shot(pg, f"{tag}_s30_list.png")
    clicked = pg.evaluate("""() => {
      const els = [...document.querySelectorAll('.gig-teaser')].filter(el => { const r=el.getBoundingClientRect(); return r.width>0 && r.height>0; });
      if(!els.length) return false; els[0].click(); return (els[0].textContent||'').trim().slice(0,40);
    }""")
    out["s30_click"] = clicked
    pg.wait_for_timeout(900)
    out["s30_hero"] = pg.evaluate(B.JS_A1_MEASURE)
    out["checks"]["s30_boss_top_visible"] = ((out["s30_hero"].get("img") or {}).get("rect") or {}).get("y", -999) >= 0
    shot(pg, f"{tag}_s30_detail.png")
    return out

CASES = {
    "gallery_932": lambda pg: case_gallery(pg, 430, 932),
    "gallery_700": lambda pg: case_gallery(pg, 430, 700),
    "gallery_tv_932": lambda pg: case_gallery_tv(pg, 430, 932),
    "nominated_932": lambda pg: case_nominated(pg, 430, 932),
    "nominated_700": lambda pg: case_nominated(pg, 430, 700),
    "declined_932": lambda pg: case_declined(pg, 430, 932),
    "declined_700": lambda pg: case_declined(pg, 430, 700),
}

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    sel = list(CASES.keys()) if arg == "all" else [arg]
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        try:
            for name in sel:
                H = 700 if name.endswith("_700") else 932
                print(f"== {name} ==", flush=True)
                errs = []
                ctx = b.new_context(viewport={"width": 430, "height": H}, device_scale_factor=2)
                pg = ctx.new_page()
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
                try:
                    if not new_game_to_map(pg):
                        results[name] = {"verdict": "ERROR", "checks": {}, "note": "new game did not reach map"}
                        print("  ERROR: no map", flush=True)
                        continue
                    r = CASES[name](pg)
                    r["pageerrors"] = errs[:8]
                    checks = r.get("checks", {})
                    r["verdict"] = "PASS" if checks and all(checks.values()) else "FAIL"
                    results[name] = r
                    print(f"  {r['verdict']} {json.dumps(checks, ensure_ascii=False)}", flush=True)
                    if errs:
                        print(f"    pageerrors: {errs[:3]}", flush=True)
                except Exception as e:
                    results[name] = {"verdict": "ERROR", "checks": {}, "error": repr(e)}
                    print(f"  ERROR {e!r}", flush=True)
                    try:
                        shot(pg, f"err_{name}.png")
                    except Exception:
                        pass
                finally:
                    ctx.close()
        finally:
            try:
                b.close()
            except Exception:
                pass
    try:
        srv.terminate()
    except Exception:
        pass
    try:
        with open(os.path.join(HERE, "drive149.json"), "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"NOTE drive147r.json write failed: {e!r}", flush=True)
    print("RESULTS_JSON_BEGIN")
    print(json.dumps(results, ensure_ascii=False))
    print("RESULTS_JSON_END")
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    print(f"OVERALL {n_pass}/{len(results)} PASS")
    sys.exit(0 if n_pass == len(results) else 1)

if __name__ == "__main__":
    main()
