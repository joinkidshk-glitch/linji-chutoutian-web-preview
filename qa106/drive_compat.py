# -*- coding: utf-8 -*-
"""v20a106 舊檔相容實駕：v105（pristine b6e90ec 鏡像）開局→寫標記→saveToSlot(3)，
   同一瀏覽器 context／同一 origin 換 v106 線上鏡像伺服器→繼續→驗證狀態還原。
   證明 v105 存檔結構喺 v106 原封載入得返，冇爛。"""
import os, json, subprocess, time, signal
from playwright.sync_api import sync_playwright

EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8932
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107"
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
res = {}

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    return p

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

srv = serve("/tmp/mirror105")
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        # ---- Phase 1: v105 開局＋寫標記＋存槽 3 ----
        pg.goto(URL); pg.wait_for_timeout(3000)
        click_first(pg, ["新遊戲"], 1500)
        click_first(pg, ["跳過教學"], 1200)
        click_first(pg, ["開始寫手帳"], 1400)
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception:
            pass
        for i in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        ok1 = pg.evaluate("""() => {
          if (!(window.S && typeof window.S.dayIndex === 'number')) return 'noS';
          window.S.money = 106106;
          window.S.dayIndex = 3;
          window.S.flags = window.S.flags || {};
          window.S.flags.qa106mark = 'v105-slot3';
          return 'marked';
        }""")
        # 經真 UI 存槽 3：☰ 選單 → 存檔 → [data-slot="3"]
        click_first(pg, ["☰"], 900)
        pg.evaluate("() => { const b = document.querySelector('[data-m=\"save\"]'); if (b) b.click(); }")
        pg.wait_for_timeout(1200)
        saved = pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (!b) return 'nobtn'; b.click(); return 'clicked'; }""")
        pg.wait_for_timeout(1000)
        # 若有覆蓋確認 modal 就確認
        click_first(pg, ["覆蓋", "確定", "確認"], 900)
        res["saveToSlot3_v105"] = ok1 + "/" + str(saved)
        chk = pg.evaluate("""() => { const r = localStorage.getItem('starVolunteer_map_v19w_slot3');
          if (!r) return null; const o = JSON.parse(r);
          return { money: o.money, dayIndex: o.dayIndex, mark: o.flags && o.flags.qa106mark }; }""")
        res["slot3_written"] = chk
        print("v105 saveToSlot:", ok1, "slot3:", chk)
        pg.screenshot(path=f"{SHOTS}/compat_v105_saved.png")
        # ---- Phase 2: 換 v106 鏡像（同 origin）→ 繼續 ----
        srv.terminate(); srv.wait(timeout=5)
        srv = serve("/tmp/mirror106")
        pg.goto(URL); pg.wait_for_timeout(2800)
        cont_visible = pg.evaluate("() => { const b = document.getElementById('btn-cont'); return !!b && b.style.display !== 'none' && b.offsetParent !== null; }")
        res["continue_visible_v106"] = cont_visible
        print("v106 繼續掣可見:", cont_visible)
        try:
            pg.locator("#btn-cont").click(timeout=4000)
        except Exception as e:
            print("btn-cont click fail:", str(e)[:120])
        pg.wait_for_timeout(2500)
        for i in range(3):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 800):
                break
        st = pg.evaluate("""() => { if (!(window.S && typeof window.S.dayIndex === 'number')) return null;
          return { money: window.S.money, dayIndex: window.S.dayIndex,
                   mark: window.S.flags && window.S.flags.qa106mark }; }""")
        res["restored_v106"] = st
        print("v106 restored:", st)
        pg.screenshot(path=f"{SHOTS}/compat_v106_restored.png")
        res["pageerrors"] = errs[:6]
        res["PASS"] = bool(chk and chk.get("money") == 106106 and chk.get("dayIndex") == 3
                           and st and st.get("money") == 106106 and st.get("dayIndex") == 3
                           and st.get("mark") == "v105-slot3" and not errs)
        print("COMPAT:", "PASS" if res["PASS"] else "FAIL", "errors:", errs[:3])
        b.close()
finally:
    try:
        srv.terminate()
    except Exception:
        pass
with open(os.path.join(HERE, "compat_log.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("DONE", res.get("PASS"))
