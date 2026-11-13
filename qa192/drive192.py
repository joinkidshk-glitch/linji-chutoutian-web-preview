# -*- coding: utf-8 -*-
"""v20a192 實駕：修 v188 review B1＋C1–C4 嘅逐項 live 驗證。
方法照抄獨立 review drive_review188.py／b.py（新遊戲 → 播種 wrapHistory →
debugForceSeasonWindow 建 pack → 請柬 → 出席 → 舞台 → 結果卡 → 報紙 queue；
Math.random 係常數；播種存檔直接寫 localStorage；主 script 係 IIFE，行 UI 路徑）。
對象：~/workspace/linji-work192 index.html（工作副本，唯讀 serve）。
重點：
- B1：8 款 win 報紙模板逐款驗——每媒介 won × Math.random 0.4（_01）／0.7（_02），
  用 queue 項 templateId 對準模板 id，headline／dek 逐字對新文案＋禁字掃描。
- C1：tv nominated 結果卡 lead_m loseLine 逐字＝「名單滑過你個名——入圍咗，未抱盃。仲有下一場。」
- C2：film／tv 閘句逐字驗；音樂 gallery 請柬零「未唱過歌」。
- C3：雙格 pack 舞台白牌（focus）＝結果卡第一行 kick（電影／電視／音樂各驗）。
- C4：gallery 請柬「今晚獎項」行＝全 slate（4 格／音樂 3 格）＋（觀禮）。
環境：Playwright venv /home/hatch/pwenv49/bin/python、headless shell chromium、
本地鏡像＋python3 -m http.server（port 19290）、viewport 430×932／430×700。
"""
import hashlib, json, os, re, subprocess, sys, time, urllib.request
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v188")
from drive_review188 import (day_idx, parse_ads, SEED_JS, click_btn,
                             click_exact, modal_info, stage_state, watch_stage, result_dom)
from drive_review188b import SEED2_JS, parse_gig36
from playwright.sync_api import sync_playwright

# 注意：唔可以直接 import review 嘅 new_game——佢硬編 PORT 18892（review 嗰邊 serve）。
# 呢度自備一個完全相同流程、指去本地 PORT 19290 嘅版本。

ROOT = "/home/hatch/workspace/linji-work192"
OUT = "/home/hatch/workspace/linji-work192/qa192"
SHOTS = os.path.join(OUT, "shots192")
PORT = 19290
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
os.makedirs(SHOTS, exist_ok=True)

BANNED = ["三句對白", "茶餐廳食面", "臨記生涯", "不殺之恩", "一句收工了", "綠葉",
          "和音", "合唱單曲", "涼茶", "跌低眼鏡", "特別獎", "臨記組", "最受歡迎"]
# templateId → （headline, dek）逐字期望（{playerName} 已填做阿偉）
NP_EXPECT = {
    "np_win_film_01": ("維港影藝獎揭曉 阿偉 奪演員獎",
                       "阿偉憑實力跑出，評審讚其眼神有戲，開始有觀眾記得佢個名。"),
    "np_win_film_02": ("影藝獎夜 阿偉奪獎成焦點",
                       "維港影藝獎側記：金禧大酒店大禮堂嗰晚，阿偉奪得演員獎，街坊笑言個樣好抵死，聲望再下一城。"),
    "np_win_tv_01": ("星河台慶夜 演員獎爆冷由阿偉奪得",
                     "廠景熬出頭！阿偉獲獎時多謝台前幕後，而家連星河電視台高層都開始留意佢。"),
    "np_win_tv_02": ("台慶夜 阿偉奪獎贏街坊票",
                     "星河台慶・年度頒獎夜側記：阿偉拿下演員獎，掌聲蓋不住，聲望再下一城。"),
    "np_win_music_01": ("星河金碟夜 阿偉奪獎跑出",
                        "錄音室熬出頭！阿偉憑歌聲獲獎，評審指其聲線有市井煙火味，喺行內漸漸有口碑。"),
    "np_win_music_02": ("金碟夜 阿偉奪獎 樂壇多把靚聲",
                        "星河金碟夜側記：金禧大酒店大禮堂嗰晚，阿偉憑歌聲奪獎，街坊話聽聲就認得，聲望悄然提升。"),
    "np_win_ad_01": ("維港街招賞 阿偉跑出",
                     "憑廣告突圍！阿偉獲評夠貼地，有街坊味，奪獎殊不容易，街坊開始記得佢個樣。"),
    "np_win_ad_02": ("街外一鏡 阿偉奪獎贏掌聲",
                     "維港街招・年度廣告賞側記：金禧大酒店大禮堂嗰晚，阿偉奪得廣告獎，聲望穩步上揚，商戶開始留意。"),
}
GATE_FILM_TV = "嗰年未做過主角／配角級作品，入圍唔到演員獎"
SLATE = {
    "award_harbour_film": "今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）",
    "award_singho_tv": "今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）",
    "award_golddisc_music": "今晚獎項：最佳男歌手、最佳女歌手、最佳新人獎（觀禮）",
    "award_harbour_ad": "今晚獎項：最佳廣告男主角、最佳廣告女主角、最佳廣告男配角、最佳廣告女配角（觀禮）",
}

