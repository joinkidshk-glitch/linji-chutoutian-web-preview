# -*- coding: utf-8 -*-
# v20a66 YEARS66 靜態測試：epoch／副題／評核鍵／gigsByYear remap／遷移掛點／玩家面年份字眼。
# 反證：喺 v20a65 index 上行會 FAIL。
# 用法：python3 tests/test_years66_static.py [path-to-index.html]
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('START epoch = 1990-03-07', 'const START = { y:1990, m:3, d:7 }' in src)
ok('開始畫面副題 1990', '<p class="start-sub">1990 · 片場星途</p>' in src)
ok('新遊戲注腳 1990 年春', '1990 年春 · 由零開始' in src)
ok('開場 modal 日期 1990年3月7日', '<h3>1990年3月7日 · 阿偉的家</h3>' in src)
ok('YEARS66 block 存在', '/* ===== v20a66 YEARS66' in src and 'function years66MigrateSave' in src and 'function years66Walk' in src and 'function years66GigRemap' in src)
ok('normalizeGigRecord 掛 years66GigRemap', 'try{ years66GigRemap(o); }catch(_y66){}' in src)
m = re.search(r'function normalizeSaveObj\(o\)\{(.*?)\n\}', src, re.S)
ok('normalizeSaveObj 掛 years66MigrateSave', bool(m) and 'years66MigrateSave(o)' in m.group(1))
ok('fresh() 打 years66Shifted 戳', 'years66Shifted:1,' in src)
ok('CONSEQ61_REVIEWS 鍵 1990/1991', re.search(r'1990:\s*\{\s*floor:\s*45', src) is not None and re.search(r'1991:\s*\{\s*floor:\s*100', src) is not None)
ok('E7 場景 variant 用 review1991', 'if(v==="review1991")' in src)
ok('冇 review1988 殘留字串', 'review1988' not in src)
ok('生活費年份閘 1991/1992', 'if(yr>=1991){' in src and 'let up = (yr>=1992) ? 600 : 300;' in src)
ok('gigsByYear 五包 remap 齊', all(s in src for s in [
    'STORY_WIRE.gigsByYear[1990] = gigsPack;', 'STORY_WIRE.gigsByYear[1991] = gigs1989;',
    'STORY_WIRE.gigsByYear[1992] = gigs1990;', 'STORY_WIRE.gigsByYear[1993] = gigs1991;',
    'STORY_WIRE.gigsByYear[1994] = gigs1992;']))
ok('gigsByYear 初值鍵 1990–1994', 'gigsByYear: { 1990: null, 1991: null, 1992: null, 1993: null, 1994: null }' in src)
ok('移民潮芬姐閘 1991', 'yearSeasonNow().year < 1991) return false' in src)
ok('移民潮到期式 1991夏/1992', 'const due = (ys.year===1991 && ys.season==="夏") || ys.year>=1992;' in src)
ok('choice47 窗口 1992 秋', src.count('choice47SeasonReached(1992, "秋")') >= 3)
ok('程天諾預熱 fromYear 1992 齊', 'fromYear:1992' in src)
ok('結局閘文字 1992 年冬', '去到 1992 年冬、賀歲片煞科之後' in src and '"1992 年冬 · 三年收科"' in src)
ok('STORY_GATE_3Y C17 yearEq 1992', 'C17: { needDone: ["C13"], yearEq: 1992' in src)
ok('id 內嵌年份解析 +2 守衛齊', src.count('(y66>=1988 && y66<=1992) ? y66+2 : y66') >= 3)
ok('SAVE key 不變', 'starVolunteer_map_v19w' in src)
print('\nFAILURES: ' + str(len(fails)) + ((' -> ' + ' | '.join(fails)) if fails else ''))
sys.exit(1 if fails else 0)
