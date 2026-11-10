# -*- coding: utf-8 -*-
# v20a74 TARGET74 靜態測試：主攻目標（目標數值）功能成個移除（用戶 2026-11-10 16:06 拍板）。
# 移除範圍：picker 設定掣（data-gtgt）、目標預設分組、地點 sheet ▲標示、
# prefs 讀寫函數；選擇器預設改用 session 上次睇開嗰組（冇就演技）。
# 反證：喺 v20a73 index 上行會 FAIL（嗰陣成套功能仲喺度）。
# 用法：python3 tests/test_target74_static.py [path-to-index.html]
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
ok('TARGET74 標記在檔', 'TARGET74' in src)

# --- 功能標識全清 ---
ok('全檔冇「主攻」字樣', '主攻' not in src)
ok('冇目標讀寫函數（ux68TargetStat／ux68SetTargetStat）',
   'function ux68TargetStat' not in src and 'function ux68SetTargetStat' not in src and 'ux68TargetStat' not in src)
ok('冇目標標示函數／樣式（ux68ApplyTargetBadges／ux68-tgt）',
   'ux68ApplyTargetBadges' not in src and 'ux68-tgt' not in src)
ok('冇設定掣部件（data-gtgt／guide68-tgtbtn／guide68-tgtrow）',
   'data-gtgt' not in src and 'guide68-tgtbtn' not in src and 'guide68-tgtrow' not in src)
ok('冇 chip「目標」標記（class="gt"）', 'class="gt"' not in src and "class='gt'" not in src)

# --- picker 本體／handler 冇目標殘留 ---
_i = src.find('function train71PickerHtml')
_j = src.find('function train71RenderPanel')
picker_block = src[_i:_j] if 0 <= _i < _j else ''
ok('picker 本體抽取到', bool(picker_block))
ok('picker 本體冇目標引用', 'TargetStat' not in picker_block and 'gtgt' not in picker_block)

_h = src.find('function train71HandleClick')
_w = src.find('(function train71WirePicker', _h)
handler_block = src[_h:_w] if 0 <= _h < _w else ''
ok('handler 抽取到', bool(handler_block))
ok('handler 冇 gtgt 分支', 'data-gtgt' not in handler_block and 'gtgt' not in handler_block)

# --- 預設分組新行為 ---
_t = src.find('function train71Stat')
_stat_block = src[_t:src.find('}', _t) + 1] if _t >= 0 else ''
ok('train71Stat 抽取到', bool(_stat_block))
ok('train71Stat 冇目標分支、fallback 演技', 'TargetStat' not in _stat_block and '"acting"' in _stat_block
   and 'ux68GuideStat' in _stat_block)

# --- organizer 其餘行為冇誤傷 ---
ok('organizer 本體保留（ux68OrganizeLocSheet／分組／摺疊）',
   'function ux68OrganizeLocSheet' in src and 'ux68-ghead' in src and 'ux68-locked-toggle' in src)
ok('organizer 冇再呼叫目標標示', 'ApplyTargetBadges' not in src)
ok('選擇器 v73 三分流保留（train73CourseKind／train73EnrollNote）',
   'function train73CourseKind' in src and 'function train73EnrollNote' in src)
ok('session 組別狀態保留（ux68GuideStat）', 'let ux68GuideStat' in src)
ok('增益衍生保留（ux68ParseGainTable）', 'function ux68ParseGainTable' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
