# -*- coding: utf-8 -*-
"""v20a202 實駕 drive202：B1 日結板／休息卡／劇情結算去向行＋B2 dismiss 提示＋C1 取消＋C2 故事鎖死提示 × 932／700。
用法：/home/hatch/pwenv49/bin/python qa202/drive202.py [--only <key>] [--vp 932|700|both]
Mirror：工作副本 ~/workspace/linji-work202，port 8977，live 模式（唔用 ?softPreview=1）。
播種：經 new_game 正常開局（slot 3），再 live 改 S（weekPlan＋probe shoots＋paper/aud/wf4/fen/sick/award）＋saveQ()。
觸發（真實 UI 路徑，唔直叫 IIFE 內函數）：開茶餐廳 sheet → sheet「返回地圖」→
  goToMapForBrowse → kickScheduleIfNeeded（今日係強制拍攝日）→ resolvePlannedDay；
  soft／rest 日：地圖 #map-start-today → startTodayScheduleFromMap。
量度（DOM 為準，截圖只係記錄）：日結板掣列／dismiss 去向／晨鏈各環出現次序／
  強制播續鏈去向／故事鎖死操作／週末／病假／休息卡／殺青獎勵／加速／頒獎禮鎖死。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, sys, argparse

ROOT = "/home/hatch/workspace/linji-work202"
HERE = os.path.join(ROOT, "qa202")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8977
URL = f"http://127.0.0.1:{PORT}/index.html"
REPORT = {"errors": [], "http_fail": [], "runs": {}}

ap = argparse.ArgumentParser()
ap.add_argument("--only", default="", help="只跑指定 case key，例如 c1-932")
ap.add_argument("--vp", default="both", choices=["932", "700", "both"])
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


STATE_JS = """() => ({
  maskOn: document.getElementById('mask').classList.contains('on'),
  dayIndex: (typeof S!=='undefined') ? S.dayIndex : null,
  dateStr: (typeof S!=='undefined') ? S.dateStr : null,
  mapVisible: (()=>{ const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : null; })(),
  homeVisible: (()=>{ const v=document.querySelector('#v-home'); return v ? v.offsetParent!==null : null; })(),
  title: (()=>{ const h=document.querySelector('#modal-inner h3'); return h ? (h.textContent||'').trim() : null; })(),
  innerText: (()=>{ const m=document.querySelector('#modal-inner'); return m ? (m.textContent||'').slice(0,220) : ''; })(),
  modalBtns: [...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim()),
  story: !!document.querySelector('.story-play .dlg106-plate'),
  storyChoices: [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null).length,
  enc: !!document.getElementById('enc79-overlay'),
  ceremony: !!document.querySelector('.awd62-stage'),
  invite: (()=>{ const b=[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null).map(x=>(x.textContent||'').trim()); return b.includes('出席') && b.includes('推辭'); })(),
  resultModal: (()=>{ const m=document.querySelector('#modal-inner'); return !!(m && m.querySelector('.sp-done-tag')); })(),
  slot: (()=>{ try{ return (typeof FREEPLAY_FW!=='undefined' && FREEPLAY_FW) ? (FREEPLAY_FW._story165AfterCont ?? null) : 'n/a'; }catch(e){ return 'err'; } })()
})"""


def st(pg):
    return pg.evaluate(STATE_JS)


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


SEED_JS = """(spec) => {
  try {
    const wd = (d)=>((d%7)+7)%7;
    while (wd(S.dayIndex) !== 0) S.dayIndex += 1;  // 歸一化到星期一
    const today = S.dayIndex, twd = wd(today);
    S.stress = 10;
    S.homeEditable = false;
    if (S.conseq61) { S.conseq61.sick = null; S.conseq61.streak90 = 0; S.conseq61.streak80 = 0; S.conseq61.cooldownUntil = 0; S.conseq61.pendingEnding = null; }
    if (S.wf4) { S.wf4.pending = null; S.wf4.pendingDay = -99; S.wf4.lastDay = -99; S.wf4.fenFarewellDone = false; }
    S.wf4FenFarewell = null;
    S.pendingMorningPaper = null;
    S.newspaperLastPresentedDay = null;
    S.pendingAud = [];
    const g = (typeof GIGS !== 'undefined' ? GIGS.find(x=>x && x.type==='電影' && x.title) : null) || {id:'probe_gig', title:'探測片'};
    S.shoots = (S.shoots||[]).filter(x=>x && !String(x.id||'').startsWith('probe196'));
    S.shoots.push({id:'probe196w', gigId:g.id, title:g.title, type:'電影', totalDays:1, doneDays:0, pay:6000, fame:5, popularity:5, signedPaid:0});
    S.shoots.push({id:'probe196f', gigId:g.id, title:g.title+'（下日）', type:'電影', totalDays:3, doneDays:0, pay:9000, fame:5, popularity:5, signedPaid:0});
    S.weekPlan = S.weekPlan || [];
    for(let i=0;i<7;i++) S.weekPlan[i]='rest';
    (spec.plan||[]).forEach((p,i)=>{ if(i<7) S.weekPlan[i]=p; });
    const ex = spec.extras||{};
    if(ex.paper){
      S.newspaperQueue = (S.newspaperQueue||[]).filter(it=>it && it.eventKey!=='probe196_paper');
      S.newspaperQueue.push({eventKey:'probe196_paper', source:'wrap', enqueuedDay:today, publishDay:today,
        fameDelta:3, paperName:'娛樂版', headline:'探測報紙頭條', dek:'探測報紙內文。', clipLabel:'', rumorEcho:'',
        templateId:'', templateEventKey:'', medium:'tv', workTitle:'探測片', tone:'', boardScentTag:'',
        storyBeatId:'', choiceFlag:'', gated:'', paras:null, imgKey:'', worldId:'', press94:'', firstPress94:false});
    }
    if(ex.aud){
      S.pendingAud.push({gigId:'probe196_aud', title:'《探測片》配角', type:'電視劇', tier:'初', locId:'tvb_longmen',
        audDay:today-1, revealDay:today, wait:1, ok:true, chancePct:80, pay:900, payBase:900, payBonus:0,
        payBonusLabel:'', payNote:'', fame:5, pop:17, days:3, fxActing:0, fxStress:0, fxFame:0, fxStressFail:0, via:'board'});
    }
    if(ex.wf4){
      const st = (typeof wf4Ensure==='function') ? wf4Ensure() : S.wf4;
      if(st){ st.pending='wf4_ev_set01'; st.pendingDay=today; st.lastDay=-99; }
    }
    if(ex.fen){
      S.wf4FenFarewell = {wroteOff:false, exodused:false, day:today};
      if(S.wf4) S.wf4.fenFarewellDone=false;
    }
    if(ex.sick){
      if(S.conseq61){ S.conseq61.sick={from:today, to:today, days:1, done:{}, creditLost:0}; S.conseq61.cooldownUntil=0; }
    }
    let award=null;
    if(ex.award && window.__awards && window.__awards.debugForceSeasonWindow){
      try{ award = window.__awards.debugForceSeasonWindow('award_harbour_ad', {forceTier:'gallery'}); }catch(e){ award={err:String(e)}; }
    }
    try{ saveQ(); }catch(e){}
    return {ok:true, dayIndex:S.dayIndex, plan:S.weekPlan.slice(), award: award ? (award.ceremonyId||award.id||JSON.stringify(award).slice(0,120)) : null};
  } catch(e){ return {ok:false, err:String(e)}; }
}"""


def seed(pg, plan, extras=None):
    r = pg.evaluate(SEED_JS, {"plan": plan, "extras": extras or {}})
    print("  seed:", r, flush=True)
    assert r.get("ok"), f"seed failed {r}"
    return r


def ensure_on_map(pg):
    for _ in range(6):
        s = st(pg)
        if s["mapVisible"] and not s["maskOn"]:
            return True
        if s["story"]:
            play_story(pg); continue
        if s["resultModal"]:
            modal_click(pg, "關閉"); pg.wait_for_timeout(800); continue
        if s["maskOn"]:
            return False
        if js_click_text(pg, "返回地圖"):
            pg.wait_for_timeout(1000); continue
        pg.wait_for_timeout(500)
    return pg.evaluate("() => { const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : false; }")


DAYEND_RE = ("殺青", "街頭", "休息", "小休", "拍攝中", "拍攝日", "散工收工", "病倒休養")


def is_dayend(s):
    # 日結板必有繼續掣（開始今日行程／返回地圖／回家結算）；報紙 modal 標題都含「殺青」但得「收下這份剪報」，唔計
    return bool(s["maskOn"] and s["title"] and any(k in s["title"] for k in DAYEND_RE)
                and any(b in s["modalBtns"] for b in ("開始今日行程", "返回地圖", "回家結算")))


def wait_dayend_modal(pg, timeout_ms=20000):
    """等日結板：中途可能有晨報／獎勵 modal／故事攔路，逐個撳穿佢哋（只撳非決策掣）。"""
    for _ in range(timeout_ms // 250):
        s = st(pg)
        if is_dayend(s):
            return s
        if s["story"]:
            play_story(pg)
        elif s["enc"]:
            dismiss_encounter(pg)
        elif s["ceremony"]:
            drive_ceremony(pg)
        elif s["maskOn"] and s["title"]:
            hit = False
            for t in ["收下這份反響", "收下這份剪報", "收下這晚", "好", "知道了", "關閉", "繼續", "下一句"]:
                if modal_click(pg, t):
                    hit = True; break
            if not hit:
                return s
        pg.wait_for_timeout(250)
    return st(pg)


def open_sheet_and_back_to_map(pg):
    """開茶餐廳 sheet → sheet「返回地圖」→ goToMapForBrowse。重試 3 次
    （開 sheet 嗰陣可能彈出 C2 等故事，播完關閉後 sheet 已閂，要重開）。"""
    for _attempt in range(3):
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
            continue
        dismiss_encounter(pg)
        if st(pg)["story"]:
            play_story(pg)
            pg.wait_for_timeout(800)
            modal_click(pg, "關閉")
            pg.wait_for_timeout(800)
        dismiss_encounter(pg)
        hit = pg.evaluate("""() => {
          const sh = document.getElementById('loc-sheet'); if (!sh) return false;
          const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === '返回地圖');
          if (!b) return false; b.click(); return true; }""")
        pg.wait_for_timeout(1500)
        if hit:
            return {"ok": True, "step": "sheet-back", "attempt": _attempt}
    return {"ok": False, "step": "open-sheet"}


def play_story(pg, max_steps=90):
    """播晒而家呢幕故事，直到故事 plate 消失（唔撳結果 modal 嘅掣，留返畀 case 決定）。"""
    log = []
    for _ in range(max_steps):
        s = st(pg)
        if not s["story"] and not s["storyChoices"]:
            return {"done": True, "log": log}
        if s["storyChoices"]:
            pg.evaluate("""() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
              if (c[0]) c[0].click(); }""")
            log.append("choice[0]")
            pg.wait_for_timeout(900)
            continue
        clicked = None
        for t in ["下一句", "繼續", "下一頁", "睇落去"]:
            if modal_click(pg, t):
                clicked = t; break
        if not clicked:
            # 兜底：撳第一粒非結果掣（結果掣：下一節／關閉／進度——唔撳）
            clicked = pg.evaluate("""() => { const bs=[...document.querySelectorAll('#modal-btns button')].filter(x=>x.offsetParent!==null);
              const b = bs.find(x=>['下一節','關閉','進度'].indexOf((x.textContent||'').trim())<0);
              if(!b) return null; const t=(b.textContent||'').trim(); b.click(); return t; }""")
        if not clicked:
            return {"done": False, "log": log, "state": st(pg)}
        log.append(clicked)
        pg.wait_for_timeout(800)
    s2 = st(pg)
    return {"done": (not s2["story"] and not s2["storyChoices"]), "log": log, "state": s2}


def drive_ceremony(pg, max_steps=40):
    """播晒頒獎典禮：撳跳過 → 結果卡收下這晚。"""
    for _ in range(max_steps):
        s = st(pg)
        if not s["ceremony"]:
            return True
        hit = pg.evaluate("""() => { const b=document.querySelector('.awd62-skip');
          if (b && b.offsetParent!==null) { b.click(); return true; } return false; }""")
        if hit:
            pg.wait_for_timeout(1500); continue
        # 舞台冇跳過掣：撳畫面快進／等 beats 行完
        pg.evaluate("""() => { const f=document.querySelector('.awd62-frame'); if(f) f.click(); }""")
        pg.wait_for_timeout(1500)
    return not st(pg)["ceremony"]


def mask_click(pg):
    """喺 modal 外嘅 mask 位撳一下（dismiss）。成功＝原本嗰個 modal 唔見咗
    （閂咗，或者 dismiss 後行咗去下一環、出咗新 modal——例如日結板 dismiss 後即出獎勵 sheet）。"""
    before = st(pg)
    if not before["maskOn"]:
        return False
    sig_before = (before["title"], tuple(before["modalBtns"]))
    def gone():
        s = st(pg)
        return (not s["maskOn"]) or ((s["title"], tuple(s["modalBtns"])) != sig_before)
    pt = pg.evaluate("""() => {
      const mi = document.querySelector('#modal-inner'); if (!mi) return null;
      const r = mi.getBoundingClientRect();
      if (r.top > 60) return {x: Math.round(r.left + r.width/2), y: Math.round(r.top - 25)};
      if (r.left > 60) return {x: Math.round(r.left - 25), y: Math.round(r.top + r.height/2)};
      return null; }""")
    if pt:
        pg.mouse.click(pt["x"], pt["y"])
        pg.wait_for_timeout(900)
        if gone():
            return True
    pg.evaluate("""() => { const m=document.getElementById('mask'); if(!m) return false;
      m.dispatchEvent(new MouseEvent('click', {bubbles:true})); return true; }""")
    pg.wait_for_timeout(900)
    return gone()


def pump_chain(pg, max_steps=48):
    """由日結板撳「開始今日行程」之後，一路撳穿晨鏈各環，直到停喺決策點。
    返 (stop, events)：stop ∈ map / dayend / confirm / invite / result / ceremony / stuck / timeout。
    events：沿途見過嘅環（reward/paper/aud/wf4/award-invite/forced-story…次序）。"""
    events = []
    for i in range(max_steps):
        pg.wait_for_timeout(500)
        s = st(pg)
        if s["enc"]:
            dismiss_encounter(pg); events.append("enc79"); continue
        if s["ceremony"]:
            events.append("ceremony-stage"); return ("ceremony", events)
        if s["story"]:
            events.append("story:" + (s["title"] or ""))
            r = play_story(pg)
            events.append("story-done:" + str(r.get("done")))
            continue
        if s["resultModal"]:
            events.append("result-modal"); return ("result", events)
        if not s["maskOn"] and s["mapVisible"]:
            events.append("map"); return ("map", events)
        if s["maskOn"] and s["title"]:
            t = s["title"]
            if is_dayend(s):
                events.append("dayend:" + t); return ("dayend", events)
            if s["invite"]:
                events.append("invite:" + t); return ("invite", events)
            if "加速本週剩餘" in t:
                events.append("accel-confirm"); return ("accel-confirm", events)
            if "開始今日行程" in s["modalBtns"]:
                events.append("confirm:" + t); return ("confirm", events)
            if "收下這份反響" in s["modalBtns"]:
                events.append("reward"); modal_click(pg, "收下這份反響"); continue
            if "收下這份剪報" in s["modalBtns"]:
                events.append("paper"); modal_click(pg, "收下這份剪報"); continue
            if "收下這晚" in s["modalBtns"]:
                events.append("award-result"); modal_click(pg, "收下這晚"); continue
            if "何生來電" in t or ("獲聘" in t):
                events.append("aud:" + t); modal_click(pg, "好"); continue
            if "日常" in t or "wf4" in (t or "").lower():
                events.append("wf4-modal:" + t)
                if not modal_click(pg, "好"):
                    modal_click(pg, s["modalBtns"][0] if s["modalBtns"] else "")
                continue
            # 其他中途 modal：WF4 事件 modal（標題＝事件名）／抉擇——撳「好」或第一粒掣
            if s["modalBtns"]:
                b0 = s["modalBtns"][0]
                events.append("modal:" + t + ":" + b0)
                if b0 in ("開始今日行程", "返回地圖"):
                    return ("decision:" + b0, events)
                modal_click(pg, b0); continue
            return ("stuck-modal", events)
        if not s["maskOn"] and not s["mapVisible"]:
            if s["homeVisible"]:
                events.append("home"); return ("home", events)
            return ("nomask-nomap", events)
    return ("timeout", events)


def pump_until(pg, wants, max_rounds=4):
    """一路 pump，直到停喺 wants 其中一個決策點；中途結果 modal（強制故事播完）
    照撳「關閉」（跟 slot 去向），逐個記錄。返 (stop, all_events)。"""
    all_ev = []
    for _ in range(max_rounds):
        stop, events = pump_chain(pg)
        all_ev += events
        if stop in wants:
            return (stop, all_ev)
        if stop == "result":
            if modal_click(pg, "關閉"):
                pg.wait_for_timeout(900)
                all_ev.append("result-closed")
                continue
            return (stop, all_ev)
        return (stop, all_ev)
    return ("timeout", all_ev)


def start_today_from_map(pg):
    """由地圖開始今日行程（soft 日：street／rest）：先試地圖 hint 嘅 #map-start-today；
    settle 後 hint 係按開局預設 plan 渲染，掣可能唔存在——後備經手帳（menu→手帳→行程頁
    #home-back-map「開始今日行程」，按 seeded plan 渲染，data-mode=start-today），
    行 startTodayScheduleFromMap → resolvePlannedDay（開頭有病假守衛，sick 會出病假板）。
    返 map-btn／home-btn／False。"""
    hit = pg.evaluate("""() => { const b=document.getElementById('map-start-today');
      if(!b || b.offsetParent===null) return false; b.click(); return true; }""")
    if hit:
        return "map-btn"
    pg.evaluate("""() => { const m=document.getElementById('btn-menu'); if(m) m.click(); return true; }""")
    pg.wait_for_timeout(600)
    hit2 = pg.evaluate("""() => { const b=document.querySelector('#menu button[data-m="journal"]');
      if(!b || b.offsetParent===null) return false; b.click(); return true; }""")
    if not hit2:
        return False
    pg.wait_for_timeout(1000)
    hit3 = pg.evaluate("""() => { const b=document.getElementById('home-back-map');
      if(!b || b.offsetParent===null) return false; b.click(); return true; }""")
    return "home-btn" if hit3 else False


def trigger_map_chain(pg):
    """經真實 UI 路徑入地圖（屋企→返回地圖；地圖→開 sheet→返回地圖）。
    注意：sheet-back（#loc-close）只係 closeSheet＋story165TryForcedPlay，唔行晨鏈；
    想行晨鏈要用日結板掣（runScheduleFromToday／goToMapForBrowse）或 start_today_from_map。
    唔消費鏈入面彈出嘅嘢（invite／故事／板），留返畀 case 處理。"""
    s = st(pg)
    if s["homeVisible"] and not s["maskOn"]:
        js_click_text(pg, "返回地圖")
    elif s["mapVisible"] and not s["maskOn"]:
        for _try in range(2):
            dismiss_encounter(pg)
            if not js_click_contains(pg, "茶餐廳", "#v-map"):
                break
            pg.wait_for_timeout(1200)
            dismiss_encounter(pg)
            if st(pg)["story"]:
                play_story(pg)
                pg.wait_for_timeout(800)
                modal_click(pg, "關閉")
                pg.wait_for_timeout(800)
            hit = pg.evaluate("""() => {
              const sh = document.getElementById('loc-sheet'); if (!sh) return false;
              const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === '返回地圖');
              if (!b) return false; b.click(); return true; }""")
            if hit:
                break
            pg.wait_for_timeout(500)
    pg.wait_for_timeout(1500)
    return st(pg)


def settle_opening(pg, max_steps=40):
    """開局 C1 會自動播：播晒佢＋關閉結果＋撳穿 B01，直到返到地圖／屋企閒置狀態。"""
    for _ in range(max_steps):
        s = st(pg)
        if s["story"]:
            play_story(pg); continue
        if s["resultModal"]:
            modal_click(pg, "關閉"); pg.wait_for_timeout(800); continue
        if s["enc"]:
            dismiss_encounter(pg); continue
        if s["ceremony"]:
            drive_ceremony(pg); continue
        if s["maskOn"]:
            if modal_click(pg, "知道了") or modal_click(pg, "好") or modal_click(pg, "關閉"):
                pg.wait_for_timeout(700); continue
            if modal_click(pg, "返回地圖"):
                pg.wait_for_timeout(900); continue
            if pg.evaluate("() => { const b=[...document.querySelectorAll('#modal-btns button')].filter(e=>e.offsetParent!==null); if(b[0]){b[0].click(); return true;} return false; }"):
                pg.wait_for_timeout(700); continue
            return False
        if s["mapVisible"] or s["homeVisible"]:
            return True
        pg.wait_for_timeout(500)
    s = st(pg)
    return bool(s["mapVisible"] or s["homeVisible"])


def settle_to_map(pg, max_rounds=8):
    for _ in range(max_rounds):
        s = st(pg)
        if s["mapVisible"] and not s["maskOn"]:
            return True
        if s["enc"]:
            dismiss_encounter(pg); continue
        if s["story"]:
            play_story(pg); continue
        if s["ceremony"]:
            drive_ceremony(pg); continue
        if s["maskOn"]:
            if modal_click(pg, "返回地圖"):
                pg.wait_for_timeout(900); continue
            if modal_click(pg, "回家結算"):
                pg.wait_for_timeout(1200); ensure_on_map(pg); continue
            if modal_click(pg, "開始今日行程"):
                pg.wait_for_timeout(900); continue
            if modal_click(pg, "好") or modal_click(pg, "關閉") or modal_click(pg, "知道了"):
                pg.wait_for_timeout(900); continue
            if pg.evaluate("() => { const b=[...document.querySelectorAll('#modal-btns button')].filter(e=>e.offsetParent!==null); if(b[0]){b[0].click(); return true;} return false; }"):
                pg.wait_for_timeout(900); continue
            return False
        if ensure_on_map(pg):
            return True
        return False
    return pg.evaluate("() => { const v=document.querySelector('#v-map'); return v ? v.offsetParent!==null : false; }")

# ============================== cases ==============================

def fresh(pw, vp):
    ctx = pw.chromium.launch(executable_path=EXE, headless=True, args=["--no-sandbox"])
    pg = ctx.new_page(viewport={"width": 390, "height": vp})
    pg.on("pageerror", lambda e: REPORT["errors"].append(str(e)))
    pg.on("console", lambda m: REPORT["errors"].append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    pg.on("response", lambda r: REPORT["http_fail"].append((r.status, r.url)) if r.status >= 400 else None)
    return ctx, pg


def shot(pg, name):
    try:
        pg.screenshot(path=os.path.join(SHOTS, name + ".png"))
    except Exception:
        pass


def run_case(pw, vp, key, fn):
    if ARGS.only and ARGS.only not in key:
        return None
    err0 = len(REPORT["errors"])
    ctx, pg = fresh(pw, vp)
    res = {"key": key, "vp": vp, "pass": False, "evidence": {}, "pageerrors": []}
    try:
        ok = new_game(pg)
        assert ok, "new_game failed"
        if not getattr(fn, "_no_settle", False):
            settled = settle_opening(pg)
            res["evidence"]["settled_opening"] = settled
            assert settled, "settle_opening failed"
        fn(pg, res)
        res["pass"] = True
    except Exception as e:
        res["error"] = str(e)
        print(f"  !! {key} EXC: {e}", flush=True)
    finally:
        res["pageerrors"] = REPORT["errors"][err0:]
        REPORT["runs"][key] = res
        print(f"== {key} {'PASS' if res['pass'] else 'FAIL'} errors={len(res['pageerrors'])} ev={json.dumps(res['evidence'], ensure_ascii=False)[:600]}", flush=True)
        try:
            ctx.close()
        except Exception:
            pass
    return res


def ev(pg, res, k, v):
    res["evidence"][k] = v
    return v


# ============================== cases ==============================
# ============================== cases ==============================

def nextline_geom(pg):
    """返 .dayend-next202 嘅量度：文字＋viewport 座標＋modal-inner 可見窗。
    第一屏可見＝成行喺 modal-inner 可見窗（唔使碌）之內。"""
    return pg.evaluate("""() => {
      const el = document.querySelector('#modal-inner .dayend-next202');
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const mi = document.getElementById('modal-inner');
      const mr = mi ? mi.getBoundingClientRect() : null;
      return {text: (el.textContent||'').trim(), top: Math.round(r.top), bottom: Math.round(r.bottom),
              vh: window.innerHeight, miTop: mr ? Math.round(mr.top) : null,
              miVisibleBottom: mr ? Math.round(Math.min(mr.bottom, window.innerHeight)) : null,
              miScrollTop: mi ? mi.scrollTop : null};
    }""")


def note_texts(pg):
    """#modal-btns 入面可見嘅 .modal-note202 文字（role:note 純文字，唔係掣）。"""
    return pg.evaluate("""() => [...document.querySelectorAll('#modal-btns .modal-note202')]
      .filter(e => e.offsetParent !== null).map(e => (e.textContent||'').trim())""")


