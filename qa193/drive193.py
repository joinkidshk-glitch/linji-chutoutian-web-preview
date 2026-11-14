# -*- coding: utf-8 -*-
"""v20a193 實駕 drive193：WF4 once 硬規則 × 932／700，LIVE 模式（唔用 ?softPreview=1）。
用法：/home/hatch/pwenv49/bin/python qa193/drive193.py
Mirror：工作副本 ~/workspace/linji-work193，port 8993。
播種：經 new_game 正常開局（slot 1，key starVolunteer_map_v19w），播完 C1 故事返地圖，
  再 live 改 S.wf4.seen＋S.weekPlan＋saveQ()。
Cases：
  A 事件正常彈出＋見過唔再出：seed seen={set03,st04,cha03,day02}，行最多 45 日（每日入
    星河電視台＋金龍茶餐廳各一次＋開始今日行程／過一日），記錄每次 WF4 modal 標題；
    斷言 ≥1 單事件彈出、全部標題唔同、seeded 嗰 4 單一次都冇出。
  B reload 後 seen-set 仲喺度：reload＋讀檔 slot 1，讀 S.wf4.seen，比對 A 嘅 fired＋seeded。
  C 舊 save 遷移：localStorage 寫入舊形 save（seen 含 set03:21、evDay 舊紀錄、
    pending 指向已見過嘅 set03），reload＋讀檔，斷言 0 pageerror、入到地圖、
    pending 被清走（唔彈 set03）、seen 保留。
  D 抽乾優雅：seed seen＝全部 72 單，行 2 日＋入兩個地點，斷言零 WF4 modal、0 pageerror、地圖正常。
  E v198×v193 互動（slot 3，獨立新局）：C1 電影線→第 15 週（day 98）＋舊 save 式 stale pending
    （seen set03:21、pending 指 set03）同時存在→首次入茶餐廳：斷言 stale pending 清走、
    目標主線幕 C6F 即出（第 6 幕・電影線：片場跟班）、boss01 唔打尖（冇霞姐 modal）、locTries 仲係 0。
    （注意：播完 C6F 再入茶餐廳唔斷言 boss01 即出——v193 pLoc 已跌到 0.03，v198 嗰粒
    seeded roll 0.1535 過唔到，boss01 唔出係頻率所致，唔係 defer 爛咗。）
量度（DOM 為準，截圖只係記錄）：WF4 modal 以 #modal-inner h3 標題∈72 單認；
  pageerror／console error／失敗請求。
"""
import os, json, subprocess, time, signal, hashlib, urllib.request, sys

ROOT = "/home/hatch/workspace/linji-work193"
HERE = os.path.join(ROOT, "qa193")
SHOTS = os.path.join(HERE, "shots193")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"  # 舊路徑執行檔已失蹤，改用 playwright 新下載同一版本 v1248
PORT = 8993
URL = f"http://127.0.0.1:{PORT}/index.html"
REPORT = {"errors": [], "http_fail": [], "cases": {}}

from playwright.sync_api import sync_playwright

TITLES = ["開鏡拜神企前排","一張摺凳嘅人情","飛紙仔殺到埋身","通宵廠凌晨三點","飯盒入面隻雞髀",
"威也衫箍到肋痛","麻雀聲入晒咪","派錯更去錯廠","老戲骨教企位","颱風困住成班人","電視精開咪",
"阿成最後一更","常餐加兩蚊","鄰枱爆大鑊","阿媽煲老火湯","表姨媽問走唔走","鄰居借電話","雪櫃上有剪報",
"Call機響錯人","電話亭長龍","大哥大好惹眼","最後一杯紅豆冰","老闆娘叫霞姐","嗰更邊個頂",
"嗰個位留返畀你","K房霸咪嗰晚","魚檔阿姐認得你","LD舖租碟夜","的士佬送機有感","散班嗰程車",
"茶客講睇場費","回流嘅舊鄰居","颱風日瞓到自然醒","傳呼台嘅一課","銀包見底嗰晚","阿婆嗰碗涼茶",
"冰室門口嗰張櫈","大排檔嗰煲及第粥","電車上面嗰段戲","天台晾衫嗰陣風","唱片舖試聽嗰首歌",
"巴士上層望住個海","茶樓飲早茶聽到消息","街市買餸撞到熟人","電話亭入面嗰個長途","Call機密碼簿唔見咗",
"銀包得返幾蚊","瞓唔着嗰晚數星","廟街夜市嗰檔煲仔飯","渡輪上面嗰陣海風","卡拉OK嗰晚有人點錯歌",
"的士上面聽到嘅電台","返屋企樓下撞到細佬","涼茶舖嗰碗廿四味",
"廠房門口嗰班車","道具房嗰把遮","化妝間嗰面鏡","收工嗰陣嗰句說話","碼頭邊嗰場夜戲",
"道具船上面嗰陣風","錄影廠門口嗰班粉絲","新聞部嗰陣騷動","化妝間借粉底","清水灣嗰陣海風",
"廣播室嗰個電話","飯堂嗰碟叉燒","外景車上面嗰程","紅磡碼頭嗰場戲","道具部嗰個電話",
"茶餐廳嗰張舊枱","老闆娘嗰煲湯","隔籬枱嗰份報紙"]
assert len(TITLES) == 72, len(TITLES)

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

