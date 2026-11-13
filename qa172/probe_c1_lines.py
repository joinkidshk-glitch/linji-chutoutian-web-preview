# -*- coding: utf-8 -*-
"""Probe：C1 句數之謎——dump live／soft 下 C1 播放期間見到嘅每一句（speaker＋text），
對照節點數據 beats／lines 總數。只係探針，唔計分。"""
import subprocess, time, os, hashlib, urllib.request, json
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work172"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8997

def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
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
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

def story_state(pg):
    return pg.evaluate("""() => {
      const plate = document.querySelector('.story-play .dlg106-plate');
      const line = plate ? plate.querySelector('.sp-line') : null;
      const spk = plate ? plate.querySelector('.sp-speaker') : null;
      const ch = [...document.querySelectorAll('.sp-choice')].filter(e => e.offsetParent !== null)
        .map(c => (c.textContent||'').trim().slice(0,30));
      return {active: !!plate, speaker: spk ? spk.textContent : null,
        text: line ? line.textContent : null, choices: ch}; }""")

def play_dump(pg):
    seen = []
    for _ in range(200):
        st = story_state(pg)
        if st["active"] and st["text"]:
            key = (st["speaker"], st["text"])
            if not seen or seen[-1] != key:
                seen.append(key)
        if st["choices"]:
            # 撳第一個抉擇，記低
            pg.evaluate("""() => { const cs=[...document.querySelectorAll('.sp-choice')].filter(e=>e.offsetParent!==null);
              if(cs.length) cs[0].click(); }""")
            seen.append(("CHOICE-CLICKED", st["choices"][0]))
            pg.wait_for_timeout(800); continue
        if click_vis(pg, "下一句"):
            continue
        mask_on = pg.evaluate("() => { const m = document.getElementById('mask'); return !!m && m.classList.contains('on'); }")
        if mask_on and click_vis(pg, "關閉"):
            continue
        if vis_btn(pg, "過一日") and not mask_on:
            break
        pg.wait_for_timeout(700)
    return seen

def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            for query, tag in [("", "LIVE"), ("?softPreview=1", "SOFT")]:
                br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
                pg = br.new_page(viewport={"width": 430, "height": 932})
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                print("=== ", tag, "new_game:", new_game(pg, query), flush=True)
                node = pg.evaluate("""() => { try {
                  const n = StoryOC.findNodeRaw('C1');
                  const beats = (n && n.beats) || [];
                  let lines = 0; beats.forEach(b => { lines += ((b.lines||[]).length); });
                  return {beats: beats.length, lines: lines,
                    beatLines: beats.map(b => (b.lines||[]).length)};
                } catch(e){ return {err: String(e)}; } }""")
                print(tag, "node C1:", json.dumps(node, ensure_ascii=False), flush=True)
                seen = play_dump(pg)
                print(tag, "dumped states:", len(seen), "pageerrors:", errs, flush=True)
                for i, (sp, tx) in enumerate(seen):
                    print(f"  {tag} {i+1:02d} [{sp}] {(tx or '')[:90]}", flush=True)
                print(tag, "done:", pg.evaluate("() => !!(S.story.done && S.story.done.C1)"), flush=True)
                br.close()
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
