# -*- coding: utf-8 -*-
"""v20a123 實駕補場 drive123b（branch only）：
  drive123 教訓：(1) overlay 首句係旁白嗰陣名牌係空嘅——用名牌認星會誤殺真巧遇；
  (2) finish_encounter_if_any 行嗰陣冇 log srcs，結果 8 張目標其實喺 pristine
  嗰陣已經 request 過（18 個目標 404），branch 嗰陣渲染咗但冇記錄到。
  今場修正：逢 overlay 出現就逐句行晒＋log 齊兩邊 srcs，唔再用名牌篩星。
  B1 tier2 天星音樂 day 608-613｜B2 tier2 金龍茶餐廳 day 974-979｜
  B3 tier3 天星音樂 day 608-613｜B4 tier3 金龍茶餐廳 day 974-979｜
  B5a 提升：Liu clash beat（1992 冬＋fav 低＋前 beat 標 done，取 liu_shy_b）｜
  B5b 提升：Chung farewell beat（1992 秋＋fav 30＋review/intel 標 done，取 chung_think_c/d）｜
  B6 掃場（只限仲未見嘅 awi 目標）：其餘五星主場各 5 日。
  PASS：8 個剩餘目標全部渲染見齊＋0 pageerror＋branch 目標 404＝0。
用法：pwenv49 python qa123/drive123b.py
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
REMAIN = ["awi_s2_surprise.webp", "awi_s2_sad.webp", "awi_s2_shy.webp",
          "awi_s3_surprise.webp", "awi_s3_sad.webp", "awi_s3_shy.webp",
          "chung_choning_think.webp", "liu_bingxing_shy.webp"]
NEW_BYTES = {n: os.path.getsize(os.path.join(ROOT, "assets", "story", "fullbody", n)) for n in REMAIN}
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
    """逐句行晒開緊嘅 overlay，log 齊每步兩邊 srcs；回傳 (seen, rendered)。"""
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
            pg.screenshot(path=f"{SHOTS}/b_{tag}_{s.replace('.webp', '')}.png")
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

def try_days(pg, loc_labels, days, targets, tag):
    """逐日入場；逢 overlay 就行晒佢。回傳 (seen, rendered, overlay_days)。"""
    seen_all = set()
    rendered_all = []
    overlay_days = []
    for day in days:
        pg.evaluate("(d) => { S.dayIndex = d; }", day)
        back_to_map(pg)
        opened = click_first(pg, loc_labels, 1800)
        pg.wait_for_timeout(900)
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            print(f"  [{tag}] day {day}: 入場冇觸發")
            back_to_map(pg)
            continue
        overlay_days.append(day)
        star = (info["R"] or {}).get("src", "?")
        print(f"  [{tag}] day {day}: overlay（R={star}），行晒佢")
        seen, rendered = step_overlay_full(pg, targets, tag)
        seen_all |= seen
        rendered_all.extend(rendered)
        print(f"  [{tag}] day {day}: seen={sorted(seen)}")
        back_to_map(pg)
        if seen_all == set(targets):
            break
    return seen_all, rendered_all, overlay_days

def phase(pg, tag, n_lead, fame, loc, days, targets):
    print(f"== {tag} tier n_lead={n_lead} ==")
    ng = new_game(pg)
    t = set_tier(pg, n_lead, fame) if (n_lead or fame) else 0
    print(f"  new_game: {ng}, tier -> {t}")
    seen, rendered, odays = try_days(pg, loc, days, set(targets), tag)
    LOG["phases"][tag] = {"seen": sorted(seen), "overlay_days": odays}
    LOG["rendered"][tag] = rendered
    LOG["seen"] = sorted(set(LOG["seen"]) | seen)
    print(f"  {tag} DONE seen={sorted(seen)} overlay_days={odays}")
    return seen

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
                    if fn in REMAIN:
                        LOG["target404"][fn] = LOG["target404"].get(fn, 0) + 1
            except Exception:
                pass
        pg.on("response", on_resp)
        chk = {}
        for n in REMAIN:
            st, ln = http_status("assets/story/fullbody/" + n)
            chk[n] = (st == 200 and ln == NEW_BYTES[n])
        print("server check all 8 ok:", all(chk.values()), chk)
        assert all(chk.values()), "server check failed — abort"
        missing = set(REMAIN)
        # B1–B4：重播
        for tag, nl, fame, loc, days, tgts in [
            ("b1_chung_t2", 1, 0, ["天星音樂"], list(range(608, 614)),
             ["awi_s2_surprise.webp", "awi_s2_sad.webp", "awi_s2_shy.webp",
              "chung_choning_think.webp"]),
            ("b2_liu_t2", 1, 0, ["金龍茶餐廳"], list(range(974, 980)),
             ["awi_s2_surprise.webp", "awi_s2_sad.webp", "awi_s2_shy.webp",
              "liu_bingxing_shy.webp"]),
            ("b3_chung_t3", 3, 70, ["天星音樂"], list(range(608, 614)),
             ["awi_s3_surprise.webp", "awi_s3_sad.webp", "awi_s3_shy.webp",
              "chung_choning_think.webp"]),
            ("b4_liu_t3", 3, 70, ["金龍茶餐廳"], list(range(974, 980)),
             ["awi_s3_surprise.webp", "awi_s3_sad.webp", "awi_s3_shy.webp",
              "liu_bingxing_shy.webp"]),
        ]:
            if not (set(tgts) & missing):
                print(f"== {tag} SKIP（目標已齊） ==")
                continue
            phase(pg, tag, nl, fame, loc, days, [t for t in tgts if t in missing])
            missing = set(REMAIN) - set(LOG["seen"])
            print("  missing now:", sorted(missing))
        # B5a：Liu clash（1992 冬）
        if "liu_bingxing_shy.webp" in missing:
            print("== b5a_liu_clash ==")
            new_game(pg)
            seen, rendered, odays = try_days(pg, ["金龍茶餐廳"], [975], {"liu_bingxing_shy.webp"}, "b5a_meet")
            LOG["rendered"]["b5a_meet"] = rendered
            LOG["seen"] = sorted(set(LOG["seen"]) | seen)
            pg.evaluate("""() => {
              S.stars = S.stars || {};
              const st = S.stars.liu_bingxing || (S.stars.liu_bingxing = {});
              st.met = true; st.fav = 5;
              st.beatsDone = Object.assign({}, st.beatsDone, { liu_tease: 1, liu_intel: 1, liu_foreshadow: 1, liu_repay: 1 });
              return { fav: st.fav, beatsDone: st.beatsDone };
            }""")
            seen, rendered, odays = try_days(pg, ["金龍茶餐廳"], list(range(1066, 1072)), {"liu_bingxing_shy.webp"}, "b5a_clash")
            LOG["phases"]["b5a_clash"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["b5a_clash"] = rendered
            LOG["seen"] = sorted(set(LOG["seen"]) | seen)
            missing = set(REMAIN) - set(LOG["seen"])
            print("  missing now:", sorted(missing))
        # B5b：Chung farewell（1992 秋）
        if "chung_choning_think.webp" in missing:
            print("== b5b_chung_farewell ==")
            new_game(pg)
            seen, rendered, odays = try_days(pg, ["天星音樂"], [608], {"chung_choning_think.webp"}, "b5b_meet")
            LOG["rendered"]["b5b_meet"] = rendered
            LOG["seen"] = sorted(set(LOG["seen"]) | seen)
            pg.evaluate("""() => {
              S.stars = S.stars || {};
              const st = S.stars.chung_choning || (S.stars.chung_choning = {});
              st.met = true; st.fav = 30;
              st.beatsDone = Object.assign({}, st.beatsDone, { chung_review: 1, chung_intel: 1 });
              return { fav: st.fav, beatsDone: st.beatsDone };
            }""")
            seen, rendered, odays = try_days(pg, ["天星音樂"], list(range(1000, 1006)), {"chung_choning_think.webp"}, "b5b_farewell")
            LOG["phases"]["b5b_farewell"] = {"seen": sorted(seen), "overlay_days": odays}
            LOG["rendered"]["b5b_farewell"] = rendered
            LOG["seen"] = sorted(set(LOG["seen"]) | seen)
            missing = set(REMAIN) - set(LOG["seen"])
            print("  missing now:", sorted(missing))
        # B6：掃場（awi 目標）
        if missing & {"awi_s2_surprise.webp", "awi_s2_sad.webp", "awi_s2_shy.webp",
                      "awi_s3_surprise.webp", "awi_s3_sad.webp", "awi_s3_shy.webp"}:
            for tag, nl, fame, loc in [
                ("b6_luk_t2", 1, 0, ["獅子山製片"]),
                ("b6_mak_t2", 1, 0, ["紅棉影業"]),
                ("b6_yip_t2", 1, 0, ["香江唱片"]),
                ("b6_gu_t2", 1, 0, ["海港廣播"]),
                ("b6_ngai_t2", 1, 0, ["維港電影"]),
                ("b6_luk_t3", 3, 70, ["獅子山製片"]),
                ("b6_mak_t3", 3, 70, ["紅棉影業"]),
            ]:
                if not (missing & {"awi_s2_surprise.webp", "awi_s2_sad.webp", "awi_s2_shy.webp",
                                   "awi_s3_surprise.webp", "awi_s3_sad.webp", "awi_s3_shy.webp"}):
                    break
                tgts = [t for t in missing if t.startswith("awi_")]
                phase(pg, tag, nl, fame, loc, list(range(0, 5)), tgts)
                missing = set(REMAIN) - set(LOG["seen"])
                print("  missing now:", sorted(missing))
        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

LOG["PASS"] = bool(not (set(REMAIN) - set(LOG["seen"]))
                   and not LOG["target404"] and not LOG["errors"])
print("seen:", LOG["seen"])
print("missing:", sorted(set(REMAIN) - set(LOG["seen"])))
print("target404:", LOG["target404"])
print("pageerrors:", LOG["errors"][:6])
print("OVERALL PASS:", LOG["PASS"])
with open(os.path.join(HERE, "drive_log123b.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
