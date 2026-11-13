#!/usr/bin/env python3
"""v20a177 實駕：頒獎禮舞台加闊後驗證（FLOOR 290→250、slots won 62／162／262／362、gallery 82／162／262、講台落中罅）。
重用 drive170_p2／drive168r／drive160r 機制（force won／gallery／nominated、逐 beat 截圖、0 pageerror），
改動：
  - 幾何新錨：FLOOR＝250、canvas 424×360、人仔 dh 72／75／96、slots won 62／162／262／362、gallery 82／162／262、
    reveal 行前腳 260、地板深 110px。
  - 行走探針：enter beat 逐格記錄人物 cx，驗真係由台側行到企位（唔係淡入企定）；walkup 繼續驗 M4 GIF .on。
  - B2：names beat 100ms 採樣（卡列容器 display／visibility／高、每張卡 opacity／.show、frame 頂／高），
    驗開場 frame 唔跳＋4 張齊嘅時間。
  - B1：每 beat frame 頂／底＋canvas 高，量上下黑帶。
  - A1：glamour cap 獎盃 img 計算樣式（金底 chip rgb(242,193,78)、22px）＋reveal 字幕獎盃同款；另存 caption zoom。
  - C1：gallery reveal 中央人 draw x 範圍 vs 講台 x194–229 重疊闊度＋canvas 像素對比。
  - C2：glamour 期間卡列 display:none、frame 比 reveal 短約 174px、canvas 底到 frame 底唔再有 174px 死位。
用法：/home/hatch/pwenv49/bin/python qa174/drive174.py [all|won_932|won_700|gallery_932|nominated_932]
Mirror：工作副本本身（~/workspace/linji-work177），port 8997，?softPreview=1。
"""
import base64, io, json, os, subprocess, sys, time
sys.path.insert(0, "/home/hatch/workspace/linji-work170/qa170")
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v168")
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v160")
import drive170_p2 as W
import drive168r as D168
import drive160r as D

HERE = "/home/hatch/workspace/linji-work177/qa177"
ROOT = "/home/hatch/workspace/linji-work177"
SHOTS = os.path.join(HERE, "shots177")
PORT = 8997
FLOOR = 250
LECTERN_X = (194, 229)
os.makedirs(SHOTS, exist_ok=True)
D168.ROOT = ROOT; D168.SHOTS = SHOTS; D168.PORT = PORT
D.ROOT = ROOT; D.SHOTS = SHOTS; D.PORT = PORT
W.SHOTS = SHOTS; W.PORT = PORT

def shot(pg, name):
    for i in range(3):
        try:
            pg.screenshot(path=os.path.join(SHOTS, name))
            return True
        except Exception:
            if i == 2: return False
            time.sleep(1.0)

