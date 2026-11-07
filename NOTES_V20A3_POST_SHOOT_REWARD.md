# NOTES · Freeplay v20a3 POST-SHOOT REWARD

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；殺青獎勵／成就傳媒殼；**唔 tip LIVE**；**唔發明長劇情弧**  
> **預覽：** `?v=20a3&softBehaviorGate=1`  
> **契約：** `docs/CONTENT_CONTRACT.md`

## 本輪加咗咩

1. **殺青後獎勵包（一次／完成）**
   - Trigger：`resolvePlannedDay` 拍攝 `finished` 成功路徑。
   - `queuePostShootRewardOnWrap(sh)` → 建 pack、寫 `S.postShootRewards`、設 pending。
   - 日結 modal 收起後 → `presentPendingPostShootReward` 出 1–3 張卡。

2. **四條頻道（data-driven stub）**
   - `press` 報紙娛樂版頭條  
   - `news` 電視／電台一句  
   - `streetFans` 街上突發被 fans 包圍（可帶 `stageVolumeDelta`）  
   - `metrics` 依 gig type：電影→票房、電視劇／綜藝→收視、唱片通告→銷量、其他→關注度  

3. **檔案**
   - `content/SCHEMA_POST_SHOOT_REWARD_v1.json`
   - `content/STUB_POST_SHOOT_REWARDS_v1.json`
   - 契約更新；`SCHEMA_FREEPLAY_FRAMEWORK_v1.json` meta → v20a3

4. **雙軌**
   - 每次殺青獎勵 baseline 幕前聲量 +1；streetFans 卡可再加 stub delta。

5. **API**
   - `__reward.check()` / `__reward.log()` / `__reward.build(sh)`
   - `__freeplay.rewards()` / `__freeplay.rewardCheck()` / `__freeplay.check()` 含 reward

## Verify

```js
await __freeplay.load();
__freeplay.check();          // ok:true；infra:"v20a3"；postShootReward:true
__reward.check();            // ok:true
__reward.build({title:"試", type:"電影", gigId:"x"});
```

預覽殺青一單後應見「傳媒・街外・成績」sheet。

## 內容 bot

只改 `STUB_POST_SHOOT_REWARDS_v1.json` 嘅文案欄：`headline`／`dek`／`line`／`blurb`／`valueLine`／`paperName`／`outlet`／`place`。  
唔改 trigger、SAVE、閘公式；唔用真藝名。

## HOLD（刻意）

- LIVE tip／抬 SAVE／89–92  
- 出圖／31 人 LOOKS；紅星長互動  
- 真實報紙排版／音效；長篇傳媒劇情弧  
