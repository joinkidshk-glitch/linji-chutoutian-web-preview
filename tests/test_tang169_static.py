# -*- coding: utf-8 -*-
# v20a169 靜態測試：v164 review B1＋B2＋C1＋C2。
# 修法選擇（見 NOTES_V20A169.md，唔好假設）：
#  B1：將「庫存空」「今日已送」加入 add() 嘅 known105 清單（一行）——費用欄
#      原樣保留呢兩個狀態字，唔再當 flavor 移入 hint、歸「免費」。唔揀「badge
#      渲染喺費用欄以外」（要改掣結構， blast radius 大）。「不耗日」→「免費」
#      嗰個映射係 UI105 S-23 既有決定，唔喺呢票郁。
#  B2：ux68OrganizeLocSheet 嘅 .ux68-why badge 由直接 append 入 .act（row flex
#      第 4 個 item，被擠到 min-content 變 7 行直欄、縱跨兩卡），改為 append 入
#      .act-txt118 文字欄（簡介之下橫排紅字）；再將 #loc-acts 由 grid 轉 flex 直欄
#      ＋掣 flex-shrink:0——實駕揭發淨係搬 badge 唔夠：grid auto 行高跟 max-content
#      （唔換行）計，長簡介卡被夾喺 50px 行高（文字欄實測 91px、掣 50px，簡介＋badge
#      溢出框外）；align-self:start 只令掣本身長返 115px、行高照舊 50px 依然重疊。
#      根治係容器轉 flex 直欄（卡高＝內容高，實測 push 卡 115px、零重疊）＋掣唔縮
#      （容器唔夠高嗰陣改內滾，唔壓縮卡高）。幾何斷言喺實駕做，唔喺靜態做。
#  C1：名筆 :liked 第一句「…靠感人情書辦事的人」疑似筆誤——改字（唔係重寫）做
#      「…靠感情、靠人情辦事的人」（跟 review 建議字眼；第一句同第二句一字唔郁）。
#      經 applyTangGift169 載入正規化覆寫 byKey＋entries 兩份，唔直改 pack JSON；
#      只喺現句含「感人情書」嗰陣先改。
#  C2：四件 v164 新貨喺 shop_street_mk stock 置頂（由第 11–14 位移到頭 4 位，
#      其餘 10 件相對次序不變）。唔揀分組（商店 modal 係 flat rows，加組頭要改
#      渲染）／唔揀 hint（治標）。只係顯示次序，count／補貨唔郁。
# 唔郁：咖啡豆 :liked 句（v167 進行中）、push1 live 到唔到、玫瑰 dislike 照扣庫存。
# 反證：喺 pristine main（5e6a6b0／v168）index 上行，新行為斷言會乾淨 FAIL，
#      唔會 crash。pack 守門斷言喺 pristine 都 PASS（佢哋守「pack 冇郁過」）。
# 行號：B1／B2／loader 呼叫全部同行改動（零行數漂移）；新函數 applyTangGift169
#      加喺檔尾（applyTangGift164 之後），test_tang152／travel114／kwan151 釘行
#      全部喺插入點之前，唔使 resync。
# 用法：python3 tests/test_tang169_static.py [path-to-index.html]
import json
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
ROOT = Path(__file__).resolve().parent.parent
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def fn_body(name):
    s = src.find('function %s(){' % name)
    if s < 0: return ''
    e = src.find('\n}\n', s)
    return src[s:e] if e > 0 else ''

# --- 紀律：SAVE key／softRev／?v= 不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- §1. B1：gate badge 狀態字入 known105 ---
ok('B1：known105 有「庫存空」＋「今日已送」',
   '"庫存空","今日已送"' in src)
ok('B1：giftGateBadge 仍然回傳呢兩個狀態字',
   'if(/庫存/.test(r)) return "庫存空";' in src
   and 'if(/今天|今日|人情急|先到這裡/.test(r)) return "今日已送";' in src)
ok('B1：已知狀態字分支喺 flavor 分支之前（入咗清單就唔會被移入 hint）',
   src.find('known105.indexOf(cost105)<0') > src.find('const known105 = ['))
ok('B1：其他 known105 狀態字唔郁（「今日已滿」「未開放」「沽清」仲喺度）',
   all(x in src for x in ('"今日已滿"', '"未開放"', '"沽清"')))
ok('B1：ok 態「不耗日」→「免費」映射唔郁（UI105 既有決定，唔喺呢票改）',
   'cost105==="無" || cost105==="不耗日"' in src)

# --- §2. B2：urgent badge 入文字欄，唔再做 row flex item ---
ok('B2：organizer 將 badge append 入 .act-txt118（有就入欄，冇先退回掣本身）',
   '(it.btn.querySelector(".act-txt118")||it.btn).appendChild(s);' in src)
ok('B2：舊寫法（badge 直接 append 入 .act）已無',
   'it.btn.appendChild(s);' not in src)
ok('B2：badge 仍然只加一次（querySelector 守門仲喺度）',
   'if(!it.btn.querySelector(".ux68-why")){' in src)
