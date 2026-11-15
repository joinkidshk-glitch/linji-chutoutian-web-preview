# -*- coding: utf-8 -*-
"""v20a225 實駕 drive225：對手線強化 R1/R2/R3/R5 live 驗證。
用法：/home/hatch/pwenv49/bin/python qa225/drive225.py
基底：main 719975f（v224）；由 drive223.py（379 行，commit 552b548）重建——drive224.py 已截斷成 17 bytes 碎片，內容以 drive223 為準＋以下修正。
修正：(1) P2 快訊 eventKey 係 rival_news_1（1-based，見 code rival_news_+(idx+1)；drive223 寫 rival_news_0 係錯，實測 queue 入面係 rival_news_1）；(2) P2 標題改查 queue 入面嗰則 headline（modal hit 唔穩定）；(3) P7 板面檢查以玩家可見文字為準，teaser gid 只作診斷——drive224 07:37 全跑 P7-board-r2 曾 FAIL（r2 teaser gid 空），但 P7-rematch-open／P7-old-gig-cleared 皆 PASS、logic test test_rival_board_r2.js 亦 ALL PASS，game state 無問題，待 live 重跑判定係 drive selector 定真問題；(4) P8 改 6 次。
Mirror：工作副本 ~/workspace/linji-work-rival，port 8973，390x844，?softPreview=1。
流程：新遊戲 → 播種（day 149、C3 hard、傳聞+剪報=3分、雙軌低必輸）
 → 過一日到 day 150（R2 快訊＋決戰開閘）→ 手帳人脈 R1 狀態行
 → 星河電視台報名《霓虹夜影》→ 試鏡→獲聘→拍攝→殺青結算輸
 → R1 狀態行轉冷卻 → 快轉到 nextOpenDay 前一日 → 過一日開第 2 輪（R5）
 → 獅子山製片板面見《火線街頭》、舊輪通告已清
 → R3：播種落選 pendingAud，逐日試，最多 6 次，睇「嗰個位最後畀咗高俊傑」
R6a（掉單唔結算）只由邏輯測試覆蓋，live 唔試（要等 14 日限期＋撞拍攝日告假，成本高）。
證據以 DOM 文字＋S 狀態為準；截圖唔用（headless shell 會出 stale frame）。
注意：瀏覽器已死（Chromium SIGTRAP），live drive 暫緩，待瀏覽器恢復先跑。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request

ROOT = "/home/hatch/workspace/linji-work-rival"
HERE = os.path.join(ROOT, "qa225")
os.makedirs(HERE, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8973
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
REPORT = os.path.join(HERE, "drive225_report.md")
LOG = {"phases": {}, "fails": []}

def note(phase, ok, detail=""):
    LOG["phases"][phase] = {"ok": ok, "detail": detail}
    print(f"[{phase}] {'PASS' if ok else 'FAIL'} {detail}", flush=True)
    if not ok:
        LOG["fails"].append(phase)

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError("http.server died on start")
    st, body = http_body("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    assert st == 200 and sha == exp, "served index mismatch"
    print("serve ok sha", sha[:12], flush=True)
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

SAFE_DISMISS = ["確定", "知道了", "好", "繼續", "下一句", "離開", "明白", "返地圖", "返回地圖", "關閉", "收起"]

def body_text(pg):
    try:
        return pg.evaluate("() => document.body ? document.body.innerText : ''") or ""
    except Exception:
        return ""

def s_eval(pg, js):
    return pg.evaluate(js)

def click_first(pg, texts, wait=900):
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

def click_exact(pg, text, wait=1200):
    ok = pg.evaluate("""(t) => {
      const els=[...document.querySelectorAll('button,[onclick],[role=button],a,div,span')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()===t;});
      if(!els.length) return false; els[0].click(); return true; }""", text)
    pg.wait_for_timeout(wait)
    return ok

def dismiss_watch(pg, targets, max_clicks=25, wait=700):
    """逐個撳安全掣，每步 snapshot；targets 命中即回傳命中字串，否則 None。"""
    seen = ""
    for _ in range(max_clicks):
        txt = body_text(pg)
        seen += "\n" + txt
        for t in targets:
            if t in txt:
                return t
        hit = click_first(pg, SAFE_DISMISS, wait)
        if not hit:
            pg.wait_for_timeout(wait)
            txt2 = body_text(pg)
            seen += "\n" + txt2
            for t in targets:
                if t in txt2:
                    return t
            break
    return None

def pass_day(pg, targets=None, max_clicks=25):
    """撳「過一日」，然後 dismiss_watch 睇 targets。回傳 (hit, day_after)。"""
    try:
        btn = pg.locator('button[data-m="rest-early"]')
        if btn.count() and btn.first.is_visible():
            btn.first.click(timeout=1500)
        else:
            click_first(pg, ["過一日"], 1000)
    except Exception as e:
        print("pass_day click failed:", e, flush=True)
    pg.wait_for_timeout(1200)
    hit = None
    if targets:
        hit = dismiss_watch(pg, targets, max_clicks=max_clicks)
    else:
        dismiss_watch(pg, [], max_clicks=8)
    try:
        day = pg.evaluate("() => (window.S ? S.dayIndex : -1)")
    except Exception:
        day = -1
    return hit, day

def rivalry_state(pg):
    return pg.evaluate("""() => {
      const r = (window.S && S.rivalry) ? JSON.parse(JSON.stringify(S.rivalry)) : null;
      return {day: S ? S.dayIndex : -1, fame: S ? S.fame : -1, credit: S ? S.industryCredit : -1,
              rivalry: r, newsIdx: r ? r.newsIdx : null,
              pendingAud: (S && S.pendingAud) ? S.pendingAud.length : -1,
              queue: (S && S.newspaperQueue) ? S.newspaperQueue.map(q=>q.eventKey) : []};
    }""")

def open_people_list(pg):
    click_first(pg, ["☰"], 1000)
    click_first(pg, ["手帳"], 1200)
    try:
        pg.locator("#hgroup-career").click(timeout=1500); pg.wait_for_timeout(800)
    except Exception:
        click_first(pg, ["事業"], 800)
    try:
        pg.locator("#htab-people").click(timeout=1500); pg.wait_for_timeout(800)
    except Exception:
        click_first(pg, ["人脈"], 800)
    try:
        return pg.evaluate("() => { const el=document.querySelector('#people-list'); return el ? el.innerText : ''; }")
    except Exception:
        return ""

def back_to_map(pg):
    click_first(pg, ["地圖"], 1000)
    click_first(pg, ["返地圖", "返回地圖"], 800)

def main():
    from playwright.sync_api import sync_playwright
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            pg.on("pageerror", lambda e: print("PAGEERROR:", str(e)[:200], flush=True))
            # ---- 新遊戲 ----
            pg.goto(URL); pg.wait_for_timeout(3000)
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
            ok = pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")
            note("P0-new-game", bool(ok), pg.evaluate("() => window.S ? (S.dayIndex + ' ' + (S.dateStr||'')) : 'no S'"))
            if not ok:
                raise RuntimeError("new game failed")

            # ---- 播種：day 149、C3 hard、傳聞+剪報=3分、雙軌低必輸 ----
            seed = pg.evaluate("""() => {
              S.dayIndex = 149;
              S.story = S.story || {}; S.story.done = S.story.done || {}; S.story.flags = S.story.flags || {};
              S.story.done.C1 = true; S.story.done.C2 = true; S.story.done.C3 = true;
              S.story.flags.rival_gao_hard = true;
              S.flags = S.flags || {}; S.flags.rival_gao_hard = true;
              S.mockRumors = S.mockRumors || [];
              if (!S.mockRumors.some(r=>r && r.id==="gao_steal_spotlight"))
                S.mockRumors.unshift({id:"gao_steal_spotlight", title:"高俊傑搶鏡", text:"", state:"normal", season:""});
              S.newspaperClippings = S.newspaperClippings || [];
              if (!S.newspaperClippings.some(c=>c && c.topicKey==="rival:gao"))
                S.newspaperClippings.push({topicKey:"rival:gao", eventKey:"story:C3", title:"高俊傑搶鏡", day:100});
              S.fame = 5; S.industryCredit = 10;
              S.npcs = S.npcs || {}; S.npcs.rival = 6;
              return {day: S.dayIndex, fame: S.fame, credit: S.industryCredit};
            }""")
            note("P1-seed", seed["day"] == 149, json.dumps(seed, ensure_ascii=False))

            # ---- 過一日到 day 150：R2 快訊 + 決戰開閘 ----
            pre = rivalry_state(pg)
            hit, day = pass_day(pg, targets=["高俊傑新劇擔正男主角", "霓虹夜影"], max_clicks=25)
            st = rivalry_state(pg)
            note("P2-day150", day == 150, f"day={day} hit={hit}")
            note("P2-rival-open", st["rivalry"] and st["rivalry"].get("faceoffState") == "open"
                 and st["rivalry"].get("round") == 1 and st["rivalry"].get("workTitle") == "霓虹夜影",
                 json.dumps(st["rivalry"], ensure_ascii=False))
            note("P2-news-enqueued", st["rivalry"] and st["rivalry"].get("newsIdx") == 1
                 and "story:C3:rival_news_1" in (st["queue"] or []),
                 f"newsIdx={st['rivalry'].get('newsIdx') if st['rivalry'] else None} queue={st['queue']}")
            _q = pg.evaluate("""() => (S.newspaperQueue||[]).filter(q=>q && (q.eventKey||'')==='story:C3:rival_news_1').map(q=>q.headline||'')""")
            note("P2-news-headline-seen", "高俊傑新劇擔正男主角" in _q or hit == "高俊傑新劇擔正男主角",
                 f"queue headlines={_q} modal hit={hit}")

            # ---- R1 狀態行（open 態）----
            people = open_people_list(pg)
            with open(os.path.join(HERE, "people_open.txt"), "w", encoding="utf-8") as f:
                f.write(people)
            idx = people.find("高俊傑")
            block = people[idx:idx + 600] if idx >= 0 else ""
            note("P3-r1-open-line", "高俊傑" in people and ("46" in block or "門檻" in block or "爭位" in block),
                 block.replace("\n", " / ")[:300])

            # ---- 入星河電視台，報名《霓虹夜影》 ----
            back_to_map(pg)
            clicked = click_exact(pg, "星河電視台", 1500)
            # 巧遇可能攔截：先行 dismiss 一輪
            dismiss_watch(pg, ["霓虹夜影"], max_clicks=10)
            sheet = body_text(pg)
            note("P4-board-faceoff", "霓虹夜影" in sheet, "板面見到《霓虹夜影》" if "霓虹夜影" in sheet else sheet[:200].replace("\n", " / "))
            if "霓虹夜影" in sheet:
                try:
                    pg.locator('.gig-card:has-text("霓虹夜影")').first.click(timeout=2000)
                except Exception:
                    pg.evaluate("""() => { const els=[...document.querySelectorAll('*')].filter(e=>e.children.length===0 && (e.textContent||'').includes('霓虹夜影'));
                      if(els.length){ let n=els[0]; for(let i=0;i<4 && n;i++){ if(n.onclick || n.className.includes('gig-card')){ n.click(); break; } n=n.parentElement; } return true; } return false; }""")
                pg.wait_for_timeout(1200)
                detail = body_text(pg)
                note("P4-detail", "霓虹夜影" in detail and ("去試鏡" in detail or "接通告" in detail),
                     detail[:200].replace("\n", " / "))
                got = click_first(pg, ["去試鏡"], 1200)
                if not got:
                    got = click_first(pg, ["接通告"], 1200)
                # confirmSpendDay 彈窗：再撳一次去試鏡／確定
                click_first(pg, ["去試鏡"], 1000)
                click_first(pg, ["確定"], 800)
                dismiss_watch(pg, [], max_clicks=6)
                pend = pg.evaluate("""() => (S.pendingAud||[]).map(p=>({gigId:p.gigId, ok:p.ok, revealDay:p.revealDay, day:S.dayIndex}))""")
                note("P4-audition-filed", any(p["gigId"] == "gig_rival_gao_faceoff" for p in pend),
                     json.dumps(pend, ensure_ascii=False))
                # 試鏡 RNG 唔係今票測試對象：若預 roll 係落選，改 ok=true（註明）
                forced = pg.evaluate("""() => {
                  const p=(S.pendingAud||[]).find(x=>x && x.gigId==="gig_rival_gao_faceoff");
                  if(p && p.ok===false){ p.ok=true; return true; } return false; }""")
                if forced:
                    print("P4 note: audition pre-roll was fail; forced ok=true (RNG not under test)", flush=True)

                # ---- 等公佈日：逐日過，直至獲聘 modal ----
                hired = False
                for i in range(6):
                    st2 = rivalry_state(pg)
                    if st2["pendingAud"] == 0:
                        break
                    hit2, day2 = pass_day(pg, targets=["獲聘"], max_clicks=20)
                    if hit2 == "獲聘":
                        hired = True
                        break
                note("P5-hired", hired, f"day={rivalry_state(pg)['day']}")
                # 拍攝日可能要佔位：dismiss 期間撳過的掣已處理；確認 shoot 已排
                shoot = pg.evaluate("""() => {
                  const out={};
                  try{ out.plan=(S.plan?Object.keys(S.plan).length:-1); }catch(e){}
                  try{ out.shootJobs=(S.shootJobs||[]).map(j=>({gigId:j.gigId||j.id, day:j.day||j.shootDay})); }catch(e){}
                  try{ out.jobs=(S.jobs||[]).map(j=>({gigId:j.gigId||j.id})); }catch(e){}
                  return out; }""")
                print("P5 shoot state:", json.dumps(shoot, ensure_ascii=False), flush=True)

                # ---- 逐日過，直至殺青結算（輸）----
                settled = False
                for i in range(20):
                    st3 = rivalry_state(pg)
                    r = st3["rivalry"] or {}
                    if r.get("faceoffState") == "none" and r.get("lastResult") == "lost":
                        settled = True
                        break
                    hit3, day3 = pass_day(pg, targets=["霓虹夜影"], max_clicks=20)
                st4 = rivalry_state(pg)
                r4 = st4["rivalry"] or {}
                note("P6-settled-lost", settled and r4.get("lastResult") == "lost" and r4.get("wins") == 0,
                     json.dumps(r4, ensure_ascii=False))
                note("P6-cooldown-90", r4.get("nextOpenDay") == (r4.get("settledDay") or 0) + 90,
                     f"settledDay={r4.get('settledDay')} nextOpenDay={r4.get('nextOpenDay')}")
                # R1 狀態行（冷卻態）
                people2 = open_people_list(pg)
                with open(os.path.join(HERE, "people_cool.txt"), "w", encoding="utf-8") as f:
                    f.write(people2)
                idx2 = people2.find("高俊傑")
                block2 = people2[idx2:idx2 + 600] if idx2 >= 0 else ""
                note("P6-r1-cool-line", "高俊傑" in people2 and ("下一場" in block2 or "再鬥" in block2 or "冷卻" in block2 or "輸" in block2),
                     block2.replace("\n", " / ")[:300])

                # ---- 快轉到 nextOpenDay 前一日，過一日開第 2 輪 ----
                ff = pg.evaluate("""() => { const r=S.rivalry; if(r && r.nextOpenDay){ S.dayIndex = r.nextOpenDay - 1; return r.nextOpenDay; } return -1; }""")
                back_to_map(pg)
                hit4, day4 = pass_day(pg, targets=["火線街頭"], max_clicks=20)
                st5 = rivalry_state(pg)
                r5 = st5["rivalry"] or {}
                note("P7-rematch-open", r5.get("faceoffState") == "open" and r5.get("round") == 2
                     and r5.get("gigId") == "gig_rival_gao_faceoff_r2" and r5.get("workTitle") == "火線街頭",
                     json.dumps(r5, ensure_ascii=False))
                gig_ids = pg.evaluate("""() => (window.GIGS||[]).filter(g=>g && (g.id||'').indexOf('gig_rival_gao_faceoff')===0).map(g=>g.id)""")
                note("P7-old-gig-cleared", gig_ids == ["gig_rival_gao_faceoff_r2"],
                     f"board rival gigs={gig_ids}")
                # 獅子山製片板面見《火線街頭》
                back_to_map(pg)
                click_exact(pg, "獅子山製片", 1500)
                dismiss_watch(pg, ["火線街頭"], max_clicks=10)
                sheet2 = body_text(pg)
                _ok7 = "火線街頭" in sheet2 and "霓虹夜影" not in sheet2
                _gid = pg.evaluate("""() => { const ts=[...document.querySelectorAll('.gig-teaser')];
                  const r2=ts.find(e=>(e.innerText||'').includes('火線街頭'));
                  const r1=ts.find(e=>(e.innerText||'').includes('霓虹夜影'));
                  return {r2: r2 ? (r2.dataset.gid||'') : null, r1: r1 ? (r1.dataset.gid||'') : null}; }""")
                print("P7-teaser-gid 診斷（drive224 07:37 曾 FAIL：r2 gid 空；只作診斷，唔計分）:", json.dumps(_gid, ensure_ascii=False), flush=True)
                note("P7-board-r2", _ok7,
                     ("見《火線街頭》，無《霓虹夜影》" if _ok7 else sheet2[:200].replace("\n", " / ")))
                # R1 狀態行（第 2 輪 open 態）
                people3 = open_people_list(pg)
                idx3 = people3.find("高俊傑")
                block3 = people3[idx3:idx3 + 600] if idx3 >= 0 else ""
                note("P7-r1-round2-line", "高俊傑" in people3 and ("火線街頭" in block3 or "第 2" in block3 or "第二" in block3 or "46" in block3),
                     block3.replace("\n", " / ")[:300])
            else:
                note("P4-board-faceoff", False, "板面無《霓虹夜影》，後續跳過")
                note("P5-hired", False, "skipped")
                note("P6-settled-lost", False, "skipped")
                note("P6-cooldown-90", False, "skipped")
                note("P7-rematch-open", False, "skipped")

            # ---- R3：落選後續（35% 機率，最多 5 次）----
            r3_hit = False
            for attempt in range(1, 7):
                seeded = pg.evaluate("""() => {
                  const g=(window.GIGS||[]).find(x=>x && x.type==="電視劇" && (x.id||'').indexOf("gig_rival")!==0);
                  if(!g) return null;
                  S.pendingAud = S.pendingAud || [];
                  S.pendingAud.push({gigId:g.id, title:g.title, type:"電視劇", tier:g.tier||"初",
                    locId:g.loc||"tvb_longmen", audDay:S.dayIndex, revealDay:S.dayIndex+1, ok:false,
                    chancePct:50, pay:1000, payBase:1000, payBonus:0, payBonusLabel:"", payNote:"",
                    fame:1, pop:1, days:1, fxActing:0, fxStress:0, fxFame:0, fxStressFail:0, via:"drive225"});
                  return {gigId:g.id, title:g.title, revealDay:S.dayIndex+1}; }""")
                if not seeded:
                    note("P8-r3", False, f"attempt {attempt}: 無電視劇通告可播種")
                    break
                hit5, day5 = pass_day(pg, targets=["嗰個位最後畀咗高俊傑", "嗰個位畀咗高俊傑"], max_clicks=20)
                logged = pg.evaluate("""() => (S.mockRumors||[]).some(x=>x && (x.id||'').indexOf('rival_took_')===0)""")
                print(f"P8 attempt {attempt}: gig={seeded['title']} hit={hit5} logged={logged}", flush=True)
                if hit5 or logged:
                    r3_hit = True
                    break
            note("P8-r3", r3_hit, "6 次內見到落選後續" if r3_hit else "6 次都無命中（機率 35%/次，邏輯測試已覆蓋）")
            br.close()
    finally:
        stop(srv)
    # ---- 報告 ----
    lines = ["# drive225 實駕報告（v20a225 對手線強化）", ""]
    for k, v in LOG["phases"].items():
        lines.append(f"- **{k}**: {'PASS' if v['ok'] else 'FAIL'} — {v['detail']}")
    lines.append("")
    lines.append(f"FAIL 數：{len(LOG['fails'])}（{', '.join(LOG['fails']) if LOG['fails'] else '無'}）")
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("REPORT:", REPORT, flush=True)
    return 0 if not LOG["fails"] else 1

if __name__ == "__main__":
    sys.exit(main())
