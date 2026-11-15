# v20a122 AUD91FIX 靜態測試：H1 晨報旗卡死修復＋H2 排程 modal onDismiss、紅線不變。
# 用法：python3 tests/test_aud91fix122_static.py [path-to-index.html]
# 反證：pristine main（v121）跑呢檔要 FAIL——舊 early-return 行仲喺度、confirmPlaceShoot
#   冇 onDismiss、closeModal 冇清旗行、NOTES_V20A122 未有。
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
    ok('content pack JSON 冇俾本包改動（v157＋v217＋v218＋v210＋v229／B3／B7 豁免以外一律唔准郁）',
       all(p in _v157_allowed | _v217_allowed | _v218_allowed | _v210_allowed | _v229_allowed | _v229_b3_allowed | _v229_b7_allowed for p in touched if p.startswith('content/') and p.endswith('.json')))
except Exception as e:
    print('SKIP content pack 檢查（git 唔可用：%s）' % e)

# ---- H1：early-return 改做清旗再繼續 ----
ok('H1 舊靜默 early-return 已刪', 'if(FREEPLAY_FW && FREEPLAY_FW._paperShowing) return true;' not in html)
ok('H1 新清旗行在位', 'if(FREEPLAY_FW && FREEPLAY_FW._paperShowing) FREEPLAY_FW._paperShowing = false;' in html)
ok('H1 標記在位', 'v20a122 AUD91FIX H1' in html)
pdp = seg('function presentDueMorningPaper(thenFn){', 'function renderClippingsPane()')
ok('H1 清旗行喺 presentDueMorningPaper 入面', 'FREEPLAY_FW._paperShowing = false;' in pdp)
ok('H1 清旗之後照檢查 hold／到期（流程不變）',
   pdp.index('FREEPLAY_FW._paperShowing = false;') < pdp.index('newspaperHoldForToday()') < pdp.index('pullDueNewspaperEdition()'))
ok('H1 晨報 modal 本身嘅 done() 清旗不變', 'if(FREEPLAY_FW) FREEPLAY_FW._paperShowing = false;' in pdp)
ok('H1 自檢 #105 人手 reset 不變（冇整爛）', '_ps105' in html)

# ---- H1 保底：closeModal 統一清旗 ----
cm = seg('function closeModal(){', '/* v19u Phase 2')
ok('H1 保底：closeModal 清 _paperShowing', 'FREEPLAY_FW._paperShowing = false' in cm)
ok('H1 保底標記在位', 'v20a122 AUD91FIX H1' in cm)

# ---- H2：confirmPlaceShoot 排程 modal 加 onDismiss ----
cps = seg('function confirmPlaceShoot(shoot, fromWeekday, thenFn){', 'function scheduleShoot(')
ok('H2 排程 modal 帶 onDismiss', 'onDismiss' in cps)
ok('H2 onDismiss 等同取消（go(false)）', 'onDismiss: ()=>go(false)' in cps)
ok('H2 標記在位', 'v20a122 AUD91FIX H2' in cps)
ok('H2 三個掣不變（確定佔用／只排空日／取消）',
   '確定佔用' in cps and '只排空日' in cps and '取消' in cps)
ok('H2 go() 定義不變（overwrite → placeShootOnPlan＋thenFn）',
   'placeShootOnPlan(shoot, fromWeekday, !!overwrite)' in cps)

# ---- R2 唔做：modal() 取代覆寫 _modalDismiss 嗰邊冇郁 ----
ok('R2 唔做：modal() 冇加取代前行舊 dismiss 嘅防守碼', '_modalDismiss' in html and 'v20a122' not in seg('function modal(html, buttons, opts){', 'function closeModal(){'))

# ---- NOTES 在位 ----
notes_path = os.path.join(ROOT, 'NOTES_V20A122.md')
ok('NOTES_V20A122 文件在位', os.path.exists(notes_path))
if os.path.exists(notes_path):
    notes = io.open(notes_path, encoding='utf-8').read()
    for kw in ['H1', 'H2', 'presentDueMorningPaper', 'confirmPlaceShoot', '回滾']:
        ok('NOTES covers ' + kw, kw in notes)

print('---')
print('PASS' if not fails else 'FAIL: ' + '; '.join(fails))
sys.exit(1 if fails else 0)
