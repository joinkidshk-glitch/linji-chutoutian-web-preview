Soft≠PASS｜Pack C/D 議拍｜1988 only｜對照 Soft 3.2.5-soft n=137 SHA 0390b091｜經 qwen3.7-max｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜castWindow HOLD（現況）｜唔改 gigs 除非用戶另開閘

# PLAN_GIG_1988_PACK_CD_BOARD_v1

## 現況（Pack B Soft 已完成項）

- **Soft 3.2.4-soft Pack B SHA 0f18fe14**：0 新槽 n=137；genreLabel OOV 95→0；中階 limits 0→20/45；中階 producer 11→27/45（≥30%）；counts.keyGigs meta 76→66；castWindow HOLD；roles[] 未開。
- **Soft 3.2.5-soft favor/rumor SHA 0390b091**：餘 21 初階 favorDelta/rumorKeys 收齊；favorDelta nonempty 137；初階 agency_ho=0；unique rumorKeys 16。
- **PLAN_GIG_1988_PACK_B_MV3_v1**：階 B＋Casting 階 C；用戶拍板揀咗「0 新槽」同「castWindow HOLD」同 OOV remap 現詞庫（即當年方案 A「mid +8」未選）。
- **Casting loc×季×初中高**：11 loc × 4 季 × 3 階 = 132 格；現行 3.2.5 缺邊=0（滿格）；127 格只有 1 則；類型跟 loc 綁定（ad_*=廣告、film_*=電影、rec_*=唱片、tvb_*=綜藝/電視劇）。
- **中階類型仍偏薄**：綜藝 6／電視劇 7／廣告 8／電影 12／唱片 12。
- **高階數據**：limits 43/46；producer 41/46；無 castWindow 欄；無 roles[]。

## 階 C 已完成／階 D 候選範圍定義（1988 only）

- **階 C 已完成**：Casting 矩陣（11 loc × 4 季 × 3 階 = 132 格）已達滿格（缺邊=0），類型與 loc 綁定邏輯已確立，初階 favor/rumor 亦已於 3.2.5-soft 收齊。
- **階 D 候選範圍（Pack C）**：聚焦於 1988 年背景下，中階數據密度提升（densify）、高階數值合理性 QA、castWindow 時間窗邏輯取捨，以及 roles[] 多人組隊機制之 MVP 評估。本階段嚴格限定於 1988 only，唔涉後續年份擴展。

## Pack C/D 議拍板 A/B 選項

### D1：中階數據擴充策略
- **選項 A**：mid +8（當年 Pack B 方案 A 未選，新增 8 個中階槽位）。
- **選項 B**：0 新槽只 densify／QA（維持 n=137，針對偏薄類型如綜藝/電視劇作內容深化與 QA）。
- **利弊**：選項 A 可快速補齊中階薄弱類型，但會打破用戶先前「0 新槽」的拍板共識；選項 B 維持現有數據規模，專注提升現有數據密度與歷史吻合度，符合先前共識。
- **對 n／UI／流水線影響**：選項 A 會令 n 增加，UI 需處理新槽位，流水線需重新跑 gen；選項 B 維持 n=137，UI 無大改，流水線只需跑 QA patch。
- **建議預設**：**選項 B**（0 新槽只 densify／QA）。

### D2：castWindow 時間窗邏輯
- **選項 A**：castWindow HOLD（維持現況，唔開新欄）。
- **選項 B**：抽樣 10 則（針對高階或特定 loc 抽樣補齊 castWindow 欄位）。
- **利弊**：選項 A 維持現狀，開發成本低，且 1988 年臨記通告未必有精確數位化時間窗概念；選項 B 可測試時間窗邏輯，但需額外定義歷史時間窗格式，且樣本數少未必具代表性。
- **對 n／UI／流水線影響**：選項 A 對 n/UI 無影響；選項 B 需 UI 新增時間窗顯示，流水線需補齊 10 則數據並驗證格式。
- **建議預設**：**選項 A**（castWindow HOLD）。

