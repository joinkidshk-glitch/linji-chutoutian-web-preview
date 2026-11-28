# -*- coding: utf-8 -*-
# v20a162 靜態測試：稱號／標籤頁（開放手帳標籤頁＋稱號顯示）。
#   (1) 三處 freeplayDevTagsOn 閘已拎走（定義＋setHomeTab 彈回＋pane 空狀態），
#       函數本身同 syncDevTagsTabVisibility 一併刪除；?devTags=1 之後係無操作。
#   (2) Tag 卡正經化：label＋來源（from 解返人話）＋軌跡組（TRAJ49_TAG_SETS 分組，
#       唯讀）；舊存檔純字串／冇 from／解唔到唔假裝有來源；hidden 繼續唔出；
#       真空狀態留返「暫時未有選角印象。」嗰句。
#   (3) 稱號區（同一頁）：現時稱號（報紙點名級＋軌跡提示）／結局梯即時位置
#       （live 唯讀 resolveEnding410(S)，淨取 career／variant＋ladder95 三項質性事實，
#       gaps95 句子唔逐字照搬、數字行唔出）／已攞獎項數目＋跳去獎項頁。
#   (4) 進度頁頂加一行現時稱號（同稱號頁同一來源）。
# 反證：喺 pristine main（9346a8e／v151）index 上行 → 多項 FAIL（唔 crash）。
# 用法：python3 tests/test_titles162_static.py [path-to-index.html]
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- v20a162 區塊（由開頭註解到 renderCastingTagsPane 函數尾，brace-match；
#      pristine 冇呢個區塊嗰陣 blk=""，斷言乾淨 FAIL，唔 crash） ---
try:
    _start = src.index('/* ===== v20a162 TITLES162')
    _fn = src.index('function renderCastingTagsPane(){', _start)
    _d, _j = 0, src.index('{', _fn)
    for _k in range(_j, len(src)):
        if src[_k] == '{': _d += 1
        elif src[_k] == '}':
            _d -= 1
            if _d == 0: _j = _k; break
    blk = src[_start:_j + 1]
except ValueError:
    blk = ''
ok('v20a162 區塊在場', bool(blk) and 'function renderCastingTagsPane(){' in blk)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('報紙點名門檻唔郁（15／40）', 'PAPER_NAME_TIER_NAMED = 15' in src and 'PAPER_NAME_TIER_TITLED = 40' in src)
ok('TRAJ49_TAG_SETS 原封（support／backstage／jianghu 三組）',
   'const TRAJ49_TAG_SETS = {' in src and '"tag_reliable"' in src and '"tag_street"' in src)
ok('trajectoryOf49 唯讀函數仲喺度', 'function trajectoryOf49(s){' in src)
ok('resolveEnding410 簽名唔郁', 'function resolveEnding410(st, opts){' in src)
ok('end95BuildGaps 唔郁（冇刪到結局嗰邊）', 'function end95BuildGaps(ctx){' in src)
ok('結局判定／TRAJ49／報紙門檻冇改過嘅字眼：block 內唔寫判定／唔寫 S.ending410',
   'S.ending410' not in blk and 'endingEveOptions410' not in blk and 'ending410AfterEveChoice' not in blk)

# --- (1) 三處閘已拎走 ---
ok('G1 freeplayDevTagsOn 定義已刪', 'function freeplayDevTagsOn' not in src)
ok('G1 freeplayDevTagsOn 呼叫已清零', 'freeplayDevTagsOn()' not in src)
ok('G1 syncDevTagsTabVisibility 定義已刪', 'function syncDevTagsTabVisibility' not in src)
ok('G1 syncDevTagsTabVisibility 呼叫已清零', 'syncDevTagsTabVisibility()' not in src)
ok('G1 setHomeTab 唔再彈 tags 返 plan', 'tab==="tags" && typeof freeplayDevTagsOn' not in src)
ok('G1 render 入面冇 dev 閘分支', 'Player default: no engineering tag spreadsheet' not in src)
ok('G1 tab 唔再 hidden（冇 tab.hidden／display none 閘）',
   'tab.hidden = !show' not in src and 'htab-tags' in src)
ok('G1 setHomeTab("tags") 重定向去作品頁＋照常 render（v389）', 'if(tab === "tags"){ tab = "works"; }' in src and 'renderCastingTagsPane();' in src)

# --- 稱號摺疊入作品頁（v389）：玩家面「稱號」，容器 id 不變 ---
ok('TAB 玩家面改名「稱號」（摺疊 summary）', '<summary>稱號</summary>' in src)
ok('TAB 舊字「標籤」唔再係掣名', 'data-htab="tags">標籤</button>' not in src)
ok('TAB 容器 id 不變、舊 tab/pane 已刪（tags-list 喺 tags389-fold 入面）',
   'id="tags-list"' in src and 'class="tags389-fold"' in src and 'id="htab-tags"' not in src and 'id="home-pane-tags"' not in src)
