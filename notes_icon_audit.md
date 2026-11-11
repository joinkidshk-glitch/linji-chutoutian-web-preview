# 圖標組 emoji 全庫審計對照表（階段一，v20a112）

- 審計對象：工作副本 `~/workspace/linji-work111/`，分支 `v112-icons`，基線 main `546007d`（`index.html` 57,225 行，5,023,304 bytes）＋ `content/items_gifts.json`。
- 樣本來源：`~/workspace/linji-icon-sample/README.md`（12 隻樣本，已批核風格：深啡墨線 `#3a2e22`、細線條、手繪微斜筆觸、無填色、透明底 PNG 256×256）。
- 新圖來源：生成工人 14 隻，已入庫 `assets/icons/`（QC 14/14 PASS，見 `qa111/qc111_icons.png`）。
- 審計方法：Python 全檔掃描——`icon:"…"`／`emoji:"…"` 欄位值窮舉＋全檔 emoji／符號序列掃描（44 個不同序列、123 處）＋逐處行號上下文核對渲染位置。

## 1. 「33 個」核實結果：字段實數係 32，連 ♥ 先係 33

| 欄位 | 不同值 | 出現次數 |
|---|---|---|
| `icon:"…"` | 23（含非 emoji 佔位 `·` ×2） | 46 |
| `emoji:"…"` | 15 | 16 |
| 兩者聯集（除 `·`） | **32** | — |

README 講「程式碼實數 33 個不同 emoji 值」係將 S-46 心形 `♥`（U+2665）計埋——`♥`/`♡` 只出現喺 `enc79PeopleHtml()`（L51166）同 `people72Html()`（L56038）嘅好感字串，唔喺任何 `icon:`／`emoji:` 欄位。**字段值 32 ＋ ♥ ＝ 33，數字對得上，來源要噉樣講先準。**全檔另有 12 個非欄位 emoji／符號序列（見 §4）。

## 2. 完整對照表：32 個欄位值 → 圖標檔

樣本 12 隻：`icon_map／sleep／mic／tea／clapper／fitness／home／news／gift／hospital／music／people`（`~/workspace/linji-icon-sample/icon_*.png`）。
新圖 14 隻：`icon_tv／radio／lion／briefcase／building／mask／book／martial／broom／sick／phone／mood／star／sparkle`（`assets/icons/` 已入庫）。

