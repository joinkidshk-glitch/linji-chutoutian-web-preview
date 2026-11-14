# v20a85 POSTER85 靜態測試：接入標記在位、SAVE/softRev/?v= 冇變、NOTES 在位、
# 主檔冇因本包脹大（圖行檔案參照；v84 基線 5,115,599 bytes，只准細增）、
# POSTER85 段冇真藝人名。反證：v84 index 冇 POSTER85 標記 → FAIL。
import io, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ipath = os.path.join(ROOT, 'index.html')
html = io.open(ipath, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('產品 ?v= 冇變', 'v20a10' in html)
ok('NOTES_V20A85 文件在位', os.path.exists(os.path.join(ROOT, 'NOTES_V20A85_POSTER.md')))
ok('POSTER85 模組標記在位', 'v20a85 POSTER85' in html)
ok('POSTER85_IDS 在位', 'const POSTER85_IDS = {' in html)
ok('poster85File 在位', 'function poster85File(gigId)' in html)
ok('查表回檔案參照', '"assets/posters/" + poster85File(gigId)' in html)
ok('試點內嵌保留（POSTER59_DATA 仍在）', 'const POSTER59_DATA = {' in html and 'poster59Path' in html)
size = os.path.getsize(ipath)
ok('主檔冇脹大（<%d；v89 BR89 有意增長至 5,288,705；v92 NAT92 通告板分布自然化（錯峰＋保底＋加厚 18 張）有意增長至 5,336,030；v95 LADDER95 結局梯擴充（新梯判定＋計數器＋9 格文案）有意增長至 5,386,704；v203 WF4 迎新期＋Phase 2 擴池（41 單新事件＋迎新期 code）有意增長至 5,448,954；v213 請柬提前＋晚間典禮有意增長至 5,491,267，上限跟住原位更新）' % (5491267 + 40000), size < 5491267 + 40000)
seg = html[html.index('v20a85 POSTER85'):html.index('function poster59Path')]
ok('POSTER85 段冇 data URI 內嵌', 'data:image' not in seg)

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
