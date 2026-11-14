# NOTES_V20A208 — 頒獎禮流程重設計：逐個獎項慢慢宣佈提名人

## §0 設計（統籌 2026-11-14 14:39 定，寫死）

- 用戶原話：「動畫要慢慢宣佈提名人的。逐個獎項宣佈提名，再最後公佈結果。然後就處理下個獎項」。
- 只做實裝＋驗證，**唔落地**（落地次序 v205→v206→v207→v208；做完 hold 分支，等統籌安排）。
- 現況（main `a426947` 已核實）：`awards62CeremonyBeats` 單一類別 beats（gallery 9.6 秒；won／nominated 約 11.5 秒），只播 focus 類別；names beat 係字幕每 750ms 輪一行、卡片 60＋i*180ms 全部出齊（第 4 張 600ms）——呢個就係要改走嘅「逐行快閃」。
- **格次序**：配角先、主角後，主角男最後壓軸——film／tv／ad：男配角 → 女配角 → 女主角 → 男主角；music：最佳新人獎 → 最佳女歌手 → 最佳男歌手。理由：配角係綠葉，先暖場；主角壓軸，男主角係成晚最高潮；音樂新人先出道亮相，再到女歌手、男歌手壓軸。
- **每格 beats**：格標題 beat（約 1200ms，淨係獎項名）→ 提名人逐個宣佈（每位一個 beat，約 1800ms：字幕讀出嗰位「星：《作品》」、嗰位嘅卡片先喺嗰刻出現、舞台上面嗰位要突出——行前／變光，其餘稍暗；唔准一次過齊出卡片）→ 懸念 1400ms → 揭曉 2100ms。玩家格：提名人＝阿偉＋3 位 fellows（4 個宣佈 beats）；其他格：3 位 fellows（3 個）。玩家格額外保留現有待遇：enter（只限玩家格之前一次，唔好每格行一次入場）、walkup 2200（won）、glamour 1800（won 有海報）、comfort 2600（nominated）。
- **每格約 12–15 秒**（玩家格連 walkup／glamour／comfort 會長啲）；**成晚 3 格約 38–45 秒、4 格約 45–55 秒**。open beat 成晚一次（開頭 1200ms），out beat 成晚一次（結尾 500ms）。gallery／推辭路徑同樣行全晚多格結構（pan beat 成晚一次開頭，declined 字幕不變，冇 enter／walkup／glamour／comfort）。
- **「跳過」掣全程保留**：任何一格撳跳過 → 成晚即刻完 → 結果卡（唔係淨係跳過而家嗰格）。撳畫面快進維持逐 beat。
- **結果卡＋報紙**：成晚完先出一次（現有 `presentAwardResult`／declined `finishSkip` 流程不變）；其他格只做提名＋得主（得主名＋獎盃），唔出完整結果卡。
- **唔郁嘅機制**：seeded fellows、D4 贏線 0.875、comfort beat、fanfare 揭曉嗰刻播（只限 won）、報紙、雙軌獎勵。`buildAwardResultPack` 嘅 `pack.categories` **唔擴大**（結果卡／請柬／log／報紙全部食佢）；全晚類別清單用 `awardsMvpCategories` 全表。
- **邊界**：某格 fellows 係空唔可以 crash——跌返舊 fallback（「入圍名單逐個唱出……」／「今晚嘅得獎者誕生——掌聲屬於台上嗰位。」）。`awardsMvpCategories` 回空就跌返現有單格行為。玩家格一定喺 pack.categories 入面；唔好假設玩家格喺次序邊個位。
- **guard**：`awards62CeremonyActive()`（v203 C3）靠 `.awd62-stage` 存在偵測典禮進行中；跨格轉場嗰陣舞台 DOM 唔可以有空隙令 guard 讀到 false——轉場要即刻接駁或保留外層 wrapper。

## §1 實作（工人填）

### 決定：實作方式 (a)——擴展 `awards62CeremonyBeats` 做多格 beat list

- 揀 (a) 唔揀 (b) 逐格鏈式呼叫現有單格播放器嘅原因：(b) 每格要起一個獨立舞台，格與格之間舞台拆走再重建有空隙（guard 會讀到 false，強制播有機會疊入嚟）；(a) 全晚一個舞台、一個 rAF loop，跳過掣 `finish()` 即係成晚完，語義天然啱；格次序／每格 beats 全部喺 beats list 一次過睇得晒，logic test 易驗。
- `window.__awards` 加 `night208: awards208NightCats`／`order208: awards208CatRank`（實駕探針用）。

