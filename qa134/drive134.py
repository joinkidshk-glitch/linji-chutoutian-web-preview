#!/usr/bin/env python3
"""v134 WF4 灰底 drive v2：每單獨立 fresh session（新 game → seed → 過一日 → 呈現 → 量度 → 截圖）。
v1 教訓：多單同一 session 串行會喺事件之間嘅過場卡住（set08/st04 FATAL）；量度只認
DLG106 舞台（.sp-bg-layer／.dlg106-plate），認唔到卡片版式（.wf4-scene105 banner），
st06 明明有街市場景圖都被判 bgOk=False。v2 每單 fresh context＋雙版式量度。
流程照抄已驗證嘅 probe134.py（新 game → slot 3 → 跳過教學 → wait_on_map → seed →
過一日 → 確認 modal 明確撳「確定過一日」→ 其餘 modal dismiss_once）。
用法：python3 qa134/drive134.py <W> <H> [ROOT] [ev1,ev2,...]
  預設 ROOT＝work copy ~/workspace/linji-work134；
  預設事件＝day02,home01,st06,set08,st04,st05（每組一單；st05 負面對照：刻意留灰，預期無場景圖）。
  對照（pristine）：傳 ROOT＝resident clone ~/workspace/linji-repo，預期 bg＝漸變／無圖（FAIL）。"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

PORT = 8967
W = int(sys.argv[1]); H = int(sys.argv[2]) if len(sys.argv) > 2 else 700
ROOT = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser("~/workspace/linji-work134")
EVS = sys.argv[4].split(",") if len(sys.argv) > 4 else ["wf4_ev_day02", "wf4_ev_home01", "wf4_ev_st06", "wf4_ev_set08", "wf4_ev_st04", "wf4_ev_st05"]
TITLES = {
    "wf4_ev_day02": "傳呼台", "wf4_ev_home01": "阿媽煲老火湯",
    "wf4_ev_st06": "魚檔阿姐", "wf4_ev_set08": "派錯更去錯廠",
    "wf4_ev_st04": "最後一杯紅豆冰", "wf4_ev_st05": "K房霸咪",
}
EXPECT_BG = {  # 預期底圖檔案（st05 刻意留灰 → 預期無場景圖）
    "wf4_ev_day02": "bg_wf4_booth", "wf4_ev_home01": "bg_wf4_home",
    "wf4_ev_st06": "bg_wf4_market", "wf4_ev_set08": "bg_loc_film_lion",
    "wf4_ev_st04": "bg_loc_cafe_cha", "wf4_ev_st05": None,
}
QA = os.path.expanduser("~/workspace/linji-work134/qa134")
os.makedirs(QA + "/shots", exist_ok=True)
OUT = f"{QA}/measure134_{W}x{H}.json"

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

def modal_h3(pg):
    return pg.evaluate("() => { const h = document.querySelector('#modal h3'); return h ? h.textContent : ''; }")

def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            btn.click(timeout=1000)
            return True
    except Exception:
        pass
    return False

def wait_on_map(pg, secs=60):
    for _ in range(int(secs / 0.7)):
        if vis_btn(pg, "過一日"):
            return True
        if not dismiss_once(pg):
            if not click_vis_btn(pg, "返回地圖"):
                pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    return False

def measure(pg):
    """雙版式量度：stage（DLG106：.sp-bg-layer＋.dlg106-plate）／card-img（.wf4-scene105 banner）
    ／card-grey（無場景圖，st05 對照）。"""
    return pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), bottom:Math.round(b.bottom)}; };
      const stageBg = q('#modal .sp-bg-layer');
      const cardBg = q('#modal .wf4-scene105');
      const plate = q('#modal .dlg106-plate');
      const line = plate ? plate.querySelector('.sp-line') : null;
      const inner = q('#modal-inner');
      const bgEl = stageBg || cardBg;
      const bgImg = bgEl ? getComputedStyle(bgEl).backgroundImage : '';
      const layout = plate ? 'stage' : (cardBg ? 'card-img' : 'card-grey');
      const pr = r(plate), lr = r(line);
      return {
        layout,
        bgImage: bgImg.slice(0, 160),
        hasBgUrl: bgImg.indexOf('url(') === 0,
        bgIsGradientOnly: bgImg.indexOf('linear-gradient') !== -1 && bgImg.indexOf('url(') === -1,
        plate: pr, line: lr,
        plateClip: (lr && pr) ? Math.round(lr.bottom - pr.bottom) : null,
        innerScrollH: inner ? inner.scrollHeight : null,
        innerClientH: inner ? inner.clientHeight : null,
        dvh: window.innerHeight,
      };
    }""")

