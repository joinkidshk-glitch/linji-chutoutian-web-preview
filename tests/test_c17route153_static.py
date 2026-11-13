# -*- coding: utf-8 -*-
# v20a153 靜態測試：v136 review A1＋B2＋B3。
# A1：C17 路由改返星河電視台（tvb_longmen）——soft gate 載入嗰陣正規化，唔改 content pack JSON。
# B2：C17 開場兩句旁白由何生企台——spDlgPairIds 開場旁白預告下一位講者。
# B3：進度頁次序（v20a191 改版：插入幕跟播次序排喺 C6 之後，唔再排尾扮第 18／19／20 幕；內部 n 保留）。
# 反證：喺 pristine main（e08a070／v148）index 上行，A1／B2／B3 新斷言要乾淨 FAIL（唔 crash）；
#      其餘基線斷言（SAVE／softRev／?v=／when 1990冬／410 locId／slots 源頭）喺 pristine 一樣 PASS；
#      410 setting／synopsis／lockedHint 三句斷言跟 v157 版措辭，喺 e08a070 會 FAIL（措辭係 v157 改嘅，唔係 v153）。
# 用法：python3 tests/test_c17route153_static.py [path-to-index.html]
import json
import re
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
root = p.parent
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


# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('410 陷阱未郁：when 仲係 1990冬', 'when: "1990冬"' in src)
ok('410 陷阱未郁：setting／synopsis 仲係 1990 年冬末',
   # v157 重寫改咗 410措辭（後台化妝間→會議室；「台慶頒獎禮之後」→「頒獎禮之後嗰晚」），
   # 斷言跟返 v157 版措辭；v153 冇郁過呢個節點。
   'setting: "星河電視台會議室；1990 年冬末，冬台慶啱啱完' in src
   and 'synopsis: "1990 年冬末，頒獎禮之後嗰晚，星河電視台會議室。何生攤開流程表' in src)
ok('410 陷阱未郁：lockedHint 仲係 1990 年冬',
   'lockedHint: "1990 年冬、台慶之後先到呢一晚。未到就照常跑通告；到咗去星河電視台會議室。' in src)
ok('410 locId／STORY_LOC_SOFT C17 仲係 tvb_longmen',
   'locId: "tvb_longmen"' in src and 'C17: "tvb_longmen"' in src)
slots_path = root / 'content' / 'STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json'
try:
    slots = json.loads(slots_path.read_text(encoding='utf-8'))
    c17slot = next((n for n in slots['nodes'] if n.get('beatId') == 'C17'), None)
    ok('slots 源頭未郁（修法喺 code 唔喺 pack）：C17 slot 仲係 agency_ho／cafe_cha',
       c17slot is not None and c17slot.get('locId') == 'agency_ho'
       and (c17slot.get('trigger') or {}).get('locIdAny') == ['agency_ho', 'cafe_cha'])
except Exception as e:
    ok('slots 源頭未郁（修法喺 code 唔喺 pack）：C17 slot 仲係 agency_ho／cafe_cha', False)
    print('  (slots read error: %s)' % e)

# --- A1：soft gate C17 正規化返 tvb_longmen ---
ok('A1：healC17Loc 喺 BehaviorGate 入面定義', 'function healC17Loc(node)' in src)
ok('A1：healC17Loc 寫死 tvb_longmen（locId＋trigger.locIdAny）',
   'held.locId = "tvb_longmen"' in src and 'held.trigger.locIdAny = ["tvb_longmen"]' in src)
ok('A1：applyFreeplaySlots（slots 接線 choke point）有呼 healC17Loc',
   'healC17Loc("C17")' in func_body(src, 'applyFreeplaySlots'))
ok('A1：evalTrigger_AND_softRumor 有呼 healC17Loc',
   'healC17Loc(id)' in func_body(src, 'evalTrigger_AND_softRumor'))
ok('A1：softCanonC17Loc 定義＋強制 tvb_longmen', 'function softCanonC17Loc(node)' in src
   and 'node.locId = "tvb_longmen"' in src)
ok('A1：故事節點 overlay 唔抄 slot.locId（C17 分支有防禦性正規化）',
   'if(id==="C17")' in src and 'softCanonC17Loc(storyNode)' in src)
ok('A1：index.html 冇殘留 C17 agency／cafe 雙門字面',
   '"agency_ho", "cafe_cha"' not in src)
ok('A1：WF4 入場攔截跟埋主線待播優先（enc79StoryPendingAt guard）',
   (lambda _m: bool(_m) and 'enc79StoryPendingAt(locId)' in src[_m.start():_m.start() + 2000])(
       re.search(r'function wf4TryLocEvent\(locId\)', src)))

# --- B2：開場旁白預告下一位講者 ---
pair_body = func_body(src, 'spDlgPairIds')
ok('B2：spDlgPairIds 開場旁白（order 空）向前搵下一位講者',
   'if(!order.length)' in pair_body and 'cur.beatIdx+1' in pair_body
   and 'spIsSystemBeat(nb)' in pair_body)
ok('B2：開場旁白只取下一位（唔預告再後嘅人）', 'dlg119DedupePair([nid])' in pair_body)
ok('B2：舊註解「開場旁白唔郁，繼續冇人」已拎走', '開場旁白（system）唔郁，繼續冇人' not in src)
ok('B2：render 旁白註解已更新（開場旁白由 B2 預告下一位講者）',
   '由 v20a153 B2 預告下一位講者企台' in src)

# --- B3：進度頁 1–20 順序（v20a191 改版：插入幕唔再排尾扮第 18／19／20 幕） ---
# v191 顯示次序跟 ORDER165（C6、C6F、C18、C19、C7–C17）；內部 n 保留
# （C6F=20、C18=18、C19=19）供 far-merge／逐項揭曉邏輯用，行為同 v153 一致。
# 反證更新：喺 v153 index 上行，新 B3 斷言要乾淨 FAIL（舊排法 C17、C18、C19、C6F）。
m = re.search(r'const order71 = \[(.*?)\];', src, re.S)
pairs = re.findall(r'\[\s*"([^"]+)"\s*,\s*(\d+)\s*\]', m.group(1)) if m else []
ok('B3：order71 抽到 20 項', len(pairs) == 20)
ok('B3：顯示次序跟播次序（C6、C6F、C18、C19、C7–C17）',
   [i for i, _ in pairs] == ['C%d' % n for n in range(1, 7)] + ['C6F', 'C18', 'C19'] + ['C%d' % n for n in range(7, 18)])
ok('B3：內部 n 保留 1–20（供 far-merge／逐項邏輯用，唔係顯示幕號）',
   sorted(int(n) for _, n in pairs) == list(range(1, 21)))
ok('B3：插入幕逐項跟幕號唔跟行 index（lastDetailN71 規則）',
   'lastDetailN71' in src and 'lastDetailN71 >= (r.n|0) - 1' in src)
ok('B3：舊行-index 規則已拎走', 'lastDetailIdx71' not in src)
ok('B3：遠幕合併行唔會印倒轉區間（farNs 空嗰陣跳過）', 'if(!farNs.length) return;' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
