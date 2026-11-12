# -*- coding: utf-8 -*-
"""v20a127 targeted re-drive（drive127b）：10 張 loader-only 圖嘅逐張阻塞實證。
任務書要求：loader-only 圖要喺場景真渲染見齊先可以報「見齊」。呢個 drive
逐張驗佢哋有冇真渲染路徑——預期結論係 10 張全部喺現行引擎下播唔到，
每張阻塞原因唔同，全部有代碼＋實機雙重證據（見 NOTES_V20A127）：
  T1 傾談分流：5 句 chow 句只會喺 colleague／rival／director 傾談池出現，
     reporter 永遠抽唔到；傾談 modal 用 PORTRAITS 靜態 bust，唔行 dlg106 loader。
  T2 C16_a 抉擇：揀「靠修音」後只出 effects.notes，resultBeats 程天諾句唔出現
     （applyChoice 從來唔讀 resultBeats）。
  T3 pack 覆寫：C9／C13／C16 播出嘅係 LIVE 版，pack 獨有句（lan／kwan／uncle
     serious）唔出現（新基底 4f4b96a 再確認）。
  T4 loader 再證：10 張喺新基底上首選＋fetch 200＋解碼。
  T5 cast_main 死檔：全程 performance entries 冇 cast_main.json；代碼 0 引用。
用法：pwenv49 python qa127/drive127b.py [root]（預設工作副本；branch only）
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "qa127")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8953
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1"
LOG = {"drive": "127b", "base": "4f4b96a", "phases": {}, "errors": [], "http404": [], "target404": {}}
LOADER10 = {"chow_choiyi_sad.webp": ("chow_choiyi", "sad"),
            "chow_choiyi_angry.webp": ("chow_choiyi", "angry"),
            "cheng_william_serious.webp": ("cheng_william", "serious"),
            "cheng_william_shy.webp": ("cheng_william", "shy"),
            "mok_siufai_sad.webp": ("mok_siufai", "sad"),
            "uncle_kim_smile.webp": ("uncle_kim", "happy"),
            "ching_tinlok_think.webp": ("ching_tinlok", "think"),
            "lan_ruoxi_serious.webp": ("lan_ruoxi", "serious"),
            "kwan_hoimei_serious.webp": ("kwan_hoimei", "serious"),
            "uncle_kim_serious.webp": ("uncle_kim", "serious")}
TALK_TARGETS = {
    "chow_angry#1": "我前幾日喺清水灣嗰組做嘢，氣氛幾好，副導又唔會亂鬧人，新人去嗰邊撞下，學到嘢又唔使捱得咁辛苦。",
    "chow_angry#2": "你嚟試鏡，唔好背到滾瓜爛熟就算，留返少少即場反應畀我睇，我想知你聽到新指示，識唔識得即刻變。",
    "chow_sad#1": "陸柏言嗰場戲，佢明明背熟晒對白，但一埋位就停咗兩停，導演冇鬧，仲叫大家抖下先，可能佢真係好攰。",
    "chow_sad#2": "呢份工我睇過，唔啱我做，漏畀你算啦：嗰組缺個肯捱夜嘅後生，你肯頂，入去就有位，唔好講我益你。",
    "chow_sad#3": "嗰個組而家四圍搵人，唔係冇人，係之前嗰個走咗佬，你有本事補到位，導演點都會記得你呢份人情。",
}

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
        raise RuntimeError("http.server died on start")
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

def step_story_multi(pg, targets, tag, max_steps=80):
    found = set()
    for step in range(max_steps):
        info = pg.evaluate(JS_STORY)
        srcs = [(c["id"], c["src"]) for c in info["chars"]]
        if step < 6 or any(s in targets for _, s in srcs):
            print(f"  STORY {tag}[{step}] spk={info['speaker']} line={info['line']} chars={srcs}", flush=True)
        for _cid, s in srcs:
            if s in targets and s not in found:
                found.add(s)
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
    }""", LOADER10)
    if isinstance(picks, dict) and picks.get("__error"):
        print(f"  LOADER module-eval failed: {picks['__error']}", flush=True)
        picks = {}
    for file, (sp, cat) in LOADER10.items():
        st, ln = http_status("assets/story/fullbody/" + file)
        exp = os.path.getsize(os.path.join(ROOT, "assets", "story", "fullbody", file))
        dec = pg.evaluate("""(url) => new Promise((res) => {
          const im = new Image();
          im.onload = () => res({ ok: true, w: im.naturalWidth, h: im.naturalHeight });
          im.onerror = () => res({ ok: false, w: 0, h: 0 });
          im.src = url;
        })""", f"assets/story/fullbody/{file}")
        first_ok = (picks.get(file, {}).get("first") == file)
        first_via = "in-page" if picks.get(file) else "node-test"
        fetch_ok = (st == 200 and ln == exp)
        out[file] = {"first": picks.get(file, {}).get("first"), "first_ok": first_ok,
                     "first_via": first_via,
                     "fetch": st, "fetch_ok": fetch_ok, "decode": dec.get("ok"),
                     "w": dec.get("w"), "h": dec.get("h")}
        print(f"  LOADER {file}: first={out[file]['first']} first_ok={first_ok} via={first_via} fetch={st} fetch_ok={fetch_ok} decode={dec.get('ok')} {dec.get('w')}x{dec.get('h')}", flush=True)
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
                    if fn in LOADER10:
                        LOG["target404"][fn] = LOG["target404"].get(fn, 0) + 1
            except Exception:
                pass
        pg.on("response", on_resp)

        print("== T1 talk routing tally ==", flush=True)
        new_game(pg)
        pg.wait_for_timeout(4000)  # 等 content packs 載入（NPC_LINES 換 disk 版）
        t1 = pg.evaluate("""(spec) => {
          const out = {};
          const ids = ['colleague', 'rival', 'director', 'reporter', 'agent'];
          for (const id of ids) {
            try { S.npcs = S.npcs || {}; S.npcs[id] = 100; } catch(_e) {}
            try { S.stress = 0; } catch(_e) {}
            const hits = {};
            for (const k of Object.keys(spec)) hits[k] = 0;
            let total = 0, distinct = new Set();
            for (let i = 0; i < 600; i++) {
              let t = '';
              try { t = pickNpcLine(id, {}) || ''; } catch(_e) { t = ''; }
              if (!t) continue;
              total++;
              distinct.add(t);
              for (const [k, line] of Object.entries(spec)) {
                if (t === line) hits[k]++;
              }
            }
            let face = null;
            try { face = (typeof PORTRAITS !== 'undefined' && NPCS[id]) ? (PORTRAITS[NPCS[id].face] || null) : null; } catch(_e) {}
            out[id] = { draws: total, distinct: distinct.size, hits, portrait: face,
                        name: (typeof NPCS !== 'undefined' && NPCS[id]) ? NPCS[id].name : null };
          }
          return out;
        }""", TALK_TARGETS)
        for nid, r in t1.items():
            print(f"  T1 {nid}（{r['name']}）：抽 {r['draws']} 次／{r['distinct']} 句唔同｜"
                  f"目標句命中 {r['hits']}｜portrait={r['portrait']}", flush=True)
        LOG["phases"]["T1_talk_routing"] = t1

        print("== T2 C16_a choice (resultBeats) ==", flush=True)
        ok = pg.evaluate("""() => {
          try { if (typeof StoryPlay !== 'undefined' && StoryPlay.start) { return !!StoryPlay.start('C16', {force:true}); } } catch(_e) {}
          return false; }""")
        print(f"  [T2] StoryPlay.start(C16): {ok}", flush=True)
        pg.wait_for_timeout(1500)
        picked = None
        for step in range(60):
            info = pg.evaluate(JS_STORY)
            if step < 3:
                print(f"  STORY T2[{step}] spk={info['speaker']} line={info['line']} choices={info['choices']}", flush=True)
            if info["choices"]:
                # 揀「靠修音」嗰個（C16_a）；若唔見就揀第一個並記錄
                got = click_first(pg, ["靠修音"], 1500)
                picked = got or click_first(pg, [info["choices"][0][:6]], 1500)
                print(f"  [T2] picked choice: {picked}", flush=True)
                pg.wait_for_timeout(1500)
                break
            clicked = pg.evaluate("""() => { const row = document.getElementById('modal-btns');
              if (!row) return false; const bs = [...row.querySelectorAll('button')].filter(x => x.offsetParent !== null && !x.disabled);
              if (!bs.length) return false; bs[0].click(); return true; }""")
            if not clicked:
                print(f"  [T2] 冇下一句掣，停（step {step}）", flush=True)
                break
            pg.wait_for_timeout(500)
        # 抉擇後畫面文字：撳埋確認掣（如有），再 dump 全文
        for _ in range(4):
            if not click_first(pg, ["確定", "確認", "好", "知道了", "繼續"], 900):
                break
        pg.wait_for_timeout(800)
        body_text = pg.evaluate("() => document.body.innerText.slice(0, 1800)")
        t2 = {"picked": picked,
              "notes_present": "你揀咗快嗰條路" in body_text,
              "resultbeats_present": "佢喺鏡入面望咗你一陣" in body_text,
              "body_head": body_text[:600]}
        print(f"  T2 picked={picked} effects.notes 現身：{t2['notes_present']} "
              f"resultBeats 程天諾句現身：{t2['resultbeats_present']}", flush=True)
        print(f"  T2 body head: {t2['body_head'][:300]!r}", flush=True)
        pg.screenshot(path=f"{SHOTS}/branch_T2_c16a_result.png")
        LOG["phases"]["T2_c16a_choice"] = t2

        print("== T3 pack overwrite re-confirm (new base) ==", flush=True)
        for tag, node, tgts in [("t3_c9", "C9", {"lan_ruoxi_serious.webp"}),
                                ("t3_c13", "C13", {"kwan_hoimei_serious.webp"}),
                                ("t3_c16", "C16", {"uncle_kim_serious.webp"})]:
            print(f"== {tag} ({node}) ==", flush=True)
            found, n = play_story_synth(pg, node, tgts, tag)
            LOG["phases"][tag] = {"found": sorted(found), "steps": n}
            print(f"  {tag} DONE found={sorted(found)}（預期 []：pack 句播唔到）", flush=True)
            click_first(pg, ["返回地圖", "返地圖", "關閉"], 900)
            pg.wait_for_timeout(600)

        print("== T4 loader re-proof (new base, 10) ==", flush=True)
        out = loader_phase(pg, "t4")
        LOG["loader"] = out
        seen10 = {f for f, v in out.items() if v["first_ok"] and v["fetch_ok"] and v["decode"]}
        print(f"  T4 loader 10/10: {len(seen10) == 10} seen={sorted(seen10)}", flush=True)
        LOG["phases"]["T4_loader"] = {"seen10": sorted(seen10)}

        print("== T5 cast_main fetch check ==", flush=True)
        t5 = pg.evaluate("""() => {
          const names = performance.getEntriesByType('resource').map(e => e.name);
          return { total: names.length,
                   cast_main: names.filter(n => n.includes('cast_main')),
                   story_detail: names.filter(n => n.includes('story_detail_c1_to_c17')).length,
                   npc_lines: names.filter(n => n.includes('npc_lines_core')).length };
        }""")
        print(f"  T5 resource entries={t5['total']} cast_main fetches={t5['cast_main']} "
              f"story_detail={t5['story_detail']} npc_lines_core={t5['npc_lines']}", flush=True)
        LOG["phases"]["T5_cast_main"] = t5

        LOG["errors"] += errs
        b.close()
finally:
    stop(srv)

print("target404:", LOG["target404"], flush=True)
print("all404:", LOG["http404"][:12], flush=True)
print("pageerrors:", LOG["errors"][:6], flush=True)
print("loader10:", json.dumps(LOG.get("loader", {}), ensure_ascii=False)[:400], flush=True)
with open(os.path.join(HERE, "drive_log127b_branch.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print("DONE")
