# -*- coding: utf-8 -*-
"""v20a212 C1 探針：catTitle 期間卡片計算樣式＋CSSOM 規則＋即時截圖量度。
目的：分清「preview212 規則冇生效」（game bug）定「截圖 stale」（探針問題）。"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/linji-work212/qa212")
import drive212 as t

d = t.d
from playwright.sync_api import sync_playwright

JS_PROBE = """() => {
  const out = {};
  // 1. CSSOM：preview212 規則在唔在
  out.rules = [];
  for (const sh of document.styleSheets) {
    let rules;
    try { rules = sh.cssRules; } catch(e) { continue; }
    for (const r of rules) {
      if (r.selectorText && r.selectorText.includes('preview212')) {
        out.rules.push({ sel: r.selectorText, css: r.style.cssText });
      }
    }
  }
  // 2. 容器
  const cards = document.querySelector('.awd63-cards');
  if (!cards) { out.noCards = true; return out; }
  const cs = getComputedStyle(cards);
  out.container = { cls: cards.className, vis: cs.visibility, disp: cs.display,
                    rect: (() => { const b = cards.getBoundingClientRect();
                      return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) }; })() };
  // 3. 每張卡
  out.cards = [];
  for (const el of cards.querySelectorAll('.awd63-card')) {
    const s = getComputedStyle(el);
    const b = el.getBoundingClientRect();
    out.cards.push({ cls: el.className, opacity: s.opacity, vis: s.visibility,
                     disp: s.display, transform: s.transform,
                     rect: { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) },
                     text: (el.textContent || '').replace(/\\s+/g, ' ').slice(0, 30) });
  }
  const cap = document.querySelector('.awd62-caption');
  out.caption = cap ? cap.textContent : '';
  return out;
}"""


def zone_stats(png, rect):
    from PIL import Image
    im = Image.open(os.path.join(d.SHOTS, png)).convert("RGB")
    cd = rect
    box = (cd["x"], cd["y"], cd["x"] + cd["w"], cd["y"] + cd["h"])
    px = list(im.crop(box).getdata())
    lum = [0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in px]
    return {"mean": round(sum(lum) / len(lum), 1), "max": round(max(lum)),
            "gt50": round(100 * sum(1 for v in lum if v > 50) / len(lum), 2),
            "gt120": round(100 * sum(1 for v in lum if v > 120) / len(lum), 2)}


def main():
    srv = d.serve()
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            ctx = b.new_context(viewport={"width": 430, "height": 932})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            assert d.new_game(pg), "new_game fail"
            d.seed(pg, {"year": 1991, "fame": 45, "credit": 50, "roles": {}, "payOverride": None}, [])
            fp, seed_used = t.force_pack_try(pg, "award_golddisc_music", "gallery", None)
            print("pack:", json.dumps({k: fp.get(k) for k in ("ceremonyId", "year", "bestOutcome", "tier")}, ensure_ascii=False), "seed", seed_used, flush=True)
            assert "error" not in fp
            inv = d.present(pg)
            assert inv.get("visible"), "no invite"
            d.click_vis(pg, "出席")
            pg.wait_for_timeout(400)
            # 等第一個 catTitle
            found = False
            for _ in range(200):
                st = pg.evaluate(t.JS_STAGE_FULL)
                if "—— 最佳新人獎 ——" in (st.get("caption") or ""):
                    found = True
                    break
                pg.wait_for_timeout(50)
            assert found, "no catTitle seen"
            pg.wait_for_timeout(400)  # 過埋 300ms opacity transition
            probe = pg.evaluate(JS_PROBE)
            print("CATTITLE PROBE:", json.dumps(probe, ensure_ascii=False, indent=1), flush=True)
            d.shot(pg, "probe_c1_cattitle.png")
            rects = pg.evaluate(t.JS_RECTS)
            print("CATTITLE ZONE:", zone_stats("probe_c1_cattitle.png", rects["cards"]), flush=True)
            # 控制組：等入下一個 nominee beat，卡應該 .show opacity 1
            for _ in range(200):
                st = pg.evaluate(t.JS_STAGE_FULL)
                if "入圍名單" in (st.get("caption") or ""):
                    break
                pg.wait_for_timeout(50)
            pg.wait_for_timeout(600)
            probe2 = pg.evaluate(JS_PROBE)
            print("NOMINEE PROBE:", json.dumps(probe2, ensure_ascii=False, indent=1), flush=True)
            d.shot(pg, "probe_c1_nominee.png")
            rects2 = pg.evaluate(t.JS_RECTS)
            print("NOMINEE ZONE:", zone_stats("probe_c1_nominee.png", rects2["cards"]), flush=True)
            print("pageerrors:", errs, flush=True)
            ctx.close()
            b.close()
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
