# -*- coding: utf-8 -*-
"""v20a123 實駕：12 張新表情圖真係喺實機渲染、404 跌到零。
  A/B：pristine（main dc12744，118 張）先行同一巧遇步驟 → 計目標 URL 404；
       再換 branch（v123-expr，130 張）重行同一日種子 → 目標檔必須渲染、404 歸零。
  階段（全部 UI 入場＋逐句行巧遇 overlay，唔直叫 IIFE 內函數）：
    P1 tier 0 彭少祺＠中環廣告（day 0 起）：awi_angry＋pang_siuki_surprise
    P2 tier 2 鍾楚凝＠天星音樂（day 608 起，1991 秋窗口）：awi_s2 surprise/sad/shy＋chung think/smile
    P3 tier 3 廖炳星＠金龍茶餐廳（day 974 起，1992 秋窗口）：awi_s3 surprise/sad/shy＋liu_bingxing_shy
  額外：P1–P3 未見齊就加開不多於 4 場（Liu tier2／Pang tier3／Chung tier3，睇晒剩餘目標）。
  P7 loader 驗證（branch 頁面內）：window.DLG106.candidates 首選＋fetch 200（何生 angry 冇
       穩定實機路徑，靠呢段驗；其餘 11 張以渲染為主、loader 為輔）。
  390×844、Playwright、可棄用槽 3。PASS：11 張渲染見齊＋ho loader/fetch OK＋branch 目標 404＝0
  ＋pristine 目標 404＞0＋0 pageerror。
用法：pwenv49 python qa123/drive123.py
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRISTINE = "/home/hatch/workspace/linji-pristine123"
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8951
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
NEW = ["awi_s2_surprise.webp", "awi_s2_sad.webp", "awi_s2_shy.webp",
       "awi_s3_surprise.webp", "awi_s3_sad.webp", "awi_s3_shy.webp",
       "awi_angry.webp", "chung_choning_think.webp", "chung_choning_smile.webp",
       "ho_sang_angry.webp", "liu_bingxing_shy.webp", "pang_siuki_surprise.webp"]
NEW_BYTES = {n: os.path.getsize(os.path.join(ROOT, "assets", "story", "fullbody", n)) for n in NEW}
LOG = {"phases": {}, "errors": [], "http404": [], "target404": {"pristine": {}, "branch": {}},
       "rendered": {"pristine": {}, "branch": {}}, "loader": {}, "server": {}}

def http_status(path):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{path}", timeout=5) as r:
            return r.status, len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, 0
    except Exception as e:
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
        raise RuntimeError(f"served index mismatch: status={st} sha={sha[:12]} expected={exp[:12]} (wrong dir/port collision?)")
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
    return { src: (im.getAttribute('src')||'').split('/').pop().split('?')[0],
             filter: im.style.filter }; };
  const name = ov.querySelector('.e79-name'); const line = ov.querySelector('.e79-line');
  return { present: true, L: one('.e79-char-l'), R: one('.e79-char-r'),
           name: name ? name.textContent : null,
           line: line ? line.textContent.slice(0,60) : null,
           hasChoice: !!ov.querySelector('.e79-choice') };
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
    r = pg.evaluate("""(arg) => {
      const leads = (typeof GIGS !== 'undefined' ? GIGS : [])
        .filter(g => g && /lead/.test(String(g.roleScale || ''))).slice(0, 3).map(g => g.id);
      S.flags = S.flags || {};
      for (let i = 0; i < arg.n; i++) S.flags['done_' + leads[i]] = 1;
      if (arg.fame) S.fame = arg.fame;
      return { leads };
    }""", {"n": n_lead, "fame": fame})
    exp = 3 if (n_lead >= 3 and fame >= 70) else (2 if n_lead >= 1 else 0)
    return exp

def back_to_map(pg):
    click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
    pg.wait_for_timeout(700)
    return pg.evaluate("""() => [...document.querySelectorAll('button')]
      .some(b => (b.textContent || '').includes('天星音樂'))""")

def finish_encounter_if_any(pg):
    for _ in range(40):
        info = pg.evaluate(JS_ENC)
        if not info["present"]:
            return False
        clicked = pg.evaluate('''() => {
          const ch = document.querySelector('.e79-choice');
          if (ch) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          return null; }''')
        if not clicked:
            return True
        pg.wait_for_timeout(350)
    return True

def step_encounter_multi(pg, targets, tag, run, max_steps=40):
    """逐句行開緊嘅巧遇，收集 targets 入面見到嘅檔＋全部渲染過嘅 fullbody 檔。"""
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
            pg.screenshot(path=f"{SHOTS}/{run}_{tag}_{s.replace('.webp', '')}.png")
        if i < 6 or seen:
            print(f"  ENC {tag}[{i}] name={info['name']} line={info['line']} L={info['L']} R={info['R']}")
        if seen == set(targets):
            pg.screenshot(path=f"{SHOTS}/{run}_{tag}_all.png")
            break
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

def try_encounter(pg, loc_labels, star_name, days, targets, tag, run):
    """逐日入場試觸發目標星巧遇；回傳 (trigger_day, seen_set, rendered_list, tried_days)。"""
    seen_all = set()
    rendered_all = []
    tried = []
    for day in days:
        pg.evaluate("(d) => { S.dayIndex = d; }", day)
        back_to_map(pg)
        print(f"  [{tag}] try dayIndex={day} -> {loc_labels[0]}")
        opened = click_first(pg, loc_labels, 1800)
        pg.wait_for_timeout(900)
        info = pg.evaluate(JS_ENC)
        tried.append(day)
        if not info["present"]:
            print(f"  [{tag}] day {day}: 入場冇觸發巧遇")
            back_to_map(pg)
            continue
        print(f"  [{tag}] day {day}: overlay name={info['name']}")
        if star_name not in (info["name"] or ""):
            print(f"  [{tag}] day {day}: 唔係目標星（{info['name']}），行完佢再試下日")
            finish_encounter_if_any(pg)
            back_to_map(pg)
            continue
        seen, rendered = step_encounter_multi(pg, targets, tag, run)
        seen_all |= seen
        rendered_all.extend(rendered)
        print(f"  [{tag}] day {day}: seen={sorted(seen)}")
        finish_encounter_if_any(pg)
        back_to_map(pg)
        return day, seen_all, rendered_all, tried
    return None, seen_all, rendered_all, tried

def loader_check(pg, checks, run):
    """頁面內 window.DLG106.candidates 首選＋fetch 200。checks: [(sp, cat, tier, expect_file)]。
    tier 靠當前遊戲 S 狀態（awi stem 由 enc79PlayerTier 實時計），所以 checks 必須同當前 tier 夾。"""
    out = {}
    for sp, cat, tier, exp in checks:
        r = pg.evaluate("""(arg) => {
          const c = (window.DLG106 && window.DLG106.candidates)
            ? window.DLG106.candidates(arg.sp, arg.cat) : [];
          const first = c.length ? c[0] : null;
          return { first: first, file: first ? first.split('/').pop().split('?')[0] : null };
        }""", {"sp": sp, "cat": cat})
        status = None
        if r["first"]:
            try:
                status = pg.evaluate("(u) => fetch(u).then(r => r.status).catch(() => -1)", r["first"])
            except Exception:
                status = -2
        ok = (r["file"] == exp and status == 200)
        out[f"{sp}:{cat}:t{tier}"] = {"first": r["first"], "status": status, "expect": exp, "ok": ok}
        print(f"  LOADER {run} {sp} {cat} t{tier}: first={r['file']} status={status} expect={exp} {'OK' if ok else 'BAD'}")
    return out

def run_phases(pg, run):
    """P1–P3；回傳每 phase 嘅 seen。"""
    res = {}
    # P1 tier 0 Pang
    print(f"== {run} P1 tier0 Pang ==")
    ng = new_game(pg)
    print(f"  new_game: {ng}")
    t1 = {"awi_angry.webp", "pang_siuki_surprise.webp"}
    d, seen, rend, tried = try_encounter(pg, ["中環廣告"], "彭少祺", list(range(0, 10)), t1, "p1_pang", run)
    res["p1"] = {"day": d, "seen": sorted(seen), "tried": tried}
    LOG["rendered"][run].setdefault("p1", rend)
    # P2 tier 2 Chung
    print(f"== {run} P2 tier2 Chung ==")
    ng = new_game(pg)
    print(f"  new_game: {ng}")
    t2 = set_tier(pg, 1, 0)
    print(f"  set_tier -> {t2}")
    t2set = {"awi_s2_surprise.webp", "awi_s2_sad.webp", "awi_s2_shy.webp",
             "chung_choning_think.webp", "chung_choning_smile.webp"}
    d, seen, rend, tried = try_encounter(pg, ["天星音樂"], "鍾楚凝", list(range(608, 618)), t2set, "p2_chung", run)
    res["p2"] = {"day": d, "seen": sorted(seen), "tried": tried}
    LOG["rendered"][run].setdefault("p2", rend)
    # P2 loader: s2 set（當前遊戲 tier 2）
    LOG["loader"].setdefault(run, {}).update(loader_check(pg, [
        ("awi", "surprise", 2, "awi_s2_surprise.webp"),
        ("awi", "sad", 2, "awi_s2_sad.webp"),
        ("awi", "shy", 2, "awi_s2_shy.webp")], run + "_p2"))
    # P3 tier 3 Liu
    print(f"== {run} P3 tier3 Liu ==")
    ng = new_game(pg)
    print(f"  new_game: {ng}")
    t3 = set_tier(pg, 3, 70)
    print(f"  set_tier -> {t3}")
    t3set = {"awi_s3_surprise.webp", "awi_s3_sad.webp", "awi_s3_shy.webp",
             "liu_bingxing_shy.webp"}
    d, seen, rend, tried = try_encounter(pg, ["金龍茶餐廳"], "廖炳星", list(range(974, 984)), t3set, "p3_liu", run)
    res["p3"] = {"day": d, "seen": sorted(seen), "tried": tried}
    LOG["rendered"][run].setdefault("p3", rend)
    # P3 loader: s3 set（當前遊戲 tier 3）
    LOG["loader"].setdefault(run, {}).update(loader_check(pg, [
        ("awi", "surprise", 3, "awi_s3_surprise.webp"),
        ("awi", "sad", 3, "awi_s3_sad.webp"),
        ("awi", "shy", 3, "awi_s3_shy.webp")], run + "_p3"))
    return res

def extra_encounters(pg, run, missing):
    """加開場數補未見目標（上限 4 場）。missing: set of 檔名。"""
    extras = [
        ("liu", ["金龍茶餐廳"], "廖炳星", list(range(974, 979)), 1, 0),
        ("pang", ["中環廣告"], "彭少祺", list(range(10, 15)), 3, 70),
        ("chung", ["天星音樂"], "鍾楚凝", list(range(608, 613)), 3, 70),
        ("liu0", ["金龍茶餐廳"], "廖炳星", list(range(974, 979)), 0, 0),
    ]
    done = 0
    for tag, loc, star, days, n_lead, fame in extras:
        if not missing or done >= 4:
            break
        print(f"== {run} EXTRA {tag} (missing={sorted(missing)}) ==")
        ng = new_game(pg)
        t = set_tier(pg, n_lead, fame) if (n_lead or fame) else 0
        print(f"  new_game: {ng}, tier -> {t}")
        d, seen, rend, tried = try_encounter(pg, loc, star, days, set(missing), "x_" + tag, run)
        LOG["rendered"][run].setdefault("x_" + tag, rend)
        LOG["phases"][run].setdefault("extra_" + tag, {"day": d, "seen": sorted(seen), "tried": tried})
        missing -= seen
        done += 1
    return missing

srv = serve(PRISTINE)
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
                    LOG["http404"].append({"run": CURRENT_RUN[0], "file": fn, "status": resp.status})
                    if fn in NEW:
                        LOG["target404"][CURRENT_RUN[0]][fn] = LOG["target404"][CURRENT_RUN[0]].get(fn, 0) + 1
            except Exception:
                pass
        CURRENT_RUN = ["pristine"]
        pg.on("response", on_resp)
        # ---- server check: pristine 新檔必須 404、舊檔 200 ----
        st, _ = http_status("assets/story/fullbody/awi_s2_surprise.webp")
        st_old, _ = http_status("assets/story/fullbody/awi_base.webp")
        LOG["server"]["pristine"] = {"new_asset_status": st, "old_asset_status": st_old}
        print("pristine server check:", LOG["server"]["pristine"])
        assert st == 404 and st_old == 200, "pristine server check failed — abort"
        # ---- pristine run ----
        print("########## PRISTINE RUN ##########")
        LOG["phases"]["pristine"] = run_phases(pg, "pristine")
        # ---- 換 server：同一 browser/context/origin，localStorage 留低 ----
        stop(srv)
        srv = serve(ROOT)
        CURRENT_RUN[0] = "branch"
        # server check: 12 張新檔全部 200＋byte 啱
        chk = {}
        for n in NEW:
            st, ln = http_status("assets/story/fullbody/" + n)
            chk[n] = {"status": st, "bytes": ln, "expect": NEW_BYTES[n], "ok": st == 200 and ln == NEW_BYTES[n]}
        LOG["server"]["branch"] = chk
        print("branch server check: all ok =", all(v["ok"] for v in chk.values()))
        assert all(v["ok"] for v in chk.values()), "branch server check failed — abort"
        # ---- branch run ----
        print("########## BRANCH RUN ##########")
        LOG["phases"]["branch"] = run_phases(pg, "branch")
        # loader: tier 0 組（開個 tier 0 新遊戲）
        print("== branch loader tier0 ==")
        new_game(pg)
        LOG["loader"].setdefault("branch", {}).update(loader_check(pg, [
            ("awi", "angry", 0, "awi_angry.webp"),
            ("chung_choning", "think", 0, "chung_choning_think.webp"),
            ("chung_choning", "happy", 0, "chung_choning_smile.webp"),
            ("ho_sang", "angry", 0, "ho_sang_angry.webp"),
            ("liu_bingxing", "shy", 0, "liu_bingxing_shy.webp"),
            ("pang_siuki", "surprise", 0, "pang_siuki_surprise.webp")], "branch_t0"))
        # ---- extras：補未見目標 ----
        seen_branch = set()
        for ph in ("p1", "p2", "p3"):
            seen_branch |= set(LOG["phases"]["branch"].get(ph, {}).get("seen", []))
        missing = (set(NEW) - {"ho_sang_angry.webp"}) - seen_branch
        print("branch missing after P1-P3:", sorted(missing))
        if missing:
            missing = extra_encounters(pg, "branch", missing)
            print("branch missing after extras:", sorted(missing))
        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

seen_branch = set()
for ph in ("p1", "p2", "p3"):
    seen_branch |= set(LOG["phases"]["branch"].get(ph, {}).get("seen", []))
for k, v in LOG["phases"]["branch"].items():
    if k.startswith("extra_"):
        seen_branch |= set(v.get("seen", []))
loader_ok = all(v.get("ok") for v in LOG["loader"].get("branch", {}).values())
branch_404 = sum(LOG["target404"]["branch"].values())
pristine_404 = sum(LOG["target404"]["pristine"].values())
render_targets = set(NEW) - {"ho_sang_angry.webp"}
LOG["PASS"] = bool(render_targets <= seen_branch
                   and loader_ok
                   and branch_404 == 0
                   and pristine_404 > 0
                   and not LOG["errors"])
print("seen_branch:", sorted(seen_branch))
print("missing render targets:", sorted(render_targets - seen_branch))
print("loader all ok:", loader_ok)
print("target404 pristine:", pristine_404, "branch:", branch_404)
print("pageerrors:", LOG["errors"][:6])
print("OVERALL PASS:", LOG["PASS"])
with open(os.path.join(HERE, "drive_log123.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
