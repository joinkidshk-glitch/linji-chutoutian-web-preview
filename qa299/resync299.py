#!/usr/bin/env python3
# v20a299 resync：index.html 淨 +280 行（Q12 三旗跟進）
#   插入點（舊行號）：StoryPlay.start choi hook ＋1 @舊 L10699 後／Q12 通告池＋merge ＋235 @舊 L22979 後／
#   choi299PrepareNode ＋43 @舊 L27493 前／gigsForLocSeasonBoard merge hook ＋1 @舊 L43293 後。
#   段漂移：＜10700 唔郁；10700–22979 各 ＋1；22980–27492 各 ＋236；27493–43292 各 ＋279；≥43293 各 ＋280。
# 做法：difflib 對位 pristine main（/tmp/pristine299.html，main 631ef7a，46813 行）→ 新檔，
#   逐個釘行核實內容逐字相同（純漂移）先改；替換用單次掃描 dict 查表（一個 regex alternation 一次過，
#   唔逐對 re.sub，免重疊 pair 食錨點）。
# 用法：python3 qa299/resync299.py [repo-root]（預設 ../，即 linji-work299）
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
PRISTINE = Path('/tmp/pristine299.html')
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

HDR = '# v20a299 resync：index.html 淨 +280 行（Q12 三旗跟進：choi hook ＋1 @舊 L10699 後／Q12 池＋merge ＋235 @舊 L22979 後／choi299PrepareNode ＋43 @舊 L27493 前／merge hook ＋1 @舊 L43293 後；總行數 46813→47093；鏈尾加 ＋v299 +280）。\n'

# ---- gift185：總行數鏈 ----
single_pass(ROOT / 'tests/test_gift185_static.py', {
    "ok('總行數 46813（": "ok('總行數 47093（",
    "＋v298 +143）', html.count(": "＋v298 +143＋v299 +280）', html.count(",
    "== 46813)": "== 47093)",
}, HDR)

# ---- tang171 / tang173：總行數鏈＋DEF 鏈＋guard ----
defline = mapped(42060)
print('tang DEF 42060 →', defline)
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    single_pass(ROOT / fname, {
        "ok('零行數漂移：總行數 46813（": "ok('零行數漂移：總行數 47093（",
        "＋v298 +143）', src.count(": "＋v298 +143＋v299 +280）', src.count(",
        "== 46813)": "== 47093)",
        "openLoc DEF 行 42060（": f"openLoc DEF 行 {defline}（",
        "＋v298 +143，travel114 釘行）',": "＋v298 +143＋v299 +280，travel114 釘行）',",
        "len(lines) >= 42066 and 'function openLoc(id, opts){' in lines[42059])":
            f"len(lines) >= {defline + 6} and 'function openLoc(id, opts){{' in lines[{defline - 1}])",
    }, HDR)

# ---- rom159：5 釘（8241／10699 喺插入點之前唔郁） ----
r159 = {old: mapped(old) for old in (25223, 26071, 14782, 25972, 25251)}
print('rom159 映射：', r159)
single_pass(ROOT / 'tests/test_rom159_static.py', {
    'line_has(25223, "v20a159 ROM159 Phase 1")': f'line_has({r159[25223]}, "v20a159 ROM159 Phase 1")',
    'line_has(26071, "COMMIT48_NODES.CMT_lan_commit")': f'line_has({r159[26071]}, "COMMIT48_NODES.CMT_lan_commit")',
    'line_has(14782, "rom159ApplyGiftOverrides()")': f'line_has({r159[14782]}, "rom159ApplyGiftOverrides()")',
    'line_has(25972, "function rom159SoMeetGate")': f'line_has({r159[25972]}, "function rom159SoMeetGate")',
    'idx_lines[25251 - 1]': f'idx_lines[{r159[25251]} - 1]',
}, '# v20a299 resync：index.html 淨 +280 行；5 個釘行按段重算（25223→%d、26071→%d、14782→%d、25972→%d、全佳 25251→%d；8241／10699 喺插入點之前唔郁），內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。\n' % (r159[25223], r159[26071], r159[14782], r159[25972], r159[25251]))

# ---- rom176：5 釘（6321 喺插入點之前唔郁；14780 同行出現兩次，用成行做 key） ----
r176 = {old: mapped(old) for old in (14780, 40295, 40645, 41945, 42101)}
print('rom176 映射：', r176)
r176repl = {f'line({old})': f'line({nw})' for old, nw in r176.items() if old != 14780}
r176repl["   'GIFT_REACT = giftReact' in line(14780) and 'rom176ApplyGiftOverrides()' in line(14780))"] = \
    f"   'GIFT_REACT = giftReact' in line({r176[14780]}) and 'rom176ApplyGiftOverrides()' in line({r176[14780]}))"
