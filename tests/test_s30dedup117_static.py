# v20a117 S-30 DEDUP117・靜態守門測試：詳情區刪除＋唯一資料搬摘要＋欄卡 meta 拆行。
# 用法：python3 tests/test_s30dedup117_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」（舊寫法出現即 FAIL）——
# 喺 v20a115（未修）index 上跑，全檔必須 FAIL（見底註）。
# 只改版式／結構：v115 定落嘅文字一句唔郁；數字一概唔變；唔改 SAVE key／softRev／?v=。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def body_of(fname, span=12000):
    i = html.find(fname)
    return html[i:i + span] if i >= 0 else ''

b = body_of('function castingNoticeDetailHtml', 14000)
t = body_of('function gigBoardTeaserHtml', 6000)

# --- 1. 詳細區成段刪除：掣＋.cn-detail＋死接線＋死 CSS ---
ok('D1 「顯示詳細 ▾」掣已刪', '顯示詳細 ▾' not in html)
ok('D1 「收起詳細 ▴」已刪', '收起詳細 ▴' not in html)
ok('D1 .cn-detail 模板 div 已刪', '<div class="cn-detail"' not in html)
ok('D1 data-cn-toggle 接線 selector 已刪', '"[data-cn-toggle]"' not in html)
ok('D1 .cn-detail-toggle CSS 已刪', '.cn-detail-toggle{' not in html)
ok('D1 .cn-detail[hidden] CSS 已刪', '.cn-detail[hidden]' not in html)
ok('D1 詳細區條件表 CSS 已刪', '.notice_table_frame{' not in html and '.cn-cond-row{' not in html)
ok('D1 詳細區期間 bar CSS 已刪', '.notice_period_bar{' not in html)
ok('D1 詳細區導演／製作人行 CSS 已刪', '.cn-director-line{' not in html and '.cn-producer-line{' not in html)
ok('D1 死 roleLine helper 已刪（連同 .cn-role-line CSS）',
   'function gigRoleLineHtml' not in html and '.cn-role-line{' not in html)
ok('D1 詳細區舊 const／模板引用死咗（condParts／deadlineBar30v2／roleLine）',
   'const condParts' not in html and 'const deadlineBar30v2' not in html
   and '${deadlineBar30v2}' not in html and 'const roleLine' not in html)
ok('D1 摘要區共用 class 保留（.cn-kv／.cn-wd-sub／.notice_synopsis_frame）',
   '.cn-kv{' in html and '.cn-wd-sub{' in html and '.notice_synopsis_frame{' in html)

# --- 2. 唯一資料搬入摘要區（有料先出）---
_i_rel = b.find('${releaseRow88}')
_i_gaps = b.find('${sumGaps}')
ok('D2 摘要區有齊五個搬入位', all(x in b for x in
   ['${limitsHtml}', '${directorRow117}', '${producerLine}', '${weeklyRow117}', '${synopsisFrame117}']))
ok('D2 搬入行喺預計播出之後、差距提示之前（事實行尾）',
   0 < _i_rel < b.find('${limitsHtml}') < b.find('${directorRow117}') < b.find('${producerLine}') < b.find('${weeklyRow117}') < b.find('${synopsisFrame117}') < _i_gaps)
ok('D2 特殊限制：gigSpecialLimitsHtml 照用（空即隱藏）', 'const limitsHtml = gigSpecialLimitsHtml(g);' in b)
ok('D2 導演：只出真名 helper 在', 'function gigDirectorRealName117' in html and 'const directorRow117' in b)
ok('D2 導演：8 個職銜值＋fallback 全部喺 generic 集',
   all(x in html for x in ['"副導"', '"特輯副導"', '"副導阿標"', '"廣告助導"', '"場務阿強"', '"外景場記"', '"平面攝影師阿忠"', '"錄音室助導"', '"組製未公開"']))
ok('D2 導演：舊寫法「導演：${dir}」已刪', '導演：${dir}' not in html)
ok('D2 製作人：改行摘要區 cn-sum-row（文字不變）',
   '<div class="cn-sum-row"><span class="k">製作人</span><span class="v">${p}</span></div>' in html)
ok('D2 每週開工：只喺 total>1 先出', '(total > 1) ? weeklyBlock' in b)
ok('D2 每週開工：原句保留（每週最多 N 日＋實際只需 N 日條件）',
   '每週最多 ${weekly} 日' in b and '實際只需通告 ${total} 日（唔係每週做滿）' in b)
ok('D2 劇情簡介：搬入摘要（原樣 markup，唔係刪除）',
   'const synopsisFrame117' in b and '劇情簡介' in b and '${synopsisFrame117}' in b)
ok('D2 POSTER90 標記註保留（詳情頁仍唔出成品海報／主演行）', 'POSTER90' in b)

# --- 3. 通告欄卡片 meta 拆行（實駕：實際只得兩段） ---
ok('D3 meta 用 metaParts 逐行渲染', 'const metaParts=[pay, days].filter(Boolean);' in t)
ok('D3 每段一行（gt-meta-line）', 'gt-meta-line' in t and '.gt-meta-line{' in html)
ok('D3 舊寫法「 · 」串連已刪', 'join(" · ")' not in t)
ok('D3 兩段內容不變（片酬＋日數，渲染只讀 metaParts，冇憑空加第三段）',
   'const metaParts=[pay, days].filter(Boolean);' in t and 'metaParts.map(m=>' in t)
ok('D3 gt-meta 容器保留', '<div class="gt-meta">' in t)

# --- 4. 紀律：v115 文字＋紅線不變 ---
ok('D4 v115 簽約金行「獲聘後即收」仍在', '（獲聘後即收）' in b)
ok('D4 v115 舊寫法「接通告後即收」仍清零', '（接通告後即收）' not in html)
ok('D4 v115 var-note 三行短句仍在',
   '成數受表現／壓力／信用影響。<br>片酬牌面係約數，實收按合約。<br>獲聘先收三成簽約金，餘額殺青先收。' in b)
ok('D4 紅線 SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('D4 紅線 softRev s107 不變', 's107' in html)
ok('D4 紅線產品 ?v= v20a10 不變', 'v=20a10' in html)

print('---')
print('PASS' if not fails else 'FAIL: ' + '; '.join(fails))
sys.exit(1 if fails else 0)
