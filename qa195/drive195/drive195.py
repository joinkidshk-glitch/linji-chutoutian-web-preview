# -*- coding: utf-8 -*-
"""v195 實駕：阿偉造型最高紀錄（B 方案）跨年驗證。
工作副本 ~/workspace/linji-work195（分支 v20a195，rebase 上 main b104f85），port 8985；
pristine 對照 ~/workspace/pristine195-b104f85（b104f85），port 8986。LIVE 模式。
播種：真存檔模板（probe195.py 經 UI 開新局＋saveQ 攞到）逐 case 改寫後寫入
localStorage slot 1（key starVolunteer_map_v19w），再經 #btn-cont「繼續」讀檔——
即係行真載入路徑（normalizeSaveObj → backfill），唔係 in-page 改 S。
對話觸發：沿用調查員方法（開金龍茶餐廳 sheet 再閂 → 強制主線 C6 播出），播唔出
就 fallback StoryPlay.start('C6', {force:true})，會如實記錄。
F：全庫搵唔到現成阿偉 angry 對白（25 句 player lines＋3 句「阿偉」beats，0 句含嬲
關鍵字），改經對話引擎 StoryPlay.start 合成 beat（emotion:"angry"＋對白含「夠啦」，
分類器同 emotion 欄兩條路都指向 angry），播出後讀 DOM img src。
G：先試 UI 路徑（地圖「進度」→「回顧手帳」／屋企掣），唔通先直接 call enterHome
（同 UI 掣 call 同一個函數），逐步記錄。
用法：/home/hatch/pwenv49/bin/python ~/workspace/linji-work195/qa195/drive195/drive195.py
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, copy
from playwright.sync_api import sync_playwright

WORK = "/home/hatch/workspace/linji-work195"
PRISTINE = "/home/hatch/workspace/pristine195-b104f85"
HERE = "/home/hatch/workspace/linji-work195/qa195/drive195"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT_W, PORT_P = 8985, 8986
URL_W = f"http://127.0.0.1:{PORT_W}/index.html"
URL_P = f"http://127.0.0.1:{PORT_P}/index.html"
SAVE_KEY = "starVolunteer_map_v19w"
LEAD90_3 = ["gig_1988_film_05", "gig_1988_film_06", "gig_1988_film_07"]

with open(os.path.join(HERE, "save_template.json"), encoding="utf-8") as f:
    TEMPLATE = json.load(f)

REPORT = {"errors": [], "http_fail": [], "angry_http": [], "runs": {}}


def serve(cwd, port):
    p = subprocess.Popen(["python3", "-m", "http.server", str(port)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=5) as r:
        body = r.read()
        assert r.status == 200
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    assert hashlib.sha256(body).hexdigest() == exp, f"served index mismatch port {port}"
    print(f"serve ok port {port} sha {exp[:12]}", flush=True)
    return p


def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass


def dismiss_encounter(pg, max_clicks=16):
    for _ in range(max_clicks):
        if pg.evaluate("() => !document.getElementById('enc79-overlay')"):
            return True
        clicked = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay'); if (!ov) return false;
          const sk = ov.querySelector('.e79-skip'); if (sk && sk.offsetParent !== null) { sk.click(); return true; }
          const ch = ov.querySelector('.e79-choice'); if (ch) { ch.click(); return true; }
          const nb = [...ov.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return true; } return false; }""")
        if not clicked:
            return pg.evaluate("() => !document.getElementById('enc79-overlay')")
        pg.wait_for_timeout(700)
    return pg.evaluate("() => !document.getElementById('enc79-overlay')")


def modal_click(pg, text):
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def js_click_text(pg, text):
    return pg.evaluate("""(t) => {
      const b = [...document.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def visible_buttons(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim().replace(/\\s+/g,' ').slice(0,28)).filter(Boolean)""")