| emoji | 欄位值出現 | 用途／出現畫面 | 對應圖標 |
|---|---|---|---|
| 🗺️ | `icon:` ×3（L34695／34710／35389） | 外出／到處逛逛（行程編輯頁分類＋活動列＋EXEC105 日結行） | `icon_map.png`（樣本） |
| 😴 | `icon:` ×2（L34706／35391） | 休息睡覺（行程編輯頁活動列＋EXEC105） | `icon_sleep.png`（樣本） |
| 🌙 | `icon:` ×1（L35390） | 提早休息（EXEC105） | `icon_sleep.png`（樣本，與 😴 共用） |
| 🎤 | `icon:` ×4（L34692／34701／35386／另 1） | 表演／街頭表演／歌藝訓練（分類＋活動列＋EXEC105＋七課） | `icon_mic.png`（樣本） |
| ☕ | `icon:` ×2＋`emoji:` ×1（L34702／35387／5347） | 咖啡店駐場／傾談社交／金龍茶餐廳地點 | `icon_tea.png`（樣本） |
| 🎬 | `icon:` ×7＋`emoji:` ×1（L34691／34718／34739／34755／35382／35965／36329／5335） | 工作／試鏡／通告／台風訓練／紅棉影業地點／殺青指標 metric | `icon_clapper.png`（樣本） |
| 🎥 | `icon:` ×4＋`emoji:` ×1（L34733／35383／35981／37001／5337） | 拍攝日／拍攝／維港電影地點／metric | `icon_clapper.png`（樣本，與 🎬 共用） |
| 💪 | `icon:` ×2（L34693／35385） | 訓練（分類＋EXEC105） | `icon_fitness.png`（樣本） |
| 🏠 | `icon:` ×1（L34694） | 休息（分類） | `icon_home.png`（樣本） |
| 📰 | `icon:` ×1＋`emoji:` 於禮物（L35388? 實為 L43638 press channel／L44369） | 報紙／殺青反響 press 卡／海外時裝雜誌（禮物） | `icon_news.png`（樣本） |
| 🎁 | `emoji:` ×2（L5353 廟街禮品地點；L29860 禮物 fallback） | 廟街禮品地點／禮物預設圖 | `icon_gift.png`（樣本） |
| 🏥 | `emoji:` ×1（L5355） | 仁康醫院地點 | `icon_hospital.png`（樣本） |
| 🎵 | `emoji:` ×1（L5327） | 香江唱片地點 | `icon_music.png`（樣本） |
| 💿 | `emoji:` ×1（L5343） | 灣仔唱片地點 | `icon_music.png`（樣本，與 🎵 共用） |
| 👥 | `icon:` ×1（L43656 streetFans channel） | 街坊反響卡（殺青反響三卡之一） | `icon_people.png`（樣本） |
| 📺 | `emoji:` ×1（L5329）＋`icon:` metric（L43626） | 星河電視台地點／收視 metric | `icon_tv.png`（新圖） |
| 📻 | `icon:` ×1＋`emoji:` ×1（L5331／43647） | 九龍電視台地點／娛樂快訊 news channel | `icon_radio.png`（新圖） |
| 📡 | `emoji:` ×1（L5333） | 海港廣播地點 | `icon_radio.png`（新圖，與 📻 共用；見 §5 註） |
| 🦁 | `emoji:` ×1（L5325） | 獅子山製片地點 | `icon_lion.png`（新圖） |
| 💼 | `emoji:` ×1（L5339） | 中環廣告地點 | `icon_briefcase.png`（新圖） |
| 🏢 | `emoji:` ×1（L5349） | 何生事務所地點 | `icon_building.png`（新圖） |
| 🎭 | `icon:` ×1（L18824） | 演技訓練（七課） | `icon_mask.png`（新圖） |
| 📚 | `icon:` ×1（L18829） | 智商／修養（七課） | `icon_book.png`（新圖） |
| 📖 | `icon:` ×1（L35381） | 劇情（EXEC105） | `icon_book.png`（新圖，與 📚 共用） |
| 🥋 | `icon:` ×1（L18830） | 武師班（七課） | `icon_martial.png`（新圖） |
| 🧹 | `icon:` ×2（L34707／35392） | 收拾房間（活動列＋EXEC105） | `icon_broom.png`（新圖） |
| 🤒 | `icon:` ×2（L34724／35388） | 病假（活動列＋EXEC105） | `icon_sick.png`（新圖） |
| 📞 | `icon:` ×2（L34744／35971） | 等消息（活動列＋拍攝簿） | `icon_phone.png`（新圖） |
| 😊 | `icon:` ×1（L18828） | 魅力訓練（七課） | `icon_mood.png`（新圖） |
| ⭐ | `emoji:` ×1（L5345） | 天星音樂地點 | `icon_star.png`（新圖） |
| ✨ | `icon:` ×1＋`emoji:` ×1（L18827／5341） | 外貌／形象（七課）／金鐘創意地點／metric fallback（L43626／43735） | `icon_sparkle.png`（新圖） |
| ✅ | `icon:` ×3（L34749／35384／37107） | 殺青（活動列＋EXEC105＋拍攝簿） | **CSS 圖形**（綠色 ✓ 字元＋`.ic-check112` 樣式；見 §3） |

結論：32 個欄位值之中，31 個有對應圖標檔，1 個（✅）行 CSS。**欄位層零缺口。**

## 3. 狀態符號 → CSS 圖形（唔畫圖）

| 符號 | 出現 | 處理 |
|---|---|---|
| ✅（`icon:` 值） | L34749／35384／37107，經 `planMeta`／EXEC105 渲染 | CSS：`<span class="ic-check112">✓</span>`（✓ U+2713 係文字元，沿用現有 `gap-ok` ✓ 慣例，只加色＋尺寸） |
| ♥／♡ | L51166 `enc79PeopleHtml()`（紅星好感）／L56038 `people72Html()`（NPC 人情） | **S-46：改 5 格進度點 CSS**（`.fav-dots112`，滿格實心／空格空心），唔使新圖 |
| ✓／✗／○ | 通告卡條件格（L34407–34656）、進度頁（L42894–42937）、日結提示（L25114／32198） | 保留文字元（已有 `gap-ok`／`gap-no`／`prog71` 顏色樣式，唔係 emoji 呈現） |
| ★／☆ | 通告星級（L34106 計數／L34392–34393 `notice_star_on/off`） | 保留文字元（已有開／關 CSS 類） |
| ☰ | 選單掣（L4991）＋7 處註釋 | 保留（三劃選單符號，唔係 emoji） |
| · | `icon:"·"` ×2（L34723 未安排／L34762 fallback） | 保留（非 emoji 佔位） |

