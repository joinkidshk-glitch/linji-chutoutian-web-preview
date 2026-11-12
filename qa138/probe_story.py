# -*- coding: utf-8 -*-
"""v138r2 診斷探針：對 5 個 story 節點逐個試 StoryPlay.start，印回傳值＋頭 12 步（講者／對白／L-R 圖）。
另試芬姐送別（exodusFenFired＋返地圖）會唔會彈出。
用法：pwenv49 python qa138/probe_story.py [root]"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8972
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError("http.server died (port taken?)")
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

JS_STORY = '''() => {
  const chars = [...document.querySelectorAll('.dlg106-char')].map(im => ({
    id: im.dataset.dlgId, src: (im.getAttribute('src')||'').split('/').pop().split('?')[0] }));
  const sp = document.querySelector('.story-play');
  const speaker = document.querySelector('.story-play .sp-speaker');
  const line = document.querySelector('.story-play .sp-line');
  const choices = [...document.querySelectorAll('.sp-choice')].map(b => b.textContent.trim());
  const toast = document.querySelector('.toast, [class*="toast"]');
  return { active: !!sp, chars, speaker: speaker ? speaker.textContent : null,
           line: line ? line.textContent : null, choices,
           toast: toast ? toast.textContent.trim().slice(0, 80) : null };
}'''

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
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

def walk(pg, tag, max_steps=12):
    for step in range(max_steps):
        info = pg.evaluate(JS_STORY)
        chars = ",".join(f"{c['id']}:{c['src']}" for c in info["chars"])
        print(f"  [{tag}] step {step} active={info['active']} spk={info['speaker']} line={(info['line'] or '')[:55]} chars=[{chars}] choices={info['choices'][:2]} toast={info['toast']}", flush=True)
        if not info["active"]:
            break
        if info["choices"]:
            click_first(pg, [info["choices"][0][:8]], 1200)
            pg.wait_for_timeout(800)
            continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            print(f"  [{tag}] no next button at step {step}", flush=True)
            break
        pg.wait_for_timeout(450)

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        new_game(pg)
        print("game ready, day:", pg.evaluate("() => S.dayIndex"), flush=True)
        for node in ["R_hiu_meet", "R_xu_meet", "R_xu_ending", "F4_stay_mind", "WF4_fen_intro"]:
            ok = pg.evaluate("""(n) => {
              try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) { return 'ERR:'+_e; }
              return false; }""", node)
            print(f"== start({node}) -> {ok} ==", flush=True)
            pg.wait_for_timeout(1200)
            walk(pg, node)
            # close any leftover session
            pg.evaluate("""() => { try { const sk = document.querySelector('.e79-skip'); } catch(_e){} return true; }""")
            click_first(pg, ["返回地圖", "關閉"], 800)
            pg.wait_for_timeout(600)
        # farewell probe: arm + map return
        print("== farewell probe ==", flush=True)
        pg.evaluate("""() => { S.exodusFenFired = true; S.wf4FenFarewell = null;
          try { const st = wf4Ensure(); if (st) st.fenFarewellDone = false; } catch(_e) {}
          try { if (S.wf4) { S.wf4.pending = null; } } catch(_e) {}
          return true; }""")
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
        pg.wait_for_timeout(1500)
        walk(pg, "farewell", max_steps=14)
        print("pageerrors:", errs[:5], flush=True)
        b.close()
finally:
    stop(srv)
print("PROBE DONE")
