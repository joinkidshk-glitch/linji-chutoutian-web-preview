# probe: serve 工作副本，開新遊戲，查 live gig 資料（ad_lead／ad_support／rec_album 嘅 pay／stars）
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work188"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 18891

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE)
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"http://127.0.0.1:{PORT}/index.html")
        pg.wait_for_timeout(3500)
        # 新遊戲（copy drive186）
        for t in ["新遊戲"]:
            try:
                pg.locator("button:has-text('" + t + "')").first.click(timeout=3000)
                pg.wait_for_timeout(1500)
            except Exception as e:
                print("click fail", t, e)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        for t in ["覆蓋", "確定", "確認"]:
            try:
                pg.locator("button:has-text('" + t + "')").first.click(timeout=900)
                pg.wait_for_timeout(900)
            except Exception:
                pass
        for t in ["跳過教學", "開始寫手帳"]:
            try:
                pg.locator("button:has-text('" + t + "')").first.click(timeout=1200)
                pg.wait_for_timeout(1200)
            except Exception:
                pass
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000)
            pg.wait_for_timeout(1200)
        except Exception:
            pass
        for t in ["確定出發"]:
            try:
                pg.locator("button:has-text('" + t + "')").first.click(timeout=1500)
                pg.wait_for_timeout(1500)
            except Exception:
                pass
        for _ in range(4):
            try:
                pg.locator("button:has-text('確定')").first.click(timeout=900)
                pg.wait_for_timeout(900)
            except Exception:
                break
        print("S ready:", pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"))
        out = pg.evaluate("""() => {
          const all = [];
          const seen = {};
          const push = (g) => { if (g && g.id && !seen[g.id]) { seen[g.id] = true; all.push(g); } };
          try { (typeof GIGS !== 'undefined' ? GIGS : []).forEach(push); } catch(e) {}
          try {
            const by = (typeof STORY_WIRE !== 'undefined' && STORY_WIRE && STORY_WIRE.gigsByYear) || {};
            Object.keys(by).forEach(y => { const gs = by[y] && by[y].gigs; if (Array.isArray(gs)) gs.forEach(push); });
          } catch(e2) {}
          const pick = (pred, n) => all.filter(pred).slice(0, n).map(g => ({ id: g.id, type: g.type, roleScale: g.roleScale, roleLabel: g.roleLabel, pay: g.pay, payExact: g.payExact || null, stars: g.stars || null, year: g.year || null }));
          return {
            total: all.length,
            ad_lead: pick(g => g.type === '廣告' && g.roleScale === 'ad_lead', 8),
            ad_support: pick(g => g.type === '廣告' && g.roleScale === 'ad_support', 4),
            ad_extra: pick(g => g.type === '廣告' && g.roleScale === 'ad_extra_day', 4),
            rec_album: pick(g => g.type === '唱片通告' && g.roleScale === 'rec_album', 6),
            film_lead: pick(g => g.type === '電影' && (g.roleScale === 'film_lead_big' || g.roleScale === 'film_second_lead') && /男主角/.test(String(g.roleLabel || '')) && !/替身/.test(String(g.roleLabel || '')), 6),
            film_sup: pick(g => g.type === '電影' && /support/.test(String(g.roleScale || '')) && /配角/.test(String(g.roleLabel || '')) && !/替身/.test(String(g.roleLabel || '')), 6),
            tv_lead: pick(g => g.type === '電視劇' && String(g.roleLabel || '') === '男主角', 6),
            tv_sup: pick(g => g.type === '電視劇' && /配角/.test(String(g.roleLabel || '')), 6),
          };
        }""")
        print(json.dumps(out, ensure_ascii=False, indent=1))
        print("pageerrors:", errs[:3])
        ctx.close()
        b.close()
finally:
    srv.terminate()