## 4. 留返 emoji（連原因）

| emoji | 出現 | 留低原因 |
|---|---|---|
| 🏆 ×7 | 頒獎卡 kicker（L44344）＋頒獎禮文案（L44761／44869／44872／44932／45375／45377） | 26 隻圖標無獎盃；獎盃係行內文案標記（非欄位值），畫一隻要另開生成。殘留缺口，見 NOTES  §7（建議跟進包加 `icon_trophy.png`）。 |
| 🔒 ×4 | 未開放劇情列（L27575／27648）、通告鎖（L33937）、週 tab 鎖（L36087） | 細 inline 狀態字元；CSS 畫鎖要額外幾何，效益低；唔係圖標系統一部分。 |
| 💡 ×4 | 通告情報標記（L34194）、地圖情報 fallback（L38008）、手帳情報行（L52206）、地圖提示（L55354） | 無對應圖標；「情報／點子」語義抽象，硬配現有圖會誤導（唔可以用燈泡以外的圖頂住）。L38008 只係 `legend_intel` 圖缺失時嘅 fallback，該圖已存在，實機唔會見到。 |
| 📋 ×1 | 地圖通告標記 fallback（L38004） | 純 fallback，`legend_board` 圖已存在，實機唔會見到。 |
| 👤 ×1 | 地圖熟人標記 fallback（L38011） | 純 fallback，`legend_acquaintance` 圖已存在，實機唔會見到。 |
| 🍍🧁🧴📎📝📼🍬🌸 ×8 | `content/items_gifts.json` 10 件禮物（每件一 emoji；另 ☕📰 同欄位表重疊） | **逐件商品 pictogram**，唔係系統圖標——要清零就要多 8 隻商品圖（菠蘿油、蛋撻、保溫瓶、髮夾、拍紙簿、卡帶、甜品盒、香氛），超出呢包 26 隻範圍。渲染處 L55822／55859／55928 照舊用 `item.emoji`，fallback 🎁→`icon_gift.png`（只換 fallback）。 |
| （硬編碼於模板嘅 🎬🎥📞✅，見 §6） | 拍攝簿 L56292–56337 | 唔留——階段二換做對應圖標／CSS（佢哋唔喺欄位，審計時要另外捉）。 |

## 5. 渲染位置總表（階段二逐面換嘅清單）

| 渲染點 | 行號 | 餵入值 | 換法 |
|---|---|---|---|
| 行程編輯頁・週日掣 `.ic` | L36163 | `planMeta().icon` | `iconHtml112()` |
| 行程編輯頁・活動列 `.ai` | L36225 | `it.icon`（PLAN 活動表 L34691–34755） | `iconHtml112()` |
| 行程編輯頁・分類 tab `.ci` | L36192 | `PLAN_CATS[].icon`（L34691–34695） | `iconHtml112()` |
| 日結結果行 | L37225 | `meta.icon` | `iconHtml112()` |
| 過去日子行（EXEC105） | L35428 經 `nbRowMeta105`（L35449） | `EXEC105_KINDS[].icon`（L35381–35392） | 經同一渲染點（唔另開） |
| 七課訓練指南行 | L31107／31136 | `COURSE_DEFS[].icon`（L18824–18830） | `iconHtml112()`（要移出 `ux68Esc()`） |
| 地圖「全部地點」列 | L38071 | `L.emoji` | `iconHtml112()` |
| 地點板標題 | L52175 | `L.emoji`（`textContent`） | 改 `innerHTML`＋`iconHtml112()` |
| 殺青反響卡 kicker | L43735 `.psr-icon` | `channel.icon`（L43626 metrics／43638 press／43647 news／43656 streetFans；fallback ✨） | `iconHtml112()` |
| 殺青反響硬編碼 kicker | L44355 ✨／L44369 📰／L44374 📻（🏆 L44344 留 emoji） | — | 逐個換；🏆 唔郁 |
| 手帳事業・拍攝簿 | L56292 📞／56301 ✅📞／56314 🎥／56329 🎬／56337 ✅ | 硬編碼 | 逐個換（✅→CSS） |
| 人脈頁 S-46 | L51166／L56038 | ♥／♡ 字串 | 5 格進度點 CSS |
| 地圖標記 fallback | L38004 📋／38008 💡／38011 👤 | 僅圖缺失時 | 唔郁（圖已存在） |
| 禮物頁／庫存 | L55822／55859／55928 | `item.emoji` | 唔郁（§4）；fallback 🎁→gift 圖 |

