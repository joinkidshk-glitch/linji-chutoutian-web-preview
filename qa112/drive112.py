# -*- coding: utf-8 -*-
"""v20a112 ICONS112 實駕（改前 pre／改後 post 共用）：
   行勻換過圖標嘅畫面：地圖頁、全部地點列、地點板、行程編輯頁、手帳各 tab
   （行程／事業拍攝簿／近況／消息／人情人脈）、日結結果行；量 img.ic112 數目＋
   殘留 emoji＋pageerror。
   用法：/home/hatch/pwenv49/bin/python qa112/drive112.py [base_url] [pre|post]
   （先喺工作副本 python3 -m http.server 8932）"""
import sys, os, json
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8932/"
TAG = sys.argv[2] if len(sys.argv) > 2 else "post"
URL = BASE + "index.html?softPreview=1&softRev=s107"
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
LOG = {"tag": TAG, "screens": {}, "errors": []}

def click_first(pg, texts, wait=1000):
    """Click first visible+enabled button whose text contains any of texts.
    Uses JS dispatch (Playwright's actionability check times out on this app's
    re-rendering modals even though the handler fires). Retries 3x: the map
    hint re-renders after a modal dismiss and the target button may appear late."""
    for _attempt in range(3):
        for t in texts:
            try:
                loc = pg.locator("button:has-text('" + t + "')")
                for i in range(loc.count()):
                    el = loc.nth(i)
                    try:
                        if el.is_visible() and el.is_enabled():
                            el.evaluate("b => b.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}))")
                            pg.wait_for_timeout(wait)
                            return t
                    except Exception:
                        pass
            except Exception:
                pass
        pg.wait_for_timeout(800)
    return None

def click_tab(pg, sel, wait=1000):
    try:
        el = pg.locator(sel).first
        if el.is_visible():
            el.click(timeout=1200); pg.wait_for_timeout(wait); return True
    except Exception:
        pass
    return False

def click_through_story(pg, max_steps=40):
    """撳晒所有 下一句／選擇，直至故事 overlay 消失。回傳撳咗幾多下。"""
    n = 0
    for _ in range(max_steps):
        clicked = pg.evaluate("""() => {
          const vis = (el) => el && el.offsetParent !== null && !el.disabled;
          const row = document.getElementById('modal-btns');
          if (row) { const bs = [...row.querySelectorAll('button')].filter(vis); if (bs.length) { bs[0].click(); return 'modal'; } }
          const ch = document.querySelector('.sp-choice');
          if (ch && vis(ch)) { ch.click(); return 'choice'; }
          const nb = [...document.querySelectorAll('.e79-btn')].find(vis);
          if (nb) { nb.click(); return 'enc-next'; }
          const ch2 = document.querySelector('.e79-choice');
          if (ch2 && vis(ch2)) { ch2.click(); return 'enc-choice'; }
          const sk = document.querySelector('.e79-skip');
          if (sk && vis(sk)) { sk.click(); return 'enc-skip'; }
          return null; }""")
        if not clicked:
            break
        n += 1
        pg.wait_for_timeout(450)
    return n

JS_MEASURE = '''() => {
  const q = (s) => document.querySelectorAll(s).length;
  const txt = (s) => { const el = document.querySelector(s); return el ? el.textContent.slice(0, 120) : null; };
  const html = (s) => { const el = document.querySelector(s); return el ? el.innerHTML.slice(0, 200) : null; };
  const EM = ["🗺️","😴","🌙","🎤","☕","🎬","🎥","💪","🏠","📰","🎁","🏥","🎵","💿","👥","📺","📻","📡","🦁","💼","🏢","🎭","📚","📖","🥋","🧹","🤒","📞","😊","⭐","✨","✅"];
  const vis = (s) => { const el = document.querySelector(s); return el ? el.offsetParent !== null : false; };
  return {
    ic112: q("img.ic112"),
    ic112_srcs: [...document.querySelectorAll("img.ic112")].slice(0, 40).map(i => (i.getAttribute("src")||"").split("/").pop()),
    ic112_broken: [...document.querySelectorAll("img.ic112")].filter(i => !i.complete || i.naturalWidth === 0).length,
    day_ic: q(".day-row .ic"), day_ic_img: q(".day-row .ic img"),
    cat_ci: q(".cat-tab .ci"), cat_ci_img: q(".cat-tab .ci img"),
    act_ai: q(".act-item .ai"), act_ai_img: q(".act-item .ai img"),
    psr_icon_img: q(".psr-icon img"),
    fav_dots: q(".fav-dots112"), fav_dots_on: q(".fav-dots112 i.on"),
    hearts_txt: (document.body.textContent.match(/[♥♡]/g) || []).length,
    loc_title: txt("#loc-title"), loc_title_html: html("#loc-title"), loc_title_img: q("#loc-title img"),
    check112: q(".ic-check112"),
    dayres_modal: (() => { const el = document.querySelector("#modal-inner");
      if (!el) return null;
      return { text: el.textContent.slice(0, 160), ic112: el.querySelectorAll("img.ic112").length,
        check: el.querySelectorAll(".ic-check112").length,
        srcs: [...el.querySelectorAll("img.ic112")].map(i => (i.getAttribute("src")||"").split("/").pop()) }; })(),
    nb_visible: vis("#notebook") || vis(".home-pane") || vis("#home-pane"),
    story_open: !!document.querySelector(".story-play"),
    enc_open: !!document.getElementById("enc79-overlay")
  };
}'''

