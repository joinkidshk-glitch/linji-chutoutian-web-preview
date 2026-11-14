# -*- coding: utf-8 -*-
"""v211 B7 探針：單場 music_nom_700，讀 reveal canvas RGB（beam 暖色偏移校準）。"""
import json, os, sys, time
sys.path.insert(0, "/home/hatch/workspace/linji-work211/qa211")
import importlib.util
spec = importlib.util.spec_from_file_location("d211", "/home/hatch/workspace/linji-work211/qa211/drive211.py")
# 唔執行 main：直接 import 會跑 main（__main__ guard 在內，安全）
d211 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d211)
import drive188 as d
from playwright.sync_api import sync_playwright

JS_RGB = """(o) => {
  const cv = document.querySelector('canvas.awd62-canvas');
  if (!cv) return { error: 'no canvas' };
  const ctx = cv.getContext('2d');
  const H = cv.height / 1.5, F = 314 / 432 * H;
  const rgbAt = (lx, ly) => {
    const bx = Math.round(lx * 1.5), by = Math.round(ly * 1.5);
    try {
      const dd = ctx.getImageData(bx - 4, by - 4, 9, 9).data;
      let r = 0, g = 0, b = 0, n = 0;
      for (let i = 0; i < dd.length; i += 4) { r += dd[i]; g += dd[i + 1]; b += dd[i + 2]; n++; }
      return { r: Math.round(r / n), g: Math.round(g / n), b: Math.round(b / n) };
    } catch (e) { return null; }
  };
  const ys = [20, 80, 140, 200, Math.round(F - 40), Math.round(F - 10)];
  const rows = ys.map(y => {
    const off = (y < F - 160) ? 10 : 38;
    const w = rgbAt(o.wcx + off, y), l = rgbAt(o.lcx + off, y);
    const lum = c => c ? Math.round((0.299 * c.r + 0.587 * c.g + 0.114 * c.b) * 10) / 10 : null;
    const warm = c => c ? (c.r - c.b) : null;
    return { y, off, win: w, lose: l, lumDiff: (w && l) ? Math.round((lum(w) - lum(l)) * 10) / 10 : null,
             warmDiff: (w && l) ? warm(w) - warm(l) : null };
  });
  return { H: Math.round(H), F: Math.round(F), rows };
}"""

srv = d.serve()
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 430, "height": 700})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        assert d.new_game(pg)
        d.seed(pg, {"year": 1990, "fame": 25, "credit": 0, "roles": {"rec": 2}, "payOverride": None}, [])
        fp, seed = d211.force_pack_try(pg, "award_golddisc_music", "nominee")
        print("pack", fp.get("bestOutcome"), "seed", seed, flush=True)
        d.present(pg)
        d.click_vis(pg, "出席")
        cap = ""
        t0 = time.time()
        while time.time() - t0 < 12:
            cap = d.stage_state(pg).get("caption") or ""
            if "得獎" in cap and cap.strip() != "得獎者是……":
                break
            pg.wait_for_timeout(250)
        pg.wait_for_timeout(700)
        w, l, info = d211.reveal_slots(fp, fp.get("bestOutcome"), cap)
        print("slots", info, "w_settled", w, "l", l, flush=True)
        print(json.dumps(pg.evaluate(JS_RGB, {"wcx": w, "lcx": l}), ensure_ascii=False, indent=1), flush=True)
        print("pageerrors", errs, flush=True)
        ctx.close()
        b.close()
finally:
    d.stop(srv)
