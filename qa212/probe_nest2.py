# -*- coding: utf-8 -*-
"""v20a212 C1 根因探針 2：喺音樂夜第 2 格提名 beat（cat 1）、第 3 格格標題（cat 2）、
第 3 格懸念 beat（cat 2）分別 dump .awd63-cards 容器數目＋visibility。"""
import json
import sys

sys.path.insert(0, "/home/hatch/workspace/linji-work212/qa212")
import drive212 as t
from probe_nest import JS_NEST

d = t.d
from playwright.sync_api import sync_playwright


def wait_cap(pg, substr, timeout=120):
    for _ in range(timeout * 20):
        st = pg.evaluate(t.JS_STAGE_FULL)
        if substr in (st.get("caption") or ""):
            return True
        pg.wait_for_timeout(50)
    return False


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
            assert wait_cap(pg, "入圍名單 1/2 · 最佳女歌手"), "no cat1 nom"
            pg.wait_for_timeout(400)
            print("CAT1 NOMINEE:", json.dumps(pg.evaluate(JS_NEST), ensure_ascii=False), flush=True)
            assert wait_cap(pg, "—— 最佳男歌手 ——"), "no cat2 title"
            pg.wait_for_timeout(400)
            print("CAT2 CATTITLE:", json.dumps(pg.evaluate(JS_NEST), ensure_ascii=False), flush=True)
            assert wait_cap(pg, "得獎者是"), "no cat2 suspense"
            pg.wait_for_timeout(400)
            print("CAT2 SUSPENSE:", json.dumps(pg.evaluate(JS_NEST), ensure_ascii=False), flush=True)
            print("pageerrors:", errs, flush=True)
            ctx.close()
            b.close()
    finally:
        d.stop(srv)


if __name__ == "__main__":
    main()
