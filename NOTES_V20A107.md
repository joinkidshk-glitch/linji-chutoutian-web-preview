# v20a107 表情補圖包：8 張新表情入庫（fix2）

底本：生成工人 fix2 補單 8 張（`linji-fullbody-batch/notes_fix2.md`：阿偉 s2/s3 think、蘇芷茵 smile、張子駿 serious、何生 sad、高文瀚 serious、鄧麗萍 serious、周采兒 think；QC pass 7／marginal 1——周采兒 think 眉帶懷疑味，收做「懷疑地諗線索」）。
紀律：SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全冇郁；**index.html 零改動**（git diff 0 行）；content JSON 一律唔改。新資產用既有版本參數 `?v=20a106`（新檔名本身就係新 URL，唔使另開版本）。

## 逐項處置

- **焗邊 8 張（跟 v106 同一方法，唔係第二套）**：米白光邊 RGB(243,233,210) 焗入圖本身；alpha 剪影（>128＋填洞）圓盤膨脹取「膨脹區−原剪影」邊帶、高斯柔化（sigma＝0.7×r/18）、畫布四邊各擴 r、原圖置中原樣貼上（唔混色，內部唔染邊色）；半徑 r＝round(3×原生高/422)，r 17–22。逐張驗證全 PASS（尺寸＝原圖+2r、邊帶米白命中 ≥99.9%、內部大差異 0.000%、單一邊帶 far_cream_px＝0、輸入外框透明即冇預焗邊）。腳本＋原始數據：`qa107/bake107.py`／`qa107/bake_results107.json`；深底拼圖目檢：`qa107/spotcheck_baked107_dark.png`（8 張單一米白邊，冇重邊冇光暈）。
- **入庫**：焗邊版入 `assets/story/fullbody/`，檔名跟生成清單一字唔差；fullbody 總數 88→96。`linji-fullbody-batch/manifest.json` 已合併 fix2 8 條（notes 加 `[v20a107]` 標記），總數 96；BATCH_NOTES.md 已加 v107 段落。

| 檔名 | 原尺寸 | 焗邊後尺寸 | r | 大小 (bytes) | 邊色命中率 | 內部大差異 | 驗證 |
|---|---|---|---|---|---|---|---|
| awi_s2_think.webp | 815×3030 | 859×3074 | 22 | 193678 | 99.97% | 0.000% | PASS |
| awi_s3_think.webp | 810×3036 | 854×3080 | 22 | 179496 | 99.94% | 0.000% | PASS |
| so_jiyan_smile.webp | 704×2600 | 740×2636 | 18 | 297704 | 99.99% | 0.000% | PASS |
| cheung_tsijun_serious.webp | 767×2719 | 805×2757 | 19 | 236066 | 99.94% | 0.000% | PASS |
| ho_sang_sad.webp | 857×2424 | 891×2458 | 17 | 182570 | 99.96% | 0.000% | PASS |
| gao_wenhan_serious.webp | 907×2473 | 943×2509 | 18 | 229338 | 100.00% | 0.000% | PASS |
| tang_laiping_serious.webp | 883×2727 | 921×2765 | 19 | 155594 | 99.99% | 0.000% | PASS |
| chow_choiyi_think.webp | 831×2739 | 869×2777 | 19 | 258392 | 99.99% | 0.000% | PASS |

合計 8 張，1,732,838 bytes。

- **程式：零改動，核實咗三點**：① `DLG106_CAT_TO_EXPR` 已認齊四個映射（think→think、happy→smile、serious→serious、sad→sad），`dlg106Candidates` 候補鏈首選即新圖（唔退 base）；② 阿偉階段判定跟現行 `enc79PlayerTier`（tier 2→awi_s2、tier 3→awi_s3），s1 回歸不變；③ 真實對白句經 `dlg106ResolveCategory`（map lookup）判返對應分類——C1 阿偉 think 句「呢兩條路真係各有千秋，要諗清楚先好決定。」→think，其餘七類各一句亦驗過。證據：`tests/test_dlg107_logic.js` 全 PASS。
- **manifest 記法分裂（老實註）**：v106 嗰 6 條 s2/s3（base/smile/serious）記做 speakerId=awi、expr=s2_smile 式；fix2 8 條記做 speakerId=awi_s2/awi_s3、expr=think。合併時冇改寫 v106 舊條目；覆蓋重計階段覆蓋按檔名派生資產集（檔名先係解析器 ground truth），唔依賴呢個分裂嘅記法。

