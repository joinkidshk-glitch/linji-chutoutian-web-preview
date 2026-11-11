# -*- coding: utf-8 -*-
"""v20a102 FX102 實駕（新局版）：訓練甲/乙/丙＋全日休息。
主駕駛 drive_fx 逐場景連跑嗰陣，訓練日俾多場景狀態干擾（週計劃
已啟動後改植唔咬），所以呢四種喺新局逐個驗：改植今日計劃 →
提早休息確認撳取消 → 頁面「開始今日行程」→ 日結板驗片。
用法：python drive_fx2.py <port>
"""
import sys
from playwright.sync_api import sync_playwright

PORT = sys.argv[1] if len(sys.argv) > 1 else "8102"
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
OUT = "/home/hatch/workspace/linji-work102/qa102/out"
R = []

def ok(cond, msg):
    R.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + msg, flush=True)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 430, "height": 932})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    def mask_on():
        return pg.evaluate("!!document.querySelector('#mask.on')")

    def video_info():
        return pg.evaluate("""() => {
          const v = document.getElementById('act-fx102-video') ||
                    document.getElementById('rest-sleep-video');
          if(!v) return null;
          return { id: v.id, src: v.getAttribute('src'),
                   paused: v.paused, t: v.currentTime };
        }""")

    def head():
        return pg.evaluate("""() => { const mi = document.getElementById('modal-inner');
          return mi ? (mi.textContent || '').slice(0, 60) : ''; }""")

    def click_text(scope, t):
        loc = pg.locator(f"{scope} button", has_text=t)
        try:
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                return True
        except Exception:
            pass
        return False

    def run_until_video(expect_file, max_steps=30):
        for _ in range(max_steps):
            v = video_info()
            if v and expect_file in (v["src"] or ""):
                return v
            if mask_on():
                h = head()
                if "提早休息" in h or "加速本週剩餘？" in h:
                    click_text("#modal-btns", "取消")
                    pg.wait_for_timeout(900)
                    continue
                done = False
                for t in ["開始今日行程", "開始", "確定", "繼續", "下一步",
                          "知道了", "收下", "好", "完成"]:
                    if click_text("#modal-btns", t):
                        done = True
                        break
                if not done:
                    pg.evaluate("""() => {
                      const bs = [...document.querySelectorAll('#modal-btns button')]
                        .filter(x => !(x.textContent || '').includes('加速'));
                      if(bs.length) bs[0].click(); }""")
                pg.wait_for_timeout(1300)
                continue
            if pg.evaluate("!!document.querySelector('#enc79-overlay')"):
                loc = pg.locator("#enc79-overlay button")
                if loc.count():
                    try:
                        loc.last.click()
                    except Exception:
                        pass
                pg.wait_for_timeout(600)
                continue
            if click_text("body", "開始今日行程"):
                pg.wait_for_timeout(1500)
                continue
            pg.evaluate("() => { const b = document.querySelector('#map-end-day'); if(b) b.click(); }")
            pg.wait_for_timeout(1600)
        return video_info()

    def dismiss(maxn=10):
        for _ in range(maxn):
            if not mask_on():
                return
            h = head()
            if "加速本週剩餘？" in h:
                click_text("#modal-btns", "取消")
                pg.wait_for_timeout(700)
                continue
            done = False
            for t in ["返回地圖", "確定", "繼續", "下一步", "知道了", "收下",
                      "好", "完成"]:
                if click_text("#modal-btns", t):
                    done = True
                    break
            if not done:
                clicked = pg.evaluate("""() => {
                  const bs = [...document.querySelectorAll('#modal-btns button')]
                    .filter(x => !(x.textContent || '').includes('加速'));
                  if(bs.length){ bs[0].click(); return true; } return false; }""")
                if not clicked:
                    return
            pg.wait_for_timeout(700)

    def scenario(name, plan_id, expect_file):
        dismiss()
        pg.evaluate(f"""() => {{
          const today = S.dayIndex|0;
          const wd = new Date(1990, 0, 1 + today).getDay();
          const slot = (wd + 6) % 7;
          S.weekPlan = ['rest','rest','rest','rest','rest','rest','rest'];
          S.weekPlan[slot] = '{plan_id}';
        }}""")
        v = run_until_video(expect_file)
        ok(v is not None and expect_file in (v["src"] or ""),
           f"{name}：日結板出啱片（{v and v['src']}）")
        if v:
            pg.wait_for_timeout(800)
            v2 = video_info()
            ok(v2 and (not v2["paused"]) and v2["t"] > v["t"],
               f"{name}：真係播緊（t {v['t']:.2f}→{v2 and v2['t']:.2f}）")
        pg.screenshot(path=f"{OUT}/{name}.png")
        dismiss()

    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(2000)
    pg.click("#btn-new")
    pg.wait_for_timeout(1200)
    try:
        pg.click("text=跳過教學", timeout=3000)
        pg.wait_for_timeout(600)
    except Exception as e:
        print("skip tutorial:", e)
    dismiss()
    pg.evaluate("() => { S.money = (S.money||0) + 200000; }")

    scenario("05_train_a", "train_acting", "fx_train_a.mp4")
    scenario("06_train_b", "train_vocal", "fx_train_b.mp4")
    scenario("07_train_c", "train_stamina", "fx_train_c.mp4")
    scenario("08_rest", "rest", "fx_rest.mp4")

    ok(not errs, f"全程冇 pageerror（{errs[:2]}）")
    print(f"drive_fx2: {sum(R)}/{len(R)} PASS")
    b.close()
