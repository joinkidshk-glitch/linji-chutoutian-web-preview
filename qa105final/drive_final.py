# -*- coding: utf-8 -*-
"""v20a105 合併版綜合實駕 v3：S-35/S-37/S-40 + 裁決人情頁指向 + S-44/S-48。
跟 WEEK105 駕駛法：window.S（gate 參數）＋ localStorage 直寫 ＋ reload＋#btn-cont。
v3 修正：先撳「開始寫手帳」過 B01 卡先做其他嘢。"""
import sys, os
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/index.html?v=20a10&softBehaviorGate=1&softRev=s107"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = "/home/hatch/workspace/linji-work105/qa105final/shots"
os.makedirs(SHOTS, exist_ok=True)
results = []
def ok(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    results.append((bool(cond), msg))

def persist(page):
    page.evaluate("""() => { localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(window.S)); }""")

def modal_text(page):
    return page.evaluate("""() => {
      const m = document.getElementById('mask');
      if(!m || !m.classList.contains('on')) return '';
      const inner = document.getElementById('modal-inner');
      return inner ? inner.innerText : '';
    }""")

def click_modal_primary(page):
    return page.evaluate("""() => {
      const row = document.getElementById('modal-btns');
      if(!row) return false;
      const btns = Array.from(row.querySelectorAll('button')).filter(b => b.offsetParent !== null && !b.disabled);
      if(!btns.length) return false;
      btns[0].click(); return true;
    }""")

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 420, "height": 900})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(URL)
    page.wait_for_timeout(2500)
    page.click("#btn-new")
    page.wait_for_timeout(2000)
    ok(page.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"), "新局 S 已建立")
    # 先落教學/B01 旗＋reload＋繼續，避開教學 modal 遮擋（跟 WEEK105 駕駛法）
    page.evaluate("""() => { const S=window.S; S.flags.tutorialDone = true; S.flags.sawB01 = true; }""")
    persist(page)
    page.reload(); page.wait_for_timeout(2000)
    page.click("#btn-cont"); page.wait_for_timeout(2500)

    # ---------- 人情頁 ----------
    page.evaluate("""() => { const b = Array.from(document.querySelectorAll('button')).find(x => x.offsetParent && x.textContent.trim() === '手帳'); if(b) b.click(); }""")
    page.wait_for_timeout(1000)
    try:
        page.click("text=人情", timeout=3000)
        page.wait_for_timeout(1200)
    except Exception as e:
        print("人情 tab click:", e)
    fav = page.evaluate("""() => { const b=document.getElementById('debt-list'); return b ? b.textContent : ''; }""")
    page.screenshot(path=f"{SHOTS}/01_favor_pane.png")
    ok("江湖路" in fav and "信任儲得夠深" in fav, "裁決：人情頁有 E5 定性指向（江湖路＋信任/清債/債權）")
    ok("就嚟到期" in fav and "已逾期" not in fav, "S-44：第一日人情頁開局債係「就嚟到期」、冇「已逾期」")

    # ---------- 設定頁 S-48 ----------
    try:
        page.click("#btn-menu", timeout=2000); page.wait_for_timeout(800)
        page.click("text=設定", timeout=2000); page.wait_for_timeout(1000)
    except Exception:
        page.evaluate("""() => { try{ openSettingsModal(); }catch(e){} }""")
        page.wait_for_timeout(1000)
    st = page.evaluate("""() => { const s=document.querySelector('.settings-list'); return s ? s.textContent : ''; }""")
    page.screenshot(path=f"{SHOTS}/02_settings.png")
    ok("未推出" not in st, "S-48：設定頁冇「未推出」死掣字樣")
    ok("即將推出" in st and "音效／音樂" in st, "S-48：音效／音樂改做「即將推出」灰字行")
    click_modal_primary(page)
    page.wait_for_timeout(600)

    # ---------- S-35：種 pendingAud ----------
    planted = page.evaluate("""() => {
      try{
        const S = window.S;
        const g = (typeof GIGS!=='undefined'?GIGS:[]).find(x=>x && x.title && x.title.indexOf('賀歲特輯')>=0) || (typeof GIGS!=='undefined'?GIGS:[]).find(x=>x&&x.id);
        if(!g) return 'no-gig';
        S.pendingAud = [{ gigId:g.id, title:g.title, type:g.type||'tv', tier:g.tier||1, locId:g.locId||'',
          audDay:S.dayIndex|0, revealDay:(S.dayIndex|0)+1, ok:true, chancePct:70,
          pay:g.pay||516, payBase:g.pay||516, payBonus:0, payBonusLabel:'', payNote:'',
          fame:g.fame||1, pop:g.popularity||2, days:g.days||2,
          fxActing:0, fxStress:10, fxFame:0, fxStressFail:5, via:'drive105final' }];
        return 'planted:'+g.id;
      }catch(e){ return 'err:'+e.message; }
    }""")
    print("pendingAud plant:", planted)
    ok(str(planted).startswith("planted"), "S-35 準備：pendingAud 已種（真 gig）")
    persist(page)
    page.reload(); page.wait_for_timeout(2000)
    page.click("#btn-cont"); page.wait_for_timeout(2500)
    # 若停喺編排步（週一未確認行程），先確認本週行程去返地圖
    try:
        if page.evaluate("() => { const b=document.getElementById('btn-confirm-plan'); return b && b.offsetParent !== null; }"):
            page.click("#btn-confirm-plan", timeout=2000)
            page.wait_for_timeout(1000)
            click_modal_primary(page)
            page.wait_for_timeout(1500)
    except Exception as e:
        print("confirm plan:", e)
    # 過一日：先試 UI 掣，唔得就用 menu 提早休息（日翻頁同公佈鏈仍然行真 code）
    flipped = False
    try:
        page.click("text=逛完・過一日", timeout=2500)
        page.wait_for_timeout(1000)
        click_modal_primary(page)
        flipped = True
    except Exception:
        try:
            page.click("#btn-menu", timeout=2000); page.wait_for_timeout(800)
            page.click("text=提早休息", timeout=2000)
            print("early rest via menu")
        except Exception as e2:
            print("early rest fallback failed:", e2)
        page.wait_for_timeout(1000)
        click_modal_primary(page)
        flipped = True
    page.wait_for_timeout(2500)
    hired = ""
    for i in range(10):
        t = modal_text(page)
        if "獲聘" in t:
            hired = t; break
        if i == 9:
            hired = t
        if not click_modal_primary(page):
            page.wait_for_timeout(900)
        page.wait_for_timeout(1300)
    page.screenshot(path=f"{SHOTS}/03_hired_modal.png")
    ok("獲聘" in hired, "S-35：獲聘 modal 出現（pendingAud 公佈鏈行通）")
    ok("成功率約" not in hired, "S-35：獲聘 modal 冇成功率殘留行")
    ok("簽約金" in hired, "S-35：獲聘 modal 有簽約金段")
    # 撳走獲聘＋排期確認殘餘 modal
    for _ in range(4):
        if not click_modal_primary(page): break
        page.wait_for_timeout(900)

    # ---------- S-37/S-40：shoot 最後一日 → 殺青板 ----------
    setup = page.evaluate("""() => {
      try{
        const S = window.S;
        const sh = (S.shoots||[])[0];
        if(!sh) return 'no-shoot:'+((S.shoots||[]).length);
        sh.pay = 516; sh.signedPaid = 155;
        sh.totalDays = Math.max(1, sh.totalDays||1);
        sh.doneDays = sh.totalDays - 1;
        sh.daysLeft = 1;
        if(typeof placeShootOnPlan==='function') placeShootOnPlan(sh, (typeof weekdayIdx==='function'?weekdayIdx(S.dayIndex):0), true);
        return 'shoot-ready:'+sh.id;
      }catch(e){ return 'err:'+e.message; }
    }""")
    print("shoot setup:", setup)
    ok(str(setup).startswith("shoot-ready"), "S-37/40 準備：shoot 已設到最後一日並排入今日")
    if str(setup).startswith("shoot-ready"):
        persist(page)
        page.reload(); page.wait_for_timeout(2000)
        page.click("#btn-cont"); page.wait_for_timeout(2500)
        try:
            if page.evaluate("() => { const b=document.getElementById('btn-confirm-plan'); return b && b.offsetParent !== null; }"):
                page.click("#btn-confirm-plan", timeout=2000)
                page.wait_for_timeout(1000)
                click_modal_primary(page)
                page.wait_for_timeout(1500)
        except Exception as e:
            print("confirm plan (shoot):", e)
        try:
            page.click("text=開始今日行程", timeout=3000)
        except Exception as e:
            print("開始今日行程 click:", e)
        page.wait_for_timeout(4500)
        wrap = modal_text(page)
        for _ in range(5):
            if "殺青" in wrap: break
            if not click_modal_primary(page): break
            page.wait_for_timeout(1800)
            wrap = modal_text(page)
        page.screenshot(path=f"{SHOTS}/04_wrap_board.png")
        ok("殺青" in wrap, "S-37/40：殺青板出現")
        ok("冇縮水" not in wrap, "S-37：舊重複段（冇縮水）已刪")
        cnt = wrap.count("實收餘額")
        ok(cnt == 1, f"S-37：對帳段只出現一次（實數 {cnt}）")
        vis = page.evaluate("""() => {
          const fig = document.querySelector('figure.chk101');
          const card = fig ? (fig.closest('.modal-card') || document.getElementById('modal-inner')) : null;
          if(!fig || !card) return {found:false};
          const r = fig.getBoundingClientRect(); const c = card.getBoundingClientRect();
          return { found:true, figTop:r.top, figBottom:r.bottom, cardTop:c.top, cardBottom:c.bottom,
                   inFirstScreen: r.top >= c.top - 4 && r.bottom <= c.bottom + 4 };
        }""")
        print("cheque visibility:", vis)
        ok(vis.get("found") and vis.get("inFirstScreen"), "S-40：支票喺殺青板第一屏完整可見")

    print("pageerrors:", errs[:5])
    ok(len(errs) == 0, "全程零 pageerror")
    browser.close()

fails = [m for c, m in results if not c]
print(f"== DRIVE FINAL v3: {len(results)-len(fails)}/{len(results)} PASS ==")
if fails:
    print("FAILED:", fails); sys.exit(1)
