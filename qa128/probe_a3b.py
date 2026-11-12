# -*- coding: utf-8 -*-
"""v128 A3b probe: N16 (force 廖炳星 presence at cafe, play first encounter to
the 副導 line) + WF4 (enter cafe 3x on day 0, 3rd entry fires WF4 loc event;
measure stage geometry). Probe-only state seeding via window.S."""
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

def play_story(pg, max_steps=40):
    for _ in range(max_steps):
        st = pg.evaluate("""() => {
          const sp = document.querySelector('.story-play');
          if (!sp) return {active:false};
          return {active:true, choices:[...sp.querySelectorAll('.sp-choice')].map(b=>b.textContent.trim().slice(0,20))}; }""")
        if not st["active"]:
            return True
        if st["choices"]:
            pg.evaluate("""() => { const c=document.querySelector('.sp-choice'); if(c) c.click(); }""")
            pg.wait_for_timeout(900)
            continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if clicked:
            pg.wait_for_timeout(800)
            continue
        hit = click_first(pg, ["下一句", "繼續", "下一步", "好", "知道了"], 700)
        if not hit:
            return False
    return pg.evaluate("() => !document.querySelector('.story-play')")

def pin_click(pg, loc_id):
    box = pg.evaluate("""(id) => { const b=document.querySelector('.pin[data-loc="'+id+'"]');
      if(!b) return null; const r=b.getBoundingClientRect();
      return {x:r.x+r.width/2, y:r.y+r.height/2}; }""", loc_id)
    if not box:
        return False
    pg.mouse.click(box["x"], box["y"])
    pg.wait_for_timeout(1600)
    return True

def ensure_quota(pg):
    pg.evaluate("""() => { const S = window.S; if(!S) return;
      S.travel114 = { day: S.dayIndex|0, used: 0 }; }""")

def seed_encounter(pg, star_id, loc_id):
    return pg.evaluate("""([sid, loc]) => {
      const S = window.S; if(!S) return 'no S';
      const day = S.dayIndex|0;
      S.starDay = { day, presence: {}, triggered: 0, doneToday: {} };
      S.starDay.presence[loc] = [sid];
      if(!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = {};
      S.wf4.lastDay = day;  // suppress WF4 so the encounter is what fires
      return 'seeded ' + sid + ' @ ' + loc + ' day ' + day;
    }""", [star_id, loc_id])

