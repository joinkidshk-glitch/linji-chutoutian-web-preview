# v398 resync：35_invite 請柬加 keepScene397:true（日結卡家族統一場景背圖），onDismiss=skip 唔郁；見 qa398/resync398.py。
# v20a236 reconfirm 靜態測試：共用確認 helper＋全部 10 個面接線＋唔准郁嘅嘢。
# 用法：python3 tests/test_reconfirm236_static.py [path-to-index.html]
import sys, pathlib
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

def fn_block(decl):
    i = html.find(decl)
    if i < 0:
        return ''
    j = html.find('{', i)
    depth = 0
    for k in range(j, len(html)):
        if html[k] == '{':
            depth += 1
        elif html[k] == '}':
            depth -= 1
            if depth == 0:
                return html[i:k + 1]
    return ''

def block_between(start, end):
    i = html.find(start)
    if i < 0:
        return ''
    j = html.find(end, i)
    return html[i:j] if j > i else ''

# ---- A. 共用機制 ----
ok('A helper confirmChoice236 已定義', 'function confirmChoice236(opts){' in html)
helper = fn_block('function confirmChoice236(opts){')
ok('A helper 有 reconfirm236 標記', 'reconfirm236' in helper)
ok('A helper 標題＋文案係書面語', '確認選擇' in helper and '你選擇了' in helper and '確定後便會即時生效' in helper)
ok('A helper 掣序：返去揀過／確定', '返去揀過' in helper and '"確定"' in helper)
ok('A helper onDismiss 等同返去（行 onCancel）', 'onDismiss' in helper and 'onCancel' in helper)
ok('A helper 選項原文有 esc', 'esc236' in helper and '&lt;' in helper)

# 12 個呼叫點＋1 個定義＝13 次 'confirmChoice236('（pickChoice／WF4／還債×2／請柬×2／傾談×2／打聽／買禮物／治療／v265 買衫）
ok('A 呼叫點齊 13 處（＋定義＝14）', html.count('confirmChoice236(') == 14)

# ---- B. 故事側 ----
pick = fn_block('function pickChoice(choiceId){')
ok('B pickChoice 有 confirmChoice236', 'confirmChoice236({' in pick)
ok('B pickChoice 確認喺 applyChoice 之前',
   pick.find('confirmChoice236({') >= 0 and pick.find('confirmChoice236({') < pick.find('StoryOC.applyChoice(n, choice)'))
ok('B pickChoice 確認後照行 N17 hook＋showResult',
   'ending410AfterEveChoice(n, choice, result)' in pick and 'showResult(n, choice, result)' in pick)
ok('B N17 hook 次序不變（applyChoice 先、hook 後）',
   pick.find('StoryOC.applyChoice(n, choice)') < pick.find('ending410AfterEveChoice(n, choice, result)'))
ok('B 故事後果提示 helper 已定義', 'function storyChoiceConsequence236(n, choice){' in html)
ok('B N17 前夕加不可更改提示', '去留決定一旦落定，不可更改。' in html)
ok('B 無選項「完成這一節」唔加確認（得一個出口、無實質抉擇）',
   'confirmChoice236' not in block_between('完成這一節', 'StoryOC.applyChoice(_sess.node, fake)'))
ok('B resolveEnding410 唔郁（入面冇 confirmChoice236）',
   'confirmChoice236' not in block_between('function resolveEnding410', '/* 前夕抉擇選項生成'))

# ---- B3. WF4 ----
ok('B3 WF4 decide 抉擇先確認', 'confirmChoice236({ choiceLabel: ch.label' in html)
ok('B3 WF4 後果提示 helper 已定義', 'function wf4FxLine236(fx){' in html)
ok('B3 WF4 seen 封印時序唔郁（wf4Fire 照寫 seen＋save）',
   'st.seen[ev.id]' in html and 'function wf4Fire(ev, doneCb){' in html)

# ---- B4. ENC79 ----
enc79 = block_between('function enc79PlayEncounter(starId, locId, wasMet){', '/* ===== v20a176 ROM176')
ok('B4 ENC79 抉擇行內確認（唔經 modal，唔俾 mask 蓋）',
   '確定選擇「' in enc79 and '返去揀過' in enc79)
ok('B4 ENC79 確定先加好感＋runChoiceFx', 'enc79AddFav(starId, fx.fav, "enc")' in enc79 and 'enc79RunChoiceFx(fx.fx)' in enc79)
ok('B4 ENC79 後果預覽行 enc79ChoiceFx', 'enc79ChoiceFx(step.seg, opt.label)' in enc79)

# ---- C. 系統側 ----
shop = block_between('function openGiftShop(shopId, L){', 'function openGiftPick(npcKey, L){')
ok('C1 買禮物先確認後扣錢', 'confirmChoice236({' in shop and 'GiftShop.buyItem(shopId, id)' in shop)
ok('C1 buyItem 本體仲在（確認嗰陣再驗）', 'function buyItem(shopId, itemId){' in html)
ok('C2 打聽先確認後扣茶錢', 'confirmChoice236({ choiceLabel: def.title' in html)
ok('C2 applyMockAsk 本體仲在（直接呼叫測試唔受影響）', 'function applyMockAsk(locId, actionId, repayOpt){' in html)
ok('C3 傾談入口×2 先確認', html.count('confirmChoice236({ choiceLabel: "與"') == 2)
ok('C3 doTalk 本體仲在', 'function doTalk(npcId, L){' in html)
ok('C4 還債禮物／現金兩掣都先確認', html.count('confirmChoice236({ choiceLabel: "以禮物還') == 1 and html.count('confirmChoice236({ choiceLabel: "以現金 $200 還') == 1)
ok('C5 請柬出席／推辭都先確認', 'confirmChoice236({ choiceLabel: "出席「' in html and 'confirmChoice236({ choiceLabel: "推辭「' in html)
ok('C5 請柬遮罩行為唔郁（onDismiss 照＝推辭）', '{ onDismiss: skip, keepSheetContent:true, keepScene397:true }' in html)
ok('C6 醫院治療先確認後扣 $600', 'confirmChoice236({ choiceLabel: "去醫院治療"' in html)
cshop = block_between('function openClothingShop265(L){', 'function renderWardrobe265(')
ok('C7 買衫先確認後扣錢（v265）', 'confirmChoice236({' in cshop and 'buyCostume265(id)' in cshop)

# ---- D. 唔准郁 ----
ok('D 送禮確認仲在（唔重複加）', '確認送禮' in html)
ok('D 接通告／試鏡確認仲在（confirmSpendDay）', 'function confirmSpendDay(actionLabel, onYes, opts){' in html)
ok('D 傳聞拼合確認已刪（v267：requestMergeConfirm 隨傳聞系統刪除）', 'function requestMergeConfirm' not in html and 'requestMergeConfirm(' not in html)
ok('D 體檢確認仲在（buyCheckup105）', 'function buyCheckup105' in html or 'buyCheckup105(' in html)
ok('D resolveEnding410 定義仲在', 'function resolveEnding410(' in html)

print()
print('RECONFIRM236 static: ' + ('ALL PASS' if not fails else 'FAIL ' + str(len(fails))))
sys.exit(1 if fails else 0)
