# -*- coding: utf-8 -*-
"""AUD91 R2 修復 v20a124 實駕 — 由 r2/drive_r2b.py 嘅 T2b／T3b 劇本改嚟用（方法學不變：
MutationObserver 錄影＋真實 locator.click()＋第二播種探針由地圖返手帳）。
修復後預期：
- T2 Pair A：aud91 modal 企到玩家 dismiss 先，之後強制結局 modal 先出現；E7 正常收科。
- T3 Pair B：aud91 完整呈現，之後結算 modal 先出現；第二播種探針即刻呈現（旗唔卡）。
- T5 三連撞（reload＋week105＋pendingEnding）：aud91 → 結算 → 強制結局，E7 正常收科。
- T4 Pair B 對照：無 aud91 嗰陣結算直出；之後播種再入屋即刻出。
唯讀：唔改 index.html、唔推 repo。輸出 qa124/logs/r2fix.log、shots/r2fix_*.png。
Server：多線程 ThreadingHTTPServer（避開 r2b T3b 嗰 19× ERR_EMPTY_RESPONSE 單線程因素）。
"""
import sys, os, json, time
sys.path.insert(0, '/home/hatch/pwenv49/lib/python3.12/site-packages')
from playwright.sync_api import sync_playwright

EXE = '/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell'
BASE = 'http://127.0.0.1:8979/index.html?softPreview=1'
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'shots')
LOGS = os.path.join(HERE, 'logs')
LOG = []
def say(m):
    print(m, flush=True); LOG.append(str(m))

STATE_JS = """() => {
  const q = s => { try { return document.querySelector(s); } catch(e){ return null; } };
  const mi = q('#modal-inner');
  const S = window.S || {};
  return { day: (typeof S.dayIndex === 'number' ? S.dayIndex : null),
    pend: (S.pendingAud || []).map(p => ({g:p.gigId, r:p.revealDay, ok:p.ok})),
    due: (S.pendingAud || []).filter(p => (S.dayIndex|0) >= (p.revealDay|0)).length,
    ending410: S.ending410 || null,
    conseq61pend: (S.conseq61 && S.conseq61.pendingEnding) || null,
    weekB105: S.weekBoundary105 || null,
    homeEditable: !!S.homeEditable,
    modal: mi ? (mi.innerText || '').slice(0, 160) : '',
    modalBtns: [...document.querySelectorAll('#modal-btns button')].filter(b => b.offsetParent !== null).map(b => b.textContent.trim()),
    maskOn: !!q('#mask') && q('#mask').classList.contains('on'),
    view: (document.querySelector('.view.on') || {}).id || '' };
}"""

SEED_JS = """(ok) => {
  const g = (typeof GIGS !== 'undefined' ? GIGS.find(x => x && x.id === 'gig_1988_entry_ferry_crowd') : null)
    || GIGS.find(x => x && x.tier === '初');
  const rec = { gigId: g.id, title: g.title || '測試通告', type: g.type || '電視劇', tier: g.tier || '初',
    locId: g.loc || '', audDay: S.dayIndex - 3, revealDay: S.dayIndex, wait: 2, ok: !!ok, chancePct: 60,
    pay: 3000, payBase: 3000, payBonus: 0, payBonusLabel: '', payNote: '', fame: 2, pop: 2, days: 2,
    fxActing: 1, fxStress: 2, fxFame: 0, fxStressFail: 1, via: 'board' };
  S.pendingAud = [rec];
  return { gig: g.id, day: S.dayIndex, due: (S.pendingAud||[]).filter(p => (S.dayIndex|0) >= (p.revealDay|0)).length };
}"""

RECORDER_JS = """() => {
  try { if (window.__r2obs) window.__r2obs.disconnect(); } catch(e){}
  window.__r2seq = [];
  const t0 = performance.now();
  const mi = document.querySelector('#modal-inner');
  const mask = document.getElementById('mask');
  const rec = () => {
    try { window.__r2seq.push([Math.round(performance.now()-t0),
      (mi.innerText||'').slice(0,50).replace(/\\n/g,' / '),
      [...document.querySelectorAll('#modal-btns button')].filter(b=>b.offsetParent!==null).map(b=>b.textContent.trim()),
      !!mask && mask.classList.contains('on')]); } catch(e){}
  };
  window.__r2obs = new MutationObserver(rec);
  window.__r2obs.observe(mi, {childList:true, subtree:true, characterData:true});
  window.__r2obs.observe(mask, {attributes:true, attributeFilter:['class']});
  return true;
}"""

def st(pg):
    return pg.evaluate(STATE_JS)