def click_first(pg, texts, wait=900):
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

def modal_click(pg, text):
    return pg.evaluate("""(t) => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const b = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent || '').trim() === t);
      if (!b) return false; b.click(); return true; }""", text)

def read_state(pg):
    return pg.evaluate("""() => {
      if (typeof S === 'undefined' || !S) return null;
      return { day: S.dayIndex, dateStr: S.dateStr || null,
        seen: (S.wf4 && S.wf4.seen) ? S.wf4.seen : null,
        pending: (S.wf4 && S.wf4.pending) ? S.wf4.pending : null,
        lastDay: (S.wf4) ? S.wf4.lastDay : null }; }""")

def wf4_title(pg):
    """而家開緊嘅 modal 係唔係 WF4 事件（h3 標題∈72 單）？返標題或 null。"""
    return pg.evaluate("""(titles) => {
      const h3 = document.querySelector('#modal-inner h3');
      if (!h3) return null;
      const t = (h3.textContent || '').trim();
      return titles.indexOf(t) >= 0 ? t : null; }""", TITLES)

def map_visible(pg):
    return pg.evaluate("() => { const v = document.querySelector('#v-map'); return !!v && v.offsetParent !== null; }")

def story_active(pg):
    return pg.evaluate("""() => {
      const plate = document.querySelector('.story-play .dlg106-plate');
      const choice = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
      return !!plate || choice.length > 0; }""")

def play_story(pg, max_steps=80, pick=None):
    for _ in range(max_steps):
        if not story_active(pg):
            return True
        if pg.evaluate("""(kw) => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
            if (!c.length) return false;
            let i = 0;
            if (kw) { for (let j=0;j<c.length;j++) if ((c[j].textContent||'').indexOf(kw) >= 0) { i = j; break; } }
            c[i].click(); return true; }""", pick):
            pg.wait_for_timeout(1000)
            continue
        if pg.evaluate("() => { const row = document.getElementById('modal-btns'); if (!row) return false; const bs=[...row.querySelectorAll('button')].filter(x=>x.offsetParent!==null && !x.disabled); if (bs.length) { bs[0].click(); return true; } return false; }"):
            pg.wait_for_timeout(900)
            continue
        pg.wait_for_timeout(800)
    return not story_active(pg)

