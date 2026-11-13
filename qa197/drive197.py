# -*- coding: utf-8 -*-
"""v20a197 BUTTONS197 實駕：B1–B7／C1–C7／D1＋U1–U6 逐項重驗（932／700＋頒獎禮 soft）。
對象：~/workspace/linji-work197 index.html（本地 serve，LIVE 模式；頒獎禮例外用 soft）。
用法：/home/hatch/pwenv49/bin/python qa197/drive197.py [932|700|awards|all]
量度一律以 DOM rect 為準（headless_shell 截圖有 stale frame 殘影，只做目視對照）。
"""
import hashlib, json, os, signal, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work197"
OUT = "/home/hatch/workspace/linji-work197/qa197"
SHOTS = os.path.join(OUT, "shots")
PORT = 18997
URL = f"http://127.0.0.1:{PORT}/index.html"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
os.makedirs(SHOTS, exist_ok=True)
R = {"viewport_runs": {}, "awards": {}, "errors": [], "pageerrors": []}

CENSUS_JS = """() => {
  const vw = window.innerWidth, vh = window.innerHeight;
  const out = [];
  const els = [...document.querySelectorAll('button, .sp-choice, input[type="button"], [role="button"]')];
  for (const b of els) {
    const r = b.getBoundingClientRect();
    const cs = getComputedStyle(b);
    if (r.width <= 0 || r.height <= 0) continue;
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const cx = Math.min(Math.max(r.left + r.width/2, 0), vw-1), cy = Math.min(Math.max(r.top + r.height/2, 0), vh-1);
    let hit = null; try { hit = document.elementFromPoint(cx, cy); } catch(e) {}
    const covered = !(hit === b || (hit && b.contains(hit)));
    out.push({text:(b.textContent||'').trim().replace(/\\s+/g,' ').slice(0,44),
      id: b.id||'', cls:(b.className||'').toString().replace(/\\s+/g,' ').slice(0,60),
      x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height),
      inVP: r.left>=-1 && r.top>=-1 && r.right<=vw+1 && r.bottom<=vh+1,
      covered, hit: covered && hit ? (hit.tagName+'#'+(hit.id||'')+'.'+(hit.className||'').toString().slice(0,30)) : '',
      disabled: !!b.disabled, tag: b.tagName});
  }
  return {vw, vh, buttons: out};
}"""

STATE_JS = """() => ({
  maskOn: document.getElementById('mask') ? document.getElementById('mask').classList.contains('on') : false,
  dayIndex: (typeof S!=='undefined' && S) ? S.dayIndex : null,
  mapVisible: (()=>{ const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : false; })(),
  title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h ? (h.textContent||'').trim() : null; })(),
  modalBtns: [...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim()),
  story: !!document.querySelector('.story-play .dlg106-plate'),
  choices: [...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null).length,
  enc: !!document.getElementById('enc79-overlay'),
  locSheet: !!document.getElementById('loc-sheet') && document.getElementById('loc-sheet').offsetParent!==null,
  locTitle: (()=>{ const t=document.getElementById('loc-title'); return t ? (t.textContent||'').trim() : ''; })(),
  menuOpen: (()=>{ const m=document.getElementById('menu'); return m ? m.offsetParent!==null && getComputedStyle(m).display!=='none' : false; })()
})"""

