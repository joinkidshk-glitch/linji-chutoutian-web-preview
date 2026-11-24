# v20a348 resync：tutorial_zh_HK 文字潤飾（官方 qwen4-max，33 行）；S-42 釘句改查 v348 潤飾後新句（意思不變）；TUT_SHOOT body[0] 潤飾版同 v108 已清電報句逐字相同，該行保留原文，釘句不變。
# v20a108 TEXT108 文字清理包・靜態守門測試。
# 用法：python3 tests/test_text108_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」（舊寫法出現即 FAIL）。
# 覆核項（S-3/10/19/23/24/28/35/37/39/44/45）只釘 v105 既定寫法仍在位，唔重驗 v105 細節。
import os, sys, json

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
tut_json = json.load(open(os.path.join(os.path.dirname(path) or '.', 'content', 'tutorial_zh_HK.json'), encoding='utf-8'))
tut_json_text = ' '.join(b for s in tut_json.get('steps', []) for b in s.get('body', []))
tut_bodies = [b for s in tut_json.get('steps', []) for b in s.get('body', [])]
# v241：JSON 做唯一來源——v108 新句直接寫入 content/tutorial_zh_HK.json（steps body／bodyAlt＋toasts body／bodyAlt），
# 唔再經 TEXTFIX55_EXACT 覆寫。tut_all 覆蓋全部教學句（新句檢查＋舊句已清檢查都用佢）。
tut_all_list = ([b for s in tut_json.get('steps', []) for b in (s.get('body', []) + s.get('bodyAlt', []))]
    + [b for t in tut_json.get('toasts', {}).values() for b in (t.get('body', []) + t.get('bodyAlt', []))])
tut_all = ' '.join(tut_all_list)
def gone_cleared(g):
    # 舊句已清＝live pack 入面冇，或者出現嗰句完整 pack 句係 TEXTFIX55_EXACT key（玩家見新句）
    if g not in tut_all: return True
    return any(g in b and ('"%s":' % b) in html for b in tut_all_list)
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def body_of(fname, span=3000):
    i = html.find(fname)
    return html[i:i + span] if i >= 0 else ''

def seg(a, b):
    i = html.find(a)
    j = html.find(b, i + 1) if i >= 0 else -1
    return html[i:j] if i >= 0 and j > i else ''

