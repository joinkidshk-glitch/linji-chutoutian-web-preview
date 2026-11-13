#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v20a175 實駕：v153 review C1＋C2。
Seed（review 同款）：1992-12-05 day 1069、C1–C16 done、C10 done。
C1：進度頁 C17／C18 開放行「已開放」得一次、note 係「返地圖嗰陣就會播出。（場景：…）」。
C2（adoption，8 次／viewport）：fresh context → 新遊戲 → B01 modal 出現後播種
    （C2–C16 done、C1 唔 done——留返「去何生事務所睇劇情」掣，行數照樣 18 行）→
    撳 B01 掣（真路徑，觸發原句 toast「已用預設行程 · 到何生事務所可播開局劇情」）
    → 300ms 內開進度頁 → 量度：overlay #toast 熄咗、banner 喺 .prog71-wrap 最頂
    in-flow、行 14–15 elementFromPoint 命中行本身、banner 同行 14–15 零相交；
    ＋1s 再量一次；～2s banner 要入 .bye 平滑收起、～2.6s 移除。
C2-live（1 次／viewport）：同一 setup，B01 掣＋#chip-story 同一個 JS task 撳，
    toast 喺進度頁開住嗰陣先觸發（80ms setTimeout）→ 驗 toast() 分流：#toast 全程唔著，
    banner 照出、行唔遮。
