# -*- coding: utf-8 -*-
"""v20a181 實駕 drive181：頒獎禮橫向舞台（won／nominated／gallery）× 932／700。
用法：/home/hatch/pwenv49/bin/python qa181/drive181.py
Mirror：工作副本 ~/workspace/linji-work181，port 8972，?softPreview=1。
播種：localStorage key starVolunteer_map_v19w slot 1（經 new_game 正常開局）。
觸發（真實 UI 路徑，唔直叫 IIFE 內函數）：seed S.pendingAwardPack（hand-built pack）＋
  S.awardsFlags["1990/award_harbour_ad"]="invited" → 開地點 sheet → 「返回地圖」→
  goToMapForBrowse → queueAwardsOnSeasonWindow → restorePendingAward136 還原請柬 →
  presentPendingAward → 請柬 modal → 出席（won／nominated）／推辭（gallery declined165）→
  awards62PlayCeremony → 播完入結果卡（收下這晚）／推辭 toast。
量度：每 beat 中段截 .awd62-frame＋DOM 證據（frame／canvas 尺寸、橫額／數字條／白牌／黃字、
  字幕、卡數、glamour on、跳過掣）＋每 beat 幾何（board／sub 行框／人頭頂／glyph 頂：黃字 fix 驗收，
  sub 行框要喺 board 入面、sub 底要高過人頭頂、board 底要唔過 glyph 頂）＋pageerror／console error／失敗請求（尤其 px_*.png 404）。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work181"
HERE = os.path.join(ROOT, "qa181")
SHOTS = os.path.join(HERE, "shots181")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8972
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
REPORT = {"errors": [], "http_fail": [], "runs": {}}


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


def new_game(pg):
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
    print("NEW GAME OK:", ok, pg.evaluate("() => window.S ? (S.dayIndex + ' ' + S.dateStr) : 'no S'"), flush=True)
    return ok


def dismiss_encounter(pg, max_clicks=16):
    for _ in range(max_clicks):
        if pg.evaluate("() => !document.getElementById('enc79-overlay')"):
            return True
        clicked = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay'); if (!ov) return false;
          const sk = ov.querySelector('.e79-skip'); if (sk && sk.offsetParent !== null) { sk.click(); return true; }
          const ch = ov.querySelector('.e79-choice'); if (ch) { ch.click(); return true; }
          const nb = [...ov.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return true; } return false; }""")
        if not clicked:
            return pg.evaluate("() => !document.getElementById('enc79-overlay')")
        pg.wait_for_timeout(700)
    return pg.evaluate("() => !document.getElementById('enc79-overlay')")


SEED_JS = """(outcome) => {
  const fellows = [
    { starId: "luk_baakyin", star: "陸柏言", title: "城寨暗夜1988" },
    { starId: "liu_bingxing", star: "廖炳星", title: "夜更和音" },
    { starId: "mak_zhendong", star: "麥震東", title: "廟街龍虎鬥" }
  ];
  const focusOutcome = outcome === "gallery" ? "gallery" : outcome;
  const cat = { id: "best_actor", label: "最佳男主角", outcome: focusOutcome, score: outcome === "won" ? 0.92 : 0.71,
    repWorkTitle: "夜更和音", weakHint62: "", line: "台上念到你。",
    fellows63: fellows, winner63: outcome === "nominated" ? fellows[0] : null };
  const cat2 = { id: "best_song", label: "最佳歌曲", outcome: "gallery", score: 0.4,
    repWorkTitle: "", weakHint62: "", line: "你坐喺席上，記住呢晚嘅掌聲。",
    fellows63: fellows, winner63: null };
  const pack = { displayName: "廣告年賞", ceremonyId: "award_harbour_ad", year: 1990, medium: "ad",
    venue99: "九龍電視城", tierLabel: outcome === "gallery" ? "旁聽" : "入圍",
    repWork62: "夜更和音", repGigId63: outcome === "won" ? "gig_1988_ad_central_spring_high" : null,
    bestOutcome: outcome, categories: [cat, cat2],
    rewards: { stageVolume: 5, industryCredit: 3 },
    press: { paperName: "娛樂快報", headline: "廣告年賞散場", dek: "頒獎夜，版面多一行。" },
    news: { outlet: "晚間娛樂快訊", line: "廣告年賞散場：臨記席都有鏡頭掃過。" },
    metricEcho: "attention" };
  S.fame = 42;
  S.awardsFlags = S.awardsFlags || {};
  S.awardsFlags["1990/award_harbour_ad"] = "invited";
  S.pendingAwardPack = pack;
  return true;
}"""

