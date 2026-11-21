# -*- coding: utf-8 -*-
# v369c travel114 修復：resync369b 嘅 r_travel_set 喺 m==n 時 return None，re.sub 將數字食咗。
#   由 git HEAD（b211dd2）版重做：difflib 對位去現行 index.html（48094 行），逐行核實內容逐字相同；
#   m==n 時原樣保留（修正）。另加 v369 兩處新 COUNT 呼叫點。
# 用法：python3 qa369/resync369c_travel.py [--apply]
import difflib, re, subprocess, sys

ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
APPLY = '--apply' in sys.argv

def git_lines(ref):
    out = subprocess.run(['git', 'show', '%s:index.html' % ref], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, ref
    return out.stdout.split('\n')

base = git_lines('b211dd2')
with open('%s/index.html' % ROOT, encoding='utf-8') as f:
    head_src = f.read()
head = head_src.split('\n')

sm = difflib.SequenceMatcher(None, base, head, autojunk=False)
MAP = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            MAP[i1 + 1 + k] = j1 + 1 + k

def map1(n):
    m = MAP.get(n)
    if m is None or base[n - 1] != head[m - 1]:
        return None
    return m

def r_travel_set(mo):
    n = int(mo.group(1)); m = map1(n)
    if m is None:
        print('travel114 UNMAPPED %d' % n)
        return mo.group(0)
    if m == n: return mo.group(0)
    return '%d,' % m

def r_travel_def(mo):
    n = int(mo.group(2)); m = map1(n)
    if m is None or m == n: return mo.group(0)
    print('travel114 %s %d -> %d' % (mo.group(1), n, m))
    return mo.group(1) + str(m)

with open('%s/tests/test_travel114_static.py' % ROOT, encoding='utf-8') as f:
    tsrc = f.read()
torig = tsrc
for name in ['COUNT_LINES', 'FREE_LINES']:
    mm = re.search(name + r' = \{(.*?)\n\}', tsrc, re.S)
    assert mm, name
    block = mm.group(1)
    newblock = re.sub(r'(\d+),', r_travel_set, block)
    tsrc = tsrc[:mm.start(1)] + newblock + tsrc[mm.end(1):]
tsrc = re.sub(r'(DEF_LINE = )(\d+)', r_travel_def, tsrc)
tsrc = re.sub(r'(WRAPPER_LINE = )(\d+)', r_travel_def, tsrc)
# v369 新增呼叫點（現行行號，grep 核實）
NEW_COUNT = [(22727, 'v369 openAskPicker369 單一打聽地點直入（計出行）'),
             (22728, 'v369 openAskPicker369 多地點揀場入場（計出行）')]
for ln_no, why in NEW_COUNT:
    assert 'openLoc(' in head[ln_no - 1], (ln_no, head[ln_no - 1])
    entry = '    %d,  # %s\n' % (ln_no, why)
    if entry.strip() not in tsrc:
        mm = re.search(r'COUNT_LINES = \{\n', tsrc)
        assert mm
        tsrc = tsrc[:mm.end()] + entry + tsrc[mm.end():]
        print('travel114 COUNT += %d' % ln_no)
# 檔頭 resync 註解
hdr = ('# v20a369 resync：index.html 淨 +181 行（UI369 CSS＋JS＋HTML 掣／票角＋殺青印（日結＋週加速摘要）＋送禮分級行＋StoryPlay rel 強調＋pin 可打聽／輕跳＋人情頁高亮排序）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移，見 qa369/resync369.py＋resync369c_travel.py（369b 食數 bug 修復重做）。\n'
       '# v369 新增 2 處 openLoc( 呼叫點（openAskPicker369 打聽揀場，入地點計出行，歸 COUNT）：呼叫點總數 +2。\n')
tsrc = hdr + tsrc
if tsrc != torig:
    print('travel114 changed')
    if APPLY:
        with open('%s/tests/test_travel114_static.py' % ROOT, 'w', encoding='utf-8') as f:
            f.write(tsrc)
print('APPLY' if APPLY else 'dry-run')
