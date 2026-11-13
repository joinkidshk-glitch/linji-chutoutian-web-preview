# -*- coding: utf-8 -*-
"""v199 B1 probe: measure dialogue-stage geometry per Awei tier/partner BEFORE fix.
Serve work199, seed tiers, synthetic StoryPlay beats, measure rects (DOM evidence)."""
import os, json, subprocess, time, signal, hashlib, urllib.request, copy, sys
from playwright.sync_api import sync_playwright

REPO = "/home/hatch/workspace/linji-work199"
HERE = "/home/hatch/workspace/linji-work199/qa199"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8999
URL = f"http://127.0.0.1:{PORT}/index.html"
SAVE_KEY = "starVolunteer_map_v19w"
with open("/home/hatch/workspace/linji-work195/qa195/drive195/save_template.json", encoding="utf-8") as f:
    TEMPLATE = json.load(f)
REPORT = {"errors": [], "http_fail": [], "runs": {}}

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

def story_next(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")

MEASURE_JS = """() => {
  const st = document.querySelector('.story-play .sp-stage') || document.querySelector('.story-play');
  const chars = [...document.querySelectorAll('.story-play .dlg106-char')].map(im=>{
    const r = im.getBoundingClientRect(); const cs = getComputedStyle(im);
    return {id: im.getAttribute('data-dlg-id'), src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
      x: Math.round(r.x*10)/10, y: Math.round(r.y*10)/10, w: Math.round(r.width*10)/10, h: Math.round(r.height*10)/10,
      natW: im.naturalWidth, natH: im.naturalHeight, ar: Math.round(im.naturalWidth/im.naturalHeight*1000)/1000,
      cssH: cs.height, cssW: cs.width, cssMaxW: cs.maxWidth, inlineH: im.style.height||'', inlineW: im.style.width||'', inlineMaxW: im.style.maxWidth||''};});
  const plate = document.querySelector('.story-play .dlg106-plate, .story-play .sp-plate');
  const pr = plate ? plate.getBoundingClientRect() : null;
  const sr = st ? st.getBoundingClientRect() : null;
  const charsBox = document.querySelector('.story-play .dlg106-chars');
  const cr = charsBox ? charsBox.getBoundingClientRect() : null;
  let gap = null;
  if (chars.length >= 2) { const a = chars[0], b = chars[1]; gap = Math.round((Math.min(a.x+b.w, b.x+b.w) - Math.max(a.x, b.x))*10)/10; }
  return {stage: sr ? {x: Math.round(sr.x), y: Math.round(sr.y), w: Math.round(sr.width), h: Math.round(sr.height), cw: st.clientWidth, ch: st.clientHeight, sw: st.scrollWidth, varH: st.style.getPropertyValue('--dlg108-char-h')||getComputedStyle(st).getPropertyValue('--dlg108-char-h')} : null,
    charsBox: cr ? {x: Math.round(cr.x), y: Math.round(cr.y), w: Math.round(cr.width), h: Math.round(cr.height)} : null,
    chars, plate: pr ? {x: Math.round(pr.x), y: Math.round(pr.y), w: Math.round(pr.width), h: Math.round(pr.height)} : null,
    docScrollW: document.documentElement.scrollWidth, winW: window.innerWidth}; }"""

def build_save(cfg):
    s = copy.deepcopy(TEMPLATE)
    s["dayIndex"] = cfg["day"]; s["fame"] = cfg["fame"]
    s["flags"] = dict(s.get("flags") or {})
    for k in list(s["flags"].keys()):
        if k.startswith("done_"): del s["flags"][k]
    for gid in cfg.get("doneFlags", []): s["flags"]["done_" + gid] = 1
    s["flags"]["playerTierMax"] = cfg.get("playerTierMax", 0)
    s["story"] = dict(s.get("story") or {})
    s["story"]["done"] = {c: True for c in ["C1","C2","C3","C4","C5"]}
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
    return {"contClicked": clicked, "stem": pg.evaluate("() => { try { return DLG106.aweiStem(); } catch(e){ return '?'; } }")}

PARTNERS = {"ho_sang": ("何生", "ho_sang"), "vera": ("Vera", "vera"), "fong_siulung": ("方小龍", "fong_siulung"), "gu_mingfai": ("顧明輝", "gu_mingfai")}

def run_beat(pg, partner_id, emotion, line):
    pname, pid = PARTNERS[partner_id]
    pg.evaluate("""() => { const s = window.StoryPlay && StoryPlay.session; if (s && StoryPlay.abort) { try { StoryPlay.abort(); } catch(e){} } }""")
    pg.wait_for_timeout(400)
    ok = pg.evaluate("""(a) => { try {
      return !!StoryPlay.start({id:'T199_PROBE', title:'199 probe', locId:'tvb_longmen', beats:[
        {speaker:a[2], speakerId:a[1], kind:'npc', lines:['你話呢場戲點收科？']},
        {speaker:'阿偉', speakerId:'player', kind:'player', emotion:a[0], lines:[a[3]]}
      ], choices:[{id:'t199_ok', label:'（驗證用，繼續）'}]}, {force:true});
    } catch(e){ return 'err:'+e; } }""", [emotion, pid, pname, line])
    pg.wait_for_timeout(1200)
    dismiss_encounter(pg)
    st1 = pg.evaluate(MEASURE_JS)
    adv = story_next(pg); pg.wait_for_timeout(900)
    dismiss_encounter(pg)
    st2 = pg.evaluate(MEASURE_JS)
    pg.evaluate("""() => { const s = window.StoryPlay && StoryPlay.session; if (s && StoryPlay.abort) { try { StoryPlay.abort(); } catch(e){} } }""")
    pg.wait_for_timeout(300)
    return {"startOk": ok, "beat1": st1, "beat2": st2}

def main():
    srv = serve(REPO, PORT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            vp = {"width": 932, "height": 1500}
            cases = [
                ("s1_ho_base", {"day":0,"fame":5,"doneFlags":[],"playerTierMax":0}, "ho_sang", "base", "記住，呢行最緊要係準時。"),
                ("s2_ho_base", {"day":400,"fame":30,"doneFlags":["gig_1988_film_05"],"playerTierMax":2}, "ho_sang", "base", "記住，呢行最緊要係準時。"),
                ("s3_ho_base", {"day":400,"fame":70,"doneFlags":["gig_1988_film_05","gig_1988_film_06","gig_1988_film_07"],"playerTierMax":3}, "ho_sang", "base", "記住，呢行最緊要係準時。"),
                ("s1_ho_angry", {"day":0,"fame":5,"doneFlags":[],"playerTierMax":0}, "ho_sang", "angry", "夠啦！呢場戲唔係咁拍㗎！"),
                ("s2_ho_angry", {"day":400,"fame":30,"doneFlags":["gig_1988_film_05"],"playerTierMax":2}, "ho_sang", "angry", "夠啦！呢場戲唔係咁拍㗎！"),
                ("s3_ho_angry", {"day":400,"fame":70,"doneFlags":["gig_1988_film_05","gig_1988_film_06","gig_1988_film_07"],"playerTierMax":3}, "ho_sang", "angry", "夠啦！呢場戲唔係咁拍㗎！"),
                ("s1_vera_base", {"day":0,"fame":5,"doneFlags":[],"playerTierMax":0}, "vera", "base", "記住，呢行最緊要係準時。"),
                ("s2_vera_base", {"day":400,"fame":30,"doneFlags":["gig_1988_film_05"],"playerTierMax":2}, "vera", "base", "記住，呢行最緊要係準時。"),
                ("s3_fong_base", {"day":400,"fame":70,"doneFlags":["gig_1988_film_05","gig_1988_film_06","gig_1988_film_07"],"playerTierMax":3}, "fong_siulung", "base", "記住，呢行最緊要係準時。"),
                ("s1_fong_base", {"day":0,"fame":5,"doneFlags":[],"playerTierMax":0}, "fong_siulung", "base", "記住，呢行最緊要係準時。"),
                ("s2_gu_base", {"day":400,"fame":30,"doneFlags":["gig_1988_film_05"],"playerTierMax":2}, "gu_mingfai", "base", "記住，呢行最緊要係準時。"),
            ]
            for name, cfg, partner, emo, line in cases:
                pg = br.new_page(viewport=vp)
                pg.on("pageerror", lambda e, n=name: REPORT["errors"].append(f"{n}: {e}"))
                pg.on("response", lambda r, n=name: REPORT["http_fail"].append(f"{n} {r.status} {r.url}") if r.status >= 400 else None)
                try:
                    post = load_seeded_save(pg, cfg)
                    res = run_beat(pg, partner, emo, line)
                    REPORT["runs"][name] = {"post": post, "res": res}
                    b2 = res["beat2"]
                    ch = [(c["id"], c["src"], c["w"], c["h"]) for c in b2["chars"]]
                    print(f"== {name} stem={post['stem']} stage={b2['stage']} chars={ch} plate={b2['plate']}", flush=True)
                except Exception as e:
                    REPORT["runs"][name] = {"error": str(e)}
                    print(f"  !! {name}: {e}", flush=True)
                pg.close()
            br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "probe199_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)
    print("pageerrors:", len(REPORT["errors"]), REPORT["errors"][:5])
    print("http_fail:", len(REPORT["http_fail"]), REPORT["http_fail"][:5])

if __name__ == "__main__":
    main()