def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    assert hashlib.sha256(body).hexdigest() == hashlib.sha256(open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest()
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def snap(pg, name):
    try:
        pg.screenshot(path=os.path.join(SHOTS, name)); return True
    except Exception as e:
        R["errors"].append(f"snap {name}: {e}"); return False

def census(pg, tag):
    c = pg.evaluate(CENSUS_JS)
    c["tag"] = tag
    return c

def rect_of(pg, js):
    return pg.evaluate(js)

def click_text(pg, text, scope=None, exact=False, wait=900):
    ok = pg.evaluate("""(a) => {
      const root = a.scope ? document.querySelector(a.scope) : document;
      if (!root) return false;
      const bs = [...root.querySelectorAll('button')].filter(b => b.offsetParent !== null && !b.disabled);
      const m = bs.find(b => a.exact ? (b.textContent||'').trim() === a.t : (b.textContent||'').includes(a.t));
      if (!m) return false; m.click(); return true; }""",
      {"t": text, "scope": scope, "exact": exact})
    if ok: pg.wait_for_timeout(wait)
    return ok

def click_first(pg, texts, wait=1000):
    for t in texts:
        if click_text(pg, t, wait=wait):
            return t
    return None

def wait_for_S(pg, timeout=15000):
    t0 = time.time()
    while time.time() - t0 < timeout / 1000:
        if pg.evaluate("() => (typeof S !== 'undefined' && S !== null)"):
            return True
        pg.wait_for_timeout(400)
    return False

def dismiss_enc3(pg, max_rounds=40):
    for _ in range(max_rounds):
        st = pg.evaluate(STATE_JS)
        if not st["enc"] and not st["story"]:
            if st["maskOn"] and "關閉" in st["modalBtns"]:
                # 劇情結算 modal（C1 完結嗰陣出）：閂佢返地圖
                click_text(pg, "關閉", scope="#modal-btns", wait=900)
                continue
            has_leave = pg.evaluate("""() => [...document.querySelectorAll('#modal-btns button')]
              .some(b => b.offsetParent!==null && /行開/.test(b.textContent||''))""")
            if has_leave and st["maskOn"]:
                click_text(pg, "行開", scope="#modal-btns", wait=900)
                continue
            return True
        if st["story"]:
            play_story(pg, max_steps=40, tag_prefix="dlg_enc3")
            continue
        r = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay'); if (!ov) return 'no-ov';
          const sk = ov.querySelector('.e79-skip');
          if (sk && sk.offsetParent !== null) { sk.click(); return 'skip'; }
          const plain = [...ov.querySelectorAll('.e79-btn:not(.e79-choice)')].find(x => x.offsetParent !== null);
          if (plain) { plain.click(); return 'next:'+(plain.textContent||'').trim().slice(0,16); }
          const ch = [...ov.querySelectorAll('.e79-btn.e79-choice')].find(x => x.offsetParent !== null);
          if (ch) { ch.click(); return 'choice:'+(ch.textContent||'').trim().slice(0,16); }
          return 'none'; }""")
        pg.wait_for_timeout(700)
        if r == 'none' or r == 'no-ov':
            return pg.evaluate("() => !document.getElementById('enc79-overlay')")
    st = pg.evaluate(STATE_JS)
    return (not st["enc"]) and (not st["story"])

def play_story(pg, max_steps=60, tag_prefix="dlg"):
    """播完當前故事；回傳每步嘅 modal-btns／choice 掣位。"""
    steps = []
    for i in range(max_steps):
        st = pg.evaluate(STATE_JS)
        if not st["story"] and st["choices"] == 0:
            return steps
        if st["choices"]:
            c = census(pg, f"{tag_prefix}_choice_{i}")
            steps.append({"step": i, "kind": "choice", "census": c})
            pg.evaluate("""() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
              if (c[0]) c[0].click(); }""")
            pg.wait_for_timeout(1200); continue
        c = census(pg, f"{tag_prefix}_line_{i}")
        steps.append({"step": i, "kind": "line", "census": c})
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            return steps
        pg.wait_for_timeout(900)
    return steps

def new_game(pg, confirm_plan=True):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_text(pg, "新遊戲", wait=1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) b.click(); }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_text(pg, "跳過教學", wait=1200)
    click_text(pg, "開始寫手帳", wait=1400)
    if confirm_plan:
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception:
            pass
        click_text(pg, "確定出發", wait=1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

def ensure_on_map(pg):
    for _ in range(8):
        st = pg.evaluate(STATE_JS)
        if st["mapVisible"] and not st["maskOn"]:
            return True
        if st["enc"]:
            dismiss_enc3(pg); continue
        if st["story"]:
            play_story(pg); continue
        if st["maskOn"]:
            # 劇情結算 modal／其他 modal：先經 dismiss 閂咗佢
            if dismiss_enc3(pg):
                continue
            return False
        if click_text(pg, "返回地圖", wait=1000):
            continue
        pg.wait_for_timeout(500)
    return pg.evaluate("() => { const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : false; }")

def finish_intro(pg):
    """開局後：播完 C1 主線＋閂「劇情結算」modal，直至返到乾淨地圖。回傳 (ok, steps)。"""
    steps = []
    for _ in range(6):
        st = pg.evaluate(STATE_JS)
        if st["mapVisible"] and not st["maskOn"]:
            return True, steps
        if st["story"] or st["choices"]:
            steps += play_story(pg, max_steps=60, tag_prefix="dlg_intro")
            continue
        dismiss_enc3(pg)
        pg.wait_for_timeout(500)
    st = pg.evaluate(STATE_JS)
    return (st["mapVisible"] and not st["maskOn"]), steps

def open_loc(pg, name, wait=1200):
    dismiss_enc3(pg)
    ok = click_text(pg, name, scope="#v-map", wait=wait)
    if not ok:
        return False
    pg.wait_for_timeout(400)
    st = pg.evaluate(STATE_JS)
    if st["story"]:
        return "story"
    return st["locSheet"]

def close_loc(pg):
    return click_text(pg, "返回地圖", scope="#loc-sheet", wait=1000)

def open_journal(pg):
    pg.evaluate("() => { const m=document.getElementById('btn-menu'); if(m) m.click(); }")
    pg.wait_for_timeout(800)
    click_text(pg, "手帳", wait=1200)
    pg.wait_for_timeout(700)

SEED_DAYEND_JS = """(branch) => {
  try {
    const wd = (d)=>((d%7)+7)%7;
    while (wd(S.dayIndex) === 6) S.dayIndex += 1;
    const today = S.dayIndex, twd = wd(today), nwd = wd(today+1);
    S.stress = 10; S.homeEditable = false;
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
    while (wd(S.dayIndex) !== 0) S.dayIndex += 1;
    S.stress = 10; S.homeEditable = false;
    if (S.conseq61) { S.conseq61.sick = null; S.conseq61.streak90 = 0; S.conseq61.streak80 = 0; S.conseq61.cooldownUntil = 0; S.conseq61.pendingEnding = null; }
    const today = S.dayIndex, twd = wd(today), nwd = wd(today+1);
    S.weekPlan = S.weekPlan || [];
    for(let i=0;i<7;i++) S.weekPlan[i]='rest';
    S.weekPlan[twd]='rest'; S.weekPlan[nwd]='street';
    try{ saveQ(); }catch(e){}
    return {ok:true, dayIndex:S.dayIndex, todayPlan:S.weekPlan[twd], tomPlan:S.weekPlan[nwd]};
  } catch(e){ return {ok:false, err:String(e)}; }
}"""

def rect(pg, sel):
    return pg.evaluate("""(s) => { const el = document.querySelector(s);
      if (!el) return {found:false};
      const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
      return {found:true, tag: el.tagName, id: el.id||'', cls: (el.className||'').toString().slice(0,80),
        x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height),
        bottom: Math.round(r.bottom), right: Math.round(r.right),
        visible: el.offsetParent!==null, disabled: !!el.disabled,
        bg: cs.backgroundColor, color: cs.color, fontSize: cs.fontSize,
        text: (el.textContent||'').trim().slice(0,40)}; }""", sel)

def modal_btns(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('#modal-btns button')]
      .filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
        return {text:(b.textContent||'').trim(), cls:(b.className||'').toString(), role:b.className,
          x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; })""")

