# v20a207 resync (part 2).
# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），6 個釘行按段 +0／+4／+84 重算。
# v20a211 resync：index.html 淨 +42 行，4 釘行按 difflib 映射重寫（純漂移，見 qa211/resync211b.py）。
# v20a176 ROM176 全面隨機巧遇・靜態測試：接線標記／紅線／玩家面文案／行號釘。
# v20a197 resync：index.html 淨 +94 行，全部錨點 difflib 對位核實純漂移（見 qa197/resync197.py）：6072→6127、31583→31638、53416→53510、53784→53878、54923→55017、55017→55111。（B4 補丁再 +9 行，見同檔。）
# v20a191 resync：index.html 淨 +47 行，6 個釘行按段 +2／+9／+47 重算，內容逐字核實純漂移。
# v20a196 resync：showResult −1／晨鏈＋74／WF4＋63／尾段＋83，5 個釘行按段重算（31583→31582、53416→53490、53784→53858、54923→54997、55017→55091），difflib 對位核實內容逐字相同，純漂移。
# v20a191 rebase 上 main b3db32f resync：見釘行區註解。
# v20a183 resync：v183 淨 ＋117 行（C7 CSS ＋2／prefKind ＋1／TryIntercept ＋1／PlayEncounter ＋2／ROM183 block ＋107／確認 modal ＋3／goBit ＋1；difflib 對位核實純漂移，見 qa183/resync183.py）。
# v20a184 rebase 上 main 0f90dc7（v183）resync：v184 淨 ＋16 行（C2 helper＋9／請柬＋1／結果卡＋1／C1 DEEPS＋4／漸變＋1 淨）；＜45748 者唔郁、其後者 ＋16（difflib 對位核實純漂移，見 qa184/resync184_rebase.py）。
# v20a181 rebase 上 main 9640c6f（v183）resync：6 個釘行按 difflib 映射重算（6032→6045、31536→31549、53053→53061、53421→53429、54560→54568、54654→54662；內容逐字相同，純漂移）。
# v20a181 第二次 rebase 上 main 77603b3（v184）resync：v184 淨 ＋16（全部喺 45748–46484 之間）；6045／31549 唔郁，53061→53077、53429→53445、54568→54584、54662→54678（difflib 雙基底對位核實純漂移，見 qa181/resync181_rebase2.py）。
# v20a182 resync：v182 淨 ＋17 行，錨點按段 ＋2／＋12／＋17（NPCS 6028＋2、載入點 31531＋2、block 53033＋12、其後 ＋17；qa182/resync182.py difflib 對位核實純漂移）。
# v20a189 resync：index.html 淨 ＋34 行（accel-link CSS ＋15 @~1831／day-res 92dvh media ＋10 @~3235／hint 刪除 −10 @37990／soft map 掣 ＋3／accel link push ＋12／day-res class ＋4；difflib 對位核實純漂移，見 qa189/resync189.py）。
# v20a189 rebase 上 main 0c29f03（v188）resync：淨 +254（v188；v190 淨 0）；釘行按段 +0／+254（6070／31574 唔郁、53115→53369、53483→53737、54622→54876、54716→54970；difflib 對位核實純漂移，見 qa189/resync189_rebase.py）。
# 用法：python3 tests/test_rom176_static.py [path-to-index.html]
# 反證：pristine main (a618a5d) 冇 ROM176 標記、「唔靠送禮」仲喺度、地點板仲有女角送禮掣 → 多項 FAIL。
import io, json, os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = io.open(path, encoding='utf-8').read()
lines = html.split('\n')
root = os.path.dirname(os.path.abspath(path))
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)
def line(n):
    return lines[n - 1] if 1 <= n <= len(lines) else ''
def seg(start, end):
    try:
        i = html.index(start)
    except ValueError:
        return ''
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

# ---- 紅線：SAVE key／softRev／?v= 不變 ----
ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('?v= 冇變', 'v=20a10' in html or '?v=20a10' in html or '20a10&softBehaviorGate' in html)