def shot(pg, name):
    pg.screenshot(path=os.path.join(SHOTS, "%s_%s.png" % (TAG, name)))

def measure(pg, name):
    m = pg.evaluate(JS_MEASURE)
    LOG["screens"][name] = m
    print(f"[{name}] ic112={m['ic112']} broken={m['ic112_broken']} day_ic={m['day_ic']}/{m['day_ic_img']} cat={m['cat_ci']}/{m['cat_ci_img']} act={m['act_ai']}/{m['act_ai_img']} favdots={m['fav_dots']}({m['fav_dots_on']} on) hearts={m['hearts_txt']} check={m['check112']} locTitle={m['loc_title']!r} locImg={m['loc_title_img']} nbVis={m['nb_visible']} story={m['story_open']} enc={m['enc_open']} dayres={m['dayres_modal']}")
    return m

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg.on("pageerror", lambda e: LOG["errors"].append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
    except Exception:
        pass
    click_first(pg, ["確定出發"], 1500)
    for i in range(4):
        if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    print("S ok:", pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')"))
    # 註：遊戲本體包喺 IIFE 入面，iconHtml112 唔掛 window——用 DOM 嘅 img.ic112 數目做活證據（見 measure）。

    # ---------- 地圖 ----------
    pg.wait_for_timeout(800)
    shot(pg, "map"); measure(pg, "map")

    # ---------- 全部地點列（地圖底欄 #map-area-list；v20a43 起 display:none，DOM 照生成＋綁定——只量 DOM，唔截元素圖） ----------
    print("all locs:", click_first(pg, ["全部地點"], 1200))
    shot(pg, "alllocs"); measure(pg, "alllocs")
    click_first(pg, ["只亮有事"], 800)

    # ---------- 地點板：金龍茶餐廳（入場可能觸發巧遇，先撳晒故事） ----------
    print("open loc 金龍茶餐廳:", click_first(pg, ["金龍茶餐廳"], 1800))
    n = click_through_story(pg)
    print("story clicks through:", n)
    pg.wait_for_timeout(600)
    shot(pg, "locsheet"); measure(pg, "locsheet")
    click_first(pg, ["返回地圖"], 1000)

    # ---------- 手帳：經 ☰ 選單 → 手帳 ----------
    print("menu:", click_tab(pg, "#btn-menu", 800))
    print("journal:", click_first(pg, ["手帳"], 1500))
    pg.wait_for_timeout(800)
    shot(pg, "nb_plan"); measure(pg, "nb_plan")

    # ---------- 手帳：人情 → 人脈 ----------
    click_tab(pg, "#hgroup-favor", 1200)
    click_tab(pg, "#htab-people", 1200)
    shot(pg, "nb_people"); measure(pg, "nb_people")

    # ---------- 手帳：事業（拍攝簿） ----------
    click_tab(pg, "#hgroup-career", 1200)
    shot(pg, "nb_career"); measure(pg, "nb_career")

    # ---------- 手帳：近況／消息 ----------
    click_tab(pg, "#hgroup-status", 1000)
    shot(pg, "nb_status"); measure(pg, "nb_status")
    click_tab(pg, "#hgroup-news", 1000)
    shot(pg, "nb_news"); measure(pg, "nb_news")

    # ---------- 返地圖 → 過一日（逛逛日冇「開始今日行程」，過一日→二次確認→結算） → 日結結果（先截圖，後撳走） ----------
    click_first(pg, ["返回地圖"], 1000)
    print("pass day:", click_first(pg, ["過一日"], 1200))
    print("confirm pass:", click_first(pg, ["確定過一日"], 1200))
    pg.wait_for_timeout(1200)
    shot(pg, "dayres"); measure(pg, "dayres")
    # 小休 modal →「開始今日行程」執行週二休息日，行 resolvePlannedDay 結果行（37225，帶 icon）
    print("start tue:", click_first(pg, ["開始今日行程"], 1500))
    pg.wait_for_timeout(1200)
    shot(pg, "dayres2"); measure(pg, "dayres2")
    # 確認 modal → 執行 → resolvePlannedDay 結果行（37225，帶 icon）
    print("confirm start:", click_first(pg, ["確定", "開始"], 1500))
    pg.wait_for_timeout(1200)
    shot(pg, "dayres3"); measure(pg, "dayres3")
    # 週三／週四都係逛逛日：過一日→小休 modal→返回地圖；週五街頭表演經「開始今日行程」執行，結果行帶 icon
    for d in ["wed", "thu"]:
        print(d, "back:", click_first(pg, ["返回地圖"], 1000))
        print(d, "pass:", click_first(pg, ["過一日"], 1200))
        print(d, "confirm:", click_first(pg, ["確定過一日"], 1200))
        pg.wait_for_timeout(1200)
    print("fri back:", click_first(pg, ["返回地圖"], 1000))
    print("fri start:", click_first(pg, ["開始今日行程"], 1500))
    pg.wait_for_timeout(1000)
    print("fri confirm:", click_first(pg, ["確定", "開始"], 1500))
    pg.wait_for_timeout(1200)
    shot(pg, "dayres_fri"); measure(pg, "dayres_fri")
    click_through_story(pg)

    print("pageerrors:", LOG["errors"][:8])
    with open(os.path.join(HERE, "drive112_%s.json" % TAG), "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=1)
    b.close()
print("DONE", TAG)
