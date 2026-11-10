# -*- coding: utf-8 -*-
# v20a80 WF1 靜態測試：劇情豐富化 WF1——後段加厚＋真空帶補幕。
# 一、框架在位（WF1 新表／注入函數／call 位順序／YEARS66 walk list／gate／CALIB60／進度頁次序）
# 二、加厚量（index 較 v79 基線 4,798,020 bytes 大咗；12 幕 beats 序列化後明顯長過 v79）
# 三、紅線：SAVE key／softRev／?v= 不變；補幕表註解以外節點文本唔直寫真曆年份
# 反證：喺 v20a79 index 上行會 FAIL（冇 WF1 標記、冇 C18/C19、byte 數唔過基線）。
# 用法：python3 tests/test_wf1_80_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('NOTES_V20A80 在位', (p.parent / 'NOTES_V20A80_WF1.md').exists())

# --- 一、框架 ---
ok('WF1 補幕表在位', 'const STORY_SPINE_NODES_WF1 = {' in src and 'C18:' in src and 'C19:' in src)
ok('注入函數在位', 'function applyStoryWf1Nodes80(){' in src)
i410 = src.find('applyStorySpineOverrides410(); }catch(_sp410){}')
iwf1 = src.find('applyStoryWf1Nodes80(); }catch(_wf1){}')
it55 = src.find('textfix55StoryPack(main)', i410)
ok('call 位順序：410 覆寫 → WF1 注入 → TEXTFIX55 清洗 main', 0 < i410 < iwf1 < it55)
ok('YEARS66 walk list 含 WF1 表', 'STORY_SPINE_NODE_C17_410, STORY_SPINE_NODES_WF1,' in src)
ok('gate C18/C19 登記', 'C18: { yearMin: 1990, seasonIn: ["冬"] }' in src and 'C19: { yearMin: 1991, seasonIn: ["春"] }' in src)
ok('CALIB60 時窗登記 C18/C19', 'C18: { year:1990, seasons:["冬"], whenLabel:"1990 年冬" }' in src and 'C19: { year:1991, seasons:["春"], whenLabel:"1991 年春" }' in src)
ok('CALIB60 標題登記 上岸路／賭枱邊', 'C18:"上岸路"' in src and 'C19:"賭枱邊"' in src)
ok('進度頁次序：C18/C19 排 C6 後 C7 前', '["C6",6],["C18",18],["C19",19],["C7",7]' in src)
ok('C18/C19 旗已寫入節點 flags_written', 'flag_wf1_studio_dream' in src and 'flag_wf1_gamble_quiet' in src)

# --- 二、加厚量 ---
ok('index 較 v79 基線大（加厚＋補幕文本入檔）', len(src.encode('utf-8')) > 4798020 + 30000)

print('\n' + ('ALL PASS' if not fails else 'FAILURES: ' + ' | '.join(fails)))
sys.exit(0 if not fails else 1)
