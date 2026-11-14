# NOTES_V20A205 — 藍若曦全身圖跟新造型 v7 重出（6 張）

## §0 摘要

- 目的：藍若曦遊戲內 6 張全身圖跟用戶 2026-11-14 13:45 拍板嘅新造型 v7 重出。只做實裝＋驗證，**唔落地**（落地另行安排）。
- 範圍：淨係 `assets/story/fullbody/lan_ruoxi_*.webp`（6 檔，同檔名覆蓋）＋呢份 NOTES。**冇改任何 code**（loader 動態路徑搵到新檔即用）。
- 分支：`v20a205`（基底 main `3768c90`＝v203）。唔郁 `assets/story/awards/px_lan_ruoxi_*.png`（等 grokbot 新 character，v204 分支嗰邊處理）、唔郁 grokbot 設計包。

## §1 設計來源（定稿，唔准改）

- 新造型 v7 設計圖：`~/workspace/linji-work204/grok-characters/designs/lan_ruoxi_design.png`
  - sha256 `7f8587734988c7835a4599c8aba157943f3f773158822a7c801b3cb246a8bd92`（已核實）
  - 高馬尾＋黃色蝴蝶結、鵝黃色針織上衣＋白色百褶短裙＋白襪＋波鞋、修長身形（腳長、頭身比例細）、陽光杏眼（普通圓形光點，**絕對冇星形閃光**）、開懷露齒笑。
- 風格參照：`~/workspace/linji-native-design/style-anchor-awei-anime.jpg`（乾淨二次元動畫風）＋舊設計 `~/workspace/linji-work204/designs-v1-superseded/lan_ruoxi_design_v1.png`（**只參考畫風，唔抄舊造型**：舊係及腰長直髮＋白蕾絲長裙）。
- 新造型同舊造型最大分別：高馬尾（舊：及腰長直髮）、短百褶裙＋露腿（舊：長裙）、黃色上衣（舊：白裙）。

## §2 六張圖清單

全部 WebP q90，同檔名覆蓋，尺寸／取景跟返現有嗰套（人物填滿成格、腳底貼底邊，同原檔一致）。

| 檔 | 尺寸 | bytes | sha256（頭 16） | 表情 |
|---|---|---|---|---|
| `lan_ruoxi_base.webp` | 792×2448 | 193,894 | `9ecf648e37991d82…` | 開懷露齒笑（＝設計圖嗰個） |
| `lan_ruoxi_sad.webp` | 762×2350 | 190,848 | `1dd25bf589ea8224…` | 眼濕濕、嘴角向下 |
| `lan_ruoxi_serious.webp` | 763×2352 | 190,802 | `9157a11ec2f98899…` | 直嘴、專注眼 |
| `lan_ruoxi_shy.webp` | 764×2352 | 191,344 | `a72b1b1cac0c1e21…` | 面紅、眼斜望、細笑 |
| `lan_ruoxi_smile.webp` | 764×2353 | 189,586 | `a4b2e14649c09040…` | 溫柔合嘴微笑（同 base 開懷笑分得清） |
| `lan_ruoxi_think.webp` | 757×2349 | 191,376 | `e2a720c5d100accb…` | 眼望上側、沉思 |

- 6 張衫／髮／塊面／身形全部一致，只改表情，每個表情一眼讀得出。
- 完整 sha256 見 §6。

## §3 生成＋後製方法

### 生成（media 管線）
- 先出 tall master（base，864×2688）：用高版舊設計 v1（792×2448）做 canvas、v7 設計圖做參照重畫（media 工具編輯高圖會保留高比例）。
- 其餘 5 個表情由 tall master 編輯，只改表情。
- 來源 PNG（工作副本 `work205_gen/`，唔入 repo；hash 見 §6）：
  - master `e7c0388e07536c492879908a27109614718aa9096c0b8eacb352453759c29da1`
  - sad `df9b24319d2ff5d56aaab1a63e52900e8beee9127e3c2f3fecbe1745f58a80a0`
  - serious `61db844b8e2aab8c5d8c027f70ed8e87a5c36a1b710bbe1f9f91e8a06e8f7ea5`
  - shy `59172acd31fa199556eda67af0a0c37a09f63421ecc31511c0e1b6a1cf01abd0`
  - smile `78a56e47e5383f0c3d3ed84d7778727d218996ca2df4e53450c654902f8157ca`
  - think `897fb87f0c8c6a9a44635fa9ff2ba1882d52bca8b647337f2b78b774e612a02b`

