# v20a193 WF4 once 硬規則靜態測試：頻率／池／死 code 清理／紀律。
# 用法：python3 tests/test_wf4_193_static.py [path-to-index.html]
# 反證：喺 pristine main（b3db32f）上行 → repeatDays 仲喺度、池得 36 單、
#   pDay 0.30／gap 2 → 多項乾淨 FAIL。
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
src = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- 紀律：SAVE key／softRev／?v= 冇改 ---
ok('SAVE key 不變', 'starVolunteer_map_v19w' in src)
ok('softRev 不變', 's107' in src)
ok('產品 ?v= 不變', 'v20a10' in src)

# --- 頻率（模擬掃出嘅數字） ---
cfg = re.search(r'const WF4_CFG = \{([^}]*)\};', src)
ok('WF4_CFG 存在', cfg is not None)
cfg_body = cfg.group(1) if cfg else ''
ok('WF4_CFG pDay 0.03', 'pDay:0.03' in cfg_body)
ok('WF4_CFG pLoc 0.03', 'pLoc:0.03' in cfg_body)
ok('WF4_CFG gapDays 3', 'gapDays:3' in cfg_body)
ok('WF4_CFG 冇 repeatDays', 'repeatDays' not in cfg_body)
ok('WF4_CFG locTriesPerDay 3／pendingMaxAge 2 不變',
   'locTriesPerDay:3' in cfg_body and 'pendingMaxAge:2' in cfg_body)

# --- once 機制：pick 唔再讀 evDay／repeatDays，見過即剔 ---
pick = src[src.find('function wf4PickEvent'):src.find('function wf4ApplyFx')]
ok('wf4PickEvent 存在', 'function wf4PickEvent' in src)
ok('wf4PickEvent 見過即剔（seen 過濾，唔分 once 旗）',
   "(st.seen[ev.id]||0) > 0) return false" in pick)
ok('wf4PickEvent 冇 evDay 冷卻讀取', 'evDay' not in pick)
ok('wf4PickEvent 冇 repeatDays', 'repeatDays' not in pick)
ok('wf4PickEvent 池空回 null', 'if(!pool.length) return null;' in pick)
fire = src[src.find('function wf4Fire'):src.find('function wf4DailyTick')]
ok('wf4Fire 唔再寫 evDay', 'evDay' not in fire)
ok('wf4Fire 寫 seen＋saveQ', 'st.seen[ev.id]' in fire and 'saveQ()' in fire)
pp = src[src.find('function wf4PresentPending'):src.find('/* ---------- WF4 碎片庫補完')]
ok('wf4PresentPending 守 once（pending 已見過就清走）',
   "(st.seen[st.pending]||0) > 0" in pp and 'st.pending = null; return false;' in pp)
ok('wf4PresentPending 守衛排喺 baseOk／強制／病假之前（Case C：清 stale 唔靠 base 條件）',
   0 <= pp.find("(st.seen[st.pending]||0) > 0") < pp.find("if(!wf4BaseOk()) return false;")
   and pp.find("(st.seen[st.pending]||0) > 0") < pp.find("todayIsForcedDay")
   and pp.find("(st.seen[st.pending]||0) > 0") < pp.find("conseq61IsSickToday"))
tick = src[src.find('function wf4DailyTick'):src.find('function wf4TryLocEvent')]
ok('wf4DailyTick 清 stale pending（唔等過期，load 補跑嗰日即清）',
   "(st.seen[st.pending]||0) > 0" in tick)
loc = src[src.find('function wf4TryLocEvent'):src.find('function wf4PresentPending')]
ok('wf4TryLocEvent 清 stale pending（唔閘住入場擲骰）',
   "(st.seen[st.pending]||0) > 0" in loc)
ok('v198×v193：wf4TryLocEvent 清 stale pending 排喺強制播 defer 守衛（story165CanPlay）之前——'
   '清 stale 係狀態清理，唔可以俾 defer 早退擋住',
   0 <= loc.find("(st.seen[st.pending]||0) > 0") < loc.find("story165CanPlay()")
   and loc.find("story165CanPlay()") < loc.find("st.locTries += 1"))
ok('全檔 repeatDays 只剩註解提及（唔係 code）',
   src.count('repeatDays') <= 1)

# --- 池：72 單，day／loc 各 36，每地點 ≥4 ---
ev_ids = re.findall(r'id:"(wf4_ev_\w+)"', src)
ok('事件總數 72', len(ev_ids) == 72)
ok('id 唯一', len(set(ev_ids)) == len(ev_ids))
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
ok('DAILY_EVENTS_WF4 陣列搵到', arr is not None)
if arr:
    body = arr.group(1)
    ok('day 池 36', body.count('trig:"day"') == 36)
    ok('loc 池 36', body.count('trig:"loc"') == 36)
    for loc, n in [('film_lion', 5), ('film_cotton', 4), ('film_harbour', 4),
                   ('tvb_longmen', 4), ('tvb_harbour', 4), ('tvb_kowloon', 4),
                   ('cafe_cha', 11)]:
        ok('loc 池 %s＝%d 單' % (loc, n), body.count('loc:"%s"' % loc) == n)
    # 條件閘放寬（v20a193）
    ok('day03 放寬到 moneyMax 1000', 'moneyMax:1000' in body and 'moneyMax:300' not in body)
    ok('home01 放寬到 stressMin 45', 'stressMin:45' in body)
    ok('day04 放寬到 stressMin 60', 'stressMin:60' in body and 'stressMin:75' not in body)

# --- 新事件場景：36 單無 loc 全入覆寫表（唔留灰） ---
m = re.search(r'const WF4_SCENE_OVERRIDE134 = \{(.*?)\};', src, re.S)
ok('WF4_SCENE_OVERRIDE134 存在', m is not None)
if m:
    table = set(re.findall(r'(wf4_ev_\w+):"', m.group(1)))
    ok('覆寫表 36 行', len(table) == 36)
    for new_id in ['wf4_ev_day05', 'wf4_ev_day16', 'wf4_ev_st12', 'wf4_ev_st17']:
        ok('新 day 事件入覆寫表：' + new_id, new_id in table)

# --- 新事件文案紀律 ---
blk = src[src.find('const DAILY_EVENTS_WF4'):src.find('/* ===== Weave Phase 3-3')]
ok('WF4 區塊冇真人名／時代錯誤詞',
   not re.search(r'周潤發|劉德華|張國榮|陳百強|梅艷芳|VCD|互聯網|狗仔隊', blk))
ok('WF4 區塊冇 1989 指向', '1989年' not in blk and '1989-06' not in blk)

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
