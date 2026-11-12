# -*- coding: utf-8 -*-
"""v20a143 BOOK143 實駕 drive143：B1 編輯掣紙面化＋B2 其餘四組 subtab 手寫行＋B3 短屏印章收細。
用法：/home/hatch/pwenv49/bin/python qa143/drive143.py
Mirror：工作副本 ~/workspace/linji-work143，port 8963，430x932＋430x700，?softPreview=1。
流程：UI 新遊戲 → 手帳（editable）→ 量度 B1/B2 計算樣式 → 逐個掣功能驗
（全日休息／全日訓練／清空本週／複製到…／每行複製／還原）→ 四組 subtab 逐個切換
（圈跟住郁）→ 確定行程 → locked 量度 B3（印章高＋可見日數）→ 返回地圖。
量度：掣 computed style／subtab 圈／印章 footer 高／可見日數／備忘紙／五 tab 殼。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work143"
HERE = os.path.join(ROOT, "qa143")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8963
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"errors": [], "http404": [], "phases": {}}

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
  const styleOf = sel => { const el = document.querySelector(sel); if(!el) return null;
    const c = cs(el); return {text: (el.textContent||'').trim().slice(0,12), rect: rect(el),
      bg: c.backgroundColor, color: c.color, fontSize: c.fontSize, fontFamily: c.fontFamily.slice(0,30),
      borderRadius: c.borderRadius, borderTop: c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor,
      borderBottom: c.borderBottomWidth+' '+c.borderBottomStyle+' '+c.borderBottomColor,
      boxShadow: (c.boxShadow||'').slice(0,40)}; };
  const quick = [...document.querySelectorAll('#nb-quick > button')].map(el => {
    const c = cs(el); return {id: el.id, text: el.textContent.trim(), rect: rect(el),
      bg: c.backgroundColor, color: c.color, fontSize: c.fontSize,
      fontFamily: c.fontFamily.slice(0,30), borderRadius: c.borderRadius,
      border: c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor}; });
  const subGroups = [...document.querySelectorAll('.hsub-group')].map(g => {
    const grp = g.getAttribute('data-hsubgroup');
    return {group: grp, on: g.classList.contains('on'), items:
      [...g.querySelectorAll('.home-tab')].map(el => { const c = cs(el); const after = cs(el, '::after');
        return {id: el.id, text: el.textContent.trim(), on: el.classList.contains('on'),
          rect: rect(el), color: c.color, fontSize: c.fontSize,
          fontFamily: c.fontFamily.slice(0,30), bg: c.backgroundColor, borderRadius: c.borderRadius,
          circle: (after.backgroundImage||'').indexOf('svg') >= 0,
          afterContent: after.content, afterW: after.width, afterH: after.height}; })}; });
  const nbM = document.getElementById('notebook');
  const nbRM = nbM ? nbM.getBoundingClientRect() : null;
  const actRM = document.getElementById('nb-actions').getBoundingClientRect();
  const days = [...document.querySelectorAll('#nb-days .day-row')].map(el => {
    const b = el.getBoundingClientRect();
    return {text: (el.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30),
            top: Math.round(b.top), bottom: Math.round(b.bottom),
            // clip-aware：唔計俾 notebook 捲走／俾 sticky footer 遮住嗰啲
            // （舊版只用 window.innerHeight 會計多咗，probe143 捉到）
            visibleFull: nbRM && b.top >= Math.round(nbRM.top) && b.bottom <= Math.round(actRM.top),
            hasCopy: !!el.querySelector('.cp')}; });
  const conf = document.getElementById('btn-confirm-plan');
  const reset = document.getElementById('btn-reset-plan');
  const cc = conf ? cs(conf) : null; const rc = reset ? cs(reset) : null;
  const nb = document.getElementById('notebook');
  const memo = document.getElementById('home-stats');
  return {
    vh: window.innerHeight, vw: window.innerWidth,
    money: S.money, dual,
    memoText: memo ? memo.textContent.replace(/\\s+/g, ' ').trim() : null,
    memoRect: rect(memo),
    tabs: [...document.querySelectorAll('#home-tabs .home-tab')].map(el => {
      const c = cs(el); return {id: el.id, text: el.textContent.trim(), on: el.classList.contains('on'),
        rect: rect(el), bg: c.backgroundColor, height: c.height, width: c.width}; }),
    quick, subGroups,
    paneOn: (()=>{ const p = document.querySelector('.home-pane.on'); return p ? p.id : null; })(),
    copyWrapOpen: (()=>{ const w = document.getElementById('nb-copy-wrap'); return w ? w.classList.contains('open') : null; })(),
    copyChips: [...document.querySelectorAll('#nb-copy-chips button')].map(el => {
      const c = cs(el); return {text: el.textContent.trim(), disabled: el.disabled, on: el.classList.contains('on'),
        borderRadius: c.borderRadius, bg: c.backgroundColor, fontSize: c.fontSize}; }),
    copyActions: [...document.querySelectorAll('.nb-copy-actions button')].map(el => {
      const c = cs(el); return {id: el.id, text: el.textContent.trim(), cls: el.className,
        borderRadius: c.borderRadius, bg: c.backgroundColor, color: c.color, fontSize: c.fontSize,
        border: c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor}; }),
    dayCopyBtn: styleOf('#nb-days .day-row .cp'),
    trainWrapVisible: (()=>{ const w = document.getElementById('nb-train71-wrap'); return w ? !w.hidden : null; })(),
    nbActions: {rect: rect(document.getElementById('nb-actions')),
      bg: cs(document.getElementById('nb-actions')).backgroundColor},
    confirm: conf ? {text: conf.textContent.trim(), disabled: conf.disabled, locked: conf.classList.contains('is-locked'),
      rect: rect(conf), color: cc.color, fontSize: cc.fontSize, bg: cc.backgroundColor,
      borderTop: cc.borderTopWidth+' '+cc.borderTopStyle+' '+cc.borderTopColor,
      borderRadius: cc.borderRadius, letterSpacing: cc.letterSpacing, transform: cc.transform} : null,
    reset: reset ? {text: reset.textContent.trim(), visible: getComputedStyle(reset).display !== 'none' && !!reset.offsetParent,
      rect: rect(reset), color: rc.color, fontSize: rc.fontSize, bg: rc.backgroundColor,
      borderBottom: rc.borderBottomWidth+' '+rc.borderBottomStyle+' '+rc.borderBottomColor,
      borderRadius: rc.borderRadius} : null,
    tag: (()=>{ const t = document.getElementById('home-back-map-tabs'); return t ? {text: t.textContent.trim(), rect: rect(t)} : null; })(),
    geometry: {notebookTop: nb ? Math.round(nb.getBoundingClientRect().top) : null,
      nbActionsRect: rect(document.getElementById('nb-actions'))},
    days: {count: days.length, fullVisible: days.filter(d => d.visibleFull).length, rows: days},
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
    pg.on("response", lambda r: http404.append({"url": r.url.split("/")[-1][:60], "status": r.status}) if r.status >= 400 else None)
    out = {}
    try:
        assert new_game_to_handbook(pg), "handbook did not open"
        pg.evaluate("() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=0; }")
        pg.wait_for_timeout(300)
        m = pg.evaluate(JS_MEASURE)
        out["editable"] = m
        pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_editable.png"))
        print(f"[{tag}] quick={[(q['text'], q['fontSize'], q['borderRadius'], q['bg']) for q in m['quick']]}", flush=True)
        print(f"[{tag}] nbActions bg={m['nbActions']['bg']} h={m['nbActions']['rect']['h']} confirm={m['confirm']['text']}|{m['confirm']['fontSize']}|{m['confirm']['borderTop']}|{m['confirm']['bg']} reset={m['reset']}", flush=True)
        print(f"[{tag}] dayCopy={m['dayCopyBtn']} memo={m['memoText']}", flush=True)
        print(f"[{tag}] tabs={[(t['text'], t['rect']['w'], t['rect']['h'], t['on']) for t in m['tabs']]} days full={m['days']['fullVisible']}/{m['days']['count']}", flush=True)
        for g in m["subGroups"]:
            print(f"[{tag}] subtab {g['group']} on={g['on']} items={[(i['text'], i['on'], i['fontSize'], i['color'], i['circle']) for i in g['items']]}", flush=True)
        base_days = day_names(pg)
        out["baseDays"] = base_days

        # ---- B1 功能：全日休息 ----
        assert click_exact(pg, "全日休息"), "全日休息掣撳唔到"
        assert click_exact(pg, "確認填入"), "確認填入撳唔到"
        rest_days = day_names(pg)
        out["b1_rest"] = {"days": rest_days, "allRest": all("休息" in d for d in rest_days)}
        print(f"[{tag}] B1 rest: allRest={out['b1_rest']['allRest']} days={rest_days}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_b1_rest.png"))
        # ---- 還原 ----
        assert click_exact(pg, "還原"), "還原掣撳唔到"
        after_reset = day_names(pg)
        out["b1_reset_after_rest"] = {"backToBase": after_reset == base_days, "days": after_reset}
        print(f"[{tag}] B1 reset after rest: backToBase={out['b1_reset_after_rest']['backToBase']}", flush=True)
        # ---- B1 功能：全日訓練（開選擇器，唔填） ----
        assert click_exact(pg, "全日訓練"), "全日訓練掣撳唔到"
        m_tr = pg.evaluate(JS_MEASURE)
        out["b1_train"] = {"pickerVisible": m_tr["trainWrapVisible"], "toast": m_tr["toast"]}
        print(f"[{tag}] B1 train: pickerVisible={m_tr['trainWrapVisible']} toast={m_tr['toast']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_b1_train.png"))
        assert click_exact(pg, "全日訓練"), "全日訓練再撳閂唔到"
        m_tr2 = pg.evaluate(JS_MEASURE)
        out["b1_train_toggle_off"] = m_tr2["trainWrapVisible"] is False
        print(f"[{tag}] B1 train toggle off: {out['b1_train_toggle_off']}", flush=True)
        # ---- B1 功能：清空本週 ----
        assert click_exact(pg, "清空本週"), "清空本週掣撳唔到"
        assert click_exact(pg, "清空可改日"), "清空可改日撳唔到"
        clear_days = day_names(pg)
        out["b1_clear"] = {"days": clear_days, "allScout": all("到處逛逛" in d for d in clear_days)}
        print(f"[{tag}] B1 clear: allScout={out['b1_clear']['allScout']}", flush=True)
        assert click_exact(pg, "還原"), "還原（清空後）撳唔到"
        out["b1_reset_after_clear"] = day_names(pg) == base_days
        print(f"[{tag}] B1 reset after clear: {out['b1_reset_after_clear']}", flush=True)
        # ---- B1 功能：每行複製（週一嗰粒 ⧉ 複製） ----
        cp_ok = pg.evaluate("""() => { const cp = document.querySelector('#nb-days .day-row .cp');
          if(!cp) return false; cp.click(); return true; }""")
        pg.wait_for_timeout(1000)
        m_cp = pg.evaluate(JS_MEASURE)
        out["b1_daycopy"] = {"clicked": cp_ok, "wrapOpen": m_cp["copyWrapOpen"],
                             "chips": [(c["text"], c["disabled"]) for c in m_cp["copyChips"]],
                             "chipStyle": (m_cp["copyChips"][0] if m_cp["copyChips"] else None),
                             "actions": [(a["text"], a["borderRadius"], a["color"]) for a in m_cp["copyActions"]]}
        print(f"[{tag}] B1 day-copy: {out['b1_daycopy']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_b1_copy.png"))
        # 揀「週末」預設＋套用複製
        assert click_exact(pg, "週末"), "週末預設撳唔到"
        assert click_exact(pg, "套用複製"), "套用複製撳唔到"
        m_ap = pg.evaluate(JS_MEASURE)
        out["b1_copy_apply"] = {"toast": m_ap["toast"], "days": day_names(pg)}
        print(f"[{tag}] B1 copy apply: toast={m_ap['toast']}", flush=True)
        assert click_exact(pg, "還原"), "還原（複製後）撳唔到"
        out["b1_reset_after_copy"] = day_names(pg) == base_days
        print(f"[{tag}] B1 reset after copy: {out['b1_reset_after_copy']}", flush=True)
        # ---- B1 功能：複製到…（由快捷掣開面板） ----
        assert click_exact(pg, "複製到…"), "複製到…撳唔到"
        m_c2 = pg.evaluate(JS_MEASURE)
        out["b1_copybtn"] = {"wrapOpen": m_c2["copyWrapOpen"], "chips": len(m_c2["copyChips"])}
        print(f"[{tag}] B1 copy-btn: wrapOpen={m_c2['copyWrapOpen']} chips={len(m_c2['copyChips'])}", flush=True)
        assert click_exact(pg, "複製到…"), "複製到…再撳閂唔到"
        m_c3 = pg.evaluate(JS_MEASURE)
        out["b1_copybtn_toggle_off"] = m_c3["copyWrapOpen"] is False
        print(f"[{tag}] B1 copy-btn toggle off: {out['b1_copybtn_toggle_off']}", flush=True)

        # ---- B2：四組 subtab 逐個切換（圈跟住郁）＋plan 組對照 ----
        b2 = {}
        for gid, subs, expect_pane in [
            ("hgroup-career", ["作品", "獎項", "回憶"], "home-pane-works"),
            ("hgroup-status", ["記數", "標籤", "庫存"], "home-pane-ledger"),
            ("hgroup-news", ["傳聞", "剪報"], "home-pane-rumor"),
            ("hgroup-favor", ["人情債", "人脈"], "home-pane-debt"),
        ]:
            pg.locator("#" + gid).click(timeout=3000); pg.wait_for_timeout(900)
            grp = pg.evaluate("""(g) => { const el = document.querySelector('.hsub-group[data-hsubgroup="'+g+'"]');
              // 標籤掣本身 hidden（pre-existing，唔係 B2 改出嚟）——淨驗可見掣
              return el ? [...el.querySelectorAll('.home-tab')].filter(b => !!b.offsetParent).map(b => b.id) : []; }""",
              {"career": "career", "status": "status", "news": "news", "favor": "favor"}[gid.split("-")[1]])
            res = {}
            for bid in grp:
                pg.locator("#" + bid).click(timeout=3000); pg.wait_for_timeout(700)
                mm = pg.evaluate(JS_MEASURE)
                g = [x for x in mm["subGroups"] if x["group"] == gid.split("-")[1]][0]
                on_items = [(i["text"], i["on"], i["circle"]) for i in g["items"]]
                res[bid] = {"pane": mm["paneOn"], "items": on_items,
                            "circleFollowsOn": all((i["circle"] is True) == i["on"] for i in g["items"])}
                print(f"[{tag}] B2 {gid}/{bid}: pane={mm['paneOn']} {on_items} circleFollows={res[bid]['circleFollowsOn']}", flush=True)
            b2[gid] = res
            pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_b2_{gid}.png"))
        out["b2"] = b2
        # plan 組對照：行程→進度→行程，圈跟住郁
        pg.locator("#hgroup-plan").click(timeout=3000); pg.wait_for_timeout(900)
        pg.locator("#htab-progress").click(timeout=3000); pg.wait_for_timeout(900)
        m_prog = pg.evaluate(JS_MEASURE)
        pg.locator("#htab-plan").click(timeout=3000); pg.wait_for_timeout(900)
        m_plan = pg.evaluate(JS_MEASURE)
        out["b2_plan_control"] = {
            "progress": [(s["text"], s["on"], s["circle"]) for s in m_prog["subGroups"][0]["items"]],
            "back": [(s["text"], s["on"], s["circle"]) for s in m_plan["subGroups"][0]["items"]]}
        print(f"[{tag}] B2 plan control: {out['b2_plan_control']}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_b2_plan.png"))

        # ---- B1 最後：確定行程 → locked ----
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        click_first(pg, ["確定出發"], 1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
                break
        pg.wait_for_timeout(800)
        assert open_handbook_via_menu(pg), "handbook did not reopen"
        # B3 對照要 scrollTop=0（drive 入面撳過掣會留低 scrollTop，唔 reset 會量多咗）
        pg.evaluate("() => { const nb=document.getElementById('notebook'); if(nb) nb.scrollTop=0; }")
        pg.wait_for_timeout(300)
        m2 = pg.evaluate(JS_MEASURE)
        out["locked"] = m2
        pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_locked.png"))
        print(f"[{tag}] locked confirm={m2['confirm']} resetVisible={m2['reset']['visible']} days full={m2['days']['fullVisible']}/{m2['days']['count']} nbActionsH={m2['nbActions']['rect']['h']} memo={m2['memoText']}", flush=True)
        # ---- 返回地圖（吊牌） ----
        pg.locator("#home-back-map-tabs").click(timeout=3000); pg.wait_for_timeout(1200)
        back = pg.evaluate("() => { const v=document.getElementById('v-map'); return !!(v && v.classList.contains('on')); }")
        out["backToMap"] = back
        print(f"[{tag}] back to map via tag: {back}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"143_{tag}_map.png"))
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
    json.dump(LOG, open(os.path.join(HERE, "drive143.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("LOG qa143/drive143.json", flush=True)
finally:
    stop(srv)
