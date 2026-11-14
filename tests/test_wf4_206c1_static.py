# v20a206 C1：迎新期保底機制（pity timer）靜態測試。
# 用法：python3 tests/test_wf4_206c1_static.py [path-to-index.html]
# 反證：喺 v203 落地基線（main 165597e）上行 → 冇 pityDay／wf4SeenAny／保底檢查 → 多項乾淨 FAIL。
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def fn_body(name):
    i = src.find('function ' + name + '(')
    if i < 0:
        return None
    j = src.find('{', i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == '{':
            depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    return None

# (1) CFG：pityDay 係數字 7，頻率全部唔郁
m = re.search(r'const WF4_CFG = \{([^}]*)\};', src)
ok('WF4_CFG 搵到', m is not None)
cfg = m.group(1) if m else ''
ok('WF4_CFG pityDay:7', 'pityDay:7' in cfg.replace(' ', ''))
ok('WF4_CFG 基線 pDay／pLoc 仲係 0.03', 'pDay:0.03' in cfg.replace(' ', '') and 'pLoc:0.03' in cfg.replace(' ', ''))
ok('WF4_CFG 迎新頻率唔郁（pDayWelcome 0.12／pLocWelcome 0.08／welcomeDays 30）',
   'pDayWelcome:0.12' in cfg.replace(' ', '') and 'pLocWelcome:0.08' in cfg.replace(' ', '')
   and 'welcomeDays:30' in cfg.replace(' ', ''))
ok('WF4_CFG gapDays／locTriesPerDay／pendingMaxAge 唔郁（3／3／2）',
   'gapDays:3' in cfg.replace(' ', '') and 'locTriesPerDay:3' in cfg.replace(' ', '')
   and 'pendingMaxAge:2' in cfg.replace(' ', ''))

# (2) wf4SeenAny 存在，兩邊都計
seen_fn = fn_body('wf4SeenAny')
ok('wf4SeenAny 函數存在', seen_fn is not None)
if seen_fn:
    ok('wf4SeenAny 計 __n（(st.seen.__n||0) > 0）', '(st.seen.__n||0) > 0' in seen_fn)
    ok('wf4SeenAny 逐個 event id 計（Object.keys(st.seen)，__n 本身唔計）',
       'Object.keys(st.seen)' in seen_fn and 'k !== "__n"' in seen_fn)

# (3) wf4DailyTick 入面有保底檢查，位置啱：base／pending 守衛之後、概率擲骰之前
tick = fn_body('wf4DailyTick')
ok('wf4DailyTick 函數存在', tick is not None)
if tick:
    ok('保底檢查用 CFG 數字（WF4_CFG.pityDay，唔寫死 7）', 'WF4_CFG.pityDay' in tick)
    ok('保底檢查問 wf4SeenAny()（從未見過）', 'wf4SeenAny()' in tick)
    ok('保底用 wf4PickEvent("day", null) 揀未見過嘅 day 事件', 'wf4PickEvent("day", null)' in tick)
    ok('保底入 pending（st.pending = pev.id，行正常 pending 機制）', 'st.pending = pev.id' in tick)
    ok('保底唔直接 fire（wf4DailyTick 入面零 wf4Fire 呼叫）', 'wf4Fire(' not in tick)
    i_base = tick.find('if(!wf4BaseOk()) return;')
    i_pity = tick.find('WF4_CFG.pityDay')
    i_roll = tick.find('wf4Rand("wf4day:"+day)')
    ok('保底位置：喺 wf4BaseOk() 守衛之後', i_base >= 0 and i_pity > i_base)
    ok('保底位置：喺概率擲骰之前', i_roll >= 0 and i_pity < i_roll)
    ok('保底設完 pending 即 return（唔再行正常擲骰）',
       bool(re.search(r'if\s*\(pev\)\s*\{\s*st\.pending = pev\.id; st\.pendingDay = day;\s*\}\s*return;', tick)))
    ok('原有概率擲骰仲喺度（wf4Rand("wf4day:"+day) >= wf4EffPDay(day)）',
       'wf4Rand("wf4day:"+day) >= wf4EffPDay(day)' in tick)
    ok('原有 pending 守衛仲喺度（if(st.pending) return;）', 'if(st.pending) return;' in tick)

# (4) 順序：wf4SeenAny 定義喺 wf4DailyTick 之前（唔靠 hoisting 以外嘅嘢）
i_seen = src.find('function wf4SeenAny(')
i_tick = src.find('function wf4DailyTick(')
ok('wf4SeenAny 定義喺 wf4DailyTick 之前', i_seen >= 0 and i_tick > i_seen)

# (5) 池／頻率函數零掂：事件總數仲係 113，迎新曲線函數仲喺度
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
n_ev = len(re.findall(r'\{\s*id:"wf4_ev_', arr.group(1))) if arr else -1
ok('事件池仲係 113 單（保底唔加／減事件）', n_ev == 113)
ok('wf4EffPDay／wf4EffPLoc 函數仲喺度（迎新曲線唔郁）',
   fn_body('wf4EffPDay') is not None and fn_body('wf4EffPLoc') is not None)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