## 6. 審計時捉到嘅三個 README 出入（已核實）

1. **「33 個」實為 32＋♥**（見 §1）。
2. **手帳頂部 5 tab 無 emoji**：行程／事業／近況／消息／人情五個頂 tab（L5108–5112）同全部子 tab（L5116–5135）全部純文字，冇任何圖標可換。README「受影響畫面 S-17：手帳頂部 5 tab」唔成立——要加圖標係新設計，唔係替換，呢包唔做。
3. **通告卡本身無類型 emoji**：通告卡嘅標記係 ★／☆ 星級、✓／✗ 條件格、💡 情報（§3／§4），唔係 🎬 類圖標；🎬 只出現喺行程／拍攝簿／metric。階段二唔會喺通告卡加新圖標。
4. **📡 歸類**：海港廣播 `📡` 用 `icon_radio.png`（廣播語義），同九龍電視台 `📻` 共用一圖——電視台用收音機圖本身係舊數據遺留（九龍電視台應配 📺，但嗰格已有星河電視台用 📺；兩個電視台撞圖係數據問題，唔喺呢包改數據，記錄低）。

## 7. 階段二輸入確認

- 26 隻圖標齊：12 樣本（`~/workspace/linji-icon-sample/icon_*.png`，待複製入 `assets/icons/`）＋14 新圖（已入庫，`assets/icons/icon_{tv,radio,lion,briefcase,building,mask,book,martial,broom,sick,phone,mood,star,sparkle}.png`，256×256 RGBA，墨色唯一 `#3a2e22`）。
- 接入策略（供階段二執行）：欄位值保留 emoji 原值，渲染處經中央 `iconHtml112(emoji)` 對照（emoji→檔名＋✅→CSS）；唔做全域取代，逐渲染點換；唔改 SAVE key／softRev／`?v=`；唔掂 v109／v110／S-30 v2 檔案。

## 8. 階段二後補充（實駕查明，2026-11-12）

- **§5「地圖『全部地點』列」L38071 實為 `#map-area-list` 底欄快捷列，v20a43 起 `display:none !important`**
  （用戶 2026-11-09 決定刪走底欄快捷列、地圖放大；JS 照生成＋綁定，DOM 入面 15 隻圖齊出、0 損壞）。
  階段二照換（萬一日後重開返條列，圖已經喺度），但**可見效果＝零**；實駕只量 DOM，唔截元素圖。
- **地圖底部提示 `#map-hint`（「今日計劃：…」）無 icon**：本身純文字，冇 emoji 可換；加圖標係新設計，唔喺呢包做。
- **日結結果行 L37225 只喺非休息執行日出現**：休息／小休日行 `presentRestSleepDayEnd` 動畫 modal（無 icon 槽）；
  階段二實駕驗證咗非休息日（週六咖啡店駐場 → `icon_tea.png`，見 `NOTES_V20A112_ICONS.md` §5）。
- **拍攝簿 5 個 icon 位未實駕**（首週無拍攝／試鏡紀錄）：已補數據驅動斷言（`tests/test_menu72_logic.js` 追加 5 斷言）；
  S-38 psr kicker 同樣只係靜態＋邏輯測試覆蓋（首週未觸發傳聞推送）。
- **地圖提示文案舊問題**：提示寫「要過日請撳「開始今日行程」」，但逛逛日實際掣名係「過一日」——文案過時，掣本身運作正常，唔喺呢包改。

