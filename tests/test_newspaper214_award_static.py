# -*- coding: utf-8 -*-
"""v20a214 NP214 頒獎結果卡報紙版式・靜態測試：接線完整 + 術語掃蕩 + 硬守衛冇俾人郁。
- renderAwardResultHtml 行 v11 報紙版式（維港日報、日期＝典禮日＋1、兩版、得主相、版尾），唔再係票根式卡片
- ★統一：awards63FellowsHtml 得主標記由 🏆 金底 chip 改做 ★＋「★為得主」圖例（報紙／頒獎結果路徑）
- 相片：兩張 webp 灰階細檔喺 assets/story/newspaper/；晨報 enqueueNewspaperFromAward 傳 imgKey
- 術語：inline 模板「碟市／臨記席」只可以留喺 TEXTFIX55_EXACT 嘅舊字串 key 入面（載入正規化）＋註解；
  「夜半靈異主題曲主唱」只可以留喺 TEXTFIX55_GIG_SUB 規則／內嵌 fallback 數據（載入正規化），唔可以出現喺渲染路徑
- presentAwardResult 唔再叫 toast；「收下這晚」＋awardSheet 保留
- 舊守衛：SAVE key／?v=／softRev 不變；content/*.json 冇改過；enqueueNewspaperFromWrap／press94* 唔郁
反證：pristine main f58f19c 冇 np214AwardPhoto214／冇 np214- 版式 → FAIL。
用法：python3 tests/test_newspaper214_award_static.py [path-to-index.html]
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')
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

def strip_comments(s):
    return re.sub(r'/\*.*?\*/', '', s, flags=re.S)

def remove_const(name):
    """攞走 const <name> = {...};／[...]; 成個陳述（brace-counting，唔計字串入面嘅括號）。"""
    i = html.find('const ' + name + ' =')
    if i < 0:
        return html
    depth = 0; started = False; instr = None; esc = False
    for k in range(i, len(html)):
        ch = html[k]
        if instr:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == instr: instr = None
            continue
        if ch in '"\'`': instr = ch; continue
        if ch in '{[':
            depth += 1; started = True
        elif ch in '}]':
            depth -= 1
            if started and depth == 0:
                return html[:i] + html[k+2:]
    return html

# ---- (1) renderAwardResultHtml 報紙版式 ----
fn = seg('function renderAwardResultHtml(', 'function presentAwardResult(')
fn_nc = strip_comments(fn)
ok('R01_award_result_fn', 'function renderAwardResultHtml(' in html)
ok('R02_masthead_214', '維港日報' in fn and 'np214-masthead' in fn)
ok('R03_headline_dek', 'np214-headline' in fn and 'np214-dek' in fn and 'press.headline' in fn)
ok('R04_date_plus_one', 'pack.dayIndex' in fn and 'fmtNewspaperDate(paperDay214)' in fn)
ok('R05_two_columns', 'np214-body2' in fn and 'np214-sidebar' in fn)
ok('R06_photo_wired', 'np214AwardPhoto214' in fn and 'np214-photowrap' in fn)
ok('R07_two_pages', 'data-np214-page="1"' in fn and 'data-np214-page="2"' in fn)
ok('R08_factbox', 'np214-factbox' in fn)
ok('R09_no_ticket_card', 'psr-sheet' not in fn_nc and 'psr-cards' not in fn_nc and 'psr-press' not in fn_nc)
ok('R10_no_metric_stub', '典禮後仍有人提起' not in fn_nc)
ok('R11_no_trophy_icon', 'iconHtml112("🏆")' not in fn_nc)
# psr-fellows63 嗰個 class 係 awards63FellowsHtml 入面出（helper 自己包），唔喺 render fn 字面——
# 渲染結果有嗰個 class 由 logic test b3 驗。
ok('R12_kept_bits', 'awards63FellowsHtml(felCat186)' in fn
   and 'psr-rep62' in fn and 'psr-weak62' in fn and 'psr-comfort147' in fn and '幕前聲望 ' in fn)
ok('R13_metric_second_page', 'metricHead214' in fn and 'np214-headline2' in fn and 'awardWinLine149' in fn)

# ---- (2) ★統一 ----
fel = seg('function awards63FellowsHtml(', 'function awardWinner149(')
fel_nc = strip_comments(fel)
ok('S01_fellows_star_mark', '"★ "' in fel and '★為得主' in fel)
ok('S02_fellows_no_trophy', 'iconHtml112("🏆")' not in fel_nc)
ok('S02b_won_player_row_restored', 'isWon211' in fel_nc and '陳偉翔' in fel_nc
   and 'parts.unshift' in fel_nc and 'repWorkTitle' in fel_nc)  # v20a214 工人 4：v211 C1 還原——won 版同屆提名加玩家一行＋圖例，★統一嗰陣誤刪咗
ok('S03_result_path_no_trophy', 'iconHtml112("🏆")' not in fn_nc)
ok('S04_star_legend_in_render_path', '★為得主' in html and 'np214AwardPhoto214' in html)

# ---- (3) 相片 ----
ok('P01_photo_const', 'const NP214_AWARD_PHOTOS_214' in html
   and 'np214_award_awi' in html and 'np214_award_lok' in html)
ok('P02_photo_paths', 'assets/story/newspaper/photo_awi_ceremony.webp' in html
   and 'assets/story/newspaper/photo_lok_ceremony.webp' in html)
for stem in ('photo_awi_ceremony', 'photo_lok_ceremony'):
    p = os.path.join(ROOT, 'assets', 'story', 'newspaper', stem + '.webp')
    ok('P03_file_exists_' + stem, os.path.exists(p))
    if os.path.exists(p):
        ok('P04_file_small_' + stem, os.path.getsize(p) < 100 * 1024)
        try:
            from PIL import Image
            im = Image.open(p).convert('RGB')
            # WebP 唔保 mode 'L'，驗像素灰階：抽樣最大通道差 <= 2/255
            px = im.resize((52, 64)).getdata()
            worst = max(max(abs(r - g), abs(g - b)) for (r, g, b) in px)
            ok('P05_grayscale_520w_' + stem, im.width == 520 and worst <= 2)
        except Exception as e:
            ok('P05_grayscale_520w_' + stem + ' (PIL unavailable: %s)' % e, False)
ok('P06_news82_merge', 'NP214_AWARD_PHOTOS_214[k]' in html and 'NEWS82_IMGS' in html)
ok('P07_morning_imgkey', html.count('imgKey: imgKey214') == 2)
ok('P08_award_enqueue_photo', 'np214AwardPhoto214(pack, opts)' in seg('function enqueueNewspaperFromAward(', 'function newspaperStoryLists()'))
ok('P09_enqueue_stores_imgkey', 'imgKey: String(raw.imgKey' in html)

# ---- (4) 術語掃蕩 ----
exact = seg('const TEXTFIX55_EXACT = {', 'const TEXTFIX55_GIG_EXACT')
ok('T01_exact_new_strings',
   '邊個上台領獎' in exact and '樂壇點樣叫人名' in exact and '金碟夜新人輩出' in exact
   and '陳偉翔嘅名第一次出現喺典禮側記' in exact and '金碟夜散場：掌聲未完' in exact
   and '台慶頒獎夜散場：觀禮席都有鏡頭掃過' in exact)
gigsub = seg('const TEXTFIX55_GIG_SUB = [', 'const TEXTFIX57_GIG_REQ')
ok('T02_gigsub_rule', '["夜半靈異主題曲主唱", "夜半靈異"]' in gigsub)
venue = seg('const VENUE99_INVITE_DEK = {', 'const VENUE99_NEWS_LINE')
venue += seg('const VENUE99_NEWS_LINE = {', 'const venue99ApplyOverlay')
ok('T03_venue99_clean', '邊個上台領獎' in venue and '陳偉翔嘅名第一次出現' in venue
   and '掌聲未完' in venue and '碟市' not in strip_comments(venue) and '臨記席' not in strip_comments(venue))
awd188 = strip_comments(seg('const AWARDS188_CATEGORIES = {', 'function awards188ApplyNpOverlay('))
ok('T04_awards188_clean', '樂壇點樣叫人名' in awd188 and '樂壇仲有下一更' in awd188
   and '碟市' not in awd188 and '臨記席' not in awd188)
pick = strip_comments(seg('function awardsPickPressNews(', 'function awardsMetricEchoLabel('))
ok('T05_pick_clean', '觀禮席都有鏡頭掃過' in pick and '臨記席' not in pick)
metric = strip_comments(seg('function awardsMetricEchoLabel(', 'function awards63InviteBitHtml('))
ok('T06_metric_clean', '銷量榜' in metric and '碟市' not in metric)
# 全檔掃蕩：TEXTFIX55_EXACT 塊＋全部 /* */ 註解攞走之後，唔可以再有碟市／臨記席
rest = remove_const('TEXTFIX55_EXACT')
rest = strip_comments(rest)
ok('T07_global_no_disc_market', '碟市' not in rest)
ok('T08_global_no_extra_seat', '臨記席' not in rest)
# 「夜半靈異主題曲主唱」只可以留喺 GIG_SUB 規則＋內嵌 fallback 數據（載入正規化），渲染路徑唔可以有
render_paths = fn + fel + pick + metric + seg('function enqueueNewspaperFromAward(', 'function newspaperStoryLists()')
ok('T09_no_bad_worktitle_in_render', '夜半靈異主題曲主唱' not in render_paths)
ok('T10_no_bad_worktitle_in_awards188', '夜半靈異主題曲主唱' not in awd188)

# ---- (5) presentAwardResult：唔再 toast ----
pres = seg('function presentAwardResult(', 'function presentAwardInvite(')
ok('A01_no_toast', 'toast(' not in strip_comments(pres))
ok('A02_keep_button', '收下這晚' in pres and 'awardSheet:true' in pres)

# ---- (6) 紅線 ----
ok('X01_save_key', html.count('starVolunteer_map_v19w') == 10)
ok('X02_version', html.count('"v20a10"') == 7)
ok('X03_softrev', 's107' in html)
ok('X04_wrap_untouched_fn', 'function enqueueNewspaperFromWrap(' in html and 'function press94FillLines(' not in html)
try:
    st = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True, timeout=30).stdout
    touched = [l for l in st.splitlines() if l[3:].startswith('content/')]
    ok('X05_content_json_untouched', touched == [])
except Exception as e:
    ok('X05_content_json_untouched (git unavailable: %s)' % e, False)

print('RESULT ' + ('FAIL ' + str(len(fails)) if fails else 'PASS'))
sys.exit(1 if fails else 0)