# ---- content pack JSON 唔郁（星 prefs＋反應句＋海媚 prefs 全部 runtime 注入） ----
prefs = json.loads(io.open(os.path.join(root, 'content/gift_prefs.json'), encoding='utf-8').read())
ok('gift_prefs.json：npcs 只有原有 6 項（冇星、冇海媚）',
   set(prefs.get('npcs', {}).keys()) == {'vera', 'hiu', 'choi', 'lan', 'xu', 'tang'})
ok('gift_prefs.json：lan／xu prefs 原封不動（唔重複注入）',
   prefs['npcs']['lan']['likes'] == ['gift_handmade_sweet', 'gift_cassette_indie']
   and prefs['npcs']['xu']['likes'] == [])
react = json.loads(io.open(os.path.join(root, 'content/gift_react_copy.json'), encoding='utf-8').read())
ok('gift_react_copy.json：55 條原封不動（冇星反應句）',
   len(react.get('entries', [])) == 55
   and not any(str(e.get('npcKey', '')).startswith(('luk_', 'liu_', 'ngai_', 'yip_', 'mak_', 'lok_', 'pang_', 'chung_', 'gu_', 'so_', 'chai_', 'ching_')) for e in react['entries']))
items = json.loads(io.open(os.path.join(root, 'content/items_gifts.json'), encoding='utf-8').read())
ok('items_gifts.json：10 樣禮物齊（唔郁）',
   {e['itemId'] for e in items.get('items', [])} >=
   {'gift_pineapple_bun_set', 'gift_egg_tart_box', 'gift_thermos', 'gift_hair_clip_set', 'gift_memo_pad',
    'gift_coffee_beans', 'gift_cassette_indie', 'gift_handmade_sweet', 'gift_fashion_mag', 'gift_perfume_sample'})

# ---- ROM176 模組在位 ----
ok('ROM176 模組標記', 'v20a176 ROM176' in html)
ok('ROM176_WOMEN 六位女角', 'const ROM176_WOMEN' in html and all(k in html for k in ['"hiu"', '"choi"', '"vera"', '"lan"', '"xu"', '"mei"']))
ok('ROM176 常數（P 0.50／share 0.65／caps 1／3／冷卻 2／保底 5）',
   'const ROM176_P = 0.50, ROM176_SHARE = 0.65, ROM176_DAILY_CAP = 1, ROM176_WEEKLY_CAP = 3, ROM176_COOLDOWN = 2, ROM176_PITY_DAYS = 5' in html)
for fn in ('rom176TryIntercept', 'rom176PlayEncounter', 'rom176DoGiveStarGift', 'rom176ApplyGiftOverrides',
           'rom176GrantWhisper', 'rom176MeiUnlocked', 'rom176BackOpts', 'rom176StarDelta', 'rom176CanGiveStarGift'):
    ok('函數在位：' + fn, ('function ' + fn) in html)

# ---- 行號釘（本票插入點；下次 resync 對呢啲） ----
# v20a199 resync：index.html 淨 +44 行（DLG199 ＋30／fitApply ＋13／WF4 onload ＋1）；釘行按 difflib 映射重算，內容逐字核實純漂移。
# v20a186 resync：index.html 淨 ＋4 行（結果卡同屆提名行移出逐類別卡，插入點 L45783–45826），其後釘行各 ＋4（53077→53081、53445→53449、54584→54588、54678→54682）；NPCS lan／GIFT_REACT 釘喺插入點之前，唔郁。
# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點 L45380–46310）；其後釘行各 +225，之前唔郁；總行數 60155→60380。
# v20a188 resync 補 +29：上一手 +225 計少咗其後再加嘅 NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口（淨 +29）；總淨變 +254，總行數 60409；difflib 對位核實全部錨點純漂移，見 qa188/resync188_verify.py。
# v20a206 C1 resync：index.html 淨 +22 行（WF4 保底，插入點舊 L41129–41496）；其後釘行各 +22（54302→54324、54670→54692、55809→55831、55903→55925），之前唔郁；qa206/resync206.py difflib 對位核實純漂移。
# v20a206 C2 resync：index.html 淨 +3 行（WF4 覆寫表頭註解＋3，插入點舊 L41271 之後）；其後釘行各 +3（54324→54327、54692→54695、55831→55834、55925→55928）；qa206/resync206c2.py difflib 對位核實純漂移。
# v20a207 rebase 上 main 8cecf7f（v206）resync：v206 +25（C1 +22／C2 +3，插入點 ~41129／41271 之後）＋v207 +34；/tmp/verify207.py 73 錨點對位零 mismatch，純漂移。
ok('釘：NPCS lan 條目 L6151', line(6151).startswith('  lan:{ id:"lan", name:"藍若曦"'))
ok('釘：載入點 L31712（GIFT_REACT 賦值同行呼叫注入）',
   'GIFT_REACT = giftReact' in line(31712) and 'rom176ApplyGiftOverrides()' in line(31712))
