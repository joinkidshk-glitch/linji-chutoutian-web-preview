# -*- coding: utf-8 -*-
"""v20a135 實駕量度：地圖底部卡收細（開局第 1 日地圖主畫面）。
量度 #map-hint 卡高、.map-wrap／.map-img 高、地圖佔屏比例；驗「過一日」可見可撳、
出行剩餘數字可見；截圖對照。
用法：/home/hatch/pwenv49/bin/python qa135/drive135.py [932|700|all] [pre|post]
  ROOT 預設工作副本；LINJI135_ROOT 可指去 pristine worktree。
  輸出 qa135/drive135_<tag>.json ＋ qa135/shots/<tag>_<WxH>.png
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

ROOT = os.environ.get("LINJI135_ROOT", "/home/hatch/workspace/linji-work135")
HERE = "/home/hatch/workspace/linji-work135/qa135"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8968
TAG = sys.argv[2] if len(sys.argv) > 2 else "run"

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

def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            btn.click(timeout=1000)
            return True
    except Exception:
        pass
    return False

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), bottom:Math.round(b.bottom)}; };
  const hint = q('#map-hint');
  const endDay = [...document.querySelectorAll('#map-end-day, #map-start-today')].find(b => { const bb = b.getBoundingClientRect(); return bb.width > 0 && bb.height > 0; });
  return {
    dvh: window.innerHeight, dvw: window.innerWidth,
    hint: r(hint), hintText: hint ? hint.textContent.replace(/\\s+/g,' ').trim() : '',
    mapWrap: r(q('.map-wrap')), mapImg: r(q('.map-img')), mapStage: r(q('.map-stage')),
    polaroid: r(q('.map-polaroid')), mapWell: r(q('.map-well')),
    mapVisibleH: (()=>{ const im=q('.map-img'), pol=q('.map-polaroid'); if(!im||!pol) return null;
      // polaroid 有 overflow:hidden：可見圖高 = 圖 ∩ polaroid 框（再夾 viewport）
      const a=im.getBoundingClientRect(), b=pol.getBoundingClientRect();
      return Math.max(0, Math.round(Math.min(a.bottom,b.bottom,window.innerHeight)-Math.max(a.top,b.top,0))); })(),
    vmap: r(q('#v-map')),
    endDayBtn: r(endDay || null), endDayText: endDay ? endDay.textContent.trim() : null,
    hasShowAll: !!(hint && hint.querySelector('#map-show-all-locs')),
    hasStory: !!(hint && hint.querySelector('.map-hint-story')),
    hasHelp: !!(hint && hint.querySelector('.map-hint-help')),
    hasAud: !!(hint && hint.querySelector('.map-hint-aud108')),
    sheetOpen: !!((document.querySelector('.map-wrap')||{}).classList||{contains:()=>false}).contains('sheet-open'),
    locSheetOn: !!((document.querySelector('#loc-sheet')||{}).classList||{contains:()=>false}).contains('on'),
    pageErrors: window.__errs || []
  };
}"""

def run_case(b, W, H):
    ctx = b.new_context(viewport={"width": W, "height": H})
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: pg.evaluate("(m)=>{ (window.__errs=window.__errs||[]).push(String(m)); }", str(e)))
    try:
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
            sheet_open = pg.evaluate("() => { const w = document.querySelector('.map-wrap'); const s = document.querySelector('#loc-sheet'); return !!(w && w.classList.contains('sheet-open')) || !!(s && s.classList.contains('on')); }")
            if sheet_open:
                # 地點 sheet 開緊：#map-hint 會被壓成 2.8em 緊湊態，唔係正常卡高
                if not click_vis_btn(pg, "返回地圖"):
                    dismiss_once(pg)
                pg.wait_for_timeout(700)
                continue
            if vis_btn(pg, "過一日"):
                break
            if not dismiss_once(pg):
                pg.wait_for_timeout(500)
            pg.wait_for_timeout(700)
        pg.wait_for_timeout(800)
        m = pg.evaluate(MEASURE_JS)
        shot = os.path.join(SHOTS, f"{TAG}_{W}x{H}.png")
        pg.screenshot(path=shot)
        m["shot"] = shot
        hint_h = m["hint"]["h"] if m["hint"] else None
        wrap_h = m["mapWrap"]["h"] if m["mapWrap"] else None
        m["mapSharePct"] = round(100.0 * wrap_h / m["dvh"], 1) if wrap_h else None
        m["mapImgSharePct"] = round(100.0 * (m["mapVisibleH"] or 0) / m["dvh"], 1)
        m["checks"] = {
            "card_le_150": (hint_h is not None and hint_h <= 150),
            "endDay_visible": bool(m["endDayBtn"]),
            "travel_num_visible": ("仲可以去" in m["hintText"] or "出行額度已用完" in m["hintText"]),
            "no_show_all": not m["hasShowAll"],
            "no_story": not m["hasStory"],
            "no_help": not m["hasHelp"],
            "no_page_errors": not m["pageErrors"],
        }
        m["verdict"] = "PASS" if all(m["checks"].values()) else "FAIL"
        return m
    finally:
        ctx.close()

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    cases = {"700": (430, 700), "932": (430, 932)}
    sel = list(cases.values()) if arg == "all" else [cases[arg]]
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    results = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=EXE)
            for (W, H) in sel:
                print(f"== case {W}x{H} (ROOT={ROOT} tag={TAG})", flush=True)
                try:
                    m = run_case(b, W, H)
                except Exception as e:
                    print(f"  ERROR {e}", flush=True)
                    results[f"{W}x{H}"] = {"verdict": "ERROR", "error": str(e)}
                    continue
                results[f"{W}x{H}"] = m
                print(f"  hint h={m['hint']['h'] if m['hint'] else None} wrap h={m['mapWrap']['h'] if m['mapWrap'] else None} "
                      f"img h={m['mapImg']['h'] if m['mapImg'] else None} visible={m['mapVisibleH']} "
                      f"imgShare={m['mapImgSharePct']}% endDay={m['endDayText']} -> {m['verdict']} {m['checks']}", flush=True)
                print(f"  hintText={m['hintText']}", flush=True)
            b.close()
    finally:
        srv.terminate()
    out = os.path.join(HERE, f"drive135_{TAG}.json")
    json.dump(results, open(out, "w"), ensure_ascii=False, indent=1)
    overall = all(v.get("verdict") == "PASS" for v in results.values())
    print("OVERALL " + ("PASS" if overall else "FAIL"), "|", out)
    sys.exit(0 if overall else 1)

if __name__ == "__main__":
    main()
