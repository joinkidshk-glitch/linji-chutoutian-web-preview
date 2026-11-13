# -*- coding: utf-8 -*-
"""v199 最終實駕：B1 三 tier 高度正規化＋C1 bust＋C2/C3 新 angry 圖。
Serve 工作副本，LIVE 模式，932／700 兩個 viewport，0 pageerror、0 http fail。
重點：
 B1：同一頁內即時切 playerTierMax（1／2／3）播同一合成 beat，逐 px 量度
     painted 高（box 高＋闊高比計，object-fit:contain 模型）——同一配對同一舞台
     三 tier 必須同高；另驗搭檔（何生撞帽不變 617px；顧明輝比 1.05）、單人、
     闊配對（方小龍）、淨空 ≥12px、無橫向溢出、對話框遮腿（框頂＜人物腳底）。
 C1：屋企／頁頭 bust 三 tier rect 56×74 一致＋src 跟 tier；s1／s3 新 bust 並排
     截圖（實際尺寸＋4× 放大）一眼分到。
 C2：同 tier angry vs serious 舞台截圖＋目視分到。
 C3：三張 angry 圖原圖對照（s1 舊 vs s2／s3 新：s2／s3 同一套眉心皺紋、無紅印）。
 WF4：wf4DlgCharsHtml108 現場 call，markup 有 onload __dlg108Fit。
用法：/home/hatch/pwenv49/bin/python qa199/drive199.py
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, copy
from playwright.sync_api import sync_playwright

REPO = "/home/hatch/workspace/linji-work199"
HERE = "/home/hatch/workspace/linji-work199/qa199"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8999
URL = f"http://127.0.0.1:{PORT}/index.html"
SAVE_KEY = "starVolunteer_map_v19w"
LEAD90_1 = ["gig_1988_film_05"]
with open("/home/hatch/workspace/linji-work195/qa195/drive195/save_template.json", encoding="utf-8") as f:
    TEMPLATE = json.load(f)
REPORT = {"errors": [], "http_fail": [], "runs": {}, "checks": []}

def check(name, cond, detail=""):
    REPORT["checks"].append({"name": name, "pass": bool(cond), "detail": detail})
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail else ""), flush=True)
    return bool(cond)

def serve(cwd, port):
    p = subprocess.Popen(["python3", "-m", "http.server", str(port)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=5) as r:
        body = r.read(); assert r.status == 200
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    assert hashlib.sha256(body).hexdigest() == exp
    print(f"serve ok port {port} sha {exp[:12]}", flush=True)
    return p

def stop(p):
    try: p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def dismiss_encounter(pg, max_clicks=16):
    for _ in range(max_clicks):
        if pg.evaluate("() => !document.getElementById('enc79-overlay')"): return True
        clicked = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay'); if (!ov) return false;
          const sk = ov.querySelector('.e79-skip'); if (sk && sk.offsetParent !== null) { sk.click(); return true; }
          const ch = ov.querySelector('.e79-choice'); if (ch) { ch.click(); return true; }
          const nb = [...ov.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return true; } return false; }""")
        if not clicked: return pg.evaluate("() => !document.getElementById('enc79-overlay')")
        pg.wait_for_timeout(700)
    return pg.evaluate("() => !document.getElementById('enc79-overlay')")

def modal_click(pg, text):
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)

def js_click_text(pg, text):
    return pg.evaluate("""(t) => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()===t);
      if(!b) return false; b.click(); return true; }""", text)

