# -*- coding: utf-8 -*-
"""v20a196 實駕 drive196：日流程自動連跑＋故事播放鎖死返地圖 × 932／700。
用法：/home/hatch/pwenv49/bin/python qa196/drive196.py [--only <key>] [--vp 932|700|both]
Mirror：工作副本 ~/workspace/linji-work196，port 8976，live 模式（唔用 ?softPreview=1）。
播種：經 new_game 正常開局（slot 3），再 live 改 S（weekPlan＋probe shoots＋paper/aud/wf4/fen/sick/award）＋saveQ()。
觸發（真實 UI 路徑，唔直叫 IIFE 內函數）：開茶餐廳 sheet → sheet「返回地圖」→
  goToMapForBrowse → kickScheduleIfNeeded（今日係強制拍攝日）→ resolvePlannedDay；
  soft／rest 日：地圖 #map-start-today → startTodayScheduleFromMap。
量度（DOM 為準，截圖只係記錄）：日結板掣列／dismiss 去向／晨鏈各環出現次序／
  強制播續鏈去向／故事鎖死操作／週末／病假／休息卡／殺青獎勵／加速／頒獎禮鎖死。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, sys, argparse

ROOT = "/home/hatch/workspace/linji-work196"
HERE = os.path.join(ROOT, "qa196")
SHOTS = os.path.join(HERE, "shots196")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8976
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


def c1(pg, res):
    """連續排程日自動連跑：Mon wrap → Tue street → Wed rest → Thu scout_all（落地圖）。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "scout_all", "rest", "rest", "rest"])
    op = open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    ev(pg, res, "mon_board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert is_dayend(s), f"expected wrap board, got {s}"
    assert "返回地圖" not in s["modalBtns"], "Mon wrap board must NOT show 返回地圖 (Tue is scheduled)"
    shot(pg, "c1-mon-board")
    assert modal_click(pg, "開始今日行程"), "no 開始今日行程 on Mon board"
    stop, events = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "tue", {"stop": stop, "events": events, "title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s), f"expected Tue street board, got {stop} {s}"
    assert "返回地圖" not in s["modalBtns"], "Tue street board must NOT show 返回地圖"
    assert s["dayIndex"] == res["evidence"]["mon_board"]["day"] + 1
    shot(pg, "c1-tue-board")
    assert modal_click(pg, "開始今日行程"), "no 開始今日行程 on Tue board"
    stop, events = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "wed", {"stop": stop, "events": events, "title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert is_dayend(s) or stop == "decision:開始今日行程", f"expected Wed rest card, got {stop} {s}"
    # Wed 休息卡嗰陣 dayIndex 已係 Thu（scout_all 逛逛日）——按 D7 應出「返回地圖」（只得呢粒）
    assert "返回地圖" in s["modalBtns"], f"Wed rest card must show 返回地圖 (Thu is map day), got {s}"
    shot(pg, "c1-wed-rest")
    assert modal_click(pg, "返回地圖"), "no 返回地圖 on Wed rest card"
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "thu", {"stop": stop, "events": events, "map": s["mapVisible"], "day": s["dayIndex"]})
    assert stop == "map" and s["mapVisible"] and not s["maskOn"], f"expected Thu map landing, got {stop} {s}"
    assert s["dayIndex"] == 3, f"expected Thu (day 3), got {s['dayIndex']}"
    shot(pg, "c1-thu-map")


def c2(pg, res):
    """逛逛日準確落地圖：Mon wrap → Tue scout_all。"""
    seed(pg, ["shoot:probe196w", "scout_all", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    ev(pg, res, "mon_board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert is_dayend(s)
    assert "返回地圖" in s["modalBtns"], "Mon wrap board must show 返回地圖 (Tue is map day)"
    shot(pg, "c2-mon-board")
    assert modal_click(pg, "返回地圖")
    pg.wait_for_timeout(1200)
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "tue", {"stop": stop, "events": events, "map": s["mapVisible"], "day": s["dayIndex"]})
    assert s["mapVisible"] and not s["maskOn"], f"expected Tue map landing, got {stop} {s}"


def c3a(pg, res):
    """dismiss 兩向 (a) 排程日：Mon wrap → mask dismiss → Tue street 照跑。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s)
    d0 = s["dayIndex"]
    assert mask_click(pg), "mask dismiss failed"
    stop, events = pump_until(pg, {"dayend", "map"})
    s = st(pg)
    ev(pg, res, "after_dismiss", {"stop": stop, "events": events, "title": s["title"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s) and s["dayIndex"] == d0 + 1, f"dismiss on scheduled day must run Tue street, got {stop} {s}"


def c3b(pg, res):
    """dismiss 兩向 (b) 逛逛日：Mon wrap → mask dismiss → 落地圖。"""
    seed(pg, ["shoot:probe196w", "scout_all", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s)
    assert mask_click(pg), "mask dismiss failed"
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after_dismiss", {"stop": stop, "events": events, "map": s["mapVisible"], "day": s["dayIndex"]})
    assert s["mapVisible"] and not s["maskOn"], f"dismiss on map day must land on map, got {stop} {s}"


def c4(pg, res):
    """晨鏈一個唔漏：Tue chain 依次出 reward → invite → paper → aud → WF4 → Tue street。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "rest", "rest", "rest", "rest"],
         {"paper": True, "aud": True, "award": True, "wf4": True})
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s)
    assert modal_click(pg, "開始今日行程")
    stop, events = pump_chain(pg)
    ev(pg, res, "phase1", {"stop": stop, "events": events})
    assert stop == "invite", f"expected award invite in chain, got {stop} {events}"
    assert any(e == "reward" for e in events), f"reward ring missing: {events}"
    # 接受請柬 → 典禮 → 結果卡 → 繼續鏈
    assert modal_click(pg, "出席"), "invite has no 出席"
    pg.wait_for_timeout(2000)
    assert st(pg)["ceremony"], "ceremony stage did not appear after accepting invite"
    ev(pg, res, "ceremony_seen", True)
    assert drive_ceremony(pg), "ceremony did not finish"
    pg.wait_for_timeout(1000)
    s = st(pg)
    ev(pg, res, "after_ceremony", {"title": s["title"], "btns": s["modalBtns"]})
    if "收下這晚" in s["modalBtns"]:
        assert modal_click(pg, "收下這晚")
    stop, events2 = pump_until(pg, {"dayend"})
    s = st(pg)
    all_ev = events + events2
    ev(pg, res, "phase2", {"stop": stop, "events": events2, "title": s["title"], "day": s["dayIndex"]})
    assert "paper" in all_ev, f"paper ring missing: {all_ev}"
    assert any(e.startswith("aud:") for e in all_ev), f"aud ring missing: {all_ev}"
    assert stop == "dayend" and is_dayend(s), f"expected Tue street board after chain, got {stop} {s}"
    wf = pg.evaluate("() => ({pending: S.wf4 ? S.wf4.pending : null, seen: S.wf4 ? (S.wf4.seen||{})['wf4_ev_set01']||0 : 0, audLeft: (S.pendingAud||[]).length})")
    ev(pg, res, "wf4_state", wf)
    assert wf["seen"] >= 1 and wf["pending"] is None, f"WF4 event not consumed: {wf}"
    assert wf["audLeft"] == 0, f"audition news not presented: {wf}"


def c5a(pg, res):
    """強制播續鏈 (a) slot=map：芬姐送別戲經地圖鏈播（afterCont=map），關閉後返地圖，日唔郁。
    （開局 C1 已由 settle 播完，Fen 係按需播種嘅強制故事；slot 係 IIFE 內部變數，live 讀唔到，
    以關閉後去向做行為斷言。）"""
    seed(pg, ["street", "scout_all", "rest", "rest", "rest", "rest", "rest"], {"fen": True})
    assert start_today_from_map(pg), "cannot start Mon street from map"
    stop, _ev0 = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "mon_board", {"stop": stop, "title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s), f"expected Mon street board, got {stop} {s}"
    assert "返回地圖" in s["modalBtns"], "Mon street board must show 返回地圖 (Tue is map day)"
    d0 = s["dayIndex"]
    assert modal_click(pg, "返回地圖"), "no 返回地圖 on Mon street board"
    stop, events = pump_until(pg, {"result"})
    s = st(pg)
    ev(pg, res, "chain", {"stop": stop, "events": events, "title": s["title"], "inner": s["innerText"][:160]})
    assert stop == "result", f"expected Fen farewell result modal, got {stop} {events} {s}"
    assert any(k in s["innerText"] for k in ("芬姐", "啟德", "送機")), f"result modal must be Fen farewell, got {s['innerText'][:160]}"
    shot(pg, "c5a-fen-result")
    assert modal_click(pg, "關閉"), "no 關閉 on Fen result modal"
    stop, events2 = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after_close", {"stop": stop, "events": events2, "map": s["mapVisible"], "mask": s["maskOn"], "day": s["dayIndex"]})
    assert stop == "map" and s["mapVisible"] and not s["maskOn"], f"slot=map must land on map, got {stop} {s}"
    assert s["dayIndex"] == d0, "day must not advance on forced-play close"

def c5b(pg, res):
    """強制播續鏈 (b) slot=schedule：芬姐送別戲經排程鏈播，關閉後 Tue street 照跑。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "rest", "rest", "rest", "rest"], {"fen": True})
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s)
    d0 = s["dayIndex"]
    assert modal_click(pg, "開始今日行程")
    stop, events = pump_until(pg, {"result"})
    s = st(pg)
    ev(pg, res, "chain", {"stop": stop, "events": events, "title": s["title"], "inner": s["innerText"][:160]})
    assert stop == "result", f"expected Fen farewell result modal, got {stop} {events} {s}"
    assert any(k in s["innerText"] for k in ("芬姐", "啟德", "送機")), f"result modal must be Fen farewell, got {s['innerText'][:160]}"
    shot(pg, "c5b-fen-result")
    assert modal_click(pg, "關閉"), "no 關閉 on Fen result modal"
    stop, events2 = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "after_close", {"stop": stop, "events": events2, "title": s["title"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s) and s["dayIndex"] == d0 + 1, f"slot=schedule must run Tue street, got {stop} {s}"

def c6(pg, res):
    """故事鎖死：開局 C1 自動播嗰陣逐個操作試——先返回唔存在、mask 撳唔走、頂欄／地圖撳唔到、跳至選項唔郁。"""
    seed(pg, ["scout_all", "scout_all", "scout_all", "scout_all", "scout_all", "scout_all", "scout_all"])
    # 等開局 C1 播出（postTutorialEntry 160ms 後自動推）
    ok = False
    for _ in range(20):
        pg.wait_for_timeout(500)
        if st(pg)["story"]:
            ok = True; break
    assert ok, "opening C1 story did not auto-play"
    s = st(pg)
    ev(pg, res, "entry", {"title": s["title"], "day": s["dayIndex"]})
    shot(pg, "c6-story")
    no_back = pg.evaluate("""() => ![...document.querySelectorAll('button')].some(b => b.offsetParent !== null && (b.textContent||'').includes('先返回'))""")
    ev(pg, res, "no_leave_btn", no_back)
    assert no_back, "「先返回」must not exist during story"
    skip_opt = pg.evaluate("""() => [...document.querySelectorAll('button')].some(b => b.offsetParent !== null && (b.textContent||'').includes('跳至選項'))""")
    ev(pg, res, "skip_to_choice_present", skip_opt)
    # mask 撳：故事唔應該走
    mask_click(pg)
    s = st(pg)
    ev(pg, res, "after_mask_click", {"story": s["story"], "mask": s["maskOn"]})
    assert s["story"], "story must still be playing after mask click"
    # elementFromPoint：頂欄／地圖位應該命中 mask／故事層，唔係地圖掣
    hits = pg.evaluate("""() => {
      const pts = [[195, 28], [195, 500], [60, 500]];
      return pts.map(([x, y]) => { const el = document.elementFromPoint(x, y);
        return el ? (el.id || el.className || el.tagName).toString().slice(0, 60) : null; }); }""")
    ev(pg, res, "elementFromPoint", hits)
    for h in hits:
        assert h is not None and ("mask" in h or "story" in h.lower() or "sp-" in h or "dlg106" in h or "modal" in h.lower() or "toast" in h.lower()), f"point must hit mask/story layer, got {h}"
    # 真滑鼠撳地圖位：故事照播，唔落地圖
    pg.mouse.click(195, 500)
    pg.wait_for_timeout(900)
    s = st(pg)
    ev(pg, res, "after_map_click", {"story": s["story"], "map": s["mapVisible"]})
    assert s["story"] and not s["mapVisible"], "clicking map area must not leave story"
    r = play_story(pg)
    assert r.get("done"), f"story did not finish: {r}"
    assert st(pg)["resultModal"]
    assert modal_click(pg, "關閉")
    pg.wait_for_timeout(1000)
    s = st(pg)
    ev(pg, res, "after_close", {"map": s["mapVisible"], "mask": s["maskOn"]})
    assert (s["mapVisible"] or s["homeVisible"]) and not s["maskOn"], f"after story close must idle on map/home, got {s}"


c6._no_settle = True

def c7(pg, res):
    """週末照常：Sun wrap → 週結回家 → 確認下週計劃 → Mon 照跑。
    注意：seed 嘅 probe196f（三日拍攝）會自動排入新一週 Mon–Wed（「拍攝檔期已定」），
    所以 Monday 跑嘅係拍攝唔係 street——day 由 Sun 13 行到 Tue 15（Mon 跑完），
    板係 Mon 拍攝板。週末流程本身（回家→確認→出發）唔變，呢個係 v196 照常驗證。"""
    # seed 用星期日做今日：直接寫 weekPlan（Sun=wrap），再將 dayIndex 推去星期日
    pg.evaluate("""() => { const wd=(d)=>((d%7)+7)%7; while(wd(S.dayIndex)!==6) S.dayIndex+=1; return S.dayIndex; }""")
    seed(pg, ["street", "rest", "rest", "rest", "rest", "rest", "shoot:probe196w"])
    # seed() 會將 dayIndex 歸一化返星期一——改返星期日（同一週）
    pg.evaluate("""() => { const wd=(d)=>((d%7)+7)%7; while(wd(S.dayIndex)!==6) S.dayIndex+=1; try{ saveQ(); }catch(e){} return S.dayIndex; }""")
    d0 = pg.evaluate("() => S.dayIndex")
    ev(pg, res, "sunday", d0)
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s), f"expected Sun wrap board, got {s}"
    # 週日 wrap 板：ended=true，繼續掣係「回家結算」（唔係「開始今日行程」）
    assert "回家結算" in s["modalBtns"], f"Sun wrap board must offer 回家結算 (week ended), got {s}"
    assert modal_click(pg, "回家結算")
    # 等回家（ended → enterHome）：撳穿中途 modal，直到 v-home 出現
    home = False
    for _ in range(40):
        pg.wait_for_timeout(500)
        s = st(pg)
        if s["homeVisible"] and not s["maskOn"]:
            home = True; break
        if s["story"]:
            play_story(pg); continue
        if s["enc"]:
            dismiss_encounter(pg); continue
        if s["maskOn"]:
            if modal_click(pg, "收下這份反響") or modal_click(pg, "收下這份剪報") or modal_click(pg, "收下這晚"):
                continue
            if modal_click(pg, "回家結算"):
                continue
            if modal_click(pg, "好") or modal_click(pg, "關閉") or modal_click(pg, "知道了"):
                continue
            if modal_click(pg, "返回地圖"):
                continue
    ev(pg, res, "home_reached", home)
    assert home, "weekend must land in home (enterHome)"
    shot(pg, "c7-home")
    # 確認下週計劃 → 出發
    for _ in range(10):
        pg.wait_for_timeout(600)
        s = st(pg)
        if not s["homeVisible"]:
            break
        try:
            pg.locator("#btn-confirm-plan").click(timeout=900); continue
        except Exception:
            pass
        if click_first(pg, ["確定出發", "開始今日行程"], 800):
            continue
        if s["maskOn"] and (modal_click(pg, "確定") or modal_click(pg, "好")):
            continue
        break
    stop, events = pump_until(pg, {"dayend", "map"})
    s = st(pg)
    ev(pg, res, "monday", {"stop": stop, "events": events, "title": s["title"], "map": s["mapVisible"], "day": s["dayIndex"]})
    # 出發即跑 Monday（已排定嘅 probe196f 拍攝日）：Mon 跑完 → Tue 15，板係 Mon 拍攝板
    assert s["dayIndex"] == d0 + 2, f"day must advance Sun->Tue (Mon shoot ran), got {s['dayIndex']} from {d0}"
    assert stop == "dayend" and is_dayend(s), f"expected Mon shoot board, got {stop} {s}"
    assert "拍攝" in (s["title"] or ""), f"Monday board must be the auto-slotted shoot, got {s['title']}"


def c8a(pg, res):
    """病假照常＋掣／dismiss 跟新規則 (a) 聽日排程：病假板只留開始今日行程，dismiss 照跑 Tue street。"""
    seed(pg, ["street", "street", "rest", "rest", "rest", "rest", "rest"], {"sick": True})
    assert start_today_from_map(pg), "cannot start Mon street from map"
    stop, _ev = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "sick_board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert s["title"] and "病倒休養" in s["title"], f"expected sick board, got {s}"
    assert "返回地圖" not in s["modalBtns"], "sick board must NOT show 返回地圖 (Tue scheduled)"
    d0 = s["dayIndex"]
    assert mask_click(pg), "mask dismiss failed"
    stop, events = pump_until(pg, {"dayend", "map"})
    s = st(pg)
    ev(pg, res, "after_dismiss", {"stop": stop, "events": events, "title": s["title"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s) and s["dayIndex"] == d0 + 1, f"sick dismiss must run Tue, got {stop} {s}"


def c8b(pg, res):
    """病假照常＋掣／dismiss 跟新規則 (b) 聽日逛逛：病假板有返回地圖，dismiss 落地圖。"""
    seed(pg, ["street", "scout_all", "rest", "rest", "rest", "rest", "rest"], {"sick": True})
    assert start_today_from_map(pg), "cannot start Mon street from map"
    stop, _ev = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "sick_board", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert s["title"] and "病倒休養" in s["title"], f"expected sick board, got {s}"
    assert "返回地圖" in s["modalBtns"], "sick board must show 返回地圖 (Tue is map day)"
    assert mask_click(pg), "mask dismiss failed"
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after_dismiss", {"stop": stop, "events": events, "map": s["mapVisible"]})
    assert s["mapVisible"] and not s["maskOn"], f"sick dismiss on map day must land on map, got {stop} {s}"


def c9a(pg, res):
    """休息卡 (a) 聽日排程：dismiss 休息卡 → Tue street 照跑。"""
    seed(pg, ["rest", "street", "rest", "rest", "rest", "rest", "rest"])
    assert start_today_from_map(pg), "cannot start Mon rest from map"
    stop, _ev = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "rest_card", {"title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert "返回地圖" not in s["modalBtns"], "rest card must NOT show 返回地圖 (Tue scheduled)"
    d0 = s["dayIndex"]
    assert mask_click(pg), "mask dismiss failed on rest card"
    stop, events = pump_until(pg, {"dayend", "map"})
    s = st(pg)
    ev(pg, res, "after_dismiss", {"stop": stop, "events": events, "title": s["title"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s) and s["dayIndex"] == d0 + 1, f"rest dismiss must run Tue street, got {stop} {s}"


def c9b(pg, res):
    """休息卡 (b) 聽日逛逛：休息卡只出「返回地圖」（v196 D1：板本身已按下一日方向收斂，
    唔再經確認 modal；確認 modal 兩向由 test_dayflow196_logic.js 覆蓋）。撳佢落地圖。"""
    seed(pg, ["rest", "scout_all", "rest", "rest", "rest", "rest", "rest"])
    assert start_today_from_map(pg), "cannot start Mon rest from map"
    stop, _ev = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "rest_card", {"title": s["title"], "btns": s["modalBtns"]})
    assert "返回地圖" in s["modalBtns"], f"rest card must show 返回地圖 (Tue is map day), got {s}"
    assert "開始今日行程" not in s["modalBtns"], f"rest card must NOT show 開始今日行程 (Tue is map day), got {s}"
    assert modal_click(pg, "返回地圖")
    pg.wait_for_timeout(1200)
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after", {"stop": stop, "events": events, "map": s["mapVisible"]})
    assert s["mapVisible"] and not s["maskOn"], f"rest card 返回地圖 must land on map, got {stop} {s}"


def c10(pg, res):
    """殺青獎勵照出＋跟新規則：wrap 板 → 開始今日行程 → 獎勵 sheet → Tue street 板。"""
    seed(pg, ["shoot:probe196w", "street", "rest", "rest", "rest", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s)
    assert modal_click(pg, "開始今日行程")
    stop, events = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "chain", {"stop": stop, "events": events, "title": s["title"], "day": s["dayIndex"]})
    assert "reward" in events, f"wrap reward sheet missing: {events}"
    assert stop == "dayend" and is_dayend(s), f"expected Tue street board after reward, got {stop} {s}"


def c11(pg, res):
    """week-accel 照舊：wrap 板 → 加速 → 確認 → 合併非關鍵日 → 摘要／地圖。"""
    seed(pg, ["shoot:probe196w", "rest", "rest", "street", "scout_all", "rest", "rest"])
    open_sheet_and_back_to_map(pg)
    s = wait_dayend_modal(pg)
    assert is_dayend(s)
    d0 = s["dayIndex"]
    assert any("加速" in b for b in s["modalBtns"]), f"accel link missing on wrap board: {s['modalBtns']}"
    assert js_click_contains(pg, "加速"), "cannot click accel link"
    # 日結板掣包咗 afterDayRes：獎勵 sheet 行先，撳穿佢先見到加速確認 modal（pre-existing 設計，v189 實駕同一寫法）
    ev(pg, res, "accel_click_reward_first", None)
    for _ in range(10):
        pg.wait_for_timeout(500)
        s = st(pg)
        if s["title"] == "加速本週剩餘？":
            break
        if "收下這份反響" in s["modalBtns"]:
            modal_click(pg, "收下這份反響"); continue
        if "收下這份剪報" in s["modalBtns"]:
            modal_click(pg, "收下這份剪報"); continue
        break
    s = st(pg)
    ev(pg, res, "accel_confirm", {"title": s["title"], "btns": s["modalBtns"]})
    assert s["title"] == "加速本週剩餘？", f"expected accel confirm, got {s}"
    assert modal_click(pg, "確認加速")
    stop, events = pump_until(pg, {"map", "dayend"})
    s = st(pg)
    ev(pg, res, "after_accel", {"stop": stop, "events": events, "title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    # 加速可能停喺摘要 modal（本週加速完成 → 繼續／返回地圖）或直接落地圖／下一關鍵板
    if s["maskOn"] and "本週加速完成" in (s["title"] or ""):
        done_btn = next((b for b in ("返回地圖", "繼續", "回家結算") if b in s["modalBtns"]), None)
        assert done_btn, f"accel summary has no continue button: {s}"
        assert modal_click(pg, done_btn)
        pg.wait_for_timeout(1000)
        stop, events = pump_until(pg, {"map", "dayend"})
        s = st(pg)
        ev(pg, res, "after_summary", {"stop": stop, "events": events, "map": s["mapVisible"], "day": s["dayIndex"]})
    assert s["dayIndex"] > d0, f"accel must advance days, got {s['dayIndex']} from {d0}"
    assert (s["mapVisible"] and not s["maskOn"]) or is_dayend(s), f"accel must end on map or a day-end board, got {stop} {s}"


def c12a(pg, res):
    """頒獎禮 (a) 請柬 dismiss＝推辭：mask 閂請柬 → 典禮照播（gallery）→ 返地圖＋log 標 skipped。"""
    seed(pg, ["street", "scout_all", "rest", "rest", "rest", "rest", "rest"], {"award": True})
    assert start_today_from_map(pg), "cannot start Mon street from map"
    stop, _ev0 = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "mon_board", {"stop": stop, "title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s), f"expected Mon street board, got {stop} {s}"
    assert "返回地圖" in s["modalBtns"], "Mon street board must show 返回地圖 (Tue is map day)"
    assert modal_click(pg, "返回地圖"), "no 返回地圖 on Mon street board"
    stop, events = pump_until(pg, {"invite"})
    s = st(pg)
    ev(pg, res, "entry", {"stop": stop, "events": events, "invite": s["invite"], "title": s["title"], "btns": s["modalBtns"]})
    assert stop == "invite" and s["invite"], f"expected award invite modal, got {stop} {events} {s}"
    assert mask_click(pg), "mask dismiss failed on invite"
    pg.wait_for_timeout(2000)
    s = st(pg)
    ev(pg, res, "after_dismiss", {"ceremony": s["ceremony"], "map": s["mapVisible"]})
    assert s["ceremony"], f"declined invite must still play ceremony (gallery), got {s}"
    assert not s["mapVisible"], "must NOT land on map while ceremony plays"
    assert drive_ceremony(pg), "ceremony did not finish"
    pg.wait_for_timeout(1200)
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after_ceremony", {"stop": stop, "events": events, "map": s["mapVisible"], "day": s["dayIndex"]})
    assert s["mapVisible"] and not s["maskOn"], f"after declined ceremony must land on map, got {stop} {s}"
    log = pg.evaluate("() => (window.__awards && window.__awards.log()) ? window.__awards.log().slice(-3) : null")
    ev(pg, res, "award_log_tail", log)
    assert log and any("skipped" in json.dumps(e) for e in log), f"award log must record skipped, got {log}"

def c12b(pg, res):
    """頒獎禮 (b) 出席＋鎖死：典禮期間地圖唔可見、elementFromPoint 命中舞台、撳極唔走。"""
    seed(pg, ["street", "scout_all", "rest", "rest", "rest", "rest", "rest"], {"award": True})
    assert start_today_from_map(pg), "cannot start Mon street from map"
    stop, _ev0 = pump_until(pg, {"dayend"})
    s = st(pg)
    ev(pg, res, "mon_board", {"stop": stop, "title": s["title"], "btns": s["modalBtns"], "day": s["dayIndex"]})
    assert stop == "dayend" and is_dayend(s), f"expected Mon street board, got {stop} {s}"
    assert "返回地圖" in s["modalBtns"], "Mon street board must show 返回地圖 (Tue is map day)"
    assert modal_click(pg, "返回地圖"), "no 返回地圖 on Mon street board"
    stop, events = pump_until(pg, {"invite"})
    s = st(pg)
    ev(pg, res, "entry", {"stop": stop, "events": events, "invite": s["invite"]})
    assert stop == "invite" and s["invite"], f"expected award invite modal, got {stop} {events} {s}"
    assert modal_click(pg, "出席"), "invite has no 出席"
    pg.wait_for_timeout(2000)
    s = st(pg)
    ev(pg, res, "ceremony", {"ceremony": s["ceremony"], "map": s["mapVisible"]})
    assert s["ceremony"], f"ceremony stage did not appear after attending, got {s}"
    assert not s["mapVisible"], "map must not be visible during ceremony"
    shot(pg, "c12b-ceremony")
    # 探點改跟舞台本身嘅 bounding rect（25／50／75% 高、橫向中央）：舊寫法寫死 y=700，
    # 700 viewport 高得 700px，y=700 啱啱喺 viewport 底邊之外，elementFromPoint 返 null——唔係鎖死失效。
    hits = pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return ['no-stage'];
      const r = st.getBoundingClientRect();
      const cx = r.left + r.width/2;
      const pts = [[cx, r.top + r.height*0.25], [cx, r.top + r.height*0.5], [cx, r.top + r.height*0.75]];
      return pts.map(([x, y]) => { const el = document.elementFromPoint(x, y);
        if (!el) return null; const s2 = el.closest('.awd62-stage');
        return s2 ? 'awd62-stage' : (el.className||el.tagName||'').toString().slice(0, 40); }); }""")
    ev(pg, res, "elementFromPoint", hits)
    assert all(h == "awd62-stage" for h in hits), f"all points must hit ceremony stage, got {hits}"
    pg.mouse.click(195, 400)
    pg.wait_for_timeout(900)
    s = st(pg)
    ev(pg, res, "after_click", {"ceremony": s["ceremony"], "map": s["mapVisible"]})
    assert s["ceremony"] and not s["mapVisible"], "clicking stage must not leave ceremony"
    assert drive_ceremony(pg), "ceremony did not finish"
    pg.wait_for_timeout(1000)
    s = st(pg)
    if "收下這晚" in s["modalBtns"]:
        assert modal_click(pg, "收下這晚")
    stop, events = pump_until(pg, {"map"})
    s = st(pg)
    ev(pg, res, "after", {"stop": stop, "events": events, "map": s["mapVisible"]})
    assert s["mapVisible"] and not s["maskOn"], f"after ceremony must land on map, got {stop} {s}"

CASES = [
    ("c1", c1), ("c2", c2), ("c3a", c3a), ("c3b", c3b), ("c4", c4),
    ("c5a", c5a), ("c5b", c5b), ("c6", c6), ("c7", c7), ("c8a", c8a),
    ("c8b", c8b), ("c9a", c9a), ("c9b", c9b), ("c10", c10), ("c11", c11),
    ("c12a", c12a), ("c12b", c12b),
]


def main():
    from playwright.sync_api import sync_playwright
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            vps = [932, 700] if ARGS.vp == "both" else [int(ARGS.vp)]
            for vp in vps:
                for name, fn in CASES:
                    key = f"{name}-{vp}"
                    run_case(pw, vp, key, fn)
    finally:
        stop(srv)
    # --only 單 case 嗰陣寫去獨立報告檔，唔覆寫 report196.json（保全全套 932 證據）。
    # 寫入失敗（間歇性 EPERM）唔好殺死個 process：stdout 嘅逐 case 結果本身就係證據。
    _rname = f"report196_{ARGS.only}_{ARGS.vp}.json" if ARGS.only else "report196.json"
    try:
        with open(os.path.join(HERE, _rname), "w", encoding="utf-8") as f:
            json.dump(REPORT, f, ensure_ascii=False, indent=2)
    except Exception as _werr:
        print(f"REPORT WRITE FAILED ({_rname}): {_werr}", flush=True)
    npass = sum(1 for r in REPORT["runs"].values() if r["pass"])
    print(f"DRIVE196: {npass}/{len(REPORT['runs'])} PASS, total pageerrors={len(REPORT['errors'])}", flush=True)
    for k, r in REPORT["runs"].items():
        print(f"  {k}: {'PASS' if r['pass'] else 'FAIL'} {r.get('error','')}", flush=True)


if __name__ == "__main__":
    main()
