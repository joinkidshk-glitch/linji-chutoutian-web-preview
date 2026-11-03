# HINT_PACING_P0_v1

- Date: 2026-11-03 Asia/Hong_Kong
- JSON `story_detail_c1_to_c17.json` **1.2.4**
- Soft≠PASS · 出圖 HOLD
- Source: tester 玩家角度「偏硬」P0（唔好假行動）

## 已改（劇本）

| # | 項 | 做法 |
|---|---|---|
| 1 | C2–C4 lockedHint | 先寫「約第N週＋隔一日」；地點行動降級「開咗再去…」 |
| 2 | C1 後單一 next | `nextHint` 只指 C2；寫明唔使重播先練 |
| 3 | C1 章戳 | `when` **W1-2**；`pacing.weekMin=1`（對齊開局週） |
| 4 | C5 | lockedHint 加「約第9週」＋初夏台慶籌備；**唔**新加見面節（R_choi_meet 仍 playerOffer false） |

## Eng 請跟（若 soft／B01 仲舊）

- 刷新 `STORY_HINT_SOFT` C1–C5 跟 1.2.4（JSON 優先亦可）
- B01／home 文案：C1 **已播完**唔好再推「本週章節／開局可先播先練」

## 驗收

- 即將可出：見 week／隔日口吻，唔似叫你即刻蹲後巷
- C1 結算 next 只講 C2
- C1 header／when 唔再 W3-4
- C5 鎖因含約第9週＋采兒／台慶

## Paths

- `content/story_detail_c1_to_c17.json`
- `content/HINT_C1C5_MAP_v1.md`
- `content/HINT_PACING_P0_v1.md`
