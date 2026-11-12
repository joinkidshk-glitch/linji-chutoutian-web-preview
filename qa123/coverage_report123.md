# v20a123 情緒覆蓋率報告

來源：`linji-expression-inventory/work/lines_classified.json`（2644 行）× `assets/story/fullbody/` 目錄檔名（130 張，含新 12 張）。
口徑同 v106/v107：精確覆蓋＝該角非 neutral 對白入面，類別有同名表情資產嘅句數。

## 總覽

- 名冊非 neutral 句精確覆蓋：**458/593 = 77.2%**（v107：439/593＝74.0%）

- 阿偉 s1：**188/188＝100.0%**（v107：184/188＝97.9%）

- 阿偉 s2：**184/188＝97.9%**（v107：123/188＝65.4%）

- 阿偉 s3：**184/188＝97.9%**（v107：123/188＝65.4%）


## 新圖 12 張各自對應句數（全部 >0，唔係死圖）

| 新資產 | 對應分類句數 |
|---|---:|
| awi_s2_surprise.webp | 27 |
| awi_s2_sad.webp | 20 |
| awi_s2_shy.webp | 14 |
| awi_s3_surprise.webp | 27 |
| awi_s3_sad.webp | 20 |
| awi_s3_shy.webp | 14 |
| awi_angry.webp | 4 |
| chung_choning_think.webp | 4 |
| chung_choning_smile.webp | 3 |
| ho_sang_angry.webp | 4 |
| liu_bingxing_shy.webp | 2 |
| pang_siuki_surprise.webp | 2 |

## 逐角表（有變動嘅角）

| 角 | 非neutral | 精確覆蓋 | 覆蓋率 | 有資產類別（除base） | 缺資產類別（句數） |
|---|---|---|---|---|---|
| awi | 188 | 188 | 100.0% | angry, sad, serious, shy, smile, surprise, think | — |
| chung_choning | 22 | 21 | 95.5% | sad, serious, smile, think | angry(1) |
| ho_sang | 33 | 33 | 100.0% | angry, sad, serious, smile, think | — |
| liu_bingxing | 27 | 23 | 85.2% | serious, shy, smile | sad(1)、surprise(2)、think(1) |
| pang_siuki | 29 | 22 | 75.9% | shy, smile, surprise | sad(3)、serious(4) |

## 殘留缺口（零精確覆蓋嘅角）

- **cheng_william**：0/2；缺 serious(1)、shy(1)；有資產 （只有 base）
- **extra_ad_fen**：0/9；缺 sad(9)；有資產 （只有 base）
- **fong_siulung**：0/8；缺 angry(1)、happy(5)、sad(2)；有資產 serious
- **kwan_hoimei**：0/1；缺 serious(1)；有資產 （只有 base）
- **mok_siufai**：0/1；缺 sad(1)；有資產 （只有 base）
- **uncle_kim**：0/2；缺 happy(1)、serious(1)；有資產 （只有 base）

## 其他值得注意嘅殘留缺口（非零但未補；最大單項 ≤5 句）

- fong_siulung：0/8（0.0%）；缺 angry(1)、happy(5)、sad(2)
- pang_siuki：22/29（75.9%）；缺 sad(3)、serious(4)
- gu_mingfai：13/22（59.1%）；缺 angry(1)、happy(4)、shy(3)、think(1)
- yip_manji：10/19（52.6%）；缺 angry(2)、serious(4)、shy(1)、surprise(2)
- lan_ruoxi：5/11（45.5%）；缺 serious(1)、shy(4)、think(1)
- ching_tinlok：22/29（75.9%）；缺 sad(4)、shy(1)、surprise(1)、think(1)
- chow_choiyi：8/13（61.5%）；缺 angry(2)、sad(3)
- ko_chunkit：21/28（75.0%）；缺 sad(3)、shy(1)、think(3)

## 數據註

- 阿偉 s2/s3 精確覆蓋剩 angry 4 句——但 runtime 候補鏈（dlg106Candidates）s2/s3 angry 會經跨階段後備攞到新出嘅 `awi_angry.webp`，實際顯示 100%，唔會退 base。

- extra_ad_fen 嘅「sad」9 句經 v106 查證係旁白假陽性（同一句旁白重複），唔使補圖；本表沿用 v106 口徑，佢仍列零覆蓋。

- 全局升幅 +19 句（439→458）：awi_angry 4、chung think 4＋happy 3、ho angry 4、liu shy 2、pang surprise 2；s2/s3 六張唔計入全局（s1 早已有 surprise／sad／shy）。
