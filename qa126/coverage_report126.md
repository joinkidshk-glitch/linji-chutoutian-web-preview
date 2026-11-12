# v20a126 情緒覆蓋率報告

來源：`linji-expression-inventory/work/lines_classified.json`（2644 行）× `assets/story/fullbody/` 目錄檔名（146 張，含新 6 張）。
口徑同 v106/v107：精確覆蓋＝該角非 neutral 對白入面，類別有同名表情資產嘅句數。

## 總覽

- 名冊非 neutral 句精確覆蓋：**483/593 = 81.5%**（v123：458/593＝77.2%）

- 阿偉 s1：**188/188＝100.0%**（v123：188/188＝100%）

- 阿偉 s2：**184/188＝97.9%**（v123：184/188＝97.9%）

- 阿偉 s3：**184/188＝97.9%**（v123：184/188＝97.9%）


## 新圖 6 張各自對應句數（全部 >0，唔係死圖）

| 新資產 | 對應分類句數 |
|---|---:|
| fong_siulung_smile.webp | 5 |
| pang_siuki_serious.webp | 4 |
| gu_mingfai_smile.webp | 4 |
| yip_manji_serious.webp | 4 |
| lan_ruoxi_shy.webp | 4 |
| ching_tinlok_sad.webp | 4 |

## 逐角表（有變動嘅角）

| 角 | 非neutral | 精確覆蓋 | 覆蓋率 | 有資產類別（除base） | 缺資產類別（句數） |
|---|---|---|---|---|---|
| fong_siulung | 8 | 5 | 62.5% | serious, smile | angry(1)、sad(2) |
| pang_siuki | 29 | 26 | 89.7% | serious, shy, smile, surprise | sad(3) |
| gu_mingfai | 22 | 17 | 77.3% | sad, serious, smile | angry(1)、shy(3)、think(1) |
| yip_manji | 19 | 14 | 73.7% | sad, serious, smile | angry(2)、shy(1)、surprise(2) |
| lan_ruoxi | 11 | 9 | 81.8% | sad, shy, smile | serious(1)、think(1) |
| ching_tinlok | 29 | 26 | 89.7% | angry, sad, serious, smile | shy(1)、surprise(1)、think(1) |

## 殘留缺口（零精確覆蓋嘅角）

- **cheng_william**：0/2；缺 serious(1)、shy(1)；有資產 （只有 base）
- **extra_ad_fen**：0/9；缺 sad(9)；有資產 （只有 base）
- **kwan_hoimei**：0/1；缺 serious(1)；有資產 （只有 base）
- **mok_siufai**：0/1；缺 sad(1)；有資產 （只有 base）
- **uncle_kim**：0/2；缺 happy(1)、serious(1)；有資產 （只有 base）

## 其他值得注意嘅殘留缺口（非零但未補；最大單項 ≤5 句）

- chow_choiyi：8/13（61.5%）；缺 angry(2)、sad(3)
- ko_chunkit：21/28（75.0%）；缺 sad(3)、shy(1)、think(3)

## 數據註

- 阿偉 s2/s3 精確覆蓋剩 angry 4 句——但 runtime 候補鏈（dlg106Candidates）s2/s3 angry 會經跨階段後備攞到 v123 新出嘅 `awi_angry.webp`，實際顯示 100%，唔會退 base。

- extra_ad_fen 嘅「sad」9 句經 v106 查證係旁白假陽性（同一句旁白重複），唔使補圖；本表沿用 v106 口徑，佢仍列零覆蓋。

- 全局升幅 +25 句（458→483）：fong happy 5、pang serious 4、gu happy 4、yip serious 4、lan shy 4、ching sad 4。

- 593 分母核對（v125 更正數字）：CHOICE47／WF3／COMMIT48 嘅 text beats（真正唔顯示嘅 51 句＋resultBeats 35 句，連 WF4 intro／送別計 73–76 句）逐句對過 `lines_classified.json`（2,644 行）——**0 句命中**，即 593 分母從來唔包呢批，v125 令佢哋顯示到亦唔影響覆蓋率，唔使改分母。