截圖只喺無 modal／無 enc79 overlay 嗰陣影；DOM 證據為準。
用法：/home/hatch/pwenv49/bin/python qa175/drive175.py [932|700|all]
"""
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v153")
import drive153r as D
from playwright.sync_api import sync_playwright

WORK_ROOT = "/home/hatch/workspace/linji-work175"
HERE = os.path.join(WORK_ROOT, "qa175")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
PORT = 8175
TOAST_MSG = "已用預設行程 · 到何生事務所可播開局劇情"
# C2 播種：C1 唔 done（留返 B01 go 掣），其餘同 review seed——行數照樣 18 行。
SEED_C2_DONE = ["C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
                "C11", "C12", "C13", "C14", "C15", "C16"]

MEASURE_JS = """() => {
  const rows = [...document.querySelectorAll('.prog71-row')];
  const r = (el) => { const b = el.getBoundingClientRect(); return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), bottom: Math.round(b.bottom)}; };
  const t = document.getElementById('toast');
  const b = document.getElementById('prog175-banner');
  const wrap = document.querySelector('#progress-list .prog71-wrap');
  const hit = {};
  for (const i of [13, 14]) {  // 0-based：第 14、15 幕
    const row = rows[i];
    if (!row) { hit[i+1] = null; continue; }
    const bb = row.getBoundingClientRect();
    const el = document.elementFromPoint(bb.x + bb.width/2, bb.y + bb.height/2);
    let inRow = false; let cur = el;
    while (cur) { if (cur === row) { inRow = true; break; } cur = cur.parentElement; }
    hit[i+1] = {el: el ? (el.tagName + '.' + (el.className||'').toString().slice(0,40)) : null, inRow};
  }
  const bannerRect = b ? r(b) : null;
  const rowRects = {};
  for (const i of [13, 14]) { if (rows[i]) rowRects[i+1] = r(rows[i]); }
  const overlap = (a, c) => a && c && !(a.x + a.w <= c.x || c.x + c.w <= a.x || a.y + a.h <= c.y || c.y + c.h <= a.y);
  return {
    toastOn: t ? t.classList.contains('on') : null,
    toastTxt: t ? (t.textContent||'').trim().slice(0,50) : '',
    banner: b ? {text: (b.textContent||'').trim(), pos: getComputedStyle(b).position,
                 firstChild: wrap ? wrap.firstChild === b : null, bye: b.classList.contains('bye'),
                 rect: bannerRect} : null,
    rows: rows.length,
    row14: rowRects[14] || null, row15: rowRects[15] || null,
    hit,
    bannerOverlapsRow14: overlap(bannerRect, rowRects[14]),
    bannerOverlapsRow15: overlap(bannerRect, rowRects[15]),
    firstRowY: rows.length ? Math.round(rows[0].getBoundingClientRect().y) : null,
  };
}"""


MEASURE_HIT_JS = """() => {
  const rows = [...document.querySelectorAll('.prog71-row')];
  const r = (el) => { const b = el.getBoundingClientRect(); return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), bottom: Math.round(b.bottom)}; };
  if (rows[14]) rows[14].scrollIntoView({block: 'center'});
  const b = document.getElementById('prog175-banner');
  const bannerRect = b ? r(b) : null;
  const hit = {};
  for (const i of [13, 14]) {
    const row = rows[i];
    if (!row) { hit[i+1] = null; continue; }
    const bb = row.getBoundingClientRect();
    const el = document.elementFromPoint(bb.x + bb.width/2, bb.y + bb.height/2);
    let inRow = false; let cur = el;
    while (cur) { if (cur === row) { inRow = true; break; } cur = cur.parentElement; }
    hit[i+1] = {el: el ? (el.tagName + '.' + (el.className||'').toString().slice(0,40)) : null, inRow};
  }
  const rowRects = {};
  for (const i of [13, 14]) { if (rows[i]) rowRects[i+1] = r(rows[i]); }
  const overlap = (a, c) => a && c && !(a.x + a.w <= c.x || c.x + c.w <= a.x || a.y + a.h <= c.y || c.y + c.h <= a.y);
  return {hit, bannerRect, row14: rowRects[14] || null, row15: rowRects[15] || null,
          bannerOverlapsRow14: overlap(bannerRect, rowRects[14]),
          bannerOverlapsRow15: overlap(bannerRect, rowRects[15])};
}"""


def hit_ok(m, n):
    h = (m.get("hit") or {}).get(str(n))
    return bool(h and h.get("inRow"))


def open_rows_c1(pg):
    return pg.evaluate("""() => {
      const rows = [...document.querySelectorAll('.prog71-row')];
      const open = rows.filter(r => r.classList.contains('open')).map(r => {
        const t = (r.textContent||'');
        const note = (r.querySelector('.prog71-note')||{}).textContent || '';
        return {text: t.replace(/\\s+/g,' ').trim().slice(0,120),
                openCount: (t.match(/已開放/g)||[]).length,
                note: note.replace(/\\s+/g,' ').trim()};
      });
      return {n: rows.length, open};
    }""")


def fresh_to_b01(pg):
    """fresh load → 新遊戲 → skip 教學 → 等 B01 modal，回傳 True／False。"""
    pg.goto(f"http://127.0.0.1:{PORT}/index.html?softPreview=1")
    pg.wait_for_timeout(1500)
    for _ in range(5):
        if D.js_click_text(pg, "新遊戲"):
            break
        pg.wait_for_timeout(1000)
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
    last = None
    for _ in range(40):
        mi = D.modal_info(pg)
        last = mi
        if mi.get("visible") and any("去何生事務所睇劇情" in b for b in mi.get("btns", [])):
            return True, None
        if mi.get("visible"):
            D.dismiss_once(pg)
        elif D.map_ready(pg):
            return False, {"seen": "map_ready 無 B01", "last": last}
        pg.wait_for_timeout(400)
    return False, {"seen": "timeout 16s 無 B01", "last": last}


def click_b01_go(pg):
    return D.click_vis_btn(pg, "去何生事務所睇劇情")


def seed_c2(pg):
    D.seed(pg, day=D.day_index(1992, 12, 5), done_ids=SEED_C2_DONE, award_flag="done", c10_flag=True)


def no_overlay(pg):
    return pg.evaluate("""() => {
      const mi = document.querySelector('#modal');
      const modalVis = (() => { if (!mi) return false; const cs = getComputedStyle(mi); const r = mi.getBoundingClientRect();
        return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'; })();
      const ov = document.getElementById('enc79-overlay');
      let encVis = false;
      if (ov) { const r = ov.getBoundingClientRect(); const cs = getComputedStyle(ov);
        encVis = r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'; }
      return {modalVis, encVis};
    }""")


def dismiss_enc79_if_any(pg):
    for _ in range(3):
        ov = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return false;
          const r = ov.getBoundingClientRect(); const cs = getComputedStyle(ov);
          if (!(r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden')) return false;
          const btns = [...ov.querySelectorAll('button')].filter(b => {
            const br = b.getBoundingClientRect(); const bcs = getComputedStyle(b);
            return br.width > 0 && br.height > 0 && bcs.visibility !== 'hidden' && bcs.display !== 'none' && !b.disabled; });
          if (!btns.length) return false;
          btns[0].click(); return true;
        }""")
        if not ov:
            return
        pg.wait_for_timeout(1100)


def adoption_check(m0, m1, m2, m3, h0, h1):
    return (m0.get("rows") == 18
            and m0["toastOn"] is False and m1["toastOn"] is False
            and m0["banner"] and m0["banner"]["text"] == TOAST_MSG
            and m0["banner"]["pos"] == "static" and m0["banner"]["firstChild"]
            and hit_ok(h0, 14) and hit_ok(h0, 15)
            and hit_ok(h1, 14) and hit_ok(h1, 15)
            and not m0["bannerOverlapsRow14"] and not m0["bannerOverlapsRow15"]
            and not m1["bannerOverlapsRow14"] and not m1["bannerOverlapsRow15"]
            and not h0["bannerOverlapsRow14"] and not h0["bannerOverlapsRow15"]
            and not h1["bannerOverlapsRow14"] and not h1["bannerOverlapsRow15"]
            and m0["banner"]["rect"]["y"] < m0["firstRowY"]
            and (m2["banner"] is None or m2["banner"]["bye"])
            and m3["banner"] is None)


def run_adoption_iter(br, tag, it, out):
    rec = {"iter": it}
    ctx = br.new_context(viewport={"width": 430, "height": 932 if tag == "932" else 700})
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: out["pageerrors"].append(str(e)))
    try:
        ok_b01, why = fresh_to_b01(pg)
        if not ok_b01:
            rec["setup"] = why
            return rec
        seed_c2(pg)
        if not click_b01_go(pg):
            rec["setup"] = "B01 掣撳唔到"
            return rec
        pg.wait_for_timeout(300)
        pre = pg.evaluate("""() => { const t = document.getElementById('toast');
          return {on: t.classList.contains('on'), txt: (t.textContent||'').trim()}; }""")
        rec["toast_before_open"] = pre
        if not pre["on"] or pre["txt"] != TOAST_MSG:
            rec["setup"] = "開頁前 toast 唔係預期狀態：%s" % pre
            return rec
        dismiss_enc79_if_any(pg)
        pg.evaluate("() => { const c = document.querySelector('#chip-story'); if(c) c.click(); }")
        pg.wait_for_timeout(150)
        m0 = pg.evaluate(MEASURE_JS)
        rec["t0"] = m0
        h0 = pg.evaluate(MEASURE_HIT_JS)
        rec["h0"] = h0
        pg.wait_for_timeout(850)
        m1 = pg.evaluate(MEASURE_JS)
        rec["t1s"] = m1
        h1 = pg.evaluate(MEASURE_HIT_JS)
        rec["h1"] = h1
        pg.wait_for_timeout(1000)
        m2 = pg.evaluate(MEASURE_JS)
        rec["t2s"] = m2
        pg.wait_for_timeout(600)
        m3 = pg.evaluate(MEASURE_JS)
        rec["t2_6s"] = m3
        if it == 1:
            ov = no_overlay(pg)
            rec["overlay_before_shot"] = ov
            if not ov["modalVis"] and not ov["encVis"]:
                pg.screenshot(path=os.path.join(SHOTS, f"progress_banner_{tag}.png"))
                rec["shot"] = f"progress_banner_{tag}.png"
        rec["pass"] = adoption_check(m0, m1, m2, m3, h0, h1)
    except Exception as e:
        rec["error"] = str(e)[:200]
        rec["pass"] = False
    finally:
        try:
            ctx.close()
        except Exception:
            pass
    return rec


def run_livefire(br, tag, out):
    rec = {}
    ctx = br.new_context(viewport={"width": 430, "height": 932 if tag == "932" else 700})
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: out["pageerrors"].append(str(e)))
    try:
        ok_b01, why = fresh_to_b01(pg)
        if not ok_b01:
            rec["setup"] = why
            return rec
        seed_c2(pg)
        pg.evaluate("""() => {
          window.__t175 = [];
          const iv = setInterval(() => {
            const t = document.getElementById('toast');
            window.__t175.push(t.classList.contains('on') ? 1 : 0);
            if (window.__t175.length > 200) clearInterval(iv);
          }, 20);
          window.__t175_iv = iv;
          const goBtn = [...document.querySelectorAll('#modal-btns button')]
            .find(b => (b.textContent||'').includes('去何生事務所睇劇情'));
          if (goBtn) goBtn.click();
          const chip = document.querySelector('#chip-story');
          if (chip) chip.click();
        }""")
        pg.wait_for_timeout(600)
        m = pg.evaluate(MEASURE_JS)
        h = pg.evaluate(MEASURE_HIT_JS)
        rec["hit_measure"] = h
        trace = pg.evaluate("() => { clearInterval(window.__t175_iv); return (window.__t175||[]); }")
        rec["measure"] = m
        rec["toast_ever_on_samples"] = sum(trace)
        rec["samples"] = len(trace)
        rec["pass"] = (sum(trace) == 0 and m["toastOn"] is False and m["rows"] == 18 and m["banner"]
                       and m["banner"]["text"] == TOAST_MSG
                       and hit_ok(h, 14) and hit_ok(h, 15)
                       and not h["bannerOverlapsRow14"] and not h["bannerOverlapsRow15"])
    except Exception as e:
        rec["error"] = str(e)[:200]
        rec["pass"] = False
    finally:
        try:
            ctx.close()
        except Exception:
            pass
    return rec


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    tags = ["932", "700"] if only == "all" else [only]
    out = {"c1": {}, "c2_adoption": {}, "c2_livefire": {}, "checks": {}, "pageerrors": []}
    srv = D.serve(WORK_ROOT, PORT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"])
            for tag in tags:
                # ---- Phase 1：C1（seeded） ----
                ctx = br.new_context(viewport={"width": 430, "height": 932 if tag == "932" else 700})
                pg = ctx.new_page()
                pg.on("pageerror", lambda e: out["pageerrors"].append(str(e)))
                D.new_game_to_map(pg, PORT)
                D.seed(pg, day=D.day_index(1992, 12, 5), done_ids=D.PRE_C17, award_flag="done", c10_flag=True)
                D.open_progress(pg)
                c1 = open_rows_c1(pg)
                out["c1"][tag] = c1
                out["checks"][f"c1_{tag}"] = (c1["n"] == 18 and len(c1["open"]) == 2
                        and all(o["openCount"] == 1 for o in c1["open"])
                        and all(o["note"].startswith("返地圖嗰陣就會播出。（場景：") for o in c1["open"]))
                ctx.close()
                # ---- Phase 2：C2 adoption × 8（每 iteration 全新 context） ----
                iters = [run_adoption_iter(br, tag, i, out) for i in range(1, 9)]
                out["c2_adoption"][tag] = iters
                out["checks"][f"c2_adoption_{tag}_8of8"] = (
                    len(iters) == 8 and all(r.get("pass") for r in iters))
                # ---- Phase 3：C2 live-fire × 1 ----
                lf = run_livefire(br, tag, out)
                out["c2_livefire"][tag] = lf
                out["checks"][f"c2_livefire_{tag}"] = bool(lf.get("pass"))
            br.close()
    finally:
        D.stop(srv)
    out["checks"]["pageerrors_0"] = len(out["pageerrors"]) == 0
    with open(os.path.join(HERE, "drive175.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({"checks": out["checks"], "pageerrors": out["pageerrors"],
                      "c1": out["c1"]}, ensure_ascii=False, indent=1))
    bad = [k for k, v in out["checks"].items() if not v]
    print("CHECKS FAIL: " + " | ".join(bad) if bad else "ALL CHECKS PASS")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
