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

# ---- P0-2(c) 中階通告 ----
ok('mid gigs const present', 'const MID_GIGS_1988_35' in html)
ok('mid gig A id present', 'gig_1988_mid35_longmen_night' in html)
ok('mid gig B id present', 'gig_1988_mid35_lion_chase' in html)
ok('mid gig A req acting 32', 'req:{ acting:32, stamina:50 }' in html)
ok('mid gig B req acting 38', 'req:{ acting:38, stamina:80 }' in html)
ok('mid gig A shoot band 3d', 'shootBand:[3, 3]' in html)
ok('mid gig B shoot band 2d', 'shootBand:[2, 2]' in html)
ok('mergeMidGigs35 defined', 'function mergeMidGigs35(' in html)
ok('mergeMidGigs35 hooked in board fetch',
   'try{ if(typeof mergeMidGigs35==="function") mergeMidGigs35(); }catch(_m35){}' in html)
ok('lingyi threshold untouched (acting 45)', '"acting": 45' in html or 'acting:45' in html)

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
ok('softRev unchanged', 's108' in html)
ok('no new content pack fetch', html.count('postShootRewards: "STUB_POST_SHOOT_REWARDS_v1.json"') == 1)

print('\n' + ('FAILED: ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
