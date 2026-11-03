# PLAN｜劇情界面 Beat Schema v1

> **時間：** 2026-11-03（Asia/Hong_Kong）  
> **觸發：** 用戶（經 tester）拍板劇情界面——角色對白半身＋情緒／表情；系統交代置中＋地點環境圖。  
> **範圍：** 只鎖 **字段計劃／對表**；**今次唔改 LIVE story JSON**；**出圖 HOLD**；iOS 做 layout／佔位。  
> **不變：** Soft≠PASS；鄧 HOLD；meet `playerOffer` **唔改 false**。  
> **對齊：** LIVE `story_detail_c1_to_c17.json` **1.2.7**；`cast_main.json`；`ART_BRIEF_GD_v1.md`；HTML `NPCS` 六人；遊戲 **11** 個 `LOCS`。

---

## 產品鎖定（一句）

| UI | 資料要求 |
|---|---|
| **角色對白** | 半身＋情緒／表情 → beat 穩定 `speakerId`＋`emotion`／`expression`；系統線無 speaker |
| **系統交代** | 置中；可配地點環境圖（`locId`／`bg`／`setting` 對齊） |

---

## A. 鎖定 beat schema（v1）

### A.1 建議形狀

```json
{
  "kind": "dialogue",
  "speakerId": "ho_sang",
  "speaker": "何生",
  "emotion": "firm",
  "expression": "default",
  "lines": ["你今天做了幾組？"],
  "bg": null,
  "locId": null
}
```

```json
{
  "kind": "system",
  "speakerId": null,
  "speaker": "系統",
  "emotion": null,
  "expression": null,
  "lines": ["茶餐廳冷氣不夠，油煙和奶茶味攪在一起。"],
  "bg": null,
  "locId": null
}
```

| 欄 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `kind` | `"dialogue"` \| `"system"` | 新稿必填；舊稿可推導 | UI 路由：半身 vs 置中 |
| `speakerId` | string \| `null` | dialogue 必填；system 必須 `null` | 穩定 id（見 §B）；引擎／半身 registry 鍵 |
| `speaker` | string | 可選（建議保留） | 玩家可見顯示名；可由 registry 解，保留方便舊稿／除錯 |
| `emotion` | enum string \| 省略 | 可選 | 未標＝`neutral`；出圖 HOLD 時 iOS 佔位色調／差分 |
| `expression` | enum string \| 省略 | 可選 | 未標＝`default`；視覺槽（眉眼／嘴） |
| `lines` | `string[]` | 必填 | 與現 LIVE 相同 |
| `bg` | string \| `null` | 可選 | beat 級環境 key（如 `bg_loc_tvb_longmen`）；覆蓋 node |
| `locId` | string \| `null` | 可選 | beat 級地圖 loc；覆蓋 node；唔寫入玩家可見 setting 文案 |

### A.2 規則

1. **`kind:"system"`** → `speakerId` **必須** `null`；**唔顯示半身**；UI **置中**；環境底優先：beat.`bg` → beat.`locId`→`bg_loc_{locId}` → node.`locId`→`bg_loc_{…}` → 中性佔位 `bg_generic_interior`。  
2. **`kind:"dialogue"`** → `speakerId` **必填**；半身疊喺環境上（layout 歸 iOS）；環境繼承同上。  
3. **`speaker` 顯示名統一：** 新稿系統線一律 `"系統"`（romance 舊 `"旁白"` 仍兼容，見 A.3）。  
4. **`setting`：** 只屬 **node** 玩家可讀文案；**永不**寫 debug／`locId`／暫掛句（已於 1.2.7 清 C1）。  
5. **`artId`（node）：** 仍做「節點關鍵卡／事態插圖」；與 beat 環境圖 **分工**——`artId`≠半身、≠`bg_loc_*`（見 §C.3）。  
6. **出圖 HOLD：** emotion／expression 只鎖字段；iOS 用剪影／色塊／簡單 tint；半身 art 未到前用 `portrait_placeholder_{speakerId}` 或 generic。

### A.3 兼容（舊 JSON 只有 `speaker`＋`lines`）

引擎推導（唔逼一次改晒 LIVE）：

| 舊 `speaker` | 推導 `kind` | 推導 `speakerId` |
|---|---|---|
| `"系統"` / `"旁白"` / `""` / 缺省 | `system` | `null` |
| 其餘顯示名 | `dialogue` | registry lookup（§B）；找不到 → `extra_unknown`＋剪影，仍可播 |

- 缺 `emotion`／`expression` → `neutral`／`default`  
- 缺 beat.`locId`／`bg` → 繼承 node  

