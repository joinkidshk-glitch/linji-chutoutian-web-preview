# -*- coding: utf-8 -*-
"""v20a107 實駕（本地鏡像＝線上版逐檔下載＋sha 核對後先駕）：
  A. 舊檔相容：v106 pristine（linji-pristine107，8d19640）開局→標記→saveToSlot(3)，
     同一瀏覽器 context／同一 origin（127.0.0.1:8947）換 v107 鏡像→繼續→驗證還原。
  B. C1 tier 2：新遊戲＋設 1 張 lead 通告已完成 → enc79PlayerTier()===2，
     播 C1 到阿偉 think 句，驗 awi_s2_think.webp 出現＋截圖。
  C. C1 tier 3：新遊戲＋設 3 張 lead 通告＋fame 70 → tier 3，
     播 C1 到同一 think 句，驗 awi_s3_think.webp 出現＋截圖。
  D. 蘇芷茵巧遇：入灣仔唱片公司（rec_wanchai），day 種子唔中就改
     S.dayIndex 重骰（1991 春窗口日 424 起，試到 435）；播到首句 happy
     「多謝大家，今日真係好多謝大家支持……」驗 so_jiyan_smile.webp＋截圖。
     注意：主 script 係 IIFE，enc79PlayEncounter／enc79PlayerTier 唔係全域，
     唔可以用 evaluate 直叫——tier 靠 S.flags＋S.fame 設，真 tier 由渲染驗證。
  390×844、Playwright、可棄用槽 3。零 pageerror 為 PASS 條件之一。
用法：pwenv49 python qa107/drive107.py
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
W107 = os.path.dirname(HERE)
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
# 注意：8931/8933/8941 已俾其他 worker 嘅 http.server 佔用；用 8947 避開。
# serve() 會驗證 bind＋線上 index sha，防靜靜伺服緊第二個目錄。
PORT = 8947
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107"
EXPECTED_INDEX_SHA = hashlib.sha256(open(os.path.join(W107, "index.html"), "rb").read()).hexdigest()
NEW_ASSET = ("assets/story/fullbody/so_jiyan_smile.webp", 297704)
LOG = {"compat": {}, "c1_s2": [], "c1_s3": [], "so_smile": [], "errors": [], "method": {}, "server": {}}

def http_get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd, check_index=True):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} probably taken)")
    if check_index:
        st, body = http_get("index.html")
        sha = hashlib.sha256(body).hexdigest()
        exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
        if st != 200 or sha != exp:
            raise RuntimeError(f"served index mismatch: status={st} sha={sha[:12]} expected={exp[:12]} (wrong dir/port collision?)")
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

JS_STORY = '''() => {
  const chars = [...document.querySelectorAll('.dlg106-char')].map(im => ({
    id: im.dataset.dlgId, src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
    filter: im.style.filter }));
  const sp = document.querySelector('.story-play');
  const speaker = document.querySelector('.story-play .sp-speaker');
  const line = document.querySelector('.story-play .sp-line');
  const choices = [...document.querySelectorAll('.sp-choice')].map(b => b.textContent.trim().slice(0,30));
  return { active: !!sp, chars, speaker: speaker ? speaker.textContent : null,
           line: line ? line.textContent.slice(0,70) : null, choices };
}'''

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return { present: false };
  const one = (sel) => { const im = ov.querySelector(sel); if (!im) return null;
    return { src: (im.getAttribute('src')||'').split('/').pop().split('?')[0], filter: im.style.filter,
             k106: im.dataset.k106 || null, ci: (typeof im._ci106 === 'number' ? im._ci106 : null) }; };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  return { present: true, L: one('.e79-char-l'), R: one('.e79-char-r'),
           name: name ? name.textContent : null,
           line: line ? line.textContent.slice(0,70) : null,
           hasChoice: !!ov.querySelector('.e79-choice') };
}'''

def new_game(pg):
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    # 有存檔時「新遊戲」會彈槽位選擇器（probe_newgame.py 實測：列出槽 1/2/3＋關閉，
    # 唔揀槽就停喺度、S 保持 null）——揀可棄用槽 3；冇存檔時唔出選擇器，直接開始。
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
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

def start_tiered_game(pg, n_lead, fame):
    """新遊戲＋設 tier；新遊戲失敗就重試一次。回傳 tier 或 None。"""
    for attempt in (1, 2):
        ok = new_game(pg)
        print(f"  new_game attempt {attempt}: {ok}")
        if not ok:
            continue
        r = set_tier(pg, n_lead, fame)
        print(f"  set_tier: {r}")
        return r["expected_tier"]
    return None

def safe_phase(tag, fn):
    try:
        return fn()
    except Exception as e:
        print(f"  !! phase {tag} exception: {e}")
        LOG["method"].setdefault(tag, {})["error"] = str(e)[:300]
        return None

def set_tier(pg, n_lead, fame):
    """設 tier 用嘅狀態（S.flags done_<lead gig>＋S.fame）。
    注意：主 script 係 IIFE，enc79PlayerTier 唔係全域，evaluate 叫唔到——
    預期 tier 按同一規則（lead>=3 且 fame>=70→3；lead>=1→2；否則 0，
    本包只設 lead 旗，sup 計 0）喺 Python 計；真 tier 由渲染結果驗證
    （C1 think 步出邊個 awi_sN_think 檔）。"""
    r = pg.evaluate("""(arg) => {
      const leads = (typeof GIGS !== 'undefined' ? GIGS : [])
        .filter(g => g && /lead/.test(String(g.roleScale || ''))).slice(0, 3).map(g => g.id);
      S.flags = S.flags || {};
      for (let i = 0; i < arg.n; i++) S.flags['done_' + leads[i]] = 1;
      if (arg.fame) S.fame = arg.fame;
      return { leads };
    }""", {"n": n_lead, "fame": fame})
    exp = 3 if (n_lead >= 3 and fame >= 70) else (2 if n_lead >= 1 else 0)
    return {"leads": r["leads"], "expected_tier": exp}

def play_c1(pg, target_src, tag):
    """播 C1 直到有角色用 target_src；回傳 (found_step, found_line)。"""
    print("enter agency:", click_first(pg, ["何生事務所"], 1800))
    pg.wait_for_timeout(800)
    st = pg.evaluate(JS_STORY)
    if not st["active"]:
        pg.evaluate("() => { const b = document.getElementById('map-progress-btn'); if (b) b.click(); }")
        pg.wait_for_timeout(1200)
        played = pg.evaluate('''() => { const b = document.querySelector('[data-prog77-play="C1"]');
          if (b) { b.click(); return true; } return false; }''')
        print("C1 play button (progress):", played)
        pg.wait_for_timeout(1500)
    found = None
    for step in range(40):
        info = pg.evaluate(JS_STORY)
        LOG[tag].append(info)
        srcs = [(c["id"], c["src"]) for c in info["chars"]]
        print(f" C1-{tag}[{step}] spk={info['speaker']} line={info['line']} chars={srcs}")
        if info["active"] and any(c["src"] == target_src for c in info["chars"]):
            pg.screenshot(path=f"{SHOTS}/{tag}.png")
            found = (step, info["line"])
            print(f"  >> {tag} FOUND at step {step}: {info['line']}")
            break
        if info["choices"]:
            click_first(pg, [info["choices"][0][:6]], 1500)
            pg.wait_for_timeout(1200)
            for _ in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續"], 900):
                    break
            break
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            print("  （冇下一句掣，停）"); break
        pg.wait_for_timeout(500)
    return found

def finish_encounter_if_any(pg):
    for _ in range(40):
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            return False
        clicked = pg.evaluate('''() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          return null; }''')
        if not clicked:
            return True
        pg.wait_for_timeout(350)
    return True

def step_encounter(pg, target_src, tag, max_steps=32):
    """播緊開緊嘅巧遇 overlay 直到 target_src 出現；回傳 found step、
    'wrong-star'（途中出現非目標角名）或 None。"""
    for i in range(max_steps):
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            return None
        LOG[tag].append(info)
        print(f" ENC {tag}[{i}] name={info['name']} line={info['line']} L={info['L']} R={info['R']}")
        if info["name"] and info["name"] not in ("蘇芷茵", "阿偉"):
            print(f"  >> wrong star: {info['name']}")
            return "wrong-star"
        if any((c or {}).get("src") == target_src for c in (info["L"], info["R"])):
            pg.screenshot(path=f"{SHOTS}/{tag}.png")
            print(f"  >> {tag} FOUND at step {i}")
            return i
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""")
        if not clicked:
            return None
        pg.wait_for_timeout(420)
    return None

