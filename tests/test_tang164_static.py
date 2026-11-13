# -*- coding: utf-8 -*-
# v20a164 靜態測試：鄧麗萍送禮補完（v152 殘留）。
# 調查結論（見 NOTES_V20A164.md §1，唔好假設）：
#  (a) gift_prefs.json tang likes／dislikes 皆空 → prefKind 永遠 neutral；
#      gift_react_copy.json 嘅 tang 專屬句齊晒（:liked 名筆／計數機／腕表、
#      :dislike 玫瑰、:neutral 拍紙簿／咖啡豆）。
#  (b) 咖啡豆只有 :neutral 句，冇 :liked 句——唔入 likes（入咗會跌返 neutral 句，
#      但 delta 計 +2，句同數打架）；咖啡豆行 neutral。
#  (c) 名筆／計數機／腕表／玫瑰四件貨根本唔喺 items_gifts.json／shops.json
#      （商店只得 10 件 MVP 貨）——冇得買就冇得送，要經載入正規化注入埋貨＋上架。
#  (d) rel_tang 係排片線生意閘（push1 需 flag_tang_open ∧ rel_tang≥2；見面 data
#      抉擇先 +1，live 再無其他 +1 來源）——送禮唔加 rel_tang，否則用錢買通排片線。
# 做法：index.html 載入正規化 applyTangGift164（跟 loc96／normaliseTangStub152 先例），
#      唔直改 content pack JSON；UI 入口＝事務所地點板「送禮：鄧麗萍」掣（見面後先出），
#      行現成 openGiftPick；MAP_NPC_TO_KEY 唔郁（佢唔係地圖駐場 NPC）。
# 反證：喺 pristine main（222a984／v152）index 上行，新行為斷言（§2／§3／§4／§5）
#      會乾淨 FAIL，唔會 crash。JSON 守門斷言（§6／§7）喺 pristine 都 PASS——
#      佢哋係「pack 冇俾人郁過＋反應句本身存在」嘅守門，唔係反證目標。感情線守門（§8）
#      喺 pristine 同樣 PASS（v152 已經清乾淨），作用係釘死唔准返生。
# 行號：除咗事務所掣一段（53760 起 ＋16 行）之外全部同行改動／檔尾加函數，
#      test_tang152 釘行（25696／31316／31460）唔受影響；travel114 免費／計數清單
#      行號 ≥53764 者 +16（見 tests/test_travel114_static.py 頭註 resync 紀錄）。
# 用法：python3 tests/test_tang164_static.py [path-to-index.html]
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

# --- §2. 載入正規化接線 ---
ok('接線：applyTangGift164 函數在位', 'function applyTangGift164(){' in src)
ok('接線：giftPrefs 賦值行同行呼叫（零行數漂移）',
   'if(giftPrefs && giftPrefs.npcs) GIFT_PREFS = giftPrefs; try{ if(typeof applyTangGift164==="function") applyTangGift164(); }catch(_t164){}' in src)

# --- §3. prefs 覆寫內容（3 liked＋1 dislike；咖啡豆唔入 likes） ---
fn = fn_body('applyTangGift164')
ok('prefs：likes＝名筆／計數機／腕表（三件，對齊已有 :liked 句）',
   't.likes = ["gift_fountain_pen","gift_desk_calculator","gift_dress_watch"];' in fn)
ok('prefs：dislikes＝玫瑰', 't.dislikes = ["gift_rose_premium"];' in fn)
ok('prefs：咖啡豆唔入 likes（佢只有 :neutral 句）', 'gift_coffee_beans' not in fn)

# --- §4. 貨品注入＋上架 ---
ok('貨：名筆 $550／計數機 $280／腕表 $650／玫瑰 $600',
   'itemId:"gift_fountain_pen", name:"名筆"' in fn and 'price:550' in fn
   and 'itemId:"gift_desk_calculator", name:"桌上計數機"' in fn and 'price:280' in fn
   and 'itemId:"gift_dress_watch", name:"正裝腕表"' in fn and 'price:650' in fn
   and 'itemId:"gift_rose_premium", name:"高級玫瑰花束"' in fn and 'price:600' in fn)
