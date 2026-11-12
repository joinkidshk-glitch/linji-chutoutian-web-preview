# -*- coding: utf-8 -*-
"""v20a116 實駕：機構老闆立繪 v2/v2b 換入上線（全 UI 路徑）。
  本地鏡像（work116）＋ Playwright 390x844 ＋可棄用槽 3。
  每間 loc：地圖 pin → 地點 sheet「只查看通告欄」→ 通告欄 modal → 撳第一張
  .gig-teaser → 通告詳情 modal → 驗 #modal-inner 英雄圖 img src 係新檔
  （_v2/_v2b）＋ naturalWidth>0 → 截圖 3 張代表（沈卓衡、羅勁威、溫子峰）。
  攔截（巧遇對話／WF4 事件／主線）：循環撳「下一句」等推進掣直至 sheet 開到。
  當日 board 冇通告嗰間：跳季重試（S.dayIndex 撥去春／夏／秋季再開 board；
  只係槽 3 測試存檔，唔影響真存檔）。
  v114 出行額度：入地點每日限 2 次——每開 2 間就 S.dayIndex+1（聽日重置額度），
  全程留喺冬季（day 0–11），board 季節不變。
  另驗：全程 0 pageerror、boss 圖 0 失敗請求（404）。
用法：/home/hatch/pwenv49/bin/python qa116/drive116.py
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
W116 = os.path.dirname(HERE)
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8961
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107"
LOG = {"locs": {}, "board_probe": {}, "errors": [], "failed_requests": []}

EXPECTED = {
    "tvb_longmen": ("沈卓衡", "boss_tvb_longmen_v2b_base.webp"),
    "film_lion": ("羅勁威", "boss_film_lion_v2b_base.webp"),
    "ad_adm": ("方樂怡", "boss_ad_adm_v2_base.webp"),
    "ad_central": ("霍君豪", "boss_ad_central_v2_base.webp"),
    "rec_hk": ("伍兆昌", "boss_rec_hk_v2_base.webp"),
    "tvb_kowloon": ("陶映紅", "boss_tvb_kowloon_v2_base.webp"),
    "film_cotton": ("鄭伯康", "boss_film_cotton_v2_base.webp"),
    "rec_wanchai": ("梁廣成", "boss_rec_wanchai_v2b_base.webp"),
    "tvb_harbour": ("顧學禮", "boss_tvb_harbour_v2b_base.webp"),
    "film_harbour": ("夏文心", "boss_film_harbour_v2_base.webp"),
    "rec_star": ("溫子峰", "boss_rec_star_v2_base.webp"),
}
SHOT_LOCS = ["tvb_longmen", "film_lion", "rec_star"]
# 季跳重試：dayIndex → 季（1990-01-01 起計；春約 day 80、夏約 day 170、秋約 day 260）
SEASON_JUMPS = [80, 170, 260]
NEXT_TEXTS = ["下一句", "繼續", "睇落去", "明白", "知道了", "我知道了", "好"]

def http_get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} probably taken)")
    st, body = http_get("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    if st != 200 or sha != exp:
        raise RuntimeError(f"served index mismatch: status={st} sha={sha[:12]} expected={exp[:12]}")
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def click_first(pg, texts, wait=800):
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

def new_game(pg):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    for _ in range(4):
        if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    pg.wait_for_timeout(1500)

def sheet_open(pg):
    """地點 sheet 係咪開咗（有「只查看通告欄」掣）。"""
    return pg.evaluate("""() => {
      const b = Array.from(document.querySelectorAll('#loc-acts button, #loc-sheet button'))
        .find(x => x.offsetParent !== null && x.textContent.includes('只查看通告欄'));
      return !!b; }""")

def dismiss_interceptors(pg, tries=60):
    """撳走巧遇對話／WF4／主線攔截，直至 sheet 開到或撳無可撳。
       WF4 流程：繼續（中途）→ 睇落去（最尾）→ 有選項就揀第一個 → 好。
       ENC79 巧遇對話掣係 .e79-btn（唔喺 #modal-btns 入面），選項文字任意。
       後備只撳 #modal-btns／.e79-btn 第一粒可見掣，唔掂地圖掣；連續 3 次無掣可撳先放棄
       （對話換拍之間可能有短暫空窗）。選項揀第一個（槽 3 測試檔，好感輕微影響可接受）。"""
    no_hit = 0
    for _ in range(tries):
        if sheet_open(pg):
            return True
        hit = pg.evaluate("""(texts) => {
          const els = Array.from(document.querySelectorAll('button, a'));
          for (const t of texts) {
            const el = els.find(x => x.offsetParent !== null && x.textContent.trim() === t);
            if (el) { el.click(); return t; }
          }
          // 後備：WF4 選項／ENC79 選項（任意文字）——只撳 modal／巧遇掣列第一粒
          const fb = Array.from(document.querySelectorAll('#modal-btns button, .e79-btn'))
            .find(x => x.offsetParent !== null);
          if (fb) { fb.click(); return 'fallback:' + fb.textContent.trim().slice(0, 12); }
          return null; }""", NEXT_TEXTS)
        if not hit:
            no_hit += 1
            if no_hit >= 3:
                return sheet_open(pg)
        else:
            no_hit = 0
        pg.wait_for_timeout(700)
    return sheet_open(pg)

def open_board(pg):
    """sheet 入面撳「只查看通告欄」，回傳 teaser 數（-1 = 撳唔到）。"""
    ok = pg.evaluate("""() => {
      const b = Array.from(document.querySelectorAll('#loc-acts button, #loc-sheet button'))
        .find(x => x.offsetParent !== null && x.textContent.includes('只查看通告欄'));
      if (!b) return false; b.click(); return true; }""")
    if not ok:
        return -1
    pg.wait_for_timeout(1200)
    return pg.evaluate("() => document.querySelectorAll('#modal-inner .gig-teaser').length")

def js_click(pg, js_expr, wait=700):
    """經 JS 直接 el.click()（繞過 Playwright hit-target 檢查；app 掣係 onclick，synthetic click 有效）。"""
    r = pg.evaluate(js_expr)
    pg.wait_for_timeout(wait)
    return r

def map_clear(pg):
    """地圖係咪返到可撳狀態（#mask 唔係 .on、無 modal 內容）。"""
    return pg.evaluate("""() => {
      const mask = document.getElementById('mask');
      const maskOn = mask && mask.classList.contains('on');
      const modalInner = document.getElementById('modal-inner');
      const modalOpen = modalInner && modalInner.innerHTML.trim().length > 0
        && modalInner.offsetParent !== null;
      return {maskOn: !!maskOn, modalOpen: !!modalOpen}; }""")