ok('TAB S.castingTags key 唔郁', 'S.castingTags' in src)

# --- (2) Tag 卡正經化 ---
ok('CARD 來源解返人話（story-ripple／story／gig 三種 from）',
   '"story-ripple:"' in blk and '"story:"' in blk and '"gig:"' in blk)
ok('CARD 故事來源經節點標題（findNodeRaw／STORY_TITLE_SOFT）',
   'StoryOC.findNodeRaw' in blk and 'STORY_TITLE_SOFT' in blk)
ok('CARD 通告來源經 work59GigLookup', 'work59GigLookup' in blk)
ok('CARD 軌跡組重用 TRAJ49_TAG_SETS（唯讀，唔改 TRAJ49）',
   'TRAJ49_TAG_SETS' in blk and 'function castingTagTrajGroup162' in blk)
ok('CARD 軌跡組優先序幕後＞江湖＞甘草', 'if(hit("backstage")) return "backstage";' in blk
   and 'if(hit("jianghu")) return "jianghu";' in blk)
ok('CARD hidden 標籤繼續唔出', 'if(m && m.hidden) return;' in blk)
ok('CARD 舊存檔純字串條目有處理', 'typeof t==="string"' in blk)
ok('CARD at（現實時間戳）唔攞嚟顯示', '.at' not in blk)
ok('CARD 來源行有「嚟自」字眼', '嚟自' in blk)
ok('CARD 真空狀態留返「暫時未有選角印象。」嗰句', '暫時未有選角印象。' in src)
ok('CARD 舊 dev 分支空狀態「暫時未有選角標籤。」已清', '暫時未有選角標籤。' not in src)

# --- (3a) 現時稱號 ---
ok('TITLE 報紙點名級重用 newspaperNameTier／newspaperPlayerRef',
   'newspaperNameTier' in blk and 'newspaperPlayerRef' in blk)
ok('TITLE 軌跡風味重用 newspaperTrajRef49', 'newspaperTrajRef49' in blk)
ok('TITLE 軌跡未定型顯示「未定型」，唔硬派', '未定型' in blk)

# --- (3b) 結局梯即時位置 ---
ok('LADDER live 唯讀呼叫 resolveEnding410(S)（唔傳 opts）',
   'resolveEnding410((typeof S!=="undefined") ? S : {})' in blk)
ok('LADDER 唔傳 opts／唔掂 E6 入口', 'opts.quit' not in blk and 'resolveEnding410(S, ' not in blk)
ok('LADDER 格名經 ENDING410_CAREER_NAMES', 'ENDING410_CAREER_NAMES[res.career]' in blk)
ok('LADDER 早期 E0 誠實顯示「浮沉未定」', '浮沉未定' in blk)
ok('LADDER 開頭講明係「而家行到邊格」，唔係結局預告', '唔係結局預告' in blk)
_rows_ok = False
if 'const rows = []; ' in blk or 'const rows = [];' in blk:
    _rs = blk.index('const rows = [];')
    _re = blk.index('return { career: res.career')
    _rows_ok = '仲差' not in blk[_rs:_re] and blk.count('仲差') == 1
ok('LADDER 數字行唔出（梯三行程式碼入面冇「仲差」；「仲差」只出現喺區塊頭註解講禁令嗰句）', _rows_ok)
ok('LADDER 質性三行：獎／擔正組合／主線脊骨',
   '獎：已經取得獎項。' in blk and '擔正組合：尚未齊全，欠' in blk and '主線：尚未走完整條主線。' in blk)
ok('LADDER gaps95 句子唔逐字照搬（回望口吻註解有交代）',
   '唔逐字照搬' in blk and '頒獎禮嗰幾晚' in blk)

# --- (3c) 已攞獎項數目＋跳轉 ---
ok('AWARDS 數目重用 end95Awards(S).wins', 'end95Awards' in blk)
ok('AWARDS 跳轉重用 setHomeTab("awards")', 'setHomeTab("awards")' in blk)
ok('AWARDS 唔複製獎項頁（區塊內冇 awards-list 渲染）', 'awards-list' not in blk)

# --- (4) 進度頁頂一行 ---
ok('PROG 進度頁頂有現時稱號行（同一來源 helper）',
   'titles162ProgressLine162()' in src and 'progTitleLine162' in src)
ok('PROG 嗰行喺 renderProgressPane71 入面', 'progTitleLine162' in src
   and src.index('function renderProgressPane71') < src.index('progTitleLine162')
   < src.index('function phase2GateFingerprint'))

# --- 弱印取捨：ensureWeakSeals 留返唔郁 ---
ok('SEAL ~8% 淡印留返（ensureWeakSeals 仲喺度，aria-hidden 裝飾）',
   'function ensureWeakSeals(){' in src and 'aria-hidden","true"' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
