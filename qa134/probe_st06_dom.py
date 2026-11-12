#!/usr/bin/env python3
"""probe st06 card-layout DOM：seed st06 → 過一日 → 等事件 modal → dump #modal 結構（睇卡片版式用咩 selector 擺場景圖）。"""
import subprocess, sys, time, os
PORT = 8968
ROOT = os.path.expanduser("~/workspace/linji-work134")
srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell")
        pg = b.new_page(viewport={"width": 430, "height": 700})
        pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1")
        pg.wait_for_timeout(1500)
        pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000)
        pg.wait_for_timeout(1000)
        try:
            pg.locator('[data-slot="3"]').first.click(timeout=1500)
            pg.wait_for_timeout(800)
        except Exception:
            pass
        for _ in range(10):
            try:
                pg.get_by_text("跳過教學", exact=True).first.click(timeout=1200)
                pg.wait_for_timeout(600)
                break
            except Exception:
                try:
                    pg.get_by_text("下一步", exact=True).first.click(timeout=1200)
                    pg.wait_for_timeout(600)
                except Exception:
                    break
        pg.wait_for_timeout(1200)
        # 入地圖：dismiss intro modal（去事務所／寫手帳）直到「過一日」出現
        def _vis(t):
            return pg.evaluate("""(t) => [...document.querySelectorAll('button')].some(b => (b.textContent||'').includes(t) && b.getBoundingClientRect().width > 0 && b.getBoundingClientRect().height > 0)""", t)
        def _click(t):
            return pg.evaluate("""(t) => {
              const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
              const vis = bs.filter(b => { const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
              if (!vis.length) return false; vis[0].click(); return true;
            }""", t)
        for _ in range(85):
            if _vis("過一日"):
                break
            try:
                btn = pg.locator('#modal-btns button').first
                if btn.is_visible(timeout=400):
                    btn.click(timeout=1000)
                    pg.wait_for_timeout(700)
                    continue
            except Exception:
                pass
            if not _click("返回地圖"):
                pg.wait_for_timeout(500)
            pg.wait_for_timeout(700)
        print("on_map:", _vis("過一日"))
        pg.evaluate("""() => {
            if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
            S.wf4.pending = 'wf4_ev_st06'; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
        }""")
        pg.evaluate("""() => {
          const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes('過一日'));
          const vis = bs.filter(b => { const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
          if (vis.length) vis[0].click();
        }""")
        found = False
        for _ in range(60):
            pg.wait_for_timeout(1000)
            h3 = pg.evaluate("() => { const h = document.querySelector('#modal h3'); return h ? h.textContent : ''; }")
            if "魚檔阿姐" in h3:
                found = True
                break
            if h3 == "確認過一日？":
                pg.evaluate("""() => {
                  const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes('確定過一日'));
                  const vis = bs.filter(b => { const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
                  if (vis.length) vis[0].click();
                }""")
            elif h3.startswith("小休"):
                pg.evaluate("""() => {
                  const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes('返回地圖'));
                  const vis = bs.filter(b => { const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
                  if (vis.length) vis[0].click();
                }""")
            else:
                try:
                    btn = pg.locator('#modal-btns button').first
                    if btn.is_visible(timeout=400):
                        btn.click(timeout=1000)
                except Exception:
                    pass
        print("found:", found)
        if found:
            pg.wait_for_timeout(800)
            dump = pg.evaluate("""() => {
              const m = document.querySelector('#modal');
              if (!m) return 'NO #modal';
              const out = {h3: (m.querySelector('h3')||{}).textContent || '',
                           modalClass: m.className, innerClass: (document.querySelector('#modal-inner')||{}).className || '',
                           imgs: [...m.querySelectorAll('img')].map(i => ({src: (i.getAttribute('src')||'').slice(0,120), cls: i.className})),
                           bgEls: [...m.querySelectorAll('*')].filter(e => { const bi = getComputedStyle(e).backgroundImage; return bi && bi.indexOf('url(') !== -1; }).map(e => ({tag: e.tagName, cls: e.className, bg: getComputedStyle(e).backgroundImage.slice(0,160)})),
                           firstKids: [...m.children].slice(0,6).map(e => e.tagName + '.' + (e.className||'').toString().slice(0,80)),
                           htmlHead: m.innerHTML.slice(0, 1200)};
              return JSON.stringify(out, null, 1);
            }""")
            print(dump)
        b.close()
finally:
    srv.terminate()
print("probe done")
