# v20a124 AUD91FIX R2 靜態測試：Pair A（enterHome +90ms 強制結局）＋Pair B（contFromSlot +80ms
# 回家結算）兩個後嚟嘅 timer 各自 defer，直至 _aud91Presenting 清先呈現（公佈先、結算／結局後）。
# 用法：python3 tests/test_aud91fix124_static.py [path-to-index.html]
# 反證：pristine main（v122）跑呢檔要 FAIL——_presentForcedEnding124／_presentSettlement124
#   唔存在、舊裸 setTimeout 仲喺度、NOTES_V20A124 未有。
import io, os, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ipath = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')
html = io.open(ipath, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end):
    try:
        i = html.index(start)
    except ValueError:
        return ''
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

# ---- 紅線：SAVE key／softRev／?v=／content pack 不變 ----
ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('?v= 冇變', 'v=20a10' in html or '?v=20a10' in html or '20a10&softBehaviorGate' in html)
try:
    st = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT,
                        capture_output=True, text=True, timeout=30)
    touched = [l[3:] for l in st.stdout.splitlines() if l.strip()]
    # v157 豁免（已拍板，窄化）：只准 content/story_detail_c1_to_c17.json 呢一次改動
    # （N1–N5 pack nodes[0–4] 重寫，v157 brief＋SCOUT §3.1：N1–N5 無覆寫，loader 成個
    # pack fetch；其餘 content JSON 一律唔准郁）。
    # v217 豁免（語言審核，已拍板）：以下 15 個 content JSON 係 v217 語言審核改動
    # （收科→埋單／高仔→高俊傑／站隊→企邊／NPC＋PHASE1 粵語化等）；其餘一律唔准郁。
    _v157_allowed = {'content/story_detail_c1_to_c17.json'}
    _v217_allowed = {'content/SANDBOX_BEHAVIOR_GATE_N1_N5_SOFT_STUB_v1.json',
        'content/SOFT_RUMOR_BEHAVIOR_GATE_PLAYTEST_FIX_v1.json',
        'content/STUB_RUMOR_FRAGMENTS_v1.json',
        'content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json',
        'content/events_zh_HK.json', 'content/gift_react_copy.json',
        'content/gigs_1988.json', 'content/gigs_1989.json',
        'content/gigs_1990.json', 'content/gigs_1991.json',
        'content/npc_lines_core.json', 'content/story_beats_phase1.json',
        'content/story_detail_rival_mentor.json',
        'content/story_detail_romance_vera_hiu_choi.json'}
    # v218 豁免（review 修復，已拍板）：以下 4 個 content JSON 係 v218 有意改動——
    # STUB_NEWSPAPER_MORNING_SOFT_v1.json（B3 標題「揭入圍」→「揭曉入圍」）、
    # tutorial_zh_HK.json（A5 locale zh-Hant-written→zh-Hant-HK）、
    # gift_react_copy.json（A3「怎麼」×8 成句轉廣東話）＋story_beats_phase1.json
    # （A5 locale）兩檔已喺 v217 豁免集入面，呢度列齊做 v218 範圍記錄。
    _v218_allowed = {'content/STUB_NEWSPAPER_MORNING_SOFT_v1.json',
        'content/tutorial_zh_HK.json', 'content/gift_react_copy.json',
        'content/story_beats_phase1.json'}
    # v210 豁免（編號統一 C→N，已拍板）：以下 18 個 content JSON 係 v210 有意改動——
    # 15 檔內容 C→N 置換（含 3 檔改名，舊名＋新名一併列出，git status 會見到 D 舊名＋?? 新名）。
    _v210_allowed = {'content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json',
        'content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.json',
        'content/MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json',
        'content/MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json',
        'content/SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json',
        'content/SANDBOX_BEHAVIOR_GATE_N1_N5_SOFT_STUB_v1.json',
        'content/SOFT_PROGRESS_SEED_C3_C5_DENG_v1.json',
        'content/SOFT_PROGRESS_SEED_DUAL_MEET_THICKEN_v1.json',
        'content/SOFT_PROGRESS_SEED_N3_N5_DENG_v1.json',
        'content/STUB_NEWSPAPER_STORY_SOFT_v1.json',
        'content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json',
        'content/gift_prefs.json', 'content/gift_react_copy.json',
        'content/story_detail_c1_to_c17.json',
        'content/story_detail_n1_to_n17.json',
        'content/story_detail_rival_mentor.json',
        'content/story_detail_romance_lan_xu.json',
        'content/story_detail_romance_vera_hiu_choi.json'}
    # v229 豁免（新通告庫 B1，已拍板）：新增 content/gigs_new.json 一檔（240 張新庫，顯示年直寫；舊 pack 唔郁）。
    _v229_allowed = {'content/gigs_new.json'}
    # v229 B3 豁免（換庫：刪舊庫＋新庫做唯一來源，已拍板）：以下 15 個舊通告庫 JSON 係 B3 有意刪除
    # （5 個舊 pack＋6 個舊版檔＋4 個 PATCH 檔；新庫 gigs_new.json 係唯一來源）。
    _v229_b3_allowed = {'content/gigs_1988.json', 'content/gigs_1989.json',
        'content/gigs_1990.json', 'content/gigs_1991.json', 'content/gigs_1992.json',
        'content/gigs_1988_3.2.5-soft.json', 'content/gigs_1988_3.2.7-soft.json',
        'content/gigs_1988_3.2.8-soft.json', 'content/gigs_1988_3.2.9-soft.json',
        'content/gigs_1988_3.2.10-soft.json',
        'content/gigs_1988_v3.2.9_soft_pre_phase_d_vocal_backup.json',
        'content/PATCH_GIGS_1988_3_2_6_SOFT.json',
        'content/PATCH_GIGS_1988_3_2_8_SOFT.json',
        'content/PATCH_GIGS_1988_3_2_9_SOFT.json',
        'content/PATCH_GIGS_1988_FAVOR_RUMOR_REMAIN21_v1.json'}
    # v229 B7 豁免（Q11 刪 stub 債，已拍板）：content/STUB_FAVOR_DEBT_SEASON_v1.json 刪 debt_slot_ngai_01 一筆（支線補完 Q11，用戶 2026-11-15 21:46）。
    _v229_b7_allowed = {'content/STUB_FAVOR_DEBT_SEASON_v1.json'}
    # v239 豁免（語言重寫 RW-4，已拍板）：頒獎＋殺青兩檔逐句重寫（晨報／故事報紙兩檔已喺 v217／v210 豁免入面）。
    _v239_allowed = {'content/STUB_AWARDS_CEREMONY_v1.json', 'content/STUB_POST_SHOOT_REWARDS_v1.json'}
    # v241 豁免（語言重寫 RW-5A，已拍板）：以下 14 個 content JSON 係 RW-5A 語言重寫改動
    # （JSON 包組逐句重寫：events／npc／tutorial／beats／gift_react／gift_prefs／items／
    #  freeplay／favor／casting／era／dualMock／dualSeed／sandbox）；其餘一律唔准郁。
    _v241_allowed = {'content/MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json',
        'content/SANDBOX_BEHAVIOR_GATE_N1_N5_SOFT_STUB_v1.json',
        'content/SOFT_PROGRESS_SEED_DUAL_MEET_THICKEN_v1.json',
        'content/STUB_CASTING_TAGS_v1.json', 'content/STUB_ERA_STARS_MVP_v1.json',
        'content/STUB_FAVOR_DEBT_SEASON_v1.json', 'content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json',
        'content/events_zh_HK.json', 'content/gift_prefs.json', 'content/gift_react_copy.json',
        'content/items_gifts.json', 'content/npc_lines_core.json', 'content/story_beats_phase1.json',
        'content/tutorial_zh_HK.json'}
    ok('content pack JSON 冇俾本包改動（v157＋v217＋v218＋v210＋v229／B3／B7＋v239＋v241 豁免以外一律唔准郁）',
       all(p in _v157_allowed | _v217_allowed | _v218_allowed | _v210_allowed | _v229_allowed | _v229_b3_allowed | _v229_b7_allowed | _v239_allowed | _v241_allowed for p in touched if p.startswith('content/') and p.endswith('.json')))
