# -*- coding: utf-8 -*-
"""v20a133 回歸 drive：WF4 隨機事件對話框喺真機短 viewport 被切（v128 回歸）。
修法：#mask.wf4-stage-on .sp-stage min-height:480px → min-height:min(480px,52dvh)（viewport-aware）。
斷言（每 viewport）：A stage.bottom ≤ storyPlay.bottom（舞台唔俾 story-play 剪）
B line.bottom ≤ plate.bottom（行文完整喺對話框入面）
C plate.bottom ≤ inner 可見底（對話框唔俾 modal-inner 剪）
D inner.scrollHeight ≤ inner.clientHeight（唔使捲都見晒）。
短 viewport 430×700／726（用戶實機 dvh）／780 係主戰場，430×932 做對照。
用法：/home/hatch/pwenv49/bin/python qa133/drive133.py [700|726|780|932|all]
ROOT 預設工作副本；設 LINJI133_ROOT 可指去 pristine worktree 做反證。
"""
import json, subprocess, sys, time, os, signal
from playwright.sync_api import sync_playwright

ROOT = os.environ.get("LINJI133_ROOT", "/home/hatch/workspace/linji-work133")
HERE = "/home/hatch/workspace/linji-work133/qa133"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8967

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

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), bottom:Math.round(b.bottom)}; };
  const inner = q('#modal-inner'), sp = q('#modal .story-play'), stage = q('#modal .sp-stage');
  const plate = q('#modal .dlg106-plate'), line = q('#modal .dlg106-plate .sp-line');
  const m = {
    h3: r(q('#modal h3')), sub: r(q('#modal .sub')),
    storyPlay: r(sp), stage: r(stage), plate: r(plate), line: r(line),
    inner: r(inner), innerScrollH: inner ? inner.scrollHeight : null,
    innerClientH: inner ? inner.clientHeight : null, innerScrollTop: inner ? inner.scrollTop : null,
    modal: r(q('#modal')), btns: r(q('#modal-btns')), dvh: window.innerHeight
  };
  return m;
}"""

def run_case(b, W, H):
    # 每 case 全新 browser context（localStorage 乾淨），免 slot 3 存檔覆蓋確認卡住後續 case
    ctx = b.new_context(viewport={"width": W, "height": H})
    pg = ctx.new_page()
    try:
        return _run_case_inner(pg, W, H)
    finally:
        ctx.close()

def _run_case_inner(pg, W, H):
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
        if vis_btn(pg, "過一日"):
            break
        if not dismiss_once(pg):
            if not click_vis_btn(pg, "返回地圖"):
                pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    for d in range(3):
        if not click_vis_btn(pg, "過一日"):
            dbg = pg.evaluate("""() => ({h3: (document.querySelector('#modal h3')||{}).textContent || '',
              btns: [...document.querySelectorAll('#modal-btns button')].map(b=>b.textContent.trim()),
              visBtns: [...document.querySelectorAll('button')].filter(b=>{const r=b.getBoundingClientRect(); return r.width>0&&r.height>0;}).map(b=>b.textContent.trim()).slice(0,12)})""")
            print(f"  [{W}x{H}] day {d} no advance btn; dbg={json.dumps(dbg, ensure_ascii=False)}")
            pg.screenshot(path=os.path.join(SHOTS, f"dbg_{W}x{H}_day{d}.png"))
            return None
        for _ in range(40):
            if vis_btn(pg, "過一日"):
                break
            dismiss_once(pg)
            pg.wait_for_timeout(700)
    pg.evaluate("""() => {
        if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
        S.wf4.pending = 'wf4_ev_day02'; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
    }""")
    click_vis_btn(pg, "過一日")
    found = False
    for i in range(60):
        pg.wait_for_timeout(1000)
        if "傳呼台" in modal_h3(pg):
            found = True
            break
        dismiss_once(pg)
    if not found:
        print(f"  [{W}x{H}] WF4 事件未出現"); return None
    pg.wait_for_timeout(800)
    m = pg.evaluate(MEASURE_JS)
    shot = os.path.join(SHOTS, f"wf4_{W}x{H}.png")
    pg.screenshot(path=shot)
    # 斷言
    sp, st, pl, ln, inn = m["storyPlay"], m["stage"], m["plate"], m["line"], m["inner"]
    inner_vis_bottom = inn["y"] + m["innerClientH"] if inn and m["innerClientH"] else None
    checks = {
        "A_stage_le_storyPlay": (st["bottom"] <= sp["bottom"] + 1) if st and sp else False,
        "B_line_le_plate": (ln["bottom"] <= pl["bottom"] + 1) if ln and pl else False,
        "C_plate_le_innerVis": (pl["bottom"] <= inner_vis_bottom + 1) if pl and inner_vis_bottom else False,
        "D_inner_noScroll": (m["innerScrollH"] <= m["innerClientH"] + 1) if m["innerScrollH"] is not None else False,
    }
    plate_vis = min(pl["bottom"], sp["bottom"]) - pl["y"] if pl and sp else None
    m["checks"] = checks
    m["plateVisiblePx"] = plate_vis
    m["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    return m

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    cases = {"700": (430, 700), "726": (430, 726), "780": (430, 780), "932": (430, 932)}
    sel = list(cases.values()) if arg == "all" else [cases[arg]]
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    results = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=EXE)
            for (W, H) in sel:
                print(f"== case {W}x{H} (ROOT={ROOT})", flush=True)
                m = run_case(b, W, H)
                if m is None:
                    results[f"{W}x{H}"] = {"verdict": "ERROR", "checks": {}}
                    continue
                results[f"{W}x{H}"] = m
                sp, st, pl = m["storyPlay"], m["stage"], m["plate"]
                print(f"  dvh={m['dvh']} storyPlay h={sp['h']} stage h={st['h']} (bottom {st['bottom']} vs sp {sp['bottom']}) "
                      f"plate h={pl['h']} visible={m['plateVisiblePx']} line bottom={m['line']['bottom']} plate bottom={pl['bottom']} "
                      f"inner {m['innerScrollH']}/{m['innerClientH']} -> {m['verdict']} {m['checks']}", flush=True)
            b.close()
    finally:
        srv.terminate()
    out = os.path.join(HERE, "drive133.json")
    json.dump(results, open(out, "w"), ensure_ascii=False, indent=1)
    overall = all(v.get("verdict") == "PASS" for v in results.values())
    print("OVERALL " + ("PASS" if overall else "FAIL"), "|", out)
    sys.exit(0 if overall else 1)

if __name__ == "__main__":
    main()
