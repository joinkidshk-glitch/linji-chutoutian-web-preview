# -*- coding: utf-8 -*-
"""v400 細改 1–3・實駕驗證。
Serves the repo this script lives in locally (--root 可指去基線副本),
Playwright headless shell 經本地 CONNECT 中繼。
用法：
  /home/hatch/pwenv49/bin/python qa400/drive400.py [--root DIR] [--only w1,w2,stress,cost,novice] [--runs N] [--weeks N]
結果 JSON＋截圖 -> qa400/verify/ 及 qa400/shots/（跟 --root 走，即係跑邊個副本就寫邊個副本）。
只量度／實駕，唔改 code。
注意：主 script 唔係全域可見（evaluate 叫唔到 enterHome／renderNotebook 等內部函數）——
播種只經 window.S＋localStorage；入屋／重繪一律經真實 DOM 撳掣（日格撳落去觸發 renderNotebook）。
"""
import sys, os, json, socket, subprocess, time, urllib.request, argparse

sys.path.insert(0, '/home/hatch/workspace/fullarc')
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/hatch/pw-browsers')
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser()
ap.add_argument('--root', default=None)
ap.add_argument('--only', default='w1,w2,stress,cost,novice')
ap.add_argument('--runs', type=int, default=2)
ap.add_argument('--weeks', type=int, default=6)
args = ap.parse_args()
# fullarc/driver.py import 嗰陣會讀 sys.argv——先清走我哋嘅旗標，免佢誤讀
sys.argv = sys.argv[:1]
import driver as drv
ITEMS = [x.strip() for x in args.only.split(',') if x.strip()]
ROOT = args.root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "qa400", "verify")
SHOTS = os.path.join(ROOT, "qa400", "shots")
os.makedirs(OUT, exist_ok=True)
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"

def free_port():
    for cand in range(9361, 9380):
        s = socket.socket()
        try: s.bind(("127.0.0.1", cand)); return cand
        except OSError: continue
        finally: s.close()
    raise RuntimeError("no free port")
PORT = free_port()
srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(30):
    time.sleep(0.5)
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5).read(); break
    except Exception: continue
URL = f"http://127.0.0.1:{PORT}/index.html"
print("serve", URL, flush=True)

def ev(pg, js, arg=None):
    try: return pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)
    except Exception as e: print("EVFAIL", str(e)[:300], flush=True); return None

def shot(pg, name):
    p = f"{SHOTS}/{name}.png"; pg.screenshot(path=p); print("SHOT", name, flush=True); return p

NAME2ID = {"到處逛逛": "scout_all", "休息瞓覺": "rest", "街頭表演": "street",
           "咖啡店駐場小表演": "cafe_gig", "歌藝訓練": "train_vocal",
           "演技訓練": "train_acting", "台風訓練": "train_stage",
           "外貌／形象": "train_looks", "魅力訓練": "train_charm",
           "智商／修養": "train_iq", "武師班": "train_stamina",
           "收拾房間": "home_chore", "補班夜班": "pt_topup"}

STATE_JS = """() => {
  if (typeof S === 'undefined' || !S) return null;
  const sick = Object.values(S.execLog105||{}).filter(e=>e && (e.kinds||[]).includes('sick')).length;
  const rows=[...document.querySelectorAll('#nb-days .day-row')].map(r=>{
    const nm=(r.querySelector('.plan-main')||{}).textContent||'';
    const hint=(r.querySelector('.plan-hint')||{}).textContent||'';
    return {name:nm.trim(), hint:hint.trim()}; });
  return { dayIndex: S.dayIndex, money: S.money, stress: S.stress, sick,
    savedPlan: (S.weekPlan||[]).slice(), homeEditable: !!S.homeEditable,
    enrolled: Object.keys(S.enrolled||{}).filter(k=>S.enrolled[k]),
    lastTrain: (typeof S.lastTrain400!=='undefined') ? (S.lastTrain400||null) : 'undef',
    trainCount: S.trainCount||{},
    view: (document.querySelector('.view.on')||{}).id || null,
    rows,
    planDom: rows.map(r=>r.name),
    suggest: (()=>{ const b=document.getElementById('nb-suggest400'); if(!b) return null;
      return { hidden: b.hidden, btns:[...b.querySelectorAll('button')].map(x=>(x.textContent||'').trim()) }; })(),
    cost: (()=>{ const c=document.getElementById('nb-cost400'); if(!c) return null;
      return { hidden: c.hidden, text:(c.textContent||'').trim() }; })(),
  }; }"""

