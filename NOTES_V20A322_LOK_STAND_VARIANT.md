# NOTES_V20A322_LOK_STAND_VARIANT

## 1. 任務一句話
`lok_stand_original` 加一個軟條件讀者——`lok_patron` 引薦句變體，唔郁任何閘。

## 2. 背景（v314 殘留已結案）
- `lok_stand_original` 授出（`lok_cover` 抉擇 A「勸佢企硬，唔好唱翻唱」，L37472）之後全檔 0 讀者。
- v314 殘留偵察（2026-11-19）結案：草稿 L323 引薦閘嘅 `lok_stand_original`＋（`lok_heard_whole` 或 `lok_praised_song`）**唔實裝做閘**——cover 窗口得 1991 年冬一季（T2–T3＋守口），加閘會永久鎖死遲遇／T1／T4 玩家＋舊存檔，兼同收尾獎勵判定（獎勵喺 Beat 5 嗰陣已派）再脫鈎；heard／praised live 已做引薦句變體（v278）。草稿 L323 已加實裝註（parent）。
- 呢票只係軟條件變體：有旗嗰陣 patron 多一句回call，令支旗有讀者。

## 3. 實裝（index.html 淨 +4 行，對白只加 1 句）
- 位置：`enc79BuildScript` 內 `lok_patron` 變體段，舊 L40194 一行 → 新 5 行（新 L40194–40198）：
  - v322 註解行（回call 草稿 L228–230「我想有人話我知，我企硬唔係傻」；明言唔係閘）
  - `const v322 = [];`
  - 有 `lok_stand_original` → push `["S","你嗰陣勸我企硬，我記得。"]`
  - 有 v278（heard／praised）→ push v278
  - `if(v322.length)` 用 `slice(0,3).concat(v322, slice(3))` 插喺第 3 句之後
- 變體句核實：廣東話對白，駱家聲口吻，回call Beat 3 A 抉擇對白；其餘 6 句 patron 對白逐字唔郁。
- 次序：stand_original 回call 行先，heard／praised 句行後（兩句都插喺第 3 句之後）。
- 守住：`lok_patron` 閘（L41822，v314：T4＋calm_truth＋三排除）、收尾獎勵判定（L39817，sideline280）、冷版／翻唱版／finale 閘、patron 其餘 6 句對白、grants、GRANT229 全部唔郁；舊檔唔 crash。
- 計數零改動：庫 307 張、trigger 37（credit 26）、BR89 18 對。

## 4. 測試
- 新檔 `tests/test_r322_lok_stand_variant.js`：15 項全 PASS
  - 靜態 6：回call 句在位、stand_original 讀者逐字、lok_patron 閘逐字唔郁、獎勵判定唔郁、heard／praised 變體句唔郁、計數
  - 行為 9：有旗 → patron 7 句（回call 插喺第 3 句之後）；無旗 → 6 句原樣；stand＋heard → 8 句（回call 行先）；stand＋praised → 8 句（回call 行先）；heard／praised 只有 → 各 7 句（v278 唔郁）；冷版 patron_cold（loose_row）→ 真係播冷版、無回call 句；翻唱版 patron_cover（cover_first）→ 真係播翻唱版、無回call 句；閘行為唔郁（calm_truth 開、join_rant 唔開）
- 反證：新測試喺 pristine（v321）index 上行，5 項 v322 專屬斷言乾淨 FAIL，其餘守衛斷言 PASS。
- 舊測試同步（resync，唔係回歸）：改動淨 +4 行，令 5 檔行數釘行測試首跑 FAIL——全部係純漂移，`qa322/resync322.py` difflib 核實唯一 hunk 係舊 L40194 一行 → 新 5 行，30+ 處錨點內容逐字相同：
  - `test_tang171_static.py`／`test_tang173_static.py`：總行數 47286→47290（鏈尾加 ＋v322 +4）；openLoc DEF 42495→42499（lines[42494]→[42498]、guard 42501→42505）
  - `test_gift185_static.py`：總行數 47286→47290（鏈尾加 ＋v322 +4）
  - `test_rom176_static.py`：4 處釘行各 +4（40727→40731、41077→41081、42380→42384、42536→42540；ok 名 L55647 等歷史標籤唔郁）
  - `test_travel114_static.py`：COUNT 4 處＋FREE 24 處各 +4、DEF_LINE 42495→42499、WRAPPER 29108 唔郁
  - 同步後 5 檔逐個重跑全 PASS。

## 5. 落地
- Suite：**385 PASS／9 FAIL**（基線 384／9，＋1 係新測試檔；9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／44／49_static／wf5_87／wrap38）
- Main HEAD：`ad5a760`（內容 `7df6ecc`＋NOTES §5 補填）
- Pages：index.html md5 `4f9885b076162bed26e34768c394c391`／4,701,789 bytes，v20a322 標記在位
- `qa296/derive296.json` 已還原，唔入版。