### A.4 emotion／expression 枚舉（v1）

**emotion（語氣／情緒槽）：**

`neutral` · `calm` · `tense` · `angry` · `warm` · `tired` · `smirk` · `worried` · `soft` · `firm`

**expression（臉部視覺槽）：**

`default` · `smile` · `frown` · `raise_brow` · `eyes_down` · `look_aside`

> v1 **唔擴**枚舉；新情緒先 map 入上表。未標＝`neutral`／`default`。

---

## B. speakerId registry（對表）

### B.1 主角＋HTML 六人（G0 半身優先）

| 顯示名 | speakerId | HTML `NPCS` key | face（現網） | 半身 artId（ART_BRIEF） | 備註 |
|---|---|---|---|---|---|
| 阿偉 | `awi` | —（主角） | — | `char_hero` | 陳偉翔；對白可出現 |
| 何生 | `ho_sang` | `agent` | `npc_ho` | `char_ho` | |
| Vera | `vera` | `stylist` | `npc_vera` | `char_vera` | 顯示名維持 Vera |
| 林曉晴 | `lin_hiu` | `colleague` | `npc_lin` | `char_lin` | |
| 張子駿 | `cheung_tsijun` | `director` | `npc_cheung` | `char_cheung` | |
| 高俊傑 | `ko_chunkit` | `rival` | `npc_ko` | `char_ko` | |
| 周采兒 | `chow_choiyi` | `reporter` | `npc_chow` | `char_chow` | |

### B.2 cast_main（snake_case 沿用）

| 顯示名 | speakerId（＝cast id） | 半身 artId | tier／備註 |
|---|---|---|---|
| 高文瀚 | `gao_wenhan` | `char_gao_wh` | 主線 |
| 藍若曦 | `lan_ruoxi` | `char_lan` | 可攻略 |
| 張克凡 | `cheung_hakfan` | `char_hakfan` | 阻力 |
| 雷勁 | `lui_ging` | `char_lui`（ART 未列明細；佔位 id） | 阻力；出圖後期 |
| 關海媚 | `kwan_hoimei` | `char_kwan`（佔位） | 可深交 |
| 鄭威廉 | `cheng_william` | `char_cheng`（佔位） | 可深交；現 beats 未見 |
| 唐素雲 | `tong_souwan` | `char_tong` | 可深交 |
| 方小龍 | `fong_siulung` | `char_fong` | 可深交（友情） |
| 徐寶珊 | `tsui_poushan` | `char_tsui` | 可攻略 |
| 莫少輝 | `mok_siufai` | `char_mok`（佔位） | 可深交；現 beats 未見 |
| 金九 | `uncle_kim` | `char_kim`（佔位） | 可深交 |
| 鄧麗萍 | `tang_laiping` | `char_tang_opt` | 阻力；**鄧 HOLD**——字段可鎖，劇情節序唔動 |

### B.3 雜角／現有 beats 出現過

| 顯示名（LIVE） | speakerId | 半身 | MVP |
|---|---|---|---|
| 藍父 | `extra_lan_father` | 無 → 剪影 | 可 |
| 約會對象 | `generic_date` | 無 → 剪影 | 可 |
| 助導阿玲 | `extra_ad_ling` | `generic_crew` | 剪影 OK |
| 助導阿森 | `extra_ad_sam` | `generic_crew` | 剪影 OK |
| 助導 | `generic_crew` | `generic_crew` | 剪影 OK |
| 副導演芬姐 | `extra_ad_fen` | `generic_crew` | 剪影 OK |
| 導演陸志明 | `extra_dir_luk` | `generic_crew` | 剪影 OK |
| 監製周世昌 | `extra_prod_chow` | `generic_crew` | 剪影 OK |
| 院線助理 | `generic_cinema_asst` | `generic_crew` | 剪影 OK |
| 周刊編輯 | `generic_mag_editor` | `generic_crew` | 剪影 OK |
| （未知顯示名） | `extra_unknown` | 剪影 | fallback |

### B.4 系統別名（唔入半身表）

| 顯示名 | kind | speakerId |
|---|---|---|
| 系統 | `system` | `null` |
| 旁白 | `system` | `null`（romance 舊稿；新稿寫「系統」） |

### B.5 計數（本計劃 registry）

- **具名半身位：** 主角 1 ＋ HTML 六人 6 ＋ cast_main 12 ＝ **19**（含鄧／佔位 artId）  
- **雜角／桶：** **10** 條具名 extra／generic ＋ `extra_unknown`  
- **系統別名：** 2（系統／旁白）  
- **合計 speaker 鍵（含系統處理）：** ~**32** 顯示名映射  

