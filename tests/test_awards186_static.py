# v20a186 修 v184 設計 review 新 C1 static tests：
# 兩類獎項嗰陣，結果卡「同屆提名」行重複兩次——renderAwardResultHtml 逐類別卡
# 各出一行同一份名單。修法：同屆提名行由逐類別卡內移出，取排序後第一個有
# fellows63 嘅類別，喺卡列之後獨立一行；helper awards63FellowsHtml 本身、數據、
# 判定、fellows 池、贏線、請柬（awards63InviteBitHtml）一字唔郁。
# 反證: run against pristine main (b1b6092) index -> 逐類別 felBit63 仲喺度 -> FAIL（唔 crash）。
import sys, re

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0: return src[i:k+1]
    return ''

result_fn = slice_fn('renderAwardResultHtml')
invite_fn = slice_fn('renderAwardInviteHtml')
helper_fn = slice_fn('awards63FellowsHtml')

# --- C1：同屆提名行只出一次 ---
chk('C1 逐類別 felBit63 已拎走（map 入面唔再出同屆提名）', 'felBit63' not in result_fn)
chk('C1 單一 fellows 行 felBit186 在位（取第一個有 fellows63 嘅類別）',
    'felCat186' in result_fn and 'fellows63' in result_fn and '.find(' in result_fn)
chk('C1 單一 fellows 行經同一 helper 出（內容逐字不變）', 'awards63FellowsHtml(felCat186)' in result_fn)
chk('C1 helper 喺結果卡只呼叫一次（唔係每類一次）', result_fn.count('awards63FellowsHtml') == 1)
chk('C1 fellows 行喺卡列之後（${catsHtml} 之後、報紙卡之前）',
    '${catsHtml}' in result_fn and '${felBit186}' in result_fn and 'psr-press' in result_fn
    and result_fn.index('${catsHtml}') < result_fn.index('${felBit186}') < result_fn.index('psr-press'))
chk('C1 冇 fellows 嗰陣唔出空行（felCat186 無就空字串）', '|| null' in result_fn and '""' in result_fn)
chk('C1 類別卡其餘內容唔郁（kicker／rep／weak／comfort 齊）',
    'repBit62' in result_fn and 'weakBit62' in result_fn and 'comfortBit147' in result_fn)
chk('C1 結果卡 focus 格行先、其餘格維持固定 id 排序（v184 C2 唔郁，v192 C3 疊加）', 'awardsCatsSorted184(pack)' in result_fn)

# --- 唔郁嘅嘢 ---
chk('helper awards63FellowsHtml 本身唔郁（得主標記＋名單格式）',
    '同屆提名' in helper_fn and '為得主' in helper_fn and 'f.star' in helper_fn)
chk('請柬同屆提名唔郁（awards63InviteBitHtml 照用）', 'awards63InviteBitHtml' in invite_fn)
chk('獎項頁同屆提名唔郁（fellowsTxt 照喺 renderAwardsPane62）',
    'fellowsTxt' in slice_fn('renderAwardsPane62'))
chk('build 層 fellows 衍生唔郁', 'fellows63' in slice_fn('buildAwardResultPack'))
chk('唔直改 content pack（index 無 content/ 寫入）', 'content/STUB_AWARDS' not in src and 'content/SCHEMA_AWARDS' not in src)

# --- 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變（s107）', 's107' in src)
chk('產品 ?v 不變（v20a10）', 'v20a10' in src)
chk('贏線不變（0.875）', 'const AWARDS62_WIN_LINE = 0.875' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
