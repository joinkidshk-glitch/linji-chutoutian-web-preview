# v20a194 頒獎禮拆 soft 閘・static tests：
# 1. 閘已拆：queueAwardsOnSeasonWindow 唔再有 `if(!awardsSoftOn() && !opts.force) return [];`，
#    成個 queue 函數體唔再提 awardsSoftOn；awardsSoftOn() 本身保留、語義唔郁。
# 2. pack meta tip 行覆寫層：磁碟上兩個 pack 繼續 ≠PASS（直改 content JSON 係紅線，
#    見 aud91fix122／124／gigreq110），載入嗰陣 awards194ApplyMetaTip 先將 runtime
#    meta 改做 PASS（v188 獎項名同一模式）；門檻／獎項／內容一字唔郁。
# 3. awardsCheck() 加 live_queue 探針、return softStatus:"PASS"；全檔得呢一處 PASS。
# 4. 其他 softStatus 讀者唔郁：tutorial overlay 三處、postShoot／報紙／freeplay／休息片
#    各自 check 繼續回 softStatus:"≠PASS"（嗰啲係成個 soft 框架嘅，唔關頒獎禮事）。
# 5. 唔郁嘅嘢：SAVE key、softRev s107、?v=v20a10、頒獎禮 header 以外嘅 "no tip LIVE"
#    （休息片嗰句）、C17 awardResolved 閘。
# 反證: run against pristine main 2374637 index -> v194 標記未入 -> FAIL（唔 crash）。
# 用法：python3 tests/test_awards194_static.py [path-to-index.html]
import json
import os
import re
import sys

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
base = os.path.dirname(os.path.abspath(idx_path))
src = open(idx_path, encoding='utf-8').read()
fails = []


def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)


