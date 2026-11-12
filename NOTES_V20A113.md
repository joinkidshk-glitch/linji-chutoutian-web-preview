# NOTES_V20A113 — 主線順序閘修復（C18／C19 跳步）

- 版本：v20a113；分支 `v113-story-gates` → squash 入 main
- 來源：用戶 2026-11-12 07:02 實玩捉到——手帳進度頁第 2 週嗰陣，第 18 幕《上岸路》已經顯示「✓ 已完成」，但第 2–17 幕全部未開放。
- 根源：`STORY_GATE_3Y` 入面 `C18: { yearMin: 1990, seasonIn: ["冬"] }` 冇 needDone、冇 weekMin；1990 年 1 月計做「冬」，第 2 週去何生事務所（C18 locId `agency_ho`）已經觸發播出，`markDone` 寫入 `S.story.done["C18"]`。C19 同款漏鏈。主幹大半有鏈，唯獨 WF1 插入幕（v20a80 真空帶補幕）漏咗。敘事上亦錯：C18 係「年尾何生約阿偉傾來年安排」，1 月播出時間線都錯埋。

## 閘改動對照表

| 幕 | 改前 | 改後 | 理據 |
|---|---|---|---|
| C18《上岸路》 | `{ yearMin: 1990, seasonIn: ["冬"] }` | `{ needDone: ["C5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"] }` | C5 係真空帶之前最後一幕必修章；weekMin 48＝1990-12-01（dayIndex 334，第 48 週），1990 年 12 月第一個週次，同 `STORY_SPINE_NODES_WF1` C18 `pacing.weekMin＝48` 一致（v20a100 A-12 章戳「約第48週」）。brief 話「約 45」——45 週係 11 月初（秋），要靠 seasonIn 先擋到 12 月；48 週語義更準，實際窗口相同，都係 12 月起。 |
| C19《賭枱邊》 | `{ yearMin: 1991, seasonIn: ["春"] }` | `{ needDone: ["C18"], weekMin: 61, yearMin: 1991, seasonIn: ["春"] }` | 1991 年春一到唔使做完 C18 就開得，同款漏鏈。weekMin 61＝1991-03-01 春首日（dayIndex 424，第 61 週），同 pacing.weekMin＝61 一致；功能上同 seasonIn＋yearMin 重疊，寫入係為咗同節點章戳對齊、等進度頁鎖定原因逐項顯示「到第 61 週」。 |
| C11（1991 夏／秋） | `{ yearMin: 1991, seasonIn: ["夏", "秋"] }` | `{ needDone: ["C7"], yearMin: 1991, seasonIn: ["夏", "秋"] }` | N 次序入面 C7 嘅下一幕，唔鏈會令 1991 夏未做 C7 都直入。安全：C11 唔喺關鍵路徑（冇嘢要 C11），C7 門檻溫和。代價：錯過 C7 夏天窗口嘅玩家，秋天嗰半開唔到 C11——一個可選場景，換嚴格 N 次序。 |
| C15（1992 春） | `{ tagAny: […], yearMin: 1992, seasonIn: ["春"] }` | `{ needDone: ["C10"], tagAny: […], yearMin: 1992, seasonIn: ["春"] }` | N 次序入面 C10 嘅下一幕。安全：C15 唔喺關鍵路徑，C14 已經要 C10，唔增加新軟鎖風險。 |
| C9（1991 冬） | `{ yearMin: 1991, seasonIn: ["冬"] }` | 不變（刻意） | **唔補鏈**：C8 係 1991 秋限定；若果 C9 要 C8，錯過 C8 秋天窗口嘅玩家會連 C9→C10→C14→C12→C16→C13→C17 成條關鍵路徑一齊死（災難性軟鎖）。C9 係恢復節點；關鍵路徑經 C10 要 C9 間接卡住，唔可以直接跳去結局。 |
| C13（1992 冬） | `{ yearMin: 1992, seasonIn: ["冬"] }` | 不變（刻意） | **唔補鏈**：C16 係 1992 秋末＋dual>125；若果 C13 要 C16，錯過 C16 嘅玩家會連 C13＋C17（結局）一齊死。C13 係恢復節點；關鍵路徑經 C17 要 C13 間接卡住。 |
| C6／C6F | route＋weekMin 15 | 不變 | 路線分支可選幕，唔當順序主幹鏈。 |