引擎 lookup 建議檔：`content/speaker_registry_v1.json`（**下一刀**先 sandbox 出；今次只 md）。

---

## C. 環境圖對表

### C.1 遊戲 11 loc → 環境佔位 key

| locId | 顯示名（HTML LOCS） | 環境 key |
|---|---|---|
| `tvb_longmen` | 星河電視台 | `bg_loc_tvb_longmen` |
| `tvb_kowloon` | 九龍電視台 | `bg_loc_tvb_kowloon` |
| `tvb_harbour` | 海港廣播 | `bg_loc_tvb_harbour` |
| `film_lion` | 獅子山製片 | `bg_loc_film_lion` |
| `film_cotton` | 紅棉影業 | `bg_loc_film_cotton` |
| `film_harbour` | 維港電影 | `bg_loc_film_harbour` |
| `ad_central` | 中環廣告 | `bg_loc_ad_central` |
| `ad_adm` | 金鐘創意 | `bg_loc_ad_adm` |
| `rec_star` | 天星音樂 | `bg_loc_rec_star` |
| `rec_wanchai` | 灣仔唱片 | `bg_loc_rec_wanchai` |
| `rec_hk` | 香江唱片 | `bg_loc_rec_hk` |
| （無 loc） | — | `bg_generic_interior` |

> 出圖 HOLD：iOS 可用純色／簡易漸層按 `type`（tv／film／ad／music）分色佔位。

### C.2 node 欄分工

| 欄 | 玩家可見？ | 用途 |
|---|---|---|
| `setting` | ✅ 文案 | 地點感覺描述；**禁** locId／暫掛／debug |
| `locId` | ❌（地圖針用） | 地圖 tip／環境預設 `bg_loc_*` |
| `artId` | 視 UI | **節點關鍵卡**（事態／章插圖），非半身、非每 beat 環境 |
| beat.`bg`／beat.`locId` | ❌ | 單句覆蓋（罕見；例：同一 node 內轉場） |

### C.3 artId vs 環境 vs 半身

```
node.artId     → 關鍵卡／章卡（story_c1、rom_lan_meet…）
bg_loc_*       → 對白／系統底圖（場所）
char_*         → dialogue 半身（speakerId）
paper_* / prop_* → 系統交代可選疊加（仿報紙等；另票）
```

### C.4 主線 C1–C17 loc（LIVE ＋ soft 建議）

| ID | LIVE locId | soft／建議（待確認標 soft） | setting 摘要 |
|---|---|---|---|
| C1–C3,C5,C6,C8,C10 | `tvb_longmen` | 已定稿 | 星河／片場 |
| C4,C7 | `ad_central` | 已定稿 soft | 事務所／中環廂房感 |
| C9 | `rec_star` | 已定稿 | 停車場後巷／車上 |
| C11 | `null` | **soft→`tvb_longmen`**（文藝組）；廣告半可 `ad_central` | 兩邊檔期撞 |
| C12 | `null` | **soft→`tvb_longmen`** | 高層／賀歲籌備 |
| C13 | `null` | **soft→`ad_adm`**（周刊代理點；對齊 locPlaceholder LOC_005） | 娛樂周刊採訪 |
| C14 | `null` | **soft→`ad_central`** | 資本場宴會／包廂 |
| C15 | `null` | **soft→`film_cotton`**（商業權力點） | 豪門宴會側廳 |
| C16 | `null` | **soft→`film_harbour`**（舊區／貨倉感） | 舊片場倉庫／金九 |
| C17 | `null` | **soft→`tvb_longmen`** | 會議室／片場晨光 |

> C11+ soft **只入本計劃**；補 LIVE 欄＝下一刀／另票；**唔開新針**。

### C.5 romance／rival／meet soft locId（依 setting 推；標 soft）

#### Rival／mentor（`story_detail_rival_mentor.json`）

| pack 前綴 | 建議 soft locId | 理據 |
|---|---|---|
| `A_ko_*` | `tvb_longmen` | 錄影廠／台慶 |
| `A_hakfan_*` | `tvb_longmen` | 試鏡／製作部／台慶後台 |
| `A_tsijun_*` | meet/push：`tvb_longmen`；crisis/ending：**soft→`film_harbour`** | 舊廠練功 vs 影展 |
| `A_fong_*` | meet：**soft→`rec_hk`**（旺角茶記感）；其餘 `tvb_longmen` | 茶餐廳／廠棚／天台 |
| `A_tong_*` | `tvb_longmen` | 排練室／天台 |
| `A_ho_*` | meet/ending：`tvb_longmen`；push/crisis：**soft→`ad_central`** | 事務所 |
| `A_gao_*` | `tvb_longmen` | 試鏡房／辦公室／天台 |
| `A_lei_*` | meet：**soft→`rec_hk`**；push1：`tvb_longmen`；push2/crisis/ending：**soft→`film_lion`** | 旺角茶記／動作貨倉 |

