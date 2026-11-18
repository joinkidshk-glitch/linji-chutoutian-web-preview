# v20a290 resync（travel114）：index.html 淨 +461 行（DLG×5 ＋369＠舊 L38585 起／STARS＋PILOT＋
# STAGEUP／CAP／WRAP ＋32／SP176＋7／FAV176＋11／GEN176＋11／onWrap 註解＋1／人脈頁 guard＋3／SIGHTINGS＋27；
# 總行數 46256→46717）。COUNT_LINES／FREE_LINES／DEF_LINE／WRAPPER_LINE 按 difflib 映射重寫，
# 內容逐字核實純漂移；openLoc( 呼叫點序列逐字一致，總數不變；ok() 名／註解入面嘅 Lxxxxx 歷史標籤唔郁。
# 用法：python3 qa290/resync114_290.py [--apply]
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path('/home/hatch/workspace/linji-work290')
OLD = subprocess.run(['git', 'show', 'HEAD:index.html'], cwd=ROOT, capture_output=True, text=True).stdout.split('\n')
NEW = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print(f'old lines={len(OLD)} new lines={len(NEW)} net={len(NEW)-len(OLD)}')

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print(f'mapped equal lines: {len(mapping)}')

# openLoc( 呼叫點序列逐字一致（index.html 內）
old_calls = [ln for ln in OLD if 'openLoc(' in ln]
new_calls = [ln for ln in NEW if 'openLoc(' in ln]
print(f'openLoc( lines: old={len(old_calls)} new={len(new_calls)} identical={old_calls == new_calls}')
problems = []
if old_calls != new_calls:
    problems.append('openLoc( 呼叫點序列唔一致（有新增／刪除／改寫）')

tf = ROOT / 'tests' / 'test_travel114_static.py'
text = tf.read_text(encoding='utf-8')

def remap_set(name):
    m = re.search(name + r' = \{(.*?)\}', text, flags=re.S)
    assert m, name
    nums = [int(x) for x in re.findall(r'\b(\d+)\b', m.group(1))]
    out = []
    for n in nums:
        if n not in mapping:
            problems.append(f'{name}: {n} 無 difflib 對位')
            continue
        m_new = mapping[n]
        if OLD[n - 1].strip() != NEW[m_new - 1].strip():
            problems.append(f'{name}: {n}->{m_new} 內容唔同：OLD={OLD[n-1].strip()[:80]!r} NEW={NEW[m_new-1].strip()[:80]!r}')
        out.append((n, m_new))
    return m, out

count_m, count_out = remap_set('COUNT_LINES')
free_m, free_out = remap_set('FREE_LINES')
for name, val in (('DEF_LINE', 41498), ('WRAPPER_LINE', 28695)):
    mm = re.search(name + r' = (\d+)', text)
    assert mm, name
    old_n = int(mm.group(1))
    assert old_n == val, f'{name} 預期 {val}，實為 {old_n}'
    new_n = mapping[old_n]
    if OLD[old_n - 1].strip() != NEW[new_n - 1].strip():
        problems.append(f'{name}: {old_n}->{new_n} 內容唔同：OLD={OLD[old_n-1].strip()[:80]!r} NEW={NEW[new_n-1].strip()[:80]!r}')
    print(f'{name}: {old_n} -> {new_n}')
print(f'COUNT_LINES: {len(count_out)} 處 :: ' + '; '.join(f'{a}->{b}' for a, b in count_out if a != b))
print(f'FREE_LINES: {len(free_out)} 處 :: ' + '; '.join(f'{a}->{b}' for a, b in free_out if a != b))
print('PROBLEMS:')
for p in problems:
    print('  ' + p)
if not problems:
    print('  （無）')

if '--apply' in sys.argv and not problems:
    def sub_set(name, pairs):
        global text
        repl = dict(pairs)
        m = re.search(name + r' = \{(.*?)\}', text, flags=re.S)
        span = m.group(1)
        span2 = re.sub(r'\b(\d+)\b', lambda mm: str(repl[int(mm.group(1))]), span)
        text = text[:m.start(1)] + span2 + text[m.end(1):]
    sub_set('COUNT_LINES', count_out)
    sub_set('FREE_LINES', free_out)
    text = re.sub(r'DEF_LINE = \d+', f'DEF_LINE = {mapping[41498]}', text)
    text = re.sub(r'WRAPPER_LINE = \d+', f'WRAPPER_LINE = {mapping[28695]}', text)
    header = '# v20a290 resync：index.html 淨 +461 行；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（內容逐字核實純漂移；openLoc( 呼叫點序列逐字一致，總數不變；DEF 41498→41959、WRAPPER 28695 唔郁）。\n'
    if not text.startswith('# v20a290 resync'):
        text = header + text
    tf.write_text(text, encoding='utf-8')
    print('已寫入。')
elif '--apply' in sys.argv:
    print('有問題，唔寫入。')
else:
    print('(dry run；加 --apply 先寫入)')
