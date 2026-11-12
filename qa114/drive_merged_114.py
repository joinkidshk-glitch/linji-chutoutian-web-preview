# -*- coding: utf-8 -*-
"""v20a114 合併後冒煙實駕（只驗收，唔改 code、唔合併、唔推 main）。
本地鏡像：main HEAD cf66865 工作樹直開 http.server（port 8977），Playwright
headless shell 駕駛，gate-on ?softPreview=1。只用存檔槽 3。
用法：/home/hatch/pwenv49/bin/python qa114/drive_114.py
產出：qa114/shots/merged114/drive_merged_*.png ＋ qa114/drive_merged_114.json ＋ qa114/drive_114_report.md
"""
import sys, os, json, subprocess, time, signal, traceback
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/linji-repo")
HERE = os.path.join(ROOT, "qa114")
SHOTS = os.path.join(HERE, "shots", "merged114")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8977
URL = f"http://127.0.0.1:{PORT}/index.html?softPreview=1&softRev=s107&nocache=merged114"
SAVE3 = "starVolunteer_map_v19w_slot3"
BLOCK_TOAST = "今日出行額度用完——今日已經去咗 2 個地方，聽日再去。"
PILOT = {"luk_baakyin", "liu_bingxing", "mak_zhendong", "yip_manji"}

LOG = {"errors": [], "console_errors": [], "failed_requests": [], "items": {}, "notes": []}

# ---------------- server ----------------
def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=ROOT,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    if p.poll() is not None:
        raise RuntimeError("http.server died on start")
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

# ---------------- JS snippets ----------------
JS_STATE = """() => {
  const S = window.S;
  const hintEl = document.getElementById('map-hint');
  const trav = hintEl ? hintEl.querySelector('.map-hint-travel') : null;
  const sheet = document.getElementById('loc-sheet');
  const modalBtns = [...document.querySelectorAll('#modal-btns button, .e79-row button, button.e79-skip')]
    .filter(b=>b.offsetParent!==null).map(b=>b.textContent.trim());
  const sheetBtns = sheet ? [...sheet.querySelectorAll('button')]
    .filter(b=>b.offsetParent!==null).map(b=>({t:b.textContent.trim().slice(0,30), id:b.id||''})) : [];
  const stage = document.querySelector('.story-play') || document.querySelector('.e79-stage');
  const e79meta = (document.querySelector('.e79-meta')||{}).textContent || null;
  return {
    hasS: !!S,
    day: S ? S.dayIndex : null,
    travel: S ? (S.travel114 || null) : null,
    remain: S ? (S.travel114 ? Math.max(0, 2 - (Number(S.travel114.used)||0)) : 2) : null,
    starDay: S ? (S.starDay || null) : null,
    money: S ? S.money : null, stress: S ? S.stress : null, stamina: S ? S.stamina : null,
    hintTravel: trav ? trav.textContent.trim() : null,
    hintTravelCls: trav ? trav.className : null,
    toast: (document.getElementById('toast')||{}).innerText || '',
    view: [...document.querySelectorAll('.view')].filter(v=>v.offsetParent!==null).map(v=>v.id),
    sheetOn: !!(sheet && sheet.classList.contains('on')),
    sheetTitle: (document.getElementById('loc-title')||{}).textContent || '',
    sheetBtns,
    modalTitle: (document.querySelector('#modal-inner h3')||{}).textContent || null,
    modalBtns,
    hasStage: !!stage,
    e79Meta: e79meta,
    stageLine: stage ? ((stage.querySelector('.sp-line')||stage.querySelector('.e79-line')||{}).textContent||'').slice(0,60) : null,
    stageChars: stage ? [...stage.querySelectorAll('.dlg106-char')].map(im=>im.dataset.dlgId||'')
      .concat([...stage.querySelectorAll('.e79-char')].map(im=>(im.getAttribute('src')||'').split('/').pop().split('?')[0].slice(0,24))) : [],
    areaList: [...document.querySelectorAll('#map-area-list button')].map(b=>b.getAttribute('data-loc')),
    showAll: (document.getElementById('map-show-all-locs')||{}).textContent || null,
    startToday: (document.getElementById('map-start-today')||{}).textContent || null,
    endDay: (document.getElementById('map-end-day')||{}).textContent || null,
    lockedPins: document.querySelectorAll('.pin.travel-locked').length,
    lockedArea: document.querySelectorAll('#map-area-list button.travel-locked').length,
    lsKeys: Object.keys(localStorage),
    prefs: (()=>{ try{ return JSON.parse(localStorage.getItem('starVolunteer_prefs_v19z9')||'null'); }catch(e){ return null; } })(),
  };
}"""

