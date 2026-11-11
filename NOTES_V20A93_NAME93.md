# v20a93 NAME93 名實對照包

用戶 2026-11-11 12:59 實玩捉到：有批通告個名／崗位係臨記、群演、路人級，
但數據畀中高級價——點名嗰張係《離境大堂一封信》機場臨記（tier 中、廣告，
1 日牌面 $4,000、實收 $3,868）。已向用戶承諾修復：逐張對照，崗位係臨記就
壓返臨記價、崗位本身係主角/配角就改走個名入面嘅「臨記」字眼。

## 根源

pack1990 批量生成嗰陣，tier 模板一併決定埋 scale／日數／片酬／聲望／人氣
快照（初 fame[5,12] pop[15,29]；中 [18,31]/[39,62]；高 [50,85]/[80,110]），
但標題／崗位係另一手寫嘅，兩邊從未對照。v90 只喺位階帶內校工期／日薪，
冇做名實對照，所以「臨記拎中級廣告帶頂薪」呢類穿咗過嚟。

## 審計（判處書：audit93/ADJUDICATION93.md）

Node 抽真函數行真管線（years66Walk → normalizeGigRecord）全池 475 張
（庫存 5 包 351＋注入 124，池內以 id 去重 469 張）。崗位 fiction 判定
優先序：synopsis／roleHint（玩家實際做咩）＞ roleLabel／標題後綴 ＞ 數據。
分析器旗 56 張＋人眼覆核（日薪 ≥2500 未旗＋synopsis 自述臨記補掃）17 張
＋softBridge 家族隨家族判 19 張，共審 92 張：

- **改價／降格 36 張**：廣告臨記/路人 8（ad_08 $4,000→$1,500 為首）、
  伴舞/替身/班底錯規模合約 19（最誇張 tv_08《霓虹星夢錄》伴舞臨記原為
  電視主角級 30 日 $30,000 → 綜藝特輯 3 日 $3,600；tv_06/07 替身雜務
  30 日主角約 → 配角主線 16 日 $11,000；「固定班底」4 張＋過場演員＋
  舉牌女郎高級特輯模板全降中級）、gig36 替身短工 2、pack1991–94
  單場戲小崗位縮日 7（14/25 日模板日數縮返場次規模、約酬等比縮）。
  過高嘅聲望／人氣快照同 breachFee（有 3 張 breach 原本高過片酬）一併正；
  硬降格嗰 8 張連 req 按比例約半，免降格後變無人接得到嘅廢工。
- **純改名 7 張**：合約規模係真、個名誤導——《冬夜情歌通宵錄》主唱臨記→
  專輯主唱、《九龍警網》臨記男主→男主角、警員臨記→夜班警員、住客臨記→
  舊樓住客、伴舞演員（16 日）→駐場伴舞、武打替身（海報拍攝）→武打模特兒、
  主要配角（捉鬼隊隊長）→捉鬼隊隊長。另有 2 張兼改名（外景嘉賓→外景伴舞、
  舉牌女郎→伴舞舉牌）計喺改價組。
- **豁免 49 張**：softBridge 常駐散工全家族 30（1988 表 12 張 $3,700＋
  gig36 橋接熟手 18 張 $4,700／$5,300；卡面明標「常駐散工・每週有工開」、
  flat 年價係機制簽名，brief 明示唔郁——其中 g36_89_brg_spr_adm
  《金鐘街招》春季熟手路人初判改價，查實屬機制家族後改判豁免）、
  exodus 資深臨記急聘 3（synopsis 明文資深價＋稀缺溢價）、gig36 男二／
  單元主角 7（自家 scale 詞彙，名價相符）、gig36 台慶男群／底座 5
  （嗰代中價短工、快照老實）、模特崗位 4（synopsis「臨記」指玩家出身，
  崗位本身係出樣模特、面孔即產品）。

## 實作（normalizeGigRecord 尾加 NAME93 層，一處生效、全池必經）

