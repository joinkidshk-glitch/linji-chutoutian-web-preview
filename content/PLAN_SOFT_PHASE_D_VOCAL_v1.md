# PLAN｜Soft Phase D 獨立歌藝 vocal v1

**日期：** 2026-11-05（Asia/Hong_Kong）  
**觸發：** 用戶開閘「要加」獨立歌藝（答「為什麼沒有歌藝」）；統籌轉交；今次**只開** `vocal`。  
**對齊：** `PLAN_GIG_MV3_ALIGN_v1` Phase D；`PLAN_GIG_REQ_BANDS_1988_v1`（max＝999）；現行 Soft LOCS `type=music`。  
**基線通告：** `gigs_1988_3.2.9-soft.json` → 已 patch **`gigs_1988_3.2.10-soft.json`**（SHA `35895f4e`）  
**映射 notes：** `NOTES_SOFT_PHASE_D_VOCAL_MAP_v1.json`
**Soft≠PASS**／唔 tip LIVE／唔抬 ?v=・SAVE（仍 **19w**）／89–92 HOLD／出圖 HOLD／`speech`・`dance` HOLD  
**Cap：** 能力（含 `vocal`／`stamina`＝體能）**999**；僅 `stress` 壓力 **100**  
**結算：** 訓練／打工／通告**只加壓力、唔扣體能**；休息恢復照舊；文案壓力向

---

## 0. 一句

開獨立 STAT `vocal`＝歌藝；唱片／歌藝系主門檻由 `stage` 改 `vocal`，`stage` 改輔；音樂地點主練 `vocal`；舊存缺 key 用開局公式補 14；能力（含體能 stamina）cap 999；僅壓力 stress cap 100。

---

## 1. STAT

| key | 玩家面 | cap | 開局常數（現行 Soft 同檔） |
|---|---|---|---|
| `vocal` | 歌藝 | **999**（能力） | **14**（同開局 `stage:14`） |

**Cap 分流（用戶 2026-11-05 改口）：**
| 欄 | 性質 | cap | 說明 |
|---|---|---|---|
| `vocal`／`stamina`（玩家面**體能**）及其他能力（`acting`／`stage`／`looks`／`iq`／`charm`＋fame／popularity 等） | 人物能力 | **999** | 與 REQ_BANDS 能力門檻對齊；**體能＝能力** |
| `stress` 壓力 | **唔算**人物能力 | **100** | 引擎 clamp；**唯獨**壓力 100 |


現行六維維持：`acting` 演技 · `stage` 台風 · `looks` 外貌 · `stamina` 體能 · `iq` 智商 · `charm` 魅力。

**語義維持（唔改 key）：** `looks`＝儀態／鏡頭樣；`charm`＝臨場親和／自信／口才感。  
**台風新定位：** `stage`＝台風／走位／鏡頭舞台感——**唔再單獨頂「歌藝」**。

**玩家面標籤（用戶 2026-11-05）：** `STAT_LABEL.stamina`＝「**體能**」（key 仍 `stamina`；**cap＝999**，屬人物能力）。條件列寫「體能」唔寫「體力」。

禁：JSON／玩家面出現未開閘 `speech`／`dance`。

**通告：** `req.stamina` **唔夾** ≤100（體能＝能力、cap 999）。僅 `req.stress`（若有）應 ≤100。


## 1b. 結算語義（用戶 2026-11-05 拍板）

| 行為 | stamina（體能／能力） | stress（壓力） | 備註 |
|---|---|---|---|
| 訓練／打工／接拍通告 | **唔扣** | **只加壓力** | 體能＝能力 999，唔再當消耗條 |
| 休息等恢復路徑 | 可照舊（若有加體能／減壓） | 可照舊減壓 | 恢復路徑唔改意圖 |

**文案：** 玩家面唔寫「耗體力／體力下降／扣體能」；改**壓力向**（壓力上升／積壓等）。`STAT_LABEL.stamina` 仍「體能」。

**引擎／iOS Soft tip：** applyTrain／通告結算 delta 去掉 `stamina:-N` 消耗；保留／加重 `stress:+N`。劇本 gigs Soft patch **唔**靠改 req 表達呢條。


## 2. 通告 req 映射表（鎖）

| 粗 `type`／範圍 | `genreLabel`（例） | 主（必顯優先） | 輔（可選／可並列） | 備註 |
|---|---|---|---|---|
| **唱片通告** | 粵語流行・國語流行・情歌・快歌・兒歌・廣告主題曲 | **`vocal`** | `stage`、`charm`、（快歌）`stamina`、（情歌／鏡頭）`looks` | 原主 `stage`→改 `vocal` |
| **唱片通告** | **合唱** | **`vocal`＋`stage` 並列** | `charm` | 合唱可雙主 |
| **唱片通告**／MV 槽 | **音樂錄像** | **`vocal`** | `stage`、`looks`、`stamina`、`charm` | 歌藝系 |
| **綜藝** | **歌唱節目** | **`vocal`** | `stage`、`charm` | 純歌藝展示 |
| **綜藝** | **晚會** | `charm`（主場控）｜歌唱位 **`vocal`＋`stage` 並列** | `stamina`、`looks` | 非純歌則唔硬加 `vocal` |
| 電影／電視劇／廣告／寫真／非歌唱綜藝 | — | **不變** | **不變** | **唔加** `vocal` 硬閘 |

