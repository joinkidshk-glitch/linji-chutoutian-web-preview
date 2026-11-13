#!/usr/bin/env python3
"""v20a170 Phase 2 實駕：新舞台-only 底圖（FLOOR 155→193）。
重用 v168 drive 機制（force won／gallery、逐 beat 截圖、0 pageerror），加腳底量度：
  - drawImage hook（window.__figDraws）：逐幀記錄人物 draw（dh 48／50／64），腳底 canvas y＝dy+dh
    （燕尾服：dy+dh*115/128，人物腳喺原圖 y115）；bg（240）同彩紙（fillRect）唔計。
  - 每 beat 歸屬：按 poll 當刻 seg（caption＋walkOn／glamOn 判 beat；pan 用「觀禮席」認）。
  - 顯示換算：canvas content rect（扣 border）＋scale＝clientWidth/424；舞台頂顯示 y＝contentTop＋193*scale。
    193 呢個錨獨立核實過：PIL 行掃描最終 424×240——中央帶幕布底 y191–193 過渡、y194 滿亮平台面，
    FLOOR＝194−1＝193。截圖存 shots_p2（唔覆蓋 Phase 1 嗰批），結果存 drive170_p2.json。
用法：/home/hatch/pwenv49/bin/python qa170/drive170.py [won_932|won_700|gallery_932|all]
Mirror：工作副本本身（~/workspace/linji-work170），port 8991，?softPreview=1。
"""
import json, os, subprocess, sys, time
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v168")
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v160")
import drive168r as D168
import drive160r as D

HERE = "/home/hatch/workspace/linji-work170/qa170"
ROOT = "/home/hatch/workspace/linji-work170"
SHOTS = os.path.join(HERE, "shots_p2")
PORT = 8991
os.makedirs(SHOTS, exist_ok=True)
D168.ROOT = ROOT; D168.SHOTS = SHOTS; D168.PORT = PORT
D.ROOT = ROOT; D.SHOTS = SHOTS; D.PORT = PORT

def shot(pg, name):
    for i in range(3):
        try:
            pg.screenshot(path=os.path.join(SHOTS, name))
            return True
        except Exception:
            if i == 2: return False
            time.sleep(1.0)

def install_fig_patch(pg):
    return pg.evaluate("""() => {
      window.__figDraws = [];
      if (!window.__figPatched) {
        window.__figPatched = true;
        const _di = CanvasRenderingContext2D.prototype.drawImage;
        CanvasRenderingContext2D.prototype.drawImage = function(img, ...rest) {
          try {
            const dh = rest[3], dw = rest[2];
            if (typeof dh === 'number' && (dh === 48 || dh === 50 || dh === 64) && dw < 70) {
              const s = img && img.src ? String(img.src) : '';
              window.__figDraws.push({t: performance.now(), dx: rest[0], dy: rest[1], dw, dh,
                tux: s.indexOf('awei_tuxedo') >= 0});
              if (window.__figDraws.length > 8000) window.__figDraws.splice(0, 4000);
            }
          } catch(e) {}
          return _di.apply(this, [img, ...rest]);
        };
      }
      return { patched: true };
    }""")

def canvas_geo(pg):
    return pg.evaluate("""() => {
      const cv = document.querySelector('.awd62-stage canvas');
      if (!cv) return null;
      const r = cv.getBoundingClientRect(), cs = getComputedStyle(cv);
      const bt = parseFloat(cs.borderTopWidth) || 0, bl = parseFloat(cs.borderLeftWidth) || 0;
      return { left: r.left + bl, top: r.top + bt, w: cv.clientWidth, h: cv.clientHeight,
               scale: cv.clientWidth / 424 };
    }""")

def seg_of(st):
    if st.get("walkOn"): return "walkup"
    if st.get("glamOn"): return "glamour"
    cap = st.get("caption") or ""
    if "拍拍你膊頭" in cap: return "comfort"
    if "掌聲響起" in cap: return "out"
    if "得獎者是" in cap: return "suspense"
    if "得獎" in cap: return "reveal"  # won「🏆 得獎！」／gallery「🏆 廖炳星憑《…》得獎」；suspense 已先認
    if "入圍名單" in cap: return "names"
    if "魚貫入場" in cap: return "enter"
    if "觀禮席" in cap: return "pan"
    if cap.strip().startswith("——"): return "open"
    return "?"