def plan_ids(rows):
    out = []
    for r in (rows or []):
        n = r["name"] if isinstance(r, dict) else r
        if n.startswith("拍攝日"):
            out.append("shoot")
        else:
            out.append(NAME2ID.get(n, "?:" + n))
    return out

def click_btn_text(pg, pat, scope=None):
    return ev(pg, """(o) => {
      const root = o.scope ? document.querySelector(o.scope) : document;
      if(!root) return null;
      const bs=[...root.querySelectorAll('button')].filter(b=>b.offsetParent!==null&&!b.disabled);
      const t=bs.find(b=>new RegExp(o.pat).test(b.textContent||''));
      if(t){ t.click(); return (t.textContent||'').trim().slice(0,40); }
      return null; }""", {"pat": pat, "scope": scope})

def click_day_row(pg, idx):
    return ev(pg, """(i) => {
      const rows=[...document.querySelectorAll('#nb-days .day-row')];
      if(!rows[i]) return null; rows[i].click(); return true; }""", idx)

def click_cat_tab(pg, pat):
    return click_btn_text(pg, pat, '#cat-tabs')

def new_game(pg):
    pg.goto(URL); pg.wait_for_timeout(2500)
    for _ in range(12):
        pg.click('#btn-new'); pg.wait_for_timeout(1200)
        st = ev(pg, "() => JSON.stringify({s: !!(typeof S!=='undefined'&&S), mask: document.getElementById('mask').classList.contains('on'), view:(document.querySelector('.view.on')||{}).id||''})")
        try: st = json.loads(st)
        except Exception: st = {}
        if st.get('s') or st.get('mask') or st.get('view') != 'v-start':
            break
    if ev(pg, "() => { const b=[...document.querySelectorAll('#modal-btns button, #slot-list button')].find(x=>x.offsetParent!==null&&/槽 1/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }"):
        pg.wait_for_timeout(1200)
        drv.click_text_in_modal(pg, r'覆蓋開新局|確定')
        pg.wait_for_timeout(1000)
    drv.skip_tutorial(pg)
    drv.click_text_in_modal(pg, r'開始寫手帳')
    pg.wait_for_timeout(1000)
    pg.wait_for_function("() => typeof S !== 'undefined' && !!S", timeout=20000)
    pg.wait_for_timeout(800)

def mutate_S(pg, **kw):
    ev(pg, """(o) => {
      Object.keys(o).forEach(k=>{ if(k==='__deleteLastTrain'){ delete S.lastTrain400; } else { S[k] = o[k]; } });
      return true; }""", kw)