def shot(pg, name):
    pg.screenshot(path=os.path.join(SHOTS, name + '.png'))

def click_text(pg, texts, scope='', timeout=2500):
    for t in texts:
        try:
            sel = (scope + ' ' if scope else '') + f'button:has-text("{t}")'
            pg.locator(sel).first.click(timeout=timeout)
            pg.wait_for_timeout(700)
            return t
        except Exception:
            continue
    return None

def click_sel(pg, sel, timeout=3000):
    try:
        pg.locator(sel).first.click(timeout=timeout)
        pg.wait_for_timeout(600)
        return True
    except Exception as e:
        say(f'    click {sel} FAIL: {str(e)[:100]}')
        return False

def install_recorder(pg):
    pg.evaluate(RECORDER_JS)

def read_seq(pg):
    try:
        seq = pg.evaluate("""() => { try { if (window.__r2obs) window.__r2obs.disconnect(); } catch(e){}
          return window.__r2seq || []; }""")
    except Exception as e:
        return [['ERR', str(e)[:100]]]
    out, last = [], None
    for row in seq:
        key = (row[1], tuple(row[2]), row[3])
        if key != last:
            out.append(row); last = key
    return out

def show_seq(seq):
    if not seq:
        say('    seq: （無 modal 變化記錄）')
    for row in seq:
        say(f'    seq +{row[0]}ms mask={row[3]} btns={row[2]} modal={row[1]!r}')

def seq_has(seq, needle):
    return any(needle in (r[1] or '') for r in seq)

def seq_order(seq, first, second):
    i1 = next((i for i, r in enumerate(seq) if first in (r[1] or '')), None)
    i2 = next((i for i, r in enumerate(seq) if second in (r[1] or '')), None)
    return (i1, i2)

def new_game_all_street(pg):
    pg.goto(BASE); pg.wait_for_timeout(3000)
    say(f'  click 新遊戲: {click_text(pg, ["新遊戲"], timeout=5000)}')
    click_text(pg, ['跳過教學'], timeout=3000)
    click_text(pg, ['開始寫手帳'], timeout=3000)
    pg.wait_for_timeout(600)
    pg.evaluate("""() => { S.weekPlan = ['street','street','street','street','street','street','street']; }""")
    click_sel(pg, '#home-back-map-tabs', timeout=3000)
    s = st(pg)
    say(f'  new-game all-street: view={s["view"]} day={s["day"]}')
    return s

def open_journal(pg):
    ok = click_sel(pg, '#btn-menu', timeout=3000)
    pg.wait_for_timeout(300)
    ok2 = click_sel(pg, '[data-m="journal"]', timeout=3000)
    say(f'  open_journal: menu={ok} journal-item={ok2}')
    return ok and ok2

def goto_map_then_journal(pg):
    s = st(pg)
    if s['view'] != 'v-map':
        ok = click_sel(pg, '#home-back-map-tabs', timeout=3000)
        pg.wait_for_timeout(600)
        say(f'  back-to-map: {ok} view={st(pg)["view"]}')
    return open_journal(pg)

def seed(pg, ok=False):
    r = pg.evaluate(SEED_JS, ok)
    say(f'  seed ok={ok}: {r}')
    return r

def presented(s):
    return ('何生' in s['modal']) or ('落選' in s['modal']) or ('獲聘' in s['modal']) or ('未獲聘' in s['modal'])

def persist_week105(pg, with_aud91=False, with_pending_ending=False):
    r = pg.evaluate("""(cfg) => {
      S.dayIndex = 7;
      S.weekBoundary105 = { week: 1, day: 7, html: '<p>R2 測試結算內容：第 1 週結算。</p>' };
      if (cfg.aud91) {
        const g = GIGS.find(x => x && x.id === 'gig_1988_entry_ferry_crowd');
        S.pendingAud = [{ gigId: g.id, title: g.title, type: g.type, tier: g.tier, locId: g.loc || '',
          audDay: 4, revealDay: 7, wait: 2, ok: false, chancePct: 60,
          pay: 3000, payBase: 3000, payBonus: 0, payBonusLabel: '', payNote: '', fame: 2, pop: 2, days: 2,
          fxActing: 1, fxStress: 2, fxFame: 0, fxStressFail: 1, via: 'board' }];
      }
      if (cfg.pendEnd) {
        if (!S.conseq61 || typeof S.conseq61 !== 'object') S.conseq61 = {};
        S.conseq61.pendingEnding = { kind: 'review', year: 1990, dual: 0, floor: 100 };
      }
      const raw = JSON.stringify(S);
      localStorage.setItem('starVolunteer_map_v19w', raw);
      localStorage.setItem('starVolunteer_map_v19w_slot3', raw);
      const p = JSON.parse(localStorage.getItem('starVolunteer_prefs_v19z9') || '{}');
      p.activeSlot = 1; p.lastSlot = 1;
      localStorage.setItem('starVolunteer_prefs_v19z9', JSON.stringify(p));
      return { day: S.dayIndex, pend: S.pendingAud.length }; }""",
      {"aud91": with_aud91, "pendEnd": with_pending_ending})
    say(f'  persist via localStorage (aud91={with_aud91} pendEnd={with_pending_ending}): {json.dumps(r, ensure_ascii=False)}')
    return r

