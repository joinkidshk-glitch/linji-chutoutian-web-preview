# -*- coding: utf-8 -*-
"""v20a105 WEEK105 實駕覆核（Playwright，本地鏡像）：
   A. S-12：週日（dayIndex=6，排程 rest）→ 日結板「回家結算」掣出現嗰陣 reload
      → 重開撳繼續 → 必須補呈現「回家結算 · 第 1 週」結算卡＋入編排步，
      生活費 $1,100 全程只扣一次（reload 前後金額一致 = 12,798）。
   B. S-13：下週週三今日格係已殺青 wrap: 標記 → 重開後今日計劃變返到處逛逛，
      地圖有「逛完・過一日」入口。
   C. S-14：手帳上週行程回顧 → 週一出「劇情・試鏡」實際紀錄、週四出
      「到處逛逛・提早休息」，唔再係「休息睡覺」。
   用法：python3 qa105/drive105.py [base_url]"""
import sys, json, time
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8905/"
URL = BASE + "?v=20a10&softBehaviorGate=1&softRev=s107"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
OUT = "qa105/shots"
import os
os.makedirs(OUT, exist_ok=True)
fails = []
def ok(cond, msg):
    print(("  ✓ " if cond else "  ✗ FAIL: ") + msg)
    if not cond:
        fails.append(msg)

def money_of(page):
    return page.evaluate("""() => {
      const raw = localStorage.getItem('starVolunteer_map_v19w');
      return raw ? JSON.parse(raw).money : null;
    }""")

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    page = b.new_page(viewport={"width": 420, "height": 900})
    page.goto(URL)
    page.wait_for_timeout(2500)
    page.click("#btn-new")  # 開新局，等內部 S 建立（window.S 經 exposePreviewDebug 暴露參照）
    page.wait_for_timeout(2000)
    ok(page.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"), "A0 新局 S 已建立")

    # ---------- A. S-12 週界 reload ----------
    page.evaluate("""() => {
      const S = window.S;
      S.flags.tutorialDone = true; S.flags.sawB01 = true;
      S.homeEditable = false;
      S.dayIndex = 6;               /* 第 1 週週日 */
      S.money = 13898; S.weekEarn = 1882;
      S.weekPlan = ["scout_all","rest","scout_all","scout_all","street","cafe_gig","rest"];
      S.weekPlanWeek37 = 1;
      localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S));
    }""")
    page.reload(); page.wait_for_timeout(2000)
    page.click("#btn-cont"); page.wait_for_timeout(2500)
    # 週日 rest 應自動行 → 日結板（回家結算掣）
    body = page.inner_text("body")
    ok("回家結算" in body, "A1 週日日結板出現「回家結算」")
    page.screenshot(path=f"{OUT}/a1_sunday_board.png")
    m1 = money_of(page)
    ok(m1 == 12798, f"A2 日結後金額 = 12,798（生活費已扣一次；實得 {m1}）")
    flag = page.evaluate("() => { const o = JSON.parse(localStorage.getItem('starVolunteer_map_v19w')); return o.weekBoundary105 && o.weekBoundary105.week; }")
    ok(flag == 1, f"A3 週界旗已落存檔（week={flag}）")
    # 喺日結板嗰陣「關閉/重開」：reload + 繼續
    page.reload(); page.wait_for_timeout(2000)
    page.click("#btn-cont"); page.wait_for_timeout(2500)
    body = page.inner_text("body")
    ok("回家結算 · 第 1 週" in body, "A4 重開後補呈現結算卡「回家結算 · 第 1 週」")
    ok("唔會重扣" in body, "A5 結算卡講明金額已入帳唔會重扣")
    m2 = money_of(page)
    ok(m2 == 12798, f"A6 重開後金額仍然 12,798（冇雙重扣錢；實得 {m2}）")
    he = page.evaluate("() => window.S && window.S.homeEditable")
    ok(he is True, "A7 已入編排下週行程步（homeEditable=true）")
    page.screenshot(path=f"{OUT}/a2_reload_settle.png")
    # 撳走結算卡 → 應該喺手帳編排行程
    page.click("text=編排新一週行程"); page.wait_for_timeout(1200)
    body = page.inner_text("body")
    ok("編輯本週行程" in body, "A8 結算卡後落入編輯本週行程")
    page.screenshot(path=f"{OUT}/a3_planner.png")

    # ---------- B. S-13 已殺青通告唔再卡住下週日子 ----------
    page.evaluate("""() => {
      const S = window.S;
      S.dayIndex = 9;               /* 第 2 週週三 */
      S.homeEditable = false;
      S.weekPlan = ["scout_all","rest","wrap:" + encodeURIComponent("《賀歲特輯》拜年群演"),"scout_all","street","cafe_gig","rest"];
      S.weekPlanWeek37 = 1;
      S.shoots = []; S.booked = [];
      S.weekBoundary105 = null;
      S.execLog105 = {
        0: { kinds: ["story","audition"], detail: "《賀歲特輯》拜年群演" },
        3: { kinds: ["browse","early_rest"], detail: "" }
      };
      localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(S));
    }""")
    page.reload(); page.wait_for_timeout(2000)
    page.click("#btn-cont"); page.wait_for_timeout(2500)
    hint = page.inner_text("#map-hint")
    ok("殺青" not in hint, f"B1 今日計劃唔再係已殺青通告（實得：{hint.splitlines()[0] if hint else ''}）")
    ok("到處逛逛" in hint, "B2 今日計劃變返到處逛逛")
    has_end = page.evaluate("() => !!document.getElementById('map-end-day')")
    ok(has_end, "B3 地圖有「逛完・過一日」入口（嗰日有正常結束方法）")
    page.screenshot(path=f"{OUT}/b1_w2wed_map.png")

    # ---------- C. S-14 手帳回顧出實際執行 ----------
    page.click("#btn-menu"); page.wait_for_timeout(600)
    page.click('[data-m="journal"]')
    page.wait_for_timeout(1500)
    days_txt = page.inner_text("#nb-days")
    ok("上週行程" in page.inner_text("body"), "C1 手帳顯示上週行程（唯讀）")
    ok("劇情" in days_txt and "試鏡" in days_txt, "C2 週一回顧 = 劇情・試鏡（實際紀錄）")
    ok("提早休息" in days_txt, "C3 週四回顧 = 含提早休息（實際紀錄）")
    mon_line = [ln for ln in days_txt.splitlines() if "試鏡" in ln]
    ok(not any("休息睡覺" in ln for ln in mon_line), "C4 試鏡嗰日唔再顯示休息睡覺")
    page.screenshot(path=f"{OUT}/c1_prevweek_review.png")
    b.close()

print("drive105:", "FAIL " + str(len(fails)) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
