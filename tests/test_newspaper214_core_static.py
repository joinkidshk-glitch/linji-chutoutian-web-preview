# -*- coding: utf-8 -*-
"""v20a214 NP214 晨報核心渲染器・靜態測試：接線完整 + 硬守衛冇俾人郁。
- NP214 CSS 在位（報頭 A、兩欄、黑白半調相、資料格／廣告格、填充字、版尾、切換掣）
- fmtNewspaperDate／newspaperFullName214／np214ShowPage／np214DateLabel 在位
- buildNewspaperEdition 用 fmtNewspaperDate 出中文遊戲日期
- renderMorningPaperHtml 行 v11 版式（維港日報、兩版切換、全名、冇「今早」／冇天氣格）
- 舊守衛：rotate(-2.2deg) 仍係 2 次（polish48）、SAVE key／?v=／softRev 不變、style 括號平衡
反證：pristine main f58f19c 冇 NP214 → FAIL。
用法：python3 tests/test_newspaper214_core_static.py [path-to-index.html]
"""
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
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

# ---- (1) NP214 CSS ----
ok('C01_np214_css_block', '/* === v20a214 NP214' in html and '/* === v20a214 NP214 完 === */' in html)
ok('C02_masthead_a', '.np214-name' in html and '#b32020' in html and 'VICTORIA HARBOUR DAILY' in html)
ok('C03_two_columns', '.np214-body2' in html and 'column-count:2' in html)
ok('C04_photo_halftone', '.np214-photo' in html and 'grayscale(1)' in html and 'contrast(1.28)' in html)
ok('C05_fact_ad_boxes', '.np214-factbox' in html and '.np214-adbox' in html)
ok('C06_filler', '.np214-filler' in html and 'blur(1.1px)' in html)
ok('C07_sidebar', '.np214-sidebar' in html and '影視娛樂' in html)
ok('C08_page_switch_css', '.np214-page' in html and '.np214-switch' in html)
ok('C09_pagefoot', '.np214-pagefoot' in html)
ok('C10_no_new_tilt', html.count('rotate(-2.2deg)') == 2)  # polish48 守衛：NP214 唔准加多個

# ---- (2) 幫手函數 ----
ok('F01_fmt_date', 'function fmtNewspaperDate(' in html)
ok('F02_full_name', 'function newspaperFullName214(' in html)
ok('F03_show_page', 'function np214ShowPage(' in html)
ok('F03b_show_page_global', 'window.np214ShowPage = np214ShowPage' in html)  # v20a214 工人 4：inline onclick 要 global，唔掛 window 撳「第二版 →」就爆
ok('F04_date_label', 'function np214DateLabel(' in html)
ok('F05_date_real_clock', 'START.y, START.m-1, START.d' in seg('function fmtNewspaperDate(', 'function newspaperFullName214('))
ok('F06_date_chinese_fmt', '星期' in seg('function fmtNewspaperDate(', 'function newspaperFullName214('))

# ---- (3) buildNewspaperEdition 日期 ----
ed = seg('function buildNewspaperEdition(', 'function pullDueNewspaperEdition(')
ok('E01_edition_uses_fmt214', 'fmtNewspaperDate(day)' in ed)
ok('E02_edition_no_fmtshort_date', 'dateLabel: (typeof fmtDateShort' not in ed)

# ---- (4) renderMorningPaperHtml v11 版式 ----
fn = seg('function renderMorningPaperHtml(', 'function pushNewspaperRumor(')
ok('R01_masthead', '維港日報' in fn)
ok('R02_two_pages', 'data-np214-page="1"' in fn and 'data-np214-page="2"' in fn)
ok('R03_switch_buttons', 'np214ShowPage(this,2)' in fn and 'np214ShowPage(this,1)' in fn)
ok('R04_full_name_wired', 'newspaperFullName214' in fn)
ok('R05_date_via_helper', 'np214DateLabel(e)' in fn)
ok('R06_no_morning_fallback', '今早' not in fn)
ok('R07_no_weather', '天氣' not in fn and '明日天氣' not in fn)
ok('R08_no_old_masthead', 'paper-mast' not in fn and 'paper-date' not in fn)
ok('R09_kicker_dedupe_kept', 'kickNorm' in fn and 'headRaw.startsWith(kickTrim)' in fn and '!kickDup' in fn)
ok('R10_photo_uses_news82', 'NEWS82_IMGS' in fn and 'np214-photo' in fn)
ok('R11_shorts_second_page', 'np214-shorts' in fn and '同版短訊' in fn)
ok('R12_fame_line_kept', '聲望未有變動' in fn and 'paper-fame' in fn)

# ---- (5) 紅線 ----
ok('X01_save_key', html.count('starVolunteer_map_v19w') == 10)
ok('X02_version', html.count('"v20a10"') == 7)
ok('X03_softrev', 's107' in html)
style = html.split('<style', 1)[1].split('</style>', 1)[0]
ok('X04_style_braces_balanced', style.count('{') == style.count('}'))
ok('X05_papersheet_opt_kept', 'paperSheet: true' in html)
ok('X06_commit_fame_untouched', 'fameApplied===true' in html and 'S.fame = Math.max(0' in html)

print('RESULT ' + ('FAIL ' + str(len(fails)) if fails else 'PASS'))
sys.exit(1 if fails else 0)
