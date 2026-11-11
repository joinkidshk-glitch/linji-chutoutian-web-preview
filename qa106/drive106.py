# -*- coding: utf-8 -*-
"""v20a106 實駕（本地鏡像＝線上版逐檔下載＋sha 核對，見 NOTES）：
   1. 主線 C1 成段播：講者句（全身雙人＋表情）／旁白句（齊暗冇名牌）／電話聲句（0.8＋電話牌）
   2. 巧遇兩段（鍾楚凝＠金鐘創意、顧明輝＠海港廣播，day0 種子）：逐句紀錄＋截圖，
      捕捉同角表情切換＋明暗交替
   用法：pwenv49 python qa106/drive106.py [base_url]"""
import sys, os, json
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8931/"
URL = BASE + "index.html?softPreview=1&softRev=s107"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
os.makedirs(SHOTS, exist_ok=True)
LOG = {"c1": [], "enc": {}, "errors": []}

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
    filter: im.style.filter, pos: im.className }));
  const sp = document.querySelector('.story-play');
  const speaker = document.querySelector('.story-play .sp-speaker');
  const plate = document.querySelector('.story-play .sp-plate');
  const line = document.querySelector('.story-play .sp-line');
  const choices = [...document.querySelectorAll('.sp-choice')].map(b => b.textContent.trim().slice(0,30));
  return { active: !!sp, chars, speaker: speaker ? speaker.textContent : null,
           plateCls: plate ? plate.className : null,
           line: line ? line.textContent.slice(0,70) : null, choices };
}'''

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return { present: false };
  const one = (sel) => { const im = ov.querySelector(sel); if (!im) return null;
    return { src: (im.getAttribute('src')||'').split('/').pop().split('?')[0], filter: im.style.filter }; };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  return { present: true, L: one('.e79-char-l'), R: one('.e79-char-r'),
           name: name ? name.textContent : null, nameCls: name ? name.className : null,
           line: line ? line.textContent.slice(0,70) : null,
           hasChoice: !!ov.querySelector('.e79-choice') };
}'''

def finish_encounter_if_any(pg, tag):
    """開地點前若有巧遇 overlay，先播完（qa105 慣例）。回傳有冇出現。"""
    seen = False
    for i in range(40):
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            break
        seen = True
        clicked = pg.evaluate('''() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          return null; }''')
        if not clicked:
            break
        pg.wait_for_timeout(350)
    if seen:
        print(f"  （先播完 {tag} 巧遇）")
    return seen

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg.on("pageerror", lambda e: LOG["errors"].append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
    except Exception:
        pass
    click_first(pg, ["確定出發"], 1500)
    for i in range(4):
        if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    print("S ok:", pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"))

    # ---------- 1. 主線 C1（先入何生事務所——進度頁明示「去何生事務所就會觸發」） ----------
    print("enter agency:", click_first(pg, ["何生事務所"], 1800))
    pg.wait_for_timeout(800)
    _st = pg.evaluate(JS_STORY)
    if not _st["active"]:
        # 未自動觸發就經進度頁「播呢幕」掣（身處地點先出掣）
        pg.evaluate("() => { const b = document.getElementById('map-progress-btn'); if (b) b.click(); }")
        pg.wait_for_timeout(1200)
        played = pg.evaluate('''() => { const b = document.querySelector('[data-prog77-play="C1"]');
          if (b) { b.click(); return true; } return false; }''')
        print("C1 play button (progress):", played)
        pg.wait_for_timeout(1500)
    got = {"speaker": False, "narration": False, "phone": False}
    speaker_base_only = True
    for step in range(40):
        info = pg.evaluate(JS_STORY)
        LOG["c1"].append(info)
        print(f" C1[{step}] spk={info['speaker']} line={info['line']} chars={[(c['id'], c['src'], c['filter']) for c in info['chars']]} plate={info['plateCls']} choices={info['choices']}")
        if info["active"]:
            pg.screenshot(path=f"{SHOTS}/c1_step{step:02d}.png")
            bright = [c["filter"] for c in info["chars"]]
            if not got["phone"] and info["plateCls"] and "dlg106-plate-phone" in info["plateCls"]:
                pg.screenshot(path=f"{SHOTS}/c1_phone.png"); got["phone"] = True; print("  >> phone shot")
            elif not got["narration"] and not info["speaker"] and len(info["chars"]) == 2 and all("0.6" in f for f in bright):
                pg.screenshot(path=f"{SHOTS}/c1_narration.png"); got["narration"] = True; print("  >> narration shot")
            elif info["speaker"] and len(info["chars"]) == 2 and any("brightness(1)" in f for f in bright):
                active_src = [c["src"] for c in info["chars"] if "brightness(1)" in c["filter"]]
                is_expr = active_src and "_base." not in active_src[0]
                if not got["speaker"] or (speaker_base_only and is_expr):
                    pg.screenshot(path=f"{SHOTS}/c1_speaker.png"); got["speaker"] = True
                    speaker_base_only = not is_expr
                    print(f"  >> speaker shot (expr={is_expr})")
        if info["choices"]:
            pg.screenshot(path=f"{SHOTS}/c1_choices.png")
            click_first(pg, [info["choices"][0][:6]], 1500)
            pg.wait_for_timeout(1200)
            for i in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續"], 900):
                    break
            break
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            print("  （冇下一句掣，停）"); break
        pg.wait_for_timeout(500)
    print("C1 got:", got)
    # 回地圖：reload + 繼續（順便驗存檔重載入到）
    pg.reload(); pg.wait_for_timeout(2200)
    click_first(pg, ["繼續"], 1800)
    pg.wait_for_timeout(800)
    print("after reload S ok:", pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"))

    # ---------- 2. 巧遇兩段 ----------
    for locname, tag in [("金鐘創意", "chung"), ("海港廣播", "gu")]:
        print("open loc:", locname, click_first(pg, [locname], 1800))
        steps = []
        for i in range(32):
            info = pg.evaluate(JS_ENC)
            if not info["present"]:
                # 可能開咗地點板未觸發：試撳板上傾談／打聽類掣
                if i == 0:
                    t = click_first(pg, ["傾談", "打聽", "傾偈"], 1500)
                    print("  sheet talk btn:", t)
                    info = pg.evaluate(JS_ENC)
                if not info["present"]:
                    break
            steps.append(info)
            pg.screenshot(path=f"{SHOTS}/enc_{tag}_step{i:02d}.png")
            print(f" ENC {tag}[{i}] name={info['name']} line={info['line']} L={info['L']} R={info['R']} choice={info['hasChoice']}")
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
            pg.wait_for_timeout(420)
        LOG["enc"][tag] = steps
        print(f" ENC {tag}: {len(steps)} steps")
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 800)

    print("pageerrors:", LOG["errors"][:6])
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "drive_log.json"), "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=1)
    b.close()
print("DONE")
