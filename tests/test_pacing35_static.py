# 節奏包（v20a35）靜態測試：接線／池數量／紅線。
# 用法：python3 tests/test_pacing35_static.py [path-to-index.html]
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# ---- P0-2(c) 中階通告（B3：舊 mid35 兩張工已刪；新庫 1990 春季本身覆蓋演技 19–44 帶，
# 星河板 tv_205（初級／演技 22／3 日）可報、variety_207（歌藝 18、gap 4）鎖住做目標、
# 獅子山板 film_111（初級／演技 15）可報；mergeMidGigs35 機制留返但池已空） ----
# v252：舊 tv_122 已消失、舊 film_104 改做夏季、舊 tv_103 改做《一屋人》男配角（演技 15，已可報）。
import json as _json
import os as _os
_pack35 = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'content', 'gigs_new.json'), encoding='utf-8'))
_spring35 = [g for g in _pack35['gigs'] if g['year'] == 1990 and g['season'] == '春']
ok('mid gigs const present', 'const MID_GIGS_1988_35' in html)
ok('B3 舊 mid35 工已刪', 'gig_1988_mid35_' not in html)
ok('B3 新庫春季覆蓋演技 19–44 帶（3 張）', sorted(g['id'] for g in _spring35 if 19 <= g['req'].get('acting', 0) <= 44) == ['gig_1990_ad_105', 'gig_1990_film_103', 'gig_1990_tv_205'])
ok('B3 mid gig A 等價：tv_205 初級／演技 22／3 日', any(g['id'] == 'gig_1990_tv_205' and g['req'].get('acting') == 22 and g['days'] == 3 for g in _spring35))
ok('B3 mid gig B 等價：film_111 初級／演技 15（獅子山春板、gap 0）', any(g['id'] == 'gig_1990_film_111' and g['req'].get('acting') == 15 for g in _spring35))
ok('mergeMidGigs35 defined', 'function mergeMidGigs35(' in html)
ok('mergeMidGigs35 hooked in board fetch',
   'try{ if(typeof mergeMidGigs35==="function") mergeMidGigs35(); }catch(_m35){}' in html)
ok('B3 進階目標留返（新庫有演技 45＋嘅工，目標唔係劈低咗）', any(g['req'].get('acting', 0) >= 45 for g in _pack35['gigs']))

# ---- P0-2(b) 訓練微事件 ----
ok('train events pool = 8', len(re.findall(r'id:"train35_', html)) == 8)
ok('maybeTrainEvent35 defined', 'function maybeTrainEvent35(' in html)
ok('train event hooked in applyTrainLesson', 'maybeTrainEvent35(notes, courseId)' in html)
ok('train event hooked in resolvePlannedDay', 'maybeTrainEvent35(notes, id)' in html)

# ---- P1-6 長工輕量抉擇 ----
ok('set choices pool = 6', len(re.findall(r'id:"set35_', html)) == 6)
ok('setChoiceOffer35 defined', 'function setChoiceOffer35(' in html)
ok('applySetChoice35 defined', 'function applySetChoice35(' in html)
ok('offer hooked in planned shoot day', 'setChoiceOffer35(sh)' in html)
ok('wire hooked after day modal', 'wireSetChoice35(); }catch(_wc35){}' in html)
ok('long-shoot gate >=4 days', '(Number(sh.totalDays)||0)<4' in html)

# ---- P0-6 文案池 ----
ok('psr extra templates = 23', len(re.findall(r'id:"psr35_', html)) == 23)
ok('augment defined', 'function augmentPostShootRewards35(' in html)
ok('augment hooked in framework load', 'augmentPostShootRewards35(); }catch(_e){}' in html)
ok('anti-repeat picker defined', 'function psrPickNoRepeat35(' in html)
ok('pick template uses anti-repeat', 'psrPickNoRepeat35(channel, pool)' in html)
ok('fans title from template', 'postShootCopyLine(fansT.title, "突發：被 fans 包圍")' in html)
ok('dek variant helper present', 'const _dekV35 = ' in html)

# ---- 紅線：SAVE key／softRev／?v=／pack JSON 冇郁 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 's107' in html)  # B3：舊釘 s111 已過期，現行 softRev 係 s107
ok('no new content pack fetch', html.count('postShootRewards: "STUB_POST_SHOOT_REWARDS_v1.json"') == 1)

print('\n' + ('FAILED: ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
