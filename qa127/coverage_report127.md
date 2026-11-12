# v20a127 情緒覆蓋率報告

來源：`linji-expression-inventory/work/lines_classified.json`（2644 行）× `assets/story/fullbody/` 目錄檔名（168 張，含新 22 張）。
口徑同 v106/v107：精確覆蓋＝該角非 neutral 對白入面，類別有同名表情資產嘅句數。

## 總覽

- 名冊非 neutral 句精確覆蓋：**515/593 = 86.8%**（v126：483/593＝81.5%）

- 阿偉 s1：**188/188＝100.0%**（v126：188/188＝100%）

- 阿偉 s2：**184/188＝97.9%**（v126：184/188＝97.9%）

- 阿偉 s3：**184/188＝97.9%**（v126：184/188＝97.9%）


## 新圖 22 張各自對應句數（全部 >0，唔係死圖）

| 新資產 | 對應分類句數 |
|---|---:|
| gu_mingfai_shy.webp | 3 |
| gu_mingfai_angry.webp | 1 |
| gu_mingfai_think.webp | 1 |
| pang_siuki_sad.webp | 3 |
| chow_choiyi_sad.webp | 3 |
| chow_choiyi_angry.webp | 2 |
| yip_manji_surprise.webp | 2 |
| yip_manji_angry.webp | 2 |
| yip_manji_shy.webp | 1 |
| ching_tinlok_shy.webp | 1 |
| ching_tinlok_surprise.webp | 1 |
| ching_tinlok_think.webp | 1 |
| lan_ruoxi_serious.webp | 1 |
| lan_ruoxi_think.webp | 1 |
| fong_siulung_sad.webp | 2 |
| fong_siulung_angry.webp | 1 |
| cheng_william_serious.webp | 1 |
| cheng_william_shy.webp | 1 |
| kwan_hoimei_serious.webp | 1 |
| mok_siufai_sad.webp | 1 |
| uncle_kim_smile.webp | 1 |
| uncle_kim_serious.webp | 1 |

## 逐角表（有變動嘅角）

| 角 | 非neutral | 精確覆蓋 | 覆蓋率 | 有資產類別（除base） | 缺資產類別（句數） |
|---|---|---|---|---|---|
| gu_mingfai | 22 | 22 | 100.0% | angry, sad, serious, shy, smile, think | — |
| pang_siuki | 29 | 29 | 100.0% | sad, serious, shy, smile, surprise | — |
| chow_choiyi | 13 | 13 | 100.0% | angry, sad, serious, smile, think | — |
| yip_manji | 19 | 19 | 100.0% | angry, sad, serious, shy, smile, surprise | — |
| ching_tinlok | 29 | 29 | 100.0% | angry, sad, serious, shy, smile, surprise, think | — |
| lan_ruoxi | 11 | 11 | 100.0% | sad, serious, shy, smile, think | — |
| fong_siulung | 8 | 8 | 100.0% | angry, sad, serious, smile | — |
| cheng_william | 2 | 2 | 100.0% | serious, shy | — |
| kwan_hoimei | 1 | 1 | 100.0% | serious | — |
| mok_siufai | 1 | 1 | 100.0% | sad | — |
| uncle_kim | 2 | 2 | 100.0% | serious, smile | — |

## 殘留缺口（零精確覆蓋嘅角）

- **extra_ad_fen**：0/9；缺 sad(9)；有資產 （只有 base）

## 其他值得注意嘅殘留缺口（非零但未補；按缺句數排）

- ngai_wingnaam：2/12（16.7%）；缺 angry(2)、happy(3)、serious(3)、surprise(1)、think(1)（共 10 句）
- lin_hiu：6/15（40.0%）；缺 angry(2)、happy(1)、serious(3)、think(3)（共 9 句）
- chai_zanhoi：6/13（46.2%）；缺 angry(1)、happy(2)、shy(2)、think(2)（共 7 句）
- ko_chunkit：21/28（75.0%）；缺 sad(3)、shy(1)、think(3)（共 7 句）
- luk_baakyin：1/8（12.5%）；缺 angry(1)、happy(4)、sad(2)（共 7 句）
- lok_gasing：10/16（62.5%）；缺 angry(2)、happy(1)、shy(2)、surprise(1)（共 6 句）
- cheung_tsijun：6/10（60.0%）；缺 angry(1)、sad(1)、think(2)（共 4 句）
- liu_bingxing：23/27（85.2%）；缺 sad(1)、surprise(2)、think(1)（共 4 句）
- cheung_hakfan：1/4（25.0%）；缺 serious(3)（共 3 句）
- lui_ging：6/9（66.7%）；缺 sad(1)、serious(2)（共 3 句）
- mak_zhendong：12/14（85.7%）；缺 angry(1)、happy(1)（共 2 句）
- tsui_poushan：1/3（33.3%）；缺 serious(2)（共 2 句）
- vera：1/3（33.3%）；缺 serious(1)、shy(1)（共 2 句）
- chung_choning：21/22（95.5%）；缺 angry(1)（共 1 句）
- so_jiyan：28/29（96.6%）；缺 surprise(1)（共 1 句）
- tong_souwan：4/5（80.0%）；缺 sad(1)（共 1 句）

## 數據註

- 阿偉 s2/s3 精確覆蓋剩 angry 4 句——但 runtime 候補鏈（dlg106Candidates）s2/s3 angry 會經跨階段後備攞到 v123 新出嘅 `awi_angry.webp`，實際顯示 100%，唔會退 base。

- extra_ad_fen 嘅「sad」9 句經 v106 查證係旁白假陽性（同一句旁白重複），唔使補圖；本表沿用 v106 口徑，佢仍列零覆蓋。

- 全局升幅 +32 句（483→515）：顧明輝 shy 3／angry 1／think 1、彭少祺 sad 3、周采兒 sad 3／angry 2、葉敏芝 surprise 2／angry 2／shy 1、程天諾 shy／surprise／think 各 1、藍若曦 serious／think 各 1、方小龍 sad 2／angry 1、鄭威廉 serious／shy 各 1、關海媚 serious 1、莫少輝 sad 1、阿金叔 happy／serious 各 1。

- 兩處標籤更正（v126 殘留表錯咗，今批核實修正）：`chow_choiyi`＝**周采兒**（娛樂記者，display「周采兒」），唔係周刊編輯——真正嘅周刊編輯係無名角色，v119 行 `shadow_male`，冇 base 圖所以唔出表情圖；「阿金叔」speaker id 係 `uncle_kim`，唔係 `kam_uncle`。

- 593 分母核對（v125 更正數字）：CHOICE47／WF3／COMMIT48 嘅 text beats（真正唔顯示嘅 51 句＋resultBeats 35 句，連 WF4 intro／送別計 73–76 句）逐句對過 `lines_classified.json`（2,644 行）——**0 句命中**，即 593 分母從來唔包呢批，v125 令佢哋顯示到亦唔影響覆蓋率，唔使改分母。
