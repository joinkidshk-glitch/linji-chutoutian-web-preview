# -*- coding: utf-8 -*-
# v20a113 主線順序閘靜態測試：C18／C19 跳步修復。
# 一、閘表字串在位（C18／C19／C11／C15 補鏈；C9／C13 刻意無 needDone＋註解在位）
# 二、遷移接線：storyGate113Scrub 函數在位＋normalizeSaveObj 內 levels75 之後、calib60 之前呼叫
# 三、基線不變：SAVE key／softRev／?v=；NOTES_V20A113 在位
# 反證：將新 C18 閘行還原做舊字串（模擬漏鏈），閘斷言必須翻轉；刪走遷移呼叫，接線斷言必須翻轉。
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
    return ('C18: { needDone: ["C5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"] }' in s
            and 'C19: { needDone: ["C18"], weekMin: 61, yearMin: 1991, seasonIn: ["春"] }' in s
            and 'C11: { needDone: ["C7"], yearMin: 1991, seasonIn: ["夏", "秋"] }' in s
            and 'C15: { needDone: ["C10"], tagAny: ["動作", "action", "tag_action", "身手好"], yearMin: 1992, seasonIn: ["春"] }' in s)
ok('閘表補鏈：C18 需 C5＋48 週／C19 需 C18＋61 週／C11 需 C7／C15 需 C10', gate_ok(src))
ok('C9／C13 刻意無 needDone（閘行唔含 needDone）',
   'C9:  { yearMin: 1991, seasonIn: ["冬"] },' in src and 'C13: { yearMin: 1992, seasonIn: ["冬"] },' in src)
ok('C9／C13 例外有 v20a113 註解（防日後有人當漏網「補返」）',
   'v20a113：刻意唔補 needDone C8' in src and 'v20a113：刻意唔補 needDone C16' in src)
ok('表頭有 v20a113 鏈審計註解', 'v20a113 鏈審計' in src)

# --- 二、遷移接線 ---
def hook_ok(s):
    i = s.find('function normalizeSaveObj(o){')
    if i < 0: return False
    j = s.find('function saveSummaryFrom(o){', i)
    body = s[i:j if j > 0 else len(s)]
    a = body.find('levels75MigrateSave(o)')
    b = body.find('storyGate113Scrub(o)')
    c = body.find('calib60MissedScan(o)')
    return 0 < a < b < c
ok('storyGate113Scrub 函數在位', 'function storyGate113Scrub(o, gate){' in src)
ok('接線：normalizeSaveObj 內 levels75 之後、calib60 之前呼叫 scrub', hook_ok(src))

# --- 反證 ---
mut = src.replace('C18: { needDone: ["C5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"] }',
                  'C18: { yearMin: 1990, seasonIn: ["冬"] }', 1)
ok('反證：舊版 C18 閘行（漏鏈）必令閘斷言翻轉', not gate_ok(mut))
mut2 = src.replace('try{ if(typeof storyGate113Scrub==="function") storyGate113Scrub(o); }catch(_e){}', '', 1)
ok('反證：刪走遷移呼叫必令接線斷言翻轉', not hook_ok(mut2))

print('\n' + ('ALL PASS' if not fails else 'FAILURES: ' + ' | '.join(fails)))
sys.exit(0 if not fails else 1)