def watch(pg, prefix, exp_beats, secs=25):
    timeline, beats_seen, seg_states, feet = [], [], {}, {}
    cur_seg, seg_start = None, None
    consumed = 0
    geo = None
    seg_geo = {}
    t0 = time.time()
    while time.time() - t0 < secs:
        st = D168.stage_state168(pg)
        if not st.get("present"):
            break
        if geo is None:
            geo = canvas_geo(pg)
        seg = seg_of(st)
        now = round((time.time() - t0) * 1000)
        if seg != cur_seg:
            if cur_seg is not None:
                beats_seen.append({"id": cur_seg, "durMs": now - seg_start})
            cur_seg, seg_start = seg, now
            seg_states[seg] = st
            seg_geo[seg] = canvas_geo(pg)
            shot(pg, f"{prefix}_beat_{seg}.png")
        seg = seg_of(st)
        now = round((time.time() - t0) * 1000)
        if seg != cur_seg:
            if cur_seg is not None:
                beats_seen.append({"id": cur_seg, "durMs": now - seg_start})
            cur_seg, seg_start = seg, now
            seg_states[seg] = st
            shot(pg, f"{prefix}_beat_{seg}.png")
        # 新 fig draws 歸入當刻 seg
        draws = pg.evaluate("() => (window.__figDraws || []).slice(%d)" % consumed)
        consumed += len(draws)
        for d in draws:
            foot = d["dy"] + d["dh"] * 115 / 128 if d["tux"] else d["dy"] + d["dh"]
            cx = d["dx"] + d["dw"] / 2
            feet.setdefault(seg, []).append({"foot": round(foot, 1), "cx": round(cx, 1),
                                             "dh": d["dh"], "tux": d["tux"]})
        pg.wait_for_timeout(150)
    if cur_seg is not None:
        beats_seen.append({"id": cur_seg, "durMs": round((time.time() - t0) * 1000) - seg_start})
    return {"beats": beats_seen, "segStates": seg_states, "feet": feet,
            "totalMs": round((time.time() - t0) * 1000), "stageGone": not D168.stage_state168(pg).get("present"),
            "canvasGeo": geo, "segGeo": seg_geo}

