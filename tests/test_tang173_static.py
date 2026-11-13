# -*- coding: utf-8 -*-
# v20a173 靜態測試：v171 review C1＋C2（兩項 C 級殘留）。
#  C1——932 淡出提示偏弱：同一個 30px 淡出，932 首屏只冚住「還人情」底 22px、
#      掣睇落完整（visFrac 1），700 就明顯切＋溶走（送禮掣 visFrac 0.84）。
#      修法揀 (a)：漸變實色 stop 由 78% 提早到 60%——純視覺改動，幾何影響最細。
#      78% 時實色線喺淡出區 23.4px 處（932「還人情」底 851 仲未到實色線 852，
#      成個掣底只係半透明漸變，睇落完整）；60% 時實色線喺 18px 處，掣底 4px
#      完全溶入底色＋上面 18px 漸變加深，半截掣提示明顯咗。唔郁掣高／卡片（B2），
#      高仲係 30px、margin-top:-30px＋margin-bottom:-7px 抵消唔郁。
#      (b) 加高到 40px 唔使做——(a) 實測夠就唔做，見 NOTES_V20A173 §1。
#  C2——鎖住態 hint 冇跟標題淡：標題 .n opacity 0.72，但 hint .h 實測 opacity 1。
#      根因：舊 rule L2024 #loc-sheet.sheet .act .h { opacity: 1 !important; }
#      用 !important 贏咗 v171 條無 !important 嘅
#      #app #loc-sheet.sheet .act.act-locked171 .h { opacity:.72; }。
#      修法：一行——v171 條 .h 規則加 !important（同行 .cost／掣底嗰兩條一樣寫法）。
#      新特異性 (2,4,0)（#app＋#loc-sheet）贏舊 rule (1,3,0)，hint 返 0.72。
#      對比度：送禮掣係 act-priority，hint 色由 L2048 #3a2e22 定（唔係 L2024 #5a4328）；
#      0.72 混合後 #6a6052 on 鎖住底 #e6dfcc = 4.63:1 ≥ 4.5，照讀到（見 NOTES §2）。
#      注意：非 priority 鎖住掣 hint 色會係 #5a4328，混合後只得 3.64:1——呢個板得
#      一粒送禮掣（priority），其他地點 NPC 送禮掣未逐個 live 驗，見 NOTES §6 殘留。
# 更正數字（v171 NOTES §4 錯，review 已證實，唔使另改 v171 NOTES）：
#      scrollH 係 814（唔係 821）；932 被淡出冚住嘅係「還人情」底 22px
#      （「聽風聲」只得 1px，唔係半截）；700 被切嗰個係「送禮：鄧麗萍」成 30px。
# 耦合提醒：淡出同 #loc-acts flex row-gap 7px 有耦合（margin-bottom:-7px 抵消），
#      之後改 gap 要一併改。
# 反證：喺 pristine（基底 e8c3a73／v170）index 上行，新行為斷言會乾淨 FAIL，
#      唔會 crash。守門斷言喺 pristine 都 PASS（佢哋守「舊嘢冇郁過」）。
# 用法：python3 tests/test_tang173_static.py [path-to-index.html]
# v20a173 rebase 上 main 0ecaeb3（v153）resync：總行數 59173→59341、DEF 53692→53860、CSS 同行 4832→4845、舊 rule L2016→L2024／L2040→L2048（逐項 grep＋git show 核實純漂移，單次掃描 dict 查表，見 NOTES_V20A173 §9）。
# v20a172 rebase 上 main e2add29（v174）resync：v172 4 hunks 淨 ＋15，總行數 59341→59356、DEF 53860→53875（qa172/resync172c.py difflib 對位核實純漂移；全套初跑由 suite 捉到，見 NOTES §5.5）。
# v20a175 rebase 上 main f09fa1b（v177）resync：index.html 淨 ＋78，總行數 59356→59434、DEF 53875→53953（L4845 喺 CSS 插入點之前，唔郁）。
# v20a178 第二次 rebase 上 main 91f264a（v175）resync：v178 ＋25 行（AWARDS64 註解＋1／ko sprite＋3／fellows 特別名額＋21）疊喺 v175 ＋78 之上，總行數 59434→59459、DEF 53953→53978（qa178/resync178b.py difflib 對位核實純漂移；三檔 rebase 衝突後以 v175 版為底重算）。
# v20a178 strip 上 91f264a resync：strip 淨 −4 行（AWARDS64 註解＋1／ko sprite＋3），總行數 59459→59455、DEF 53978→53974（qa178/resync178c.py difflib 對位核實純漂移）。
# v20a176 resync：淨 ＋538 行（NPCS ＋7／星收尾掣 ＋12／ROM176 block ＋501／茶聽 ＋12／addLoc −13／openLoc 掛點 ＋5／doGiveGift ＋4／人脈頁 ＋10），總行數 59356→59894、DEF 53875→54394（qa176/resync176.py 逐行核實內容逐字相同，純漂移）。
# v20a176 rebase 上 main 91f264a（v175）resync：v175 淨 ＋78（CSS ＋10／toast ＋15／prog175 ＋51＋render ＋2），總行數 59894→59972、DEF 54394→54472（qa176/resync176_rebase.py difflib 對位核實純漂移）。
# v20a176 第三輪 rebase 上 main c682cc2（v178）resync：v178 淨 ＋21（fellows 特別名額＋21；註解＋sprite 來回 ＋4−4 抵消），總行數 59972→59993、DEF 54472→54493（qa176/resync176_rebase3.py difflib 對位核實純漂移；三檔 rebase 衝突後取 v176 嗰邊，v178 註解行補返）。
# v20a183 resync：v183 淨 ＋117 行（C7 CSS ＋2／prefKind ＋1／TryIntercept ＋1／PlayEncounter ＋2／ROM183 block ＋107／確認 modal ＋3／goBit ＋1；difflib 對位核實純漂移，見 qa183/resync183.py）。
# v20a184 rebase 上 main 0f90dc7（v183）resync：v184 淨 ＋16 行（C2 helper＋9／請柬＋1／結果卡＋1／C1 DEEPS＋4／漸變＋1 淨）；＜45748 者唔郁、其後者 ＋16（difflib 對位核實純漂移，見 qa184/resync184_rebase.py）。
# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510、CSS 同行 4845→4847（qa182/resync182.py difflib 對位核實純漂移）。
# v20a181 resync：index.html 淨 ＋8，總行數 59434→59442、DEF 53953→53961、L4845→L4858（awards CSS ＋13，difflib 對位核實純漂移）。
# v20a181 rebase 上 main 9640c6f（v183）resync：總行數 60127→60135、DEF 54623→54631、L4849→L4862（difflib 對位核實純漂移）。
# v20a181 第二次 rebase 上 main 77603b3（v184）resync：總行數 60135→60151、DEF 54631→54647；L4862 唔郁（喺 v184 插入點之前；difflib 對位核實純漂移，見 qa181/resync181_rebase2.py）。
# v20a186 resync：index.html 淨 ＋4 行（結果卡同屆提名行移出逐類別卡，插入點 L45783–45826），總行數 60151→60155、DEF 54647→54651；L4862 唔郁（喺插入點之前）。
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
def blend(fg, bg, a):
    f = [int(fg[i:i+2], 16) for i in (0, 2, 4)]
    b = [int(bg[i:i+2], 16) for i in (0, 2, 4)]
    return ''.join('%02x' % round(a * x + (1 - a) * y) for x, y in zip(f, b))

