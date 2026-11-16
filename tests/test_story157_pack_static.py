# -*- coding: utf-8 -*-
# v20a157 C1-N5 pack 重寫靜態測試（pack 分檔組）。
# 落點：content/story_detail_n1_to_n17.json nodes[0-4]；nodes[5:]（N6–N19）一字唔郁（v233 起含 N18／N19）。
# 反證：喺 pristine main（e08a070／v148）pack 上行會 FAIL（標題／beats 數／notes 全唔同），唔 crash。
# 用法：python3 tests/test_story157_pack_static.py [path-to-pack-json]
import hashlib
import json
import re
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'content' / 'story_detail_n1_to_n17.json'
pack = json.loads(p.read_text(encoding='utf-8'))
fails = []


def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)


nodes = pack.get('nodes', [])
ok('pack 有 19 個 nodes', len(nodes) == 19)  # v233 RW-2：N18／N19 新增（內嵌 WF1 表同步入 pack）
ok('pack version 不變', pack.get('version') == '1.2.8')
ok('nodes[0-4] 係 N1-N5', [n.get('id') for n in nodes[:5]] == ['N1', 'N2', 'N3', 'N4', 'N5'])

# --- nodes[5-16] 死版一字唔郁（pristine main e08a070 嘅 sha；v217 語言審核改咗 N6+ 節點文字，sha 重算；
#      v20a210 編號統一 C→N 純改名，79 行逐行核實全部只係 C<n>→N<m> 對照改名，sha 再重算；
#      v20a231 RW-1 逐句重寫 N6–N9（87 處 JSON 改動，N10–N17 一字未郁），sha 再重算；
#      v20a233 RW-2 逐句重寫 N6–N19 內嵌表＋同步返 JSON（N6–N17 取代死 pack 節點、新增 N18／N19），sha 再重算；
#      v20a235 結局唔畀玩家揀（N17 synopsis 六意向→走定留＋flags_written 刪三死旗；beats 一字未郁），sha 再重算） ---
tail = json.dumps(nodes[5:], sort_keys=True, ensure_ascii=False)
ok('nodes[5-16] 同 pristine 一致',
   hashlib.sha256(tail.encode('utf-8')).hexdigest()
   == '7adfea57abd947f6c4569cf7fed805028e4b66a85cfc249b211ec3b652b11e99')

# --- 標題／setting／synopsis 按設計 ---
ok('標題 N1-N5 按設計（N5 用 TEXTFIX55 淨化形「辣手問題」；v221 書面語改寫：N1「冇價」→「無價」、N5「嘅」→「的」）',
   [n.get('title') for n in nodes[:5]]
   == ['第一日：無價', '後巷聽古', '高俊傑搶鏡', '何生攤記數簿', '采兒的辣手問題'])
ok('setting 按設計',
   [n.get('setting') for n in nodes[:5]]
   == ['何生事務所', '片場後巷／附近茶餐廳', '星河片場廠景／休息角／茶水間',
       '何生事務所', '片場休息角小訪桌（摺椅、筆記本），秋日午後'])
ok('synopsis 係設計首段（唔含「現行…」DEV 段落／N-code）',
   all('現行' not in n.get('synopsis', '') for n in nodes[:5])
   and '上一幕教他「冇價」' in nodes[1].get('synopsis', '')
   and '第一天出現過的記數簿' in nodes[3].get('synopsis', ''))

# --- beats：設計 Beat 1-5 按講者分拆（設計 script beat 8/8/8/8/9；引擎 beat 數見 manifest） ---
ok('beats 數 N1-N5', [len(n['beats']) for n in nodes[:5]] == [16, 9, 10, 11, 9])
ok('beat 行數 N1-N5', [sum(len(b['lines']) for b in n['beats']) for n in nodes[:5]]
   == [19, 12, 12, 12, 11])
ALLOWED_SPEAKERS = {'系統', '何生', '阿偉', '張子駿', '老臨記', '副導', '高俊傑', '周采兒'}
ALLOWED_EMOTIONS = {'neutral', 'calm', 'tense', 'angry', 'warm', 'tired',
                    'smirk', 'worried', 'soft', 'firm'}
