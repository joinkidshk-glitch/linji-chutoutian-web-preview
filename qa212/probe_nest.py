# -*- coding: utf-8 -*-
"""v20a212 C1 根因探針：列出所有 .awd63-cards 容器（懷疑巢狀）＋每張卡嘅計算 visibility／opacity，
分別喺 catTitle 同 nominee beat 採樣。"""
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/linji-work212/qa212")
import drive212 as t

d = t.d
from playwright.sync_api import sync_playwright

JS_NEST = """() => {
  const out = { containers: [], cards: [], caption: '' };
  document.querySelectorAll('.awd63-cards').forEach((el, i) => {
    const s = getComputedStyle(el);
    const b = el.getBoundingClientRect();
    let parent = el.parentElement;
    out.containers.push({ i, cls: el.className, vis: s.visibility, disp: s.display,
      parentCls: parent ? parent.className : null,
      rect: { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) },
      nCards: el.querySelectorAll(':scope > .awd63-card').length,
      nDescCards: el.querySelectorAll('.awd63-card').length });
  });
  document.querySelectorAll('.awd63-card').forEach((el, i) => {
    const s = getComputedStyle(el);
    out.cards.push({ i, cls: el.className, vis: s.visibility, opacity: s.opacity });
  });
  const cap = document.querySelector('.awd62-caption');
  out.caption = cap ? cap.textContent : '';
  return out;
}"""


def main():
    srv = d.serve()
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=d.EXE, args=["--no-sandbox"])
            ctx = b.new_context(viewport={"width": 430, "height": 932})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            assert d.new_game(pg)
            d.seed(pg, {"year": 1991, "fame": 45, "credit": 50, "roles": {}, "payOverride": None}, [])
            fp, _ = t.force_pack_try(pg, "award_golddisc_music", "gallery", None)
            assert "error" not in fp
            assert d.present(pg).get("visible")
            d.click_vis(pg, "出席")
            pg.wait_for_timeout(400)
            for _ in range(200):
                st = pg.evaluate(t.JS_STAGE_FULL)
                if "—— 最佳新人獎 ——" in (st.get("caption") or ""):
                    break
                pg.wait_for_timeout(50)
            pg.wait_for_timeout(400)
            print("CATTITLE:", json.dumps(pg.evaluate(JS_NEST), ensure_ascii=False, indent=1), flush=True)
            for _ in range(300):
                st = pg.evaluate(t.JS_STAGE_FULL)
                if "入圍名單 1/3" in (st.get("caption") or ""):
                    break
                pg.wait_for_timeout(50)
            pg.wait_for_timeout(600)
            print("NOMINEE:", json.dumps(pg.evaluate(JS_NEST), ensure_ascii=False, indent=1), flush=True)
            print("pageerrors:", errs, flush=True)
            ctx.close()
            b.close()
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
