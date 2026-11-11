# -*- coding: utf-8 -*-
"""v20a109 A 線實駕：對話舞台 per-character 身高比（pre/post 對照共用）。
   用法：/home/hatch/pwenv49/bin/python drive109a.py <repo-root> <pre|post> [port]
   流程：本地 http.server → 新遊戲（槽 3 可棄用）→ C1 主線（阿偉×何生）量度
         → 直接 enc79PlayEncounter 開三段巧遇首句：彭少祺@ad_central、
         鍾楚凝@rec_star、顧明輝@tvb_harbour（forceFirst，同一句 pre/post 對照）。
   產出：qa109a/shots/<tag>_*.png ＋ qa109a/drive_<tag>.json
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = sys.argv[1]
TAG = sys.argv[2] if len(sys.argv) > 2 else "pre"
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 8961
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107"
ERRORS = []
LOG = {"tag": TAG, "root": ROOT, "errors": ERRORS, "c1": {}, "enc": {}}

def http_get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} taken?)")
    st, body = http_get("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    if st != 200 or sha != exp:
        raise RuntimeError(f"served index mismatch: {st} sha={sha[:12]} expected={exp[:12]}")
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
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

def back_to_map(pg):
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
    return pg.evaluate("""() => !!document.getElementById('map-hint') && !!document.getElementById('map-hint').offsetParent""")

JS_STORY = '''() => {
  const sp = document.querySelector('.story-play');
  if (!sp) return { active: false };
  const speaker = document.querySelector('.story-play .sp-speaker');
  const plate = document.querySelector('.story-play .sp-plate');
  const line = document.querySelector('.story-play .sp-line');
  const stage = document.querySelector('.story-play .sp-stage');
  return { active: true, speaker: speaker ? speaker.textContent : null,
    plateTop: plate ? +plate.getBoundingClientRect().top.toFixed(1) : null,
    charHVar: stage ? (getComputedStyle(stage).getPropertyValue('--dlg108-char-h') || '').trim() : null,
    line: line ? line.textContent : null,
    choices: [...document.querySelectorAll('.sp-choice')].map(b => b.textContent.trim().slice(0,30)) };
}'''

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return { present: false };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  const box = ov.querySelector('.e79-box'); const stage = ov.querySelector('.e79-stage');
  return { present: true, name: name ? name.textContent : null,
    line: line ? line.textContent : null,
    boxTop: box ? +box.getBoundingClientRect().top.toFixed(1) : null,
    stageH: stage ? +stage.getBoundingClientRect().height.toFixed(1) : null,
    charHVar: stage ? (getComputedStyle(stage).getPropertyValue('--dlg108-char-h') || '').trim() : null };
}'''

JS_MEASURE_IMG = '''(sel) => {
  const out = [];
  document.querySelectorAll(sel).forEach(im => {
    const r = im.getBoundingClientRect();
    out.push({ id: im.dataset.dlgId || im._sid106 || null,
      src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
      top: +(r.top.toFixed(1)), bottom: +(r.bottom.toFixed(1)), height: +(r.height.toFixed(1)),
      left: +(r.left.toFixed(1)), right: +(r.right.toFixed(1)), width: +(r.width.toFixed(1)),
      inlineH: im.style.height || null,
      nat: (im.naturalWidth||0) + 'x' + (im.naturalHeight||0) });
  });
  return out;
}'''

def next_step(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")

def finish_encounter(pg):
    for _ in range(30):
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; } return null; }""")
        if not clicked:
            break
        pg.wait_for_timeout(400)
        if not pg.evaluate(JS_ENC)["present"]:
            break

