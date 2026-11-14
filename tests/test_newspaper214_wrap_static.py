# -*- coding: utf-8 -*-
"""v20a214 NP214・殺青報紙＋WF3／story 報紙＋第二版厚度・靜態測試（工人 3）
- base 唔出報紙：press94FillLines 已刪、入閘標記已清、閘口回 null
- 殺青報紙相片：np214WrapPoster214 對應 poster59Path，key 唔撞 WF3／頒獎
- WF3／story：世界事件三段＋相齊、story 單段；排序／摺疊唔郁
- 第二版廣告：兩格真內容廣告（樣本 v11 原文），用工人 1 已備 .np214-adbox CSS，唔加新 CSS
- 邊欄留返；殺青獎勵 sheet／推出日機制唔郁（推出日另開票，唔入 v214）
反證：pristine main（f58f19c）index 冇 np214* → 大量 FAIL。
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
fails = []
def ok(name, cond, extra=''):
    print(('PASS ' if cond else 'FAIL ') + name + ((' ' + extra) if (extra and not cond) else ''))
    if not cond: fails.append(name)

def seg(start, end):
    i = html.index(start)
    j = html.index(end, i) if end else len(html)
    return html[i:j]

# ---- (1) base 唔出報紙：填位已刪、閘口回 null ----
ok('S01_fill_fn_gone', 'function press94FillLines(' not in html)
ok('S02_no_fill_mark', 'press94: "fill"' not in html)
wrap = seg('function enqueueNewspaperFromWrap(', 'function enqueueNewspaperFromAward(')
ok('S03_gate_returns_null', 'press94IsBaseRole(gig94, labelHint94)' in wrap
   and 'return null' in wrap and 'press94FillLines' not in wrap)
ok('S04_classifier_badge_kept', 'function press94RoleClass(' in html
   and 'function press94TierBadge(' in html and 'function press94ClaimFirstNamed(' in html)
ok('S05_reward_sheet_kept', 'function presentPostShootReward(' in html)

# ---- (2) 殺青報紙相片 ----
ok('S06_poster_helper', 'function np214WrapPoster214(' in html
   and 'np214_poster_' in html and 'poster59Path(gigId)' in html)
ok('S07_wrap_imgkey', 'imgKey: poster214 ? poster214.key : ""' in wrap)
ok('S08_poster_files', all(
    os.path.exists(os.path.join(ROOT, 'assets/posters', 'poster-' + k[4:] + '.webp'))
    for k in re.findall(r'"(gig_1988_[a-z0-9_]+)": 1', seg('const POSTER85_IDS = {', '};\nfunction poster85File'))))
m85 = re.search(r'const POSTER85_IDS = \{(.*?)\};', html, re.S)
ok('S09_poster85_count', m85 is not None and len(re.findall(r'"gig_[^"]+"', m85.group(1))) == 59,
   'n=%s' % (len(re.findall(r'"gig_[^"]+"', m85.group(1))) if m85 else 'missing'))
ok('S10_no_wf3_key_collision', 'np214_poster_' in html
   and 'np214_poster_' not in seg('const NP214_AWARD_PHOTOS_214 = {', '};'))

# ---- (3) WF3／story：新版式出得啱，排序／摺疊唔郁 ----
ev = re.search(r'const NEWS82_EVENTS = \[(.*?)\n\];', html, re.S)
ok('S11_world_events', ev is not None and len(re.findall(r'paras:\[', ev.group(1))) == 7)
ni = json.load(open(os.path.join(ROOT, 'content/news_images_v82.json'), encoding='utf-8'))
ok('S12_world_imgkeys', ev is not None and set(re.findall(r'imgKey:"([^"]+)"', ev.group(1))) <= set(ni['images'].keys()))
ok('S13_world_render', 'e.worldId' in html and '(e.paras||[]).map' in html
   and 'dekStrip' in html)
ok('S14_story_render', 'function enqueueNewspaperFromStory(' in html
   and 'source: "story"' in html
   and 'imgKey' not in seg('function enqueueNewspaperFromStory(', 'function newspaperDueItems('))
ok('S15_edition_sort_kept', 'news82IsHead(a.worldId) ? 2 : 1' in html
   and '同日還有 "+overflow.length+" 則' in html)
ok('S16_no_release_mechanism', 'enqueueNewspaperItem' in html
   and 'source: "release"' not in html and 'releaseDay' not in html)

# ---- (4) 第二版廣告＋邊欄 ----
ok('S17_ads_helper', 'function np214Page2Ads214(' in html
   and '星光卡拉 OK' in html and '歡唱 $38／小時' in html
   and '旺角彌敦道 123 號 3 樓' in html and '電話 388 4567' in html
   and '金龍茶餐廳' in html and '菠蘿油' in html and '絲襪奶茶' in html
   and '通宵營業' in html)
ok('S18_ads_two_boxes', html.count('<div class="np214-adbox">') == 2)
ok('S19_ads_wired_once', html.count('np214Page2Ads214()') == 2)  # 定義 1 次＋渲染器插入呼叫 1 次
ok('S20_adbox_css_reused', '.paper-sheet .np214-adbox{' in html
   and '.paper-sheet .np214-adbox .np214-ad-name{' in html)
render = seg('function renderMorningPaperHtml(', 'function pushNewspaperRumor(')
ok('S21_ads_not_in_shorts', 'np214Page2Ads214' in render
   and 'shorts.push' not in render)
ok('S22_sidebar_kept', '影視娛樂' in render and 'np214-filler-v' in render
   and 'paperSideItemForDay' not in render)
ok('S23_filler_fallback_kept', "length<=2 ? `<p class=\"np214-filler\"" in render)

# ---- (5) 紅線：工人 1／2 範圍唔郁 ----
ok('S24_core_kept', 'function renderMorningPaperHtml(' in html
   and 'function fmtNewspaperDate(' in html and 'function newspaperFullName214(' in html)
ok('S25_award_kept', 'function renderAwardResultHtml(' in html
   and 'function np214AwardPhoto214(' in html)
ok('S26_no_new_css_class', html.count('.paper-sheet .np214-adbox') == 4)  # 工人 1 已備 4 條 rule，工人 3 冇加
print('RESULT ' + ('FAIL ' + str(len(fails)) if fails else 'PASS'))
sys.exit(1 if fails else 0)