for n in nodes[:5]:
    beats = n['beats']
    ok('%s beats 唔空、第一個 beat 唔空' % n['id'],
       len(beats) > 0 and len(beats[0].get('lines', [])) > 0)
    ok('%s 每個 beat 單一講者、講者喺 SP_SPEAKER_LEGACY、行唔空' % n['id'],
       all(b.get('speaker') in ALLOWED_SPEAKERS and b.get('lines')
           and all(isinstance(x, str) and x.strip() for x in b['lines'])
           for b in beats))
    ok('%s kind 對應講者（系統=system、阿偉=player、其餘=npc）' % n['id'],
       all((b['kind'] == 'system') == (b['speaker'] == '系統') for b in beats)
       and all((b['kind'] == 'player') == (b['speaker'] == '阿偉')
               for b in beats if b['speaker'] != '系統'))
    ok('%s emotion（如有）只用十個值' % n['id'],
       all(b.get('emotion') in ALLOWED_EMOTIONS for b in beats if b.get('emotion')))
    ok('%s beats 無年份 1990／無 1989／無 N-code／無禁用詞' % n['id'],
       not re.search(r'1990 年|1989|送命題|星河電視城|聲量|周刊', json.dumps(beats, ensure_ascii=False))
       and 'N1 ' not in json.dumps(beats, ensure_ascii=False))

# --- N1 必守 ---
c1 = nodes[0]
ok('N1 locId 係 agency_ho', c1.get('locId') == 'agency_ho')
ok('N1 phase P1', c1.get('phase') == 'P1')
ok('N1 playerOffer 非空', bool((c1.get('playerOffer') or '').strip()))
ok('N1 openConditions []', c1.get('openConditions') == [])
ok('N1 pacing.weekMin 1', (c1.get('pacing') or {}).get('weekMin') == 1)
ok('N1 講者只用何生／阿偉／張子駿／系統',
   {b['speaker'] for b in c1['beats']} <= {'何生', '阿偉', '張子駿', '系統'})

# --- N2-N5 閘唔郁 ---
GATES = {
    'N2': (['N1', 'week_min:4', 'days_after_prev:1'],
           {'weekMin': 4, 'minDaysAfterPrev': 1, 'when': '1988春 / W4-5', 'prevMain': 'N1'}),
    'N3': (['N2', 'week_min:6', 'days_after_prev:1'],
           {'weekMin': 6, 'minDaysAfterPrev': 1, 'when': '1988春 / W6-8', 'prevMain': 'N2'}),
    'N4': (['N3', 'week_min:8', 'days_after_prev:1'],
           {'weekMin': 8, 'minDaysAfterPrev': 1, 'when': '1988春 / W8-9', 'prevMain': 'N3'}),
    'N5': (['N4', 'week_min:9', 'days_after_prev:1'],
           {'weekMin': 9, 'minDaysAfterPrev': 1, 'when': '1988秋 / W9-10', 'prevMain': 'N4'}),
}
for n in nodes[1:5]:
    oc, pacing = GATES[n['id']]
    ok('%s openConditions 照舊' % n['id'], n.get('openConditions') == oc)
    ok('%s pacing 照舊' % n['id'], n.get('pacing') == pacing)
ok('N5 openConditionsAny／thresholds 照舊',
   nodes[4].get('openConditionsAny') == ['rel_choi_threshold', 'season_1988_autumn', 'season_1988_winter']
   and (nodes[4].get('thresholds') or {}).get('rel_choi_threshold') == 2)

