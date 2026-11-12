# -*- coding: utf-8 -*-
"""v20a131 B批實駕 drive131：B3 殺青三卡米色／B2 事業 tab 筆記紙／B4 對話框短句置中。
用法：/home/hatch/pwenv49/bin/python qa131/drive131.py
Mirror：工作副本 ~/workspace/linji-work131，port 8961，390x844，?softPreview=1。
B3：真 buildPostShootRewardPack（試幾款 gigType 直至三 channel 齊）＋真 presentPostShootReward。
B2：☰ → 手帳 → 事業 tab（空狀態）＋ seed 一條 wrapHistory 出 .req 紙卡；獎項／回憶副 tab。
B4：主線合成 StoryPlay.start(A_fong_push1) 逐句量度；巧遇 seed 彭少祺 fav 5 入中環廣告逐句量度。
量度：Range 取文字首／尾行 rect，對比內文區上下留白（置中 ⇔ 上下差 ≤6px）。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work131"
HERE = os.path.join(ROOT, "qa131")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8961
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
    print("NEW GAME OK:", ok, pg.evaluate("() => window.S ? (S.dayIndex + ' ' + S.dateStr) : 'no S'"), flush=True)
    return ok

JS_B2 = """() => {
  const cs = s => { const el = document.querySelector(s); if(!el) return null;
    const b = el.getBoundingClientRect(); const c = getComputedStyle(el);
    return {bg: c.backgroundColor, bgImg: (c.backgroundImage||'').slice(0,120),
            color: c.color, border: c.borderTopColor,
            x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; };
  const req = document.querySelector('#works-list > .req');
  return {
    worksList: cs('#works-list'), awardsList: cs('#awards-list'), memoryList: cs('#memory-list'),
    jobsH: cs('#works-list .jobs72-h'),
    req: req ? cs('#works-list > .req') : null,
    reqSub: req ? getComputedStyle(req.querySelector('div')).color : null,
    worksEmptyH: cs('#works-list .works-empty59 h3'),
    careerTabOn: (()=>{ const b=document.getElementById('hgroup-career'); return b ? b.className : null; })(),
    txt: (document.querySelector('#works-list')||{textContent:''}).textContent.slice(0,120)
  };
}"""

JS_B3 = """() => {
  const cards = [...document.querySelectorAll('.psr-card')].map(el => {
    const c = getComputedStyle(el);
    return {cls: el.className, bgImg: c.backgroundImage, border: c.borderTopColor,
            title: (el.querySelector('.psr-title')||{textContent:''}).textContent.slice(0,30)};
  });
  return {sheet: !!document.querySelector('.psr-sheet'), cards};
}"""

JS_B3_BUILD = """() => {
  // 每份 pack = 1 張 metrics ＋ 1–2 張 press/news/streetFans（v20a38 入選先抽），
  // 所以目標係搵一份有 news 卡嘅 pack（三卡＝metrics＋news＋另一張），唔係三 channel 齊。
  const R = window.__reward;
  if (!R || typeof R.build !== 'function') return {ok: false, why: 'no __reward.build'};
  const types = ['電影','電視劇','唱片通告','廣告'];
  for (let t = 0; t < types.length; t++) {
    for (let k = 0; k < 6; k++) {
      const sh = { title: '試玩通告' + t + '-' + k, type: types[t],
                   gigId: '__b3_' + t + '_' + k, id: '__b3_' + t + '_' + k };
      const pack = R.build(sh);
      const chs = (pack.cards||[]).map(c => c.channel);
      if (chs.includes('news')) {
        window.__b3pack = pack;
        return {ok: true, t, type: types[t], k, channels: chs};
      }
    }
  }
  return {ok: false};
}"""

JS_B3_PRESENT = """(arg) => {
  const R = window.__reward;
  // 用 BUILD 嗰陣搵到嘅同一份 pack（present 嗰陣唔重抽，否則隨機重抽會換走 news 卡）
  const pack = window.__b3pack || R.build({ title: '試玩通告' + arg.t, type: arg.type,
               gigId: '__b3_' + arg.t + '_' + arg.k, id: '__b3_' + arg.t + '_' + arg.k });
  const chs = (pack.cards||[]).map(c => c.channel);
  const shown = R.present(pack, function(){});
  return {shown, channels: chs};
}"""

JS_STORY_MEASURE = """() => {
  const plate = document.querySelector('.story-play .dlg106-plate');
  if (!plate) return {active: false};
  const line = plate.querySelector('.sp-line');
  const spk = plate.querySelector('.sp-speaker');
  const pr = plate.getBoundingClientRect();
  const lr = line ? line.getBoundingClientRect() : null;
  const sr = spk ? spk.getBoundingClientRect() : null;
  let textBox = null;
  if (line && line.textContent.trim()) {
    const range = document.createRange();
    range.selectNodeContents(line);
    const rects = [...range.getClientRects()];
    if (rects.length) {
      const tops = rects.map(r => r.top), bots = rects.map(r => r.bottom);
      textBox = {top: Math.round(Math.min(...tops)), bottom: Math.round(Math.max(...bots)),
                 lines: rects.length, firstH: Math.round(rects[0].height)};
    }
  }
  const cs = getComputedStyle(plate);
  return {active: true,
    plateH: Math.round(pr.height), plateDisplay: cs.display, plateFlexDir: cs.flexDirection,
    speaker: spk ? spk.textContent : null, speakerTop: sr ? Math.round(sr.top) : null,
    lineTop: lr ? Math.round(lr.top) : null, lineBottom: lr ? Math.round(lr.bottom) : null,
    lineH: lr ? Math.round(lr.height) : null,
    lineMarginTop: line ? getComputedStyle(line).marginTop : null,
    lineMarginBottom: line ? getComputedStyle(line).marginBottom : null,
    text: line ? line.textContent.slice(0, 60) : null,
    textLen: line ? line.textContent.length : 0,
    revealing: line ? line.classList.contains('sp-revealing') : null,
    textBox,
    centerGap: (textBox && lr) ? {top: Math.round(textBox.top - lr.top),
                                  bottom: Math.round(lr.bottom - textBox.bottom)} : null};
}"""

JS_ENC_MEASURE = """() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return {present: false};
  const line = ov.querySelector('.e79-line');
  const name = ov.querySelector('.e79-name');
  if (!line) return {present: true, noLine: true};
  const lr = line.getBoundingClientRect();
  const cs = getComputedStyle(line);
  let textBox = null;
  if (line.textContent.trim()) {
    const range = document.createRange();
    range.selectNodeContents(line);
    const rects = [...range.getClientRects()];
    if (rects.length) {
      const tops = rects.map(r => r.top), bots = rects.map(r => r.bottom);
      textBox = {top: Math.round(Math.min(...tops)), bottom: Math.round(Math.max(...bots)),
                 lines: rects.length};
    }
  }
  return {present: true, lineH: Math.round(lr.height),
    display: cs.display, alignItems: cs.alignItems,
    name: name ? name.textContent : null,
    text: line.textContent.slice(0, 60), textLen: line.textContent.length,
    textBox,
    centerGap: (textBox) ? {top: Math.round(textBox.top - lr.top),
                            bottom: Math.round(lr.bottom - textBox.bottom)} : null};
}"""

def step_story_measure(pg, tag, max_steps=25):
    """逐句行主線，量度每一句；回傳量度 list。"""
    out = []
    for step in range(max_steps):
        pg.wait_for_timeout(2200)
        m = pg.evaluate(JS_STORY_MEASURE)
        if not m.get("active"):
            break
        # 等 reveal 完成（文字長度穩定）
        t1 = m.get("textLen")
        pg.wait_for_timeout(600)
        m2 = pg.evaluate(JS_STORY_MEASURE)
        if m2.get("textLen") != t1 and m2.get("revealing"):
            pg.wait_for_timeout(1500)
            m = pg.evaluate(JS_STORY_MEASURE)
        else:
            m = m2
        m["step"] = step
        out.append(m)
        print(f"  STORY {tag}[{step}] spk={m.get('speaker')} len={m.get('textLen')} "
              f"plateH={m.get('plateH')} gap={m.get('centerGap')} txt={m.get('text')}", flush=True)
        if m.get("textBox") and m["textBox"]["lines"] <= 2 and m.get("centerGap"):
            pg.screenshot(path=os.path.join(SHOTS, f"b4_story_short_{tag}_s{step}.png"))
            print("  SHOT b4_story_short_%s_s%d.png" % (tag, step), flush=True)
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            break
        pg.wait_for_timeout(500)
    return out

def step_enc_measure(pg, tag, max_steps=40):
    out = []
    for i in range(max_steps):
        m = pg.evaluate(JS_ENC_MEASURE)
        if not m.get("present"):
            break
        m["step"] = i
        out.append(m)
        print(f"  ENC {tag}[{i}] name={m.get('name')} len={m.get('textLen')} "
              f"lineH={m.get('lineH')} gap={m.get('centerGap')} txt={m.get('text')}", flush=True)
        if m.get("textBox") and m["textBox"]["lines"] <= 2 and m.get("centerGap"):
            pg.screenshot(path=os.path.join(SHOTS, f"b4_enc_short_{tag}.png"))
            print("  SHOT b4_enc_short_%s.png" % tag, flush=True)
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""")
        if not clicked:
            break
        pg.wait_for_timeout(500)
    return out

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
        http404 = []
        def on_resp(resp):
            try:
                if resp.status >= 400:
                    http404.append({"url": resp.url.split("/")[-1][:60], "status": resp.status})
            except Exception:
                pass
        pg.on("response", on_resp)

        # ---------- B2 ----------
        print("== B2 ==", flush=True)
        assert new_game(pg)
        pg.wait_for_timeout(1200)
        pg.locator("button:has-text('☰')").first.click(timeout=3000); pg.wait_for_timeout(900)
        assert click_first(pg, ["手帳"], 1400), "open notebook failed"
        pg.wait_for_timeout(1000)
        assert click_exact(pg, "事業"), "career tab failed"
        pg.wait_for_timeout(1200)
        b2_empty = pg.evaluate(JS_B2)
        pg.screenshot(path=os.path.join(SHOTS, "b2_works_empty.png"))
        print("B2 empty:", json.dumps(b2_empty, ensure_ascii=False), flush=True)
        # seed 一條殺青履歷，出 .req 紙卡（renderWorksPane 唔係 global，撳返作品副 tab 觸發重繪）
        pg.evaluate("""() => {
          const g = (typeof GIGS !== 'undefined' && GIGS.length) ? GIGS[0] : null;
          S.wrapHistory = [{title: g ? g.title : '試玩通告', type: g ? (g.type||'電影') : '電影',
                            totalDays: 3, pay: 1200, fame: 5, rating: '順利'}];
        }""")
        pg.wait_for_timeout(300)
        assert click_exact(pg, "作品"), "works subtab re-click failed"
        pg.wait_for_timeout(900)
        b2_req = pg.evaluate(JS_B2)
        pg.screenshot(path=os.path.join(SHOTS, "b2_works_req.png"))
        print("B2 with req:", json.dumps(b2_req, ensure_ascii=False), flush=True)
        # 獎項／回憶副 tab
        assert click_exact(pg, "獎項"), "awards subtab failed"
        pg.wait_for_timeout(900)
        b2_aw = pg.evaluate(JS_B2)
        pg.screenshot(path=os.path.join(SHOTS, "b2_awards.png"))
        assert click_exact(pg, "回憶"), "memory subtab failed"
        pg.wait_for_timeout(900)
        b2_mem = pg.evaluate(JS_B2)
        pg.screenshot(path=os.path.join(SHOTS, "b2_memory.png"))
        print("B2 awards list:", json.dumps(b2_aw.get("awardsList"), ensure_ascii=False), flush=True)
        print("B2 memory list:", json.dumps(b2_mem.get("memoryList"), ensure_ascii=False), flush=True)
        LOG["phases"]["B2"] = {"empty": b2_empty, "req": b2_req,
                               "awardsList": b2_aw.get("awardsList"), "memoryList": b2_mem.get("memoryList")}
        click_first(pg, ["返回地圖"], 900)

        # ---------- B3 ----------
        print("== B3 ==", flush=True)
        found = pg.evaluate(JS_B3_BUILD)
        print("B3 build search:", found, flush=True)
        assert found.get("ok"), "no 3-channel pack found"
        shown = pg.evaluate(JS_B3_PRESENT, {"t": found["t"], "type": found["type"], "k": found["k"]})
        print("B3 present:", shown, flush=True)
        pg.wait_for_timeout(1200)
        b3 = pg.evaluate(JS_B3)
        pg.screenshot(path=os.path.join(SHOTS, "b3_psr.png"))
        print("B3 cards:", json.dumps(b3, ensure_ascii=False), flush=True)
        LOG["phases"]["B3"] = {"build": found, "present": shown, "cards": b3}
        click_first(pg, ["收下這份反響"], 900)
        pg.wait_for_timeout(800)

        # ---------- B4 主線 ----------
        print("== B4 story ==", flush=True)
        ok = pg.evaluate("""(n) => {
          try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) {}
          return false; }""", "A_fong_push1")
        print("StoryPlay.start(A_fong_push1):", ok, flush=True)
        assert ok
        pg.wait_for_timeout(1500)
        story_measures = step_story_measure(pg, "fong")
        LOG["phases"]["B4story"] = story_measures
        # 行完 beats 會停喺抉擇屏（唔係地圖）：揀第一個選項 → 結算 modal → 撳掣返地圖
        pg.wait_for_timeout(800)
        picked = pg.evaluate("""() => { const c = document.querySelector('.sp-choice');
          if (c) { c.click(); return c.textContent.slice(0,30); } return null; }""")
        print("story choice picked:", picked, flush=True)
        pg.wait_for_timeout(1500)
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續", "返回地圖"], 900):
                break
        pg.wait_for_timeout(800)
        map_on = pg.evaluate("""() => {
          const v = document.getElementById('v-map');
          const btn = [...document.querySelectorAll('button')].find(b => (b.textContent||'').includes('中環廣告') && b.offsetParent !== null);
          return {mapOn: !!(v && v.classList.contains('on')), hasAdBtn: !!btn}; }""")
        print("back on map:", map_on, flush=True)
        LOG["phases"]["B4storyReturn"] = map_on

        # ---------- B4 巧遇（新開一局，fresh session；drive126 同款做法） ----------
        # 有機觸發喺播完故事嘅同一局入面連續 12 日都唔中（見 drive131.json／dbg_enc3；
        # 懷疑係故事後狀態／行程干擾，唔係 B4 改動——enc79 攔截本身冇掂過），改用 fresh 局
        #（dbg_enc.py 實證：fresh 局 day 1 即觸發），同 drive126 每 phase new_game 一致。
        print("== B4 enc (fresh game) ==", flush=True)
        assert new_game(pg)
        pg.wait_for_timeout(1200)
        pg.evaluate("""(a) => {
          S.stars = S.stars || {};
          const st = S.stars[a.star] || (S.stars[a.star] = {});
          st.met = true; st.fav = a.fav; st.beatsDone = {}; st.poolSeen = {};
          st.heartDone = false; st.stage = 0; st.wrapEcho = false; st.capHit = false;
        }""", {"star": "pang_siuki", "fav": 5})
        enc_measures = []
        for day in range(0, 12):
            pg.evaluate("(d) => { S.dayIndex = d; }", day)
            # 確保身處地圖（上一日可能開咗地點 sheet 而冇巧遇）
            click_first(pg, ["返回地圖"], 700)
            pg.wait_for_timeout(400)
            map_ok = pg.evaluate("""() => {
              const v = document.getElementById('v-map');
              const btn = [...document.querySelectorAll('button')].find(b => (b.textContent||'').includes('中環廣告') && b.offsetParent !== null);
              return !!(v && v.classList.contains('on') && btn); }""")
            if not map_ok:
                print(f"  enc day {day}: 地圖唔可見，跳過", flush=True)
                continue
            click_first(pg, ["中環廣告"], 1800)
            pg.wait_for_timeout(1000)
            info = pg.evaluate(JS_ENC_MEASURE)
            state = pg.evaluate("""() => {
              const sheet = document.getElementById('loc-sheet');
              const toast = document.querySelector('.toast');
              return {sheetOn: !!sheet && sheet.classList.contains('on'),
                      toast: toast ? toast.textContent.slice(0, 60) : '',
                      travel: (window.S && S.travel114) ? S.travel114 : null}; }""")
            if not info.get("present"):
                print(f"  enc day {day}: 冇觸發 sheetOn={state['sheetOn']} toast={state['toast']!r} travel={state['travel']}", flush=True)
                continue
            print(f"  enc overlay day {day}", flush=True)
            enc_measures = step_enc_measure(pg, "pang")
            break
        LOG["phases"]["B4enc"] = enc_measures
        click_first(pg, ["返回地圖"], 700)

        LOG["errors"] = errs
        LOG["http404"] = http404
        print("PAGEERRORS:", errs[:10], flush=True)
        print("HTTP404:", http404[:10], flush=True)
        json.dump(LOG, open(os.path.join(HERE, "drive131.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("LOG qa131/drive131.json", flush=True)
        b.close()
finally:
    stop(srv)
