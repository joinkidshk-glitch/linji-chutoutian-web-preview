#!/usr/bin/env python3
"""v360 真駕驗證 v2：② 舊檔回填（真 save/reload）＋① 呈現（aud91Log 證據）＋② 殺青授予"""
import json, sys
from playwright.sync_api import sync_playwright

EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
URL = "http://127.0.0.1:8931/index.html"
COMEDY = "gig_1990_film_102"
ACTION = "gig_1990_film_103"
SAVE_KEY = "starVolunteer_map_v19w"

results = []
def check(name, ok, detail=""):
    results.append((name, ok))
    print(("PASS" if ok else "FAIL"), name, detail)

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=EXE, args=[
        "--no-sandbox", "--proxy-server=http://127.0.0.1:18081",
        "--proxy-bypass-list=127.0.0.1", "--ignore-certificate-errors"])
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)

    def dismiss(n=8):
        for _ in range(n):
            try:
                page.evaluate("""() => {
                  const m = document.getElementById('mask');
                  if(m && m.classList.contains('on')){
                    const btns = [...document.querySelectorAll('#modal-btns button')];
                    const b = btns.find(x=>/好|繼續|確定|知道了|開始|下一步/.test(x.textContent)) || btns[btns.length-1];
                    if(b) b.click(); else m.click();
                  }
                }""")
            except Exception:
                pass
            page.wait_for_timeout(450)

    def has_S():
        return page.evaluate("() => typeof S!=='undefined' && !!S && typeof S.dayIndex==='number'")

    def click_text(patterns, tries=10):
        for _ in range(tries):
            clicked = page.evaluate("""(pats) => {
              const btns = [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null);
              for(const p of pats){ const b = btns.find(x=>new RegExp(p).test(x.textContent)); if(b){ b.click(); return b.textContent.trim(); } }
              return null;
            }""", patterns)
            if clicked:
                return clicked
            page.wait_for_timeout(600)
        return None

    for _ in range(12):
        if has_S():
            break
        click_text([r"新遊戲|開始遊戲|新局"], tries=2)
        page.wait_for_timeout(800)
        dismiss(3)
    print("has_S:", has_S())
    dismiss(10)

    # ---- ② backfill via real save/reload (exact key) ----
    page.evaluate("""(a) => {
      S.castingTags = [];
      S.wrapHistory = [{gigId: a.comedy, title:'《老闆唔易做》', type:'電影', wrappedDay: 5}];
      S.flags = S.flags || {};
      S.flags['done_'+a.action] = 1;
      S.flags.sawTutAudFail = true;
      S.flags.sawTutShoot = true;
      localStorage.setItem(a.key, JSON.stringify(S));
    }""", {"comedy": COMEDY, "action": ACTION, "key": SAVE_KEY})
    page.reload(wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    for _ in range(12):
        if has_S():
            break
        click_text([r"繼續|讀取存檔|槽"], tries=2)
        page.wait_for_timeout(800)
        dismiss(3)
    dismiss(10)
    st = page.evaluate("() => ({ wrap: (S.wrapHistory||[]).map(h=>h.gigId), tags: (S.castingTags||[]).map(t=>({id:t.id,from:t.from})) })")
    print("AFTER RELOAD:", st)
    ids = [t["id"] for t in st["tags"]]
    check("② 真檔 reload 回填 tag_comedy", "tag_comedy" in ids, str(ids))
    check("② 真檔 reload 回填 tag_action", "tag_action" in ids, str(ids))

    # ---- ① overdue pending presents (aud91Log as evidence) ----
    log0 = page.evaluate("() => (S.aud91Log||[]).length")
    page.evaluate("""() => {
      S.pendingAud = [{ gigId:'gig_1990_film_102', title:'測試通告', type:'電影', tier:'初', locId:'film_victoria',
        audDay: (S.dayIndex|0)-6, revealDay: (S.dayIndex|0)-2, ok:false, chancePct:50,
        pay:100, payBase:100, payBonus:0, payBonusLabel:'', payNote:'', fame:1, pop:1, days:1,
        fxActing:0, fxStress:0, fxFame:0, fxStressFail:0, via:'' }];
      S.flags.sawTutAudFail = true;
    }""")
    presented = False
    for _ in range(14):
        click_text([r"確定過一日", r"過一日", r"確定本週行程", r"返回地圖"], tries=1)
        page.wait_for_timeout(900)
        dismiss(4)
        if page.evaluate("() => (S.aud91Log||[]).length") > log0:
            presented = True
            break
    pend = page.evaluate("() => (S.pendingAud||[]).length")
    check("① 逾期 pending 真呈現（aud91Log+1）", presented and pend == 0, f"log {log0}-> {page.evaluate('() => (S.aud91Log||[]).length')} pending={pend}")

    # ---- ② live grant on wrap ----
    page.evaluate("""(gid) => {
      const gig = (GIGS||[]).find(g=>g.id===gid) || {};
      S.castingTags = [];
      S.shoots = [{ id:'sh360', gigId: gid, title: gig.title||'測試', workTitle: gig.workTitle||'', roleLabel: gig.roleLabel||'',
        type: gig.type||'電影', tier: gig.tier||'初', roleScale: gig.roleScale||'', daysLeft:1, totalDays:1,
        pay:100, fame:1, payBase:100, payBonus:0, payBonusLabel:'', popularity:1, locId: gig.loc||'film_victoria',
        doneDays:0, shootWeekdays:[0,1,2,3,4,5,6], hiredAtDay:(S.dayIndex|0)-1, deadlineDays:30, deadlineDay:(S.dayIndex|0)+30,
        overdueConsumed:false, signedPaid:30 }];
      S.weekPlan = ['shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360'];
      S.flags.sawTutShoot = true;
    }""", COMEDY)
    wrapped = False
    for _ in range(16):
        click_text([r"確定本週行程", r"開始今日|今日行程|繼續今日"], tries=1)
        page.wait_for_timeout(900)
        dismiss(4)
        if page.evaluate("() => (S.castingTags||[]).some(t=>t.id==='tag_comedy')"):
            wrapped = True
            break
        if page.evaluate("() => (S.shoots||[]).length") == 0:
            break
    tags2 = page.evaluate("() => (S.castingTags||[]).map(t=>t.id)")
    shoots_left = page.evaluate("() => (S.shoots||[]).length")
    check("② 殺青即時授予 tag_comedy", wrapped, f"tags={tags2} shoots_left={shoots_left}")

    browser.close()

fails = [r for r in results if not r[1]]
print(f"\nTOTAL {len(results)-len(fails)}/{len(results)} PASS")
sys.exit(1 if fails else 0)
