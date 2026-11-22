# v377 resync: index.html net +15 lines (advanceDay phase sync +5 @~20333,
# countYearMediumWraps comment +1 @~31511, awards62YearWorks cumulative +3 @~32966,
# scoreParts spec gate +6 @~33109 -- wait, total +15: +5+1+3+6=15).
# Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap377.json')).items()}

def remap(text, nums, label):
    """Replace each number in nums (as standalone token) with mapped value, single pass."""
    pat = re.compile(r'\b(' + '|'.join(str(n) for n in nums) + r')\b')
    def sub(m):
        old = int(m.group(1))
        new = mapping.get(old)
        if new is None:
            print(f'  !! {label}: {old} UNMAPPED')
            return m.group(1)
        return str(new)
    out, n = pat.subn(sub, text)
    print(f'{label}: {n} replacements')
    return out

def load(p): return open(p, encoding='utf-8').read()
def save(p, t): open(p, 'w', encoding='utf-8').write(t)

# --- rom176: line(42051), line(42403), line(43706), line(43867) ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [42051, 42403, 43706, 43867], 'rom176')
save(p, t)

# --- rom159: line_has(26576), line_has(27470), line_has(27325), idx_lines[26604-1] ---
p = 'tests/test_rom159_static.py'
t = load(p)
t = remap(t, [26576, 27470, 27325, 26604], 'rom159')
save(p, t)

# --- travel114: free-list line numbers ---
p = 'tests/test_travel114_static.py'
t = load(p)
t = remap(t, [25829, 27175, 27176, 27252, 29549, 29582, 41849], 'travel114')
save(p, t)

# --- tang171/tang173/gift185: total 48624 -> 48639 (count('\n')), openLoc 43826 -> 43841 ---
# total is a literal in assertion; handle separately (not via linemap since it's a count)
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py']:
    t = load(p)
    t2 = remap(t, [43826], p + ' openLoc')
    t2 = t2.replace("html.count('\\n') == 48624", "html.count('\\n') == 48639")
    t2 = t2.replace("總行數 48624（", "總行數 48639（")
    t2 = t2.replace("＋v376 +23）", "＋v376 +23＋v377 +15）")
    save(p, t2)
    print(p, 'total/openLoc updated')

print('done')