def open_encounter(pg, star_name, loc_btn, key, star_id=None, loc_id=None):
    """玩法入場（108v 配方）：逐日改 dayIndex＋S.starDay=null 重骰出沒盤，
       直到該星 overlay 出現；錯星就先行完佢再試下一日。回傳量度 dict。"""
    days = [None] + list(range(424, 441))
    for day in days:
        if day is not None:
            pg.evaluate("(d) => { S.dayIndex = d; S.starDay = null; }", day)
            print(f"  {key} try dayIndex={day}")
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)
        cr = click_first(pg, [loc_btn], 1800)
        pg.wait_for_timeout(900)
        info = pg.evaluate(JS_ENC)
        print(f"  {key} day={day} click={cr} present={info.get('present')} pres_at_loc={pg.evaluate('(l) => ((S.starDay||{}).presence||{})[l] || null', loc_id)}")
        if not info["present"]:
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)
            continue
        # 唔用名牌認星：首句可以係旁白（名牌空白），用人物圖 id 認
        chars0 = pg.evaluate(JS_MEASURE_IMG, ".e79-char")
        ids0 = [c["id"] for c in chars0]
        if star_id not in ids0:
            print(f"  {key} wrong stars {ids0} — 行完再試")
            finish_encounter(pg)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)
            continue
        chars = pg.evaluate(JS_MEASURE_IMG, ".e79-char")
        gap = round(chars[1]["left"] - chars[0]["right"], 1) if len(chars) == 2 else None
        topdiff = round(chars[1]["top"] - chars[0]["top"], 1) if len(chars) == 2 else None
        rec = {"found": True, "day": pg.evaluate("() => S.dayIndex"),
               "name": info.get("name"), "line": (info.get("line") or "")[:60],
               "charHVar": info.get("charHVar"), "boxTop": info.get("boxTop"),
               "stageH": info.get("stageH"), "gap": gap, "topDiff": topdiff, "chars": chars}
        print(f" ENC {key}: day={rec['day']} charHVar={info.get('charHVar')} gap={gap} topDiff={topdiff} chars={[(c['id'], c['src'], c['height'], c['top']) for c in chars]} line={(info.get('line') or '')[:40]}")
        pg.screenshot(path=f"{SHOTS}/{TAG}_enc_{key}.png")
        pg.wait_for_timeout(300)
        finish_encounter(pg)
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)
        return rec
    print(f" ENC {key}: NOT FOUND in {len(days)} tries")
    return {"found": False}


srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: ERRORS.append("pageerror: " + str(e)))
        pg.on("console", lambda m: ERRORS.append("console.error: " + m.text) if m.type == "error" else None)

        print("new game:", new_game(pg))

        # ---- C1 主線：搵第一個雙人步（預期 阿偉×何生）----
        print("enter agency:", click_first(pg, ["何生事務所"], 1800))
        pg.wait_for_timeout(800)
        st = pg.evaluate(JS_STORY)
        if not st["active"]:
            pg.evaluate("() => { const b = document.getElementById('map-progress-btn'); if (b) b.click(); }")
            pg.wait_for_timeout(1200)
            print("C1 play button:", pg.evaluate('''() => { const b = document.querySelector('[data-prog77-play="C1"]');
              if (b) { b.click(); return true; } return false; }'''))
            pg.wait_for_timeout(1500)
        for step in range(15):
            info = pg.evaluate(JS_STORY)
            chars = pg.evaluate(JS_MEASURE_IMG, ".dlg106-char") if info["active"] else []
            if info["active"] and len(chars) == 2:
                gap = round(chars[1]["left"] - chars[0]["right"], 1)
                LOG["c1"] = {"step": step, "speaker": info.get("speaker"), "line": (info.get("line") or "")[:60],
                             "charHVar": info.get("charHVar"), "plateTop": info.get("plateTop"),
                             "gap": gap, "chars": chars}
                print(f" C1[{step}] spk={info.get('speaker')} charHVar={info.get('charHVar')} gap={gap} chars={[(c['id'], c['height'], c['top']) for c in chars]}")
                pg.screenshot(path=f"{SHOTS}/{TAG}_c1_awixho.png")
                break
            if info.get("choices"):
                print(" C1 choices hit before 2-char step, stop"); break
            if not next_step(pg):
                print(" C1 no next button, stop"); break
            pg.wait_for_timeout(500)
        else:
            print(" C1: no 2-char step in 15")

        print("back_to_map:", back_to_map(pg))

        # ---- 三段巧遇首句（玩法入場，同一新檔首遇段 pre/post 對照）----
        for star_name, loc_btn, key, star_id, loc_id in [("顧明輝", "海港廣播", "gu", "gu_mingfai", "tvb_harbour"),
                                                      ("彭少祺", "中環廣告", "pang", "pang_siuki", "ad_central"),
                                                      ("鍾楚凝", "天星音樂", "chung", "chung_choning", "rec_star")]:
            LOG["enc"][key] = open_encounter(pg, star_name, loc_btn, key, star_id, loc_id)
        b.close()
finally:
    stop(srv)

with open(os.path.join(HERE, f"drive_{TAG}.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("ERRORS:", ERRORS if ERRORS else "none")
print("LOG:", json.dumps(LOG, ensure_ascii=False)[:1500])