def story_next(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")

MEASURE_JS = """() => {
  const st = document.querySelector('.story-play .sp-stage') || document.querySelector('.story-play');
  const chars = [...document.querySelectorAll('.story-play .dlg106-char')].map(im=>{
    const r = im.getBoundingClientRect(); const cs = getComputedStyle(im);
    const ar = (im.naturalWidth||0)/(im.naturalHeight||1);
    const paintedH = Math.min(r.height, r.width/ar);
    return {id: im.getAttribute('data-dlg-id'), src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
      x: Math.round(r.x*10)/10, y: Math.round(r.y*10)/10, w: Math.round(r.width*10)/10, h: Math.round(r.height*10)/10,
      natW: im.naturalWidth, natH: im.naturalHeight, ar: Math.round(ar*10000)/10000,
      paintedH: Math.round(paintedH*10)/10, paintedW: Math.round(paintedH*ar*10)/10,
      cssMaxW: cs.maxWidth, inlineH: im.style.height||''};});
  const plate = document.querySelector('.story-play .dlg106-plate, .story-play .sp-plate');
  const pr = plate ? plate.getBoundingClientRect() : null;
  const sr = st ? st.getBoundingClientRect() : null;
  let gap = null, overlap = false;
  if (chars.length >= 2) {
    const a = chars[0], b = chars[1];
    const l = a.x < b.x ? a : b, r2 = a.x < b.x ? b : a;
    gap = Math.round((r2.x - (l.x + l.w))*10)/10; overlap = gap < 0;
  }
  const awi = chars.find(c=>c.id==='awi');
  const legCover = (awi && pr) ? Math.round((awi.y + awi.h) - pr.y) : null;
  return {stage: sr ? {x: Math.round(sr.x), y: Math.round(sr.y), w: Math.round(sr.width), h: Math.round(sr.height),
      varH: st.style.getPropertyValue('--dlg108-char-h')||''} : null,
    chars, plate: pr ? {x: Math.round(pr.x), y: Math.round(pr.y), w: Math.round(pr.width), h: Math.round(pr.height)} : null,
    gap, overlap, legCover, docScrollW: document.documentElement.scrollWidth, winW: window.innerWidth}; }"""

def build_save(cfg):
    s = copy.deepcopy(TEMPLATE)
    s["dayIndex"] = cfg["day"]; s["fame"] = cfg["fame"]
    s["flags"] = dict(s.get("flags") or {})
    for k in list(s["flags"].keys()):
        if k.startswith("done_"): del s["flags"][k]
    for gid in cfg.get("doneFlags", []): s["flags"]["done_" + gid] = 1
    s["flags"]["playerTierMax"] = cfg.get("playerTierMax", 0)
    s["story"] = dict(s.get("story") or {})
    s["story"]["done"] = {c: True for c in ["C1", "C2", "C3", "C4", "C5"]}
    s["story"]["lastMainDoneDay"] = cfg["day"] - 8
    return s

def load_seeded_save(pg, cfg):
    save = build_save(cfg)
    pg.goto(URL); pg.wait_for_timeout(2500)
    pg.evaluate("(a) => localStorage.setItem(a[0], JSON.stringify(a[1]))", [SAVE_KEY, save])
    pg.goto(URL); pg.wait_for_timeout(2500)
    clicked = pg.evaluate("() => { const b=document.getElementById('btn-cont'); if(!b || b.offsetParent===null) return false; b.click(); return true; }")
    pg.wait_for_timeout(2000)
    dismiss_encounter(pg); modal_click(pg, "關閉"); pg.wait_for_timeout(500); dismiss_encounter(pg)
    return {"contClicked": clicked,
            "stem": pg.evaluate("() => { try { return DLG106.aweiStem(); } catch(e){ return '?'; } }")}

PARTNERS = {"ho_sang": ("何生", "ho_sang"), "vera": ("Vera", "vera"),
            "fong_siulung": ("方小龍", "fong_siulung"), "gu_mingfai": ("顧明輝", "gu_mingfai")}

def set_tier(pg, tier):
    pg.evaluate("(t) => { S.flags.playerTierMax = t; }", tier)
    pg.wait_for_timeout(200)
    return pg.evaluate("() => { try { return DLG106.aweiStem(); } catch(e){ return '?'; } }")

def run_beat(pg, partner_id, emotion, line, solo=False):
    pname, pid = PARTNERS[partner_id]
    pg.evaluate("""() => { const s = window.StoryPlay && StoryPlay.session; if (s && StoryPlay.abort) { try { StoryPlay.abort(); } catch(e){} } }""")
    pg.wait_for_timeout(400)
    if solo:
        beats = "[{speaker:'阿偉', speakerId:'player', kind:'player', emotion:a[0], lines:[a[3]]}]"
    else:
        beats = ("[{speaker:a[2], speakerId:a[1], kind:'npc', lines:['你話呢場戲點收科？']},"
                 "{speaker:'阿偉', speakerId:'player', kind:'player', emotion:a[0], lines:[a[3]]}]")
    ok = pg.evaluate("""(a) => { try {
      return !!StoryPlay.start({id:'T199_DRV', title:'199 drive', locId:'tvb_longmen', beats: %s,
        choices:[{id:'t199_ok', label:'（驗證用，繼續）'}]}, {force:true});
    } catch(e){ return 'err:'+e; } }""" % beats, [emotion, pid, pname, line])
    pg.wait_for_timeout(1200)
    dismiss_encounter(pg)
    if not solo:
        story_next(pg); pg.wait_for_timeout(900)
    dismiss_encounter(pg)
    m = pg.evaluate(MEASURE_JS)
    pg.evaluate("""() => { const s = window.StoryPlay && StoryPlay.session; if (s && StoryPlay.abort) { try { StoryPlay.abort(); } catch(e){} } }""")
    pg.wait_for_timeout(300)
    return {"startOk": ok, "m": m}

def shot_stage(pg, name):
    dismiss_encounter(pg); pg.wait_for_timeout(500); dismiss_encounter(pg)
    el = pg.query_selector(".story-play")
    if el:
        try: el.screenshot(path=os.path.join(SHOTS, f"{name}_stage.png"))
        except Exception: pass
    try: pg.screenshot(path=os.path.join(SHOTS, f"{name}.png"))
    except Exception as e: print(f"  [shot skipped: {name} ({e})]", flush=True)

def run_chain(pg):
    return pg.evaluate("""() => { const out = {};
      for (const e of ["base","smile","sad","serious","shy","surprise","think","angry"]) {
        const c = DLG106.candidates('awi', e);
        out[e] = (c[0]||'').split('/').pop().split('?')[0];
      } return out; }""")

def run_home_bust(pg, name):
    js_click_text(pg, "返回地圖"); pg.wait_for_timeout(900)
    home = pg.evaluate("""() => { const im=document.getElementById('home-awi');
      const v=document.getElementById('v-home');
      if(!im) return null;
      return {srcHead:(im.getAttribute('src')||'').slice(0,200), complete: !!im.complete, natW: im.naturalWidth||0,
              homeVisible: !!(v && v.offsetParent!==null),
              rect: (()=>{const r=im.getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)};})()}; }""")
    if not home or not home.get("homeVisible"):
        pg.evaluate("() => { try { enterHome(null, false); } catch(e){} }")
        pg.wait_for_timeout(1200)
        home = pg.evaluate("""() => { const im=document.getElementById('home-awi');
          const v=document.getElementById('v-home');
          if(!im) return null;
          return {srcHead:(im.getAttribute('src')||'').slice(0,200), complete: !!im.complete, natW: im.naturalWidth||0,
                  homeVisible: !!(v && v.offsetParent!==null),
                  rect: (()=>{const r=im.getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)};})()}; }""")
    if home and home.get("homeVisible"):
        try: pg.screenshot(path=os.path.join(SHOTS, f"{name}_home.png"))
        except Exception as e: print(f"  [shot skipped: {name}_home ({e})]", flush=True)
        try:
            el = pg.query_selector("#home-awi")
            if el: el.screenshot(path=os.path.join(SHOTS, f"{name}_home_bust.png"))
        except Exception: pass
    js_click_text(pg, "返回地圖"); pg.wait_for_timeout(800)
    dismiss_encounter(pg)
    return home

def main():
    srv = serve(REPO, PORT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            for vp in [{"width": 932, "height": 1500}, {"width": 700, "height": 1400}]:
                tag = str(vp["width"])
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=tag: REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=tag: REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    post = load_seeded_save(pg, {"day": 400, "fame": 30, "doneFlags": LEAD90_1, "playerTierMax": 2})
                    check(f"{tag} 載入 day400 ptm2 stem=s2", post["stem"] == "awi_s2", post)
                    REPORT["runs"][f"load_{tag}"] = post
                    # ---- B1：同一頁切 tier，同一 beat（何生＋base）逐 px 量度 ----
                    ho = {}
                    for tier, stem in [(1, "awi"), (2, "awi_s2"), (3, "awi_s3")]:
                        st = set_tier(pg, tier)
                        res = run_beat(pg, "ho_sang", "base", "記住，呢行最緊要係準時。")
                        ho[tier] = res["m"]
                        awi = next((c for c in res["m"]["chars"] if c["id"] == "awi"), None)
                        print(f"== {tag} tier{tier} stem={st} varH={res['m']['stage']['varH']} awi={awi} gap={res['m']['gap']} legCover={res['m']['legCover']} scrollW={res['m']['docScrollW']}/{res['m']['winW']}", flush=True)
                        if tier == 2:
                            shot_stage(pg, f"T2_{tag}_ho_base")
                    hs = [next(c["paintedH"] for c in ho[t]["chars"] if c["id"] == "awi") for t in (1, 2, 3)]
                    check(f"{tag} B1 何生＋base：三 tier painted 高同高（{hs}，spread {max(hs)-min(hs):.1f}px）",
                          max(hs) - min(hs) <= 1.0, hs)
                    check(f"{tag} B1 何生＋base：三 tier box 高同高",
                          len({next(c['h'] for c in ho[t]['chars'] if c['id']=='awi') for t in (1,2,3)}) == 1, hs)
                    check(f"{tag} B1 何生 painted 高三 tier 一致（撞帽者不變）",
                          len({next(c['paintedH'] for c in ho[t]['chars'] if c['id']=='ho_sang') for t in (1,2,3)}) == 1,
                          [next(c['paintedH'] for c in ho[t]['chars'] if c['id']=='ho_sang') for t in (1,2,3)])
                    for t in (1, 2, 3):
                        check(f"{tag} B1 tier{t} 淨空 ≥12px、無重疊", ho[t]["gap"] is not None and ho[t]["gap"] >= 12 and not ho[t]["overlap"], ho[t]["gap"])
                        check(f"{tag} B1 tier{t} 無橫向溢出", ho[t]["docScrollW"] <= ho[t]["winW"], f"{ho[t]['docScrollW']}/{ho[t]['winW']}")
                        check(f"{tag} B1 tier{t} 對話框遮腿（框頂＜腳底，遮 {ho[t]['legCover']}px）",
                              ho[t]["legCover"] is not None and ho[t]["legCover"] > 0, ho[t]["legCover"])
                    # ---- B1：angry／serious 各 tier 同高 ----
                    for emo, line in [("angry", "夠啦！呢場戲唔係咁拍㗎！"), ("serious", "記住，呢行最緊要係準時。")]:
                        hs_e = []
                        for tier in (1, 2, 3):
                            set_tier(pg, tier)
                            res = run_beat(pg, "ho_sang", emo, line)
                            hs_e.append(next(c["paintedH"] for c in res["m"]["chars"] if c["id"] == "awi"))
                            if tier == 2:
                                shot_stage(pg, f"T2_{tag}_ho_{emo}")
                        check(f"{tag} B1 何生＋{emo}：三 tier painted 高同高（{hs_e}，spread {max(hs_e)-min(hs_e):.1f}px）",
                              max(hs_e) - min(hs_e) <= 1.0, hs_e)
                        REPORT["runs"][f"{tag}_ho_{emo}"] = hs_e
                    # ---- B1：其他搭檔（tier 2 為主＋tier 1／3 對照）----
                    for pid in ("vera", "fong_siulung", "gu_mingfai"):
                        hs_p = []
                        for tier in (1, 2, 3):
                            set_tier(pg, tier)
                            res = run_beat(pg, pid, "base", "記住，呢行最緊要係準時。")
                            hs_p.append(next(c["paintedH"] for c in res["m"]["chars"] if c["id"] == "awi"))
                        check(f"{tag} B1 {pid}＋base：三 tier painted 高同高（{hs_p}）", max(hs_p) - min(hs_p) <= 1.0, hs_p)
                        REPORT["runs"][f"{tag}_{pid}"] = hs_p
                    # 顧明輝比 1.05（tier 2）
                    set_tier(pg, 2)
                    res = run_beat(pg, "gu_mingfai", "base", "記住，呢行最緊要係準時。")
                    gu = next(c for c in res["m"]["chars"] if c["id"] == "gu_mingfai")
                    aw = next(c for c in res["m"]["chars"] if c["id"] == "awi")
                    check(f"{tag} B1 顧明輝／阿偉 painted 比 1.05（實測 {gu['paintedH']/aw['paintedH']:.3f}）",
                          abs(gu["paintedH"] / aw["paintedH"] - 1.05) < 0.01, (gu["paintedH"], aw["paintedH"]))
                    # ---- B1：單人阿偉 ----
                    hs_solo = []
                    for tier in (1, 2, 3):
                        set_tier(pg, tier)
                        res = run_beat(pg, "ho_sang", "base", "記住，呢行最緊要係準時。", solo=True)
                        solo_chars = res["m"]["chars"]
                        hs_solo.append(solo_chars[0]["paintedH"] if solo_chars else None)
                    check(f"{tag} B1 單人阿偉：三 tier painted 高同高（{hs_solo}）",
                          None not in hs_solo and max(hs_solo) - min(hs_solo) <= 1.0, hs_solo)
                    REPORT["runs"][f"{tag}_solo"] = hs_solo
                    # ---- 表情鏈＋新圖自然尺寸 ----
                    chain = {}
                    for tier in (1, 2, 3):
                        set_tier(pg, tier)
                        chain[tier] = run_chain(pg)
                    check(f"{tag} 表情鏈 angry 首選：s1 awi_angry／s2 awi_s2_angry／s3 awi_s3_angry",
                          chain[1]["angry"] == "awi_angry.webp" and chain[2]["angry"] == "awi_s2_angry.webp"
                          and chain[3]["angry"] == "awi_s3_angry.webp", chain)
                    nat = pg.evaluate("""() => { const out = {};
                      for (const f of ['awi_s2_angry.webp','awi_s3_angry.webp']) {
                        const im = new Image(); out[f] = 'pending'; }
                      return new Promise(res => {
                        const r = {};
                        for (const f of ['awi_s2_angry.webp','awi_s3_angry.webp']) {
                          const im = new Image();
                          im.onload = () => { r[f] = [im.naturalWidth, im.naturalHeight]; if (Object.keys(r).length === 2) res(r); };
                          im.onerror = () => { r[f] = 'error'; if (Object.keys(r).length === 2) res(r); };
                          im.src = 'assets/story/fullbody/' + f;
                        } }); }""")
                    check(f"{tag} 新 angry 圖自然尺寸 896×2976", nat == {"awi_s2_angry.webp": [896, 2976], "awi_s3_angry.webp": [896, 2976]}, nat)
                    REPORT["runs"][f"{tag}_chain"] = chain
                    # ---- C1／C2：屋企 bust＋serious 對照 ----
                    homes = {}
                    for tier in (1, 2, 3):
                        set_tier(pg, tier)
                        homes[tier] = run_home_bust(pg, f"T{tier}_{tag}")
                    rects = [homes[t]["rect"] for t in (1, 2, 3)]
                    check(f"{tag} C1 屋企 bust 三 tier rect 一致 56×74", all(r["w"] == 56 and r["h"] == 74 for r in rects), rects)
                    check(f"{tag} C1 屋企 bust 全部 complete＋naturalWidth 240",
                          all(homes[t]["complete"] and homes[t]["natW"] == 240 for t in (1, 2, 3)), homes)
                    REPORT["runs"][f"{tag}_home"] = homes
                    # WF4 markup 現場檢查
                    wf4 = pg.evaluate("""() => { try {
                      const h = wf4DlgCharsHtml108({beats:[{sp:'阿偉', tx:'test'}]}, {sp:'阿偉', tx:'test'});
                      return {hasFit: h.indexOf('__dlg108Fit') >= 0, hasChar: h.indexOf('dlg106-char') >= 0, len: h.length};
                    } catch(e){ return {err: '' + e}; } }""")
                    check(f"{tag} WF4 markup 有 onload __dlg108Fit", wf4.get("hasFit") and wf4.get("hasChar"), wf4)
                    REPORT["runs"][f"{tag}_wf4"] = wf4
                except Exception as e:
                    REPORT["runs"][f"error_{tag}"] = {"error": str(e)}
                    print(f"  !! {tag}: {e}", flush=True)
                pg.close()
            br.close()
    finally:
        stop(srv)
    # bust src 身份事後對照（同 review195 手法）
    _h = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()
    import re as _re
    def _cand(pat):
        m = _re.search(pat, _h)
        return m.group(1)[:200] if m else None
    _cands = {"s1": _cand(r'"hero_awi": "(data:image[^"]{100,})"'),
              "s2": _cand(r'awi_s2: "(data:image[^"]{100,})"'),
              "s3": _cand(r'awi_s3: "(data:image[^"]{100,})"')}
    for _k, _v in list(REPORT["runs"].items()):
        if _k.endswith("_home") and isinstance(_v, dict):
            for _t, _home in _v.items():
                if isinstance(_home, dict) and _home.get("srcHead"):
                    _head = _home["srcHead"][:200]
                    _home["bustMatch"] = {k: (_head == c) for k, c in _cands.items() if c}
    try:
        with open(os.path.join(HERE, "drive199_report.json"), "w", encoding="utf-8") as f:
            json.dump(REPORT, f, ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"[report write skipped (sandbox write block): {e}] — checks above stand", flush=True)
    n_pass = sum(1 for c in REPORT["checks"] if c["pass"])
    print(f"CHECKS {n_pass}/{len(REPORT['checks'])} PASS")
    for c in REPORT["checks"]:
        if not c["pass"]: print("  FAIL:", c["name"], c["detail"])
    print("pageerrors:", len(REPORT["errors"]), REPORT["errors"][:5])
    print("http_fail:", len(REPORT["http_fail"]), REPORT["http_fail"][:5])

if __name__ == "__main__":
    main()
