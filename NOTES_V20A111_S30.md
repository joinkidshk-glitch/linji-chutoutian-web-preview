# v20a111 S-30v2 通告詳情實物化・套用上線

> 用戶 2026-11-12 06:59 拍板「用 v2，套用」。Base：main `0bb85b2`（v20a109 B）；
> 收尾前 main 推進到 `8e9e773`（v20a109 NOTES＋合併證據，零 code 改動），分支已 rebase
> 上去，無衝突。分支 `v111-s30`，squash 入 main。
> 紀律：SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全冇郁；
> content JSON 一律唔改；數值／機制零改動（只改呈現：`castingNoticeDetailHtml` 模板＋
> `gigCastPeriodLine`／`gigCastDeadlineText30v2`＋本範圍 CSS）。

## 1. 改動

### 1a. 負責人對照表填滿（`GIG_ISSUER_FIGURE_MAP30V2`，key＝`g.loc`）

卡上人物＝發通告機構嘅老闆，唔係主角／主演、唔係導演／製片。11 間機構老闆全部係
為本遊戲新創作嘅虛構人物（玩家面永禁真藝名），全身立繪按 v106 生產規格出
（風格錨、成張重生、焗米白邊、QC 分級），入庫 `assets/story/fullbody/boss_<loc>_base.webp`：

| loc | 機構 | 老闆 | 職位 |
|---|---|---|---|
| tvb_longmen | 星河電視台 | 沈卓衡 | 台長 |
| film_lion | 獅子山製片 | 羅勁威 | 老闆 |
| ad_adm | 金鐘創意 | 方樂怡 | 老闆 |
| ad_central | 中環廣告 | 霍君豪 | 老闆 |
| rec_hk | 香江唱片 | 伍兆昌 | 老闆 |
| tvb_kowloon | 九龍電視台 | 陶映紅 | 台長 |
| film_cotton | 紅棉影業 | 鄭伯康 | 老闆 |
| rec_wanchai | 灣仔唱片 | 梁廣成 | 老闆 |
| tvb_harbour | 海港廣播 | 顧學禮 | 台長 |
| film_harbour | 維港電影 | 夏文心 | 老闆 |
| rec_star | 天星音樂 | 溫子峰 | 老闆 |

- 名牌顯示「老闆名／機構 · 職位」（例：沈卓衡／星河電視台 · 台長）。
- 後備規則不變：對照表 → 何生（何生事務所 · 你的經理人）→ 阿偉／主演永不頂替 →
  圖缺失英雄區成區隱藏，只出卡。全庫 149 張通告嘅 loc 全部喺 11 間之內；
  未映射 loc（合成測試 `cafe_cha`）已驗證行何生後備。
- 圖檔 QC：10 pass、1 marginal——**溫子峰面相偏後生**（睇落廿歲頭，唔似 33 歲老闆），
  收 marginal 唔重擲，留待用戶睇樣後決定係咪重擲。

### 1b. 通告期間拆行（只限詳情頁；用戶 06:47 指住實機圖提出）

改前：`通告期間 1990年冬季檔 · 獲聘後 10 日內完成 · 約 1 個工作天`——三個概念串埋
一行，「約 1 個工作天」會喺短語中間斷行，兼同上面「通告日數：共 1 天」重複。
改後（`gigCastPeriodLine` 只留季節／檔期窗；新 helper `gigCastDeadlineText30v2`）：

| 行 | 改前 | 改後 |
|---|---|---|
| 通告期間 | `1990年冬季檔 · 獲聘後 10 日內完成 · 約 1 個工作天` | `1990年冬季檔` |
| 完成期限（新行） | — | `獲聘後 10 日內` |
| 底部 `notice_period_bar` | 同上串埋一行 | 拆做期間＋期限兩行 |

- 「約 N 個工作天」刪走（通告日數行已有同一數字）。
- 有 `castWindow` 嘅通告保留原有 `startHint ～ endHint` 範圍寫法；冇 season
  （不限／全年）照出「1990年通告檔」；冇 ddl 嗰陣期限行成行隱藏，唔留空行。
  註：`effectiveShootDeadlineDays` 有 fallback（`max(14, d*3)`），真實 149 張通告
  全部有 `shootDeadlineDays`，隱藏分支係防禦性質（空 gig 實測回「獲聘後 14 日內」）。
- 短語唔准中間斷開：`notice_period_bar` 加 `word-break:keep-all`（限
  `cn-paper30v2` 範圍；摘要 `.v` 上版已有 keep-all）。
- **唔郁通告欄卡片 meta 行**（`gigBoardTeaserHtml`，約 33905–33931 行，卡片 meta
  入面嘅「獲聘後 N 日內完成」）——留返跟進，見 §5。

