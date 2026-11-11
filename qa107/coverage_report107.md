# v20a107 情緒覆蓋率報告

來源：`linji-expression-inventory/work/lines_classified.json`（2644 行）× `linji-fullbody-batch/manifest.json`（96 條，已合併 fix2 8 張）。
口徑同 v106：精確覆蓋＝該角非 neutral 對白入面，類別有同名表情資產嘅句數。

## 總覽

- 名冊非 neutral 句精確覆蓋：**439/593 = 74.0%**（v106：403/593＝68.0%）

- 阿偉 s1：184/188＝97.9%（不變）

- 阿偉 s2：**123/188＝65.4%**（v106：60/188＝31.9%）

- 阿偉 s3：**123/188＝65.4%**（v106：60/188＝31.9%）


## 新圖 8 張各自對應句數（全部 >0，唔係死圖）

| 新資產 | 對應分類句數 |
|---|---|
| awi_s2_think.webp | 63 |
| awi_s3_think.webp | 63 |
| so_jiyan_smile.webp | 12 |
| cheung_tsijun_serious.webp | 6 |
| ho_sang_sad.webp | 6 |
| gao_wenhan_serious.webp | 4 |
| tang_laiping_serious.webp | 4 |
| chow_choiyi_think.webp | 4 |

## 逐角表（有變動嘅角）

| 角 | 非neutral | 精確覆蓋 | 覆蓋率 | 有資產類別（除base） | 缺資產類別（句數） |
|---|---|---|---|---|---|
| awi | 188 | 184 | 97.9% | sad, serious, shy, smile, surprise, think | angry(4) |
| so_jiyan | 29 | 28 | 96.6% | sad, serious, shy, smile | surprise(1) |
| cheung_tsijun | 10 | 6 | 60.0% | serious, smile | angry(1)、sad(1)、think(2) |
| ho_sang | 33 | 29 | 87.9% | sad, serious, smile, think | angry(4) |
| gao_wenhan | 4 | 4 | 100.0% | angry, serious | — |
| tang_laiping | 4 | 4 | 100.0% | sad, serious | — |
| chow_choiyi | 13 | 8 | 61.5% | serious, smile, think | angry(2)、sad(3) |

## 殘留缺口（零精確覆蓋嘅角）

- **cheng_william**：0/2；缺 serious(1)、shy(1)；有資產 （只有 base）
- **extra_ad_fen**：0/9；缺 sad(9)；有資產 （只有 base）
- **fong_siulung**：0/8；缺 angry(1)、happy(5)、sad(2)；有資產 serious
- **kwan_hoimei**：0/1；缺 serious(1)；有資產 （只有 base）
- **mok_siufai**：0/1；缺 sad(1)；有資產 （只有 base）
- **uncle_kim**：0/2；缺 happy(1)、serious(1)；有資產 （只有 base）

## 其他值得注意嘅殘留缺口（非零但未補）

- yip_manji：10/19（52.6%）；缺 angry(2)、serious(4)、shy(1)、surprise(2)
- pang_siuki：20/29（69.0%）；缺 sad(3)、serious(4)、surprise(2)
- gu_mingfai：13/22（59.1%）；缺 angry(1)、happy(4)、shy(3)、think(1)
- fong_siulung：0/8（0.0%）；缺 angry(1)、happy(5)、sad(2)
- ngai_wingnaam：2/12（16.7%）；缺 angry(2)、happy(3)、serious(3)、surprise(1)、think(1)
- lin_hiu：6/15（40.0%）；缺 angry(2)、happy(1)、serious(3)、think(3)
- chung_choning：14/22（63.6%）；缺 angry(1)、happy(3)、think(4)
- luk_baakyin：1/8（12.5%）；缺 angry(1)、happy(4)、sad(2)

## 數據註

- extra_ad_fen 嘅「sad」9 句經 v106 查證係旁白假陽性（同一句旁白重複），唔使補圖；本表沿用 v106 口徑，佢仍列零覆蓋。

- 阿偉 s1/s2/s3 共用同一 609 句池；s2/s3 各補 think 63 句，故階段覆蓋各升 63 句，但全局 awi 只計 s1 一次，think 早已有圖，全局升幅只計其餘 6 張新圖對應嘅 36 句（12+6+6+4+4+4）。

- manifest 記法分裂（老實註）：v106 嗰 6 條 s2/s3（base/smile/serious）記做 speakerId=awi、expr=s2_smile 式；fix2 8 條記做 speakerId=awi_s2/awi_s3、expr=think。本報告階段覆蓋按檔名派生資產集（檔名先係解析器 ground truth），唔依賴呢個分裂嘅記法；合併時冇改寫 v106 舊條目。
