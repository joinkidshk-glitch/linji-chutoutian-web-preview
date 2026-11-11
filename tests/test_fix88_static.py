# v20a88 FIX88 靜態測試：修復標記在位、SAVE/softRev/?v= 冇變、NOTES 在位、
# 四個板面呼叫點全數改用提早窗判準、12 張冬季工 id 齊全、冇真藝人名。
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
ok('冬季入門陣列在位', 'const WINTER_ENTRY_GIGS_88 = [' in html)
ok('冬季橋接陣列＋合併在位', 'const WINTER_BRIDGE_GIGS_88 = [' in html and 'function mergeWinterBridge88()' in html)
ok('入門合併接入冬季池', 'poolBase88.concat(poolW88)' in html or 'poolW88' in html)
for gid in ['gig_1988_entry_winter_cny_crew','gig_1988_entry_winter_market_ad','gig_1988_entry_winter_cny_crowd',
            'gig_1988_entry_winter_cinema_crowd','gig_1988_entry_winter_food_hand','gig_1988_entry_winter_rec_chorus',
            'gig_1988_winter88_bridge_cny_support','gig_1988_winter88_bridge_lion_dance','gig_1988_winter88_bridge_food_ad',
            'gig_1988_winter88_bridge_mtv','gig_1988_winter88_bridge_chase','gig_1988_winter88_bridge_tv_unit']:
    ok('冬季工在位 ' + gid, gid in html)
seg_start = html.index('v20a88 FIX88-B：冬季入門工')
seg_end = html.index('const WINTER_BRIDGE_GIGS_88')
seg = html[seg_start:seg_end]
ok('冬季入門段冇真藝人名', not any(n in seg for n in ['周星馳','劉德華','張國榮','周潤發','梁朝偉','梅艷芳','張曼玉','王祖賢','鍾楚紅','林青霞']))

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
