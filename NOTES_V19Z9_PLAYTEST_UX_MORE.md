# v19z9 — playtest UX leftovers（多存檔／設定／短教學／浮動文案）

Branch `fix/playtest-ux-v19z9`. Closes intentional leftovers from NOTES_V19Z8.

## Fixes

| # | Issue | Fix |
|---|-------|-----|
| 1 | 單存檔 | **3 存檔槽**：槽 1＝既有 `SAVE` 鍵 `starVolunteer_map_v19w`（舊檔自動相容）；槽 2／3＝`SAVE_slot2`／`SAVE_slot3`。標題「讀檔」、選單「存檔／讀檔／新遊戲」開槽表（週／存款／幕前聲量摘要）；覆蓋要確認。`activeSlot`／`lastSlot` 存 prefs |
| 2 | 無設定頁 | 選單「設定」：BGM／音效靜音 stub、音量滑桿（prefs 持久；暫無 Audio 節點）、對白速度（慢／中／快／即出）、減少動態。鍵：`starVolunteer_prefs_v19z9` |
| 3 | 教學過長 | `TUT_MAIN_IDS` → **4 步**：`TUT_WELCOME`／`TUT_MAP`／`TUT_BOARD`／`TUT_DONE`；訓練／打聽／手帳要點併入 MAP／BOARD／DONE 文案；保留「跳過教學」；`postTutorialEntry`／C1 不變。`tutorial_zh_HK.json` version 3 |
| 4 | ％／片酬難懂 | 試鏡結果：`chanceVarianceNote`（表現／壓力／信用）；獲聘：`payContractNote`（合約鎖定 vs 約酬區間）；殺青：`payWrapNote`（實收＝合約額）；通告摘要加一句說明 |
| 5 | 對白速度 | 事態 `.sp-line` 逐字；「下一句」先播完／跳過再進下一句；減少動態／即出＝一次顯示 |

## Cache

`?v=19z8` → `?v=19z9`

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath`
- `SAVE` 鍵名仍 `starVolunteer_map_v19w`（self-check 維持）
- 唔 tip LIVE week-gate

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z9&softBehaviorGate=1`

1. 有舊檔 → 槽 1 顯示進度；可存入槽 2；讀槽 2 繼續
2. 選單設定：改對白速度／減少動態 → 重整後仍在；事態對白跟速度
3. 新遊戲教學只有 4 步；跳過後仍可進事態／B01
4. 接通告／獲聘／殺青卡見到成功率原因同合約／實收說明

## Leftovers

- 真實 BGM／SFX 檔接入（prefs 已預留）
- 人情倒數日 badge、更多存檔雲端同步
