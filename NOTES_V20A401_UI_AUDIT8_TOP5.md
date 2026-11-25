# NOTES_V20A401_UI_AUDIT8_TOP5

第八輪 UI 檢視頭五項（用戶 2026-11-24 16:01 下令「直到 GPT 覺得全部畫面 A 級先停下來畀我睇」；
檢視報告 `~/workspace/linji-ui-audit-2026-11-24g/REPORT.md` §四，GPT A 0／B 4／C 186，190 張截圖係 v399）。
基線 v400（main `dcae7a1`，suite 424 PASS／9 FAIL）。

## 改動一覽（只做頭五項）

### 1. 黑幕＋底部大卡 modal 語言 → 場景實物紙卡（共用 `scenePaper401`）
- `modal(html, buttons, opts)` 新 opt `scenePaper401`：mask 同時掛 `scene398`（漸變 dim
頂.10／底.42，唔再純黑 `rgba(0,0,0,.72)`）＋ `scene-paper401`；`closeModal()` 清走；
`setUnderlyingInert(true, …)` 同樣留場景。`keepScene397` 觸發不變。
- v401 CSS（`</style>` 前集中區塊）：`#mask.scene-paper401.modal`——8px 細圓角、幼墨線邊
`#a98d4f`、米紙漸變底 `#fbf4dd→#f3e6c8`、深紙影、頂部膠紙貼（`::before` 72×12px 半透明紙帶）；
`#modal-btns` 透明底、去頂邊分隔線；主掣啞面票籤（實色啞金 `#d8c49a` 深色字、無漸變無 inset
高光），次掣素紙（`#fbf4dd` 幼墨線邊）。紙卡同時滿足 tut_04（「開始寫手帳」唯一實色頁籤、
何生選項素紙吊牌）同 46（唔用金光催人揀付費）嘅 GPT 要求。
- 套用點（只限名單）：43b 等消息卡（keepScene397 隔籬加）、43d 獲聘 ×3 呼叫點（grant229 即派、
試鏡公佈無 gig 分支、有 gig 分支）、43f 落選、43e 首次落選教學卡（`presentAudFailSettlement`；
另加 `#mask.tut-on.scene-paper401` 覆寫 tut-on 背景）、46 醫院 offer ×2（有錢／唔夠錢）、
46b 醫院確認（`confirmChoice236` 加 passthrough，只由醫院呼叫點傳入，其他確認 modal 唔受影響）、
46d 病假日結（`afterDayModal` 加 passthrough，只由病假 resolver 兩處呼叫點傳入；
45／45c 同一病假路徑一併得同一紙殼，內容數字唔郁）、B01 教學完結卡（`showB01HomeModal`）。
其他 modal（通告詳情、確認 modal 等）唔掛，一律唔郁。
- **限度**：無新插畫資產——實物感靠場景 dim（背後地圖／屋企透出）＋現有支票（43d 已有）＋紙品殼語言；
GPT 想要嘅電話聽筒／探熱針插畫唔喺今票範圍。43e 係 `.tut-card`，窄紙條規則（14px）specificity
高過紙卡 8px，佢保留 14px 窄紙條＋場景 dim，屬教學卡家族，唔係漏改。

### 2. 教學遮罩：挖空＋頂欄同步降亮＋卡邊背景字＋窄紙條
- `#mask.tut-on` 改全幅均勻 dim `rgba(0,0,0,.78)`（頂欄同步降亮，唔再留頂欄光，取代舊漸變）。
- `refreshTutSpotlight398()` 定位金圈之後，用 ring rect vs mask rect 計 `--tut-hole-x/y/r` 寫入 #mask
＋掛 `tut-hole401`；CSS 用 radial-gradient 挖空圈內（6px 羽化邊）。唔係 TUT_MAP／教學完咗就清走
（`!on` 分支＋`setTutMask(false)` 兩處）。實測挖空中心 (91.3, 288.7) 同金圈中心完全重合，半徑 42px。
金圈本身一字唔郁（置中、浮貼空隙 5.8px、撞圈標籤 hidden、離開即還原）。
- 教學期間隱去地圖提示列／圖例：`#app.tut-stage397.map-hint,.map-legend{ display:none}`
（`tut-stage397` 已由 `setTutMask` 開關，離開即還原）。tut_03 底部日卡半截字靠窄卡＋實駕核實，
實測三步 `clipped: []`，唔使再加隱藏。
- 教學卡改窄紙條：`#mask.tut-on.modal:has(.tut-card)` 收窄到 `min(330px, calc(100% - 32px))`
（實測 modal 326px），米紙底＋幼邊＋紙影；掣列改 row 右對齊、透明底無分隔線；「下一步」做右下頁籤
（自動闊、40px 高、降飽和啞金 `#d8c49a`、order 2）；「跳過教學」／replay 降為卡內次要文字掣
（透明底、無邊、底線細字、order 1／3）。`--tut-shell-bottom` 量度 code 留低唔刪（變死碼但無害）。

