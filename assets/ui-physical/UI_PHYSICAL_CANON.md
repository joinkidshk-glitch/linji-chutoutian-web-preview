# 《臨記出頭天》— 減網頁感 UI 美術 canon（GD → iOS）**v2 爆改**

正式遊戲名：**臨記出頭天**  
專案路徑：`/workspace/star-volunteer-web/assets/ui-physical/`  
立繪準繩：`../hero_awi.jpg`（暖膚、海軍藍西裝、奶油底、清晰 2D 插畫）  
NPC 肖像：**唔改**  
備份：`_v1_bak/`（v1 全套）、`_blank_bak/`、`_garbled_bak/`

## v2 爆改重點（2026-11-02）
- 色票加深對比，跟阿偉暖色／80s 港產海報
- 開始畫面 lockup 加大人物、少米黄空白；標題 **臨記出頭天** 用本機 Noto CJK 燒錄（禁止 AI 漢字）
- 拍立得框真實比例（約 1:1.2），透明相井；大頭針＋leader line
- 通告真紙質；印章單層 Noto「初／中／高／急」
- 手帳／票根：**空白底無 baked 示範中文／殘影**
- HUD：实体膠掣切片，唔似 CSS pill
- Toast：票根比例＋獨立 `stamp_complete` 層

## Brand
| 檔 | 用途 |
|----|------|
| `brand/logo_lockup.jpg\|png` | 阿偉＋標題 lockup（開始／商店） |
| `brand/title_banner.jpg\|png` | 橫向標題「臨記出頭天」 |
| `brand/logo_wordmark.jpg\|png` | 純字 wordmark |
| `brand/start_title_card.jpg\|png` | 9:16 開始卡 |

之後所有 moodboard／切圖／文案標名用 **臨記出頭天**，唔用「星途志願」作出品名。

## 設計原則
- 實體物件：紙、手帳、膠掣、拍立得／機殼、票根 —— **唔似** HTML card／CSS pill
- 角標／印章：**單層**（一枚圖）
- **空白底規則**：`notebook_spread`、`ticket_stub` 不得含示範行程／「完成」／亂碼／殘影；App live 疊字
- **文字 vs 裝飾線（硬規則）**：live 字不得錯疊格線／底紋；手帳用橫線 list，唔用七欄直格；票根撕線區中間保持可疊字空白
- Brand 標題與印章短字可用 Noto 燒錄；**禁止** AI 生成漢字
- 最終目標：**原生 iOS**；用戶批視覺後先套

## 色票（v2 加深）
| Token | Hex | 用途 |
|-------|-----|------|
| `cream` | `#F2EBD8` | 紙底、手帳內頁、阿偉底 |
| `paper` | `#E6D2A8` | 通告紙、舊紙 |
| `ink` | `#1A1410` | 正文（更深） |
| `muted` | `#6B5340` | 次要字／格線 |
| `navy` | `#1A1A2E` | 標題／西裝 |
| `gold` | `#C9A227` | 描邊／釘裝（更飽） |
| `stamp_red` | `#C43C2A` | 油墨印章 |
| `shell` | `#C8BDB0` | 機殼塑膠 |
| `shell_dark` | `#2E2A26` | 按鍵凹位 |
| `jade` | `#4A8F7A` | 廣告檔 |
| `sky` | `#5A8FBF` | 電視檔 |
| `rose` | `#C46A8A` | 電影檔 |
| `violet` | `#8A6AB0` | 唱片檔 |
| `safe_pad` | 頂 54 / 底 34 pt | iPhone safe area |

**避免**：大面積網頁 navy 底、半透明 panel 堆疊。

## 字級（iOS 建議）
| 用途 | 字級 | 字重 | 備註 |
|------|------|------|------|
| 遊戲標題 | brand 圖／約 28–34 pt | Heavy | 臨記出頭天 |
| 標題 H1 | 22–24 pt | Bold | 通告標題 |
| 標題 H2 | 17–18 pt | Semibold | 地點、手帳日 |
| 正文 | 15–16 pt | Regular | blurb |
| 輔助 | 12–13 pt | Regular | 次要 |
| 角標／印章 | 10–11 pt | Heavy | 單層圖可燒錄 |
| 字體 | PingFang HK／系統中文 | — | 標題跟 brand |

## 檔案地圖
- `moodboard/ui_moodboard.jpg|png`（及 `_v4`）— 標《臨記出頭天》
- `brand/` `notice/` `notebook/` `hud/` `map-frame/` `toast/`
- `slices.json` — 9-slice／contentRect／safe-area
- `MANIFEST.md`

## 接入提示（iOS）— **等用戶批視覺後先套**
1. 開始畫面：`brand/logo_lockup` 或 `start_title_card`／`title_banner`
2. 通告：`notice_paper.png` + `seal_*.png`
3. 手帳：`notebook_spread`／`notebook_spread_list`（**list-lined 空白**：螺旋＋橫線／輕紙紋；**唔要七欄直格**；日名／行程 App 疊；硬規則：文字唔可錯疊裝飾線）
4. HUD：`hud_buttons_sheet`／`hud_shell_bar`
5. 地圖：`map_polaroid_frame` contentRect + `map_pin` + `map_leader_line`；內嵌 hk_map
6. Toast：空白 `ticket_stub`；結果字 App 疊；可選 `stamp_complete.png`
