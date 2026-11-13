#!/usr/bin/env python3
"""v185 實駕：932／700 × 女角／星選擇器。
B1 硬標準：尾行卡片中心點＋「選」掣中心點 elementFromPoint 命中卡片／「選」本身；
700 下尾行 bottom ≤ 取消掣欄頂（btnrow top）；尾行「選」真滑鼠點擊送出。
C1：700 兩欄下全部卡片名 1 行（.n 高 == 1 行），名＋×N 同行，唔准孤兒行。
932 對照：單欄 list 可碌係正常，唔變壞。
用法：/home/hatch/pwenv49/bin/python qa185/drive185.py [case|all]"""
import json, subprocess, sys, time, os
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v183")
import probe183 as P
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work185"
HERE = "/home/hatch/workspace/linji-work185/qa185"
PORT = 8981
P.ROOT = ROOT
P.PORT = PORT

def shot(pg, name):
    try:
        pg.screenshot(path=os.path.join(HERE, name))
        return True
    except Exception:
        return False

def pick_geom(pg):
    """量度選擇器幾何＋命中＋名行數。回傳 dict。"""
    return pg.evaluate("""() => {
      const list = document.getElementById('gift-pick-list');
      const btns = document.querySelector('#modal-btns');
      const btnRow = btns ? [...btns.querySelectorAll('button')].find(b => (b.textContent||'').includes('取消')) : null;
      const btnTop = btnRow ? Math.round(btnRow.getBoundingClientRect().top) : null;
      const btnBottom = btnRow ? Math.round(btnRow.getBoundingClientRect().bottom) : null;
      const mi = document.getElementById('modal-inner');
      const rows = [...document.querySelectorAll('#gift-pick-list > *')].map(el => {
        const r = el.getBoundingClientRect();
        const cx = Math.round((r.left + r.right) / 2), cy = Math.round((r.top + r.bottom) / 2);
        const hit = document.elementFromPoint(cx, cy);
        const cost = el.querySelector('.cost');
        let costHit = null, costCx = null, costCy = null;
        if (cost) { const cb = cost.getBoundingClientRect();
          costCx = Math.round((cb.left + cb.right) / 2); costCy = Math.round((cb.top + cb.bottom) / 2);
          const ch = document.elementFromPoint(costCx, costCy);
          costHit = ch ? (ch === cost || cost.contains(ch)) : false; }
        const n = el.querySelector('.n');
        const nH = n ? Math.round(n.getBoundingClientRect().height) : null;
        return { name: (el.innerText || '').split('\\n')[0].slice(0, 24),
          top: Math.round(r.top), bottom: Math.round(r.bottom),
          hitIsRow: hit ? el.contains(hit) : false,
          hitTag: hit ? (hit.tagName + '.' + (hit.className || '').toString().slice(0, 30)) : null,
          costHit, costCx, costCy, nH };
      });
      const tail = rows.slice(-2);
      return { rows, nRows: rows.length, btnTop, btnBottom,
        tailBottomMax: tail.length ? Math.max(...tail.map(r => r.bottom)) : null,
        tailAllHit: tail.length === 2 && tail.every(r => r.hitIsRow && r.costHit),
        tailBottomLeBtnTop: tail.length === 2 && btnTop !== null && Math.max(...tail.map(r => r.bottom)) <= btnTop,
        allHit: rows.length > 0 && rows.every(r => r.hitIsRow && r.costHit),
        allNamesOneLine: rows.length > 0 && rows.every(r => r.nH !== null && r.nH <= 22),
        innerScroll: mi ? { scrollH: mi.scrollHeight, clientH: mi.clientHeight } : null };
    }""")

def scroll_inner_bottom(pg):
    """將 #modal-inner 碌到底（932 單欄對照用；700 唔需要）。"""
    return pg.evaluate("""() => { const mi = document.getElementById('modal-inner');
      if (!mi) return null; const before = mi.scrollTop; mi.scrollTop = mi.scrollHeight;
      return { before, after: mi.scrollTop, max: mi.scrollHeight - mi.clientHeight }; }""")

def open_woman_picker(pg):
    """新遊戲 → 撞林曉晴 → 撳送禮 → 選擇器。回傳 (ok, info)。"""
    if not P.new_game_to_map(pg):
        return False, {"step": "new_game_to_map"}
    mi, day, attempts = P.enter_woman(pg, "hiu", "tvb_longmen")
    if not (mi and mi.get("visible")):
        return False, {"step": "encounter", "attempts": attempts}
    if not P.click_vis_btn(pg, "送禮", "#modal"):
        return False, {"step": "click_gift"}
    pg.wait_for_timeout(1000)
    pick = P.wait_modal(pg, 4)
    if not pick.get("visible"):
        return False, {"step": "pick_modal"}
    return True, {"day": day}

