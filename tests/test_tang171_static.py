# v20a214 rebase 上 main d1239d4 resync：index.html 淨 +358 行，總行數 61994→62352、DEF 56466→56824（difflib 對位核實純漂移，見 qa214/resync214_rebase.py）。
# v20a207 resync (part 2).
# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），總行數 60522→60609、DEF 55018→55102。
# v20a203 resync：index.html 淨 +233 行（見 qa203/resync203.py difflib 對位核實純漂移），總行數 61167→61400、DEF 55639→55872。
# v20a206 C1 resync：index.html 淨 +22 行（WF4 保底，插入點舊 L41129–41496）；總行數 61400→61422、DEF 55872→55894（qa206/resync206.py difflib 對位核實純漂移）。
# v20a206 C2 resync：index.html 淨 +3 行（WF4 覆寫表頭註解＋3，插入點舊 L41271 之後）；總行數 61422→61425、DEF 55894→55897（qa206/resync206c2.py difflib 對位核實純漂移）。
# v20a208 resync：index.html 淨 +223 行（見 qa208/resync208.py difflib 對位核實純漂移；rebase 上 main b7ddb37 後 qa208/resync208_rebase.py 再對位核實），總行數 61491→61714、DEF 55963→56186。
# v20a212 resync：index.html 淨 +39 行（見 qa212/resync212.py difflib 對位核實純漂移），總行數 61714→61753、DEF 56186→56225。
# v20a215 resync：index.html 淨 +140 行（見 qa215/resync215.py difflib 對位核實純漂移），總行數 61795→61935、DEF 56267→56407（名公式補返漏咗嘅 v211 +42；真 DEF 喺 56267 唔係 56225）。
# -*- coding: utf-8 -*-
# v20a197 resync：index.html 淨 +94 行，總行數 60490→60584、DEF 54986→55080（difflib 對位核實純漂移，見 qa197/resync197.py；B4 補丁再 +9 行）。
# v20a196 resync：index.html 淨 +83 行，總行數 60490→60573、DEF 54986→55060（difflib 對位核實內容逐字相同，純漂移）。
# v20a196 落地合併上 main 2de5026：總行數 60817→60900、DEF 55310→55384（v197 ＋94 之上再 ＋83）。
# v20a202 resync：index.html 淨 +88 行（見 qa202/resync202.py），總行數 60900→60988、DEF 55384→55460。
# v20a191 resync：index.html 淨 +47 行，總行數 60155→60202、DEF 54651→54698。
# v20a191 rebase 上 main b3db32f resync：總行數 60443→60490、DEF 54940→54986。
# v20a191 rebase 上 main 593a845 resync：總行數 60409→60456、DEF 54905→54952。
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
# 行號：全部同行改動（CSS 規則 append 入 L4832 v169 行、add() 同行加 class、
#      sync 定義＋scroll wiring append 入 resize 守門行、resize handler／rAF／openLoc 尾
#      同行加呼叫），總行數 59171 不變，openLoc DEF 行 53690 不變——
#      （v20a170 resync：P2 fallback 註解 +2 行 → 總行數 59173，openLoc DEF 行 53692）
# v20a149 rebase 上 main e8c3a73（v170）resync：淨 ＋98 行（CSS ＋13／JS ＋85），總行數 59173→59271、DEF 53692→53790；其餘斷言唔郁。
# v20a149 fixup3（rebase 上 e8c3a73）：reveal 行融返一行（−1），總行數 59271→59270、DEF 53790→53789。
#      test_tang152／travel114／kwan151 釘行全部唔使 resync。
# v20a153 第三輪 rebase 上 main a500536（v149）resync：總行數 59270→59341、DEF 53789→53860（difflib 對位核實純漂移，見 qa153/resync_rebase153c.py）。
# v20a173 更新（見 NOTES_V20A173 §1–§2）：淡出實色 stop 78%→60%、鎖住態 .h 加
#      !important——下面兩條斷言跟住改，舊值斷言搬咗去 test_tang173_static.py
#      （驗新值存在＋舊值唔存在），唔係刪咗守門。
# v20a173 rebase 上 main 0ecaeb3（v153）：同行改動，總行數 59341、DEF 53860 不變。
# v20a172 rebase 上 main a500536（v149）resync：v149 淨 ＋97，總行數 59285、openLoc DEF 行 53804（qa172/resync172b.py difflib 對位核實）。
# v20a172 rebase 上 main e2add29（v174）resync：v172 4 hunks 淨 ＋15，總行數 59341→59356、DEF 53860→53875（qa172/resync172c.py difflib 對位核實純漂移）。
# v20a175 rebase 上 main f09fa1b（v177）resync：index.html 淨 ＋78，總行數 59356→59434、DEF 53875→53953。
# v20a178 第二次 rebase 上 main 91f264a（v175）resync：v178 ＋25 行（AWARDS64 註解＋1／ko sprite＋3／fellows 特別名額＋21）疊喺 v175 ＋78 之上，總行數 59434→59459、DEF 53953→53978（qa178/resync178b.py difflib 對位核實純漂移；三檔 rebase 衝突後以 v175 版為底重算）。
# v20a178 strip 上 91f264a resync：strip 淨 −4 行（AWARDS64 註解＋1／ko sprite＋3），總行數 59459→59455、DEF 53978→53974（qa178/resync178c.py difflib 對位核實純漂移）。
# v20a181 resync：index.html 淨 ＋8（awards CSS ＋13／頒獎禮區淨 −26／尾段 ＋8），總行數 59434→59442、DEF 53953→53961（difflib 對位核實純漂移）。
# v20a181 rebase 上 main 9640c6f（v183）resync：總行數 60127→60135、DEF 54623→54631（difflib 對位核實純漂移）。
# v20a181 第二次 rebase 上 main 77603b3（v184）resync：總行數 60135→60151、DEF 54631→54647（v184 淨 ＋16 全喺 DEF 之前；difflib 對位核實純漂移，見 qa181/resync181_rebase2.py）。
# v20a186 resync：index.html 淨 ＋4 行（結果卡同屆提名行移出逐類別卡，插入點 L45783–45826），總行數 60151→60155、DEF 54647→54651；L4862 唔郁（喺插入點之前）。
# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點 L45380–46310）；其後釘行各 +225，之前唔郁；總行數 60155→60380。
# v20a188 resync 補 +29：上一手 +225 計少咗其後再加嘅 NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口（淨 +29）；總淨變 +254，總行數 60409；difflib 對位核實全部錨點純漂移，見 qa188/resync188_verify.py。
# 反證：喺 pristine main（56141a3／v169）index 上行，新行為斷言會乾淨 FAIL，
#      唔會 crash。守門斷言喺 pristine 都 PASS（佢哋守「舊嘢冇郁過」）。
# 用法：python3 tests/test_tang171_static.py [path-to-index.html]
# v20a176 resync：淨 ＋538 行（NPCS ＋7／星收尾掣 ＋12／ROM176 block ＋501／茶聽 ＋12／addLoc −13／openLoc 掛點 ＋5／doGiveGift ＋4／人脈頁 ＋10），總行數 59341→59879、DEF 53860→54379（qa176/resync176.py 逐行核實內容逐字相同，純漂移）。
# v20a176 rebase 上 main 91f264a（v175）resync：v175 淨 ＋78（CSS ＋10／toast ＋15／prog175 ＋51＋render ＋2），總行數 59894→59972、DEF 54394→54472（qa176/resync176_rebase.py difflib 對位核實純漂移）。
# v20a176 第三輪 rebase 上 main c682cc2（v178）resync：v178 淨 ＋21（fellows 特別名額＋21；註解＋sprite 來回 ＋4−4 抵消），總行數 59972→59993、DEF 54472→54493（qa176/resync176_rebase3.py difflib 對位核實純漂移；三檔 rebase 衝突後取 v176 嗰邊，v178 註解行補返）。
# v20a183 resync：v183 淨 ＋117 行（C7 CSS ＋2／prefKind ＋1／TryIntercept ＋1／PlayEncounter ＋2／ROM183 block ＋107／確認 modal ＋3／goBit ＋1；difflib 對位核實純漂移，見 qa183/resync183.py）。
# v20a184 rebase 上 main 0f90dc7（v183）resync：v184 淨 ＋16 行（C2 helper＋9／請柬＋1／結果卡＋1／C1 DEEPS＋4／漸變＋1 淨）；＜45748 者唔郁、其後者 ＋16（difflib 對位核實純漂移，見 qa184/resync184_rebase.py）。
# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510（qa182/resync182.py difflib 對位核實純漂移）。
# v20a189 resync：index.html 淨 ＋34 行（accel-link CSS ＋15 @~1831／day-res 92dvh media ＋10 @~3235／hint 刪除 −10 @37990／soft map 掣 ＋3／accel link push ＋12／day-res class ＋4；difflib 對位核實純漂移，見 qa189/resync189.py）。
# v20a189 rebase 上 main 0c29f03（v188）resync：DEF 54685→54939（+254，v188；difflib 對位核實純漂移，見 qa189/resync189_rebase.py）。
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
ok('零行數漂移：總行數 62492（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140）', src.count('\n') == 62492)
ok('零行數漂移：openLoc DEF 行 56964（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140，travel114 釘行）',
   len(lines) >= 56964 and 'function openLoc(id, opts){' in lines[56963])
# v20a215 rebase 上 main 7e27e1a resync：v215 淨 +140 行，釘行按 difflib 映射重寫，qa215 resync 核實純漂移（總行數 62352→62492；DEF 56824→56964）。# --- §1. C1：捲動提示（淡出漸變） ---
ok('C1：淡出漸變 CSS 規則存在（loc-acts-more171::after＋linear-gradient）',
   '#loc-acts.loc-acts-more171::after' in src
   and 'linear-gradient(to bottom, rgba(248,241,222,0), #f8f1de 60%)' in src)  # v20a173：stop 78%→60%
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
   and '.act.act-locked171 .h{ opacity:.72 !important; }' in src)  # v20a173：.h 加 !important
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
