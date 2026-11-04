Soft≠PASS｜Pack favor／rumor 收斂｜對齊 3.2.4-soft｜經 qwen3.7-max｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD

經 Qwen qwen3.7-max

# PLAN_GIG_1988_FAVOR_RUMOR_FILL_REMAIN21_v1

**Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD**

## 範圍
本計劃針對《臨記出頭天》1988年初階通告數據，專門處理剩餘 21 則 favor 同 rumor 皆空嘅初階 gig。目標係補全數據結構，確保叙事同系統邏輯完整，同時嚴格遵守玩家面顯示規範。

## 對照 3.2.4
- **對齊 gigs 3.2.4-soft n=137**：本次填空後，1988 年 gig 總數將達 137 則，全數具備 nonempty favor 同 rumor。
- **Soft A/B 處理**：唔使區分 Soft A/B。統籌已指示選填收齊，沿 Soft A 模式處理；2B 階段嘅 `agency_ho` 僅限於高階 gig，初階嚴格禁用。

## 餘 21 清單摘要
以下為 21 則初階 gig 嘅 favor target 同 rumor 分配摘要。Favor target 全數映射至對應 `crew_{loc}`，rumor 傾向季節對齊並確保 16 個 existing keys 全數覆蓋。

| gig_id | season | loc | favor target | rumor_key |
| :--- | :---: | :--- | :--- | :--- |
| gig_1988_mtv_wanchai_spring | 春 | rec_wanchai | crew_rec_wanchai | rumor_liu_bing_sing_88_spring |
| gig_1988_rec_star_spring_low | 春 | rec_star | crew_rec_star | rumor_mak_chun_tung_88_spring |
| gig_1988_rec_hk_summer | 夏 | rec_hk | crew_rec_hk | rumor_ngai_wing_naam_88_summer |
| gig_1988_rec_star_summer | 夏 | rec_star | crew_rec_star | rumor_chai_chun_hoi_88_summer |
| gig_1988_ad_central_summer_low | 夏 | ad_central | crew_ad_central | rumor_env_chai_chun_hoi |
| gig_1988_film_harbour_summer_low | 夏 | film_harbour | crew_film_harbour | rumor_env_ngai_wing_naam |
| gig_1988_film_lion_summer_low | 夏 | film_lion | crew_film_lion | rumor_env_liu_bing_sing |
| gig_1988_tvb_harbour_summer_low | 夏 | tvb_harbour | crew_tvb_harbour | rumor_env_mak_chun_tung |
| gig_1988_tvb_longmen_summer_low | 夏 | tvb_longmen | crew_tvb_longmen | rumor_env_luk_pak_yin |
| gig_1988_ad_central_autumn_low | 秋 | ad_central | crew_ad_central | rumor_yip_man_chi_88_autumn |
| gig_1988_film_cotton_autumn_low | 秋 | film_cotton | crew_film_cotton | rumor_lok_ka_sing_88_autumn |
| gig_1988_film_harbour_autumn_low | 秋 | film_harbour | crew_film_harbour | rumor_env_yip_man_chi |
| gig_1988_rec_star_autumn_low | 秋 | rec_star | crew_rec_star | rumor_env_lok_ka_sing |
| gig_1988_tvb_kowloon_autumn_low | 秋 | tvb_kowloon | crew_tvb_kowloon | rumor_env_pang_siu_kei |
| gig_1988_tvb_longmen_autumn_low | 秋 | tvb_longmen | crew_tvb_longmen | rumor_chai_chun_hoi_88_summer |
| gig_1988_mtv_wanchai_winter | 冬 | rec_wanchai | crew_rec_wanchai | rumor_pang_siu_kei_88_winter |
| gig_1988_ad_adm_winter_low | 冬 | ad_adm | crew_ad_adm | rumor_luk_pak_yin_88_winter |
| gig_1988_ad_central_winter_low | 冬 | ad_central | crew_ad_central | rumor_env_pang_siu_kei |
| gig_1988_film_lion_winter_low | 冬 | film_lion | crew_film_lion | rumor_env_luk_pak_yin |
| gig_1988_rec_star_winter_low | 冬 | rec_star | crew_rec_star | rumor_env_lok_ka_sing |
| gig_1988_tvb_harbour_winter_low | 冬 | tvb_harbour | crew_tvb_harbour | rumor_ngai_wing_naam_88_summer |

## favor 規則
- **數值與目標**：初階 favor value 固定為 `1`；target 嚴格使用 `crew_{loc}`（例如 `loc=rec_hk` 則 target 為 `crew_rec_hk`）。
- **初階禁令**：絕對禁止喺初階 gig 使用 `agency_ho`、`ho_manager` 或任何 `star_*` 作為 target。
- **內部與玩家面**：內部數據結構仍保留 `agency_ho` 概念，但經理人對外顯示統一為「何生」，玩家面絕唔會出現 "Ho 哥" 或相關工程詞。

## rumor 規則
- **數量限制**：每則 gig 恰好用 1 條 rumorKey，唔准多填或留空。
- **Key 來源**：只用既有嘅 16 個 rumor keys，唔新增任何 key。
- **季節對齊**：優先參考 `seasonHint` 進行分配，確保叙事氛圍同季節吻合；部分 key 會跨季節復用以填滿 21 個 gig，但必須保證 16 個 unique keys 至少出現 1 次。

## Acceptance
- **數據完整性**：nonempty favor + rumor 嘅 gig 總數必須達到 137（即 `n=137`）。
- **覆蓋率**：unique rumor keys 使用數量必須 `≥16`。
- **玩家面合規 (bannedScan = 0)**：
  - 零 "Ho 哥"（對外只顯示何生）。
  - 零 真藝名（只使用角色名或代稱）。
  - 零 工程詞（嚴禁出現 flag、gate、week-gate、SHA 等字眼）。
- **狀態標記**：確認 Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD 已正確套用。

## 流水線
1. **數據注入**：將上述 21 則 gig 嘅 favor target 同 rumor key 寫入 JSON 數據庫。
2. **靜態掃描**：運行 bannedScan 腳本，確保玩家面文本無違規詞彙。
3. ** uniqueness 校驗**：跑一次 count distinct rumor_key，確認結果 ≥16。
4. **統籌覆核**：提交 PR 並標記相關 HOLD 狀態，等待統籌 final check。

## Out of scope
- **唔改** 任何 pay、req、loc、season、文案、isKeyGig 或 boardHookMode。
- **唔處理** 高階 gig 嘅 favor 調整（高階沿用 Soft A 2B agency_ho 邏輯）。
- **唔涉及** 89–92 年份嘅數據變動（維持 HOLD 狀態）。

## 擬轉統籌一句
「21 個初階 gig 嘅 favor 同 rumor 已按季節 hint 填齊，16 個 rumor key 全數覆蓋，玩家面 scan 過無 Ho 哥同工程詞，請 check 下個 PR，記得呢批依然係 Soft≠PASS 同埋出圖 HOLD 狀態。」