### 後製（`work205_gen/process205.py`，v4，工作副本內）
生成圖係 RGB 實色淡底，原檔係 RGBA 透明底，必須去背＋逐檔 resize 到前任尺寸。v4 做法：
1. **Outline-barrier flood fill 去背**：人物用深色線勾邊，攞線做屏障；背景＝同邊界相連嘅非屏障區。唔用顏色距離做主判斷——因為白裙同淡底撞色（裙 dist ~3–5，幾乎同背景一樣）。
2. **Tight crop**：按人物 bbox 裁到目標長闊比再 resize，人物填滿成格、腳底貼底邊（跟原檔取景）。
3. **1.5px Gaussian 羽化**，WebP q90。
- **v1／v2 失敗教訓**：全域顏色距離（`dist < 12`）食咗白裙／白波鞋，透明 0.63／不透明 0.29（原檔約 0.44／0.52）；v2 只吸圍封淡底窿都唔得，因為裙下半本身就同背景連埋一齊。結論：**白衫人物去背唔可以用顏色，要用線做屏障**。
- v3（barrier，未 crop）：裙保住咗，但人物喺格入面偏細（腳底離底邊 41px，不透明 0.39）。v4 加 tight crop 後腳底貼底邊（bbox rows 0–2447）。

## §4 驗證結果

### 目視（逐張）
- 灰底＋深底 contact sheet：6 張人物完整，冇背景殘留、冇食咗嘅部位、冇光暈硬邊（深底見薄米白光邊，同原檔焗邊效果一致）。
- 塊面放大（base／think／shy）：陽光杏眼係普通圓形光點，**零星光**；零文字；畫風跟原本嗰套（柔和幼線、淡色）。
- 表情分明：base 開懷笑／sad 眼濕濕／serious 直嘴／shy 面紅斜望／smile 合嘴微笑／think 望上沉思。
- 新造型齊：高馬尾＋黃蝴蝶結、鵝黃針織上衣、白百褶短裙、白襪＋波鞋、修長身形。

### Alpha 數字（6 檔）
| 檔 | 透明 | 不透明 | 角落 alpha | 裙區 alpha 均值 |
|---|---|---|---|---|
| base | 0.5196 | 0.4237 | 0 | 241.0 |
| sad | 0.5156 | 0.4280 | 0 | 243.2 |
| serious | 0.5145 | 0.4298 | 0 | 243.7 |
| shy | 0.5206 | 0.4235 | 0 | 244.7 |
| smile | 0.5166 | 0.4286 | 0 | 243.7 |
| think | 0.5097 | 0.4338 | 0 | 244.9 |

- 註：不透明 0.42–0.43 低過原檔 base 組 0.52／serious 組 0.64，**唔係去背食圖**——係新造型本身露腿＋短裙＋高馬尾（舊係長裙＋及腰長髮，實色面積本身大啲）。裙區 alpha 均值 241–245（裙實色，僅 5–7% 像素 <250，係裙側邊緣／褶影），人物 bbox 填滿成格（rows 0–2447、cols 40–780），證實冇食圖。
- 原檔對照：base 透明 0.4396／不透明 0.5236；serious 透明 0.3176／不透明 0.6449（原檔兩組本身都有差異）。

### Loader 引用（grep `lan_ruoxi`，index.html）
- L26602 角色表 `"lan_ruoxi"`、L27177 身高比 1.00、L27321 名對照 藍若曦→lan_ruoxi、L27352 `lan_ruoxi: { artId:"char_lan" … }`、L54798 `PORTRAITS.npc_lan = "assets/story/fullbody/lan_ruoxi_base.webp?v=20a176"`。
- L26468 動態路徑 `assets/story/fullbody/{stem}_{expr}.(webp|png)?v=20a106`——6 個檔同檔名覆蓋即搵到，唔使改 code。

### 測試（30 項，全綠）
- 核心 8 項：`test_dlg126_logic.js`／`test_dlg127_logic.js`／`test_rom176_logic.js`／`test_dlg106_logic.js`／`test_dlg109_height_logic.js`（RESULT/ALL PASS）＋`test_dlg126_static.py`／`test_dlg127_static.py`（焗邊尺寸＝原圖+2r，PASS）＋`test_bust109_static.py`（FAILURES: 0）。
- 追加 22 項（全部有提及 fullbody／lan_ruoxi 嘅測試）：`test_cleanup100_static`、`test_weave46_static`、`test_dlg106_static`、`test_dlg107_logic/static`、`test_dlg108_static`、`test_dlg109_height_static`、`test_dlg119_logic/static`、`test_dlg123_logic/static`、`test_dlg138_logic/static`、`test_awei195_static`、`test_awei199_static`、`test_awei201_static`、`test_locpanel118_static`、`test_ui108_static`、`test_ui131b1_static`、`test_wf4dlg108_logic/static`、`test_s30v2upd_logic`——全部 PASS／ALL PASS／FAILURES: 0。
- 註：`test_dlg108_static` 跑嗰陣重寫 `qa108d/remeasure108d.json`（184 張重測），寫入後同 HEAD 一致，工作區冇多餘改動。