# ================= 主流程：單一 browser／context；compat 段中途換 server（同 origin） =================
srv = serve("/home/hatch/workspace/linji-pristine107")
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        # ---- A：v106 開局＋標記＋存槽 3 ----
        print("== compat phase 1 (v106) ==")
        print("new game:", new_game(pg))
        ok1 = pg.evaluate("""() => {
          if (!(window.S && typeof window.S.dayIndex === 'number')) return 'noS';
          window.S.money = 106107;
          window.S.dayIndex = 3;
          window.S.flags = window.S.flags || {};
          window.S.flags.qa107mark = 'v106-slot3';
          return 'marked'; }""")
        click_first(pg, ["☰"], 900)
        pg.evaluate("() => { const b = document.querySelector('[data-m=\"save\"]'); if (b) b.click(); }")
        pg.wait_for_timeout(1200)
        saved = pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
          if (!b) return 'nobtn'; b.click(); return 'clicked'; }""")
        pg.wait_for_timeout(1000)
        click_first(pg, ["覆蓋", "確定", "確認"], 900)
        chk = pg.evaluate("""() => { const r = localStorage.getItem('starVolunteer_map_v19w_slot3');
          if (!r) return null; const o = JSON.parse(r);
          return { money: o.money, dayIndex: o.dayIndex, mark: o.flags && o.flags.qa107mark }; }""")
        LOG["compat"]["save_v106"] = {"mark": ok1, "slot_btn": saved, "slot3": chk}
        print("v106 saveToSlot:", ok1, saved, chk)
        pg.screenshot(path=f"{SHOTS}/compat_v106_saved.png")
        # ---- 換 server：同一 browser／context／origin（127.0.0.1:8947），localStorage 留低 ----
        stop(srv)
        srv = serve(W107)   # v107 鏡像（main 16363f3；index＋8 資產 sha 已同線上逐一核對）
        # 硬驗：新資產必須由呢個 server 200 返嚟、byte 數啱（run 3 教訓：port 俾 work108b
        # 佔咗，serve 靜靜失敗，全程駕緊人哋個版本，新檔全部 404 退 base）
        st, body = http_get(NEW_ASSET[0])
        LOG["server"]["new_asset"] = {"status": st, "bytes": len(body), "expected": NEW_ASSET[1],
                                       "match": st == 200 and len(body) == NEW_ASSET[1]}
        print("server new-asset check:", LOG["server"]["new_asset"])
        if not LOG["server"]["new_asset"]["match"]:
            raise RuntimeError("new asset NOT served by this server — aborting drive")
        # ---- B：繼續 v106 槽 3 ----
        print("== compat phase 2 (v107 continue) ==")
        pg.goto(URL); pg.wait_for_timeout(3000)
        # #btn-cont 係 display:none 起步，boot 完成先顯示；等佢現身再撳（唔係靠估）
        cont = pg.evaluate("""() => {
          const b = document.getElementById('btn-cont');
          return b ? { visible: b.offsetParent !== null, text: (b.textContent || '').trim() } : null; }""")
        print("btn-cont at +3s:", cont)
        for _ in range(10):
            vis = pg.evaluate("""() => { const b = document.getElementById('btn-cont');
              return !!(b && b.offsetParent !== null); }""")
            if vis:
                break
            pg.wait_for_timeout(1000)
        print("continue click:",
              pg.evaluate("""() => { const b = document.getElementById('btn-cont');
                if (b && b.offsetParent !== null) { b.click(); return 'btn-cont'; } return null; }""")
              or click_first(pg, ["繼續"], 1800))
        pg.wait_for_timeout(1200)
        restored = pg.evaluate("""() => {
          if (!(window.S && typeof window.S.dayIndex === 'number')) return null;
          return { money: window.S.money, dayIndex: window.S.dayIndex,
                   mark: window.S.flags && window.S.flags.qa107mark }; }""")
        LOG["compat"]["restored_v107"] = restored
        LOG["compat"]["PASS"] = (restored == {"money": 106107, "dayIndex": 3, "mark": "v106-slot3"})
        print("restored:", restored, "PASS:", LOG["compat"]["PASS"])
        pg.screenshot(path=f"{SHOTS}/compat_v107_restored.png")

        # ---- C：C1 tier 2 ----
        print("== C1 tier2 ==")
        def _c1s2():
            t = start_tiered_game(pg, 1, 0)
            if t != 2:
                LOG["method"]["c1_s2"] = {"found": None, "tier": t}
                return None
            f2 = play_c1(pg, "awi_s2_think.webp", "c1_s2")
            LOG["method"]["c1_s2"] = {"found": f2, "tier": t}
            print("C1 s2 found:", f2)
            return f2
        safe_phase("c1_s2", _c1s2)

        # ---- D：C1 tier 3（新遊戲重開） ----
        print("== C1 tier3 ==")
        def _c1s3():
            t = start_tiered_game(pg, 3, 70)
            if t != 3:
                LOG["method"]["c1_s3"] = {"found": None, "tier": t}
                return None
            f3 = play_c1(pg, "awi_s3_think.webp", "c1_s3")
            LOG["method"]["c1_s3"] = {"found": f3, "tier": t}
            print("C1 s3 found:", f3)
            return f3
        safe_phase("c1_s3", _c1s3)

        # ---- E：蘇芷茵巧遇 ----
        print("== so_jiyan encounter ==")
        def back_to_map(pg):
            # C1 抉擇後仲有尾段對白（story-play 仍 active 時「返回地圖」撳極都唔郁）：
            # 先逐句行完，再返地圖，最後驗地圖上有「灣仔唱片」掣。
            for _ in range(20):
                st = pg.evaluate(JS_STORY)
                if not st["active"]:
                    break
                clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
                  if (row) { const bb = [...row.querySelectorAll('button')].find(x => x.offsetParent !== null);
                    if (bb) { bb.click(); return 'modal'; } }
                  const nx = [...document.querySelectorAll('button')].find(x => (x.textContent||'').includes('下一句') && x.offsetParent !== null);
                  if (nx) { nx.click(); return 'next'; } return null; }""")
                if not clicked:
                    break
                pg.wait_for_timeout(700)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 1200)
            pg.wait_for_timeout(800)
            on_map = pg.evaluate("""() => [...document.querySelectorAll('button')]
              .some(b => (b.textContent || '').includes('灣仔唱片'))""")
            print("  back_to_map on_map:", on_map)
            return on_map
        on_map = back_to_map(pg)
        found_so = None
        method = None
        if not on_map:
            print("  !! NOT on map — so phase cannot open rec_wanchai; aborting phase E")
            LOG["method"]["so_smile"] = {"found_step": None, "method": "ABORT: not on map after C1"}
        else:
            # 先試 day0 入場；唔中就逐日改 dayIndex 重骰（1991 春窗口日 424 起）
            for day in [None, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435]:
                if day is not None:
                    pg.evaluate("(d) => { S.dayIndex = d; S.starDay = null; }", day)
                    print(f"  try dayIndex={day}")
                click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)
                print("open rec_wanchai:", click_first(pg, ["灣仔唱片", "灣仔", "唱片"], 1800))
                pg.wait_for_timeout(900)
                info = pg.evaluate(JS_ENC)
                if not info["present"]:
                    print("  （入場冇觸發巧遇）")
                    click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)
                    continue
                print(f"  overlay: name={info['name']} line={info['line']}")
                found_so = step_encounter(pg, "so_jiyan_smile.webp", "so_smile")
                method = f"UI入場 dayIndex={pg.evaluate('() => S.dayIndex')}"
                if isinstance(found_so, int):
                    break
                finish_encounter_if_any(pg)
                click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)
                found_so = None
        LOG["method"]["so_smile"] = {"found_step": found_so, "method": method}
        print("so smile found:", found_so, "method:", method)
        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

LOG["PASS"] = bool(LOG["compat"].get("PASS")
                   and (LOG["method"].get("c1_s2") or {}).get("found") is not None
                   and (LOG["method"].get("c1_s3") or {}).get("found") is not None
                   and (LOG["method"].get("so_smile") or {}).get("found_step") is not None
                   and not LOG["errors"])
print("pageerrors:", LOG["errors"][:6])
print("OVERALL PASS:", LOG["PASS"])
with open(os.path.join(HERE, "drive_log107.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
