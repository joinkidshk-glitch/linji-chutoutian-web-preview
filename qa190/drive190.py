# -*- coding: utf-8 -*-
"""v20a190 實駕 drive190：修 v187 review 新 C1（glamour panel 縮短貼底）（won／nominated／gallery）× 932／700。
用法：/home/hatch/pwenv49/bin/python qa190/drive190.py
新增量度：B1 用 canvas toDataURL＋PIL 量地板帶／人頭頂（唔靠截圖，避 headless stale frame）；
  C1 glamour 海報 img vs 白牌 DOM 重疊；C2 卡罅＋角標 clearance；C3 out polling 捉 500ms 窗口內 canvas 人物對比；
  C4 walkup_mid 像素量度（阿偉腳 268 vs 提名人腳 262）；C5 frame 頂 reveal vs glamour 下移量；C6 glyph 頂 152。
Mirror：工作副本 ~/workspace/linji-work187，port 8974，?softPreview=1。
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

ROOT = "/home/hatch/workspace/linji-work190"
HERE = os.path.join(ROOT, "qa190")
SHOTS = os.path.join(HERE, "shots190")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8977
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
    const headTopY = Math.round(c.top + 173 * sY), glyphTopY = Math.round(c.top + 152 * sY); /* v20a187 C6：glyph 頂 150→152 */
    const glam = (() => {
      const im = q('.awd63-glamour-panel>img'), pn = q('.awd63-glamour-panel'), gl = q('.awd63-glamour.on');
      if (!im || !gl) return null;
      const ir = rr(im), pr = rr(pn);
      const ox = Math.max(0, Math.min(ir.right, b.right) - Math.max(ir.left, b.left));
      const oy = Math.max(0, Math.min(ir.bottom, b.bottom) - Math.max(ir.top, b.top));
      const ov = q('.awd63-glamour'), ovr = ov ? rr(ov) : null;
      const cs = pn ? getComputedStyle(pn) : null, ics = im ? getComputedStyle(im) : null;
      const emptyTop = ir.top - pr.top, panelH = pr.bottom - pr.top;
      return { img: ir, panel: pr, overlay: ovr, overlapX: ox, overlapY: oy, overlap: ox > 0 && oy > 0,
        imgTopAboveBoardBottom: ir.top >= Math.round(b.bottom),
        clearancePx: ir.top - Math.round(b.bottom),
        emptyTop, panelH, emptyRatio: panelH ? +(emptyTop / panelH).toFixed(3) : null,
        bottomGap: pr.bottom - ir.bottom,
        imgNatural: [im.naturalWidth, im.naturalHeight], imgW: ir.right - ir.left,
        panelW: pr.right - pr.left, imgMaxH: ics ? ics.maxHeight : null,
        overlayAlign: ov ? getComputedStyle(ov).alignItems : null };
    })();
    const cardsGeom = (() => {
      const els = [...document.querySelectorAll('.awd63-card')];
      if (!els.length) return null;
      const rs = els.map(rr);
      const gaps = rs.slice(1).map((r2, i) => Math.round(r2.left - rs[i].right));
      return { rects: rs, gaps, minGap: gaps.length ? Math.min(...gaps) : null,
        badgeClearance: gaps.length ? Math.min(...gaps) - 14 : null, /* 你徽右出 7＋🏆 左出 7 */
        rowWidth: Math.round(rs[rs.length - 1].right - rs[0].left) };
    })();
    return { canvas: rr(cv2), board: rr(bd), sub: rr(sb), subLines: lines,
      headTopY, glyphTopY, floorY: Math.round(c.top + 262 * sY),
      glyphGapPx: glyphTopY - Math.round(b.bottom),
      slots: [60, 180, 300, 420].map(x => Math.round(c.left + x * sX)),
      subInsideBoard: lines.length > 0 && lines.every(l => l.top >= Math.round(b.top) && l.bottom <= Math.round(b.bottom) && l.left >= Math.round(b.left) && l.right <= Math.round(b.right)),
      subAboveHeads: lines.length > 0 && lines.every(l => l.bottom < headTopY),
      boardAboveGlyph: Math.round(b.bottom) <= glyphTopY,
      glamour: glam, cardsGeom };
  })();
  return {
    stage: !!q('.awd62-stage'),
    frame: r ? { w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top) } : null,
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

CANVAS_JS = """() => { const cv = document.querySelector('.awd62-canvas'); if (!cv) return null; return cv.toDataURL('image/png'); }"""

OUT_STATE_JS = """(wantGlamOff) => {
  const st = !!document.querySelector('.awd62-stage');
  if (!st) return { stage: false };
  const cap = document.querySelector('.awd62-caption');
  const capHidden = !cap || cap.style.display === 'none' || (cap.textContent || '').trim() === '';
  const capText = cap ? (cap.textContent || '').trim() : '';
  const glam = !!document.querySelector('.awd63-glamour.on');
  // v20a187：gallery out 有收尾字幕「掌聲響起——今晚完滿落幕。」（caption 唔隱藏），
  //   won／nominated out caption 係 ""（隱藏）——兩種都係 out，唔好淨係用 capHidden 判
  const isOut = capHidden || capText.indexOf('今晚完滿落幕') >= 0;
  return { stage: true, capHidden, capText, glamourOn: glam, out: isOut && (!wantGlamOff || !glam) };
}"""

# --- v20a187：canvas 像素量度（toDataURL 即時 bitmap，唔靠截圖，避 headless stale frame） ---
import base64, io, statistics
from PIL import Image

def canvas_image(pg):
    url = pg.evaluate(CANVAS_JS)
    if not url:
        return None
    return Image.open(io.BytesIO(base64.b64decode(url.split(',', 1)[1]))).convert('RGB')

def _lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def analyze_b1(im, slots=(60, 180, 300, 420)):
    """B1：names beat canvas（720×540 backing，邏輯 ×1.5）——地板帶（木色行）＋人頭頂（幕布色對比）。
    slots 按 outcome 傳入（won／nominated 4 slots，gallery 3 slots 75／240／405）。"""
    W, H = im.size
    def px(bx, by):
        return im.getpixel((max(0, min(W - 1, bx)), max(0, min(H - 1, by))))
    def is_wood(c):
        # 藍容差 20：地板頂 12px 高光（rgba 白 0.10）令 b 升到 111，<16 會漏咗成段頂（run 2 讀到 242 嘅原因）；
        # 橫紋（b=71，差 24）同豎縫（b≈80，差 15——但掃描欄 x=10／120／460 唔係縫位）唔受影響
        return abs(c[0] - 0xd9) < 16 and abs(c[1] - 0xa7) < 16 and abs(c[2] - 0x5f) < 20
    def is_wood_dim(c):  # 後備：萬一撞正 suspense 暗場（overlay 0.52），木色暗一半都認到
        return abs(c[0] - 109) < 22 and abs(c[1] - 83) < 22 and abs(c[2] - 55) < 22
    tops, bots = [], []
    for lx in (10, 120, 460):  # 避開人物／豎縫／側幕
        col = int(lx * 1.5)
        rows = [y for y in range(H) if is_wood(px(col, y))]
        if len(rows) < 10:
            rows = [y for y in range(H) if is_wood_dim(px(col, y))]
        if rows:
            tops.append(min(rows) / 1.5)
            bots.append((max(rows) + 1) / 1.5)
    floor_top = min(tops); floor_bot = max(bots)
    def differs_curtain(c):
        return abs(c[0] - 0xf2) > 28 or abs(c[1] - 0xe8) > 28 or abs(c[2] - 0xd5) > 28
    heads = {}
    for slot in slots:
        cx = int(slot * 1.5); head = None
        for ly in range(150, 258):
            by = int(ly * 1.5)
            cnt = sum(1 for bx in range(cx - 22, cx + 23) if differs_curtain(px(bx, by)))
            cnt2 = sum(1 for bx in range(cx - 22, cx + 23) if differs_curtain(px(bx, by + 1)))
            if cnt >= 5 and cnt2 >= 3:
                head = ly; break
        heads[slot] = head
    hs = [262 - h for h in heads.values() if h is not None]
    person_h = sum(hs) / len(hs) if hs else None
    return {"floor_top": round(floor_top, 1), "floor_bot": round(floor_bot, 1),
            "floor_depth": round(floor_bot - floor_top, 1), "heads": heads,
            "person_h": round(person_h, 1) if person_h else None,
            "floor_over_person": round((floor_bot - floor_top) / person_h, 2) if person_h else None,
            "below_feet_over_person": round((floor_bot - 262) / person_h, 2) if person_h else None}

def analyze_out_contrast(im):
    """C3：out 期間人物對比——y 180–250 邏輯帶，每行 x 40–440 亮度 max-min 中位數。
    有人物（就算暗落緊）對比大；空台＋均勻 overlay 對比細。"""
    vals = []
    for ly in range(180, 251, 3):
        by = int(ly * 1.5)
        lums = [_lum(im.getpixel((int(lx * 1.5), by))) for lx in range(40, 441, 4)]
        vals.append(max(lums) - min(lums))
    return round(statistics.median(vals), 1)

def analyze_walkup_mid(im):
    """C4：walkup 中段——rows 264–270 邏輯（提名人腳底 262 之下），搵最暗 30px 區 vs 提名人 300 對照區。
    阿偉腳 268＋接觸影應該明顯暗過淨地板；對照區得地板＋橫紋。"""
    def zone_mean(x0, x1):
        vals = []
        for ly in range(264, 271):
            for lx in range(x0, x1 + 1, 2):
                vals.append(_lum(im.getpixel((int(lx * 1.5), int(ly * 1.5)))))
        return sum(vals) / len(vals)
    best = None
    for x0 in range(0, 211, 10):
        mm = zone_mean(x0, x0 + 30)
        if best is None or mm < best[1]:
            best = (x0, mm)
    ctrl = zone_mean(285, 315)
    return {"darkest_x0": best[0], "darkest_mean": round(best[1], 1),
            "control_mean": round(ctrl, 1), "delta": round(ctrl - best[1], 1)}

SAMPLES = {
    "won": [(600, "open"), (2000, "enter"), (4000, "names"), (6000, "suspense"),
            (7800, "reveal"), (9400, "walkup_mid"), (12000, "glamour")],
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
    if not hit:
        print(f"  !! 撳唔到{ATTEND[outcome]}", flush=True)
        REPORT["runs"][key] = {"invite": True, "attend": False}
        return False
    # 等舞台出現：唔死等 1500ms（嗰段時間 ceremony 已經行緊，t0 會滯後 ~1.5s，成個取樣時鐘漂移——
    #   v181 review §5 同一個問題）；改 100ms poll 即刻錨定 t0。
    stage_ok = False
    for _ in range(50):
        pg.wait_for_timeout(100)
        if pg.evaluate("() => !!document.querySelector('.awd62-stage')"):
            stage_ok = True
            break
    if not stage_ok:
        print("  !! 撳完冇舞台", flush=True)
        REPORT["runs"][key] = {"invite": True, "attend": True, "stage": False}
        return False
    samples = []
    probes = {}
    t0 = time.time()
    for at_ms, beat in SAMPLES[outcome]:
        # v20a187：絕對時鐘取樣（唔用累進 wait——截圖／探針耗時唔可以累積落下一個樣本）
        delay = at_ms - (time.time() - t0) * 1000
        if delay > 0:
            pg.wait_for_timeout(delay)
        if beat == "walkup_mid":
            # caption 錨定：等 walkup 字幕出現即探（行到中段 wp≈0.45，阿偉 x≈60 啱啱掠過左邊提名人；
            #   run 2 等多 600ms 嗰陣已經 wp 0.83、行到 x≈140，掠過嗰刻影唔到）
            for _ in range(40):
                cap = pg.evaluate("() => (document.querySelector('.awd62-caption') || {}).textContent || ''")
                if "阿偉行上台" in cap:
                    break
                pg.wait_for_timeout(100)
            pg.wait_for_timeout(100)
        ev = pg.evaluate(EVIDENCE_JS)
        rec = {"t": at_ms, "real_ms": round((time.time() - t0) * 1000), "beat": beat, "ev": ev}
        samples.append(rec)
        # v20a187 canvas 探針（toDataURL 即時 bitmap）——先探針，截圖放後面（截圖慢，唔可以拖慢探針）
        try:
            if beat == "names":
                # caption 錨定：等「入圍名單」字幕先探（唔係嘅話可能已經跌入 suspense 暗場，木色對唔上）
                for _ in range(8):
                    cap = pg.evaluate("() => (document.querySelector('.awd62-caption') || {}).textContent || ''")
                    if "入圍名單" in cap:
                        break
                    pg.wait_for_timeout(100)
                im = canvas_image(pg)
                if im:
                    probes["b1"] = analyze_b1(im, [75, 240, 405] if outcome == "gallery" else [60, 180, 300, 420])
                    probes["names_contrast"] = analyze_out_contrast(im)
            elif beat == "open":
                im = canvas_image(pg)
                if im:
                    probes["open_contrast"] = analyze_out_contrast(im)
            elif beat == "walkup_mid":
                im = canvas_image(pg)
                if im:
                    probes["c4"] = analyze_walkup_mid(im)
        except Exception as e:
            print(f"  probe {beat} failed: {str(e)[:100]}", flush=True)
        if beat in ("names", "reveal", "walkup_mid", "glamour", "comfort") and not (outcome == "gallery" and beat == "reveal"):
            # gallery reveal 唔截圖：reveal 截圖慢（~1s+），會拖過 out 500ms 窗口（run 2 gallery out 捉唔到就係咁）；
            # gallery reveal 截圖 run 2 已經有，out poll 優先
            try:
                pg.locator(".awd62-frame").screenshot(path=os.path.join(SHOTS, f"{key}_{beat}.png"), timeout=3000)
            except Exception as e:
                print(f"  shot {beat} failed: {str(e)[:80]}", flush=True)
        print(f"  [{beat} t={at_ms}] frame={ev['frame']} canvas={ev['canvasAttr']}/{ev['canvasBox']} "
              f"banner={ev['banner']!r} L={ev['stripL']!r} R={ev['stripR']!r} board={ev['board']!r} "
              f"cards={ev['cards']} glam={ev['glamourOn']} cap={(ev['caption'] or '')[:40]!r} "
              f"geomIn={(ev['geom'] or {}).get('subInsideBoard')} aboveHead={(ev['geom'] or {}).get('subAboveHeads')} "
              f"aboveGlyph={(ev['geom'] or {}).get('boardAboveGlyph')} lines={(ev['geom'] or {}).get('subLines')} "
              f"glamOverlap={(ev['geom'] or {}).get('glamour')} cardGap={(ev['geom'] or {}).get('cardsGeom')} "
              f"glyphGap={(ev['geom'] or {}).get('glyphGapPx')} probe={probes.get('b1') or probes.get('c4') or ''}", flush=True)
    # v20a187 C3：out polling——捉 500ms 窗口（caption 隱藏＋won 要 glamour 已閂），即刻捉 canvas 對比
    out_probe = None
    for _ in range(60):
        st = pg.evaluate(OUT_STATE_JS, outcome == "won")
        if st.get("out"):
            try:
                im = canvas_image(pg)
                if im:
                    out_probe = {"contrast": analyze_out_contrast(im),
                                 "glamourOn": st.get("glamourOn"), "capHidden": st.get("capHidden")}
            except Exception as e:
                print(f"  out probe failed: {str(e)[:100]}", flush=True)
            try:
                pg.locator(".awd62-frame").screenshot(path=os.path.join(SHOTS, f"{key}_out.png"), timeout=5000)
            except Exception:
                pass
            print(f"  [out probe] {out_probe}", flush=True)
            break
        if not st.get("stage"):
            break
        pg.wait_for_timeout(80)
    probes["out"] = out_probe
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
                           "samples": samples, "probes": probes, "stage_gone": stage_gone}
    return stage_gone


def main():
    # ONLY 環境變數：只跑指定場（例如 ONLY=932_gallery 或 ONLY=gallery），報告寫 drive187_report_<only>.json，
    #   唔會覆蓋全套 drive190_report.json；用嚟針對重跑單一 outcome（gallery out 探針）
    only = os.environ.get("ONLY", "")
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            vps = (932, 700) if not only or not any(str(v) in only for v in (932, 700)) else tuple(v for v in (932, 700) if str(v) in only)
            for vp in vps:
                pg = br.new_page(viewport={"width": vp, "height": 844})
                pg.on("pageerror", lambda e: REPORT["errors"].append(f"{vp}: {e}"))
                pg.on("console", lambda m: REPORT["errors"].append(f"{vp} console.{m.type}: {m.text}") if m.type == "error" else None)
                pg.on("response", lambda r: REPORT["http_fail"].append(f"{vp} {r.status} {r.url}") if r.status >= 400 else None)
                pg.on("requestfailed", lambda r: REPORT["http_fail"].append(f"{vp} REQFAIL {r.url}"))
                assert new_game(pg), "new game failed"
                dismiss_encounter(pg)
                outcomes = [o for o in ("won", "nominated", "gallery") if not only or o in only or (f"{vp}_{o}") == only]
                for i, outcome in enumerate(outcomes):
                    ok = run_ceremony(pg, vp, outcome, first=(i == 0))
                    if not ok:
                        print(f"  !! {vp}_{outcome} 未正常完場", flush=True)
                    pg.wait_for_timeout(600)
                pg.close()
            br.close()
    finally:
        stop(srv)
    report_name = "drive190_report.json" if not only else "drive190_report_" + only.replace("/", "_") + ".json"
    with open(os.path.join(HERE, report_name), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)
    print("pageerrors:", len(REPORT["errors"]), REPORT["errors"][:5])
    print("http_fail:", len(REPORT["http_fail"]), REPORT["http_fail"][:5])
    print("runs:", {k: v.get("stage_gone") for k, v in REPORT["runs"].items()})
    # --- v20a187 驗收總表 ---
    print("== v190 acceptance ==")
    n_geom = n_in = n_head = n_glyph = 0
    for key, run in REPORT["runs"].items():
        for s in run.get("samples", []):
            g = (s.get("ev") or {}).get("geom") or {}
            if g:
                n_geom += 1
                n_in += 1 if g.get("subInsideBoard") else 0
                n_head += 1 if g.get("subAboveHeads") else 0
                n_glyph += 1 if g.get("boardAboveGlyph") else 0
    print(f"yellow-text 30/30 check: geom samples={n_geom} subInside={n_in} subAboveHeads={n_head} boardAboveGlyph={n_glyph}")
    for key, run in REPORT["runs"].items():
        pr = run.get("probes") or {}
        b1 = pr.get("b1")
        if b1:
            print(f"B1 {key}: floor {b1['floor_top']}–{b1['floor_bot']} depth={b1['floor_depth']} "
                  f"person_h={b1['person_h']} floor/person={b1['floor_over_person']} "
                  f"below/person={b1['below_feet_over_person']} heads={b1['heads']} "
                  f"names_contrast={pr.get('names_contrast')} open_contrast={pr.get('open_contrast')}")
        c4 = pr.get("c4")
        if c4:
            print(f"C4 {key}: darkest_x0={c4['darkest_x0']} delta={c4['delta']} "
                  f"(darkest {c4['darkest_mean']} vs control {c4['control_mean']})")
        out = pr.get("out")
        nc = pr.get("names_contrast")
        print(f"C3 {key}: out_probe={out} (names_contrast={nc} 對照：有人物應 >> 空台)")
        # C5：glamour frame 頂 − 之前最後一個非 glamour 樣本 frame 頂（v174 trade-off，預期 ~124px）
        tops = [(s["beat"], (s["ev"].get("frame") or {}).get("top")) for s in run.get("samples", [])]
        glam_tops = [t for b, t in tops if b == "glamour" and t is not None]
        pre_tops = [t for b, t in tops if b in ("reveal", "walkup_mid") and t is not None]
        if glam_tops and pre_tops:
            print(f"C5 {key}: glamour frameTop={glam_tops[0]} vs pre={pre_tops[-1]} shift={glam_tops[0] - pre_tops[-1]}px")
        for s in run.get("samples", []):
            g = (s.get("ev") or {}).get("geom") or {}
            if s["beat"] == "glamour" and g.get("glamour") is not None:
                gl = g['glamour']
                print(f"C1 {key}: glamour overlap={gl['overlap']} "
                      f"overlapX={gl['overlapX']} overlapY={gl['overlapY']} "
                      f"imgTopAboveBoardBottom={gl['imgTopAboveBoardBottom']} img={gl['img']}")
                print(f"v190 {key}: panel={gl['panel']} emptyTop={gl.get('emptyTop')} panelH={gl.get('panelH')} "
                      f"emptyRatio={gl.get('emptyRatio')} clearance={gl.get('clearancePx')} bottomGap={gl.get('bottomGap')} "
                      f"imgNatural={gl.get('imgNatural')} imgW={gl.get('imgW')} panelW={gl.get('panelW')} "
                      f"imgMaxH={gl.get('imgMaxH')} overlayAlign={gl.get('overlayAlign')} overlay={gl.get('overlay')}")
            if s["beat"] == "reveal" and g.get("cardsGeom"):
                print(f"C2 {key}: cardGaps={g['cardsGeom']['gaps']} minGap={g['cardsGeom']['minGap']} "
                      f"badgeClearance={g['cardsGeom']['badgeClearance']} rowWidth={g['cardsGeom']['rowWidth']}")
            if s["beat"] in ("reveal", "glamour"):
                print(f"C5/C6 {key} [{s['beat']}]: frameTop={(s['ev'].get('frame') or {}).get('top')} "
                      f"glyphGapPx={g.get('glyphGapPx')}")


if __name__ == "__main__":
    main()
