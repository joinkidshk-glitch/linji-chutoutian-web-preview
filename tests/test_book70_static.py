# -*- coding: utf-8 -*-
# v20a70 BOOK70 靜態測試：手帳五大類導航（10 tab → 5 大類＋組內分段）／訓練段拼入行程頁／恆常出口。
# 反證：喺 v20a69 index 上行會 FAIL（冇 BOOK70 標記、仲係 10 個 tab、出口跟日子狀態改名）。
# 用法：python3 tests/test_book70_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- (1) 一級五大類 ---
ok('一級只剩 5 個大類掣（行程／事業／近況／消息／人情）',
   src.count('data-hgroup="') == 5
   and all(s in src for s in ['data-hgroup="plan"', 'data-hgroup="career"', 'data-hgroup="status"', 'data-hgroup="news"', 'data-hgroup="favor"'])
   and all(s in src for s in ['>行程</button>', '>事業</button>', '>近況</button>', '>消息</button>', '>人情</button>']))
ok('冇返舊 10-tab 結構（htab-plan／htab-guide 唔再存在）',
   'id="htab-plan"' not in src and 'id="htab-guide"' not in src and 'data-htab="guide"' not in src and 'id="home-pane-guide"' not in src)

# --- (2) 組內分段：子掣齊＋分組正確 ---
def between(a, b):
    i, j = src.find(a), src.find(b)
    return src[i:j] if 0 <= i < j else ''
career = between('data-hsubgroup="career"', 'data-hsubgroup="status"')
status = between('data-hsubgroup="status"', 'data-hsubgroup="news"')
news = between('data-hsubgroup="news"', '</div>\n      </div>\n      <div class="home-pane on"')
ok('事業組分段＝作品＋獎項＋回憶', all(s in career for s in ['id="htab-works"', 'id="htab-awards"', 'id="htab-memory"']))
ok('近況組分段＝記數＋標籤', all(s in status for s in ['id="htab-ledger"', 'id="htab-tags"']))
ok('消息組分段＝傳聞＋剪報', all(s in news for s in ['id="htab-rumor"', 'id="htab-clippings"']))
ok('子頁 pane 全部保留（9 個）', all(('id="home-pane-%s"' % s) in src for s in
   ['plan','ledger','rumor','clippings','debt','tags','works','awards','memory']))
ok('分組映射 BOOK70_TAB_GROUP 齊 9 子頁',
   'const BOOK70_TAB_GROUP' in src and all(s in src for s in
   ['plan:"plan"', 'works:"career"', 'awards:"career"', 'memory:"career"', 'ledger:"status"',
    'tags:"status"', 'rumor:"news"', 'clippings:"news"', 'debt:"favor"']))
ok('分組同步＋子頁點擊接線（book70SyncTabGroups／home-subtabs onclick）',
   'function book70SyncTabGroups' in src and '_homeSubtabsEl' in src and 'book70SyncTabGroups(tab)' in src)
ok('大類掣 data-htab 跟組內記憶子頁（舊呼叫／自檢兼容）', 'book70GroupSub[g] || BOOK70_GROUP_FIRST[g]' in src)

# --- (3) 訓練段拼入行程頁 ---
i_plan = src.find('id="home-pane-plan"')
i_train = src.find('id="home-train70"')
i_next = src.find('id="home-pane-ledger"')
ok('訓練段喺行程頁 pane 入面（plan pane 同下一個 pane 之間）', 0 <= i_plan < i_train < i_next)
ok('指南渲染改掛 train70-list（冇再用 guide-list）',
   'getElementById("train70-list")' in src and 'getElementById("guide-list")' not in src)
ok('主次分家部件齊（主修大卡／附帶細行／分家衍生）',
   all(s in src for s in ['function book70CourseCard', 'function book70CourseMini', 'function book70SplitForStat', 'function ux68CoursePrimaryStat']))
ok('主修卡四格關鍵數（增益／費用／耗時／壓力）',
   all(s in src for s in ['<span>增益</span>', '<span>費用</span>', '<span>耗時</span>', '<span>壓力</span>']))
ok('前往掣兼任答案（報名／報主課／加練三種寫法齊）',
   all(s in src for s in [' 報名</button>', ' 報主課</button>', ' 加練</button>']))
ok('附帶組預設摺疊（data-tsub＋hidden subbody）', 'data-tsub="1"' in src and 't70-subbody" hidden' in src)
ok('地點全名單收落展開（data-tloc／t70-locall hidden）', 'data-tloc="' in src and 't70-locall-' in src)
# 實駕教訓（v70 駕駛 P2）：.t70-locall 設咗 display:block 會蓋過 [hidden] 嘅 UA display:none，
# 令完整地點名單未展開已經顯示（卡面瘦身失效）。要明文 [hidden] 守衛先算數。
ok('地點全名單 [hidden] 守衛（display 唔准蓋過收起狀態）', '.t70-locall[hidden]{ display:none; }' in src)
ok('訓練段開合函數（book70OpenTrainSection）＋標頭提示位', 'function book70OpenTrainSection' in src and 'id="train70-hint"' in src)

# --- (4) 恆常出口 ---
ok('出口容器唔再 hidden（HTML 層）', 'id="home-tab-exit" hidden' not in src and 'id="home-tab-exit"' in src)
ok('恆常出口函數 book70ExitHome（純返地圖）', 'function book70ExitHome' in src)
ok('出口掣 onclick 行 book70ExitHome', '_homeTabExitBtn.onclick' in src and 'book70ExitHome(); }catch' in src)
ok('syncHomeTabExit 唔再睇 srcShown／journalTab（舊共用掣邏輯已拆）',
   'const srcShown' not in src and 'const journalTab' not in src)
ok('行程頁日子狀態掣保留（繼續行程／開始今日行程／返回地圖三態仲喺 #home-back-map 度）',
   all(s in src for s in ['"繼續行程"', '"開始今日行程"', 'hbm.textContent = forced']))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
