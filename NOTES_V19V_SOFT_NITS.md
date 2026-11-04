# v19v Soft≠PASS · 出圖 HOLD · 唔 publish

Phone web preview tip. Soft nits only, after v19u browser PASS. Parent tip stays `?v=19u` until coordinator OK. This PR does not merge and does not publish Pages. LIVE stays on 19u.

1. SAVE `starVolunteer_map_v19u` → `starVolunteer_map_v19v`（`refreshCopyPacksFromDisk` fetch `?v=` 跟住 bust）。Preview `?v=19v`.
2. `content/gigs_1988.json` 先把 meta `counts.keyGigs` **76→66**（對齊 `isKeyGig: true`）。其後同一 PR 換上 Pack B **3.2.4-soft**（見下）。89–92 同 C 閘未動。
3. 人情債 id `debt_may_winter_makeup` 不變。玩家面債主 **化妝姐美兒**；seasonHint「冬天乾燥，美兒會提你買返支潤膚膏。」舊種子若仍寫 May，開手帳時改寫顯示。
4. 茶餐廳第一筆打聽（大堂飲茶聽八卦一定入帳；若先撳後巷／執漏，該筆亦入帳）寫入 `notebook.rumors`／傳聞 tab，state **剛聽聞**。之後仍跟刷新 B，唔係次次有新料。唔改銀碼、日、fame。
5. 地圖／loc toast 唔再因為身在地圖就 `closeSheet()`。只有呼叫方傳 `closeSheet:true` 先收 sheet。地圖上 sheet 開住時，票根 toast 移到分區掣下面，茶餐廳／事務所三個行動同「返地圖」保持可見。
6. Modal 豎滾選擇列：小賣／送禮 `.act` 喺 `#modal-inner` 內，右掣 `min-width:0`＋唔縮，避免尾掣被橫向裁走。Casting sheet 底掣仍喺 `#modal-btns`，未改。

6. Soft-PASS 圖：`assets/story/locs/bg_loc_cafe_cha.jpg`、`bg_loc_agency_ho.jpg` 掛上對應 Loc sheet（`?v=19v`），故事背景候選亦先搵 `assets/story/locs/`。HUD `hud_shell_bar` 同拍立得 `map_polaroid_frame` 換輕量檔，CSS `?v=16` → `?v=19v`。相井透明。無 C 閘／通告正文改動。

7. Phase 2 deepen Soft（mock only）：手動拼合三對（確認對話；對得上先出合成卡同「啪！蓋個印…」；對唔上「牛頭唔搭馬嘴」）。今季催收卡＋模糊債語。罰只係 toast 同「人情壓力」顯示，唔寫壓力閘、唔鎖通告。弱標籤係手帳暗紋約 8%（捱得／識做等），唔出標籤列表、唔出工程 id。債主維持 **化妝姐美兒**。A/B 仍係金龍｜手動｜模糊債｜淡入｜推門｜刷新 B。

8. Pack B：`content/gigs_1988.json` 換成 **3.2.4-soft**，SHA256 `0f18fe14c389c42aface4c01692c4addd39657303b5c2b4ce0d9cdf80eb6e93c`，n=137，`counts.keyGigs`=66，`isKeyGig` true=66，`castWindow` 無。對照 pre 3.2.3-soft（SHA `cfc72fe8…`）只差 `genreLabel`／中階 `limits`／中階 `producer` 同 meta。pay／req／loc／season／storyKeys 等未改。Changelog：`content/CHANGELOG_GIGS_1988_3_2_4_SOFT.md`（SHA256 `d68526c8…`）。SAVE 仍 `starVolunteer_map_v19v`。

9. `bg_loc_agency_ho.jpg` 換 cork 輕改稿，SHA256 `43acc91f4cfd0851480a12185346929facb37cf50f81bfcc9d53d3acf7270369`，720×1280。路徑同 `?v=19v`，SAVE 不變。未接 era_stars。

10. Phase 3 Soft（mock）：四人遠觀純文字＋音（`luk_baakyin`／`liu_bingxing`／`ngai_wingnaam`／`yip_manji`），唔掛剪影。通告卡只 ready「可接通告／接通告」或 locked「暫未能報＋離開」。未合條件撳掣會 shake，toast「條件未合」加副行。`isSoftTryGig` 恆 false。唔改 `canAudition` 門檻、唔改 gigs JSON。無 era_stars 檔可抄。

C1–C5 閘、硬鎖門檻、看板分級邏輯未改。89–92 HOLD。gigs 仍 **3.2.4-soft**。

Soft≠PASS. 出圖 HOLD. 唔 publish. 唔 merge.