JS_MODAL_CLICK = """(labels) => {
  const btns=[...document.querySelectorAll('#modal-btns button, .e79-row button, button.e79-skip')]
    .filter(b=>b.offsetParent!==null && !b.disabled);
  for(const lab of labels){
    const b=btns.find(x=>(x.textContent||'').trim().includes(lab));
    if(b){ b.click(); return lab; }
  }
  return null;
}"""

JS_FIRST_DLG_CLICK = """() => {
  const btns=[...document.querySelectorAll('#modal-btns button, .e79-row button, button.e79-skip')]
    .filter(b=>b.offsetParent!==null && !b.disabled);
  if(!btns.length) return null;
  const deny=['取消','唔好','稍後','唔去','唔要'];
  const pick=btns.find(b=>!deny.some(d=>(b.textContent||'').includes(d)));
  if(!pick) return 'all-denied:'+btns.map(b=>b.textContent.trim()).join('|');
  const t=pick.textContent.trim(); pick.click(); return t;
}"""

JS_ANY_CLICK = """(labels) => {
  const btns=[...document.querySelectorAll('button')]
    .filter(b=>b.offsetParent!==null && !b.disabled);
  for(const lab of labels){
    const b=btns.find(x=>(x.textContent||'').trim().includes(lab));
    if(b){ b.click(); return lab; }
  }
  return null;
}"""

JS_SHOW_ALL = """() => {
  const b=document.getElementById('map-show-all-locs');
  if(!b) return 'no-btn';
  if(b.textContent.includes('全部地點')){ b.click(); return 'clicked-show-all'; }
  return 'already-all';
}"""

