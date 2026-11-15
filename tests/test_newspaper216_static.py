# -*- coding: utf-8 -*-
"""v20a216 報紙修復・靜態測試：CSS 接線＋R0/R2/R4/R5 硬守衛。
用法：python3 tests/test_newspaper216_static.py [path-to-index.html]
反證：對 pristine main（v215，/tmp/pristine216_index.html）乾淨 FAIL——
  無 headline3／無 nobreak／第二版硬寫「同版短訊」／-7px 仲喺度／花邊全口語。
"""
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond, extra=''):
    print(('PASS ' if cond else 'FAIL ') + name + ((' ' + extra) if (extra and not cond) else ''))
    if not cond:
        fails.append(name)

def seg(start, end=None):
    i = html.find(start)
    if i < 0:
        return ''
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

# ---- (1) R1：頭條 CSS ----
ok('C01_headline3_26px', '.np214-headline3' in html and 'font-size:26px' in seg('.paper-sheet .np214-headline3{', '}'))
ok('C01b_headline4_22px', '.np214-headline4' in html and 'font-size:22px' in seg('.paper-sheet .np214-headline4{', '}'))
ok('C02_headline_balance', 'text-wrap:balance' in html and 'overflow-wrap:break-word' in html)
ok('C03_nobreak_span', '.np214-nobreak' in html and 'white-space:nowrap' in html)
ok('C04_headline_red', '.np214-headline .red' in html and '#b32020' in html)
fn = seg('function renderMorningPaperHtml(', 'function pushNewspaperRumor(')
ok('C05_headline_tiers_wired', 'np214-headline3' in fn and 'np214-headline4' in fn and 'headClass216' in fn and 'headRich216' in fn)
ok('C06_headline_no_fixed_37_only', 'class="${headClass216(e.headline)}"' in fn)

# ---- (2) R0：殘留填位過濾接線 ----
for fname in ['ensureNewspaperQueue', 'enqueueNewspaperItem', 'buildNewspaperEdition']:
    body = seg('function %s(' % fname, 'function ', )
    ok('R0_%s_filters_fill' % fname, 'press94==="fill"' in seg('function %s(' % fname, '\n}\n'),
       fname)
ok('R0_no_literal_fill_mark', 'press94: "fill"' not in html)  # v214 S02 守衛，v216 照守
ok('R0_pulldue_null_guard', 'if(!edition) return null' in seg('function pullDueNewspaperEdition(', 'function newspaperHoldForToday('))

# ---- (3) R2：第二版真標題 ----
# R2 斷言字串本身喺 newspaperCheck 出現（反向檢查），所以只掃渲染器段，唔掃全檔。
ok('R2_no_hardcoded_section_headline', '<h3 class="np214-headline2">同版短訊</h3>' not in fn)
ok('R2_p2_headline_from_first_short', 'p2HeadRaw216' in fn and 'firstShort216' in fn)
ok('R2_column_name_kept_kicker_foot', '<p class="np214-kicker">同版短訊</p>' in fn)

# ---- (4) R3：填版接線 ----
ok('R3_factbox_emitted', 'factbox216' in fn and 'np214-factbox' in fn)
ok('R3_factbox_real_rows', '<b>作品</b>' in fn and '<b>媒介</b>' in fn)
ok('R3_factbox_wide_inline', '.np214-factbox.np214-factbox-wide .np214-row .np214-v' in html
   and 'display:inline' in seg('.paper-sheet .np214-factbox.np214-factbox-wide .np214-row .np214-v{', '}'))
ok('R3_p1_filler', 'fillerP1216' in fn and 'np214-filler' in fn and 'np214-filler-left' not in fn)
ok('R3_p2_filler_scales', 'p2Fillers216' in fn and 'p2FillerN216' in fn and '.slice(0, p2FillerN216)' in fn
   and '金碟夜 唱片銷量' in fn and '電視城 片場 臨記' in fn and '唱片舖 卡式帶' in fn)
ok('R3_sidebar_preview', 'sidePrev216' in fn and '同版：' in fn)
ok('R3_edition_passthrough', 'workTitle: head.workTitle' in html and 'roleLabel: role216' in html)

# ---- (5) R4：掣唔疊紙 ----
ok('R4_no_negative_btn_margin', 'margin-top:-7px' not in html)
ok('R4_76px_after_34px', html.index('padding-bottom:76px') > html.index('padding-bottom:34px'))
ok('R4_paper_modal_88dvh', re.search(r'#mask\.paper-on:not\(\.tut-on\) \.modal\{\n  max-height:min\(88dvh,88svh,760px\)', html) is not None)
ok('R4_switchrow_sticky', '.paper-sheet .np214-switchrow{ position:sticky; bottom:0;' in html)
ok('R4_present_clears_story_play', 'story-play-on' in seg('function presentDueMorningPaper(', 'function renderClippingsPane(')
   and 'classList.remove("story-play-on")' in seg('function presentDueMorningPaper(', 'function renderClippingsPane('))

# ---- (6) R5：書面語防倒退（同 newspaperCheck 口徑） ----
def banned(txt):
    noq = re.sub(r'「[^」]*」', '', txt or '')
    if re.search(r'[喺嘅咗唔]', noq):
        return True
    if '嗰' in noq:
        return True
    if re.search(r'係[^。]{0,12}定', noq):  # 「係…定…」口語選擇句（E5 原文）
        return True
    if '估緊' in noq:
        return True
    t2 = re.sub(r'電話|說話|話題|通話|熱話|一句話', '', txt or '')
    if '話' in t2:
        return True
    if re.search(r'cut|mark', txt or '', re.I):
        return True
    return False

m = re.search(r'const PAPER_SIDE_ITEMS = \[(.*?)\n\];', html, re.S)
items = re.findall(r'\{[^}]*?h:"((?:[^"\\]|\\.)*)", d:"((?:[^"\\]|\\.)*)"[^}]*?\}', m.group(1)) if m else []
ok('R5_side_count_39', len(items) == 39, 'n=%d' % len(items))
bad = [(i + 1) for i, (h, d) in enumerate(items) if banned(h + d)]
ok('R5_side_all_clean', not bad, 'bad=%s' % bad)
ev = re.search(r'const NEWS82_EVENTS = \[(.*?)\n\];', html, re.S)
badw = []
if ev:
    for em in re.finditer(r'\{ id:"(\w+)", day:\d+, level:"(\w+)".*?paras:\[(.*?)\]', ev.group(1), re.S):
        if em.group(2) != 'side':
            continue
        for p in re.findall(r'"((?:[^"\\]|\\.)*)"', em.group(3)):
            if banned(p):
                badw.append(em.group(1))
ok('R5_world_side_clean', not badw, 'bad=%s' % badw)
ok('R5_check_lint_wired', 'banned216' in html and 'r5_side_colloquial216' in html)

# ---- (7) 紅線 ----
ok('X01_save_key', html.count('starVolunteer_map_v19w') == 10)
ok('X02_version', html.count('"v20a10"') == 7)
ok('X03_softrev', 's107' in html)
ok('X04_rotate_count_2', html.count('rotate(-2.2deg)') == 2)
style = html.split('<style', 1)[1].split('</style>', 1)[0]
ok('X05_style_braces_balanced', style.count('{') == style.count('}'))

print('RESULT ' + ('FAIL ' + str(len(fails)) if fails else 'PASS'))
sys.exit(1 if fails else 0)
