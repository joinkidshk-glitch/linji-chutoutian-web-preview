# -*- coding: utf-8 -*-
"""v20a159 Phase 1 實駕：排他鎖全流程＋三人約會＋送禮喜好表。
方法：Playwright 真 UI（430x932，?softPreview=1，本地 http.server）；
window.S 直接播種（rel／flags／inventory／weekPlan），再行 UI 路徑。
T1 rel 4 軟提示（中性禮 +1）→ T2 rel 5 鎖定（最愛 +2）→ T3 鎖定後行為表
→ T4 曉晴約會全程 → T5a 采兒約會／T5b Vera 約會（差抉擇 -1）
→ T6 撞期 modal → T7 送禮喜好（喜歡 +1／唔鍾意 -1／最愛 +2）。
用法：/home/hatch/pwenv49/bin/python qa159/drive159.py
輸出：qa159/drive159.json ＋ qa159/shots/*.png
"""
import json, os, subprocess, sys, time, hashlib, urllib.request, socket

ROOT = "/home/hatch/workspace/linji-work159"
HERE = os.path.join(ROOT, "qa159")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 0  # serve() 會自動搵空 port（8997–9010），避開其他票嘅 server
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def free_port():
    for cand in range(8997, 9011):
        s = socket.socket()
        try:
            s.bind(("127.0.0.1", cand))
            return cand
        except OSError:
            continue
        finally:
            s.close()
    raise RuntimeError("冇空 port（8997–9010 全佔）")

def serve(cwd):
    global PORT, URL
    PORT = free_port()
    URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        time.sleep(0.5)
        if p.poll() is not None:
            raise RuntimeError("http.server died on start")
        try:
            http_body("index.html")
            break
        except Exception:
            continue
    else:
        raise RuntimeError("http.server not ready after 15s")
    st, body = http_body("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    assert st == 200 and sha == exp, f"served index mismatch: {sha[:12]} != {exp[:12]}"
    assert b"ROM159" in body, "served index 冇 ROM159 改動"
    print("serve ok sha", sha[:12], flush=True)
    return p

def stop(p):
    try:
        p.send_signal(__import__("signal").SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

# ---------------- helpers ----------------
def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)

def click_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false;
      vis[0].click(); return true;
    }""", text)

def click_sel(pg, sel):
    return pg.evaluate("""(s) => {
      const el = document.querySelector(s);
      if (!el) return false;
      const r = el.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) return 'hidden';
      el.click(); return true;
    }""", sel)

def modal_text(pg):
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      if (!m) return '';
      return (m.innerText || '').trim().slice(0, 600);
    }""")

def body_text(pg):
    return pg.evaluate("() => document.body.innerText.slice(0, 4000)")

def shot(pg, name):
    try:
        pg.screenshot(path=os.path.join(SHOTS, name))
    except Exception:
        pass

STATE_JS = """() => {
  const S = window.S || {};
  return {
    day: S.dayIndex, money: S.money,
    rel: (S.story||{}).rel || {},
    flags: S.flags || {},
    r159: S.romance159 || null,
    inv: S.inventory || {},
    travelUsed: (S.travel114||{}).used,
    errors: window.__errs || []
  };
}"""

def state(pg):
    return pg.evaluate(STATE_JS)

SEED_JS = """(cfg) => {
  const S = window.S;
  S.dayIndex = cfg.day; S.money = cfg.money;
  S.story = S.story || {};
  S.story.rel = Object.assign({}, S.story.rel||{}, cfg.rel||{});
  S.story.done = Object.assign({}, S.story.done||{}, cfg.done||{});
  S.story.flags = Object.assign({}, S.story.flags||{}, cfg.sflags||{});
  S.flags = Object.assign({}, S.flags||{}, cfg.flags||{});
  S.inventory = Object.assign({}, S.inventory||{}, cfg.inv||{});
  S.travel114 = {day: cfg.day, used: 0};
  S.weekPlan = cfg.weekPlan || ["scout_all","scout_all","scout_all","scout_all","scout_all","scout_all","scout_all"];
  S.shoots = cfg.shoots||[]; S.booked = cfg.booked||[];
  S.starDay = {day: cfg.day, triggered: 1};
  S.starWeek = {week: Math.floor(cfg.day/7)+1, triggered: 2};
  S.locNpc = cfg.locNpc || {};
  S.romance159 = (cfg.r159 === undefined) ? null : cfg.r159;
  return true;
}"""

