# v20a202 B1/B2/C1/C2・靜態測試
# 逐字核對四項修法嘅落點（文案層，唔郁 v196 承諾制流程）。
# 用法：python3 tests/test_dayend202_static.py [path-to-index.html]
# 反證：對 pristine main（860e790）index 行 → 全部 v202 新寫法唔存在，乾淨 FAIL（唔 crash）。
# 行號（2026-11-14，基底 860e790＋v202 改動後）：helpers L38153–38190、
# afterDayModal L37104、resolvePlannedDay L38340、modal L39609、
# showResult L28083、render L28210、enc79PlayEncounter L53710、
# presentStartScheduleConfirm45 L57728、presentRestSleepDayEnd L57764、
# CSS L1863–1865。rebase 後行號漂移要人手 resync（跟返現行慣例）。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end):
    # 搵唔到起點就返空字串：檢查項會乾淨 FAIL，唔會 crash（反證嗰陣要呢個行為）
    if start not in html:
        return ''
    i = html.index(start)
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

def idx(hay, needle):
    return hay.index(needle) if needle in hay else -1

fn_helpers = seg('function nextDayLabel202(){', 'function dayEndContinueButtons(')
fn_modal = seg('function modal(html, buttons, opts){', 'function closeModal(){')
fn_after = seg('function afterDayModal(', '/* v20a38')
fn_resolve = seg('function resolvePlannedDay(', 'function autoPushC1IfNeeded(')
fn_result = seg('  function showResult(', '  function render(){')
fn_render = seg('  function render(){', '  function playOpenPicker(){')
fn_confirm = seg('function presentStartScheduleConfirm45(', '/** Compact rest day-end')
fn_rest = seg('function presentRestSleepDayEnd(', 'function playRestSleepFx(')
fn_enc79 = seg('function enc79PlayEncounter(', '/* ===== v20a176 ROM176')

# ---- B1：下一日去向 helper ----
ok('B1 helpers exist (nextDayLabel202/dayEndNextLine202/dayEndDismissNote202/storyResultDestLine202)',
   'function nextDayLabel202(){' in html
   and 'function dayEndNextLine202(ended){' in html
   and 'function dayEndDismissNote202(ended){' in html
   and 'function storyResultDestLine202(){' in html)
ok('B1 label follows nextDayIsMap logic (mapish incl wrap:/audition:)',
   'isMapDay(id)' in fn_helpers and 'String(id).startsWith("wrap:")' in fn_helpers
   and 'String(id).startsWith("audition:")' in fn_helpers)
ok('B1 map day hardcodes 到處逛逛 (唔用 scout_nt raw id)',
   'label:"到處逛逛"' in fn_helpers)
ok('B1 rest special-cased to 休息 (唔係 PLAN_ITEMS 嘅「休息睡覺」)',
   'if(String(id)==="rest") return { kind:"schedule", label:"休息" };' in fn_helpers)
ok('B1 schedule line says （自動行程）, map line says （返地圖自由行）',
   '（自動行程）' in fn_helpers and '（返地圖自由行）' in fn_helpers)
ok('B1 ended returns no next line',
   'if(ended) return "";' in fn_helpers)
ok('B1 result dest line only peeks slot (唔消費 _story165AfterCont)',
   'FREEPLAY_FW._story165AfterCont || null' in fn_helpers
   and 'story165AfterContTake' not in fn_helpers)
ok('B1 result dest line uses 今日 framing for schedule slot',
   '關閉之後：繼續跑今日行程' in fn_helpers and '關閉：返地圖' in fn_helpers)

# ---- B1/B2：三塊日結板都掛咗去向行＋dismiss note ----
ok('B1 afterDayModal: next line right after <h3>',
   '`<h3>${title}</h3>${dayEndNextLine202(ended)}' in fn_after)
ok('B2 afterDayModal: dismiss note pushed to btns before modal()',
   'btns.push(dayEndDismissNote202(ended))' in fn_after)
ok('B1 resolvePlannedDay: both modal branches have next line after <h3>',
   fn_resolve.count('`<h3>${title}</h3>${dayEndNextLine202(ended)}') == 2)
