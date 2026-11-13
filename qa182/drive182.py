# -*- coding: utf-8 -*-
"""v20a182 實駕：高俊傑上頒獎禮（第二階段；v20a178-strip 後重跑）。
LIVE 模式（無參數，唔用 ?softPreview=1；v165 B1 教訓）。播種存檔直接寫 localStorage
（key starVolunteer_map_v19w，slot 1——經新遊戲＋in-page seed，唔經 softPreview）。
Cases（每 case 全新 browser context）：
  ko_932：430×932，seed 1991，逐個典禮試到有高俊傑做 fellow 嗰場（nominated），
          出席 → 唱名 caption 有「高俊傑」＋提名卡列有佢張卡＋舞台佢嗰位跌返剪影
          （#1d1832 兩格，企位喺最右 slot；紅褸 0 粒），0 pageerror。
  ko_700：同上，430×700。
v20a178-strip（用戶 2026-11-13 15:11 方向更正）：Q 版 sprite 衍生剝走，舞台直接用
PixelLab character 嗰步由 v180 接手；本票淨留入池邏輯。冇咗 sprite 之後 loadSpr 載唔到
跌返剪影，唔穿崩——呢個係預期中間狀態，唔係 FAIL。舊版驗紅褸（607 粒）嗰項改做驗證
剪影 fallback（見 ko_sil_in_shot／stage_shows_ko_silhouette＋stage_no_ko_red_jacket）。
搵場方法：debugForceSeasonWindow 回傳嘅 pack.categories[].fellows63 逐個典禮試
（seed 年份跟候選年份；seeded 抽選令同一 (year, ceremony, medium) 每次結果相同，
試到有就 present＋出席，唔使撞運氣）。
證據以 DOM 層為準＋唱名嗰刻截圖目視舞台。
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

ROOT = "/home/hatch/workspace/linji-work182"
HERE = os.path.join(ROOT, "qa182")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 18282
SAVE_KEY = "starVolunteer_map_v19w"


def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                         cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
        body = r.read()
    want = hashlib.sha256(open(os.path.join(ROOT, "index.html"), "rb").read()).hexdigest()[:12]
    got = hashlib.sha256(body).hexdigest()[:12]
    print("serve sha", got, "want", want, flush=True)
    assert got == want, "served index.html != work copy"
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


def click_first(pg, texts, wait=1000):
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


def vis_btn(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').includes(t));
      return bs.some(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; }); }""", text)


def new_game(pg, query=""):
    pg.goto(f"http://127.0.0.1:{PORT}/index.html{query}")
    pg.wait_for_timeout(3000)
    click_first(pg, ["新遊戲"], 1500)
    pg.evaluate("""() => { const b = document.querySelector('[data-slot="3"]');
      if (b && b.offsetParent !== null) { b.click(); return true; } return false; }""")
    pg.wait_for_timeout(1200)
    click_first(pg, ["覆蓋", "確定", "確認"], 900)
    click_first(pg, ["跳過教學"], 1200)
    click_first(pg, ["開始寫手帳"], 1400)
    try:
        pg.locator("#btn-confirm-plan").click(timeout=3000)
        pg.wait_for_timeout(1200)
    except Exception:
        pass
    click_first(pg, ["確定出發"], 1500)
    for _ in range(4):
        if not click_first(pg, ["確定", "確認", "好", "知道了"], 900):
            break
    ok = pg.evaluate("() => !!(window.S && typeof window.S.dayIndex === 'number')")
    print("NEW GAME OK:", ok, pg.evaluate("() => window.S ? (S.dayIndex + ' ' + S.dateStr) : 'no S'"), flush=True)
    return ok


def day_index(y, m, d):
    return (datetime.date(y, m, d) - datetime.date(1990, 1, 1)).days


