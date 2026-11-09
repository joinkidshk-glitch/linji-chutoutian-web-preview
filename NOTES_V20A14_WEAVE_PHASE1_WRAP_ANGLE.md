# NOTES v20a14 — Weave Phase 1-2：殺青報「角度」（殺青後 → 報紙）

日期：2026-11-09
性質：soft 預覽功能增量（串聯規劃 Phase 1 第 2 步）。Soft≠PASS。SAVE key 不變、softRev 不變（s107）、`?v=` 不變（v20a10）。
狀態：本地完成＋測試全過；待 v20a13 部署覆檢完成後先推分支合併（避免部署隊列混亂）。

## 背景

串聯規劃 §3.3：報紙主報道嘅角度，應該由殺青後反響決定（至少 2 個角度版本），
唔好下下得一個寫法。原本 `newspaperWrapFaceLines` 只有「穩陣」一種角度
（走位穩妥／鏡頭前不搶戲），殺青後反響幾好都係咁寫。

## 改動（只改 index.html）

1. **新增 `newspaperWrapAngle(sh, pack)`**：用現有訊號判定角度，零新機制——
   殺青後反響包入面街坊卡帶幕前聲量加成（`stageVolumeDelta ≥ 1`，即俾街坊留意到），
   或通告本身聲望值 ≥ 3 → `spotlight`（搶眼）；其餘 → `steady`（穩陣）。
2. **`newspaperWrapFaceLines(subject, angle)`**：加可選角度參數。
   `spotlight` 時按媒介換 dek＋rumor（電視「嗰場戲俾人記住」、電影「鏡頭前搶眼，副導記低咗佢個名」、
   唱片「嗰段演出俾人點名提起」、廣告「出鏡嗰下俾人記住個樣」）；headline 不變（事實句唔跟角度轉）。
   無傳角度＝穩陣舊寫法，一字不改。
3. **`enqueueNewspaperFromWrap`**：計角度、傳入 FaceLines，並將角度存入報紙 item 嘅 `tone` 欄
   （日後報紙連載／點名門檻可讀返）。
   淡紙路徑（fame < 15）維持唔傳角度：低聲望嗰陣報紙保持低調，係 #104 原意，唔搶眼。

## 測試

- 新增 `tests/test_weave12_logic.js`：角度判定 5 項＋穩陣回歸（舊句原文保留）＋搶眼各媒介＋無參數兼容。16/16 PASS。
- 新增 `tests/test_weave12_static.py`：接入點、tone 落欄、淡紙路徑未變、SAVE／softRev 未變。7/7 PASS。
- 回歸：Weave 1-1、P0、P0-3 測試照過；全檔 `node --check` OK。

## 待覆檢（合併＋部署後）

- 做一單有街坊反響嘅通告殺青：翌日報紙 dek 應為搶眼寫法（按媒介）；
  做一單無反響嘅：應維持穩陣寫法。剪報 tone 欄應分別存到 `spotlight`／`steady`。
