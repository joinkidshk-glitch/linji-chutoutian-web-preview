# v20a207 resync：index.html 淨 +34 行（見 qa207/resync207.py，73 錨點對位零 mismatch，純漂移）。
# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），總行數 60522→60609。
# v20a203 resync：index.html 淨 +233 行（見 qa203/resync203.py difflib 對位核實純漂移），總行數 61167→61400。
# v20a206 C1 resync：index.html 淨 +22 行（WF4 保底：註解＋3／wf4SeenAny＋10／保底檢查＋9，插入點舊 L41129–41496）；總行數 61400→61422（qa206/resync206.py difflib 對位核實純漂移）。
# v20a206 C2 resync：index.html 淨 +3 行（WF4 覆寫表頭註解＋3，插入點舊 L41271 之後）；總行數 61422→61425（qa206/resync206c2.py difflib 對位核實純漂移）。
# v20a208 resync：index.html 淨 +223 行（見 qa208/resync208.py difflib 對位核實純漂移；rebase 上 main b7ddb37 後 qa208/resync208_rebase.py 再對位核實），總行數 61491→61714。
# v20a185 GIFT185 靜態測試：修 v183 review B1（700 尾行俾取消掣欄遮住）＋C1（兩欄卡名「×N」孤兒跌行）。
# v20a197 resync：index.html 淨 +94 行，總行數 60490→60584（difflib 對位核實純漂移，見 qa197/resync197.py；其餘斷言唔郁；B4 補丁再 +9 行）。
# v20a196 resync：index.html 淨 +83 行，總行數 60490→60573（showResult −1／晨鏈＋74／WF4＋63／尾段＋83 淨計；其餘斷言唔郁）。
# v20a196 落地合併上 main 2de5026：總行數 60817→60900（v197 ＋94 之上再 ＋83）。
# v20a202 resync：index.html 淨 +88 行（見 qa202/resync202.py），總行數 60900→60988。
# v20a191 resync：index.html 淨 +47 行，總行數 60155→60202（其餘斷言唔郁）。
# v20a191 rebase 上 main b3db32f resync：總行數 60443→60490。
# v20a191 rebase 上 main 593a845 resync：總行數 60409→60456。
# 修法路線 a：卡名一行 ellipsis＋數量 span 鎖 nowrap → 卡片 85→67px，5 行一眼全見，尾行清過取消掣欄；
# 另加 .act min-width:0，防 nowrap 名撐闊 grid 軌（右欄伸出 modal 外、elementFromPoint 命中 BODY）。
# 零淨行數改動（2 行改、0 行加減，總行數 60143 不變——rebase 上 v184 main 77603b3 後基底 60127→60143，v185 本身淨 0），kwan151／tang152／rom176 行號釘逐檔核實見下。
# v20a181 第三次 rebase 上 main cd4985f（v185）resync：v185 本身淨 0 行，v181 淨 ＋8，合併後總行數 60143→60151（code 數更新，標籤留返 main 數字）。
# v20a186 resync：index.html 淨 ＋4 行（結果卡同屆提名行移出逐類別卡，插入點 L45783–45826），總行數 60151→60155。
# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點 L45380–46310）；其後釘行各 +225，之前唔郁；總行數 60155→60380。
# v20a188 resync 補 +29：上一手 +225 計少咗其後再加嘅 NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口（淨 +29）；總淨變 +254，總行數 60409；difflib 對位核實全部錨點純漂移，見 qa188/resync188_verify.py。
# v20a189 resync：index.html 淨 ＋34 行（accel-link CSS ＋15 @~1831／day-res 92dvh media ＋10 @~3235／hint 刪除 −10 @37990／soft map 掣 ＋3／accel link push ＋12／day-res class ＋4；difflib 對位核實純漂移，見 qa189/resync189.py）。
# v20a189 rebase 上 main 0c29f03（v188）：總行數 60409＋34＝60443（v188 淨 +254 疊喺分支基底之上，v189 淨 +34 疊加；斷言本身唔使改行號）。
# 反證：pristine main (01ddcaa) 冇 v185 標記／spans／規則 → 多項 FAIL（唔 crash）。
# 用法：python3 tests/test_gift185_static.py [path-to-index.html]
import io, os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = io.open(path, encoding='utf-8').read()
lines = html.split('\n')
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
        j = min(len(html), i + 40000)
    return html[i:j]

# ---- 紅線：SAVE key／softRev／?v= 不變；唔直改 content pack JSON ----
ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('?v= 冇變', 'v=20a10' in html)
ok('總行數 61714（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223）', html.count('\n') == 61714)
# ---- B1：路線 a 標記＋grid 軌防撐闊 ----
ok('B1 v185 標記在位（路線 a：唔靠碌，一眼全見）',
   'v20a185 B1+C1' in html and '路線 a' in html)
ok('B1 .act min-width:0（防 nowrap 名撐闊 grid 軌）',
   '#gift-pick-list .act{ min-width:0 !important; }' in html)

# ---- C1：名 span ellipsis＋數量 span nowrap ----
ok('C1 .n 行 flex（icon＋名＋數量一行）',
   '#gift-pick-list .n{ display:flex !important; align-items:baseline !important; gap:4px !important; }' in html)
ok('C1 名 span ellipsis＋nowrap＋min-width:0',
   '#gift-pick-list .n .gift-pick-name{ flex:1 1 auto !important; min-width:0 !important; overflow:hidden !important; text-overflow:ellipsis !important; white-space:nowrap !important; }' in html)
ok('C1 數量 span nowrap＋唔縮',
   '#gift-pick-list .n .gift-pick-count{ flex:0 0 auto !important; white-space:nowrap !important; }' in html)
ok('C1 icon 唔縮（.ic112 flex:0 0 auto）',
   '#gift-pick-list .n .ic112{ flex:0 0 auto !important; }' in html)

# ---- openGiftPick row 模板用 spans；舊裸「名 ×N」清走 ----
pick = seg('function openGiftPick(npcKey, L){', 'function doGiveGift(npcKey, itemId, L){')
ok('C1 row 模板：名入 .gift-pick-name span',
   '<span class="gift-pick-name">${item.name}</span>' in pick)
ok('C1 row 模板：數量入 .gift-pick-count span',
   '<span class="gift-pick-count">×${count}</span>' in pick)
ok('C1 row 模板：舊裸「${item.name} ×${count}」已清走',
   '${item.name} ×${count}' not in pick)
ok('C1 row 模板：「選」掣仲在', '<div class="cost">選</div>' in pick)
ok('C1 row 模板：偏好標記行唔郁', '偏好標記：${tag}' in pick)

# ---- v183 C7 兩欄設計原封不動（淨係修遮擋，唔推翻兩欄） ----
ok('C7 700 media query 兩欄原封不動',
   '@media (max-height:720px){ #gift-pick-list{ display:grid; grid-template-columns:1fr 1fr; gap:4px 8px; }' in html
   and '#gift-pick-list .act{ margin-bottom:0 !important; padding:6px 8px !important; }' in html)
ok('C7 取消掣 pinned 規則唔郁', '#modal-btns{' in html and 'position: sticky' in html)

# ---- 作用域：淨係 #gift-pick-list，唔郁禮品店 list／其他 .n ----
ok('C1 規則全部鎖喺 #gift-pick-list 作用域',
   html.count('gift-pick-name') == 2 and html.count('gift-pick-count') == 2)
ok('禮品店 list 唔用新 spans（openGiftShop 模板唔郁）',
   '<span class="gift-pick-name">' not in seg('function openGiftShop(shopId, L){', 'function openGiftPick(npcKey, L){'))

print('---')
print('FAILURES: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
