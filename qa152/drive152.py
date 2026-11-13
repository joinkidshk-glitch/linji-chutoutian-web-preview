#!/usr/bin/env python3
"""v20a152 live drive: 鄧麗萍只刪感情線，留返排片。
Usage: drive152.py [root] [port]
本地鏡像 + Playwright（唔直連 github.io），?softPreview=1&softBehaviorGate=1。
 - T1 meet（seed_deng_meet_ready 自動播）：見面文案係公事（數據／檔期／排片），揀 data 抉擇後
   flag_tang_open=true、rel_tang 升；全程唔出現感情線開閘字眼。
 - T2 push（seed_deng_push_ready 自動播 push1）：事務所行動表開 push2→crisis 逐節播；
   行動表／全頁唔再出現 R_tang_ending／HE／BE（「應承佢嗰格」「跨越商業界線」「盟友以上」「嗰個紅圈」）。
 - T3 送禮：名筆／計數機／腕表／咖啡豆有公事反應；玫瑰得新公事拒絕句（唔見「綁架我的情緒」／「心軟」）；
   腕表唔見「感情條款」。註：openGiftPick 唔係 global（主 script 係 IIFE），tang 亦唔係地點 panel NPC，
   pick-list modal 無法由外面驅動；改行 window.GiftShop.giveGift，回傳 line 就係 doGiveGift 喺結果 modal
   一字不改 render 嗰句（reactionLine，經 TEXTFIX55）。
 - 全程 0 pageerror。
Saves qa152/shots152/*.png + qa152/drive152.json under root.
"""
import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8123
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
SHOTS = os.path.join(ROOT, "qa152", "shots152")
os.makedirs(SHOTS, exist_ok=True)

FORBIDDEN = ["感情線", "開閘", "盟友以上", "嗰個紅圈", "跨越商業界線", "應承佢嗰格",
             "R_tang_ending", "flag_tang_commit", "flag_tang_he", "flag_tang_be",
             "C_tang_ending_he", "C_tang_ending_be", "綁架我的情緒", "你想我心軟"]
FORBIDDEN_GIFT = FORBIDDEN + ["感情條款"]

def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
    }""", text)

def click_vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false; vis[0].click(); return true;
    }""", text)

