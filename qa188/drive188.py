# -*- coding: utf-8 -*-
"""v20a188 實駕：頒獎禮獎項改名＋提名掛鈎（15 個新獎項、role-based 提名閘）。
對象：本地工作副本 ~/workspace/linji-work188/index.html（serve 工作副本本身）。
場次：932／700 × 四場典禮 × won／nominated（實路徑，唔 forceOutcome——
  代碼根本冇 forceOutcome；debugForceSeasonWindow 只接受 forceTier）。
  廣告 won 喺實玩入面數學上到唔到（最佳現實種子 base ≈ 0.75–0.81，贏線 0.875；
  詳見 NOTES）：ad won 改用 synthetic-pay probe（h.pay=25000）行同一條
  實路徑驗 won 渲染，並明確標記為非現實種子；另加 1990 ad extra-only
  gallery case 驗角色閘（請柬＋閘句，唔出席）。
播種：新遊戲＋in-page seed（wrapHistory 由 live gig 池揀最高質＋
  source-parse 嘅 ad gig36／exodus 記錄；h.pay 用 pay 範圍中位數，
  唯一例外係 ad won synthetic probe）。
斷言（每 case）：請柬「今晚獎項」行＝按 id 排序嘅新 label；白牌＝焦點新獎項名；
  結果卡 kicker＝pack 類別、每類 line（win／lose）逐字出現；報紙 queue 有
  award 項且無舊名；手帳獎項頁有典禮名＋徽章＋代表作、無舊名；全 DOM 無舊
  label；0 pageerror。截圖放 qa188/shots188/。
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work188"
QA = os.path.join(ROOT, "qa188")
SHOTS = os.path.join(QA, "shots188")
EXE = "/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 18890

OLD_LABELS = ["年度廣告新面孔", "街外最記得住嘅一鏡", "街外最記得住的一鏡", "年度新人碟緣",
              "最受歡迎出鏡嗓", "最受歡迎出鏡嗓／面孔", "影壇新面孔",
              "年度票房話題綠葉", "最佳電視新人", "最受歡迎螢幕面孔",
              "綜藝閃光綠葉", "最佳班底", "最佳班底／群戲"]
NEW_LABELS = ["最佳男主角", "最佳女主角", "最佳男配角", "最佳女配角",
              "最佳男歌手", "最佳女歌手", "最佳新人獎",
              "最佳廣告男主角", "最佳廣告女主角", "最佳廣告男配角", "最佳廣告女配角"]
CEREMONY_NAME = {"award_harbour_film": "維港影藝獎",
                 "award_singho_tv": "星河台慶・年度頒獎夜",
                 "award_golddisc_music": "星河金碟夜",
                 "award_harbour_ad": "維港街招・年度廣告賞"}

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


def click_exact(pg, text):
    return pg.evaluate("""(t) => {
      const bs = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').trim() === t);
      const vis = bs.filter(b => { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
      if (!vis.length) return false; vis[0].click(); return true; }""", text)


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


def parse_ad_gigs(src):
    """由 index.html source 抽廣告 gig 記錄（gig36 ad_lead＋exodus ad_support）。
    原因：呢啲 gig 唔喺 1990 開局 GIGS 池（GIGS36 要 mergeYearGigs36 按年注入，
    exodus 要 mergeExodusGigs 注入；兩者都喺 IIFE 入面，頁面 global 叫唔到）。
    Awards 計分只用 roleScale／pay 段／stars——呢啲值 source-parse 同實玩 wrap
    完全一樣（ad_lead／ad_support 唔喺 AWARDS62_ROLE_Q，質素行 pay 段兜底）。"""
    out = []

    def fields(txt):
        def one(pat):
            m = re.search(pat, txt)
            return m.group(1) if m else ""
        def pay():
            m = re.search(r"pay:\s*\[(\d+)\s*,\s*(\d+)\]", txt)
            if m:
                return [int(m.group(1)), int(m.group(2))]
            m2 = re.search(r"payExact:\s*(\d+)", txt)
            return int(m2.group(1)) if m2 else None
        return {"id": one(r"id:\s*\"([^\"]+)\""),
                "year": int(one(r"year:\s*(\d+)") or 0),
                "type": one(r"type:\s*\"([^\"]+)\""),
                "roleScale": one(r"roleScale:\s*\"([^\"]+)\""),
                "roleLabel": one(r"roleLabel:\s*\"([^\"]*)\""),
                "pay": pay(),
                "payExact": int(one(r"payExact:\s*(\d+)") or 0) or None,
                "title": one(r"title:\s*\"([^\"]*)\""),
                "workTitle": one(r"workTitle:\s*\"([^\"]*)\""),
                "stars": int(one(r"stars:\s*(\d+)") or 0) or None}

    # gig36({ ... }) 係多行定義——逐行搵會漏，要 DOTALL 撈成個 call 再抽欄
    for m in re.finditer(r"gig36\(\{(.*?)storyKeys:\[[^\]]*\]\s*\}\)", src, re.S):
        blk = m.group(1)
        if 'type:"廣告"' in blk and 'roleScale:"ad_lead"' in blk:
            out.append(fields(blk))
    i = src.find('id:"gig_exodus_ad_manager"')
    if i >= 0:
        out.append(fields(src[i:i + 2600]))
    return [g for g in out if g["id"] and g["roleScale"]]


JS_SEED = """(o) => {
  const RQ = { film_lead_big:1.00, tv_lead_long:1.00, film_support_main:0.78, tv_support_main:0.78,
    rec_album:0.66, film_support_small:0.55, tv_cameo_short:0.55, mtv:0.48, ad_av:0.48,
    variety_special:0.48, ad_print:0.40, variety_ep:0.40, photobook:0.40,
    film_extra_day:0.22, tv_extra_day:0.22, ad_extra_day:0.22, rec_extra_day:0.22, variety_extra_day:0.22 };
  const qOf = g => { let q = RQ[g.roleScale] || 0;
    if(!q){ const pay = (g.payExact!=null ? g.payExact : (Array.isArray(g.pay) ? g.pay[1] : 0)) || 0;
      q = pay>=20000?0.80:(pay>=8000?0.62:(pay>=3000?0.48:(pay>=1200?0.36:0.25))); }
    const st = Number(g.stars); if(st>=5) q+=0.04; else if(st<=1) q-=0.04;
    return Math.min(1, Math.max(0.05, q)); };
  const all = []; const seen = {}; const liveIds = {};
  const push = (g, live) => { if (g && g.id && !seen[g.id]) { seen[g.id] = true; all.push(g); if (live) liveIds[g.id] = 1; } };
  try { (typeof GIGS !== 'undefined' ? GIGS : []).forEach(g => push(g, true)); } catch(e) {}
  try { const by = (typeof STORY_WIRE !== 'undefined' && STORY_WIRE && STORY_WIRE.gigsByYear) || {};
    Object.keys(by).forEach(y => { const gs = by[y] && by[y].gigs; if (Array.isArray(gs)) gs.forEach(g => push(g, true)); }); } catch(e2) {}
  (o.adGigs || []).forEach(g => { if (g && g.id) push({ id:g.id, type:g.type, roleScale:g.roleScale,
    roleLabel:g.roleLabel, pay:g.pay, payExact:(g.payExact!=null?g.payExact:null),
    stars:(g.stars!=null?g.stars:1), title:g.title, workTitle:g.workTitle||'', year:g.year, days:2 }, false); });
  const isStunt = g => /替身/.test(String(g.roleLabel||''));
  const PREDS = {
    film_lead: g => g.type==='電影' && (g.roleScale==='film_lead_big'||g.roleScale==='film_second_lead') && /男主角/.test(String(g.roleLabel||'')),
    film_sup: g => g.type==='電影' && /support/.test(String(g.roleScale||'')) && /配角/.test(String(g.roleLabel||'')),
    film_extra: g => g.type==='電影' && g.roleScale==='film_extra_day',
    tv_lead: g => g.type==='電視劇' && /男主角/.test(String(g.roleLabel||'')),
    tv_sup: g => g.type==='電視劇' && /support/.test(String(g.roleScale||'')) && /配角/.test(String(g.roleLabel||'')),
    rec: g => g.type==='唱片通告' && g.roleScale==='rec_album',
    ad_lead: g => g.type==='廣告' && g.roleScale==='ad_lead',
    ad_sup: g => g.type==='廣告' && g.roleScale==='ad_support',
    ad_extra: g => g.type==='廣告' && g.roleScale==='ad_extra_day'
  };
  const chosen = {}; const wraps = [];
  Object.keys(o.roles || {}).forEach(k => {
    const n = o.roles[k] || 0; if (!n || !PREDS[k]) return;
    const cands = all.filter(g => !isStunt(g) && PREDS[k](g)).sort((a,b) => qOf(b)-qOf(a)).slice(0, n);
    chosen[k] = cands.map(g => ({ id: g.id, q: +qOf(g).toFixed(2), live: !!liveIds[g.id] }));
    cands.forEach(g => {
      const payArr = Array.isArray(g.pay) ? g.pay : null;
      const payMid = (g.payExact!=null) ? g.payExact : (payArr ? Math.round((Number(payArr[0])+Number(payArr[1]))/2) : 0);
      wraps.push({ gigId: g.id, title: g.title||g.id, type: g.type||'', workTitle: g.workTitle||'',
        roleLabel: g.roleLabel||'', roleScale: g.roleScale||'', year: o.year,
        totalDays: 2, pay: (o.payOverride!=null ? o.payOverride : payMid),
        fame: Array.isArray(g.fame)? g.fame[0] : 0, popularity: 0,
        wrappedDay: o.wrapDay, rating: '順利殺青' });
    });
  });
  S.dayIndex = o.dayIndex;
  S.story = S.story || {}; S.story.done = {}; S.story.flags = S.story.flags || {}; S.story.rel = S.story.rel || {};
  S.awardsFlags = {}; S.pendingAwardPack = null;
  S.wf4 = { lastDay: -99, seen: {}, pending: null, pendingDay: -99, flags: {}, evDay: {}, locDay: -99, locTries: 0, fenFarewellDone: true };
  S.fame = o.fame; S.stage = 60; S.acting = 60; S.industryCreditDelta = o.creditDelta;
  S.money = 5000; S.stress = 0; S.flags = S.flags || {};
  S.wrapHistory = wraps; S.newspaperQueue = []; S.news = S.news || [];
  S.story.gigCount = wraps.length;
  return { day: S.dayIndex, wraps: wraps.length, chosen };
}"""


def seed(pg, spec, ad_gigs):
    return pg.evaluate(JS_SEED, {"dayIndex": day_index(spec["year"], 10, 20),
                                 "wrapDay": day_index(spec["year"], 9, 15),
                                 "year": spec["year"], "fame": spec["fame"],
                                 "creditDelta": spec["credit"],
                                 "roles": spec["roles"], "adGigs": ad_gigs,
                                 "payOverride": spec.get("payOverride")})


def set_random(pg, v):
    pg.evaluate("(v) => { Math.random = () => v; return true; }", v)


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
      return {visible:true, h3, btns, body: (m.innerText || '').slice(0, 2000)};
    }""")


def force_pack(pg, ceremony_id, tier=None):
    return pg.evaluate("""(o) => {
      try {
        const p = window.__awards.debugForceSeasonWindow(o.id, o.tier ? { forceTier: o.tier } : {});
        if (!p) return { error: 'no pack' };
        const cats = (p.categories || []).map(c => ({ id: c.id || '', outcome: c.outcome,
          label: c.label, score: (c.score!=null ? +c.score.toFixed(4) : null),
          line: c.line || '', repWorkTitle: c.repWorkTitle || '' }));
        let elig = null;
        try { elig = window.__awards.eligible188(o.id, p.year); } catch(e) {}
        return { ceremonyId: p.ceremonyId, year: p.year, bestOutcome: p.bestOutcome, tier: p.tier,
                 cats, eligibleIds: elig ? elig.map(c => c.id) : null };
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
      const board = st.querySelector('.awd181-board .awd181-t');
      const sub = st.querySelector('.awd181-board .awd181-sub, .awd181-sub');
      return { present: true, caption: cap ? cap.textContent : '',
               board: board ? board.textContent : '',
               boardSub: sub ? sub.textContent : '' };
    }""")


def watch(pg, secs=24):
    timeline = []
    last = None
    boards = []
    t0 = time.time()
    while time.time() - t0 < secs:
        st = stage_state(pg)
        if not st.get("present"):
            break
        cap = st.get("caption") or ""
        if cap != last:
            timeline.append({"t": round((time.time() - t0) * 1000), "caption": cap[:160]})
            last = cap
        b = st.get("board") or ""
        if b and b not in boards:
            boards.append(b)
        pg.wait_for_timeout(90)
    return {"timeline": timeline, "boards": boards,
            "totalMs": round((time.time() - t0) * 1000),
            "stageGone": not stage_state(pg).get("present")}


def result_dom(pg):
    return pg.evaluate("""() => {
      const sheet = document.querySelector('#modal .awd-sheet');
      if (!sheet) return { present: false };
      const cards = [...sheet.querySelectorAll('.psr-card')].map(el => ({
        kicker: (el.querySelector('.psr-kicker')||{textContent:''}).textContent.trim(),
        title: (el.querySelector('.psr-title')||{textContent:''}).textContent.trim() }));
      return { present: true, cards,
               kickers: cards.map(c => c.kicker), titles: cards.map(c => c.title),
               text: (sheet.innerText || '') };
    }""")


def newspaper_award(pg):
    return pg.evaluate("""() => {
      const q = (S && S.newspaperQueue) || [];
      return q.map(n => ({ source: n.source || '', headline: n.headline || '',
        dek: n.dek || '', title: n.title || '', clipLabel: n.clipLabel || '' }));
    }""")


def journal_awards(pg):
    # 新遊戲結束喺週行程畫面（手帳已開、行程 tab）：#btn-menu 嗰陣係隱藏，
    # 唔使經 ☰→手帳，直接撳 事業 → 獎項。地圖畫面就照舊經 ☰→手帳。
    st = pg.evaluate("""() => {
      const menu = document.getElementById('btn-menu');
      const menuVis = !!(menu && menu.offsetParent !== null);
      const biz = [...document.querySelectorAll('button')].find(
        b => (b.textContent||'').trim() === '事業' && b.offsetParent !== null);
      return { menuVis, bizVis: !!biz }; }""")
    if st.get("menuVis"):
        pg.locator("#btn-menu").click(timeout=3000)
        pg.wait_for_timeout(900)
        if not click_text(pg, ["手帳"], 1400):
            return {"error": "open notebook failed"}
        pg.wait_for_timeout(1000)
    elif not st.get("bizVis"):
        return {"error": "neither menu nor notebook visible"}
    if not click_exact(pg, "事業"):
        return {"error": "career tab failed"}
    pg.wait_for_timeout(1200)
    if not click_exact(pg, "獎項"):
        return {"error": "awards subtab failed"}
    pg.wait_for_timeout(900)
    return pg.evaluate("""() => {
      const el = document.querySelector('#awards-list');
      return { text: el ? (el.innerText || '') : '', present: !!el };
    }""")


def old_in(txt):
    return [l for l in OLD_LABELS if l in (txt or "")]


CASES = [
    # name, ceremony, year, expect_outcome, H, fame, credit, roles, cross, payOverride, note
    ("film_won_932", "award_harbour_film", 1990, "won", 932, 45, 50,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2}, None, "real"),
    ("film_won_700", "award_harbour_film", 1990, "won", 700, 45, 50,
     {"film_lead": 2, "film_sup": 1, "tv_lead": 2}, None, "real"),
    ("film_nom_932", "award_harbour_film", 1990, "nominated", 932, 25, 0,
     {"film_lead": 1, "film_sup": 1}, None, "real"),
    ("film_nom_700", "award_harbour_film", 1990, "nominated", 700, 25, 0,
     {"film_lead": 1, "film_sup": 1}, None, "real"),
    ("tv_won_932", "award_singho_tv", 1990, "won", 932, 45, 50,
     {"tv_lead": 2, "tv_sup": 1, "film_lead": 2}, None, "real"),
    ("tv_won_700", "award_singho_tv", 1990, "won", 700, 45, 50,
     {"tv_lead": 2, "tv_sup": 1, "film_lead": 2}, None, "real"),
    ("tv_nom_932", "award_singho_tv", 1990, "nominated", 932, 25, 0,
     {"tv_lead": 1, "tv_sup": 1}, None, "real"),
    ("tv_nom_700", "award_singho_tv", 1990, "nominated", 700, 25, 0,
     {"tv_lead": 1, "tv_sup": 1}, None, "real"),
    ("music_won_932", "award_golddisc_music", 1990, "won", 932, 45, 50,
     {"rec": 4, "film_lead": 2}, None, "real"),
    ("music_won_700", "award_golddisc_music", 1990, "won", 700, 45, 50,
     {"rec": 4, "film_lead": 2}, None, "real"),
    ("music_nom_932", "award_golddisc_music", 1990, "nominated", 932, 25, 0,
     {"rec": 2}, None, "real"),
    ("music_nom_700", "award_golddisc_music", 1990, "nominated", 700, 25, 0,
     {"rec": 2}, None, "real"),
    ("ad_nom_sup_932", "award_harbour_ad", 1990, "nominated", 932, 25, 0,
     {"ad_sup": 1, "ad_extra": 1}, None, "real"),
    ("ad_nom_sup_700", "award_harbour_ad", 1990, "nominated", 700, 25, 0,
     {"ad_sup": 1, "ad_extra": 1}, None, "real"),
    ("ad_nom_lead_932", "award_harbour_ad", 1991, "nominated", 932, 25, 0,
     {"ad_lead": 2}, None, "real"),
    ("ad_won_att_932", "award_harbour_ad", 1991, "nominated", 932, 45, 50,
     {"ad_lead": 3, "film_lead": 2}, None, "real-ceiling"),
    ("ad_won_synth_932", "award_harbour_ad", 1991, "won", 932, 45, 50,
     {"ad_lead": 2, "ad_sup": 1, "ad_extra": 1, "film_lead": 2}, 25000, "synthetic-pay"),
    ("ad_gallery_932", "award_harbour_ad", 1990, "gallery", 932, 45, 50,
     {"ad_extra": 2}, None, "real-gate"),
]


