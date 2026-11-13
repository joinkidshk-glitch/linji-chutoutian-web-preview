# -*- coding: utf-8 -*-
# v20a161 靜態測試：首頁簡介句收窄＋置左，避開阿偉塊面（唔郁企位）。
# 反證：喺 pristine main（e08a070／v148）index 上行會 FAIL（冇 v20a161 區塊）。
# 用法：python3 tests/test_start161_static.py [path-to-index.html]
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('簡介句文字本身唔改', '港產新人<strong>陳偉翔（阿偉）</strong>，自己跑通告——臨記埋位，一步一步上。' in src)
ok('企位唔郁：v53 bottom:170px／height:min(52%,430px) 原封不動',
   '#app #v-start .start52 .start-standee{\n  bottom:170px;\n  height:min(52%,430px);\n}' in src)
ok('v52 企位基線唔郁（bottom:148px／height:min(44%,372px) 仲喺度）',
   'bottom:148px' in src and 'height:min(44%,372px)' in src)
ok('v53 簡介句基線唔郁（max-width:332px＋柔霧底仲喺度）',
   'max-width:332px' in src and 'radial-gradient(115% 135% at 50% 45%' in src)

# --- v161：收窄＋置左 ---
m = re.search(r'/\* === v20a161.*?=== v20a161 完 === \*/', src, re.S)
ok('v20a161 區塊在場', bool(m))
blk = m.group(0) if m else ''
ok('v161：簡介句 max-width:140px', 'max-width:140px' in blk)
ok('v161：簡介句 text-align:left', 'text-align:left' in blk)
ok('v161：簡介句 margin-left:0（置左，靠 .start-head 20px padding 落位）',
   'margin:2px 0 0' in blk)
ok('v161：140px 規則喺區塊內只出現一次（唔係全局規則）', blk.count('max-width:140px') == 1)
ok('v161：區塊內只得一條 .start-intro 規則（唔掂企位／標題／掣／其他畫面）',
   blk.count('#app #v-start .start52 .start-intro{') == 1
   and '.start-standee' not in blk and '.start-title' not in blk and '#btn-new' not in blk)
ok('v161：註解寫明量度數字同企位唔郁原因', '175.5' in blk and 'bottom:170px' in blk)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