ok('B2 resolvePlannedDay: dismiss note pushed once (兩分支共用 btns)',
   fn_resolve.count('btns.push(dayEndDismissNote202(ended))') == 1)
ok('B1 rest card: next line right after <h3>',
   '`<h3>${title}</h3>${dayEndNextLine202(ended)}' in fn_rest)
ok('B2 rest card: dismiss note pushed to btns before modal()',
   'btns.push(dayEndDismissNote202(ended))' in fn_rest)
ok('B1 showResult: dest line right after <h3>劇情結算</h3>',
   '`<h3>劇情結算</h3>${storyResultDestLine202()}' in fn_result)
ok('B2 dismiss note wording covers all three destinations',
   '撳出面＝繼續跑聽日行程' in fn_helpers and '撳出面＝返地圖' in fn_helpers
   and '撳出面＝回家結算' in fn_helpers)

# ---- B2：modal() role:"note" 支援 ----
ok('B2 modal() renders role:"note" as a plain div (唔係掣)',
   'b.role==="note"' in fn_modal and 'document.createElement("div")' in fn_modal
   and 'note.className="modal-note202"' in fn_modal)
ok('B2 note has no onclick attached (唔可撳)',
   idx(fn_modal, 'role==="note"') < idx(fn_modal, 'btn.onclick'))

# ---- C1：確認 modal 取消掣 ----
ok('C1 confirm takes onCancel (third arg)',
   'function presentStartScheduleConfirm45(onStart, onMap, onCancel){' in html)
ok('C1 cancel button labelled 取消（返去休息卡）',
   '取消（返去休息卡）' in fn_confirm)
ok('C1 cancel only rendered when onCancel given (defensive)',
   'if(goCancel) btns45.push' in fn_confirm)
ok('C1 confirm dismiss note states the D1 rule',
   '撳出面＝開始今日行程' in fn_confirm and '撳出面＝返地圖' in fn_confirm)
ok('C1 rest card passes onCancel that re-presents the same rest card',
   'presentStartScheduleConfirm45(proceedSchedule, proceedMap, ()=>{' in fn_rest
   and 'presentRestSleepDayEnd(opts);' in fn_rest)
ok('C1 confirm title stays a question (家下有真選擇，問句合理)',
   '<h3>開始今日行程？</h3>' in fn_confirm)

# ---- C2：故事鎖死提示 ----
ok('C2 StoryPlay render pushes lock hint note into modalBtns',
   '劇情進行中，播完先可以離開' in fn_render
   and 'modalBtns.push({ label:"劇情進行中，播完先可以離開", role:"note" });' in fn_render)
ok('C2 hint is pushed after the beats/choices branch (兩種 mode 都有)',
   idx(fn_render, 'modalBtns.push({ label:"劇情進行中，播完先可以離開", role:"note" });')
   > idx(fn_render, 'modalBtns.push({ label:"下一句"')
   and idx(fn_render, 'modalBtns.push({ label:"劇情進行中，播完先可以離開", role:"note" });')
   > idx(fn_render, 'modalBtns.push({ label:"完成這一節"'))
ok('C2 enc79 overlay NOT given the lock hint (佢有「點頭離開」出口，唔係鎖死)',
   '劇情進行中，播完先可以離開' not in fn_enc79
   and '點頭離開' in fn_enc79)

# ---- CSS ----
ok('CSS has .dayend-next202 + .modal-note202 + dark story override',
   '.dayend-next202{' in html and '.modal-note202{' in html
   and '#mask.story-play-on .modal-note202{' in html)

# ---- 流程唔郁（v196 承諾制原封不動）----
ok('v196 dismiss rules untouched (afterDayModal dismissFn / resolve dismissNb)',
   'const dismissFn = ended ? go :' in fn_after
   and 'const dismissNb = ended ? nextNbReward :' in fn_resolve)
ok('v196 confirm dismiss untouched (map→goMap / schedule→goStart)',
   'onDismiss: ()=>{ try{ if(mapNext45) goMap(); else goStart(); }catch(_e){} }' in fn_confirm)

print('')
if fails:
    print('FAILURES: %d -> %s' % (len(fails), ' | '.join(fails)))
    sys.exit(1)
print('ALL PASS')
