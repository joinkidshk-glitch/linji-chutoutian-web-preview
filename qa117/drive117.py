# -*- coding: utf-8 -*-
"""v20a117 實駕：S-30 DEDUP117 詳情區刪除＋唯一資料搬摘要＋欄卡 meta 拆行，改前／改後對照。
   用法：/home/hatch/pwenv49/bin/python drive117.py <repo-root> <before|after> [port]
   流程（每版）：本地 http.server → 新遊戲（槽 3 可棄用，?softPreview=1）
     → 墊高數值（過 canAudition 閘見底部 note）→ 入星河電視台睇《賀歲特輯》
     → 返地圖 → 入維港電影睇《戲院人潮》→ 每張：通告欄 meta 讀出＋摘要逐行讀出
       ＋（改前）撳「顯示詳細」讀詳細區；（改後）確認掣消失＋碌到底部。
   產出：qa117/shots/<tag>_*.png ＋ qa117/drive117_<tag>.json
   注意：遊戲本體係 IIFE，一律行 UI 撳掣；S／GIGS 有 window 導出，只讀數據。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = sys.argv[1]
TAG = sys.argv[2] if len(sys.argv) > 2 else "before"
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 8971
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107"
# (key, gig id, 地點名, 地點 sheet 入口掣文字)
GIGS = [
    ("cny", "gig_1988_entry_winter_cny_crowd", "星河電視台"),
    ("cinema", "gig_1988_entry_winter_cinema_crowd", "維港電影"),
]
ERRORS = []
LOG = {"tag": TAG, "root": ROOT, "port": PORT, "errors": ERRORS,
       "entries": 0, "encounter_on_entry": {}, "gigs": {}, "director_census": None}

def http_get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} taken?)")
    st, body = http_get("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    if st != 200 or sha != exp:
        raise RuntimeError(f"served index mismatch: {st} sha={sha[:12]} expected={exp[:12]}")
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

def dom_click(pg, sub, selector="button"):
    return pg.evaluate("""([sub, sel]) => {
      const els=[...document.querySelectorAll(sel)].filter(x=>x.offsetParent!==null);
      const hit=els.find(x=>(x.textContent||'').includes(sub));
      if(!hit) return {found:false};
      hit.click(); return {found:true, text:hit.textContent.trim().replace(/\\s+/g,' ').slice(0,70)}; }""",
      [sub, selector])

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
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov || !ov.offsetParent) return { present: false };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  return { present: true, name: name ? name.textContent : null,
    line: line ? line.textContent : null };
}'''

def finish_encounter(pg):
    for _ in range(30):
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; } return null; }""")
        if not clicked:
            break
        pg.wait_for_timeout(400)
        if not pg.evaluate(JS_ENC)["present"]:
            break

def dismiss_interstitial(pg):
    """入場隨機事件 modal 鏈（例如維港電影「通宵廠凌晨三點」：繼續→睇落去→二揀一）
       會擋住地點 sheet。隨機觸發，有時唔出。逐個撳走：先撳確認類掣，淨低二揀一
       嗰陣撳第一個（棄用槽存檔，後果唔影響 S-30 核對，log 低佢）；見到
       「只查看通告欄」即停。"""
    for _ in range(6):
        st = pg.evaluate("""() => {
          const btns=[...document.querySelectorAll('#modal-btns button, #mask button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim());
          return { btns }; }""")
        btns = st["btns"]
        if not btns:
            return "clear"
        if any("只查看通告欄" in x for x in btns):
            return "board"
        hit = pg.evaluate("""() => {
          const btns=[...document.querySelectorAll('#modal-btns button, #mask button')].filter(x=>x.offsetParent!==null);
          const ack=btns.find(x=>/^(繼續|知道了|睇落去|明白|收到)$/.test((x.textContent||'').trim()));
          const b=ack||btns[0];
          const t=(b.textContent||'').trim(); b.click(); return {clicked:t, wasChoice:!ack}; }""")
        print("dismiss interstitial:", hit)
        pg.wait_for_timeout(900)
    return "still_blocked"

def open_board(pg, loc_name):
    """入地點＋清事件鏈＋開通告欄；唔成功就返地圖重入一次（隨機事件未必再觸發）。"""
    for attempt in (1, 2):
        LOG["entries"] += enter_loc(pg, loc_name)
        pg.wait_for_timeout(800)
        dismiss_interstitial(pg)
        r = dom_click(pg, "只查看通告欄")
        print(f"board click (attempt {attempt}):", r)
        if r.get("found"):
            pg.wait_for_timeout(1500)
            return True
        print("board not reached, back to map and retry")
        dom_click(pg, "返回地圖")
        pg.wait_for_timeout(1000)
    return False

