# -*- coding: utf-8 -*-
# v20a113 主線順序閘靜態測試：N18／N19 跳步修復。
# 一、閘表字串在位（N18／N19／N8／N12 補鏈；N10／N16 刻意無 needDone＋註解在位）
# 二、遷移接線：storyGate113Scrub 函數在位＋normalizeSaveObj 內 levels75 之後、calib60 之前呼叫
# 三、基線不變：SAVE key／softRev／?v=；NOTES_V20A113 在位
# 反證：將新 N18 閘行還原做舊字串（模擬漏鏈），閘斷言必須翻轉；刪走遷移呼叫，接線斷言必須翻轉。
# 用法：python3 tests/test_story_gate113_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('NOTES_V20A113 在位', (p.parent / 'NOTES_V20A113.md').exists())

# --- 一、閘表 ---
def gate_ok(s):
    return ('N18: { needDone: ["N5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"] }' in s
            and 'N19: { needDone: ["N18"], weekMin: 61, yearMin: 1991, seasonIn: ["春"] }' in s
            and 'N8: { needDone: ["N7"], yearMin: 1991, seasonIn: ["夏", "秋"] }' in s
            and 'N12: { needDone: ["N11"], yearMin: 1992, seasonIn: ["春", "夏"] }' in s)
ok('閘表補鏈：N18 需 N5＋48 週／N19 需 N18＋61 週／N8 需 N7／N12 需 N11', gate_ok(src))
ok('N10／N16 刻意無 needDone（閘行唔含 needDone）',
   'N10:  { weekMin: 100, yearMin: 1991, seasonIn: ["冬"] },' in src and 'N16: { weekMin: 153, yearMin: 1992, seasonIn: ["冬"] },' in src)  # v372：加 weekMin 防年頭冬尾搶閘，仍無 needDone
ok('N10／N16 例外有 v20a113 註解（防日後有人當漏網「補返」）',
   'v20a113：刻意唔補 needDone N9' in src and 'v20a113：刻意唔補 needDone N15' in src)
ok('表頭有 v20a113 鏈審計註解', 'v20a113 鏈審計' in src)

# --- 二、遷移接線 ---
def hook_ok(s):
    i = s.find('function normalizeSaveObj(o){')
    if i < 0: return False
    j = s.find('function saveSummaryFrom(o){', i)
    body = s[i:j if j > 0 else len(s)]
    b = body.find('storyGate113Scrub(o)')
    c = body.find('calib60MissedScan(o)')
    return 0 < b < c and 'MigrateSave' not in body
ok('storyGate113Scrub 函數在位', 'function storyGate113Scrub(o, gate){' in src)
ok('接線：normalizeSaveObj 內 scrub 在 calib60 之前、冇遷移呼叫（v228）', hook_ok(src))

# --- 四、v20a249 LIVE tip：evalNode 唔再以 gatePath() 閘住 stub 分支；sentinel 回 false ---
def evalnode_seg(s):
    i = s.find('function evalNode(node, opts){')
    j = s.find('function iterNodes(){', i)
    return s[i:j if j > 0 else len(s)]
ev = evalnode_seg(src)
ok('v249 LIVE tip：evalNode 有 live 路徑（coversNode 即行 stub trigger，唔查 gatePath）',
   '} else if(typeof BehaviorGate!=="undefined" && BehaviorGate.coversNode(node)){' in ev
   and 'return BehaviorGate.evalTrigger_AND(node, opts);' in ev)
ok('v249 LIVE tip：Deng 守衛維持喺 soft 分支（唔郁）',
   'BehaviorGate.gatePath()==="soft"' in ev)
def livefn_seg(s):
    i = s.find('function liveWeekGateStillActive(){')
    return s[i:i+600]
ok('v249 LIVE tip：liveWeekGateStillActive() 回 false', 'return false;' in livefn_seg(src))
ok('v250 GRANT229：N4 收窄到 N4_b、N18 收窄到 N18_a、N5:* 已拆做 N5_a／b／c',
   '"N4:N4_b":' in src and '"N18:N18_a":' in src and '"N5:*":' not in src
   and '"N5:N5_a":' in src and '"N5:N5_b":' in src and '"N5:N5_c":' in src
   and '"N4:*":' not in src and '"N18:*":' not in src)
ok('v251 GRANT229：B 組 17 鍵齊（N7×3／N8×3／N9×2／N10×3／N11×2／N12×2／N19×2），無 wildcard',
   all(('"N%d:%s":' % (n, c)) in src for n, c in
       [(7, 'N7_a'), (7, 'N7_b'), (7, 'N7_c'), (8, 'N8_a'), (8, 'N8_b'), (8, 'N8_c'),
        (9, 'N9_a'), (9, 'N9_b'), (10, 'N10_a'), (10, 'N10_b'), (10, 'N10_c'),
        (11, 'N11_a'), (11, 'N11_b'), (12, 'N12_a'), (12, 'N12_b'),
        (19, 'N19_a'), (19, 'N19_b')])
   and '"N7:*":' not in src and '"N8:*":' not in src and '"N9:*":' not in src
   and '"N10:*":' not in src and '"N11:*":' not in src and '"N12:*":' not in src
   and '"N19:*":' not in src)
ok('v249 E1：end95SpineDone 在位＋e1Qual95 用 spine95.done',
   'function end95SpineDone(st){' in src and 'leadMedia95.length >= 2 && spine95.done' in src)
ok('v249 E1：snapshot／ladder95 有 spine95',
   'spine95: { done: spine95.done, missing: spine95.missing.slice() }' in src)

# --- 反證 ---
mut = src.replace('N18: { needDone: ["N5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"] }',
                  'N18: { yearMin: 1990, seasonIn: ["冬"] }', 1)
ok('反證：舊版 N18 閘行（漏鏈）必令閘斷言翻轉', not gate_ok(mut))
mut2 = src.replace('try{ if(typeof storyGate113Scrub==="function") storyGate113Scrub(o); }catch(_e){}', '', 1)
ok('反證：刪走 scrub 呼叫必令接線斷言翻轉', not hook_ok(mut2))

print('\n' + ('ALL PASS' if not fails else 'FAILURES: ' + ' | '.join(fails)))
sys.exit(0 if not fails else 1)