### 改動清單（index.html，＋259／−36，淨 ＋223 行，總行數 61432→61655）

| 位置 | 改動 |
|---|---|
| L47535 `awards208CatRank(c)`（新） | 格次序 rank：support 男 0／女 1、newcomer 0、singer 女 1／男 2、lead 女 2／男 3；未知 role／gender 排最後（9）。 |
| L47543 `awards208NightCats(pack)`（新） | 全晚清單：`awardsMvpCategories(ceremonyId)` 全表按 rank 排；每格帶 outcome（pack.categories 有就用佢，否則 "gallery"）、fellows（pack 有就用 `fellows63`，否則即場 `awards63Fellows(ceremony, year, gender, catId)` 計，seeded）、winner（玩家格贏 → null，得主係阿偉，同 `awardWinner149` 一致；玩家格 nominated → `winner63`；其他格 → `fellows[0]`）、repTitle（只限玩家格）、isFocus。`!pack.ceremonyId`／全表空 → 回 null（跌返舊單格）。 |
| L47578 `awards208NomineeSlotIdx(...)`（新） | 提名 beat → 舞台 slot 映射：slots 佈局係 fellows 順序、玩家 splice 入 min(1, 數) 位；玩家格 nominee 0（阿偉）→ slot 1（有 ≥1 fellow 嗰陣），其餘按 fellows 順序對位。 |
| L47584 `awards62CeremonyBeats(pack)` | night 建到就行多格：open 1200（成晚一次）→ gallery 加 pan 2000（成晚一次）→ 每格：enter 1750（只限玩家格之前一次）＋catTitle 1200＋nominee beats（每位 2000ms，見下）＋suspense 1400＋reveal 2100＋玩家格 walkup 2200（won）／glamour 1800（won 有海報）／comfort 2600（nominated）→ out 500（成晚一次）。每 beat 帶 `catIdx`／`catId`／`catLabel`；nominee beat 額外帶 `nomineeIdx`／`nomineeTotal`／`star`／`title`／`me`／`slotIdx`，caption 係「星：《作品》」。fellows 空嗰格：一個通用 nominee beat（「入圍名單逐個唱出……」）＋揭曉 fallback 文案。night 建唔到 → 舊單格 code 原封不動（fallback，舊 logic test 嘅 pack 冇 ceremonyId，照舊綠）。 |
| L47747 `awards62PlayCeremony(pack, doneFn)` | 多格狀態（`night208`／`curCatIdx208`／`curCat208`／`curOutcome208`，fellows／winFellow／repTitle／slots／playerSlot／winnerSlot／entryPlan／cardsData／cardEls 全部改 `let`）；初值第 0 格。`buildSlots208`／`buildCardsData208`／`cardsHtmlFor208`／`buildEntryPlan208` 四個 builder（初建＋轉格共用，slots／卡片佈局同舊 code 一致）；`applyCatState208(ci)`（L47937）：轉格嗰陣重建 slots／entryPlan／卡片 DOM／白牌（`.awd181-t` 改做而家嗰格名、`.awd181-sub` 改代表作／「入圍名單逐一揭曉」）＋卡片 `on` 即刻拎走（新格逐張出）＋新格 fellows px 預載；**舞台唔拆**（`removeChild` 全場只得 `cleanup` 一處，guard 唔見空隙）。全晚所有格 fellows 一次過預載。`glamour` cap 用 `pack.repWork62`（唔用初值 repTitle——初值係第 0 格，非玩家格就係 ""）。 |
| 同上 `draw()` | 加 `catTitle` 分支（新格提名人企定）＋`nominee` 分支（被宣佈嗰位行前半步＋光池，其餘 alpha 0.45）；reveal 分支條件由 pack `best === "won"` 改做而家呢格 `curOutcome208 === "won"`（其他格揭曉唔可以誤行燕尾服捧杯分支）；`out` 分支維持 pack `best`（夜晚完結嗰陣贏家照著燕尾服）。 |
| 同上 `applyBeatCaption`／`syncCards`／`advance()` | nominee 字幕：`入圍名單 n/N · 獎項名`＋「星：《作品》」；reveal 金字改睇 `curOutcome208`；`syncCards` nominee 嗰陣只出已宣佈嗰啲卡（`i <= nomineeIdx`）；`advance()` 每次轉 beat 先 `applyCatState208(beat.catIdx)` 再 caption／confetti；fanfare 只限玩家格贏嗰格揭曉（`curOutcome208 === "won"`）。跳過掣／撳畫面快進唔郁（跳過＝成晚完）。 |