### 3. 「繼續」掣字疊影：共用金掣改實色
- L993 共用 `button.p` 規則：背景漸變 `#E6D2A8→#C9A227` → 實色 `#C9A227`；`box-shadow` 刪走
`inset 0 1px 0 rgba(242,235,216,.55)` 高光（留 `0 2px 0 #6B5340` 底邊）；加 `text-shadow:none`；
字色維持 `var(--ink)` #1A1410。**事前 grep 證實**：全檔無任何 `text-shadow`／`text-stroke`／
`drop-shadow` 落喺 button／modal 掣度——重影根源係漸變＋inset 高光造成嘅浮雕觀感，唔係字陰影；
今次一次過清走晒三個候選元兇（漸變／高光／陰影）。
- 實測：43b「繼續」放大圖字乾淨無疊影；對比度 #1A1410 對 #C9A227 ＝ **7.54:1**（紙卡內 #D8C49A ＝
**10.67:1**），≥4.5:1。紙卡內正文對紙底：h3 15.5／13.78、內文 11.98／10.64、金字 5.39／4.79。
- 注意：審計 probe 嘅 CONTRAST_JS 只讀 `backgroundColor`，漸變底（透明色）會一路行到深色 body，
計出 1.08–2.71 假低值——上面數字係對住實際紙漸變兩端逐項重計，唔係 probe 原數。

### 4. 35c P2：加分歸屬＋主標對調＋小檔案旁註
- Dual 行兩處（`renderPostShootRewardHtml`、`renderAwardResultHtml`）改逐項組裝：有值先列、無值省略、
` · ` 連接。雙值輸出同舊版逐字相同（`幕前聲望 +1 · 業內信用 +2`，舊測試 b7 照舊通過）；
單值嗰陣只出有值嗰項（實駕 P2 單值出「業內信用 +1」）；零值成行唔出。寫 inline，唔叫外援——
測試獨立 eval 抽函數。
- 主標對調（只限入圍＋他人奪獎嗰案，即 P2 相係陳偉翔、主標寫錯人嗰案）：新 `metricHead401`＝
「陳偉翔散場」，奪獎行降做小標（新 `<p class="np214-subhead401">`，次級大細深棕粗體），lead
唔再以奪獎行開頭（保留「散場報道的觀察對象」字串）。**玩家奪獎／旁聽沿用舊主標**：玩家奪獎嗰陣
`win149` 係 null（winner63 係 null，得主就係玩家）、P2 根本冇相，主標本身就係玩家，唔存在錯配；
旁聽冇代表作（`rep214` 空），同樣沿用。舊測試 c1–c3（winLine 字串在位）照舊通過——小標保留字串。
- 小檔案改剪報旁註（CSS only，限 `.awd-result396`，晨報渲染器唔郁）：去框、虛線頂線、細字 12.8px、
旁註體。橫額同右欄一字唔郁。

### 5. 通告欄：整理選單索引紙＋詳情合約紙
- 整理選單：保留 v399 釘死嘅三條原規則唔郁，後加覆寫做側邊紙籤拉出嘅小型索引紙——紙底漸變＋微斜
−0.6°＋紙影；選項改文字行（透明底、無邊、無圓角，唔再係等寬膠囊掣）；選中加紅筆剔號
（`::before` 紅框＋`::after "✓"` 紅色 #B3261E）。DOM／class／`data-sort392`／`data-filter392` 一字唔郁。
- 詳情頁：片酬／簽約金／違約金三行包入 `.cn-contract401` 合約紙（行本身 `.cn-sum-row` 唔變）＋
紅色「合約」印章；`.board-calc397` 預期日薪算式改手寫式計算備註（`--hand363` LXGW WenKai、細字、
次要色、左側虛線）；詳情紙加底 padding 28px（同舊 L5716 規則同級 specificity 後出先贏），
確保已公布陣容最後一行可完整捲出。分層同計法一字唔郁。

## 邊界
- 唔做（下一批）：21_debt、07c／05b／07b、33、11c、88、08b 紅字、43d 綠字／支票「簽約金」掂底線、
24_menu、掣量背景卸載八項。唔改 SAVE key（`starVolunteer_map_v19w`）／softRev／產品 `?v=`。
唔改任何規則數字。唔改主線／結局／頒獎贏線。