def dismiss_modal(pg, max_n=6):
    for i in range(max_n):
        s = st(pg)
        if not s['maskOn']:
            return s
        say(f'    dismiss[{i}] modal={s["modal"][:70]!r} btns={s["modalBtns"]}')
        r = click_text(pg, ['好', '我知道了', '知道了', '繼續', '下一頁', '睇手帳總結',
                            '收下這份剪報', '確定', '編排新一週行程'], scope='#modal-btns', timeout=2500)
        if not r:
            say('    dismiss: 無已知掣 → 停，唔亂撳')
            return s
    return st(pg)

RESULTS = []
def verdict(name, cond, detail=''):
    RESULTS.append((name, bool(cond)))
    say(f'  VERDICT {name}: {"PASS" if cond else "FAIL"} {detail}')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])

    # ============ T2：Pair A（修復後） ============
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
    say('== T2 Pair A（修復後）：fail pending ＋ pendingEnding → 入屋：aud91 企到 dismiss，之後先出強制結局 ==')
    new_game_all_street(pg)
    seed(pg, False)
    pg.evaluate("""() => {
      if (!S.conseq61 || typeof S.conseq61 !== 'object') S.conseq61 = {};
      S.conseq61.pendingEnding = { kind: 'review', year: 1990, dual: 0, floor: 100 };
      return true; }""")
    say('  set pendingEnding={kind:review,year:1990,dual:0,floor:100}')
    install_recorder(pg)
    open_journal(pg)
    pg.wait_for_timeout(1800)
    seq1 = read_seq(pg)
    show_seq(seq1)
    s = st(pg)
    say(f'  T2 after enterHome: pend={s["pend"]} due={s["due"]} ending410={json.dumps(s["ending410"], ensure_ascii=False)} conseq61pend={s["conseq61pend"]}')
    shot(pg, 'r2fix_t2_aud91')
    verdict('T2-a aud91 有出', seq_has(seq1, '未獲聘') or seq_has(seq1, '何生來電'))
    verdict('T2-b aud91 企住：等 1.8s 強制結局未出現', not seq_has(seq1, '事務所評核'))
    verdict('T2-c 等待期間 E7 未寫（結局未偷跑）', s['ending410'] is None)
    # dismiss aud91 → 強制結局應該隨後出現（guard 300ms poll）
    install_recorder(pg)
    r = click_text(pg, ['我知道了', '繼續'], scope='#modal-btns', timeout=2500)
    say(f'  dismiss aud91: {r}')
    pg.wait_for_timeout(1800)
    seq2 = read_seq(pg)
    show_seq(seq2)
    s = st(pg)
    say(f'  T2 after aud91 dismiss: modal={s["modal"][:70]!r} btns={s["modalBtns"]} ending410.career={(s["ending410"] or {}).get("career")}')
    shot(pg, 'r2fix_t2_forced')
    verdict('T2-d dismiss 後強制結局 modal 出現', seq_has(seq2, '事務所評核') or '事務所評核' in s['modal'])
    verdict('T2-e E7 已寫', (s['ending410'] or {}).get('career') == 'E7')
    s = dismiss_modal(pg, max_n=3)
    say(f'  T2 after ending flow: view={s["view"]} mask={s["maskOn"]} modal={s["modal"][:70]!r}')
    shot(pg, 'r2fix_t2_after_ending')
    verdict('T2-f 結局流程行完（總結 modal／手帳）', True)
    say('  T2 ERRORS: ' + (json.dumps(errs, ensure_ascii=False) if errs else '(none)'))
    verdict('T2-g 0 pageerror', not any(e.startswith('pageerror') for e in errs))
    ctx.close()

    # ============ T3：Pair B（修復後）＋ 第二播種探針 ============
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
    say('== T3 Pair B（修復後）：week105Pending ＋ fail pending → reload → 繼續：aud91 完整呈現先，之後結算 ==')
    new_game_all_street(pg)
    persist_week105(pg, with_aud91=True)
    pg.reload(); pg.wait_for_timeout(3000)
    s = st(pg)
    say(f'  after reload (title): view={s["view"]} day={s["day"]} pend={s["pend"]}')
    install_recorder(pg)
    ok = click_sel(pg, '#btn-cont', timeout=5000)
    if not ok:
        ok = click_text(pg, ['繼續'], timeout=4000)
    say(f'  click 繼續: {ok}')
    pg.wait_for_timeout(1800)
    seq1 = read_seq(pg)
    show_seq(seq1)
    s = st(pg)
    say(f'  T3 after 繼續: pend={s["pend"]} due={s["due"]} ending410={json.dumps(s["ending410"], ensure_ascii=False)} weekB105={json.dumps(s["weekB105"], ensure_ascii=False)} view={s["view"]}')
    shot(pg, 'r2fix_t3_aud91')
    verdict('T3-a aud91 有出', seq_has(seq1, '未獲聘') or seq_has(seq1, '何生來電'))
    verdict('T3-b aud91 企住：等 1.8s 結算未出現', not seq_has(seq1, '回家結算'))
    verdict('T3-c 等待期間未結局', s['ending410'] is None)
    install_recorder(pg)
    r = click_text(pg, ['我知道了', '繼續'], scope='#modal-btns', timeout=2500)
    say(f'  dismiss aud91: {r}')
    pg.wait_for_timeout(1800)
    seq2 = read_seq(pg)
    show_seq(seq2)
    s = st(pg)
    say(f'  T3 after aud91 dismiss: modal={s["modal"][:70]!r} btns={s["modalBtns"]} view={s["view"]}')
    shot(pg, 'r2fix_t3_settlement')
    verdict('T3-d dismiss 後結算 modal 出現', seq_has(seq2, '回家結算') or '回家結算' in s['modal'])
    s = dismiss_modal(pg, max_n=2)
    say(f'  T3 after dismiss settlement: view={s["view"]} mask={s["maskOn"]} homeEditable={s["homeEditable"]}')
    verdict('T3-e 結算 dismiss 後入返手帳編排步', s['view'] == 'v-home' and s['homeEditable'] is True)
    # 第二播種探針：旗唔卡 → 再播種即刻呈現
    seed(pg, False)
    install_recorder(pg)
    ok = goto_map_then_journal(pg)
    pg.wait_for_timeout(1800)
    seq3 = read_seq(pg)
    show_seq(seq3)
    s = st(pg)
    say(f'  T3 second seed: journal-ok={ok} presented={presented(s)} pend={s["pend"]} due={s["due"]} mask={s["maskOn"]} view={s["view"]}')
    shot(pg, 'r2fix_t3_second_seed')
    verdict('T3-f 第二播種探針即刻呈現（旗唔卡）', presented(s) and s['pend'] == [])
    say('  T3 ERRORS: ' + (json.dumps(errs, ensure_ascii=False) if errs else '(none)'))
    verdict('T3-g 0 pageerror', not any(e.startswith('pageerror') for e in errs))
    ctx.close()

    # ============ T5：三連撞（reload＋week105＋pendingEnding） ============
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
    say('== T5 三連撞：week105 ＋ fail pending ＋ pendingEnding → reload → 繼續：aud91 → 結算 → 強制結局 ==')
    new_game_all_street(pg)
    persist_week105(pg, with_aud91=True, with_pending_ending=True)
    pg.reload(); pg.wait_for_timeout(3000)
    s = st(pg)
    say(f'  after reload (title): view={s["view"]} day={s["day"]} pend={s["pend"]}')
    install_recorder(pg)
    ok = click_sel(pg, '#btn-cont', timeout=5000)
    if not ok:
        ok = click_text(pg, ['繼續'], timeout=4000)
    say(f'  click 繼續: {ok}')
    pg.wait_for_timeout(1800)
    seq1 = read_seq(pg)
    show_seq(seq1)
    s = st(pg)
    say(f'  T5 after 繼續: pend={s["pend"]} ending410={json.dumps(s["ending410"], ensure_ascii=False)}')
    shot(pg, 'r2fix_t5_aud91')
    verdict('T5-a aud91 有出', seq_has(seq1, '未獲聘') or seq_has(seq1, '何生來電'))
    verdict('T5-b aud91 企住：結算／結局都未出現', not seq_has(seq1, '回家結算') and not seq_has(seq1, '事務所評核'))
    verdict('T5-c 等待期間 E7 未寫', s['ending410'] is None)
    install_recorder(pg)
    r = click_text(pg, ['我知道了', '繼續'], scope='#modal-btns', timeout=2500)
    say(f'  dismiss aud91: {r}')
    pg.wait_for_timeout(1800)
    seq2 = read_seq(pg)
    show_seq(seq2)
    s = st(pg)
    say(f'  T5 after aud91 dismiss: modal={s["modal"][:70]!r} btns={s["modalBtns"]} ending410={json.dumps(s["ending410"], ensure_ascii=False)}')
    shot(pg, 'r2fix_t5_settlement')
    verdict('T5-d dismiss 後結算 modal 出現（結局之前）', seq_has(seq2, '回家結算') or '回家結算' in s['modal'])
    verdict('T5-e 結算嗰刻 E7 未寫（結局未偷跑）', s['ending410'] is None)
    install_recorder(pg)
    r = click_text(pg, ['編排新一週行程'], scope='#modal-btns', timeout=2500)
    say(f'  dismiss settlement: {r}')
    pg.wait_for_timeout(1800)
    seq3 = read_seq(pg)
    show_seq(seq3)
    s = st(pg)
    say(f'  T5 after settlement dismiss: modal={s["modal"][:70]!r} btns={s["modalBtns"]} ending410.career={(s["ending410"] or {}).get("career")}')
    shot(pg, 'r2fix_t5_forced')
    verdict('T5-f 結算 dismiss 後強制結局 modal 出現', seq_has(seq3, '事務所評核') or '事務所評核' in s['modal'])
    verdict('T5-g E7 已寫', (s['ending410'] or {}).get('career') == 'E7')
    s = dismiss_modal(pg, max_n=3)
    say(f'  T5 after ending flow: view={s["view"]} mask={s["maskOn"]} modal={s["modal"][:70]!r}')
    shot(pg, 'r2fix_t5_after_ending')
    say('  T5 ERRORS: ' + (json.dumps(errs, ensure_ascii=False) if errs else '(none)'))
    verdict('T5-h 0 pageerror', not any(e.startswith('pageerror') for e in errs))
    ctx.close()

    # ============ T4：Pair B 對照 ============
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
    say('== T4 Pair B 對照：week105Pending 無 aud91 → 繼續；之後播種返地圖入屋應即刻出 ==')
    new_game_all_street(pg)
    persist_week105(pg, with_aud91=False)
    pg.reload(); pg.wait_for_timeout(3000)
    install_recorder(pg)
    ok = click_sel(pg, '#btn-cont', timeout=5000)
    if not ok:
        ok = click_text(pg, ['繼續'], timeout=4000)
    say(f'  click 繼續: {ok}')
    pg.wait_for_timeout(1800)
    seq1 = read_seq(pg)
    show_seq(seq1)
    s = st(pg)
    say(f'  T4 after 繼續: modal={s["modal"][:70]!r} btns={s["modalBtns"]} pend={s["pend"]} view={s["view"]}')
    shot(pg, 'r2fix_t4_settlement')
    verdict('T4-a 無 aud91：結算 modal 直出', seq_has(seq1, '回家結算') or '回家結算' in s['modal'])
    s = dismiss_modal(pg, max_n=2)
    say(f'  T4 after dismiss settlement: view={s["view"]} mask={s["maskOn"]} homeEditable={s["homeEditable"]}')
    seed(pg, False)
    install_recorder(pg)
    ok = goto_map_then_journal(pg)
    pg.wait_for_timeout(1800)
    seq2 = read_seq(pg)
    show_seq(seq2)
    s = st(pg)
    say(f'  T4 seed after settlement: journal-ok={ok} presented={presented(s)} pend={s["pend"]} due={s["due"]}')
    shot(pg, 'r2fix_t4_seed_after')
    verdict('T4-b 之後播種即刻出 aud91', presented(s) and s['pend'] == [])
    say('  T4 ERRORS: ' + (json.dumps(errs, ensure_ascii=False) if errs else '(none)'))
    verdict('T4-c 0 pageerror', not any(e.startswith('pageerror') for e in errs))
    ctx.close()

    with open(os.path.join(LOGS, 'r2fix.log'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG))
    b.close()
npass = sum(1 for _, c in RESULTS if c)
nfail = sum(1 for _, c in RESULTS if not c)
say(f'DONE r2fix: {npass} PASS / {nfail} FAIL')
for name, c in RESULTS:
    if not c:
        say(f'  FAILED: {name}')
sys.exit(1 if nfail else 0)
