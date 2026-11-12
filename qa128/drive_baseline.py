# -*- coding: utf-8 -*-
"""v128 baseline: measure map one-screen layout on pristine v126 (work copy, no edits yet).
Mirror: work copy ~/workspace/linji-work128 served on 8952. Viewport 390x844 (+420x900).
Seeds via new_game() into slot 3 only (disposable profile)."""
import sys, os, json
sys.path.insert(0, "/home/hatch/workspace/linji-ui-style-unify")
from drive_lib import new_game, shot, EXE
from playwright.sync_api import sync_playwright

PORT = 8952
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
SHOTS = "/home/hatch/workspace/linji-work128/qa128/shots"
PROFILE = "/home/hatch/workspace/linji-work128/qa128/profile"
os.makedirs(SHOTS, exist_ok=True)

MEASURE_JS = """() => {
  const r = s => { const el = document.querySelector(s); if(!el) return null;
    const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            bottom: Math.round(b.bottom), display: cs.display, position: cs.position, overflow: cs.overflow}; };
  const lbl = txt => { const els=[...document.querySelectorAll('.mn68,.md97')].filter(e=>e.textContent.trim()===txt);
    if(!els.length) return null; const b=els[0].getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; };
  return {
    vh: window.innerHeight, docScrollH: document.documentElement.scrollHeight,
    bodyScrollH: document.body.scrollHeight, scrollY: window.scrollY,
    app: r('#app'), vmap: r('#v-map'), bar: r('#map-bar'), wrap: r('.map-wrap'),
    polaroid: r('.map-polaroid'), stage: r('.map-stage'), hint: r('#map-hint'),
    progBtn: r('#map-progress-btn'), chipStory: r('#chip-story'),
    showAll: r('#map-show-all-locs'),
    stressTrack: (()=>{ const el=document.querySelector('.hud-stress-track'); if(!el) return null;
      const b=el.getBoundingClientRect(); const v=document.querySelector('.hud-stress-val');
      const vs=v?getComputedStyle(v):null; return {h: Math.round(b.height), w: Math.round(b.width),
        valFont: vs?vs.fontSize:null, valWeight: vs?vs.fontWeight:null}; })(),
    labels: { starTV: lbl('星河電視台'), hotel: lbl('金禧大酒店'),
      pokfulam: lbl('薄扶林'), wanchai: lbl('灣仔'), cwb: lbl('銅鑼灣') },
    errs: (window.__errs||[]).slice(-5),
    story: (()=>{ const el=document.querySelector('.map-hint-story'); if(!el) return null;
      const b=el.getBoundingClientRect();
      return {tag: el.tagName, h: Math.round(b.height), scrollH: el.scrollHeight, display: getComputedStyle(el).display,
        txt: el.textContent.slice(0,60)}; })()
  };
}"""

def main():
    vw = int(sys.argv[1]) if len(sys.argv) > 1 else 390
    vh = int(sys.argv[2]) if len(sys.argv) > 2 else 844
    tag = sys.argv[3] if len(sys.argv) > 3 else "base"
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = br.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=2,
                             user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
        # new_game uses drive_lib URL (8951) — override by going direct: replicate minimal flow
        pg.goto(URL); pg.wait_for_timeout(3200)
        pg.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='新遊戲'); if(b) b.click(); }""")
        pg.wait_for_timeout(1200)
        pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]'); if (b && b.offsetParent !== null) b.click(); }""")
        pg.wait_for_timeout(1200)
        for t in ["覆蓋", "確定", "確認"]:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); break
            except Exception: pass
        for t in ["跳過教學", "開始寫手帳", "確定出發"]:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(1200)
            except Exception: pass
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception: pass
        for _ in range(5):
            hit = False
            for t in ["確定", "確認", "好", "知道了"]:
                try:
                    loc = pg.locator("button:has-text('" + t + "')")
                    if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); hit = True; break
                except Exception: pass
            if not hit: break
        pg.wait_for_timeout(1500)
        m = pg.evaluate(MEASURE_JS)
        m["pageerrors"] = errs
        print(json.dumps(m, ensure_ascii=False, indent=1))
        pg.screenshot(path=os.path.join(SHOTS, f"map_{tag}_{vw}x{vh}.png"))
        print("SHOT map_%s_%dx%d.png" % (tag, vw, vh))
        br.close()

if __name__ == "__main__":
    main()
