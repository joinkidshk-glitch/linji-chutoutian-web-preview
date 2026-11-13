# -*- coding: utf-8 -*-
"""v20a186 實駕：修 v184 review 新 C1——兩類獎項嗰陣，結果卡「同屆提名」行只出一次。
對象：本地工作副本 ~/workspace/linji-work186/index.html（serve 工作副本本身，content/＋assets/ 齊）。
場次：1991 星河台慶 award_singho_tv、nominated；fellows 葉敏芝／鍾楚凝／高俊傑（得主葉敏芝）。
Cases：430×932／430×700 各兩跑（ko_932a／ko_932b／ko_700a／ko_700b），每跑全新 context；LIVE 模式；
播種存檔直接寫 localStorage（key starVolunteer_map_v19w，slot 1 經新遊戲）。
斷言（每 case）：
  C1：結果卡 body 入面「同屆提名」出現次數 == 1（兩類／單類都係 1）；
      名單「葉敏芝《渡輪燈火》、鍾楚凝《星光夜》、高俊傑《潮汐家庭》」逐字出現 1 次；
      DOM：.psr-fellows63 節點只得 1 個，且喺最後一張類別卡之後、報紙卡之前（卡底獨立一行）；
      類別卡內冇 .psr-fellows63。
  守門：請柬「今晚獎項」行按 id 排序唔郁；結果卡 kicker 次序同請柬一致；唱名有高俊傑；0 pageerror。
pack 類別數係 pickN 隨機（1 或 2 類），四跑未必有齊兩種——主程式會按需加跑，直到兩類＋單類各至少一跑（上限 8 跑）。
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work186"
QA = os.path.join(ROOT, "qa186")
SHOTS = os.path.join(QA, "shots")
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 18690
LIST_TXT = "葉敏芝《渡輪燈火》、鍾楚凝《星光夜》、高俊傑《潮汐家庭》"

os.makedirs(SHOTS, exist_ok=True)


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


def stop(p):
    try:
        p.send_signal(subprocess.signal.SIGTERM)
        p.wait(timeout=5)
    except Exception:
        try:
            p.kill()
        except Exception:
            pass


def shot(pg, name):
    try:
        pg.screenshot(path=os.path.join(SHOTS, name))
        return True
    except Exception:
        return False


def click_text(pg, texts, wait=900):
    for t in texts:
        try:
            loc = pg.locator("button:has-text('" + t + "')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900)
                        pg.wait_for_timeout(wait)
                        return t
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
        pg.locator("#btn-confirm-plan").click(timeout=3000)
        pg.wait_for_timeout(1200)
    except Exception:
        pass
    click_text(pg, ["確定出發"], 1500)
    for _ in range(4):
        if not click_text(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    return pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")


def day_index(y, m, d):
    return (datetime.date(y, m, d) - datetime.date(1990, 1, 1)).days


def seed(pg, day):
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = 120; S.stage = 60; S.acting = 60;
      S.industryCreditDelta = 80;
      S.money = 5000; S.stress = 0;
      S.flags = S.flags || {};
      return { day: S.dayIndex };
    }""", {"day": day})


def modal_info(pg):
    return pg.evaluate("""() => {
      const m = document.querySelector('#modal');
      if (!m) return {visible:false};
      const cs = getComputedStyle(m);
      const r = m.getBoundingClientRect();
      const vis = r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden';
      if (!vis) return {visible:false};
      const h3 = (document.querySelector('#modal h3')||{}).textContent || '';
      const btns = [...document.querySelectorAll('#modal-btns button')].map(b => (b.textContent||'').trim()).filter(Boolean);
      return {visible:true, h3, btns, body: (m.innerText || '').slice(0, 1500)};
    }""")


def force_pack(pg, ceremony_id, tier):
    return pg.evaluate("""(o) => {
      try {
        const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
        if (!p) return { error: 'no pack' };
        const cats = (p.categories || []).map(c => ({
          id: c.id || '', outcome: c.outcome, label: c.label,
          fellows: (c.fellows63 || []).map(f => ({ star: f.star || '', starId: f.starId || '', title: f.title || '', assigned: !!f.assigned })) }));
        const ko = cats.some(c => c.fellows.some(f => f.starId === 'ko_chunkit' || f.star === '高俊傑'));
        return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome, tier: p.tier, cats, ko };
      } catch(e) { return { error: String(e) }; }
    }""", {"id": ceremony_id, "tier": tier})