作者／Soft patch 規則：唱片系每則 `req` **必須有** `vocal`；原 `stage` 數值可保留作輔或按 band 微調，**唔刪除**除非 QA 要減維。

---

## 3. 訓練 loc→課

| locId | 地名 | type | 報名文案 | courseId | 課名 |
|---|---|---|---|---|---|
| `rec_hk` | 香江唱片 | music | 報名：練歌／錄音室 | `train_vocal` | 歌藝訓練 |
| `rec_wanchai` | 灣仔唱片 | music | 報名：練歌／錄音室 | `train_vocal` | 歌藝訓練 |
| `rec_star` | 天星音樂 | music | 報名：練歌／錄音室 | `train_vocal` | 歌藝訓練 |

- `TRAIN_BY_TYPE.music`：`train_stage` → **`train_vocal`**
- 新增 `COURSE_DEFS.train_vocal`（增益對齊既有初階課量級，建議 `vocal:4+R(0,2)`＋**只加壓力**（唔扣 stamina；對齊結算語義））
- **保留** `train_stage`／進階台風：非音樂台風、綜藝走位等
- `COURSE_ENROLL_EXTRA.music` 可續掛 `train_charm`（輔）

---

## 4. 舊存補 key（已揀）

**揀：開局公式**

- 新局：`vocal:14`（與現行 Soft 開局 `stage:14` 同檔）
- 舊存缺 `vocal`：寫入 **14**（**唔抄** `stage` 現值，避免主 `vocal`＋輔 `stage` 雙重計入已訓進度）

*備選 B（另議）：缺 key 時 `vocal=min(stage,999)`——僅當 Soft 抽樣要保已訓音樂線進度。*

唔抬 SAVE schema／`?v=`（仍 **19w**）。

---

## 5. 玩家面

- `STAT_LABEL.vocal`＝「歌藝」
- 條件列：**「歌藝：需要 N」**（本 Phase D 鎖；其他 STAT 可仍 `名：>N`）
- 屬性面板顯示「歌藝」條；**唔**顯示口才／動感未實作欄
- looks／charm 玩家面文案維持現映射語義

---

## 6. Soft tip 清單（唔改 LIVE）

**劇本：**
1. Soft gigs patch：**已交** `3.2.10-soft`（vocal 映射＋體力→體能文案；唔夾 stamina）
2. 訓練表／notes 對齊 §3（iOS Soft tip 跟）
3. 交統籌抽樣 → iOS Soft tip（**唔 tip LIVE**）

**iOS Soft：**
1. STAT 讀寫＋cap 999；面板「歌藝」
2. 缺 key migrate＝14
3. 通告條件顯示「歌藝：需要 N」；req 校驗支援 `vocal`（及雙主並列）
4. `type=music` 報名／上課走 `train_vocal`
5. 禁 UI 露出 speech／dance
6. 結算：訓練／打工／通告**只加壓力、唔扣體能**；文案壓力向；休息恢復照舊

---

## 7. QA 勾

1. 舊存無 `vocal` → 讀入後＝14  
2. 唱片通告主見「歌藝：需要 N」；`stage` 若有則輔顯示  
3. `rec_hk`／`rec_wanchai`／`rec_star` 訓練加 `vocal`（唔再主加 `stage`）  
4. 合唱／歌唱節目／晚會歌唱位：`vocal`＋`stage` 並列行為正確  
5. 非歌藝系 req **無** `vocal`；全庫 **無** `speech`／`dance`  
6. Soft≠PASS；`?v=` 仍 19w
7. `vocal`／`stamina`（體能）可至 999；僅 `stress` clamp 100；**唔**夾 `req.stamina`
8. 訓練／打工／通告結算無 stamina 負 delta；有 stress 正 delta；文案無「耗體力」

---

## 8. 閘

Soft≠PASS · 唔 tip LIVE · 唔抬 ?v=／SAVE（19w）· 89–92 HOLD · 出圖 HOLD · 只開 `vocal`（`speech`／`dance` HOLD）· **vocal／stamina（體能）／能力 cap 999；僅 stress cap 100** · **訓練／打工／通告只加壓力、唔扣體能**

---

### 映射速查

| 範圍 | 主 | 輔 |
|---|---|---|
| 唱片通告（非合唱） | vocal | stage, charm… |
| 合唱 | vocal＋stage | charm |
| 音樂錄像 | vocal | stage, looks, stamina, charm |
| 歌唱節目 | vocal | stage, charm |
| 晚會（歌唱位） | vocal＋stage（並列） | charm… |
| 非歌藝系 | 不變 | 不變 |




---

## 9. Soft gigs patch 狀態（2026-11-05）

- 已交 **`gigs_1988_3.2.10-soft.json`** SHA `35895f4e`（pre 3.2.9 `fe70d5c1`）
- CHANGELOG `CHANGELOG_GIGS_1988_3_2_10_SOFT.md`
- 用戶改口：`stamina`／體能＝能力 **999**；**取消** stamina req clamp；`stress` 仍 100
- 結算：訓練／打工／通告只加壓力、唔扣 stamina（iOS Soft tip）
- Soft≠PASS｜唔 tip LIVE｜19w｜89–92 HOLD