def new_game(pg):
    pg.goto(f"http://127.0.0.1:{PORT}/index.html")
    pg.wait_for_timeout(3000)
    click_btn(pg, "新遊戲", 1500); pg.wait_for_timeout(600)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) b.click(); }""")
    pg.wait_for_timeout(1000)
    for t in ["覆蓋", "確定", "確認"]:
        click_btn(pg, t, 700)
    click_btn(pg, "跳過教學", 1200)
    click_btn(pg, "開始寫手帳", 1200)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1000)
    except Exception: pass
    click_btn(pg, "確定出發", 1200)
    for _ in range(4):
        if not click_btn(pg, "確定", 700) and not click_btn(pg, "確認", 700) \
           and not click_btn(pg, "好", 700) and not click_btn(pg, "知道了", 700):
            break
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")

def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    assert hashlib.sha256(body).hexdigest()[:12] == hashlib.sha256(
        open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest()[:12]
    return p

def stop(p):
    try:
        p.send_signal(subprocess.signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def snap(pg, name):
    try: pg.screenshot(path=os.path.join(SHOTS, name)); return True
    except Exception: return False

# literal 播種（照抄 review drive_review188c.py SEED3）：2 部非主角／非配角電影作品
# （動作組臨記＋替身），作品數＋雙軌夠數，先至觸發角色閘句。gig 池本身得 1 部
# film extra，經 SEED2 播唔齊 2 部——唔係 game bug，係播種池問題。
SEED3_JS = """(o) => {
  const mk = (g) => ({ gigId: g.id, title: g.title, type: g.type, workTitle: g.workTitle,
    roleLabel: g.roleLabel, roleScale: g.roleScale, year: o.year, totalDays: 2,
    pay: g.pay, fame: 0, popularity: 0, wrappedDay: o.wrapDay, rating: '順利殺青' });
  const wraps = [
    mk({ id:'gig_exodus_film_hand', title:'《江邊小鎮》動作組熟手（急聘）', type:'電影',
         workTitle:'江邊小鎮', roleLabel:'動作組熟手臨記', roleScale:'film_action_extra', pay:2900 }),
    mk({ id:'gig_br89_stunt_ngai', title:'情報通告：《鐵血柔情》替身缺位', type:'電影',
         workTitle:'鐵血柔情', roleLabel:'情報通告・替身位', roleScale:'film_stunt', pay:1000 })
  ];
  S.dayIndex = o.dayIndex;
  S.story = S.story || {}; S.story.done = {}; S.story.flags = S.story.flags || {}; S.story.rel = S.story.rel || {};
  S.awardsFlags = {}; S.pendingAwardPack = null;
  S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
  S.fame = 45; S.stage = 60; S.acting = 60; S.industryCreditDelta = 50;
  S.money = 5000; S.stress = 0; S.flags = S.flags || {};
  S.wrapHistory = wraps; S.newspaperQueue = []; S.news = S.news || [];
  S.story.gigCount = wraps.length;
  return { day: S.dayIndex, wraps: wraps.length };
}"""

def force_pack(pg, cer):
    return pg.evaluate("""(o) => {
      try {
        const p = window.__awards.debugForceSeasonWindow(o.id, {});
        if (!p) return {error:'no pack'};
        return {ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome, tier: p.tier,
          cats: (p.categories||[]).map(x => ({id:x.id||'', outcome:x.outcome, label:x.label,
            score: x.score!=null?+x.score.toFixed(4):null, line:x.line||'', rep:x.repWorkTitle||''}))};
      } catch(e) { return {error: String(e)}; } }""", {"id": cer})

def invite_line(body):
    for ln in (body or "").splitlines():
        if ln.strip().startswith("今晚獎項"): return ln.strip()
    return ""

def newspaper_queue(pg):
    return pg.evaluate("() => ((S && S.newspaperQueue) || []).map(n => ({source:n.source||'', headline:n.headline||'', dek:n.dek||'', clipLabel:n.clipLabel||'', templateId:n.templateId||''}))")

# name, ceremony, year, H, fame, credit, roles, payOverride, rand, mode, extra(roles-seed2?)
# mode: won01/won02 用 templateId 驗 B1；nom 驗 C1＋C3；gate 驗 C2／C4
CASES = [
    ("b1_film_01_932",  "award_harbour_film",   1990, 932, 45, 50, {"film_lead":2,"film_sup":1,"tv_lead":2}, None,  0.4, "won", None),
    ("b1_film_02_932",  "award_harbour_film",   1990, 932, 45, 50, {"film_lead":2,"film_sup":1,"tv_lead":2}, None,  0.7, "won", None),
    ("b1_tv_01_932",    "award_singho_tv",      1990, 932, 45, 50, {"tv_lead":2,"tv_sup":1,"film_lead":2},  None,  0.4, "won", None),
    ("b1_tv_02_932",    "award_singho_tv",      1990, 932, 45, 50, {"tv_lead":2,"tv_sup":1,"film_lead":2},  None,  0.7, "won", None),
    ("b1_music_01_932", "award_golddisc_music", 1990, 932, 45, 50, {"rec":4,"film_lead":2},                None,  0.4, "won", None),
    ("b1_music_02_700", "award_golddisc_music", 1990, 700, 45, 50, {"rec":4,"film_lead":2},                None,  0.7, "won", None),
    ("b1_ad_01_932",    "award_harbour_ad",     1991, 932, 45, 50, {"ad_lead":2,"ad_sup":1,"film_lead":2}, 25000, 0.4, "won", None),
    ("b1_ad_02_932",    "award_harbour_ad",     1991, 932, 45, 50, {"ad_lead":2,"ad_sup":1,"film_lead":2}, 25000, 0.7, "won", None),
    ("c1_tv_lose_932",  "award_singho_tv",      1990, 932, 25, 0,  {"tv_lead":1,"tv_sup":1},               None,  0.4, "nom", None),
    ("c2_film_gate_932","award_harbour_film",   1990, 932, 45, 50, {"film_extra":2},                      None,  0.4, "gate", "film3"),
    ("c2_tv_gate_932",  "award_singho_tv",      1990, 932, 45, 50, {"tv_extra":2},                        None,  0.4, "gate", "tv"),
    ("c2_music_gate_932","award_golddisc_music",1990, 932, 45, 50, {"film_lead":2},                       None,  0.4, "gate", "music"),
    ("c4_film_gal_932", "award_harbour_film",   1990, 932, 45, 50, {"film_extra":2},                      None,  0.4, "gate", "film3"),
    ("c4_music_gal_932","award_golddisc_music", 1990, 932, 45, 50, {"film_lead":2},                       None,  0.4, "gate", "music"),
    ("c4_tv_gal_932",   "award_singho_tv",      1990, 932, 25, 0,  {"tv_sup":1},                          None,  0.4, "gate", "tv"),
]

def run_case(pw, cfg, ads, extra, results):
    name, cer, year, H, fame, credit, roles, payov, rnd, mode, gate_kind = cfg
    print(f"== {name} ({cer} {year} rand={rnd} mode={mode}) ==", flush=True)
    out = {"case": name, "ceremony": cer, "year": year, "mode": mode, "rand": rnd, "checks": {}}
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            c = out["checks"]
            if not new_game(pg):
                c["new_game"] = False; out["verdict"] = "ERROR"; results[name] = out; return
            c["new_game"] = True
            if gate_kind == "film3":
                sd = pg.evaluate(SEED3_JS, {"dayIndex": day_idx(year, 10, 20), "wrapDay": day_idx(year, 9, 15),
                    "year": year})
                c["seed_roles_found"] = sd.get("wraps") == 2
            elif gate_kind in ("film", "tv"):
                sd = pg.evaluate(SEED2_JS, {"dayIndex": day_idx(year, 10, 20), "wrapDay": day_idx(year, 9, 15),
                    "year": year, "fame": fame, "credit": credit, "roles": roles, "extra": extra})
                c["seed_roles_found"] = all(len(sd["picked"].get(k, [])) == n for k, n in roles.items())
            else:
                sd = pg.evaluate(SEED_JS, {"dayIndex": day_idx(year, 10, 20), "wrapDay": day_idx(year, 9, 15),
                    "year": year, "fame": fame, "credit": credit, "roles": roles, "ads": ads, "payOverride": payov})
                c["seed_roles_found"] = all(len(sd["picked"].get(k, [])) == n for k, n in roles.items())
            out["seed"] = sd
            pg.evaluate("(v) => { Math.random = () => v; return true; }", rnd)
            pack = force_pack(pg, cer)
            out["pack"] = pack
            c["pack_built"] = "error" not in pack
            if "error" in pack:
                out["verdict"] = "ERROR"; results[name] = out; print("  ERROR pack", pack, flush=True); return
            pg.evaluate("() => { try { window.__awards.present(); } catch(e){} }")
            pg.wait_for_timeout(1000)
            inv = modal_info(pg)
            out["invite"] = inv
            c["invite_shown"] = bool(inv.get("visible"))
            body = inv.get("body") or ""
            snap(pg, f"{name}_invite.png")
            if mode == "gate":
                got = invite_line(body)
                out["invite_awards_line"] = got
                if name.startswith("c4_"):
                    c["c4_full_slate"] = got == SLATE[cer]
                    c["c4_no_contest_wording"] = "你爭" not in body
                # 角色閘句只喺 c2 專案驗：c4_tv_gal 得 1 部作品，數目閘先行係正確，
                # 唔可以要求角色閘句出現（review tv_suponly 同一道理）。
                if name.startswith("c2_") and gate_kind in ("film", "tv", "film3"):
                    c["c2_gate_line_verbatim"] = GATE_FILM_TV in body
                    c["c2_gate_tier_gallery"] = "旁聽席" in body
                if gate_kind == "music":
                    c["c2_music_no_dead_line"] = "未唱過歌" not in body
                out["pageerrors"] = errs[:8]
                c["zero_pageerror"] = len(errs) == 0
                out["verdict"] = "PASS" if all(c.values()) else "FAIL"
                results[name] = out
                print(f"  {out['verdict']} fail={json.dumps({k:v for k,v in c.items() if not v}, ensure_ascii=False)}", flush=True)
                return
            # 出席 → 舞台
            if not click_btn(pg, "出席", 900):
                c["attend_clicked"] = False; out["verdict"] = "FAIL"; results[name] = out; return
            c["attend_clicked"] = True
            pg.wait_for_timeout(400)
            c["stage_appears"] = bool(stage_state(pg).get("present"))
            w = watch_stage(pg, 26)
            out["watch"] = w
            c["stage_gone_after"] = bool(w.get("gone"))
            boards = w.get("boards") or []
            out["boards"] = boards
            c["board_present"] = len(boards) >= 1
            pg.wait_for_timeout(600)
            res = modal_info(pg)
            out["result_modal"] = {k: v for k, v in res.items() if k != "overflow"}
            c["result_shown"] = bool(res.get("visible"))
            rk = result_dom(pg)
            out["result_dom"] = rk
            cat_cards = [x for x in (rk.get("cards") or [])
                         if (x.get("kicker") or "").strip().startswith(("入圍", "得獎", "觀禮"))]
            rk_labels = [x["kicker"].split("·")[-1].strip() for x in cat_cards if "·" in x["kicker"]]
            out["result_kicker_order"] = [x.get("kicker") for x in cat_cards]
            snap(pg, f"{name}_result.png")
            # C3：舞台白牌（focus）＝結果卡第一行
            if boards and rk_labels:
                c["c3_first_row_is_focus"] = rk_labels[0] == boards[0]
            else:
                c["c3_first_row_is_focus"] = False
            out["c3_board_vs_first"] = {"board": boards[0] if boards else None,
                                        "first_kicker": rk_labels[0] if rk_labels else None}
            if mode == "nom":
                line_by = {x.get("label"): x.get("line") for x in pack.get("cats") or []}
                out["tv_lead_lose_line"] = line_by.get("最佳男主角")
                c["c1_lose_line_verbatim"] = line_by.get("最佳男主角") == "名單滑過你個名——入圍咗，未抱盃。仲有下一場。"
                c["c1_no_shuhai"] = "還有" not in (line_by.get("最佳男主角") or "")
            if mode == "won":
                c["outcome_won"] = pack.get("bestOutcome") == "won"
                click_btn(pg, "收下這晚", 900)
                pg.wait_for_timeout(900)
                nq = newspaper_queue(pg)
                out["newspaper"] = nq
                aw = [n for n in nq if n.get("templateId", "").startswith("np_win_")]
                out["newspaper_win_items"] = aw
                c["newspaper_has_win"] = len(aw) >= 1
                if aw:
                    item = aw[0]
                    exp = NP_EXPECT.get(item.get("templateId") or "")
                    out["newspaper_template"] = item.get("templateId")
                    if exp:
                        c["b1_headline_verbatim"] = item.get("headline") == exp[0]
                        c["b1_dek_verbatim"] = item.get("dek") == exp[1]
                    else:
                        c["b1_headline_verbatim"] = False
                        c["b1_dek_verbatim"] = False
                    c["b1_no_banned"] = not any(x in (item.get("headline") or "") or x in (item.get("dek") or "") for x in BANNED)
                    if item.get("templateId") == "np_win_music_01":
                        c["b1_music01_no_newcomer_word"] = "新人" not in (item.get("headline") or "") and "新人" not in (item.get("dek") or "")
                else:
                    c["b1_headline_verbatim"] = False
                    c["b1_dek_verbatim"] = False
                    c["b1_no_banned"] = False
            out["pageerrors"] = errs[:8]
            c["zero_pageerror"] = len(errs) == 0
            out["verdict"] = "PASS" if all(c.values()) else "FAIL"
            results[name] = out
            print(f"  {out['verdict']} fail={json.dumps({k:v for k,v in c.items() if not v}, ensure_ascii=False)}", flush=True)
            if errs: print(f"    pageerrors: {errs[:3]}", flush=True)
        except Exception as e:
            out["error"] = repr(e); out["verdict"] = "ERROR"; out["pageerrors"] = errs[:8]
            results[name] = out; print(f"  ERROR {e!r}", flush=True)
            try: snap(pg, f"err_{name}.png")
            except Exception: pass
        finally:
            ctx.close()
    finally:
        b.close()

def main():
    srv = serve()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
            src = r.read().decode("utf-8", "replace")
        ads = parse_ads(src)
        extra = parse_gig36(src, {"tv_regular_extra"})
        i = src.find('id:"gig_exodus_film_hand"')
        blk = src[i:i+2200]
        def fld(p):
            m = re.search(p, blk); return m.group(1) if m else ""
        pm = re.search(r"pay:\s*\[(\d+)\s*,\s*(\d+)\]", blk)
        extra.append({"id": "gig_exodus_film_hand", "type": "電影", "roleScale": "film_action_extra",
                      "roleLabel": fld(r"roleLabel:\s*\"([^\"]*)\""),
                      "pay": [int(pm.group(1)), int(pm.group(2))] if pm else None,
                      "title": fld(r"title:\s*\"([^\"]*)\""),
                      "workTitle": fld(r"workTitle:\s*\"([^\"]*)\""), "stars": 1, "year": 1990})
        print("ad gigs parsed:", len(ads), "extra gigs:", len(extra), flush=True)
        results = {}
        only = set(sys.argv[1:])
        cases = [cfg for cfg in CASES if not only or cfg[0] in only]
        with sync_playwright() as pw:
            for cfg in cases:
                run_case(pw, cfg, ads, extra, results)
        with open(os.path.join(OUT, "drive192.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        npass = sum(1 for r in results.values() if r.get("verdict") == "PASS")
        print(f"== SUMMARY {npass}/{len(results)} PASS ==", flush=True)
        for k, r in results.items():
            print(f"  {k}: {r.get('verdict')} fail={json.dumps({kk:vv for kk,vv in (r.get('checks') or {}).items() if not vv}, ensure_ascii=False)}", flush=True)
    finally:
        stop(srv)

if __name__ == "__main__":
    main()