def enter_loc(pg, loc_name):
    """入地點；ENC79 攔路就播完再入。回傳 (entries, enc_first)."""
    entries = 0
    print("enter:", dom_click(pg, loc_name)); entries += 1
    pg.wait_for_timeout(1200)
    enc = pg.evaluate(JS_ENC)
    LOG["encounter_on_entry"][loc_name] = enc
    if enc["present"]:
        print("ENC79 攔路，先播完再入")
        finish_encounter(pg)
        print("encounter finished, present now:", pg.evaluate(JS_ENC))
        dom_click(pg, "返回地圖")
        pg.wait_for_timeout(800)
        print("re-enter:", dom_click(pg, loc_name)); entries += 1
        pg.wait_for_timeout(1200)
        print("encounter on re-entry:", pg.evaluate(JS_ENC))
    return entries

# 讀通告欄卡片 meta（實際渲染段數＋結構）
JS_BOARD_META = '''(gid) => {
  const card = document.querySelector('.gig-teaser[data-gid="' + gid + '"]');
  if (!card) return { found: false };
  const m = card.querySelector('.gt-meta');
  if (!m) return { found: true, meta: null };
  return { found: true, metaText: m.innerText.trim(),
    metaHtml: m.innerHTML.trim().slice(0, 300),
    childTags: [...m.children].map(c => c.tagName + '.' + (c.className||'')),
    childCount: m.children.length,
    childTexts: [...m.children].map(c => c.innerText.trim()) };
}'''

# 讀詳情卡全貌：摘要行／cn-kv 行／導演／製作人／簡介／掣／詳細區
JS_SHEET = '''() => {
  const frame = document.querySelector('.notice_sheet_frame');
  if (!frame) return { present: false };
  const rows = [...frame.querySelectorAll('.cn-summary .cn-sum-row')].map(r => ({
    k: (r.querySelector('.k')||{}).textContent ? r.querySelector('.k').textContent.trim() : null,
    v: (r.querySelector('.v')||{}).textContent ? r.querySelector('.v').textContent.trim() : null }));
  const kvs = [...frame.querySelectorAll('.cn-summary .cn-kv')].map(e => ({
    cls: e.className, text: e.innerText.trim().replace(/\\n/g, ' | ') }));
  const dirEl = frame.querySelector('.cn-director-line');
  const prodEl = frame.querySelector('.cn-producer-line');
  const synEl = frame.querySelector('.notice_synopsis_frame');
  const t = frame.querySelector('[data-cn-toggle]');
  const det = frame.querySelector('.cn-detail');
  const mi = document.getElementById('modal-inner');
  const allNotes = mi ? [...mi.querySelectorAll('.var-note')].map(e => e.innerText.trim()) : [];
  const frameNotes = [...frame.querySelectorAll('.var-note')].map(e => e.innerText.trim());
  const titleEl = frame.querySelector('h2.cn-work');
  return { present: true,
    title: titleEl ? titleEl.textContent.trim() : null,
    sumRows: rows, kvRows: kvs,
    directorLine: dirEl ? dirEl.innerText.trim() : null,
    producerLine: prodEl ? prodEl.innerText.trim() : null,
    synopsis: synEl ? synEl.innerText.trim().slice(0, 600) : null,
    togglePresent: !!t, toggleText: t ? t.textContent.trim() : null,
    detailPresent: !!det, detailHidden: det ? !!det.hidden : null,
    detailText: det ? det.innerText.trim().slice(0, 2500) : null,
    varNotesInCard: frameNotes,
    bottomNotes: allNotes.filter(x => !frameNotes.includes(x)) };
}'''

JS_GIGDATA = '''(gid) => {
  const g = (window.GIGS||[]).find(x => x && x.id === gid) || null;
  if (!g) return { found: false };
  return { found: true, title: g.title, director: g.director ?? null,
    producer: g.producer ?? null, limits: g.limits ?? null,
    shootWeekdays: g.shootWeekdays ?? null, shootDaysHint: g.shootDaysHint ?? null,
    shootBand: g.shootBand ?? null, payExact: g.payExact ?? null,
    releaseLabel: g.releaseLabel || null, req: g.req || null, tier: g.tier || null };
}'''

JS_CENSUS = '''() => {
  const GENERIC = ["副導","特輯副導","副導阿標","廣告助導","場務阿強","外景場記","平面攝影師阿忠","錄音室助導"];
  const gs = (window.GIGS||[]);
  const vals = gs.map(g => (g && g.director != null) ? String(g.director) : "<MISSING>");
  const gen = {};
  vals.forEach(v => { if (GENERIC.includes(v)) gen[v] = (gen[v]||0)+1; });
  return { total: gs.length, missing: vals.filter(v => v==="<MISSING>").length,
    genericTotal: Object.values(gen).reduce((a,b)=>a+b,0), genericBreakdown: gen,
    distinct: [...new Set(vals)].length,
    withProducer: gs.filter(g => g && g.producer).length,
    withLimitsNotes: gs.filter(g => g && g.limits && Array.isArray(g.limits.notes) && g.limits.notes.length).length,
    withLimitsObj: gs.filter(g => g && g.limits).length };
}'''

def scroll_modal_bottom(pg):
    pg.evaluate('''() => {
      const mi = document.getElementById('modal-inner');
      if (mi) mi.scrollTop = mi.scrollHeight;
      const b = document.querySelector('.notice_sheet_body');
      if (b) b.scrollTop = b.scrollHeight; }''')
    pg.wait_for_timeout(600)

