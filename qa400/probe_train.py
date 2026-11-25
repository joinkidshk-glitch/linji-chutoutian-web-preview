# -*- coding: utf-8 -*-
"""probe train tab DOM at week-2 notebook."""
import sys, time, json, subprocess, importlib.util
sys.path.insert(0, '/home/hatch/workspace/fullarc')
from playwright.sync_api import sync_playwright
import driver as drv
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
ROOT = "/home/hatch/workspace/linji-work400"
LOG = open(f"{ROOT}/qa400/verify/probe_train.log", "w", encoding="utf-8")
def lg(*a):
    print(*a, flush=True); print(*a, file=LOG, flush=True)
srv = subprocess.Popen(["python3","-m","http.server","19396","--bind","127.0.0.1"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
URL = "http://127.0.0.1:19396/index.html"
spec = importlib.util.spec_from_file_location("d400", f"{ROOT}/qa400/drive400.py")
# import helpers without running main: exec only up to results = {} (module runs drive at import, so instead copy via exec of file head)
src = open(f"{ROOT}/qa400/drive400.py", encoding="utf-8").read()
head = src.split("results = {}")[0]
ns = {"__file__": f"{ROOT}/qa400/drive400.py"}
exec(head, ns)
ev = ns["ev"]; click_btn_text = ns["click_btn_text"]; click_day_row = ns["click_day_row"]
click_cat_tab = ns["click_cat_tab"]; new_game = ns["new_game"]; mutate_S = ns["mutate_S"]
play_week = ns["play_week"]; STATE_JS = ns["STATE_JS"]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox','--proxy-server=http://127.0.0.1:18081','--ignore-certificate-errors'])
    pg = b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2).new_page()
    pg.set_default_timeout(10000)
    new_game(pg)
    mutate_S(pg, enrolled={"train_vocal": True}, trainCount={"train_vocal": 3}, lastTrain400="train_vocal")
    ok, note = play_week(pg)
    lg("arrive", ok, note)
    lg("cat-tabs html:", ev(pg, "() => (document.getElementById('cat-tabs')||{outerHTML:''}).outerHTML.slice(0,800)"))
    click_day_row(pg, 1)
    pg.wait_for_timeout(500)
    lg("after day-row click, act-list btns:", ev(pg, """() => [...document.querySelectorAll('#act-list button')].map(x=>(x.textContent||'').trim().slice(0,30))"""))
    lg("click 訓練 tab:", click_cat_tab(pg, r'訓練'))
    pg.wait_for_timeout(900)
    lg("after tab, act-list btns:", ev(pg, """() => [...document.querySelectorAll('#act-list button')].map(x=>(x.textContent||'').trim().slice(0,40))"""))
    lg("guide68-meta:", ev(pg, """() => [...document.querySelectorAll('#act-list .guide68-meta')].map(x=>(x.textContent||'').trim())"""))
    lg("train71-pick:", ev(pg, """() => [...document.querySelectorAll('#act-list .train71-pick')].map(x=>x.getAttribute('data-t71pick'))"""))
    lg("act-list html head:", ev(pg, "() => (document.getElementById('act-list')||{innerHTML:''}).innerHTML.slice(0,1500)"))
    pg.screenshot(path=f"{ROOT}/qa400/shots/probe_train.png")
    b.close()
srv.terminate()
lg("DONE")