def result_inner(pg):
    return pg.evaluate("""() => { const m = document.querySelector('#modal-inner');
      return m ? (m.textContent||'') : ''; }""")


def story_note_visible(pg):
    return pg.evaluate("""() => {
      const notes = [...document.querySelectorAll('#modal-btns .modal-note202')]
        .filter(e => e.offsetParent !== null).map(e => (e.textContent||'').trim());
      return notes; }""")


def b1a(pg, res):
    """B1 行程日：Mon shoot → Tue street 板，聽日行喺第一屏見到。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s), f"expected Mon wrap board, got {s}"
    g = nextline_geom(pg)
    ev(pg, res, "board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"], "geom": g})
    assert g and g["text"] == "聽日：街頭表演（自動行程）", f"next line wrong: {g}"
    assert g["top"] >= g["miTop"] and g["bottom"] <= g["miVisibleBottom"], f"next line NOT first-screen: {g}"
    shot(pg, f"b1a-board-{res['vp']}")


def b1b(pg, res):
    """B1 逛逛日：Mon shoot → Tue scout_all 板，聽日行喺第一屏見到。"""
    seed(pg, ["shoot:probe196w", "scout_all", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s), f"expected Mon wrap board, got {s}"
    g = nextline_geom(pg)
    ev(pg, res, "board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"], "geom": g})
    assert g and g["text"] == "聽日：到處逛逛（返地圖自由行）", f"next line wrong: {g}"
    assert g["top"] >= g["miTop"] and g["bottom"] <= g["miVisibleBottom"], f"next line NOT first-screen: {g}"
    shot(pg, f"b1b-board-{res['vp']}")


def b2a(pg, res):
    """B2 排程日：板底有 dismiss 提示；撳出面真係跑聽日街頭表演（唔係返地圖）。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s), f"expected Mon wrap board, got {s}"
    notes = note_texts(pg)
    ev(pg, res, "board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"], "notes": notes})
    assert "撳出面＝繼續跑聽日行程" in notes, f"dismiss note missing: {notes}"
    d0 = s["dayIndex"]
    shot(pg, f"b2a-board-{res['vp']}")
    assert mask_click(pg), "mask dismiss failed"
    stop, events = pump_until(pg, {"dayend", "map"})
    s = st(pg)
    ev(pg, res, "after_dismiss", {"stop": stop, "events": events, "title": s["title"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s) and s["dayIndex"] == d0 + 1, \
        f"dismiss on scheduled day must run Tue street, got {stop} {s}"


def b2b(pg, res):
    """B2 逛逛日：板底有 dismiss 提示；撳出面真係返地圖。"""
    seed(pg, ["shoot:probe196w", "scout_all", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s), f"expected Mon wrap board, got {s}"
    notes = note_texts(pg)
    ev(pg, res, "board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"], "notes": notes})
    assert "撳出面＝返地圖" in notes, f"dismiss note missing: {notes}"
    shot(pg, f"b2b-board-{res['vp']}")
    assert mask_click(pg), "mask dismiss failed"
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after_dismiss", {"stop": stop, "events": events, "map": s["mapVisible"], "day": s["dayIndex"]})
    assert s["mapVisible"] and not s["maskOn"], f"dismiss on map day must land on map, got {stop} {s}"


def c1a(pg, res):
    """C1 休息卡確認：有「取消（返去休息卡）」；取消真係返去休息卡（日唔郁）；
    再入確認，撳出面（dismiss）照跟 D1 跑聽日街頭表演。"""
    seed(pg, ["rest", "street", "rest", "rest", "rest", "rest", "rest"])
    assert start_today_from_map(pg), "cannot start Mon rest from map"
    stop, events = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "rest_card", {"stop": stop, "events": events, "title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s), f"expected Mon rest card, got {stop} {s}"
    g = nextline_geom(pg)
    notes = note_texts(pg)
    ev(pg, res, "rest_card_v202", {"geom": g, "notes": notes})
    assert g and g["text"] == "聽日：街頭表演（自動行程）", f"rest card next line wrong: {g}"
    assert g["top"] >= g["miTop"] and g["bottom"] <= g["miVisibleBottom"], f"rest card next line NOT first-screen: {g}"
    assert "撳出面＝繼續跑聽日行程" in notes, f"rest card dismiss note missing: {notes}"
    d_rest = s["dayIndex"]
    title0 = s["title"]
    shot(pg, f"c1a-restcard-{res['vp']}")
    assert modal_click(pg, "開始今日行程"), "no 開始今日行程 on rest card"
    pg.wait_for_timeout(900)
    s = st(pg)
    ev(pg, res, "confirm", {"title": s["title"], "btns": s["modalBtns"], "notes": note_texts(pg)})
    assert "取消（返去休息卡）" in s["modalBtns"], f"confirm has no 取消: {s}"
    assert "撳出面＝開始今日行程" in note_texts(pg), f"confirm dismiss note missing: {note_texts(pg)}"
    shot(pg, f"c1a-confirm-{res['vp']}")
    assert modal_click(pg, "取消（返去休息卡）"), "cannot click 取消"
    pg.wait_for_timeout(900)
    s = st(pg)
    ev(pg, res, "after_cancel", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert s["title"] == title0 and s["dayIndex"] == d_rest, \
        f"取消 must return to rest card (same day), got {s}"
    assert "開始今日行程" in s["modalBtns"], f"rest card lost 開始今日行程 after cancel: {s}"
    # 再入確認，dismiss（撳出面）照跟 D1 跑聽日
    assert modal_click(pg, "開始今日行程"), "no 開始今日行程 on rest card (2nd)"
    pg.wait_for_timeout(900)
    assert mask_click(pg), "confirm mask dismiss failed"
    stop, events = pump_until(pg, {"dayend", "map"})
    s = st(pg)
    ev(pg, res, "after_confirm_dismiss", {"stop": stop, "events": events, "title": s["title"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s) and s["dayIndex"] == d_rest + 1, \
        f"confirm dismiss must run Tue street, got {stop} {s}"


c1a._vps = [932]


def c1b(pg, res):
    """C1（700）：取消路徑同 c1a（淨驗取消返休息卡）。"""
    seed(pg, ["rest", "street", "rest", "rest", "rest", "rest", "rest"])
    assert start_today_from_map(pg), "cannot start Mon rest from map"
    stop, events = pump_until(pg, {"dayend"})
    s = st(pg)
    assert stop == "dayend" and is_dayend(s), f"expected Mon rest card, got {stop} {s}"
    d_rest = s["dayIndex"]
    title0 = s["title"]
    g = nextline_geom(pg)
    ev(pg, res, "rest_card", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"], "geom": g})
    assert g and g["text"] == "聽日：街頭表演（自動行程）", f"rest card next line wrong: {g}"
    assert g["top"] >= g["miTop"] and g["bottom"] <= g["miVisibleBottom"], f"rest card next line NOT first-screen: {g}"
    shot(pg, f"c1b-restcard-{res['vp']}")
    assert modal_click(pg, "開始今日行程"), "no 開始今日行程 on rest card"
    pg.wait_for_timeout(900)
    s = st(pg)
    assert "取消（返去休息卡）" in s["modalBtns"], f"confirm has no 取消: {s}"
    shot(pg, f"c1b-confirm-{res['vp']}")
    assert modal_click(pg, "取消（返去休息卡）"), "cannot click 取消"
    pg.wait_for_timeout(900)
    s = st(pg)
    ev(pg, res, "after_cancel", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert s["title"] == title0 and s["dayIndex"] == d_rest, \
        f"取消 must return to rest card (same day), got {s}"


c1b._vps = [700]


def c2a(pg, res):
    """C2 主線：C1 播放期間，掣列見到「劇情進行中，播完先可以離開」細字。
    （_no_settle：要喺 settle 之前捉到 C1 播放中。）"""
    for _ in range(60):
        s = st(pg)
        if s["story"]:
            break
        if s["resultModal"]:
            modal_click(pg, "關閉"); pg.wait_for_timeout(700); continue
        if s["enc"]:
            dismiss_encounter(pg); continue
        if s["maskOn"] and s["title"]:
            if modal_click(pg, "好") or modal_click(pg, "知道了") or modal_click(pg, "關閉"):
                pg.wait_for_timeout(700); continue
        pg.wait_for_timeout(500)
    s = st(pg)
    assert s["story"], f"C1 story never appeared, got {s}"
    notes = story_note_visible(pg)
    ev(pg, res, "story_notes", notes)
    assert "劇情進行中，播完先可以離開" in notes, f"story lock note missing: {notes}"
    shot(pg, f"c2a-story-{res['vp']}")
    r = play_story(pg)
    ev(pg, res, "story_played", r.get("done"))
    settled = settle_opening(pg)
    ev(pg, res, "settled_opening", settled)
    assert settled, "settle_opening failed after C1"


c2a._no_settle = True


def c2b(pg, res):
    """C2 巧遇對照：enc79 overlay 唔係鎖死，唔應該有鎖死細字。
    機制（L53732／enc79BuildScript）：初遇（met=false）唔出點頭離開，要播完先走得；
    重遇先由第一句就有點頭離開。重遇 live 驗唔到：S.stars 係 lazy init（settle 嗰陣
    根本未有，播種 met=true 無嘢可設；probe 證實 S.stars===undefined），而同一粒星
    同日有冷卻（ENC79_COOLDOWN），唔可以即日再撞同一粒星。所以 live 驗初遇路徑
    （播到尾，驗收尾掣）；重遇路徑（點頭離開）以源碼核實（built.first 閘）。"""
    found = False
    for loc in ("茶餐廳", "事務所", "唱片公司"):
        if st(pg)["enc"]:
            found = True
            break
        js_click_contains(pg, loc, "#v-map")
        pg.wait_for_timeout(1500)
        if st(pg)["enc"]:
            found = True
            break
        # 冇 overlay：返地圖再試下一個地點
        pg.evaluate("""() => { const sh=document.getElementById('loc-sheet');
          if(!sh) return false; const b=[...sh.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='返回地圖');
          if(b){ b.click(); return true; } return false; }""")
        pg.wait_for_timeout(900)
    assert found, "no enc79 overlay appeared at any location"
    ov = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
      if(!ov) return null;
      const btns=[...ov.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim());
      return {btns, hasLockNote:(ov.textContent||'').includes('劇情進行中')}; }""")
    ev(pg, res, "overlay_first", ov)
    assert ov and not ov["hasLockNote"], f"enc79 overlay must NOT carry the story-lock note: {ov}"
    if "點頭離開" in ov["btns"]:
        ev(pg, res, "exit_path", "repeat-skip")
        shot(pg, f"c2b-enc79-{res['vp']}")
        ok = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay'); if(!ov) return false;
          const b=[...ov.querySelectorAll('button')].find(x=>x.offsetParent!==null && (x.textContent||'').trim()==='點頭離開');
          if(!b) return false; b.click(); return true; }""")
        assert ok, "cannot click 點頭離開"
        pg.wait_for_timeout(900)
        assert not st(pg)["enc"], "overlay still present after 點頭離開"
        return
    # 後備：初遇——播到尾，驗收尾掣
    ev(pg, res, "exit_path", "first-meeting-playthrough")
    shot(pg, f"c2b-enc79-first-{res['vp']}")
    last_btn = None
    for _ in range(24):
        ov = pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay');
          if(!ov) return null;
          const btns=[...ov.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>(b.textContent||'').trim());
          return {btns, hasLockNote:(ov.textContent||'').includes('劇情進行中')}; }""")
        if ov is None:
            break
        assert not ov["hasLockNote"], f"enc79 overlay must NOT carry the story-lock note: {ov}"
        last_btn = ov["btns"]
        if not pg.evaluate("""() => { const ov=document.getElementById('enc79-overlay'); if(!ov) return false;
          const sk=ov.querySelector('.e79-skip'); if(sk && sk.offsetParent!==null){ sk.click(); return true; }
          const ch=ov.querySelector('.e79-choice'); if(ch){ ch.click(); return true; }
          const nb=[...ov.querySelectorAll('.e79-btn')].find(b=>b.offsetParent!==null);
          if(nb){ nb.click(); return true; } return false; }"""):
            break
        pg.wait_for_timeout(700)
    ev(pg, res, "last_btns", last_btn)
    assert not st(pg)["enc"], "overlay still present after playing through first meeting"
    assert last_btn and "（返去睇下呢度有咩做）" in last_btn,         f"first-meeting close button missing: {last_btn}"


c2b._vps = [932]


def b1c(pg, res):
    """B1 劇情結算（排程 slot）：Fen 送別結算寫明關閉之後繼續跑今日街頭表演。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "rest", "rest", "rest", "rest"], {"fen": True})
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s)
    assert modal_click(pg, "開始今日行程")
    stop, events = pump_until(pg, {"result"})
    s = st(pg)
    inner = result_inner(pg)
    ev(pg, res, "chain", {"stop": stop, "events": events, "title": s["title"], "inner_head": inner[:220]})
    assert stop == "result", f"expected Fen farewell result modal, got {stop} {events} {s}"
    assert any(k in inner for k in ("芬姐", "啟德", "送機")), f"result modal must be Fen farewell, got {inner[:160]}"
    assert "關閉之後：繼續跑今日行程「街頭表演」（自動行程）" in inner, \
        f"result dest line wrong/missing: {inner[:220]}"
    shot(pg, f"b1c-fen-result-{res['vp']}")
    assert modal_click(pg, "關閉"), "no 關閉 on Fen result modal"
    stop, events2 = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "after_close", {"stop": stop, "events": events2, "title": s["title"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s), f"close must continue Tue street, got {stop} {s}"


b1c._vps = [932]


def b1d(pg, res):
    """B1 劇情結算（地圖 slot）：Fen 送別結算寫明關閉之後返地圖。"""
    seed(pg, ["street", "scout_all", "rest", "rest", "rest", "rest", "rest"], {"fen": True})
    assert start_today_from_map(pg), "cannot start Mon street from map"
    stop, _ev0 = pump_until(pg, {"dayend"})
    s = st(pg)
    assert stop == "dayend" and is_dayend(s), f"expected Mon street board, got {stop} {s}"
    assert "返回地圖" in s["modalBtns"], "Mon street board must show 返回地圖 (Tue is map day)"
    assert modal_click(pg, "返回地圖"), "no 返回地圖 on Mon street board"
    stop, events = pump_until(pg, {"result"})
    s = st(pg)
    inner = result_inner(pg)
    ev(pg, res, "chain", {"stop": stop, "events": events, "title": s["title"], "inner_head": inner[:220]})
    assert stop == "result", f"expected Fen farewell result modal, got {stop} {events} {s}"
    assert any(k in inner for k in ("芬姐", "啟德", "送機")), f"result modal must be Fen farewell, got {inner[:160]}"
    assert "關閉之後：返地圖（今日：到處逛逛）" in inner, \
        f"result dest line wrong/missing: {inner[:220]}"
    shot(pg, f"b1d-fen-result-{res['vp']}")
    assert modal_click(pg, "關閉"), "no 關閉 on Fen result modal"
    stop, events2 = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after_close", {"stop": stop, "events": events2, "map": s["mapVisible"], "day": s["dayIndex"]})
    assert stop == "map" and s["mapVisible"] and not s["maskOn"], f"slot=map must land on map, got {stop} {s}"


b1d._vps = [932]


CASES = [
    ("b1a", b1a), ("b1b", b1b), ("b2a", b2a), ("b2b", b2b),
    ("c1a", c1a), ("c1b", c1b), ("c2a", c2a), ("c2b", c2b),
    ("b1c", b1c), ("b1d", b1d),
]

def main():
    from playwright.sync_api import sync_playwright
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            vps = [932, 700] if ARGS.vp == "both" else [int(ARGS.vp)]
            for vp in vps:
                for name, fn in CASES:
                    if getattr(fn, "_vps", None) and vp not in fn._vps:
                        continue
                    key = f"{name}-{vp}"
                    run_case(pw, vp, key, fn)
    finally:
        stop(srv)
    # --only 單 case 嗰陣寫去獨立報告檔，唔覆寫 report196.json（保全全套 932 證據）。
    # 寫入失敗（間歇性 EPERM）唔好殺死個 process：stdout 嘅逐 case 結果本身就係證據。
    _rname = f"report202_{ARGS.only}_{ARGS.vp}.json" if ARGS.only else "report202.json"
    try:
        with open(os.path.join(HERE, _rname), "w", encoding="utf-8") as f:
            json.dump(REPORT, f, ensure_ascii=False, indent=2)
    except Exception as _werr:
        print(f"REPORT WRITE FAILED ({_rname}): {_werr}", flush=True)
    npass = sum(1 for r in REPORT["runs"].values() if r["pass"])
    print(f"DRIVE202: {npass}/{len(REPORT['runs'])} PASS, total pageerrors={len(REPORT['errors'])}", flush=True)
    for k, r in REPORT["runs"].items():
        print(f"  {k}: {'PASS' if r['pass'] else 'FAIL'} {r.get('error','')}", flush=True)


if __name__ == "__main__":
    main()
