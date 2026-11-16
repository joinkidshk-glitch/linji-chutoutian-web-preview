# v20a88 FIX88 靜態測試：修復標記在位、SAVE/softRev/?v= 冇變、NOTES 在位、
# 四個板面呼叫點全數改用提早窗判準、B3 冬季入門改由新庫 entryGigPool229 承接、
# 12 張舊冬季工已刪、冇真藝人名。
# 反證：v87 index 冇 FIX88 標記 → FAIL。
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
ok('NOTES_V20A88 文件在位', os.path.exists(os.path.join(ROOT, 'NOTES_V20A88_GIGFIX.md')))
ok('FIX88 模組標記在位', 'v20a88 FIX88' in html)
ok('EARLY88 模組標記在位', 'v20a88 EARLY88' in html)
ok('GIG_REQ_KEYS88 在位', 'const GIG_REQ_KEYS88 = {' in html)
ok('normalizeGigRecord 剝鍵段在位', 'FIX88-A（根治 v66 幻影門檻）' in html)
ok('reqGap 防禦在位', 'FIX88-A 防禦' in html)
ok('提早窗判準函數在位', 'function gigSeasonHidden88(g, cur)' in html and 'function gigSeasonEarlyVisible88(g)' in html)
ok('提早窗 = 60 日', 'const GIG_SEASON_LEAD88 = 60;' in html)
ok('上映行函數在位', 'function gigReleaseLine88(g)' in html)
ok('詳情頁檔期行接線', 'releaseRow88' in html)
ok('板面函數改用提早窗判準', 'gigSeasonHidden88(g, curSeason)' in html)
ok('入門池改用提早窗判準', 'gigSeasonHidden88(g, cur)' in html)
ok('openLoc scrub 改用提早窗判準', 'gigSeasonHidden88(gig, calendarSeason())' in html)
ok('B3 冬季入門陣列已刪（WINTER_ENTRY_GIGS_88 唔再存在）', 'WINTER_ENTRY_GIGS_88' not in html)
ok('冬季橋接陣列＋合併在位', 'const WINTER_BRIDGE_GIGS_88 = [' in html and 'function mergeWinterBridge88()' in html)
ok('B3 入門合併改由新庫篩出（entryGigPool229）', 'function entryGigPool229(' in html and 'entryGigPool229()' in html)
ok('B3 12 張舊冬季工已刪', 'gig_1988_entry_winter_' not in html and 'gig_1988_winter88_bridge_' not in html)
# B3：冬季入門覆蓋由新庫 entryGigPool229 承接——1990 冬季有 4 張臨記工過到開局門檻
# （v20a252 新庫重生成：16→4，見 NOTES；數字係庫實數，唔係設計下限——跌穿要由庫工人覆核）
import json as _json
_pack = _json.load(open(os.path.join(ROOT, 'content', 'gigs_new.json'), encoding='utf-8'))
_open = {'acting':18,'stage':14,'vocal':14,'looks':22,'charm':16,'iq':20,'stamina':75}
_winter_entry = [g for g in _pack['gigs'] if g['year']==1990 and g['season']=='冬' and g['tier']=='臨記'
                 and all(v <= _open.get(k, 0) for k, v in g['req'].items())]
ok('B3 新庫 1990 冬季入門覆蓋（4 張臨記工過開局門檻）', len(_winter_entry) == 4)
seg_start = html.index('function entryGigPool229(')
seg_end = html.index('function mergeEntryGigsIntoPool(')
seg = html[seg_start:seg_end]
ok('入門池段冇真藝人名', not any(n in seg for n in ['周星馳','劉德華','張國榮','周潤發','梁朝偉','梅艷芳','張曼玉','王祖賢','鍾楚紅','林青霞']))

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