### 提名 beat 時長：統籌原文約 1800ms → 實作 2000ms（有記錄嘅偏離）

- 統籌原文每格算式（1200＋1800×N＋1400＋2100）得出非玩家格 10.1 秒、玩家格 11.9 秒，同「每格約 12–15 秒」／「3 格 38–45 秒」本身有出入。2000ms 令成晚總數落返任務範圍（見下表），每格 10.7／12.7 秒（玩家格連 extras 更長）。偏離只係 +200ms／位，字幕可讀性更好；如果統籌要死守 1800ms，成晚 3 格會係 35.6 秒（低過 38 秒下限），4 格 45.7 秒（範圍內）。

### 每格／成晚秒數算式（logic test 鎖死）

| 場 | 算式 | 總數 |
|---|---|---|
| 非玩家格 | 1200＋2000×3＋1400＋2100 | 10,700ms |
| 玩家格 nominated | 1200＋2000×4＋1400＋2100＋2600 | 15,300ms（唔計 enter 1750） |
| 玩家格 won（有海報） | 1200＋2000×4＋1400＋2100＋2200＋1800 | 16,700ms（唔計 enter 1750） |
| 成晚 film nominated（4 格） | 1200＋1750＋3×10700＋15300＋500 | **50,850ms ≈ 51 秒**（45–55 ✓） |
| 成晚 music nominated（3 格） | 1200＋1750＋2×10700＋15300＋500 | **40,150ms ≈ 40 秒**（38–45 ✓） |
| 成晚 film won（有海報，4 格） | 1200＋1750＋3×10700＋16700＋500 | **52,250ms ≈ 52 秒**（45–55 ✓） |
| 成晚 film gallery（4 格） | 1200＋2000＋4×10700＋500 | 46,300ms ≈ 46 秒 |

### 測試檔改動

- 新 `tests/test_awards208_logic.js`（35 項）＋新 `tests/test_awards208_static.py`（41 項）。
- 舊測試更新（意圖不變，錨點跟重構／行號漂移）：
  - 純行號漂移（`qa208/resync208.py` difflib 對位核實全部逐字相同）：`test_gift185_static.py` 總行數 61432→61655；`test_rom176_static.py` 4 釘（54334→54557、54702→54925、55841→56064、55935→56158）；`test_tang171_static.py`／`test_tang173_static.py` 總行數＋openLoc DEF 55904→56127；`test_travel114_static.py` FREE 22 行＋COUNT 4 行（59985→60208、60163→60386、60309→60532、60330→60553）＋DEF 55904→56127（WRAPPER 45136 唔郁）。
  - 內容錨點跟重構：`test_awards160_m4_static.py`（walkup push 兩處，兩處都喺 won guard 入面）；`test_awards160_m6_static.py`（reveal won 區條件 `best` → `curOutcome208`）；`test_awards160_m9_static.py`（fanfare 觸發條件同上）；`test_awards177_static.py`（玩家 slot splice 搬入 `buildSlots208`）；`test_awards178_static.py`／`test_awards182_static.py`（卡片 builder 搬入 `buildCardsData208`，`fl.forEach(f=> cd.push`）。

## §2 驗證（工人填，統籌獨立重驗）

### 新測試＋反證

- `node tests/test_awards208_logic.js`：**ALL PASS（35 項）**。
- `python3 tests/test_awards208_static.py`：**ALL PASS（41 項）**。
- 反證（pristine main `a426947`，`/tmp/pristine208.html`）：logic **FAILED 35**（抽唔到 `awards208CatRank` 即逐項 FAIL，唔 crash）；static **FAILED 28**（其餘 13 項係舊有內容，照 PASS）。

### 全套 `qa131/run_suite.sh`

- 基線 A（實體 pristine worktree，main `a426947`，`qa208/suite208_base.txt`）：**287 PASS／13 FAIL**。
- 跑 B（工作版，`qa208/suite208_workB.txt`）：**289 PASS／13 FAIL**。FAIL 清單同基線逐項一致（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38——全部 pre-existing），**零回歸**；＋2 PASS 係新嘅兩個 v208 測試檔。
- 舊 awards logic 測試（62／63／178／181／186／187／188／190／192／194／200／204）喺工作版全部 ALL PASS（fallback 路徑）。

