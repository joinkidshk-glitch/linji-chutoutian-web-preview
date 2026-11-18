# v20a290 resync：index.html 淨 +461 行（DLG×5 ＋369＠舊 L38585 起／STARS＋PILOT＋STAGEUP／CAP／WRAP
# ＋32＠舊 L38592–38628／SP176＋7／FAV176＋11／GEN176＋11／onWrap 註解＋1／人脈頁 guard＋3／SIGHTINGS＋27；
# 總行數 46256→46717）。釘行按 difflib 映射重寫，內容逐字核實純漂移；ok() 名入面嘅 Lxxxxx 歷史標籤唔郁；
# 總行數斷言＋鏈尾標籤＋openLoc DEF 標籤／guard 一併更新（＋v290 +461）。
# 用法：python3 qa290/resync290.py [--apply]
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path('/home/hatch/workspace/linji-work290')
OLD = subprocess.run(['git', 'show', 'HEAD:index.html'], cwd=ROOT, capture_output=True, text=True).stdout.split('\n')
NEW = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print(f'old lines={len(OLD)} new lines={len(NEW)} net={len(NEW)-len(OLD)}')

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
mapping = {}  # old 1-based lineno -> new 1-based lineno (equal blocks only)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print(f'mapped equal lines: {len(mapping)}')

def drift_ok(old_n, new_n):
    return OLD[old_n - 1].rstrip() == NEW[new_n - 1].rstrip()

# anchor patterns: (regex, group index of the number, kind)
# 注意：tests 用嘅 lines[] 係 0-based index（lines[41497]＝1-based 41498 行）；均匀漂移區內
# mapping[N] 同 mapping[N+1]-1 數值相同，取代值啱；內容核實額外用 DEF 行直接對過（見下）。
PATTERNS = [
    (re.compile(r'\bline\((\d+)\)'), 1, 'line()'),
    (re.compile(r'\b(?:idx_lines|lines|html_lines)\[(\d+)\s*-\s*1\]'), 1, 'lines[N-1]'),
    (re.compile(r'\b(?:idx_lines|lines|html_lines)\[(\d+)\]'), 1, 'lines[N]'),
]
TOTAL_OLD = 46256
TOTAL_NEW = 46717

apply = '--apply' in sys.argv
touched = {}
problems = []
for tf in sorted((ROOT / 'tests').glob('test_*.py')):
    text = tf.read_text(encoding='utf-8')
    has_line_helper = bool(re.search(r'def line\(n\)', text))
    repl = {}  # exact old snippet -> new snippet (single-scan dict)
    notes = []
    # total-count assertions + chain labels
    if str(TOTAL_OLD) in text:
        if f"== {TOTAL_OLD}" in text:
            repl[f'== {TOTAL_OLD}'] = f'== {TOTAL_NEW}'
            notes.append(f'total == {TOTAL_OLD} -> {TOTAL_NEW}')
        m = re.search(re.escape(f'總行數 {TOTAL_OLD}') + r'（(.*?)）', text)
        if m and 'v289 +36' in m.group(1):
            old_label = f'總行數 {TOTAL_OLD}（{m.group(1)}）'
            new_label = f'總行數 {TOTAL_NEW}（{m.group(1)}＋v290 +461）'
            repl[old_label] = new_label
            notes.append(f'total label {TOTAL_OLD} -> {TOTAL_NEW}')
    # openLoc DEF 標籤＋guard（tang171／tang173）：標籤「DEF 行 41498（…＋v289 +36，travel114 釘行）」→
    # 41959＋鏈尾 ＋v290 +461；guard len(lines) >= 41504（＝DEF 行＋6）→ 41965。數值經 difflib 核實：
    # 舊 1-based 41498／新 1-based 41959 皆為 'function openLoc(id, opts){'。
    if 'openLoc DEF 行 41498' in text:
        repl['openLoc DEF 行 41498'] = 'openLoc DEF 行 41959'
        notes.append('openLoc DEF 標籤 41498 -> 41959')
        if '＋v289 +36，travel114 釘行）' in text:
            repl['＋v289 +36，travel114 釘行）'] = '＋v289 +36＋v290 +461，travel114 釘行）'
            notes.append('openLoc DEF 鏈尾 ＋v290 +461')
    if 'len(lines) >= 41504' in text:
        repl['len(lines) >= 41504'] = 'len(lines) >= 41965'
        notes.append('openLoc guard 41504 -> 41965')
    for rx, gi, kind in PATTERNS:
        if kind == 'line()' and not has_line_helper:
            continue
        for mm in rx.finditer(text):
            n = int(mm.group(gi))
            if n not in mapping:
                problems.append(f'{tf.name}: {kind} {n} 無 difflib 對位（改動區內／已刪行）')
                continue
            m_new = mapping[n]
            if m_new == n:
                continue
            if not drift_ok(n, m_new):
                problems.append(f'{tf.name}: {kind} {n}->{m_new} 內容唔同，非純漂移：OLD={OLD[n-1][:80]!r} NEW={NEW[m_new-1][:80]!r}')
                continue
            old_snip = mm.group(0)
            new_snip = old_snip.replace(str(n), str(m_new), 1)
            if old_snip != new_snip:
                repl[old_snip] = new_snip
                notes.append(f'{kind} {n} -> {m_new}')
    if repl:
        touched[tf.name] = (notes, repl)
        if apply:
            # single-scan substitution over all snippets in this file
            keys = sorted(repl, key=len, reverse=True)
            rx_all = re.compile('|'.join(re.escape(k) for k in keys))
            text2 = rx_all.sub(lambda m: repl[m.group(0)], text)
            header = '# v20a290 resync：index.html 淨 +461 行；釘行按 difflib 映射重寫（內容逐字核實純漂移；ok() 名入面嘅 Lxxxxx 歷史標籤唔郁）；總行數 46256→46717。\n'
            if not text2.startswith('# v20a290 resync'):
                text2 = header + text2
            tf.write_text(text2, encoding='utf-8')
        print(f'{tf.name}: {len(notes)} 處 :: ' + '; '.join(notes))

print(f'\nTOUCHED FILES: {len(touched)}')
print('PROBLEMS:')
for p in problems:
    print('  ' + p)
if not problems:
    print('  （無）')
if not apply:
    print('\n(dry run；加 --apply 先寫入)')
