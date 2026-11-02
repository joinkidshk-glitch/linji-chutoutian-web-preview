# QA｜V17S 瀏覽器覆測（legend／map-hint／手帳地圖接地）

> **時間：** 2026-11-03 ~04:32（Asia/Hong_Kong）  
> **測方：** Tester 夜間自主  
> **SAVE：** `starVolunteer_map_v17s`  
> **feature commit：** `8d209aa` · NOTES `6967d98`  
> **URL：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17s （清 `starVolunteer_*`）  
> **裝置：** phone · 390×844 · DevTools  
> **規則：** Soft≠PASS · 出圖 HOLD

---

## Verdict

**PASS with nits**（v17s · `8d209aa` · `?v=17s` · 390×844 · fresh）

| # | 閘 | 結果 | 備註 |
|---|---|---|---|
| A | LIVE／WIRING | **PASS** | gigs 30 fromFile；SAVE v17s；favicon 404 唔擋 |
| B | 自動 C1 | **PASS** | 跳過教學 → 自動「先練／先賺」 |
| C | 金 tip＋「劇」＋圖例 | **PASS** | 圖例：有板／情報／**劇·事態**／熟人／非本區 |
| D | loc 播事態 hitbox | **PASS** | 播事態 55px；只睇通告板 44px |
| E | 結算 nextHint | **PASS** | 人話；無 flag_／need_done／AND／P1.5；nit「低。」斷行 |
| F | C1 後 tip→C2 | **PASS** | HUD 事態 1 |
| G | 通告板 era_* | **PASS** | 人話季節；無「工。」；nit 首次板被鎖教學蓋 |
| H | 手帳事態＋地圖去 | **PASS** | 「地圖去「星河電視台」」；nit「台」斷行 |
| I | StoryPlay 一屏 | **PASS** | 對白＋選項無巢狀滾 |
| J | map-hint | **PASS** | 「劇」事態見圖例＋金框／劇針 |
| S1–S4 | v17s 專項／回歸 | **PASS** | legend／hint／home／autoC1／era |

串：v17p–v17r P0／可發現性 · **v17s 圖例＋手帳接地**。  
規則：Soft≠PASS · 出圖 HOLD。

---

## Nits → 跟進

| 優先 | 項 | 狀態 |
|---|---|---|
| P1 | 首次只睇通告板被 TUT_AUD_LOCK 蓋；我知道了返地圖唔返板 | → **v17t**（thenFn→doScout） |
| P2 | 手帳「星河電視／台」斷字；結算「低。」斷行 | HOLD 字排 |
| P2 | C1 後 B01／日開始卡仍叫播「先練／先賺」 | → **v17t**（C1 done 文案） |

*完 — QA_V17S_BROWSER_v1*
