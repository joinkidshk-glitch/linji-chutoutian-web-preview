# -*- coding: utf-8 -*-
"""v20a115 實駕：S-30 TEXT115 通告詳情卡文字重寫，改前／改後對照。
   用法：/home/hatch/pwenv49/bin/python drive115.py <repo-root> <before|after> [port]
   流程（每版）：本地 http.server → 新遊戲（槽 3 可棄用，?softPreview=1）
     → 墊高數值（S.vocal/stage/charm/stamina/fame；只為過 canAudition 閘見到
       softPreview 底部 note，唔郁文字、唔接通告）
     → 入星河電視台（ENC79 攔路就先播完再入）→ 只查看通告欄
     → 依次開兩張通告詳情：① 主目標 gig_1988_tvb_longmen_spring_high
       《靈幻喜劇迎春夜》（任務指定 id）② 《賀歲特輯》拜年群演
       gig_1988_entry_winter_cny_crowd（任務指定標題＋$156 簽約金所指嗰張；
       兩張 releaseLabel 相同，同一組文字改動）
     → 每張：摺疊態 DOM 讀行＋截圖 → 撳「顯示詳細」→ 展開態 DOM 讀行＋截圖
       （頂＋碌到底部）→ 撳「離開」返通告欄開下一張。
   產出：qa115/shots/<tag>_*.png ＋ qa115/drive115_<tag>.json
   （兩版跑完再合併做 qa115/drive115.json。）
   注意：遊戲本體係 IIFE，canAudition／openCastingNoticeDetail 等唔係全域，
   一律行 UI 撳掣；S／GIGS 有 window 導出，只讀數據。
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
GIGS = [
    ("spring", "gig_1988_tvb_longmen_spring_high", "靈幻喜劇迎春夜"),
    ("cny", "gig_1988_entry_winter_cny_crowd", "賀歲特輯"),
]
ERRORS = []
LOG = {"tag": TAG, "root": ROOT, "port": PORT, "errors": ERRORS,
       "entries": 0, "encounter_on_entry": None, "gigs": {}}

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
    """DOM .click()：地圖熱區掣 Playwright 撳唔到，DOM click 先穩。"""
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

JS_DETAIL = '''() => {
  const t = document.querySelector('[data-cn-toggle]');
  if (!t) return { present: false };
  let root = t;
  for (let i = 0; i < 8 && root.parentElement; i++) {
    root = root.parentElement;
    if (root.querySelector && root.querySelector('.cn-sum-row')) break;
  }
  const rows = [...root.querySelectorAll('.cn-sum-row')].map(r => ({
    k: (r.querySelector('.k')||{}).textContent ? r.querySelector('.k').textContent.trim() : null,
    v: (r.querySelector('.v')||{}).textContent ? r.querySelector('.v').textContent.trim() : null }));
  const det = root.querySelector('.cn-detail');
  // 底部 note 係 openCastingNoticeDetail 喺 castingNoticeDetailHtml 之後 append，
  // 係 .notice_sheet_frame 嘅兄弟節點——要由成個 #modal-inner 讀先見到。
  const mi = document.getElementById('modal-inner');
  const allNotes = mi ? [...mi.querySelectorAll('.var-note')].map(e => e.innerText.trim()) : [];
  const frame = root.closest ? root.closest('.notice_sheet_frame') : null;
  const frameNotes = frame ? [...frame.querySelectorAll('.var-note')].map(e => e.innerText.trim()) : [];
  const titleEl = (frame && frame.querySelector('h2.cn-work')) || (mi && mi.querySelector('h2.cn-work'));
  return { present: true,
    title: titleEl ? titleEl.textContent.trim() : null,
    sumRows: rows,
    varNotes: allNotes,
    varNotesInCard: frameNotes,
    bottomNotes: allNotes.filter(x => !frameNotes.includes(x)),
    toggleText: t.textContent.trim(), toggleExpanded: t.getAttribute('aria-expanded'),
    detailHidden: det ? !!det.hidden : null,
    detailText: det ? det.innerText.trim().slice(0, 2000) : null };
}'''

JS_GIGDATA = '''(gid) => {
  const g = (window.GIGS||[]).find(x => x && x.id === gid) || null;
  if (!g) return { found: false };
  return { found: true, title: g.title, payExact: g.payExact ?? null,
    pay: g.pay ?? null, signFee30: (typeof g.payExact === 'number' ? Math.round(g.payExact*0.3) : null),
    releaseLabel: g.releaseLabel || null, req: g.req || null, tier: g.tier || null };
}'''

def scroll_modal_bottom(pg):
    pg.evaluate('''() => {
      const t = document.querySelector('[data-cn-toggle]');
      if (!t) return;
      let el = t;
      while (el) { if (el.scrollHeight > el.clientHeight + 10) { el.scrollTop = el.scrollHeight; }
        el = el.parentElement; }
    }''')
    pg.wait_for_timeout(600)

def drive_gig(pg, key, gid, title_sub):
    rec = {"gig_id": gid, "data": pg.evaluate(JS_GIGDATA, gid)}
    # 板卡：.gig-teaser[data-gid]
    opened = pg.evaluate("""(gid) => {
      const card = document.querySelector('.gig-teaser[data-gid="' + gid + '"]');
      if (card && card.offsetParent !== null) { card.click(); return 'teaser'; }
      const cards = [...document.querySelectorAll('.gig-teaser')].filter(x=>x.offsetParent!==null);
      return 'not_found:' + cards.map(c=>c.dataset.gid).join(','); }""", gid)
    pg.wait_for_timeout(1200)
    rec["open"] = opened
    det0 = pg.evaluate(JS_DETAIL)
    rec["collapsed"] = det0
    pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_collapsed.png")
    print(f"  [{key}] open={opened} detail={det0.get('present')} title={det0.get('title')}")
    if det0.get("present"):
        clicked = pg.evaluate('''() => {
          const t = document.querySelector('[data-cn-toggle]');
          if (t && t.offsetParent !== null) { t.click(); return true; } return false; }''')
        pg.wait_for_timeout(1000)
        det1 = pg.evaluate(JS_DETAIL)
        rec["expanded"] = det1
        rec["toggle_clicked"] = clicked
        print(f"  [{key}] toggle={clicked} detailHidden={det1.get('detailHidden')}")
        pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_expanded.png")
        scroll_modal_bottom(pg)
        pg.screenshot(path=f"{SHOTS}/{TAG}_{key}_expanded_bottom.png")
        rec["expanded_bottom"] = pg.evaluate(JS_DETAIL)
    # 離開返通告欄（唔撳「去試鏡」，唔耗日）
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
        print("story active:", pg.evaluate("() => !!document.querySelector('.story-play')"))
        # 墊高數值過 canAudition 閘（fresh 遠低於 req＋fame 地板），只為見底部 note
        pg.evaluate("() => { S.vocal=400; S.stage=400; S.charm=450; S.stamina=350; S.fame=20; S.acting=400; }")
        print("boosted stats:", pg.evaluate("() => ({vocal:S.vocal, stage:S.stage, charm:S.charm, stamina:S.stamina, fame:S.fame, acting:S.acting})"))

        # ---- 入星河電視台 ----
        print("enter tvb:", dom_click(pg, "星河電視台"))
        LOG["entries"] = 1
        pg.wait_for_timeout(1200)
        enc = pg.evaluate(JS_ENC)
        print("encounter on entry:", enc)
        if enc["present"]:
            LOG["encounter_on_entry"] = enc
            print("ENC79 攔路，先播完再入")
            finish_encounter(pg)
            print("encounter finished, present now:", pg.evaluate(JS_ENC))
            dom_click(pg, "返回地圖")
            pg.wait_for_timeout(800)
            print("re-enter tvb:", dom_click(pg, "星河電視台"))
            LOG["entries"] = 2
            pg.wait_for_timeout(1200)
            print("encounter on re-entry:", pg.evaluate(JS_ENC))
        else:
            LOG["encounter_on_entry"] = {"present": False}
        print("sheet open:", pg.evaluate("() => !!document.querySelector('.map-wrap.sheet-open')"))

        # ---- 通告欄 ----
        print("board click:", dom_click(pg, "只查看通告欄"))
        pg.wait_for_timeout(1500)
        print("board teasers:", pg.evaluate("() => [...document.querySelectorAll('.gig-teaser')].filter(x=>x.offsetParent!==null).map(c=>c.dataset.gid)"))
        pg.screenshot(path=f"{SHOTS}/{TAG}_board.png")

        for key, gid, sub in GIGS:
            print(f"driving {key} {gid} ...")
            LOG["gigs"][key] = drive_gig(pg, key, gid, sub)

        b.close()
finally:
    stop(srv)

with open(os.path.join(HERE, f"drive115_{TAG}.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("ERRORS:", ERRORS if ERRORS else "none")
for key in ("spring", "cny"):
    g = LOG["gigs"].get(key) or {}
    c = (g.get("collapsed") or {})
    e = (g.get("expanded") or {})
    print(f"[{key}] data={json.dumps(g.get('data'), ensure_ascii=False)}")
    print(f"[{key}] collapsed rows={json.dumps(c.get('sumRows'), ensure_ascii=False)}")
    print(f"[{key}] collapsed varNotes={json.dumps(c.get('varNotes'), ensure_ascii=False)}")
    print(f"[{key}] expanded varNotes={json.dumps(e.get('varNotes'), ensure_ascii=False)}")
