# -*- coding: utf-8 -*-
"""probe e_lok_T0 重演：lok met/fav0/stage0 @ 星河，逐日 dump：
  S.dayIndex、S.starDay.day／presence、overlay、location title、travel114。"""
import sys, os, subprocess, time, signal, json
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8974
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def click_first(pg, texts, wait=900):
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

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=ROOT,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", str(e)[:300], flush=True))
        pg.on("console", lambda m: print("CONSOLE", m.type, str(m.text)[:200], flush=True) if m.type in ("error", "warning") else None)
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
        for day in range(0, 6):
            pg.evaluate("""() => {
              S.stars = S.stars || {};
              const st = S.stars.lok_gasing || (S.stars.lok_gasing = {});
              st.met = true; st.fav = 0; st.stage = 0; st.beatsDone = {}; st.poolSeen = {};
              st.heartDone = false; st.wrapEcho = false; st.capHit = false; st.lastDay = -99;
              st.homeVisits = 0; st.homeVisitDay = -1; S.fame = 0; return true; }""")
            pg.evaluate("(d) => { S.dayIndex = d; }", day)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 700)
            r = click_first(pg, ["星河"], 1500)
            pg.wait_for_timeout(800)
            st = pg.evaluate("""() => {
              const btns=[...document.querySelectorAll('button')].filter(b=>(b.textContent||'').includes('星河'));
              const b0=btns[0];
              let cover=null;
              if(b0){ const r=b0.getBoundingClientRect(); const el=document.elementFromPoint(r.x+r.width/2, r.y+r.height/2); cover = el ? (el.tagName+'.'+(el.className||'').toString().slice(0,60)+' text='+(el.textContent||'').slice(0,30)) : 'none'; }
              const layers=[...document.querySelectorAll('body > div')].filter(d=>{ const cs=getComputedStyle(d); return cs.position==='fixed' && d.offsetParent!==null; }).map(d=> d.id+'/'+(d.className||'').toString().slice(0,40)+' z='+getComputedStyle(d).zIndex+' disp='+getComputedStyle(d).display);
              return {
              day: S.dayIndex,
              starDay: S.starDay ? {day: S.starDay.day, triggered: S.starDay.triggered, doneToday: S.starDay.doneToday} : null,
              travel: S.travel114 || null,
              overlay: !!document.getElementById('enc79-overlay'),
              storyPlay: !!document.querySelector('.story-play'),
              storyLine: (document.querySelector('.story-play .sp-line')||{}).textContent || null,
              storySpeaker: (document.querySelector('.story-play .sp-speaker')||{}).textContent || null,
              title: (document.querySelector('#loc-title')||{}).textContent || null,
              coverAtPin: cover, layers: layers,
              sheetCls: (document.getElementById('loc-sheet')||{}).className || null,
              wf4pending: (S.wf4||{}).pending || null,
              visBtns: [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => (b.textContent||'').trim().slice(0,20)).slice(0, 14),
            }}""")
            print(f"day {day} click->{r} " + json.dumps(st, ensure_ascii=False))
            # 若有 overlay，行兩步再關（模擬 walker 會撳走佢）
            for _ in range(3):
                ov = pg.evaluate("() => !!document.getElementById('enc79-overlay')")
                if not ov:
                    break
                pg.evaluate("""() => {
                  const chs = [...document.querySelectorAll('.e79-choice')].filter(b => b.offsetParent !== null);
                  if (chs.length) { chs[0].click(); return; }
                  const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null && !b.classList.contains('e79-skip'));
                  if (nb) { nb.click(); return; }
                  const sk = document.querySelector('.e79-skip'); if (sk) sk.click(); }""")
                pg.wait_for_timeout(400)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 700)
        b.close()
finally:
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE DONE")
