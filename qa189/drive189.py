# -*- coding: utf-8 -*-
"""v20a189 實駕 drive189：日結板三粒掣（返回地圖／開始今日行程／加速本週剩餘）× 932／700。
用法：/home/hatch/pwenv49/bin/python qa189/drive189.py [--mode pristine|fixed]
Mirror：工作副本 ~/workspace/linji-work189，port 8975，live 模式（唔用 ?softPreview=1）。
播種：經 new_game 正常開局（slot 3），再 live 改 S（weekPlan＋probe shoots）＋saveQ()。
觸發（真實 UI 路徑，唔直叫 IIFE 內函數）：開茶餐廳 sheet → sheet「返回地圖」→
  goToMapForBrowse → kickScheduleIfNeeded（今日係強制拍攝日）→ resolvePlannedDay →
  殺青 wrap 日結 modal。分支由聽日計劃決定：street=soft／scout_all=map／shoot:=forced。
  休息卡另案：今日 rest → 地圖 #map-start-today → presentRestSleepDayEnd。
量度（DOM 為準，截圖只係記錄）：#modal-btns 掣列（label／role／行數）、加速係掣定細連結、
  #modal-inner scrollHeight vs clientHeight、綠色 .good 行有冇喺 fold 位裁一半、
  撳掣後去向（地圖／新日結板）＋dayIndex 變化、pageerror／console error／失敗請求。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, sys, argparse

ROOT = "/home/hatch/workspace/linji-work189"
HERE = os.path.join(ROOT, "qa189")
SHOTS = os.path.join(HERE, "shots189")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8975
URL = f"http://127.0.0.1:{PORT}/index.html"
REPORT = {"errors": [], "http_fail": [], "runs": {}}

ap = argparse.ArgumentParser()
ap.add_argument("--mode", default="pristine", choices=["pristine", "fixed"])
ap.add_argument("--only", default="", help="只跑指定 case key，例如 soft-map-932")
ARGS = ap.parse_args()


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


def js_click_text(pg, text):
    return pg.evaluate("""(t) => {
      const b = [...document.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def js_click_contains(pg, text, scope=None):
    return pg.evaluate("""(args) => {
      const root = args.scope ? document.querySelector(args.scope) : document;
      if (!root) return false;
      const b = [...root.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').includes(args.t));
      if (!b) return false; b.click(); return true; }""", {"t": text, "scope": scope})


def modal_click(pg, text):
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)


def play_through_story(pg, max_steps=80):
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


SEED_JS = """(branch) => {
  try {
    const wd = (d)=>((d%7)+7)%7;
    // 歸一化：逢週日就將 dayIndex 推前到星期一（唔係就 wrap 日撞週結，ended=true 冇得驗分支；
    // probe 專用，唔改經濟／劇情，只係揀個星期一開局）。
    while (wd(S.dayIndex) === 6) S.dayIndex += 1;
    const today = S.dayIndex, twd = wd(today), nwd = wd(today+1);
    S.stress = 10;
    S.homeEditable = false;
    if (S.conseq61) { S.conseq61.sick = null; S.conseq61.streak90 = 0; S.conseq61.streak80 = 0; S.conseq61.cooldownUntil = 0; S.conseq61.pendingEnding = null; }
    const g = (typeof GIGS !== 'undefined' ? GIGS.find(x=>x && x.type==='電影' && x.title) : null) || {id:'probe_gig', title:'探測片'};
    S.shoots = (S.shoots||[]).filter(x=>x && x.id!=='probe189w' && x.id!=='probe189f');
    S.shoots.push({id:'probe189w', gigId:g.id, title:g.title, type:'電影', totalDays:1, doneDays:0, pay:6000, fame:5, popularity:5, signedPaid:0});
    S.shoots.push({id:'probe189f', gigId:g.id, title:g.title+'（下日）', type:'電影', totalDays:3, doneDays:0, pay:9000, fame:5, popularity:5, signedPaid:0});
    S.weekPlan = S.weekPlan || [];
    for(let i=0;i<7;i++) S.weekPlan[i]='rest';
    S.weekPlan[twd]='shoot:probe189w';
    if(branch==='soft') S.weekPlan[nwd]='street';
    else if(branch==='map') S.weekPlan[nwd]='scout_all';
    else if(branch==='forced') S.weekPlan[nwd]='shoot:probe189f';
    try{ saveQ(); }catch(e){}
    return {ok:true, gigId:g.id, dayIndex:S.dayIndex, todayPlan:S.weekPlan[twd], tomPlan:S.weekPlan[nwd]};
  } catch(e){ return {ok:false, err:String(e)}; }
}"""

SEED_REST_JS = """() => {
  try {
    const wd = (d)=>((d%7)+7)%7;
    // 歸一化到星期一（今日 Mon、聽日 Tue street，週內仲有 rest 日 → 加速連結要出現）
    while (wd(S.dayIndex) !== 0) S.dayIndex += 1;
    S.stress = 10;
    S.homeEditable = false;
    if (S.conseq61) { S.conseq61.sick = null; S.conseq61.streak90 = 0; S.conseq61.streak80 = 0; S.conseq61.cooldownUntil = 0; S.conseq61.pendingEnding = null; }
    const today = S.dayIndex, twd = wd(today), nwd = wd(today+1);
    S.weekPlan = S.weekPlan || [];
    for(let i=0;i<7;i++) S.weekPlan[i]='rest';
    S.weekPlan[twd]='rest';
    S.weekPlan[nwd]='street';
    try{ saveQ(); }catch(e){}
    return {ok:true, dayIndex:S.dayIndex, todayPlan:S.weekPlan[twd], tomPlan:S.weekPlan[nwd]};
  } catch(e){ return {ok:false, err:String(e)}; }
}"""

MEASURE_JS = """() => {
  const q = (s) => document.querySelector(s);
  const mi = q('#modal-inner'), mb = q('#modal-btns'), modal = q('#modal');
  if (!mi || !mb) return {modalOpen:false};
  const r = (el) => { const b = el.getBoundingClientRect();
    return {top:Math.round(b.top), bottom:Math.round(b.bottom), left:Math.round(b.left), right:Math.round(b.right), w:Math.round(b.width), h:Math.round(b.height)}; };
  const mir = r(mi), mbr = r(mb);
  const btns = [...mb.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>{
    const cs = getComputedStyle(b);
    return {t:(b.textContent||'').trim(), cls:b.className, fontSize:cs.fontSize,
      minHeight:cs.minHeight, bg:cs.backgroundColor, deco:cs.textDecorationLine, rect:r(b)}; });
  // 每行文字：.result-line + #modal-inner 內 p／gold／good 元素，睇有冇喺 fold 位裁一半
  const lines = [];
  mi.querySelectorAll('.result-line, p, .wrap-poster59-cap, figure.chk101').forEach(el=>{
    const b = el.getBoundingClientRect();
    if (b.height <= 0) return;
    const txt = (el.textContent||'').trim().slice(0,40);
    const green = !!el.querySelector('.good') || el.classList.contains('good') || (el.closest && el.closest('.good'));
    const straddle = b.top < mir.bottom && b.bottom > mir.bottom;
    const fullyBelow = b.top >= mir.bottom;
    lines.push({txt, green, top:Math.round(b.top), bottom:Math.round(b.bottom), straddle, fullyBelow,
      cls: el.className && String(el.className).slice(0,40)});
  });
  const greenCut = lines.filter(l=>l.green && l.straddle);
  const anyCut = lines.filter(l=>l.straddle);
  const h3 = mi.querySelector('h3');
  return {modalOpen: document.getElementById('mask').classList.contains('on'),
    title: h3 ? (h3.textContent||'').trim() : null,
    dayIndex: (typeof S!=='undefined') ? S.dayIndex : null,
    dateStr: (typeof S!=='undefined') ? S.dateStr : null,
    modalRect: modal ? r(modal) : null, innerRect: mir, btnsRect: mbr,
    inner: {scrollH: mi.scrollHeight, clientH: mi.clientHeight, scrollTop: mi.scrollTop,
      overflowY: getComputedStyle(mi).overflowY, canScroll: mi.scrollHeight > mi.clientHeight + 1},
    btns, btnRows: (()=>{ const tops=[...new Set(btns.map(b=>b.rect.top))]; return tops.length; })(),
    lines, greenCut, anyCut: anyCut.map(l=>({txt:l.txt, top:l.top, bottom:l.bottom})),
    greenCutN: greenCut.length, anyCutN: anyCut.length,
    hint: !!mi.querySelector('.week-accel-hint'),
    mapVisible: (()=>{ const v=q('#v-map'); return v ? v.offsetParent!==null : null; })()};
}"""

SCROLL_JS = """() => {
  const mi = document.querySelector('#modal-inner');
  if (!mi) return {ok:false};
  const before = mi.scrollTop;
  mi.scrollTop = mi.scrollHeight;
  const after = mi.scrollTop;
  const mir = mi.getBoundingClientRect();
  const last = [];
  mi.querySelectorAll('.result-line, p').forEach(el=>{
    const b = el.getBoundingClientRect();
    if (b.height <= 0) return;
    last.push({txt:(el.textContent||'').trim().slice(0,40),
      green: !!el.querySelector('.good') || el.classList.contains('good'),
      top:Math.round(b.top), bottom:Math.round(b.bottom),
      fullyVisible: b.top >= mir.top && b.bottom <= mir.bottom});
  });
  const hint = mi.querySelector('.week-accel-hint');
  const hr = hint ? hint.getBoundingClientRect() : null;
  return {ok:true, before, after, moved: after > before,
    maxScroll: mi.scrollHeight - mi.clientHeight,
    lastLines: last.slice(-4),
    hintVisible: hr ? (hr.top >= mir.top && hr.bottom <= mir.bottom) : null};
}"""

STATE_JS = """() => ({
  maskOn: document.getElementById('mask').classList.contains('on'),
  dayIndex: (typeof S!=='undefined') ? S.dayIndex : null,
  dateStr: (typeof S!=='undefined') ? S.dateStr : null,
  mapVisible: (()=>{ const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : null; })(),
  title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h ? (h.textContent||'').trim() : null; })(),
  modalBtns: [...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim()),
  story: !!document.querySelector('.story-play .dlg106-plate'),
  enc: !!document.getElementById('enc79-overlay')
})"""


def ensure_on_map(pg):
    """新局完係 v-home；撳「返回地圖」入地圖（JS click，唔怕遮住）。"""
    for _ in range(6):
        st = pg.evaluate(STATE_JS)
        if st["mapVisible"] and not st["maskOn"]:
            return True
        if st["story"]:
            play_through_story(pg); continue
        if st["maskOn"]:
            return False
        if js_click_text(pg, "返回地圖"):
            pg.wait_for_timeout(1000); continue
        pg.wait_for_timeout(500)
    return pg.evaluate("() => { const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : false; }")


def settle_to_map(pg, max_rounds=6):
    """每個 case 完結後收尾：撳穿殘留日結板／中途 modal，直到返到地圖。"""
    for _ in range(max_rounds):
        st = pg.evaluate(STATE_JS)
        if st["mapVisible"] and not st["maskOn"]:
            return True
        if st["enc"]:
            dismiss_encounter(pg); continue
        if st["story"]:
            play_through_story(pg); continue
        if st["maskOn"]:
            if modal_click(pg, "返回地圖"):
                pg.wait_for_timeout(900); chain_to_map(pg); continue
            if modal_click(pg, "回家結算"):
                pg.wait_for_timeout(1200); ensure_on_map(pg); continue
            if modal_click(pg, "開始今日行程"):
                pg.wait_for_timeout(900); chain_to_map(pg); continue
            if modal_click(pg, "好") or modal_click(pg, "關閉") or modal_click(pg, "知道了"):
                pg.wait_for_timeout(900); continue
            if pg.evaluate("() => { const b=[...document.querySelectorAll('#modal-btns button')].filter(e=>e.offsetParent!==null); if(b[0]){b[0].click(); return true;} return false; }"):
                pg.wait_for_timeout(900); continue
            return False
        if ensure_on_map(pg):
            return True
        return False
    return pg.evaluate("() => { const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : false; }")


def open_sheet_and_back_to_map(pg):
    """開茶餐廳 sheet → sheet「返回地圖」→ goToMapForBrowse（kick 今日強制日）。"""
    dismiss_encounter(pg)
    ensure_on_map(pg)
    opened = False
    for _ in range(4):
        opened = js_click_contains(pg, "茶餐廳", "#v-map")
        if opened:
            break
        pg.wait_for_timeout(900)
        ensure_on_map(pg)
    pg.wait_for_timeout(1500)
    if not opened:
        return {"ok": False, "step": "open-sheet"}
    dismiss_encounter(pg)
    # C1 可能喺第一次入地點嗰陣彈出
    if pg.evaluate("() => !!document.querySelector('.story-play .dlg106-plate')"):
        play_through_story(pg)
        pg.wait_for_timeout(800)
        modal_click(pg, "關閉")
        pg.wait_for_timeout(800)
    hit = pg.evaluate("""() => {
      const sh = document.getElementById('loc-sheet'); if (!sh) return false;
      const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === '返回地圖');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    return {"ok": bool(hit), "step": "sheet-back" if hit else "sheet-back-missing"}


def wait_dayend_modal(pg, timeout_ms=15000):
    """等日結板：中途可能有晨報／獎勵 modal 攔路，逐個撳穿佢哋。"""
    dayend_re = ("殺青", "街頭", "休息", "小休", "拍攝中", "拍攝日", "散工收工")
    for _ in range(timeout_ms // 250):
        st = pg.evaluate(STATE_JS)
        if st["maskOn"] and st["title"] and any(k in st["title"] for k in dayend_re):
            return st
        if st["story"]:
            play_through_story(pg)
        elif st["enc"]:
            dismiss_encounter(pg)
        elif st["maskOn"] and st["title"]:
            # 中途 modal（晨報／獎勵／報紙）：撳主掣穿過去
            hit = False
            for t in ["收下這份反響", "收下這份剪報", "收下這晚", "好", "知道了", "關閉", "繼續", "返回地圖"]:
                if modal_click(pg, t):
                    hit = True; break
            if not hit:
                return st
        pg.wait_for_timeout(250)
    return pg.evaluate(STATE_JS)


def chain_to_map(pg, max_steps=24):
    """撳完掣之後一路撳穿中途 modal（殺青獎勵／晨報／報紙），直到返到地圖或新日結板。"""
    log = []
    for i in range(max_steps):
        pg.wait_for_timeout(600)
        st = pg.evaluate(STATE_JS)
        log.append({"step": i, "maskOn": st["maskOn"], "title": st["title"],
                    "btns": st["modalBtns"], "day": st["dayIndex"], "map": st["mapVisible"]})
        if st["enc"]:
            dismiss_encounter(pg); continue
        if st["story"]:
            play_through_story(pg); continue
        # 劇情抉擇（.sp-choice，唔係 #modal-btns 掣）：揀第一項
        if pg.evaluate("() => [...document.querySelectorAll('.sp-choice')].some(e => e.offsetParent !== null)"):
            pg.evaluate("() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null); if (c[0]) c[0].click(); }")
            log.append({"clicked": "sp-choice[0]"})
            pg.wait_for_timeout(900)
            continue
        if not st["maskOn"] and st["mapVisible"]:
            return {"reached": "map", "log": log}
        if st["maskOn"] and st["title"]:
            # 新日結板（開始行程後嘅下一日結算）
            if st["title"] and ("拍攝中" in st["title"] or "街頭" in st["title"] or "休息" in st["title"] or "小休" in st["title"]):
                return {"reached": "new-dayend", "log": log}
            # 中途 modal：優先撳佢嘅主掣
            for t in ["收下這份反響", "收下這份剪報", "收下這晚", "睇落去", "繼續", "下一句", "好", "知道了", "關閉", "返回地圖", "回家結算"]:
                if modal_click(pg, t):
                    log.append({"clicked": t}); break
            else:
                # 劇情抉擇 modal（兩選一）：撳第一粒掣當揀第一個選項
                if pg.evaluate("() => { const b=[...document.querySelectorAll('#modal-btns button')].filter(e=>e.offsetParent!==null); if(b[0]){b[0].click(); return b[0].textContent.trim();} return null; }"):
                    log.append({"clicked": "first-btn-fallback"})
                else:
                    return {"reached": "stuck-modal", "log": log}
            continue
        if not st["maskOn"] and not st["mapVisible"]:
            if pg.evaluate("() => { const v=document.querySelector('#v-home'); return v ? v.offsetParent!==null : false; }"):
                return {"reached": "home", "log": log}
            return {"reached": "nomask-nomap", "log": log}
    return {"reached": "timeout", "log": log}


def run_wrap_case(pg, vp, branch, click_label, tag):
    """一個 wrap modal case：播種 → 開板 → 量度 → 撳指定掣 → 驗去向。"""
    key = f"{tag}-{branch}-{click_label}-{vp}"
    if ARGS.only and ARGS.only not in key:
        return None
    pg.set_viewport_size({"width": 390, "height": vp})
    pg.wait_for_timeout(400)
    seed = pg.evaluate(SEED_JS, branch)
    print(f"== {key} == seed={seed}", flush=True)
    assert seed.get("ok"), f"seed failed {seed}"
    day_before = pg.evaluate("() => S.dayIndex")
    op = open_sheet_and_back_to_map(pg)
    st = wait_dayend_modal(pg)
    print(f"  open={op} state title={st['title']!r} day={st['dayIndex']} btns={st['modalBtns']}", flush=True)
    m = pg.evaluate(MEASURE_JS)
    pg.wait_for_timeout(300)
    m["scrollTest"] = pg.evaluate(SCROLL_JS)
    pg.evaluate("() => { const mi=document.querySelector('#modal-inner'); if(mi) mi.scrollTop=0; }")
    pg.wait_for_timeout(200)
    pg.screenshot(path=os.path.join(SHOTS, f"{key}_modal.png"))
    day_at_modal = m.get("dayIndex")
    clicked = modal_click(pg, click_label)
    print(f"  click {click_label!r} -> {clicked}", flush=True)
    pg.wait_for_timeout(800)
    out = chain_to_map(pg)
    day_after = pg.evaluate("() => S.dayIndex")
    print(f"  outcome={out['reached']} day {day_before}->{day_at_modal}->{day_after}", flush=True)
    settled = settle_to_map(pg)
    print(f"  settle_to_map={settled}", flush=True)
    res = {"key": key, "vp": vp, "branch": branch, "click": click_label,
           "seed": seed, "open": op, "modal": m, "clicked": clicked,
           "outcome": out["reached"], "chain": out["log"],
           "day_before": day_before, "day_at_modal": day_at_modal, "day_after": day_after,
           "settled": settled,
           "pageerrors": list(REPORT["errors"])}
    REPORT["runs"][key] = res
    return res


def click_through_to_confirm(pg, max_steps=12):
    """撳完加速／返回地圖後，中途可能有殺青獎勵 modal（收下這份反響／剪報）攔路；
    逐個撳穿佢哋，直到「加速本週剩餘？」確認 modal 出現（返 True）或返到日結板（返 False）。"""
    for _ in range(max_steps):
        pg.wait_for_timeout(700)
        st = pg.evaluate(STATE_JS)
        if st["title"] == "加速本週剩餘？":
            return True
        if st["title"] and "殺青" in st["title"]:
            return False
        if st["story"]:
            play_through_story(pg); continue
        if st["enc"]:
            dismiss_encounter(pg); continue
        if st["maskOn"]:
            for t in ["收下這份反響", "收下這份剪報", "收下這晚", "知道了", "好", "關閉", "睇落去", "繼續"]:
                if modal_click(pg, t):
                    break
            else:
                return False
            continue
        return False
    return pg.evaluate("() => { const h=document.querySelector('#modal-inner h3'); return h && (h.textContent||'').trim()==='加速本週剩餘？'; }")


def run_accel_case(pg, vp, tag="accel"):
    """加速兩段：
    (1) soft 板撳加速 →（穿獎勵 modal）→ 確認 modal 出現 → 取消 → 落返地圖（既定行為：取消即關板，日唔郁）；
    (2) 重新播種再開板 → 撳加速 → 確認加速 → 行加速流程（合併本週剩餘日 → 落地圖／下一關鍵板）。"""
    key = f"{tag}-{vp}"
    if ARGS.only and ARGS.only not in key:
        return None
    pg.set_viewport_size({"width": 390, "height": vp})
    pg.wait_for_timeout(400)
    # --- 段 1：確認 modal ＋ 取消 ---
    seed = pg.evaluate(SEED_JS, "soft")
    assert seed.get("ok")
    op = open_sheet_and_back_to_map(pg)
    st = wait_dayend_modal(pg)
    m = pg.evaluate(MEASURE_JS)
    m["scrollTest"] = pg.evaluate(SCROLL_JS)
    pg.evaluate("() => { const mi=document.querySelector('#modal-inner'); if(mi) mi.scrollTop=0; }")
    print(f"== {key} == title={st['title']!r} btns={st['modalBtns']}", flush=True)
    pg.screenshot(path=os.path.join(SHOTS, f"{key}_modal.png"))
    accel_label = None
    for b in m.get("btns", []):
        if "加速" in b["t"]:
            accel_label = b["t"]
    if not accel_label:
        print(f"  !! no accel control found: {m.get('btns')}", flush=True)
        res = {"key": key, "vp": vp, "modal": m, "accel_label": None, "error": "no-accel-control"}
        REPORT["runs"][key] = res
        dump_report()
        return res
    day0 = pg.evaluate("() => S.dayIndex")
    ok1 = modal_click(pg, accel_label)
    pg.wait_for_timeout(900)
    reached_confirm = click_through_to_confirm(pg)
    st1 = pg.evaluate(STATE_JS)
    print(f"  accel click -> {ok1}; confirm reached={reached_confirm} title={st1['title']!r} btns={st1['modalBtns']}", flush=True)
    pg.screenshot(path=os.path.join(SHOTS, f"{key}_confirm.png"))
    cancel = modal_click(pg, "取消")
    pg.wait_for_timeout(800)
    st2 = pg.evaluate(STATE_JS)
    print(f"  cancel -> {cancel}; after-cancel mask={st2['maskOn']} map={st2['mapVisible']} day={st2['dayIndex']}", flush=True)
    cancel_ok = bool(cancel) and (not st2["maskOn"]) and bool(st2["mapVisible"]) and st2["dayIndex"] == day0
    # --- 段 2：重新播種，確認加速行流程 ---
    seed2 = pg.evaluate(SEED_JS, "soft")
    assert seed2.get("ok")
    op2 = open_sheet_and_back_to_map(pg)
    st_b = wait_dayend_modal(pg)
    day0b = pg.evaluate("() => S.dayIndex")
    ok2 = modal_click(pg, accel_label)
    pg.wait_for_timeout(900)
    reached2 = click_through_to_confirm(pg)
    st3 = pg.evaluate(STATE_JS)
    print(f"  accel again -> {ok2}; confirm2 reached={reached2} title={st3['title']!r} btns={st3['modalBtns']}", flush=True)
    confirm = modal_click(pg, "確認加速")
    pg.wait_for_timeout(1200)
    out = chain_to_map(pg)
    day_after = pg.evaluate("() => S.dayIndex")
    print(f"  confirm -> {confirm}; outcome={out['reached']} day {day0b}->{day_after}", flush=True)
    settled = settle_to_map(pg)
    print(f"  settle_to_map={settled}", flush=True)
    res = {"key": key, "vp": vp, "modal": m, "accel_label": accel_label,
           "confirm_reached": bool(reached_confirm),
           "confirm_title": st1["title"], "confirm_btns": st1["modalBtns"],
           "cancel_ok": cancel_ok, "cancel_mask": st2["maskOn"], "cancel_map": st2["mapVisible"],
           "cancel_day": st2["dayIndex"],
           "confirm2_reached": bool(reached2),
           "confirm_click": bool(confirm), "outcome": out["reached"], "chain": out["log"],
           "day_before": day0, "day_after": day_after, "settled": settled}
    REPORT["runs"][key] = res
    return res


def run_rest_case(pg, vp):
    """休息卡：今日 rest → 地圖 #map-start-today → rest 日結板 → 撳返回地圖。"""
    key = f"rest-soft-map-{vp}"
    if ARGS.only and ARGS.only not in key:
        return None
    pg.set_viewport_size({"width": 390, "height": vp})
    pg.wait_for_timeout(400)
    seed = pg.evaluate(SEED_REST_JS)
    assert seed.get("ok"), f"rest seed failed {seed}"
    print(f"== {key} == seed={seed}", flush=True)
    day_before = pg.evaluate("() => S.dayIndex")
    op = open_sheet_and_back_to_map(pg)
    pg.wait_for_timeout(800)
    if pg.evaluate("() => !!document.querySelector('.story-play .dlg106-plate')"):
        play_through_story(pg)
        pg.wait_for_timeout(800)
        settle_to_map(pg)
    st = pg.evaluate(STATE_JS)
    print(f"  after sheet-back: map={st['mapVisible']} mask={st['maskOn']} title={st['title']!r}", flush=True)
    # 地圖 #map-start-today 應該出現（今日 rest 係 soft 行程）
    started = pg.evaluate("""() => { const b=document.getElementById('map-start-today');
      if (!b || b.offsetParent===null) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1200)
    st2 = wait_dayend_modal(pg)
    m = pg.evaluate(MEASURE_JS)
    m["scrollTest"] = pg.evaluate(SCROLL_JS)
    pg.evaluate("() => { const mi=document.querySelector('#modal-inner'); if(mi) mi.scrollTop=0; }")
    print(f"  start-today -> {started}; rest modal title={st2['title']!r} btns={st2['modalBtns']}", flush=True)
    pg.screenshot(path=os.path.join(SHOTS, f"{key}_modal.png"))
    clicked = modal_click(pg, "返回地圖")
    pg.wait_for_timeout(800)
    out = chain_to_map(pg)
    day_after = pg.evaluate("() => S.dayIndex")
    print(f"  click 返回地圖 -> {clicked}; outcome={out['reached']} day {day_before}->{day_after}", flush=True)
    settled = settle_to_map(pg)
    print(f"  settle_to_map={settled}", flush=True)
    res = {"key": key, "vp": vp, "modal": m, "started": bool(started),
           "clicked": bool(clicked), "outcome": out["reached"], "chain": out["log"],
           "day_before": day_before, "day_after": day_after, "settled": settled}
    REPORT["runs"][key] = res
    return res


def dump_report():
    with open(os.path.join(HERE, f"drive189_report_{ARGS.mode}.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=1)


def main():
    from playwright.sync_api import sync_playwright
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 390, "height": 932})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
            pg.on("requestfailed", lambda r: REPORT["http_fail"].append(r.url))
            REPORT["errors"] = errs
            assert new_game(pg), "new game failed"
            ensure_on_map(pg)
            # warmup：唔播種，淨開一次 sheet（C1 會喺第一次入地點嗰陣彈，播完佢），之後各 case 唔再受阻
            op = open_sheet_and_back_to_map(pg)
            print("warmup open:", op, flush=True)
            settle_to_map(pg)
            print("warmup done, day:", pg.evaluate("() => S.dayIndex"), flush=True)
            for vp in (932, 700):
                for fn_call in [
                    lambda: run_wrap_case(pg, vp, "soft", "返回地圖", "wrap"),
                    lambda: run_wrap_case(pg, vp, "soft", "開始今日行程", "wrap"),
                    lambda: run_wrap_case(pg, vp, "map", "返回地圖", "wrap"),
                    lambda: run_wrap_case(pg, vp, "forced", "開始今日行程", "wrap"),
                    lambda: run_accel_case(pg, vp),
                    lambda: run_rest_case(pg, vp),
                ]:
                    try:
                        fn_call()
                    except Exception as e:
                        print(f"  !! case crashed: {e}", flush=True)
                        REPORT["runs"][f"crashed-{vp}-{len(REPORT['runs'])}"] = {"error": str(e)}
                    dump_report()
            br.close()
    finally:
        stop(srv)
    dump_report()
    # 摘要
    print("\n===== SUMMARY =====")
    for k, r in REPORT["runs"].items():
        m = r.get("modal") or {}
        inner = m.get("inner") or {}
        print(f"{k}: outcome={r.get('outcome')} btns={[b['t'] for b in m.get('btns',[])]} "
              f"rows={m.get('btnRows')} scroll={inner.get('scrollH')}/{inner.get('clientH')} "
              f"greenCut={m.get('greenCutN')} anyCut={m.get('anyCutN')} "
              f"day={r.get('day_before')}->{r.get('day_after')} settled={r.get('settled')}")
    print("pageerrors:", REPORT["errors"])
    print("http_fail:", REPORT["http_fail"])


if __name__ == "__main__":
    main()
