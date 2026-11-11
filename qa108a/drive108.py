# -*- coding: utf-8 -*-
"""v20a108 D-8（二期）實駕：WF4 隨機事件接入 DLG106 舞台。
   本地鏡像＝工作副本 linji-work108a 直接 http.server（分支未合併，唔經線上）。
   真路徑：新遊戲→地圖後，經 evaluate 設 S.wf4.pending＝指定事件（只代勞隨機
   抽籤；呈現鏈 wf4PresentPending→wf4Fire→wf4PlayEvent 全部行真 code），
   再經真 UI「☰→提早休息→確定休息→返回地圖」入地圖觸發。
   （主 script 包咗 IIFE，wf4PlayEvent／DAILY_EVENTS_WF4 唔係全域，直接 evaluate
   叫唔到——第一版實駕就係咁失敗，已改行呢條真路徑。）
   駕三單：st03（think 表情切換）＋day02（sad）＋set01（無名舊路徑後備）。
   用法：先起 server（nohup python3 -m http.server 8932，根目錄 linji-work108a），
   再 pwenv49 python qa108a/drive108.py [base_url]"""
import sys, os, json
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8932/"
URL = BASE + "index.html?softPreview=1&softRev=s107"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
LOG = {"events": {}, "errors": [], "S": {}}

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

def click_modal_first(pg):
    return pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")

JS_WF4 = '''() => {
  const chars = [...document.querySelectorAll('.dlg106-char')].map(im => {
    const r = im.getBoundingClientRect();
    return { id: im.dataset.dlgId, src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
      filter: im.style.filter, w: Math.round(r.width), h: Math.round(r.height),
      ok: im.complete && im.naturalWidth > 0 }; });
  const stage = document.querySelector('.story-play .sp-stage');
  const sr = stage ? stage.getBoundingClientRect() : null;
  const speaker = document.querySelector('.story-play .sp-speaker');
  const plate = document.querySelector('.story-play .sp-plate');
  const line = document.querySelector('.story-play .sp-line');
  const btns = [...document.querySelectorAll('#modal-btns button')].filter(b => b.offsetParent !== null).map(b => b.textContent.trim());
  const h3 = document.querySelector('#modal-inner h3');
  return { hasStage: !!stage, stageRect: sr ? {w: Math.round(sr.width), h: Math.round(sr.height)} : null,
    chars, speaker: speaker ? speaker.textContent : null,
    plateCls: plate ? plate.className : null, line: line ? line.textContent.slice(0,60) : null,
    hasScene105: !!document.querySelector('.wf4-scene105'), btns,
    title: h3 ? h3.textContent : null };
}'''

def drive_event(pg, ev_id, title, tag):
    """設 pending → 休息過日 → 返回地圖 → 事件經真路徑彈出；逐步截圖＋紀錄。"""
    day = pg.evaluate(
        "() => { const S = window.S; if (!S) return -1;"
        " S.wf4 = S.wf4 || {}; S.wf4.pending = '%s'; S.wf4.pendingDay = S.dayIndex; S.wf4.lastDay = -99;"
        " return S.dayIndex; }" % ev_id)
    print(f" {tag}: pending 已設（day {day}）")
    click_first(pg, ["☰"], 900)
    pg.evaluate("() => { const b = document.querySelector('[data-m=\"rest-early\"]'); if (b) b.click(); }")
    pg.wait_for_timeout(1000)
    click_first(pg, ["確定休息"], 1500)
    steps, seen_title, seen_stage, done = [], False, False, False
    for i in range(24):
        pg.wait_for_timeout(700)
        info = pg.evaluate(JS_WF4)
        steps.append(info)
        is_ev = info["title"] == title
        if is_ev:
            seen_title = True
        if info["hasStage"]:
            seen_stage = True
        print(f"  [{tag} step{i}] stage={info['hasStage']} rect={info['stageRect']} title={info['title']} "
              f"spk={info['speaker']} line={info['line']} chars={[(c['id'], c['src'], c['filter'], str(c['w'])+'x'+str(c['h']), 'ok' if c['ok'] else 'BROKEN') for c in info['chars']]} "
              f"scene105={info['hasScene105']} btns={info['btns']}")
        if seen_title:
            pg.screenshot(path=f"{SHOTS}/{tag}_{i:02d}.png")
        if seen_title and not info["btns"] and info["title"] is None:
            done = True; break
        if not click_modal_first(pg):
            # modal 外（可能係報紙／其他畫面）：試撳返地圖／關閉類掣
            back = pg.evaluate("""() => { const b = [...document.querySelectorAll('button')].filter(x => x.offsetParent !== null)
              .find(x => ['返回地圖','關閉','繼續','好','知道了'].includes(x.textContent.trim()));
              if (!b) return false; b.click(); return true; }""")
            if not back:
                print("  （冇掣可撳，停）"); break
        pg.wait_for_timeout(450)
    LOG["events"][tag] = {"id": ev_id, "title": title, "seen_title": seen_title,
                          "seen_stage": seen_stage, "done": done, "steps": steps}
    print(f" {tag}: seen_title={seen_title} seen_stage={seen_stage} done={done} steps={len(steps)}")
    return seen_title and done

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
    LOG["S"]["before"] = pg.evaluate("() => ({stress: S.stress, stamina: S.stamina, money: S.money, day: S.dayIndex})")
    print("S before:", LOG["S"]["before"])

    # 1. st03 大哥大好惹眼：旁白 base 0.6 → 阿偉 think 全光（表情切換）
    r1 = drive_event(pg, "wf4_ev_st03", "大哥大好惹眼", "st03")
    print("  S after st03:", pg.evaluate("() => ({stress: S.stress, stamina: S.stamina, day: S.dayIndex})"))
    # 2. day02 傳呼台嘅一課：旁白 → 阿偉 sad 全光（第二個具名事件＋唔同表情）
    r2 = drive_event(pg, "wf4_ev_day02", "傳呼台嘅一課", "day02")
    print("  S after day02:", pg.evaluate("() => ({stress: S.stress, stamina: S.stamina, day: S.dayIndex})"))
    # 3. set01 開鏡拜神企前排：無名舊路徑（場務／旁白）——場景底＋純文字，唔出企立
    r3 = drive_event(pg, "wf4_ev_set01", "開鏡拜神企前排", "set01")
    LOG["S"]["after"] = pg.evaluate("() => ({stress: S.stress, stamina: S.stamina, money: S.money, day: S.dayIndex})")
    print("S after all:", LOG["S"]["after"])
    LOG["events_summary"] = {"st03": r1, "day02": r2, "set01": r3}
    print("pageerrors:", LOG["errors"][:6])
    with open(os.path.join(HERE, "drive_log.json"), "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=1)
    b.close()
print("DONE", LOG["events_summary"])
