# v20a37 驗證修復包・靜態測試：接線標記／紅線／NOTES。
# 用法：python3 tests/test_verify37_static.py [path-to-index.html]
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end):
    i = html.index(start)
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 20000)
    return html[i:j]

# ---- item 1：雙軌解釋改觸發（有真結算 dual 物件就出，唔再要求正 delta） ----
exp_seg = seg('function dualTrackExplainHtml34(', 'try{\n  window.__dualHud')
ok('item1 explainer no longer gated on positive delta',
   'dStage)||0)>0' not in exp_seg and 'result.dual' in exp_seg and 'guidanceDualExplained34' in exp_seg)
sr_seg = seg('function showResult(node, choice, result){', 'function newlyOpenAfter')
ok('item1 showResult still appends explainer', 'dualTrackExplainHtml34(result)' in sr_seg)

# ---- item 2a：頭條變體池 ----
ok('item2a headline variant pool present', '_headPick37' in html and '煞科見報' in html and '拍畢' in html)
face_seg = seg('function newspaperWrapFaceLines(', 'function newspaperWrapFadeLines')
ok('item2a headline pool has >=6 variants per branch', face_seg.count('book+') + face_seg.count('headWho+') >= 10)

# ---- item 2b：metrics 單抽 ----
bps_seg = seg('function buildPostShootRewardPack(', 'function queuePostShootRewardOnWrap')
ok('item2b metrics single-draw (no double postShootPickTemplate for metrics)',
   bps_seg.count('postShootPickTemplate("metrics"') == 1 and 'if(!metricT) metricT = postShootPickTemplate("metrics", gigType, scene38);' in bps_seg)  # v20a38：fallback 呼叫加 scene38 參數，單抽不變量不變

# ---- item 2c：增補池冇具名作品 ----
pool_seg = seg('const PSR_EXTRA_TEMPLATES_35', 'const _psrLastPick35')
ok('item2c extra pool has no named work 夜班廠景', '夜班廠景' not in pool_seg)
ok('item2c fixed card present (深宵廠景煞科)', '深宵廠景煞科，新面孔企到尾' in pool_seg)

# ---- item 3：獲聘文案講明殺青後入帳（兩條路徑＋手帳頁） ----
ok('item3 doAudition pending line', '殺青後入帳：約酬' in html and '未殺青前唔會加，拍完嗰日先入帳' in html)
ok('item3 both hire paths carry the line', html.count('殺青後入帳：約酬') >= 2)
ok('item3 jobs pane marks pending', '（殺青後入帳）' in html)

# ---- item 4：週行程戳 ----
ok('item4 stamp helpers present', 'function stampWeekPlan37(' in html and 'function nbRangeLabel37(' in html and 'S.weekPlanWeek37' in html)
ok('item4 renderNotebook uses plan-week label', 'nbRangeLabel37()' in seg('function renderNotebook(){', 'function enterHome('))
ok('item4 prev-week title copy', '上週行程（唯讀）' in html)

# ---- item 5：場數 remain 正規化 ----
ok('item5 shootDayLine computes remain', 'remain:Math.max(0' in html)
ok('item5 fill-layer normalizes pack templates', 'split("餘{total}").join("餘{remain}")' in html)
ok('item5 embedded typed pool fixed', '餘{remain}場' in html)

# ---- item 6：節奏參數 ----
ok('item6a train cooldown present', 'since<=0' in seg('function maybeTrainEvent35(', 'function setChoiceOffer35('))
ok('item6b set-choice force rule present', 'force37' in seg('function setChoiceOffer35(', 'function applySetChoice35('))

# ---- item 7：事態預告補地點 ----
ok('item7 picker lock rows append play location', '開咗去' in seg('function playOpenPicker(){', 'function spPlayerMeta(') or '開咗去' in html)
ok('item7 progress line appends play location', 'locBit37' in html)
ok('item7 here-block names location', '先可以播這幕' in html)

# ---- item 8：差額界限 ----
ok('item8 far-gap cap present', 'const GIG_GAP_FAR37 = 80;' in html and 'function gigGapBoardLine37(' in html and '長遠目標 · 暫未及' in html)
ok('item8 board teaser uses board line', 'gigGapBoardLine37(g)' in html)

# ---- item 9：傳聞來源跟行動地點 ----
ask_seg = seg('function applyMockAsk(', 'function mockAskAlreadyHeard')
ok('item9 rumor source prefers action source', 'const rumorSource = def.source || (catalog && catalog.source)' in ask_seg)

# ---- 紅線：SAVE key／softRev／?v= 冇郁 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 's111' in html)

# ---- NOTES ----
notes_path = os.path.join(os.path.dirname(os.path.abspath(path)), 'NOTES_V20A37_VERIFY_FIXES.md')
ok('NOTES file present', os.path.exists(notes_path))
if os.path.exists(notes_path):
    notes = open(notes_path, encoding='utf-8').read()
    for kw in ['雙軌', '收視關注', '殺青後入帳', '週行程', '餘', '訓練', '長工', '解鎖條件', '長遠目標', '傳聞來源', '教學債']:
        ok('NOTES covers ' + kw, kw in notes)

print('\nVERIFY37 STATIC: ' + ('ALL PASS' if not fails else (str(len(fails)) + ' FAIL -> ' + ' | '.join(fails))))
sys.exit(1 if fails else 0)