# --- choices：id／旗／stats／tags／ripple 全部保留現行原值 ---
EXPECTED = {
    'N1_a': (['route_tv'], {}, [], {'tag': '電視城起步', 'creditDelta': 0, 'rivalAttitude': 'neutral', 'debtDelta': 0, 'stressDelta': 0, 'healthDelta': 0, 'bondDepth': 'initial', 'intelShare': 'low', 'mapTilt': '電視城／動作組', 'statTilt': '穩紮根基偏訓練'}),
    'N1_b': (['route_film'], {}, [], {'tag': '片場散工起步', 'creditDelta': 0, 'rivalAttitude': 'neutral', 'debtDelta': 0, 'stressDelta': 0, 'healthDelta': 0, 'bondDepth': 'initial', 'intelShare': 'low', 'mapTilt': '電影片場散工', 'statTilt': '現金快、人脈易散'}),
    'N2_a': (['flag_network_stay'], {}, ['片場老油條'], {'tag': '片場老油條', 'stressDelta': 1}),
    'N2_b': (['flag_hustle_board'], {}, ['電視城乖仔'], {'tag': '電視城乖仔', 'stressDelta': -1}),
    'N3_a': (['rival_gao_hard'], {}, [], {'creditDelta': -1, 'rivalAttitude': '高俊傑記仇，往後處處針對', 'stressDelta': 2}),
    'N3_b': (['rival_gao_endure'], {}, [], {'creditDelta': 1, 'rivalAttitude': '高俊傑覺得你好蝦，變本加厲', 'stressDelta': 3}),
    'N4_a': (['flag_refuse_gig_with_ho'], {}, [], {'debtDelta': 1, 'creditDelta': -1}),
    'N4_b': (['flag_take_harsh_gig'], {}, ['捱得'], {'tag': '捱得', 'stressDelta': 8, 'healthDelta': -5}),
    'N5_a': (['choi_honest'], {}, [], {'bondDepth': '坦誠加深', 'intelShare': '互相分享近況級', 'stressDelta': 1}),
    'N5_b': (['choi_spin'], {}, [], {'bondDepth': '表面和氣', 'intelShare': '只換包裝情報'}),
    'N5_c': (['choi_dodge'], {}, [], {'bondDepth': '疏離一截', 'intelShare': '情報共享降級', 'stressDelta': -1}),
}
ok('choices 數 N1-N5', [len(n['choices']) for n in nodes[:5]] == [2, 2, 2, 2, 3])
ok('choice id 保留', [c['id'] for n in nodes[:5] for c in n['choices']]
   == ['N1_a', 'N1_b', 'N2_a', 'N2_b', 'N3_a', 'N3_b', 'N4_a', 'N4_b', 'N5_a', 'N5_b', 'N5_c'])
for n in nodes[:5]:
    for c in n['choices']:
        flags, stats, tags, ripple = EXPECTED[c['id']]
        eff = c.get('effects', {})
        ok('%s flags 保留原名' % c['id'], eff.get('flags') == flags)
        ok('%s stats 保留（S1 唔做，N5_a 唔加 rel_choi）' % c['id'], eff.get('stats') == stats)
        ok('%s tags 保留' % c['id'], eff.get('tags') == tags)
        ok('%s ripple 保留現行執行值' % c['id'], eff.get('ripple') == ripple)
        notes = eff.get('notes', '')
        ok('%s notes 係單一字串、非空、唔寫數字、唔含 flag_/rel_ 標記' % c['id'],
           isinstance(notes, str) and bool(notes.strip())
           and not re.search(r'[0-9±]', notes)
           and 'flag_' not in notes and 'rel_' not in notes
           and notes.strip().endswith('。'))
        rb = c.get('resultBeats', [])
        ok('%s resultBeats 有料（設計 6x＋Beat 7 收尾）' % c['id'],
           len(rb) >= 4 and all(r.get('lines') for r in rb))

# --- resultBeats 數＋收尾 Beat 7 在場 ---
ok('resultBeats beat 數',
   [[len(c['resultBeats']) for c in n['choices']] for n in nodes[:5]]
   == [[6, 5], [4, 4], [4, 4], [4, 4], [4, 4, 4]])
ok('resultBeats 行數',
   [[sum(len(r['lines']) for r in c['resultBeats']) for c in n['choices']] for n in nodes[:5]]
   == [[7, 6], [6, 5], [5, 5], [5, 5], [5, 5, 5]])
CLOSING = {'N1': '保母車', 'N2': '坐在摺凳上的那個人', 'N3': '報紙會連載',
           'N4': '這一行人人都有本數', 'N5': '週刊'}
for n in nodes[:5]:
    ok('%s 每個 choice 嘅 resultBeats 尾段有 Beat 7 收尾' % n['id'],
       all(CLOSING[n['id']] in json.dumps(c['resultBeats'], ensure_ascii=False)
           for c in n['choices']))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