ok('釘：ROM176 block 起點 L54658', line(54658).startswith('/* ===== v20a176 ROM176'))
ok('釘：rom176ApplyGiftOverrides 定義 L55026', line(55026).startswith('function rom176ApplyGiftOverrides()'))
ok('釘：addLocTalkGiftActs L56165', line(56165).startswith('function addLocTalkGiftActs(add, L, npcId)'))
ok('釘：openLoc rom176 攔截 L56259', 'rom176TryIntercept(id)' in line(56259))
# v20a208 resync：rebase 上 main b7ddb37，釘行按 difflib 映射重寫（54393→54616、54761→54984、55900→56123、55994→56217；6151／31712 唔郁），qa208/resync208_rebase.py 核實純漂移。
# v20a211 rebase resync：v208 +223 之上再加 v211 +42（54616→54658、54984→55026、56123→56165、56217→56259），diff 映射逐行內容核實純漂移。
# v20a191 rebase 上 main b3db32f resync：v189 淨 +34 行＋v191 淨 +47 行，6 個釘行按段 +2／+9／+47 重算（6070→6072、31574→31583、53369→53416、53737→53784、54876→54923、54970→55017），difflib 對位核實純漂移。

# ---- 注入呼叫位置（GIFT 賦值之後、同一行） ----
gi = html.find('GIFT_REACT = giftReact')
ci = html.find('rom176ApplyGiftOverrides()')
ok('注入呼叫喺 GIFT_REACT 賦值之後', gi >= 0 and ci > gi)

# ---- NPCS 藍／徐／海媚 ----
for k, nm, face, homes in (('lan', '藍若曦', 'npc_lan', '"tvb_longmen","tvb_kowloon"'),
                           ('xu', '徐寶珊', 'npc_xu', '"ad_central","ad_adm"'),
                           ('mei', '關海媚', 'npc_mei', '"ad_adm","rec_hk"')):
    ok('NPCS 有 %s（%s，homes 主＋副）' % (k, nm),
       ('  %s:{ id:"%s", name:"%s"' % (k, k, nm)) in html and ('face:"%s"' % face) in html and homes in html)

# ---- 48 條星反應句（FAV176 24＋GEN176 24） ----
fav = seg('const FAV176 = [', '];')
gen = seg('const GEN176 = [', '];')
stars = ['luk_baakyin', 'liu_bingxing', 'ngai_wingnaam', 'yip_manji', 'mak_zhendong', 'lok_gasing',
         'pang_siuki', 'chung_choning', 'gu_mingfai', 'so_jiyan', 'chai_zanhoi', 'ching_tinlok']
ok('FAV176 24 條（每星 2 條最愛 item-specific）',
   len(re.findall(r'\["[a-z_]+","gift_[a-z_]+",', fav)) == 24
   and all(fav.count('["' + s + '",') == 2 for s in stars))
ok('GEN176 24 條（每星喜歡／唔鍾意各 1 條 tier-generic）',
   len(re.findall(r'\["[a-z_]+","(liked|dislike)",', gen)) == 24
   and all(gen.count('["' + s + '","liked"') == 1 and gen.count('["' + s + '","dislike"') == 1 for s in stars))
ok('海媚 prefs 注入（最愛保溫瓶＋拍紙簿）',
   'mei:{ fav:["gift_thermos","gift_memo_pad"]' in html)

