> Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜玩家面禁真藝名／禁「Ho 哥」→「何生」／favor `agency_ho`｜經 qwen3.7-max

# PLAN_STORY_BEHAVIOR_GATE_FULL_ALIGN_SOFT_v1

## §0 用戶改口（2026-11-08）
- 私聊「嚴格做滿」＋widget **`full_literal_including_gates`**（t380u／t380s1780）。
- **C1–C5 全部跟 FULL 字面**（含改 Soft 已拍板閘）＋FULL 餘波做滿。
- **舊 Soft 拍板作廢：** C1 `cafe_cha`；C4 `softLogic=AND` favor∧loc 死鎖。
- 新閘：C1 `agency_ho`；C4 `softLogic=OR`（`debtMin:1` 人情債 **或** `favorMin:1` Soft 近似左肢 **或** `loc=agency_ho`）。
- Soft≠PASS｜**唔 tip LIVE**｜唔抬 `?v=`／SAVE（仍 20a10／19w）｜出圖 HOLD｜89–92 HOLD。

## §1 範圍／Out of scope
- **範圍**：FULL 字面閘＋餘波落地（slots／story／sandbox stub）＋Soft 預覽引擎最小 OR／debt patch。
- **Out of scope**：唔 tip LIVE；唔改 LIVE week-gate 主路徑（仍 `liveWeekGateStillActive=true`）；唔改 89–92；出圖 HOLD；唔改 choice／flags id。

## §2 FULL vs Soft 對齊矩陣（C1–C5｜改口後）

| beatId | FULL 字面 | Soft 現況（改口後） | 偏差標記 | 處理 |
|---|---|---|---|---|
| C1 | loc=`agency_ho`；Week1–4 | loc=`agency_ho`；weekMin 地板 | **已跟 FULL**（舊 cafe_cha 作廢） | stub／slots／story 齊 |
| C2 | needDone C1；gig≥3；片場；標籤沉澱 | 同左＋tags「電視城乖仔／片場老油條」 | 無 | 餘波落地 |
| C3 | fame>15；高仔搶鏡；信用／對手態度 | fameMin16；ripple creditDelta／rivalAttitude | 無 | 餘波落地 |
| C4 | 人情債>0 **或** loc=`agency_ho` | softLogic=`OR`；debtMin=1；favorMin=1（近似左肢）；loc agency_ho | **已跟 FULL OR**；favor 作 debt 可玩近似（NOTES） | 引擎 patch＋smoke 改合約 |
| C5 | 秋|冬；cafe|片場；choi_*；羈絆／情報 | seasonAny autumn|winter；choi_honest／spin／dodge；bond／intel ripple | FULL 裸 spin／dodge → Soft `choi_*`（對照） | 主線名《采兒小訪題》 |

## §3 tip 前 checklist
- [x] C1 agency_ho／C4 OR＋debtMin／C5 秋冬
- [x] nextHint 全空
- [x] rival_gao 唔入 C5
- [x] DualMeet chrome＝支線
- [ ] feature flag 合流（仍缺口）
- [ ] LIVE tip（**禁止直至明示**）
- [x] Soft≠PASS｜tipForbidden

## §4 Soft 瀏覽器建議驗點
1. C1 必須 `agency_ho` 開；`cafe_cha` 唔開主線 C1。
2. C4：只到事務所（favor0／debt0）可開；只欠債（他處）可開；只 favor≥1（他處）可開；三者皆無 → 鎖。
3. C3 fame15 鎖／16 開；C5 夏鎖／秋冬開。
4. 玩家面：何生、傳聞、禁噂／Ho哥；C2／C4 標籤可讀；C5 羈絆／情報 ripple 可讀。

## §5 Acceptance／Out of scope
- **Acceptance**：閘＋餘波跟 FULL 字面（用戶改口）；預覽引擎支援 C4 OR／debtCount；smoke 合約已放寬。
- **Out of scope**：唔 tip LIVE；唔抬 version；iOS Soft tip 另排。

---
*文末註：經 qwen3.7-max；FULL PLAN sha8 `6a405b25`；用戶 2026-11-08 full_literal_including_gates*