EVIDENCE_JS = """() => {
  const q = (s) => document.querySelector(s);
  const txt = (s) => { const e = q(s); return e ? (e.textContent || '').trim() : null; };
  const fr = q('.awd62-frame'), cv = q('.awd62-canvas');
  const r = fr ? fr.getBoundingClientRect() : null;
  const cr = cv ? cv.getBoundingClientRect() : null;
  const geom = (() => {
    const rr = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
      return { top: Math.round(b.top), bottom: Math.round(b.bottom), left: Math.round(b.left), right: Math.round(b.right) }; };
    const cv2 = q('.awd62-canvas'), bd = q('.awd181-board'), sb = q('.awd181-sub');
    if (!cv2 || !bd || !sb) return null;
    const c = cv2.getBoundingClientRect(), sY = c.height / 360, sX = c.width / 480;
    const lines = [...sb.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => {
      const rg = document.createRange(); rg.selectNodeContents(n); const b = rg.getBoundingClientRect();
      return { top: Math.round(b.top), bottom: Math.round(b.bottom), left: Math.round(b.left), right: Math.round(b.right) }; });
    const b = bd.getBoundingClientRect();
    const headTopY = Math.round(c.top + 173 * sY), glyphTopY = Math.round(c.top + 150 * sY);
    return { canvas: rr(cv2), board: rr(bd), sub: rr(sb), subLines: lines,
      headTopY, glyphTopY, floorY: Math.round(c.top + 262 * sY),
      slots: [60, 180, 300, 420].map(x => Math.round(c.left + x * sX)),
      subInsideBoard: lines.length > 0 && lines.every(l => l.top >= Math.round(b.top) && l.bottom <= Math.round(b.bottom) && l.left >= Math.round(b.left) && l.right <= Math.round(b.right)),
      subAboveHeads: lines.length > 0 && lines.every(l => l.bottom < headTopY),
      boardAboveGlyph: Math.round(b.bottom) <= glyphTopY };
  })();
  return {
    stage: !!q('.awd62-stage'),
    frame: r ? { w: Math.round(r.width), h: Math.round(r.height) } : null,
    canvasAttr: cv ? [cv.width, cv.height] : null,
    canvasBox: cr ? { w: Math.round(cr.width), h: Math.round(cr.height) } : null,
    banner: txt('.awd181-banner'), stripL: txt('.awd181-strip.l'), stripR: txt('.awd181-strip.r'),
    board: txt('.awd181-board'), sub: txt('.awd181-sub'),
    caption: txt('.awd62-caption'),
    cards: document.querySelectorAll('.awd63-card').length,
    glamourOn: !!q('.awd63-glamour.on'),
    skip: !!q('.awd62-skip'),
    geom
  };
}"""

SAMPLES = {
    "won": [(600, "open"), (2000, "enter"), (4000, "names"), (6000, "suspense"),
            (7800, "reveal"), (10000, "walkup"), (12000, "glamour")],
    "nominated": [(600, "open"), (2000, "enter"), (4000, "names"), (6000, "suspense"),
                  (7800, "reveal"), (10000, "comfort")],
    "gallery": [(600, "open"), (2000, "pan"), (4000, "names"), (6300, "suspense"), (8000, "reveal")],
}
TOTAL_MS = {"won": 14000, "nominated": 12500, "gallery": 10200}
ATTEND = {"won": "出席", "nominated": "出席", "gallery": "推辭"}


