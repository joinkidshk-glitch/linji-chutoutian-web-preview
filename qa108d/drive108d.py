# -*- coding: utf-8 -*-
"""v20a108d 實駕量度（改後 post；改前 pre 共用舊版 drive108d_pre 數據）：
   1. 主線 C1：逐句量 .dlg106-char（高 60%?、腳底、淨空、computed filter、canvas 可見鞋底 y）、
      .sp-plate 高（固定 118？）、牌頂遮腿（elementFromPoint）、#modal-btns「下一句」掣 rect。
   2. 巧遇鍾楚凝＠金鐘創意：逐句量 .e79-char 同上＋ .e79-box 高（固定？）、盒頂遮腿、
      .e79-btn rect；鎖定用戶截圖兩句旁白做對照。
   用法：/home/hatch/pwenv49/bin/python qa108d/drive108d.py [base_url] [pre|post]
   （先喺工作副本 python3 -m http.server 8931）"""
import sys, os, json
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8931/"
TAG = sys.argv[2] if len(sys.argv) > 2 else "post"
URL = BASE + "index.html?softPreview=1&softRev=s107"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
LOG = {"tag": TAG, "c1": [], "enc_chung": [], "errors": []}

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

JS_MEASURE_IMG = '''(sel) => {
  const out = [];
  document.querySelectorAll(sel).forEach(im => {
    const r = im.getBoundingClientRect();
    const cs = getComputedStyle(im);
    let soleY = null, soleFrac = null;
    try {
      const cv = document.createElement('canvas');
      cv.width = im.naturalWidth; cv.height = im.naturalHeight;
      const cx = cv.getContext('2d'); cx.drawImage(im, 0, 0);
      const d = cx.getImageData(0, 0, cv.width, cv.height).data;
      const W = cv.width, H = cv.height;
      for (let y = H - 1; y >= 0; y--) {
        let hit = false;
        for (let x = Math.floor(W*0.15); x < Math.floor(W*0.85); x += 2) {
          if (d[(y*W + x)*4 + 3] >= 128) { hit = true; break; }
        }
        if (hit) { soleFrac = y / H; soleY = r.top + soleFrac * r.height; break; }
      }
    } catch(e) { soleY = 'canvas-err:' + e; }
    out.push({ id: im.dataset.dlgId || im._sid106 || null,
      src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
      filterInline: im.style.filter, filterComputed: cs.filter,
      top: +(r.top.toFixed(1)), bottom: +(r.bottom.toFixed(1)), height: +(r.height.toFixed(1)),
      left: +(r.left.toFixed(1)), right: +(r.right.toFixed(1)),
      soleY: (typeof soleY === 'number' ? +soleY.toFixed(1) : soleY), soleFrac,
      nat: (im.naturalWidth||0) + 'x' + (im.naturalHeight||0) });
  });
  return out;
}'''