# ---------------- helpers ----------------
class Drv:
    def __init__(self, pg):
        self.pg = pg
        self.n = 0

    def shot(self, name):
        self.n += 1
        path = os.path.join(SHOTS, f"drive_merged_{name}.png")
        try:
            self.pg.screenshot(path=path)
        except Exception as e:
            LOG["notes"].append(f"shot {name} failed: {e}")
        return path

    def st(self):
        return self.pg.evaluate(JS_STATE)

    def modal_click(self, labels, wait=700):
        r = self.pg.evaluate(JS_MODAL_CLICK, labels)
        if r:
            self.pg.wait_for_timeout(wait)
        return r

    def any_click(self, labels, wait=700):
        r = self.pg.evaluate(JS_ANY_CLICK, labels)
        if r:
            self.pg.wait_for_timeout(wait)
        return r

    def click_text(self, texts, wait=900):
        for t in texts:
            try:
                loc = self.pg.locator("button:has-text('" + t + "')")
                for i in range(loc.count()):
                    el = loc.nth(i)
                    try:
                        if el.is_visible() and el.is_enabled():
                            el.click(timeout=900)
                            self.pg.wait_for_timeout(wait)
                            return t
                    except Exception:
                        pass
            except Exception:
                pass
        return None

    def wait_map(self, timeout_ms=8000):
        for _ in range(timeout_ms // 400):
            s = self.st()
            if "v-map" in s["view"] and not s["sheetOn"] and not s["modalBtns"]:
                return s
            self.pg.wait_for_timeout(400)
        return self.st()

    def ensure_map(self):
        """Close sheet / dismiss ack modals until back on map (no sheet, no modal)."""
        for _ in range(12):
            s = self.st()
            if "v-map" in s["view"] and not s["sheetOn"] and not s["modalBtns"] and not s["hasStage"]:
                return s
            if s["sheetOn"]:
                try:
                    self.pg.locator("#loc-close").click(timeout=1200)
                except Exception:
                    self.pg.evaluate("() => { const b=document.getElementById('loc-close'); if(b) b.click(); }")
                self.pg.wait_for_timeout(800)
                continue
            if s["hasStage"] or s["modalBtns"]:
                if not self.modal_click(["下一句", "繼續", "知道了", "好", "確定", "明白", "點頭離開", "離開", "關閉", "返回"]):
                    self.any_click(["下一句", "點頭離開", "繼續"])
                self.pg.wait_for_timeout(500)
                continue
            self.pg.wait_for_timeout(500)
        return self.st()

    def drive_dialogue(self, max_steps=45):
        """Click through story/encounter/WF4 dialogue until sheet opens or back on map.
        Returns (outcome, steps_log) where outcome in sheet/map/stuck."""
        steps = []
        for i in range(max_steps):
            s = self.st()
            steps.append({"i": i, "stage": s["hasStage"], "chars": s["stageChars"],
                          "modalTitle": s["modalTitle"], "modalBtns": s["modalBtns"],
                          "sheetOn": s["sheetOn"], "line": s["stageLine"]})
            if s["sheetOn"]:
                return "sheet", steps
            if "v-map" in s["view"] and not s["hasStage"] and not s["modalBtns"]:
                return "map", steps
            hit = self.modal_click(["下一句", "繼續", "我知道了", "好", "確定", "明白",
                                    "點頭離開", "離開", "返去", "關閉", "返回"])
            if not hit:
                # Choice step in an encounter (option labels vary): pick first non-decline.
                hit = self.pg.evaluate(JS_FIRST_DLG_CLICK)
                if hit:
                    steps.append({"i": i, "choice_click": hit})
            if not hit:
                hit = self.any_click(["下一句", "點頭離開", "繼續"])
            if not hit:
                return "stuck", steps
            self.pg.wait_for_timeout(450)
        return "stuck", steps

    def enter_loc(self, loc_id, tag):
        """Click a location from the map PIN (real user path; the #map-area-list
        bottom bar is display:none since v20a43, so its buttons are not clickable).
        Drive any intercept dialogue. Returns outcome dict."""
        s0 = self.st()
        trig0 = (s0["starDay"] or {}).get("triggered", 0)
        self.ensure_map()
        self.pg.wait_for_timeout(500)
        btn = self.pg.locator(f'#map-pins button.pin[data-loc="{loc_id}"]')
        used_js_fallback = False
        try:
            btn.click(timeout=5000)
        except Exception as e:
            # Fallback: synthetic click on the real pin element (same onclick -> openLoc).
            r = self.pg.evaluate(
                """(loc) => { const b=document.querySelector('#map-pins button.pin[data-loc="'+loc+'"]');
                   if(!b) return 'no-pin';
                   const r=b.getBoundingClientRect();
                   if(r.width===0 || r.height===0) return 'zero-rect';
                   b.click(); return 'js-clicked'; }""", loc_id)
            used_js_fallback = True
            if r != "js-clicked":
                return {"outcome": "click-fail", "error": str(e)[:300] + " | pin=" + r, "before": s0}
        # poll: toast (blocked) / sheet / stage
        blocked_toast = None
        saw_stage = False
        for _ in range(30):
            self.pg.wait_for_timeout(400)
            s = self.st()
            if s["toast"] and "今日出行額度用完" in s["toast"]:
                blocked_toast = s["toast"]
                break
            if s["sheetOn"]:
                break
            if s["hasStage"] or s["modalBtns"]:
                saw_stage = True
                break
        s = self.st()
        if blocked_toast:
            self.shot(f"{tag}_blocked")
            return {"outcome": "blocked", "toast": blocked_toast, "before": s0, "after": s,
                    "sheetOn": s["sheetOn"], "view": s["view"], "js_fallback": used_js_fallback}
        if s["sheetOn"]:
            self.shot(f"{tag}_sheet")
            return {"outcome": "sheet", "before": s0, "after": s, "saw_stage": saw_stage,
                    "js_fallback": used_js_fallback}
        if saw_stage or s["hasStage"] or s["modalBtns"]:
            out, steps = self.drive_dialogue()
            s2 = self.st()
            self.shot(f"{tag}_afterdlg_{out}")
            return {"outcome": f"dialogue-{out}", "before": s0, "after": s2,
                    "trig_delta": ((s2["starDay"] or {}).get("triggered", 0) - trig0),
                    "dlg_steps": len(steps),
                    "dlg_last": steps[-1] if steps else None,
                    "js_fallback": used_js_fallback}
        self.shot(f"{tag}_unknown")
        return {"outcome": "unknown", "before": s0, "after": s, "js_fallback": used_js_fallback}

    def back_to_map(self):
        s = self.st()
        if s["sheetOn"]:
            try:
                self.pg.locator("#loc-close").click(timeout=2000)
            except Exception:
                self.pg.evaluate("() => { const b=document.getElementById('loc-close'); if(b) b.click(); }")
            self.pg.wait_for_timeout(900)
        return self.ensure_map()

    def advance_day(self, tag):
        """Click 過一日 → confirm → drive day-end/newspaper modals until next day on map."""
        s0 = self.st()
        day0 = s0["day"]
        log = []
        self.ensure_map()
        # #map-end-day lives inside #map-hint, which is visibility:hidden while a
        # toast is up (#app.toast-up). Wait the toast out first (1.8s).
        for _ in range(12):
            if not self.pg.evaluate("() => document.getElementById('app').classList.contains('toast-up')"):
                break
            self.pg.wait_for_timeout(300)
        try:
            self.pg.locator("#map-end-day").click(timeout=6000)
        except Exception as e:
            log.append({"end_day_pw_click_fail": str(e)[:250]})
            r = self.pg.evaluate("""() => { const b=document.getElementById('map-end-day');
              if(!b) return 'no-btn'; b.click(); return 'js-clicked'; }""")
            log.append({"end_day_js_fallback": r})
            if r != "js-clicked":
                # Forced scheduled day (e.g. Tue rest): no 過一日 button is rendered.
                # Advance by executing the day's schedule instead.
                st_now = self.st()
                log.append({"forced_day_fallback": True, "startToday": st_now.get("startToday"),
                            "hint": (st_now.get("hintTravel") or "")[:40]})
                clicked = None
                try:
                    self.pg.locator("#map-start-today").click(timeout=4000)
                    clicked = "map-start-today"
                except Exception:
                    clicked = self.pg.evaluate("""() => { const b=document.getElementById('map-start-today');
                      if(!b) return 'no-start-btn'; b.click(); return 'js-clicked'; }""")
                log.append({"start_today_click": clicked})
                if clicked in (None, "no-start-btn"):
                    # Last resort: journal's 開始今日行程 / 繼續行程 button.
                    clicked = self.any_click(["開始今日行程", "繼續行程"])
                    log.append({"journal_start_click": clicked})
                if not clicked:
                    self.shot(f"{tag}_noendbtn")
                    return {"ok": False, "error": str(e)[:300], "before": s0, "log": log}
        self.pg.wait_for_timeout(900)
        hit = self.modal_click(["確定過一日"])
        log.append({"confirm": hit})
        for i in range(30):
            s = self.st()
            log.append({"i": i, "day": s["day"], "view": s["view"], "modalTitle": s["modalTitle"],
                        "modalBtns": s["modalBtns"], "stage": s["hasStage"], "sheet": s["sheetOn"]})
            if s["day"] is not None and s["day"] > day0 and "v-map" in s["view"] \
                    and not s["modalBtns"] and not s["hasStage"] and not s["sheetOn"]:
                self.shot(f"{tag}_nextday")
                return {"ok": True, "before": s0, "after": s, "log": log}
            if s["hasStage"] or s["modalBtns"]:
                if not self.modal_click(["返回地圖", "繼續", "知道了", "好", "確定", "明白",
                                        "下一句", "下一頁", "收起", "關閉"]):
                    # Fallback: click first modal button unless it is a decline/cancel.
                    # (Day-end / newspaper modals vary; stalling here blocked run 1.)
                    fb = self.pg.evaluate("""() => {
                      const bs=[...document.querySelectorAll('#modal-btns button')]
                        .filter(b=>b.offsetParent!==null && !b.disabled);
                      if(!bs.length) return null;
                      const deny=['取消','唔好','稍後','唔去','唔要','開始今日行程'];
                      const pick=bs.find(b=>!deny.some(d=>(b.textContent||'').includes(d)));
                      if(!pick) return 'all-denied:'+bs.map(b=>b.textContent.trim()).join('|');
                      const t=pick.textContent.trim(); pick.click(); return t; }""")
                    log.append({"fallback_click": fb})
                    if fb is None or (isinstance(fb, str) and fb.startswith("all-denied")):
                        self.any_click(["返回地圖", "繼續", "下一句"])
                self.pg.wait_for_timeout(500)
                continue
            self.pg.wait_for_timeout(500)
        s = self.st()
        self.shot(f"{tag}_stuck")
        return {"ok": False, "before": s0, "after": s, "log": log}

    def new_game_slot3(self, tag):
        """Fresh game into slot 3 only. Assumes localStorage may be empty (seed slot 3)."""
        self.pg.goto(URL)
        self.pg.wait_for_timeout(2500)
        keys = self.pg.evaluate("() => Object.keys(localStorage).filter(k=>k.indexOf('starVolunteer')===0)")
        if not keys:
            self.pg.evaluate(
                "() => localStorage.setItem('starVolunteer_map_v19w_slot3', "
                "JSON.stringify({dayIndex:0,money:0,fame:0}))")
            LOG["notes"].append(f"{tag}: seeded slot3 minimal save so slot modal appears")
        self.click_text(["新遊戲"])
        self.pg.wait_for_timeout(900)
        # slot modal?
        has_slots = self.pg.evaluate("() => !!document.querySelector('#slot-list [data-slot=\"3\"]')")
        if has_slots:
            self.pg.evaluate("() => { const b=document.querySelector('[data-slot=\"3\"]'); if(b) b.click(); }")
            self.pg.wait_for_timeout(900)
            self.modal_click(["覆蓋開新局"])
            self.pg.wait_for_timeout(800)
        self.click_text(["跳過教學"], 1200)
        self.pg.wait_for_timeout(600)
        self.click_text(["開始寫手帳"], 1400)
        self.pg.wait_for_timeout(600)
        try:
            self.pg.locator("#btn-confirm-plan").click(timeout=3000)
            self.pg.wait_for_timeout(1200)
        except Exception:
            pass
        self.modal_click(["確定出發"])
        for _ in range(5):
            if not self.modal_click(["確定", "確認", "好", "知道了"]):
                break
        s = self.wait_map()
        self.shot(f"{tag}_map")
        return s


def record(item, verdict, detail):
    LOG["items"][item] = {"verdict": verdict, "detail": detail}
    print(f"[{item}] {verdict}: {json.dumps(detail, ensure_ascii=False)[:900]}")


def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
            pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
            pg.on("pageerror", lambda e: LOG["errors"].append(str(e)))
            pg.on("console", lambda m: LOG["console_errors"].append(m.text) if m.type == "error" else None)
            pg.on("requestfailed", lambda r: LOG["failed_requests"].append(r.url.split("?")[0][-90:]))
            d = Drv(pg)

            # ---------- Item 1+2+3 : fresh game A ----------
            s = d.new_game_slot3("A_fresh")
            hint1 = s.get("hintTravel")
            shot_a_map = "shots/merged114/drive_merged_A_fresh_map.png"
            record("1_map_hint", "PASS" if hint1 == "今日出行：仲可以去 2 個地方" else "FAIL",
                   {"hint": hint1, "day": s.get("day"), "travel": s.get("travel"),
                    "activeSlot": (s.get("prefs") or {}).get("activeSlot"),
                    "shot": shot_a_map})

            r1 = d.enter_loc("cafe_cha", "A1_cafe")
            s_after1 = d.st()
            d.back_to_map()
            s_map1 = d.st()
            d.shot("A_after1_map")
            ok2a = (r1["outcome"] in ("sheet", "dialogue-sheet")
                    and s_after1.get("travel", {}).get("used") == 1
                    and s_map1.get("hintTravel") == "今日出行：仲可以去 1 個地方")
            record("2a_first_entry", "PASS" if ok2a else "FAIL",
                   {"enter": r1["outcome"], "used": (s_after1.get("travel") or {}),
                    "hint_after": s_map1.get("hintTravel"),
                    "shot": "shots/merged114/drive_merged_A1_cafe_sheet.png / drive_merged_A_after1_map.png"})

            r2 = d.enter_loc("gift_shop", "A2_gift")
            s_after2 = d.st()
            d.back_to_map()
            s_map2 = d.st()
            d.shot("A_after2_map")
            ok2b = (r2["outcome"] in ("sheet", "dialogue-sheet")
                    and (s_after2.get("travel") or {}).get("used") == 2
                    and s_map2.get("hintTravel") == "今日出行額度已用完，聽日再去")
            record("2b_second_entry", "PASS" if ok2b else "FAIL",
                   {"enter": r2["outcome"], "used": s_after2.get("travel"),
                    "hint_after": s_map2.get("hintTravel"),
                    "lockedPins": s_map2.get("lockedPins"), "lockedArea": s_map2.get("lockedArea"),
                    "shot": "shots/merged114/drive_merged_A2_gift_sheet.png / drive_merged_A_after2_map.png"})

            r3 = d.enter_loc("hospital", "A3_hosp")
            s_after3 = d.st()
            ok3 = (r3["outcome"] == "blocked"
                   and r3.get("toast") == BLOCK_TOAST
                   and not s_after3.get("sheetOn")
                   and "v-map" in s_after3.get("view", [])
                   and (s_after3.get("travel") or {}).get("used") == 2)
            record("3_blocked", "PASS" if ok3 else "FAIL",
                   {"enter": r3, "toast": r3.get("toast"), "sheetOn": s_after3.get("sheetOn"),
                    "view": s_after3.get("view"), "used": (s_after3.get("travel") or {}),
                    "shot": "shots/merged114/drive_merged_A3_hosp_blocked.png"})

            # ---------- Item 4 : fresh game B, re-entry counts ----------
            s = d.new_game_slot3("B_fresh")
            rb1 = d.enter_loc("cafe_cha", "B1_cafe")
            d.back_to_map()
            rb2 = d.enter_loc("cafe_cha", "B2_cafe_again")
            s_b2 = d.st()
            d.back_to_map()
            s_b2map = d.st()
            rb3 = d.enter_loc("gift_shop", "B3_gift")
            ok4 = ((rb2["outcome"] in ("sheet", "dialogue-sheet"))
                   and (s_b2.get("travel") or {}).get("used") == 2
                   and s_b2map.get("hintTravel") == "今日出行額度已用完，聽日再去"
                   and rb3["outcome"] == "blocked")
            record("4_reentry_counts", "PASS" if ok4 else "FAIL",
                   {"first": rb1["outcome"], "reentry": rb2["outcome"],
                    "used_after_reentry": s_b2.get("travel"),
                    "hint_after_reentry": s_b2map.get("hintTravel"),
                    "third": rb3["outcome"], "third_toast": rb3.get("toast"),
                    "shot": "shots/merged114/drive_merged_B2_cafe_again_sheet.png / drive_114_B3_gift_blocked.png"})

            # ---------- Item 5 : next-day reset (continue game B) ----------
            used_before_adv = d.st().get("travel")
            adv = d.advance_day("B_advance")
            s5 = d.st()
            ok5 = adv["ok"] and (used_before_adv or {}).get("used") == 2 \
                and s5.get("remain") == 2 \
                and s5.get("hintTravel") == "今日出行：仲可以去 2 個地方" \
                and (s5.get("travel") or {}).get("used") == 0
            record("5_next_day_reset", "PASS" if ok5 else "FAIL",
                   {"advance": {k: adv[k] for k in ("ok",) if k in adv},
                    "used_before": used_before_adv,
                    "day_before": adv["before"]["day"], "day_after": s5.get("day"),
                    "travel": s5.get("travel"), "hint": s5.get("hintTravel"),
                    "error": adv.get("error"),
                    "log_tail": adv.get("log", [])[-6:],
                    "shot": "shots/merged114/drive_merged_B_advance_nextday.png"})

            # ---------- Item 6 : encounter still works ----------
            d.new_game_slot3("C_fresh")
            enc = {"found": False, "days_tried": [], "detail": []}
            for day_try in range(4):
                st0 = d.st()
                probe = d.enter_loc("hospital", f"C{day_try}_probe_hosp")
                st1 = d.st()
                presence = ((st1.get("starDay") or {}).get("presence") or {})
                trig0 = (st1.get("starDay") or {}).get("triggered", 0)
                pilot_locs = []
                for loc, stars in presence.items():
                    for sid in (stars or []):
                        if sid in PILOT:
                            pilot_locs.append((loc, sid))
                enc["days_tried"].append({"day": st1.get("day"), "probe": probe["outcome"],
                                          "presence": presence, "pilot_locs": pilot_locs})
                d.back_to_map()
                if not pilot_locs:
                    adv2 = d.advance_day(f"C{day_try}_adv")
                    if not adv2["ok"]:
                        enc["detail"].append({"day": day_try, "no_pilot": True,
                                              "advance_log": adv2.get("log", [])[-8:]})
                        break
                    continue
                loc, sid = pilot_locs[0]
                st_pre = d.st()
                r_star = d.enter_loc(loc, f"C{day_try}_star_{loc}")
                st_post = d.st()
                trig1 = (st_post.get("starDay") or {}).get("triggered", 0)
                fired = (r_star["outcome"].startswith("dialogue")
                         and r_star.get("trig_delta", 0) >= 1) or trig1 > trig0
                enc["found"] = fired
                enc["detail"].append({"day": st_pre.get("day"), "loc": loc, "star": sid,
                                      "enter": r_star["outcome"],
                                      "trig_before": trig0, "trig_after": trig1,
                                      "used_after": st_post.get("travel"),
                                      "sheet_after_dlg": st_post.get("sheetOn"),
                                      "stage_chars": r_star.get("dlg_last", {}).get("chars") if isinstance(r_star.get("dlg_last"), dict) else None})
                d.back_to_map()
                break
            record("6_encounter", "PASS" if enc["found"] else "FAIL",
                   {"found": enc["found"], "days_tried": enc["days_tried"],
                    "detail": enc["detail"],
                    "shot": "shots/merged114/drive_merged_C*_star_*_afterdlg_*.png"})

            print("pageerrors:", len(LOG["errors"]), LOG["errors"][:5])
            print("console errors:", len(LOG["console_errors"]), LOG["console_errors"][:5])
            print("failed requests:", len(LOG["failed_requests"]))
            b.close()
    finally:
        stop(srv)

    with open(os.path.join(HERE, "drive_merged_114.json"), "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=1)
    print("WROTE", os.path.join(HERE, "drive_merged_114.json"))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        with open(os.path.join(HERE, "drive_merged_114.json"), "w", encoding="utf-8") as f:
            json.dump(LOG, f, ensure_ascii=False, indent=1)
        raise
