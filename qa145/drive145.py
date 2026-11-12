# -*- coding: utf-8 -*-
"""v20a145 BOOK145 實駕 drive145：B1 短屏鎖定態 7/7＋B2 八組 pane 紙面＋B3 訓練選擇器紙面。
用法：/home/hatch/pwenv49/bin/python qa145/drive145.py
Mirror：工作副本 ~/workspace/linji-work145，port 8966，430x932＋430x700，?softPreview=1。
流程：UI 新遊戲 → 手帳（editable）→ B3 chips 量度＋切換＋掛已報名驗填滿 → B1 編輯功能
（休息／清空／還原）→ B2 四組 subtab 逐個切換＋pane 底色量度 → 確定行程 → locked 量度
B1（clip-aware 七日＋標題／提示列＋印章＋footer）→ 吊牌返地圖。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work145"
HERE = os.path.join(ROOT, "qa145")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8966
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"errors": [], "http404": [], "phases": {}}

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
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
                        el.scroll_into_view_if_needed(timeout=2000)
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

def click_exact(pg, text, wait=1200):
    ok = pg.evaluate("""(t) => {
      const els=[...document.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()===t;});
      if(!els.length) return false; els[0].scrollIntoView({block:'nearest'}); els[0].click(); return true; }""", text)
    pg.wait_for_timeout(wait)
    return ok

def new_game_to_handbook(pg):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    pg.wait_for_timeout(1000)
    on = pg.evaluate("() => { const v=document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")
    print("handbook open (editable):", on, flush=True)
    return on

def open_handbook_via_menu(pg):
    pg.locator("button:has-text('☰')").first.click(timeout=3000); pg.wait_for_timeout(900)
    ok = click_first(pg, ["手帳"], 1400)
    pg.wait_for_timeout(1000)
    on = pg.evaluate("() => { const v=document.getElementById('v-home'); return !!(v && v.classList.contains('on')); }")
    print("handbook open via menu:", ok, on, flush=True)
    return on

JS_MEASURE = """() => {
  const cs = (el, pseudo) => el ? getComputedStyle(el, pseudo || null) : null;
  const rect = el => { if(!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const S = window.S || {};
  let dual = null;
  try { dual = (typeof syncDualTracks === 'function') ? syncDualTracks(S) : null; } catch(_e) {}
  const nbM = document.getElementById('notebook');
  const nbRM = nbM ? nbM.getBoundingClientRect() : null;
  const actRM = document.getElementById('nb-actions').getBoundingClientRect();
  const days = [...document.querySelectorAll('#nb-days .day-row')].map(el => {
    const b = el.getBoundingClientRect();
    return {text: (el.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30),
            top: Math.round(b.top), bottom: Math.round(b.bottom),
            visibleFull: nbRM && b.top >= Math.round(nbRM.top) && b.bottom <= Math.round(actRM.top)}; });
  const conf = document.getElementById('btn-confirm-plan');
  const cc = conf ? cs(conf) : null;
  const chips = [...document.querySelectorAll('#train71-picker .guide68-chip')].map(el => {
    const c = cs(el); return {text: el.textContent.trim(), on: el.classList.contains('on'),
      bg: c.backgroundColor, color: c.color, fontSize: c.fontSize,
      fontFamily: c.fontFamily.slice(0,40), borderRadius: c.borderRadius,
      border: c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor,
      boxShadow: (c.boxShadow||'').slice(0,50)}; });
  const picks = [...document.querySelectorAll('#train71-picker .train71-pick')].map(el => {
    const c = cs(el); return {text: el.textContent.trim(), bg: c.backgroundColor, color: c.color,
      fontSize: c.fontSize, fontFamily: c.fontFamily.slice(0,40), borderRadius: c.borderRadius,
      border: c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor}; });
  const subGroups = [...document.querySelectorAll('.hsub-group')].map(g => {
    const grp = g.getAttribute('data-hsubgroup');
    return {group: grp, on: g.classList.contains('on'), items:
      [...g.querySelectorAll('.home-tab')].map(el => { const c = cs(el); const after = cs(el, '::after');
        return {id: el.id, text: el.textContent.trim(), on: el.classList.contains('on'),
          circle: (after.backgroundImage||'').indexOf('svg') >= 0}; })}; });
  const paneBgs = {};
  for (const p of document.querySelectorAll('.home-pane')) {
    const js = p.querySelector('.journal-scroll, .ledger-wrap');
    paneBgs[p.id] = {on: p.classList.contains('on'),
      bg: js ? getComputedStyle(js).backgroundColor : getComputedStyle(p).backgroundColor};
  }
  const lightText = {};
  for (const sel of ['#home-pane-ledger .ledger-enroll', '#home-pane-people .people-next',
                     '#home-pane-debt .pane-intro', '#home-pane-rumor .pane-intro',
                     '#home-pane-rumor .rumor-hint', '#home-pane-inv .jobs72-h',
                     '#home-pane-people .jobs72-h', '#home-pane-progress .prog71-h',
                     '#home-pane-progress .prog71-intro']) {
    const el = document.querySelector(sel);
    lightText[sel] = el ? {text: (el.textContent||'').trim().slice(0,30), color: cs(el).color,
      bg: cs(el).backgroundColor} : null;
  }
  const title = document.getElementById('nb-plan-title');
  const mode = document.getElementById('nb-plan-mode');
  const range = document.getElementById('nb-range');
  const memo = document.getElementById('home-stats');
  return {
    vh: window.innerHeight, vw: window.innerWidth,
    money: S.money, dual,
    memoText: memo ? memo.textContent.replace(/\\s+/g, ' ').trim() : null,
    tabs: [...document.querySelectorAll('#home-tabs .home-tab')].map(el => {
      const c = cs(el); return {id: el.id, text: el.textContent.trim(), on: el.classList.contains('on'),
        rect: rect(el), bg: c.backgroundColor, height: c.height, width: c.width}; }),
    subGroups, paneBgs, lightText,
    chips, picks,
    trainWrapVisible: (()=>{ const w = document.getElementById('nb-train71-wrap'); return w ? !w.hidden : null; })(),
    zeroNote: (()=>{ const n = document.querySelector('#train71-picker .train73-zero');
      return n ? n.textContent.trim().slice(0,50) : null; })(),
    pickerText: (()=>{ const w = document.getElementById('train71-picker');
      return w ? w.textContent.replace(/\\s+/g,' ').trim().slice(0,220) : null; })(),
    nbActions: {rect: rect(document.getElementById('nb-actions')),
      bg: cs(document.getElementById('nb-actions')).backgroundColor},
    confirm: conf ? {text: conf.textContent.trim(), disabled: conf.disabled, locked: conf.classList.contains('is-locked'),
      rect: rect(conf), color: cc.color, fontSize: cc.fontSize, bg: cc.backgroundColor,
      borderTop: cc.borderTopWidth+' '+cc.borderTopStyle+' '+cc.borderTopColor,
      borderRadius: cc.borderRadius, letterSpacing: cc.letterSpacing, transform: cc.transform} : null,
    reset: (()=>{ const r = document.getElementById('btn-reset-plan');
      return r ? {text: r.textContent.trim(), visible: getComputedStyle(r).display !== 'none' && !!r.offsetParent} : null; })(),
    tag: (()=>{ const t = document.getElementById('home-back-map-tabs'); return t ? {text: t.textContent.trim(), rect: rect(t)} : null; })(),
    b1parts: {
      title: title ? {display: cs(title).display, rect: rect(title)} : null,
      mode: mode ? {display: cs(mode).display, rect: rect(mode), text: (mode.textContent||'').trim().slice(0,30)} : null,
      range: range ? {rect: rect(range), marginBottom: cs(range).marginBottom} : null,
      notebookTop: nbM ? Math.round(nbM.getBoundingClientRect().top) : null,
      nbActionsTop: Math.round(actRM.top), nbActionsH: Math.round(actRM.height)},
    days: {count: days.length, fullVisible: days.filter(d => d.visibleFull).length, rows: days},
    paneOn: (()=>{ const p = document.querySelector('.home-pane.on'); return p ? p.id : null; })(),
    toast: (()=>{ const t = document.querySelector('.toast'); return t ? t.textContent.trim().slice(0,60) : null; })()
  };
}"""

def day_names(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('#nb-days .day-row')].map(el =>
      (el.textContent||'').replace(/\\s+/g,' ').trim().slice(0,40))""")

def run_viewport(pw, width, height, tag):
    ctx = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"]).new_context(
        viewport={"width": width, "height": height}, device_scale_factor=2,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
    http404 = []
    pg.on("response", lambda r: http404.append({ "url": r.url.split("/")[-1][:60], "status": r.status}) if r.status >= 400 else None)
    out = {}
    try:
        assert new_game_to_handbook(pg), "handbook did not open"
        pg.evaluate("() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=0; }")
        pg.wait_for_timeout(300)
        base_days = day_names(pg)
        out["baseDays"] = base_days
        m0 = pg.evaluate(JS_MEASURE)
        out["editable"] = { "memo": m0["memoText"], "tabs": [(t["text"], t["rect"]["w"], t["rect"]["h"], t["on"]) for t in m0["tabs"]] }
        print(f"[{tag}] editable memo={m0['memoText']} tabs={out['editable']['tabs']}", flush=True)

        # ---- B3：開選擇器，量 chips 紙面樣 ----
        assert click_exact(pg, "全日訓練"), "全日訓練撳唔到"
        m = pg.evaluate(JS_MEASURE)
        out["b3_open"] = {"pickerVisible": m["trainWrapVisible"], "chips": m["chips"],
                          "zeroNote": m["zeroNote"], "toast": m["toast"]}
        print(f"[{tag}] B3 open picker={m['trainWrapVisible']} zeroNote={m['zeroNote']}", flush=True)
        for c in m["chips"]:
            print(f"[{tag}]   chip {c['text']:8s} on={c['on']} bg={c['bg']} color={c['color']} fs={c['fontSize']} r={c['borderRadius']} border={c['border']} font={c['fontFamily']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_b3_chips.png"))
        # 切換去 台風 chip：圈（.on）要跟住郁，picker 內容要轉做台風課
        chip_ok = pg.evaluate("""() => { const b=[...document.querySelectorAll('#train71-picker .guide68-chip')]
          .find(e=>e.textContent.includes('台風')); if(!b) return false; b.click(); return true; }""")
        pg.wait_for_timeout(900)
        m2 = pg.evaluate(JS_MEASURE)
        out["b3_switch"] = {"clicked": chip_ok,
            "onChip": [c["text"] for c in m2["chips"] if c["on"]],
            "pickerMentionsStage": ("台風訓練" in (m2["pickerText"] or "")),
            "pickerText": m2["pickerText"]}
        print(f"[{tag}] B3 switch to 台風: {out['b3_switch']}", flush=True)
        # 掛一個已報名（live S）再重開 picker，驗「揀課填滿可改日子」
        enr = pg.evaluate("""() => { try {
          if (typeof S === 'undefined' || !S) return 'no-S';
          S.enrolled = Object.assign({}, S.enrolled || {}, {train_stage: true});
          return JSON.stringify(S.enrolled); } catch(e){ return 'err:'+e; } }""")
        print(f"[{tag}] B3 enroll live S: {enr}", flush=True)
        assert click_exact(pg, "全日訓練"), "全日訓練再撳閂唔到"
        assert click_exact(pg, "全日訓練"), "全日訓練重開唔到"
        m3 = pg.evaluate(JS_MEASURE)
        out["b3_enrolled"] = {"picks": m3["picks"], "pickerText": m3["pickerText"]}
        print(f"[{tag}] B3 enrolled picks={m3['picks']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_b3_enrolled.png"))
        filled = None
        if m3["picks"]:
            pick_ok = pg.evaluate("""() => { const b=document.querySelector('#train71-picker .train71-pick');
              if(!b) return false; b.click(); return true; }""")
            pg.wait_for_timeout(900)
            click_first(pg, ["確認填入"], 1200)
            filled = day_names(pg)
            print(f"[{tag}] B3 fill: pickClicked={pick_ok} days={filled}", flush=True)
            pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_b3_filled.png"))
        out["b3_fill"] = {"days": filled,
            "allStage": bool(filled) and all(("台風訓練" in d or "休息" in d or "街頭表演" in d or "咖啡店" in d) for d in filled)}
        # 還原返原狀
        assert click_exact(pg, "還原"), "還原（填滿後）撳唔到"
        out["b3_reset_after_fill"] = day_names(pg) == base_days
        print(f"[{tag}] B3 reset after fill: {out['b3_reset_after_fill']}", flush=True)
        assert click_exact(pg, "全日訓練"), "全日訓練閂唔到（收尾）"
        pg.wait_for_timeout(500)

        # ---- B1 編輯功能回歸：全日休息 → 還原；清空 → 還原 ----
        assert click_exact(pg, "全日休息"), "全日休息撳唔到"
        assert click_exact(pg, "確認填入"), "確認填入撳唔到"
        rest_days = day_names(pg)
        out["b1_rest"] = {"allRest": all("休息" in d for d in rest_days)}
        assert click_exact(pg, "還原"), "還原（休息後）撳唔到"
        out["b1_reset_after_rest"] = day_names(pg) == base_days
        assert click_exact(pg, "清空本週"), "清空本週撳唔到"
        assert click_exact(pg, "清空可改日"), "清空可改日撳唔到"
        clear_days = day_names(pg)
        out["b1_clear"] = {"allScout": all("到處逛逛" in d for d in clear_days)}
        assert click_exact(pg, "還原"), "還原（清空後）撳唔到"
        out["b1_reset_after_clear"] = day_names(pg) == base_days
        print(f"[{tag}] B1 func rest={out['b1_rest']} clear={out['b1_clear']} resets={out['b1_reset_after_rest']}/{out['b1_reset_after_clear']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_editable.png"))

        # ---- B2：四組 subtab 逐個切換＋pane 底色 ----
        b2 = {}
        for gid, subs in [
            ("hgroup-career", ["htab-works", "htab-awards", "htab-memory"]),
            ("hgroup-status", ["htab-ledger", "htab-inv"]),
            ("hgroup-news", ["htab-rumor", "htab-clippings"]),
            ("hgroup-favor", ["htab-debt", "htab-people"]),
        ]:
            pg.locator("#" + gid).click(timeout=3000); pg.wait_for_timeout(900)
            for bid in subs:
                try:
                    pg.locator("#" + bid).click(timeout=3000)
                except Exception:
                    print(f"[{tag}]   subtab {bid} click FAIL", flush=True); continue
                pg.wait_for_timeout(700)
                mm = pg.evaluate(JS_MEASURE)
                g = [x for x in mm["subGroups"] if x["group"] == gid.split("-")[1]][0]
                on_items = [(i["text"], i["on"], i["circle"]) for i in g["items"]]
                pane_on = mm["paneOn"]
                b2[bid] = {"pane": pane_on, "bg": mm["paneBgs"].get(pane_on),
                           "items": on_items,
                           "circleFollowsOn": all((i["circle"] is True) == i["on"] for i in g["items"])}
                print(f"[{tag}] B2 {bid}: pane={pane_on} bg={b2[bid]['bg']} circleFollows={b2[bid]['circleFollowsOn']}", flush=True)
                pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_b2_{bid}.png"))
        # plan 組對照：進度 pane 底色＋行程／進度圈跟住郁
        pg.locator("#hgroup-plan").click(timeout=3000); pg.wait_for_timeout(900)
        pg.locator("#htab-progress").click(timeout=3000); pg.wait_for_timeout(900)
        m_prog = pg.evaluate(JS_MEASURE)
        b2["htab-progress"] = {"pane": m_prog["paneOn"], "bg": m_prog["paneBgs"].get(m_prog["paneOn"]),
            "items": [(i["text"], i["on"], i["circle"]) for i in m_prog["subGroups"][0]["items"]],
            "circleFollowsOn": all((i["circle"] is True) == i["on"] for i in m_prog["subGroups"][0]["items"])}
        print(f"[{tag}] B2 htab-progress: {b2['htab-progress']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_b2_htab-progress.png"))
        pg.locator("#htab-plan").click(timeout=3000); pg.wait_for_timeout(900)
        out["b2"] = b2
        out["b2_lightText"] = pg.evaluate(JS_MEASURE)["lightText"]
        print(f"[{tag}] B2 lightText: {out['b2_lightText']}", flush=True)

        # ---- B1 鎖定：確定行程 → locked 量度 ----
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        pg.wait_for_timeout(800)
        assert open_handbook_via_menu(pg), "handbook did not reopen"
        pg.evaluate("() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=0; }")
        pg.wait_for_timeout(300)
        m2 = pg.evaluate(JS_MEASURE)
        out["locked"] = m2
        pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_locked.png"))
        print(f"[{tag}] locked confirm={m2['confirm']} resetVisible={m2['reset']['visible']} days full={m2['days']['fullVisible']}/{m2['days']['count']} nbActionsH={m2['nbActions']['rect']['h']} b1parts={m2['b1parts']}", flush=True)
        for d in m2["days"]["rows"]:
            print(f"[{tag}]   day {d['text'][:14]:16s} top={d['top']} bottom={d['bottom']} full={d['visibleFull']}", flush=True)
        # ---- 返回地圖（吊牌） ----
        pg.locator("#home-back-map-tabs").click(timeout=3000); pg.wait_for_timeout(1200)
        back = pg.evaluate("() => { const v=document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }")
        out["backToMap"] = back
        print(f"[{tag}] back to map via tag: {back}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"145_{tag}_map.png"))
        out["errors"] = errs
        out["http404"] = http404
        print(f"[{tag}] PAGEERRORS: {errs[:5]} HTTP404: {http404[:5]}", flush=True)
    finally:
        ctx.close()
    return out

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        LOG["phases"]["932"] = run_viewport(pw, 430, 932, "932")
        LOG["phases"]["700"] = run_viewport(pw, 430, 700, "700")
    json.dump(LOG, open(os.path.join(HERE, "drive145.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("LOG qa145/drive145.json", flush=True)
finally:
    stop(srv)
