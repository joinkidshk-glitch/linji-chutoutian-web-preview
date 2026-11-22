# v20a379 — 第四輪評估修正（P1 四項＋重點 P2）＋結局判定層覆核

日期：2026-11-22。基線：v378（`091800c`，suite 400 PASS／9 FAIL）。
來源：`~/workspace/linji-playtest-eval4-2026-11-22/REPORT.md`（第四輪多工人評估，冇 P0）。
逐項對 live code 核實後先改；唔改玩法結構、SAVE key、softRev、產品 `?v=`、贏線 0.875、floor 140、warnLine 180、E1 門檻 350。

## P1 四項

1. **送禮耗日文案統一**：核實 `softSocialCostsDay()`（＝`!softPreviewOn()`）live 會耗一日，文案跟實收改。
   - 巧遇 modal 硬寫「傾談／送禮唔耗日」改動態判斷（耗日時寫「會用去 1 日」）。
   - 標題畫面 `#start-soft-tip` 加 `display:none` 初始，唔再閃出錯誤提示。
   - textfix 覆寫值改 live 準確版：「和熟人傾談或者送禮，會用去一日（茶錢照扣）；訓練、試鏡、休息和跟行程開工，同樣會算日。」
2. **N17 退圈警告加強**：`endingEveOptions410` 三個 quit 選項 note 各加「此選擇不可逆轉，結局會按退圈計算。」設計不變（退圈仍覆蓋 E1），只加強警告。
3. **音樂獎落敗差額提示**：新增 `awards379GapBand(score)`，按同贏線 0.875 距離分三段定性（≤0.05「只差一線」／≤0.15「差一截」／其餘「距離得獎還有一段路」），唔出原始分數；接喺 `buildAwardResultPack` 嘅 weakHint 後。贏線不變。
4. **fame 週跌交代**：核實 −2/週嚟自 settleWeek 體能 <12（非被動衰減，唔係 bug）；`content/events_zh_HK.json` WEEK_LOW_STA 兩句＋index.html fallback 加「聲望下跌」明寫，機制不變。

## 重點 P2

5. **預設計劃壓力感知**：`defaultWeekPlan()` 加壓力判斷——`S.stress ≥60` 訓練位改休息（兩日休息）、`≥80` 再多一日（三日）；壓力唔高行為不變。
6. **林曉晴／周采兒 commit 場景**：`endingRomanceScene410` 曉晴兩版＋采兒一版各加「那晚之後，你們正式成為情侶。」（同 v376 四條新線口徑一致，HE＝正式成為情侶）。
7. **好感分母**：`rom183RelText183`／`rom183RelLine183` 硬編 ／5 → ／7（rel 上限 v378 已改 7）。
8. **撞頂送禮提示**：`openGiftPick` 確認 modal 加 `capLine379`——rel ≥7 時寫明「好感已達上限（7／7）——再送都不會再升，禮物和日子照樣會用去。」
9. **徐寶珊送禮閘旗標**：`content/gift_prefs.json` xu `requireFlagsAny` 由永遠唔會寫嘅 `warm/cold/cool` 改做 meet 實際寫嘅 `flag_xu_met_polite`／`flag_xu_met_distance`（核實 `story_detail_romance_lan_xu.json`）。
10. **UI 三項**（先諮詢 GPT-6.2-sol，原稿存 `~/workspace/linji-drive379/gpt_ui_plan.txt`）：
    - 地圖標籤重疊：`deCollideLabels363()` 加「我喺呢度」標籤（`.me363-tag`）做障礙物，重疊嘅地點名推落。
    - 頒獎空黑：`.awd62-stage` 背景由平黑改聚光燈漸層（佈局不變，frame 頂釘死維持 v218 決定）；入圍卡預覽不透明度 .22→.38。
    - 約會文字卡：`rom159DateScene` 兩個 modal 改用劇情對話同款 `.dlg` 呈現（立繪＋名＋對話框，立繪經 NPCS face→PORTRAITS；葉／蘇冇 NPC 立繪跌返純文字，待五位新星美術票）。

## 補充覆核：結局判定層 17 格再驗（v378 ID 改動後）

方法：借 `tests/test_weave410_logic.js` harness 抽真判定函數（`resolveEnding410` 全鏈＋`ending410ResolvePresent410` 覆寫路徑），合成狀態逐格命中。腳本＋輸出存 `~/workspace/linji-drive379/verify_endings379.js`／`verify_endings379_out.txt`（唔入 repo）。

**結果：29 案全 PASS，17 格全部仍可達**（E0/E1/E2/E3/E4/E5/E6/E7/SS/FK/TK/SK/GH/CK/AK/ID/CR），含 E3 三變體、E4 兩變體、E6 三變體、E7 覆寫＋E3/E4/E5/E6 豁免。v378 改動專項：ID 新窗（聲望 100＋信用 80→ID）、平衡 profile（聲望 65＋信用 64→E2 唔入 ID）、次序（ID 窗內＋E3/E5 資格→E3/E5，ID 移後成立）全部驗證。

## 測試 resync

index.html 淨 +50 行。按 difflib 映射（`qa379/resync379.py`）更新行號釘：rom159／rom176／travel114（COUNT／FREE／DEF／WRAPPER）／tang171／tang173／gift185（總行數 48773→48823、openLoc 43939→43985）。文字釘更新：awards212 預覽不透明度 .38、stamina58 低體能句（加「聲望下跌」）、rom183 分母 ／7、text55 A6 期望句、awards62/188 抽取清單加 `awards379GapBand`。rom159 gift_prefs 斷言改精確替代（xu 旗）＋正向斷言。

Suite：**400 PASS／9 FAIL**（九項已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），同 v378 基線一致。
