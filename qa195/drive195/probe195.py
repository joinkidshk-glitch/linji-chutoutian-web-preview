# -*- coding: utf-8 -*-
"""v195 probe: capture a real save template, test Continue flow, tea-room story trigger,
and dump map-view buttons (home path discovery). Work copy only, port 8985."""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work195"
HERE = "/home/hatch/workspace/linji-work195/qa195/drive195"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8985
URL = f"http://127.0.0.1:{PORT}/index.html"

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    st, body = http_body("index.html")
    assert st == 200
    print("serve ok sha", hashlib.sha256(body).hexdigest()[:12], flush=True)
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def click_first(pg, texts, wait=1000):
    for t in texts:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

def new_game(pg):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
    except Exception:
        pass
    click_first(pg, ["確定出發"], 1500)
    for _ in range(4):
        if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    ok = pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")
    print("NEW GAME OK:", ok, pg.evaluate("() => window.S ? (S.dayIndex + ' ' + (S.dateStr||'')) : 'no S'"), flush=True)
    return ok

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

def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 932, "height": 1500})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("response", lambda r: errs.append(f"HTTP {r.status} {r.url}") if r.status >= 400 else None)
            assert new_game(pg), "new game failed"
            dismiss_encounter(pg)
            # capture save template
            pg.evaluate("() => { if (typeof saveQ==='function') saveQ(); }")
            pg.wait_for_timeout(500)
            raw = pg.evaluate("() => localStorage.getItem('starVolunteer_map_v19w')")
            print("save len:", len(raw or ""), flush=True)
            with open(os.path.join(HERE, "save_template.json"), "w", encoding="utf-8") as f:
                f.write(raw or "")
            s = json.loads(raw)
            print("save keys:", sorted(s.keys()), flush=True)
            print("dayIndex:", s.get("dayIndex"), "fame:", s.get("fame"), "story.done:", (s.get("story") or {}).get("done"), flush=True)
            print("flags sample:", {k: v for k, v in list((s.get("flags") or {}).items())[:15]}, flush=True)
            # reload -> Continue
            pg.goto(URL); pg.wait_for_timeout(2500)
            vis = pg.evaluate("() => { const b=document.getElementById('btn-cont'); return b ? (b.offsetParent!==null) : 'missing'; }")
            print("btn-cont visible after reload:", vis, flush=True)
            pg.evaluate("() => { const b=document.getElementById('btn-cont'); if(b) b.click(); }")
            pg.wait_for_timeout(2000)
            print("after continue S:", pg.evaluate("() => window.S ? (S.dayIndex+' fame='+S.fame+' storyDone='+JSON.stringify(Object.keys(S.story.done||{}))) : 'no S'"), flush=True)
            dismiss_encounter(pg)
            # seed C1-C5 done + day 300, then tea-room trigger
            pg.evaluate("""() => {
              S.dayIndex = 300; S.fame = 30;
              S.flags = Object.assign({}, S.flags||{});
              S.flags["done_gig_1988_film_05"] = 1;
              S.story.done = Object.assign({}, S.story.done, {C1:true,C2:true,C3:true,C4:true,C5:true});
              S.story.lastMainDoneDay = 292;
              try { StoryOC.syncPhaseFromProgress(); } catch(e){}
              try { if (window.syncGigsForCalendarYear) window.syncGigsForCalendarYear(true); } catch(e){}
            }""")
            print("seeded stem:", pg.evaluate("() => (window.DLG106&&DLG106.aweiStem)?DLG106.aweiStem():'?'"), "playerTierMax:", pg.evaluate("() => S.flags.playerTierMax"), flush=True)
            # dump map buttons
            btns = pg.evaluate("""() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim().slice(0,24)).filter(Boolean).slice(0,60)""")
            print("VISIBLE BUTTONS:", json.dumps(btns, ensure_ascii=False), flush=True)
            # tea-room trigger
            pg.evaluate("""() => { const b=[...document.querySelectorAll('#v-map button')].find(x=>x.offsetParent!==null && (x.textContent||'').includes('茶餐廳')); if(b) b.click(); return !!b; }""")
            pg.wait_for_timeout(1500)
            dismiss_encounter(pg)
            pg.evaluate("""() => { const sh=document.getElementById('loc-sheet'); if(!sh) return false;
              const b=[...sh.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='返回地圖');
              if(!b) return false; b.click(); return true; }""")
            pg.wait_for_timeout(1500)
            st = pg.evaluate("""() => { const plate=document.querySelector('.story-play .dlg106-plate, .story-play .sp-plate');
              const spk=document.querySelector('.story-play .sp-speaker');
              const imgs=[...document.querySelectorAll('.dlg106-char')].map(im=>({id:im.getAttribute('data-dlg-id'),src:(im.getAttribute('src')||'').slice(0,90)}));
              return {active: !!plate, speaker: spk?spk.textContent.trim():'', line: plate?plate.textContent.replace(/\\s+/g,' ').trim().slice(0,60):'', imgs}; }""")
            print("STAGE AFTER TEA-ROOM:", json.dumps(st, ensure_ascii=False), flush=True)
            pg.screenshot(path=os.path.join(HERE, "shots", "probe_stage.png"))
            print("pageerrors/http:", errs, flush=True)
            br.close()
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
