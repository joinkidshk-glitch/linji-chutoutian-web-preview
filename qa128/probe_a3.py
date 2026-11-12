# -*- coding: utf-8 -*-
"""v128 A3 probe: measure current state of N5 / D-1 / D-7 / N4 (C1),
N16 (encounter third party), WF4 stage geometry.
Probe-only: drives the game via UI + direct function calls (enc79PlayEncounter /
wf4PlayEvent) to reach states that are random in normal play. No game code changed."""
import sys, os, json
sys.path.insert(0, "/home/hatch/workspace/linji-ui-style-unify")
from drive_lib import EXE
from playwright.sync_api import sync_playwright

PORT = 8952
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
SHOTS = "/home/hatch/workspace/linji-work128/qa128/shots"
os.makedirs(SHOTS, exist_ok=True)

def click_first(pg, texts, wait=900):
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

def story_state(pg):
    return pg.evaluate("""() => {
      const root = document.getElementById('story-play-root');
      if (!root) return {active:false};
      const head = root.querySelector('.sp-head');
      const stage = root.querySelector('.sp-stage');
      const chars = [...root.querySelectorAll('.dlg106-char,.sp-bust')].map(im=>{
        const b = im.getBoundingClientRect();
        return {id: im.dataset.dlgId || im.alt || '', cls: im.className,
          x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
          filter: im.style.filter || getComputedStyle(im).filter}; });
      const topEls = [...document.querySelectorAll('#mask *')].filter(el=>{
        const b = el.getBoundingClientRect();
        return b.top < 30 && b.bottom > 0 && b.width > 0 && b.height > 0 && b.top < 0;
      }).map(el=>{ const b=el.getBoundingClientRect();
        return {tag: el.tagName, cls: String(el.className).slice(0,60), txt: (el.textContent||'').trim().slice(0,20),
          x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; });
      const line = (root.querySelector('.sp-line')||{}).textContent || '';
      const speaker = (root.querySelector('.sp-speaker')||{}).textContent || '';
      const kind = stage ? stage.dataset.spKind : '';
      return {active:true, kind, head: !!head, headText: head ? head.textContent.trim().slice(0,60) : '',
        line: line.slice(0,50), speaker, chars, clippedTop: topEls.slice(0,8)};
    }""")