def new_game_to_map(pg):
    """新 game → slot 3 → 跳過教學 → 地圖（照 probe134.py 驗證過嘅流程）。"""
    pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1")
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
    return wait_on_map(pg)

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
results = {}
failed_reqs = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell")
        for ev in EVS:
            title = TITLES[ev]
            ctx = b.new_context(viewport={"width": W, "height": H})
            pg = ctx.new_page()
            pg.on("requestfailed", lambda req: failed_reqs.append(req.url))
            pg.on("response", lambda resp: failed_reqs.append(resp.url) if resp.status >= 400 else None)
            m = {"found": False, "expect": EXPECT_BG[ev], "bgOk": False, "plateOk": False}
            if not new_game_to_map(pg):
                print(ev, "FATAL: 未到地圖"); results[ev] = m; ctx.close(); continue
            # 確保過一日可見（可能要先撳開始今日行程）
            for _ in range(30):
                if vis_btn(pg, "過一日"):
                    break
                if click_vis_btn(pg, "開始今日行程"):
                    pg.wait_for_timeout(1000)
                    continue
                if not dismiss_once(pg):
                    if not click_vis_btn(pg, "返回地圖"):
                        pg.wait_for_timeout(500)
                pg.wait_for_timeout(700)
            pg.evaluate("""(ev) => {
                if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
                S.wf4.pending = ev; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
            }""", ev)
            click_vis_btn(pg, "過一日")
            found = False
            for _ in range(45):
                pg.wait_for_timeout(1000)
                h3 = modal_h3(pg)
                if title in h3:
                    found = True
                    break
                # 過一日二次確認：明確撳「確定過一日」（probe134 驗證過）
                if h3 == "確認過一日？":
                    if click_vis_btn(pg, "確定過一日"):
                        continue
                dismiss_once(pg)
            pg.wait_for_timeout(800)
            if found:
                m = measure(pg)
            m["found"] = found
            m["expect"] = EXPECT_BG[ev]
            if EXPECT_BG[ev]:
                m["bgOk"] = bool(found and m.get("hasBgUrl") and EXPECT_BG[ev] in (m.get("bgImage") or ""))
            else:
                # st05 對照：刻意留灰 → 預期無場景圖（card-grey，無 url）
                m["bgOk"] = bool(found and m.get("layout") == "card-grey" and not m.get("hasBgUrl"))
            no_scroll = (m.get("innerScrollH") is not None and m.get("innerClientH") is not None
                         and m["innerScrollH"] <= m["innerClientH"] + 1)
            if m.get("layout") == "stage":
                m["plateOk"] = bool(found and m.get("plateClip") is not None and m["plateClip"] <= 0 and no_scroll)
            else:
                m["plateOk"] = bool(found and no_scroll)
            results[ev] = m
            print(ev, "found:", found, "layout:", m.get("layout"), "bgOk:", m["bgOk"], "plateOk:", m["plateOk"],
                  "bg:", (m.get("bgImage") or "")[:80], "plateClip:", m.get("plateClip"))
            pg.screenshot(path=f"{QA}/shots/wf4_134_{ev}_{W}x{H}.png")
            ctx.close()
        b.close()
finally:
    srv.terminate()
results["_failedRequests"] = [u for u in failed_reqs if "bg_wf4" in u or "bg_loc" in u]
json.dump(results, open(OUT, "w"), ensure_ascii=False, indent=1)
npass = sum(1 for ev in EVS if results[ev]["bgOk"] and results[ev]["plateOk"])
print(f"TOTAL {npass}/{len(EVS)} 事件 bg＋plate 雙 PASS；failed scene requests: {results['_failedRequests']}")
print("done", OUT)
sys.exit(0 if npass == len(EVS) and not results["_failedRequests"] else 1)