def dismiss_once(pg):
    """處理一個攔截畫面（唔包 WF4 modal——嗰個由 caller 記錄先）。"""
    if wf4_title(pg):
        return False
    r = pg.evaluate("""() => {
      const ov = document.getElementById('enc79-overlay'); if (ov) {
        const sk = ov.querySelector('.e79-skip'); if (sk && sk.offsetParent !== null) { sk.click(); return 'enc-skip'; }
        const ch = ov.querySelector('.e79-choice'); if (ch) { ch.click(); return 'enc-choice'; }
        const nb = [...ov.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
        if (nb) { nb.click(); return 'enc-btn'; } }
      return false; }""")
    if r:
        return r
    if story_active(pg):
        if pg.evaluate("() => { const c=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null); if(c[0]) { c[0].click(); return true; } return false; }"):
            return 'story-choice'
        if pg.evaluate("() => { const row = document.getElementById('modal-btns'); if (!row) return false; const bs=[...row.querySelectorAll('button')].filter(x=>x.offsetParent!==null && !x.disabled); if (bs.length) { bs[0].click(); return true; } return false; }"):
            return 'story-next'
        return False
    r = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false;
      const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return 'modal-btn:' + (bs[0].textContent || '').trim().slice(0,12); }""")
    return r or False

def settle(pg, timeout_ms=15000):
    """等到冇攔截畫面或者超時。返 ('map'|'wf4'|'timeout', wf4title)。"""
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout_ms:
        t = wf4_title(pg)
        if t:
            return ('wf4', t)
        r = dismiss_once(pg)
        if r:
            pg.wait_for_timeout(700)
            continue
        if map_visible(pg):
            return ('map', None)
        pg.wait_for_timeout(600)
    return ('timeout', wf4_title(pg))

def handle_wf4(pg, tag, seen_titles):
    title = wf4_title(pg)
    if not title:
        return None
    seen_titles.append(title)
    pg.screenshot(path=os.path.join(SHOTS, f"{tag}_wf4_{len(seen_titles)}.png"))
    for _ in range(14):
        if not wf4_title(pg):
            break
        clicked = (modal_click(pg, "繼續") or modal_click(pg, "睇落去")
                   or pg.evaluate("""() => { const row = document.getElementById('modal-btns');
                     if (!row) return false;
                     const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
                     if (!bs.length) return false; bs[0].click(); return true; }"""))
        pg.wait_for_timeout(700)
        if not clicked:
            break
    return title

def go_map(pg):
    """返地圖（home 頁撳返回地圖；已經喺地圖就唔郁）。"""
    if map_visible(pg):
        return True
    pg.evaluate("() => { const b=document.getElementById('home-back-map'); if(b && b.offsetParent!==null) b.click(); }")
    pg.wait_for_timeout(1200)
    if map_visible(pg):
        return True
    js_click_text(pg, "返回地圖")
    pg.wait_for_timeout(1200)
    return map_visible(pg)

def load_slot(pg, slot="1"):
    """標題畫面讀檔 → 揀 slot → 等入地圖／home。"""
    click_first(pg, ["讀檔"], 1200)
    pg.evaluate("(s) => { const b = document.querySelector('[data-slot=\"' + s + '\"]'); if (b && b.offsetParent !== null) { b.click(); return true; } return false; }", slot)
    pg.wait_for_timeout(1500)
    click_first(pg, ["覆蓋", "確定", "確認"], 800)
    return settle(pg, timeout_ms=15000)

def new_game(pg, slot="1", pick=None):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("(s) => { const b = document.querySelector('[data-slot=\"' + s + '\"]'); if (b && b.offsetParent !== null) { b.click(); return true; } return false; }", slot)
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
    # C1 開局故事播晒佢（唔喺度 settle——settle 會亂撳 home 頁嘅掣）
    if not play_story(pg, max_steps=80, pick=pick):
        print("WARN: story not cleared", flush=True)
    pg.wait_for_timeout(1500)
    if not go_map(pg):
        # 重試：可能 home-back-map 當刻隱藏，試文字掣
        js_click_text(pg, "返回地圖")
        pg.wait_for_timeout(1200)
        go_map(pg)
    settle(pg, timeout_ms=8000)
    go_map(pg)
    st = read_state(pg)
    print("NEW GAME:", st and st['day'], "map:", map_visible(pg), flush=True)
    return st is not None and map_visible(pg)

def seed_seen(pg, seen_dict):
    r = pg.evaluate("""(seen) => {
      try {
        if (typeof S === 'undefined' || !S) return {ok:false, err:'no S'};
        if (!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = { lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false };
        for (const k of Object.keys(seen)) S.wf4.seen[k] = seen[k];
        S.wf4.seen.__n = Object.keys(S.wf4.seen).filter(k=>k!=='__n').reduce((a,k)=>a+(S.wf4.seen[k]||0),0);
        S.weekPlan = S.weekPlan || [];
        for (let i=0;i<7;i++) S.weekPlan[i]='rest';
        try { saveQ(); } catch(e){}
        return {ok:true, seen: S.wf4.seen};
      } catch(e){ return {ok:false, err:String(e)}; } }""", seen_dict)
    print("SEED:", r, flush=True)
    return r.get('ok')

def reseed_week_rest(pg):
    pg.evaluate("""() => {
      try { S.weekPlan = []; for (let i=0;i<7;i++) S.weekPlan[i]='rest'; try{ saveQ(); }catch(e){} return true; } catch(e){ return false; } }""")
    pg.reload(); pg.wait_for_timeout(2500)
    load_slot(pg, "1")
    go_map(pg)

def visit_loc(pg, loc_id, tag, seen_titles):
    if not go_map(pg):
        return ('not-on-map', None)
    ok = pg.evaluate("""(loc) => {
      const b = document.querySelector('button[data-loc="' + loc + '"]');
      if (!b || b.offsetParent === null) return false; b.click(); return true; }""", loc_id)
    pg.wait_for_timeout(1200)
    if not ok:
        return ('no-btn', None)
    t = wf4_title(pg)
    if t:
        title = handle_wf4(pg, tag + '_' + loc_id, seen_titles)
        pg.wait_for_timeout(800)
        settle(pg, timeout_ms=8000)
        go_map(pg)
        return ('wf4', title)
    settle(pg, timeout_ms=8000)
    js_click_text(pg, "返回地圖")
    pg.wait_for_timeout(800)
    settle(pg, timeout_ms=8000)
    go_map(pg)
    return ('sheet', None)

def start_today(pg, tag, seen_titles):
    day0 = (read_state(pg) or {}).get('day')
    # 1. 開始今日行程（有 soft 行程嗰日）2. 過一日（自由日）3. 冇掣→重設本週 rest＋reload
    clicked = pg.evaluate("""() => {
      const b = document.getElementById('map-start-today');
      if (b && b.offsetParent !== null) { b.click(); return 'start'; }
      const e = document.getElementById('map-end-day');
      if (e && e.offsetParent !== null) { e.click(); return 'endday'; }
      return false; }""")
    pg.wait_for_timeout(1000)
    if not clicked:
        reseed_week_rest(pg)
        clicked = pg.evaluate("""() => {
          const b = document.getElementById('map-start-today');
          if (b && b.offsetParent !== null) { b.click(); return 'start'; }
          const e = document.getElementById('map-end-day');
          if (e && e.offsetParent !== null) { e.click(); return 'endday'; }
          return false; }""")
        pg.wait_for_timeout(1000)
    if not clicked:
        return ('no-start-btn', day0)
    t0 = time.time()
    while time.time() - t0 < 45:
        t = wf4_title(pg)
        if t:
            handle_wf4(pg, tag + '_day', seen_titles)
            pg.wait_for_timeout(700)
            continue
        r = dismiss_once(pg)
        if r:
            pg.wait_for_timeout(700)
            continue
        st = read_state(pg)
        if st and day0 is not None and st['day'] != day0 and map_visible(pg):
            return ('advanced', st['day'])
        pg.wait_for_timeout(600)
    st = read_state(pg)
    return ('timeout', st and st['day'])

def run_case_a(pg):
    titles = []
    days = 0
    max_days = 45
    while days < max_days and len(titles) < 3:
        st = read_state(pg)
        if not st:
            return {'ok': False, 'why': 'no S', 'titles': titles, 'days': days}
        for loc in ['tvb_longmen', 'cafe_cha']:
            visit_loc(pg, loc, f"A_d{st['day']}", titles)
            if len(titles) >= 3:
                break
        if len(titles) >= 3:
            break
        r, day1 = start_today(pg, f"A_d{st['day']}", titles)
        days += 1
        print(f"A day {st['day']} -> {day1} ({r}), wf4 so far: {titles}", flush=True)
        if r == 'no-start-btn':
            break
    seeded_titles = {"飛紙仔殺到埋身", "最後一杯紅豆冰", "常餐加兩蚊", "傳呼台嘅一課"}
    leaked = [t for t in titles if t in seeded_titles]
    return {'ok': len(titles) >= 1 and not leaked and len(titles) == len(set(titles)),
            'titles': titles, 'days': days, 'leaked': leaked,
            'distinct': len(set(titles))}

ALL72 = ["wf4_ev_set01","wf4_ev_set02","wf4_ev_set03","wf4_ev_set04","wf4_ev_set05","wf4_ev_set06","wf4_ev_set07","wf4_ev_set08","wf4_ev_set09","wf4_ev_set10","wf4_ev_cha01","wf4_ev_cha02","wf4_ev_cha03","wf4_ev_cha04","wf4_ev_home01","wf4_ev_home02","wf4_ev_home03","wf4_ev_home04","wf4_ev_st01","wf4_ev_st02","wf4_ev_st03","wf4_ev_st04","wf4_ev_boss01","wf4_ev_boss02","wf4_ev_boss03","wf4_ev_st05","wf4_ev_st06","wf4_ev_st07","wf4_ev_st08","wf4_ev_st09","wf4_ev_st10","wf4_ev_st11","wf4_ev_day01","wf4_ev_day02","wf4_ev_day03","wf4_ev_day04","wf4_ev_day05","wf4_ev_day06","wf4_ev_day07","wf4_ev_day08","wf4_ev_day09","wf4_ev_day10","wf4_ev_day11","wf4_ev_day12","wf4_ev_day13","wf4_ev_day14","wf4_ev_day15","wf4_ev_day16","wf4_ev_st12","wf4_ev_st13","wf4_ev_st14","wf4_ev_st15","wf4_ev_st16","wf4_ev_st17","wf4_ev_set11","wf4_ev_set12","wf4_ev_set13","wf4_ev_set14","wf4_ev_set15","wf4_ev_set16","wf4_ev_set17","wf4_ev_set18","wf4_ev_set19","wf4_ev_set20","wf4_ev_set21","wf4_ev_set22","wf4_ev_set23","wf4_ev_set24","wf4_ev_set25","wf4_ev_cha05","wf4_ev_cha06","wf4_ev_cha07"]

def story_act191(pg):
    return pg.evaluate("""() => {
      const act = document.querySelector('.sp-act191');
      const plate = document.querySelector('.story-play .dlg106-plate');
      const h3 = document.querySelector('.sp-head-opening h3');
      return { active: !!plate || !!document.querySelector('.sp-head-opening'),
        act191: act ? act.textContent.trim() : null,
        nodeTitle: h3 ? h3.textContent.trim() : null }; }""")

def close_loc_sheet(pg):
    """關地點 sheet（#loc-close「返回地圖」）——呢個掣嘅 onclick 先 closeSheet 再
    story165TryForcedPlay：強制播係喺閂 sheet 嗰陣先觸發，唔係入場嗰陣。
    （drive198 嘅 run_forced_case 都係 open → close_loc → 讀故事；淨係讀入場嗰刻會見唔到故事。）"""
    hit = pg.evaluate("""() => {
      const sh = document.getElementById('loc-sheet'); if (!sh) return false;
      const b = [...sh.querySelectorAll('button')].find(x => x.offsetParent !== null && (x.textContent||'').trim() === '返回地圖');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    return hit

def run_case_e(pg):
    """E：v198×v193 互動。獨立新局 slot 3：C1 電影線 → day 98（第 15 週）→
    seed stale pending（seen set03:21、pending 指 set03）→ 首次入茶餐廳。
    斷言：入場嗰刻 stale pending 清走、boss01 唔打尖、locTries 仲係 0；
    閂 sheet 之後目標主線幕 C6F 即出（第 6 幕・電影線：片場跟班），播完 mark done。"""
    assert new_game(pg, slot="3", pick="接電影散工賺快錢"), "new game E failed"
    pg.wait_for_timeout(1500)
    click_first(pg, ["關閉"], 800)
    go_map(pg)
    settle(pg, timeout_ms=8000)
    go_map(pg)
    seed = pg.evaluate("""() => {
      try {
        S.dayIndex = 98;
        // 跟 drive198 A_film 播種：C1 已播完，C2–C5 done＋lastDoneDay 90，C6F 先開到
        S.story.done = Object.assign({}, S.story.done, { C1: true, C2: true, C3: true, C4: true, C5: true });
        S.story.lastMainDoneDay = 90;
        S.fame = 26; S.industryCredit = 49; S.money = 14936;
        try { StoryOC.syncPhaseFromProgress(); } catch(e){}
        let open = null;
        try { const oc = StoryOC.listOpen({checkNodePhase:true, player:true, ignoreSheetLoc:true});
          open = (oc.open||[]).map(r=>r.id); } catch(e){ open = 'StoryOC-unreachable:' + String(e); }
        // 舊 save 式 stale pending：set03 見過 21 次，pending 仲指住佢
        if (!S.wf4) S.wf4 = { lastDay:-99, seen:{}, pending:null, pendingDay:-99, flags:{}, evDay:{}, locDay:-99, locTries:0, fenFarewellDone:false };
        S.wf4.seen['wf4_ev_set03'] = 21;
        S.wf4.seen.__n = 21;
        S.wf4.pending = 'wf4_ev_set03'; S.wf4.pendingDay = 98;
        S.wf4.lastDay = 95; S.wf4.locDay = -99; S.wf4.locTries = 0;
        try { saveQ(); } catch(e){}
        return {ok:true, day: S.dayIndex, week: Math.floor(S.dayIndex/7)+1, open: open,
          pending: S.wf4.pending, locTries: S.wf4.locTries};
      } catch(e){ return {ok:false, err:String(e)}; } }""")
    print("E seed:", seed, flush=True)
    if not go_map(pg):
        return {'ok': False, 'why': 'not-on-map-after-seed', 'seed': seed}
    ok = pg.evaluate("""() => {
      const b = document.querySelector('button[data-loc="cafe_cha"]');
      if (!b || b.offsetParent === null) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1500)
    st = read_state(pg)
    tries = pg.evaluate("() => (S.wf4 ? S.wf4.locTries : null)")
    wf4t = wf4_title(pg)
    print("E entry: clicked:", ok, "state:", st, "locTries:", tries, "wf4title:", wf4t, flush=True)
    entry_ok = bool(ok) and bool(st) and st.get('pending') is None and tries == 0 and wf4t is None
    # 強制播喺閂 sheet 嗰陣先觸發：閂咗再讀故事
    closed = close_loc_sheet(pg)
    sp = story_act191(pg)
    print("E after close: closed:", closed, "story:", sp, flush=True)
    pg.screenshot(path=os.path.join(SHOTS, "E_story_open.png"))
    res = {'ok': entry_ok and bool(closed)
           and sp.get('act191') == "第 6 幕・電影線：片場跟班",
           'entry_ok': entry_ok, 'closed': closed,
           'seed': seed, 'state': st, 'locTries': tries, 'story': sp, 'wf4title': wf4t}
    # 播埋 C6F，核實目標幕真係播完 mark done（唔係齋彈個頭）
    if sp.get('active'):
        play_story(pg, max_steps=80)
        pg.wait_for_timeout(800)
        click_first(pg, ["關閉"], 800)
        done = pg.evaluate("() => { try { return { c6f: StoryOC.isDone('C6F') }; } catch(e){ return { err: String(e) }; } }")
        print("E C6F done:", done, flush=True)
        res['c6f_done'] = done
        res['ok'] = res['ok'] and done.get('c6f') is True
    return res

def main():
    srv = serve(ROOT)
    try:
        with sync_playwright() as pw:
            for height, tag in [(844, '932'), (700, '700')]:
                br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
                pg = br.new_page(viewport={"width": 390, "height": height})
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) else None)
                pg.on("requestfailed", lambda r: REPORT["http_fail"].append(r.url))
                if tag == '932':
                    assert new_game(pg, slot="1"), "new game failed"
                    assert seed_seen(pg, {"wf4_ev_set03": 1, "wf4_ev_st04": 1, "wf4_ev_cha03": 1, "wf4_ev_day02": 1}), "seed failed"
                    pg.screenshot(path=os.path.join(SHOTS, "A_map_start.png"))
                    resA = run_case_a(pg)
                    REPORT["cases"]["A_events"] = resA
                    before = read_state(pg)
                    pg.reload(); pg.wait_for_timeout(2500)
                    load_slot(pg, "1")
                    after = read_state(pg)
                    seen_before = (before or {}).get('seen') or {}
                    seen_after = (after or {}).get('seen') or {}
                    kept = all((seen_after.get(k) or 0) >= v for k, v in seen_before.items() if k != '__n')
                    REPORT["cases"]["B_reload_seen"] = {"ok": kept and after is not None,
                        "before_n": len([k for k in seen_before if k != '__n']),
                        "after_n": len([k for k in seen_after if k != '__n']),
                        "errors": errs}
                    print("B:", REPORT["cases"]["B_reload_seen"], flush=True)
                    r = pg.evaluate("""() => {
                      try {
                        const raw = localStorage.getItem('starVolunteer_map_v19w');
                        if (!raw) return {ok:false, err:'no save'};
                        const o = JSON.parse(raw);
                        const day = (o.dayIndex|0);
                        o.wf4 = { lastDay: day - 5, seen: { 'wf4_ev_set03': 21, 'wf4_ev_st04': 7, 'wf4_ev_cha03': 2, __n: 30 },
                          pending: 'wf4_ev_set03', pendingDay: day, flags: {}, evDay: { 'wf4_ev_set03': day - 5, 'wf4_ev_st04': day - 3 },
                          locDay: -99, locTries: 0, fenFarewellDone: false };
                        localStorage.setItem('starVolunteer_map_v19w', JSON.stringify(o));
                        return {ok:true, day};
                      } catch(e){ return {ok:false, err:String(e)}; } }""")
                    print("C seed old save:", r, flush=True)
                    pg.reload(); pg.wait_for_timeout(2500)
                    load_slot(pg, "1")
                    go_map(pg)
                    # pending 守衛喺 wf4PresentPending（返地圖嗰陣行）：入一個地點再返嚟觸發佢
                    visit_loc(pg, 'cafe_cha', "C", [])
                    stC = read_state(pg)
                    REPORT["cases"]["C_old_save"] = {"ok": bool(stC) and (stC.get('pending') is None)
                        and (stC.get('seen') or {}).get('wf4_ev_set03') == 21,
                        "state": stC, "errors": errs}
                    print("C:", REPORT["cases"]["C_old_save"], flush=True)
                    seed_seen(pg, {})
                    r = pg.evaluate("""(evs) => {
                      try {
                        for (const id of evs) S.wf4.seen[id] = 1;
                        S.wf4.pending = null;
                        try { saveQ(); } catch(e){}
                        return {ok:true, n: evs.length};
                      } catch(e){ return {ok:false, err:String(e)}; } }""", ALL72)
                    print("D seed all seen:", r, flush=True)
                    titlesD = []
                    for loc in ['tvb_longmen', 'cafe_cha']:
                        visit_loc(pg, loc, "D", titlesD)
                    start_today(pg, "D", titlesD)
                    for loc in ['tvb_longmen', 'cafe_cha']:
                        visit_loc(pg, loc, "D2", titlesD)
                    start_today(pg, "D2", titlesD)
                    stD = read_state(pg)
                    REPORT["cases"]["D_exhausted"] = {"ok": len(titlesD) == 0 and bool(stD) and map_visible(pg),
                        "wf4_titles_seen": titlesD, "state_day": stD and stD['day'], "errors": errs}
                    print("D:", REPORT["cases"]["D_exhausted"], flush=True)
                    pg.screenshot(path=os.path.join(SHOTS, "D_map_end.png"))
                    resE = run_case_e(pg)
                    REPORT["cases"]["E_v198x193"] = resE
                    print("E:", json.dumps(resE, ensure_ascii=False), flush=True)
                else:
                    assert new_game(pg, slot="1"), "new game 700 failed"
                    assert seed_seen(pg, {"wf4_ev_set03": 1}), "seed 700 failed"
                    titles = []
                    for _ in range(5):
                        st = read_state(pg)
                        if not st:
                            break
                        visit_loc(pg, 'cafe_cha', "S700", titles)
                        start_today(pg, "S700", titles)
                    REPORT["cases"]["smoke_700"] = {"ok": read_state(pg) is not None,
                        "titles": titles, "errors": errs}
                    print("700 smoke:", REPORT["cases"]["smoke_700"], flush=True)
                REPORT["cases"][f"errors_{tag}"] = errs
                br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive193_report.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=2)
    print(json.dumps(REPORT, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