def click_tail_cost(pg):
    """真滑鼠點擊尾行右邊一張（淡香水試用裝）嘅「選」掣中心點。回傳 (clicked, confirm_h3)。"""
    g = pick_geom(pg)
    tail = g["rows"][-1]
    pg.mouse.click(tail["costCx"], tail["costCy"])
    pg.wait_for_timeout(900)
    conf = P.wait_modal(pg, 4)
    return bool(conf.get("visible")), conf

def send_and_result(pg):
    """確認 modal 撳「送出」→ 結果 modal。回傳 result modal info。"""
    ok = P.click_vis_btn(pg, "送出", "#modal")
    pg.wait_for_timeout(1200)
    res = P.wait_modal(pg, 4)
    return ok, res

def case_woman(pg, W, H):
    out = {"checks": {}}
    ok, info = open_woman_picker(pg)
    out["open"] = info
    out["checks"]["open_picker"] = ok
    if not ok:
        return out
    g = pick_geom(pg)
    out["geom"] = g
    out["checks"]["ten_rows"] = g["nRows"] == 10
    out["checks"]["c1_all_names_one_line"] = g["allNamesOneLine"]
    shot(pg, f"woman_pick_{W}x{H}.png")
    if H == 700:
        out["checks"]["all_rows_hit"] = g["allHit"]
        out["checks"]["tail_all_hit"] = g["tailAllHit"]
        out["checks"]["b1_tail_bottom_le_btn_top"] = g["tailBottomLeBtnTop"]
    else:
        # 932 單欄：第一眼尾行喺摺疊下面係正常 modal 行為——碌到底再驗尾行
        out["checks"]["932_inner_scrollable"] = bool(g["innerScroll"]) and g["innerScroll"]["scrollH"] > g["innerScroll"]["clientH"]
        out["scroll932"] = scroll_inner_bottom(pg)
        pg.wait_for_timeout(300)
        g2 = pick_geom(pg)
        out["geom_scrolled"] = g2
        out["checks"]["932_tail_all_hit_after_scroll"] = g2["tailAllHit"]
        out["checks"]["932_tail_bottom_le_btn_top_after_scroll"] = g2["tailBottomLeBtnTop"]
        shot(pg, f"woman_pick_scrolled_{W}x{H}.png")
    # 尾行「選」真點擊送出（700 驗 B1 尾兩件撳得到；932 驗對照唔變壞）
    clicked, conf = click_tail_cost(pg)
    out["confirm"] = conf
    out["checks"]["tail_cost_click_opens_confirm"] = clicked and "確認送禮" in (conf.get("h3") or "")
    out["checks"]["confirm_names_perfume"] = "淡香水試用裝" in (conf.get("body") or "")
    shot(pg, f"woman_confirm_{W}x{H}.png")
    sent, res = send_and_result(pg)
    out["result"] = res
    out["checks"]["send_click"] = sent
    out["checks"]["result_modal_shown"] = bool(res.get("visible"))
    out["checks"]["result_plus1"] = "好感 +1" in (res.get("body") or "")
    out["rel_after"] = P.rel_of(pg, "hiu")
    out["checks"]["rel_0_to_1"] = out["rel_after"] == 1
    shot(pg, f"woman_result_{W}x{H}.png")
    return out

