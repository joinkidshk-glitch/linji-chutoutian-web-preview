# -*- coding: utf-8 -*-
# v20a81 WF2 靜態測試：感情線廣東話化＋半線差一步收尾＋彭少祺正名。
# 一、框架在位（覆寫表／apply 函數／WeakSet 守衛／call 位順序：48 藍PA → WF1 → WF2 → TEXTFIX55）
# 二、正名：彭兆基全檔歸零、彭少祺 ≥34 處、C10 顯示名 key 同步
# 三、紅線：SAVE key／softRev／?v= 不變；index 較 v80 基線增長
# 反證：喺 v20a80 index 上行會 FAIL（冇 WF2 標記、彭兆基 34 處、byte 數唔過）。
# 用法：python3 tests/test_wf2_81_static.py [path-to-index.html]
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
ok('NOTES_V20A81 在位', (p.parent / 'NOTES_V20A81_WF2.md').exists())

# --- 一、框架 ---
ok('WF2 覆寫表在位', 'const ROMANCE_WF2_OVERRIDES = {' in src and 'R_hiu_meet' in src and 'R_tang_ending' in src)
ok('apply 函數在位', 'function applyRomanceWf2Overrides81(){' in src)
ok('冪等守衛 WeakSet 在位', 'const WF2_APPLIED81 = new WeakSet();' in src)
i48 = src.find('applyStorySpineOverrides48(); }catch(_sp48){}')
iwf1 = src.find('applyStoryWf1Nodes80(); }catch(_wf1){}')
iwf2 = src.find('applyRomanceWf2Overrides81(); }catch(_wf2){}')
it55 = src.find('textfix55StoryPack(rom1)', iwf1)
ok('call 位順序：48 藍PA → WF1 → WF2 → TEXTFIX55 rom1', 0 < i48 < iwf1 < iwf2 < it55)
ok('覆寫表定義早過 call 位', 0 < src.find('const ROMANCE_WF2_OVERRIDES') < iwf2)

# --- 二、彭少祺正名 ---
ok('彭兆基全檔歸零', src.count('彭兆基') == 0)
ok('彭少祺 ≥34 處（實 %d）' % src.count('彭少祺'), src.count('彭少祺') >= 34)
ok('speaker→sprite 對照 key 已同步正名', '"彭少祺": null' in src or '"彭少祺":' in src)

# --- 三、增長 ---
ok('index 較 v80 基線大（覆寫表入檔）', len(src.encode('utf-8')) > 4854789 + 30000)

print('\n' + ('ALL PASS' if not fails else 'FAILURES: ' + ' | '.join(fails)))
sys.exit(0 if not fails else 1)
