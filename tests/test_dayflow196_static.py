# v20a196 日流程自動連跑＋故事播放鎖死返地圖・靜態測試
# 逐字照 NOTES_V20A196 §0（D1–D7）＋§6 實作清單核對。
# 用法：python3 tests/test_dayflow196_static.py [path-to-index.html]
# 反證：對 pristine（v191）index 行 → 新函數／新寫法全部唔存在，乾淨 FAIL（唔 crash）。
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

fn_next = seg('function nextDayIsMap(){', 'function story165AfterContTake(){')
fn_slot = seg('function story165AfterContTake(){', 'function dayEndContinueButtons(')
fn_dayend = seg('function dayEndContinueButtons(', 'function flushWeekAccelSummary(')
fn_chain = seg('function morningChain196(', 'function runScheduleFromToday(){')
fn_run = seg('function runScheduleFromToday(){', 'function resolvePlannedDay(')
fn_map = seg('function goToMapForBrowse(){', '/* v19z8')
fn_after = seg('function afterDayModal(', '/* v20a38')
fn_resolve = seg('function resolvePlannedDay(', 'function autoPushC1IfNeeded(')
fn_forced = seg('function story165TryForcedPlay(', '/** v17p PLAN 9.1')
fn_wf4 = seg('function wf4PresentPending(', '/* ---------- WF4 碎片庫')
fn_fen = seg('function wf4PresentFenFarewell(', '/* ---------- WF4 對手')
fn_result = seg('  function showResult(', '  function render(){')
fn_render = seg('  function render(){', '  function playOpenPicker(){')
fn_confirm = seg('function presentStartScheduleConfirm45(', '/** Compact rest day-end')
fn_rest = seg('function presentRestSleepDayEnd(', 'function playRestSleepFx(')

# ---- 1：D7 helper＋D3 slot helpers 在位 ----
ok('D7 helper nextDayIsMap exists with wrap:/audition: mapish logic',
   'function nextDayIsMap(){' in html
   and '!nextId' in fn_next and 'isMapDay(nextId)' in fn_next
   and 'String(nextId).startsWith("wrap:")' in fn_next
   and 'String(nextId).startsWith("audition:")' in fn_next)
ok('D3 slot helpers exist (take/set/clear on FREEPLAY_FW._story165AfterCont)',
   'function story165AfterContTake(){' in html
   and 'function story165AfterContSet(kind){' in html
   and 'function story165AfterContClear(){' in html
   and 'FREEPLAY_FW._story165AfterCont' in fn_slot)
ok('slot take is one-shot (clears on read) and validates kind',
   'FREEPLAY_FW._story165AfterCont = null;' in fn_slot
   and '(v==="schedule" || v==="map") ? v : null' in fn_slot)

# ---- 2：共用晨鏈 runner ----
ok('morningChain196 exists with both modes (mapMode flag + afterKind)',
   'function morningChain196(finalFn, opts){' in html
   and 'const afterKind = opts.mapMode ? "map" : "schedule";' in fn_chain)
ok('chain order is reward>award>paper>aud>wf4>sick>kick>forced>done',
   idx(fn_chain, 'presentPendingPostShootReward(step)') > 0
   and idx(fn_chain, 'presentPendingPostShootReward(step)') < idx(fn_chain, 'presentPendingAward(step)')
   < idx(fn_chain, 'presentDueMorningPaper(step)') < idx(fn_chain, 'aud91PresentDue(step)')
   < idx(fn_chain, 'wf4PresentPending(step,') < idx(fn_chain, 'conseq61ResolveSickDay')
   < idx(fn_chain, 'kickScheduleIfNeeded()') < idx(fn_chain, 'story165TryForcedPlay(afterKind)')
   < idx(fn_chain, 'done();'))
ok('chain kick is map-mode only', 'if(opts.mapMode){' in fn_chain)
ok('chain WF4 passes allowForced + afterCont',
   'wf4PresentPending(step, { allowForced:true, afterCont:afterKind })' in fn_chain)