def play_week(pg, deadline_s=240):
    """Confirm the editable plan as-is (if confirm available), then drive days until
    back at an editable home. Returns (ok, note)."""
    dbg = open(os.path.join(OUT, "playweek.log"), "a", encoding="utf-8")
    def lg(*a):
        print("[pw]", *a, file=dbg, flush=True)
    # 1) confirm (only if the confirm button is present & unlocked)
    conf = ev(pg, """() => {
      const b = document.getElementById('btn-confirm-plan');
      if (!b || b.offsetParent === null || b.disabled) return 'absent';
      if ((b.className||'').includes('is-locked')) return 'locked';
      b.click(); return 'clicked'; }""")
    t0 = time.time()
    start_day = ev(pg, "() => (typeof S!=='undefined'&&S) ? S.dayIndex : -1")
    if start_day is None:
        start_day = -1
    lg("start conf=", conf, "start_day=", start_day)
    it = 0
    while time.time() - t0 < deadline_s:
        pg.wait_for_timeout(700)
        it += 1
        st = ev(pg, """() => JSON.stringify({ed: !!(typeof S!=='undefined'&&S&&S.homeEditable),
          day: (typeof S!=='undefined'&&S)?S.dayIndex:-1,
          view:(document.querySelector('.view.on')||{}).id||'',
          mask: document.getElementById('mask').classList.contains('on'),
          sheet: (document.getElementById('loc-sheet')||{classList:{contains:()=>false}}).classList.contains('on'),
          sleep: (()=>{ const b=document.getElementById('btn-sleep265'); return !!(b&&b.offsetParent!==null); })(),
          startDay: (()=>{ const v=document.getElementById('v-home'); if(!v) return false;
            return [...v.querySelectorAll('button')].some(x=>x.offsetParent!==null&&/開始今日行程|開始行程/.test(x.textContent||'')); })(),
          conf: (()=>{ const b=document.getElementById('btn-confirm-plan'); return !!(b&&b.offsetParent!==null&&!b.disabled&&!(b.className||'').includes('is-locked')); })() })""")
        try: st = json.loads(st)
        except Exception: st = {}
        if it % 5 == 1 or (st.get('day') != start_day):
            lg(it, "day=", st.get('day'), "ed=", st.get('ed'), "view=", st.get('view'),
               "mask=", st.get('mask'), "sheet=", st.get('sheet'), "sleep=", st.get('sleep'),
               "startDay=", st.get('startDay'), "conf=", st.get('conf'), "raw=", str(st)[:120] if not isinstance(st, dict) else "")
        if st.get('ed') and st.get('view') == 'v-home' and not st.get('mask'):
            # a fresh editable home after the week boundary (day advanced past start)
            if (st.get('day') or 0) > start_day or conf != 'clicked':
                lg("return ok day", st.get('day'))
                dbg.close()
                return True, f"week done day {start_day}->{st.get('day')} conf={conf}"
        if st.get('mask'):
            # 故事／結算／日結 modal：優先撳推進掣，否則第一粒可見掣
            # （N1「通告板」16 句＋二選一＋確認＋結算＋進度，probe400 驗證過此口徑行得通）
            hit = ev(pg, """() => {
              const all=[...document.querySelectorAll('#modal-btns button, #story-btns button, #story-box button, #story button, #mask button')].filter(x=>x.offsetParent!==null&&!x.disabled);
              const t=all.find(x=>/瞓覺|下一句|跳至選項|繼續|確定|知道了|開始|收到|關閉|下一步|明白/.test(x.textContent||''))
                || all.find(x=>(x.getAttribute('role')||'')==='p')
                || all[all.length-1];
              if(!t) return null; t.click(); return (t.textContent||'').trim().slice(0,30); }""")
            lg(it, "mask click:", hit)
            continue
        if st.get('sheet'):
            # location sheet on the map: close it (roaming handled by going home)
            ev(pg, "() => { const c=document.getElementById('loc-close'); if(c){ c.click(); return true; } return false; }")
            lg(it, "sheet close")
            continue
        if st.get('view') == 'v-home':
            if st.get('conf'):
                ev(pg, "() => { const b=document.getElementById('btn-confirm-plan'); if(b) b.click(); return true; }")
                lg(it, "confirm click")
                continue
            if st.get('startDay'):
                click_btn_text(pg, r'開始今日行程|開始行程', '#v-home')
                lg(it, "startDay click")
                continue
            if st.get('sleep'):
                ev(pg, "() => { const b=document.getElementById('btn-sleep265'); if(b) b.click(); return true; }")
                lg(it, "sleep click")
                continue
            hit = click_btn_text(pg, r'繼續行程|返回地圖', '#v-home')
            if hit:
                lg(it, "home resume:", hit)
                continue
        if st.get('view') == 'v-map':
            # free-roam day: go home (free) then sleep there
            hit = ev(pg, """() => {
              const p=document.querySelector('.pin[data-loc="home"]');
              if(!p) return null; p.click(); return 'home-pin'; }""")
            if hit:
                pg.wait_for_timeout(900)
                # home sheet: enter the house
                hit2 = click_btn_text(pg, r'入屋|返屋企|屋企|回家', '#loc-sheet')
                if not hit2:
                    ev(pg, "() => { const c=document.getElementById('loc-close'); if(c) c.click(); return true; }")
                lg(it, "map home-pin:", hit, hit2)
                continue
        # unknown state: poke a generic continue button if any
        hit = click_btn_text(pg, r'繼續行程|開始今日行程|返回地圖')
        if hit:
            lg(it, "generic poke:", hit)
            continue
        if it % 10 == 0:
            lg(it, "NO ACTION day=", st.get('day'), "view=", st.get('view'), "ed=", st.get('ed'), "mask=", st.get('mask'))
    st = ev(pg, STATE_JS)
    lg("timeout", st and st['dayIndex'], st and st['view'], st and st['homeEditable'])
    dbg.close()
    return False, f"timeout week (day={st and st['dayIndex']} view={st and st['view']} ed={st and st['homeEditable']})"