single_pass(ROOT / 'tests/test_rom176_static.py', r176repl, '# v20a299 resync：index.html 淨 +280 行；5 個釘行按段重算（14780→%d、40295→%d、40645→%d、41945→%d、42101→%d；6321 喺插入點之前唔郁），內容逐字核實純漂移；L55647 等名唔郁。\n' % (r176[14780], r176[40295], r176[40645], r176[41945], r176[42101]))

# ---- tang152：2 個 0-based 索引（L31610／L31754 係 ok() 名入面嘅歷史標籤，唔郁） ----
t152 = {14708: mapped(14708), 14835: mapped(14835)}
print('tang152 映射（1-based 行）：', t152)
single_pass(ROOT / 'tests/test_tang152_static.py', {
    'lines()[14707]': f'lines()[{t152[14708] - 1}]',
    'lines()[14834]': f'lines()[{t152[14835] - 1}]',
}, '# v20a299 resync：index.html 淨 +280 行；2 個釘索引各 ＋1（14707→%d、14834→%d；插入點舊 L10699 之後），內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。\n' % (t152[14708] - 1, t152[14835] - 1))

# ---- text125：三錨點（報錯字串行號一併更新） ----
t125 = {old: mapped(old) for old in (11278, 11420, 16349)}
print('text125 映射：', t125)
single_pass(ROOT / 'tests/test_text125_static.py', {
    'if len(ls) < 11278 or FALLBACK not in ls[11277]:': f'if len(ls) < {t125[11278]} or FALLBACK not in ls[{t125[11278] - 1}]:',
    '"currentLine 第 11278 行冇 text fallback"': f'"currentLine 第 {t125[11278]} 行冇 text fallback"',
    'if len(ls) < 11420 or FALLBACK not in ls[11419]:': f'if len(ls) < {t125[11420]} or FALLBACK not in ls[{t125[11420] - 1}]:',
    '"advance 第 11420 行冇 text fallback"': f'"advance 第 {t125[11420]} 行冇 text fallback"',
    'if len(ls) < 16349 or': f'if len(ls) < {t125[16349]} or',
    "'if(typeof b.text === \"string\" && b.text){' not in ls[16348]": f"'if(typeof b.text === \"string\" && b.text){{' not in ls[{t125[16349] - 1}]",
    '"applyFamilySafeToNode 第 16349 行冇 b.text 分支"': f'"applyFamilySafeToNode 第 {t125[16349]} 行冇 b.text 分支"',
}, '# v20a299 resync：index.html 淨 +280 行；三錨點各 ＋1（currentLine 11278→%d、advance 11420→%d、applyFamilySafe 16349→%d；插入點舊 L10699 之後），內容逐字相同，純漂移；報錯字串行號一併更新。\n' % (t125[11278], t125[11420], t125[16349]))

# ---- travel114：COUNT／FREE／DEF／WRAPPER 全部按 difflib 映射 ----
t114 = ROOT / 'tests/test_travel114_static.py'
ttext = t114.read_text(encoding='utf-8')
m_count = re.search(r'COUNT_LINES = \{([^}]*)\}', ttext, re.S)
m_free = re.search(r'FREE_LINES = \{([^}]*)\}', ttext, re.S)
pins = [int(x) for x in re.findall(r'\b\d+\b', m_count.group(1))]
pins += [int(x) for x in re.findall(r'\b\d+\b', m_free.group(1))]
pins += [42060, 28817]  # DEF_LINE、WRAPPER_LINE
print(f'travel114 釘點：COUNT {len(pins) - 40 - 2}＋FREE 40＋DEF／WRAPPER 2＝{len(pins)} 處')
repl114 = {}
for old in sorted(set(pins)):
    nw = mapped(old)
    # list 項：整行做 key（含註解，唯一）；DEF／WRAPPER：賦值行做 key
    if old == 42060:
        repl114['DEF_LINE = 42060'] = f'DEF_LINE = {nw}'
    elif old == 28817:
        repl114['WRAPPER_LINE = 28817'] = f'WRAPPER_LINE = {nw}'
    else:
        oldline = [l for l in ttext.splitlines() if re.match(r'^\s+' + str(old) + r',', l)]
        if len(oldline) != 1:
            raise SystemExit(f'travel114：list 項舊行 {old} 搵到 {len(oldline)} 行')
        repl114[oldline[0]] = oldline[0].replace(str(old), str(nw), 1)
print('travel114 映射（舊→新，唔郁者略）：', {o: mapping[o] for o in sorted(set(pins)) if mapping[o] != o})
single_pass(t114, repl114,
            '# v20a299 resync：index.html 淨 +280 行；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 42060→%d、WRAPPER 28817→%d；內容逐行核實純漂移；openLoc( 呼叫點總數不變）。\n' % (mapping[42060], mapping[28817]))

print('RESYNC299 DONE')
