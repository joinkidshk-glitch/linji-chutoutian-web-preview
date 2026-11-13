# -*- coding: utf-8 -*-
"""v20a179 實駕：v172 review 唯一新項 C1——鎖行「（場景：X）」改標籤式「場景：X」。
Mirror：~/workspace/linji-work179（分支 v20a179，基底 7801a72），port 8996。
LIVE 模式（無參數）。helpers 改編自 qa172/drive172.py（new_game／story_state／
play_story／clear_encounter／open_notebook／progress_rows／seed_day21），
seed_s2_or 跟 review drive172r2.py（C1–C3 done＋favor 歸零＋mockDebts 清空）。
播種後開手帳係全新渲染，唔會讀 stale DOM（v172 review 探針教訓）。
Cases：A 932 S1（C2 已開放行唔變＋C3 鎖行標籤式）／B 932 S2（C4 OR 行＋C5
多地點行標籤式）／C 700 S1（同 A，700 viewport）。
"""
import json, subprocess, sys, time, os, hashlib, urllib.request, signal
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work179"
HERE = "/home/hatch/workspace/linji-work179/qa179"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8996
results = []

def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    want = hashlib.sha256(open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest()[:12]
    got = hashlib.sha256(body).hexdigest()[:12]
    print("serve sha", got, "want", want, flush=True)
    assert got == want, "served index.html != work copy"
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

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

def click_vis(pg, text):
    ok = pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false; vis[0].click(); return true; }""", text)
    pg.wait_for_timeout(700)
    return ok

def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; }); }""", text)

def clear_encounter(pg, max_steps=40):
    handled = False
    for _ in range(max_steps):
        present = pg.evaluate("""() => {
          const ov = document.getElementById('enc79-overlay');
          if (!ov) return false;
          const line = ov.querySelector('.e79-line');
          return !!(line && (line.textContent||'').trim()); }""")
        if not present:
            return handled
        handled = True
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""")
        pg.wait_for_timeout(700)
        if not clicked:
            break
    return handled

def new_game(pg, query=""):
    pg.goto(f"http://127.0.0.1:{PORT}/index.html{query}")
    pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
    except Exception:
        pass
    click_first(pg, ["確定出發"], 1500)
    for _ in range(4):
        if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    ok = pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")
    print("NEW GAME OK:", ok, pg.evaluate("() => window.S ? (S.dayIndex + ' ' + S.dateStr) : 'no S'"), flush=True)
    return ok

def story_state(pg):
    return pg.evaluate("""() => {
      const plate = document.querySelector('.story-play .dlg106-plate');
      const choice = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null);
      const line = plate ? plate.querySelector('.sp-line') : null;
      const spk = plate ? plate.querySelector('.sp-speaker') : null;
      const title = document.querySelector('.story-play .sp-title, .story-play h2, .story-play h3');
      return {active: !!plate,
        maskStory: !!document.querySelector('#mask.story-play-on'),
        speaker: spk ? spk.textContent : null,
        text: line ? line.textContent.slice(0, 120) : null,
        title: title ? title.textContent.slice(0, 40) : null,
        choices: choice.map(c => (c.textContent||'').trim().slice(0, 40)),
      }; }""")

def play_story(pg, secs=180):
    lines = []
    for _ in range(int(secs / 0.7)):
        st = story_state(pg)
        if st["active"] and st["text"]:
            t1 = st["text"]
            pg.wait_for_timeout(500)
            st2 = story_state(pg)
            if st2["active"] and st2["text"] == t1:
                if not lines or lines[-1]["text"] != t1:
                    lines.append({"speaker": st2["speaker"], "text": t1, "title": st2["title"]})
                st = st2
            else:
                continue
        if pg.evaluate("""() => { const cs=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
            if(!cs.length) return false; cs[0].click(); return true; }"""):
            pg.wait_for_timeout(800); continue
        if click_vis(pg, "下一句"):
            continue
        mask_on = pg.evaluate("() => { const m = document.getElementById('mask'); return !!m && m.classList.contains('on'); }")
        if mask_on and click_vis(pg, "關閉"):
            continue
        if vis_btn(pg, "過一日") and not mask_on:
            break
        pg.wait_for_timeout(700)
    return {"lines": lines, "on_map": vis_btn(pg, "過一日") and not pg.evaluate(
        "() => { const m = document.getElementById('mask'); return !!m && m.classList.contains('on'); }")}

def seed_day21(pg):
    return pg.evaluate("""() => { S.dayIndex = 21; S.story.done.C1 = true; S.story.done.C2 = false;
      S.story.lastMainDoneDay = 20; S.gigCount = 3; S.story.gigCount = 3;
      S.rumors = ['tvb_rules_gossip']; S.story.rumors = ['tvb_rules_gossip'];
      if (S.travel114) S.travel114.used = 0; return true; }""")

def seed_s2_or(pg):
    return pg.evaluate("""() => {
      S.dayIndex = 21; S.story.lastMainDoneDay = 20;
      ['C1','C2','C3'].forEach(id => { S.story.done[id] = true; });
      S.gigCount = 3; S.story.gigCount = 3;
      S.rumors = ['tvb_rules_gossip']; S.story.rumors = ['tvb_rules_gossip'];
      if (!S.story.favor) S.story.favor = {};
      S.story.favor.agency_ho = 0;
      if (S.story.rel) { S.story.rel.rel_ho = 0; S.story.rel.rel_agent = 0; }
      if (S.npcs) S.npcs.agent = 0;
      S.mockDebts = [];
      if (S.travel114) S.travel114.used = 0;
      return true; }""")

def open_notebook(pg):
    ok = pg.evaluate("""() => { const b = document.getElementById('btn-menu');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(800)
    ok2 = pg.evaluate("""() => { const b = document.querySelector('[data-m="journal"]');
      if (!b) return false; b.click(); return true; }""")
    pg.wait_for_timeout(1200)
    return bool(ok and ok2 and pg.evaluate("() => !!document.querySelector('#v-home')"))

def nb_tab(pg, text):
    return pg.evaluate("""(t) => {
      const els=[...document.querySelectorAll('#v-home button')].filter(e=>{
        const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && (e.innerText||'').trim()===t;});
      if(!els.length) return false; els[0].click(); return true; }""", text)

def progress_rows(pg):
    return pg.evaluate("""() => {
      const rows = [...document.querySelectorAll('#home-pane-progress .prog71-row')].map(e => {
        const btn = e.querySelector('button');
        return {playBtn: btn ? (btn.innerText||'').trim() : null,
                txt: (e.innerText||'').replace(/\\n/g,'／').slice(0,400)}; });
      return rows; }""")

def shot(pg, name):
    clear_encounter(pg)
    try:
        pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(SHOTS, name))
    except Exception as e:
        print("shot fail", name, e, flush=True)

