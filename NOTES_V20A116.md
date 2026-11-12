# v20a116 機構老闆立繪 v2/v2b 換入上線

> 用戶 2026-11-12 07:46 睇完 v2b 對照話「ok」——拍板成套換入。Base：origin/main `41e4be8`
> （v20a111，線上現行版）；合併前 origin/main 先後推進到 `2d71588`（v113＋v115＋v114）再到
> `a02f77f`（v117），分支兩次 rebase 上去，兩次都無衝突。分支 `v116-boss-swap`，squash 入 main。
> 紀律：SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全冇郁；
> `?v=20a106` 圖片版本參數維持不變（新檔名本身就係 cache-buster）；content JSON 一律唔改；
> 數值／機制零改動（只改對照表 src 指向＋入庫 11 張新圖）。

## 1. 改動

### 1a. 對照表改指新檔（`GIG_ISSUER_FIGURE_MAP30V2`，index.html 約 34579–34589 行）

| loc | 機構 | 老闆 | 新檔 |
|---|---|---|---|
| tvb_longmen | 星河電視台 | 沈卓衡（台長） | `boss_tvb_longmen_v2b_base.webp` |
| film_lion | 獅子山製片 | 羅勁威 | `boss_film_lion_v2b_base.webp` |
| ad_adm | 金鐘創意 | 方樂怡 | `boss_ad_adm_v2_base.webp` |
| ad_central | 中環廣告 | 霍君豪 | `boss_ad_central_v2_base.webp` |
| rec_hk | 香江唱片 | 伍兆昌 | `boss_rec_hk_v2_base.webp` |
| tvb_kowloon | 九龍電視台 | 陶映紅（台長） | `boss_tvb_kowloon_v2_base.webp` |
| film_cotton | 紅棉影業 | 鄭伯康 | `boss_film_cotton_v2_base.webp` |
| rec_wanchai | 灣仔唱片 | 梁廣成 | `boss_rec_wanchai_v2b_base.webp` |
| tvb_harbour | 海港廣播 | 顧學禮（台長） | `boss_tvb_harbour_v2b_base.webp` |
| film_harbour | 維港電影 | 夏文心 | `boss_film_harbour_v2_base.webp` |
| rec_star | 天星音樂 | 溫子峰 | `boss_rec_star_v2_base.webp` |

- 7 張 v2（動畫風重製）＋ 4 張 v2b（修正擲：收咗太卡通嘅表情／眼鏡／圓面）。
- v1 檔 `boss_<loc>_base.webp` 全部留喺 `assets/story/fullbody/` 做後備，唔刪除。
- 對照表上面嘅註解已更新，寫明 v116 換入＋回滾方法。
- 後備規則不變：對照表搵唔到 → 何生；阿偉／主演永不頂替；圖缺失只出卡。

### 1b. 新圖入庫（`assets/story/fullbody/`，binary 原檔，11 張）

| 檔 | bytes | sha256（首 12 位） |
|---|---|---|
| boss_ad_adm_v2_base.webp | 90,754 | ebc6ed23fa32 |
| boss_ad_central_v2_base.webp | 58,582 | 3952ec634df6 |
| boss_film_cotton_v2_base.webp | 64,750 | f7c0ce76d9a7 |
| boss_film_harbour_v2_base.webp | 57,604 | 41bc9660b26f |
| boss_film_lion_v2b_base.webp | 287,762 | 1d4bab739a6c |
| boss_rec_hk_v2_base.webp | 65,200 | c312d3eaac8e |
| boss_rec_star_v2_base.webp | 82,330 | 6f3de10c5891 |
| boss_rec_wanchai_v2b_base.webp | 218,852 | 9578205bf5be |
| boss_tvb_harbour_v2b_base.webp | 215,710 | 9808d22090a7 |
| boss_tvb_kowloon_v2_base.webp | 62,304 | 2ad704c42a34 |
| boss_tvb_longmen_v2b_base.webp | 112,628 | a07f61a785f9 |

### 1c. 測試更新

- `tests/test_s30v2upd_logic.js`：對照表期望 src 改指新檔（逐間斷言 `_v2`／`_v2b` 後綴）；
  新增守門：11 間無一指舊 v1 檔、11 張新檔全部入庫、11 張 v1 檔仍在庫（回滾後備）。
- `tests/test_dlg107_static.py`：fullbody 總數斷言 107 → **118**（v111 11 張 v1＋v116 11 張新檔；
  純計數更新，唔係回歸——新測試喺 pristine v111 index 上跑係 12 FAIL 反證，見 §3）。

## 2. 已知接受項（用戶已睇過，唔使再擲）

- 沈卓衡 v2b 偏嚴肅；羅勁威黑恤衫變圓領 Tee 剪裁（可接受變體）。
- 4 張 marginal 淡淡年齡線（羅勁威、霍君豪、陶映紅、鄭伯康），卡頂細圖唔易察覺。
- 溫子峰 v2 已解決「廿歲頭」問題（面相約 30–33 歲），舊 marginal 關閉。

## 3. 測試

- 守門 `node tests/test_s30v2upd_logic.js`：**ALL PASS**；反證：同一測試對 pristine v111
  index.html 跑係 **12 FAIL**（11 間 map src＋「無一指舊 v1」），證明守到換入。
- `tests/test_dlg107_static.py`：PASS（更新後）；inline script `node --check` PASS。
- 全套 A/B（`qa116/run_suite.py`）：舊基線 pristine origin/main `41e4be8` ＝ **147 PASS／12 FAIL**；
  工作版（未 rebase）＝ **147 PASS／12 FAIL**，零新增回歸。
