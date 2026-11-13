# -*- coding: utf-8 -*-
# v20a167 靜態測試：鄧麗萍咖啡豆 :liked 句補完（用戶 2026-11-13 拍板；v164 殘留 §1.2）。
# 背景：v164 刻意將咖啡豆留喺 neutral——pack 得 :neutral 句（GR-tang-coffee｜neutral），
#      入 likes 會句（neutral 口吻）同數（liked +2）打架。呢票補一條新 :liked 句，
#      再將咖啡豆入 likes，四件齊 liked。
# 新句（見 NOTES_V20A167.md §1）：
#   「鄧麗萍：「咖啡豆，啱用。夜更對帳要頂到天光，冇佢啲數會走樣。」」
#   「鄧麗萍：「我收下。你識得將心意變成數字，呢啲先叫實用。」」
#   口吻：公事／排片部／講數字，同名筆／計數機／腕表三句同一風格；唔講感情、唔曖昧。
# 做法：載入正規化 applyTangGift167（跟 v164 先例），唔直改 pack JSON；呼叫點喺
#      refreshCopyPacksFromDisk 嘅 GIFT_REACT 賦值行（同行 append，零行數漂移）——
#      一定要喺 GIFT_REACT 賦值之後、textfix55Walk(giftReact) 之前。
# 句數一致性（見 NOTES §3）：reactionEntry 查到新 liked 句；calcDelta 計 liked（raw +2）；
#      giveGift tang 專例 applied 強制 0；giveGift 回傳 delta:applied；doGiveGift tang
#      顯示「排片關係不變」——結果 modal 顯示嘅係 applied（0），唔係 rawDelta，唔會一邊話
#      liked、一邊顯示 neutral 數。
# 反證：喺 pristine main（60b0a8f／v166）index 上行，新行為斷言（§2／§3／§4）會乾淨 FAIL，
#      唔會 crash。Pack／感情線守門（§5／§6）喺 pristine 都 PASS——佢哋係守門，唔係反證目標。
# 用法：python3 tests/test_tang167_static.py [path-to-index.html]
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

L1 = '鄧麗萍：「咖啡豆，啱用。夜更對帳要頂到天光，冇佢啲數會走樣。」'
L2 = '鄧麗萍：「我收下。你識得將心意變成數字，呢啲先叫實用。」'
NEUTRAL = '鄧麗萍：「咖啡豆……夜更對帳用得着。放那邊，我自己煮。」'

# --- 紀律：SAVE key／softRev／?v= 不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- §2. 載入正規化接線 ---
fn = fn_body('applyTangGift167')
ok('接線：applyTangGift167 函數在位', 'function applyTangGift167(){' in src)
ok('接線：GIFT_REACT 賦值行同行呼叫（零行數漂移）',
   'if(giftReact && (giftReact.byKey || giftReact.entries)) GIFT_REACT = giftReact; try{ if(typeof applyTangGift167==="function") applyTangGift167(); }catch(_t167){}' in src)
ok('接線：呼叫點喺 GIFT_REACT 賦值之後（唔係 applyTangGift164 嗰行之前）',
   src.find('applyTangGift167(); }catch(_t167){}') > src.find('GIFT_REACT = giftReact;'))
ok('接線：新句注入喺 textfix55Walk(giftReact) 之前（行同一套清洗）',
   src.find('applyTangGift167(); }catch(_t167){}') >= 0
   and src.find('applyTangGift167(); }catch(_t167){}') < src.find('textfix55Walk(giftReact, null, null, TEXTFIX55_OPTS_GIFT)'))

# --- §3. 新 :liked 句（存在＋口吻＋唔係 neutral 重用） ---
ok('新句：byKey 鍵 tang:gift_coffee_beans:liked 在位',
   'const key = "tang:gift_coffee_beans:liked";' in fn)
ok('新句：id 跟 pattern（GR-tang-coffee｜liked）',
   'id:"GR-tang-coffee｜liked"' in fn)
ok('新句：pref 係 liked', 'pref:"liked"' in fn and 'itemId:"gift_coffee_beans"' in fn)
ok('新句：兩行全文在位（L1＋L2）', L1 in fn and L2 in fn)
ok('新句：唔係 neutral 句重用（冇「放那邊，我自己煮」）',
   'function applyTangGift167(){' in src and '放那邊，我自己煮' not in fn and NEUTRAL not in fn)
ok('新句：口吻係公事／數字（有「數字」「對帳」「實用」）',
   all(w in fn for w in ('對帳', '數字', '實用')))
ok('新句：唔講感情、唔曖昧（新句兩行冇感情／花／鍾意你）',
   L1 in fn and L2 in fn and all(w not in (L1 + L2) for w in ('感情', '鍾意你', '花店', '綁架')))
