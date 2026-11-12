# -*- coding: utf-8 -*-
"""v20a126 實駕 drive126（branch／pristine 兩跑，同一腳本）：
  目標 6 張：fong_siulung_smile、pang_siuki_serious、gu_mingfai_smile、
  yip_manji_serious、lan_ruoxi_shy、ching_tinlok_sad。
  巧遇 4 星（真 UI 路徑：入主場地點 → ENC79 overlay 逐句行晒，log 齊兩邊 srcs）：
    pang（中環廣告，T0 opener 有 serious 句；seed met＋fav 5）｜
    ching（天星音樂，first＋T0 opener 有 sad 句；先 610-621，唔中再 730-741＋met／fav 15）｜
    yip（香江唱片，heart 有 serious 句；seed met＋fav 50，tier≥3 先播 heart）｜
    gu（海港廣播，T1 opener 有 happy 句；seed met＋fav 15）。
  主線 2 角：
    fong：A_fong_push1（happy 句「跳完呢場，我請你食宵夜，哈哈！」）——先試 3 日入
      星河電視台睇下有冇 storylet 觸發，唔中就合成 StoryPlay.start(id)（真播放器＋
      真 loader，只係觸發合成；v119 合成對照先例）。
    lan：R_lan_meet（shy 句首句）——同上，seed phase P2；唔中就合成。
  Pristine 跑同一套：目標 404 數要跌（branch 0；pristine 遇上嗰句即 404）。
  用法：pwenv49 python qa126/drive126.py [root] [branch|pristine]
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE = sys.argv[2] if len(sys.argv) > 2 else "branch"
ONLY = sys.argv[3] if len(sys.argv) > 3 else "all"  # all | enc | story
HERE = os.path.join(ROOT, "qa126")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8951
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
TARGETS = ["fong_siulung_smile.webp", "pang_siuki_serious.webp",
           "gu_mingfai_smile.webp", "yip_manji_serious.webp",
           "lan_ruoxi_shy.webp", "ching_tinlok_sad.webp"]
LOG = {"mode": MODE, "phases": {}, "errors": [], "http404": [], "target404": {},
       "rendered": {}, "seen": []}

def http_status(path):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
            return r.status, len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, 0
    except Exception:
        return None, 0

def http_body(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
        return r.status, r.read()

def serve(cwd):
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=cwd,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError(f"http.server died on start (port {PORT} probably taken)")
    st, body = http_body("index.html")
    sha = hashlib.sha256(body).hexdigest()
    exp = hashlib.sha256(open(os.path.join(cwd, "index.html"), "rb").read()).hexdigest()
    if st != 200 or sha != exp:
        raise RuntimeError(f"served index mismatch: status={st} sha={sha[:12]} expected={exp[:12]}")
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

JS_ENC = '''() => {
  const ov = document.getElementById('enc79-overlay');
  if (!ov) return { present: false };
  const one = (sel) => { const im = ov.querySelector(sel); if (!im) return null;
    return { src: (im.getAttribute('src')||'').split('/').pop().split('?')[0] }; };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  return { present: true, L: one('.e79-char-l'), R: one('.e79-char-r'),
           name: name ? name.textContent : null,
           line: line ? line.textContent.slice(0,60) : null };
}'''

JS_STORY = '''() => {
  const chars = [...document.querySelectorAll('.dlg106-char')].map(im => ({
    id: im.dataset.dlgId, src: (im.getAttribute('src')||'').split('/').pop().split('?')[0] }));
  const sp = document.querySelector('.story-play');
  const speaker = document.querySelector('.story-play .sp-speaker');
  const line = document.querySelector('.story-play .sp-line');
  const choices = [...document.querySelectorAll('.sp-choice')].map(b => b.textContent.trim().slice(0,30));
  return { active: !!sp, chars, speaker: speaker ? speaker.textContent : null,
           line: line ? line.textContent.slice(0,70) : null, choices };
}'''

def new_game(pg):
    pg.goto(URL); pg.wait_for_timeout(3000)
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
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

def set_tier(pg, n_lead, fame):
    pg.evaluate("""(arg) => {
      const leads = (typeof GIGS !== 'undefined' ? GIGS : [])
        .filter(g => g && /lead/.test(String(g.roleScale || ''))).slice(0, 3).map(g => g.id);
      S.flags = S.flags || {};
      for (let i = 0; i < arg.n; i++) S.flags['done_' + leads[i]] = 1;
      if (arg.fame) S.fame = arg.fame;
    }""", {"n": n_lead, "fame": fame})

def seed_star(pg, star, fav):
    pg.evaluate("""(a) => {
      S.stars = S.stars || {};
      const st = S.stars[a.star] || (S.stars[a.star] = {});
      st.met = true; st.fav = a.fav; st.beatsDone = {}; st.poolSeen = {};
      st.heartDone = false; st.stage = 0; st.wrapEcho = false; st.capHit = false;
      return { met: st.met, fav: st.fav };
    }""", {"star": star, "fav": fav})

def back_to_map(pg):
    click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
    pg.wait_for_timeout(700)

def step_overlay_full(pg, targets, tag, max_steps=40):
    seen = set()
    rendered = []
    for i in range(max_steps):
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            break
        srcs = [c["src"] for c in (info["L"], info["R"]) if c and c.get("src")]
        rendered.extend(srcs)
        newly = [s for s in srcs if s in targets and s not in seen]
        for s in srcs:
            if s in targets:
                seen.add(s)
        for s in newly:
            pg.screenshot(path=f"{SHOTS}/{MODE}_{tag}_{s.replace('.webp', '')}.png")
            print(f"  >> {tag}[{i}] TARGET {s} :: {info['name']} | {info['line']}", flush=True)
        if i < 4:
            print(f"  ENC {tag}[{i}] name={info['name']} line={info['line']} L={info['L']} R={info['R']}", flush=True)
        clicked = pg.evaluate("""() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""")
        if not clicked:
            break
        pg.wait_for_timeout(420)
    return seen, rendered

def try_days_enc(pg, loc_labels, days, targets, tag):
    seen_all = set()
    rendered_all = []
    overlay_days = []
    for day in days:
        pg.evaluate("(d) => { S.dayIndex = d; }", day)
        back_to_map(pg)
        click_first(pg, loc_labels, 1800)
        pg.wait_for_timeout(900)
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            print(f"  [{tag}] day {day}: 入場冇觸發", flush=True)
            back_to_map(pg)
            continue
        overlay_days.append(day)
        print(f"  [{tag}] day {day}: overlay，行晒佢", flush=True)
        seen, rendered = step_overlay_full(pg, targets, tag)
        seen_all |= seen
        rendered_all.extend(rendered)
        print(f"  [{tag}] day {day}: seen={sorted(seen)}", flush=True)
        back_to_map(pg)
        if seen_all == set(targets):
            break
    return seen_all, rendered_all, overlay_days

def step_story(pg, target, tag, max_steps=70):
    """行緊嘅 .story-play 逐句行，睇 target 檔。回傳 (found, steps)。"""
    for step in range(max_steps):
        info = pg.evaluate(JS_STORY)
        srcs = [(c["id"], c["src"]) for c in info["chars"]]
        if step < 6 or target in [s for _, s in srcs]:
            print(f"  STORY {tag}[{step}] spk={info['speaker']} line={info['line']} chars={srcs}", flush=True)
        if info["active"] and any(s == target for _, s in srcs):
            pg.screenshot(path=f"{SHOTS}/{MODE}_{tag}_{target.replace('.webp', '')}.png")
            print(f"  >> {tag} FOUND {target} at step {step}: {info['line']}", flush=True)
            return True, step + 1
        if info["choices"]:
            click_first(pg, [info["choices"][0][:6]], 1500)
            pg.wait_for_timeout(1200)
            for _ in range(4):
                if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續"], 900):
                    break
            continue
        clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
          if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
          if (!bs.length) return false; bs[0].click(); return true; }""")
        if not clicked:
            print(f"  [{tag}] 冇下一句掣，停（step {step}）", flush=True)
            break
        pg.wait_for_timeout(500)
    return False, max_steps

