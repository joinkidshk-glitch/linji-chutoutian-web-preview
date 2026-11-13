#!/usr/bin/env python3
"""v20a174 rebase 實駕補驗：M5 彩紙 GIF（v149 B1）喺合併後 636×540 backing 下，
reveal／comfort／out 期間顯示（.awd62-m5fx149.on＝2 張），其餘 beats 收起（0 張）。
用法：/home/hatch/pwenv49/bin/python qa174/probe_m5.py
（won case：reveal＋out；nominated case：reveal＋comfort＋out）"""
import json, os, subprocess, sys, time
sys.path.insert(0, "/home/hatch/workspace/linji-work170/qa170")
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v168")
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v160")
import drive170_p2 as W
import drive168r as D168
import drive160r as D

HERE = "/home/hatch/workspace/linji-work174/qa174"
ROOT = "/home/hatch/workspace/linji-work174"
PORT = 8995
D168.ROOT = ROOT; D168.PORT = PORT
D.ROOT = ROOT; D.PORT = PORT
W.PORT = PORT

def m5_state(pg):
    return pg.evaluate("""() => {
      const imgs = Array.prototype.slice.call(document.querySelectorAll('.awd62-m5fx149'));
      if (!imgs.length) return {n: 0};
      const cs = getComputedStyle(imgs[0]);
      return {n: imgs.length, on: imgs.filter(i => i.classList.contains('on')).length,
              display: cs.display, vis: cs.visibility, op: cs.opacity,
              complete: imgs.map(i => i.complete), nw: imgs.map(i => i.naturalWidth),
              srcs: imgs.map(i => (i.src || '').split('/').slice(-1)[0])};
    }""")

def run_case(pw, name, kind):
    pg = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"]).new_page(viewport={"width": 430, "height": 932})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    try:
        assert D.new_game_to_map(pg), "去唔到地圖"
        day = D.day_index(1991, 10, 20)
        D.seed_won_poster(pg, day)
        if kind == "won":
            fa = D.force_award(pg, "award_harbour_film", "nominee", want_won=True)
            assert fa["pack"].get("bestOutcome") == "won"
        else:
            fa = W.force_nominated(pg)
            assert fa["pack"].get("bestOutcome") == "nominated"
        assert D.attend(pg), "請柬出席撳唔到"
        samples = []
        t0 = time.time()
        while time.time() - t0 < 25:
            st = D168.stage_state168(pg)
            if not st.get("present"):
                break
            seg = W.seg_of(st)
            samples.append({"t": round((time.time() - t0) * 1000), "seg": seg, "m5": m5_state(pg)})
            pg.wait_for_timeout(100)
        by_seg = {}
        for s in samples:
            by_seg.setdefault(s["seg"], []).append(s["m5"].get("on"))
        ok = True
        detail = {}
        for seg, ons in by_seg.items():
            if seg in ("reveal", "comfort", "?"):  # '?'＝out beat（seg_of 未識別 out）
                good = all(o == 2 for o in ons)
                detail[seg] = {"n": len(ons), "all_on_2": good, "min": min(ons), "max": max(ons)}
            else:
                good = all(o == 0 for o in ons)
                detail[seg] = {"n": len(ons), "all_off_0": good, "min": min(ons), "max": max(ons)}
            ok = ok and good
        first = samples[0]["m5"] if samples else {}
        gif_ok = first.get("n") == 2 and all(first.get("complete") or []) and all((w or 0) > 0 for w in (first.get("nw") or []))
        return {"case": name, "pass": bool(ok and gif_ok and not errs), "pageerrors": errs,
                "gif": first, "bySeg": detail, "nSamples": len(samples)}
    finally:
        try: pg.close()
        except Exception: pass

def main():
    from playwright.sync_api import sync_playwright
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        D.check_served()
        results = {}
        with sync_playwright() as pw:
            results["won"] = run_case(pw, "won", "won")
            results["nominated"] = run_case(pw, "nominated", "nominated")
        json.dump(results, open(os.path.join(HERE, "probe_m5.json"), "w"), ensure_ascii=False, indent=1)
        for name, r in results.items():
            print(f"{name}: {'PASS' if r.get('pass') else 'FAIL'} pageerrors={len(r.get('pageerrors', []))}")
            print(f"  gif={json.dumps(r.get('gif'), ensure_ascii=False)}")
            print(f"  bySeg={json.dumps(r.get('bySeg'), ensure_ascii=False)}")
        print("OVERALL", "PASS" if all(r.get("pass") for r in results.values()) else "FAIL")
        return 0 if all(r.get("pass") for r in results.values()) else 1
    finally:
        D.stop_server(srv)

if __name__ == "__main__":
    sys.exit(main())