## 實裝
- `index.html` 淨 +192 行（51369→51561）。CSS 集中區塊喺 `</style>` 前（v401 註解）；L993 金掣規則
改實色；`modal()`／`closeModal()` 加 `scenePaper401`；呼叫點加 opt（43b／43d×3／43e／43f、
46×2／46b passthrough／46d 病假路徑×2／B01）；`refreshTutSpotlight398()` 加挖空變數＋清除路徑；
35c dual 組裝＋主標／小標＋lead；詳情合約紙包裝。
- 新測試：`tests/test_v401_logic.js`（16 項）＋`tests/test_v401_static.py`（43 項）——兩份 exit 0。
另修過一個測試本身嘅 bug：玩家奪獎 e 組最初假設主標一樣對調，實測 `win149` null＋P2 無相，
證明嗰案唔存在錯配，改斷言做「沿用舊主標」。
- Resync：`qa401/resync401.py`（OLD＝v400 main `dcae7a1`，difflib 映射，內容逐字核實純漂移）——
travel114 FREE 44／COUNT 13／DEF 46159→46334／WRAPPER 32284→32443；rom159 6 釘＋全佳行；
rom176 6 釘；tang152 兩釘；text125 三錨點；gift185／tang171／tang173 總行數 51369→51561、
openLoc DEF 46159→46334、tang173 lines[5389]→[5393]（8 處）。
- 四個舊逐字釘因有意圖改動而更新（意圖保留，見各檔 v401 註記）：`test_v391_ui_static.py`
（金漸變→實色金，改釘 `background:#C9A227`）；`test_v397_static.py`（`setUnderlyingInert` 加
scene401 或項）；`test_v398_static.py`（scene398 toggle 加 scene401 或項）；
`test_v399_static.py`（43b 加 scenePaper401 opt；refresh `!on` 分支加清挖空）。
- 實駕：`qa401/drive401.py`（手法照抄第八輪審計 probe；證據 `~/workspace/linji-drive401/`——
`phone401.json`／`hosp401.json`／`tut401.json`／`awards401.json`／`board401.json`＋截圖）。

## 測試
- 全套 suite：**TOTAL PASS 426 FAIL 9**（`~/workspace/suite401b.txt`，重跑確認；基線 424／9，
  +2 係 v401 兩份新測試全過，9 項 FAIL 同基線逐項相同：flash51／slot50／soft_tip_111_restore／
  start53／weave43／weave44／weave49／wf5_87／wrap38——全部 pre-existing，零新 FAIL）。
  第一次跑 422／13——4 項新 FAIL 全部係上述舊逐字釘，修好後重跑已消除。
- 實駕覆驗（五項，全部通過）：
① 電話／醫院／教學完結卡：mask 全部 `scene398 scene-paper401`、漸變 dim、modal 8px 紙卡＋膠紙貼；
43b／43d／43e／43f／46／46b／46c／46d／B01 全部截圖核實（43e 係 tut-card，14px 窄紙條＋場景 dim）。
② 教學：遮罩全幅均勻 `rgba(0,0,0,.78)`（頂欄同步降亮）；step1 挖空中心同金圈中心完全重合
(91.3, 288.7) r=42px，圈內大樓光猛、其餘均勻暗；hint／legend `display:none`，三步 `clipped: []`；
卡闊 326px；「下一步」80×40 右下頁籤、「跳過教學」64×40 文字鏈。
③ 「繼續」掣字：放大圖無疊影；`text-shadow:none`、底 `none`（實色）、對比度 10.67:1（紙卡內）
／7.54:1（L993 實色金）。
④ 35c P2：主標「陳偉翔散場」、小標「彭少祺憑《冬暖》奪獎」、lead 無奪獎行前綴、
dual 單值「業內信用 +1」、小檔案虛線頂線＋透明底＋12.8px；捲到底 dual 行＋小檔案完整可見。
⑤ 通告欄：整理選單紙底＋微斜、選項文字行、選中紅 ✓（預期日薪／全部）；詳情合約紙三行
（片酬 $378／簽約金約 $113／違約金 $200）＋紅「合約」印章；算式 LXGW WenKai 手寫；
陣容尾行「女配角江詩盈」完整捲出（`lastFullyVisible: true`）。

## 遺留／下一批
- 43d 支票「簽約金」掂底線＋綠字 4.42（下一批，唔喺今票範圍）。
- 35c P2 相片用 `cropbanner` aspect-ratio——實駕證實無裁頭（之前一張圖係 modal 捲到底嘅假象），唔使修。
- 審計 CONTRAST_JS 漸變盲點（見 §3）：漸變底卡嘅正文對比度要用實際紙色重計，唔好信 probe 原數。
