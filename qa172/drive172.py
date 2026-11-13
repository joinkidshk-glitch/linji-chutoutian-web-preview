# -*- coding: utf-8 -*-
"""v20a172 實駕：v165 review B1＋C1 修復。
Mirror：~/workspace/linji-work172（分支 v20a172，基底 6d08c7c），port 8999。
LIVE 模式（無參數）為主——驗強制播必須行 live（NOTES §2 規則）；soft case 專門驗
B1(b) 新行為（強制播帶 ignoreSheetLoc，soft 下都播到；普通 start 仍然受 soft 閘擋）。
助手（helpers）改編自 v165 review 獨立 drive（drive165r.py）：new_game／story_state／
play_story／clear_encounter／open_notebook／progress_rows／open_location。
證據以 DOM 層為準；headless_shell 截圖間中有 stale frame，只作輔助——每次截圖前先
清 enc79 overlay（v167 教訓）；「過一日」掣喺 modal 下面都讀到 visible，唔可當作
「已返地圖」信號（要加 mask 檢查）。
Cases：A live fresh C1／B 進度頁鎖行 C3（932）／C #loc-close live C2／
D soft fresh C1（新行為）／E soft 普通 start 仍然受閘 vs 強制播對照／F 700 綜合。
"""
import json, subprocess, sys, time, os, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work172"
HERE = "/home/hatch/workspace/linji-work172/qa172"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8999
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
        p.send_signal(subprocess.signal.SIGTERM); p.wait(timeout=5)
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
    """逐句撳「下一句」／抉擇，直至返地圖。計句嗰陣要等打字機停定先計——
    .sp-line 逐字打出，未停定嗰陣 poll 到半句會當多咗一句（探針證實：C1 節點
    數據 8 beats／16 lines，但唔等停定會數到 18–22 個 DOM 狀態）。"""
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
                continue  # 仲打緊字，下個 loop 再睇
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
    # 注意：liveGigCount() 讀嘅係 S.story.gigCount（＋S.flags done_*），唔係 S.gigCount；
    # liveRumors() 讀嘅係 S.mockRumors／S.notebook.rumors／S.story.rumors／flags，
    # 唔係 S.rumors——v165 review 嘅種子兩個 field 都寫錯，soft 下 C2 永遠唔達
    # （見 NOTES §6.3）。正確 field 係 story.gigCount／story.rumors；舊寫法留返無害。
    return pg.evaluate("""() => { S.dayIndex = 21; S.story.done.C1 = true; S.story.done.C2 = false;
      S.story.lastMainDoneDay = 20; S.gigCount = 3; S.story.gigCount = 3;
      S.rumors = ['tvb_rules_gossip']; S.story.rumors = ['tvb_rules_gossip'];
      if (S.travel114) S.travel114.used = 0; return true; }""")

