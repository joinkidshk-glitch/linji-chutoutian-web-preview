# 《臨記出頭天》— 減網頁感 UI 美術 canon（GD → iOS）

正式遊戲名：**臨記出頭天**  
專案路徑仍：`/workspace/star-volunteer-web/assets/ui-physical/`  
立繪準繩：`../hero_awi.jpg`（暖膚、海軍藍西裝、奶油底、清晰 2D 插畫）  
NPC 肖像：**唔改**

## Brand
| 檔 | 用途 |
|----|------|
| `brand/logo_lockup.jpg\|png` | Logo＋阿偉 lockup（開始畫面／商店圖） |
| `brand/title_banner.jpg\|png` | 橫向標題字 臨記出頭天 |
| `brand/logo_wordmark.jpg` | 純字 wordmark |

之後所有 moodboard／切圖／文案標名用 **臨記出頭天**，唔用「星途志願」作出品名。

## 設計原則
- 實體物件：紙、手帳、膠掣、拍立得／機殼、票根 —— **唔似** HTML card／CSS pill／灰 disabled web button
- 角標／印章：**單層**（一枚圖），避免疊多层 HTML badge
- 最終目標：**原生 iOS**；切圖優先 @2x／@3x 友好、透明底 PNG／可 9-slice 的框

## 色票（跟阿偉暖色＋港產 80s）
| Token | Hex | 用途 |
|-------|-----|------|
| `cream` | `#F0F0E0` | 紙底、手帳內頁、阿偉底 |
| `paper` | `#EFE0BC` | 通告紙、舊手帳 |
| `ink` | `#2A2118` | 正文 |
| `muted_ink` | `#8A7355` | 次要字 |
| `navy` | `#202030` | 標題字／西裝／重點 |
| `gold_seal` | `#C4A574` | 標題描邊、印章邊、釘裝線 |
| `stamp_red` | `#C45C4A` | 油墨印章（初／中／高／急） |
| `jade` | `#4A8F7A` | 廣告檔次／OK |
| `sky` | `#5A8FBF` | 電視檔 |
| `rose` | `#C46A8A` | 電影檔 |
| `violet` | `#8A6AB0` | 唱片檔 |
| `shell` | `#D8D0C4` | 機殼塑膠 |
| `shell_dark` | `#3A3530` | 按鍵凹位 |
| `safe_pad` | 頂 54 / 底 34 pt | iPhone safe area 預留 |

**避免**：大面積 `#0a1424` navy 網頁底當「遊戲世界」；浮層半透明 panel 堆疊。

## 字級（iOS 建議）
| 用途 | 字級 | 字重 | 備註 |
|------|------|------|------|
| 遊戲標題 | 見 brand 圖／約 28–34 pt | Heavy | 臨記出頭天 |
| 標題 H1 | 22–24 pt | Bold / 800 | 通告標題、結果大字 |
| 標題 H2 | 17–18 pt | Semibold | 地點名、手帳日 |
| 正文 | 15–16 pt | Regular | 通告 blurb |
| 輔助 | 12–13 pt | Regular | 次要、成本 |
| 角標／印章字 | 10–11 pt | Heavy | 單層圖內可燒錄 |
| 字體 | PingFang HK / 系統中文 | — | 標題可跟 brand wordmark 感覺 |

## 檔案地圖
- `moodboard/ui_moodboard.jpg|png` — 已標《臨記出頭天》
- `brand/` — logo／標題字
- `notice/` — 通告紙、撕邊、單層角標印章
- `notebook/` — 釘裝手帳、七日格底
- `hud/` — 实体掣／機殼
- `map-frame/` — 拍立得地圖框
- `toast/` — 票根結果條
- `slices.json` — 9-slice／safe-area 提示

## 接入提示（iOS）
1. 開始畫面／App 名顯示用 `brand/title_banner` 或 `logo_lockup`
2. 通告：`notice_paper.png` 做背景；角標用 `seal_*.png`
3. 手帳：`notebook_spread.png`（**空白底**：只螺旋／紙紋／七日空格；日名／行程由 App 疊字）
4. HUD：`hud_buttons_sheet`／`hud_shell_bar`
5. 地圖：`map_polaroid_frame` 內嵌 `hk_map`
6. Toast：`ticket_stub.png`（**空白票形／撕邊**）；結果字由 App 疊；可選 `stamp_complete.png`；bottom safe area
