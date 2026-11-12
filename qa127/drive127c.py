# -*- coding: utf-8 -*-
"""v20a127 T1b：傾談 modal 實機示範（drive127c）。
目的：證明傾談句喺真 UI 出現嗰陣，畫面係 PORTRAITS 靜態 bust（唔係 dlg106 表情）。
做法：新遊戲 → S.npcs.colleague=100（開 daily＋insider 池）→ S.locNpc 派曉晴去
紅棉影業 → 入場 → 撳「同林曉晴傾談」→ 記錄 modal 對白＋頭像 src＋截圖；
每傾完 reset S.flags.softTalkUsed=0 再傾，最多 12 次；撞到 5 句目標句任何一句
即停並另存截圖。首談有 hiu 專屬開場分支（撳掣行到結果 modal 先記錄）。
若派位被 refreshNpc 蓋過（sheet 唔係曉晴），碌日（S.dayIndex+1）再試，最多 4 日；
再唔得就 fallback 去事務所同何生傾（駐場 NPC，modal 機制一樣）。
用法：pwenv49 python qa127/drive127c.py [root]
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "qa127")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8954
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"drive": "127c", "talks": [], "errors": []}
TARGET_LINES = {
    "我前幾日喺清水灣嗰組做嘢，氣氛幾好，副導又唔會亂鬧人，新人去嗰邊撞下，學到嘢又唔使捱得咁辛苦。",
    "你嚟試鏡，唔好背到滾瓜爛熟就算，留返少少即場反應畀我睇，我想知你聽到新指示，識唔識得即刻變。",
    "陸柏言嗰場戲，佢明明背熟晒對白，但一埋位就停咗兩停，導演冇鬧，仲叫大家抖下先，可能佢真係好攰。",
    "呢份工我睇過，唔啱我做，漏畀你算啦：嗰組缺個肯捱夜嘅後生，你肯頂，入去就有位，唔好講我益你。",
    "嗰個組而家四圍搵人，唔係冇人，係之前嗰個走咗佬，你有本事補到位，導演點都會記得你呢份人情。",
}

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
    if st != 200 or sha != exp:
        raise RuntimeError("served index mismatch")
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

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return { present: false };
  return { present: true };
}'''

def step_overlay_away(pg, max_steps=30):
    for _ in range(max_steps):
        if not pg.evaluate(JS_ENC)["present"]:
            return True
        clicked = pg.evaluate("""() => {
          const chs = [...document.querySelectorAll('.e79-choice')].filter(b => b.offsetParent !== null);
          if (chs.length) { chs[0].click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""")
        if not clicked:
            return False
        pg.wait_for_timeout(420)
    return not pg.evaluate(JS_ENC)["present"]

JS_MODAL = '''() => {
  const dlg = document.querySelector('.dlg');
  if (!dlg) return null;
  const img = dlg.querySelector('.dlg-portrait');
  const name = dlg.querySelector('.dlg-name');
  const bub = dlg.querySelector('.dlg-bubble');
  const aff = dlg.querySelector('.dlg-aff');
  const btns = [...document.querySelectorAll('#modal-btns button')].filter(b => b.offsetParent !== null)
    .map(b => b.textContent.trim());
  return { name: name ? name.textContent : null,
           bubble: bub ? bub.textContent.slice(0, 120) : null,
           img: img ? img.getAttribute('src') : null,
           hasAff: !!aff, btns };
}'''

SAFE_MODAL_BTNS = ["繼續", "睇落去", "知道了", "明白", "關閉", "好", "確定"]

def dismiss_modal_any(pg, max_clicks=8):
    """WF4 風物卡係多頁 modal（繼續 → 睇落去 → …），逐頁撳到佢閂為止。
    只撳安全嘅敘事掣；見到其他掣（真抉擇）即停，唔擅自揀。
    回傳：有冇真係拆到一個 modal（冇 modal 喺度回 False，等上層去撳地點）。"""
    dismissed = False
    for _ in range(max_clicks):
        btns = pg.evaluate("""() => {
          const md = document.querySelector('#modal');
          if (!md || md.offsetParent === null) return [];
          return [...document.querySelectorAll('#modal-btns button')]
            .filter(b => b.offsetParent !== null).map(b => b.textContent.trim());
        }""")
        if not btns:
            return dismissed
        nxt = next((t for t in btns if any(t.startswith(s) for s in SAFE_MODAL_BTNS)), None)
        if nxt is None:
            # 例外：WF4 風物卡「老戲骨教企位」尾頁係二揀一學嘢選項（純 flavor，
            # 同 story drive 撳 choice[0] 同級）——認住標題先撳第一個，其他 modal 照停。
            is_flavor = pg.evaluate("""() => {
              const md = document.querySelector('#modal');
              return md ? md.innerText.includes('老戲骨教企位') : false; }""")
            if not is_flavor:
                print(f"  [T1b] modal 出現非敘事掣 {btns}，停手唔撳", flush=True)
                return dismissed
            nxt = btns[0]
            print(f"  [T1b] WF4 風物卡尾頁，撳第一個選項「{nxt}」", flush=True)
        if not click_first(pg, [nxt[:8]], 900):
            return dismissed
        dismissed = True
        pg.wait_for_timeout(500)
    return dismissed

def enter_loc_and_talk(pg, loc_label, talk_label, max_rounds=10):
    """入場 → 遇攔截（WF4 風物卡／巧遇 overlay）就拆咗佢再入過 → 直到見到傾談掣。
    關鍵：WF4 攔截後玩家返返地圖，sheet 未開；要再撳多次地點先開到 sheet。
    （攔截後重入免費，唔再扣額度。）"""
    for _ in range(max_rounds):
        got = click_first(pg, [talk_label], 900)
        if got:
            return got
        if dismiss_modal_any(pg):
            pg.wait_for_timeout(500)
            continue
        if pg.evaluate(JS_ENC)["present"]:
            step_overlay_away(pg)
            pg.wait_for_timeout(500)
            continue
        if click_first(pg, [loc_label], 1500):
            pg.wait_for_timeout(900)
            continue
        return None
    return click_first(pg, [talk_label], 900)

def read_modal(pg):
    return pg.evaluate(JS_MODAL)

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        new_game(pg)
        # 派曉晴去紅棉影業；碌日搵佢（refreshNpc 每日重派）
        npc = None
        for day in [0, 1, 2, 3]:
            pg.evaluate("(d) => { S.dayIndex = d; S.npcs = S.npcs || {}; S.npcs.colleague = 100; "
                        "S.locNpc = S.locNpc || {}; S.locNpc['film_cotton'] = 'colleague'; return true; }", day)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
            pg.wait_for_timeout(600)
            got = enter_loc_and_talk(pg, "紅棉影業", "同林曉晴傾談")
            if got:
                npc = "colleague"
                print(f"  [T1b] day {day}：sheet 見到曉晴，已撳傾談", flush=True)
                break
            print(f"  [T1b] day {day}：sheet 唔係曉晴（talk 掣搵唔到），碌下一日", flush=True)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
        if not npc:
            # fallback：事務所駐場何生（modal 機制一樣，證靜態 bust）
            print("  [T1b] 4 日都搵唔到曉晴，fallback 事務所何生", flush=True)
            pg.evaluate("() => { S.dayIndex = 0; S.npcs = S.npcs || {}; S.npcs.agent = 100; return true; }")
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
            pg.wait_for_timeout(600)
            got = enter_loc_and_talk(pg, "何生事務所", "同何生傾談")
            npc = "agent" if got else None
            print(f"  [T1b] fallback 何生傾談掣：{got}", flush=True)
        if not npc:
            print("  [T1b] FAIL：傾談掣都搵唔到", flush=True)
            LOG["errors"].append("no talk button found")
        else:
            target_hit = False
            for n in range(12):
                # 行到結果 modal（首談有開場分支，要撳多兩層）
                rec = None
                for _round in range(5):
                    m = read_modal(pg)
                    if not m:
                        break
                    if m["hasAff"] and m["bubble"]:
                        rec = m
                        break
                    # 開場分支：撳第一個主掣
                    if m["btns"]:
                        click_first(pg, [m["btns"][0][:8]], 1200)
                        pg.wait_for_timeout(600)
                        continue
                    break
                if not rec:
                    print(f"  [T1b] talk {n+1}：讀唔到結果 modal", flush=True)
                    break
                is_target = rec["bubble"] in TARGET_LINES
                print(f"  [T1b] talk {n+1} {rec['name']}｜img={rec['img']}｜target={is_target}｜{rec['bubble'][:60]}", flush=True)
                LOG["talks"].append({"n": n + 1, "npc": npc, "name": rec["name"],
                                      "img": rec["img"], "target": is_target,
                                      "bubble": rec["bubble"]})
                pg.screenshot(path=f"{SHOTS}/branch_T1b_talk{n+1}_{npc}.png")
                if is_target:
                    target_hit = True
                    print("  [T1b] ★ 撞到目標句（chow 分類句）——以曉晴靜態 bust 出現", flush=True)
                    break
                # 閂 modal → 返地點 sheet（travelFree；風物卡可能再出）→ reset cap → 再傾
                click_first(pg, ["關閉"], 1000)
                pg.wait_for_timeout(800)
                pg.evaluate("() => { S.flags = S.flags || {}; S.flags.softTalkUsed = 0; return true; }")
                got = enter_loc_and_talk(pg,
                    "紅棉影業" if npc == "colleague" else "何生事務所",
                    "同林曉晴傾談" if npc == "colleague" else "同何生傾談")
                if not got:
                    print(f"  [T1b] talk {n+2}：返 sheet 後傾談掣唔見咗，停", flush=True)
                    break
            LOG["target_hit"] = target_hit
        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

print("talks:", len(LOG["talks"]), "target_hit:", LOG.get("target_hit"), flush=True)
for t in LOG["talks"]:
    print(f"  talk{t['n']} {t['name']} img={t['img']} target={t['target']} :: {t['bubble'][:50]}", flush=True)
print("pageerrors:", LOG["errors"][:6], flush=True)
with open(os.path.join(HERE, "drive_log127c_branch.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
