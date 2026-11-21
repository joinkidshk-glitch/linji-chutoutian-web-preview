# v20a361 P1 兩項平衡修復靜態釘：A 頒獎天花板（ad_lead/music_lead/variety_host_lead）B 結局可達性
# （合約信用＋E3/E5 提前＋floor 140＋F2 豁免＋負標籤預警）。
# 內容錨點（唔釘行號，免漂移）；行為驗證見 qa361/qa361_harness.js（36 項，真引擎/真函數）。
import json, re, sys

src = open('index.html', encoding='utf-8').read()
pack = json.load(open('content/gigs_new.json', encoding='utf-8'))
gigs = {g['id']: g for g in pack['gigs']}
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    m = re.search(r'function ' + name + r'\s*\(', src)
    if not m:
        return ''
    i = src.index('{', m.start())
    d, j = 0, i
    while j < len(src):
        if src[j] == '{':
            d += 1
        elif src[j] == '}':
            d -= 1
            if d == 0:
                break
        j += 1
    return src[m.start():j + 1]

# A1：ROLE_Q 新擔正級 q=0.78；贏線冇郁
rq = src[src.index('const AWARDS62_ROLE_Q'):src.index('const AWARDS62_ROLE_Q') + 1200]
chk('A1 ROLE_Q ad_lead/music_lead/variety_host_lead 0.78 在位',
    'ad_lead: 0.78' in rq and 'music_lead: 0.78' in rq and 'variety_host_lead: 0.78' in rq)
chk('A1 贏線 AWARDS62_WIN_LINE=0.875 冇郁', 'const AWARDS62_WIN_LINE = 0.875;' in src)

# A2：ROLE_SCALE_BAND＋擔正表＋end229IsLead 同步
band = src[src.index('const ROLE_SCALE_BAND'):src.index('const ROLE_SCALE_BAND') + 1200]
chk('A2 ROLE_SCALE_BAND 三新 scale 在位',
    'ad_lead:[1,2]' in band and 'music_lead:[6,14]' in band and 'variety_host_lead:[1,3]' in band)
chk('A2 AWARDS65/END95/PRESS94 擔正表含 variety_host_lead',
    src.count('variety_host_lead:1') + src.count('variety_host_lead: 1') >= 3)
islead = slice_fn('end229IsLead')
chk('A2 end229IsLead 認三新 scale',
    'music_lead' in islead and 'ad_lead' in islead and 'variety_host_lead' in islead)

# A3：通告庫轉換＋新增（326 張）
chk('A3 通告庫 330 張', len(pack['gigs']) == 330)  # v372 +4（ad/host 供應 2→3）
for gid, sc in [('gig_1992_ad_107', 'ad_lead'), ('gig_1992_ad_203', 'ad_lead'),
                ('gig_1991_ad_109', 'ad_lead'), ('gig_1991_ad_110', 'ad_lead'),
                ('gig_1991_variety_103', 'variety_host_lead'), ('gig_1991_variety_110', 'variety_host_lead'),
                ('gig_1992_variety_102', 'variety_host_lead'), ('gig_1992_variety_106', 'variety_host_lead'),
                ('gig_1990_rec_110', 'music_lead'), ('gig_1990_rec_303', 'music_lead'),
                ('gig_1991_rec_107', 'music_lead'), ('gig_1991_rec_108', 'music_lead'),
                ('gig_1992_rec_105', 'music_lead'), ('gig_1992_rec_109', 'music_lead')]:
    chk('A3 ' + gid + '=' + sc, gigs.get(gid, {}).get('roleScale') == sc)
chk('A3 新廣告通告有 product/brand',
    all(gigs[g].get('product') and gigs[g].get('brand') for g in ['gig_1991_ad_109', 'gig_1991_ad_110']))

# B1：合約信用（CFG／函數／殺青 hook／舊檔回填）
chk('B1 CONTRACT_CREDIT361_CFG 在位（+1/+1/季4/生涯36）',
    'perWrap: 1' in src and 'highTierBonus: 1' in src and 'quarterCap: 4' in src and 'lifetimeCap: 36' in src)
cc = slice_fn('contractCredit361OnWrap')
chk('B1 contractCredit361OnWrap 寫 delta＋雙上限',
    'industryCreditDelta' in cc and 'quarterCap' in cc and 'lifetimeCap' in cc)
chk('B1 殺青 hook 在位（end95AddWrap 旁）',
    'contractCredit361OnWrap(S, _g95, S.dayIndex|0)' in src)
chk('B1 舊檔回填 contractCredit361Backfill＋normalize 呼叫',
    'function contractCredit361Backfill(' in src and 'contractCredit361Backfill(o)' in src)

# B2：E3/E5 提前＋credit>fame 守門（次序：ID→E3→E5→CR→E2）
res = slice_fn('resolveEnding410')
i_id = res.index('career = "ID"')
i_e3 = res.index('career = "E3"')
i_e5 = res.index('career = "E5"')
i_cr = res.index('career = "CR"')
i_e2 = res.index('career = "E2"')
chk('B2 判定次序 ID→E3→E5→CR→E2', i_id < i_e3 < i_e5 < i_cr < i_e2)
chk('B2 E3/E5 有 credit>fame 守門',
    'credit>fame && endingE3Eligible410(s)' in res and 'credit>fame && (favor.settled + favor.creditsHeld)>=T.e5FavorTotal' in res)

# B3：floor 140／warnLine 180＋F2 豁免 helper
chk('B3 CONSEQ61_REVIEWS 1992 floor 140／warnLine 180',
    '1992: { floor: 140, warnLine: 180, boundaryWeek: 156 }' in src)
ex = slice_fn('ending361FloorExempt')
chk('B3 ending361FloorExempt 豁免 E6/E4/E3/E5',
    all(x in ex for x in ['"E6"', '"E4"', '"E3"', '"E5"']))
chk('B3 F2 覆寫改行 ending361FloorExempt', '!ending361FloorExempt(res.career)' in src)

# B4：負標籤即時預警＋gaps95 交代
ntw = slice_fn('negTagWarn361')
chk('B4 negTagWarn361 兩段文案在位',
    '這是負面印記，會影響結局' in ntw and '負面印記已有兩個' in ntw)
ac = slice_fn('applyCastingTags')
chk('B4 applyCastingTags 新增後呼叫 negTagWarn361', 'negTagWarn361(added)' in ac)
bg = slice_fn('end95BuildGaps')
chk('B4 gaps95 負標籤交代行在位', '負面印記，你身上有' in bg and 'negTags: neg' in src)

print('TOTAL FAIL' if fails else 'ALL PASS', len(fails))
sys.exit(1 if fails else 0)
