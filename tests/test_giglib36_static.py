# 通告庫修補包（v20a36）靜態測試：接線／池數量／紅線／內容標準。
# 用法：python3 tests/test_giglib36_static.py [path-to-index.html]
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# ---- F1 死卡正規化 ----
ok('F1 normalize remaps sing->vocal', 'rq.vocal = Math.max(Number(rq.vocal)||0, Number(rq.sing)||0); delete rq.sing;' in html)
ok('F1 normalize remaps dance->stage', 'rq.stage = Math.max(Number(rq.stage)||0, Number(rq.dance)||0); delete rq.dance;' in html)
ok('F1 inside normalizeGigRecord', html.index('rq.vocal') > html.index('function normalizeGigRecord('))

# ---- 注入接線 ----
ok('mergeYearGigs36 defined', 'function mergeYearGigs36(' in html)
ok('mergeYearGigs36 hooked in board fetch',
   'try{ if(typeof mergeYearGigs36==="function") mergeYearGigs36(); }catch(_y36){}' in html)
ok('gig36 factory defined', 'function gig36(spec){' in html)
ok('cross-year leak guard present', 'GIGS36_ALL_IDS[g.id] && !wantIds[g.id]' in html)

# ---- 池數量 ----
ok('1989 F5 pool = 6', html.count('id:"g36_89_spr_') >= 6)
ok('1989 bridge pool = 10', len(re.findall(r'id:"g36_89_brg_', html)) == 10)
ok('1989 F2 pool = 7', len(re.findall(r'id:"g36_89_(spr_harbour_epic|sum_|aut_|win_)', html)) >= 7)
ok('1990 bridge pool = 8', len(re.findall(r'id:"g36_90_brg_', html)) == 8)
ok('exodus gigs total = 5', len(re.findall(r'id:"gig_exodus_', html)) == 5)
ok('exodus additions present', all(x in html for x in ['gig_exodus_rec_producer','gig_exodus_tv_kowloon','gig_exodus_ad_manager']))
ok('finale gig present', 'g36_90_win_lion_newyear' in html)
ok('blockbuster 100+ gig present', 'req:{ acting:105, stamina:90 }' in html)
ok('1990 80-95 gig present', 'req:{ acting:85, stage:35 }' in html and 'req:{ acting:88, stamina:100 }' in html)

# ---- F8 閘 ----
ok('credit gates = 3 total (89x2 + 90x1)',
   len(re.findall(r'industryCreditMin:(30|40|50)', html)) == 3)
ok('tag gates present (comedy x2 + action x1)',
   html.count('requiresCastingTagAny:["tag_comedy", "喜劇細胞"]') == 2 and
   html.count('requiresCastingTagAny:["tag_action", "動作演員"]') == 1)

# ---- 內容標準：通用工名禁用清單（新增通告 title 唔准命中） ----
block_start = html.index('/* ===== v20a36')
block_end = html.index('/** v19l', block_start)
block = html[block_start:block_end]
titles = re.findall(r'title:"([^"]+)"', block)
ok('new gig titles found (>=55)', len(titles) >= 55)
BANNED = ['電影配角','電視配角','廣告拍攝','電影拍攝','配角招募','演員招募','臨時演員招募','群眾演員']
ok('no banned generic titles', not any(b in t for t in titles for b in BANNED))
ok('every title has work-title brackets', all(('《' in t or '「' in t) for t in titles))
# 新增通告 req 只准真屬性 key
reqs = re.findall(r'req:\{([^}]*)\}', block)
keys = set()
for r in reqs:
    keys.update(k.strip() for k in re.findall(r'(\w+):', r))
ok('new gig req keys all real stats', keys <= {'acting','stage','vocal','looks','stamina','iq','charm'})
ok('no sing/dance in new gig reqs', 'sing' not in keys and 'dance' not in keys)

# ---- 紅線：SAVE key／softRev／?v=／1988 階梯冇郁 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 'softRev=s107' in html or '"s107"' in html)
ok('lingyi threshold untouched (acting 45)', '"acting": 45' in html or 'acting:45' in html)
ok('mid35 gigs untouched', 'gig_1988_mid35_longmen_night' in html and 'gig_1988_mid35_lion_chase' in html)

print('\nFAILURES: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