ok('runScheduleFromToday scheduled day runs full chain then resolvePlannedDay',
   'morningChain196(()=>{ resolvePlannedDay(id); }, { mapMode:false });' in fn_run)
ok('runScheduleFromToday mapish still goes to map (week-accel summary intact)',
   '本週加速完成' in fn_run and 'goToMapForBrowse();' in fn_run)
ok('goToMapForBrowse delegates to shared chain in map mode, then shows map',
   'morningChain196(()=>{' in fn_map and '{ mapMode:true });' in fn_map
   and idx(fn_map, 'morningChain196(()=>{') < idx(fn_map, 'show("v-map")'))
ok('goToMapForBrowse no longer has its own inline chain (no duplicated award/paper calls)',
   'presentPendingAward(()=>{ try{ goToMapForBrowse();' not in fn_map
   and 'presentDueMorningPaper(()=>{ try{ goToMapForBrowse();' not in fn_map
   and 'wf4PresentPending()) return' not in fn_map)

# ---- 3：日結掣＋dismiss 跟 D7 ----
ok('dayEndContinueButtons uses shared helper for nextIsMap',
   'const nextIsMap = nextDayIsMap();' in fn_dayend)
ok('soft branch no longer emits 返回地圖 (only one such label left: the map branch)',
   fn_dayend.count('label:"返回地圖"') == 1
   and 'label:"開始今日行程", role:"g", on:goRunSchedule' in fn_dayend)
ok('forced/map/ended branches unchanged',
   'btns.push({label:"開始今日行程", role:"p", on:goRunSchedule});' in fn_dayend
   and 'btns.push({label:"回家結算", role:"p", on:goRunSchedule});' in fn_dayend
   and 'label:"返回地圖", role:"p", on: (typeof goRunSchedule==="function") ? goRunSchedule' in fn_dayend)
ok('accel link unchanged', 'role:"link"' in fn_dayend and '想跳過本週剩餘日子？加速' in fn_dayend)
ok('afterDayModal dismiss follows D7 (schedule=go, map=goToMapForBrowse)',
   'if(nextDayIsMap()) goToMapForBrowse(); else go();' in fn_after)
ok('resolvePlannedDay dismissNb follows D7 (reward first, then schedule/map)',
   'if(nextDayIsMap()) goToMapForBrowse(); else nextNb();' in fn_resolve)
ok('degraded fallbacks follow D7 (no unconditional 返回地圖)',
   fn_after.count('label: ended?"回家結算":"返回地圖"') == 0
   and fn_resolve.count('label: ended?"回家結算":"返回地圖"') == 0)

# ---- 4：WF4（continuation＋forced 放寬＋Fen slot）----
ok('wf4PresentPending takes (cont, opts) with allowForced gate',
   'function wf4PresentPending(cont, opts){' in html
   and 'if(!opts.allowForced && typeof todayIsForcedDay==="function" && todayIsForcedDay()) return false;' in fn_wf4)
ok('wf4PresentPending fires with chain continuation (not hardcoded map)',
   'wf4Fire(ev, done196);' in fn_wf4
   and 'const done196 = (typeof cont==="function") ? cont :' in fn_wf4)
ok('wf4PresentPending passes afterCont to Fen farewell',
   'wf4PresentFenFarewell(opts.afterCont)' in fn_wf4)
ok('wf4PresentFenFarewell takes afterCont and writes slot before story starts',
   'function wf4PresentFenFarewell(afterCont){' in html
   and 'story165AfterContSet(afterCont || "map")' in fn_fen)
ok('story165TryForcedPlay takes afterCont and writes slot on start',
   'function story165TryForcedPlay(afterCont){' in html
   and 'story165AfterContSet(afterCont || "map")' in fn_forced)
ok('slot is written at exactly two places (forced play + Fen farewell)',
   html.count('story165AfterContSet(afterCont || "map")') == 2)