results = {}

def run_item(pg, name, fn):
    print(f"=== {name} ===", flush=True)
    try:
        results[name] = fn(pg)
    except Exception as e:
        results[name] = {"error": str(e)[:500]}
        print("ERR", name, str(e)[:500], flush=True)
    print(json.dumps({name: results[name]}, ensure_ascii=False)[:1800], flush=True)

def item_w1(pg):
    new_game(pg)
    st = ev(pg, STATE_JS)
    shot(pg, "w1_home")
    ok = bool(st and st["savedPlan"] == ["scout_all","rest","scout_all","scout_all","street","cafe_gig","rest"])
    return {"pass": ok, "weekPlan": st and st["savedPlan"], "dayIndex": st and st["dayIndex"]}

def arrive_week2(pg, mutate=None):
    """Play week 1 as-is; arrive at the editable week-2 home. mutate (dict) is
    applied to live S BEFORE confirming week 1 (enrolled/lastTrain survive the week)."""
    new_game(pg)
    if mutate:
        mutate_S(pg, **mutate)
    ok, note = play_week(pg)
    st = ev(pg, STATE_JS)
    return ok, note, st

def item_w2(pg):
    ok, note, st = arrive_week2(pg, mutate={"enrolled": {"train_vocal": True},
                                            "trainCount": {"train_vocal": 0},
                                            "lastTrain400": "train_vocal"})
    out = {"arrive": {"ok": ok, "note": note}, "dayIndex": st and st["dayIndex"],
           "planDom": st and st["planDom"], "suggest": st and st["suggest"],
           "dayHints": st and [r["hint"] for r in (st["rows"] or [])]}
    out["plan_ids"] = plan_ids(st["rows"]) if st else []
    out["train_slot_free"] = bool(out["plan_ids"] and out["plan_ids"][1] == "scout_all")
    out["both_suggest"] = bool(st and st["suggest"] and st["suggest"]["btns"] == ["沿用上次：歌藝訓練", "補最低屬性：歌藝訓練"])
    shot(pg, "w2_suggest")
    hit = click_btn_text(pg, r'補最低屬性', '#nb-suggest400')
    st2 = ev(pg, STATE_JS)
    out["click_lowest"] = hit
    out["after_lowest_ids"] = plan_ids(st2["rows"]) if st2 else []
    out["after_lowest_cost"] = st2 and st2["cost"]
    out["after_lowest_lastTrain"] = st2 and st2["lastTrain"]
    shot(pg, "w2_after_lowest")
    # reset via 行程工具 menu -> 還原
    click_btn_text(pg, r'行程工具', '#nb-quick')
    pg.wait_for_timeout(500)
    click_btn_text(pg, r'還原', '#nb-tools397-menu')
    pg.wait_for_timeout(600)
    st3 = ev(pg, STATE_JS)
    out["after_reset_ids"] = plan_ids(st3["rows"]) if st3 else []
    hit2 = click_btn_text(pg, r'沿用上次', '#nb-suggest400')
    st4 = ev(pg, STATE_JS)
    out["click_last"] = hit2
    out["after_last_ids"] = plan_ids(st4["rows"]) if st4 else []
    out["after_last_cost"] = st4 and st4["cost"]
    # old save: no lastTrain, nothing enrolled -> no train buttons (re-render via day click)
    mutate_S(pg, enrolled={}, __deleteLastTrain=True)
    click_day_row(pg, 0)
    pg.wait_for_timeout(600)
    st5 = ev(pg, STATE_JS)
    out["old_save_suggest"] = st5 and st5["suggest"]
    out["old_save_no_train_btns"] = bool(st5 and st5["suggest"] and not any("上次" in b or "最低屬性" in b for b in st5["suggest"]["btns"]))
    out["pass"] = bool(ok and out["train_slot_free"] and out["both_suggest"]
                       and out["after_lowest_ids"] and out["after_lowest_ids"][1] == "train_vocal"
                       and out["after_last_ids"] and out["after_last_ids"][1] == "train_vocal"
                       and out["old_save_no_train_btns"]
                       and out["after_lowest_cost"] and not out["after_lowest_cost"]["hidden"]
                       and "歌藝" in (out["after_lowest_cost"]["text"] or ""))
    return out