except Exception as e:
    print('SKIP content pack 檢查（git 唔可用：%s）' % e)

# ---- Pair A：enterHome 強制結局 timer 加 defer guard ----
eh = seg('function enterHome(summary, editable, initialTab){', 'function resetPlanDraft(){')
ok('Pair A guard 函數在位', '_presentForcedEnding124' in eh)
ok('Pair A guard check _aud91Presenting', '_aud91Presenting' in eh and 'setTimeout(_presentForcedEnding124, 300)' in eh)
ok('Pair A guard 旗清先行 conseq61PresentForcedEnding',
   'conseq61PresentForcedEnding();' in eh and '_aud91Presenting' in eh and eh.index('_aud91Presenting') < eh.index('conseq61PresentForcedEnding();'))
ok('Pair A 初次延遲維持 90ms', 'setTimeout(_presentForcedEnding124, 90)' in eh)
ok('Pair A 舊裸 timer 已刪', 'setTimeout(()=>{ try{ conseq61PresentForcedEnding(); }catch(_e){} }, 90)' not in eh)
ok('Pair A 標記在位', 'v20a124 AUD91FIX R2 Pair A' in eh)
ok('Pair A 前置條件不變（pendingEnding＋未結局）',
   'S.conseq61.pendingEnding && !S.ending410' in eh)