### D3：高階 limits／producer 數據品質
- **選項 A**：高階 limits／producer 抽樣 QA（針對 limits 43/46 及 producer 41/46 進行人工或 LLM 抽樣審查）。
- **選項 B**：暫不動（接受現行數值，唔作額外 QA）。
- **利弊**：選項 A 可確保高階數據的合理性與 1988 歷史吻合度，避免 OOV 或極端數值；選項 B 節省時間，但可能留有未發現的邏輯瑕疵。
- **對 n／UI／流水線影響**：選項 A 唔改變 n，UI 無影響，流水線需增加抽樣 review 環節；選項 B 無影響。
- **建議預設**：**選項 A**（高階 limits／producer 抽樣 QA）。

### D4：roles[] 多人組隊機制
- **選項 A**：roles[] 仍 HOLD（維持現況，唔開新欄）。
- **選項 B**：開 MVP 單角色（新增 roles[] 欄位，支援單一角色 MVP 結構）。
- **利弊**：選項 A 維持現狀，避免過度設計，1988 現況無此欄；選項 B 可為未來多人組隊鋪路，但強行開 MVP 會增加 schema 複雜度，且現階段無實際使用場景。
- **對 n／UI／流水線影響**：選項 A 無影響；選項 B 需改 DB schema、UI 需支援角色列表，流水線需重構相關 gen 邏輯。
- **建議預設**：**選項 A**（roles[] 仍 HOLD）。

## 建議預設組合總結

綜合上述分析，本輪 Pack C/D 建議預設組合為：
**D1(0 新槽只 densify/QA) ＋ D2(castWindow HOLD) ＋ D3(高階抽樣 QA) ＋ D4(roles[] 仍 HOLD)**。
此組合最大程度尊重用戶先前拍板共識，聚焦於 1988 數據品質打磨，唔引入非必要之結構性改動。

## 若揀 mid+8：新槽必填欄重申

若用戶最終改揀 D1 選項 A（mid +8），必須嚴格遵守以下新槽必填欄規範：
- **必填**：workTitle / genreLabel (ALIGN§3) / roleLabel (≤8) / director / payExact / breachFee / applyDeadlineDays / req / stars=3 / tier=中。
- **可選**：producer / limits。
- **favor/rumor**：跟 Pack A 規則後補，且 favor target 必須對準 agency_ho（留意初階 agency_ho=0 之現況）。

## 流水線

1. **拍板**：用戶確認本檔 A/B 選項。
2. **qwen gen**：根據拍板結果，由 qwen3.7-max 生成對應 patch 數據。
3. **HK review**：港式書面語及 1988 歷史背景審查。
4. **Soft patch**：合併至 Soft JSON 結構。
5. **tester**：自動化與手動驗證。
6. **用戶 OK 先寫 Soft JSON**：確認無誤後寫入。
7. **仍 Soft≠PASS 唔 tip**：嚴格執行硬閘，未達標絕唔 tip LIVE。

## 驗收清單

- [ ] 確認 D1-D4 選項拍板結果。
- [ ] 確認 n=137 維持不變（若揀 D1 選項 B）。
- [ ] 確認高階 limits/producer 抽樣 QA 完成且無 OOV。
- [ ] 確認 castWindow 與 roles[] 維持 HOLD。
- [ ] 確認 favor target agency_ho 邏輯正確。
- [ ] 確認流水線各節點簽核。

## Out of Scope

- **89–92 HOLD**：本檔僅限 1988 only，唔涉 1989-1992 年份。
- **唔 tip LIVE**：嚴格執行 Soft≠PASS 硬閘。
- **出圖 HOLD**：本輪唔處理任何圖像生成或 UI 出圖。
- **改 LIVE**：唔改動現有 LIVE 環境配置。
- **禁真藝名入玩家面**：嚴格過濾，確保玩家面唔會出現真實藝人姓名。
- **禁「Ho 哥」字眼**：玩家面一律稱「何生」，絕唔使用「Ho 哥」。
- **本檔唔寫庫**：本規劃檔僅作議拍板用途，唔直接寫入資料庫，需經流水線轉 Soft JSON。