> Soft≠PASS｜3.2.10-soft｜SHA `35895f4e`｜pre 3.2.9 `fe70d5c1`｜Phase D vocal｜唔 tip LIVE｜19w｜89–92 HOLD

# CHANGELOG_GIGS_1988_3_2_10_SOFT

## 摘要
Phase D 開獨立歌藝：Soft gigs `req` 主鍵映射 `stage`→`vocal`（`stage` 保留輔）；合唱／晚會（有 `stage`）`vocal`＋`stage` 並列；玩家面「體力」→「體能」。  
**唔夾** `stamina` req（體能＝人物能力，cap **999**）。`stress`>100 可夾（本包 **0**）。  
結算語義（訓練／打工／通告）只加壓力、**唔扣** stamina——屬 **iOS Soft tip**，本包唔改引擎。

## 映射
| 範圍 | 規則 |
|---|---|
| 唱片通告（全 genre） | 主 `vocal`＝原 `stage`；`stage` 輔保留 |
| 音樂錄像 | 同上 |
| 合唱 | `vocal`＋`stage` 並列 |
| 綜藝·歌唱節目（有 stage） | 主 `vocal`；`stage` 輔 |
| 綜藝·晚會（有 stage＝歌唱位） | 加 `vocal` 並列 |
| 電影／電視劇／廣告／寫真／其他綜藝 | **唔加** `vocal` |

## 啟發式（未加 vocal）
| id | 原因 |
|---|---|
| `gig_1988_tvb_harbour_autumn_low` | 歌唱節目但無 stage；角色舉牌助手 → 未加 vocal |

## Counts
- n＝**137**
- vocalAdded＝**43**（req 現有 vocal）
- vocalPrimary＝**31**
- parallelVocalStage＝**14**
- staminaClamped＝**0**（取消；唔改 stamina 數值）
- stressClamped＝**0**
- 體力→體能 gigs＝**36**
- speech／dance keys＝**0**

## 閘
Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=／SAVE（仍 **19w**）｜89–92 HOLD｜speech／dance HOLD｜出圖 HOLD

## 檔
- `gigs_1988_3.2.10-soft.json`
- `gigs_1988.json`（Soft preview 載入源同步；**唔**當 LIVE tip）
- backup：`gigs_1988_v3.2.9_soft_pre_phase_d_vocal_backup.json`
- plan：`PLAN_SOFT_PHASE_D_VOCAL_v1.md`／`NOTES_SOFT_PHASE_D_VOCAL_MAP_v1.json`
