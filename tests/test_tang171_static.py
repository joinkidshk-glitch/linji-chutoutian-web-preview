# -*- coding: utf-8 -*-
# v20a171 靜態測試：v169 review C1＋C2。
# 修法選擇（見 NOTES_V20A171.md，唔好假設）：
#  C1：push 並存態成版掣過長，最尾掣要碌先見，首屏冇提示——揀 acts 區底加淡出
#      漸變（唔係接受現狀，用戶已拍板要修；唔揀摺起低優先掣，改可用性風險大；
#      唔揀加提示字，要改 DOM 結構）。實現：#loc-acts.loc-acts-more171::after
#      sticky 底緣 30px 漸變（唔佔位、唔攔點擊、唔郁掣高／佈局，B2 卡片幾何不變）＋
#      window.syncLocActsFade171()——內容超出可視高而且未捲到底先掛 class；掛喺
#      openLoc 尾、rAF、scroll listener、resize 四處。class 捲到底自動除返，唔留殘影。
#      ::after 唔佔位：高 30px 由 margin-top:-30px 抵消，#loc-acts flex row-gap 7px
#      由 margin-bottom:-7px 抵消（實駕驗過：掛 class 前後 scrollHeight 同為 814）。
#  C2：鎖住態（庫存空／今日已送）同可送態一眼分唔到——add() 入面費用欄係呢兩個
#      狀態字嗰陣加 act-locked171 class（只由 giftGateBadge 出，唔會誤傷其他掣）；
#      CSS 掣身變灰（底 #e6dfcc＋邊框 #a89a7c，標題／hint 微淡 .72），費用欄轉深啡灰
#      #6b5636（同鎖住底對比度 5.25:1，高過 B1 實測 4.21:1，唔會灰到讀唔到）。
#      只做視覺區分：disabled／aria／點擊／toast 全部唔郁，撳鎖住態照有 toast 講原因。
# 唔郁：v167 review C1（接受現狀）、咖啡豆句、push1 到唔到、玫瑰扣庫存、v170／v149。
# 行號：六處全部同行改動（CSS 規則 append 入 L4832 v169 行、add() 同行加 class、
#      sync 定義＋scroll wiring append 入 resize 守門行、resize handler／rAF／openLoc 尾
#      同行加呼叫），總行數 59171 不變，openLoc DEF 行 53690 不變——
#      （v20a170 resync：P2 fallback 註解 +2 行 → 總行數 59173，openLoc DEF 行 53692）
# v20a149 rebase 上 main e8c3a73（v170）resync：淨 ＋98 行（CSS ＋13／JS ＋85），總行數 59173→59271、DEF 53692→53790；其餘斷言唔郁。
# v20a149 fixup3（rebase 上 e8c3a73）：reveal 行融返一行（−1），總行數 59271→59270、DEF 53790→53789。
#      test_tang152／travel114／kwan151 釘行全部唔使 resync。
# v20a153 第三輪 rebase 上 main a500536（v149）resync：總行數 59270→59341、DEF 53789→53860（difflib 對位核實純漂移，見 qa153/resync_rebase153c.py）。
# 反證：喺 pristine main（56141a3／v169）index 上行，新行為斷言會乾淨 FAIL，
#      唔會 crash。守門斷言喺 pristine 都 PASS（佢哋守「舊嘢冇郁過」）。
# 用法：python3 tests/test_tang171_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
ROOT = Path(__file__).resolve().parent.parent
src = p.read_text(encoding='utf-8')
lines = src.split('\n')
fails = []
total = [0]
def ok(name, cond):
    total[0] += 1
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _lum(hexs):
    r, g, b = (int(hexs[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
def contrast(fg, bg):
    l1, l2 = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

# --- 紀律：SAVE key／softRev／?v= 不變；零行數漂移 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('零行數漂移：總行數 59270（v170 59173＋v149 ＋97）', src.count('\n') == 59341)
ok('零行數漂移：openLoc DEF 行 53860 不變（travel114 釘行）',
   len(lines) >= 53860 and 'function openLoc(id, opts){' in lines[53859])

# --- §1. C1：捲動提示（淡出漸變） ---
ok('C1：淡出漸變 CSS 規則存在（loc-acts-more171::after＋linear-gradient）',
   '#loc-acts.loc-acts-more171::after' in src
   and 'linear-gradient(to bottom, rgba(248,241,222,0), #f8f1de 78%)' in src)
ok('C1：漸變唔佔位（sticky＋margin-top:-30px 抵消 30px 高＋margin-bottom:-7px 抵消 7px flex gap）',
   'position:sticky; bottom:0;' in src and 'height:30px; margin-top:-30px; margin-bottom:-7px;' in src)
ok('C1：漸變唔攔點擊（pointer-events:none）',
   '#loc-acts.loc-acts-more171::after' in src and 'pointer-events:none; z-index:5;' in src)
ok('C1：sync 函數存在（掛 window，openLoc／scroll／resize 都讀到）',
   'window.syncLocActsFade171=function(){' in src)
ok('C1：sync 條件啱——超出可視高而且未捲到底先掛 class',
   'a.scrollHeight>a.clientHeight+4 && a.scrollTop+a.clientHeight<a.scrollHeight-4' in src
   and 'a.classList.toggle("loc-acts-more171"' in src)
ok('C1：scroll listener 已接（捲動嗰陣即時更新提示）',
   'a171.addEventListener("scroll"' in src)
ok('C1：openLoc 尾＋rAF 有呼叫 sync（渲染完即計一次）',
   src.count('window.syncLocActsFade171();') >= 4)
ok('C1：B2 守門——#loc-acts 仲係 flex 直欄＋掣 flex-shrink:0（卡片唔重疊）',
   '#loc-sheet.sheet.locpanel118 #loc-acts{ display:flex !important; flex-direction:column !important; }' in src
   and '#loc-sheet.sheet.locpanel118 #loc-acts .act{ flex-shrink:0; }' in src)
ok('C1：B2 守門——badge 仲係入文字欄（v169 修法一字唔郁）',
   'badge 入文字欄' in src)

# --- §2. C2：鎖住態視覺區分 ---
ok('C2：add() 入面鎖住態加 act-locked171 class',
   'if(cost105==="庫存空"||cost105==="今日已送") b.className+=" act-locked171";' in src)
ok('C2：鎖住態 CSS 存在（掣身灰米底＋灰邊框）',
   '#app #loc-sheet.sheet .act.act-locked171{ background:#e6dfcc !important; border-color:#a89a7c !important; }' in src)
ok('C2：鎖住態費用欄轉深啡灰 #6b5636（唔再係紅 #C43C2A）',
   '#app #loc-sheet.sheet .act.act-locked171 .cost{ color:#6b5636 !important; }' in src)
ok('C2：鎖住態標題／hint 微淡（opacity .72）',
   '.act.act-locked171 .n{ opacity:.72; }' in src
   and '.act.act-locked171 .h{ opacity:.72; }' in src)
_c = contrast('6b5636', 'e6dfcc')
print('INFO locked cost contrast #6b5636 on #e6dfcc = %.2f:1' % _c)
ok('C2：鎖住態費用欄對比度 >= 4.5:1（高過 B1 實測 4.21:1，讀得到）', _c >= 4.5)
ok('C2：只做視覺區分——鎖住態嗰行冇加 disabled（撳落去照有 toast）',
   'act-locked171' in src and all('b.disabled' not in ln and '.disabled=' not in ln
       for ln in lines if 'act-locked171' in ln and 'className' in ln))
ok('C2：鎖住態點擊行為唔郁——送禮掣撳落去照 toast 原因',
   'if(!live.ok){ toast(live.reason||"暫不可送"); return; }' in src)
ok('C2：B1 守門——known105 仲有「庫存空」「今日已送」（費用欄文字唔郁）',
   '"庫存空","今日已送"' in src)
ok('C2：B1 守門——giftGateBadge 仍然回傳呢兩個狀態字',
   'if(/庫存/.test(r)) return "庫存空";' in src
   and 'if(/今天|今日|人情急|先到這裡/.test(r)) return "今日已送";' in src)
ok('C2：可送態唔郁——.act .cost 仲係紅 #C43C2A 800 weight',
   '.act .cost{' in src and 'color: var(--stamp-red,#C43C2A) !important;' in src)

print('TOTAL %d PASS %d FAIL %d' % (total[0], total[0] - len(fails), len(fails)))
if fails:
    print('FAILED: ' + '; '.join(fails))
    sys.exit(1)