#### Romance Vera／曉晴／采兒

| pack | soft locId |
|---|---|
| `R_vera_*` | `tvb_longmen`（造型間）；push2 茶聚 **soft→`ad_central`** 附近感仍可用 longmen／不開 cafe 針 |
| `R_hiu_*` | `tvb_longmen` |
| `R_choi_*` | meet：`tvb_longmen`；push：**soft→`ad_adm`**；crisis：`ad_adm`；ending：**soft→`ad_adm`** |

#### Romance 藍／徐／鄧

| pack | soft locId |
|---|---|
| `R_lan_*` | meet：**soft→`rec_hk`**；push：`tvb_longmen`／`rec_star`；crisis：**soft→`film_cotton`**；ending：`tvb_longmen` |
| `R_xu_*` | **soft→`ad_central`**（春茗／會所／資本場） |
| `R_tang_*` | **soft→`film_cotton`**（院線／排片；對齊紅棉院線片公司感） |
| `R_tang_meet_stub` | **soft→`ad_adm`** | 公關會議室 |

#### Meet／playerOffer

- 地圖 meet 觸發仍跟既有 `PLAYER_OFFER_MEET`／loc 首次進入邏輯。  
- **本計劃唔改**任何 `playerOffer: false`；只註 soft loc 方便環境圖。  
- 鄧線：**HOLD**——registry／soft loc 可預留，**唔排節序、唔開 offer**。

---

## D. 範圍與遷移序

| 步 | 內容 | 今次？ |
|---|---|---|
| **1** | Schema 鎖＋registry／環境對表（本 md＋handoff） | ✅ |
| **2** | C1 sandbox／（可選）C1 LIVE 加字段**樣本** | ❌ 下一刀；唔改 LIVE 除非 parent 再叫 |
| **3** | C1–C17 批量補 `kind`／`speakerId`／emotion | ❌ |
| **4** | meet／romance／rival 批量＋soft `locId` 欄（只加欄唔改劇情） | ❌ |
| — | 出圖 G0 半身／`bg_loc_*` | **HOLD** |
| — | Soft 當 PASS | **禁止** |
| — | 鄧節序／playerOffer false→true | **禁止** |

**兼容策略：** 引擎先推導舊稿（A.3）；新稿／sandbox 先寫滿字段；批量用腳本 `speaker`→`speakerId` map。

---

## E. iOS／tester 驗收清單

### E.1 iOS（layout／佔位；讀本 plan）

- [ ] `kind:dialogue`＋有效 `speakerId` → 半身位＋ emotion／expression 槽（tint／標籤即可）  
- [ ] `kind:system` → **無半身**、文案**置中**、有環境底（`bg`／`locId`／node loc／generic）  
- [ ] 舊 JSON 無新欄仍可播（推導路徑）  
- [ ] `setting` 唔當 debug 顯示 locId  
- [ ] node.`artId` 關鍵卡與環境底可分開開關  
- [ ] Soft≠PASS；出圖資產缺失時用佔位，唔 block 播片  

### E.2 tester 抽樣（公開站／本機；字段到位後）

- [ ] C1 首個系統 beat：置中＋`tvb_longmen` 環境佔位  
- [ ] C1 何生對白：`speakerId=ho_sang` 半身槽  
- [ ] romance 抽一節：舊「旁白」→ 當 system  
- [ ] 雜角（助導等）：剪影／`generic_crew` 唔 crash  
- [ ] 回歸：choice／flags／playerOffer／事態 title 未回歸  

---

## F. 相關路徑

| 路徑 | 角色 |
|---|---|
| `content/PLAN_STORY_UI_BEAT_SCHEMA_v1.md` | 本計劃（權威） |
| `content/HANDOFF_STORY_UI_BEAT_SCHEMA_v1.md` | 短交接 |
| `content/story_detail_c1_to_c17.json` | LIVE 1.2.7（今次唔改） |
| `content/cast_main.json` | npc id |
| `content/ART_BRIEF_GD_v1.md` | 半身 artId |
| `index.html` `LOCS`／`NPCS` | 11 loc＋六人 face |
| 鏡：`sv-phone-preview/content/`、bot store | 同文 |

---

*完｜PLAN_STORY_UI_BEAT_SCHEMA_v1*
