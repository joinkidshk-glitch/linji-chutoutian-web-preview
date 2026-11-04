# v19w Soft≠PASS · 行為閘引擎切片＋鄧線 meet mock · 唔 tip

預覽 `?v=19w`。SAVE `starVolunteer_map_v19w`。LIVE 預設仍係 week-gate。Soft preview 要自己開 flag。唔 merge。出圖 HOLD。89–92 HOLD。

## 權威檔 SHA256

| 檔 | SHA8 | SHA256 |
|---|---|---|
| `content/PLAN_STORY_BEHAVIOR_GATE_ENGINE_SLICE_v1.md` | `8450130d` | `8450130d0d8773bd392178578418141b11648b3da5b596eaa0af2ce129e955d7` |
| `content/SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json` | `cba0e877` | `cba0e8770395f39af78844680398db41006f28cae086043e757311515dd35ab1` |
| `content/PLAN_STORY_DENG_LINE_SOFT_v1.md` | `043a70ff` | `043a70ffed5368a62469872d7b7567a0852b3bb24838f0c1cfd63d9f0e8b185f` |
| `content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.json` | `f5986e81` | `f5986e81515ad8a90aa920f5aaa85896543f9b84506cffccb48f9e22887322a6` |

stubRev `v1.2.0-engine-slice`。鄧線 scope `meet_only`。

## 點樣開 Soft preview

網址加 `?softBehaviorGate=1`（`?softPreview=1` 同樣）。或者：

```js
localStorage.setItem("starVolunteer_softBehaviorGatePreview","1")
```

然後重新整理。關掉就刪呢個 key，並且唔好帶 query。預設 flag 關，C1–C5 仍行原本 `openConditions`／`pacing.weekMin`。

開住之後，主控台：

```js
__behaviorGate.selfCheck()
__dengLine.selfCheck()
```

## C1–C5 抽樣

評估讀 stub `nodes[].trigger`，順序跟 `engineSlice.evalOrder`。玩家面鎖時只見「暫未能報」同「離開」。`nextHint` 唔顯示。

```js
__behaviorGate.sample("C1", { week:1, atLoc:"cafe_cha" })
__behaviorGate.sample("C3", { week:6, atLoc:"tvb_longmen", done:{C2:true}, dayIndex:30, lastMainDoneDay:20, rumors:["gao_steal_spotlight"], fame:15 }) // 唔過
__behaviorGate.sample("C3", { week:6, atLoc:"tvb_longmen", done:{C2:true}, dayIndex:30, lastMainDoneDay:20, rumors:["gao_steal_spotlight"], fame:16 }) // 過（聲量大於 15）
__behaviorGate.sample("C4", { week:8, atLoc:"agency_ho", favor:1, done:{C3:true}, dayIndex:40, lastMainDoneDay:30 })
__behaviorGate.sample("C4", { week:8, atLoc:"cafe_cha", favor:5, done:{C3:true}, dayIndex:40, lastMainDoneDay:30 }) // AND，唔係 OR
__behaviorGate.sample("C5", { week:9, atLoc:"cafe_cha", season:"秋", rumors:["choi_recent_news"], done:{C4:true}, dayIndex:50, lastMainDoneDay:40 })
```

地圖：開 flag 之後，C1 喺金龍茶餐廳先會開。C3 聲量 16 先過，15 唔過。C4 要何生好感至少 1 而且人喺事務所。C5 要秋或冬、地點、以及傳聞種子。`rival_gao` 只留 C3 選擇旗。

## 鄧線 Soft A

只 mock `R_tang_meet`。push1／push2／crisis／ending HOLD。`rel_tang_threshold` 鎖 2。開線要 C5 完成，而且事務所好感至少 1（同 C4 嘅 favor 咬合），人要喺何生事務所。玩家面叫鄧麗萍。關海媚唔升格。唔搶曉晴同采兒。LIVE `story_detail_romance_tang.json` 冇改。

旗開、C5 已完成、人喺事務所，地點表先出現「鄧麗萍約談排片」。未夠條件就「暫未能報」＋離開。

```js
__dengLine.openGate({ ctx:{ atLoc:"agency_ho", favor:1, done:{ C5:true } } })
```

## 合圖（只掛已 Soft 過嘅檔）

已合：10 張公司 `bg_loc_*`（九龍／海港、獅子山／紅棉／維港、中環／金鐘、香江／灣仔／天星）、`so_jiyan` bust×3、何生 `char_ho_bust_frown`／`smile`（c1＋dialog；皺眉 bak 保留）、林曉晴／周采兒／高俊傑／鄧麗萍／雷勁各 bust×3。`rec_wanchai` Soft OK。已 tip 嘅茶餐廳、事務所、星河廠、茶餐廳 beat 圖冇覆蓋。

HOLD 唔加：`char_hero_bust_raise_brow*` 新稿（c1／dialog）、`vera_bust_*` 三檔。

## 19v nits

票根 toast 抬高，開住地點表時壓低過底掣；視窗彈層時 toast 唔再蓋住底掣。劇情簡介滾區底部加留白。印章 cache `?v=19w`。刪咗冇人用嘅 `.soft-try-note`。`isSoftTryGig` 維持 false。遠觀文案欄叫 `distanceLook`。