ok('貨：四件都入 shop_street_mk 每週補貨（2／2／1／2）',
   'put("gift_fountain_pen", 2); put("gift_desk_calculator", 2); put("gift_dress_watch", 1); put("gift_rose_premium", 2);' in fn)
ok('貨：舊檔同週 shopStock 補埋缺嘅四格',
   'fill("gift_fountain_pen", 2); fill("gift_desk_calculator", 2); fill("gift_dress_watch", 1); fill("gift_rose_premium", 2);' in fn)
ok('貨：注入冪等（已存在唔重複加）', fn.count('if(!items.some(x=>x && x.itemId===it.itemId)) items.push(it);') == 1
   and fn.count('if(!shop.stock.some(r=>r && r.itemId===id)) shop.stock.push(') == 1)

ok('貨：四件新貨 emoji 都有圖標對照（v112 墨線風，唔准 passthrough）',
   all(('"🖊️":"gift_pen"' in src, '"🧮":"gift_calculator"' in src,
        '"⌚":"gift_watch"' in src, '"🌹":"gift_rose"' in src)))
ok('貨：四隻新圖標檔案齊（256×256 透明底）',
   all((ROOT / 'assets' / 'icons' / ('icon_gift_%s.png' % st)).is_file()
       for st in ('pen', 'calculator', 'watch', 'rose')))

# --- §5. giveGift：鄧麗萍唔加 rel_tang ---
ok('rel：giveGift tang 專例，applied 強制 0',
   'let applied = (npcKey==="tang") ? 0 : rawDelta;' in src)
ok('rel：其他人唔受影響（舊行已無，tang 三元只出現一次）',
   '    let applied = rawDelta;' not in src
   and src.count('let applied = (npcKey==="tang") ? 0 : rawDelta;') == 1)

# --- §6. UI 入口（事務所地點板＋結果文案） ---
ok('UI：事務所出「送禮：鄧麗萍」掣，行現成 openGiftPick',
   'add("送禮：鄧麗萍", hint, giftGateBadge(gate), ()=>{' in src
   and 'openGiftPick("tang", L);' in src)
ok('UI：掣只喺見面後出（flag_tang_open）', 'tangOpen = !!StoryOC.getFlag("flag_tang_open");' in src)
ok('UI：掣只喺事務所出（L.id==="agency_ho"）',
   'if(L.id==="agency_ho" && typeof GiftShop!=="undefined" && typeof StoryOC!=="undefined"){' in src)
ok('UI：送禮選擇頁 tang 副標講明唔會改變排片關係',
   'npcKey==="tang"?"每日限送 1 次 · 送禮只係公事心意，唔會改變排片關係"' in src)
ok('UI：送禮結果 tang 顯示「排片關係不變」唔係「好感 ±0」',
   'const deltaTxt = npcKey==="tang" ? "排片關係不變" :' in src)
ok('UI：手帳庫存提示提埋鄧麗萍', '喺事務所見過鄧麗萍之後' in src)  # v176 改咗句式（去「或者」），意思不變

# --- §7. pack JSON 守門（冇直改；反應句 id 同 prefs key 對得上） ---
prefs = json.loads((ROOT / 'content' / 'gift_prefs.json').read_text(encoding='utf-8'))
react = json.loads((ROOT / 'content' / 'gift_react_copy.json').read_text(encoding='utf-8'))
items = json.loads((ROOT / 'content' / 'items_gifts.json').read_text(encoding='utf-8'))
shops = json.loads((ROOT / 'content' / 'shops.json').read_text(encoding='utf-8'))
tang_prefs = prefs.get('npcs', {}).get('tang', {})
ok('pack 唔郁：gift_prefs.json tang likes／dislikes 仲係空（覆寫喺 index.html）',
   tang_prefs.get('likes') == [] and tang_prefs.get('dislikes') == [])
