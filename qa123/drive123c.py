# -*- coding: utf-8 -*-
"""v20a123 實駕補場 drive123c（branch only）：淨返 awi_s2_sad／awi_s3_sad。
  C1 tier2／C2 tier3：葉敏芝 yip_choice beat（1991 年＋fav tier≥2；foreshadow 標 done
       逼 PickBeat 落 choice，內有阿偉 sad 句「你放心，今日呢番話，出咗呢道門就冇咗。」）。
       香江唱片 rec_hk，1991 夏 day 516 起。
  C3 後備：主線 C7（tier2，sad 句喺 C7 beats）／C14（tier3）經進度頁播呢幕，
       先種 S.story.done 前置＋設返相應季節日。
  PASS：兩張 sad 全部渲染見齊＋0 pageerror＋branch 目標 404＝0。
用法：pwenv49 python qa123/drive123c.py
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8951
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
TARGETS = ["awi_s2_sad.webp", "awi_s3_sad.webp"]
LOG = {"phases": {}, "errors": [], "http404": [], "target404": {},
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
    return 3 if (n_lead >= 3 and fame >= 70) else (2 if n_lead >= 1 else 0)

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
            pg.screenshot(path=f"{SHOTS}/c_{tag}_{s.replace('.webp', '')}.png")
            print(f"  >> {tag}[{i}] TARGET {s} :: {info['name']} | {info['line']}")
        if i < 4:
            print(f"  ENC {tag}[{i}] name={info['name']} line={info['line']} L={info['L']} R={info['R']}")
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
            print(f"  [{tag}] day {day}: 入場冇觸發")
            back_to_map(pg)
            continue
        overlay_days.append(day)
        print(f"  [{tag}] day {day}: overlay，行晒佢")
        seen, rendered = step_overlay_full(pg, targets, tag)
        seen_all |= seen
        rendered_all.extend(rendered)
        print(f"  [{tag}] day {day}: seen={sorted(seen)}")
        back_to_map(pg)
        if seen_all == set(targets):
            break
    return seen_all, rendered_all, overlay_days

def play_story_node(pg, node, target, tag, max_steps=70):
    """經進度頁播呢幕；逐句行，睇 target 檔。回傳 (found, steps_played)。"""
    pg.evaluate("() => { const b = document.getElementById('map-progress-btn'); if (b) b.click(); }")
    pg.wait_for_timeout(1200)
    played = pg.evaluate("""(n) => { const b = document.querySelector('[data-prog77-play="' + n + '"]');
      if (b) { b.click(); return true; } return false; }""", node)
    print(f"  [{tag}] progress play {node}: {played}")
    if not played:
        return False, 0
    pg.wait_for_timeout(1500)
    for step in range(max_steps):
        info = pg.evaluate(JS_STORY)
        srcs = [(c["id"], c["src"]) for c in info["chars"]]
        if step < 4 or target in [s for _, s in srcs]:
            print(f"  STORY {tag}[{step}] spk={info['speaker']} line={info['line']} chars={srcs}")
        if info["active"] and any(s == target for _, s in srcs):
            pg.screenshot(path=f"{SHOTS}/c_{tag}_{target.replace('.webp', '')}.png")
            print(f"  >> {tag} FOUND {target} at step {step}: {info['line']}")
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
            print(f"  [{tag}] 冇下一句掣，停（step {step}）")
            break
        pg.wait_for_timeout(500)
    return False, max_steps

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
        for n in TARGETS:
            st, ln = http_status("assets/story/fullbody/" + n)
            assert st == 200, f"server check failed for {n}"
        print("server check ok")
        missing = set(TARGETS)
        # C1 tier2 Yip choice
        print("== c1_yip_t2 ==")
        new_game(pg); t = set_tier(pg, 1, 0); print("  tier ->", t)
        pg.evaluate("""() => {
          S.stars = S.stars || {};
          const st = S.stars.yip_manji || (S.stars.yip_manji = {});
          st.met = true; st.fav = 25; st.beatsDone = { yip_foreshadow: 1 };
          return st;
        }""")
        seen, rendered, odays = try_days_enc(pg, ["香江唱片"], list(range(516, 522)), {"awi_s2_sad.webp"}, "c1_yip_t2")
        LOG["phases"]["c1"] = {"seen": sorted(seen), "overlay_days": odays}
        LOG["rendered"]["c1"] = rendered
        LOG["seen"] = sorted(set(LOG["seen"]) | seen)
        missing = set(TARGETS) - set(LOG["seen"])
        print("  missing now:", sorted(missing))
        # C2 tier3 Yip choice
        if "awi_s3_sad.webp" in missing:
            print("== c2_yip_t3 ==")
            new_game(pg); t = set_tier(pg, 3, 70); print("  tier ->", t)
            pg.evaluate("""() => {
              S.stars = S.stars || {};
              const st = S.stars.yip_manji || (S.stars.yip_manji = {});
              st.met = true; st.fav = 25; st.beatsDone = { yip_foreshadow: 1 };
              return st;
            }""")
            seen, rendered, odays = try_days_enc(pg, ["香江唱片"], list(range(516, 522)), {"awi_s3_sad.webp"}, "c2_yip_t3")
            LOG["phases"]["c2"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["c2"] = rendered
            LOG["seen"] = sorted(set(LOG["seen"]) | seen)
            missing = set(TARGETS) - set(LOG["seen"])
            print("  missing now:", sorted(missing))
        # C3 後備：主線 C7（tier2）／C14（tier3）
        if "awi_s2_sad.webp" in missing:
            print("== c3_c7_t2 ==")
            new_game(pg); t = set_tier(pg, 1, 0)
            pg.evaluate("""() => {
              S.dayIndex = 180;
              S.story = S.story || {}; S.story.done = S.story.done || {};
              for (const n of ["C1","C2","C3","C4","C5","C6"]) S.story.done[n] = 1;
              return { day: S.dayIndex };
            }""")
            click_first(pg, ["維港電影"], 1800)
            pg.wait_for_timeout(900)
            found, n = play_story_node(pg, "C7", "awi_s2_sad.webp", "c3_c7_t2")
            LOG["phases"]["c3"] = {"found": found, "steps": n}
            if found:
                LOG["seen"] = sorted(set(LOG["seen"]) | ["awi_s2_sad.webp"])
            missing = set(TARGETS) - set(LOG["seen"])
            print("  missing now:", sorted(missing))
        if "awi_s3_sad.webp" in missing:
            print("== c3_c14_t3 ==")
            new_game(pg); t = set_tier(pg, 3, 70)
            pg.evaluate("""() => {
              S.dayIndex = 200;
              S.story = S.story || {}; S.story.done = S.story.done || {};
              for (const n of ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12","C13"]) S.story.done[n] = 1;
              return { day: S.dayIndex };
            }""")
            click_first(pg, ["星河電視台"], 1800)
            pg.wait_for_timeout(900)
            found, n = play_story_node(pg, "C14", "awi_s3_sad.webp", "c3_c14_t3")
            LOG["phases"]["c3b"] = {"found": found, "steps": n}
            if found:
                LOG["seen"] = sorted(set(LOG["seen"]) | ["awi_s3_sad.webp"])
            missing = set(TARGETS) - set(LOG["seen"])
            print("  missing now:", sorted(missing))
        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

LOG["PASS"] = bool(not (set(TARGETS) - set(LOG["seen"]))
                   and not LOG["target404"] and not LOG["errors"])
print("seen:", LOG["seen"])
print("missing:", sorted(set(TARGETS) - set(LOG["seen"])))
print("target404:", LOG["target404"])
print("pageerrors:", LOG["errors"][:6])
print("OVERALL PASS:", LOG["PASS"])
with open(os.path.join(HERE, "drive_log123c.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