## §5 唔做／唔郁

- 唔郁 `assets/story/awards/px_lan_ruoxi_*.png`（v204 分支，grokbot 新 character 嗰邊換）。
- 唔郁 grokbot 設計包（`~/workspace/linji-work204/grok-characters-v204-v7.zip` 等）。
- 唔改任何 code；唔落地（等另行安排；落地嗰陣工作副本即刪，見磁碟紀律）。
- 生成中間檔（6 張 864×2688 PNG＋`process205.py`）留喺工作副本 `work205_gen/`，唔入 repo；hash 見 §3／§6。

## §6 完整 sha256

設計圖：`7f8587734988c7835a4599c8aba157943f3f773158822a7c801b3cb246a8bd92`

```
9ecf648e37991d82a01d3056d094123349d21510317c48fb05730351e43f7c24  lan_ruoxi_base.webp
1dd25bf589ea8224f3a79e83234815dc32cdfc03e3d1b7d8adb1a69654e565c5  lan_ruoxi_sad.webp
9157a11ec2f988991f609d48f947679288db67835c69d1c135b4bbc044489ee4  lan_ruoxi_serious.webp
a72b1b1cac0c1e219b0b2d6bcebcc8f690836f6028f347abb7949d109288b042  lan_ruoxi_shy.webp
a4b2e14649c090405c6aee102dc1bfd72445fc066c0da4e90fc88d8715d3f679  lan_ruoxi_smile.webp
e2a720c5d100accbea09a3c0d52b208b9b2a02cf4ebfa7760844e6fbd2a45d22  lan_ruoxi_think.webp
```

## §7 落地前重驗（落地統籌，2026-11-14）

- **Rebase**：基底 `3768c90`（v203）→ `9e338d6`（v204 已落地），乾淨，零衝突；分支新 HEAD 待 commit。6 張 webp hash 同 §6 一致，rebase 前後不變。
- **相關測試 30 項重跑，全綠**：JS 11 項（dlg126／127／rom176／dlg106／dlg109_height／dlg107／119／123／138 logic、wf4dlg108、s30v2upd）＋static 19 項（dlg126／127／bust109／cleanup100／weave46／dlg106／107／108／109_height／119／123／138／awei195／199／201／locpanel118／ui108／ui131b1／wf4dlg108 static）。
- **全套 A/B**：工作版 **287／13**、pristine（main `9e338d6` detached worktree）**287／13**；work-only／pristine-only FAIL 皆空，**零回歸**。13 項 FAIL 全部係已知 pre-existing static（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／44／49／wf5_87／wrap38），同 v204 基線逐項一致。
- **實駕（本地鏡像＋Playwright，`StoryPlay.start(id,{force:true})` 播晒 5 節 R_lan_*）**：舞台出現新造型，base／smile／sad／think／shy 5 個表情逐張截圖核實分得清（`linji-design-review-v205/shots/lan_{base,smile,sad,think,shy}_*.png`）；6 檔 HTTP 全部 200，零 `lan_ruoxi` 404。**serious 冇喺舞台出現**：全遊戲 86 節 probe 過，藍若曦對白冇一句 resolve 到 serious（base 9／sad 2／shy 3／smile 1／think 1 句）；serious 檔本身齊（HTTP 200，candidate chain 入面有，缺圖會優雅退 base）——係內容現況，唔係 v205 缺陷（舊檔時代都一樣，v205 冇改 code／冇改對白）。
- **附帶觀察（pre-existing，唔係 v205 回歸）**：R_lan_* 5 節嘅 artId 圖（`rom_lan_meet/push1/push2/crisis/ending`）喺 repo 入面唔存在，引擎試咗多個路徑 404 後退返素色舞台底。v205 只掂 6 張 webp＋NOTES，呢啲檔喺 main 一樣唔存在；舞台本身運作正常。

## §8 落地紀錄

- 遊戲 commit `1cf324e`（squash merge `v20a205`，7 檔：6 張 webp＋NOTES），已 push 上 GitHub main。
- 線上核實：index.html 5,451,440 bytes sha `ad3005f8…` 同 repo HEAD 一致（index.html 本版冇改）；新 base webp 線上 sha `9ecf648e…` 同 repo 一致，新造型已上線。
- 重驗：相關測試 30 項全綠；全套 287／13 零回歸（pristine A/B）；實駕 5 節 R_lan_*，base／smile／sad／think／shy 5 表情上台截圖核實，serious 檔齊但遊戲入面冇對白 resolve 到佢（內容現況，見 §7）。
