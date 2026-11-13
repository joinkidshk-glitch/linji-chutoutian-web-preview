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
    # （C1–C5 pack nodes[0–4] 重寫，v157 brief＋SCOUT §3.1：C1–C5 無覆寫，loader 成個
    # pack fetch；其餘 content JSON 一律唔准郁）。
    _v157_allowed = {'content/story_detail_c1_to_c17.json'}
    ok('content pack JSON 冇俾本包改動（v157 只豁免 story_detail_c1_to_c17.json）',
       all(p in _v157_allowed for p in touched if p.startswith('content/') and p.endswith('.json')))
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