## 2. Patch

- 製造器＋demo 包：`~/workspace/linji-work108c/qa108c/s30v2/`（`make_patch_v2.py`、
  `s30v2_physicalisation.patch`、`demo_s30v2.html`、`NOTES.md`）。
- Patch：`index.html` 231 行、6 hunk、+143／−13；由乾淨 main `0bb85b2` 生成。
- `git apply --check`（乾淨 main 副本）PASS；`node --check`（抽 inline script）通過。

## 3. 測試

- 新守門：`tests/test_s30v2upd_logic.js`（37 項：期間／期限拆行邊界、11 間對照表、
  何生後備、11 張 boss 圖＋何生圖入庫）——全部 PASS；pristine 反證：
  更新後嘅 `test_dlg107_static.py` 喺 pristine 必須 FAIL（96≠107）。
- 全套 A/B（`qa111/run_suite.py`）：基線 pristine main `0bb85b2` ＝ **146 PASS／12 FAIL**；
  工作版 ＝ **147 PASS／12 FAIL**，FAIL 清單逐字相同（12 個已知環境性 static FAIL：
  flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／
  weave43／weave44／weave49／wrap38）。**零新增回歸**；+1＝新守門測試。
- 舊斷言更新（附反證，唔係放寬）：`test_dlg107_static.py` fullbody 總數 96→107
  （v111 加 11 張 boss 圖）；`test_dlg108_static.py`／`test_dlg109_height_static.py`
  真檔重測排除 `boss_*`（通告負責人立繪唔係對話舞台角色，唔入配對／身高重測；
  對話資產數維持 96，配對統計回復原值）；`test_ui108_static.py` S-33 視窗
  7000→11000（`castingNoticeDetailHtml` 由 ~6.9k 漲到 9750 字元）。

## 4. 實駕驗收（390×844，Playwright，`~/workspace/linji-work108c/qa108c/s30v2/`）

| 截圖 | 內容 | 結果 |
|---|---|---|
| `live_v111_boss_shot.png`／`live_v111_boss_expand_shot.png` | 《賀歲特輯》沈卓衡企卡頂，摺疊＋展開 | 0 pageerror |
| `live_v111_cinema_shot.png` | 《戲院人潮》夏文心企卡頂（改前係何生） | 0 pageerror |
| `live_v111_fallback_shot.png` | 合成通告 loc `cafe_cha` → 何生後備 | 0 pageerror |
| `live_v2_period_before_shot.png`／`live_v2_period_before_expand_shot.png` | 改前對照（舊 patch，期間行三合一） | 0 pageerror |

- 每行一個概念、無重複、無短語中間斷行、無空行殘留；摺疊態卡身零捲動維持；
  期間行／期限行、底部兩行 bar 全部睇得清（見 `live_v111_*_metrics.json`）。
- 舊檔相容（`drive_compat111.py`，槽 3）：pristine main 存檔（money 111111／dayIndex 3／
  mark `v111-slot3`）喺 v111 版完整還原，PASS，0 pageerror。

## 6. 上線核實（合併後）

- main commit：`3d20b58`（分支 `v111-s30` squash 入 main；分支本身亦已推上 origin 備查）。
- 線上核實（GitHub Pages，推送後即時對版，無部署延遲）：`index.html` 5,088,978 bytes、
  sha256 `83737185a0f3176abda874eeb99d665f3e5d21035510108c732ba0ee82de66ad`，同本地合併版
  逐 byte 一致；抽查 boss 圖三張（`boss_tvb_longmen_base`／`boss_film_harbour_base`／
  `boss_rec_star_base`，帶 `?v=20a106`）全部 HTTP 200＋sha 同本地一致；何生圖 HTTP 200。

## 5. 殘留／跟進（唔入今包）

1. **通告欄卡片 meta 未修**：卡片 meta 行仍係「酬勞 · 約 N 日 · 獲聘後 N 日內完成」
   串埋一行（`gigBoardTeaserHtml`）。留返跟進一票。
2. **溫子峰圖 marginal**：面相偏後生（見 §1a）。等用戶睇樣後決定係咪重擲。
3. 主 script 包喺 IIFE 入面，遊戲函數唔係全域——實駕一律行 UI 撳入，唔好用
   `evaluate` 直開（舊 `drive_verify.py` 嘅 `var04` 模式實質係 no-op；
   新版 `drive_verify_v2upd.py` 改行通告欄路線，fallback 用改 loc 再撳卡）。
4. `qa109b/shots/` 兩張 PNG 喺基線套件運行期間被平行工作改動過，今包唔入；
   已還原到 HEAD（可再生 artifact）。
