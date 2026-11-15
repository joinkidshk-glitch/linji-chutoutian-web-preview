# -*- coding: utf-8 -*-
# v20a198 靜態測試：B1 強制播優先於 WF4 地點事件＋N1 死 code 清除＋N2 鎖住插入行／按段合併＋N3 場景行唔重複路線名。
# B1：wf4TryLocEvent 有強制播 pending（story165CanPlay）嗰陣 defer，唔計 locTries；boss01 定義唔郁。
# C1：storyMapHintHtml／refreshMapHintStory 宣告＋export＋呼叫點全部冇晒；
#     storyMainProgressLine 保留＋仲行共用幕號。
# C2：鎖住插入行（prog71-insert）＋遠幕按段合併（segOf198／farLbl198）；舊 guard／舊「–17」模板冇晒；
#     路線條件唔再寫死「行電視線」。
# C3：場景頂 head 經 storySettingStripRoute198 剝走路線名；節點 setting 資料本身唔郁。
# 反證：喺 pristine（v191）index 上行，B1／N2／N3 新斷言要乾淨 FAIL（唔 crash）；
#      其餘基線斷言（SAVE／softRev／?v=／閘唔郁）喺 pristine 一樣 PASS。
# 用法：python3 tests/test_story198_static.py [path-to-index.html]
import json
import re
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
# v20a234：內嵌主線表已刪，N6 setting 正本而家係 JSON pack；N6F 仲係內嵌 BR89 表。
pack = json.loads((p.parent / 'content' / 'story_detail_n1_to_n17.json').read_text(encoding='utf-8'))
n6 = next((n for n in pack['nodes'] if n.get('id') == 'N6'), None)
fails = []


def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)


def func_body(src_text, fname):
    """抽一段 function fname(...) { ... }（由宣告行起到下一個同級 function 為止）。"""
    m = re.search(r'function ' + re.escape(fname) + r'\b', src_text)
    if not m:
        return ''
    start = m.start()
    m2 = re.search(r'\n  function ', src_text[start + 10:])
    return src_text[start:start + 10 + m2.start()] if m2 else src_text[start:]


def func_body_braces(src_text, fname):
    """抽一段頂層 function（大括號計數，唔受下一個 function 縮排影響）。"""
    m = re.search(r'function ' + re.escape(fname) + r'\b', src_text)
    if not m:
        return ''
    j = src_text.index('{', m.start())
    depth = 0
    for k in range(j, len(src_text)):
        if src_text[k] == '{':
            depth += 1
        elif src_text[k] == '}':
            depth -= 1
            if depth == 0:
                return src_text[m.start():k + 1]
    return ''


# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('開放條件／閘唔郁', 'N6F: { route: "route_film", weekMin: 15 }' in src
   and 'N18: { needDone: ["N5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"] }' in src
   and 'N19: { needDone: ["N18"], weekMin: 61, yearMin: 1991, seasonIn: ["春"] }' in src)
ok('WF4 事件池唔郁（boss01 之外嘅事件唔掂）', 'wf4_ev_cha01' in src and 'wf4_ev_boss02' in src
   and 'wf4_ev_boss03' in src and 'wf4_ev_st10' in src)
# v20a193 改咗頻率（用戶拍板：once 硬規則嘅數學代價，密度跌約 4 倍）——
# v198 嗰陣嘅 0.30／0.20 已經唔係現行值；呢度釘死 v193 新值。v198 嘅保證係
# boss01 定義／池唔郁，唔係機率唔郁。
ok('WF4_CFG 機率跟 v193（pDay／pLoc 0.03；v198 嗰陣係 0.30／0.20）',
   'pDay:0.03' in src and 'pLoc:0.03' in src)

# --- B1：強制播優先於 WF4 地點事件 ---
wf4 = func_body_braces(src, 'wf4TryLocEvent')
ok('B1：wf4TryLocEvent 有強制播守衛（story165CanPlay）', 'story165CanPlay()' in wf4)
ok('B1：守衛喺 locTries 計數之前（defer 唔嘥當日事件額）',
   'story165CanPlay()' in wf4 and 'st.locTries += 1' in wf4
   and wf4.index('story165CanPlay()') < wf4.index('st.locTries += 1'))
ok('B1：守衛喺 roll 之前（唔係擲完先攔）',
   'story165CanPlay()' in wf4 and 'wf4Rand("wf4loc:' in wf4
   and wf4.index('story165CanPlay()') < wf4.index('wf4Rand("wf4loc:'))
ok('B1：A1 守衛仲喺度（同一地點有主線待播照樣 defer）', 'enc79StoryPendingAt(locId)' in wf4)
ok('B1：boss01 定義唔郁（once:true、茶餐廳、setFlag boss_met）',
   'id:"wf4_ev_boss01", grp:"茶餐廳", trig:"loc", loc:"cafe_cha", once:true, setFlag:"boss_met"' in src)
