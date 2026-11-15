# -*- coding: utf-8 -*-
# v20a228：拎走全部四個存檔遷移函數（c2n210／years66／jan67／levels75）。
# 用法：python3 qa228/delete228.py（喺 worktree 根目錄行；只改 index.html）
# 做法：內容錨點定位刪除區間，逐區驗證內容先刪；唔用行號硬編、唔用逐對 re.sub。
import sys

P = 'index.html'
lines = open(P, encoding='utf-8').read().split('\n')
orig_total = len(lines)

def find(pred, start=0):
    for i in range(start, len(lines)):
        if pred(lines[i]):
            return i
    raise AssertionError('anchor not found: %s' % pred)

def find_line(text, start=0):
    i = find(lambda s: s == text, start)
    return i

def expect(i, text):
    assert lines[i] == text, 'L%d mismatch:\n  got: %r\n  exp: %r' % (i + 1, lines[i], text)

# ---------- 單行／註解編輯（先做，行號未郁） ----------
# (E) COURSE_DEFS 註解：拎走遷移句
i = find_line('     COURSE_DEFS 只剩 7 基礎課；舊檔嘅中課痕跡由 levels75MigrateSave 喺載入時遷移。 */')
lines[i] = '     COURSE_DEFS 只剩 7 基礎課。 */'

# (F) LEVELS75 block 註解：拎走遷移句
i = find_line('   「而家邊級、仲差幾堂升級」隨時計得返；舊進階課點遷移見 levels75MigrateSave。')
lines[i] = '   「而家邊級、仲差幾堂升級」隨時計得返。'

# (A) YEARS66 block header：拎走遷移句，註解收尾
i = find_line('   __y66w 旗冪等，同一物件唔會俾 +2 兩次。舊存檔由 years66MigrateSave 喺 normalizeSaveObj')
expect(i + 1, '   一次性遷移（epoch guard：dayIndex 不變、衍生日期自動 +2、已存絕對年份鍵 remap）。 */')
lines[i] = '   __y66w 旗冪等，同一物件唔會俾 +2 兩次。 */'
del lines[i + 1]

# (C) JAN67 block header：兩件事 → 一件事
i = find_line('   本 block 兩件事：(1) 舊存檔遷移 jan67MigrateSave；(2) 開局季節文字定點修正')
expect(i + 1, '   jan67OpeningTextFix（pack 本體唔改，行 TEXTFIX55／YEARS66 載入修正先例）。')
lines[i] = '   本 block 做開局季節文字定點修正 jan67OpeningTextFix（pack 本體唔改，'
lines[i + 1] = '   行 TEXTFIX55／YEARS66 載入修正先例）。'

# (H) fresh() 印：留印（存檔格式相容），註解講明遷移已刪
i = find_line('    years66Shifted:1, /* v20a66：新檔出生已係 1990 曆法，存檔遷移唔好掂 */')
lines[i] = '    years66Shifted:1, /* v20a228：遷移已刪，留印只為存檔格式相容 */'
i = find_line('    startEpoch67:1, /* v20a67：新檔出生已係 1 月 epoch，JAN67 遷移唔好掂 */')
lines[i] = '    startEpoch67:1, /* v20a228：遷移已刪，留印只為存檔格式相容 */'

# (G) LEVELS75_MID_OF：只得遷移用，拎走
i = find_line('const LEVELS75_MID_OF = { train_acting_mid: "train_acting", train_stage_mid: "train_stage" };')
del lines[i]

# ---------- 區間刪除（由底向上，等行號唔郁） ----------
spans = []  # (start_idx, end_idx_exclusive, label)

# (K) c2n210MigrateSave 函數：由 def 到 maybeUnlockMidCourses 之前
s = find_line('function c2n210MigrateSave(o){')
e = find_line('function maybeUnlockMidCourses(notes){', s)
assert 'function c2n210MigrateSave' in lines[s]
assert not any(l.startswith('function ') for l in lines[s + 1:e]), 'unexpected fn inside c2n210 span'
spans.append((s, e, 'c2n210MigrateSave'))

# (J) levels75MigrateSave 函數：由 def 到 c2n210 def 之前
s = find_line('function levels75MigrateSave(o){')
e = find_line('function c2n210MigrateSave(o){', s)
assert not any(l.startswith('function ') for l in lines[s + 1:e]), 'unexpected fn inside levels75 span'
spans.append((s, e, 'levels75MigrateSave'))

# (I) normalizeSaveObj 呼叫點：由 v20a66 註解到 c2n210 呼叫行
s = find_line('  /* v20a66 YEARS66：舊存檔年份遷移（epoch guard：dayIndex 不變、絕對年份鍵 remap，一次性） */')
e = find_line('  try{ if(typeof c2n210MigrateSave==="function") c2n210MigrateSave(o); }catch(_e){}', s) + 1
expect(e - 1, '  try{ if(typeof c2n210MigrateSave==="function") c2n210MigrateSave(o); }catch(_e){}')
assert lines[e] == '  /* v20a113 GATE113：清走跳步存檔嘅非法 done 標記（前置未滿足／早過窗口嗰陣播出嘅 N18／N19／N8／N12）；', 'GATE113 anchor moved: %r' % lines[e]
spans.append((s, e, 'normalizeSaveObj 呼叫點 ×4'))

# (D) JAN67 遷移機械：由 day-shift 註解到 jan67MigrateSave 函數尾（開局季節註解之前）
s = find_line('/* 1990-01-01 → 1990-03-07 相差 65 日：舊檔（3 月 epoch）dayIndex +65，曆法日期原封不動。 */')
e = find(lambda l: l.startswith('/* 開局季節文字定點修正：'), s)
assert 'function jan67MigrateSave(o){' in '\n'.join(lines[s:e]), 'jan67 fn missing from span'
assert 'function jan67ShiftDayStamps' in '\n'.join(lines[s:e]), 'jan67 walker missing from span'
assert 'function jan67OpeningTextFix' not in '\n'.join(lines[s:e]), 'opening fix must stay'
spans.append((s, e, 'jan67 遷移機械'))

# (B) years66MigrateSave 註解＋函數：由舊存檔註解到 JAN67 block 之前
s = find_line('/* 舊存檔遷移（epoch guard）：v65 或更早開嘅檔冇 years66Shifted 印——dayIndex 唔郁（衍生日期')
e = find(lambda l: l.startswith('/* ===== v20a67 JAN67'), s)
assert 'function years66MigrateSave(o){' in '\n'.join(lines[s:e]), 'years66 fn missing from span'
assert 'function years66Walk' not in '\n'.join(lines[s:e]), 'years66Walk must stay'
spans.append((s, e, 'years66MigrateSave'))

for (s, e, label) in sorted(spans, reverse=True):
    print('delete L%d-%d (%d 行): %s' % (s + 1, e, e - s, label))
    del lines[s:e]

open(P, 'w', encoding='utf-8').write('\n'.join(lines))
src = '\n'.join(lines)
n = src.count('MigrateSave')
print('總行數 %d → %d（淨 -%d）' % (orig_total, len(lines), orig_total - len(lines)))
print('index.html 殘留 MigrateSave：%d 處' % n)
assert n == 0, 'MigrateSave 仲有殘留'
print('DELETE228 OK')