def present(pg):
    pg.evaluate("() => { try { window.__awards.present(); } catch(e) { return String(e); } }")
    pg.wait_for_timeout(1000)
    return modal_info(pg)


def stage_state(pg):
    return pg.evaluate("""() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      return { present: true, caption: cap ? cap.textContent : '' };
    }""")


def watch(pg, secs=24):
    timeline = []
    last = None
    t0 = time.time()
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        cap = st.get("caption") or ""
        if cap != last:
            timeline.append({"t": round((time.time() - t0) * 1000), "caption": cap[:160]})
            last = cap
        pg.wait_for_timeout(90)
    return {"timeline": timeline, "totalMs": round((time.time() - t0) * 1000),
            "stageGone": not stage_state(pg).get("present")}


def result_dom(pg):
    return pg.evaluate("""() => {
      const sheet = document.querySelector('#modal .awd-sheet');
      if (!sheet) return { present: false };
      const fellows = [...sheet.querySelectorAll('.psr-fellows63')];
      const cards = [...sheet.querySelectorAll('.psr-card')];
      const kickers = [...sheet.querySelectorAll('.psr-card .psr-kicker')].map(k => (k.textContent||'').trim());
      const felInCard = fellows.filter(f => f.closest('.psr-card')).length;
      const order = [...sheet.querySelectorAll('.psr-cards > *')].map(el => el.className || el.tagName);
      const felIdx = order.findIndex(c => String(c).includes('psr-fellows63'));
      const pressIdx = order.findIndex(c => String(c).includes('psr-press'));
      const lastMetricIdx = order.map((c, i) => String(c).includes('psr-metrics') ? i : -1).filter(i => i >= 0).pop();
      return { present: true, fellowsCount: fellows.length, fellowsText: fellows.map(f => (f.textContent||'').trim()),
               felInCard, felIdx, pressIdx, lastMetricIdx, kickers, order };
    }""")


CANDIDATES = [
    (1991, "award_singho_tv", "nominee"),
    (1991, "award_golddisc_music", "nominee"),
    (1992, "award_golddisc_music", "nominee"),
    (1992, "award_singho_tv", "nominee"),
    (1991, "award_harbour_film", "nominee"),
    (1992, "award_harbour_film", "nominee"),
    (1991, "award_harbour_ad", "nominee"),
]