ok('B1：story165CanPlay 本身唔郁（仲係經 story165NextOpen）',
   'return story165NextOpen();' in func_body_braces(src, 'story165CanPlay'))
ok('B1：晨鏈 wf4PresentPending 次序唔郁（pending day 事件先行，唔關 boss01 事）',
   # v20a196 D2：晨鏈搬入共用 runner morningChain196，wf4PresentPending 改帶續鏈（step＋allowForced／afterCont），
   # 舊式無參呼叫已拎走；pending day 事件仍然喺鏈入面、仍然喺強制播之前，boss01（trig:"loc"）仍然唔關事。
   'wf4PresentPending(step, { allowForced:true, afterCont:afterKind })' in src
   and src.index('wf4PresentPending(step') < src.index('強制播（播之前寫續鏈 slot'))

# --- C1：死 code 已清 ---
ok('N1：storyMapHintHtml 宣告已拎走', 'function storyMapHintHtml(){' not in src)
ok('N1：refreshMapHintStory 宣告已拎走', 'function refreshMapHintStory(){' not in src)
ok('N1：window export 已拎走', 'window.refreshMapHintStory' not in src)
ok('N1：呼叫點已拎走（唔留 refreshMapHintStory();）', 'refreshMapHintStory();' not in src)
ok('N1：storyMainProgressLine 保留（已測試嘅「下一幕」句式規格）', 'function storyMainProgressLine(){' in src)
ok('N1：storyMainProgressLine 仲行共用幕號（唔係扮修好）',
   'storyActLabel(openMain.id)' in func_body(src, 'storyMainProgressLine')
   and 'storyActLabel(id)' in func_body(src, 'storyMainProgressLine'))
ok('N1：「三處同一來源」註解已更正（唔再話地圖提示係第三處）',
   'v20a198 C1 更正' in src and '三處同一來源' not in func_body(src, 'storyActLabel'))

# --- C2：鎖住插入行＋按段合併 ---
rp = func_body(src, 'renderProgressPane71')
ok('N2：鎖住插入行出獨立行（prog71-insert 標記）', 'prog71-insert' in rp)
ok('N2：舊 guard 已拎走（唔再 skip 鎖住插入幕）', 'if(storyActIsInsert(r.id)) return;' not in rp)
ok('N2：遠幕合併按段計（segOf198）', 'segOf198' in rp)
ok('N2：合併區間用段內首末（farLbl198），唔再寫死「–17」',
   'farLbl198' in rp and '"第 \'+loN+\'–17 幕"' not in rp)
ok('N2：得返一幕嗰陣印單幕（唔印「第 17–17 幕」）', 'loN===hiN' in rp)
ok('N2：插入行截斷遠幕段（farMerged105 重置）', 'if(storyActIsInsert(r.id)) farMerged105 = false;' in rp)
ok('N2：遠幕合併 fallback 保留（farNs 空嗰陣跳過）', 'if(!farNs.length) return;' in rp)
ok('N2：逐項揭曉閾值邏輯保留（lastDetailN71）', 'lastDetailN71 >= (r.n|0) - 1' in rp)
ok('N2：路線條件跟 token 分返電視線／電影線（唔再寫死）',
   'route_film' in func_body(src, 'prog71GateItems')
   and 'text:(tok.indexOf("route_film")>=0 ? "行電影線" : "行電視線")' in func_body(src, 'prog71GateItems'))

# --- C3：場景行唔重複路線名 ---
sp = src[src.index('const StoryPlay = (()=>{'):src.index('const StoryPlay = (()=>{') + 120000] if 'const StoryPlay = (()=>{' in src else ''
strip = func_body_braces(src, 'storySettingStripRoute198')
ok('N3：head 經 storySettingStripRoute198 出場景行', 'storySettingStripRoute198(n.setting)' in sp)
ok('N3：helper 剝走「電影線：」同「電視線：」', '.replace(/電影線：/g,"")' in strip and '.replace(/電視線：/g,"")' in strip)
ok('N3：節點 setting 資料本身唔郁（N6／N6F 原字仲有路線名）',
   n6 is not None and n6.get('setting') == '星河電視台飯堂 · 1988 年 · 電視線：角落那張桌子'
   and 'setting: "獅子山製片廠 · 1988 年 · 電影線：佈景板後面那個位置"' in src)
ok('N3：幕號行仲喺度（路線名只係由場景行拎走，唔係成個 head 拎走）',
   'sp-act191' in sp and 'storyActLabel(n.id)' in sp)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