def item_stress(pg):
    ok, note, st = arrive_week2(pg)
    out = {"arrive": {"ok": ok, "note": note}, "dayIndex": st and st["dayIndex"]}
    # push stress to 85 AFTER arrival (no drift), re-render by clicking a day row
    mutate_S(pg, stress=85)
    click_day_row(pg, 0)
    pg.wait_for_timeout(600)
    st = ev(pg, STATE_JS)
    out["plan_before"] = plan_ids(st["rows"]) if st else []
    out["suggest"] = st and st["suggest"]
    out["stress"] = st and st["stress"]
    out["suggest_shown"] = bool(st and st["suggest"] and not st["suggest"]["hidden"]
                                and any("壓力偏高" in b for b in st["suggest"]["btns"])
                                and any("再加一日休息" in b for b in st["suggest"]["btns"]))
    out["unchanged_before_click"] = bool(out["plan_before"] and out["plan_before"][0] == "scout_all")
    shot(pg, "stress_suggest")
    hit = click_btn_text(pg, r'壓力偏高', '#nb-suggest400')
    st2 = ev(pg, STATE_JS)
    out["click_rest"] = hit
    out["plan_after"] = plan_ids(st2["rows"]) if st2 else []
    out["after_cost"] = st2 and st2["cost"]
    out["suggest_after"] = st2 and st2["suggest"]
    out["pass"] = bool(ok and out["suggest_shown"] and out["unchanged_before_click"]
                       and out["plan_after"] and out["plan_after"][0] == "rest"
                       and st2["cost"] and not st2["cost"]["hidden"]
                       and "壓力清零" in (st2["cost"]["text"] or ""))
    return out