def drive_gig(pg, key, gid):
    rec = {"gig_id": gid, "data": pg.evaluate(JS_GIGDATA, gid)}
    rec["board_meta"] = pg.evaluate(JS_BOARD_META, gid)
    opened = pg.evaluate("""(gid) => {
      const card = document.querySelector('.gig-teaser[data-gid="' + gid + '"]');
      if (card && card.offsetParent !== null) { card.click(); return 'teaser'; }
      const cards = [...document.querySelectorAll('.gig-teaser')].filter(x=>x.offsetParent!==null);
      return 'not_found:' + cards.map(c=>c.dataset.gid).join(','); }""", gid)
    pg.wait_for_timeout(1200)
    rec["open"] = opened
    sheet0 = pg.evaluate(JS_SHEET)
    rec["sheet"] = sheet0
    pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_sheet.png")
    print(f"  [{key}] open={opened} title={sheet0.get('title')} toggle={sheet0.get('togglePresent')} detail={sheet0.get('detailPresent')}")
    print(f"  [{key}] meta={json.dumps(rec['board_meta'], ensure_ascii=False)}")
    if sheet0.get("togglePresent"):
        clicked = pg.evaluate('''() => {
          const t = document.querySelector('[data-cn-toggle]');
          if (t && t.offsetParent !== null) { t.click(); return true; } return false; }''')
        pg.wait_for_timeout(1000)
        rec["toggle_clicked"] = clicked
        rec["expanded"] = pg.evaluate(JS_SHEET)
        pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_expanded.png")
        scroll_modal_bottom(pg)
        pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_expanded_bottom.png")
        rec["expanded_bottom"] = pg.evaluate(JS_SHEET)
    else:
        scroll_modal_bottom(pg)
        pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_sheet_bottom.png")
        rec["sheet_bottom"] = pg.evaluate(JS_SHEET)
    left = pg.evaluate('''() => {
      const row = document.getElementById('modal-btns');
      if (!row) return 'no_modal_btns';
      const btns = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null);
      const leave = btns.find(x => !/試鏡/.test(x.textContent||''));
      if (leave) { leave.click(); return leave.textContent.trim(); }
      return 'no_leave_btn:' + btns.map(x=>x.textContent.trim()).join('|'); }''')
    pg.wait_for_timeout(1200)
    rec["leave"] = left
    rec["board_back"] = pg.evaluate("() => !!document.querySelector('.gig-teaser')")
    print(f"  [{key}] leave={left} board_back={rec['board_back']}")
    return rec

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: ERRORS.append("pageerror: " + str(e)))
        pg.on("console", lambda m: ERRORS.append("console.error: " + m.text) if m.type == "error" else None)

        print("new game:", new_game(pg))
        pg.evaluate("() => { S.vocal=400; S.stage=400; S.charm=450; S.stamina=350; S.fame=20; S.acting=400; }")
        LOG["director_census"] = pg.evaluate(JS_CENSUS)
        print("census:", json.dumps(LOG["director_census"], ensure_ascii=False))

        for key, gid, loc_name in GIGS:
            print(f"driving {key} {gid} @ {loc_name} ...")
            open_board(pg, loc_name)
            print("board teasers:", pg.evaluate("() => [...document.querySelectorAll('.gig-teaser')].filter(x=>x.offsetParent!==null).map(c=>c.dataset.gid)"))
            pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_board.png")
            LOG["gigs"][key] = drive_gig(pg, key, gid)
            # 返地圖（下一張喺另一地點）
            print("back to map:", dom_click(pg, "返回地圖"))
            pg.wait_for_timeout(1000)

        b.close()
finally:
    stop(srv)

with open(os.path.join(HERE, f"drive117_{TAG}.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("ERRORS:", ERRORS if ERRORS else "none")
for key in ("cny", "cinema"):
    g = LOG["gigs"].get(key) or {}
    s = (g.get("sheet") or {})
    print(f"[{key}] data director={json.dumps((g.get('data') or {}).get('director'), ensure_ascii=False)} producer={json.dumps((g.get('data') or {}).get('producer'), ensure_ascii=False)} limits={json.dumps((g.get('data') or {}).get('limits'), ensure_ascii=False)}")
    print(f"[{key}] meta={json.dumps(g.get('board_meta'), ensure_ascii=False)}")
    print(f"[{key}] sumRows={json.dumps(s.get('sumRows'), ensure_ascii=False)}")
    print(f"[{key}] kvRows={json.dumps(s.get('kvRows'), ensure_ascii=False)}")
    print(f"[{key}] directorLine={json.dumps(s.get('directorLine'), ensure_ascii=False)} producerLine={json.dumps(s.get('producerLine'), ensure_ascii=False)}")
    print(f"[{key}] synopsis={json.dumps((s.get('synopsis') or '')[:120], ensure_ascii=False)}")
    print(f"[{key}] toggle={s.get('togglePresent')} detail={s.get('detailPresent')} detailHidden={s.get('detailHidden')}")
