# -*- coding: utf-8 -*-
"""drive126 探針：StoryPlay.start('A_fong_push1') 之後 DOM 實際狀態。"""
import subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work126"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8952
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=ROOT,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(3000)
        for t in ["新遊戲"]:
            try:
                pg.locator(f"button:has-text('{t}')").first.click(timeout=2000)
            except Exception as e:
                print("click fail", t, e)
            pg.wait_for_timeout(1500)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) b.click(); }""")
        pg.wait_for_timeout(1200)
        for t in ["覆蓋", "確定", "確認"]:
            try:
                pg.locator(f"button:has-text('{t}')").first.click(timeout=900)
            except Exception:
                pass
            pg.wait_for_timeout(700)
        for t in ["跳過教學", "開始寫手帳"]:
            try:
                pg.locator(f"button:has-text('{t}')").first.click(timeout=900)
            except Exception:
                pass
            pg.wait_for_timeout(1000)
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000)
        except Exception:
            pass
        pg.wait_for_timeout(1200)
        for t in ["確定出發"]:
            try:
                pg.locator(f"button:has-text('{t}')").first.click(timeout=900)
            except Exception:
                pass
            pg.wait_for_timeout(1200)
        print("S ok:", pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"))
        # go to 星河電視台 (tvb_longmen) first, then start
        for t in ["星河電視台"]:
            try:
                pg.locator(f"button:has-text('{t}')").first.click(timeout=3000)
            except Exception as e:
                print("loc click fail", e)
            pg.wait_for_timeout(2000)
        print("at loc:", pg.evaluate("() => (S && S.loc) || (S && S.currentLoc) || '?'"))
        pg.evaluate("""() => { S.story = S.story || {}; S.story.phase = "P2"; }""")
        print("homeEditable:", pg.evaluate("() => S.homeEditable"))
        r = pg.evaluate("""() => {
          const out = {};
          try { out.findNode = !!StoryOC.findNode('A_fong_push1'); } catch(e){ out.findNodeErr = String(e); }
          try { out.findNodeLan = !!StoryOC.findNode('R_lan_meet'); } catch(e){ out.findNodeLanErr = String(e); }
          try { out.startFong = StoryPlay.start('A_fong_push1', {force:true}); } catch(e){ out.startErr = String(e); }
          try { out.toastAfter = (document.querySelector('.toast')||{}).textContent; } catch(e){}
          return out;
        }""")
        print("start result:", r)
        pg.wait_for_timeout(2500)
        dom = pg.evaluate("""() => {
          const q = (s) => { const el = document.querySelector(s); return el ? { cls: el.className, txt: (el.textContent||'').slice(0,150) } : null; };
          return {
            storyPlay: q('.story-play'),
            spSpeaker: q('.story-play .sp-speaker'),
            spLine: q('.story-play .sp-line'),
            dlgChars: [...document.querySelectorAll('.dlg106-char')].map(im=>({id: im.dataset.dlgId, src: (im.getAttribute('src')||'').split('/').pop()})),
            modalBtns: q('#modal-btns'),
            modalBtnsList: [...document.querySelectorAll('#modal-btns button')].map(b=>b.textContent.trim().slice(0,30)),
            toast: q('.toast'),
            storyDlg: q('#story-dlg'),
            spWrap: q('.sp-wrap'),
            bodyTxt: (document.body.innerText||'').slice(0,400),
          };
        }""")
        print("DOM:", dom)
        pg.screenshot(path="/tmp/probe_fong.png")
        print("pageerrors:", errs)
        b.close()
finally:
    srv.send_signal(signal.SIGTERM)
print("DONE")