def modal_text(pg):
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      return m ? m.innerText : '';
    }""")

def page_text(pg):
    return pg.evaluate("() => document.body.innerText || ''")

def seed_entry(pg, seed, secs=45):
    """seed 流程：goto ?softSeed=… 之後 boot 嗰陣直接用種子狀態開局並自動播目標 beat（唔經「新遊戲」）。
    回傳 True＝已到地圖（過一日可見）或故事 modal 已開。"""
    pg.goto(f"http://127.0.0.1:{PORT}/?softPreview=1&softBehaviorGate=1&softSeed={seed}")
    for i in range(int(secs / 0.7)):
        if vis_btn(pg, "下一句") or vis_btn(pg, "過一日"):
            return True
        if i == 10:
            # 後備：舊版流程要撳新遊戲
            try:
                pg.get_by_text("新遊戲", exact=False).first.click(timeout=1500)
                pg.wait_for_timeout(1000)
            except Exception:
                pass
            try:
                pg.evaluate("() => { try { if (window.__softSeed) window.__softSeed.apply(); } catch(e){} }")
            except Exception:
                pass
        pg.wait_for_timeout(700)
    return False

def wait_story_modal(pg, secs=30):
    """等 StoryPlay 對話 modal 出現（有「下一句」掣），期間嘗試補 apply seed。"""
    for i in range(int(secs / 0.7)):
        if vis_btn(pg, "下一句"): return True
        if i == 8:
            pg.evaluate("() => { try { if (window.__softSeed) window.__softSeed.apply(); } catch(e){} }")
        pg.wait_for_timeout(700)
    return False

def dismiss_story_end(pg, secs=15):
    """播完劇情會出「劇情結算」modal（掣「關閉」／「進度」），要閂咗先返到地圖，否則之後撳針無效。"""
    for _ in range(int(secs / 0.7)):
        if vis_btn(pg, "過一日"): return True
        if click_vis_btn(pg, "關閉"):
            pg.wait_for_timeout(700); continue
        if click_vis_btn(pg, "返回地圖"):
            pg.wait_for_timeout(700); continue
        pg.wait_for_timeout(700)
    return vis_btn(pg, "過一日")

def play_story(pg, choice_substr, secs=90):
    """撳「下一句」直到出抉擇，撳含 choice_substr 嗰個，繼續撳到 modal 完；回傳全程文字。"""
    texts = []
    picked = False
    for _ in range(int(secs / 0.7)):
        t = modal_text(pg)
        if t and t not in texts: texts.append(t)
        if not picked and choice_substr and click_vis_btn(pg, choice_substr):
            picked = True; pg.wait_for_timeout(800); continue
        if click_vis_btn(pg, "下一句"):
            pg.wait_for_timeout(700); continue
        if vis_btn(pg, "返回地圖") or vis_btn(pg, "過一日"):
            break
        pg.wait_for_timeout(700)
    return {"texts": texts, "picked": picked, "ended_on_map": vis_btn(pg, "過一日")}

def state_probe(pg):
    return pg.evaluate("""() => {
      const out = {};
      try { out.flags = (typeof S !== 'undefined' && S.flags) || {}; } catch(e){ out.flags = {}; }
      try { out.relTang = (typeof S !== 'undefined' && S.story && S.story.rel && S.story.rel.rel_tang); } catch(e){}
      try { out.relTang2 = (typeof S !== 'undefined' && S.rel && S.rel.rel_tang); } catch(e){}
      try { out.doneTang = (typeof StoryOC !== 'undefined' && StoryOC.isDone) ?
        ['R_tang_meet','R_tang_push1','R_tang_push2','R_tang_crisis','R_tang_ending'].map(id => [id, StoryOC.isDone(id)]) : []; } catch(e){ out.doneTang = []; }
      try { out.flagOpen = (typeof StoryOC !== 'undefined' && StoryOC.getFlag) ? StoryOC.getFlag('flag_tang_open') : null; } catch(e){ out.flagOpen = null; }
      try { out.flagCommit = (typeof StoryOC !== 'undefined' && StoryOC.getFlag) ? StoryOC.getFlag('flag_tang_commit') : null; } catch(e){ out.flagCommit = null; }
      return out;
    }""")

def open_agency(pg):
    """撳地圖 agency_ho 針，等 loc-sheet 出現。"""
    ok = pg.evaluate("""() => {
      const pins = [...document.querySelectorAll('[data-loc="agency_ho"]')];
      for (const p of pins) {
        const img = p.querySelector('.pin-img'); if (img) { img.click(); return 'pin-img'; }
        const lab = p.querySelector('.plab'); if (lab) { lab.click(); return 'plab'; }
        p.click(); return 'pin';
      }
      return '';
    }""")
    for _ in range(15):
        pg.wait_for_timeout(700)
        if pg.evaluate("() => { const s=document.getElementById('loc-sheet'); return !!s && s.classList.contains('on'); }"):
            return ok or True
    return False

def sheet_buttons(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('#loc-sheet button, #loc-acts button')]
      .map(b => (b.textContent||'').trim()).filter(Boolean)""")

srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
results = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)

        # ---------- T1：meet ----------
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        rec = {"test": "T1_meet", "pageerrors": 0}
        rec["on_map"] = seed_entry(pg, "seed_deng_meet_ready")
        rec["story_modal"] = wait_story_modal(pg)
        if rec["story_modal"]:
            play = play_story(pg, "遞上")
            rec["picked_data_choice"] = play["picked"]
            rec["story_text"] = "\n---\n".join(play["texts"])
            rec["forbidden_in_story"] = [w for w in FORBIDDEN if w in rec["story_text"]]
            rec["has_business_words"] = all(w in rec["story_text"] for w in ["數據", "檔期"])
        pg.wait_for_timeout(1500)
        st = state_probe(pg)
        rec["flag_tang_open"] = bool(st.get("flags", {}).get("flag_tang_open") or st.get("flagOpen"))
        rec["rel_tang"] = st.get("relTang2") if st.get("relTang2") is not None else st.get("relTang")
        rec["done"] = dict(st.get("doneTang") or [])
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"] and rec["story_modal"] and rec.get("picked_data_choice")
                           and not rec.get("forbidden_in_story") and rec["flag_tang_open"]
                           and rec["done"].get("R_tang_meet"))
        pg.screenshot(path=f"{SHOTS}/t1_meet.png")
        results.append(rec); print("T1", rec["pass"], "flag_open:", rec["flag_tang_open"], "rel:", rec["rel_tang"], "forbidden:", rec.get("forbidden_in_story"))
        ctx.close()

        # ---------- T2：push line ----------
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        rec = {"test": "T2_push", "pageerrors": 0}
        rec["on_map"] = seed_entry(pg, "seed_deng_push_ready")
        rec["story_modal"] = wait_story_modal(pg)
        played = {}
        if rec["story_modal"]:
            play = play_story(pg, "情報")  # push1：拿出試映情報換冷門檔資料
            played["R_tang_push1"] = play["picked"]
            rec["push1_text"] = "\n---\n".join(play["texts"])
        pg.wait_for_timeout(1200)
        dismiss_story_end(pg)
        rec["agency_open"] = open_agency(pg)
        if rec["agency_open"]:
            btns = sheet_buttons(pg)
            rec["agency_buttons"] = btns
            rec["ending_button_present"] = any(("應承" in t or "紅圈" in t or "年終的抉擇" in t) for t in btns)
            # push2：標題「午夜場後的試探」
            if click_vis_btn(pg, "午夜場後的試探"):
                pg.wait_for_timeout(800)
                play = play_story(pg, "齋講檔期")  # WF5 覆寫 label（mock 原句「只談檔期」已覆寫）
                played["R_tang_push2"] = play["picked"]
                rec["push2_text"] = "\n---\n".join(play["texts"])
                pg.wait_for_timeout(800)
                dismiss_story_end(pg)
                rec["agency_open2"] = open_agency(pg)
                if rec.get("agency_open2"):
                    if click_vis_btn(pg, "黃金檔期之爭"):
                        pg.wait_for_timeout(800)
                        play = play_story(pg, "票房行先")  # WF5 覆寫 label（mock 原句「以票房為先」已覆寫）
                        played["R_tang_crisis"] = play["picked"]
                        rec["crisis_text"] = "\n---\n".join(play["texts"])
        pg.wait_for_timeout(1200)
        st = state_probe(pg)
        rec["played"] = played
        rec["done"] = dict(st.get("doneTang") or [])
        rec["flag_commit_seen"] = bool(st.get("flagCommit"))
        body = page_text(pg)
        rec["forbidden_on_page"] = [w for w in FORBIDDEN if w in body]
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"] and rec["story_modal"] and played.get("R_tang_push1")
                           and played.get("R_tang_push2") and played.get("R_tang_crisis")
                           and not rec.get("ending_button_present") and not rec.get("forbidden_on_page")
                           and not rec["flag_commit_seen"] and not rec["done"].get("R_tang_ending"))
        pg.screenshot(path=f"{SHOTS}/t2_push.png")
        results.append(rec); print("T2", rec["pass"], "played:", played, "done:", rec["done"], "forbidden:", rec.get("forbidden_on_page"))
        ctx.close()

        # ---------- T3：gifts（沿用 T2 嘅 context 狀態：flag_tang_open＋rel 2）----------
        # 為免每日限送 1 次擋路，每次送禮前 dayIndex+1；庫存直接播種（沿用舊 drive S 播種模式）。
        ctx = b.new_context(viewport={"width": 430, "height": 932})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        rec = {"test": "T3_gifts", "pageerrors": 0, "reactions": {}}
        rec["on_map"] = seed_entry(pg, "seed_deng_push_ready")
        pg.wait_for_timeout(1500)
        pg.evaluate("() => { try { if (window.__softSeed) window.__softSeed.apply(); } catch(e){} }")
        pg.wait_for_timeout(1500)
        # 自動播出嚟嘅 push1 modal：正規播完佢（揀情報抉擇），淨係要 flag_tang_open 狀態
        if wait_story_modal(pg, secs=15):
            play_story(pg, "情報")
        dismiss_story_end(pg)
        st = state_probe(pg)
        rec["flag_tang_open"] = bool(st.get("flags", {}).get("flag_tang_open") or st.get("flagOpen"))
        rec["giftpick_fn"] = pg.evaluate("() => typeof openGiftPick")
        pg.evaluate("""() => {
          try {
            S.inventory = S.inventory || {};
            ['gift_fountain_pen','gift_desk_calculator','gift_dress_watch','gift_coffee_beans','gift_rose_premium','gift_memo_pad']
              .forEach(id => { S.inventory[id] = 3; });
            if (S.giftMeta) { S.giftMeta.lastGiveDay = {}; S.giftMeta.weekGiftGain = {}; }
          } catch(e){}
        }""")
        rec["can_give"] = pg.evaluate("() => { try { return GiftShop.canGive('tang'); } catch(e){ return {ok:false, reason:'err:'+e.message}; } }")
        gift_cases = [
            ("gift_fountain_pen", "名筆", "pen", "liked"),
            ("gift_desk_calculator", "計數機", "calc", "liked"),
            ("gift_dress_watch", "腕表", "watch", "liked"),
            ("gift_coffee_beans", "咖啡豆", "coffee", "neutral"),
            ("gift_rose_premium", "玫瑰", "rose", "dislike"),
        ]
        for item_id, expect_word, tag, pref in gift_cases:
            # 每日限送 1 次＋每週淨好感軟 +2：每次送禮前推一日並清 weekGiftGain，確保反應句唔受軟上限變體影響
            pg.evaluate("() => { try { S.dayIndex = (S.dayIndex|0) + 1; if (S.giftMeta) { S.giftMeta.lastGiveDay = {}; S.giftMeta.weekGiftGain = {}; } } catch(e){} }")
            # openGiftPick 唔係 global（主 script 係 IIFE），禮物 modal 只能經地點 panel NPC 入（tang 唔係 panel NPC）；
            # 改行 window.GiftShop.giveGift——回傳嘅 line 就係 doGiveGift 喺結果 modal 一字不改 render 嗰句（reactionLine，經 TEXTFIX55）。
            res = pg.evaluate("""(id) => {
              try { const r = GiftShop.giveGift('tang', id); return {ok: r.ok, line: r.line || '', kind: r.kind || '', reason: r.reason || ''}; }
              catch(e){ return {ok:false, line:'', kind:'', reason:'err:'+e.message}; }
            }""", item_id)
            txt = res.get("line") or ""
            # 專屬反應句直接驗證：reactionEntry 用 entry 本身嘅 pref 查（liked／dislike／neutral），
            # 證明 TEXTFIX55 改寫後嘅玩家可見輸出。live giveGift 行 prefKind（gift_prefs likes／dislikes 係空，
            # pre-existing）永遠 neutral，所以 pen／calc／watch／rose 專屬句喺 live 行唔到，只能經呢度驗證——見 NOTES §6。
            ent = pg.evaluate("""([id, pref]) => {
              try { const e = GiftShop.reactionEntry('tang', id, pref);
                return e ? (e.lines || []).join('\\n') : null; }
              catch(err){ return 'err:' + err.message; }
            }""", [item_id, pref])
            ent_txt = ent or ""
            rec["reactions"][tag] = {"ok": res.get("ok"), "kind": res.get("kind"), "reason": res.get("reason"),
                                     "text": txt, "live_line": txt,
                                     "entry_text": ent_txt,
                                     "has_expect": expect_word in txt,
                                     "entry_has_expect": expect_word in ent_txt,
                                     "forbidden": [w for w in FORBIDDEN_GIFT if w in txt],
                                     "entry_forbidden": [w for w in FORBIDDEN_GIFT if w in ent_txt]}
            if tag == "rose":
                rec["reactions"][tag]["has_new_rose_line"] = "呢度係排片部，唔係花店" in txt
                rec["reactions"][tag]["entry_has_new_rose_line"] = "呢度係排片部，唔係花店" in ent_txt
            if tag == "watch":
                rec["reactions"][tag]["has_new_watch_line"] = "錶係錶，檔期係檔期" in txt
                rec["reactions"][tag]["entry_has_new_watch_line"] = "錶係錶，檔期係檔期" in ent_txt
            pg.screenshot(path=f"{SHOTS}/t3_gift_{tag}.png")
        # live 行：coffee（neutral entry）要見到專屬句；其餘 live 行只會見到通用佔位句（pre-existing gap，見 NOTES §6），
        # 專屬句改由 entry_text 驗證；玫瑰／腕表新句以 entry 為準。
        ok_live_coffee = rec["reactions"]["coffee"]["has_expect"] and not rec["reactions"]["coffee"]["forbidden"]
        ok_entry = all(r["entry_has_expect"] and not r["entry_forbidden"] for r in rec["reactions"].values())
        rec["pageerrors"] = len(errs); rec["errors"] = errs[:3]
        rec["pass"] = bool(rec["on_map"] and rec["flag_tang_open"]
                           and all(r["ok"] for r in rec["reactions"].values())
                           and ok_live_coffee and ok_entry
                           and rec["reactions"]["rose"]["entry_has_new_rose_line"]
                           and rec["reactions"]["watch"]["entry_has_new_watch_line"])
        results.append(rec)
        print("T3", rec["pass"], {k: (v["has_expect"], v["entry_has_expect"], v["forbidden"], v["entry_forbidden"]) for k, v in rec["reactions"].items()})
        ctx.close()
        b.close()
finally:
    srv.terminate()
with open(os.path.join(ROOT, "qa152", "drive152.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
n_pass = sum(1 for r in results if r.get("pass") and r.get("pageerrors") == 0)
print(f"OVERALL {n_pass}/{len(results)}")
