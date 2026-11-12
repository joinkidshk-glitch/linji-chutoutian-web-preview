# -*- coding: utf-8 -*-
"""v20a142 實駕：A1 老闆 bust 髮頂被切（列表 scrollTop 殘留假設）＋A2 空狀態死位＋B1 地圖標籤壓紋底。
用法：/home/hatch/pwenv49/bin/python qa142/drive142.py [--only a1|a2|b1]
[ROOT 預設工作副本；設 LINJI142_ROOT 可指去其他 root 做反證／對照]
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request

ROOT = os.environ.get("LINJI142_ROOT", "/home/hatch/workspace/linji-work142")
HERE = "/home/hatch/workspace/linji-work142/qa142"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8973
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"errors": [], "http404": [], "cases": {}}

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
    print("serve ok", cwd, "sha", sha[:12], flush=True)
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

def click_exact(pg, text, wait=1200):
    ok = pg.evaluate("""(t) => {
      const els=[...document.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()===t;});
      if(!els.length) return false; els[0].click(); return true; }""", text)
    pg.wait_for_timeout(wait)
    return ok

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
    print("NEW GAME OK:", ok, flush=True)
    return ok

def clear_encounter(pg, max_steps=40):
    handled = False
    for _ in range(max_steps):
        present = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return false;
          const line = ov.querySelector('.e79-line');
          return !!(line && (line.textContent||'').trim()); }""")
        if not present:
            return handled
        handled = True
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""")
        pg.wait_for_timeout(700)
        if not clicked:
            break
    return handled

def open_location(pg, name):
    """v137：冇「全部地點」掣（v135 拎走），直接撳地圖 pin（.pin-img／.plab）。
    撳針後可能彈 ENC79 巧遇（播完先開 sheet），要清埋巧遇再驗 sheet；唔得就重撳一次。"""
    click_first(pg, ["返回地圖"], 800)
    pg.wait_for_timeout(600)
    for _ in range(2):
        loc_id = pg.evaluate("""(name) => {
          const pins=[...document.querySelectorAll('.pin')];
          const p=pins.find(x=>{ const l=x.querySelector('.plab'); return l && (l.textContent||'').trim()===name; });
          if(!p) return null;
          const img=p.querySelector('.pin-img'); if(img){ img.click(); return p.dataset.loc; }
          const lab=p.querySelector('.plab'); if(lab){ lab.click(); return p.dataset.loc; }
          return null; }""", name)
        pg.wait_for_timeout(1200)
        clear_encounter(pg)
        pg.wait_for_timeout(600)
        if loc_id and pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }"):
            return True
        click_first(pg, ["返回地圖"], 600)
        pg.wait_for_timeout(400)
    return False

JS_A1_MEASURE = """() => {
  const r = s => { const el = document.querySelector(s); if(!el) return null;
    const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), bottom: Math.round(b.bottom)}; };
  const mi = document.getElementById('modal-inner');
  const img = document.querySelector('.cn-issuer-img30v2');
  return {
    vh: window.innerHeight,
    maskCls: (document.getElementById('mask')||{}).className || '',
    appST: document.getElementById('app') ? document.getElementById('app').scrollTop : null,
    appSH: document.getElementById('app') ? document.getElementById('app').scrollHeight : null,
    mi: mi ? {scrollTop: mi.scrollTop, scrollH: mi.scrollHeight, clientH: mi.clientHeight,
               overflowY: getComputedStyle(mi).overflowY} : null,
    sheetBody: (()=>{ const b=document.querySelector('.notice_sheet_body');
      return b ? {scrollTop: b.scrollTop, scrollH: b.scrollHeight} : null; })(),
    modal: r('.modal'), hero: r('.cn-issuer30v2'),
    img: img ? {rect: r('.cn-issuer-img30v2'), natW: img.naturalWidth, natH: img.naturalHeight,
                src: (img.getAttribute('src')||'').split('/').pop().slice(0,44)} : null,
    cap: r('.cn-issuer-cap30v2'),
    h2: (()=>{ const h=document.querySelector('.cn-work');
      return h ? {txt:(h.textContent||'').trim().slice(0,20), rect:r('.cn-work')} : null; })(),
    boss: (()=>{ const c=document.querySelector('.cn-issuer-cap30v2 b');
      return c ? c.textContent : null; })(),
  };
}"""

def open_board(pg):
    """喺 loc-sheet 撳「只查看通告欄」，等 board modal（.gig-teaser）出現。"""
    hit = pg.evaluate("""() => {
      const els=[...document.querySelectorAll('#loc-sheet button, #loc-acts button')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').includes('只查看通告欄');});
      if(!els.length) return false; els[0].click(); return true; }""")
    pg.wait_for_timeout(1200)
    return hit and pg.evaluate("() => !!document.querySelector('.gig-teaser')")

def open_first_teaser(pg):
    ok = pg.evaluate("""() => {
      const c = document.querySelector('.gig-teaser');
      if(!c) return false; c.click(); return true; }""")
    pg.wait_for_timeout(1200)
    return ok and pg.evaluate("() => !!document.querySelector('.cn-issuer30v2')")

def close_detail_to_board(pg):
    """撳「離開」→ doScout 重開 board；等 .gig-teaser 再出現。"""
    pg.evaluate("""() => { const b=[...document.querySelectorAll('#modal-btns button')].find(x=>(x.innerText||'').trim()==='離開'); if(b) b.click(); return true; }""")
    pg.wait_for_timeout(1200)
    return pg.evaluate("() => !!document.querySelector('.gig-teaser')")

def case_a1(pw, tag, scroll_px):
    """一個 session：新遊戲 → 中環廣告 → board →（捲 scroll_px）→ 開第一張詳情 → 量度。"""
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 430, "height": 932})
    pg.on("console", lambda m: LOG["errors"].append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: LOG["errors"].append("PAGEERROR: " + str(e)))
    pg.on("response", lambda r: LOG["http404"].append(r.url) if r.status == 404 else None)
    try:
        assert new_game(pg), "new game failed"
        clear_encounter(pg)
        assert open_location(pg, "中環廣告"), "open loc 中環廣告 failed"
        clear_encounter(pg)
        assert open_board(pg), "open board failed"
        before = pg.evaluate("""() => { const mi=document.getElementById('modal-inner');
          return mi ? {scrollH: mi.scrollHeight, clientH: mi.clientHeight, scrollTop: mi.scrollTop} : null; }""")
        if scroll_px:
            got = pg.evaluate("""(px) => { const mi=document.getElementById('modal-inner');
              mi.scrollTop = px; return mi.scrollTop; }""", scroll_px)
            print(f"  [{tag}] board scroll set {scroll_px} -> actual {got} (scrollH {before['scrollH']} clientH {before['clientH']})", flush=True)
        else:
            print(f"  [{tag}] board fresh scrollTop={before['scrollTop']} scrollH={before['scrollH']} clientH={before['clientH']}", flush=True)
        assert open_first_teaser(pg), "open teaser failed"
        m = pg.evaluate(JS_A1_MEASURE)
        img_y = (m.get("img") or {}).get("rect", {}).get("y")
        mi_st = (m.get("mi") or {}).get("scrollTop")
        app_st = m.get("appST")
        clipped = img_y is not None and img_y < 0
        ok142 = (not clipped) and app_st == 0 and mi_st == 0
        LOG["cases"][tag] = {"measure": m, "board_before": before, "img_clipped": clipped, "pass": ok142}
        print(f"  [{tag}] img_y={img_y} app.scrollTop={app_st} mi.scrollTop={mi_st} boss={m.get('boss')} -> {'PASS' if ok142 else 'FAIL'}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"142_{tag}.png"))
        return m
    finally:
        br.close()

BOSS_LOCS = [
    ("tvb_longmen", "星河電視台", "沈卓衡"), ("film_lion", "獅子山製片", "羅勁威"),
    ("ad_adm", "金鐘創意", "方樂怡"), ("ad_central", "中環廣告", "霍君豪"),
    ("rec_hk", "香江唱片", "伍兆昌"), ("tvb_kowloon", "九龍電視台", "陶映紅"),
    ("film_cotton", "紅棉影業", "鄭伯康"), ("rec_wanchai", "灣仔唱片", "梁廣成"),
    ("tvb_harbour", "海港廣播", "顧學禮"), ("film_harbour", "維港電影", "夏文心"),
    ("rec_star", "天星音樂", "溫子峰"),
]

def open_first_detail_from_sheet(pg, loc_id):
    """地點 sheet 入面撳第一張通告（試鏡入口／board teaser），開詳情卡。"""
    picks = pg.evaluate("""(locId) => {
      const gs = (window.GIGS||[]).filter(g => g && g.loc === locId);
      return gs.slice(0, 10).map(g => ({id: g.id, title: g.title})); }""", loc_id)
    for p in picks:
        frag = p["title"].split("》")[0].replace("《", "")
        hit = pg.evaluate("""(frag) => {
          const els=[...document.querySelectorAll('#loc-sheet button, #loc-acts button, #loc-sheet [role=button]')].filter(e=>{
            const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').includes(frag);});
          if(!els.length) return false; els[0].click(); return true; }""", frag)
        pg.wait_for_timeout(1200)
        if hit and pg.evaluate("() => !!document.querySelector('.cn-issuer30v2')"):
            return p
        pg.evaluate("""() => { const b=[...document.querySelectorAll('#modal-btns button')].find(x=>(x.innerText||'').trim()==='離開'); if(b) b.click(); return true; }""")
        pg.wait_for_timeout(800)
    return None

def case_a1_bosses(pw):
    """一個 session 逐位開 11 位老闆詳情（經地點 sheet 通告入口），量髮頂。"""
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 430, "height": 932})
    pg.on("console", lambda m: LOG["errors"].append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: LOG["errors"].append("PAGEERROR: " + str(e)))
    pg.on("response", lambda r: LOG["http404"].append(r.url) if r.status == 404 else None)
    results = {}
    try:
        assert new_game(pg), "new game failed"
        for loc_id, loc_name, boss in BOSS_LOCS:
            pg.evaluate("() => { if (window.S && window.S.travel114) window.S.travel114.used = 0; return true; }")
            clear_encounter(pg)
            if not open_location(pg, loc_name):
                print(f"  [a1-boss] {boss} ({loc_id}): open loc FAILED", flush=True)
                results[loc_id] = {"pass": False, "why": "open loc failed"}
                continue
            clear_encounter(pg)
            opened = open_first_detail_from_sheet(pg, loc_id)
            if not opened:
                # 後備：board 路徑
                if open_board(pg):
                    opened = open_first_teaser(pg) and {"title": "board-first"} or None
            if not opened:
                print(f"  [a1-boss] {boss} ({loc_id}): no gig detail", flush=True)
                results[loc_id] = {"pass": False, "why": "no gig detail"}
                click_first(pg, ["返回地圖"], 700)
                continue
            m = pg.evaluate(JS_A1_MEASURE)
            img_y = (m.get("img") or {}).get("rect", {}).get("y")
            ok142 = (img_y is not None and img_y >= 0 and m.get("appST") == 0
                     and m.get("boss") == boss and (m.get("hero") or {}).get("h") == 240)
            results[loc_id] = {"pass": ok142, "measure": m}
            print(f"  [a1-boss] {boss}: img_y={img_y} appST={m.get('appST')} heroH={(m.get('hero') or {}).get('h')} -> {'PASS' if ok142 else 'FAIL'}", flush=True)
            pg.screenshot(path=os.path.join(SHOTS, f"142_a1_boss_{loc_id}.png"))
            close_detail_to_board(pg)
            click_first(pg, ["返回地圖"], 700)
            pg.wait_for_timeout(500)
            clear_encounter(pg)
        LOG["cases"]["a1_bosses"] = results
        return results
    finally:
        br.close()

def case_a1_reviewflow(pw, tag):
    """review 原流程（drive_review5/6：手帳事業→去通告欄→撳年宵花市）——pristine 下重現到 img y=-40。"""
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 430, "height": 932})
    pg.on("console", lambda m: LOG["errors"].append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: LOG["errors"].append("PAGEERROR: " + str(e)))
    pg.on("response", lambda r: LOG["http404"].append(r.url) if r.status == 404 else None)
    try:
        pg.goto(URL); pg.wait_for_timeout(3000)
        click_first(pg, ["新遊戲"], 1500)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        click_first(pg, ["覆蓋", "確定", "確認"], 900)
        click_first(pg, ["跳過教學"], 1200)
        pg.wait_for_timeout(1200)
        clear_encounter(pg)  # v142：開局有機會彈 ENC79 巧遇（P 50%），唔清會食咗之後嘅點擊，令「去通告欄」開唔到板
        click_first(pg, ["☰"], 700)
        click_first(pg, ["手帳"], 900)
        click_first(pg, ["事業"], 800)
        click_first(pg, ["去通告欄"], 1200)
        clear_encounter(pg)
        box = None
        for _ in range(3):  # 板未 render 完就重搵
            box = pg.evaluate("""() => {
              const els = [...document.querySelectorAll('*')].filter(el => el.children.length === 0 && (el.textContent||'').trim() === '年宵花市');
              if (!els.length) return null;
              const r = els[0].getBoundingClientRect();
              return {x: r.x + r.width/2, y: r.y + r.height/2}; }""")
            if box:
                break
            pg.wait_for_timeout(1200)
        assert box, "年宵花市 card not found"
        pg.mouse.click(box["x"], box["y"]); pg.wait_for_timeout(1200)
        m = pg.evaluate(JS_A1_MEASURE)
        img_y = (m.get("img") or {}).get("rect", {}).get("y")
        ok142 = img_y is not None and img_y >= 0 and m.get("appST") == 0
        LOG["cases"][tag] = {"measure": m, "pass": ok142}
        print(f"  [{tag}] img_y={img_y} appST={m.get('appST')} modal={m.get('modal')} -> {'PASS' if ok142 else 'FAIL'}", flush=True)
        pg.screenshot(path=os.path.join(SHOTS, f"142_{tag}.png"))
        return m
    finally:
        br.close()

JS_MAP_MEASURE = """() => {
  const r = el => { const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), bottom: Math.round(b.bottom), right: Math.round(b.right)}; };
  const img = document.getElementById('map-img');
  // 可見標籤係 .mn68（.plab 係 display:none 舊層）；pin 掣另計
  const labels = [...document.querySelectorAll('.map-names68 .mn68')].map(e => (
    {text: (e.textContent||'').trim(), rect: r(e), style: e.getAttribute('style')}));
  const pins = [...document.querySelectorAll('.pin')].map(p => {
    const im = p.querySelector('.pin-img');
    return {loc: p.dataset.loc, btn: r(p), img: im ? r(im) : null};
  });
  return {vh: window.innerHeight, mapImg: img ? r(img) : null, labels, pins};
}"""

def case_b1(pw):
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 430, "height": 932})
    pg.on("console", lambda m: LOG["errors"].append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: LOG["errors"].append("PAGEERROR: " + str(e)))
    pg.on("response", lambda r: LOG["http404"].append(r.url) if r.status == 404 else None)
    try:
        assert new_game(pg), "new game failed"
        clear_encounter(pg)
        pg.wait_for_timeout(800)
        m = pg.evaluate(JS_MAP_MEASURE)
        LOG["cases"]["b1_map"] = m
        pg.screenshot(path=os.path.join(SHOTS, "142_b1_map_932.png"))
        # 15/15 熱區逐針實撳
        hits = []
        for pin in m["pins"]:
            loc = pin["loc"]
            # 每針之前重置當日出行額度（S.travel114.used=0），等 15 針都開到 sheet；
            # 額度本身唔郁（v114 邏輯不變，淨係測試期重置計數）。
            pg.evaluate("() => { if (window.S && window.S.travel114) window.S.travel114.used = 0; return true; }")
            ok = pg.evaluate("""(loc) => {
              const p = document.querySelector('.pin[data-loc="' + loc + '"] .pin-img');
              if(!p) return false; p.click(); return true; }""", loc)
            pg.wait_for_timeout(900)
            clear_encounter(pg)
            sheet = pg.evaluate("""() => { const s=document.getElementById('loc-sheet');
              if(!s || !s.classList.contains('on')) return null;
              return (s.innerText||'').slice(0,60); }""")
            hits.append({"loc": loc, "clicked": ok, "sheet": sheet})
            print(f"  [b1] pin {loc}: clicked={ok} sheet={'Y' if sheet else 'N'} {str(sheet)[:40] if sheet else ''}", flush=True)
            pg.screenshot(path=os.path.join(SHOTS, f"142_b1_pin_{loc}.png"))
            click_first(pg, ["返回地圖"], 700)
            pg.wait_for_timeout(500)
            clear_encounter(pg)
        LOG["cases"]["b1_pins"] = hits
        m2 = pg.evaluate(JS_MAP_MEASURE)
        LOG["cases"]["b1_map_after"] = m2
        # 標籤兩兩碰撞檢查（15 張，含 4 張郁過嘅）＋4 張新位
        def overlap(a, b):
            return a["x"] < b["x"] + b["w"] and a["x"] + a["w"] > b["x"] and a["y"] < b["y"] + b["h"] and a["y"] + a["h"] > b["y"]
        labs = m2["labels"]
        clashes = []
        for i in range(len(labs)):
            for j in range(i + 1, len(labs)):
                if overlap(labs[i]["rect"], labs[j]["rect"]):
                    clashes.append((labs[i]["text"], labs[j]["text"]))
        LOG["cases"]["b1_label_clashes"] = clashes
        print("  [b1] label clashes:", clashes if clashes else "none", flush=True)
        for l in labs:
            if l["text"] in ("香江唱片", "廟街禮品", "海港廣播", "金龍茶餐廳"):
                print(f"  [b1] {l['text']}: {l['rect']} style={l['style']}", flush=True)
        return m, hits
    finally:
        br.close()

JS_A2_MEASURE = """() => {
  const r = s => { const el = document.querySelector(s); if(!el) return null;
    const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), bottom: Math.round(b.bottom)}; };
  const vis = s => { const el = document.querySelector(s); if(!el) return false;
    const b = el.getBoundingClientRect(); return b.height > 0 && b.width > 0; };
  const txt = s => { const el = document.querySelector(s); return el ? (el.innerText||'').trim().slice(0,400) : null; };
  const lastBottom = s => { const el = document.querySelector(s); if(!el) return null;
    const kids = [...el.querySelectorAll('*')].filter(k=>{ const b=k.getBoundingClientRect(); return b.height>0; });
    if(!kids.length) return null; return Math.round(Math.max(...kids.map(k=>k.getBoundingClientRect().bottom))); };
  return {
    vh: window.innerHeight,
    progressPaneVis: vis('#home-pane-progress'),
    progressWrap: r('.prog71-wrap'),
    progressPane: r('#home-pane-progress'),
    progressContentBottom: lastBottom('#home-pane-progress'),
    progressScroll: (()=>{ const el=document.querySelector('#home-pane-progress .journal-scroll');
      return el ? {scrollH: el.scrollHeight, clientH: el.clientHeight, scrollTop: el.scrollTop} : null; })(),
    progressText: txt('#home-pane-progress'),
    worksPaneVis: vis('#home-pane-works'),
    worksPane: r('#home-pane-works'),
    worksContentBottom: lastBottom('#home-pane-works'),
    worksText: txt('#home-pane-works'),
    worksEmpty: vis('.works-empty59'),
    worksEmptyRect: r('.works-empty59'),
    worksFrames: document.querySelectorAll('.works-frame142').length,
  };
}"""

def open_notebook(pg):
    pg.click("#btn-menu"); pg.wait_for_timeout(800)
    pg.click('[data-m="journal"]'); pg.wait_for_timeout(1200)
    return pg.evaluate("() => !!document.querySelector('#v-home')")

def click_nb_button(pg, text):
    hit = pg.evaluate("""(t) => {
      const els=[...document.querySelectorAll('#v-home button')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()===t;});
      if(!els.length) return false; els[0].click(); return true; }""", text)
    pg.wait_for_timeout(1000)
    return hit

def case_a2(pw):
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 430, "height": 932})
    pg.on("console", lambda m: LOG["errors"].append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: LOG["errors"].append("PAGEERROR: " + str(e)))
    pg.on("response", lambda r: LOG["http404"].append(r.url) if r.status == 404 else None)
    try:
        assert new_game(pg), "new game failed"
        clear_encounter(pg)
        assert open_notebook(pg), "open notebook failed"
        # 進度頁：plan pane 內「進度」掣
        assert click_nb_button(pg, "進度"), "progress button not found"
        pg.wait_for_timeout(800)
        m = pg.evaluate(JS_A2_MEASURE)
        m["next142"] = pg.evaluate("() => document.querySelectorAll('.prog71-next142').length")
        m["next142Text"] = pg.evaluate("() => { const el=document.querySelector('.prog71-next142'); return el ? (el.innerText||'').trim().slice(0,200) : null; }")
        LOG["cases"]["a2_progress"] = m
        print("  [a2-progress] paneVis=", m.get("progressPaneVis"), "wrap=", m.get("progressWrap"),
              "pane=", m.get("progressPane"), "next142=", m.get("next142"),
              "deadBelowWrap=", (m.get("progressPane") or {}).get("bottom", 0) - (m.get("progressWrap") or {}).get("bottom", 0), flush=True)
        pg.screenshot(path=os.path.join(SHOTS, "142_a2_progress_932.png"))
        # 事業 tab
        assert click_nb_button(pg, "事業"), "works tab not found"
        pg.wait_for_timeout(800)
        m2 = pg.evaluate(JS_A2_MEASURE)
        LOG["cases"]["a2_works"] = m2
        print("  [a2-works] paneVis=", m2.get("worksPaneVis"), "empty=", m2.get("worksEmpty"),
              "frames=", m2.get("worksFrames"), "pane=", m2.get("worksPane"),
              "contentBottom=", m2.get("worksContentBottom"), flush=True)
        pg.screenshot(path=os.path.join(SHOTS, "142_a2_works_932.png"))
        return m, m2
    finally:
        br.close()

def main():
    from playwright.sync_api import sync_playwright
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            if only in (None, "a1"):
                case_a1(pw, "a1_scrolled40", 40)
                case_a1(pw, "a1_fresh", 0)
                case_a1_reviewflow(pw, "a1_reviewflow1")
                case_a1_reviewflow(pw, "a1_reviewflow2")
                case_a1_bosses(pw)
            if only == "a1bosses":
                case_a1_bosses(pw)
            if only in (None, "a2"):
                case_a2(pw)
            if only in (None, "b1"):
                case_b1(pw)
    finally:
        stop(srv)
    print("ERRORS:", json.dumps(LOG["errors"][:10], ensure_ascii=False), flush=True)
    print("404:", json.dumps(LOG["http404"][:10], ensure_ascii=False), flush=True)
    json.dump(LOG, open(os.path.join(HERE, "drive142.json"), "w"), ensure_ascii=False, indent=1)
    print("DRIVE142 done", flush=True)

if __name__ == "__main__":
    main()