- **Rebase 後覆核（第一次）**：新基線 pristine origin/main `2d71588`（v113＋v115＋v114）＝ **154 PASS／12 FAIL**；
  工作版 ＝ **154 PASS／12 FAIL**，FAIL 清單逐字相同，零新增回歸。
  - 覆核中途捉到一項：`tests/test_travel114_static.py` 寫死行號（FREE_LINES 等），我初版註解由 7 行
    變 12 行令後面行號移位 +5 → 該測試 FAIL。修法：註解壓返 7 行（行數中立，14+/14-），
    回滾詳情留喺本 NOTES §5，唔郁 v114 測試。修好後該測試 PASS，全套返 154/12。
- **Rebase 後覆核（第二次，v117 S-30 詳情區改版）**：新基線 pristine origin/main `a02f77f` ＝ **155 PASS／12 FAIL**；
  工作版 ＝ **155 PASS／12 FAIL**，逐字相同，零新增回歸（基線工作副本 `~/workspace/linji-base116bwt`）。
  註：中途 service 重啟清咗 /tmp，基線檔重跑過一次先對到，結果一致。

## 4. 實駕（`qa116/drive116.py`，本地鏡像＋Playwright 390×844＋可棄用槽 3）

- 真 UI 路徑逐間開卡：地圖 pin → 地點 sheet「只查看通告欄」→ 通告欄 modal → 撳第一張
  `.gig-teaser` → 通告詳情 modal，驗英雄圖 src 係新檔＋naturalWidth>0。
- **11/11 間 PASS，0 pageerror，boss 圖 0 失敗請求**（DRIVE116 PASS）。
- 截圖：`qa116/shots/boss_tvb_longmen.png`（沈卓衡 v2b）、`boss_film_lion.png`（羅勁威 v2b）、
  `boss_rec_star.png`（溫子峰 v2）——三張都見到新圖企卡頂＋名牌。
- **Rebase 後重跑**（合併後分支，v114 出行額度已入）：同樣 11/11 PASS。Drive 已加額度適應——
  每開 2 間就 `S.dayIndex+1`（聽日重置額度），全程留喺冬季（day 0–11），board 季節不變；
  `forceRestore`（返地點選單）唔計額度，每間只係 1 次。
- **第二次 rebase 後（v117）重跑**：同樣 11/11 PASS（v117 改咗詳情區版面，卡頂英雄圖無影響）。
- 其餘失敗請求係**已知舊問題，唔關 v116 事**：巧遇對話表情缺檔 404（每 run 撞到嘅星唔同，
  缺檔亦唔同：第一 run 係 `chung_choning_think.webp/.png`，rebase 後 run 係
  `pang_siuki_surprise`＋`awi_angry` 各一對；drive 準則已收窄到只計 boss 圖）。
- 實駕中途修咗兩個 drive 腳本問題（唔係遊戲 bug）：
  - WF4 事件推進掣係「繼續」→「睇落去」→選項→「好」，舊 list 冇「睇落去」會卡死；
  - ENC79 巧遇對話掣係 `.e79-btn`（唔喺 `#modal-btns` 入面），選項文字任意，要加後備撳掣。
  兩個都已寫入 `qa116/drive116.py` 嘅 `dismiss_interceptors`（連續 3 次無掣可撳先放棄；
  選項揀第一個，槽 3 測試檔，好感輕微影響可接受）。
- 其餘 2 個失敗請求係**已知舊問題，唔關 v116 事**：`chung_choning_think.webp/.png` 404
  （鍾楚凝 think 表情缺檔，巧遇段已知殘留；drive 準則已收窄到只計 boss 圖）。

## 5. 回滾

- v1 檔：`assets/story/fullbody/boss_<loc>_base.webp`（11 張，仍在 repo）。
- 回滾＝對照表 11 行 src 指返 `boss_<loc>_base.webp?v=20a106`（即 v111 狀態）。
- 工作檔（生成圖＋manifest＋對照表）：
  - v2：`~/workspace/linji-work108c/qa108c/s30v2/boss_portraits/v2_anime/`
    （成品 `final/`、manifest `manifest_boss_v2.json`、對照 `sheets/sheet_compare_v1v2.png`、
    `sheets/sheet_faces_v1v2.png`）
  - v2b：`~/workspace/linji-work108c/qa108c/s30v2/boss_portraits/v2b_fix/`
    （成品 `final/`、manifest `manifest_boss_v2b.json`、對照 `sheets/sheet_faces_v2_v2b.png`）
- 換入前 v1 對照表見 v111 NOTES（`NOTES_V20A111*.md`，main `41e4be8`）。

## 6. 殘留缺口

- v115 文字重寫已合併入 main（本分支 rebase 後實駕截圖見到新版短行文字），唔係 v116 漏改。
- 巧遇對話表情缺檔（每 run 唔同星：鍾楚凝 think、彭少祺 surprise、阿偉 angry 等）係舊殘留，
  另開一票處理，唔喺呢包。
- v110／v112 同時進行緊；本分支由 origin/main `41e4be8` 開出，收尾前兩次 rebase
  （`2d71588` → `a02f77f`），兩次都無衝突；基線工作副本留喺 `~/workspace/linji-base116wt`
 （pristine `2d71588`）同 `~/workspace/linji-base116bwt`（pristine `a02f77f`）。