def run_viewport(pw, H, label):
    print(f"===== VIEWPORT 430x{H} ({label}) =====", flush=True)
    rec = {"height": H, "screens": {}, "probes": {}, "notes": []}
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        # ---- B2/D1 未確認態：新遊戲，停喺寫手帳之前唔撳確認 ----
        if not new_game(pg, confirm_plan=False):
            rec["notes"].append("new_game FAILED"); R["viewport_runs"][label] = rec; return rec
        pg.wait_for_timeout(600)
        rec["probes"]["b2_unconfirmed"] = {
            "confirm": rect(pg, "#btn-confirm-plan"),
            "reset": rect(pg, "#btn-reset-plan"),
            "bar": rect(pg, "#nb-actions"),
            "quick_visible": pg.evaluate("() => { const q=document.getElementById('nb-quick'); return q ? q.offsetParent!==null : null; }"),
        }
        # B7 初 paint：分類掣＋bar＋notebook scrollTop（未碌過）
        rec["probes"]["b7_first_paint"] = pg.evaluate("""() => {
          const nb = document.getElementById('notebook');
          const tabs = document.getElementById('cat-tabs');
          const bar = document.getElementById('nb-actions');
          if (!nb || !tabs || !bar) return {found:false};
          const bs = [...tabs.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>{ const r=x.getBoundingClientRect();
            return {t:(x.textContent||'').trim(), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), bottom:Math.round(r.bottom)}; });
          const br = bar.getBoundingClientRect();
          return {scrollTop: nb.scrollTop, scrollHeight: nb.scrollHeight, clientHeight: nb.clientHeight,
            barTop: Math.round(br.top), barH: Math.round(br.height),
            catTop: Math.round(tabs.getBoundingClientRect().top), catBottom: Math.round(tabs.getBoundingClientRect().bottom),
            buttons: bs}; }""")
        snap(pg, f"{label}_b2_unconfirmed.png")
        # C1：主分頁切頁唔郁
        rec["probes"]["c1_tabs"] = pg.evaluate("""() => {
          const out = {};
          const tabs = [...document.querySelectorAll('#home-tabs .home-tab')];
          for (const t of tabs) {
            t.click();
            const on = document.querySelector('#home-tabs .home-tab.on');
            const r = on ? on.getBoundingClientRect() : null;
            out[(t.textContent||'').trim()] = r ? {x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)} : null;
          }
          return out; }""")
        pg.wait_for_timeout(500)
        # 返去行程頁
        click_text(pg, "行程", scope="#home-tabs", wait=900)
        # C7：sub-tab 名
        rec["probes"]["c7_subtab"] = pg.evaluate("""() => { const b=document.getElementById('htab-plan');
          return b ? (b.textContent||'').trim() : null; }""")
        # B7 撳到：分類掣中心點 elementFromPoint 係咪掣本身
        rec["probes"]["b7_clickable"] = pg.evaluate("""() => {
          const tabs = document.getElementById('cat-tabs');
          if (!tabs) return {found:false};
          return [...tabs.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>{
            const r=x.getBoundingClientRect(); const cx=r.left+r.width/2, cy=r.top+r.height/2;
            const hit=document.elementFromPoint(cx, cy);
            return {t:(x.textContent||'').trim(), hit: hit===x, hitTag: hit?hit.tagName+'#'+(hit.id||''):null}; }); }""")
        # U6（可編輯態）：逐日「⧉ 複製」vs 快捷列「複製到…」係咪開同一個 panel
        rec["probes"]["u6_copy"] = pg.evaluate("""() => {
          const panel = () => { const w=document.getElementById('nb-copy-wrap');
            return w ? {open: w.classList.contains('open'), display: getComputedStyle(w).display} : null; };
          const before = panel();
          const cp = document.querySelector('.day-row .cp');
          let rowBtn = null, selDayBefore = (typeof planSelDay!=='undefined') ? planSelDay : null;
          if (cp) { rowBtn = (cp.textContent||'').trim(); cp.click(); }
          const afterRow = panel();
          const selDayAfterRow = (typeof planSelDay!=='undefined') ? planSelDay : null;
          const q = document.getElementById('nb-q-copy');
          return {before, rowBtn, selDayBefore, selDayAfterRow, afterRow,
            quickBtn: q ? (q.textContent||'').trim() : null}; }""")
        pg.wait_for_timeout(600)
        # 閂 panel 再經快捷列開（同一 panel、source 日＝當前選中日）
        pg.evaluate("""() => { const q=document.getElementById('nb-q-copy'); if (q) q.click(); }""")
        pg.wait_for_timeout(600)
        rec["probes"]["u6_copy"]["afterQuick"] = pg.evaluate("""() => { const w=document.getElementById('nb-copy-wrap');
          return w ? {open: w.classList.contains('open'), display: getComputedStyle(w).display} : null; }""")
        rec["probes"]["u6_copy"]["selDayAfterQuick"] = pg.evaluate("() => (typeof planSelDay!=='undefined') ? planSelDay : null")
        # 閂返 panel，唔好影響之後嘅確認流程
        pg.evaluate("() => { try { toggleCopyPanel(false); } catch(e){} return true; }")
        pg.wait_for_timeout(400)
        # B2/D1：撳確認 → 鎖定印章
        click_text(pg, "確定本週行程", scope="#nb-actions", wait=1200)
        pg.wait_for_timeout(900)
        rec["probes"]["b2_locked"] = {
            "confirm": rect(pg, "#btn-confirm-plan"),
            "reset": rect(pg, "#btn-reset-plan"),
            "bar": rect(pg, "#nb-actions"),
            "quick_visible": pg.evaluate("() => { const q=document.getElementById('nb-quick'); return q ? q.offsetParent!==null : null; }"),
            "stamp_click_noop": pg.evaluate("""() => { const el=document.getElementById('btn-confirm-plan');
              if (!el) return {found:false};
              const before = document.getElementById('mask') ? document.getElementById('mask').classList.contains('on') : false;
              el.click();
              return {tag: el.tagName, maskBefore: before,
                maskAfter: document.getElementById('mask') ? document.getElementById('mask').classList.contains('on') : false}; }"""),
        }
        snap(pg, f"{label}_b2_locked.png")
        # B2 沉澱態：出返手帳再入過（renderNotebook 重跑），量 reset disabled＋quick 隱藏＋印章未旋轉幾何
        click_text(pg, "返回地圖", scope="#home-tab-exit", wait=1000)
        pg.wait_for_timeout(600)
        open_journal(pg)
        pg.wait_for_timeout(700)
        rec["probes"]["b2_locked_settled"] = pg.evaluate("""() => {
          const conf = document.getElementById('btn-confirm-plan');
          const reset = document.getElementById('btn-reset-plan');
          const q = document.getElementById('nb-quick');
          const bar = document.getElementById('nb-actions');
          const box = (el) => el ? {offsetW: el.offsetWidth, offsetH: el.offsetHeight,
            offsetL: el.offsetLeft, offsetT: el.offsetTop} : null;
          return {
            confirmTag: conf ? conf.tagName : null, confirmText: conf ? (conf.textContent||'').trim() : null,
            confirmBox: box(conf),
            confirmBg: conf ? getComputedStyle(conf).backgroundColor : null,
            resetDisabled: reset ? reset.disabled : null,
            resetDisplay: reset ? getComputedStyle(reset).display : null,
            resetOpacity: reset ? getComputedStyle(reset).opacity : null,
            quickDisplay: q ? getComputedStyle(q).display : null,
            quickInline: q ? q.style.display : null,
            barH: bar ? bar.offsetHeight : null,
            homeEditable: (typeof S!=='undefined' && S) ? S.homeEditable : null}; }""")
        # D1 印章 noop：撳印章前後 S.homeEditable／手帳狀態唔變、唔彈 modal
        rec["probes"]["b2_stamp_noop"] = pg.evaluate("""() => {
          const conf = document.getElementById('btn-confirm-plan');
          const before = {editable: S.homeEditable,
            maskOn: document.getElementById('mask').classList.contains('on'),
            journalOpen: !!document.querySelector('#home-pane-plan') && document.querySelector('#home-pane-plan').offsetParent!==null};
          if (conf) conf.click();
          const after = {editable: S.homeEditable,
            maskOn: document.getElementById('mask').classList.contains('on'),
            journalOpen: !!document.querySelector('#home-pane-plan') && document.querySelector('#home-pane-plan').offsetParent!==null};
          return {tag: conf ? conf.tagName : null, before, after, noop: JSON.stringify(before)===JSON.stringify(after)}; }""")
        # 完成開局 → 地圖（C1 主線＋結算 modal 一併處理）
        click_text(pg, "確定出發", wait=1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        rec["probes"]["intro_finished"], intro_steps = finish_intro(pg)
        # B1 主線「下一句」：由 intro 逐句 census 抽出
        rec["probes"]["b1_mainline"] = [
            {"step": s["step"], "kind": s["kind"],
             "next": [x for x in s["census"]["buttons"] if "下一句" in x["text"]][:2],
             "choices": [x for x in s["census"]["buttons"] if x["cls"].find("sp-choice") >= 0][:3]}
            for s in intro_steps[:8]]
        snap(pg, f"{label}_b1_mainline.png")
        dismiss_enc3(pg)
        ensure_on_map(pg)
        dismiss_enc3(pg)
        pg.wait_for_timeout(600)
        # ---- C2＋B6 乾淨地圖 ----
        rec["probes"]["map_clean"] = {
            "start_today": rect(pg, "#map-start-today"),
            "end_day": rect(pg, "#map-end-day"),
            "hint": rect(pg, "#map-hint"),
            "appScrollTop": pg.evaluate("() => document.getElementById('app').scrollTop"),
            "wrapScrollTop": pg.evaluate("() => { const w=document.querySelector('.map-wrap'); return w ? w.scrollTop : null; }"),
        }
        snap(pg, f"{label}_map_clean.png")
        # ---- B6＋B5＋C3：開茶餐廳 sheet ----
        r = open_loc(pg, "茶餐廳")
        rec["notes"].append(f"open 茶餐廳 -> {r}")
        pg.wait_for_timeout(700)
        st = pg.evaluate(STATE_JS)
        if st["story"]:
            play_story(pg, max_steps=30, tag_prefix="dlg_tea")
            dismiss_enc3(pg); ensure_on_map(pg)
            r = open_loc(pg, "茶餐廳")
            pg.wait_for_timeout(700)
        rec["probes"]["b6_sheet_open"] = {
            "start_today": rect(pg, "#map-start-today"),
            "end_day": rect(pg, "#map-end-day"),
            "hint": rect(pg, "#map-hint"),
            "appScrollTop": pg.evaluate("() => document.getElementById('app').scrollTop"),
            "wrapScrollTop": pg.evaluate("() => { const w=document.querySelector('.map-wrap'); return w ? w.scrollTop : null; }"),
            "sheet": rect(pg, "#loc-sheet"),
        }
        rec["probes"]["b5_loc_close"] = pg.evaluate("""() => { const b=document.getElementById('loc-close');
          if (!b) return {found:false};
          const r=b.getBoundingClientRect();
          return {tag:b.tagName, offsetW:b.offsetWidth, offsetH:b.offsetHeight,
            bbox:{x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)},
            text:(b.textContent||'').trim()}; }""")
        rec["probes"]["c3_acts"] = pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet .act')]
          .filter(b=>b.offsetParent!==null).map(b=>{ const r=b.getBoundingClientRect();
            return {t:(b.textContent||'').trim().slice(0,20), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}; })""")
        snap(pg, f"{label}_loc_tearoom.png")
        close_loc(pg)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- B1 巧遇：逐個地點試，直至 enc79 彈出 ----
        enc = None
        for loc in ["茶餐廳", "星河電視台", "廟街", "清水灣片場", "啟德機場", "中環", "尖沙咀", "旺角", "銅鑼灣", "油麻地"]:
            r = open_loc(pg, loc)
            pg.wait_for_timeout(600)
            st = pg.evaluate(STATE_JS)
            if st["enc"]:
                enc = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                  if (!ov) return null;
                  const nb=[...ov.querySelectorAll('.e79-btn:not(.e79-choice)')].find(x=>x.offsetParent!==null);
                  const r=nb?nb.getBoundingClientRect():null;
                  const line=(ov.querySelector('.e79-line')||{}).textContent||'';
                  return {nb: r?{x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), text:(nb.textContent||'').trim()} : null,
                    line: line.slice(0,30)}; }""")
                snap(pg, f"{label}_b1_enc.png")
                # 撳一次「下一句」，驗證對白有推進
                before = enc["line"] if enc else ""
                pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                  const nb=[...ov.querySelectorAll('.e79-btn:not(.e79-choice)')].find(x=>x.offsetParent!==null);
                  if (nb) nb.click(); }""")
                pg.wait_for_timeout(900)
                after = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                  return ov ? ((ov.querySelector('.e79-line')||{}).textContent||'').slice(0,30) : 'CLOSED'; }""")
                enc["advance"] = {"before": before, "after": after, "advanced": before != after}
                break
            if st["story"]:
                play_story(pg, max_steps=30, tag_prefix="dlg_encloc")
            if st["locSheet"]:
                close_loc(pg)
            dismiss_enc3(pg)
            ensure_on_map(pg)
        rec["probes"]["b1_encounter"] = enc
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- C6＋U2：通告板（星河電視台 sheet → 通告欄） ----
        open_loc(pg, "星河電視台")
        pg.wait_for_timeout(700)
        dismiss_enc3(pg)
        pg.wait_for_timeout(500)
        if click_text(pg, "通告欄", scope="#loc-acts", wait=1500):
            pg.wait_for_timeout(900)
            rec["probes"]["c6_board"] = pg.evaluate("""() => {
              const cards=[...document.querySelectorAll('#modal-inner .gig-teaser, #modal-inner .gig-card')].filter(e=>e.offsetParent!==null)
                .map(e=>{ const r=e.getBoundingClientRect(); return {y:Math.round(r.top), bottom:Math.round(r.bottom), h:Math.round(r.height)}; });
              const det=document.querySelector('#modal-inner details.gig-locked108');
              const sum=det?det.querySelector('summary'):null;
              const sr=sum?sum.getBoundingClientRect():null;
              const scs=sum?getComputedStyle(sum):null;
              return {cards, n: cards.length,
                gaps: cards.slice(1).map((c,i)=>Math.round(c.y-cards[i].bottom)),
                summary: sr?{x:Math.round(sr.left), y:Math.round(sr.top), w:Math.round(sr.width), h:Math.round(sr.height),
                  bg: scs.backgroundColor, text:(sum.textContent||'').trim().slice(0,40)} : null}; }""")
            snap(pg, f"{label}_c6_board.png")
            # U2：開第一張可接通告詳情
            opened = pg.evaluate("""() => {
              const cards = [...document.querySelectorAll('#modal-inner button')].filter(b=>b.offsetParent!==null && (b.textContent||'').includes('可接通告'));
              if (!cards.length) return null;
              cards[0].click(); return (cards[0].textContent||'').trim().slice(0,30); }""")
            pg.wait_for_timeout(1200)
            rec["probes"]["u2_detail"] = {"opened": opened, "census": census(pg, "casting_detail")}
            snap(pg, f"{label}_u2_detail.png")
            click_first(pg, ["返回", "關閉"], 900)
            pg.wait_for_timeout(800)
            click_first(pg, ["返去地點", "返回地圖"], 900)
            pg.wait_for_timeout(800)
        close_loc(pg)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- B5 手帳吊牌（未旋轉幾何：父層 rotate(2.5°) 會膨脹 bbox） ----
        open_journal(pg)
        rec["probes"]["b5_home_back"] = pg.evaluate("""() => { const b=document.getElementById('home-back-map-tabs');
          if (!b) return {found:false};
          const r=b.getBoundingClientRect();
          return {tag:b.tagName, offsetW:b.offsetWidth, offsetH:b.offsetHeight,
            bbox:{x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)},
            bg:getComputedStyle(b).backgroundColor, text:(b.textContent||'').trim()}; }""")
        click_first(pg, ["返回地圖"], 900)
        pg.wait_for_timeout(800)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- U4：額度用完嗰陣 TVB 入口 ----
        pg.evaluate("""() => { try { S.travel114 = S.travel114 || {}; S.travel114.used = 2; S.travel114.day = S.dayIndex; saveQ(); } catch(e){} return true; }""")
        pg.wait_for_timeout(400)
        before_sheet = pg.evaluate(STATE_JS)
        open_loc(pg, "星河電視台")
        pg.wait_for_timeout(800)
        after = pg.evaluate(STATE_JS)
        rec["probes"]["u4_quota"] = {"before": before_sheet, "after": after,
            "sheet_opened": after["locSheet"], "locTitle": after["locTitle"]}
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- U6 鎖定態對照：逐日複製掣應該唔見（只喺可編輯態生成） ----
        open_journal(pg)
        rec["probes"]["u6_copy_locked"] = pg.evaluate("""() => ({
          cpCount: document.querySelectorAll('.day-row .cp').length,
          quickDisplay: (()=>{ const q=document.getElementById('nb-quick'); return q ? getComputedStyle(q).display : null; })(),
          homeEditable: (typeof S!=='undefined' && S) ? S.homeEditable : null})""")
        click_first(pg, ["返回地圖"], 900)
        pg.wait_for_timeout(800)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- B4＋U1：soft 日結板 ----
        pg.evaluate(SEED_DAYEND_JS, "soft")
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        open_loc(pg, "茶餐廳")
        pg.wait_for_timeout(600)
        st = pg.evaluate(STATE_JS)
        if st["story"]:
            play_story(pg, max_steps=30, tag_prefix="dlg_dayend")
        close_loc(pg)
        pg.wait_for_timeout(1200)
        rec["probes"]["b4_soft"] = {"modal": rect(pg, "#mask .modal"), "btns": modal_btns(pg),
            "title": pg.evaluate(STATE_JS)["title"]}
        snap(pg, f"{label}_b4_soft.png")
        if click_text(pg, "返回地圖", scope="#modal-btns", wait=1200):
            pg.wait_for_timeout(900)
            rec["probes"]["b4_soft_after_back"] = pg.evaluate(STATE_JS)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- B4＋U1：rest 日結板 ----
        pg.evaluate(SEED_REST_JS)
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        if click_text(pg, "開始今日行程", scope="#v-map", wait=1200):
            pg.wait_for_timeout(1200)
            rec["probes"]["b4_rest"] = {"modal": rect(pg, "#mask .modal"), "btns": modal_btns(pg),
                "title": pg.evaluate(STATE_JS)["title"]}
            snap(pg, f"{label}_b4_rest.png")
            ok = click_text(pg, "返回地圖", scope="#modal-btns", wait=1500)
            pg.wait_for_timeout(1200)
            rec["probes"]["u1_rest_back"] = {"clicked": ok, "state": pg.evaluate(STATE_JS)}
        dismiss_enc3(pg)
        ensure_on_map(pg)
        # ---- C4＋C2：過一日確認 modal（自由日）＋過一日掣紙色 ----
        pg.evaluate("""() => { try { S.weekPlan = S.weekPlan || []; for(let i=0;i<7;i++) S.weekPlan[i]='rest'; S.homeEditable=false; saveQ(); } catch(e){} return true; }""")
        pg.reload(); pg.wait_for_timeout(2500); wait_for_S(pg)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        rec["probes"]["c2_end_day"] = {"end_day": rect(pg, "#map-end-day"), "start_today": rect(pg, "#map-start-today")}
        if click_text(pg, "過一日", scope="#v-map", wait=1200):
            pg.wait_for_timeout(900)
            rec["probes"]["c4_overday"] = {"btns": modal_btns(pg), "title": pg.evaluate(STATE_JS)["title"]}
            snap(pg, f"{label}_c4_overday.png")
            click_first(pg, ["取消", "唔好", "返回"], 900)
            pg.wait_for_timeout(700)
        rec["screens"]["map_final"] = census(pg, "map_final")
        snap(pg, f"{label}_final.png")
        rec["pageerrors"] = errs[:10]
        rec["zero_pageerror"] = len(errs) == 0
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
        R["errors"].append(f"{label}: {e!r}")
        try: snap(pg, f"{label}_ERR.png")
        except Exception: pass
    finally:
        ctx.close(); b.close()
    R["viewport_runs"][label] = rec
    print(f"== {label} done, pageerrors={len(errs)} ==", flush=True)
    return rec

