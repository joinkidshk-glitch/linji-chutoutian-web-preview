#!/usr/bin/env python3
"""v20a284 R5 B/C/D/F: gigs_new.json edits (B tv_201, C film_112, D tv_106, F new film_114).
Round-trip safe: json.dumps(ensure_ascii=False, indent=2) is byte-identical to the
original file when unmutated (verified before running).
Usage: python3 qa284/gig_edit284.py  (run from repo root)
"""
import json, sys

PATH = 'content/gigs_new.json'
raw = open(PATH, encoding='utf-8').read()
d = json.loads(raw)
gigs = d['gigs']
by_id = {g['id']: g for g in gigs}
assert len(gigs) == 288, len(gigs)
assert len(by_id) == 288

# ---- B: gig_1992_tv_201 -> 1991 spring, tier mid, pay to mid peer band ----
g = by_id['gig_1992_tv_201']
assert g['year'] == 1992 and g['season'] == '春' and g['tier'] == '高級' and g['pay'] == [510, 630], g
assert g['trigger'] == {'kind': 'credit', 'creditId': 'credit_fen_rescue', 'creditOwner': '芬姐'}
g['year'] = 1991
g['tier'] = '中級'
g['pay'] = [270, 330]  # mid TV 3-day peer-exact (90-110/day; SPEC 7.1 mid band 90-160/day)

# ---- C: gig_1991_film_112 -> ordinary board gig (drop dead trigger) ----
g = by_id['gig_1991_film_112']
assert g['trigger'] == {'kind': 'credit', 'creditId': 'credit_wf3_lu_team', 'creditOwner': '陸柏言'}, g
assert 'discoverNote' in g and g['discoverNote'].startswith('陸柏言團隊引薦')
assert '憑陸柏言團隊引薦入組' in g['blurb']
del g['trigger']
del g['discoverNote']
g['blurb'] = '小成本靈異片，夜半渡假屋無人應聲。鍾楚凝飾演第一個撞鬼的住客，麥震東飾演膽大妄為的男住客；你擔任男主角，在渡假屋走廊與山路之間查探真相。'
# storyKeys kept (v274 precedent: de-triggered rec_105 kept ['gu_mingfai']); invisible metadata, no runtime read.

# ---- D: gig_1991_tv_106 -> 1992 spring (tier/pay unchanged) ----
g = by_id['gig_1991_tv_106']
assert g['year'] == 1991 and g['season'] == '夏' and g['tier'] == '初級', g
assert g['trigger'] == {'kind': 'credit', 'creditId': 'credit_enc79_yip_manager', 'creditOwner': '葉經理人'}
g['year'] = 1992
g['season'] = '春'

# ---- F: new 1992 Lu referral gig, gig_1992_film_114 (BR89 15th pair) ----
assert 'gig_1992_film_114' not in by_id
assert not any(x.get('workTitle') == '海角歸人' for x in gigs)
assert not any(x.get('title') == '《海角歸人》男配角' for x in gigs)
new_gig = {
    'id': 'gig_1992_film_114',
    'title': '《海角歸人》男配角',
    'type': '電影',
    'tier': '中級',
    'category': '作品',
    'genre': '文藝',
    'workTitle': '海角歸人',
    'roleLabel': '男配角',
    'loc': 'film_harbour',
    'director': '導演',
    'year': 1992,
    'season': '春',
    'days': 12,
    'roleScale': 'film_support_main',
    'req': {'acting': 75},
    'hard': 0.5,
    'pay': [1210, 1430],
    'fame': [28, 45],
    'blurb': '漁村碼頭歸人故事，陸柏言飾演多年後返鄉的老船工，鍾楚凝飾演守在碼頭的妻子；你飾演船工的年輕拍檔，憑陸柏言引薦入組，跟隨船隊走遍江河。',
    'synopsis': '故事講述老船工阿海（陸柏言飾）年輕時離開漁村去外海討生活，多年後返鄉，發現碼頭已經變了樣：舊街坊搬走了大半，剩低的都老了。妻子阿芳（鍾楚凝飾）守住碼頭邊的老屋，每日望住海平線等船返嚟。阿海的妹妹阿燕（江詩盈飾）在碼頭開了一間小食店，一邊招呼街坊，一邊勸阿海留低唔好再出海。你飾演阿海的年輕拍檔，戲分集中在碼頭裝卸與夜釣的場面，要在陸柏言身邊襯托他的沉默，動作沉穩，說對白時注視海面。',
    'roleHint': '中級文藝片男配角，戲分貫穿碼頭外景，講求內斂沉穩，適合已有文藝片經驗的演員。',
    'posterBrief': '漁村碼頭清晨，陸柏言站在船頭望向海平線，鍾楚凝站在老屋門口望向碼頭，江詩盈站在小食店門口手持漁網，背景是漁船、遠山與歸鳥，氣氛蒼涼而深情。',
    'cast': {'leadM': 'luk_baakyin', 'leadF': 'chung_choning', 'supportM': None, 'supportF': 'kong_siying'},
    'trigger': {'kind': 'credit', 'creditId': 'credit_enc83_luk_patron', 'creditOwner': '陸柏言'},
    'discoverNote': '陸柏言引薦：文藝片《海角歸人》男配角，憑人情入組。',
    'storyKeys': ['luk_baakyin'],
}
idx113 = next(i for i, x in enumerate(gigs) if x['id'] == 'gig_1992_film_113')
gigs.insert(idx113 + 1, new_gig)
assert len(gigs) == 289
assert len({x['id'] for x in gigs}) == 289

out = json.dumps(d, ensure_ascii=False, indent=2)
assert out != raw
open(PATH, 'w', encoding='utf-8').write(out)
print('OK: 288 -> 289 gigs; B/C/D/F applied')
