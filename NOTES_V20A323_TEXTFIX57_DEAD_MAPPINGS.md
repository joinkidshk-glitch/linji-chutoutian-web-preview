# NOTES_V20A323_TEXTFIX57_DEAD_MAPPINGS

## §1 改動（v323，TEXTFIX57 收尾）

刪死映射＋刪 KEY_RENAME＋補武師班漏網句。偵察 brief 已對 live 核實；統籌開工前喺工作副本逐行再核實一次，行號全部吻合（index.html 47,290 行，main e862947）。

### index.html（淨 −13 行→實數見 §5）
1. TEXTFIX57_EXACT（L14401–14409）刪 5 條死映射：#1 新課程解鎖魅力課、#2 訓練解鎖試鏡、#3 情報刷新金龍茶餐廳、#5 動作演員、#6 大牌；只留 `"未解鎖": "未開放"` 一條。L14404 v241 舊註解一併清走（所指條目早已唔喺度）。
2. L14411 `TEXTFIX57_KEY_RENAME` 成行刪。
3. L14484–14487 walk hook 簡化：刪 nk57 兩行，`else o[k] = nv57;` 改直寫 `o[k] = nv57;`。
4. 附帶：v20a57 區頭註解 B 類描述改返真實（死映射＋標籤改名＋walk 改名已刪，只留一條 EXACT）——註解本身講緊已刪嘅機制，唔改會誤導後人。
5. 唔郁：TEXTFIX57_PHRASES（L14410）、textfix55Str L14463 讀取點、textfix55Freeplay L14539、N9／N12 tagAny（L6825／6836，兩處 live 閘）、ENDING_NEG_TAGS410（L12543）、WEAK_MARKS（L27968，死常數，另開票）。

### content/events_zh_HK.json:145
- `"新課程解鎖：武師班可以報名。"` → `"新課程開辦：武師班可以報名。"`（同孖生句 UNLOCK_CHARM L100／UNLOCK_IQ L104 一致；之前三句得武師班漏網）。

### 測試同步（3 檔）
- tests/test_terms57_logic.js：刪 L30（'B1 unlock event'）、L31（'B1 tutorial title'）、L35（'A3 情報刷新'）、L37（'B2 動作演員 tag'）、L38（'B2 大牌 tag'）、L43–44（'B2 registry labels'／'B2 registry labelToId keys'）；L48 'B2 freeplay wiring' 改為斷言 walk 後 registry 原封不動（label 留「動作演員」、labelToId key 留「動作演員」）；孤兒註解一併修正（B1／A3／B2／registry／wiring 段）。保留 L14（tables present）、L32–33（'B1 lockedHint'）、L39（'B2 prose untouched'）同全部 PHRASES 檢查。
- tests/test_terms57_static.py：L27「tables present」刪 `'TEXTFIX57_KEY_RENAME' in region` 一項；「B2 gate/tag values renamed」`src.count('"身手好"') >= 4` 改 `== 2`（名改 4→2）。
- tests/test_newspaper214_award_logic.js：CONST_NAMES（L53–54）刪 `"TEXTFIX57_KEY_RENAME"` 一項。

### 測試 resync（8 檔，純行數漂移，v322 前例）
- 本票 index.html 淨 −9 行（刪除區間舊 L14401–14487），8 檔釘行測試即 FAIL；逐個直接跑證實全部係真漂移，唔係回歸。difflib 核實：新舊 index.html 除刪除區間外逐字相同，其後錨點一律 −9。
- 腳本 `qa323/resync323.py`（單次掃描 dict 查表，唔用逐對 re.sub；精確錨點＋次數斷言＋新行內容核實）：gift185（總行數鏈 ＋v323 −9，47290→47281）、tang171／tang173（總行數鏈＋openLoc DEF 42499→42490、lines[42498]→[42489]）、tang152（lines() 索引 14708→14699、14835→14826）、text125（b.text 釘行 16350→16341）、rom159（25466→25457、26314→26305、14783→14774、26215→26206、全佳 25494→25485；8241／10699 唔郁）、rom176（14781→14772、40731→40722、41081→41072、42384→42375、42540→42531；6321 唔郁）、travel114（COUNT 12／FREE 30／DEF 42499→42490／WRAPPER 29108→29099；其餘 10 處 FREE 唔郁）。ok() 名入面嘅 L 號係歷史標籤，一律唔郁。
- 8 檔 resync 後逐個直接跑全部 PASS；全套 suite 見 §5。

### 已核實唔使改嘅測試（開工前逐項對過）
- test_r295_click_not_gam.js（TEXTFIX57_EXACT 仍有定義，eval 唔受影響）、test_text108_static.py:85（S-42 釘長 key「訓練解鎖試鏡；打聽免費…」唔喺 html，刪短 key 唔衝突）、test_tang152_static.py（TEXTFIX55 #2）、test_weave46_static.py:57–59、test_story_gate113_static.py:26、test_gig229_v251_c.js、test_weave410_static.py:33、test_awards62_logic.js（'動作演員' 只係 fixture 輸入值）、test_weave46_logic.js、test_weave48_logic.js（castingTags fixture 輸入值，walk 後留原值正合預期）。
- qa149/pristine_index.html 係歷史快照，唔郁。

## §2 驗收
- 直接跑三檔改動測試：test_terms57_logic.js ALL PASS、test_terms57_static.py ALL PASS、test_newspaper214_award_logic.js 42/42 passed。
- node --check 過（兩檔 JS）＋ python -m py_compile 過（static.py）。
- `grep -c '"身手好"' index.html` = 2（L6825／L6836 live 閘）；`grep "解鎖" content/events_zh_HK.json` = 0；`grep -c TEXTFIX57_KEY_RENAME index.html` = 0；`grep -c nk57 index.html` = 0。
- 全套 suite：見 §5（基線 385／9）。

## §3 殘留
- WEAK_MARKS（L27968）係死常數，呢票唔郁，另開票。
- v20a57 區頭註解已改；NOTES_V20A57_TERMS.md 歷史文件唔郁。
- 「身手好」L28822 係 regex `/動作|tag_action|身手好/` 入面嘅無引號出現，唔計入 `"身手好"` 兩處；嗰行係 tag 檢測，唔郁。

## §4 出貨
- 工作副本：linji-work323（clone 式），分支 v323。
- 合併：常駐 clone `git fetch`＋`git merge --squash FETCH_HEAD`，見 §5。

## §5 落地實際數（待填）
- 內容 commit：
- main HEAD：
- suite：
- Pages md5／bytes：
- 工作副本已刪：