ok('pack 唔郁：gift_prefs.json tang 見面閘留返 flag_tang_open',
   tang_prefs.get('requireFlagsAny') == ['flag_tang_open'])
ok('pack 唔郁：items_gifts.json 仲係 10 件，冇新貨 id',
   len(items.get('items', [])) == 10
   and not any(x.get('itemId') in ('gift_fountain_pen', 'gift_desk_calculator', 'gift_dress_watch', 'gift_rose_premium')
             for x in items.get('items', [])))
ok('pack 唔郁：shops.json shop_street_mk 仲係 10 格，冇新貨 id',
   len(shops.get('shops', [{}])[0].get('stock', [])) == 10
   and not any(r.get('itemId') in ('gift_fountain_pen', 'gift_desk_calculator', 'gift_dress_watch', 'gift_rose_premium')
             for r in shops.get('shops', [{}])[0].get('stock', [])))
by = react.get('byKey', {})
ok('反應句：三件 liked 都有 :liked 句（id 對得上）',
   by.get('tang:gift_fountain_pen:liked', {}).get('id') == 'GR-tang-pen｜liked'
   and by.get('tang:gift_desk_calculator:liked', {}).get('id') == 'GR-tang-calc｜liked'
   and by.get('tang:gift_dress_watch:liked', {}).get('id') == 'GR-tang-watch｜liked')
ok('反應句：玫瑰有 :dislike 句（GR-tang-rose｜dislike）',
   by.get('tang:gift_rose_premium:dislike', {}).get('id') == 'GR-tang-rose｜dislike')
ok('反應句：拍紙簿／咖啡豆有 :neutral 句（行 neutral 分流）',
   by.get('tang:gift_memo_pad:neutral', {}).get('id') == 'GR-tang-memo｜neutral'
   and by.get('tang:gift_coffee_beans:neutral', {}).get('id') == 'GR-tang-coffee｜neutral')
ok('反應句：咖啡豆冇 :liked 句（所以唔入 likes，見 NOTES §1）',
   'tang:gift_coffee_beans:liked' not in by)
ok('反應句：每件 liked／dislike 貨都有對應 pref 分流（likes↔:liked、dislikes↔:dislike）',
   all('tang:%s:liked' % i in by for i in ('gift_fountain_pen', 'gift_desk_calculator', 'gift_dress_watch'))
   and 'tang:gift_rose_premium:dislike' in by)

# --- §8. 感情線守門（v152 嘅線唔准返生） ---
ok('守線：tang_commit／R_tang_ending／HE／BE 繼續零引用（引號版）',
   '"flag_tang_commit"' not in src and "'flag_tang_commit'" not in src
   and '"flag_tang_he"' not in src and '"flag_tang_be"' not in src
   and 'C_tang_ending_he' not in src and 'C_tang_ending_be' not in src)
ok('守線：R_tang_ending 只剩載入過濾嗰一次', src.count('"R_tang_ending"') == 1)
ok('守線：排片閘門 flag_tang_open ∧ rel_tang≥2 唔郁',
   'pushGate("R_tang_push1", { ctx:{ flags:{ flag_tang_open:true }, rel_tang:2 } }).ok!==true' in src)
ok('守線：MAP_NPC_TO_KEY 唔郁（冇為佢加地圖 NPC 對應）',
   'const MAP_NPC_TO_KEY = { stylist:"vera", colleague:"hiu", reporter:"choi" };' in src)
ok('守線：送禮未開閘文案仲係 tangLocked（院線未到時候）', 'sys.tangLocked||"院線那邊，還未到送禮的時候。"' in src)

print('RESULT ' + ('FAIL (%d)' % len(fails) if fails else 'PASS'))
sys.exit(1 if fails else 0)
