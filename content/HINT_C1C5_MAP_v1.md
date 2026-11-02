# 主線 C1–C5 地圖 hint｜HINT_C1C5_MAP_v1

> **時間：** 2026-11-03（Asia/Hong_Kong）  
> **來源：** `PLAN_MAP_BOARD_DECISIONS_v1.md`＋`PLAN_MAP_STORY_PROGRESS_v1.md` §3.1.1／§4  
> **檔：** `story_detail_c1_to_c17.json` **1.1 → 1.2**  
> **HOLD：** 出圖、鄧節序、C5 裸旗 rename、index 引擎大改、romance／rival meet `playerOffer`（本輪只做主線）

---

## 勾選

| # | 項 | 狀態 |
|---|---|---|
| 1 | C1–C5：`locId`／`playerHint`／`lockedHint`／`nextHint`／`playerOffer:true` | ✅ |
| 2 | C5 `thresholds.rel_choi_threshold`＝**2**；Any OR 夏保留 | ✅ |
| 3 | pack `version` bump 1.2；`edits`／`qa.map_hint_c1c5` 記 BOARD_DECISIONS | ✅ |
| 4 | 書面港語；禁薄本／趕板／苛約；玩家文案無 raw `flag_*` | ✅ |
| 5 | loc 皆現有 LOCS（`tvb_longmen`／`ad_central`） | ✅ |
| 6 | 未改 index.html；未改 Soft leftover 他檔；未出圖 | ✅ |

---

## 文案表（落檔）

| ID | locId | playerHint（可播） | lockedHint（未開） | nextHint（播完） |
|---|---|---|---|---|
| C1 | `tvb_longmen` | 星河電視台廠景有幕等你：先練定先賺。 | 去星河電視台廠景——通告欄旁有幕等你揀。 | 下一幕「留人脈／趕通告」——殺青後可喺片場後巷留低。 |
| C2 | `tvb_longmen` | 後巷有人約飯；通告欄又貼咗新單。 | 殺青後喺片場後巷留低——人脈同下一張通告會撞期。 | 下一幕「對對手硬／忍」——多留意星河電影組通告欄。 |
| C3 | `tvb_longmen` | 通告欄前氣氛緊，有人睇住你嘅名牌。 | 多去星河電影組通告欄——搶位爭執快發生。 | 下一幕「何生拒單」——中環廣告那邊有份外判通告等你表態。 |
| C4 | `ad_central` | 何生檯面有份通告紙等你表態。 | 何生會拎份條款含糊嘅外判通告——留意經理人事務所。 | 下一幕「采兒小訪題」——同周采兒處好關係，或捱到台慶籌備季。 |
| C5 | `tvb_longmen` | 片場邊有小訪位，筆記本已經打開。 | 同周采兒處好關係，或捱到台慶籌備季，先有小訪。 | 主線這段告一段落——繼續跑通告、見人，留意之後 P1.5 事態。 |

> 對齊計劃草案：用「通告欄」代替單獨「板」口語縮寫；C2／C4 soft loc 跟拍板（新針 HOLD）。

---

## loc／門檻

| 節 | loc（拍板） | 備註 |
|---|---|---|
| C1 | `tvb_longmen` | 星河廠 |
| C2 | `tvb_longmen` | soft（茶餐廳無針） |
| C3 | `tvb_longmen` | 電影組通告欄 |
| C4 | `ad_central` | soft＝中環廣告／經理人側 |
| C5 | `tvb_longmen` | 片場邊；跟 setting |

**C5：** `openConditionsAny`＝`rel_choi_threshold` **OR** `season_1988_summer_anni_prep`；`thresholds.rel_choi_threshold`＝**2**（note：拍板 2026-11-03＝2）。

**平行 meet `playerOffer`：** 本輪跳過 romance／rival；主線五節明示 `true`。

---

## 自檢

- [x] C1–C5 四欄＋`playerOffer` 齊  
- [x] 禁詞（薄本／趕板／苛約）＝0  
- [x] 玩家 hint 無 `flag_*`  
- [x] C5 thresh＝2；OR 夏保留  
- [x] loc ∈ LOCS  
- [x] beats／choices／flags_written 未改（C5 裸旗 HOLD）

---

## Paths

- `/workspace/star-volunteer-web/content/story_detail_c1_to_c17.json`
- `/workspace/star-volunteer-web/content/HINT_C1C5_MAP_v1.md`
- `/workspace/star-volunteer-web/content/PLAN_MAP_BOARD_DECISIONS_v1.md`
- store：`/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/`（同上三檔）

## Skipped

- index.html／StoryOC 讀欄  
- 出圖  
- 鄧節序  
- C5 `choi_*` → `flag_choi_*` rename  
- romance／rival meet `playerOffer`  
- 通知用戶／tester  

---

*完 — HINT_C1C5_MAP_v1*


## Nit fix 2026-11-03
- pack **1.2.1**：C5 `nextHint` 去工程期號 `P1.5`；「這段」→「呢段」。