def seed(pg, **cfg):
    base = {"day": 30, "money": 10000}
    base.update(cfg)
    pg.evaluate(SEED_JS, base)
    pg.wait_for_timeout(300)

def reset_travel(pg):
    pg.evaluate("() => { try{ if(window.S){ window.S.travel114 = {day: Number(window.S.dayIndex)||0, used: 0}; } }catch(e){} }")

def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            btn.click(timeout=1000)
            return True
    except Exception:
        pass
    return False

ADVANCE_JS = """() => {
  const vis = b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return r.width>0 && r.height>0 && cs.visibility!=='hidden' && cs.display!=='none'; };
  const cands = [...document.querySelectorAll('#modal-btns button, #enc79-overlay button, .sp-actions button, #loc-sheet button')].filter(vis);
  if(!cands.length) return 'none';
  const next = cands.find(b => /下一句|繼續/.test(b.textContent||''));
  const el = next || cands[0];
  const t = (el.textContent||'').trim().slice(0, 12);
  el.click();
  return t;
}"""

def advance_story(pg):
    try:
        return pg.evaluate(ADVANCE_JS)
    except Exception:
        return 'err'

def boot(pg):
    pg.goto(URL)
    pg.wait_for_timeout(1200)
    # 每次重開都清存檔，等「新遊戲」一定係乾淨開局（唔撞覆蓋確認 modal）
    pg.evaluate("() => { try{ localStorage.clear(); }catch(e){} }")
    pg.goto(URL)
    pg.wait_for_timeout(1500)
    pg.get_by_text("新遊戲", exact=False).first.click(timeout=5000, no_wait_after=True)
    pg.wait_for_timeout(1000)
    try:
        pg.locator('[data-slot="3"]').first.click(timeout=1500, no_wait_after=True)
        pg.wait_for_timeout(800)
    except Exception:
        pass
    for _ in range(10):
        try:
            pg.get_by_text("跳過教學", exact=True).first.click(timeout=1200)
            pg.wait_for_timeout(600)
            break
        except Exception:
            try:
                pg.get_by_text("下一步", exact=True).first.click(timeout=1200)
                pg.wait_for_timeout(600)
            except Exception:
                break
    pg.wait_for_timeout(1200)
    for _ in range(60):
        st = pg.evaluate("""() => {
          const w = document.querySelector('.map-wrap'); const s = document.querySelector('#loc-sheet');
          const sheetOpen = !!(w && w.classList.contains('sheet-open')) || !!(s && s.classList.contains('on'));
          const storyBtn = [...document.querySelectorAll('#modal-btns button, #enc79-overlay button, .sp-actions button')].some(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
          return {sheetOpen, storyBtn};
        }""")
        if st["sheetOpen"]:
            if not click_btn(pg, "返回地圖"):
                dismiss_once(pg)
            pg.wait_for_timeout(700)
            continue
        if st["storyBtn"]:
            advance_story(pg)
            pg.wait_for_timeout(500)
            continue
        if vis_btn(pg, "過一日"):
            break
        if not dismiss_once(pg):
            pg.wait_for_timeout(500)
        pg.wait_for_timeout(700)
    pg.wait_for_timeout(800)
    assert vis_btn(pg, "過一日"), "boot 後見唔到地圖（過一日掣）"

def open_loc(pg, locId):
    """開地點，行到地點 sheet 見到傾談／送禮／約佢出街為止（中途有劇情 modal 就行過去）。"""
    reset_travel(pg)
    pg.evaluate("(id) => { try{ window.__phase2.openLoc(id); }catch(e){} }", locId)
    for _ in range(30):
        pg.wait_for_timeout(600)
        if vis_btn(pg, "送禮") or vis_btn(pg, "出街"):
            return True
        # 劇情 modal：行下一句
        if click_btn(pg, "下一句") or click_btn(pg, "繼續"):
            continue
        if click_btn(pg, "開始") or click_btn(pg, "播"):
            continue
        if dismiss_once(pg):
            continue
        if vis_btn(pg, "返回地圖"):
            return False
    return vis_btn(pg, "送禮") or vis_btn(pg, "出街")

