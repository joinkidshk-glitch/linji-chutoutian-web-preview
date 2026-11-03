# PLAN｜通告對齊《明星志願3》欄位 v1

**日期：** 2026-11-03（Asia/Hong_Kong）  
**觸發：** 用戶拍板——通告對齊 MV3 欄位；tester 轉交；劇本鎖 schema／genreLabel／角色職位／特殊限制。  
**對齊：** `PLAN_GIG_CASTING_NOTICE_DETAIL_v1`、`PLAN_GIG_PAY_EXACT_v1`、`PLAN_GIG_BREACH_FEE_v1`、`PLAN_GIG_CASTING_REQ_NUM_COPY_v1`、`PLAN_SHOOT_CAREER_SCHEDULE_v2`  
**Soft≠PASS**／出圖 HOLD  
**交：** tester（合你方 PLAN）／iOS／GD；補庫另開閘

---

## 0. 一句

Detail 跟 MV3：**通告名、細類型、星等、角色／職位、片酬 exact、拍攝天數、條件 >N、特殊限制、導演／製作人**；類型核心能力用**現行六維映射**，MVP **唔新開**歌藝／口才數值欄。

---

## 1. 介面欄 ↔ 我方（鎖）

| MV3／用戶 | 我方顯示 | 資料 | MVP |
|---|---|---|---|
| 通告名稱 | 作品名／通告題 | `workTitle`∥《》∥`title` | 派生；後補 `workTitle` |
| 類型（細） | 類型 pill | **`genreLabel`**（粗 `type` 仍存） | **加欄**；缺則粗 `type` |
| 星等 1–5 | 難易度 ★ | 既有 tier／hard／roleScale 派生 | 沿用 DETAIL §3.6 |
| 角色／職位 | 角色 | **`roleLabel`**（新）∥`roleHint` 短稱 | **加欄**；缺則截 `roleHint` 首句或「通告角色」 |
| 酬勞 | 片酬 | exact（PAY_EXACT） | 已鎖 |
| 拍攝天數 | 總天／每週 | `shootDaysHint`／weekdays | 沿用 |
| 條件門檻 | 條件 | `req`＋聲望；顯示 `名：>N` | 已鎖 v1.1 |
| 特殊限制 | **特殊限制** | **`limits`**（新） | **加欄**；空則隱藏整塊 |
| 製作人／導演 | 導演；製作人可選 | `director`；**`producer`**（新，可選） | 缺→組製未公開；NPC 友好影響＝後日引擎 |
| 違約金 | 違約金 | BREACH_FEE | 已鎖；**無簽約** |

---

## 2. 屬性映射（MV3 類型核心 → 我方）

### 2.1 現行玩家維（唔改名）

`acting` 演技 · `stage` 台風 · `looks` 外貌 · `stamina` 體力 · `iq` 智商 · `charm` 魅力  
（另：`fame` 聲望 · `popularity` 人氣＝檔次／曝光，唔作「核心系」主能力）

### 2.2 類型核心 → 主／輔 req（鎖；作者填 req 時跟表）

| MV3 核心 | 粗 `type` | 主能力（必顯門檻優先） | 輔能力（可選） | **加新數值欄？** |
|---|---|---|---|---|
| 歌藝系 | 唱片通告 | **`stage`（台風）** | `charm`、`stamina`（合唱／快歌） | **否（MVP）** |
| 演技 | 電影、電視劇 | **`acting`** | `looks`、`iq`、`stamina`（替身／動作） | **否** |
| 口才 | 綜藝（主持／訪談／遊戲主持向） | **`charm`** | `stage`、`iq` | **否（MVP）** |
| 儀態＋自信 | 廣告、寫真／平面 | **`looks`＋`charm`** | `stamina`（街頭／長拍） | **否** |

**說明：** MV3「歌藝／口才」喺我方用現有維**語義承接**（台風≈舞台歌唱表現；魅力≈臨場口才／親和）。玩家面條件列**仍顯示我方 STAT 名**（台風／魅力…），唔造「歌藝：>60」除非後日開閘加欄。

### 2.3 後日可選加欄（**未開閘**）

| 候補 | 何時 |
|---|---|
| `vocal` 歌藝 | 用戶明確要獨立訓練／成長線 |
| `speech` 口才 | 同上（主持線加重） |
| `dance` 動感 | 若與體力分家 |

未開閘前：**禁止** JSON 出現未實作 key 作硬閘。

### 2.4 類型→預設主門檻（缺 req 時引擎／作者提示，非自動改庫）

| type | 建議至少 |
|---|---|
| 唱片通告 | stage |
| 電影／電視劇 | acting |
| 綜藝 | charm 或 stage |
| 廣告 | looks 或 charm |

