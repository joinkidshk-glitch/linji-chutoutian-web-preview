# -*- coding: utf-8 -*-
# v20a67 JAN67 靜態測試：1 月 epoch／JAN67 block／遷移接線次序／評核邊界週／開局季節文字清零。
# 反證：喺 v20a66 index 上行會 FAIL。
# 用法：python3 tests/test_jan67_static.py [path-to-index.html]
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('START epoch = 1990-01-01', 'const START = { y:1990, m:1, d:1 }' in src)
ok('JAN67 block 存在', '/* ===== v20a67 JAN67' in src and 'function jan67MigrateSave' in src
   and 'function jan67ShiftDayStamps' in src and 'function jan67OpeningTextFix' in src)
ok('JAN67_DAY_SHIFT = 65', 'const JAN67_DAY_SHIFT = 65;' in src)
ok('JAN67_DAY_KEYS 含 lastGiveDay（map 形日戳）', 'paidFlavorDay:1, lastGiveDay:1' in src)
ok('fresh() 打 startEpoch67 戳', 'startEpoch67:1,' in src)

m = re.search(r'function normalizeSaveObj\(o\)\{(.*?)\n\}', src, re.S)
body = m.group(1) if m else ''
i66 = body.find('years66MigrateSave(o)'); i67 = body.find('jan67MigrateSave(o)')
imiss = body.find('calib60MissedScan(o)'); ileg = body.find('conseq61LegacyMark(o)')
ok('遷移接線次序：years66 → jan67 → missedScan/legacyMark',
   0 <= i66 < i67 < imiss and i67 < ileg)

ok('評核邊界週 52／104', re.search(r'1990:\s*\{\s*floor:\s*45,\s*warnLine:\s*65,\s*boundaryWeek:\s*52\s*\}', src) is not None
   and re.search(r'1991:\s*\{\s*floor:\s*100,\s*warnLine:\s*130,\s*boundaryWeek:\s*104\s*\}', src) is not None)
ok('softC10 改年內週（(week-1)%52）', '((week - 1) % 52) + 1' in src and 'wkInYear < 49 || wkInYear > 52' in src)
m2 = re.search(r'function softC10WindowActive\(\)\{(.*?)\n\}', src, re.S)
ok('softC10 冇舊絕對週 40–43 殘留', bool(m2) and 'w>=40' not in m2.group(1) and 'weekNumNow()>=40' not in m2.group(1))

ok('開始畫面印章 一九九零', '一九九零' in src)
ok('全檔冇 一九八八 殘留', '一九八八' not in src)
ok('新遊戲注腳 1990 年冬', '1990 年冬 · 由零開始' in src and '1990 年春 · 由零開始' not in src)
ok('B01 modal 日期動態衍生（冇硬編碼舊日期）', '1990年3月7日' not in src and 'return "1990年1月1日"' in src)
ok('開局文字對照表齊（開場白＋教學）',
   '"1990 年初，阿偉在黃大仙屋邨起步"' in src and '"1990 年初，你在黃大仙屋邨當臨記起步"' in src)
ok('冬季開局卡來歷齊（阿標／美兒）', 'card_biao_winter:' in src and 'card_may_winter:' in src)
ok('副題不變 1990 · 片場星途', '<p class="start-sub">1990 · 片場星途</p>' in src)
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and "softRev: 's107'" not in src and 's107' in src and 'v20a10' in src)
print('\nFAILURES: ' + str(len(fails)) + ((' -> ' + ' | '.join(fails)) if fails else ''))
sys.exit(1 if fails else 0)