def close_to_map(pg):
    """由 board/detail 返到地圖：離開（detail）→ 返地點選單（board）→ 返回地圖（sheet）。
       全部經 JS click，逐段驗狀態，最多重試一次。"""
    for _ in range(2):
        js_click(pg, """() => { const b = document.querySelector('#modal-btns .btn_leave');
          if (b) { b.click(); return 'btn_leave'; }
          const els = Array.from(document.querySelectorAll('#modal-btns button'))
            .find(x => x.offsetParent !== null && x.textContent.includes('離開'));
          if (els) { els.click(); return 'leave-text'; } return null; }""")
        js_click(pg, """() => { const b = Array.from(document.querySelectorAll('#modal-btns button, button'))
          .find(x => x.offsetParent !== null && x.textContent.trim() === '返地點選單');
          if (b) { b.click(); return true; } return false; }""")
        js_click(pg, """() => { const b = document.getElementById('loc-close');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        st = map_clear(pg)
        if not st["maskOn"] and not st["modalOpen"]:
            return True
    return map_clear(pg)

def check_detail(pg, loc, name, fname):
    """開咗詳情 modal 後驗英雄圖。回傳 (pass, hero_list)。"""
    pg.wait_for_timeout(900)
    hero = pg.evaluate("""() => {
      const scope = document.getElementById('modal-inner') || document;
      return Array.from(scope.querySelectorAll('img'))
        .map(im => ({src: im.getAttribute('src') || '', full: im.currentSrc || im.src,
                     w: im.naturalWidth, h: im.naturalHeight, complete: im.complete}))
        .filter(x => x.full.includes('boss_')); }""")
    good = [h for h in hero if fname in h["full"] and h["w"] > 0]
    return (len(good) >= 1), hero

def drive_one_loc(pg, loc, name, fname):
    """開一間 loc 嘅通告詳情並驗圖。回傳 dict。"""
    st = map_clear(pg)
    if st["maskOn"] or st["modalOpen"]:
        if not close_to_map(pg):
            return {"name": name, "pass": False, "reason": f"map not clear before pin: {st}"}
    ok = pg.evaluate(f"""() => {{ const p = document.querySelector('button.pin[data-loc="{loc}"]');
      if (!p) return false; p.click(); return true; }}""")
    if not ok:
        return {"name": name, "pass": False, "reason": "map pin not found"}
    pg.wait_for_timeout(900)
    if not dismiss_interceptors(pg):
        return {"name": name, "pass": False, "reason": "sheet never opened (interceptor stuck)"}
    n = open_board(pg)
    if n < 0:
        return {"name": name, "pass": False, "reason": "board button not found"}
    if n == 0:
        close_to_map(pg)
        return {"name": name, "pass": False, "reason": "board empty today", "empty_board": True}
    # 撳第一張 teaser → 詳情
    pg.evaluate("""() => { const c = document.querySelector('#modal-inner .gig-teaser');
      if (c) c.click(); }""")
    passed, hero = check_detail(pg, loc, name, fname)
    if loc in SHOT_LOCS:
        pg.screenshot(path=os.path.join(SHOTS, f"boss_{loc}.png"))
    # 詳情 → 返 board → 返 sheet → 返地圖
    back = close_to_map(pg)
    return {"name": name, "pass": passed, "hero": hero, "teasers": n,
            "back_to_map": back}

def main():
    srv = serve(W116)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 844})
            pg.on("pageerror", lambda e: LOG["errors"].append(str(e)))
            pg.on("requestfailed", lambda r: LOG["failed_requests"].append(r.url))
            pg.on("response", lambda r: LOG["failed_requests"].append(r.url) if r.status >= 400 else None)
            new_game(pg)
            print("GIGS in page:", pg.evaluate("() => (window.GIGS || []).length"))
            # 探針：當日各 pin 嘅 board 數（aria-label「通告欄 N 則」）
            LOG["board_probe"] = pg.evaluate("""() => {
              const out = {};
              for (const b of document.querySelectorAll('button.pin[data-loc]')) {
                out[b.dataset.loc] = b.getAttribute('aria-label') || '';
              } return out; }""")
            for loc, lab in LOG["board_probe"].items():
                if loc in EXPECTED:
                    print(f"probe {loc}: {lab}")
            pending = []
            entries = 0  # v114 出行額度：入地點每日限 2 次，滿 2 間就撥一日重置
            for loc, (name, fname) in EXPECTED.items():
                if entries >= 2:
                    pg.evaluate("() => { S.dayIndex = (S.dayIndex|0) + 1; }")
                    pg.wait_for_timeout(600)
                    entries = 0
                try:
                    res = drive_one_loc(pg, loc, name, fname)
                except Exception as e:
                    res = {"name": name, "pass": False, "reason": f"drive exception: {e!r}"}
                    try:
                        close_to_map(pg)
                    except Exception:
                        pass
                entries += 1
                LOG["locs"][loc] = res
                print(("PASS " if res.get("pass") else "FAIL ") + f"{loc} {name}: {res}")
                if res.get("empty_board"):
                    pending.append(loc)
            # 季跳重試：board 當日冇通告嗰啲
            for loc in pending:
                name, fname = EXPECTED[loc]
                done = False
                for day in SEASON_JUMPS:
                    pg.evaluate(f"() => {{ S.dayIndex = {day}; }}")
                    pg.wait_for_timeout(600)
                    res = drive_one_loc(pg, loc, name, fname)
                    if res.get("pass"):
                        res["season_jump_day"] = day
                        LOG["locs"][loc] = res
                        print(f"PASS {loc} {name} (season jump day {day}): {res}")
                        done = True
                        break
                    if not res.get("empty_board"):
                        LOG["locs"][loc] = res
                        print(f"FAIL {loc} {name} (season jump day {day}): {res}")
                        done = True
                        break
                if not done:
                    print(f"FAIL {loc} {name}: board empty in all tried seasons")
            br.close()
    finally:
        stop(srv)
    n_pass = sum(1 for v in LOG["locs"].values() if v.get("pass"))
    boss_failed = [u for u in LOG["failed_requests"] if "boss_" in u]
    other_failed = [u for u in LOG["failed_requests"] if "boss_" not in u]
    LOG["summary"] = {"pass": n_pass, "total": len(EXPECTED),
                      "pageerrors": len(LOG["errors"]),
                      "failed_requests": len(LOG["failed_requests"]),
                      "boss_failed_requests": boss_failed,
                      "other_failed_requests": other_failed}
    with open(os.path.join(HERE, "drive116.json"), "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=2)
    print(f"SUMMARY {n_pass}/{len(EXPECTED)} locs PASS; pageerrors={len(LOG['errors'])} failed_req={len(LOG['failed_requests'])} (boss: {len(boss_failed)}, other: {len(other_failed)})")
    if LOG["errors"]:
        print("PAGEERRORS:", LOG["errors"][:5])
    if boss_failed:
        print("BOSS_FAILED_REQ:", boss_failed[:5])
    if other_failed:
        # 已知舊問題（唔關 v116 事）：鍾楚凝 think/smile 表情缺檔，巧遇段出 404
        print("OTHER_FAILED_REQ (known pre-existing, non-boss):", other_failed[:5])
    ok = (n_pass == len(EXPECTED) and not LOG["errors"] and not boss_failed)
    print("DRIVE116 " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