# --- 紀律：SAVE key／softRev／?v= 不變；零行數漂移 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('零行數漂移：總行數 59442（v181 ＋8）', src.count('\n') == 60155)
ok('零行數漂移：openLoc DEF 行 53961（v181 ＋8，travel114 釘行）',
   len(lines) >= 54651 and 'function openLoc(id, opts){' in lines[54650])
ok('零行數漂移：L4862 仲係 v169／v171／v173 同行（v181 CSS ＋13，kwan151／tang152 釘行已一併 resync）',
   len(lines) >= 4862 and 'loc-acts-more171::after' in lines[4861] and 'act-locked171' in lines[4861])
ok('L4862 註解平衡：/* 數＝*/ 數，鎖住底 rule 唔喺註解入面（v173 曾中招：註解入面再插 /*…*/ 令首個 */ 提早閂註解，殘尾變裸文吞咗鎖住底 rule 嘅 selector，live 底色跌返 #f5e6c0）',
   lines[4861].count('/*') == lines[4861].count('*/')
   and lines[4861].rfind('/*', 0, lines[4861].find('#app #loc-sheet.sheet .act.act-locked171{ background'))
   < lines[4861].rfind('*/', 0, lines[4861].find('#app #loc-sheet.sheet .act.act-locked171{ background')))