ok('Pair A aud91 本身 +50ms timer 不變', 'aud91PresentDue(null);' in eh)
ok('Pair A 三連撞：等埋結算 done 先出結局',
   '_week105SettlePending124' in eh and '_week105SettleDone124' in eh and eh.count('setTimeout(_presentForcedEnding124, 300)') == 2)
ok('Pair A 三連撞：冇結算等緊嗰陣唔會被拖住（pending 假即過）',
   '&& !_week105SettleDone124' in eh)

# ---- Pair B：contFromSlot 回家結算 timer 加 defer guard ----
cf = seg('function contFromSlot(slot){', 'function cont(){')
ok('Pair B guard 函數在位', '_presentSettlement124' in cf)
ok('Pair B guard check _aud91Presenting', '_aud91Presenting' in cf and 'setTimeout(_presentSettlement124, 300)' in cf)
ok('Pair B guard 旗清先開結算 modal',
   '回家結算' in cf and '_aud91Presenting' in cf and cf.index('_aud91Presenting') < cf.index('回家結算'))
ok('Pair B 初次延遲維持 80ms', 'setTimeout(_presentSettlement124, 80)' in cf)
ok('Pair B 結算 modal 內容不變（標題＋掣＋唔重扣行字）',
   '編排新一週行程' in cf and '金額嗰陣已經入帳，唔會重扣' in cf)
ok('Pair B 舊裸 timer 已刪（modal 直掛 setTimeout 80）',
   'setTimeout(()=>{\n        try{\n          modal(`<h3>回家結算' not in cf)
ok('Pair B 標記在位', 'v20a124 AUD91FIX R2 Pair B' in cf)
ok('Pair B enterHome 呼叫不變（先入編排步再補結算）',
   'enterHome({ weekNum: wp105.week' in cf)
ok('Pair B 三連撞：contFromSlot 記低結算等緊（pending 真／done 假）',
   '_week105SettlePending124 = true' in cf and '_week105SettleDone124 = false' in cf)
ok('Pair B 三連撞：結算掣 on 記 done', '_week105SettleDone124 = true' in cf)
ok('Pair B 三連撞：結算 modal 有 onDismiss 記 done（遮罩點走都計）',
   'onDismiss' in cf and cf.count('_week105SettleDone124 = true') == 2)

# ---- 三連撞旗：module-level 宣告在位 ----
ok('三連撞旗宣告在位', 'var _week105SettlePending124 = false;' in html and 'var _week105SettleDone124 = false;' in html)
ok('三連撞旗宣告跟 _aud91Presenting 埋一齊',
   'var _week105SettlePending124' in html and 'let _aud91Presenting' in html
   and abs(html.index('var _week105SettlePending124') - html.index('let _aud91Presenting')) < 1200)

# ---- R2 唔做：modal() 冇加通用 guard ----
mo = seg('function modal(html, buttons, opts){', 'function closeModal(){')
ok('R2 唔做：modal() 冇 v20a124 防守碼', 'v20a124' not in mo)
ok('R2 唔做：modal() _modalDismiss 覆寫行不變',
   '_modalDismiss = typeof opts.onDismiss==="function" ? opts.onDismiss : null' in mo)

# ---- 兩個 guard 對稱：同一個 defer 間隔、同一個旗 ----
ok('對稱：兩個 guard 都係 300ms 再 check',
   html.count('setTimeout(_presentForcedEnding124, 300)') == 2 and html.count('setTimeout(_presentSettlement124, 300)') == 1)
ok('對稱：冇其他地方引用 _presentForcedEnding124／_presentSettlement124',
   html.count('_presentForcedEnding124') == 4 and html.count('_presentSettlement124') == 3)

# ---- NOTES 在位 ----
notes_path = os.path.join(ROOT, 'NOTES_V20A124.md')
ok('NOTES_V20A124 文件在位', os.path.exists(notes_path))
if os.path.exists(notes_path):
    notes = io.open(notes_path, encoding='utf-8').read()
    for kw in ['Pair A', 'Pair B', '三連撞', '_aud91Presenting', '_week105SettleDone124', 'conseq61PresentForcedEnding', '回滾']:
        ok('NOTES covers ' + kw, kw in notes)

print('---')
print('PASS' if not fails else 'FAIL: ' + '; '.join(fails))
sys.exit(1 if fails else 0)
