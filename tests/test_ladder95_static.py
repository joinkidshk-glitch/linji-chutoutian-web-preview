# v20a95 LADDER95 靜態測試：新梯標記在位、9 格名冊齊、計數器接線（normalize 種子＋殺青鈎）、
# E4→E3 舊相鄰分支已移除、SAVE/softRev/?v= 冇變、NOTES 在位、段內冇真藝人名。
# 反證：v94 index 冇 LADDER95 標記 → FAIL。
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
ok('NOTES_V20A95 文件在位', any(f.startswith('NOTES_V20A95') for f in os.listdir(ROOT)))
ok('LADDER95 模組標記在位', 'v20a95 LADDER95' in html)
ok('門檻表 ENDING95_T 在位', 'const ENDING95_T = {' in html)
ok('計數器函數在位', 'function careerStats95Of(st)' in html and 'function end95AddWrap(Sref, gig, sh)' in html)
ok('殺青鈎在位（wrapHistory unshift 之前）', 'end95AddWrap(S, _g95, sh);' in html)
_i95h = html.find('end95AddWrap(S, _g95, sh);')
_i95u = html.find('S.wrapHistory.unshift', _i95h)
ok('鈎位核實：同段 unshift 喺鈎之後', _i95h >= 0 and _i95u > _i95h)
ok('normalize 種子在位', 'o.careerStats95 = end95DeriveStats(o);' in html)
ok('fresh 預設 careerStats95: null', 'careerStats95: null, /* v20a95' in html)
for nm in ['SS: "一線巨星"', 'FK: "影壇天王"', 'TK: "電視天王"', 'SK: "歌王"', 'GH: "金牌司儀"', 'CK: "喜劇泰斗"', 'AK: "動作巨星"', 'ID: "人氣偶像"', 'CR: "實力派演員"']:
    ok('名冊新格 ' + nm, nm in html)
ok('E3 變體函數在位', 'function end95E3Variant(st, stats, favor)' in html)
ok('差邊瓣函數在位', 'function end95BuildGaps(ctx)' in html)
ok('總結頁差邊瓣呈現在位', '回望嗰一格' in html)
ok('E4→E3 舊相鄰分支已移除', 'base.career==="E4" && endingBackstageClose410(s)' not in html)
ok('resolve 輸出 gaps95/ladder95', 'gaps95: gaps95,' in html and 'ladder95: { total: total95' in html)
seg_start = html.find('v20a95 LADDER95')
seg_end = html.find('function resolveEnding410', seg_start) if seg_start >= 0 else -1
seg = html[seg_start:seg_end] if (seg_start >= 0 and seg_end > seg_start) else ''
ok('LADDER95 段冇真藝人名', not any(n in seg for n in ['周星馳','劉德華','張國榮','周潤發','梁朝偉','梅艷芳','張曼玉','王祖賢','鍾楚紅','林青霞']))

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