JS_STORY = '''() => {
  const sp = document.querySelector('.story-play');
  if (!sp) return { active: false };
  const speaker = document.querySelector('.story-play .sp-speaker');
  const plate = document.querySelector('.story-play .sp-plate');
  const line = document.querySelector('.story-play .sp-line');
  const bg = document.querySelector('.story-play .sp-bg-layer');
  const stage = document.querySelector('.story-play .sp-stage');
  const btns = [...document.querySelectorAll('#modal-btns button')].filter(x => x.offsetParent !== null && !x.disabled)
    .map(b => { const r = b.getBoundingClientRect(); return { text: b.textContent.trim().slice(0,12), w: +r.width.toFixed(1), h: +r.height.toFixed(1), x: +r.left.toFixed(1), cls: b.className, bg: getComputedStyle(b).backgroundColor, deco: getComputedStyle(b).textDecorationLine }; });
  const choices = [...document.querySelectorAll('.sp-choice')].map(b => b.textContent.trim().slice(0,30));
  let cover = null;
  try {
    const pr = plate ? plate.getBoundingClientRect() : null;
    const chars = [...document.querySelectorAll('.dlg106-char')];
    if (pr && chars.length) {
      const c = chars[0].getBoundingClientRect();
      const x = c.left + c.width / 2, y = pr.top + 60;
      const el = document.elementFromPoint(x, y);
      cover = { probeX: +x.toFixed(1), probeY: +y.toFixed(1), plateTop: +pr.top.toFixed(1),
        hit: el ? (el.className && el.className.baseVal !== undefined ? 'svg' : String(el.className).slice(0,40)) + '|' + el.tagName : null,
        hitInPlate: el ? !!el.closest('.sp-plate') : null, hitIsImg: el ? el.tagName === 'IMG' : null };
    }
  } catch(e) { cover = 'err:' + e; }
  return { active: true, speaker: speaker ? speaker.textContent : null,
    plateH: plate ? +plate.getBoundingClientRect().height.toFixed(1) : null,
    plateTop: plate ? +plate.getBoundingClientRect().top.toFixed(1) : null,
    plateCls: plate ? plate.className : null,
    bgCls: bg ? bg.className : null,
    charHVar: stage ? (getComputedStyle(stage).getPropertyValue('--dlg108-char-h') || '').trim() : null,
    line: line ? line.textContent : null, choices, btns, cover };
}'''

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return { present: false };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  const box = ov.querySelector('.e79-box');
  const stage = ov.querySelector('.e79-stage');
  const btns = [...ov.querySelectorAll('.e79-btn')].filter(x => x.offsetParent !== null)
    .map(b => { const r = b.getBoundingClientRect(); return { text: b.textContent.trim().slice(0,14), w: +r.width.toFixed(1), h: +r.height.toFixed(1), x: +r.left.toFixed(1), cls: b.className, bg: getComputedStyle(b).backgroundColor, deco: getComputedStyle(b).textDecorationLine }; });
  let cover = null;
  try {
    const br = box ? box.getBoundingClientRect() : null;
    const chars = [...ov.querySelectorAll('.e79-char')];
    if (br && chars.length) {
      const c = chars[chars.length-1].getBoundingClientRect();
      const x = c.left + c.width / 2, y = br.top + 60;
      const el = document.elementFromPoint(x, y);
      cover = { probeX: +x.toFixed(1), probeY: +y.toFixed(1), boxTop: +br.top.toFixed(1),
        hit: el ? (el.className && el.className.baseVal !== undefined ? 'svg' : String(el.className).slice(0,40)) + '|' + el.tagName : null,
        hitInBox: el ? !!el.closest('.e79-box') : null, hitIsImg: el ? el.tagName === 'IMG' : null };
    }
  } catch(e) { cover = 'err:' + e; }
  return { present: true, name: name ? name.textContent : null,
    nameH: name ? +name.getBoundingClientRect().height.toFixed(1) : null,
    line: line ? line.textContent : null,
    boxH: box ? +box.getBoundingClientRect().height.toFixed(1) : null,
    boxTop: box ? +box.getBoundingClientRect().top.toFixed(1) : null,
    stageH: stage ? +stage.getBoundingClientRect().height.toFixed(1) : null,
    charHVar: stage ? (getComputedStyle(stage).getPropertyValue('--dlg108-char-h') || '').trim() : null,
    lineH: line ? +line.getBoundingClientRect().height.toFixed(1) : null,
    hasChoice: !!ov.querySelector('.e79-choice'), btns, cover };
}'''

def shot(pg, name):
    pg.screenshot(path=os.path.join(SHOTS, "%s_%s.png" % (TAG, name)))

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
    print("DLG108 live:", pg.evaluate("() => !!(window.DLG108 && window.DLG108.fitPct)"))

    # ---------- 1. 主線 C1 ----------
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
    c1_nar_done = False; c1_cover_done = False
    for step in range(40):
        info = pg.evaluate(JS_STORY)
        chars = pg.evaluate(JS_MEASURE_IMG, ".dlg106-char") if info["active"] else []
        rec = dict(info); rec["chars"] = chars
        LOG["c1"].append(rec)
        gap = None
        if len(chars) == 2:
            gap = round(chars[1]["left"] - chars[0]["right"], 1)
        print(f" C1[{step}] spk={info.get('speaker')} plateH={info.get('plateH')} plateTop={info.get('plateTop')} bg={info.get('bgCls')} charHVar={info.get('charHVar')} gap={gap} cover={info.get('cover')} btns={info.get('btns')} chars={[(c['id'], c['src'], c['filterComputed'], c['height'], c['bottom']) for c in chars]} line={(info.get('line') or '')[:40]}")
        if info["active"] and info.get("speaker") is None and len(chars) == 2 and not c1_nar_done:
            shot(pg, "c1_narration"); c1_nar_done = True; print("  >> c1 narration shot")
        if info["active"] and info.get("speaker") and len(chars) == 2 and not c1_cover_done:
            shot(pg, "main_cover"); c1_cover_done = True; print("  >> main cover shot")
        if info.get("choices"):
            shot(pg, "c1_choices")
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
    pg.reload(); pg.wait_for_timeout(2200)
    click_first(pg, ["繼續"], 1800)
    pg.wait_for_timeout(800)

    # ---------- 2. 巧遇鍾楚凝＠金鐘創意 ----------
    print("open loc 金鐘創意:", click_first(pg, ["金鐘創意"], 1800))
    targets = {"金鐘一間廣告公司搞發佈酒會": "enc_nar_3line", "佢講完就想行": "enc_nar_2line"}
    got_targets = set(); enc_cover_done = False; enc_nar_shot = False
    for i in range(32):
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            if i == 0:
                t = click_first(pg, ["傾談", "打聽", "傾偈"], 1500)
                print("  sheet talk btn:", t)
                info = pg.evaluate(JS_ENC)
            if not info["present"]:
                break
        chars = pg.evaluate(JS_MEASURE_IMG, ".e79-char")
        rec = dict(info); rec["chars"] = chars
        LOG["enc_chung"].append(rec)
        gap = round(chars[1]["left"] - chars[0]["right"], 1) if len(chars) == 2 else None
        print(f" ENC[{i}] name={info.get('name')} boxH={info.get('boxH')} boxTop={info.get('boxTop')} stageH={info.get('stageH')} lineH={info.get('lineH')} charHVar={info.get('charHVar')} gap={gap} cover={info.get('cover')} btns={info.get('btns')} chars={[(c['id'], c['src'], c['filterComputed'], c['height'], c['bottom']) for c in chars]} line={(info.get('line') or '')[:44]}")
        for key, tag in targets.items():
            if key in (info.get("line") or "") and tag not in got_targets:
                shot(pg, tag); got_targets.add(tag); print("  >> shot", tag)
        if info.get("name") == "鍾楚凝" and not enc_cover_done:
            shot(pg, "enc_cover"); enc_cover_done = True; print("  >> enc cover shot")
        if not info.get("name") and not enc_nar_shot and i > 0:
            shot(pg, "enc_narration"); enc_nar_shot = True; print("  >> enc narration shot")
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
        pg.wait_for_timeout(450)
    print("targets got:", sorted(got_targets))
    print("pageerrors:", LOG["errors"][:6])
    with open(os.path.join(HERE, "drive108d_%s.json" % TAG), "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=1)
    b.close()
print("DONE", TAG)