ok('新句：唔撞 TEXTFIX 改寫（冇 着／别／沒有／我們，上座率）',
   L1 in fn and L2 in fn and all(w not in (L1 + L2) for w in ('着', '别', '沒有', '我們', '上座率')))

# --- §4. 咖啡豆入 likes＋句數一致性 ---
ok('likes：咖啡豆入 likes（冪等 push，有 indexOf 檢查）',
   't.likes.indexOf("gift_coffee_beans")<0' in fn and 't.likes.push("gift_coffee_beans")' in fn)
ok('likes：v164 嗰三件唔郁（applyTangGift164 仲係三件賦值，咖啡豆唔喺佢入面）',
   't.likes = ["gift_fountain_pen","gift_desk_calculator","gift_dress_watch"];' in fn_body('applyTangGift164')
   and 'gift_coffee_beans' not in fn_body('applyTangGift164'))
ok('一致：reactionEntry 查 byKey（pref liked 唔跌返 neutral）',
   'let ent = by[npcKey+":"+itemId+":"+prefKey];' in src)
ok('一致：calcDelta 計 liked（raw +2 來自 deltaRel.liked）',
   'const { delta:rawDelta, kind, relKey } = calcDelta(npcKey, itemId);' in src
   and 'let delta = kind==="liked" ? (Number(dr.liked)||2)' in src)
ok('一致：giveGift tang 專例照行（applied 強制 0，rel_tang 唔郁）',
   'let applied = (npcKey==="tang") ? 0 : rawDelta;' in src)
ok('一致：giveGift 回傳 delta:applied（唔係 rawDelta）',
   'kind, delta:applied, softcap, line, relKey, before, after, costsDay:true' in src)
ok('一致：結果 modal tang 顯示「排片關係不變」，唔顯示數字',
   'const deltaTxt = npcKey==="tang" ? "排片關係不變" :' in src)

# --- §5. 唔影響其他人＋pack JSON 守門 ---
react = json.loads((ROOT / 'content' / 'gift_react_copy.json').read_text(encoding='utf-8'))
prefs = json.loads((ROOT / 'content' / 'gift_prefs.json').read_text(encoding='utf-8'))
by = react.get('byKey', {})
ok('唔郁人：新函數只掂 tang 咖啡鍵，冇其他 NPC 咖啡鍵',
   all((':%s:gift_coffee_beans' % n) not in fn for n in ('choi', 'vera', 'hiu', 'xu', 'lan', 'mei'))
   and 'tang:gift_coffee_beans:liked' in fn)
ok('唔郁人：采兒咖啡 :liked 句仲喺 pack（GR-choi-coffee｜liked，原文不變）',
   by.get('choi:gift_coffee_beans:liked', {}).get('id') == 'GR-choi-coffee｜liked'
   and by.get('choi:gift_coffee_beans:liked', {}).get('lines', [None])[0] ==
       '周采兒：「蘭芳的豆？你有做功課。夜更截稿前，就靠這個提神。」')
ok('唔郁人：注入冪等（byKey 已有唔重加、entries 已有唔重加）',
   'if(!R.byKey[key]){' in fn
   and 'if(!R.entries.some(e=>e && e.id==="GR-tang-coffee｜liked")) R.entries.push(ent);' in fn)
ok('pack 唔郁：gift_react_copy.json 仲係得 6 句 tang，咖啡豆冇 :liked 句（注入喺 index.html）',
   len([e for e in react.get('entries', []) if e.get('npcKey') == 'tang']) == 6
   and 'tang:gift_coffee_beans:liked' not in by)
ok('pack 唔郁：咖啡豆 :neutral 句仲喺度（GR-tang-coffee｜neutral）',
   by.get('tang:gift_coffee_beans:neutral', {}).get('id') == 'GR-tang-coffee｜neutral')
ok('pack 唔郁：gift_prefs.json tang likes／dislikes 仲係空',
   prefs.get('npcs', {}).get('tang', {}).get('likes') == []
   and prefs.get('npcs', {}).get('tang', {}).get('dislikes') == [])

# --- §6. 感情線守門（v152 嘅線唔准返生） ---
ok('守線：tang_commit／R_tang_ending／HE／BE 繼續零引用（引號版）',
   '"flag_tang_commit"' not in src and "'flag_tang_commit'" not in src
   and '"flag_tang_he"' not in src and '"flag_tang_be"' not in src
   and 'C_tang_ending_he' not in src and 'C_tang_ending_be' not in src)
ok('守線：R_tang_ending 只剩載入過濾嗰一次', src.count('"R_tang_ending"') == 1)
ok('守線：MAP_NPC_TO_KEY 唔郁（冇為佢加地圖 NPC 對應）',
   'const MAP_NPC_TO_KEY = { stylist:"vera", colleague:"hiu", reporter:"choi" };' in src)

print('RESULT ' + ('FAIL (%d)' % len(fails) if fails else 'PASS'))
sys.exit(1 if fails else 0)
