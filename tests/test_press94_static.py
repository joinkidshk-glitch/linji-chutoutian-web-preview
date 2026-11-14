# -*- coding: utf-8 -*-
"""v20a94 PRESS94・靜態測試：接線完整 + 硬守衛冇俾人郁。
- 分類器/里程碑/徽章函數在位；enqueueNewspaperFromWrap 有 base 入閘分支（回 null，唔出報紙）
- 填位（press94FillLines）已退役（v20a214 NP214，用戶 2026-11-14 18:14 拍板：base 殺青
  唔出報紙，連製作消息填位都唔出，報紙路徑唔留死 code）
- gigCardHtml／gigBoardTeaserHtml 用 press94TierBadge（同見報門檻共用分類）
- seal_extra.png 資產存在；SAVE key／softRev／?v= 不變；分類器唔改 tier 數據（冇 .tier 賦值）
反證：v93 index 冇 press94 → FAIL。
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
fails = []
def ok(name, cond, extra=''):
    print(('PASS ' if cond else 'FAIL ') + name + ((' ' + extra) if (extra and not cond) else ''))
    if not cond: fails.append(name)

ok('S01_classifier', 'function press94RoleClass(' in html and 'PRESS94_BASE_SCALES' in html)
ok('S02_fill_retired', 'function press94FillLines(' not in html and 'press94: "fill"' not in html)
ok('S03_badge_fn', 'function press94TierBadge(' in html)
seg_wrap = html[html.index('function enqueueNewspaperFromWrap('):html.index('function enqueueNewspaperFromWrap(') + 6000]
ok('S04_gate_wired', 'press94IsBaseRole(gig94, labelHint94)' in seg_wrap
   and 'return null' in seg_wrap and 'press94: "fill"' not in seg_wrap)
ok('S05_milestone', 'press94ClaimFirstNamed' in html and 'press94FirstNamedDay' in html
   and '第一次出現在本報的殺青消息' in html)
ok('S06_card_badge', html.count('press94TierBadge(g)') >= 2)
ok('S07_seal_asset', os.path.exists(os.path.join(ROOT, 'assets/ui-physical/notice/seal_extra.png')))
ok('S08_save_key', 'starVolunteer_map_v19w' in html)
ok('S09_softrev', '"s107"' in html or "'s107'" in html or 's107' in html)
ok('S10_version', 'v20a10' in html)
# 分類器區塊唔准寫 tier（純讀分類）：抽 press94 段落檢查冇 .tier = 賦值
m = re.search(r'v20a94 PRESS94：見報門檻.*?function enqueueNewspaperFromWrap', html, re.S)
ok('S11_classifier_no_tier_write', bool(m) and ('.tier =' not in m.group(0)) and ('.tier=' not in m.group(0)))
# 頁內自檢新契約在位（v20a214：base 斷言改版，舊 fill 斷言已廢）
ok('S12_selftest_new_contract', 'ferry_gate214' in html and 'hi15_gate214' in html and 'p94_fill_gone214' in html)
print('RESULT ' + ('FAIL ' + str(len(fails)) if fails else 'PASS'))
sys.exit(1 if fails else 0)