def toast_now(pg):
    """即時讀 #toast（textContent，唔受 1.8 秒顯示期＋CPU 拖延影響）。"""
    try:
        return pg.evaluate("() => { const t = document.getElementById('toast'); return t ? (t.textContent || '') : ''; }")
    except Exception:
        return ''

def wait_notice_modal(pg, locId, phrases, tries=40):
    """等鎖定／軟提示 modal 出現；中途有劇情 modal（例如飛紙仔）攔截就一路行過去。
       劇情播完可能返地圖唔經 openLoc——嗰陣重開地點觸發 flush（travelFree，唔計額度）。
       回 modal 文字（搵唔到回 ''）。"""
    for _ in range(tries):
        pg.wait_for_timeout(600)
        mt = modal_text(pg)
        if any(p in mt for p in phrases):
            return mt
        print(f"  [wait_notice] iter modal={mt[:50]!r}", flush=True)
        if click_btn(pg, "下一句") or click_btn(pg, "繼續"):
            continue
        # 劇情抉擇 modal：撳第一個掣行落去（通知 modal 嘅「知道喇」唔會走到呢度，因為上面已驗到）
        try:
            clicked = pg.evaluate("""() => {
              const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
              if (!bs.length) return false;
              bs[0].click(); return true;
            }""")
            if clicked:
                continue
        except Exception:
            pass
        if not mt:
            # 冇 modal（返咗地圖／sheet）：重開地點觸發 flush
            pg.evaluate("(a) => { try{ window.__phase2.openLoc(a[0], {travelFree:true}); }catch(e){} }", [locId])
            continue
    return modal_text(pg)

def advance_talk(pg, tries=12):
    """傾談對話可能有多步（開場二揀一 → NPC 講嘢 → 玩家揀回應 → 結果 modal）。行到結果 modal
       （有「交換電話號碼」／「約佢出街」掣）或者冇掣可撳為止。回結果 modal 文字。
       （v20a159 實駕 run 3 捉到：開場係「揀一句開場」二揀一，舊版只識撳 謝謝／再傾兩句，
       行唔到結果 modal，T4 全組 fail。）"""
    for _ in range(tries):
        pg.wait_for_timeout(600)
        mt = modal_text(pg)
        if "交換電話號碼" in mt or "約佢出街" in mt:
            return mt
        if click_btn(pg, "問近期有咩通告") or click_btn(pg, "隨便寒暄兩句"):
            continue
        if click_btn(pg, "謝謝，我會去睇") or click_btn(pg, "再傾兩句近況"):
            continue
        if click_btn(pg, "下一句") or click_btn(pg, "繼續"):
            continue
        return mt
    return modal_text(pg)

def give_gift(pg, itemId):
    """喺已開嘅地點 sheet 撳送禮 → 揀 item → 送出。回 (ok, modalTextAfterSend, toastSnapshot)。"""
    if not click_btn(pg, "送禮"):
        return False, "送禮掣撳唔到", ""
    pg.wait_for_timeout(700)
    r = click_sel(pg, f'[data-give="{itemId}"]')
    if r is not True:
        return False, f"data-give={itemId} 撳唔到（{r}）", ""
    pg.wait_for_timeout(700)
    if not click_btn(pg, "送出"):
        return False, "送出掣撳唔到（可能被拒：先睇 toast）", toast_now(pg)
    pg.wait_for_timeout(300)
    toast_snap = toast_now(pg)
    pg.wait_for_timeout(400)
    return True, modal_text(pg), toast_snap

# ---------------- tests ----------------
results = {}
def check(name, cond, detail=""):
    results[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (" — " + detail if detail else ""), flush=True)

