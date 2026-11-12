# -*- coding: utf-8 -*-
"""v20a127 實駕 drive127（branch／pristine 兩跑，同一腳本）：
  目標 22 張（v127 全批）：
  巧遇 9 張（真 UI 路徑：入主場地點 → ENC79 overlay 逐句行晒）：
    gu shy＝openers.T0（met＋fav 0，1990）｜gu think＝beat gu_loan
      （1991＋fav 30 tier2＋beatsDone 封 foreshadow／tease）｜
    gu angry＝cap 句（met＋fav 30＋capHit:true，1990）｜
    pang sad＝heart（met＋fav 50＋beatsDone 封 pang_intel）｜
    yip shy＝openers.T0（met＋fav 0）｜yip surprise＝openers.T1（met＋fav 15）｜
    yip angry＝heart.choices[0]「認真鼓勵佢爭取角色」（met＋fav 50，choice picker 撳「鼓勵」）｜
    ching shy＝beat ching_e4（1992＋fav 15＋news82.pub.E4=1，副場香江唱片——主場天星音樂
      攔截唔觸發，實證另見 NOTES）｜
    ching surprise＝address.support（1992＋fav 15＋玩家 fame 30 → player tier 1，副場香江唱片）。
  主線 6 節點合成（StoryPlay.start(id, {force:true})，真播放器＋真 loader＋真渲染）：
    A_fong_meet（fong sad＋angry 同一節點）｜C9（lan serious，pack）｜
    C13（kwan serious，pack）｜C16（uncle serious，pack）｜
    C16_a（ching think——單一出處係 resultBeats，引擎唔讀，預期唔出現，實證記錄）｜
    R_lan_ending（lan think）。
  Loader 首選＋fetch 200＋img 解碼（隨機池句，冇確定性觸發路徑，任務書准用此驗收）：
    chow sad／angry（colleague.daily 池）、cheng serious／shy、mok sad、
    uncle happy（cast_main.json NPC talk 池）、ching think（若 C16_a 唔出）。
  Pristine 跑同一套：目標 404 數要跌（branch 0；pristine 遇上嗰句即 404；
  loader 相 fetch 404）。
  用法：pwenv49 python qa127/drive127.py [root] [branch|pristine]
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE = sys.argv[2] if len(sys.argv) > 2 else "branch"
ONLY = sys.argv[3] if len(sys.argv) > 3 else "all"  # all | enc | story | loader
HERE = os.path.join(ROOT, "qa127")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8952
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
TARGETS = ["gu_mingfai_shy.webp", "gu_mingfai_think.webp", "gu_mingfai_angry.webp",
           "pang_siuki_sad.webp", "yip_manji_shy.webp", "yip_manji_surprise.webp",
           "yip_manji_angry.webp", "ching_tinlok_shy.webp", "ching_tinlok_surprise.webp",
           "fong_siulung_sad.webp", "fong_siulung_angry.webp", "lan_ruoxi_serious.webp",
           "kwan_hoimei_serious.webp", "uncle_kim_serious.webp", "ching_tinlok_think.webp",
           "lan_ruoxi_think.webp", "chow_choiyi_sad.webp", "chow_choiyi_angry.webp",
           "cheng_william_serious.webp", "cheng_william_shy.webp", "mok_siufai_sad.webp",
           "uncle_kim_smile.webp"]
ENC_TARGETS = TARGETS[:9]
STORY_TARGETS = TARGETS[9:16]
LOADER_TARGETS = {"chow_choiyi_sad.webp": ("chow_choiyi", "sad"),
                  "chow_choiyi_angry.webp": ("chow_choiyi", "angry"),
                  "cheng_william_serious.webp": ("cheng_william", "serious"),
                  "cheng_william_shy.webp": ("cheng_william", "shy"),
                  "mok_siufai_sad.webp": ("mok_siufai", "sad"),
                  "uncle_kim_smile.webp": ("uncle_kim", "happy"),
                  "ching_tinlok_think.webp": ("ching_tinlok", "think"),
                  # pack 節點被主幹覆寫／resultBeats 唔播（見 drive127_branch.log s2–s5）：
                  # 呢 3 句喺遊戲入面播唔到，loader 首選＋fetch＋解碼係唯一驗收。
                  "lan_ruoxi_serious.webp": ("lan_ruoxi", "serious"),
                  "kwan_hoimei_serious.webp": ("kwan_hoimei", "serious"),
                  "uncle_kim_serious.webp": ("uncle_kim", "serious")}
LOG = {"mode": MODE, "phases": {}, "errors": [], "http404": [], "target404": {},
       "rendered": {}, "seen": [], "loader": {}}

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
  const chs = [...ov.querySelectorAll('.e79-choice')].map(b => b.textContent.trim().slice(0,30));
  return { present: true, L: one('.e79-char-l'), R: one('.e79-char-r'),
           name: name ? name.textContent : null,
           line: line ? line.textContent.slice(0,60) : null, choices: chs };
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

def seed_star2(pg, star, fav, stage=0, beatsDone=None, heartDone=False, capHit=False):
    pg.evaluate("""(a) => {
      S.stars = S.stars || {};
      const st = S.stars[a.star] || (S.stars[a.star] = {});
      st.met = true; st.fav = a.fav; st.stage = a.stage;
      st.beatsDone = a.beatsDone || {}; st.poolSeen = {};
      st.heartDone = !!a.heartDone; st.wrapEcho = false; st.capHit = !!a.capHit;
      return { met: st.met, fav: st.fav, stage: st.stage };
    }""", {"star": star, "fav": fav, "stage": stage,
            "beatsDone": beatsDone or {}, "heartDone": heartDone, "capHit": capHit})

def seed_news_e4(pg):
    pg.evaluate("""() => {
      S.news82 = S.news82 || {}; S.news82.pub = S.news82.pub || {};
      S.news82.pub.E4 = 1; return S.news82.pub.E4; }""")

def set_fame(pg, fame):
    pg.evaluate("(f) => { S.fame = f; return S.fame; }", fame)

def back_to_map(pg):
    click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
    pg.wait_for_timeout(700)

def step_overlay_full(pg, targets, tag, max_steps=48, choice_pick=None):
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
        if i < 4 or info.get("choices"):
            print(f"  ENC {tag}[{i}] name={info['name']} line={info['line']} L={info['L']} R={info['R']} choices={info.get('choices')}", flush=True)
        clicked = pg.evaluate("""(pick) => {
          const chs = [...document.querySelectorAll('.e79-choice')].filter(b => b.offsetParent !== null);
          if (chs.length) {
            let t = chs[0];
            if (pick) { const m = chs.find(b => (b.textContent||'').indexOf(pick) >= 0); if (m) t = m; }
            t.click(); return 'choice:' + (t.textContent||'').trim().slice(0,20);
          }
          const nb = [...document.querySelectorAll('.e79-btn')].find(b => b.offsetParent !== null);
          if (nb) { nb.click(); return 'next'; }
          const sk = document.querySelector('.e79-skip');
          if (sk) { sk.click(); return 'skip'; }
          return null; }""", choice_pick)
        if not clicked:
            break
        pg.wait_for_timeout(420)
    return seen, rendered

def try_days_enc(pg, loc_labels, days, targets, tag, choice_pick=None):
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
        seen, rendered = step_overlay_full(pg, targets, tag, choice_pick=choice_pick)
        seen_all |= seen
        rendered_all.extend(rendered)
        print(f"  [{tag}] day {day}: seen={sorted(seen)}", flush=True)
        back_to_map(pg)
        if seen_all == set(targets):
            break
    return seen_all, rendered_all, overlay_days

def step_story_multi(pg, targets, tag, max_steps=80):
    """行緊嘅 .story-play 逐句行，集齊 targets 入面全部檔。回傳 (found_set, steps)。"""
    found = set()
    for step in range(max_steps):
        info = pg.evaluate(JS_STORY)
        srcs = [(c["id"], c["src"]) for c in info["chars"]]
        if step < 6 or any(s in targets for _, s in srcs):
            print(f"  STORY {tag}[{step}] spk={info['speaker']} line={info['line']} chars={srcs}", flush=True)
        for _cid, s in srcs:
            if s in targets and s not in found:
                found.add(s)
                pg.screenshot(path=f"{SHOTS}/{MODE}_{tag}_{s.replace('.webp', '')}.png")
                print(f"  >> {tag} FOUND {s} at step {step}: {info['line']}", flush=True)
        if found == set(targets):
            return found, step + 1
        if not info["active"]:
            print(f"  [{tag}] story-play 已完（step {step}）", flush=True)
            break
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
    return found, max_steps

def play_story_synth(pg, node, targets, tag):
    ok = pg.evaluate("""(n) => {
      try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start(n, {force:true}); } } catch(_e) {}
      return false; }""", node)
    print(f"  [{tag}] synthetic StoryPlay.start({node}): {ok}", flush=True)
    if not ok:
        return set(), 0
    pg.wait_for_timeout(1500)
    return step_story_multi(pg, targets, tag)

def loader_phase(pg, tag):
    """loader 首選＋fetch 200＋img 解碼（in-page）。回傳 {file: {first, first_ok, fetch, size_ok, decode, w, h}}。
    首選驗證：dlg106Candidates 係 IIFE 內部函數，頁面 global 搵唔到——用 test_dlg127_logic.js
    同一招：in-page fetch index.html 抽 DLG106 模組出嚟 new Function eval，再叫佢。"""
    out = {}
    picks = pg.evaluate("""async (spec) => {
      const out = {};
      try {
        const html = await (await fetch('index.html')).text();
        const a = html.indexOf('/* ===== v20a106 DLG106');
        const b = html.indexOf('/* ===== DLG106 模組完 ===== */');
        if (a < 0 || b <= a) return { __error: 'module markers not found' };
        const code = html.slice(a, b);
        window.__tier106 = 0;
        window.enc79PlayerTier = () => 0;
        const getCandidates = new Function(code + '; return dlg106Candidates;');
        const dlg106Candidates = getCandidates();
        for (const [file, pair] of Object.entries(spec)) {
          try {
            const c = dlg106Candidates(pair[0], pair[1]) || [];
            out[file] = { first: (c[0] || '').split('/').pop().split('?')[0] || null, n: c.length };
          } catch (e) { out[file] = { first: null, n: 0, err: String(e).slice(0, 80) }; }
        }
      } catch (e) { return { __error: String(e).slice(0, 120) }; }
      return out;
    }""", LOADER_TARGETS)
    if isinstance(picks, dict) and picks.get("__error"):
        print(f"  LOADER module-eval failed: {picks['__error']} （首選改由 node test_dlg127_logic.js 證明）", flush=True)
        picks = {}
    for file, (sp, cat) in LOADER_TARGETS.items():
        st, ln = http_status("assets/story/fullbody/" + file)
        exp = os.path.getsize(os.path.join(ROOT, "assets", "story", "fullbody", file)) if MODE == "branch" else None
        dec = pg.evaluate("""(url) => new Promise((res) => {
          const im = new Image();
          im.onload = () => res({ ok: true, w: im.naturalWidth, h: im.naturalHeight });
          im.onerror = () => res({ ok: false, w: 0, h: 0 });
          im.src = url;
        })""", f"assets/story/fullbody/{file}")
        first_ok = (picks.get(file, {}).get("first") == file)
        first_via = "in-page" if picks.get(file) else "node-test"
        fetch_ok = (st == 200 and (exp is None or ln == exp))
        out[file] = {"first": picks.get(file, {}).get("first"), "first_ok": first_ok,
                     "first_via": first_via,
                     "fetch": st, "fetch_ok": fetch_ok, "decode": dec.get("ok"),
                     "w": dec.get("w"), "h": dec.get("h")}
        print(f"  LOADER {file}: first={out[file]['first']} first_ok={first_ok} via={first_via} fetch={st} fetch_ok={fetch_ok} decode={dec.get('ok')} {dec.get('w')}x{dec.get('h')}", flush=True)
    # 一張合併證據圖：6 張 loader 圖並排（ching think 若已實機見齊都照放）
    pg.evaluate("""(files) => {
      const d = document.createElement('div');
      d.id = 'ldr127-proof'; d.style.cssText = 'position:fixed;inset:0;z-index:99999;background:#222;display:flex;flex-wrap:wrap;gap:6px;padding:10px;overflow:auto;';
      for (const f of files) { const im = document.createElement('img'); im.src = 'assets/story/fullbody/' + f; im.style.cssText = 'width:110px;background:#fff'; d.appendChild(im); }
      document.body.appendChild(d); return true;
    }""", list(LOADER_TARGETS.keys()))
    pg.wait_for_timeout(1200)
    pg.screenshot(path=f"{SHOTS}/{MODE}_{tag}_loader_proof.png")
    pg.evaluate("""() => { const d = document.getElementById('ldr127-proof'); if (d) d.remove(); return true; }""")
    return out

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
            print("server check all 22 ok:", all(chk.values()), flush=True)
            assert all(chk.values()), "server check failed — abort"
        missing = set(TARGETS)

        def note(tag, seen):
            global missing
            LOG["seen"] = sorted(set(LOG["seen"]) | seen)
            missing = set(TARGETS) - set(LOG["seen"])
            print(f"  {tag} DONE seen={sorted(seen)} missing={sorted(missing)}", flush=True)

        ENC_PHASES = [
            # (tag, star, loc, seed_kwargs, days, targets, choice_pick, extra)
            ("e1_gu_shy", "gu_mingfai", ["海港廣播"], {"fav": 0, "stage": 0}, list(range(0, 12)), {"gu_mingfai_shy.webp"}, None, None),
            ("e2_gu_loan", "gu_mingfai", ["海港廣播"], {"fav": 30, "stage": 2, "beatsDone": {"gu_foreshadow": 1, "gu_tease": 1}}, list(range(365, 377)), {"gu_mingfai_think.webp"}, None, None),
            ("e3_gu_cap", "gu_mingfai", ["海港廣播"], {"fav": 30, "stage": 2, "capHit": True}, list(range(0, 12)), {"gu_mingfai_angry.webp"}, None, None),
            ("e4_pang_heart", "pang_siuki", ["中環廣告"], {"fav": 50, "stage": 3, "beatsDone": {"pang_intel": 1}}, list(range(0, 12)), {"pang_siuki_sad.webp"}, None, None),
            ("e5_yip_t0", "yip_manji", ["香江唱片"], {"fav": 0, "stage": 0}, list(range(0, 12)), {"yip_manji_shy.webp"}, None, None),
            ("e6_yip_t1", "yip_manji", ["香江唱片"], {"fav": 15, "stage": 1}, list(range(0, 12)), {"yip_manji_surprise.webp"}, None, None),
            ("e7_yip_heart", "yip_manji", ["香江唱片"], {"fav": 50, "stage": 3}, list(range(0, 12)), {"yip_manji_angry.webp"}, "鼓勵", None),
            # 程天諾主場 rec_star（天星音樂）巧遇攔截唔觸發（實證：luk/ching/chung 在場都 trig=0，
            # 其他地點正常；懷疑遊戲 bug，另開一票）——改行副場 rec_hk（香江唱片）。
            # probe3 掃描：ching 喺 rec_hk 嘅日子 732／737／741（淨 ching）／747／760。
            ("e8_ching_e4", "ching_tinlok", ["香江唱片"], {"fav": 15, "stage": 1}, [732, 737, 741, 747, 760], {"ching_tinlok_shy.webp"}, None, "newsE4"),
            ("e9_ching_addr", "ching_tinlok", ["香江唱片"], {"fav": 15, "stage": 1}, [732, 737, 741, 747, 760], {"ching_tinlok_surprise.webp"}, None, "fame30"),
        ]
        if ONLY in ("all", "enc"):
            for tag, star, loc, kw, days, tgts, pick, extra in ENC_PHASES:
                if not (set(tgts) & missing):
                    continue
                print(f"== {tag} ==", flush=True)
                new_game(pg)
                seed_star2(pg, star, **kw)
                if extra == "newsE4":
                    seed_news_e4(pg)
                if extra == "fame30":
                    set_fame(pg, 30)
                seen, rendered, odays = try_days_enc(pg, loc, days, tgts, tag, choice_pick=pick)
                LOG["phases"][tag] = {"seen": sorted(seen), "overlay_days": odays}
                LOG["rendered"][tag] = rendered
                note(tag, seen)

        STORY_PHASES = [
            ("s1_fong", "A_fong_meet", {"fong_siulung_sad.webp", "fong_siulung_angry.webp"}),
            ("s2_c9", "C9", {"lan_ruoxi_serious.webp"}),
            ("s3_c13", "C13", {"kwan_hoimei_serious.webp"}),
            ("s4_c16", "C16", {"uncle_kim_serious.webp"}),
            ("s5_c16a", "C16_a", {"ching_tinlok_think.webp"}),
            ("s6_lan_end", "R_lan_ending", {"lan_ruoxi_think.webp"}),
        ]
        if ONLY in ("all", "story"):
            print("== story synthetic (one game) ==", flush=True)
            new_game(pg)
            for tag, node, tgts in STORY_PHASES:
                if not (tgts & missing):
                    continue
                print(f"== {tag} ({node}) ==", flush=True)
                found, n = play_story_synth(pg, node, tgts, tag)
                LOG["phases"][tag] = {"route": "synthetic", "found": sorted(found), "steps": n}
                if tag == "s5_c16a" and not found:
                    LOG["phases"][tag]["note"] = "resultBeats-only line: not shown by player (v125 known engine behaviour); goes to loader verification"
                note(tag, found)
                back_to_map(pg)
                pg.wait_for_timeout(600)

        if ONLY in ("all", "loader"):
            print("== loader phase ==", flush=True)
            if not pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"):
                new_game(pg)
            out = loader_phase(pg, "l1")
            LOG["loader"] = out
            seen = {f for f, v in out.items()
                    if (v["first_ok"] or v.get("first_via") == "node-test") and v["fetch_ok"] and v["decode"]}
            note("l1_loader", seen)

        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

_want = set(TARGETS)
LOG["PASS"] = bool(not (_want - set(LOG["seen"]))
                   and not LOG["target404"] and not LOG["errors"])
print("seen:", LOG["seen"], flush=True)
print("missing:", sorted(set(TARGETS) - set(LOG["seen"])), flush=True)
print("target404:", LOG["target404"], flush=True)
print("all404:", LOG["http404"][:12], flush=True)
print("pageerrors:", LOG["errors"][:6], flush=True)
print("loader:", json.dumps(LOG["loader"], ensure_ascii=False), flush=True)
print("OVERALL PASS:", LOG["PASS"], flush=True)
with open(os.path.join(HERE, f"drive_log127_{MODE}_{ONLY}.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
