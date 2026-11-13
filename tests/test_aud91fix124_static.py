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
    # （C1–C5 pack nodes[0–4] 重寫，v157 brief＋SCOUT §3.1：C1–C5 無覆寫，loader 成個
    # pack fetch；其餘 content JSON 一律唔准郁）。
    _v157_allowed = {'content/story_detail_c1_to_c17.json'}
    ok('content pack JSON 冇俾本包改動（v157 只豁免 story_detail_c1_to_c17.json）',
       all(p in _v157_allowed for p in touched if p.startswith('content/') and p.endswith('.json')))
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
