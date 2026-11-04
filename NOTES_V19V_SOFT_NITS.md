# v19v Soft≠PASS · 出圖 HOLD · 唔 publish

Phone web preview tip. Soft nits only, after v19u browser PASS. Parent tip stays `?v=19u` until coordinator OK. This PR does not merge and does not publish Pages. LIVE stays on 19u.

1. SAVE `starVolunteer_map_v19u` → `starVolunteer_map_v19v`（`refreshCopyPacksFromDisk` fetch `?v=` 跟住 bust）。Preview `?v=19v`.
2. `content/gigs_1988.json` 仍係 **3.2.3-soft**、n=137。只改 meta `counts.keyGigs` **76→66**，對齊 `isKeyGig: true` 實數。通告正文、閘、89–92 未動。
3. 人情債 id `debt_may_winter_makeup` 不變。玩家面債主 **化妝姐美兒**；seasonHint「冬天乾燥，美兒會提你買返支潤膚膏。」舊種子若仍寫 May，開手帳時改寫顯示。
4. 茶餐廳第一筆打聽（大堂飲茶聽八卦一定入帳；若先撳後巷／執漏，該筆亦入帳）寫入 `notebook.rumors`／傳聞 tab，state **剛聽聞**。之後仍跟刷新 B，唔係次次有新料。唔改銀碼、日、fame。
5. 地圖／loc toast 唔再因為身在地圖就 `closeSheet()`。只有呼叫方傳 `closeSheet:true` 先收 sheet。地圖上 sheet 開住時，票根 toast 移到分區掣下面，茶餐廳／事務所三個行動同「返地圖」保持可見。
6. Modal 豎滾選擇列：小賣／送禮 `.act` 喺 `#modal-inner` 內，右掣 `min-width:0`＋唔縮，避免尾掣被橫向裁走。Casting sheet 底掣仍喺 `#modal-btns`，未改。

6. Soft-PASS 圖：`assets/story/locs/bg_loc_cafe_cha.jpg`、`bg_loc_agency_ho.jpg` 掛上對應 Loc sheet（`?v=19v`），故事背景候選亦先搵 `assets/story/locs/`。HUD `hud_shell_bar` 同拍立得 `map_polaroid_frame` 換輕量檔，CSS `?v=16` → `?v=19v`。相井透明。無 C 閘／通告正文改動。

7. Phase 2 deepen Soft（mock only）：手動拼合三對（確認對話；對得上先出合成卡同「啪！蓋個印…」；對唔上「牛頭唔搭馬嘴」）。今季催收卡＋模糊債語。罰只係 toast 同「人情壓力」顯示，唔寫壓力閘、唔鎖通告。弱標籤係手帳暗紋約 8%（捱得／識做等），唔出標籤列表、唔出工程 id。債主維持 **化妝姐美兒**。A/B 仍係金龍｜手動｜模糊債｜淡入｜推門｜刷新 B。

C1–C5 閘、硬鎖、看板分級、通告 JSON 內容（除 keyGigs 數字）未改。

Soft≠PASS. 出圖 HOLD. 唔 publish. 唔 merge.