def next_step(pg):
    """Advance one story beat via #modal-btns first button (下一句)."""
    ok = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
      if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
      if (!bs.length) return false; bs[0].click(); return true; }""")
    pg.wait_for_timeout(900)
    return ok

def pin_click(pg, loc_id):
    box = pg.evaluate("""(id) => { const b=document.querySelector('.pin[data-loc="'+id+'"]');
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x+r.width/2, y:r.y+r.height/2}; }""", loc_id)
    if not box:
        return False
    pg.mouse.click(box["x"], box["y"])
    pg.wait_for_timeout(1600)
    return True

def main():
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                             user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15")
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
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
        for t in ["跳過教學", "開始寫手帳"]:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(1200)
            except Exception: pass
        try:
            pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
        except Exception: pass
        click_first(pg, ["確定出發"], 1500)
        for _ in range(5):
            hit = False
            for t in ["確定", "確認", "好", "知道了"]:
                try:
                    loc = pg.locator("button:has-text('" + t + "')")
                    if loc.count() and loc.first.is_visible(): loc.first.click(timeout=900); pg.wait_for_timeout(900); hit = True; break
                except Exception: pass
            if not hit: break
        pg.wait_for_timeout(1200)

        out = {}
        # --- C1: agency -> 播劇情, step through beats 1..6 + choices ---
        print("== C1 ==", flush=True)
        pin_click(pg, "agency_ho")
        print("播劇情:", click_first(pg, ["播劇情"], 1800), flush=True)
        pg.wait_for_timeout(800)
        steps = []
        for i in range(8):
            st = story_state(pg)
            steps.append(st)
            print(f"step{i}: kind={st.get('kind')} head={st.get('head')} speaker={st.get('speaker')!r} line={st.get('line')!r} chars={[(c['id'],c['w'],c['h'],c['filter']) for c in st.get('chars',[])]}", flush=True)
            if i == 0:
                pg.screenshot(path=os.path.join(SHOTS, "a3_c1_step0_390x844.png"))
            if i == 2:
                pg.screenshot(path=os.path.join(SHOTS, "a3_c1_step2_390x844.png"))
            if st.get("kind") == "choices" or not st.get("active"):
                break
            # choice screen reached? .sp-choice present
            has_choice = pg.evaluate("() => !!document.querySelector('.sp-choice')")
            if has_choice:
                pg.screenshot(path=os.path.join(SHOTS, "a3_c1_choices_390x844.png"))
                print("CHOICE screen:", pg.evaluate("""() => {
                  const btns=[...document.querySelectorAll('#modal-btns button')].map(b=>b.textContent.trim());
                  const cards=[...document.querySelectorAll('.sp-choice')].map(b=>b.textContent.trim().slice(0,30));
                  return {modalBtns: btns, cards}; }"""), flush=True)
                break
            next_step(pg)
        out["c1_steps"] = steps
        # pick first choice to finish C1
        pg.evaluate("() => { const c=document.querySelector('.sp-choice'); if(c) c.click(); }")
        pg.wait_for_timeout(1200)
        click_first(pg, ["好", "知道了", "完成"], 900)
        pg.wait_for_timeout(900)
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
        pg.wait_for_timeout(700)

        # --- N16: force 廖炳星 first encounter, play to the 副導 line ---
        print("== N16 encounter ==", flush=True)
        pg.evaluate("""() => { try{ enc79PlayEncounter('liu_bingxing', 'cafe_cha', false); }catch(e){ return String(e); } }""")
        pg.wait_for_timeout(1200)
        enc_steps = []
        for i in range(8):
            st = pg.evaluate("""() => {
              const ov = document.querySelector('#enc79-overlay');
              if(!ov) return {active:false};
              const chars=[...ov.querySelectorAll('.e79-char')].map(im=>{ const b=im.getBoundingClientRect();
                return {sid: im._sid106||'', x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), filter: im.style.filter}; });
              return {active:true, name: (ov.querySelector('.e79-name')||{}).textContent||'',
                line: (ov.querySelector('.e79-line')||{}).textContent||'', chars}; }""")
            enc_steps.append(st)
            print(f"enc{i}: name={st.get('name')!r} line={st.get('line','')[:40]!r} chars={[(c['sid'],c['w'],c['h'],c['filter']) for c in st.get('chars',[])]}", flush=True)
            if "副導" in st.get("line",""):
                pg.screenshot(path=os.path.join(SHOTS, "a3_enc_fudao_390x844.png"))
                break
            pg.evaluate("""() => { const b=[...document.querySelectorAll('#enc79-overlay .e79-btn')].find(x=>x.textContent.trim()==='下一句'); if(b) b.click(); }""")
            pg.wait_for_timeout(900)
        out["enc_steps"] = enc_steps
        pg.evaluate("""() => { const b=[...document.querySelectorAll('#enc79-overlay .e79-btn')].find(x=>/下一句|返去/.test(x.textContent)); if(b) b.click(); }""")
        pg.wait_for_timeout(800)
        # finish encounter via skip if still up
        pg.evaluate("""() => { const s=document.querySelector('#enc79-overlay .e79-skip'); if(s) s.click(); }""")
        pg.wait_for_timeout(900)

        # --- WF4: fire wf4_ev_cha02 directly, measure stage geometry ---
        print("== WF4 ==", flush=True)
        fired = pg.evaluate("""() => {
          try{ const ev = DAILY_EVENTS_WF4.find(e=>e && e.id==='wf4_ev_cha02');
            if(!ev) return 'no ev'; wf4PlayEvent(ev, ()=>{}); return 'fired'; }
          catch(e){ return 'err:'+String(e); } }""")
        print("wf4 fired:", fired, flush=True)
        pg.wait_for_timeout(1200)
        wf = pg.evaluate("""() => {
          const st = document.querySelector('#modal-inner .sp-stage');
          if(!st) return {active:false, html: (document.getElementById('modal-inner')||{}).textContent.slice(0,80)};
          const b = st.getBoundingClientRect();
          const chars=[...st.querySelectorAll('.dlg106-char')].map(im=>{ const r=im.getBoundingClientRect();
            return {sid: im.dataset.dlgId||'', x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; });
          const modal = document.getElementById('modal-inner').getBoundingClientRect();
          return {active:true, stage:{x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height)},
            modal:{w:Math.round(modal.width),h:Math.round(modal.height)}, chars}; }""")
        print("WF4:", json.dumps(wf, ensure_ascii=False), flush=True)
        out["wf4"] = wf
        pg.screenshot(path=os.path.join(SHOTS, "a3_wf4_390x844.png"))
        out["pageerrors"] = errs
        print("PAGEERRORS:", errs)
        with open("/home/hatch/workspace/linji-work128/qa128/a3_probe.json", "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        br.close()

if __name__ == "__main__":
    main()