- `NAME93_FIX` 對照表 43 個 id（改價 36＋改名 7），`name93ApplyGig` 只認
  id、絕對值賦值（title／roleLabel／tier／roleScale／shootBand／
  shootDaysHint／payExact／pay／breachFee／fame／popularity／req／
  synopsis・roleHint 字串替換），冪等；排喺 DUR90 之後，本層數值行先。
- 改 scale 嗰批嘅新 shootBand 全部唔等於 DUR90_OLD_BAND 指紋，
  二次 normalize 唔會被 DUR90 重新校準覆寫（邏輯測試有冪等斷言釘住）。
- 唔改 gig id、唔直改 pack JSON、唔改 SAVE key／softRev／?v=。
- 已獲聘 shoot 喺 scheduleShoot 已 snapshot totalDays／pay，舊檔／
  進行中通告沿用接單數值，唔回溯。
- 改名嗰批有 A 級海報嘅 3 張（tv_kowloon_winter_high、
  film_lion_spring_high、rec_wanchai_winter_high）：海報圖本身無字、
  標題由 app 疊印，改名唔使重出圖；殺青／作品牆讀接單 snapshot，一致。

## 唔郁清單

softBridge 全家族 30 張全部數值、exodus 3 張、入門／冬季橋 gig、主演回填
（LEADSTAR59）同海報接線、試鏡／頒獎／結局判定、DUR90／NAT92 機制本身。

## 驗證

- 新測試：`tests/test_name93_logic.js`（對照表 43 id 在池／錨點 ad_08
  1500・tv_08 降格／全池名實守門：臨記類崗位日薪・快照・日數上限＋冇
  「臨記＋主角類」矛盾名銜／softBridge 全家族豁免完整／冪等／改名冇撞名／
  deadline）＋`tests/test_name93_static.py`（紀律＋錨點字面）——全 PASS。
  反證：同一套測試行落 pristine v92（b545c45），logic 16 項 FAIL、
  static 13 項 FAIL（exit 1），新包先至 PASS。
- 審計前後 diff（audit93/pool_audit_before.json vs after）：全池恰好
  43 張有變，零誤傷。
- 全套測試 A/B：基線 118 檔同 v92 main 逐檔尾行結果一致（12 個環境性
  FAIL 檔兩邊同樣 FAIL）；新增只有 name93 兩檔 PASS。零回歸。
- 普查（census93＝census92 複本＋NAME93 抽取；對 pristine main 先重演
  v92 基線數字無誤）：day-0 可接 14→14；第一週逐日 14×7、逐地點
  min ≥1；三年全板 0 格數 0/0/0；pool 171/85/83 不變；1990 中/高
  「恰好 2」37.0%→32.7%（降格令中高格分布更散，向好方向，守衛 <40%）。
- 節奏模型（v90 確定性 1990 全年模型、同策略）：完成 41→41、片酬
  總額 72,550→70,750（−2.5%）、雙軌 288→288——±10% 內。
- 真 UI 實駕（本地鏡像 port 9093、Playwright、槽 3；證據
  audit93/drive93_evidence.json＋drive93_board_adm.png＋
  drive93_detail_ad08.png）：直播池抽查改名／降格全中（《九龍警網》
  男主角、《冬夜情歌通宵錄》專輯主唱、tv_08 中 tier／variety_special、
  film_04 film_support_small）；真 UI 開金鐘創意通告欄，《離境大堂
  一封信》卡面「片酬 $1,500（約酬 $1,350–$1,650）· 拍攝約 1 日」；
  撳入詳情：角色職位「機場臨記」、片酬 $1,500、通告日數共 1 天；
  pageerror 0。
- 已知取捨：ad_08 嘅 req（聲望 16／外貌 300／魅力 340／演技 240）係
  pack 中級模板門檻，本包唔郁——價已壓返臨記級，門檻屬供應分級，
  郁 req 會改變可接性同普查口徑，超出本包範圍；fiction 上係「機場
  送別特寫位要靚樣熟手」嘅精選臨記，價錢而家老實。
