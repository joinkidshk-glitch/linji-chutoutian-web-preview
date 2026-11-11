# -*- coding: utf-8 -*-
"""FX102 debug：逐步睇改植拍攝日之後嘅流程狀態。"""
import sys
from playwright.sync_api import sync_playwright

PORT = "8102"
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
OUT = "/home/hatch/workspace/linji-work102/qa102/out"

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 430, "height": 932})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    def state(tag):
        s = pg.evaluate("""() => {
          const v = document.getElementById('act-fx102-video');
          const mi = document.getElementById('modal-inner');
          return {
            day: (typeof S !== 'undefined') ? (S.dayIndex|0) : -1,
            plan: (typeof S !== 'undefined') ? JSON.stringify(S.weekPlan) : '?',
            mask: !!document.querySelector('#mask.on'),
            mapOn: !!document.querySelector('#v-map.on'),
            video: v ? v.getAttribute('src') : null,
            modalHead: mi ? (mi.textContent || '').slice(0, 60) : '',
            endDayBtn: !!document.querySelector('#map-end-day'),
            confirmBtn: [...document.querySelectorAll('button')]
              .some(x => (x.textContent || '').includes('確定本週行程')),
          };
        }""")
        print(tag, s)
        return s

    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(2000)
    pg.click("#btn-new")
    pg.wait_for_timeout(1200)
    try:
        pg.click("text=跳過教學", timeout=3000)
        pg.wait_for_timeout(600)
    except Exception:
        pass
    # dismiss 任何 modal（撳第一掣）
    for _ in range(6):
        if not pg.evaluate("!!document.querySelector('#mask.on')"):
            break
        loc = pg.locator("#modal-btns button")
        if loc.count():
            try:
                loc.first.click()
            except Exception:
                break
        pg.wait_for_timeout(700)
    state("after-new-game")
    # 去地圖
    for _ in range(5):
        if pg.evaluate("!!document.querySelector('#v-map.on')"):
            break
        loc = pg.locator("button", has_text="返回地圖")
        try:
            if loc.count() and loc.first.is_visible():
                loc.first.click()
        except Exception:
            pass
        pg.wait_for_timeout(900)
    state("on-map")

    pg.evaluate("""() => {
      const today = S.dayIndex|0;
      const wd = new Date(1990, 0, 1 + today).getDay();
      const slot = (wd + 6) % 7;
      S.shoots = [{ id: 'sh_fx', gigId: 'fx_g1', title: '都市電視劇',
        workTitle: '', roleLabel: '配角', type: '電視劇', tier: '初',
        roleScale: '配角', daysLeft: 2, totalDays: 2, pay: 3000, fame: 2,
        payBase: 3000, payBonus: 0, payBonusLabel: '', popularity: 2,
        locId: 'tvb_harbour', doneDays: 0, shootWeekdays: [slot],
        hiredAtDay: today, deadlineDays: 30, deadlineDay: today + 30,
        overdueConsumed: false, breachFee: 0, signedPaid: 900 }];
      S.weekPlan = ['rest','rest','rest','rest','rest','rest','rest'];
      S.weekPlan[slot] = 'shoot:sh_fx';
    }""")
    state("after-plant")
    loc = pg.locator("button", has_text="確定本週行程")
    try:
        if loc.count() and loc.first.is_visible():
            loc.first.click()
            pg.wait_for_timeout(1200)
    except Exception as e:
        print("confirm click:", e)
    state("after-confirm")
    pg.screenshot(path=f"{OUT}/dbg0.png")
    for i in range(8):
        s = state(f"step{i}-before")
        if s["video"]:
            print("VIDEO FOUND:", s["video"])
            pg.screenshot(path=f"{OUT}/dbg_video.png")
            break
        if s["mask"]:
            loc = pg.locator("#modal-btns button")
            if loc.count():
                try:
                    print("  click modal btn:", loc.first.inner_text()[:20])
                    loc.first.click()
                except Exception:
                    pass
            pg.wait_for_timeout(1300)
            continue
        try:
            pg.click("#map-end-day", timeout=1500)
            pg.wait_for_timeout(1800)
        except Exception as e:
            print("  end-day click fail")
            pg.wait_for_timeout(800)
    state("final")
    print("pageerrors:", errs[:3])
    b.close()
