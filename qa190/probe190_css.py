import subprocess, time, signal, json
from playwright.sync_api import sync_playwright
URI = open('/tmp/poster_uri.txt').read()
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
srv = subprocess.Popen(["python3", "-m", "http.server", "8978"], cwd="/home/hatch/workspace/linji-work190",
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
JS = """async (uri) => {
  const out = {};
  function build(){
    document.querySelectorAll('.awd63-glamour').forEach(e=>e.remove());
    document.querySelectorAll('#probe-style').forEach(e=>e.remove());
    const ov = document.createElement('div');
    ov.className = 'awd63-glamour on';
    ov.style.width = '760px';
    ov.innerHTML = '<div class="awd63-glamour-panel"><img src="' + uri + '"/>' +
      '<div class="cap">\\u1f3c6 \\u5f97\\u734e<br/>\\u6700\\u4f73\\u7537\\u4e3b\\u89d2\\uff1a\\u300a\\u591c\\u66f4\\u548c\\u97f3\\u300b</div></div>';
    document.body.appendChild(ov);
    return ov;
  }
  function measure(ov){
    const pn = ov.querySelector('.awd63-glamour-panel');
    const im = ov.querySelector('img');
    const r = (el)=>{ const b = el.getBoundingClientRect(); return {top: Math.round(b.top*10)/10, bottom: Math.round(b.bottom*10)/10, w: Math.round((b.right-b.left)*10)/10, h: Math.round((b.bottom-b.top)*10)/10}; };
    return { overlay: r(ov), panel: r(pn), img: r(im),
      emptyTop: Math.round((im.getBoundingClientRect().top - pn.getBoundingClientRect().top)*10)/10,
      emptyRatio: Math.round((im.getBoundingClientRect().top - pn.getBoundingClientRect().top) / (pn.getBoundingClientRect().bottom - pn.getBoundingClientRect().top) * 1000)/1000,
      imgMaxH: getComputedStyle(im).maxHeight };
  }
  const ov = build();
  await ov.querySelector('img').decode();
  out.A932 = measure(ov);
  const st1 = document.createElement('style'); st1.id='probe-style';
  st1.textContent = '.awd63-glamour{align-items:flex-end !important;container-type:size !important}' +
    '.awd63-glamour-panel>img{max-height:calc(40cqh - 8px) !important}';
  document.head.appendChild(st1);
  out.G932 = measure(ov);
  ov.style.width = '672px';
  out.G700 = measure(ov);
  st1.textContent = '';
  out.F700 = measure(ov);
  return out;
}"""
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        pg = br.new_page(viewport={"width": 932, "height": 844})
        pg.goto("http://127.0.0.1:8978/index.html?softPreview=1")
        pg.wait_for_timeout(2500)
        res = pg.evaluate(JS, URI)
        print(json.dumps(res, indent=1, ensure_ascii=False))
        br.close()
finally:
    srv.send_signal(signal.SIGTERM)
