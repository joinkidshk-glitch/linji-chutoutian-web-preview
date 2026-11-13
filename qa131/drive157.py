# -*- coding: utf-8 -*-
"""v20a157 實駕 drive157：N1-N5 全程試玩＋關鍵閘＋審計斷裂逐支驗＋F4/G4＋C17。
用法：/home/hatch/pwenv49/bin/python qa131/drive157.py
Mirror：工作副本 ~/workspace/linji-work157，port 8971，390x844，?softPreview=1。
播種：localStorage key starVolunteer_map_v19w slot 1（經 new_game 正常開局後再 seed S 欄位）。
量度：逐句行 StoryPlay（#modal-btns 首掣），記低每句講者＋首 60 字；抉擇屏撳 .sp-choice。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work157"
HERE = os.path.join(ROOT, "qa131")
SHOTS = os.path.join(HERE, "shots157")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8971
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


JS_STORY_STATE = """() => {
  const plate = document.querySelector('.story-play .dlg106-plate');
  const choice = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
  const line = plate ? plate.querySelector('.sp-line') : null;
  const spk = plate ? plate.querySelector('.sp-speaker') : null;
  const title = document.querySelector('.story-play .sp-title, .story-play h2, .story-play h3');
  return {active: !!plate,
    speaker: spk ? spk.textContent : null,
    text: line ? line.textContent.slice(0, 120) : null,
    textLen: line ? line.textContent.length : 0,
    title: title ? title.textContent.slice(0, 40) : null,
    choices: choice.map(c => (c.textContent||'').trim().slice(0, 40)),
    modalBtns: (()=>{ const r=document.getElementById('modal-btns');
      return r ? [...r.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(b=>(b.textContent||'').trim().slice(0,20)) : []; })()
  };
}"""

JS_SHEET_BTNS = """() => {
  const els=[...document.querySelectorAll('#loc-sheet button, #loc-sheet [role=button], #loc-sheet a')].filter(e=>e.offsetParent!==null);
  return els.map(e=> (e.innerText||e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,60));
}"""


def story_active(pg):
    return pg.evaluate(JS_STORY_STATE)


def step_story(pg, tag, max_steps=40):
    """逐句行主線；回傳 {lines:[{spk,text}], choices:[...]}。"""
    lines = []
    for step in range(max_steps):
        pg.wait_for_timeout(900)
        m = story_active(pg)
        if not m.get("active"):
            break
        if m.get("choices"):
            return {"lines": lines, "choices": m["choices"], "title": m.get("title")}
        if m.get("text"):
            # 等 reveal 完成（長度穩定）
            pg.wait_for_timeout(500)
            m2 = story_active(pg)
            if m2.get("text") and len(m2["text"]) >= len(m["text"]):
                m = m2
            lines.append({"spk": m.get("speaker"), "text": m.get("text")})
            print(f"  STORY {tag}[{step}] spk={m.get('speaker')} txt={m.get('text')}", flush=True)
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            break
        pg.wait_for_timeout(400)
    m = story_active(pg)
    return {"lines": lines, "choices": m.get("choices") or [], "title": m.get("title")}


def pick_choice(pg, idx=0):
    picked = pg.evaluate("""(i) => { const c = [...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
      if (!c[i]) return null; const t = c[i].textContent.slice(0,40); c[i].click(); return t; }""", idx)
    pg.wait_for_timeout(1500)
    return picked


def dismiss_result(pg):
    for _ in range(5):
        if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續", "返回地圖"], 900):
            break
    pg.wait_for_timeout(600)


LOC_IDS = {"何生事務所": "agency_ho", "星河電視台": "tvb_longmen", "天星音樂": "rec_star"}
# 地圖地點係 .pin 掣（class 尾係地點 type）：文字掣／#map-area-list 都搵唔到嗰陣
# 用 pin click（probe_e2/e3 實證：#map-area-list button[data-loc] 喺地圖畫面係 missing，
# 文字掣亦撳唔到；.pin.agency 唯一，tv/music 有多個同 type pin，唔好用佢哋做 pin fallback）。
LOC_PIN = {"何生事務所": "agency"}


def click_btn_containing(pg, needle, wait=1200, scope=None):
    """按子字串撳可見掣（全文比對，唔經截斷文字；回傳全文或 None）。
    scope：CSS selector，限死範圍（例如 '#loc-sheet'）；唔傳即全頁——
    全頁只適用於字串夠獨特嘅場合（G4 卡名），sheet offer 一定要傳 scope，
    否則「劇情」呢類通字會誤撳支線掣（run2d C4 誤播曉晴支線就係咁嚟）。"""
    txt = pg.evaluate("""(args) => {
      const root = args.scope ? document.querySelector(args.scope) : document;
      if (!root) return null;
      const els=[...root.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').includes(args.n);});
      if(!els.length) return null; const t=els[0].innerText; els[0].click(); return t; }""",
      {"n": needle, "scope": scope})
    pg.wait_for_timeout(wait)
    return txt


def open_location_ui(pg, name, dismiss_intercept=True):
    """地圖撳地點名入 sheet；回傳 sheet 掣清單（或 None）。
    dismiss_intercept：入場撞正 enc79 巧遇攔截嗰陣，係咪即刻清走 overlay
    等 sheet render。預設 True（Phase A/E：要 sheet 唔要 overlay）。
    Phase D 掃描一定要傳 False——佢要 overlay 留低先認到係邊粒星，
    自己讀完 meta 先 dismiss；傳 True 會令 D 永遠捉唔到程天諾（run4 教訓：
    ching＋陸柏言兩次攔截都喺 D 讀 meta 之前俾清走咗）。"""
    dismiss_encounter(pg)
    click_first(pg, ["返回地圖"], 700)
    pg.evaluate("() => { const v=document.getElementById('v-map'); if(v && !v.classList.contains('on')){ const b=[...document.querySelectorAll('button')].find(x=>(x.textContent||'').includes('地圖') && x.offsetParent!==null); if(b) b.click(); } }")
    pg.wait_for_timeout(600)
    hit = click_first(pg, [name], 1800)
    if hit is None and name in LOC_IDS:
        ok = pg.evaluate("""(lid) => {
          const b = document.querySelector('#map-area-list button[data-loc="'+lid+'"]');
          if (!b || b.offsetParent === null) return false; b.click(); return true; }""", LOC_IDS[name])
        pg.wait_for_timeout(1000)
        if ok:
            hit = name
    if hit is None and name in LOC_PIN:
        ok = pg.evaluate("""(cls) => {
          const pin = document.querySelector('.pin.'+cls);
          if (!pin || pin.offsetParent === null) return false; pin.click(); return true; }""", LOC_PIN[name])
        pg.wait_for_timeout(1200)
        if ok:
            hit = name
    pg.wait_for_timeout(1000)
    if hit is None:
        return None
    # enc79 攔截：入場嗰陣有星在場（兼無主線待播壓住）會先彈全屏巧遇，
    # sheet 要等巧遇完先 render。唔清走 overlay，sheet 得返「返回地圖」。
    # （run3 Phase E：C1 已 done → agency 無主線待播壓住，day 900 開事務所
    # 撞正巧遇攔截，F4 卡撳唔到；probe_e5 實證 ovInDom=true、sheet 空。
    # 反證：probe_e4 fresh 局 C1 未 done，主線壓住攔截，開門即見 sheet。）
    if not dismiss_intercept:
        return pg.evaluate(JS_SHEET_BTNS)
    pg.wait_for_timeout(1200)
    ov_meta = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
      if(!ov) return null; const m=ov.querySelector('.e79-meta');
      return m ? m.textContent : 'overlay-no-meta'; }""")
    if ov_meta is not None:
        print(f"  open {name}: enc79 intercept ({ov_meta})，清走 overlay", flush=True)
        dismiss_encounter(pg)
        pg.wait_for_timeout(1200)
    return pg.evaluate(JS_SHEET_BTNS)


def dismiss_encounter(pg, max_clicks=16):
    """清走 enc79 overlay：有 skip 撳 skip，否則逐句撳到完（尾段抉擇撳第一項）。"""
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


def close_sheets(pg):
    """清走殘留 overlay／sheet，返地圖（Phase D→E 交接用）。"""
    dismiss_encounter(pg)
    click_first(pg, ["返回地圖"], 700)
    click_first(pg, ["關閉"], 500)
    pg.wait_for_timeout(500)


def try_offer_in_sheet(pg, needles, story_prefix=True):
    """喺 loc sheet 入面搵劇情 offer 掣撳落去；回傳撳到嘅掣文字或 None。
    story_prefix=True（主線 C1–C5）：只撳「播劇情：」開頭嘅掣，needle 必須喺
    offer 標題入面。「劇情」呢類通字絕對唔可以直接當 needle——支線掣全文都
    含「劇情」，run2d/run2e 就係咁誤撳咗曉晴支線，C4 播錯、C5 斷言死。
    story_prefix=False（F4 卡式掣，無「播劇情：」前綴）：限死 #loc-sheet
    範圍＋子字串，needle 本身要夠獨特（「去留」／「何生有句說話」）。"""
    btns = pg.evaluate(JS_SHEET_BTNS)
    print("  sheet buttons:", json.dumps(btns, ensure_ascii=False), flush=True)
    for n in needles:
        if story_prefix:
            got = pg.evaluate("""(nn) => {
              const root = document.querySelector('#loc-sheet'); if (!root) return null;
              const els=[...root.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
                const t=(e.innerText||'').trim();
                return e.getBoundingClientRect().width>0 && e.offsetParent!==null && t.startsWith('播劇情：') && t.includes(nn);});
              if(!els.length) return null; const t=els[0].innerText; els[0].click(); return t; }""", n)
        else:
            got = click_btn_containing(pg, n, 1500, scope="#loc-sheet")
            if got:
                return got
            continue
        pg.wait_for_timeout(1500)
        if got:
            return got
    if story_prefix:
        # 後備：撳第一個「播劇情：」開頭嘅掣
        got = pg.evaluate("""() => {
          const root = document.querySelector('#loc-sheet'); if (!root) return null;
          const els=[...root.querySelectorAll('button,[onclick],[role=button],a')].filter(e=>{
            const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim().startsWith('播劇情：');});
          if(!els.length) return null; const t=els[0].innerText; els[0].click(); return t; }""")
        pg.wait_for_timeout(1500)
        return got
    return None


def force_start(pg, node_id):
    return pg.evaluate("""(n) => {
      try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) { return 'ERR:'+_e; }
      return false; }""", node_id)


def plain_start(pg, node_id):
    return pg.evaluate("""(n) => {
      try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n); } } catch(_e) { return 'ERR:'+_e; }
      return false; }""", node_id)


def seed(pg, js):
    return pg.evaluate(js)


# IIFE-internal helpers 的等價 live 讀法（只用已暴露的 window.S / window.StoryOC；
# 函數體逐字對照 index.html：enc87StoryFlag L53058、enc83NodeDone L52890、
# enc79TierOf L51816、endingFlag410 L29216、ECHO89 表 L30175-30196）。
# 背景：主 script 由 L17 (function(){ 包住，上述函數／const 唔係 global，
# page.evaluate 直接叫會 ReferenceError（drive2 第一跑 C16 抉擇後死喺呢度）。
JS_D157_HELPERS = """() => {
  window.__d157_flag = (k) => { try {
    if (S.flags && S.flags[k]) return true;
    if (S.story && S.story.flags && S.story.flags[k]) return true;
  } catch(_e){} return false; };
  window.__d157_nodeDone = (id) => { try {
    if (typeof StoryOC !== "undefined" && StoryOC.isDone) return !!StoryOC.isDone(id);
  } catch(_e){}
    try { return Number((S.flags && S.flags["done_"+id]) || 0) > 0; } catch(_e){ return false; } };
  window.__d157_tier = (fav) => { const f = Number(fav)||0; return f>=70?4 : f>=45?3 : f>=25?2 : f>=10?1 : 0; };
  window.__d157_year = () => { const d = S.dayIndex; return 1990 + (d>=730?2 : d>=365?1 : 0); };
  window.__d157_echo89 = () => {
    const ECHO89 = [
      ["flag_role_cop", "你第一個畀人記住嘅戲路，係警察——企得穩嗰種正氣，成咗你嘅招牌之一。"],
      ["flag_role_gangster", "你第一個畀人記住嘅戲路，係黑幫——狠嗰段落足力，嗰種狠勁，成咗你嘅招牌之一。"],
      ["flag_fans_mediate", "樂壇前哨嗰場風波，你企中間調停——記者同歌迷都畀面你，嗰日之後，行內人對你改觀。"],
      ["flag_bing_bridge", "茶餐廳嗰次，你夠膽當場度橋畀廖炳星——星哥嗰種人，記人唔記戲，佢記住你。"],
      ["flag_chase_for_ho", "年尾嗰次，你幫何生追過數——把口講到明嗰種企硬，何生之後冇再試你。"],
      ["flag_canteen_grind", "電視台飯堂嗰排閒角，你熬得安安穩穩——嗰種捱法，係你嘅底子。"],
      ["flag_canteen_quit", "電視台飯堂嗰份閒角，你揀唔接，繼續跑通告搏機會——嗰種唔安份，推咗你行到呢度。"],
      ["flag_studio_follow", "大製作嗰期跟班，你由開鏡跟到殺青——成個廠點運作，你嗰期學晒。"],
      ["flag_studio_roam", "大製作嗰個跟班位，你揀唔接，繼續跑通告搏機會——嗰種唔安份，推咗你行到呢度。"],
      ["flag_stunt_refuse", "高危替身嗰次，你老實拒接——呢行唔係下下都要搏，識講「未到」，有時先行得遠。"],
      ["flag_miss_deflect", "嗰次記者圍攻，你引開咗支咪幫人擋——邊個幫過邊個，呢行啲人記性好到你唔信。"],
      ["flag_fans_support", "樂壇前哨嗰日，你留低幫歌迷打點派水——企到人上車嗰種耐性，唔係個個有。"],
      ["flag_fans_avoid", "樂壇前哨嗰場風波，你揀行後門避開——唔捲入，嗰次係啱嘅。"],
      ["flag_bing_background", "茶餐廳嗰次，你揀企喺背景唔搶風頭——嗰種分寸，後來救過你好多次。"],
      ["flag_rain_shelter", "暴雨嗰日，你揀保住套戲服——唔衝出去，唔代表冇膽，只係你知咩先最緊要。"],
      ["flag_newyear_script", "賀歲嗰次，你死背劇本一字不差——嗰種穩陣，監製嗰邊記低咗。"],
      ["flag_newyear_twotakes", "賀歲嗰次，你臨場改詞嗌多一個 take——嗰種執生，導演嗰邊記低咗。"],
      ["flag_wf1_studio_dream", "嗰日你講過想自己開公司——嗰粒種子，收科都仲喺度生根。"],
      ["flag_wf1_steady_craft", "你揀咗穩打穩扎磨手藝嗰條路——三年行落嚟，你嘅戲，係咁磨出嚟嘅。"],
      ["flag_wf1_gamble_observe", "賭枱邊嗰晚，你企喺側邊睇足全程——睇人賭，學到嘅嘢多過自己落場賭。"],
      ["flag_wf1_gamble_quiet", "賭枱邊嗰晚，你靜靜走開——嗰種唔埋枱嘅定力，救過你唔止一次。"],
      ["flag_wf3_m27_stand", "影人上街嗰陣，你企出嚟嗌過——嗰種企位，行內人記住。"],
      ["flag_wf3_m27_quiet", "影人上街嗰陣，你揀企後排睇清楚——唔出聲，唔代表冇諗法。"]
    ];
    const out = []; let n = 0;
    for (const [flag, line] of ECHO89) {
      if (n >= 3) break;
      const ok = !!((S.story && S.story.flags && S.story.flags[flag]) || (S.flags && S.flags[flag]) || (S.story && S.story.routes && S.story.routes[flag]));
      if (ok) { out.push(line); n++; }
    }
    return out;
  };
  return true;
}"""


def done_flags(pg):
    return pg.evaluate("""() => ({done: (S.story && S.story.done) || {},
      flags: (S.story && S.story.flags) || {}, day: S.dayIndex})""")


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

        # ---------- Phase A: N1-N5 UI 全程 ----------
        print("== Phase A: N1-N5 ==", flush=True)
        assert new_game(pg)
        assert pg.evaluate(JS_D157_HELPERS), "inject d157 helpers failed"
        phaseA = {}
        # C1: 事務所 offer（UI 路徑）
        btns = open_location_ui(pg, "何生事務所")
        print("  C1 sheet:", json.dumps(btns, ensure_ascii=False), flush=True)
        got = try_offer_in_sheet(pg, ["第一日", "冇價", "劇情"])
        via = "ui" if got else "force"
        if not got:
            print("  C1 offer 唔見，改行 force-start（記低）", flush=True)
            assert force_start(pg, "C1"), "force C1 failed"
        pg.wait_for_timeout(1200)
        r = step_story(pg, "C1")
        pg.screenshot(path=os.path.join(SHOTS, "c1_mid.png"))
        phaseA["C1"] = {"via": via, "offerBtn": got, "lines": len(r["lines"]),
                        "first": (r["lines"][0] if r["lines"] else None),
                        "choices": r["choices"]}
        assert r["choices"], "C1 無抉擇屏"
        print("  C1 pick:", pick_choice(pg, 0), flush=True)
        dismiss_result(pg)
        st = done_flags(pg)
        phaseA["C1"]["done"] = bool(st["done"].get("C1"))
        phaseA["C1"]["route_tv"] = bool(st["flags"].get("route_tv"))
        print("  C1 done/route_tv:", phaseA["C1"]["done"], phaseA["C1"]["route_tv"], flush=True)
        pg.screenshot(path=os.path.join(SHOTS, "c1_after.png"))

        # C2-C5：seed 日數＋地點 UI offer，唔得就 force-start
        plan = [("C2", 21, "星河電視台", ["後巷聽古", "劇情"], 0),
                ("C3", 35, "星河電視台", ["高仔搶鏡", "劇情"], 0),
                ("C4", 49, "何生事務所", ["何生攤記數簿", "劇情"], 1),
                ("C5", 56, "星河電視台", ["采兒", "劇情"], 0)]
        for nid, day, loc, needles, ch in plan:
            seed(pg, f"() => {{ S.dayIndex = {day}; }}")
            pg.wait_for_timeout(600)
            btns = open_location_ui(pg, loc)
            got = try_offer_in_sheet(pg, needles)
            via = "ui" if got else "force"
            if not got:
                assert force_start(pg, nid), f"force {nid} failed"
            pg.wait_for_timeout(1200)
            r = step_story(pg, nid)
            phaseA[nid] = {"via": via, "offerBtn": got, "lines": len(r["lines"]),
                           "first": (r["lines"][0] if r["lines"] else None),
                           "choices": r["choices"]}
            assert r["choices"], f"{nid} 無抉擇屏"
            print(f"  {nid} pick:", pick_choice(pg, ch), flush=True)
            dismiss_result(pg)
            st = done_flags(pg)
            phaseA[nid]["done"] = bool(st["done"].get(nid))
            print(f"  {nid} done:", phaseA[nid]["done"], flush=True)
            pg.screenshot(path=os.path.join(SHOTS, f"{nid.lower()}_after.png"))
        LOG["phases"]["A_N1_N5"] = phaseA

        # ---------- Phase B: 關鍵閘（non-force start） ----------
        print("== Phase B: gates ==", flush=True)
        gates = {}
        # C18：C5 done＋day 334 應開；day 300 唔應開
        seed(pg, "() => { S.dayIndex = 300; }")
        gates["C18_day300_no"] = plain_start(pg, "C18")
        dismiss_result(pg)
        seed(pg, "() => { S.dayIndex = 334; }")
        gates["C18_day334_yes"] = plain_start(pg, "C18")
        if gates["C18_day334_yes"]:
            pg.wait_for_timeout(1000)
            r = step_story(pg, "C18", max_steps=15)
            gates["C18_lines"] = len(r["lines"])
            gates["C18_first"] = r["lines"][0] if r["lines"] else None
            pg.screenshot(path=os.path.join(SHOTS, "c18_mid.png"))
            if r["choices"]:
                pick_choice(pg, 0)
            dismiss_result(pg)
        # C11：無 C7 唔開；有 C7＋1991 夏開
        seed(pg, "() => { S.dayIndex = 546; S.story.done.C7 = false; }")
        gates["C11_noC7_no"] = plain_start(pg, "C11")
        dismiss_result(pg)
        seed(pg, "() => { S.story.done.C7 = true; }")
        gates["C11_withC7_yes"] = plain_start(pg, "C11")
        if gates["C11_withC7_yes"]:
            pg.wait_for_timeout(1000)
            r = step_story(pg, "C11", max_steps=15)
            gates["C11_lines"] = len(r["lines"])
            gates["C11_beat2"] = r["lines"][1] if len(r["lines"]) > 1 else None
            pg.screenshot(path=os.path.join(SHOTS, "c11_mid.png"))
            if r["choices"]:
                pick_choice(pg, 0)
            dismiss_result(pg)
        # C15：無動作標籤唔開；有標籤＋C10 done＋1992 春開
        seed(pg, "() => { S.dayIndex = 790; S.story.done.C10 = true; S.castingTags = []; }")
        gates["C15_noTag_no"] = plain_start(pg, "C15")
        dismiss_result(pg)
        seed(pg, "() => { S.castingTags = [{id:'tag_action', label:'動作'}]; }")
        gates["C15_withTag_yes"] = plain_start(pg, "C15")
        if gates["C15_withTag_yes"]:
            pg.wait_for_timeout(1000)
            r = step_story(pg, "C15", max_steps=12)
            gates["C15_lines"] = len(r["lines"])
            pg.screenshot(path=os.path.join(SHOTS, "c15_mid.png"))
            if r["choices"]:
                pick_choice(pg, 0)
            dismiss_result(pg)
        # C17：day 1065＋award 未 resolve 唔開；award done 開；backstop day 1096 無條件開
        seed(pg, "() => { S.dayIndex = 1065; S.story.done.C13 = true; (S.awardsFlags=S.awardsFlags||{})['1992/award_singho_tv']=''; }")
        gates["C17_day1065_noAward_no"] = plain_start(pg, "C17")
        dismiss_result(pg)
        seed(pg, "() => { (S.awardsFlags=S.awardsFlags||{})['1992/award_singho_tv']='done'; }")
        gates["C17_day1065_awardDone_yes"] = plain_start(pg, "C17")
        if gates["C17_day1065_awardDone_yes"]:
            pg.wait_for_timeout(800)
            dismiss_result(pg)  # 唔播住，留返 Phase E 先播
        seed(pg, "() => { S.dayIndex = 1096; S.story.done.C13 = false; (S.awardsFlags=S.awardsFlags||{})['1992/award_singho_tv']=''; }")
        gates["C17_backstop1096_yes"] = plain_start(pg, "C17")
        if gates["C17_backstop1096_yes"]:
            pg.wait_for_timeout(800)
            dismiss_result(pg)
        LOG["phases"]["B_gates"] = gates
        print("gates:", json.dumps(gates, ensure_ascii=False), flush=True)

        # ---------- Phase C: 審計斷裂逐支驗（live） ----------
        print("== Phase C: audit flags ==", flush=True)
        audit = {}
        # C16_b 苦練 -> flag_vocal_train；ENC79_BEATS when() live 評估
        assert force_start(pg, "C16"), "force C16 failed"
        pg.wait_for_timeout(1000)
        r = step_story(pg, "C16", max_steps=24)
        assert r["choices"], "C16 無抉擇屏"
        print("  C16 pick b(苦練):", pick_choice(pg, 1), flush=True)
        dismiss_result(pg)
        audit["C16_train_flag"] = pg.evaluate("() => __d157_flag('flag_vocal_train')")
        audit["C16_done"] = pg.evaluate("() => __d157_nodeDone('C16')")
        audit["ching_after_train_when"] = pg.evaluate(
            "() => __d157_nodeDone('C16') && __d157_flag('flag_vocal_train')")
        audit["ching_after_polish_when_afterTrain"] = pg.evaluate(
            "() => __d157_nodeDone('C16') && __d157_flag('flag_vocal_polish')")
        # C9_c 兩邊拖 -> flag_mediate_gu_debt；gu_loan when() live 評估
        assert force_start(pg, "C9"), "force C9 failed"
        pg.wait_for_timeout(1000)
        r = step_story(pg, "C9", max_steps=24)
        print("  C9 pick c(兩邊拖):", pick_choice(pg, 2), flush=True)
        dismiss_result(pg)
        audit["C9_mediate_flag"] = pg.evaluate("() => __d157_flag('flag_mediate_gu_debt')")
        audit["gu_loan_when"] = pg.evaluate(
            "() => __d157_year()>=1991 && __d157_tier(60)>=2")
        # C14_c 兩邊都唔應死 -> flag_side_undecided；chai_repay when()
        assert force_start(pg, "C14"), "force C14 failed"
        pg.wait_for_timeout(1000)
        r = step_story(pg, "C14", max_steps=24)
        print("  C14 pick c:", pick_choice(pg, 2), flush=True)
        dismiss_result(pg)
        audit["C14_undecided_flag"] = pg.evaluate("() => __d157_flag('flag_side_undecided')")
        audit["chai_repay_when"] = pg.evaluate(
            "() => __d157_tier(60)>=2 && (__d157_flag('flag_side_film') || __d157_flag('flag_side_tv') || __d157_flag('flag_side_undecided') || __d157_nodeDone('C14'))")
        # C2_a 留低 -> flag_network_stay；C2_b -> flag_hustle_board。
        # STORY_FLAG_EVENT 本身係 IIFE-internal const（L47379），live 讀唔到；
        # 映射在位與否用靜態 grep 驗（同檔 index.html），live 只驗兩支旗真係寫入。
        _src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
        audit["network_map_present"] = ('flag_network_stay: "story:C2:network"' in _src
                                        and 'flag_hustle_board: "story:C2:hustle"' in _src)
        audit["network_flags_live"] = pg.evaluate(
            "() => ({stay: __d157_flag('flag_network_stay'), hustle: __d157_flag('flag_hustle_board')})")
        # wf1 四旗 -> ECHO89：endingInserts410 係 IIFE-internal（L30082），
        # 用 __d157_echo89 等價重演（同一張表＋同一 endingFlag410 口徑＋上限 3）。
        audit["wf1_echo"] = pg.evaluate("""() => {
          S.story.flags.flag_wf1_studio_dream = true;
          S.story.flags.flag_wf1_steady_craft = true;
          S.story.flags.flag_wf1_gamble_quiet = true;
          S.story.flags.flag_wf1_gamble_observe = true;
          const out = __d157_echo89();
          return {raw: out, filtered: out.filter(t => /開公司|穩打穩扎|賭枱|企枱邊/.test(t))};
        }""")
        audit["wf1_echo_raw"] = audit["wf1_echo"]["raw"]
        audit["wf1_echo"] = audit["wf1_echo"]["filtered"]
        # C5 alias 斷裂（outstanding）：裸名 choi_honest 寫入，但 flag_choi_honest 永遠唔中
        assert force_start(pg, "C5"), "force C5 failed"
        pg.wait_for_timeout(1000)
        r = step_story(pg, "C5", max_steps=24)
        print("  C5 pick a(老實說出):", pick_choice(pg, 0), flush=True)
        dismiss_result(pg)
        audit["C5_choi_honest_written"] = pg.evaluate("() => !!((S.story&&S.story.flags)||{}).choi_honest")
        audit["C5_flag_choi_honest_read"] = pg.evaluate("() => StoryOC.getFlag('flag_choi_honest')")
        LOG["phases"]["C_audit"] = audit
        print("audit:", json.dumps(audit, ensure_ascii=False), flush=True)

        # ---------- Phase D: 程天諾真觸發（after_train 對白） ----------
        print("== Phase D: ching encounter live trigger ==", flush=True)
        enc = {}
        # 用同一局：C16 已播＋train 旗已寫；set 1992 秋＋met/fav
        seed(pg, """() => {
          S.dayIndex = 973; S.story.done.C16 = true;
          S.story.flags.flag_vocal_train = true;
          S.stars = S.stars || {};
          S.stars.ching_tinlok = Object.assign({}, S.stars.ching_tinlok,
            {met:true, fav:50, beatsDone:{}, poolSeen:{}, heartDone:false, stage:0});
        }""")
        enc["when_live"] = pg.evaluate(
            "() => __d157_nodeDone('C16') && __d157_flag('flag_vocal_train')")
        # 逐日掃 973-1000：intercept 每日揀星（未做節拍優先，同分按名冊序），
        # 唔係程天諾就清走 overlay 繼續掃；用 .e79-meta 認星（run2c 只睇 .e79-name，
        # 第一句係旁白嗰陣名係空，誤將魏詠男當成目標）。
        fired = None
        seen = []
        for d in range(973, 1001):
            seed(pg, f"() => {{ S.dayIndex = {d}; }}")
            click_first(pg, ["返回地圖"], 700)
            pg.wait_for_timeout(400)
            btns = open_location_ui(pg, "天星音樂", dismiss_intercept=False)
            pg.wait_for_timeout(1200)
            ov = pg.evaluate("""() => { const ov = document.getElementById('enc79-overlay');
              if (!ov) return {present:false};
              const meta = ov.querySelector('.e79-meta');
              const line = ov.querySelector('.e79-line'); const name = ov.querySelector('.e79-name');
              return {present:true, meta: meta ? meta.textContent : null, name: name ? name.textContent : null,
                      text: line ? line.textContent.slice(0,100) : null}; }""")
            print(f"  enc day {d}:", json.dumps(ov, ensure_ascii=False), flush=True)
            if not ov.get("present"):
                close_sheets(pg)
                continue
            if "程天諾" not in (ov.get("meta") or ""):
                seen.append({"day": d, "meta": ov.get("meta"), "text": ov.get("text")})
                dismiss_encounter(pg)
                close_sheets(pg)
                continue
            fired = {"day": d, "ov": ov}
            pg.screenshot(path=os.path.join(SHOTS, "ching_enc.png"))
            # 行幾句對白，睇係咪 after_train 內容
            lines = []
            for _ in range(10):
                m = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
                  if(!ov) return null; const l=ov.querySelector('.e79-line');
                  return l ? l.textContent.slice(0,120) : null; }""")
                if not m:
                    break
                lines.append(m)
                clicked = pg.evaluate("""() => {
                  const ch=document.querySelector('.e79-choice'); if(ch){ch.click(); return 'choice';}
                  const nb=[...document.querySelectorAll('.e79-btn')].find(b=>b.offsetParent!==null);
                  if(nb){nb.click(); return 'next';} return null; }""")
                if not clicked:
                    break
                pg.wait_for_timeout(700)
            fired["lines"] = lines
            dismiss_encounter(pg)
            break
        enc["seen_other"] = seen
        enc["fired"] = fired
        LOG["phases"]["D_ching_enc"] = enc

        # ---------- Phase E: F4 / G4 UI ----------
        print("== Phase E: F4/G4 ==", flush=True)
        e = {}
        close_sheets(pg)  # run2c：Phase D 殘留 overlay 令開地點失敗，F4/G4 全 null
        # F4 季節閘：CHOICE47_DEFS F4_stay_mind year 1992 season 夏；
        # calendarSeason 月份制（6–8 月=夏）。day 881 = 1992-05-31 仍係春，
        # 卡唔出（run2f 就係咁）；邊界 day 882 = 1992-06-01。probe_e/e3 實證
        # day 890/900 卡出、撳到、播到。seed 900 留返 margin。
        seed(pg, "() => { S.dayIndex = 900; }")  # 1992-06-19 夏
        btns = open_location_ui(pg, "何生事務所")
        e["F4_sheet"] = btns
        got = try_offer_in_sheet(pg, ["去留", "何生有句說話"], story_prefix=False)
        e["F4_offer"] = got
        if got:
            pg.wait_for_timeout(1200)
            r = step_story(pg, "F4", max_steps=10)
            e["F4_lines"] = len(r["lines"])
            e["F4_first"] = r["lines"][0] if r["lines"] else None
            pg.screenshot(path=os.path.join(SHOTS, "f4_mid.png"))
            if r["choices"]:
                print("  F4 pick a(唔走):", pick_choice(pg, 0), flush=True)
                dismiss_result(pg)
                e["F4_flag_stay"] = pg.evaluate("() => __d157_flag('flag_stay_mind')")
        # G4：1992 冬返屋企——屋企唔係地圖地點（LOCS 無 home id，index.html
        # L51732 註明「LOCS 現時冇屋企地點」），地圖撳「屋企」永遠唔會成功
        # （run2f home_hit null 就係咁嚟）。正確路徑：☰ 選單 → 手帳 →
        # 人情頁 →「屋企有話同你講」卡 →「返屋企講清楚」。
        seed(pg, "() => { S.dayIndex = 1065; }")  # 1992-12-01 冬
        close_sheets(pg)
        pg.evaluate("""() => { const b=document.getElementById('btn-menu');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(800)
        home_open = pg.evaluate("""() => {
          const b = document.querySelector('#menu [data-m="journal"], #menu [data-m="home"]');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        if not home_open or not pg.evaluate("() => { const h=document.querySelector('.home'); return !!(h && h.offsetParent!==null); }"):
            # 後備：頂欄進度 chip 同樣入返手帳（enterHome progress）
            click_first(pg, ["進度"], 1200)
            pg.wait_for_timeout(1000)
        e["home_hit"] = home_open
        fav = pg.evaluate("""() => { const b=document.querySelector('#hgroup-favor');
          if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
        pg.wait_for_timeout(1200)
        e["favor_tab"] = fav
        got = pg.evaluate("""() => {
          const b = document.querySelector('[data-choice47="G4_family_job"]');
          if (!b || b.offsetParent === null) return null;
          const t = (b.innerText||'').trim(); b.click(); return t; }""")
        if not got:
            got = click_btn_containing(pg, "返屋企講清楚", 1500)
        e["G4_card"] = got
        if got:
            pg.wait_for_timeout(1200)
            r = step_story(pg, "G4", max_steps=10)
            e["G4_lines"] = len(r["lines"])
            e["G4_first"] = r["lines"][0] if r["lines"] else None
            pg.screenshot(path=os.path.join(SHOTS, "g4_mid.png"))
            if r["choices"]:
                print("  G4 pick b(繼續做落去):", pick_choice(pg, 1), flush=True)
                dismiss_result(pg)
                e["G4_flag_decline"] = pg.evaluate("() => __d157_flag('flag_family_job_decline')")
        LOG["phases"]["E_F4_G4"] = e

        # ---------- Phase F: C17 全程（fresh page，播完即結局） ----------
        print("== Phase F: C17 ==", flush=True)
        pg2 = ctx.new_page()
        pg2.on("pageerror", lambda er: errs.append("pg2: " + str(er)))
        assert new_game(pg2)
        seed(pg2, """() => {
          S.dayIndex = 1065; S.story.done.C13 = true;
          (S.awardsFlags=S.awardsFlags||{})['1992/award_singho_tv']='done';
        }""")
        ok17 = plain_start(pg2, "C17")
        f = {"gate_open": ok17}
        if ok17:
            pg2.wait_for_timeout(1200)
            # 用 pg2 行 beats：重用 step 邏輯（簡化版 inline）
            # 注意：抉擇屏行 .sp-choices-layout，.dlg106-plate 會消失——
            # 一定要先睇 choices 再睇 active（run2c 就係呢度斷錯，抉擇屏明明出咗都當播完）。
            lines = []
            for step in range(40):
                pg2.wait_for_timeout(900)
                m = pg2.evaluate(JS_STORY_STATE)
                if m.get("choices"):
                    f["choices"] = m["choices"]
                    break
                if not m.get("active"):
                    break
                if m.get("text"):
                    lines.append({"spk": m.get("speaker"), "text": m.get("text")})
                    print(f"  C17[{step}] spk={m.get('speaker')} txt={m.get('text')}", flush=True)
                clicked = pg2.evaluate("""() => { const row = document.getElementById('modal-btns');
                  if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
                  if (!bs.length) return false; bs[0].click(); return true; }""")
                if not clicked:
                    break
                pg2.wait_for_timeout(400)
            f["lines"] = len(lines)
            f["first"] = lines[0] if lines else None
            f["meeting_room"] = any("會議室" in (l["text"] or "") for l in lines)
            f["taiwan"] = any("台灣" in (l["text"] or "") for l in lines)
            pg2.screenshot(path=os.path.join(SHOTS, "c17_mid.png"))
            if f.get("choices"):
                picked = pg2.evaluate("""() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
                  if(!c[0]) return null; const t=c[0].textContent.slice(0,40); c[0].click(); return t; }""")
                f["picked"] = picked
                pg2.wait_for_timeout(2500)
                pg2.screenshot(path=os.path.join(SHOTS, "c17_after_choice.png"))
                f["ending410"] = pg2.evaluate("() => S.ending410 ? {career: S.ending410.career, eveKey: S.ending410.eveKey} : null")
                f["ending_body_snippet"] = pg2.evaluate("() => (document.body.innerText||'').replace(/\\s+/g,' ').slice(0,300)")
            else:
                # 無抉擇屏：播完就係咁完，記低結局狀態（S.ending410 應為 null）
                pg2.wait_for_timeout(2000)
                pg2.screenshot(path=os.path.join(SHOTS, "c17_ending.png"))
                f["ending410"] = pg2.evaluate("() => S.ending410 ? {career: S.ending410.career, eveKey: S.ending410.eveKey} : null")
                f["ending_body_snippet"] = pg2.evaluate("() => (document.body.innerText||'').replace(/\\s+/g,' ').slice(0,300)")
        LOG["phases"]["F_C17"] = f
        print("C17:", json.dumps(f, ensure_ascii=False), flush=True)

        LOG["errors"] = errs
        LOG["http404"] = http404
        print("PAGEERRORS:", errs[:10], flush=True)
        print("HTTP404:", http404[:10], flush=True)
        json.dump(LOG, open(os.path.join(HERE, "drive157.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("LOG qa131/drive157.json", flush=True)
        b.close()
finally:
    stop(srv)