STAGE_JS = """() => {
  const imgs = [...document.querySelectorAll('.dlg106-char')].map(im=>({
    id: im.getAttribute('data-dlg-id'),
    src: (im.getAttribute('src')||'').slice(0,120),
    complete: !!im.complete, natW: im.naturalWidth||0 }));
  const plate = document.querySelector('.story-play .dlg106-plate, .story-play .sp-plate');
  const spk = document.querySelector('.story-play .sp-speaker');
  const choices = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null).length;
  return {active: !!plate || choices>0, speaker: spk ? spk.textContent.trim() : '',
    line: plate ? plate.textContent.replace(/\\s+/g,' ').trim().slice(0,80) : '',
    imgs, choices};
}"""


def story_next(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")


def build_save(cfg):
    s = copy.deepcopy(TEMPLATE)
    s["dayIndex"] = cfg["day"]
    s["fame"] = cfg["fame"]
    s["flags"] = dict(s.get("flags") or {})
    for k in list(s["flags"].keys()):
        if k.startswith("done_"):
            del s["flags"][k]
    for gid in cfg.get("doneFlags", []):
        s["flags"]["done_" + gid] = 1
    if "playerTierMax" in cfg:
        s["flags"]["playerTierMax"] = cfg["playerTierMax"]
    else:
        s["flags"].pop("playerTierMax", None)  # 舊檔形狀：冇呢支旗
    s["story"] = dict(s.get("story") or {})
    s["story"]["done"] = {c: True for c in ["C1", "C2", "C3", "C4", "C5"]}
    s["story"]["lastMainDoneDay"] = cfg["day"] - 8
    return s


def load_seeded_save(pg, url, cfg):
    """寫 localStorage → reload → #btn-cont 繼續（真載入路徑）。回傳載入後量度。"""
    save = build_save(cfg)
    pg.goto(url); pg.wait_for_timeout(2500)
    pg.evaluate("(args) => localStorage.setItem(args[0], JSON.stringify(args[1]))", [SAVE_KEY, save])
    pg.goto(url); pg.wait_for_timeout(2500)
    clicked = pg.evaluate("() => { const b=document.getElementById('btn-cont'); if(!b || b.offsetParent===null) return false; b.click(); return true; }")
    pg.wait_for_timeout(2000)
    dismiss_encounter(pg)
    modal_click(pg, "關閉"); pg.wait_for_timeout(500)
    dismiss_encounter(pg)
    post = pg.evaluate("""() => {
      const hasTier = !!(window.S && S.flags && typeof S.flags.playerTierMax !== 'undefined');
      let live = null; try { live = (typeof enc79PlayerTier === 'function') ? enc79PlayerTier() : null; } catch(e){}
      let stem = '?'; try { stem = (window.DLG106 && DLG106.aweiStem) ? DLG106.aweiStem() : '?'; } catch(e){}
      let cands = []; try { cands = (window.DLG106 && DLG106.candidates) ? DLG106.candidates('awi','angry') : []; } catch(e){}
      return {contClicked: %s, day: (window.S ? S.dayIndex : null), fame: (window.S ? S.fame : null),
        ptm: (window.S && S.flags) ? S.flags.playerTierMax : undefined, ptmPresent: hasTier,
        liveTier: live, stem, gigsYear: (window.STORY_WIRE && STORY_WIRE.gigsYearActive),
        candsAngry0: (cands[0]||'').split('/').pop(), candsAngry: cands.slice(0,3).map(u=>u.split('/').pop())};
    }""" % ("true" if clicked else "false"))
    post["seed"] = {"day": cfg["day"], "fame": cfg["fame"],
                    "doneFlags": cfg.get("doneFlags", []),
                    "playerTierMax_seeded": cfg.get("playerTierMax", "<absent: old-save shape>")}
    return post


def trigger_story(pg):
    """調查員方法：開茶餐廳 sheet 再閂 → 強制主線播出；播唔出就 fallback C6。"""
    pg.evaluate("""() => { const s = window.StoryPlay && StoryPlay.session; if (s && StoryPlay.abort) { try { StoryPlay.abort(); } catch(e){} } }""")
    pg.wait_for_timeout(400)
    opened = pg.evaluate("""() => { const b=[...document.querySelectorAll('#v-map button')].find(x=>x.offsetParent!==null && (x.textContent||'').includes('茶餐廳'));
      if(!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    dismiss_encounter(pg)
    closed = pg.evaluate("""() => { const sh=document.getElementById('loc-sheet'); if(!sh) return false;
      const b=[...sh.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='返回地圖');
      if(!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    st = pg.evaluate(STAGE_JS)
    method = "tea-room"
    if not st["active"]:
        ok = pg.evaluate("() => { try { return !!StoryPlay.start('C6', {force:true}); } catch(e){ return false; } }")
        pg.wait_for_timeout(1200)
        st = pg.evaluate(STAGE_JS)
        method = "fallback-StoryPlay.start(C6) ok=" + str(ok)
    return method, st


def play_lines(pg, name, max_lines=12):
    lines = []
    shot_awis = False
    for i in range(max_lines):
        st = pg.evaluate(STAGE_JS)
        if not st["active"]:
            break
        awi_src = next((im["src"] for im in st["imgs"] if im["id"] == "awi"), None)
        lines.append({"i": i, "speaker": st["speaker"], "line": st["line"],
                      "awiSrc": awi_src, "allImgs": st["imgs"]})
        if i == 0:
            pg.screenshot(path=os.path.join(SHOTS, f"{name}_dlg0.png"))
        if awi_src and not shot_awis:
            pg.screenshot(path=os.path.join(SHOTS, f"{name}_awi.png"))
            shot_awis = True
        if st["choices"]:
            break
        if not story_next(pg):
            break
        pg.wait_for_timeout(800)
    return lines


def close_story(pg):
    """播完揀第一個選項＋閂 modal，返地圖。"""
    for _ in range(6):
        st = pg.evaluate(STAGE_JS)
        if not st["active"]:
            break
        if st["choices"]:
            pg.evaluate("""() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null); if (c[0]) c[0].click(); }""")
            pg.wait_for_timeout(1000)
            continue
        if not story_next(pg):
            break
        pg.wait_for_timeout(700)
    modal_click(pg, "關閉"); pg.wait_for_timeout(600)
    js_click_text(pg, "返回地圖"); pg.wait_for_timeout(1000)
    dismiss_encounter(pg)


def run_angry(pg, name, tier):
    """F：StoryPlay.start 合成 angry beat（emotion:"angry"＋對白含「夠啦」）。"""
    pg.evaluate("""() => { const s = window.StoryPlay && StoryPlay.session; if (s && StoryPlay.abort) { try { StoryPlay.abort(); } catch(e){} } }""")
    pg.wait_for_timeout(400)
    ok = pg.evaluate("""() => { try {
      return !!StoryPlay.start({id:'T195_ANGRY', title:'195 驗證', beats:[
        {speaker:'何生', speakerId:'ho_sang', kind:'npc', lines:['你話呢場戲點收科？']},
        {speaker:'阿偉', speakerId:'player', kind:'player', emotion:'angry', lines:['夠啦！呢場戲唔係咁拍㗎！']}
      ], choices:[{id:'t195_ok', label:'（驗證用，繼續）'}]}, {force:true});
    } catch(e){ return 'err:'+e; } }""")
    pg.wait_for_timeout(1200)
    st1 = pg.evaluate(STAGE_JS)
    cat = pg.evaluate("() => { try { return DLG106.resolveCategory({emotion:'angry', text:'夠啦！呢場戲唔係咁拍㗎！'}); } catch(e){ return 'err'; } }")
    adv = story_next(pg)
    pg.wait_for_timeout(900)
    st2 = pg.evaluate(STAGE_JS)
    awi2 = next((im for im in st2["imgs"] if im["id"] == "awi"), None)
    pg.screenshot(path=os.path.join(SHOTS, f"{name}_angry.png"))
    pg.evaluate("""() => { const s = window.StoryPlay && StoryPlay.session; if (s && StoryPlay.abort) { try { StoryPlay.abort(); } catch(e){} } }""")
    pg.wait_for_timeout(400)
    return {"startOk": ok, "resolveCategory": cat, "beat1": st1, "beat2": st2,
            "awiImg": awi2, "expect": f"awi_s{tier}_angry.webp"}


def run_home(pg, name, tier):
    """G：先試 UI 路徑，唔通先直接 call enterHome（同 UI 掣同一個函數）。"""
    attempts = []
    js_click_text(pg, "返回地圖"); pg.wait_for_timeout(900)
    btns0 = visible_buttons(pg)
    attempts.append({"step": "map buttons", "buttons": btns0})
    # 1. 「進度」掣（地圖頂列，label 係「進度＋badge」）
    hit = pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim().startsWith('進度'));
      if(!b) return false; b.click(); return true; }""")
    attempts.append({"step": "click 進度 button", "clicked": hit})
    pg.wait_for_timeout(1200)
    btns1 = visible_buttons(pg)
    attempts.append({"step": "after 進度 buttons", "buttons": btns1})
    got_home = False
    if hit:
        for t in ["回顧手帳", "屋企", "返屋企"]:
            if js_click_text(pg, t):
                attempts.append({"step": f"click '{t}' in modal", "clicked": True})
                pg.wait_for_timeout(1200)
                break
        else:
            attempts.append({"step": "no 回顧手帳/屋企 button in modal", "clicked": False})
    home = pg.evaluate("""() => { const im=document.getElementById('home-awi');
      const v=document.getElementById('v-home');
      if(!im) return null;
      return {src:(im.getAttribute('src')||'').slice(0,140), complete: !!im.complete, natW: im.naturalWidth||0,
              homeVisible: !!(v && v.offsetParent!==null)}; }""")
    if not home or not home.get("homeVisible"):
        attempts.append({"step": "fallback: direct enterHome(null,false)", "clicked": True})
        pg.evaluate("() => { try { enterHome(null, false); } catch(e){ return 'err:'+e; } }")
        pg.wait_for_timeout(1200)
        home = pg.evaluate("""() => { const im=document.getElementById('home-awi');
          const v=document.getElementById('v-home');
          if(!im) return null;
          return {src:(im.getAttribute('src')||'').slice(0,140), complete: !!im.complete, natW: im.naturalWidth||0,
                  homeVisible: !!(v && v.offsetParent!==null)}; }""")
    if home:
        pg.screenshot(path=os.path.join(SHOTS, f"{name}_home.png"))
    return {"attempts": attempts, "home": home, "expectTier": tier}


def awi_tier_of(src):
    if not src:
        return None
    if "awi_s3_" in src:
        return 3
    if "awi_s2_" in src:
        return 2
    if "awi_" in src:
        return 1
    return None


def run_dialogue_case(pg, name, url, cfg, expect_tier, extra=None):
    post = load_seeded_save(pg, url, cfg)
    method, st0 = trigger_story(pg)
    lines = play_lines(pg, name)
    awi_lines = [ln for ln in lines if ln.get("awiSrc")]
    tiers = [awi_tier_of(ln["awiSrc"]) for ln in awi_lines]
    dlg_pass = (post["stem"] == f"awi_s{expect_tier}" if expect_tier > 1 else post["stem"] == "awi") \
        and len(awi_lines) > 0 and all(t == expect_tier for t in tiers)
    res = {"case": name, "viewport": pg.viewport_size, "seed": post["seed"],
           "postLoad": {k: v for k, v in post.items() if k != "seed"},
           "trigger": method, "lines": lines,
           "awiLines": len(awi_lines), "awiTiers": tiers,
           "expectTier": expect_tier, "verdict": "PASS" if dlg_pass else "FAIL"}
    if extra == "lazy":
        lazy = pg.evaluate("""() => { delete S.flags.playerTierMax;
          const stem = (window.DLG106 && DLG106.aweiStem) ? DLG106.aweiStem() : '?';
          return {stemAfterDelete: stem, ptmAfterStemRead: S.flags.playerTierMax}; }""")
        res["lazyBackfill"] = lazy
        res["lazyPass"] = (lazy["stemAfterDelete"] == "awi_s2" and lazy["ptmAfterStemRead"] == 2)
    close_story(pg)
    REPORT["runs"][name] = res
    print(f"== {name} vp={pg.viewport_size} stem={post['stem']} ptm={post.get('ptm')} "
          f"live={post.get('liveTier')} awiLines={len(awi_lines)} tiers={tiers} -> {res['verdict']}", flush=True)
    return res


def main():
    srv_w = serve(WORK, PORT_W)
    srv_p = serve(PRISTINE, PORT_P)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            viewports = [{"width": 932, "height": 1500}, {"width": 700, "height": 1400}]
            # ---- 工作版 cases ----
            for vp in viewports:
                tag = f"{vp['width']}"
                # A
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=f"A_{tag}": REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=f"A_{tag}": REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    run_dialogue_case(pg, f"A_{tag}", URL_W,
                                      {"day": 300, "fame": 30, "doneFlags": ["gig_1988_film_05"], "playerTierMax": 2}, 2)
                except Exception as e:
                    REPORT["runs"][f"A_{tag}"] = {"error": str(e)}
                    print(f"  !! A_{tag} exception: {e}", flush=True)
                pg.close()
                # B (+lazy, +F2, +G2 同頁)
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=f"B_{tag}": REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=f"B_{tag}": (REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None,
                                                             REPORT["angry_http"].append(f"{n} {r.status} {r.url}") if "awi_s2_angry" in r.url else None))
                try:
                    r = run_dialogue_case(pg, f"B_{tag}", URL_W,
                                          {"day": 400, "fame": 30, "doneFlags": ["gig_1988_film_05"], "playerTierMax": 2}, 2,
                                          extra="lazy")
                    f2 = run_angry(pg, f"F2_{tag}", 2)
                    src2 = (f2["awiImg"] or {}).get("src", "")
                    f2["verdict"] = "PASS" if ("awi_s2_angry.webp" in src2 and (f2["awiImg"] or {}).get("complete") and (f2["awiImg"] or {}).get("natW", 0) > 0) else "FAIL"
                    REPORT["runs"][f"F2_{tag}"] = f2
                    print(f"== F2_{tag} awiSrc={src2} -> {f2['verdict']}", flush=True)
                    g2 = run_home(pg, f"G2_{tag}", 2)
                    hsrc = (g2["home"] or {}).get("src", "")
                    g2["verdict"] = "PASS" if ("s2" in hsrc and (g2["home"] or {}).get("natW", 0) > 0) else "FAIL"
                    REPORT["runs"][f"G2_{tag}"] = g2
                    print(f"== G2_{tag} homeSrc={hsrc} -> {g2['verdict']}", flush=True)
                except Exception as e:
                    REPORT["runs"][f"B_{tag}"] = {"error": str(e)}
                    print(f"  !! B_{tag} exception: {e}", flush=True)
                pg.close()
                # C
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=f"C_{tag}": REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=f"C_{tag}": REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    run_dialogue_case(pg, f"C_{tag}", URL_W,
                                      {"day": 400, "fame": 30, "doneFlags": ["gig_1989_tv_10"], "playerTierMax": 2}, 2)
                except Exception as e:
                    REPORT["runs"][f"C_{tag}"] = {"error": str(e)}
                    print(f"  !! C_{tag} exception: {e}", flush=True)
                pg.close()
                # D day300 (+F3/G3 喺 D-day400 頁做，見下)
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=f"D300_{tag}": REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=f"D300_{tag}": REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    run_dialogue_case(pg, f"D300_{tag}", URL_W,
                                      {"day": 300, "fame": 70, "doneFlags": LEAD90_3, "playerTierMax": 3}, 3)
                except Exception as e:
                    REPORT["runs"][f"D300_{tag}"] = {"error": str(e)}
                    print(f"  !! D300_{tag} exception: {e}", flush=True)
                pg.close()
                # D day400 (+F3, +G3 同頁)
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=f"D400_{tag}": REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=f"D400_{tag}": (REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None,
                                                             REPORT["angry_http"].append(f"{n} {r.status} {r.url}") if "awi_s3_angry" in r.url else None))
                try:
                    run_dialogue_case(pg, f"D400_{tag}", URL_W,
                                      {"day": 400, "fame": 70, "doneFlags": LEAD90_3, "playerTierMax": 3}, 3)
                    f3 = run_angry(pg, f"F3_{tag}", 3)
                    src3 = (f3["awiImg"] or {}).get("src", "")
                    f3["verdict"] = "PASS" if ("awi_s3_angry.webp" in src3 and (f3["awiImg"] or {}).get("complete") and (f3["awiImg"] or {}).get("natW", 0) > 0) else "FAIL"
                    REPORT["runs"][f"F3_{tag}"] = f3
                    print(f"== F3_{tag} awiSrc={src3} -> {f3['verdict']}", flush=True)
                    g3 = run_home(pg, f"G3_{tag}", 3)
                    hsrc3 = (g3["home"] or {}).get("src", "")
                    g3["verdict"] = "PASS" if ("s3" in hsrc3 and (g3["home"] or {}).get("natW", 0) > 0) else "FAIL"
                    REPORT["runs"][f"G3_{tag}"] = g3
                    print(f"== G3_{tag} homeSrc={hsrc3} -> {g3['verdict']}", flush=True)
                except Exception as e:
                    REPORT["runs"][f"D400_{tag}"] = {"error": str(e)}
                    print(f"  !! D400_{tag} exception: {e}", flush=True)
                pg.close()
                # E 舊檔 backfill（冇 playerTierMax 呢支旗）
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=f"E_{tag}": REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=f"E_{tag}": REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    r = run_dialogue_case(pg, f"E_{tag}", URL_W,
                                          {"day": 400, "fame": 30, "doneFlags": ["gig_1988_film_05"]}, 2)
                    r["backfillPass"] = (r["postLoad"].get("ptm") == 2)
                    if not r["backfillPass"]:
                        r["verdict"] = "FAIL"
                    REPORT["runs"][f"E_{tag}"] = r
                    print(f"== E_{tag} backfill ptm={r['postLoad'].get('ptm')} -> {'PASS' if r['backfillPass'] else 'FAIL'}", flush=True)
                except Exception as e:
                    REPORT["runs"][f"E_{tag}"] = {"error": str(e)}
                    print(f"  !! E_{tag} exception: {e}", flush=True)
                pg.close()
            # ---- pristine 對照 H：B／D（932＋700 做 B，932 做 D）----
            for vp, cases in [(viewports[0], ["B", "D"]), (viewports[1], ["B"])]:
                tag = f"{vp['width']}"
                for c in cases:
                    name = f"H{c}_pristine_{tag}"
                    pg = br.new_page(viewport=vp)
                    pg.on("pageerror", lambda e, n=name: REPORT["errors"].append(f"{n}: {e}"))
                    pg.on("response", lambda r, n=name: REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                    try:
                        cfg = {"day": 400, "fame": 30, "doneFlags": ["gig_1988_film_05"]} if c == "B" \
                            else {"day": 400, "fame": 70, "doneFlags": LEAD90_3}
                        # pristine 冇 playerTierMax：seed 唔寫呢支旗（舊檔形狀）；預期跌返 s1
                        r = run_dialogue_case(pg, name, URL_P, cfg, 1)
                        REPORT["runs"][name] = r
                    except Exception as e:
                        REPORT["runs"][name] = {"error": str(e)}
                        print(f"  !! {name} exception: {e}", flush=True)
                    pg.close()
            br.close()
    finally:
        stop(srv_w); stop(srv_p)
    with open(os.path.join(HERE, "drive195_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)
    print("pageerrors:", len(REPORT["errors"]), REPORT["errors"][:5])
    print("http_fail:", len(REPORT["http_fail"]), REPORT["http_fail"][:5])
    print("angry_http:", REPORT["angry_http"])
    for k, v in REPORT["runs"].items():
        print(k, "->", v.get("verdict", v.get("error", "?")))


if __name__ == "__main__":
    main()
