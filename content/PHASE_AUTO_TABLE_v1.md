# PHASE_AUTO_TABLE_v1｜遊玩自動推進 phase（C1→C17）

> **時間：** 2026-11-03（Asia/Hong_Kong）  
> **狀態：** 計劃 only — **唔改 JSON／index／出圖**  
> **對齊：** `QA_PLAYER_V17N_HIGHBAR_STATIC_v1.md` P0#5；`PLOT_DETAIL_UNLOCK_v1.md` §1；`PLAN_MAP_STORY_PROGRESS_v1.md`  
> **規則：** Soft≠PASS；出圖暫緩；書面語現代  
> **用途：** `StoryOC.markDone`／`applyChoice` 後按表 `setPhase`；debug「phase→P2」僅備援

---

## 1. 原則

1. **玩家路徑必須自動升 phase**；唔可靠接線面板 Playtest。  
2. Phase 只升唔降（除非新局／讀檔）。  
3. 年曆進入（1989…）可作 **OR** 升階；主線 done 為權威觸發之一。  
4. `listOpen`／`StoryPlay.start` 玩家模式用 **`ev.ok`**（含 phase soft）；`openable` 僅 debug／force。  
5. 本表數值／週數仍屬方向性；playtest 可微調，但**唔可**留「只靠 debug」。

---

## 2. 自動推進表

| 到達 phase | 觸發（任一即可升；建議全寫引擎） | 主線節點帶 |
|---|---|---|
| **P1** | 新局／教學完成 | C1–C5 |
| **P1.5** | `C5` done **或**（1988 秋曆＋週數方向門檻） | C6–C7 |
| **P2** | `C7` done **或** 進入 1989 年曆 | C8–C10 |
| **P3** | 進入 1990 **且**（`C10` done **或** P2 關鍵旗 ≥1：例 `route_indie`／`route_commercial`／`anni_*`） | C11（＋感情留白） |
| **P4** | 進入 1991 **且**（`C11` done **或** 中高 tier 方向旗） | C12–C15 |
| **P5** | 進入 1992 | C16–C17 |

### markDone 建議掛鉤（最小實作）

| 事件 | `setPhase` |
|---|---|
| 教學結束／新局入地圖 | 確保 `P1` |
| `markDone('C5')` | → `P1.5`（若尚未 ≥） |
| `markDone('C7')` | → `P2` |
| `markDone('C10')` | 可保持 P2；進 1990 時 → `P3` |
| `markDone('C11')` | 進 1991 時 → `P4`（或即時 P4 若年已到） |
| 年曆跨入 1989／90／91／92 | 分別至少 P2／P3／P4／P5 |

> 與 UNLOCK §1「進入條件」一致；本表把「文件方向」落成**引擎義務**。

---

## 3. 與 listOpen／開局佇列

- 升 phase 後重算 map tip／事態列表（見 `PLAN_MAP_STORY_PROGRESS_v1.md`）。  
- 開局玩家佇列：**只推 C1**；平行 meet 唔因 phase=P1 就晒冷（見地圖計劃 §9）。  
- stub／`phaseSoft` 失敗節：**唔入**玩家 open。

---

## 4. 驗收

- [ ] 只靠 StoryPlay 打通 C1→C7（唔撳 Playtest）→ phase 顯示 **P2**；C8 可播且非 soft 偷跑  
- [ ] 開局 `R_tang_meet`／stub **不可**玩家 start  
- [ ] Soft≠PASS；出圖暫緩  

---

## 5. Cross-link

- `PLOT_DETAIL_UNLOCK_v1.md` §1／新增「玩家可讀未開」  
- `PLAN_MAP_STORY_PROGRESS_v1.md`  
- `WIRING_OC_ENGINE_v1.md`（`setPhase`／`ok` vs `openable`）  
- `QA_PLAN_GAP_vs_PLAYER_V17N_v1.md`
- C5 開節門檻（非 phase 升階）：`rel_choi_threshold=2` 見 `PLAN_MAP_STORY_PROGRESS_v1.md` §9.7／`PLAN_BOARD_3_v1.md`（本表只管 `C5` done→P1.5）

*完 — PHASE_AUTO_TABLE_v1*