def run_case(pw, fn, name, height=932):
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 430, "height": height})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("CONSOLE-ERR: " + m.text) if m.type == "error" else None)
    rec = {"case": name}
    try:
        fn(pg, rec)
    except Exception as e:
        rec["exception"] = str(e)
    finally:
        rec["pageerrors"] = errs[:5]
        results.append(rec)
        print(name, "PASS" if rec.get("pass") and not errs else "FAIL",
              "| pageerrors:", len(errs), "|",
              {k: v for k, v in rec.items() if k not in ("case", "pass", "pageerrors")}, flush=True)
        br.close()
    return rec

def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            # ============ A: 932 S1——C2 已開放行唔變＋C3 鎖行標籤式 ============
            def case_a(pg, rec):
                rec["new_game"] = new_game(pg)
                clear_encounter(pg)
                if story_state(pg)["active"]:
                    play_story(pg)
                seed_day21(pg)
                pg.wait_for_timeout(500)
                rec["nb_open"] = open_notebook(pg)
                rec["nb_progress_tab"] = nb_tab(pg, "進度")
                pg.wait_for_timeout(900)
                rows = progress_rows(pg)
                rec["rows"] = rows[:4]
                shot(pg, "A_progress_s1.png")
                c2 = rows[1] if len(rows) > 1 else {}
                c3 = rows[2] if len(rows) > 2 else {}
                c2t, c3t = c2.get("txt") or "", c3.get("txt") or ""
                rec["c2_open_unchanged"] = ("返地圖嗰陣就會播出" in c2t
                    and "（場景：星河電視台）" in c2t and c2.get("playBtn") is None)
                rec["c3_tag"] = ("場景：星河電視台" in c3t)
                rec["c3_no_paren"] = ("（場景：" not in c3t)
                rec["c3_no_trigger"] = ("先播到呢幕" not in c3t and "就會觸發" not in c3t)
                rec["c3_rumor_hint_kept"] = ("聽到傳聞" in c3t)
                rec["pass"] = bool(rec["new_game"] and rec["nb_open"] and rec["nb_progress_tab"]
                    and rec["c2_open_unchanged"] and rec["c3_tag"] and rec["c3_no_paren"]
                    and rec["c3_no_trigger"] and rec["c3_rumor_hint_kept"])
            run_case(pw, case_a, "A_932_s1_open_c2_locked_c3")

            # ============ B: 932 S2——C4 OR 行＋C5 多地點行標籤式 ============
            def case_b(pg, rec):
                rec["new_game"] = new_game(pg)
                clear_encounter(pg)
                if story_state(pg)["active"]:
                    play_story(pg)
                seed_s2_or(pg)
                pg.wait_for_timeout(500)
                rec["c4_remain"] = pg.evaluate("""() => { try {
                  const p = BehaviorGate.progressToward({ id: 'C4' });
                  return p.remain; } catch(e){ return 'ERR:'+e; } }""")
                rec["nb_open"] = open_notebook(pg)
                rec["nb_progress_tab"] = nb_tab(pg, "進度")
                pg.wait_for_timeout(900)
                rows = progress_rows(pg)
                rec["rows"] = rows[:6]
                shot(pg, "B_progress_s2.png")
                c4 = rows[3] if len(rows) > 3 else {}
                c5 = rows[4] if len(rows) > 4 else {}
                c4t, c5t = c4.get("txt") or "", c5.get("txt") or ""
                rec["c4_or_tag"] = ("或場景：何生事務所" in c4t)
                rec["c4_no_paren"] = ("（場景：" not in c4t)
                rec["c4_no_or_to"] = ("或到" not in c4t)
                rec["c5_tag"] = ("場景：金龍茶餐廳或星河電視台" in c5t)
                rec["c5_no_paren"] = ("（場景：" not in c5t)
                rec["pass"] = bool(rec["new_game"] and rec["nb_open"] and rec["nb_progress_tab"]
                    and rec["c4_or_tag"] and rec["c4_no_paren"] and rec["c4_no_or_to"]
                    and rec["c5_tag"] and rec["c5_no_paren"])
            run_case(pw, case_b, "B_932_s2_or_c4_multi_c5")

            # ============ C: 700 S1——同 A ============
            def case_c(pg, rec):
                rec["new_game"] = new_game(pg)
                clear_encounter(pg)
                if story_state(pg)["active"]:
                    play_story(pg)
                seed_day21(pg)
                pg.wait_for_timeout(500)
                rec["nb_open"] = open_notebook(pg)
                rec["nb_progress_tab"] = nb_tab(pg, "進度")
                pg.wait_for_timeout(900)
                rows = progress_rows(pg)
                rec["rows"] = rows[:4]
                shot(pg, "C700_progress_s1.png")
                c2 = rows[1] if len(rows) > 1 else {}
                c3 = rows[2] if len(rows) > 2 else {}
                c2t, c3t = c2.get("txt") or "", c3.get("txt") or ""
                rec["c2_open_unchanged"] = ("返地圖嗰陣就會播出" in c2t
                    and "（場景：星河電視台）" in c2t and c2.get("playBtn") is None)
                rec["c3_tag"] = ("場景：星河電視台" in c3t)
                rec["c3_no_paren"] = ("（場景：" not in c3t)
                rec["pass"] = bool(rec["new_game"] and rec["nb_open"] and rec["nb_progress_tab"]
                    and rec["c2_open_unchanged"] and rec["c3_tag"] and rec["c3_no_paren"])
            run_case(pw, case_c, "C_700_s1_open_c2_locked_c3", height=700)
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive179.json"), "w", encoding="utf-8") as f:
        json.dump({"cases": results}, f, ensure_ascii=False, indent=2)
    n_pass = sum(1 for r in results if r.get("pass") and not r.get("pageerrors"))
    n_err = sum(len(r.get("pageerrors") or []) for r in results)
    print(f"OVERALL {n_pass}/{len(results)} cases PASS (0 pageerror 計入), total pageerrors={n_err}")

if __name__ == "__main__":
    main()