def js_click_text(pg, text):
    """JS .click() 撳可見掣（Playwright 真撳會俾上層 stage／熱區遮住 hit-target 失敗）。"""
    return pg.evaluate("""(t) => {
      const b = [...document.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def js_click_contains(pg, text, scope=None):
    return pg.evaluate("""(args) => {
      const root = args.scope ? document.querySelector(args.scope) : document;
      if (!root) return false;
      const b = [...root.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').includes(args.t));
      if (!b) return false; b.click(); return true; }""", {"t": text, "scope": scope})


def play_through_story(pg, max_steps=80):
    """播晒當前主線劇情（C1 會喺第一次入地點嗰陣自動彈）：逐句撳 #modal-btns 首掣，抉擇撳第一項。"""
    for _ in range(max_steps):
        st = pg.evaluate("""() => {
          const plate = document.querySelector('.story-play .dlg106-plate');
          const choice = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
          return {active: !!plate || choice.length > 0, choices: choice.length}; }""")
        if not st["active"]:
            return True
        if st["choices"]:
            pg.evaluate("""() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
              if (c[0]) c[0].click(); }""")
            pg.wait_for_timeout(1200)
            continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            return False
        pg.wait_for_timeout(900)
    return pg.evaluate("""() => !document.querySelector('.story-play .dlg106-plate')
      && ![...document.querySelectorAll('.sp-choice')].some(e => e.offsetParent !== null)""")


def modal_click(pg, text):
    """撳 #modal-btns 入面嗰粒掣（唔會撳錯 #loc-close／home tab 同名掣）。"""
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def has_invite(pg):
    return pg.evaluate("() => [...document.querySelectorAll('button')].some(b => b.offsetParent !== null && (b.textContent || '').trim() === '出席')")


def advance_morning(pg, timeout_s=60):
    """行 morning chain 直到請柬彈出：過一日 → 確定過一日 → 開始今日行程 → 返回地圖（modal）→ 請柬。
    沿途 modal 按優先次序撳：收下這份剪報 ＞ 返回地圖（直接行 goToMapForBrowse）＞
    開始今日行程 ＞ 確定過一日 ＞ 關閉 ＞ 知道了。"""
    print("  advance_morning: click 過一日 ->", js_click_text(pg, "過一日"), flush=True)
    for _ in range(int(timeout_s * 2)):
        pg.wait_for_timeout(500)
        if has_invite(pg):
            print("  advance_morning: invite found", flush=True)
            return True
        if pg.evaluate("() => !!document.getElementById('enc79-overlay')"):
            dismiss_encounter(pg)
            continue
        if modal_click(pg, "收下這晚"):
            print("  advance_morning: click 收下這晚", flush=True)
            continue
        if modal_click(pg, "收下這份剪報"):
            print("  advance_morning: click 收下這份剪報", flush=True)
            continue
        if modal_click(pg, "返回地圖"):
            print("  advance_morning: click 返回地圖(modal)", flush=True)
            continue
        if modal_click(pg, "開始今日行程"):
            print("  advance_morning: click 開始今日行程", flush=True)
            continue
        if modal_click(pg, "確定過一日"):
            print("  advance_morning: click 確定過一日", flush=True)
            continue
        if modal_click(pg, "關閉"):
            print("  advance_morning: click 關閉", flush=True)
            continue
        if modal_click(pg, "知道了"):
            print("  advance_morning: click 知道了", flush=True)
            continue
        # 地圖掣（唔係 modal 掣）：今日仲有行程未跑，撳佢跑埋先返地圖見請柬
        if js_click_text(pg, "開始今日行程"):
            print("  advance_morning: click 開始今日行程（地圖掣）", flush=True)
            continue
    print("  advance_morning: TIMEOUT, state:", pg.evaluate("""() => ({
      day: S.dayIndex,
      modalBtns: [...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim()),
      modalText: (()=>{const m=document.querySelector('#modal, .modal'); return m ? (m.textContent||'').slice(0,80) : null;})() })"""), flush=True)
    return has_invite(pg)


def trigger_invite(pg, outcome, first=False):
    """seed pack →（首次：開茶餐廳 sheet 觸發 C1，播完＋閂總結）→ morning chain → 等請柬 modal。"""
    pg.evaluate(SEED_JS, outcome)
    dismiss_encounter(pg)
    if first:
        # 返地圖（新局完係 v-home 週計劃頁；「返回地圖」掣俾 stage 遮住，要 JS click）
        js_click_text(pg, "返回地圖")
        pg.wait_for_timeout(1200)
        # 開地點 sheet：撳地圖熱區「茶餐廳」（中性地點；事務所會自動播 C1）
        opened = js_click_contains(pg, "茶餐廳", "#v-map")
        pg.wait_for_timeout(1500)
        if not opened:
            print("  !! 開唔到茶餐廳 sheet", flush=True)
            return False
        dismiss_encounter(pg)
        # 閂 sheet：限死 #loc-sheet 範圍撳「返回地圖」（頁面有另一粒同名 home tab 掣，唔可以撳錯）
        hit = pg.evaluate("""() => {
          const sh = document.getElementById('loc-sheet'); if (!sh) return false;
          const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === '返回地圖');
          if (!b) return false; b.click(); return true; }""")
        pg.wait_for_timeout(1200)
        if not hit:
            print("  !! sheet 冇「返回地圖」掣", flush=True)
            return False
        # C1 會喺第一次入地點嗰陣自動彈出——播完佢＋閂總結 modal
        play_through_story(pg)
        pg.wait_for_timeout(800)
        modal_click(pg, "關閉")
        pg.wait_for_timeout(800)
    return advance_morning(pg)


def run_ceremony(pg, vp, outcome, first=False):
    key = f"{vp}_{outcome}"
    print(f"== {key} ==", flush=True)
    if not trigger_invite(pg, outcome, first=first):
        print("  !! 等唔到請柬 modal", flush=True)
        REPORT["runs"][key] = {"invite": False}
        return False
    hit = modal_click(pg, ATTEND[outcome])
    pg.wait_for_timeout(1500)
    if not hit:
        print(f"  !! 撳唔到{ATTEND[outcome]}", flush=True)
        REPORT["runs"][key] = {"invite": True, "attend": False}
        return False
    # 等舞台出現（出席 handler 有 modal 收合，唔好 300ms 就判死）
    stage_ok = False
    for _ in range(10):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => !!document.querySelector('.awd62-stage')"):
            stage_ok = True
            break
    if not stage_ok:
        print("  !! 撳完冇舞台", flush=True)
        REPORT["runs"][key] = {"invite": True, "attend": True, "stage": False}
        return False
    samples = []
    last = 0
    t0 = time.time()
    for at_ms, beat in SAMPLES[outcome]:
        pg.wait_for_timeout(at_ms - last)
        last = at_ms
        ev = pg.evaluate(EVIDENCE_JS)
        samples.append({"t": at_ms, "real_ms": round((time.time() - t0) * 1000), "beat": beat, "ev": ev})
        try:
            pg.locator(".awd62-frame").screenshot(path=os.path.join(SHOTS, f"{key}_{beat}.png"), timeout=5000)
        except Exception as e:
            print(f"  shot {beat} failed: {str(e)[:80]}", flush=True)
        print(f"  [{beat} t={at_ms}] frame={ev['frame']} canvas={ev['canvasAttr']}/{ev['canvasBox']} "
              f"banner={ev['banner']!r} L={ev['stripL']!r} R={ev['stripR']!r} board={ev['board']!r} "
              f"cards={ev['cards']} glam={ev['glamourOn']} cap={(ev['caption'] or '')[:40]!r} "
              f"geomIn={(ev['geom'] or {}).get('subInsideBoard')} aboveHead={(ev['geom'] or {}).get('subAboveHeads')} "
              f"aboveGlyph={(ev['geom'] or {}).get('boardAboveGlyph')} lines={(ev['geom'] or {}).get('subLines')}", flush=True)
    # 等舞台拆走（播完）
    stage_gone = False
    for _ in range(20):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => !document.querySelector('.awd62-stage')"):
            stage_gone = True
            break
    print(f"  stage_gone={stage_gone}", flush=True)
    # 善後：結果卡「收下這晚」／推辭 toast 後返地圖
    pg.wait_for_timeout(800)
    modal_click(pg, "收下這晚")
    pg.wait_for_timeout(1200)
    dismiss_encounter(pg)
    REPORT["runs"][key] = {"invite": True, "attend": True, "stage": True,
                           "samples": samples, "stage_gone": stage_gone}
    return stage_gone


def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            for vp in (932, 700):
                pg = br.new_page(viewport={"width": vp, "height": 844})
                pg.on("pageerror", lambda e: REPORT["errors"].append(f"{vp}: {e}"))
                pg.on("console", lambda m: REPORT["errors"].append(f"{vp} console.{m.type}: {m.text}") if m.type == "error" else None)
                pg.on("response", lambda r: REPORT["http_fail"].append(f"{vp} {r.status} {r.url}") if r.status >= 400 else None)
                pg.on("requestfailed", lambda r: REPORT["http_fail"].append(f"{vp} REQFAIL {r.url}"))
                assert new_game(pg), "new game failed"
                dismiss_encounter(pg)
                for i, outcome in enumerate(("won", "nominated", "gallery")):
                    ok = run_ceremony(pg, vp, outcome, first=(i == 0))
                    if not ok:
                        print(f"  !! {vp}_{outcome} 未正常完場", flush=True)
                    pg.wait_for_timeout(600)
                pg.close()
            br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive181_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)
    print("pageerrors:", len(REPORT["errors"]), REPORT["errors"][:5])
    print("http_fail:", len(REPORT["http_fail"]), REPORT["http_fail"][:5])
    print("runs:", {k: v.get("stage_gone") for k, v in REPORT["runs"].items()})


if __name__ == "__main__":
    main()