def case_star(pg, W, H):
    """星選擇器：搵 ENC79 候選星 → 播完對話 → 送禮掣 → 選擇器；700 驗 B1＋C1，932 驗對照。"""
    out = {"checks": {}}
    out["checks"]["new_game_to_map"] = P.new_game_to_map(pg)
    cands = P.find_star_candidates()
    out["candidates"] = cands[:3]
    out["checks"]["found_star_candidates"] = len(cands) > 0
    if not cands:
        return out
    found, info = None, None
    for c in cands:
        day, loc, star = c["day"], c["loc"], c["star"]
        P.seed_day(pg, day)
        way = P.enter_loc(pg, loc)
        if not way:
            return {**out, "checks": {**out["checks"], "enter_loc_ui_works": False}}
        pg.wait_for_timeout(1500)
        info_try = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return {visible:false};
          const r = ov.getBoundingClientRect();
          if (r.width <= 0 || r.height <= 0) return {visible:false};
          return {visible:true, name: (ov.querySelector('.e79-name')||{}).textContent || '',
                  btns: [...ov.querySelectorAll('.e79-row button')].map(b => (b.textContent||'').trim()).filter(Boolean)};
        }""")
        mi_try = P.modal_info(pg)
        if info_try.get("visible"):
            found, info = c, info_try
            break
        if mi_try.get("visible"):
            P.dismiss_once(pg)
            pg.wait_for_timeout(800)
        if P.sheet_visible(pg):
            P.back_to_map(pg)
        elif not P.map_ready(pg):
            P.dismiss_once(pg)
            pg.wait_for_timeout(800)
            P.back_to_map(pg)
    out["found"] = found
    out["checks"]["star_overlay_shown"] = bool(found and info.get("visible"))
    if not found:
        return out
    out["star"] = found["star"]
    # 播完 ENC79 對話到出「送禮畀」掣（以 .e79-line 有文字為準先行）
    gift_btn = None
    steps = 0
    t0 = time.time()
    while time.time() - t0 < 12:
        info2 = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return {visible:false};
          const r = ov.getBoundingClientRect();
          if (r.width <= 0 || r.height <= 0) return {visible:false};
          const line = (ov.querySelector('.e79-line')||{}).textContent || '';
          return {visible:true, line: line.slice(0, 80),
                  btns: [...ov.querySelectorAll('.e79-row button')].map(b => (b.textContent||'').trim()).filter(Boolean)};
        }""")
        if not info2.get("visible"):
            break
        out["e79_line_sample"] = info2.get("line")
        if any(b.startswith("送禮畀") for b in info2.get("btns") or []):
            gift_btn = [b for b in info2["btns"] if b.startswith("送禮畀")][0]
            break
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
    out["e79_steps"] = steps
    out["checks"]["gift_btn_at_last_step"] = bool(gift_btn)
    out["checks"]["e79_line_has_text"] = bool(out.get("e79_line_sample"))
    if not gift_btn:
        return out
    out["checks"]["click_star_gift_btn"] = P.click_vis_btn(pg, gift_btn, "#enc79-overlay")
    pg.wait_for_timeout(1000)
    pick = P.wait_modal(pg, 4)
    out["checks"]["gift_pick_shown"] = bool(pick.get("visible"))
    if not pick.get("visible"):
        return out
    g = pick_geom(pg)
    out["geom"] = g
    out["checks"]["ten_rows"] = g["nRows"] == 10
    out["checks"]["c1_all_names_one_line"] = g["allNamesOneLine"]
    shot(pg, f"star_pick_{W}x{H}.png")
    if H == 700:
        out["checks"]["all_rows_hit"] = g["allHit"]
        out["checks"]["tail_all_hit"] = g["tailAllHit"]
        out["checks"]["b1_tail_bottom_le_btn_top"] = g["tailBottomLeBtnTop"]
    else:
        out["checks"]["932_inner_scrollable"] = bool(g["innerScroll"]) and g["innerScroll"]["scrollH"] > g["innerScroll"]["clientH"]
        out["scroll932"] = scroll_inner_bottom(pg)
        pg.wait_for_timeout(300)
        g2 = pick_geom(pg)
        out["geom_scrolled"] = g2
        out["checks"]["932_tail_all_hit_after_scroll"] = g2["tailAllHit"]
        out["checks"]["932_tail_bottom_le_btn_top_after_scroll"] = g2["tailBottomLeBtnTop"]
        shot(pg, f"star_pick_scrolled_{W}x{H}.png")
    clicked, conf = click_tail_cost(pg)
    out["confirm"] = conf
    out["checks"]["tail_cost_click_opens_confirm"] = clicked and "確認送禮" in (conf.get("h3") or "")
    shot(pg, f"star_confirm_{W}x{H}.png")
    sent, res = send_and_result(pg)
    out["result"] = res
    out["checks"]["send_click"] = sent
    out["checks"]["result_modal_shown"] = bool(res.get("visible"))
    import re as _re
    out["checks"]["result_has_delta"] = bool(_re.search(r"好感 [+-]\d", res.get("body") or ""))
    out["checks"]["result_is_minus1_dislike"] = "好感 -1" in (res.get("body") or "")  # 淡香水對廖炳星係 dislike，-1 先啱
    shot(pg, f"star_result_{W}x{H}.png")
    return out

CASES = {
    "woman_700": (case_woman, 430, 700),
    "woman_932": (case_woman, 430, 932),
    "star_700": (case_star, 430, 700),
    "star_932": (case_star, 430, 932),
}

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    results = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=P.EXE)
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
                print(f"== {name}: {out['verdict']} ({sum(1 for v in ch.values() if v)}/{len(ch)} checks, {len(errs)} pageerrors)", flush=True)
                for k, v in ch.items():
                    if not v:
                        print(f"   FAIL check: {k}", flush=True)
                ctx.close()
            b.close()
    finally:
        srv.terminate()
    with open(os.path.join(HERE, "drive185.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v["verdict"] for k, v in results.items()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