# ---- 星送禮接駁 ----
ok('enc79AddFav 週軟頂包埋 "gift"（兩處）', html.count('|| src==="gift"') == 2)
ok('giveGift 回傳冇 costsDay:true 殘留', 'costsDay:true' not in html)
dg = seg('function doGiveGift(npcKey, itemId, L){', 'function inv72Html')
ok('doGiveGift 有星分支（唔行 giveGift）', 'enc79StarDef(npcKey)' in dg and 'rom176DoGiveStarGift(npcKey, itemId, L)' in dg)
ok('doGiveGift／doTalk／openGiftPick 返程行 rom176BackOpts', html.count('rom176BackOpts()') >= 5)
ok('星巧遇收尾有「送禮」掣', '送禮畀" + def.name' in html and 'rom176CanGiveStarGift(starId)' in html)
ok('openGiftPick 星副標（每日每星限送 1 份）', '每日每星限送 1 份' in html)

# ---- 地點板：女角掣拎走，非女角保留 ----
ok('地點板冇女角送禮掣（「送禮：${NPCS」零出現）', '送禮：${NPCS' not in html)
al = seg('function addLocTalkGiftActs(add, L, npcId){', 'function openLoc')
ok('addLocTalkGiftActs 有女角閘（rom176IsWomanNpc）', 'rom176IsWomanNpc' in al)
ok('addLocTalkGiftActs 冇 romance 送禮 try block', 'romanceKeyFromMapNpc' not in al)
ok('非女角傾談掣保留', '同${NPCS[npcId].name}傾談' in al)
ok('鄧麗萍送禮掣保留（agency_ho 專屬段）', '送禮：鄧麗萍' in html)

# ---- openLoc 攔截次序：女角先過星 ----
ok('openLoc 有 rom176 攔截', 'rom176TryIntercept(id)' in html)
ok('女角攔截行先過星攔截', html.find('rom176TryIntercept(id)') >= 0 and html.find('rom176TryIntercept(id)') < html.find('enc79TryIntercept(id)'))

# ---- 文案 ----
ok('紅星段「唔靠送禮」已改', '唔靠送禮' not in html)
ok('紅星段新文案', '撞到嗰陣可以傾偈、送禮。' in html)
ok('人脈頁提示改做「撞佢」', '去佢常出沒嘅地方撞佢；撞到先可以傾談／送禮。' in html)
ok('人脈頁女角行有出沒提示', '多數喺' in html and '常喺' in html and '出沒' in html)
ok('庫存頁送禮提示改做「撞到先送得」', '喺地點撞到女角／紅星嗰陣先送得' in html)

# ---- 風聲（女角版） ----
ok('茶聽有女角風聲分支（roll<0.50）', 'rom176TeaTargets()' in html and 'romwhisper' in html)
ok('風聲 rumorId 用 romwind:', '"romwind:"+gain.key+":"+day' in html)
ok('茶餐廳女角行蹤線 6 句', all(x in html for x in ['ROM176_TEA_LINES', '林曉晴呢排多數喺', '周采兒呢幾日成日喺', 'Vera 呢排多數喺', '藍若曦呢排成日喺', '徐寶珊呢幾日多數喺', '關海媚呢排會喺']))

# ---- 海媚閘（C9 主閘，day≥699 退路＝1991-12-01） ----
ok('海媚閘主閘係 isDone("C9")', 'StoryOC.isDone("C9")' in html)
ok('海媚閘退路 day≥699', '>= 699' in seg('function rom176MeiUnlocked()', 'function rom176WhisperActive'))

# ---- 唔郁嘅嘢 ----
ok('星冇寫入 S.npcs（NPCS 冇星 id 條目）',
   not any(('  %s:{ id:"%s"' % (s, s)) in html for s in stars))
ok('冇自己寫排他鎖／約會系統', 'rom159DateGate' in html and 'function rom159DateGate' not in html)
ok('約會入口 defensive（只喺 typeof 檢查後出）', 'typeof rom159DateGate==="function"' in html)

print('---')
print('FAILURES: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