def foot_stats(samples):
    if not samples: return None
    fs = sorted(s["foot"] for s in samples)
    cxs = sorted(set(s["cx"] for s in samples))
    return {"n": len(samples), "foot_min": fs[0], "foot_med": fs[len(fs)//2], "foot_max": fs[-1],
            "cx": cxs, "tux_n": sum(1 for s in samples if s["tux"])}

def force_nominated(pg):
    """force 一個 nominated（入圍落選）pack：逐次重骰，唔係就推辭再嚟。"""
    for attempt in range(1, 9):
        pack = pg.evaluate("""(o) => {
          try {
            const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
            if (!p) return { error: 'no pack' };
            return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome,
                     tier: p.tier, repGigId63: p.repGigId63 || '',
                     categories: (p.categories || []).map(c => ({ outcome: c.outcome, label: c.label, score: (c.score != null ? +c.score.toFixed(3) : null) })) };
          } catch(e) { return { error: String(e) }; }
        }""", {"id": "award_harbour_film", "tier": "nominee"})
        if pack.get("error"):
            return {"pack": pack, "attempts": attempt, "invite": D.modal_info(pg)}
        if pack.get("bestOutcome") == "nominated":
            pg.evaluate("() => { try { window.__awards.present(); } catch(e) {} }")
            pg.wait_for_timeout(1000)
            return {"pack": pack, "attempts": attempt, "invite": D.modal_info(pg)}
        D.click_vis_btn(pg, "推辭")
        pg.wait_for_timeout(400)
    return {"pack": pack, "attempts": 8, "invite": D.modal_info(pg), "note": "never nominated"}

def run_case(pw, name, height, kind):
    from playwright.sync_api import sync_playwright as _sp  # noqa
    out = {"case": name, "checks": {}, "errors": []}
    errs = []
    pg = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"]).new_page(viewport={"width": 430, "height": height})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    pg.on("response", lambda r: errs.append(f"http{r.status}: {r.url}") if r.status >= 400 else None)
    try:
        assert D.new_game_to_map(pg), "去唔到地圖"
        D.install_draw_patch(pg)
        install_fig_patch(pg)
        day = D.day_index(1991, 10, 20)
        if kind == "won":
            D.seed_won_poster(pg, day)
            fa = D.force_award(pg, "award_harbour_film", "nominee", want_won=True)
            assert fa["pack"].get("bestOutcome") == "won", "重骰都唔贏：%s" % fa["pack"]
        elif kind == "nominated":
            D.seed_won_poster(pg, day)
            fa = force_nominated(pg)
            assert fa["pack"].get("bestOutcome") == "nominated", "重骰都唔係 nominated：%s" % fa["pack"]
        else:
            D.seed_plain(pg, day)
            fa = D.force_award(pg, "award_harbour_film", "gallery", want_won=False)
            assert fa["pack"].get("bestOutcome") == "gallery", "pack 唔係 gallery：%s" % fa["pack"]
        out["pack"] = fa["pack"]
        shot(pg, f"{name}_invite.png")
        out["expected_beats"] = D.expected_beats(pg, fa["pack"])
        assert D.attend(pg), "請柬出席撳唔到"
        w = watch(pg, name, out["expected_beats"], 25)
        out["watch"] = w
        # 幾何用 names 段嗰個（卡列出齊、frame 定咗形；open／glamour 段 frame 高唔同，canvas 頂會郁）
        geo = (w.get("segGeo") or {}).get("names") or (w.get("segGeo") or {}).get("reveal") or w.get("canvasGeo")
        out["canvasGeo"] = geo
        out["segGeo"] = w.get("segGeo")
        # 腳底統計（每 beat）
        stats = {seg: foot_stats(s) for seg, s in w["feet"].items()}
        out["footStats"] = stats
        if geo:
            # 舞台頂顯示 y＝實測 canvas content 頂＋193*scale；193 呢個錨獨立由 PIL 行掃描核實
            # （最終 424×240：中央帶幕布底 y191–193 過渡、y194 滿亮平台面）。
            out["stageTopDisplay"] = round(geo["top"] + 193 * geo["scale"], 1)
        pg.wait_for_timeout(600)
        res = D.modal_info(pg)
        out["result_card"] = res
        shot(pg, f"{name}_result.png")
        c = out["checks"]
        seen = set(b["id"] for b in w["beats"])
        exp_ids = set(b.get("id") for b in (out["expected_beats"] or []) if isinstance(b, dict))
        if kind == "won":
            c["beats_all_seen"] = seen >= {"open", "enter", "names", "suspense", "reveal", "walkup", "glamour"}
            c["walkup_gif_on"] = bool((w["segStates"].get("walkup") or {}).get("walkOn"))
            _wi = (w["segStates"].get("walkup") or {}).get("walkImg") or {}
            c["walkup_img_complete"] = bool(_wi.get("complete"))
            c["glamour_tux_drawn"] = (stats.get("glamour") or {}).get("tux_n", 0) > 0
        elif kind == "nominated":
            c["beats_all_seen"] = seen >= {"open", "enter", "names", "suspense", "reveal", "comfort"}
            c["walkup_absent"] = "walkup" not in seen
            c["glamour_absent"] = "glamour" not in seen
        else:
            c["beats_all_seen"] = seen >= {"open", "pan", "names", "suspense", "reveal"}
            c["walkup_absent"] = "walkup" not in seen
            c["glamour_absent"] = "glamour" not in seen
        # 腳底＝193（reveal 行前 200±2，bob -1 容差）；只驗呢個 case 預期有嘅 beat
        for seg, exp in (("pan", 193), ("enter", 193), ("names", 193), ("suspense", 193),
                         ("comfort", 193), ("glamour", 193)):
            if seg not in exp_ids:
                continue
            s = stats.get(seg)
            if seg == "comfort":
                # comfort 緊接 reveal：第一個 poll 會滲入 reveal 尾幀（得主行前腳 200／x≈120），
                # 所以只驗 median＋min（193），唔驗 max
                c[f"foot_{seg}_193"] = bool(s) and abs(s["foot_med"] - exp) <= 1 and s["foot_min"] >= exp - 2
            else:
                c[f"foot_{seg}_193"] = bool(s) and abs(s["foot_med"] - exp) <= 1 and s["foot_min"] >= exp - 2 and s["foot_max"] <= exp + 2
        s = stats.get("reveal")
        # reveal：多數係企定 fellows（193），得主行前腳 200（＋7，燕尾服 200.5 係 Math.round 頂位 +0.5）——用 max 驗行前
        c["foot_reveal_200"] = bool(s) and 199 <= s["foot_max"] <= 201.5 and s["foot_min"] >= 192
        # slot x：4 slots 94／166／238／310；gallery 3 slots 130／202／274（±3）
        ns = stats.get("names") or {}
        cxs = ns.get("cx") or []
        exp_cx = [130, 202, 274] if kind == "gallery" else [94, 166, 238, 310]
        c["slot_cx"] = len(cxs) == len(exp_cx) and all(abs(a - b) <= 3 for a, b in zip(cxs, exp_cx))
        out["slotCxMeasured"] = cxs
        # 顯示 y：腳底顯示值對舞台頂顯示值 ±3（舞台頂錨＝PIL 量度 y194）
        if geo and stats.get("names"):
            foot_disp = round(geo["top"] + stats["names"]["foot_med"] * geo["scale"], 1)
            out["footDisplayNames"] = foot_disp
            c["foot_display_on_stage_top"] = abs(foot_disp - out["stageTopDisplay"]) <= 3
        c["result_shown"] = bool(res.get("visible"))
        c["stage_gone_after"] = bool(w.get("stageGone"))
        out["pass"] = all(c.values())
    except Exception as e:
        out["pass"] = False
        out["error"] = str(e)
    finally:
        out["pageerrors"] = errs
        out["checks"]["zero_pageerror"] = len(errs) == 0
        out["pass"] = out.get("pass", False) and len(errs) == 0
        try: pg.close()
        except Exception: pass
    return out

def main():
    from playwright.sync_api import sync_playwright
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        D.check_served()
        results = {}
        with sync_playwright() as pw:
            if which in ("all", "won_932"):
                results["won_932"] = run_case(pw, "won_932", 932, "won")
            if which in ("all", "won_700"):
                results["won_700"] = run_case(pw, "won_700", 700, "won")
            if which in ("all", "gallery_932"):
                results["gallery_932"] = run_case(pw, "gallery_932", 932, "gallery")
            if which in ("all", "nominated_932"):
                results["nominated_932"] = run_case(pw, "nominated_932", 932, "nominated")
        json.dump(results, open(os.path.join(HERE, "drive170_p2.json"), "w"), ensure_ascii=False, indent=1)
        for name, r in results.items():
            print(f"{name}: {'PASS' if r.get('pass') else 'FAIL'} pageerrors={len(r.get('pageerrors', []))}")
            print(f"  checks={json.dumps(r.get('checks'), ensure_ascii=False)}")
            print(f"  canvasGeo={r.get('canvasGeo')} stageTopDisplay={r.get('stageTopDisplay')} footDisplayNames={r.get('footDisplayNames')}")
            print(f"  footStats={json.dumps(r.get('footStats'), ensure_ascii=False)}")
            print(f"  slotCx={r.get('slotCxMeasured')} beats={[(b['id'], b['durMs']) for b in (r.get('watch') or {}).get('beats', [])]}")
            if r.get("error"): print("  ERROR:", r["error"])
        ok = all(r.get("pass") for r in results.values())
        print("OVERALL", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    finally:
        D.stop_server(srv)

if __name__ == "__main__":
    sys.exit(main())