# ---- 紅線：SAVE key／softRev／產品 ?v= 冇郁 ----
ok('紅線 SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('紅線 softRev s107', 's107' in html)
ok('紅線產品 ?v= v20a10', 'v20a10' in html)

# ---- S-26：地點板括號說明只第一次出 ----
ok('S-26 長句仍在（第一次用）', '暫時未見熟人（熟人會隨日子／時段出入；地圖標亮＝在場）' in html)
ok('S-26 短句在位（之後用）', 'who = "暫時未見熟人"' in html)
ok('S-26 旗標 seenLocWhoHint26 落 S.flags', 'seenLocWhoHint26' in html)
ok('S-26 長句只出現一次（唔係每板重複寫死）', html.count('暫時未見熟人（熟人會隨日子／時段出入；地圖標亮＝在場）') == 1)

# ---- S-42：系統 modal 文案潤飾（TUTORIAL_ZH_HK 系統組） ----
# v241b: inline TUTORIAL_ZH_HK deleted (JSON sole source); the 13 new sentences now live
# as TEXTFIX55_EXACT values in index.html, the 12 gone sentences must be absent everywhere.
# v241：B 將新句寫入 JSON 嗰陣自行改寫，偏離 v108 定稿——已按已刪 EXACT 值逐句還原 v108 新句入 JSON；
# 13 新句改查 tut_all（JSON 全文），唔再查 index.html（EXACT 值已隨死映射一併刪除）。
tut = tut_all
for new_s in ('地圖上標示的地點都可以前往',
              '在茶餐廳或事務所「打聽」不耗日',
              '通告欄可免費先看',
              '開工前先看手帳',
              '到對應地點報名訓練',
              '訓練堂數足夠後',
              '只有訓練、試鏡、休息和跟行程開工才算日',
              '教學先到這裡',
              '建議先去訓練或看看通告欄',
              '今次未獲聘，這一場不能再參加',
              '回去訓練，或另選一張通告',
              '獲聘之後，拍攝日已經排進了行程',
              '開工前先看手帳和行程，按上面的安排去做'):
    ok('S-42 新句在位「' + new_s[:14] + '」', new_s in tut)
for gone in ('獲聘後，拍攝日已排進行程。', '開工前看手帳和行程，跟進度。',
             '已獲聘，拍攝日記在行程。', '按行程開工，手帳可看進度。',
             '本次未獲聘，且不可再參加本場。', '可去訓練，或另選通告。',
             '地圖上的地點，就是你可以去的地方', '通告欄可先免費查看',
             '記數簿記收支；行程記拍攝與本週安排', '教學先到這裡（可跳過；選單可重看）。',
             '下一步：訓練／通告欄／進度。', '社交與觀察課就會開放'):
    ok('S-42 舊電報句已清「' + gone[:14] + '」', gone_cleared(gone))
ok('S-42 何生組唔郁（TUT_WELCOME 仍係何生）',
   any(s.get('id') == 'TUT_WELCOME' and s.get('speaker') == '何生' for s in tut_json.get('steps', [])))

# ---- S-42（live 路徑）：v241：JSON 做唯一來源——v108 新句已直接寫入 content/tutorial_zh_HK.json，
#    6 個舊 EXACT 覆寫（源頭舊句已唔喺任何 content pack）隨死映射一併刪除；呢度改釘「舊 key 已清＋新值喺 JSON」。
#    （舊覆寫值即係而家 JSON 入面嘅新句，逐條對過，一字不差。）
for _k, _v in (('獲聘後，製作日已排進行程。', '獲聘之後，拍攝日已經排進了行程。'),
               ('建議：先訓練或看通告欄，再打開選單「事態」——第一段故事會接著出現。', '建議先去訓練或看看通告欄，再按地圖上的「進度」掣——第一段故事會接著出現。'),
               ('下一步：訓練／通告欄／事態。', '下一步：去訓練，或看看通告欄和進度。'),
               ('到對應地點報名訓練，提升能力來解鎖試鏡門檻。', '到對應地點報名訓練，能力達標才夠試鏡門檻。'),
               ('訓練解鎖試鏡；打聽免費不耗日（試玩閘下傾談／送禮亦不耗日）。', '訓練夠數才能報名試鏡；打聽、傾談和送禮都不耗日（茶錢另計）。'),
               ('打聽免費。正式版傾談／送禮佔一日；試玩閘下亦不耗日。', '傾談和送禮都不耗日（茶錢另計）。')):
    ok('S-42 live：舊覆寫已刪＋新句喺 JSON「' + _k[:12] + '」', ('"%s":' % _k) not in html and _v in tut_all)

# ---- S-49：完結一日統一叫「過一日」 ----
ok('S-49 地圖金掣＝過一日', '>過一日</button>' in html)
ok('S-49 選單項「過一日」已刪（v397：地圖入口保留）', 'data-m="rest-early"' not in html)
ok('S-49 舊名「逛完・過一日」已清', '逛完・過一日' not in html)
ok('S-49 舊名「提早休息（過一日）」已清', '提早休息（過一日）' not in html)
ok('S-49 確認框標題＝確認過一日', '確認過一日？' in html)
ok('S-49 確認掣＝確定過一日', '確定過一日' in html)
ok('S-49 回顧記名保留「提早休息」（S-14 實際執行類型，唔等於全日休息）',
   'early_rest:{ icon:"🌙", name:"提早休息" }' in html)

# ---- S-50：modal 關閉掣統一 ----
ok('S-50 設定 modal 關閉掣＝關閉', 'label:"關閉"' in body_of('function openSettingsModal', 4000))
ok('S-50 全檔再冇 label:"完成"', 'label:"完成"' not in html)

# ---- S-15：提早休息＝小休級，同全日休息分名（數值唔郁） ----
ok('S-15 確認框講明小休', '這次只是小休，減壓有限，不像睡足一日那樣將壓力清零' in html)
ok('S-15 確認框舊句「等同休息」已清', '等同休息' not in html)
ok('S-15 提早休息日結板標題＝小休', '小休（週${wd}）' in html)
ok('S-15 全日休息標題仍係「休息」（doRest／週計劃 rest 日）',
   html.count('休息（週${wd}）') >= 1 or '休息（週${weekdayName' in html)
ok('S-15 提早休息減壓數值唔郁（stress:-(4+R(0,4))）', 'stress:-(4+R(0,4))' in html)
ok('S-15 全日休息清零數值唔郁（stress:-S.stress）', 'stress:-S.stress' in html)

# ---- S-41：班底見報加來源語境（覆寫表注入，唔改 content pack） ----
ok('S-41 覆寫表有入行消息眉題',
   '"電視城臨記班底添新血": "入行消息：電視台臨記班底添新血"' in html)
ok('S-41 出報機制唔郁（enqueue／出報日相關函數仍在）',
   'function buildNewspaperEdition' in html and 'function enqueueNewspaper' in html)

# ---- S-47：作品牆文案唔再承諾做唔到嘅嘢 ----
ok('S-47 空牆新句在位', '有作品圖的製作，殺青之後，它的作品圖就會黐在這面牆上' in html)
ok('S-47 空牆講明電視特輯冇海報', '沒有海報的製作（例如電視特輯）' in html)
ok('S-47 空牆舊承諾已清', '接到有名有姓嘅製作，殺青之後，佢嘅作品圖就會黐喺呢面牆度' not in html)
ok('S-47 有牆備註已加限定', '有作品圖的殺青製作會收錄在這裡' in html)
ok('S-47 有牆備註舊句已清', '殺青作品會收錄喺度。早期做臨記' not in html)

# ---- 覆核項：v105 既定寫法仍在位（走樣即 FAIL） ----
ok('覆核 S-3 行程編輯頁教學行在位', 'id="plan-teach105"' in html)
ok('覆核 S-10 劇情卡「›」釘右中線', '.map-hint-story-btn::after' in html and 'content:"›"' in html)
# v20a198 C1：storyMapHintHtml 已成個拎走（死 code），progShort105（副行截第一句）只係嗰個
# 已刪 renderer 入面嘅局部變量，一併消失；「下一幕」句式本身留喺 storyMainProgressLine
#（規格＋dev 自檢），內容由進度頁逐行前置句承載。
ok('v198 C1：副行截第一句隨地圖提示 renderer 一併拎走', 'progShort105' not in html and 'function storyMainProgressLine(){' in html)
ok('覆核 S-19 確定行程唔再彈壓力 modal', 'commitPlanAndGo();' in body_of('function confirmPlan', 1500))
ok('覆核 S-19 壓力影響句係完整句子', '已經爆煲邊緣' in body_of('function stressImpactLine34', 1500))
ok('覆核 S-23 費用欄正規化在位（v389 輸出改「不耗日」）', 'cost105 = "不耗日";' in html)
ok('覆核 S-24 事務所信任行冇結局配方', '江湖撈家' not in body_of('function enc79HoTrustLine', 1200))
ok('覆核 S-24 人情頁有江湖路指向（統籌裁決分工）', '日後自有一條江湖路給阿偉走' in html)
ok('覆核 S-28 未達標格式「現值／需 X（差 N）」', '／需 ${b.need}（差 ${b.gap}）' in html)
hired = seg('function aud91PresentOne', '/* 落選')
ok('覆核 S-35 獲聘 modal 有簽約金行', '簽約金 $ ${signPay' in hired)
ok('覆核 S-35 獲聘 modal 有殺青結算行', '殺青嗰日先結算' in hired)
ok('覆核 S-35 獲聘 modal 冇成功率行', '成功率約' not in hired)
ok('覆核 S-37 殺青對帳只留 payWrapNote 一段', 'payWrapNote(sh)' in html)
ok('覆核 S-37 舊重複段只剩刪除註解', html.count('今次入帳係餘額') == 1)
ok('覆核 S-39 生活費用完成日計星期', 'weekdayIdx((S.dayIndex|0)-1)' in body_of('function livingCostDayEndHint', 800))
ok('覆核 S-44 開局冬債狀態＝就嚟到期', 'card_biao_winter' in html and 'status:"就嚟到期"' in html)
ok('覆核 S-45 遠幕合併行在位', 'farMerged105' in html)

print()
print('text108 static: %d fails' % len(fails))
sys.exit(1 if fails else 0)
