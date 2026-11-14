# -*- coding: utf-8 -*-
"""v209 實駕：藍若曦 6 張全身圖補光邊後，對話舞台核實。
- 工作副本 ~/workspace/linji-work209（main a426947 + v209），port 20991。
- 播 R_lan_meet / push1 / crisis / ending，逐句記 DOM（img src／rect／filter／opacity），
  每個唔同表情影一張；重點：(a) 光邊喺舞台底色上面見到；(b) ending 旁白句
  （think）嗰陣聽者／旁白變暗 0.60，光邊跟住變暗（filter 喺同一張 img 度）。
- 6 張 webp HTTP 200、0 pageerror、零破圖。
Playwright venv /home/hatch/pwenv49/bin/python；headless_shell 截圖可能有 stale frame，
每句同時記 DOM 證據。"""
import hashlib, json, os, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work209"
SHOTS = "/home/hatch/workspace/linji-work209/qa209/shots"
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 20991
os.makedirs(SHOTS, exist_ok=True)

def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    got = hashlib.sha256(body).hexdigest()
    want = hashlib.sha256(open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest()
    print("serve sha", got[:12], "repo", want[:12], flush=True)
    assert got == want
    return p

def stop(p):
    try:
        p.send_signal(subprocess.signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def click_text(pg, texts, wait=900):
    for t in texts:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception: pass
        except Exception: pass
    return None

def new_game(pg):
    pg.goto(f"http://127.0.0.1:{PORT}/index.html")
    pg.wait_for_timeout(3000)
    click_text(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_text(pg, ["覆蓋", "確定", "確認"], 900)
    click_text(pg, ["跳過教學"], 1200)
    click_text(pg, ["開始寫手帳"], 1400)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
    except Exception: pass
    click_text(pg, ["確定出發"], 1500)
    for _ in range(4):
        if not click_text(pg, ["確定", "確認", "好", "知道了"], 900): break
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

STAGE_JS = """() => {
  const out = { text:'', imgs:[], choices:[], speaker:'' };
  const cands = [...document.querySelectorAll('#modal p, #modal div')].filter(e=>{
    const t=(e.textContent||'').trim(); const r=e.getBoundingClientRect();
    return t.length>3 && r.width>50 && r.height>10; });
  if (cands.length) {
    cands.sort((a,b)=>(b.textContent||'').length-(a.textContent||'').length);
    out.text = (cands[0].textContent||'').trim().slice(0,200);
  }
  [...document.querySelectorAll('img')].forEach(im=>{
    const r = im.getBoundingClientRect(); const cs = getComputedStyle(im);
    if (r.width>20 && r.height>20 && cs.visibility!=='hidden' && cs.display!=='none') {
      out.imgs.push({src:(im.getAttribute('src')||'').split('?')[0], x:Math.round(r.x), y:Math.round(r.y),
        w:Math.round(r.width), h:Math.round(r.height), op:cs.opacity, filter:cs.filter,
        natW:im.naturalWidth, natH:im.naturalHeight});
    }
  });
  out.choices = [...document.querySelectorAll('#modal button')].map(b=>(b.textContent||'').trim());
  const sp = document.querySelector('#modal .sp-name, #modal [class*="sp-name"], #modal .dlg-name');
  if (sp) out.speaker = (sp.textContent||'').trim();
  return out;
}"""

def click_next(pg):
    return pg.evaluate("""() => {
      const b=[...document.querySelectorAll('#modal button')].find(x=>(x.textContent||'').includes('下一句'));
      if(!b) return false; b.click(); return true; }""")

def shot(pg, name):
    pg.wait_for_timeout(900)
    try: pg.screenshot(path=os.path.join(SHOTS, name)); return True
    except Exception as e: print("shot fail", name, e); return False

def main():
    srv = serve()
    errs, cerrs = [], []
    log = {"nodes": {}, "http": {}, "main": {}}
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            try:
                ctx = b.new_context(viewport={"width": 390, "height": 844})
                pg = ctx.new_page()
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: cerrs.append(m.text) if m.type == "error" else None)
                print("new_game", new_game(pg), flush=True)
                pg.wait_for_timeout(1200)
                for node in ["R_lan_meet", "R_lan_push1", "R_lan_crisis", "R_lan_ending"]:
                    ok = pg.evaluate("(id)=>{ try{ return !!window.StoryPlay.start(id,{force:true}); }catch(e){ return 'ERR:'+e.message; } }", node)
                    print(node, "start", ok, flush=True)
                    pg.wait_for_timeout(1200)
                    lines, seen = [], set()
                    for step in range(8):
                        st = pg.evaluate(STAGE_JS)
                        key = st["text"]
                        if key and key not in seen:
                            seen.add(key)
                            lan = [i for i in st["imgs"] if "lan_ruoxi" in i["src"]]
                            expr = lan[0]["src"].split("lan_ruoxi_")[-1].replace(".webp", "") if lan else "none"
                            lines.append({"step": step, "text": key[:80], "lan": lan,
                                          "speaker": st["speaker"], "btns": st["choices"]})
                            shot(pg, f"v209_{node}_{expr}_s{step}.png")
                        if st["choices"] and not any("下一句" in c for c in st["choices"]):
                            shot(pg, f"v209_{node}_choices.png")
                            break
                        if not click_next(pg):
                            break
                        pg.wait_for_timeout(700)
                    log["nodes"][node] = {"start": ok, "lines": lines}
                    print(node, "lines", len(lines),
                          [(l["lan"][0]["src"].split("_")[-1] if l["lan"] else "-",
                            (l["lan"][0]["filter"] if l["lan"] else "-")) for l in lines], flush=True)
                    pg.evaluate("""() => {
                      const bs=[...document.querySelectorAll('#modal button')].filter(x=>{const r=x.getBoundingClientRect(); return r.width>0;});
                      if(bs.length){ bs[0].click(); return true; } return false; }""")
                    pg.wait_for_timeout(1000)
                    click_text(pg, ["確定", "確認", "好", "知道了"], 600)
                    pg.wait_for_timeout(600)
                # 6 張 webp HTTP
                for e in ["base", "sad", "serious", "shy", "smile", "think"]:
                    url = f"http://127.0.0.1:{PORT}/assets/story/fullbody/lan_ruoxi_{e}.webp"
                    try:
                        req = urllib.request.Request(url, method="HEAD")
                        with urllib.request.urlopen(req, timeout=5) as r:
                            log["http"][e] = r.status
                    except Exception as ex:
                        log["http"][e] = getattr(ex, "code", "ERR")
                print("http", log["http"], flush=True)
                log["main"]["broken_imgs"] = pg.evaluate("""() => {
                  const bad=[]; [...document.querySelectorAll('img')].forEach(im=>{ const r=im.getBoundingClientRect();
                    if(r.width>20&&r.height>20&&(!im.naturalWidth||im.complete===false)) bad.push(im.getAttribute('src')); });
                  return bad; }""")
                ctx.close()
            finally:
                b.close()
    finally:
        stop(srv)
    log["pageerrors"] = errs
    log["console_errors"] = cerrs[:10]
    with open("/home/hatch/workspace/linji-work209/qa209/drive209.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=1)
    print("PAGEERRORS:", len(errs), errs[:3], flush=True)
    print("CONSOLE ERRORS:", len(cerrs), cerrs[:3], flush=True)
    print("BROKEN IMGS:", log["main"].get("broken_imgs"), flush=True)

main()