- yearMin 唔轉 yearEq：brief 只叫加 needDone＋weekMin；codebase 慣例係 yearMin（C17 例外用 yearEq 1992，因為係結局事件閘）；C9／C10 等同樣用 yearMin，改 C18 會破壞一致性。
- 其餘閘不變：C7←C5、C8←C7、C10←C9、C14←C10、C12←C14、C16←C12、C17←C13 早已有鏈。
- 關鍵路徑：C5→C7→C8→C9→C10→C14→C12→C16→C13→C17；錨點係 C10 要 C9、C17 要 C13——自由節點 C9／C13 經呢兩個錨點間接卡住。

## 載入遷移 `storyGate113Scrub(o, gate)`

- 掛入 `normalizeSaveObj`，次序：levels75 之後、calib60MissedScan 之前（等被清走嗰幕若果已過窗，可以正確登記做「已錯過」；未過窗就留返未開放狀態）。
- 判準（forensic：`S.story.done` 只係 boolean map，冇逐幕播出日子）：
  - (a) needDone 鏈：done 已標、但任一前置而家未 done → 必清；
  - (b) weekMin：done 已標、但而家週數 < 閘嘅 weekMin → 播出嗰陣週數只會更細，必清（日子只會向前行；jan67 遷移喺呢步之前已經對返新 epoch）。
- 覆蓋 STORY_GATE_3Y 全部有 needDone／weekMin 嘅幕（C6／C6F 順帶覆蓋，舊制下佢哋嘅 done 本身已受閘守住，唔會誤清）。
- 合法完成唔會誤清：合法播出嗰陣前置已齊＋週數已夠，之後週數只會更大、前置唔會變返未做。
- 冪等；回傳清走咗嘅 id 清單；退化輸入（null／空物件／冇 story.done）唔炸。

## 殘留缺口（已知，唔扮冇）

1. **yearMin 每年重開**：C18／C19 理論上每年同季都開得（1991／1992 年冬 C18 都會重開），同 CALIB60「1990 年冬／1991 年春」單一窗口顯示有落差。呢個係全庫 yearMin 閘共有嘅既有模式（C9 1992 年冬都會重開），唔係 v113 新引入，留返以後整體檢討，唔喺呢包靜靜地改 yearEq。
2. **遷移盲點**：1 月播出、之後先做完 C5 嘅檔（C18 done＋C5 done 並存、而家週數 ≥48），(a)(b) 都捉唔到——`S.story.done` 冇播出日子，無法分辨合法 12 月播出同非法 1 月播出。留返以後若果加逐幕完成日子紀錄先至補得返。
3. **C9／C13 刻意唔鏈**：進度頁上佢哋可以先過前一幕完成——呢個係設計決定（防軟鎖），唔係漏網。守門測試編碼咗呢個判斷（EXPECT map 寫明 C9／C13 預期無 needDone，連同 index 註解）。

## 測試

- 新：`tests/test_story_gate113_logic.js`（24 項：鏈守門 C1–C19＋C6／C6F 豁免＋無環＋前置存在＋weekMin 48／61＋遷移 10 項＋反證 3 項）、`tests/test_story_gate113_static.py`（閘字串＋接線次序＋反證）。
- 改：`tests/test_wf1_80_logic.js` §(4)（舊「冇 needDone 唔卡主線」斷言改做 v113 鏈斷言；gate 模擬擴充 needDone＋weekMin，新增第 2 週／C5 未做唔開斷言）、`tests/test_wf1_80_static.py`（閘字串更新）。
- 全套：見下節「測試結果」（對基線 A/B）。

