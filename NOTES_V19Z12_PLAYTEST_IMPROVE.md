# v19z12 — playtest improve（v19z11 試玩清單）

Branch `fix/playtest-improve-v19z12`. Implements backlog from《臨記出頭天》ux-findings（B1／M3 → M7／N1／N7 及可行 minor／nit）。

## Fixes

| # | Pri | Issue | Fix |
|---|-----|-------|-----|
| 1 | B1／M3 | 遮罩搶點；手帳未確認已播主線 | `setUnderlyingInert` 擴至 menubar／確定掣；`#app.ui-inert` CSS；StoryPlay「下一句／選項」進 `#modal-btns`；`homeEditable` 時 `StoryPlay.start` 拒播；教學後唔再 `play:true` 自動播 C1 |
| 2 | M1 | 「繼續」吞地圖／自由日 | `todayIsForcedDay` 只強制 `shoot:`／`job:`；日結預設「返回地圖」；soft 行程另有「開始今日行程」；「加速本週剩餘」二次確認並列出日子 |
| 3 | M2／M4 | 打聽「免費」矛盾；nextHint 洩漏 | 文案改「不耗日（茶錢另計）」；結算／player pack **永不**露出 pacing `nextHint`／週數 lockedHint（改玩家短句） |
| 4 | B2 | 煙酒內容 vs 家庭向 | `contentFilterOn`：設定「家庭友善內容」或 soft 預設；替換 C1 抽煙句、後巷食煙→食糖水、傳聞買醉用字；adult path 關 filter 仍在 |
| 5 | M5／M6 | 空地點面板；通告雙 CTA | `#loc-sheet:not(.on)` 完全收合；通告欄 modal 開時 `board-modal-open` 停用／提示地點列 |
| 6 | M7／N1／N7 | 週結生活費節奏；桌面 rail；矮屏 CTA | 週六／日日結加生活費預估；修 `#desktop-rail` 被後寫 `display:none` 蓋掉；`#modal-btns` safe-area／矮屏 padding |
| 7 | M8／T4 | 雙「靜音」無區分；暫無音訊 | `aria-label` BGM／音效靜音；disable＋預留；藏音量滑桿 |
| 8 | N2／N3／N4／N5／N6／N8／T1／T3 | 手帳 a11y、對白速度、熟人、遠觀、標題存檔、選項預覽、用詞、傳聞標 | act `aria-label`；預設對白「快」；熟人出入說明；遠觀 flavor；無存檔 disabled；選項信用＋／金錢＋；「我知道了」；「街坊傳聞」 |

## Cache

`?v=19z11` → `?v=19z12`

Prefs key 仍 `starVolunteer_prefs_v19z9`（相容；新增可選 `familySafeContent`）。

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath`
- `nextHint_neverShow` 玩家面做成 **live 預設**（唔改 flag 名）
- 家庭友善內容：soft 預設開，可用設定關掉還原 adult 文案／後巷食煙

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z12&softBehaviorGate=1`

1. 新局手帳未確定 → 唔會全屏自動播 C1；確定出發／到金龍先可播
2. 日結遮罩開住 → 底層「確定」點唔到
3. 訓練日結 → 預設「返回地圖」；下一日街頭唔會被「繼續」連消；加速要確認並列日
4. 規則文案無「打聽免費」誤導；C1 結算無「約第 N 週」pacing nextHint
5. soft／家庭友善：開場無抽煙、金龍見「食糖水」而非「食煙」
6. 未選針：地點 sheet 收合；通告欄開時地點列唔重複接單
7. 桌面 ≥900px 見側欄操作提示；設定 BGM／音效 aria 可分

## Deferred

- N2 週列與選項完全分層重排（已加 aria-label）
- 完整音訊接線（仍預留）
- 通告「差哪項能力」soft-leave 全面接上（既有 soft 設計，未本輪擴寫全部板面）

Auth: t1u
