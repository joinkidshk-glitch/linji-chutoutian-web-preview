# v20a348 resync：tutorial TUT_MAP 句經官方 qwen4-max 潤飾收緊（意思不變），釘句改查新句。
# 引導包（v20a34）靜態測試：接線斷言＋P0-3 指引文案核對＋壓力真碼分支釘住。
import re, sys, json, os
html = open(sys.argv[1] if len(sys.argv)>1 else 'index.html', encoding='utf-8').read()
fails = []
def ok(name, cond):
    if not cond: fails.append(name)
    print(('PASS' if cond else 'FAIL')+' '+name)

def seg(start, end):
    return html.split(start)[1].split(end)[0]

# ---- P0-1：差額接線 ----
ok('gap helpers exist', 'function gigGapBits34(' in html and 'function gigGapLine34(' in html and 'function gigGapTotal34(' in html)
gap_seg = seg('function gigGapBits34(', 'function gigGapTotal34(')
ok('gap calc reuses fameFloor + req + STAT_LABEL (same source as detail)',
   'fameFloor(g)' in gap_seg and 'g.req' in gap_seg and 'STAT_LABEL' in gap_seg)
ok('gap calc does not touch canAudition', 'canAudition' not in gap_seg)
teaser_seg = seg('function gigBoardTeaserHtml(', 'function gigTypeCoarse(')
ok('teaser renders gap only when locked', 'boardState==="locked"' in teaser_seg and 'gt-gap' in teaser_seg and 'gigGapLine34(g)' in teaser_seg)
ok('teaser closest marker via opts', 'opts.closest' in teaser_seg and '最接近' in teaser_seg)
scout_seg = seg('function doScout(L){', 'function applyTrainLesson(')
ok('doScout computes closest without reordering shown', 'closest34' in scout_seg and 'gigGapTotal34(g)' in scout_seg)
card_seg = seg('function gigCardHtml(', '/* ===== v19c PLAN_GIG_PAY_EXACT')
ok('gigCardHtml locked rate carries gap line', 'gigGapLine34(g)' in card_seg and 'req-gap' in card_seg)

# ---- P0-3：死路修正接線＋文案核對（v20a267：傳聞提示／拼合已刪，打聽改直接講情報） ----
ok('v267 rumorHearHint helper 已刪', 'function rumorHearHint' not in html and 'rumorHearHint' not in html)
ok('v267 MOCK_ASK 唔再派傳聞卡（grantsRumorId 清零）', 'grantsRumorId' not in html)
pt_seg = seg('function progressToward(node){', 'function softWeekGateShell')
ok('progressToward 冇傳聞步驟', 'rumorAny' not in pt_seg and 'rumorHearHint' not in pt_seg)
ok('progressToward loc step marked as play loc', 'remain.push("到"+names.join("或")+"播")' in pt_seg)
lock_seg = seg('function softLockPlayerLine(node){', 'function lockedCopy_noEngineeringTerms')
ok('softLockPlayerLine 冇傳聞位', 'rumorAny' not in lock_seg and 'rumorHearHint' not in lock_seg)
# 核對清單（靜態層面）：MOCK_ASK 只有茶餐廳／事務所派 tvb_rules 情報；電視台冇打聽行動
ask_seg = seg('const MOCK_ASK = {', 'function applyMockAsk(')
ok('MOCK_ASK 五個行動直接帶情報文字', ask_seg.count('intelText:') >= 5)
intel_locs = re.findall(r'(\w+):\s*\[\s*\{[^]]*?intelText:"入廠拍劇最忌遲到', ask_seg)
ok('tvb_rules 情報只喺 cafe_cha + agency_ho', sorted(set(intel_locs)) == ['agency_ho', 'cafe_cha'])
ok('no guidance text sends player to TV station to hear rules',
   '星河電視台聽' not in html and '去星河電視台打聽' not in html and '電視台打聽電視城規矩' not in html)
# v241b: inline TUTORIAL_ZH_HK deleted (JSON sole source); check live JSON + EXACT override instead
_tut_dir = os.path.dirname(sys.argv[1]) if len(sys.argv) > 1 else '.'
tut_json = json.load(open(os.path.join(_tut_dir, 'content', 'tutorial_zh_HK.json'), encoding='utf-8'))
tut_map = next(s for s in tut_json['steps'] if s['id'] == 'TUT_MAP')
tut_map_body = ' '.join(tut_map.get('body', []))
# v20a108 TEXT108 S-42：TUT_MAP 舊句「茶餐廳／事務所「打聽」不耗日」改寫做完整句，意思不變（打聽唔耗日＋傳聞入手帳）
# v241：v108 新句已直接寫入 JSON（舊 EXACT 覆寫隨死映射刪除）；查 JSON 新句，唔再查舊句。
ok('tutorial ask guidance names only cafe/agency (both have ask)', '在茶餐廳或事務所「打聽」不耗日' in tut_map_body)
ok('tutorial ask guidance EXACT override removed (dead map deleted, JSON carries written form)',
   '"能力不夠就去報名訓練；茶餐廳／事務所「打聽」不耗日，傳聞會記入手帳。":' not in html
   and '能力不足，就去報名訓練；在茶餐廳或事務所「打聽」不耗日，情報會直接告訴你。' in tut_map_body)