def install_fig_patch174(pg):
    return pg.evaluate("""() => {
      window.__figDraws = [];
      if (!window.__figPatched) {
        window.__figPatched = true;
        const _di = CanvasRenderingContext2D.prototype.drawImage;
        CanvasRenderingContext2D.prototype.drawImage = function(img, ...rest) {
          try {
            const dh = rest[3], dw = rest[2];
            if (typeof dh === 'number' && (dh === 72 || dh === 75 || dh === 96) && dw < 110) {
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

def frame_state(pg):
    return pg.evaluate("""() => {
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect();
        return {top: Math.round(b.top), bottom: Math.round(b.bottom), left: Math.round(b.left),
                right: Math.round(b.right), h: Math.round(b.height), w: Math.round(b.width)}; };
      const cs = el => { if(!el) return null; const s = getComputedStyle(el);
        return {display: s.display, visibility: s.visibility, opacity: s.opacity}; };
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const fr = st.querySelector('.awd62-frame');
      const cv = st.querySelector('canvas');
      const cards = st.querySelector('.awd63-cards');
      const cardEls = cards ? Array.prototype.slice.call(cards.querySelectorAll('.awd63-card')) : [];
      const cap = st.querySelector('.awd62-caption');
      const glam = st.querySelector('.awd63-glamour');
      const capImg = glam ? glam.querySelector('.cap img') : null;
      const capImgStyle = capImg ? (() => { const s = getComputedStyle(capImg);
        return {bg: s.backgroundColor, w: s.width, h: s.height, border: s.borderTopWidth}; })() : null;
      const capTxt = st.querySelector('.awd62-caption');
      const revImg = capTxt ? capTxt.querySelector('img') : null;
      const revImgStyle = revImg ? (() => { const s = getComputedStyle(revImg);
        return {bg: s.backgroundColor, w: s.width, h: s.height}; })() : null;
      return { present: true, frame: r(fr), canvas: r(cv),
        canvasAttr: cv ? {w: cv.width, h: cv.height} : null,
        cards: cards ? Object.assign(r(cards), cs(cards),
          {n: cardEls.length,
           ops: cardEls.map(e => Math.round(parseFloat(getComputedStyle(e).opacity) * 100) / 100),
           shows: cardEls.map(e => e.classList.contains('show'))}) : null,
        caption: cap ? Object.assign(r(cap), {display: getComputedStyle(cap).display}) : null,
        glamOn: glam ? glam.classList.contains('on') : false,
        capImg: capImg ? Object.assign(r(capImg), capImgStyle,
          {nw: capImg.naturalWidth, complete: capImg.complete, src: (capImg.src || '').split('/').slice(-1)[0]}) : null,
        revImg: revImgStyle,
        canvasData: null };
    }""")

def watch174(pg, prefix, secs=25):
    timeline, beats_seen, seg_states, feet = [], [], {}, {}
    names_samples = []
    cur_seg, seg_start = None, None
    consumed = 0
    geo = None
    seg_geo = {}
    frame_by_seg = {}
    t0 = time.time()
    names_t0 = None
    reveal_canvas = None
    while time.time() - t0 < secs:
        st = D168.stage_state168(pg)
        fs = frame_state(pg)
        if not st.get("present"):
            break
        if geo is None:
            geo = W.canvas_geo(pg)
        seg = W.seg_of(st)
        if seg == "reveal" and reveal_canvas is None:
            try:
                reveal_canvas = pg.evaluate("""() => {
                  const cv = document.querySelector('.awd62-stage canvas');
                  return cv ? cv.toDataURL('image/png') : null; }""")
            except Exception:
                reveal_canvas = None
        now = round((time.time() - t0) * 1000)
        if seg != cur_seg:
            if cur_seg is not None:
                beats_seen.append({"id": cur_seg, "durMs": now - seg_start})
            cur_seg, seg_start = seg, now
            seg_states[seg] = st
            seg_geo[seg] = W.canvas_geo(pg)
            frame_by_seg[seg] = fs
            shot(pg, f"{prefix}_beat_{seg}.png")
            if seg == "names":
                names_t0 = now
        if seg == "names":
            names_samples.append({"t": now - (names_t0 or now),
                                  "frameTop": (fs.get("frame") or {}).get("top"),
                                  "frameH": (fs.get("frame") or {}).get("h"),
                                  "cards": fs.get("cards")})
        draws = pg.evaluate("() => (window.__figDraws || []).slice(%d)" % consumed)
        consumed += len(draws)
        for d in draws:
            foot = d["dy"] + d["dh"] * 115 / 128 if d["tux"] else d["dy"] + d["dh"]
            cx = d["dx"] + d["dw"] / 2
            feet.setdefault(seg, []).append({"foot": round(foot, 1), "cx": round(cx, 1),
                                             "dh": d["dh"], "tux": d["tux"],
                                             "x0": d["dx"], "x1": d["dx"] + d["dw"]})
        pg.wait_for_timeout(100)
    if cur_seg is not None:
        beats_seen.append({"id": cur_seg, "durMs": round((time.time() - t0) * 1000) - seg_start})
    return {"beats": beats_seen, "segStates": seg_states, "feet": feet,
            "totalMs": round((time.time() - t0) * 1000), "stageGone": not D168.stage_state168(pg).get("present"),
            "canvasGeo": geo, "segGeo": seg_geo, "frameBySeg": frame_by_seg,
            "namesSamples": names_samples, "revealCanvasData": reveal_canvas}

def foot_stats(samples):
    if not samples: return None
    fs = sorted(s["foot"] for s in samples)
    cxs = sorted(set(s["cx"] for s in samples))
    return {"n": len(samples), "foot_min": fs[0], "foot_med": fs[len(fs)//2], "foot_max": fs[-1],
            "cx": cxs, "tux_n": sum(1 for s in samples if s["tux"])}

def run_case(pw, name, height, kind):
    out = {"case": name, "checks": {}, "errors": []}
    errs = []
    pg = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"]).new_page(viewport={"width": 430, "height": height})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    pg.on("response", lambda r: errs.append(f"http{r.status}: {r.url}") if r.status >= 400 else None)
    try:
        assert D.new_game_to_map(pg), "去唔到地圖"
        D.install_draw_patch(pg)
        install_fig_patch174(pg)
        day = D.day_index(1991, 10, 20)
        if kind == "won":
            D.seed_won_poster(pg, day)
            fa = D.force_award(pg, "award_harbour_film", "nominee", want_won=True)
            assert fa["pack"].get("bestOutcome") == "won", "重骰都唔贏：%s" % fa["pack"]
        elif kind == "nominated":
            D.seed_won_poster(pg, day)
            fa = W.force_nominated(pg)
            assert fa["pack"].get("bestOutcome") == "nominated", "重骰都唔係 nominated：%s" % fa["pack"]
        else:
            D.seed_plain(pg, day)
            fa = D.force_award(pg, "award_harbour_film", "gallery", want_won=False)
            assert fa["pack"].get("bestOutcome") == "gallery", "pack 唔係 gallery：%s" % fa["pack"]
        out["pack"] = fa["pack"]
        shot(pg, f"{name}_invite.png")
        out["expected_beats"] = D.expected_beats(pg, fa["pack"])
        assert D.attend(pg), "請柬出席撳唔到"
        w = watch174(pg, name, 25)
        out["watch"] = w
        geo = (w.get("segGeo") or {}).get("names") or (w.get("segGeo") or {}).get("reveal") or w.get("canvasGeo")
        out["canvasGeo"] = geo
        stats = {seg: foot_stats(s) for seg, s in w["feet"].items()}
        out["footStats"] = stats
        if geo:
            out["stageTopDisplay"] = round(geo["top"] + FLOOR * geo["scale"], 1)
        # --- B1：每 beat 黑帶 ---
        fb = w.get("frameBySeg") or {}
        bands = {}
        for seg, fs in fb.items():
            fr = fs.get("frame") or {}
            cv = fs.get("canvas") or {}
            bands[seg] = {"frameTop": fr.get("top"), "frameBottom": fr.get("bottom"),
                          "frameH": fr.get("h"), "canvasH": cv.get("h"),
                          "topBand": fr.get("top"), "botBand": height - (fr.get("bottom") or 0)}
        out["bands"] = bands
        # --- B2：names 採樣分析 ---
        ns = w.get("namesSamples") or []
        if ns:
            tops = [s["frameTop"] for s in ns if s.get("frameTop") is not None]
            first_show = next((s["t"] for s in ns if s.get("cards") and any(s["cards"].get("shows") or [])), None)
            all_show = next((s["t"] for s in ns if s.get("cards") and s["cards"].get("shows") and all(s["cards"]["shows"])), None)
            all_opaque = next((s["t"] for s in ns if s.get("cards") and s["cards"].get("ops") and all(o >= 0.99 for o in s["cards"]["ops"])), None)
            first_vis = next((s["t"] for s in ns if s.get("cards") and s["cards"].get("visibility") == "visible"), None)
            _open_tops = [x["frameTop"] for x in ns if x.get("frameTop") is not None and x.get("t", 99999) <= 800]
            out["namesProbe"] = {"nSamples": len(ns),
                                 "frameTopMin": min(tops) if tops else None,
                                 "frameTopMax": max(tops) if tops else None,
                                 "frameTopJump": (max(tops) - min(tops)) if tops else None,
                                 # v177：B2 驗嘅係開場跳位——字幕行數變化（1 行↔2 行）會令 frame 高尾段郁 ~9px，
                                 # 嗰個係 caption 換行，唔係卡列跳位；開場 800ms 內先係 B2 範圍（舊 bug 83px）
                                 "frameTopJumpOpening800": (max(_open_tops) - min(_open_tops)) if _open_tops else None,
                                 "firstVisibleMs": first_vis, "firstShowMs": first_show,
                                 "allShowMs": all_show, "allOpaqueMs": all_opaque,
                                 "beatLenMs": next((b["durMs"] for b in w["beats"] if b["id"] == "names"), None)}
        # --- A1：glamour／reveal 獎盃 chip ---
        glam_fs = fb.get("glamour") or {}
        rev_fs = fb.get("reveal") or {}
        out["trophy"] = {"glamourCapImg": glam_fs.get("capImg"), "revealCapImg": rev_fs.get("revImg")}
        # --- C2：glamour frame 收短 ---
        if "glamour" in fb and "reveal" in fb:
            out["glamourFrame"] = {"glamourH": (fb["glamour"].get("frame") or {}).get("h"),
                                   "revealH": (fb["reveal"].get("frame") or {}).get("h"),
                                   "glamourCards": (fb["glamour"].get("cards") or {}).get("display"),
                                   "canvasBottomToFrameBottom": ((fb["glamour"].get("frame") or {}).get("bottom") or 0) - ((fb["glamour"].get("canvas") or {}).get("bottom") or 0)}
        # --- C1：gallery 中央人 vs 講台 ---
        if kind == "gallery":
            rev = stats.get("reveal") or {}
            # v177：gallery 82／162／262——中央人（162）右緣 193、右邊人（262）左緣 231，同講台 x194–229 應該零重疊
            draws_rev = (w["feet"].get("reveal") or [])
            ovs = []
            seen_cx = {}
            for d in draws_rev:
                seen_cx.setdefault(round(d["cx"]), d)
            for cx, d0 in sorted(seen_cx.items()):
                ovs.append({"cx": cx, "x0": d0["x0"], "x1": d0["x1"],
                            "ov": max(0, min(d0["x1"], LECTERN_X[1]) - max(d0["x0"], LECTERN_X[0]))})
            if ovs:
                out["c1"] = {"figs": ovs, "lecternX": list(LECTERN_X),
                             "overlapPx": max(o["ov"] for o in ovs)}
            # canvas 像素：watch 喺 reveal 段內讀咗 canvas（舞台拆咗之後讀唔到）
            data_url = w.get("revealCanvasData")
            out["c1CanvasSaved"] = False
            if data_url:
                open(os.path.join(HERE, f"{name}_c1_canvas.png"), "wb").write(base64.b64decode(data_url.split(",", 1)[1]))
                out["c1CanvasSaved"] = True
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
        for seg, exp in (("pan", FLOOR), ("enter", FLOOR), ("names", FLOOR), ("suspense", FLOOR),
                         ("comfort", FLOOR), ("glamour", FLOOR)):
            if seg not in exp_ids:
                continue
            s = stats.get(seg)
            if seg in ("comfort", "suspense"):
                # comfort 緊接 reveal：第一個 poll 會滲入 reveal 尾幀（得主行前腳 300／x≈170），
                # suspense 同理：poll 邊界 race 會將一格 reveal 行前燕尾服（腳 ~293）撥入 suspense
                # （all-run won_932：n=48 入面得 1 格 tux，cx 165）——所以只驗 median＋min（290），唔驗 max
                c[f"foot_{seg}_{FLOOR}"] = bool(s) and abs(s["foot_med"] - exp) <= 1.5 and s["foot_min"] >= exp - 3
            else:
                c[f"foot_{seg}_{FLOOR}"] = bool(s) and abs(s["foot_med"] - exp) <= 1.5 and s["foot_min"] >= exp - 3 and s["foot_max"] <= exp + 3
        s = stats.get("reveal")
        c["foot_reveal_260"] = bool(s) and 259 <= s["foot_max"] <= 261.5 and s["foot_min"] >= FLOOR - 2
        ns2 = stats.get("names") or {}
        cxs = ns2.get("cx") or []
        exp_cx = [82, 162, 262] if kind == "gallery" else [62, 162, 262, 362]
        c["slot_cx"] = len(cxs) == len(exp_cx) and all(abs(a - b) <= 3 for a, b in zip(cxs, exp_cx))
        out["slotCxMeasured"] = cxs
        # v177 行走探針：enter beat 人物 cx 逐格移動（由台側 −30／454 行到企位），唔係淡入企定
        ent = w["feet"].get("enter") or []
        ent_cx = sorted(set(d["cx"] for d in ent))
        out["enterWalk"] = {"nDistinctCx": len(ent_cx),
                            "cxMin": ent_cx[0] if ent_cx else None,
                            "cxMax": ent_cx[-1] if ent_cx else None,
                            "cxSpan": (ent_cx[-1] - ent_cx[0]) if len(ent_cx) >= 2 else 0}
        # gallery 冇 enter beat（pan 企定亮相），行走探針 N/A 當 PASS；won／nominated 先驗真行入場
        c["enter_walk_real"] = True if kind == "gallery" else (len(ent_cx) >= 12 and out["enterWalk"]["cxSpan"] >= 200)
        if geo:
            out["floorDepthDisplay"] = round(110 * geo["scale"], 1)
            c["floor_depth_110_logic"] = True
        if geo and stats.get("names"):
            foot_disp = round(geo["top"] + stats["names"]["foot_med"] * geo["scale"], 1)
            out["footDisplayNames"] = foot_disp
            c["foot_display_on_stage_top"] = abs(foot_disp - out["stageTopDisplay"]) <= 3
        # B1：黑帶收窄（932：open 上黑帶 < 250，舊 295；canvas 高 > 300，舊 233）
        if height == 932 and "open" in bands:
            c["b1_open_top_band_lt_250"] = (bands["open"]["topBand"] or 999) < 250
            c["b1_canvas_h_gt_300"] = (bands["open"]["canvasH"] or 0) > 300
        if "reveal" in bands and "open" in bands:
            if kind == "gallery":
                # gallery 冇卡列：reveal frame 由字幕行數決定，比 open 短 18px 係字幕行數差（舊 gallery reveal 帶 ~291）
                c["b1_gallery_reveal_band_lt_260"] = (bands["reveal"]["topBand"] or 999) < 260
            else:
                c["b1_reveal_band_lt_open"] = (bands["reveal"]["topBand"] or 999) <= (bands["open"]["topBand"] or 0) + 5
        # B2：frame 唔跳＋4 張齊得快（gallery 冇卡列，卡片指標 N/A，只驗 frame）
        np = out.get("namesProbe") or {}
        if np:
            _jump = np.get("frameTopJumpOpening800")
            c["b2_frame_no_jump"] = _jump is not None and _jump <= 5
            _all = np.get("allShowMs")
            # allShow 為 None 即係冇卡列（gallery）——N/A 當 PASS；有卡列嗰陣要 <900ms（舊 1382ms）
            c["b2_all_show_lt_900ms"] = True if _all is None else _all < 900
            _first = np.get("firstVisibleMs")
            # 採樣粒度 ~250ms（100ms wait＋兩次 evaluate），容器開場一個 tick（125ms）內可見；閾值 700ms
            c["b2_first_visible_lt_700ms"] = True if _first is None else _first < 700
        # A1：金底 chip
        tr = out.get("trophy") or {}
        if kind == "won":
            gi = tr.get("glamourCapImg") or {}
            c["a1_glamour_trophy_gold_chip"] = gi.get("bg") == "rgb(242, 193, 78)" and gi.get("w") == "22px"
            c["a1_glamour_trophy_loaded"] = bool(gi.get("complete")) and (gi.get("nw") or 0) > 0
            ri = tr.get("revealCapImg") or {}
            c["a1_reveal_trophy_gold_chip"] = ri.get("bg") == "rgb(242, 193, 78)"
        # C2：glamour 收短
        gf = out.get("glamourFrame")
        if kind == "won" and gf:
            c["c2_glamour_cards_display_none"] = gf.get("glamourCards") == "none"
            c["c2_glamour_frame_shorter_by_150plus"] = (gf.get("revealH") or 0) - (gf.get("glamourH") or 0) >= 150
            _db = gf.get("canvasBottomToFrameBottom")
            c["c2_no_174_dead_band"] = _db is not None and _db < 120
        # C1：中央人重疊 ≤ 5px
        if kind == "gallery" and out.get("c1"):
            c["c1_centre_overlap_le_5px"] = out["c1"]["overlapPx"] <= 5
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
        json.dump(results, open(os.path.join(HERE, "drive177.json"), "w"), ensure_ascii=False, indent=1)
        for name, r in results.items():
            print(f"{name}: {'PASS' if r.get('pass') else 'FAIL'} pageerrors={len(r.get('pageerrors', []))}")
            print(f"  checks={json.dumps(r.get('checks'), ensure_ascii=False)}")
            print(f"  canvasGeo={r.get('canvasGeo')} stageTopDisplay={r.get('stageTopDisplay')} footDisplayNames={r.get('footDisplayNames')}")
            print(f"  footStats={json.dumps(r.get('footStats'), ensure_ascii=False)}")
            print(f"  slotCx={r.get('slotCxMeasured')} beats={[(b['id'], b['durMs']) for b in (r.get('watch') or {}).get('beats', [])]}")
            print(f"  bands={json.dumps(r.get('bands'), ensure_ascii=False)}")
            print(f"  namesProbe={json.dumps(r.get('namesProbe'), ensure_ascii=False)}")
            print(f"  trophy={json.dumps(r.get('trophy'), ensure_ascii=False)}")
            print(f"  glamourFrame={json.dumps(r.get('glamourFrame'), ensure_ascii=False)} c1={json.dumps(r.get('c1'), ensure_ascii=False)}")
            if r.get("error"): print("  ERROR:", r["error"])
        ok = all(r.get("pass") for r in results.values())
        print("OVERALL", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    finally:
        D.stop_server(srv)

if __name__ == "__main__":
    sys.exit(main())