### 實駕（2026-11-14，`qa208/drive208.py`，Playwright headless shell，本地 http.server port 20890，播種存檔直寫 localStorage）

**最終輪 5/5 PASS**（第三輪，約 07:21 UTC；之後音樂場景為補截圖再單獨重跑兩次，都 PASS）。每場 0 pageerror／0 requestfailed。

| 場景 | 預期總時長（in-page `beatsTotal`） | 實測（舞台出現→散場） | 差 |
|---|---|---|---|
| film nominated 932 | 50,850ms | 50,123ms | −727ms |
| film won 932 | 52,250ms | 51,437ms | −813ms |
| music gallery 932 | 33,800ms | 32,831ms | −969ms |
| ad declined 932 | 46,500ms | 45,587ms | −913ms |
| film skip（700，第 2 格撳跳過） | — | 第 2 格格標題嗰陣撳，舞台即走＋結果卡即出（`skip_t` < 30s ✓） | — |

（實測一律短 ~0.7–1.0s：watch 喺撳「出席」後 400ms 先開始採樣＋poll lag，屬量度偏移，唔係產品短咗；全部喺 ±5000ms 容差內。）

逐場 timeline 檢查全綠：格標題次序啱（男配→女配→女主→男主；音樂：新人→女歌手→男歌手）；提名 beat 唔重複字幕數 13／13／8／12（音樂女歌手格得 2 位 fellows，見下）；揭曉 4／4／3／4；玩家格卡片逐張 1→2→3→4（`cap_max` 計）；格標題嗰陣卡片收起（shown 0）；board 次序啱；結果卡＋報紙正常（declined：冇結果卡、log 標 skipped、有 declined 報紙）。

**截圖**（`qa208/shots208/`，全部目視核實過）：

- `film_nom_932_nom2.png`：字幕「入圍名單 2/4 · 最佳男配角／陸柏言：《歲歲平安》」，淨出 2 張卡（阿偉＋陸柏言），其餘兩張未出 ✓
- `film_nom_932_reveal.png`：「🏆 陸柏言憑《歲歲平安》得獎／你嘅《新春大吉》入圍到最後——差少少，下年再嚟。」＋彩紙，4 卡齊 ✓
- `film_won_932_reveal.png`：「🏆 得獎！／最佳男配角：《新春大吉》」＋彩紙，阿偉著燕尾服企台上 ✓
- `film_won_932_walkup.png`：「阿偉行上台，接過獎盃，高高舉起。」4 卡齊，阿偉卡金框 ✓（glamour overlay `.awd63-glamour.on` 採樣見過；fanfare flag `attempted` ✓）
- `music_gal_932_nom.png`：「入圍名單 1/2 · 最佳女歌手／藍若曦：《三年》」；**注意**：影相嗰刻卡片列係空——觸發影相快過 `syncCards` 下一個 rAF tick（字幕同步改、卡片 125ms 後先加 `show`），timeline 數據證實卡片之後逐張出，唔係產品問題
- `music_gal_932_lastcat.png`：尾格「—— 最佳男歌手 ——」✓
- `ad_dec_932_cat2.png`：「—— 最佳廣告女主角 ——」格標題，3 位提名人企台、卡片收起 ✓
- `film_skip_700_cat2_title.png`／`_result.png`：第 2 格標題＋即出結果卡 ✓

**目視觀察（留畀設計 review，唔係功能缺陷）**：宣佈嗰位「行前半步＋光池、其餘 alpha 0.45」喺靜態截圖睇唔出明顯分別（code 有，見 draw `nominee` branch：`drawFigure(s, i, { alpha: 0.45 })`＋`lightPool`；0.45 暗角喺細 px 公仔＋光猛舞台上面 subtle）。另：音樂女歌手格得 2 位 fellows（1991 年音樂池按性別分流得 2 女），屬數據現況，唔係 bug。

**第一輪實駕 1/5 嘅原因（全部係 drive 腳本／播種問題，唔係產品問題，已修）**：