def s_probe(pg):
    return pg.evaluate("""() => { try { return {
      dayIndex: S.dayIndex, travelUsed: (S.travel114||{}).used,
      done: Object.keys(S.story && S.story.done || {}).filter(k => S.story.done[k]),
      gatePath: (typeof BehaviorGate!=='undefined' ? BehaviorGate.gatePath() : 'NOBG'),
    }; } catch(e){ return {err: String(e)}; } }""")

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
                txt: (e.innerText||'').replace(/\\n/g,'／').slice(0,200)}; });
      return rows; }""")

def open_location(pg, name):
    click_first(pg, ["返回地圖"], 800)
    pg.wait_for_timeout(600)
    for _ in range(2):
        pg.evaluate("""(name) => {
          const pins=[...document.querySelectorAll('.pin')];
          const p=pins.find(x=>{ const l=x.querySelector('.plab'); return l && (l.textContent||'').trim()===name; });
          if(!p) return null;
          const img=p.querySelector('.pin-img'); if(img){ img.click(); return p.dataset.loc; }
          const lab=p.querySelector('.plab'); if(lab){ lab.click(); return p.dataset.loc; }
          return null; }""", name)
        pg.wait_for_timeout(1200)
        clear_encounter(pg)
        pg.wait_for_timeout(600)
        if pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }"):
            return True
        click_first(pg, ["返回地圖"], 600)
        pg.wait_for_timeout(400)
    return False

def sheet_on(pg):
    return pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }")

def shot(pg, name):
    clear_encounter(pg)
    try:
        pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(SHOTS, name))
    except Exception as e:
        print("shot fail", name, e, flush=True)

def run_case(pw, fn, name):
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 430, "height": 932})
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
        print(name, "PASS" if rec.get("pass") else "FAIL",
              "| pageerrors:", len(errs), "|", {k: v for k, v in rec.items()
              if k not in ("case", "pass", "pageerrors")}, flush=True)
        br.close()
    return rec

def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            # ============ A: live fresh C1 即播 ============
            def case_a(pg, rec):
                rec["new_game"] = new_game(pg)
                clear_encounter(pg)
                pg.wait_for_timeout(1500)
                st = story_state(pg)
                rec["c1_auto_play"] = bool(st["active"] and st["maskStory"])
                rec["c1_title"] = st["title"]
                rec["c1_first_text"] = st["text"]
                rec["travel_before"] = s_probe(pg).get("travelUsed")
                shot(pg, "A_c1_stage.png")
                play = play_story(pg)
                rec["c1_lines"] = len(play["lines"])
                rec["c1_done"] = "C1" in (s_probe(pg).get("done") or [])
                rec["back_on_map"] = play["on_map"]
                rec["travel_after"] = s_probe(pg).get("travelUsed")
                rec["pass"] = bool(rec["new_game"] and rec["c1_auto_play"]
                                   and rec["c1_title"] and "第一日" in (rec["c1_title"] or "")
                                   and rec["c1_lines"] == 16 and rec["c1_done"]
                                   and rec["back_on_map"] and rec["travel_before"] == 0
                                   and rec["travel_after"] == 0)
            run_case(pw, case_a, "A_live_fresh_c1")

            # ============ B: 進度頁鎖行 C3（932） ============
            def case_b(pg, rec):
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
                shot(pg, "B_progress_notebook.png")
                c2 = rows[1] if len(rows) > 1 else {}
                c3 = rows[2] if len(rows) > 2 else {}
                rec["c2_open_row_ok"] = ("返地圖嗰陣就會播出" in (c2.get("txt") or "")
                                         and "場景" in (c2.get("txt") or "")
                                         and c2.get("playBtn") is None)
                rec["c3_locked_scene_framing"] = ("（場景：星河電視台）" in (c3.get("txt") or ""))
                rec["c3_no_trigger_framing"] = ("先播到呢幕" not in (c3.get("txt") or "")
                                                and "去星河電視台先播到" not in (c3.get("txt") or "")
                                                and "就會觸發" not in (c3.get("txt") or ""))
                rec["c3_rumor_hint_kept"] = ("聽到傳聞" in (c3.get("txt") or ""))
                rec["pass"] = bool(rec["new_game"] and rec["nb_open"] and rec["nb_progress_tab"]
                                   and rec["c2_open_row_ok"] and rec["c3_locked_scene_framing"]
                                   and rec["c3_no_trigger_framing"] and rec["c3_rumor_hint_kept"])
            run_case(pw, case_b, "B_progress_locked_c3")

            # ============ C: #loc-close live C2 ============
            def case_c(pg, rec):
                rec["new_game"] = new_game(pg)
                clear_encounter(pg)
                if story_state(pg)["active"]:
                    play_story(pg)
                seed_day21(pg)
                pg.wait_for_timeout(500)
                rec["agency_open"] = open_location(pg, "何生事務所")
                rec["travel_after_open"] = s_probe(pg).get("travelUsed")
                rec["sheet_before_close"] = sheet_on(pg)
                rec["loc_close_clicked"] = pg.evaluate("""() => {
                  const b = document.getElementById('loc-close');
                  if (!b) return false; b.click(); return true; }""")
                pg.wait_for_timeout(1500)
                st = story_state(pg)
                rec["c2_forced_via_locclose"] = bool(st["active"] and st["maskStory"])
                rec["c2_title"] = st["title"]
                geom = pg.evaluate("""() => ({
                  storyRoots: document.querySelectorAll('#story-play-root').length,
                  sheetOn: (()=>{ const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); })(),
                  awdStage: document.querySelectorAll('.awd62-stage').length,
                  travelUsed: (S.travel114||{}).used,
                })""")
                rec["geom"] = geom
                rec["single_stage"] = geom["storyRoots"] == 1 and geom["sheetOn"] is False and geom["awdStage"] == 0
                shot(pg, "C_c2_forced_stage.png")
                if rec["c2_forced_via_locclose"]:
                    play = play_story(pg)
                    rec["c2_lines"] = len(play["lines"])
                    rec["c2_done"] = "C2" in (s_probe(pg).get("done") or [])
                    rec["back_on_map"] = play["on_map"]
                rec["pass"] = bool(rec["new_game"] and rec["agency_open"] and rec["travel_after_open"] == 1
                                   and rec["c2_forced_via_locclose"] and rec["single_stage"]
                                   and geom["travelUsed"] == 1 and rec.get("c2_done") and rec.get("back_on_map"))
            run_case(pw, case_c, "C_loc_close_live_c2")

            # ============ D: soft fresh C1（B1 新行為） ============
            def case_d(pg, rec):
                rec["new_game"] = new_game(pg, "?softPreview=1")
                clear_encounter(pg)
                pg.wait_for_timeout(2000)
                st = story_state(pg)
                rec["gate_path"] = s_probe(pg).get("gatePath")
                rec["c1_auto_play_soft"] = bool(st["active"] and st["maskStory"])
                rec["c1_title"] = st["title"]
                rec["c1_first_text"] = st["text"]
                shot(pg, "D_soft_c1_stage.png")
                if rec["c1_auto_play_soft"]:
                    play = play_story(pg)
                    rec["c1_lines"] = len(play["lines"])
                    rec["c1_done"] = "C1" in (s_probe(pg).get("done") or [])
                    rec["back_on_map"] = play["on_map"]
                rec["pass"] = bool(rec["new_game"] and rec["gate_path"] == "soft"
                                   and rec["c1_auto_play_soft"] and rec.get("c1_lines") == 16
                                   and rec.get("c1_done") and rec.get("back_on_map"))
            run_case(pw, case_d, "D_soft_forced_c1")

            # ============ E: soft 普通 start 仍然受閘 vs 強制播對照 ============
            def case_e(pg, rec):
                rec["new_game"] = new_game(pg, "?softPreview=1")
                clear_encounter(pg)
                # soft 下 C1 會經強制播即播（D 已驗）；播完佢先種 day21
                if story_state(pg)["active"]:
                    play_story(pg)
                seed_day21(pg)
                pg.wait_for_timeout(500)
                rec["gate_path"] = s_probe(pg).get("gatePath")
                rec["on_map"] = vis_btn(pg, "過一日")
                probe = pg.evaluate("""() => { try {
                  const node = (typeof StoryOC!=='undefined' && StoryOC.findNodeRaw) ? StoryOC.findNodeRaw('C2') : null;
                  if (!node) return {storyOC: false};
                  const evPlain = StoryOC.evalNode(node, {checkNodePhase:true});
                  const evIgn = StoryOC.evalNode(node, {checkNodePhase:true, ignoreSheetLoc:true});
                  return {storyOC: true,
                    ev_plain_ok: evPlain.ok, ev_plain_reasons: evPlain.reasons,
                    ev_ign_ok: evIgn.ok, ev_ign_reasons: evIgn.reasons};
                } catch(e){ return {err: String(e)}; } }""")
                rec["eval_probe"] = probe
                rec["eval_plain_fails_only_on_loc"] = (probe.get("ev_plain_ok") is False
                                                       and probe.get("ev_plain_reasons") == ["locIdAny"])
                rec["eval_ign_ok"] = probe.get("ev_ign_ok") is True
                rec["ordinary_start_c2"] = pg.evaluate("() => { try { return !!StoryPlay.start('C2'); } catch(e){ return 'ERR:'+e; } }")
                rec["ordinary_still_gated"] = rec["ordinary_start_c2"] is False
                rec["no_story_after_ordinary"] = not story_state(pg)["active"]
                # 經手帳「返回地圖」（book70ExitHome）觸發強制播
                rec["nb_open"] = open_notebook(pg)
                pg.wait_for_timeout(600)
                rec["back_clicked"] = click_vis(pg, "返回地圖")
                pg.wait_for_timeout(1500)
                st = story_state(pg)
                rec["c2_forced_via_book70"] = bool(st["active"] and st["maskStory"])
                rec["c2_title"] = st["title"]
                shot(pg, "E_soft_c2_forced_stage.png")
                if rec["c2_forced_via_book70"]:
                    play = play_story(pg)
                    rec["c2_lines"] = len(play["lines"])
                    rec["c2_done"] = "C2" in (s_probe(pg).get("done") or [])
                    rec["back_on_map"] = play["on_map"]
                rec["pass"] = bool(rec["new_game"] and rec["gate_path"] == "soft" and rec["on_map"]
                                   and rec["eval_plain_fails_only_on_loc"] and rec["eval_ign_ok"]
                                   and rec["ordinary_still_gated"] and rec["no_story_after_ordinary"]
                                   and rec["c2_forced_via_book70"] and rec.get("c2_done") and rec.get("back_on_map"))
            run_case(pw, case_e, "E_soft_ordinary_vs_forced")

            # ============ F: 700 綜合 ============
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 430, "height": 700})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("CONSOLE-ERR: " + m.text) if m.type == "error" else None)
            rec = {"case": "F_700_live_c1_and_locked"}
            try:
                rec["new_game"] = new_game(pg)
                clear_encounter(pg)
                pg.wait_for_timeout(1500)
                st = story_state(pg)
                rec["c1_auto_play"] = bool(st["active"] and st["maskStory"])
                rec["c1_first_text"] = st["text"]
                shot(pg, "F700_c1_stage.png")
                if rec["c1_auto_play"]:
                    play_story(pg)
                seed_day21(pg)
                pg.wait_for_timeout(500)
                rec["nb_open"] = open_notebook(pg)
                rec["nb_progress_tab"] = nb_tab(pg, "進度")
                pg.wait_for_timeout(900)
                rows = progress_rows(pg)
                c3 = rows[2] if len(rows) > 2 else {}
                rec["c3_txt"] = (c3.get("txt") or "")[:200]
                rec["c3_locked_scene_framing"] = ("（場景：星河電視台）" in (c3.get("txt") or ""))
                rec["c3_no_trigger_framing"] = ("先播到呢幕" not in (c3.get("txt") or "")
                                                and "就會觸發" not in (c3.get("txt") or ""))
                shot(pg, "F700_progress_notebook.png")
                rec["pass"] = bool(rec["new_game"] and rec["c1_auto_play"] and rec["nb_open"]
                                   and rec["nb_progress_tab"] and rec["c3_locked_scene_framing"]
                                   and rec["c3_no_trigger_framing"])
            except Exception as e:
                rec["exception"] = str(e)
            finally:
                rec["pageerrors"] = errs[:5]
                results.append(rec)
                print("F_700_live_c1_and_locked", "PASS" if rec.get("pass") else "FAIL",
                      "| pageerrors:", len(errs), "|",
                      {k: v for k, v in rec.items() if k not in ("case", "pass", "pageerrors")}, flush=True)
                br.close()
    finally:
        stop(srv)
    with open(os.path.join(HERE, "drive172.json"), "w", encoding="utf-8") as f:
        json.dump({"cases": results}, f, ensure_ascii=False, indent=2)
    n_pass = sum(1 for r in results if r.get("pass") and not r.get("pageerrors"))
    n_err = sum(len(r.get("pageerrors") or []) for r in results)
    print(f"OVERALL {n_pass}/{len(results)} cases PASS (0 pageerror 計入), total pageerrors={n_err}")

if __name__ == "__main__":
    main()