def item_cost(pg):
    ok, note, st = arrive_week2(pg, mutate={"enrolled": {"train_vocal": True},
                                            "trainCount": {"train_vocal": 3},
                                            "lastTrain400": "train_vocal"})
    out = {"arrive": {"ok": ok, "note": note}}
    out["dayHints"] = st and [r["hint"] for r in (st["rows"] or [])]
    out["scout_hint"] = any("本週外出機會剩" in h for h in (out["dayHints"] or []))
    # generic change: select 週三 (index 2), perform tab, pick 街頭表演
    click_day_row(pg, 2)
    pg.wait_for_timeout(400)
    click_cat_tab(pg, r'表演')
    pg.wait_for_timeout(600)
    hit = click_btn_text(pg, r'街頭表演', '#act-list')
    st2 = ev(pg, STATE_JS)
    out["click_street"] = hit
    out["plan_after"] = plan_ids(st2["rows"]) if st2 else []
    out["cost_after"] = st2 and st2["cost"]
    out["hints_after_street"] = st2 and [r["hint"] for r in (st2["rows"] or [])]
    out["train_hint"] = any("再 2 堂升二級" in h for h in (out["hints_after_street"] or []))
    shot(pg, "cost_street")
    # train slot via picker: select 週二, train tab, pick 歌藝訓練 -> day hint + cost line
    click_day_row(pg, 1)
    pg.wait_for_timeout(400)
    click_cat_tab(pg, r'訓練')
    pg.wait_for_timeout(800)
    # 訓練頁籤先揀屬性 chip（預設演技），再出該屬性嘅課程卡
    ev(pg, """() => { const c=document.querySelector('#act-list .guide68-chip[data-gstat="vocal"]');
      if(c) c.click(); return true; }""")
    pg.wait_for_timeout(800)
    card_meta = ev(pg, """() => [...document.querySelectorAll('#act-list .guide68-meta')].map(x=>(x.textContent||'').trim())""")
    out["card_meta"] = card_meta
    out["card_prog"] = any("再 2 堂升二級" in m for m in (card_meta or []))
    hit_train = ev(pg, """() => { const b=document.querySelector('#act-list .train71-pick[data-t71pick="train_vocal"]');
      if(!b) return null; b.click(); return true; }""")
    pg.wait_for_timeout(600)
    st3 = ev(pg, STATE_JS)
    out["click_train_pick"] = hit_train
    out["plan_after_train"] = plan_ids(st3["rows"]) if st3 else []
    out["hints_after_train"] = st3 and [r["hint"] for r in (st3["rows"] or [])]
    out["cost_after_train"] = st3 and st3["cost"]
    out["train_hint"] = any("再 2 堂升二級" in h for h in (out["hints_after_train"] or []))
    out["pass"] = bool(ok and out["scout_hint"] and hit
                       and out["plan_after"] and out["plan_after"][2] == "street"
                       and st2["cost"] and not st2["cost"]["hidden"]
                       and "35–60" in (st2["cost"]["text"] or "")
                       and out["card_prog"] and hit_train
                       and out["plan_after_train"] and out["plan_after_train"][1] == "train_vocal"
                       and out["train_hint"]
                       and st3["cost"] and not st3["cost"]["hidden"]
                       and "歌藝 +1 堂" in (st3["cost"]["text"] or ""))
    return out

def item_novice(pg):
    runs = []
    for r in range(args.runs):
        new_game(pg)
        weekly = []
        ok_all = True
        for w in range(1, args.weeks + 1):
            st0 = ev(pg, STATE_JS)
            ok, note = play_week(pg)
            st1 = ev(pg, STATE_JS)
            weekly.append({"week": w, "ok": ok, "note": note,
                           "start": {"day": st0 and st0["dayIndex"], "money": st0 and st0["money"], "stress": st0 and st0["stress"]},
                           "end": {"day": st1 and st1["dayIndex"], "money": st1 and st1["money"], "stress": st1 and st1["stress"], "sick": st1 and st1["sick"]}})
            if not ok:
                ok_all = False
                break
            pg.wait_for_timeout(500)
        st = ev(pg, STATE_JS)
        runs.append({"run": r + 1, "ok": ok_all, "weeks": weekly,
                     "final": {"day": st and st["dayIndex"], "money": st and st["money"],
                               "stress": st and st["stress"], "sick": st and st["sick"]}})
    return {"runs": runs}

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox',
        '--proxy-server=http://127.0.0.1:18081', '--ignore-certificate-errors'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.set_default_timeout(10000)
    try:
        if 'w1' in ITEMS: run_item(pg, 'w1', item_w1)
        if 'w2' in ITEMS: run_item(pg, 'w2', item_w2)
        if 'stress' in ITEMS: run_item(pg, 'stress', item_stress)
        if 'cost' in ITEMS: run_item(pg, 'cost', item_cost)
        if 'novice' in ITEMS: run_item(pg, 'novice', item_novice)
    finally:
        b.close()
    srv.terminate()

with open(os.path.join(OUT, "drive400.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("WROTE", os.path.join(OUT, "drive400.json"), flush=True)