def seed(pg, *, day, fame=120, stage=60, acting=60, credit_delta=80, money=5000, stress=0):
    return pg.evaluate("""(o) => {
      S.dayIndex = o.day;
      S.story = S.story || {};
      S.story.done = {};
      S.story.flags = S.story.flags || {};
      S.story.rel = S.story.rel || {};
      S.awardsFlags = {};
      S.pendingAwardPack = null;
      S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
      S.fame = o.fame; S.stage = o.stage; S.acting = o.acting;
      S.industryCreditDelta = o.credit_delta;
      S.money = o.money; S.stress = o.stress;
      S.flags = S.flags || {};
      if (typeof BehaviorGate !== "undefined" && BehaviorGate.readCtx) {
        const ctx = BehaviorGate.readCtx({});
        return { day: S.dayIndex, week: ctx.week, year: ctx.year, season: ctx.season, dual: ctx.dual };
      }
      return { day: S.dayIndex };
    }""", {"day": day, "fame": fame, "stage": stage, "acting": acting,
            "credit_delta": credit_delta, "money": money, "stress": stress})


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
      const body = (m.innerText || '').slice(0, 1200);
      return {visible:true, h3, btns, body};
    }""")


def dismiss_once(pg):
    try:
        btn = pg.locator('#modal-btns button').first
        if btn.is_visible(timeout=400):
            try:
                btn.click(timeout=1000)
            except Exception:
                pass
            return True
    except Exception:
        pass
    return False


def force_pack(pg, ceremony_id, tier):
    """淨 force 唔 present，睇 pack 有冇高俊傑。回傳 {pack, ko}。"""
    return pg.evaluate("""(o) => {
      try {
        const p = window.__awards.debugForceSeasonWindow(o.id, { forceTier: o.tier });
        if (!p) return { error: 'no pack' };
        const cats = (p.categories || []).map(c => ({
          outcome: c.outcome, label: c.label,
          fellows: (c.fellows63 || []).map(f => ({ star: f.star || '', starId: f.starId || '', title: f.title || '', gigId: f.gigId || '', assigned: !!f.assigned })) }));
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
      const skip = st.querySelector('.awd62-skip');
      const cards = [...document.querySelectorAll('.awd63-card')].map(c => {
        const cc = c.querySelector('.awd63-csscard');
        return {
        star: (c.querySelector('.s')||{}).textContent || '',
        title: (c.querySelector('.t')||{}).textContent || '',
        hasPoster: !!c.querySelector(':scope > img'),
        faceText: cc ? (cc.textContent||'').trim() : null,
        faceBg: cc ? getComputedStyle(cc).backgroundImage : null,
        cls: c.className,
        visible: !!(c.offsetParent !== null && getComputedStyle(c).opacity !== '0') }; });
      const cardsOn = !!(document.querySelector('.awd63-cards') && document.querySelector('.awd63-cards').classList.contains('on'));
      return { present: true,
               caption: cap ? cap.textContent : '',
               skipVisible: !!skip && skip.getBoundingClientRect().width > 0,
               cards, cardsOn };
    }""")


def modal_geom(pg):
    """C2 量度：modal 幾何＋#mask class（story-play-on 會令 modal height:100% 全黑）。"""
    return pg.evaluate("""() => {
      const mask = document.getElementById('mask');
      const modal = document.getElementById('modal');
      const inner = document.getElementById('modal-inner');
      const btns = document.getElementById('modal-btns');
      if (!modal) return {present:false};
      const mr = modal.getBoundingClientRect();
      const cs = getComputedStyle(modal);
      const innerKids = inner ? [...inner.querySelectorAll('*')].filter(el => {
        const r = el.getBoundingClientRect(); const cs2 = getComputedStyle(el);
        return r.height > 0 && cs2.visibility !== 'hidden' && (el.textContent||'').trim(); }) : [];
      const textBottom = innerKids.length ? Math.round(Math.max(...innerKids.map(el => el.getBoundingClientRect().bottom))) : -1;
      const textTop = innerKids.length ? Math.round(Math.min(...innerKids.map(el => el.getBoundingClientRect().top))) : -1;
      return {
        maskClasses: mask ? mask.className : '',
        modalTop: Math.round(mr.top), modalH: Math.round(mr.height), modalBottom: Math.round(mr.bottom),
        modalMaxH: cs.maxHeight, modalBg: cs.backgroundColor,
        innerScrollH: inner ? inner.scrollHeight : -1, innerClientH: inner ? inner.clientHeight : -1,
        btnsTop: btns ? Math.round(btns.getBoundingClientRect().top) : -1,
        btnsH: btns ? Math.round(btns.getBoundingClientRect().height) : -1,
        viewportH: window.innerHeight,
        textTop, textBottom, textH: (textTop >= 0 && textBottom >= 0) ? textBottom - textTop : -1,
        voidBelowText: (textBottom >= 0 && btns) ? Math.round(btns.getBoundingClientRect().top - textBottom) : -1 };
    }""")


def awards_overflow(pg):
    return pg.evaluate("""() => {
      const items = [...document.querySelectorAll('#awards-list .awd62-item')].map(it => {
        const whens = [...it.querySelectorAll('.awd62-when')].map(d => ({
          text: d.textContent.slice(0, 100),
          scrollW: d.scrollWidth, clientW: d.clientWidth }));
        const fels = [...it.querySelectorAll('.awd62-fellows')].map(d => ({
          text: d.textContent.slice(0, 100),
          scrollW: d.scrollWidth, clientW: d.clientWidth }));
        return { whens, fels, itemScrollW: it.scrollWidth, itemClientW: it.clientWidth }; });
      return items; }""")


def ko_red_in_shot(path):
    """唱名截圖入面搵高俊傑皮褸平塗色 (182,28,32)：全場唯一用呢隻紅嘅係佢
    （舞台紅幕布／其他人衫色實測 0 粒完全相等；v178 實測 ko_names 932 嗰張 609 粒，
    全部聚喺 x296–340／y391–413，即最右企位件褸）。
    v20a178-strip 之後呢項應該讀 0（sprite 已剝走，冇紅褸可言）——見
    stage_no_ko_red_jacket。經系統 /usr/bin/python3＋PIL 計（Playwright venv 冇 PIL）。"""
    try:
        r = subprocess.run(["/usr/bin/python3", os.path.join(HERE, "ko_red.py"), path],
                           capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:
        return {"koRedPx": -1, "bbox": None, "error": repr(e)}


def ko_sil_in_shot(path):
    """唱名截圖入面數剪影降級色 (29,24,50)（#1d1832）：drawSpr 載唔到 sprite 就畫
    兩格呢隻色嘅剪影（闊方頭＋短身）。v20a178-strip 之後高俊傑嗰位應該係剪影——
    舊 ko_names 截圖（有紅褸嗰陣）實測 silPx = 0，呢隻色係乾淨分辨器。
    經系統 /usr/bin/python3＋PIL 計（Playwright venv 冇 PIL）。"""
    try:
        r = subprocess.run(["/usr/bin/python3", os.path.join(HERE, "ko_sil.py"), path],
                           capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:
        return {"silPx": -1, "bbox": None, "error": repr(e)}


def sil_ok(sil):
    """剪影 fallback 斷言：夠多粒（頭＋身兩格約 4600 canvas px，閾值取 1000 留足 margin）、
    聚喺最右企位（slotCx 362 ± 35 canvas px → 截圖 x 約 327–397；閾值 x0 >= 300、x1 <= 415）、
    有頭身尺寸（闊、高各 >= 40px）。"""
    try:
        b = sil.get("bbox") or {}
        return (sil.get("silPx", 0) >= 1000 and b.get("x0", 0) >= 300 and b.get("x1", 999) <= 415
                and (b.get("x1", 0) - b.get("x0", 0)) >= 40 and (b.get("y1", 0) - b.get("y0", 0)) >= 40)
    except Exception:
        return False


def watch_ceremony(pg, secs=24, shot_at=None):
    timeline = []
    last = None
    cards_ko = None
    t0 = time.time()
    took = set()
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        cap = st.get("caption") or ""
        now = round((time.time() - t0) * 1000)
        if cap != last:
            timeline.append({"t": now, "caption": cap[:160]})
            last = cap
            if shot_at:
                for key, name in shot_at:
                    if key in cap and name not in took:
                        shot(pg, name)
                        took.add(name)
        if cards_ko is None and st.get("cards"):
            hit = [c for c in st["cards"] if c.get("star") == "高俊傑"]
            if hit:
                cards_ko = {"t": now, "cards": st["cards"], "cardsOn": st.get("cardsOn")}
                shot(pg, shot_at[1][1] if shot_at and len(shot_at) > 1 else "ko_cards.png")
        pg.wait_for_timeout(90)
    total = round((time.time() - t0) * 1000)
    return {"timeline": timeline, "totalMs": total,
            "stageGone": not stage_state(pg).get("present"), "cardsKo": cards_ko}


# 候選場（年，典禮，tier）：stub 探測話 1991 tv／1991 music／1992 music 有佢，
# 實盤 gigs 唔同所以逐場試 pack，試到有先 present。
CANDIDATES = [
    (1991, "award_singho_tv", "nominee"),
    (1991, "award_golddisc_music", "nominee"),
    (1992, "award_golddisc_music", "nominee"),
    (1992, "award_singho_tv", "nominee"),
    (1991, "award_harbour_film", "nominee"),
    (1992, "award_harbour_film", "nominee"),
    (1991, "award_harbour_ad", "nominee"),
]


def case_ko(pg, W, H):
    out = {"checks": {}, "tried": []}
    if not new_game(pg):
        out["checks"]["new_game"] = False
        return out
    out["checks"]["new_game"] = True
    found = None
    for (year, cer, tier) in CANDIDATES:
        seed(pg, day=day_index(year, 10, 20), fame=120, stage=60, acting=60, credit_delta=80)
        fp = force_pack(pg, cer, tier)
        tried = {"year": year, "ceremony": cer, "tier": tier,
                 "ko": bool(fp.get("ko")), "bestOutcome": fp.get("bestOutcome"),
                 "error": fp.get("error")}
        out["tried"].append(tried)
        print(f"  try {year} {cer} {tier}: ko={tried['ko']} outcome={tried['bestOutcome']} err={tried['error']}", flush=True)
        if fp.get("ko"):
            found = {"year": year, "ceremony": cer, "tier": tier, "pack": fp}
            break
        pg.wait_for_timeout(300)
    out["found"] = found
    out["checks"]["pack_has_ko"] = bool(found)
    if not found:
        return out
    inv = present(pg)
    out["invite"] = inv
    out["checks"]["invite_shown"] = bool(inv.get("visible"))
    out["checks"]["invite_has_attend"] = any("出席" in b for b in inv.get("btns") or [])
    out["invite_geom"] = modal_geom(pg)
    _ig = out["invite_geom"]
    # C2：請柬唔再係 story 全屏黑 modal——mask 唔帶 story-play-on，modal 收窄到底紙高度，
    # 內容下黑空細（pristine：932px 全高、void ~640px）
    out["checks"]["invite_no_story_play_on"] = "story-play-on" not in (_ig.get("maskClasses") or "")
    out["checks"]["invite_modal_compact"] = (_ig.get("modalH") or 9999) <= 560
    out["checks"]["invite_void_small"] = (_ig.get("voidBelowText") is not None and _ig.get("voidBelowText") != -1 and _ig.get("voidBelowText") <= 80)
    out["checks"]["invite_has_awards_line"] = "今晚獎項" in (inv.get("body") or "")
    shot(pg, f"ko_invite_{W}x{H}.png")
    if not out["checks"]["invite_shown"]:
        return out
    click_vis(pg, "出席")
    pg.wait_for_timeout(400)
    st0 = stage_state(pg)
    out["stage_at_start"] = {k: v for k, v in st0.items() if k != "cards"}
    out["checks"]["stage_appears"] = bool(st0.get("present"))
    w = watch_ceremony(pg, 24, shot_at=[
        ("高俊傑", f"ko_names_{W}x{H}.png"),
        ("高俊傑", f"ko_cards_{W}x{H}.png"),
    ])
    out["watch"] = w
    caps = " || ".join(e["caption"] for e in w["timeline"])
    out["checks"]["rollcall_names_ko"] = "高俊傑" in caps
    out["checks"]["cards_show_ko"] = bool(w.get("cardsKo"))
    if w.get("cardsKo"):
        out["cardsKo"] = w["cardsKo"]
        # C1：三張 CSS 卡卡面要一眼分得開——face 文字（首字＋全名＋媒介）同底色 tint 各不相同
        _cards = w["cardsKo"].get("cards") or []
        _css = [c for c in _cards if not c.get("hasPoster")]
        _faces = [(c.get("faceText") or "") for c in _css]
        _bgs = [(c.get("faceBg") or "") for c in _css]
        out["checks"]["cards_all_css_fallback"] = len(_css) == 3 and len(_cards) == 3
        out["checks"]["cards_faces_distinct"] = len(set(_faces)) == 3 and all(f for f in _faces)
        out["checks"]["cards_tints_distinct"] = len(set(_bgs)) == 3
        out["checks"]["cards_face_has_mono_name"] = all(
            (c.get("star") or "")[:1] in (c.get("faceText") or "") and (c.get("star") or "") in (c.get("faceText") or "")
            for c in _css)
    names_shot = os.path.join(SHOTS, f"ko_names_{W}x{H}.png")
    ko_red = ko_red_in_shot(names_shot)
    out["ko_red"] = ko_red
    ko_sil = ko_sil_in_shot(names_shot)
    out["ko_sil"] = ko_sil
    out["checks"]["stage_no_ko_red_jacket"] = ko_red.get("koRedPx", -1) == 0
    out["checks"]["stage_shows_ko_silhouette"] = sil_ok(ko_sil)
    out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
    pg.wait_for_timeout(600)
    res = modal_info(pg)
    out["result_card"] = res
    out["checks"]["result_card_shown"] = bool(res.get("visible"))
    shot(pg, f"ko_result_{W}x{H}.png")
    dismiss_once(pg)
    # --- B1：獎項頁提名行溢出（followup4 流程）---
    pg.wait_for_timeout(1200)
    click_vis(pg, "事業")
    pg.wait_for_timeout(900)
    pg.evaluate("""() => { const el = document.querySelector('#htab-awards'); if (el) el.click(); }""")
    pg.wait_for_timeout(1000)
    out["awards_overflow"] = awards_overflow(pg)
    # B1：提名行唔再裁切——.awd62-fellows 准換行，scrollW ≤ clientW，全名＋作品＋得主標記齊
    _ov = out["awards_overflow"] or []
    _fels = [_f for _it in _ov for _f in (_it.get("fels") or [])]
    _whens = [_w for _it in _ov for _w in (_it.get("whens") or [])]
    out["checks"]["awards_fellows_row_present"] = len(_fels) >= 1
    out["checks"]["awards_fellows_no_overflow"] = all(
        (_f.get("scrollW") or 0) <= (_f.get("clientW") or 0) for _f in _fels)
    out["checks"]["awards_fellows_full_text"] = any(
        "高俊傑《潮汐家庭》" in (_f.get("text") or "") for _f in _fels)
    out["checks"]["awards_date_row_unchanged"] = any(
        (_w.get("scrollW") == 144 and _w.get("clientW") == 144) for _w in _whens)
    shot(pg, f"fu4_awards_page_{W}x{H}.png")
    return out


CASES = {
    "ko_932": lambda pg, W, H: case_ko(pg, W, H),
    "ko_700": lambda pg, W, H: case_ko(pg, W, H),
}


def run_case(pw, name, results):
    H = 700 if name == "ko_700" else 932
    print(f"== {name} ==", flush=True)
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            r = case_ko(pg, 430, H)
            r["pageerrors"] = errs[:8]
            checks = r.get("checks", {})
            r["checks"]["zero_pageerror"] = len(errs) == 0
            checks = r["checks"]
            r["verdict"] = "PASS" if checks and all(checks.values()) else "FAIL"
            results[name] = r
            print(f"  {r['verdict']} {json.dumps(checks, ensure_ascii=False)}", flush=True)
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
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    sel = list(CASES.keys()) if arg == "all" else [arg]
    srv = serve()
    results = {}
    try:
        with sync_playwright() as pw:
            for name in sel:
                try:
                    run_case(pw, name, results)
                except Exception as e:
                    print(f"  browser attempt failed: {e!r}", flush=True)
                    results[name] = {"verdict": "ERROR", "checks": {}, "error": repr(e)}
    finally:
        stop(srv)
    try:
        json.dump(results, open(os.path.join(HERE, "drive182.json"), "w"), ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"NOTE drive182.json write failed: {e!r}", flush=True)
    print("RESULTS_JSON_BEGIN")
    print(json.dumps(results, ensure_ascii=False))
    print("RESULTS_JSON_END")
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    print(f"OVERALL {n_pass}/{len(results)} PASS")
    sys.exit(0 if n_pass == len(results) else 1)


if __name__ == "__main__":
    main()