---

## 3. `genreLabel` 細類清單（鎖詞庫；可擴但唔亂造）

寫入 JSON 必須用下表**原文**（港產書面）；一則一標。

### 3.1 電影（`type=電影`）
愛情文藝片 · 江湖動作片 · 喜劇片 · 警匪片 · 驚慄片 · 青春片 · 文藝片 · 歷史／時代片 · 奇幻片

### 3.2 電視劇（`type=電視劇`）
時裝劇 · 處境喜劇 · 家庭倫理劇 · 警匪劇 · 偶像劇 · 時代劇 · 單元劇

### 3.3 唱片通告（`type=唱片通告`）
粵語流行 · 國語流行 · 情歌 · 快歌 · 合唱 · 音樂錄像 · 廣告主題曲 · 兒歌

### 3.4 廣告（`type=廣告`）
影視廣告 · 平面廣告 · 街頭宣傳 · 產品代言

### 3.5 綜藝（`type=綜藝`）
遊戲節目 · 訪談節目 · 歌唱節目 · 晚會 · 外景綜藝 · 資訊節目

### 3.6 寫真／平面（`roleScale=photobook` 或等同）
個人寫真 · 雜誌封面 · 雜誌內頁  
（粗 type 可仍歸廣告或日後獨立；pill 用本細類）

**缺 `genreLabel`：** UI 顯示粗 type（電影／電視劇／…）；補庫優先熱門則。

---

## 4. 角色／職位 `roleLabel`

| 值例 | 適用 |
|---|---|
| 男主角／女主角／男配角／女配角 | 電影／電視 |
| 客串／特約／群戲 | 電影／電視 |
| 替身／動作替身 | 動作向 |
| 主持／嘉賓／固定班底 | 綜藝 |
| 主唱／和音／舞者 | 唱片／MTV |
| 模特兒／路人演員 | 廣告／寫真 |

規則：`roleLabel` 短（≤8 字佳）；詳細演技說明留 `roleHint`／劇情簡介。  
多角色後日 `roles[].label`；MVP 單值。

---

## 5. 特殊限制 `limits`

```json
"limits": {
  "gender": "any",
  "licenses": [],
  "groupOnly": false,
  "minAge": null,
  "maxAge": null,
  "notes": []
}
```

| 欄 | 含義 | 玩家面 |
|---|---|---|
| `gender` | `any`／`male`／`female` | 不限性別／限男性／限女性 |
| `licenses` | 字串陣列 | `須持有：駕駛執照`（多個用顿號） |
| `groupOnly` | bool | `須以組合／團體報名` |
| `minAge`/`maxAge` | 可選 | `年齡 N–M 歲`（有先寫） |
| `notes` | 自由書面短句 | 原樣列（例：`須懂游泳`、`須接受剪髮`） |

**全空／缺欄：** Detail **唔顯示**「特殊限制」標題。  
硬閘：引擎可讀 `gender`／牌照；`notes` 預設只展示，開閘先做檢查。

---

## 6. 導演／製作人

| 欄 | MVP |
|---|---|
| `director` | 已有計劃；缺＝組製未公開 |
| `producer` | 可選；缺則唔顯示「製作人」行 |
| NPC 友好影響試鏡率 | **後日**（關聯 NPC id）；本 PLAN 只預留顯示位 |

---

## 7. Schema 增量總表

```json
{
  "workTitle": "鐵血英雄傳",
  "genreLabel": "江湖動作片",
  "roleLabel": "動作替身",
  "director": "…",
  "producer": "…",
  "limits": {
    "gender": "male",
    "licenses": [],
    "groupOnly": false,
    "notes": ["須接受煙火場面"]
  },
  "payExact": 4000,
  "breachFee": 2000
}
```

既有 `type req pay roleHint shoot*` **保留**。

---

## 8. 分階段

| 階 | 誰 | 內容 |
|---|---|---|
| **A** | iOS | 欄位位：genre／roleLabel／limits／producer；空則隱藏或派生 |
| **B** | 劇本 | 詞庫內補 `genreLabel`／`roleLabel`；抽樣 `limits` |
| **C** | 引擎 | limits 硬閘（性別等）；producer／NPC 友好 |
| **D** | 用戶開閘 | 先可加 `vocal`／`speech` |

---

## 9. QA

1. 細類 pill 只用 §3 詞庫。  
2. 唱片門檻見台風／魅力等**我方名**，無未實作「歌藝」key。  
3. 特殊限制空＝唔顯示；有則書面句。  
4. Soft≠PASS。

Soft≠PASS · 出圖 HOLD