## 實駕

- 新檔：開局→第 2 週→何生事務所，C18 唔再出現；進度頁第 18 幕顯示未開放（鎖定原因逐項：先完成第 5 幕、到第 48 週）。
- 舊檔：構造受影響存檔（C1 done＋C18 done，第 2 週）載入，C18 被重置返未開放；C1 保留。
- 證據：`~/workspace/linji-work113/`（截圖＋drive log）。

## 測試結果

- 全套 A/B（runner `~/workspace/linji-work113/run_suite.sh`，每檔獨立計 PASS／FAIL；輸出存 `~/workspace/linji-work113/suite_*.txt`）：
  - 最終基線（origin/main v115 `2b42ca0`）：錄得 **5,563 PASS／43 FAIL**；逐行加總核對後發現 runner 漏咗 `test_s30text115_static.py` 一行回顯（v115 自身測試，單獨跑 15 PASS／0 FAIL），完整基線應為 **5,578 PASS／43 FAIL**。
  - v113 branch（rebase 上 v115 後 `aead4ba`）：**5,616 PASS／43 FAIL**——FAIL 數目同名單同基線逐字一致（poster59 11、soft_tip_111_restore 21、其餘 10 檔各 1–2，共 43，全部 pre-existing），零新增回歸；+38 PASS＝新測試 gate113 logic 23＋static 10＋weave45 新增 2＋wf1 新增 3。
  - 附註：背景執行輸出有間歇甩行前科（早前一次基線跑漏咗 9 行回顯，總數不變），所以每次 A/B 都有逐行加總核對；上面數字係加總核對後嘅。
  - 中途發現：初版 branch 令 weave45／46／48 logic＋weave48 static 失敗（4 檔）——原因係呢啲測試按舊設計斷言 C11／C15 唔使前置就開；已按 wf1_80 同一做法同步更新測試（加 withDone／done 前置＋缺前置反例），唔係改返個閘遷就舊測試。
- 新測試：`tests/test_story_gate113_logic.js` 23 PASS、`tests/test_story_gate113_static.py` 10 PASS（連反證）。

## 實駕

- 腳本 `~/workspace/linji-work113/drive_gate113.py`，本地鏡像＋Playwright，**14/14 ALL PASS**，零 pageerror。
- 新檔：槽 3 構造存檔（dayIndex 7、done 空，經真實 讀檔→槽 3 載入路徑）→ `BehaviorGate.evalGate3Y('C18')` 回 `ok:false`，reasons `['needDone:C5', 'weekMin:48']`；去何生事務所，sheet 開到，畫面無「上岸路」；`StoryOC.listOpen` open=[C1]、done=[]。
- 舊檔：槽 3 構造（dayIndex 7、done C1＋C18）→載入後 `S.story.done` 得返 `{C1: true}`，C18 已清；`listOpen` done=[C1]。
- 進度頁（兩線一致）：第 1 幕已開放（B：✓ 已完成，C1 保留）、第 2／3 幕未開放、第 4–17 幕摺疊未開放；**成頁完全冇「上岸路」**。附註：進度頁只揭曉前線幾幕，C18／C19 唔會單獨列出——所以驗收重點係「成頁冇上岸路」，唔係搵一格「未開放」；第 2 週舊版顯示「第 18 幕 ✓ 已完成」嘅問題已消失。
- 證據：`~/workspace/linji-work113/shots/`（`A_agency_week2.png`、`A_progress_week2.png`、`B_progress_after_load.png`）、`drive113.json`。
- 誠實說明：時鐘推進用存檔編輯（槽 3 構造，dayIndex 7）——手帳「全日休息」掣只係填寫週計劃範本，唔係即時執行；逐日行足 7 日要行完整個週計劃執行流程，超出呢包驗收範圍。閘評估／進度頁／載入遷移全部行真代碼，唔係 mock。

## 合併紀錄

（待填：main commit＋線上 byte＋sha）