def run_case(pw, cfg, ad_gigs, results):
    name, cer, year, expect, H, fame, credit, roles, pay_override, note = cfg
    print(f"== {name} ({cer} {year} expect={expect} {note}) ==", flush=True)
    out = {"case": name, "ceremony": cer, "year": year, "expect": expect,
           "note": note, "checks": {}}
    errs = []
    b = pw.chromium.launch(executable_path=EXE)
    try:
        ctx = b.new_context(viewport={"width": 430, "height": H})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
        try:
            if not new_game(pg):
                out["checks"]["new_game"] = False
                out["verdict"] = "ERROR"
                results[name] = out
                print("  ERROR new_game", flush=True)
                return
            out["checks"]["new_game"] = True
            sd = seed(pg, {"year": year, "fame": fame, "credit": credit,
                           "roles": roles, "payOverride": pay_override}, ad_gigs)
            out["seed"] = sd
            # 每個角色至少揀到一張（ad gig36／exodus 唔喺 live 池係預期內，live:false 唔扣分）
            out["checks"]["seed_roles_found"] = all(
                len(sd["chosen"].get(k, [])) == n for k, n in roles.items())
            set_random(pg, 0.4)
            fp = force_pack(pg, cer)
            out["pack"] = fp
            out["checks"]["pack_built"] = "error" not in fp
            if "error" in fp:
                out["verdict"] = "ERROR"
                results[name] = out
                print("  ERROR pack", fp, flush=True)
                return
            out["checks"]["tier_real_path"] = fp.get("tier") in ("nominee", "gallery")
            out["checks"]["outcome_matches"] = fp.get("bestOutcome") == expect
            out["checks"]["cats_all_new"] = all(
                c.get("label") in NEW_LABELS for c in fp.get("cats") or [])
            out["checks"]["cats_ids_new"] = all(
                c.get("id") in ["cat_film_lead_m", "cat_film_lead_f", "cat_film_support_m",
                                "cat_film_support_f", "cat_tv_lead_m", "cat_tv_lead_f",
                                "cat_tv_support_m", "cat_tv_support_f", "cat_ad_lead_m",
                                "cat_ad_lead_f", "cat_ad_support_m", "cat_ad_support_f",
                                "cat_music_singer_m", "cat_music_singer_f",
                                "cat_music_newcomer"]
                for c in fp.get("cats") or [])
            out["checks"]["cats_no_old_label"] = not any(
                old_in(c.get("label", "")) for c in fp.get("cats") or [])
            out["checks"]["cats_have_line"] = all(
                bool(c.get("line")) for c in fp.get("cats") or [])
            # gallery 池係全表（睇人哋攞獎），唔係 eligible 子集——只喺 nominee 路徑斷言
            out["checks"]["eligible_subset"] = (
                fp.get("tier") == "gallery" or fp.get("eligibleIds") is None or
                set(c.get("id") for c in fp.get("cats") or []) <= set(fp.get("eligibleIds") or []))
            # gallery case：淨驗請柬＋閘句，唔出席
            inv = present(pg)
            out["invite"] = inv
            out["checks"]["invite_shown"] = bool(inv.get("visible"))
            body = inv.get("body") or ""
            out["checks"]["invite_no_old"] = not old_in(body)
            sorted_labels = [c.get("label") for c in sorted(
                fp.get("cats") or [], key=lambda c: c.get("id") or "")]
            line = ""
            for ln in body.splitlines():
                if ln.strip().startswith("今晚獎項"):
                    line = ln.strip()
                    break
            out["invite_awards_line"] = line
            out["checks"]["invite_awards_sorted"] = bool(line) and line == (
                "今晚獎項：" + "、".join(sorted_labels))
            if expect == "gallery":
                out["checks"]["invite_gallery_tier"] = "旁聽席" in body
                out["checks"]["invite_role_gate_line"] = "未做過主角" in body
                shot(pg, f"{name}_invite.png")
                out["pageerrors"] = errs[:8]
                out["checks"]["zero_pageerror"] = len(errs) == 0
                out["verdict"] = "PASS" if all(out["checks"].values()) else "FAIL"
                results[name] = out
                print(f"  {out['verdict']} {json.dumps(out['checks'], ensure_ascii=False)}", flush=True)
                return
            shot(pg, f"{name}_invite.png")
            if not inv.get("visible"):
                out["verdict"] = "FAIL"
                results[name] = out
                return
            click_vis(pg, "出席")
            pg.wait_for_timeout(400)
            out["checks"]["stage_appears"] = bool(stage_state(pg).get("present"))
            w = watch(pg, 24)
            out["watch"] = w
            caps = " || ".join(e["caption"] for e in w["timeline"])
            out["checks"]["stage_gone_after"] = bool(w.get("stageGone"))
            out["checks"]["board_is_new_label"] = bool(w.get("boards")) and all(
                b in NEW_LABELS for b in w.get("boards"))
            out["checks"]["board_in_pack"] = bool(w.get("boards")) and all(
                b in [c.get("label") for c in fp.get("cats") or []] for b in w.get("boards"))
            pack_labels = [c.get("label") for c in fp.get("cats") or []]
            rep_title = (fp.get("cats") or [{}])[0].get("repWorkTitle") or ""
            # won：揭曉字幕寫明獎項名；nominated：揭曉字幕寫得主＋玩家代表作名，唔寫獎項名
            # （白牌已經驗咗焦點獎項名；呢度驗字幕有實質內容，唔係空轉）
            out["checks"]["stage_caption_has_content"] = (
                (expect == "won" and any(lab in caps for lab in pack_labels))
                or (expect == "nominated" and bool(rep_title) and rep_title in caps))
            pg.wait_for_timeout(600)
            res = modal_info(pg)
            out["result_card"] = res
            out["checks"]["result_card_shown"] = bool(res.get("visible"))
            rbody = res.get("body") or ""
            out["checks"]["result_no_old"] = not old_in(rbody)
            out["checks"]["result_lines_present"] = all(
                (c.get("line") or "") in rbody for c in fp.get("cats") or [])
            rk = result_dom(pg)
            out["result_dom"] = {k: v for k, v in rk.items() if k != "text"}
            rk_labels = [k.split("·")[-1].strip() for k in (rk.get("kickers") or [])
                         if "·" in k and k.strip().startswith(("入圍", "得獎", "觀禮"))]
            out["checks"]["result_kickers_match_pack"] = (
                sorted(rk_labels) == sorted(pack_labels))
            # 每張類別卡：kicker 嘅 label 對應嘅 line 要逐字出現喺同一張卡嘅 title
            line_by_label = {c.get("label"): c.get("line") for c in fp.get("cats") or []}
            cat_cards = [c for c in (rk.get("cards") or [])
                         if (c.get("kicker") or "").strip().startswith(("入圍", "得獎", "觀禮"))]
            out["checks"]["result_titles_match_lines"] = (
                len(cat_cards) == len(fp.get("cats") or []) and all(
                    line_by_label.get(c["kicker"].split("·")[-1].strip()) == c.get("title")
                    for c in cat_cards))
            shot(pg, f"{name}_result.png")
            click_vis(pg, "收下這晚")
            pg.wait_for_timeout(900)
            # 報紙 queue（結果卡之後先入 queue；就算 modal 仲開住都讀到）
            nq = newspaper_award(pg)
            out["newspaper"] = nq
            aw = [n for n in nq if "award" in (n.get("source") or "").lower()
                  or "頒獎" in (n.get("headline") or "") or "獎" in (n.get("headline") or "")]
            out["checks"]["newspaper_has_award"] = len(aw) >= 1
            nq_text = json.dumps(nq, ensure_ascii=False)
            out["checks"]["newspaper_no_old"] = not old_in(nq_text)
            # 手帳獎項頁
            jn = journal_awards(pg)
            out["journal"] = jn
            jtxt = jn.get("text") or ""
            out["checks"]["journal_shown"] = bool(jn.get("present")) and not jn.get("error")
            out["checks"]["journal_has_ceremony"] = CEREMONY_NAME[cer] in jtxt
            out["checks"]["journal_has_badge"] = ("得獎" in jtxt) or ("入圍" in jtxt)
            rep = (fp.get("cats") or [{}])[0].get("repWorkTitle") or ""
            out["checks"]["journal_has_rep"] = bool(rep) and rep in jtxt
            out["checks"]["journal_no_old"] = not old_in(jtxt)
            shot(pg, f"{name}_journal.png")
            # 全 DOM 舊名掃描
            dom_text = pg.evaluate("() => document.body.innerText || ''")
            out["checks"]["dom_no_old"] = not old_in(dom_text)
            out["pageerrors"] = errs[:8]
            out["checks"]["zero_pageerror"] = len(errs) == 0
            out["verdict"] = "PASS" if all(out["checks"].values()) else "FAIL"
            results[name] = out
            print(f"  {out['verdict']} cats={[ (c['id'], c['outcome'], c['score']) for c in fp.get('cats') or [] ]} "
                  f"{json.dumps(out['checks'], ensure_ascii=False)}", flush=True)
            if errs:
                print(f"    pageerrors: {errs[:3]}", flush=True)
        except Exception as e:
            # 保留已攞到嘅部分數據（pack／invite／result），唔好成個 case 洗走
            out["error"] = repr(e)
            out["verdict"] = "ERROR"
            out["pageerrors"] = errs[:8]
            results[name] = out
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
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5) as r:
            src = r.read().decode("utf-8", "replace")
        ad_gigs = parse_ad_gigs(src)
        print("ad gigs parsed:", json.dumps(ad_gigs, ensure_ascii=False), flush=True)
        results = {}
        with sync_playwright() as pw:
            for cfg in CASES:
                run_case(pw, cfg, ad_gigs, results)
        with open(os.path.join(QA, "drive188.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        npass = sum(1 for r in results.values() if r.get("verdict") == "PASS")
        print(f"== SUMMARY {npass}/{len(results)} PASS ==", flush=True)
        for k, r in results.items():
            print(f"  {k}: {r.get('verdict')} "
                  f"{json.dumps({kk: vv for kk, vv in (r.get('checks') or {}).items() if not vv}, ensure_ascii=False)}",
                  flush=True)
    finally:
        stop(srv)


if __name__ == "__main__":
    main()