def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0:
        return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{':
            depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    return ''


# --- 反證守衛：v194 標記唔在就乾淨 FAIL，唔好逐項誤判 ---
NEED194 = ['v20a194：頒獎禮拆 soft 閘', 'live_queue', 'softStatus:"PASS"', 'awards194ApplyMetaTip']
missing194 = [s for s in NEED194 if s not in src]
if missing194:
    for m in missing194:
        chk('反證：%s 唔存在（pristine main 預期，v194 未入）' % m, False)
    print('\nFAILED: %d' % len(fails))
    sys.exit(1)

# --- 1. 閘已拆，awardsSoftOn() 保留 ---
chk('1：閘行唔見咗', 'if(!awardsSoftOn() && !opts.force) return [];' not in src)
queue_fn = slice_fn('queueAwardsOnSeasonWindow')
queue_code = re.sub(r'/\*.*?\*/', '', queue_fn, flags=re.S)
chk('1：queue 函數體（除註解外）唔再提 awardsSoftOn', 'awardsSoftOn' not in queue_code)
chk('1：queue 函數仲在位', 'function queueAwardsOnSeasonWindow(opts)' in src)
soft_fn = slice_fn('awardsSoftOn')
chk('1：awardsSoftOn() 定義保留', 'function awardsSoftOn()' in src)
chk('1：awardsSoftOn() 語義唔郁（仲問 BehaviorGate 旗標）',
    'featureFlag_softBehaviorGatePreview' in soft_fn)
chk('1：朝早鏈照樣 call queue（presentPendingAward 唔郁）',
    'queueAwardsOnSeasonWindow();' in slice_fn('presentPendingAward'))
chk('1：頒獎禮 header 改做 tipped LIVE',
    'AWARDS CEREMONY — four medium tracks; v20a194 tipped LIVE' in src)

# --- 2. pack meta tip 行覆寫層（唔直改 content JSON——repo 紅線） ---
schema = json.load(open(os.path.join(base, 'content', 'SCHEMA_AWARDS_CEREMONY_v1.json'), encoding='utf-8'))
stub = json.load(open(os.path.join(base, 'content', 'STUB_AWARDS_CEREMONY_v1.json'), encoding='utf-8'))
chk('2：磁碟上 schema meta 仲係 ≠PASS（直改 content JSON 係紅線，見 aud91fix122／124）',
    schema['meta']['softStatus'] == '≠PASS')
chk('2：磁碟上 stub meta 仲係 ≠PASS（覆寫層先改 runtime）',
    stub['meta']['softStatus'] == '≠PASS')
chk('2：覆寫函數 awards194ApplyMetaTip 在位', 'function awards194ApplyMetaTip(FW)' in src)
tip_fn = slice_fn('awards194ApplyMetaTip')
chk('2：覆寫將兩個 pack meta 改做 PASS', tip_fn.count('softStatus = "PASS"') == 2)
chk('2：覆寫改埋 note（schema 嗰句 no tip LIVE／stub 嗰句 Soft≠PASS）',
    'v20a194: tipped LIVE' in tip_fn)
tip_head = src[max(0, src.find('function awards194ApplyMetaTip(FW)') - 900):src.find('function awards194ApplyMetaTip(FW)')]
chk('2：覆寫註解講明紅線（唔直改 content JSON）',
    'aud91fix122' in tip_head and 'content/*.json' in tip_head)
chk('2：loadFreeplayFramework 喺 awards188 覆寫之後呼叫 meta tip',
    'awards194ApplyMetaTip(FREEPLAY_FW)' in src and
    src.find('awards194ApplyMetaTip(FREEPLAY_FW)') > src.find('awards188ApplyNpOverlay(FREEPLAY_FW);'))
EXP = [('award_harbour_ad', '春', 6, ['廣告']),
       ('award_golddisc_music', '夏', 16, ['唱片通告']),
       ('award_harbour_film', '秋', 28, ['電影']),
       ('award_singho_tv', '冬', 40, ['電視劇', '綜藝'])]
got = [(c['id'], c.get('season'), c.get('weekMinSoft'), c.get('matchTypes'))
       for c in schema['ceremonies']]
chk('2：schema 4 場 id／季節／weekMinSoft／matchTypes 一字唔郁', got == EXP)
chk('2：stub 4 場 id／displayName 唔郁',
    [(c['id'], c.get('displayName')) for c in stub['ceremonies']] ==
    [('award_harbour_ad', '維港街招・年度廣告賞'),
     ('award_golddisc_music', '星河金碟夜'),
     ('award_harbour_film', '維港影藝獎'),
     ('award_singho_tv', '星河台慶・年度頒獎夜')])

# --- 3. awardsCheck 探針＋PASS ---
chk_fn = slice_fn('awardsCheck')
chk('3：awardsCheck 有 live_queue 探針', 'live_queue' in chk_fn)
chk('3：awardsCheck 有 meta_tip 核實', 'meta_tip' in chk_fn)
chk('3：探針用 forceCeremonyId 跳季節唔跳旗標',
    'forceCeremonyId:"award_harbour_ad"' in chk_fn)
chk('3：探針有還原（snapshot／finally）', 'finally' in chk_fn and 'snapPending' in chk_fn)
chk('3：awardsCheck return softStatus:"PASS"',
    'softStatus:"PASS"' in chk_fn)
chk('3：全檔 softStatus:"PASS" 恰好 1 處（淨係 awardsCheck）',
    src.count('softStatus:"PASS"') == 1)
chk('3：全檔 softStatus:"≠PASS" 仲有 6 處（其他 check 嘅 return 唔郁；'
    '另有 tutorial overlay 三處 !== 寫法，見第 4 項）',
    src.count('softStatus:"≠PASS"') == 6)

# --- 4. 其他 softStatus 讀者唔郁 ---
chk('4：tutorial overlay 讀 softStatus 三處仲在',
    src.count('pack.meta.softStatus!=="≠PASS"') == 3)
chk('4：postShootRewardCheck 繼續回 ≠PASS',
    'softStatus:"≠PASS"' in slice_fn('postShootRewardCheck'))
chk('4：newspaperCheck 繼續回 ≠PASS',
    'softStatus:"≠PASS"' in slice_fn('newspaperCheck'))
chk('4：freeplay check 繼續回 ≠PASS',
    'softStatus:"≠PASS"' in src[src.find('awardsCeremony: typeof queueAwardsOnSeasonWindow') - 3000:
                                  src.find('awardsCeremony: typeof queueAwardsOnSeasonWindow')])
chk('4：restSleepFxCheck 繼續回 ≠PASS',
    'softStatus:"≠PASS"' in slice_fn('restSleepFxCheck'))

# --- 5. 唔郁嘅嘢 ---
chk('5：SAVE key 唔郁', 'starVolunteer_map_v19w' in src)
chk('5：softRev s107 唔郁', 'softRev:"s107"' in src)
chk('5：awardsCheck version 仲係 v20a10', 'version:"v20a10"' in chk_fn)
chk('5：休息片 "no tip LIVE" 嗰句仲在（唔關頒獎禮事）',
    'REST SLEEP FX — 8-bit clip inside rest day-end panel; Soft≠PASS; no tip LIVE' in src)
chk('5：C17 awardResolved 閘唔郁',
    'awardResolved: { ceremonyId: "award_singho_tv", year: 1992 }' in src)

print('\nFAILED: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