ok('v267 tutorial 唔再話傳聞記入手帳（情報站：直接講）',
   '打聽回來的傳聞會記入手帳' not in tut_map_body and '傳聞會記入手帳' not in html)

# ---- P0-4：過一日掣接線 ----
# v20a108 TEXT108 S-49：地圖金掣舊名「逛完・過一日」退役，統一叫「過一日」
ok('end-day button id + label in paintBar', 'id="map-end-day"' in html and '>過一日</button>' in html)
pb_seg = seg('function paintBar(){', 'let __storyMapRedrawT')
ok('end-day button only on map days (isMapDay gate)', 'isMapDay(todayPlanId())' in pb_seg and 'map-end-day' in pb_seg)
ok('end-day button excluded when homeEditable', 'S.homeEditable' in pb_seg)
ok('end-day click routes to existing confirmEarlyRestFromMenu', 'edBtn.onclick' in pb_seg and 'confirmEarlyRestFromMenu()' in pb_seg)
ok('endBrowseDayGoHome unchanged path (writeTodayPlan rest + tickDay)',
   'writeTodayPlan("rest")' in seg('function endBrowseDayGoHome(){', 'function goJournalFromMenu()'))

# ---- P0-5：出場交代接線 ----
ok('debt origin table exists with four opening debts',
   all(k in seg('const DEBT_ORIGIN_LINES34', 'function renderDebtPane(){') for k in
       ['debt_family_home', 'card_ho_spring', 'card_zhang_spring', 'debt_ho_tutorial']))
debt_seg = seg('function renderDebtPane(){', 'function playPushDoor()')
ok('debt pane renders origin lines for season + mock cards', debt_seg.count('DEBT_ORIGIN_LINES34') >= 3 and '來歷：' in debt_seg)
ok('debt pane intro line present', '這頁記住誰欠阿偉、阿偉欠誰' in debt_seg)
ok('v267 renderRumorPane 已刪', 'function renderRumorPane(' not in html)
ok('v267 傳聞頁介紹句已刪', '呢頁係你聽返嚟嘅傳聞碎片' not in html)
ok('v267 傳聞卡來源 fallback 已刪', '街坊傳聞' not in html)
ok('debt data structures untouched (no origin field written into debt rows)',
   'origin34' not in seg('function ensureFamilyHomeDebt(){', '/* 還清屋企債'))

# ---- P1-1(a)：壓力真碼分支釘住（helper 數字要同呢度一致） ----
ok('stressImpact34 helper exists', 'function stressImpact34(' in html and 'function stressImpactLine34(' in html)
street_seg = seg('else if(id==="street"){', 'else if(id==="cafe_gig"){')
cafe_seg = seg('else if(id==="cafe_gig"){', 'else if(id.startsWith("job:")')
ok('REAL income code: street stress>=90 pay*0.2', 'pay*0.2' in street_seg and 'st>=90' in street_seg)
ok('REAL income code: street stress>=70 pay*0.5', 'pay*0.5' in street_seg and 'st>=70' in street_seg)
ok('REAL income code: cafe stress>=90 pay*0.2 / >=70 pay*0.5', 'pay*0.2' in cafe_seg and 'pay*0.5' in cafe_seg)
chance_seg = seg('function chance(gig){', '/** Concise lock reason')
ok('REAL chance code: stress>=70 p*=0.78', 'p *= 0.78' in chance_seg and '>=70' in chance_seg)
ok('REAL chance code: stress>=90 p*=0.7 (cumulative)', 'p *= 0.7' in chance_seg and '>=90' in chance_seg)
imp_seg = seg('function stressImpact34(', 'function stressImpactLine34(')
ok('helper mirrors real branches (0.5/0.78 then 0.2/0.78*0.7)',
   'income = 0.5' in imp_seg and 'audition = 0.78' in imp_seg and 'income = 0.2' in imp_seg and '0.78*0.7' in imp_seg)
prev_seg = seg('function showStressPreviewModal(pv, go){', 'function confirmPlan(){')
ok('preview modal renders consequence line from pv.peak', 'stressImpactLine34(pv.peak, "高峰壓力")' in prev_seg)

# ---- P1-1(b)：雙軌解釋接線 ----
ok('dual explainer helper exists', 'function dualTrackExplainHtml34(' in html)
exp_seg = seg('function dualTrackExplainHtml34(', 'try{\n  window.__dualHud')
# v20a37 改約：正 delta 門檻經實機證實永不觸發（N1/N2 delta 恆 0）；改為「有真結算 dual 物件＋只出一次旗」
ok('explainer gated on real settle dual object + once flag',
   'guidanceDualExplained34' in exp_seg and 'result.dual' in exp_seg)
ok('explainer scale matches newspaperNameTier thresholds (15 named / 40 titled)',
   '去到 15' in exp_seg and '去到 40' in exp_seg)
sr_seg = seg('function showResult(node, choice, result){', 'function newlyOpenAfter')
ok('showResult appends explainer once after dual html', 'dualTrackExplainHtml34(result)' in sr_seg)

# ---- 紅線：SAVE key／softRev／?v= 冇郁 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
print('\nGUIDANCE34 STATIC: ' + ('ALL PASS' if not fails else str(len(fails)) + ' FAIL'))
sys.exit(1 if fails else 0)
