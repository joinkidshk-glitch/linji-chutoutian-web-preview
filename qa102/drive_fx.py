# -*- coding: utf-8 -*-
"""v20a102 FX102 實駕驗證（本地鏡像，真 UI 流程）：
改植 S.weekPlan/S.shoots（qa101 drive_c 既定套路）→ 確定本週行程 →
#map-end-day 推進 → 日結板出現嗰刻驗 <video> 片種＋真係播緊 → 截圖。
用法：python drive_fx.py <port>
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
    print(("PASS " if cond else "FAIL ") + msg)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 430, "height": 932})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    def mask_on():
        return pg.evaluate("!!document.querySelector('#mask.on')")

    def btn(scope, part):
        loc = pg.locator(f"{scope} button", has_text=part)
        try:
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                return True
        except Exception:
            pass
        return False

    def dismiss(maxn=12):
        for _ in range(maxn):
            if not mask_on():
                return
            head = pg.evaluate("""() => { const mi = document.getElementById('modal-inner');
              return mi ? (mi.textContent || '').slice(0, 40) : ''; }""")
            if "加速" in head and "？" in head:
                if btn("#modal-btns", "取消"):
                    pg.wait_for_timeout(700)
                    continue
            done = False
            for t in ["確定", "繼續", "下一步", "知道了", "收下", "好", "完成",
                      "返回地圖", "開始今日行程"]:
                if btn("#modal-btns", t):
                    done = True
                    break
            if not done:
                # fallback：唔好撳「加速」嗰粒（會入加速模式吞咗訓練日）
                clicked = pg.evaluate("""() => {
                  const bs = [...document.querySelectorAll('#modal-btns button')]
                    .filter(x => !(x.textContent || '').includes('加速'));
                  if(bs.length){ bs[0].click(); return true; } return false; }""")
                if not clicked:
                    return
            pg.wait_for_timeout(700)

    def clear_enc():
        for _ in range(10):
            if not pg.evaluate("!!document.querySelector('#enc79-overlay')"):
                return
            loc = pg.locator("#enc79-overlay button")
            if loc.count():
                try:
                    loc.last.click()
                except Exception:
                    return
            else:
                return
            pg.wait_for_timeout(500)

    def video_info():
        return pg.evaluate("""() => {
          const v = document.getElementById('act-fx102-video') ||
                    document.getElementById('rest-sleep-video');
          if(!v) return null;
          return { id: v.id, src: v.getAttribute('src'),
                   paused: v.paused, t: v.currentTime };
        }""")

    def run_until_video(expect_file, max_steps=46):
        """推進日子直到日結板出片。計劃日要經「開始今日行程」行；
        提早休息確認撳取消（唔好嘥咗計劃日）；加速確認永遠取消
        （加速會靜默吞咗訓練日，唔會出板）。"""
        for _ in range(max_steps):
            v = video_info()
            if v and expect_file in (v["src"] or ""):
                return v
            if mask_on():
                head = pg.evaluate("""() => { const mi = document.getElementById('modal-inner');
                  return mi ? (mi.textContent || '').slice(0, 60) : ''; }""")
                if "提早休息" in head:
                    btn("#modal-btns", "取消")
                    pg.wait_for_timeout(900)
                    continue
                if "加速本週剩餘？" in head:
                    btn("#modal-btns", "取消")
                    pg.wait_for_timeout(900)
                    continue
                if btn("#modal-btns", "開始今日行程"):
                    pg.wait_for_timeout(1500)
                    continue
                done = False
                for t in ["開始", "確定", "繼續", "下一步", "知道了", "收下",
                          "好", "完成"]:
                    if btn("#modal-btns", t):
                        done = True
                        break
                if not done:
                    pg.evaluate("""() => {
                      const bs = [...document.querySelectorAll('#modal-btns button')]
                        .filter(x => !(x.textContent || '').includes('加速'));
                      if(bs.length) bs[0].click(); }""")
                pg.wait_for_timeout(1100)
                continue
            clear_enc()
            if btn("body", "開始今日行程"):
                pg.wait_for_timeout(1500)
                continue
            # #map-end-day 喺 viewport 摺位之下，Playwright click 撳唔到——JS click
            clicked = pg.evaluate("""() => { const b = document.querySelector('#map-end-day');
              if(b){ b.click(); return true; } return false; }""")
            if clicked:
                pg.wait_for_timeout(1600)
                continue
            pg.wait_for_timeout(800)
        return video_info()

    def plant(js):
        pg.evaluate(f"""() => {{
          const today = S.dayIndex|0;
          const wd = new Date(1990, 0, 1 + today).getDay();
          const slot = (wd + 6) % 7;
          S.weekPlan = ['rest','rest','rest','rest','rest','rest','rest'];
          {js}
        }}""")
        btn("body", "確定本週行程")
        pg.wait_for_timeout(1000)

    def ensure_map():
        for _ in range(6):
            if pg.evaluate("() => { const m = document.getElementById('v-map');"
                           " return m && m.classList.contains('on'); }"):
                return True
            if mask_on():
                dismiss()
            if btn("body", "返回地圖"):
                pg.wait_for_timeout(900)
                continue
            try:
                pg.click("#home-back-map-tabs", timeout=1500)
            except Exception:
                pass
            pg.wait_for_timeout(900)
        return pg.evaluate("() => { const m = document.getElementById('v-map');"
                           " return m && m.classList.contains('on'); }")

    def scenario(name, setup_js, expect_file):
        dismiss()
        clear_enc()
        ok(ensure_map(), f"{name}：喺地圖先改植")
        plant(setup_js)
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
        clear_enc()

    # ---- 開局 ----
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
    try:
        pg.click("#home-back-map-tabs", timeout=5000)
        pg.wait_for_timeout(1200)
    except Exception as e:
        print("to map:", e)
    ok(pg.evaluate("() => !!(window.__fx102 && __fx102.check().ok)"),
       "頁內自檢 __fx102.check() 全綠")
    ok(pg.evaluate("() => __restFx.check().ok"), "restFx 自檢全綠（新 src）")
    pg.evaluate("() => { S.money = (S.money||0) + 200000; }")

    SHOOT = """S.shoots = [{ id: 'sh_fx', gigId: '%s', title: '%s',
      workTitle: '', roleLabel: '配角', type: '%s', tier: '初',
      roleScale: '配角', daysLeft: 2, totalDays: 2, pay: 3000, fame: 2,
      payBase: 3000, payBonus: 0, payBonusLabel: '', popularity: 2,
      locId: '%s', doneDays: 0, shootWeekdays: [slot], hiredAtDay: today,
      deadlineDays: 30, deadlineDay: today + 30, overdueConsumed: false,
      breachFee: 0, signedPaid: 900 }];
      S.weekPlan[slot] = 'shoot:sh_fx';"""

    scenario("01_shoot", SHOOT % ("fx_g1", "都市電視劇", "電視劇", "tvb_harbour"),
             "fx_shoot.mp4")
    scenario("02_record", SHOOT % ("fx_g2", "大碟錄音", "唱片通告", "rec_star"),
             "fx_record.mp4")
    scenario("03_shoot_ext", SHOOT % ("fx_g3", "廟街外景追逐戲", "電影", "film_lion"),
             "fx_shoot_ext.mp4")

    # 試鏡：逐張入門通告試，直到有一張過到資格（resolve 出試鏡片）
    cands = pg.evaluate("""() => (typeof GIGS !== 'undefined' ? GIGS : [])
      .filter(g => g && g.id && !g.softBridge)
      .slice(0, 60).map(g => g.id)""")
    got = False
    for gid in cands[:10]:
        dismiss()
        clear_enc()
        ensure_map()
        plant(f"S.weekPlan[slot] = 'job:{gid}';")
        v = run_until_video("fx_audition.mp4", max_steps=18)
        if v and "fx_audition.mp4" in (v["src"] or ""):
            ok(True, f"04_audition：日結板出啱片（{gid}）")
            pg.wait_for_timeout(800)
            v2 = video_info()
            ok(v2 and (not v2["paused"]) and v2["t"] > v["t"],
               "04_audition：真係播緊")
            pg.screenshot(path=f"{OUT}/04_audition.png")
            got = True
            dismiss()
            clear_enc()
            break
        dismiss()
        clear_enc()
    if not got:
        ok(False, "04_audition：十張候選都冇出試鏡片")

    scenario("05_train_a", "S.weekPlan[slot] = 'train_acting';",
             "fx_train_a.mp4")
    scenario("06_train_b", "S.weekPlan[slot] = 'train_vocal';",
             "fx_train_b.mp4")
    scenario("07_train_c", "S.weekPlan[slot] = 'train_stamina';",
             "fx_train_c.mp4")
    scenario("08_rest", "S.weekPlan[slot] = 'rest';", "fx_rest.mp4")

    ok(not errs, f"全程冇 pageerror（{errs[:2]}）")
    print(f"drive_fx: {sum(R)}/{len(R)} PASS")
    b.close()
