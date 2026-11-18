# NOTES_V20A289 — Q1 劣評分支：表現判定

## 拍板
用戶 2026-11-18 13:00 拍板：**表現判定——演得差先出劣評**（Q1，26 條設計問題第 1 條）。

## 舊制點解死咗
- `enc79OnWrap` 舊判：`bad = (Number(sh.fame)||0) <= 1`。
- `sh.fame` 係 `scheduleShoot` 存入嘅 fame roll；全庫 289 張 fame roll 最低 5（`gig_1990_ad_201` 等），`fame<=1` 永不成立。
- 結果：劣評而家出唔到；殺青好感永遠係好評格（主角 +3／配角 +1）。

## 新制：`enc79WrapPerf(sh, g)`（index.html，`enc79OnWrap` 後面）
殺青嗰陣可用訊號，兩個：
1. **底圍欠數（short）**：`Σ max(0, req − S[k])`，只計 `GIG_REQ_KEYS88` 七鍵（非屬性鍵防禦同 `reqGap` 一致）。
   - **只讀底數，衫加成唔計**（v20a265 硬規則：加成唔入殺青判定）。試鏡靠衫頂住入門檻，殺青嗰陣底圍唔夠就會見到欠數；即派／引薦等非試鏡途徑獲聘同樣會計。
   - `canAudition` 本身係硬閘（有效數值唔夠唔畀報），所以欠數主要嚟自衫頂入門檻＋非試鏡獲聘。
2. **壓力（S.stress）**：0–100，85 係遊戲本身危險線（≥85 唔畀做非休息非拍攝活動）。

### 公式
```
pBad = min(0.30, short × 0.03) + (stress ≥ 85 ? 0.20 : stress ≥ 60 ? 0.08 : 0)
pBad = min(pBad, 0.50)
bad  = pBad > 0 && R(1,100) <= round(pBad × 100)
```

### 校準表
| 情況 | short | stress | pBad |
|---|---|---|---|
| 表現合格、壓力正常 | 0 | <60 | **0 — 絕唔出劣評** |
| 壓力偏高（谷緊） | 0 | 60–84 | 8% |
| 壓力爆煲（危險線） | 0 | ≥85 | 20% |
| 衫頂住入門檻（欠 4） | 4 | <60 | 12% |
| 欠 10 | 10 | <60 | 30%（欠數項上限） |
| 欠 10＋爆煲 | 10 | ≥85 | 50%（合計上限） |
| 無 req 臨記＋低壓 | 0 | <60 | 0 |

好評仍係常態：表現合格嗰陣機率係 0，唔係細機率；劣評只會喺欠數／壓力嗰陣先有機會出。
`sh.fame` 唔再參與判定（佢係獎勵 roll，唔係表現分）。

## 改動
- `index.html`：
  - 新增 `enc79WrapPerf(sh, g)`（回傳 `{bad, pBad, short, stress}`；缺值時當合格）。
  - `enc79OnWrap`：`bad` 改讀 `enc79WrapPerf(sh, g)`；註解更新，舊制 `fame<=1` 判句刪除。
  - 位置注意：新函數放喺 `enc79OnWrap` 後面，唔郁 `function enc79OnWrap` 嘅位置（`test_weave46_static.py` 用佢做 ROM183 區塊邊界）。
- `tests/test_enc79_logic.js`：fns 抽取表加 `enc79WrapPerf`；殺青劣評 case 改由壓力驅動（stress 90＋R 最小值 → 劣評 +1）；加「舊制退役」斷言（fame 0 但表現合格 → 照樣好評 +3）。
- 新增 `tests/test_r289_wrap_perf_logic.js`（22 項）：公式逐格、壓力邊界 59／60／84／85、擲骰邊界 12／13、缺值／非屬性鍵防禦、onWrap 四角分格好／劣、舊制退役。
- 新增 `tests/test_r289_wrap_perf_static.py`：函數在位、舊判句已刪、掛點未郁、NOTES 在位。

## 唔郁嘅嘢
- 好感分格不變：好評主角 +3／配角 +1，劣評主角 +1／配角 0；`grant()` 未郁。
- 報紙／殺青卡唔顯示好／劣文字（本來就冇），今次唔加 UI。
- `scheduleShoot`／shoot record 唔加欄位（判定用殺青嗰陣 live state 計，唔使存表現分）。
- SAVE key／softRev／產品 `?v=` 未郁。

## 驗證
- 新測試逐個直接跑：`test_r289_wrap_perf_logic.js` 22 項 ALL PASS；`test_r289_wrap_perf_static.py` ALL PASS；`test_enc79_logic.js` 全過。
- 全套 suite（工作副本，第二跑）：**TOTAL PASS 351 FAIL 9**——9 項全部係已知 pre-existing FAIL（flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），零新 FAIL。基線 349／9，新加 2 個測試檔全過。
- 釘行 resync：新函數令 index.html 淨 +36 行（46220→46256），5 檔釘行測試漂移（gift185／rom176／tang171／tang173／travel114），22 處錨點內容逐字核實純漂移後 resync（單次掃描 dict 查表，`/tmp/resync289.py`），逐個重跑 ALL PASS。
