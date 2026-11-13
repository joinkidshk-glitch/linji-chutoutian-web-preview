#!/usr/bin/env python3
"""v185 幾何量度：700 下 gift pick modal-inner 係咪真係碌唔郁 + 卡片高度構成。"""
import json, subprocess, sys, time, os
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v183")
import probe183 as P
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work185"
PORT = 8978
P.ROOT = ROOT
P.PORT = PORT
SHOTS = "/home/hatch/workspace/linji-work185/qa185"

def geom(pg):
    return pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
        return { top: Math.round(b.top), bottom: Math.round(b.bottom), left: Math.round(b.left), right: Math.round(b.right),
                 h: Math.round(b.height), w: Math.round(b.width) }; };
      const mi = q('#modal-inner'), list = q('#gift-pick-list'), modal = q('#modal'), btns = q('#modal-btns');
      const card = list ? list.querySelector('.act') : null;
      const out = { vh: innerHeight, modal: r(modal), inner: r(mi), list: r(list), btns: r(btns) };
      if (mi) out.innerScroll = { scrollH: mi.scrollHeight, clientH: mi.clientHeight, scrollTop: mi.scrollTop, overflowY: getComputedStyle(mi).overflowY };
      if (list) out.listScroll = { scrollH: list.scrollHeight, clientH: list.clientHeight, overflowY: getComputedStyle(list).overflowY };
      if (card) { const cs = getComputedStyle(card);
        out.card = { h: Math.round(card.getBoundingClientRect().height),
          n: (() => { const n = card.querySelector('.n'); if (!n) return null;
            const b = n.getBoundingClientRect(); const cs2 = getComputedStyle(n);
            return { h: Math.round(b.height), lines: Math.round(b.height / parseFloat(cs2.lineHeight)), text: (n.innerText||'').slice(0,30), fontSize: cs2.fontSize, lineHeight: cs2.lineHeight }; })(),
          hline: (() => { const h = card.querySelector('.h'); if (!h) return null;
            const b = h.getBoundingClientRect(); const cs2 = getComputedStyle(h);
            return { h: Math.round(b.height), lines: Math.round(b.height / parseFloat(cs2.lineHeight)) }; })(),
          padTop: cs.paddingTop, padBottom: cs.paddingBottom }; }
      // 每行 elementFromPoint（中心點 + 「選」掣中心點）
      out.rowHit = [...document.querySelectorAll('#gift-pick-list > *')].map(el => {
        const b = el.getBoundingClientRect();
        const cx = Math.round((b.left + b.right) / 2), cy = Math.round((b.top + b.bottom) / 2);
        const hit = document.elementFromPoint(cx, cy);
        const cost = el.querySelector('.cost');
        let costHit = null;
        if (cost) { const cb = cost.getBoundingClientRect();
          const ccx = Math.round((cb.left + cb.right) / 2), ccy = Math.round((cb.top + cb.bottom) / 2);
          const ch = document.elementFromPoint(ccx, ccy);
          costHit = { hitIsCost: ch ? (ch === cost || cost.contains(ch)) : false,
                      hitTag: ch ? (ch.tagName + '.' + (ch.className || '').toString().slice(0, 30)) : null }; }
        return { name: (el.innerText || '').split('\\n')[0].slice(0, 22),
          top: Math.round(b.top), bottom: Math.round(b.bottom),
          hitIsRow: hit ? el.contains(hit) : false,
          hitTag: hit ? (hit.tagName + '.' + (hit.className || '').toString().slice(0, 30)) : null,
          costHit };
      });
      // C1：每張卡 .n 係咪兩行（孤兒 ×N）
      out.nameLines = [...document.querySelectorAll('#gift-pick-list .n')].map(n => {
        const b = n.getBoundingClientRect(); const cs = getComputedStyle(n);
        const lh = parseFloat(cs.lineHeight) || 16;
        return { text: (n.innerText || '').replace(/\\n/g, ' / ').slice(0, 40), h: Math.round(b.height),
                 lines: Math.round(b.height / lh) };
      });
      return out;
    }""")

def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    out = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=P.EXE)
            ctx = b.new_context(viewport={"width": 430, "height": 700})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            P.new_game_to_map(pg)
            mi, day, attempts = P.enter_woman(pg, "hiu", "tvb_longmen")
            out["encounter"] = bool(mi and mi.get("visible"))
            P.click_vis_btn(pg, "送禮", "#modal")
            pg.wait_for_timeout(1000)
            pick = P.wait_modal(pg, 4)
            out["pick_shown"] = bool(pick.get("visible"))
            out["before"] = geom(pg)
            # 試碌 modal-inner 到底
            sc = pg.evaluate("""() => { const mi = document.getElementById('modal-inner');
              if (!mi) return null; const before = mi.scrollTop; mi.scrollTop = mi.scrollHeight;
              return { before, after: mi.scrollTop, max: mi.scrollHeight - mi.clientHeight }; }""")
            out["innerScrollTest"] = sc
            pg.wait_for_timeout(300)
            out["afterScroll"] = geom(pg)
            pg.screenshot(path=os.path.join(SHOTS, "geom700.png"))
            out["pageerrors"] = errs
            ctx.close()
            b.close()
    finally:
        srv.terminate()
    with open(os.path.join(SHOTS, "geom700.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
