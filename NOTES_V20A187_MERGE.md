# v20a187 落地紀錄

- 遊戲 commit：`fe09b67`（squash merge `v20a187`）
- 基底：`cbc3636`（v186 NOTES）
- 線上核實：5,310,960 bytes，sha256 `c02b36ec3533b71ef9a2ff7212afe85c00b49986682d3a20153cb079663360d2`，同 repo `HEAD:index.html` 完全一致（2026-11-13 19:1x HKT，Pages 部署滯後約 100 秒，第一 curl 仲係 v186 舊版）。
- `git fsck --strict`：只有 dangling blob/tree（squash merge 正常殘留），無錯誤。
- 落地內容：修 v181 設計 review B1＋C1–C6（地板收窄 y228–310／海報避牌／卡罅 24px／out 留人／walkup 前層／glyph 罅；C5 keep——v174 已接受 trade-off，B1 唔郁 frame 高）。
- 驗證：新測試 43＋43 項 ALL PASS（統籌親自重跑新測試＋181 測試）；全套 255／12 零回歸（FAIL 清單同 12 項穩定 pre-existing 一致）；實駕 6/6、0 pageerror。
- Push 一次成功，無斷線。