# ---- 5：showResult 消費 slot；下一節唔消費；進度清 slot ----
ok('showResult close consumes slot: schedule runs schedule, map goes to map',
   'const cont196 = (typeof story165AfterContTake==="function") ? story165AfterContTake() : null;' in fn_result
   and 'if(cont196==="schedule"){ try{ runScheduleFromToday(); }catch(_e){} return; }' in fn_result
   and 'if(cont196==="map"){ try{ goToMapForBrowse(); }catch(_e){} return; }' in fn_result)
ok('showResult onDismiss consumes slot too',
   'const cont196d = (typeof story165AfterContTake==="function") ? story165AfterContTake() : null;' in fn_result
   and 'if(cont196d==="schedule"){ try{ runScheduleFromToday(); }catch(_e){} return; }' in fn_result)
ok('showResult takes slot exactly twice (close + dismiss), clears it on 進度 x2',
   fn_result.count('story165AfterContTake()') == 2
   and fn_result.count('story165AfterContClear()') == 2)
ok('showResult no longer unconditionally shows v-map on close (slot checked first)',
   idx(fn_result, 'story165AfterContTake()') < idx(fn_result, 'try{ show("v-map"); }catch(_e){}'))

# ---- 6：D4 故事鎖死 ----
ok('render no longer emits 先返回 anywhere',
   '"先返回"' not in fn_render)
ok('lockedForced / leaveStory / seedDismiss code removed (comments may still name them)',
   'const lockedForced' not in html and 'if(!lockedForced)' not in html
   and 'const leaveStory' not in html and 'const seedDismiss' not in html)
ok('render onDismiss unconditionally re-renders (old lockedForced path for all stories)',
   'const dismissOpts = { onDismiss:()=>{ try{ render(); }catch(_e){} } };' in fn_render)
ok('spSoftSeedCanDismiss function kept (offer logic may use it); render only mentions it in a comment now',
   'function spSoftSeedCanDismiss(){' in html and fn_render.count('spSoftSeedCanDismiss()') == 1)
ok('跳至選項 untouched in render', '跳至選項' in fn_render)

# ---- 7：休息卡＋確認 modal ----
ok('confirm45: scheduled day has no 返回地圖, dismiss starts schedule',
   'const btns45 = [{ label:"開始今日行程"' in fn_confirm
   and 'if(mapNext45) btns45.push({ label:"返回地圖"' in fn_confirm
   and 'if(mapNext45) goMap(); else goStart();' in fn_confirm)
ok('rest card dismiss follows D7',
   'if(nextDayIsMap()) goMap(); else goSchedule();' in fn_rest)
ok('rest card fallback never defaults to goMap any more',
   'finish(orig || goMap)' not in html and 'orig : goMap' not in fn_rest)
ok('rest card confirm-failure path follows D7',
   'if(nextDayIsMap()) proceedMap(); else proceedSchedule();' in fn_rest)

# ---- 8：唔郁清單（紅線）----
ok('redline SAVE key untouched', 'starVolunteer_map_v19w' in html)
ok('redline softRev s107 present', 's107' in html)
ok('redline ?v= v20a10 present', '?v=20a10' in html)
ok('redline awards soft gate untouched (queueAwardsOnSeasonWindow still gated)',
   'awardsSoftOn()' in html)
ok('redline C17 gate untouched (weekMin 153 + backstopDay 1096)',
   'weekMin: 153' in html and 'backstopDay: 1096' in html)
ok('redline travel cap untouched', 'TRAVEL114_DAILY_CAP = 2' in html)
ok('redline handbook exits untouched (book70ExitHome / loc-close still exist)',
   'function book70ExitHome(' in html and 'document.getElementById("loc-close").onclick' in html)
ok('notes file exists', os.path.exists(os.path.join(os.path.dirname(os.path.abspath(path)), 'NOTES_V20A196.md')))

print('')
if fails:
    print('FAILED: ' + ' | '.join(fails))
    sys.exit(1)
print('DAYFLOW196 STATIC: ALL PASS')
