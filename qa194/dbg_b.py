# -*- coding: utf-8 -*-
"""debug B：逐段 dump——new_game → seed → 返回地圖 → 過一日 → 睇 state。"""
import os, subprocess, time, signal, json
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work194"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8996


def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
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


DUMP = """() => {
  const vis = [...document.querySelectorAll('[id^="v-"]')].filter(e => e.offsetParent !== null).map(e => e.id);
  const st = document.getElementById('map-start-today');
  const modal = document.querySelector('.awd-sheet, [class*="modal"]');
  return {views: vis, dayIndex: window.S ? S.dayIndex : null,
          flags: window.S ? Object.assign({}, S.awardsFlags || {}) : null,
          pending: window.S ? !!S.pendingAwardPack : null,
          mapStartToday: st ? {visible: st.offsetParent !== null, text: (st.textContent || '').trim()} : null,
          modalVisible: !!modal,
          modalText: modal ? (modal.textContent || '').slice(0, 120) : null,
          planId: (() => { try { return (typeof todayPlanId === 'function') ? String(todayPlanId()) : 'n/a'; } catch(e){ return 'err'; } })(),
          storyOverlay: !!document.querySelector('.story-play, [class*="story"]')};
}"""


def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = ctx.new_page(viewport={"width": 932, "height": 700})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{PORT}/index.html"); pg.wait_for_timeout(3000)
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
            print("after new_game:", json.dumps(pg.evaluate(DUMP), ensure_ascii=False), flush=True)
            # seed：同 drive194 run B
            pg.evaluate("""() => {
              const mk = (g, day) => ({gigId: g.id, title: g.title, type: g.type,
                totalDays: 3, pay: 1000, fame: 2, popularity: 0, wrappedDay: day, rating: "順利殺青"});
              const picks = {};
              const want = {"廣告":2, "唱片通告":2, "電影":2, "電視劇":3, "綜藝":1};
              for (const t of Object.keys(want)) picks[t] = (window.GIGS || []).filter(g => g && g.type === t).slice(0, want[t]);
              const wraps = [];
              const take = (t, days) => { (picks[t]||[]).slice(0, days.length).forEach((g,i)=> wraps.push(mk(g, days[i]))); };
              take("廣告", [30, 45]); take("電視劇", [20, 100]); take("綜藝", [300]);
              take("唱片通告", [120, 140]); take("電影", [200, 230]);
              S.dayIndex = 60; S.fame = 26; S.industryCredit = 49;
              S.wrapHistory = wraps; S.postShootRewards = [];
              if (S.story) S.story.gigCount = wraps.length;
              S.awardsFlags = {}; S.pendingAwardPack = null;
              if (S.awardsLog) S.awardsLog = [];
            }""")
            pg.wait_for_timeout(800)
            print("after seed:", json.dumps(pg.evaluate(DUMP), ensure_ascii=False), flush=True)
            r1 = pg.evaluate("""() => {
              const b = document.getElementById('home-back-map-tabs');
              if (b && b.offsetParent !== null) { b.click(); return true; } return false;
            }""")
            pg.wait_for_timeout(2000)
            print("clicked back-to-map:", r1, json.dumps(pg.evaluate(DUMP), ensure_ascii=False), flush=True)
            r2 = pg.evaluate("""() => {
              const b = document.getElementById('map-start-today');
              if (b && b.offsetParent !== null) { b.click(); return '#map-start-today'; } return null;
            }""")
            pg.wait_for_timeout(2500)
            print("clicked start-today:", r2, json.dumps(pg.evaluate(DUMP), ensure_ascii=False), flush=True)
            # 日結板「返回地圖」→ goToMapForBrowse 晨鏈（v189：soft 日呢粒係真返地圖）
            r3 = click_first(pg, ["返回地圖"], 1500)
            pg.wait_for_timeout(2500)
            print("clicked day-end 返回地圖:", r3, json.dumps(pg.evaluate(DUMP), ensure_ascii=False), flush=True)
            print("pageerrors:", errs, flush=True)
            ctx.close()
    finally:
        stop(srv)


if __name__ == "__main__":
    main()