ok('B2：.ux68-why 樣式唔郁（display:block、紅字，入欄後即係簡介之下橫排一行）',
   '.ux68-why{ display:block; font-size:.74rem; font-weight:700; color:#9c3d1e;' in src)
ok('B2：#loc-acts 由 grid 轉 flex 直欄（卡高隨內容增長，唔再被 grid 行高夾住）',
   '#loc-sheet.sheet.locpanel118 #loc-acts{ display:flex !important; flex-direction:column !important; }' in src)
ok('B2：#loc-acts 掣 flex-shrink:0（容器唔夠高嗰陣唔壓縮卡高，改為內滾）',
   '#loc-sheet.sheet.locpanel118 #loc-acts .act{ flex-shrink:0; }' in src)
ok('B2：flex 直欄下掣闊度唔郁（.act width:100%＋預設 stretch）',
   '.act{display:flex;justify-content:space-between;gap:8px;align-items:center;width:100%;' in src)
ok('B2：organizer 仍然只喺有要事／鎖定／多組嗰陣先重組（早退條件唔郁）',
   'if(!hasUrgent && !hasLocked && groupSet.size <= 1) return;' in src)

# --- §3. C1：名筆句改字（覆寫，唔直改 pack） ---
fn = fn_body('applyTangGift169')
ok('C1：applyTangGift169 函數在位', 'function applyTangGift169(){' in src)
ok('C1：接線喺 GiftShop.ensureSave() 行同行呼叫（零行數漂移，喺 GIFT_REACT 賦值後）',
   'try{ if(typeof GiftShop!=="undefined") GiftShop.ensureSave(); }catch(_g){} try{ if(typeof applyTangGift169==="function") applyTangGift169(); }catch(_t169){}' in src)
ok('C1：接線喺 textfix55Walk(giftReact) 之前（新句行同一套清洗）',
   src.find('applyTangGift169(); }catch(_t169){}') < src.find('textfix55Walk(giftReact, null, null, TEXTFIX55_OPTS_GIFT)'))
ok('C1：新句全文＝「…靠感情、靠人情辦事的人。」（改字，唔係重寫）',
   '鄧麗萍：「名筆。簽名、批檔期、改數字，都用得着。你至少知道我不是靠感情、靠人情辦事的人。」' in fn)
ok('C1：第一句「名筆。簽名、批檔期、改數字，都用得着。」一字唔郁',
   '名筆。簽名、批檔期、改數字，都用得着。' in fn)
ok('C1：byKey（tang:gift_fountain_pen:liked）＋entries（GR-tang-pen｜liked）兩邊一齊覆寫',
   'R.byKey["tang:gift_fountain_pen:liked"]' in fn
   and 'e.id==="GR-tang-pen｜liked"' in fn)
ok('C1：只喺現句含「感人情書」嗰陣先改（pack 日後已修正唔會俾覆寫返）',
   fn.count('indexOf("感人情書")>=0') == 2)
ok('C1：唔掂咖啡豆（v167 範圍）', 'gift_coffee_beans' not in fn)
ok('C1：唔掂 likes／dislikes（純文案覆寫）',
   'likes' not in fn and 'dislikes' not in fn)

# --- §4. C2：新貨置頂 ---
ok('C2：置頂次序＝名筆／計數機／腕表／玫瑰（跟 v164 注入次序）',
   'const TOP169 = ["gift_fountain_pen","gift_desk_calculator","gift_dress_watch","gift_rose_premium"];' in fn)
ok('C2：穩定重排（頭四位＋其餘不變），冪等',
   'const reordered = top.concat(rest);' in fn
   and 'for(let i=0;i<reordered.length;i++) shop.stock[i] = reordered[i];' in fn)
ok('C2：只郁 shop_street_mk stock 陣，唔郁 count／補貨／舊檔 shopStock',
   's.shopId==="shop_street_mk"' in fn and 'restock' not in fn
   and 'shopStock' not in fn and 'S.giftMeta' not in fn)
ok('C2：商店渲染跟 stock 陣次序（shopList map shop.stock）',
   'return (shop.stock||[]).map(row=>{' in src)

# --- §5. pack JSON 守門（冇直改） ---
react = json.loads((ROOT / 'content' / 'gift_react_copy.json').read_text(encoding='utf-8'))
shops = json.loads((ROOT / 'content' / 'shops.json').read_text(encoding='utf-8'))
by = react.get('byKey', {})
ok('pack 唔郁：gift_react_copy.json 原句仲有「感人情書」（覆寫喺 index.html）',
   '感人情書' in by.get('tang:gift_fountain_pen:liked', {}).get('lines', [''])[0])
ok('pack 唔郁：shops.json shop_street_mk 仲係 10 格，冇新貨 id',
   len(shops.get('shops', [{}])[0].get('stock', [])) == 10
   and not any(r.get('itemId') in ('gift_fountain_pen', 'gift_desk_calculator', 'gift_dress_watch', 'gift_rose_premium')
             for r in shops.get('shops', [{}])[0].get('stock', [])))

print('RESULT ' + ('FAIL (%d)' % len(fails) if fails else 'PASS'))
sys.exit(1 if fails else 0)