def case_ko(pg, W, H, suffix):
    out = {"checks": {}, "tried": []}
    if not new_game(pg):
        out["checks"]["new_game"] = False
        return out
    out["checks"]["new_game"] = True
    found = None
    for (year, cer, tier) in CANDIDATES:
        seed(pg, day_index(year, 10, 20))
        fp = force_pack(pg, cer, tier)
        out["tried"].append({"year": year, "ceremony": cer, "ko": bool(fp.get("ko")),
                             "n_cats": len(fp.get("cats") or []), "bestOutcome": fp.get("bestOutcome"),
                             "error": fp.get("error")})
        if fp.get("ko"):
            found = {"year": year, "ceremony": cer, "tier": tier, "pack": fp}
            break
        pg.wait_for_timeout(300)
    out["found"] = found
    out["checks"]["pack_has_ko"] = bool(found)
    if not found:
        return out
    out["n_cats"] = len(found["pack"]["cats"])
    inv = present(pg)
    out["invite"] = inv
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    line = ""
    for ln in (inv.get("body") or "").splitlines():
        if ln.strip().startswith("今晚獎項"):
            line = ln.strip()
            break
    out["invite_awards_line"] = line
    sorted_labels = [c.get("label") for c in sorted(found["pack"]["cats"], key=lambda c: c.get("id") or "")]
    out["invite_sorted_labels"] = sorted_labels
    out["raw_cat_ids"] = [c.get("id") for c in found["pack"]["cats"]]
    out["checks"]["invite_awards_sorted_by_id"] = bool(line) and line == ("今晚獎項：" + "、".join(sorted_labels))
    shot(pg, f"ko_invite_{suffix}.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis(pg, "出席")
    pg.wait_for_timeout(400)
    out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
    w = watch(pg, 24)
    out["watch"] = w
    caps = " || ".join(e["caption"] for e in w["timeline"])
    out["checks"]["rollcall_names_ko"] = "高俊傑" in caps
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    body = res.get("body") or ""
    out["result_fellows_count"] = body.count("同屆提名")
    out["result_list_count"] = body.count(LIST_TXT)
    out["checks"]["c1_fellows_row_once"] = out["result_fellows_count"] == 1
    out["checks"]["c1_list_text_once_verbatim"] = out["result_list_count"] == 1
    rk = result_dom(pg)
    out["result_dom"] = rk
    out["checks"]["c1_dom_single_fellows_node"] = rk.get("fellowsCount") == 1
    out["checks"]["c1_dom_not_inside_cat_card"] = rk.get("felInCard") == 0
    out["checks"]["c1_dom_after_last_cat_before_press"] = (
        # .psr-cards 嘅頭 n_cats 個子元素係類別卡（psr-metrics），其後先係餘韻卡（同樣 psr-metrics，
        # 喺 press／news 之後）——所以用 felIdx == n_cats 斷言，唔可以用 lastMetricIdx（會撈埋餘韻卡）。
        rk.get("felIdx", -1) == out["n_cats"]
        and rk.get("pressIdx", -1) == rk.get("felIdx", -1) + 1)
    rk_labels = [k.split("·")[-1].strip() for k in (rk.get("kickers") or [])
                 if k.strip().startswith(("入圍 ·", "得獎 ·", "觀禮 ·"))]
    out["result_kickers"] = rk.get("kickers")
    out["checks"]["result_cats_sorted_by_id"] = rk_labels == sorted_labels
    shot(pg, f"ko_result_{suffix}.png")
    return out


def run_case(pw, name, H, suffix, results):
    print(f"== {name} ==", flush=True)
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            r = case_ko(pg, 430, H, suffix)
            r["pageerrors"] = errs[:8]
            r["checks"]["zero_pageerror"] = len(errs) == 0
            r["verdict"] = "PASS" if r["checks"] and all(r["checks"].values()) else "FAIL"
            results[name] = r
            print(f"  {r['verdict']} n_cats={r.get('n_cats')} fellows={r.get('result_fellows_count')} "
                  f"list={r.get('result_list_count')} {json.dumps(r['checks'], ensure_ascii=False)}", flush=True)
            if errs:
                print(f"    pageerrors: {errs[:3]}", flush=True)
        except Exception as e:
            results[name] = {"verdict": "ERROR", "checks": {}, "error": repr(e)}
            print(f"  ERROR {e!r}", flush=True)
            try:
                shot(pg, f"err_{name}.png")
            except Exception:
                pass
        finally:
            ctx.close()
    finally:
        b.close()


def main():
    srv = serve()
    results = {}
    plan = [("ko_932a", 932, "430x932a"), ("ko_932b", 932, "430x932b"),
            ("ko_700a", 700, "430x700a"), ("ko_700b", 700, "430x700b")]
    try:
        with sync_playwright() as pw:
            for name, H, suffix in plan:
                run_case(pw, name, H, suffix, results)
            # 加跑直到兩類＋單類各至少一跑（上限 8 跑）
            extra = 0
            while extra < 4:
                have_dual = any(isinstance(v, dict) and v.get("n_cats") == 2 for v in results.values())
                have_single = any(isinstance(v, dict) and v.get("n_cats") == 1 for v in results.values())
                if have_dual and have_single:
                    break
                extra += 1
                H = 932 if extra % 2 == 1 else 700
                run_case(pw, f"ko_extra{extra}", H, f"430x{H}extra{extra}", results)
    finally:
        stop(srv)
    json.dump(results, open(os.path.join(QA, "drive186.json"), "w"), ensure_ascii=False, indent=1)
    cases = [v for v in results.values() if isinstance(v, dict) and "verdict" in v]
    n_pass = sum(1 for v in cases if v.get("verdict") == "PASS")
    have_dual = any(v.get("n_cats") == 2 for v in cases)
    have_single = any(v.get("n_cats") == 1 for v in cases)
    print(f"OVERALL {n_pass}/{len(cases)} PASS dual={have_dual} single={have_single}")
    print("RESULTS_JSON_BEGIN")
    print(json.dumps(results, ensure_ascii=False))
    print("RESULTS_JSON_END")
    sys.exit(0 if (n_pass == len(cases) and have_dual and have_single) else 1)


if __name__ == "__main__":
    main()
