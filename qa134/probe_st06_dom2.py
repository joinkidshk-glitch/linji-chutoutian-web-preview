#!/usr/bin/env python3
"""v134 probe：逐單 seed WF4 事件，逐步 log 狀態，搵出 st06/set08/st04 唔觸發嘅原因。
用法：python3 qa134/probe134.py [ROOT] [ev1,ev2,...]"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright

PORT = 8969
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/linji-work134")
EVS = ["wf4_ev_st06"]

def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)

def click_vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false;
      vis[0].click(); return true;
    }""", text)

def state(pg):
    return pg.evaluate("""() => {
      const h = document.querySelector('#modal h3');
      const btns = [...document.querySelectorAll('#modal-btns button')].map(b => b.textContent.trim());
      return {
        day: (typeof S!=='undefined' && S) ? S.dayIndex : null,
        pending: (typeof S!=='undefined' && S && S.wf4) ? S.wf4.pending : null,
        pendingDay: (typeof S!=='undefined' && S && S.wf4) ? S.wf4.pendingDay : null,
        lastDay: (typeof S!=='undefined' && S && S.wf4) ? S.wf4.lastDay : null,
        tier: (typeof wf4Tier==='function') ? wf4Tier() : null,
        h3: h ? h.textContent : '',
        modalBtns: btns,
        hasOverDay: [...document.querySelectorAll('button')].some(b => (b.textContent||'').includes('過一日') && b.getBoundingClientRect().width > 0),
        hasStartPlan: [...document.querySelectorAll('button')].some(b => (b.textContent||'').includes('開始今日行程') && b.getBoundingClientRect().width > 0),
        hasReturnMap: [...document.querySelectorAll('button')].some(b => (b.textContent||'').includes('返回地圖') && b.getBoundingClientRect().width > 0),
      };
    }""")

def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            btn.click(timeout=1000)
            return True
    except Exception:
        pass
    return False

def wait_on_map(pg, secs=60):
    for _ in range(int(secs / 0.7)):
        if vis_btn(pg, "過一日"):
            return True
        if not dismiss_once(pg):
            if not click_vis_btn(pg, "返回地圖"):
                pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    return False

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
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
        print("after new game:", json.dumps(state(pg), ensure_ascii=False))
        if not wait_on_map(pg):
            print("FATAL: 未到地圖"); sys.exit(2)
        print("on_map:", json.dumps(state(pg), ensure_ascii=False))
        for ev in EVS:
            print(f"===== {ev} =====")
            # 確保過一日可見（可能要先撳開始今日行程）
            for _ in range(30):
                if vis_btn(pg, "過一日"):
                    break
                if click_vis_btn(pg, "開始今日行程"):
                    pg.wait_for_timeout(1000)
                    print("  clicked 開始今日行程 ->", json.dumps(state(pg), ensure_ascii=False))
                    continue
                if not dismiss_once(pg):
                    if not click_vis_btn(pg, "返回地圖"):
                        pg.wait_for_timeout(500)
                pg.wait_for_timeout(700)
            print("  before seed:", json.dumps(state(pg), ensure_ascii=False))
            pg.evaluate("""(ev) => {
                if (!S.wf4) S.wf4 = {lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false};
                S.wf4.pending = ev; S.wf4.pendingDay = S.dayIndex|0; S.wf4.lastDay = -99;
            }""", ev)
            print("  after seed:", json.dumps(state(pg), ensure_ascii=False))
            click_vis_btn(pg, "過一日")
            title = {"wf4_ev_st06": "魚檔阿姐", "wf4_ev_set08": "派錯更去錯廠", "wf4_ev_st04": "最後一杯紅豆冰"}.get(ev, ev)
            found = False
            for i in range(45):
                pg.wait_for_timeout(1000)
                st = state(pg)
                print(f"  t+{i+1}s:", json.dumps(st, ensure_ascii=False))
                if title in st["h3"]:
                    found = True
                    break
                # 確認過一日 modal：明確撳「確定過一日」
                if st["h3"] == "確認過一日？":
                    if click_vis_btn(pg, "確定過一日"):
                        print("  clicked 確定過一日")
                        continue
                dismiss_once(pg)
            print(f"  FOUND={found}")
            pg.screenshot(path=f"/tmp/probe134_{ev}.png")
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
                print("DOM DUMP:"); print(dump)
            # 撳晒成單返地圖
            for _ in range(40):
                if vis_btn(pg, "過一日") or vis_btn(pg, "開始今日行程"):
                    break
                if not dismiss_once(pg):
                    if not click_vis_btn(pg, "返回地圖"):
                        pg.wait_for_timeout(500)
                pg.wait_for_timeout(700)
        b.close()
finally:
    srv.terminate()
print("probe done")
