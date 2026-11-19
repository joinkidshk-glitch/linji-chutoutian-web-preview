# qa327/resync327b.py — v20a327 resync 續：rom159＋content JSON 豁免（suite 兜底）
# （第一跑 381／13：基線 9 項以外多出 4 項，全部核實係 v327 改動嘅直接後果，唔係回歸：
#  rom159 四個釘行純 −33 漂移；aud91fix122／124／newspaper214 三檔 content JSON 守門
#  係因為本包有意刪咗 content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json 嘅 overdueSoftLock 一行，
#  按慣例（v157／v217／…／v268／v297）加 _v327_allowed 豁免）。
# 用法：python3 qa327/resync327b.py  （喺工作副本根目錄行；只改 4 檔測試，唔郁 index.html）
import subprocess

NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()
assert len(OLD) == 47280 and len(NEW) == 47244, (len(OLD), len(NEW))

def replace_once(path, old, new, expect=1):
    s = open(path, encoding='utf-8').read()
    n = s.count(old)
    assert n == expect, (path, old[:70], n, expect)
    open(path, 'w', encoding='utf-8').write(s.replace(old, new))
    print('  %s: replaced %r (x%d)' % (path, old[:60], n))

def prepend_header(path, line):
    s = open(path, encoding='utf-8').read()
    assert not s.startswith(line), path
    open(path, 'w', encoding='utf-8').write(line + '\n' + s)
    print('  %s: header added' % path)

# ---- rom159：4 個釘行各 −33（全部喺 17563–35369 區；ok() 名入面嘅 L 號係歷史標籤，唔郁） ----
for old_n, frag in [(25457, 'v20a159 ROM159 Phase 1'),
                    (26305, 'COMMIT48_NODES.CMT_lan_commit'),
                    (26206, 'function rom159SoMeetGate')]:
    new_n = old_n - 33
    replace_once('tests/test_rom159_static.py', 'line_has(%d,' % old_n, 'line_has(%d,' % new_n)
    assert frag in NEW[new_n - 1], (new_n, frag, NEW[new_n - 1][:80])
replace_once('tests/test_rom159_static.py', 'idx_lines[25485 - 1]', 'idx_lines[25452 - 1]')
assert '查實' in NEW[25452 - 1], NEW[25451][:80]
assert open('index.html', encoding='utf-8').read().count('全佳') == 1
prepend_header('tests/test_rom159_static.py',
    '# v20a327 resync：index.html 淨 −36 行（刪死鎖；4 個釘行各 −33（25457→25424、26305→26272、26206→26173、全佳 25485→25452；8241／10699／14774 喺刪除點之前唔郁），內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁，見 qa327/resync327b.py）。')

# ---- content JSON 守門豁免：三檔加 _v327_allowed ----
V327_DEF = """    # v327 豁免（死鎖刪除，已拍板）：content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json 刪 overdueSoftLock 一行
    # （死鎖成把刪走，schema 唔留死引用）。
    _v327_allowed = {'content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json'}"""
V268_LINE = "    _v268_allowed = {'content/story_detail_romance_tang.json'}"
for path in ['tests/test_aud91fix122_static.py', 'tests/test_aud91fix124_static.py',
             'tests/test_newspaper214_award_static.py']:
    replace_once(path, V268_LINE, V268_LINE + '\n' + V327_DEF)
    replace_once(path, '_rw8_allowed | _v268_allowed', '_rw8_allowed | _v268_allowed | _v327_allowed')
# aud122／124 嘅 ok() 名列明豁免版本，加 v327；newspaper214 嘅 X05 名無版本表，唔郁
for path in ['tests/test_aud91fix122_static.py', 'tests/test_aud91fix124_static.py']:
    replace_once(path, '＋v268 豁免以外一律唔准郁', '＋v268＋v327 豁免以外一律唔准郁')

print('resync327b done')