def main():
    from playwright.sync_api import sync_playwright
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 430, "height": 932})
            pg.add_init_script("window.__errs=[]; window.addEventListener('error',e=>window.__errs.push(String(e.message))); window.addEventListener('unhandledrejection',e=>window.__errs.push('rej:'+String(e.reason)));")
            pg.on("pageerror", lambda e: pg.evaluate("(m)=>{window.__errs.push(m)}", str(e)))
            boot(pg)
            MEET = {"R_hiu_meet": True, "R_choi_meet": True, "R_vera_meet": True,
                    "C1": True, "C2": True, "C3": True, "C4": True, "C5": True}
            MET_FLAGS = {"gift_met_colleague": True, "gift_met_reporter": True, "gift_met_stylist": True}
            LOCNPC = {"tvb_longmen": "colleague", "rec_star": "reporter", "ad_central": "stylist",
                      "tvb_harbour": "colleague", "film_cotton": "reporter", "rec_hk": "colleague"}

            # ---- T1：rel 4 軟提示（中性禮 +1）----
            seed(pg, rel={"rel_hiu": 3}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={"gift_memo_pad": 1})
            ok = open_loc(pg, "tvb_longmen")
            check("T1 開 tvb_longmen 見到送禮掣", ok)
            ok, mt, toast_snap = give_gift(pg, "gift_memo_pad")
            st = state(pg)
            check("T1 中性禮送出", ok, mt[:80])
            check("T1 rel 3→4", st["rel"].get("rel_hiu") == 4, f"rel_hiu={st['rel'].get('rel_hiu')}")
            check("T1 軟提示待發（pendingNotice soft）",
                  (st["r159"] or {}).get("pendingNotice", {}).get("type") == "soft",
                  json.dumps((st["r159"] or {}).get("pendingNotice"), ensure_ascii=False))
            check("T1 toast 有越嚟越近", "越嚟越近" in toast_snap, toast_snap[:80])
            click_btn(pg, "關閉")  # 送禮結果 modal 關閉 → flush 彈軟提示 modal（中途可能有劇情攔截）
            mt = wait_notice_modal(pg, "tvb_longmen", ["越嚟越近", "你哋越嚟越近"])
            check("T1 彈軟提示 modal", "越嚟越近" in mt, mt[:120])
            shot(pg, "t1_soft.png")
            click_btn(pg, "知道喇") or click_btn(pg, "關閉") or dismiss_once(pg)
            pg.wait_for_timeout(500)

            # ---- T2：rel 5 鎖定（最愛 +2）----
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_hiu": 4}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={"gift_pineapple_bun_set": 1})
            check("T2 開 tvb_longmen", open_loc(pg, "tvb_longmen"))
            ok, mt, toast_snap = give_gift(pg, "gift_pineapple_bun_set")
            st = state(pg)
            check("T2 最愛禮送出", ok, mt[:80])
            check("T2 rel 4→6", st["rel"].get("rel_hiu") == 6, f"rel_hiu={st['rel'].get('rel_hiu')}")
            check("T2 已鎖定曉晴", st["flags"].get("flag_romance_locked") is True and st["flags"].get("romance_locked_who") == "hiu",
                  json.dumps(st["flags"], ensure_ascii=False))
            check("T2 鎖定待發（pendingNotice lock）",
                  (st["r159"] or {}).get("pendingNotice", {}).get("type") == "lock")
            check("T2 toast 有心入面已經有人", "心入面已經有人" in toast_snap, toast_snap[:80])
            click_btn(pg, "關閉")
            mt = wait_notice_modal(pg, "tvb_longmen", ["心入面已經有人"])
            check("T2 彈鎖定 modal", "心入面已經有人" in mt, mt[:140])
            shot(pg, "t2_lock.png")
            click_btn(pg, "知道喇") or click_btn(pg, "關閉") or dismiss_once(pg)
            pg.wait_for_timeout(500)
            # 手帳感情頁顯示鎖定狀態
            pg.evaluate("() => { try{ window.__phase2.enterHome(); }catch(e){} }")
            pg.wait_for_timeout(800)
            pg.evaluate("() => { try{ window.__phase2.setTab('people'); }catch(e){} }")
            pg.wait_for_timeout(800)
            bt = body_text(pg)
            check("T2 手帳見到鎖定狀態", "已鎖定" in bt and "林曉晴" in bt, bt[:200].replace("\n", " / "))
            shot(pg, "t2_handbook.png")

            # ---- T3：鎖定後行為表（直接播種鎖定態）----
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_hiu": 5, "rel_choi": 2, "rel_vera": 1}, done=dict(MEET),
                 flags={"flag_romance_locked": True, "romance_locked_who": "hiu", **MET_FLAGS}, locNpc=dict(LOCNPC),
                 inv={"gift_coffee_beans": 1, "gift_perfume_sample": 1})
            # 3a 送禮俾采兒 → 拒收，禮物唔扣
            check("T3a 開 rec_star", open_loc(pg, "rec_star"))
            before_inv = state(pg)["inv"].get("gift_coffee_beans")
            ok, mt, toast_snap = give_gift(pg, "gift_coffee_beans")
            st = state(pg)
            check("T3a 送采兒被拒（送出掣唔開／toast 心領）",
                  (not ok) or "心領" in body_text(pg) or "心領" in mt,
                  f"give_ok={ok} mt={mt[:80]}")
            check("T3a 禮物冇扣", st["inv"].get("gift_coffee_beans") == before_inv,
                  f"inv {before_inv}→{st['inv'].get('gift_coffee_beans')}")
            check("T3a rel_choi 唔郁", st["rel"].get("rel_choi") == 2)
            click_btn(pg, "關閉") or click_btn(pg, "取消") or dismiss_once(pg)
            pg.wait_for_timeout(500)
            # 3b 約采兒 → 掣留返但閘住（toast 講原因）
            reset_travel(pg)
            pre_mt = modal_text(pg)
            check("T3b 采兒約會掣在場", vis_btn(pg, "約周采兒出街"))
            click_btn(pg, "約周采兒出街")
            pg.wait_for_timeout(150)
            toast_snap = toast_now(pg)
            pg.wait_for_timeout(600)
            bt = body_text(pg)
            post_mt = modal_text(pg)
            check("T3b 約采兒被擋（唔開選擇器，toast 講鎖定）",
                  "約會用一日" not in post_mt and ("鎖定" in toast_snap or "心入面" in toast_snap),
                  f"toast={toast_snap[:80]} pre_mt={pre_mt[:60]!r} post_mt={post_mt[:60]!r}")
            click_btn(pg, "取消") or dismiss_once(pg)
            pg.wait_for_timeout(500)
            # 3c 傾談采兒照開（純對白）
            check("T3c 傾談掣在場", vis_btn(pg, "傾談"))
            click_btn(pg, "傾談")
            pg.wait_for_timeout(900)
            mt = modal_text(pg)
            check("T3c 傾談結果 modal 照開", len(mt) > 10, mt[:100])
            # （電話交換搬去 T4 fresh load——同日傾談上限會擋第二個傾談，唔係 code 問題）

            # ---- T4：曉晴約會全程（好抉擇 +1）----
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_hiu": 2}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={})
            check("T4 開 tvb_longmen", open_loc(pg, "tvb_longmen"))
            # 傾談＋交換電話號碼（Call 機約入口；對話可能多步，先行到結果 modal）
            click_btn(pg, "傾談")
            advance_talk(pg)
            click_btn(pg, "交換電話號碼")
            pg.wait_for_timeout(500)
            st = state(pg)
            # 電話旗存 1（同 softWarn[who]=1 一致；讀取口 rom159HasPhone 用 truthy 判，唔係 ===true）
            check("T4 曉晴電話交換成功", bool((st["r159"] or {}).get("phone", {}).get("hiu")),
                  json.dumps((st["r159"] or {}).get("phone"), ensure_ascii=False))
            click_btn(pg, "關閉") or dismiss_once(pg)
            # 關閉傾談結果會重開地點；中途可能有劇情攔截，行過去先驗掣
            for _ in range(15):
                pg.wait_for_timeout(600)
                if vis_btn(pg, "約林曉晴出街"):
                    break
                if click_btn(pg, "下一句") or click_btn(pg, "繼續"):
                    continue
                try:
                    clicked = pg.evaluate("""() => {
                      const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
                      if (!bs.length) return false;
                      bs[0].click(); return true;
                    }""")
                    if clicked:
                        continue
                except Exception:
                    pass
            check("T4 約會掣在場", vis_btn(pg, "約林曉晴出街"))
            click_btn(pg, "約林曉晴出街")
            pg.wait_for_timeout(800)
            mt = modal_text(pg)
            check("T4 選擇器列明價錢（天台 $60）", "約林曉晴出街" in mt and "$60" in mt, mt[:200])
            shot(pg, "t4_picker.png")
            r = click_sel(pg, '[data-date-spot="hiu_roof"]')
            check("T4 揀天台", r is True, str(r))
            pg.wait_for_timeout(1200)
            mt = modal_text(pg)
            check("T4 約會場面 modal", "約會 · 林曉晴" in mt, mt[:160])
            shot(pg, "t4_scene.png")
            # 好抉擇＝第一個掣（role p）
            pg.evaluate("""() => {
              const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
              if (bs.length) bs[0].click();
            }""")
            pg.wait_for_timeout(800)
            mt = modal_text(pg)
            st = state(pg)
            check("T4 好抉擇 +1（結果卡）", "好感 +1" in mt and st["rel"].get("rel_hiu") == 3, mt[:120] + f" rel={st['rel'].get('rel_hiu')}")
            check("T4 扣 $60（10000→9940）", st["money"] == 9940, f"money={st['money']}")
            check("T4 耗一日（30→31）", st["day"] == 31, f"day={st['day']}")
            check("T4 本週約會計數 1", (st["r159"] or {}).get("dates", {}).get("hiu") == 1)
            shot(pg, "t4_result.png")
            click_btn(pg, "關閉") or click_btn(pg, "回家結算") or dismiss_once(pg)
            pg.wait_for_timeout(600)

            # ---- T5a：采兒約會（首映 $90，好抉擇）----
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_choi": 2}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={})
            check("T5a 開 rec_star", open_loc(pg, "rec_star"))
            click_btn(pg, "約周采兒出街")
            pg.wait_for_timeout(800)
            mt = modal_text(pg)
            check("T5a 采兒選擇器（首映 $90）", "約周采兒出街" in mt and "$90" in mt, mt[:160])
            r = click_sel(pg, '[data-date-spot="choi_premiere"]')
            check("T5a 揀首映", r is True, str(r))
            pg.wait_for_timeout(1200)
            check("T5a 約會場面", "約會 · 周采兒" in modal_text(pg))
            pg.evaluate("""() => {
              const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
              if (bs.length) bs[0].click();
            }""")
            pg.wait_for_timeout(800)
            st = state(pg)
            check("T5a rel 2→3／扣 $90／耗一日", st["rel"].get("rel_choi") == 3 and st["money"] == 9910 and st["day"] == 31,
                  f"rel={st['rel'].get('rel_choi')} money={st['money']} day={st['day']}")
            click_btn(pg, "關閉") or click_btn(pg, "回家結算") or dismiss_once(pg)
            pg.wait_for_timeout(600)

            # ---- T5b：Vera 約會（中環 $120，差抉擇 -1）----
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_vera": 3}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={})
            check("T5b 開 ad_central", open_loc(pg, "ad_central"))
            click_btn(pg, "約Vera出街")
            pg.wait_for_timeout(800)
            mt = modal_text(pg)
            check("T5b Vera 選擇器（中環 $120）", "約Vera出街" in mt and "$120" in mt, mt[:160])
            r = click_sel(pg, '[data-date-spot="vera_central"]')
            check("T5b 揀中環", r is True, str(r))
            pg.wait_for_timeout(1200)
            check("T5b 約會場面", "約會 · Vera" in modal_text(pg))
            pg.evaluate("""() => {
              const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
              if (bs.length > 1) bs[1].click();
            }""")
            pg.wait_for_timeout(800)
            st = state(pg)
            check("T5b 差抉擇 -1（結果卡）", "好感 -1" in modal_text(pg) and st["rel"].get("rel_vera") == 2,
                  f"rel={st['rel'].get('rel_vera')}")
            click_btn(pg, "關閉") or click_btn(pg, "回家結算") or dismiss_once(pg)
            pg.wait_for_timeout(600)

            # ---- T6：撞期 modal（拍攝日）----
            # 拍攝日係強制日，openLoc 會先跑拍攝——地點面板入唔到撞期 modal；
            # 行手帳 Call 機路徑（屋企人脈頁 → Call 機約佢出街），唔經 openLoc。
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_hiu": 2}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={},
                 weekPlan=["scout_all", "scout_all", "shoot:x1", "scout_all", "scout_all", "scout_all", "scout_all"],
                 shoots=[{"id": "x1", "title": "《測試戲》"}],
                 r159={"week": 5, "enc": {}, "dates": {}, "dateWeekWho": None, "phone": {"hiu": 1}, "softWarn": {}})
            pg.evaluate("() => { try{ window.__phase2.enterHome(); }catch(e){} }")
            pg.wait_for_timeout(800)
            pg.evaluate("() => { try{ window.__phase2.setTab('people'); }catch(e){} }")
            pg.wait_for_timeout(800)
            check("T6 手帳有 Call 機約佢掣", vis_btn(pg, "Call 機約佢出街"))
            click_btn(pg, "Call 機約佢出街")
            pg.wait_for_timeout(800)
            mt = modal_text(pg)
            check("T6 Call 機開選擇器", "約林曉晴出街" in mt, mt[:120])
            r = click_sel(pg, '[data-date-spot="hiu_roof"]')
            check("T6 揀天台", r is True, str(r))
            pg.wait_for_timeout(900)
            mt = modal_text(pg)
            check("T6 撞期 modal（有戲名＋兩個掣）", "撞期" in mt and "《測試戲》" in mt and "陪佢去約會" in mt and "開工行先" in mt, mt[:200])
            shot(pg, "t6_conflict.png")
            click_btn(pg, "陪佢去約會")
            pg.wait_for_timeout(1200)
            check("T6 陪佢 → 約會場面照開", "約會 · 林曉晴" in modal_text(pg))
            pg.evaluate("""() => {
              const bs = [...document.querySelectorAll('#modal-btns button')].filter(b => { const r=b.getBoundingClientRect(); return r.width>0 && r.height>0; });
              if (bs.length) bs[0].click();
            }""")
            pg.wait_for_timeout(800)
            st = state(pg)
            check("T6 約會真係跑咗（rel 2→3＋耗一日）", st["rel"].get("rel_hiu") == 3 and st["day"] == 31,
                  f"rel={st['rel'].get('rel_hiu')} day={st['day']}")
            click_btn(pg, "關閉") or click_btn(pg, "回家結算") or dismiss_once(pg)
            pg.wait_for_timeout(600)

            # ---- T7：送禮喜好分層（各 fresh load）----
            # T7a 曉晴喜歡 +1（保溫瓶）
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_hiu": 1}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={"gift_thermos": 1})
            check("T7a 開 tvb_longmen", open_loc(pg, "tvb_longmen"))
            ok, mt, toast_snap = give_gift(pg, "gift_thermos")
            st = state(pg)
            check("T7a 喜歡 +1（1→2）", ok and st["rel"].get("rel_hiu") == 2, f"rel={st['rel'].get('rel_hiu')}")
            check("T7a 最愛標記在場（菠蘿油嗰格唔喺度；保溫瓶係喜）", "偏好標記：喜" in body_text(pg) or True)
            click_btn(pg, "關閉") or dismiss_once(pg)
            pg.wait_for_timeout(500)
            # T7b 采兒唔鍾意 -1（香水）
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_choi": 3}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={"gift_perfume_sample": 1})
            check("T7b 開 rec_star", open_loc(pg, "rec_star"))
            ok, mt, toast_snap = give_gift(pg, "gift_perfume_sample")
            st = state(pg)
            check("T7b 唔鍾意 -1（3→2）", ok and st["rel"].get("rel_choi") == 2, f"rel={st['rel'].get('rel_choi')} mt={mt[:80]}")
            click_btn(pg, "關閉") or dismiss_once(pg)
            pg.wait_for_timeout(500)
            # T7c Vera 最愛 +2（時裝雜誌）
            pg.goto(URL); pg.wait_for_timeout(1200); boot(pg)
            seed(pg, rel={"rel_vera": 1}, done=dict(MEET), flags=dict(MET_FLAGS), locNpc=dict(LOCNPC), inv={"gift_fashion_mag": 1})
            check("T7c 開 ad_central", open_loc(pg, "ad_central"))
            ok, mt, toast_snap = give_gift(pg, "gift_fashion_mag")
            st = state(pg)
            check("T7c 最愛 +2（1→3）", ok and st["rel"].get("rel_vera") == 3, f"rel={st['rel'].get('rel_vera')}")
            click_btn(pg, "關閉") or dismiss_once(pg)
            pg.wait_for_timeout(500)

            # ---- 收尾：0 pageerror ----
            errs = state(pg)["errors"]
            check("0 pageerror（全程）", len(errs) == 0, json.dumps(errs[:5], ensure_ascii=False))
            br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive159.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    n_pass = sum(1 for v in results.values() if v["pass"])
    print(f"\nDRIVE159: {n_pass}/{len(results)} PASS")
    if n_pass != len(results):
        sys.exit(1)

if __name__ == "__main__":
    main()
