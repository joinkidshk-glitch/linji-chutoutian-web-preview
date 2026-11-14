# v20a204 probe：喺真頁面（實 GIGS／LEADSTAR59）枚舉 awards63Fellows，
# 睇吓邊啲 (year, medium, gender) 會出新星（lan_ruoxi／shum_yingsuet／kong_siying）。
import hashlib, json, os, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work204"
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 20491
VENV = "/home/hatch/pwenv49/bin/python"

def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    want = hashlib.sha256(open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest()[:12]
    got = hashlib.sha256(body).hexdigest()[:12]
    print("serve sha", got, "want", want, flush=True)
    assert got == want
    return p

JS = """() => {
  const F = window.__awards && window.__awards.fellows63;
  const probe = {};
  ['awards63Fellows','AWARDS204_FEMALE_STARS','AWARDS63_POOL','GIGS','S'].forEach(n => {
    try { probe[n] = typeof eval(n); } catch(e) { probe[n] = 'ERR:' + String(e).slice(0,40); }
  });
  if (!F) return { probe, error: 'no __awards.fellows63' };
  const out = { probe };
  const cers = [
    { id:'award_golddisc_music', medium:'music', matchTypes:['唱片通告'] },
    { id:'award_harbour_film', medium:'film', matchTypes:['電影'] },
    { id:'award_singho_tv', medium:'tv', matchTypes:['電視劇','綜藝'] },
    { id:'award_harbour_ad', medium:'ad', matchTypes:['廣告'] }
  ];
  for (const cer of cers) for (const y of [1990, 1991, 1992]) for (const g of ['f','m','']) {
    const fl = F(cer, y, g);
    out[cer.medium + '/' + y + '/' + (g || 'mix')] = fl.map(f => f.starId + '(' + f.star + ')');
  }
  return out;
}"""

def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 932, "height": 932})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{PORT}/index.html")
            pg.wait_for_timeout(3000)
            res = pg.evaluate(JS)
            print(json.dumps(res, ensure_ascii=False, indent=1))
            print("pageerrors:", errs)
            br.close()
    finally:
        srv.terminate()

if __name__ == "__main__":
    main()
