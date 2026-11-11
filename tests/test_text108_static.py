# v20a108 TEXT108 文字清理包・靜態守門測試。
# 用法：python3 tests/test_text108_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」（舊寫法出現即 FAIL）。
# 覆核項（S-3/10/19/23/24/28/35/37/39/44/45）只釘 v105 既定寫法仍在位，唔重驗 v105 細節。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
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
tut = seg('const TUTORIAL_ZH_HK', 'let TUTORIAL = TUTORIAL_ZH_HK')
for new_s in ('地圖上面嘅地點，就係你可以去嘅地方',
              '喺茶餐廳或者事務所「打聽」唔耗日',
              '通告欄可以免費睇住先',
              '開工之前，記得睇手帳',
              '去對應地點報名訓練',
              '訓練堂數儲夠之後',
              '只有訓練、試鏡、休息同跟行程開工先會計日',
              '教學先到呢度',
              '建議你先去訓練，或者睇吓通告欄',
              '今次未獲聘，呢一場唔可以再參加',
              '可以返去訓練，或者另揀一張通告',
              '獲聘之後，拍攝日已經排咗進行程',
              '開工之前，記得睇手帳同行程，跟住上面嘅安排去做'):
    ok('S-42 新句在位「' + new_s[:14] + '」', new_s in tut)
for gone in ('獲聘後，拍攝日已排進行程。', '開工前看手帳和行程，跟進度。',
             '已獲聘，拍攝日記在行程。', '按行程開工，手帳可看進度。',
             '本次未獲聘，且不可再參加本場。', '可去訓練，或另選通告。',
             '地圖上的地點，就是你可以去的地方', '通告欄可先免費查看',
             '記數簿記收支；行程記拍攝與本週安排', '教學先到這裡（可跳過；選單可重看）。',
             '下一步：訓練／通告欄／進度。', '社交與觀察課就會開放'):
    ok('S-42 舊電報句已清「' + gone[:14] + '」', gone not in tut)
ok('S-42 何生組唔郁（TUT_WELCOME 仍係何生）', '"id":"TUT_WELCOME","speaker":"何生"' in tut)

# ---- S-42（live 路徑）：覆寫表 TEXTFIX55_EXACT —— live 教學行 content/tutorial_zh_HK.json，
#    經 textfix55SimplePack 清洗；inline const 只係 fallback。pack 異文必須喺表入面，否則實駕仍見舊句 ----
ok('S-42 live：pack 異文「製作日」覆寫在位',
   '"獲聘後，製作日已排進行程。": "獲聘之後，拍攝日已經排咗進行程。"' in html)
ok('S-42 live：pack 異文「選單事態」覆寫在位（順帶修正做進度掣）',
   '"建議：先訓練或看通告欄，再打開選單「事態」——第一段故事會接著出現。": "建議你先去訓練，或者睇吓通告欄，再撳地圖上嘅「進度」掣——第一段故事會接著出現。"' in html)
ok('S-42 live：pack 異文「事態」bodyAlt 覆寫在位',
   '"下一步：訓練／通告欄／事態。": "下一步：去訓練，或者睇吓通告欄同進度。"' in html)
ok('S-42 live：pack 異文 TRAIN 覆寫在位',
   '"到對應地點報名訓練，提升能力來解鎖試鏡門檻。": "去對應地點報名訓練，能力夠數先報到試鏡門檻。"' in html)
ok('S-42 live：3 個既有覆寫值已更新（MAPalt／NPCbody／NPCalt）',
   '"訓練解鎖試鏡；打聽免費不耗日（試玩閘下傾談／送禮亦不耗日）。": "訓練夠數先報得試鏡；打聽、傾談同送禮都唔耗日（茶錢另計）。"' in html
   and '"打聽免費。正式版傾談／送禮佔一日；試玩閘下亦不耗日。": "傾談同送禮都唔佔日子（茶錢另計）。"' in html)

# ---- S-49：完結一日統一叫「過一日」 ----
ok('S-49 地圖金掣＝過一日', '>過一日</button>' in html)
ok('S-49 選單項＝過一日', 'data-m="rest-early">過一日</button>' in html)
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
ok('S-15 確認框講明小休', '呢次只係小休，減壓有限，唔似得瞓足一日咁將壓力清零' in html)
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
ok('S-47 空牆新句在位', '有作品圖嘅製作，殺青之後，佢嘅作品圖就會黐喺呢面牆度' in html)
ok('S-47 空牆講明電視特輯冇海報', '冇海報嘅製作（例如電視特輯）' in html)
ok('S-47 空牆舊承諾已清', '接到有名有姓嘅製作，殺青之後，佢嘅作品圖就會黐喺呢面牆度' not in html)
ok('S-47 有牆備註已加限定', '有作品圖嘅殺青製作會收錄喺度' in html)
ok('S-47 有牆備註舊句已清', '殺青作品會收錄喺度。早期做臨記' not in html)

# ---- 覆核項：v105 既定寫法仍在位（走樣即 FAIL） ----
ok('覆核 S-3 行程編輯頁教學行在位', 'id="plan-teach105"' in html)
ok('覆核 S-10 劇情卡「›」釘右中線', '.map-hint-story-btn::after' in html and 'content:"›"' in html)
ok('覆核 S-10 副行截第一句', 'progShort105' in html)
ok('覆核 S-19 確定行程唔再彈壓力 modal', 'commitPlanAndGo();' in body_of('function confirmPlan', 1500))
ok('覆核 S-19 壓力影響句係完整句子', '已經爆煲邊緣' in body_of('function stressImpactLine34', 1500))
ok('覆核 S-23 費用欄正規化在位', 'cost105 = "免費"' in html)
ok('覆核 S-24 事務所信任行冇結局配方', '江湖撈家' not in body_of('function enc79HoTrustLine', 1200))
ok('覆核 S-24 人情頁有江湖路指向（統籌裁決分工）', '第日自有一條江湖路畀你行' in html)
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
