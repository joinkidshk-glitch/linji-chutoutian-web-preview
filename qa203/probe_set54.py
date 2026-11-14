# set54 探針：pending-seed 後載入，dump S.wf4＋畫面狀態，定位點解唔彈。
import os, json, subprocess, time, signal, hashlib, urllib.request, sys
sys.path.insert(0, '/home/hatch/workspace/linji-work203/qa203')
import importlib.util
spec = importlib.util.spec_from_file_location('d203', '/home/hatch/workspace/linji-work203/qa203/drive203.py')
d203 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d203)
from playwright.sync_api import sync_playwright

def probe(pg, target, day, money=None, fame=None, stress=None):
    r = d203.seed_pending(pg, target, day, money, fame, stress)
    st = d203.read_state(pg)
    info = d203.wf4_info(pg)
    scr = pg.evaluate("""() => ({
      map: !!document.querySelector('#v-map') && document.querySelector('#v-map').offsetParent !== null,
      modalH3: (document.querySelector('#modal-inner h3')||{}).textContent || null,
      modalBtns: [...document.querySelectorAll('#modal-btns button')].map(b=>(b.textContent||'').trim()),
      story: !!document.querySelector('.story-play .dlg106-plate'),
      ceremony: !!document.querySelector('.awd62-stage'),
      home: !!document.querySelector('#v-home') && document.querySelector('#v-home').offsetParent !== null,
    })""")
    print(f"PROBE {target} day={day}: seed={r.get('ok')} state_day={st and st['day']} pending={st and st['pending']} seen_n={len([k for k in (st and st['seen'] or {}) if k!='__n'])} wf4={info} screen={scr}", flush=True)
    return info

srv = d203.serve(d203.ROOT)
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=d203.EXE, args=["--no-sandbox"])
        pg = br.new_page(viewport={"width": 390, "height": 844})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        assert d203.new_game(pg, slot="1"), "new game failed"
        probe(pg, "wf4_ev_set54", 730)
        probe(pg, "wf4_ev_set54", 731)
        probe(pg, "wf4_ev_set54", 800)
        probe(pg, "wf4_ev_set17", 730, fame=26)
        probe(pg, "wf4_ev_set54", 730, fame=26)
        print("pageerrors:", errs, flush=True)
        br.close()
finally:
    d203.stop(srv)