def seed_no_encounter(pg):
    return pg.evaluate("""() => {
      const S = window.S; if(!S) return 'no S';
      const day = S.dayIndex|0;
      const stars = ["luk_baakyin","liu_bingxing","ngai_wingnaam","yip_manji","mak_zhendong",
        "lok_gasing","pang_siuki","chung_choning","gu_mingfai","so_jiyan","chai_zanhoi","ching_tinlok"];
      if(S.starDay && S.starDay.day === day){
        S.starDay.doneToday = S.starDay.doneToday || {};
        stars.forEach(id => S.starDay.doneToday[id] = 1);
      }
      // do NOT touch S.wf4 here: the loc counter must accumulate across entries
      return 'suppressed';
    }""")

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
        # C1 first so pins work
        print("== C1 ==", flush=True)
        pin_click(pg, "agency_ho")
        print("播劇情:", click_first(pg, ["播劇情"], 1800), flush=True)
        pg.wait_for_timeout(800)
        print("C1 cleared:", play_story(pg, 30), flush=True)
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
        pg.wait_for_timeout(700)

        out = {}
        # --- N16 ---
        print("== N16 ==", flush=True)
        print(seed_encounter(pg, "liu_bingxing", "cafe_cha"), flush=True)
        ensure_quota(pg)
        pin_click(pg, "cafe_cha")
        pg.wait_for_timeout(1000)
        enc_steps = []
        for i in range(10):
            st = pg.evaluate("""() => {
              const ov = document.querySelector('#enc79-overlay');
              if(!ov) return {active:false};
              const chars=[...ov.querySelectorAll('.e79-char')].map(im=>{ const b=im.getBoundingClientRect();
                return {sid: im._sid106||'', x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), filter: im.style.filter}; });
              return {active:true, name: (ov.querySelector('.e79-name')||{}).textContent||'',
                line: (ov.querySelector('.e79-line')||{}).textContent||'', chars}; }""")
            enc_steps.append(st)
            print(f"enc{i}: name={st.get('name')!r} line={st.get('line','')[:44]!r} chars={[(c['sid'],c['w'],c['h'],c['filter']) for c in st.get('chars',[])]}", flush=True)
            if "副導" in st.get("line",""):
                pg.screenshot(path=os.path.join(SHOTS, "a3_enc_fudao_390x844.png"))
                break
            if not st.get("active"):
                print("  overlay gone?", flush=True)
                break
            pg.evaluate("""() => { const b=[...document.querySelectorAll('#enc79-overlay .e79-btn')].find(x=>x.textContent.trim()==='下一句'); if(b) b.click(); }""")
            pg.wait_for_timeout(900)
        out["enc_steps"] = enc_steps
        # close encounter: click through to the end (choices first, then 下一句/返去), then skip
        for _ in range(16):
            still = pg.evaluate("() => !!document.querySelector('#enc79-overlay')")
            if not still:
                break
            pg.evaluate("""() => {
              const ov = document.querySelector('#enc79-overlay'); if(!ov) return;
              const ch = ov.querySelector('.e79-choice');
              if(ch){ ch.click(); return; }
              const b=[...ov.querySelectorAll('.e79-btn')].find(x=>/下一句|返去/.test(x.textContent));
              if(b) b.click(); }""")
            pg.wait_for_timeout(700)
        pg.evaluate("""() => { const s=document.querySelector('#enc79-overlay .e79-skip'); if(s) s.click(); }""")
        pg.wait_for_timeout(900)
        print("encounter closed:", pg.evaluate("() => !document.querySelector('#enc79-overlay')"),
              "view:", pg.evaluate("() => { const v=document.querySelector('.view.on'); return v ? v.id : 'none'; }"), flush=True)
        click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
        pg.wait_for_timeout(700)

        print("== WF4 ==", flush=True)
        print("day/wf4:", pg.evaluate("() => ({day: window.S.dayIndex, wf4: window.S.wf4})"), flush=True)
        # reset the WF4 gate ONCE (the encounter seed set lastDay=day, which
        # blocks wf4BaseOk via gapDays) + the loc counter, so entries 1..3 = tries 1..3
        pg.evaluate("""() => { const S = window.S; if(!S.wf4 || typeof S.wf4 !== 'object') S.wf4 = {};
          S.wf4.lastDay = -99; S.wf4.locDay = -99; S.wf4.locTries = 0; S.wf4.pending = null;
          S.wf4.seen = S.wf4.seen || {}; S.wf4.seen.__n = 3; /* pick hash -> boss01 (has 阿偉) */
          return 'reset'; }""")
        wf = None
        for entry in range(1, 4):
            seed_no_encounter(pg)
            ensure_quota(pg)
            pin_click(pg, "cafe_cha")
            pg.wait_for_timeout(1200)
            wf = pg.evaluate("""() => {
              const st = document.querySelector('#modal-inner .sp-stage');
              const sheet = document.getElementById('loc-sheet');
              const sheetOn = sheet && (sheet.classList.contains('on') || sheet.classList.contains('sheet-live'));
              if(!st) return {stage:false, sheetOn: !!sheetOn,
                modalText: (document.getElementById('modal-inner')||{}).textContent.slice(0,60)};
              const b = st.getBoundingClientRect();
              const chars=[...st.querySelectorAll('.dlg106-char')].map(im=>{ const r=im.getBoundingClientRect();
                return {sid: im.dataset.dlgId||'', x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; });
              const modal = document.getElementById('modal-inner').getBoundingClientRect();
              const title = (document.querySelector('#modal-inner h3')||{}).textContent||'';
              return {stage:true, title, stage:{x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height)},
                modal:{w:Math.round(modal.width),h:Math.round(modal.height)}, chars}; }""")
            print(f"entry{entry}:", json.dumps(wf, ensure_ascii=False), flush=True)
            print(f"  wf4state:", pg.evaluate("() => ({day: window.S.dayIndex, lastDay: window.S.wf4.lastDay, locDay: window.S.wf4.locDay, locTries: window.S.wf4.locTries, pending: window.S.wf4.pending, plan: window.S.todayPlan || window.S.plan || null})"), flush=True)
            if wf.get("stage"):
                pg.screenshot(path=os.path.join(SHOTS, "a3_wf4_390x844.png"))
                break
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
            pg.wait_for_timeout(700)
        out["wf4"] = wf
        out["pageerrors"] = errs
        print("PAGEERRORS:", errs)
        with open("/home/hatch/workspace/linji-work128/qa128/a3b_probe.json", "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        br.close()

if __name__ == "__main__":
    main()