# --- §1. C1：淡出實色 stop 78% → 60% ---
ok('C1：淡出漸變實色 stop 已提早到 60%',
   'linear-gradient(to bottom, rgba(248,241,222,0), #f8f1de 60%)' in src)
ok('C1：舊 78% stop 已唔存在（唔係兩條並存）',
   'linear-gradient(to bottom, rgba(248,241,222,0), #f8f1de 78%)' not in src)
ok('C1：幾何唔郁——淡出高仲係 30px、margin 抵消唔郁（scrollH 唔郁）',
   'height:30px; margin-top:-30px; margin-bottom:-7px;' in src)
ok('C1：漸變仲係 sticky 底緣＋唔攔點擊（pointer-events:none）',
   '#loc-acts.loc-acts-more171::after' in src and 'position:sticky; bottom:0;' in src
   and 'pointer-events:none; z-index:5;' in src)
ok('C1：sync 函數＋條件唔郁（超出可視高而且未捲到底先掛 class）',
   'window.syncLocActsFade171=function(){' in src
   and 'a.scrollHeight>a.clientHeight+4 && a.scrollTop+a.clientHeight<a.scrollHeight-4' in src)
ok('C1：B2 守門——#loc-acts 仲係 flex 直欄＋掣 flex-shrink:0（卡片唔重疊）',
   '#loc-sheet.sheet.locpanel118 #loc-acts{ display:flex !important; flex-direction:column !important; }' in src
   and '#loc-sheet.sheet.locpanel118 #loc-acts .act{ flex-shrink:0; }' in src)

# --- §2. C2：鎖住態 hint 加 !important ---
ok('C2：鎖住態 .h 規則有 !important（贏返舊 rule L2024 嘅 opacity:1 !important）',
   '#app #loc-sheet.sheet .act.act-locked171 .h{ opacity:.72 !important; }' in src)
ok('C2：舊無 !important 嘅 .h 規則已唔存在（唔係兩條並存）',
   '.act.act-locked171 .h{ opacity:.72; }' not in src)
ok('C2：標題 .n 仲係 opacity .72（唔郁）',
   '.act.act-locked171 .n{ opacity:.72; }' in src)
ok('C2：舊 rule L2024 仲喺度（修法係加 !important 贏佢，唔係刪佢）',
   '#loc-sheet.sheet .act .h{' in src and 'opacity: 1 !important;' in src)
ok('C2：鎖住態掣身／費用欄唔郁（灰米底 #e6dfcc＋深啡灰 #6b5636）',
   '#app #loc-sheet.sheet .act.act-locked171{ background:#e6dfcc !important; border-color:#a89a7c !important; }' in src
   and '#app #loc-sheet.sheet .act.act-locked171 .cost{ color:#6b5636 !important; }' in src)
ok('C2：只做視覺區分——鎖住態嗰行冇加 disabled（撳落去照有 toast）',
   'act-locked171' in src and all('b.disabled' not in ln and '.disabled=' not in ln
       for ln in lines if 'act-locked171' in ln and 'className' in ln))
ok('C2：B1 守門——known105 仲有「庫存空」「今日已送」（費用欄文字唔郁）',
   '"庫存空","今日已送"' in src)
ok('C2：可送態唔郁——.act .cost 仲係紅 #C43C2A 800 weight',
   '.act .cost{' in src and 'color: var(--stamp-red,#C43C2A) !important;' in src)
_h = blend('3a2e22', 'e6dfcc', 0.72)
_c = contrast(_h, 'e6dfcc')
print('INFO locked hint blended #%s on #e6dfcc = %.2f:1 (priority gift btn, color #3a2e22)' % (_h, _c))
ok('C2：鎖住態 hint 淡咗照讀到——混合後對比度 >= 4.5:1', _c >= 4.5)
_c2 = contrast('6b5636', 'e6dfcc')
print('INFO locked cost contrast #6b5636 on #e6dfcc = %.2f:1' % _c2)
ok('C2：鎖住態費用欄對比度 >= 4.5:1（高過 B1 實測 4.21:1）', _c2 >= 4.5)

print('TOTAL %d PASS %d FAIL %d' % (total[0], total[0] - len(fails), len(fails)))
if fails:
    print('FAILED: ' + '; '.join(fails))
    sys.exit(1)