def run_awards(pw):
    print("===== AWARDS (soft) =====", flush=True)
    rec = {"screens": {}, "notes": [], "skip_track": [], "invite": None}
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        pg.goto(URL + "?softPreview=1")
        pg.wait_for_timeout(3000)
        if not new_game(pg):
            rec["notes"].append("new_game FAILED"); R["awards"] = rec; return rec
        st = pg.evaluate(STATE_JS)
        if st["story"] or st["choices"]:
            play_story(pg, max_steps=60, tag_prefix="dlg_awd")
        st = pg.evaluate(STATE_JS)
        if st["maskOn"]:
            click_first(pg, ["關閉"], 900); pg.wait_for_timeout(800)
        dismiss_enc3(pg)
        ensure_on_map(pg)
        dismiss_enc3(pg)
        pg.evaluate("""() => {
          try {
            S.dayIndex = 292; S.fame = 45; S.industryCreditDelta = 50; S.stage = 60; S.acting = 60;
            S.awardsFlags = {}; S.pendingAwardPack = null; S.newspaperQueue = []; S.news = S.news || [];
            S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
            const g = (typeof GIGS !== 'undefined' ? GIGS.filter(x=>x && x.type==='電影' && /男主角/.test(String(x.roleLabel||''))) : []);
            const pick = g.slice(0, 2);
            S.wrapHistory = pick.map(x => ({ gigId: x.id, title: x.title||x.id, type: '電影', workTitle: x.workTitle||'',
              roleLabel: x.roleLabel||'', roleScale: x.roleScale||'', year: 1990, totalDays: 2,
              pay: 20000, fame: 0, popularity: 0, wrappedDay: 250, rating: '順利殺青' }));
            S.story = S.story || {}; S.story.done = {}; S.story.flags = S.story.flags || {}; S.story.rel = S.story.rel || {};
            try{ saveQ(); }catch(e){}
            return {picked: pick.map(x=>x.id)}; } catch(e){ return {err:String(e)}; } }""")
        pack = pg.evaluate("""() => {
          try { const p = window.__awards.debugForceSeasonWindow('award_harbour_film', {});
            return p ? {bestOutcome: p.bestOutcome, cats: (p.categories||[]).map(x=>({id:x.id, label:x.label, outcome:x.outcome}))} : {error:'no pack'};
          } catch(e) { return {error: String(e)}; } }""")
        rec["notes"].append("pack=" + json.dumps(pack, ensure_ascii=False))
        pg.evaluate("() => { try { window.__awards.present(); } catch(e){} }")
        pg.wait_for_timeout(1200)
        rec["screens"]["award_invite"] = census(pg, "award_invite")
        # C4：請柬掣 DOM 次序 vs 視覺 y
        rec["invite"] = pg.evaluate("""() => {
          const btns=[...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null)
            .map(b=>{ const r=b.getBoundingClientRect();
              return {text:(b.textContent||'').trim(), cls:(b.className||'').toString(),
                x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height),
                order: getComputedStyle(b).order}; });
          const mask=document.getElementById('mask');
          return {btns, maskCls: mask ? mask.className : null}; }""")
        snap(pg, "awd_01_invite.png")
        if click_text(pg, "出席", wait=1000):
            t0 = time.time()
            while time.time() - t0 < 26:
                s = pg.evaluate("""() => {
                  const st = document.querySelector('.awd62-stage');
                  if (!st) return {stage:false};
                  const cap = st.querySelector('.awd62-caption');
                  const skip = [...document.querySelectorAll('button')].find(b => b.offsetParent!==null && /跳過/.test(b.textContent||''));
                  const r = skip ? skip.getBoundingClientRect() : null;
                  return {stage:true, caption: cap ? cap.textContent : '',
                    skip: r ? {x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height), t:(skip.textContent||'').trim()} : null}; }""")
                rec["skip_track"].append({"t": round((time.time()-t0)*1000), **s})
                if not s.get("stage"):
                    break
                pg.wait_for_timeout(500)
            pg.wait_for_timeout(800)
            rec["screens"]["award_result"] = census(pg, "award_result")
            snap(pg, "awd_02_result.png")
            click_first(pg, ["收下這晚"], 900)
            pg.wait_for_timeout(900)
        rec["pageerrors"] = errs[:10]
        rec["zero_pageerror"] = len(errs) == 0
    except Exception as e:
        rec["notes"].append("EXCEPTION: " + repr(e))
        R["errors"].append(f"awards: {e!r}")
        try: snap(pg, "awd_ERR.png")
        except Exception: pass
    finally:
        ctx.close(); b.close()
    R["awards"] = rec
    print(f"== awards done, skip samples={len(rec['skip_track'])}, pageerrors={len(errs)} ==", flush=True)
    return rec

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    srv = serve()
    try:
        with sync_playwright() as pw:
            if which in ("all", "932"):
                run_viewport(pw, 932, "932")
            if which in ("all", "700"):
                run_viewport(pw, 700, "700")
            if which in ("all", "awards"):
                run_awards(pw)
        with open(os.path.join(OUT, "drive197.json"), "w", encoding="utf-8") as f:
            json.dump(R, f, ensure_ascii=False, indent=1)
        print("== ALL DONE ==", flush=True)
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