## 覆蓋率前後對照（同 v106 口徑重計，`qa107/coverage107.py`＋`qa107/coverage_report107.md`）

| 指標 | v106 | v107 | 變化 |
|---|---|---|---|
| 全局精確覆蓋（名冊非 neutral） | 403/593＝68.0% | **439/593＝74.0%** | +36 句 |
| 阿偉 s1 | 184/188＝97.9% | 184/188＝97.9% | 不變 |
| 阿偉 s2 | 60/188＝31.9% | **123/188＝65.4%** | +63 句（think） |
| 阿偉 s3 | 60/188＝31.9% | **123/188＝65.4%** | +63 句（think） |
| 蘇芷茵 | 16/29＝55.2% | **28/29＝96.6%** | +12 句（happy） |
| 張子駿 | 0/10＝0% | **6/10＝60.0%** | +6 句（serious），脫離零覆蓋 |
| 何生 | 23/33＝69.7% | **29/33＝87.9%** | +6 句（sad） |
| 高文瀚 | 0/4＝0% | **4/4＝100%** | +4 句（serious），脫離零覆蓋 |
| 鄧麗萍 | 0/4＝0% | **4/4＝100%** | +4 句（serious），脫離零覆蓋 |
| 周采兒 | 4/13＝30.8% | **8/13＝61.5%** | +4 句（think） |

數字全部由數據重計得出，唔係硬抄：全局升幅 36＝其餘 6 張新圖對應句數（12+6+6+4+4+4）；阿偉 think 63 句全局早已有 s1 圖，只計階段升幅。零精確覆蓋角由 9 個減到 6 個。

## 測試證據

- 新增守門：`tests/test_dlg107_static.py`（基線不變、8 張存在＋WebP 檔頭＋總數 96、每張對應句數、缺檔／改錯名／空集反證＋真磁碟 temp 目錄負向測試、焗邊報告數值對照）＋`tests/test_dlg107_logic.js`（候補鏈首選、階段判定 tier 2/3/0、真實對白句分類、tier 切換／未知講者／垃圾輸入反證）——全 PASS。
- 全套 A/B：work107 **136 PASS／12 FAIL**，pristine 基線（v106 後 main，8d19640）**134 PASS／12 FAIL**，FAIL 清單逐字相同（12 個全屬已知環境性 static FAIL，同 v106 基線一致），**零新增 FAIL**；差額 +2 PASS 就係新增 dlg107 兩檔。證據：`qa107/suite_work107.txt`／`qa107/suite_baseline107.txt`。
- index.html 零改動（git diff 0 行），故無需重抽 main script 做 node --check（v106 已驗；本包冇掂過佢）。

## 未達標位／殘留缺口（老實申報）

- **零精確覆蓋角仲有 6 個**：鄭威廉 cheng_william（0/2：serious 1、shy 1）、芬姐 extra_ad_fen（0/9：sad 9——經 v106 查證係旁白假陽性，唔使補圖）、方小龍 fong_siulung（0/8：happy 5、sad 2、angry 1）、關海媚 kwan_hoimei（0/1：serious 1）、莫少輝 mok_siufai（0/1：sad 1）、金九 uncle_kim（0/2：happy 1、serious 1）。留返下次。
- **其他未補缺口（逐角句數，見 coverage_report107.md）**：葉敏芝 yip_manji serious 4、彭少祺 pang_siuki serious 4、顧明輝 gu_mingfai happy 4、魏詠男 ngai_wingnaam serious 3＋happy 3、林曉晴 lin_hiu serious 3＋think 3、鍾楚凝 chung_choning think 4＋happy 3、陸柏言 luk_baakyin happy 4、阿偉 s2/s3 surprise 27＋sad 20＋shy 14＋angry 4（階段覆蓋仲係 65.4%，未齊）、蘇芷茵 surprise 1、張子駿 think 2、周采兒 sad 3、何生 angry 4。
- **隨機事件 WF4 未套新呈現**：v106 已列，今包範圍外，維持不變。
- **周采兒 think 係 marginal**：眉角帶懷疑味，收做「懷疑地諗線索」；鄧麗萍 serious 神態偏凌厲但屬人設範圍內，收 pass。兩張已喺生成筆記老實寫明。

## 部署核實＋實駕結果（待補）