def try_storylet_days(pg, loc_labels, days, tag):
    """入地點幾日，睇下有冇 .story-play 自動觸發。回傳 True 如果觸發咗。"""
    for day in days:
        pg.evaluate("(d) => { S.dayIndex = d; }", day)
        back_to_map(pg)
        click_first(pg, loc_labels, 1800)
        pg.wait_for_timeout(1200)
        info = pg.evaluate(JS_STORY)
        enc = pg.evaluate(JS_ENC)
        if info["active"]:
            print(f"  [{tag}] day {day}: story-play 自動觸發", flush=True)
            return True
        if enc["present"]:
            print(f"  [{tag}] day {day}: 巧遇 overlay（唔係 storylet），行晒佢先", flush=True)
            step_overlay_full(pg, set(), tag + "_enc")
        back_to_map(pg)
    return False

def play_story_synth(pg, node, target, tag):
    """合成：直接 StoryPlay.start(node)，其餘全部真（播放器＋loader＋渲染）。"""
    ok = pg.evaluate("""(n) => {
      try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) {}
      return false; }""", node)
    print(f"  [{tag}] synthetic StoryPlay.start({node}): {ok}", flush=True)
    if not ok:
        return False, 0
    pg.wait_for_timeout(1500)
    return step_story(pg, target, tag)

srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        def on_resp(resp):
            try:
                u = resp.url
                if "assets/story/fullbody/" in u and resp.status >= 400:
                    fn = u.split("/").pop().split("?")[0]
                    LOG["http404"].append({"file": fn, "status": resp.status})
                    if fn in TARGETS:
                        LOG["target404"][fn] = LOG["target404"].get(fn, 0) + 1
            except Exception:
                pass
        pg.on("response", on_resp)
        if MODE == "branch":
            chk = {}
            for n in TARGETS:
                st, ln = http_status("assets/story/fullbody/" + n)
                chk[n] = (st == 200 and ln == os.path.getsize(os.path.join(ROOT, "assets", "story", "fullbody", n)))
            print("server check all 6 ok:", all(chk.values()), chk, flush=True)
            assert all(chk.values()), "server check failed — abort"
        missing = set(TARGETS)

        def note(tag, seen):
            global missing
            LOG["seen"] = sorted(set(LOG["seen"]) | seen)
            missing = set(TARGETS) - set(LOG["seen"])
            print(f"  {tag} DONE seen={sorted(seen)} missing={sorted(missing)}", flush=True)

        # ---- E1 pang（T0 opener serious）----
        if ONLY in ("all", "enc") and "pang_siuki_serious.webp" in missing:
            print("== e1_pang ==", flush=True)
            new_game(pg); seed_star(pg, "pang_siuki", 5)
            seen, rendered, odays = try_days_enc(pg, ["中環廣告"], list(range(0, 12)), {"pang_siuki_serious.webp"}, "e1_pang")
            LOG["phases"]["e1_pang"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["e1_pang"] = rendered
            note("e1_pang", seen)

        # ---- E2 ching（first＋T0 opener sad；610-621，唔中再 730-741）----
        if ONLY in ("all", "enc") and "ching_tinlok_sad.webp" in missing:
            print("== e2_ching ==", flush=True)
            new_game(pg)
            seen, rendered, odays = try_days_enc(pg, ["天星音樂"], list(range(610, 622)), {"ching_tinlok_sad.webp"}, "e2_ching")
            LOG["phases"]["e2_ching"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["e2_ching"] = rendered
            note("e2_ching", seen)
        if ONLY in ("all", "enc") and "ching_tinlok_sad.webp" in missing:
            print("== e2b_ching92 ==", flush=True)
            new_game(pg); seed_star(pg, "ching_tinlok", 15)
            seen, rendered, odays = try_days_enc(pg, ["天星音樂"], list(range(730, 742)), {"ching_tinlok_sad.webp"}, "e2b_ching92")
            LOG["phases"]["e2b_ching92"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["e2b_ching92"] = rendered
            note("e2b_ching92", seen)

        # ---- E3 yip（heart serious；fav 50 tier 3）----
        if ONLY in ("all", "enc") and "yip_manji_serious.webp" in missing:
            print("== e3_yip_heart ==", flush=True)
            new_game(pg); seed_star(pg, "yip_manji", 50)
            seen, rendered, odays = try_days_enc(pg, ["香江唱片"], list(range(0, 12)), {"yip_manji_serious.webp"}, "e3_yip_heart")
            LOG["phases"]["e3_yip_heart"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["e3_yip_heart"] = rendered
            note("e3_yip_heart", seen)
        if ONLY in ("all", "enc") and "yip_manji_serious.webp" in missing:
            print("== e3b_yip_lead ==", flush=True)
            new_game(pg); set_tier(pg, 1, 0); seed_star(pg, "yip_manji", 25)
            seen, rendered, odays = try_days_enc(pg, ["香江唱片"], list(range(0, 12)), {"yip_manji_serious.webp"}, "e3b_yip_lead")
            LOG["phases"]["e3b_yip_lead"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["e3b_yip_lead"] = rendered
            note("e3b_yip_lead", seen)

        # ---- E4 gu（T1 opener happy；fav 15）----
        if ONLY in ("all", "enc") and "gu_mingfai_smile.webp" in missing:
            print("== e4_gu ==", flush=True)
            new_game(pg); seed_star(pg, "gu_mingfai", 15)
            seen, rendered, odays = try_days_enc(pg, ["海港廣播"], list(range(0, 12)), {"gu_mingfai_smile.webp"}, "e4_gu")
            LOG["phases"]["e4_gu"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["e4_gu"] = rendered
            note("e4_gu", seen)
        if ONLY in ("all", "enc") and "gu_mingfai_smile.webp" in missing:
            print("== e4b_gu_heart ==", flush=True)
            new_game(pg); seed_star(pg, "gu_mingfai", 50)
            seen, rendered, odays = try_days_enc(pg, ["海港廣播"], list(range(0, 12)), {"gu_mingfai_smile.webp"}, "e4b_gu_heart")
            LOG["phases"]["e4b_gu_heart"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["e4b_gu_heart"] = rendered
            note("e4b_gu_heart", seen)

        # ---- S1 fong（A_fong_push1）----
        if ONLY in ("all", "story") and "fong_siulung_smile.webp" in missing:
            print("== s1_fong ==", flush=True)
            new_game(pg)
            trig = try_storylet_days(pg, ["星河電視台"], [0, 1, 2], "s1_fong_trig")
            if trig:
                found, n = step_story(pg, "fong_siulung_smile.webp", "s1_fong")
                LOG["phases"]["s1_fong"] = {"route": "storylet", "found": found, "steps": n}
                if found: note("s1_fong", {"fong_siulung_smile.webp"})
            else:
                print("  [s1_fong] 3 日入電視台無 storylet 觸發，轉合成", flush=True)
                found, n = play_story_synth(pg, "A_fong_push1", "fong_siulung_smile.webp", "s1_fong")
                LOG["phases"]["s1_fong"] = {"route": "synthetic", "found": found, "steps": n}
                if found: note("s1_fong", {"fong_siulung_smile.webp"})

        # ---- S2 lan（R_lan_meet，seed phase P2）----
        if ONLY in ("all", "story") and "lan_ruoxi_shy.webp" in missing:
            print("== s2_lan ==", flush=True)
            new_game(pg)
            pg.evaluate("""() => { S.story = S.story || {}; S.story.phase = "P2"; return S.story.phase; }""")
            trig = try_storylet_days(pg, ["星河電視台"], [0, 1, 2], "s2_lan_trig")
            if trig:
                found, n = step_story(pg, "lan_ruoxi_shy.webp", "s2_lan")
                LOG["phases"]["s2_lan"] = {"route": "storylet", "found": found, "steps": n}
                if found: note("s2_lan", {"lan_ruoxi_shy.webp"})
            else:
                print("  [s2_lan] 3 日入電視台無 storylet 觸發，轉合成", flush=True)
                found, n = play_story_synth(pg, "R_lan_meet", "lan_ruoxi_shy.webp", "s2_lan")
                LOG["phases"]["s2_lan"] = {"route": "synthetic", "found": found, "steps": n}
                if found: note("s2_lan", {"lan_ruoxi_shy.webp"})

        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

_want = set(TARGETS) if ONLY == "all" else ({"fong_siulung_smile.webp", "lan_ruoxi_shy.webp"} if ONLY == "story"
         else {"pang_siuki_serious.webp", "gu_mingfai_smile.webp", "yip_manji_serious.webp", "ching_tinlok_sad.webp"})
LOG["PASS"] = bool(not (_want - set(LOG["seen"]))
                   and not LOG["target404"] and not LOG["errors"])
print("seen:", LOG["seen"], flush=True)
print("missing:", sorted(set(TARGETS) - set(LOG["seen"])), flush=True)
print("target404:", LOG["target404"], flush=True)
print("all404:", LOG["http404"][:12], flush=True)
print("pageerrors:", LOG["errors"][:6], flush=True)
print("OVERALL PASS:", LOG["PASS"], flush=True)
with open(os.path.join(HERE, f"drive_log126_{MODE}_{ONLY}.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
