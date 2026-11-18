#!/usr/bin/env python3
# v20a298 resync：index.html 淨 +143 行（Q11 拒單債到期循環）
#   插入點（舊行號）：advanceDay tick ＋2 @舊 L19559 後／mergeFavorGigs 改寫＋ripple block
#   ＋140 @舊 L22881 起／手帳 backfill ＋1 @舊 L27996 後。
# 做法：difflib 對位 pristine main → 新檔，逐個釘行核實內容逐字相同（純漂移）先改；
#   替換用單次掃描 dict 查表（一個 regex alternation 一次過，唔逐對 re.sub，免重疊 pair 食錨點）。
# 用法：python3 qa298/resync298.py [repo-root]（預設 ../，即 linji-work298）
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
PRISTINE = Path('/tmp/pristine298.html')
NEW = ROOT / 'index.html'

pris = PRISTINE.read_text(encoding='utf-8').splitlines()
new = NEW.read_text(encoding='utf-8').splitlines()
print(f'pristine {len(pris)} 行，新檔 {len(new)} 行，淨 {len(new) - len(pris):+d}')

# difflib 對位：equal 區先有舊→新行號映射
mapping = {}
sm = difflib.SequenceMatcher(None, pris, new, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
print(f'對位 equal 行：{len(mapping)}')

def mapped(old):
    """舊行號 → 新行號，兼核實內容逐字相同；唔得就 raise。"""
    if old not in mapping:
        raise SystemExit(f'MISMATCH：舊行 {old} 唔喺 equal 區（改動區內，唔係純漂移）')
    nw = mapping[old]
    if pris[old - 1].strip() != new[nw - 1].strip():
        raise SystemExit(f'MISMATCH：舊行 {old} vs 新行 {nw} 內容唔同：\n  舊：{pris[old - 1].strip()[:100]}\n  新：{new[nw - 1].strip()[:100]}')
    return nw

def single_pass(path, repl, header):
    """repl：{舊字串: 新字串}；一次 regex alternation 掃晒，唔逐對 sub。"""
    text = path.read_text(encoding='utf-8')
    for old in repl:
        if text.count(old) != 1:
            raise SystemExit(f'{path.name}：key 出現 {text.count(old)} 次（預期 1）：{old[:80]!r}')
    pat = re.compile('|'.join(re.escape(k) for k in sorted(repl, key=len, reverse=True)))
    text = pat.sub(lambda m: repl[m.group(0)], text)
    if header and not text.startswith(header):
        text = header + '\n' + text
    path.write_text(text, encoding='utf-8')
    print(f'{path.name}：改咗 {len(repl)} 處')
    return repl

HDR = '# v20a298 resync：index.html 淨 +143 行（Q11 拒單債到期循環：advanceDay tick ＋2 @舊 L19559 後／mergeFavorGigs 改寫＋ripple block ＋140 @舊 L22881 起／手帳 backfill ＋1 @舊 L27996 後；總行數 46670→46813；鏈尾加 ＋v298 +143）。\n'

# ---- gift185：總行數鏈（count 斷言分兩段 key，避開 backslash 轉義） ----
single_pass(ROOT / 'tests/test_gift185_static.py', {
    "ok('總行數 46670（": "ok('總行數 46813（",
    "＋v297 −64）', html.count(": "＋v297 −64＋v298 +143）', html.count(",
    "== 46670)": "== 46813)",
}, HDR)

# ---- tang171 / tang173：總行數鏈＋DEF 鏈＋guard ----
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    single_pass(ROOT / fname, {
        "ok('零行數漂移：總行數 46670（": "ok('零行數漂移：總行數 46813（",
        "＋v297 −64）', src.count(": "＋v297 −64＋v298 +143）', src.count(",
        "== 46670)": "== 46813)",
        "openLoc DEF 行 41917（": "openLoc DEF 行 42060（",
        "＋v297 −59，travel114 釘行）',": "＋v297 −59＋v298 +143，travel114 釘行）',",
        "len(lines) >= 41923 and 'function openLoc(id, opts){' in lines[41916])":
            "len(lines) >= 42066 and 'function openLoc(id, opts){' in lines[42059])",
    }, HDR)

# ---- rom159：4 釘（8241／10699／14782 喺插入點之前唔郁） ----
r159 = {old: mapped(old) for old in (25081, 25929, 25830, 25109)}
print('rom159 映射：', r159)
single_pass(ROOT / 'tests/test_rom159_static.py', {
    'line_has(25081, "v20a159 ROM159 Phase 1")': f'line_has({r159[25081]}, "v20a159 ROM159 Phase 1")',
    'line_has(25929, "COMMIT48_NODES.CMT_lan_commit")': f'line_has({r159[25929]}, "COMMIT48_NODES.CMT_lan_commit")',
    'line_has(25830, "function rom159SoMeetGate")': f'line_has({r159[25830]}, "function rom159SoMeetGate")',
    'idx_lines[25109 - 1]': f'idx_lines[{r159[25109]} - 1]',
}, '# v20a298 resync：index.html 淨 +143 行；4 個釘行按段重算（25081→%d、25929→%d、25830→%d、全佳 25109→%d；8241／10699／14782 喺插入點之前唔郁），內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。\n' % (r159[25081], r159[25929], r159[25830], r159[25109]))

# ---- rom176：4 釘（6321／14780 喺插入點之前唔郁） ----
r176 = {old: mapped(old) for old in (40152, 40502, 41802, 41958)}
print('rom176 映射：', r176)
single_pass(ROOT / 'tests/test_rom176_static.py', {
    f'line({old})': f'line({nw})' for old, nw in r176.items()
}, '# v20a298 resync：index.html 淨 +143 行；4 個釘行各 ＋143（40152→%d、40502→%d、41802→%d、41958→%d；6321／14780 喺插入點之前唔郁），內容逐字核實純漂移；L55647 等名唔郁。\n' % (r176[40152], r176[40502], r176[41802], r176[41958]))

# ---- travel114：COUNT／FREE／DEF／WRAPPER 全部按 difflib 映射 ----
t114 = ROOT / 'tests/test_travel114_static.py'
ttext = t114.read_text(encoding='utf-8')
m_count = re.search(r'COUNT_LINES = \{([^}]*)\}', ttext, re.S)
m_free = re.search(r'FREE_LINES = \{([^}]*)\}', ttext, re.S)
pins = [int(x) for x in re.findall(r'\b\d+\b', m_count.group(1))]
pins += [int(x) for x in re.findall(r'\b\d+\b', m_free.group(1))]
pins += [41917, 28674]  # DEF_LINE、WRAPPER_LINE
print(f'travel114 釘點：COUNT {len(pins) - 40 - 2}＋FREE 40＋DEF／WRAPPER 2＝{len(pins)} 處')
repl114 = {}
for old in sorted(set(pins)):
    nw = mapped(old)
    # list 項：整行做 key（含註解，唯一）；DEF／WRAPPER：賦值行做 key
    if old == 41917:
        repl114['DEF_LINE = 41917'] = f'DEF_LINE = {nw}'
    elif old == 28674:
        repl114['WRAPPER_LINE = 28674'] = f'WRAPPER_LINE = {nw}'
    else:
        oldline = [l for l in ttext.splitlines() if re.match(r'^\s+' + str(old) + r',', l)]
        if len(oldline) != 1:
            raise SystemExit(f'travel114：list 項舊行 {old} 搵到 {len(oldline)} 行')
        repl114[oldline[0]] = oldline[0].replace(str(old), str(nw), 1)
print('travel114 映射（舊→新，唔郁者略）：', {o: mapping[o] for o in sorted(set(pins)) if mapping[o] != o})
single_pass(t114, repl114,
            '# v20a298 resync：index.html 淨 +143 行；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 41917→%d、WRAPPER 28674→%d；內容逐行核實純漂移；openLoc( 呼叫點總數不變）。\n' % (mapping[41917], mapping[28674]))

print('RESYNC298 DONE')