1. open beat 字幕「—— 維港影藝獎 ——」俾分析計咗做格標題 → 格標題改準確匹配。
2. 提名／揭曉數數咗採樣樣本唔係唔重複字幕（同一 beat 卡片出現會多一個樣本；懸念「得獎者是……」含「得獎」）→ 改 `cap_max` 計唔重複字幕＋揭曉排除「得獎者是」。
3. 第 1 格係玩家格嗰陣提名數係 4，唔係 fellows 數 3 → `nom_n()` 按 focus／outcome 計。
4. gallery 夜嘅 focus 只係 `categories[0]` 兜底，唔係玩家格 → 玩家檢查只喺 focus outcome 係 won／nominated 嗰陣先驗。
5. walkup 檢查用「行上台」撞咗 comfort 句「下年，我要自己行上台。」→ 改用 walkup 獨有「接過獎盃」。
6. **won 播種贏唔到**：舊 seed（film_lead 2＋film_sup 1，fame 80／credit 60）base 只有 0.82（主軌 0.40＋作品 0.42，tag／repPower 皆 0），taste 最多 +0.05，永遠過唔到贏線 0.875——30 個 seed 全 nominated。改加跨媒介作品（tv_lead 2＋tv_sup 1＋ad_lead 1；ad_lead 池係空，但 tv 3 部夠 crossN≥2、crossQ 1.00）→ repPower +0.08，base ≈0.90，seed 1 即贏（`beatsTotal` 52250，同 §1 logic 表一致）。呢個係 drive 播種技巧，唔係產品改動。
7. attend 分支嘅截圖觸發曾經俾 `str.replace`（replace-all）誤寫成 decline 嗰組，第二輪重跑冇中途截圖；已修正。音樂觸發字串由「1/3 ·」改「· 最佳女歌手」（嗰格得 2 位）。
8. 中途 runtime restart 一次，中斷咗第二輪重跑（log 0 bytes、JSON 停留第一輪）；已完整重跑第三輪 5/5 PASS，JSON 係第三輪結果。

## §3 落地（統籌）

### Rebase 上 main `b7ddb37`（v207 NOTES）

- 分支舊 HEAD `fdf1c40`（base `a426947`）→ rebase 後 HEAD `3f7371b`（`d11d0f3`＋`47fff16`＋rebase fix `3f7371b`）。
- 衝突：index.html 1 處（註解插入撞位——v207 B2 將舞台註解由 480×360 改 480×432，v208 同位插入 `buildSlots208`／`buildCardsData208`；解法：保留 v208 兩個函數＋v207 嘅 432 註解，v208 嗰邊舊 360 註解棄用）＋5 個靜態測試共 10 個 hunk（全部係釘行行號漂移）。
- 測試 resync 方法：`qa208/resync208_rebase.py`——pristine main `b7ddb37` 同工作版 index.html 做 difflib 單次掃描 dict 查表（淨 +223 行，總行數 61491→61714），逐個釘行核實內容逐字相同（rom176 6 釘、travel114 COUNT 12／FREE 33／DEF／WRAPPER、tang DEF、gift185 總行數——全部 SAME，純漂移）。
- 唯一手動修正：tang171／tang173 嘅 openLoc DEF 斷言，label 改咗 56186 但 0-based index 漏咗改（`lines[55962]`→`lines[56185]`），commit `3f7371b`。

### 重驗（rebase 後，2026-11-14）

- 新測試：`node tests/test_awards208_logic.js` ALL PASS（35 項）；`python3 tests/test_awards208_static.py` ALL PASS（41 項）。
- 受影響靜態測試逐個覆驗：gift185／rom176／tang171／tang173／travel114／awards160_m4／m6／m9／awards177／178／182——全部 ALL PASS。
- 全套 `qa131/run_suite.sh`：基線 A（pristine worktree main `b7ddb37`，`qa208/suite208_base_rebased.txt`）**291 PASS／13 FAIL**；跑 B（工作版，`qa208/suite208_work_rebased.txt`）**293 PASS／13 FAIL**，FAIL 清單同基線逐項一致，**零回歸**（＋2 PASS 係 v208 兩個新測試檔）。
- 實駕重跑（`qa208/drive208.py`，同一腳本，rebase 後工作版）：**5/5 PASS**，0 pageerror／0 requestfailed。film nominated 50,135ms（預期 50,850）／film won 51,394ms（預期 52,250，強 seed fame 80／credit 60＋跨媒介作品，seed 1 即 won；walkup／glamour／fanfare 全部見到）／music gallery 33,024ms（預期 33,800）／ad declined 45,674ms（預期 46,500）／film skip 700 第 2 格撳跳過即完＋結果卡即出。`qa208/drive208.json`＋截圖已更新做呢輪結果。
