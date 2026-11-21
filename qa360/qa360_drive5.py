#!/usr/bin/env python3
import sys
from playwright.sync_api import sync_playwright

EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
URL = "http://127.0.0.1:8931/index.html"
COMEDY = "gig_1990_film_102"
SAVE_KEY = "starVolunteer_map_v19w"

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
                    const b = btns.find(x=>/好|繼續|確定|知道了|開始|下一步|下一句/.test(x.textContent)) || btns[btns.length-1];
                    if(b) b.click(); else m.click();
                  }
                }""")
            except Exception:
                pass
            page.wait_for_timeout(450)

    def has_S():
        return page.evaluate("() => typeof S!=='undefined' && !!S && typeof S.dayIndex==='number'")

    for _ in range(12):
        if has_S():
            break
        page.evaluate("""() => {
          const btns = [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null);
          const b = btns.find(x=>/新遊戲|開始遊戲|新局/.test(x.textContent));
          if(b) b.click();
        }""")
        page.wait_for_timeout(800)
        dismiss(3)
    dismiss(10)

    page.evaluate("""(a) => {
      const gig = (GIGS||[]).find(g=>g.id===a.gid) || {};
      S.castingTags = [];
      S.shoots = [{ id:'sh360', gigId: a.gid, title: gig.title||'測試', workTitle: gig.workTitle||'', roleLabel: gig.roleLabel||'',
        type: gig.type||'電影', tier: gig.tier||'初', roleScale: gig.roleScale||'', daysLeft:1, totalDays:1,
        pay:100, fame:1, payBase:100, payBonus:0, payBonusLabel:'', popularity:1, locId: gig.loc||'film_victoria',
        doneDays:0, shootWeekdays:[0,1,2,3,4,5,6], hiredAtDay:(S.dayIndex|0)-1, deadlineDays:30, deadlineDay:(S.dayIndex|0)+30,
        overdueConsumed:false, signedPaid:30 }];
      S.weekPlan = ['shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360','shoot:sh360'];
      S.flags.sawTutShoot = true;
      S.story = S.story || {done:{},flags:{},rel:{},routes:{},phase:'P1'};
      S.story.done = S.story.done || {};
      ['N1','N2','N3','N4','N5'].forEach(n=>{ S.story.done[n]=1; });
      localStorage.setItem(a.key, JSON.stringify(S));
    }""", {"gid": COMEDY, "key": SAVE_KEY})

    page.reload(wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    for _ in range(12):
        if has_S():
            break
        page.evaluate("""() => {
          const btns = [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null);
          const b = btns.find(x=>/繼續|讀取存檔|槽/.test(x.textContent));
          if(b) b.click();
        }""")
        page.wait_for_timeout(800)
        dismiss(3)
    dismiss(6)

    page.evaluate("""() => {
      const btns = [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null);
      const b = btns.find(x=>/確定本週行程/.test(x.textContent));
      if(b) b.click();
    }""")
    page.wait_for_timeout(2000)
    page.screenshot(path="/tmp/v360_dbg3.png")
    info = page.evaluate("""() => {
      const m = document.getElementById('mask');
      return { maskOn: m ? m.className : null,
               inner: (document.getElementById('modal-inner')||{}).textContent?.slice(0,120),
               btns: [...document.querySelectorAll('#modal-btns button')].map(b=>b.textContent.trim()),
               day: S.dayIndex, shoots: (S.shoots||[]).length, plan: S.weekPlan };
    }""")
    print("STATE:", info)

    # day-res card: click mask at (195,120) per AGENTS.md, else click gold continue
    for i in range(30):
        page.mouse.click(195, 120)
        page.wait_for_timeout(800)
        dismiss(3)
        tags = page.evaluate("() => (S.castingTags||[]).map(t=>t.id)")
        shoots = page.evaluate("() => (S.shoots||[]).length")
        day = page.evaluate("() => S.dayIndex")
        print(f"step{i} day={day} shoots={shoots} tags={tags}")
        if "tag_comedy" in tags or shoots == 0:
            break
    page.screenshot(path="/tmp/v360_dbg4.png")
    ok = "tag_comedy" in page.evaluate("() => (S.castingTags||[]).map(t=>t.id)")
    print("PASS ② 殺青即時授予 tag_comedy" if ok else "FAIL ② 殺青即時授予 tag_comedy")
    browser.close()
    sys.exit(0 if ok else 1)
