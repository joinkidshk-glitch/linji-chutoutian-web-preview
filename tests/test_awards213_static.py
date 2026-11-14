# v20a213 請柬提前 3 日＋典禮改晚上播・static tests：
# 1. 請柬窗口＝[典禮日−3, 典禮日]（季節配對唔再係閘；week 閘＋C10 讓路照留）。
# 2. 請柬決定＝預約（book attend／decline），唔即播；晚間播掛喺晨鏈頭＋日結續鏈；典禮日係關鍵日。
# 3. 報紙 publishDay＝典禮日＋1（override 嗰陣先改，冇 override 照舊 day+1）。
# 4. 請柬文案有 stamp 寫實日期，冇 stamp 跌返「今晚」。
# 5. 唔郁嘅嘢：贏線 0.875、獎項表、報紙翌日規則、C10 anti-stack、SAVE key、softRev s107、?v=v20a10。
# 反證: run against pristine main f58f19c index -> v213 標記未入 -> FAIL（唔 crash）。
# 用法：python3 tests/test_awards213_static.py [path-to-index.html]
import re
import sys

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
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


# --- 反證守衛：v213 標記唔在就乾淨 FAIL，唔好逐項誤判 ---
NEED213 = ['AWARDS213_LEAD_DAYS', 'awardBooked213', 'awards213PlayBookedEvening', '典禮夜：']
missing213 = [s for s in NEED213 if s not in src]
if missing213:
    for m in missing213:
        chk('反證：%s 唔存在（pristine main 預期，v213 未入）' % m, False)
    print('\nFAILED: %d' % len(fails))
    sys.exit(1)

queue_fn = slice_fn('queueAwardsOnSeasonWindow')
invite_fn = slice_fn('renderAwardInviteHtml')
present_fn = slice_fn('presentAwardInvite')
chain_fn = slice_fn('morningChain196')
plan_fn = slice_fn('resolvePlannedDay')
crit_fn = slice_fn('isCriticalPlanDay')
paper_fn = slice_fn('enqueueNewspaperFromAward')
gate_fn = slice_fn('awards62GateLineHtml')
play_fn = slice_fn('awards213PlayBookedEvening')
book_fn = slice_fn('awards213Book')
restore_fn = slice_fn('restorePendingAward136')
queue_invite_fn = slice_fn('queueAwardInvite')

# --- 1. 請柬窗口 ---
chk('1：LEAD_DAYS＝3', 'const AWARDS213_LEAD_DAYS = 3;' in src)
chk('1：典禮日＝季節首日（春 3／夏 6／秋 9／冬 12）',
    '"春":3, "夏":6, "秋":9, "冬":12' in src)
chk('1：queue 用窗口 [典禮日−3, 典禮日] 判', 'cerDay213 - AWARDS213_LEAD_DAYS' in queue_fn)
chk('1：queue 唔再用季節配對做閘（請柬日仲係上一季）', '!awardsSeasonMatches(ceremony)' not in queue_fn)
chk('1：queue week 閘照留（雙保險）', 'awardsWeekOk(ceremony)' in queue_fn)
chk('1：queue C10 讓路照留（TV only＋ignoreC10）',
    'softC10WindowActive()' in queue_fn and 'ignoreC10' in queue_fn)
chk('1：queue 決定咗唔重排（HasBooked 閘）', 'awards213HasBooked(year, ceremony.id)' in queue_fn)
chk('1：queue 印典禮日＋請柬日 stamp',
    'pack.ceremonyDay213 = cerDay213b' in queue_fn and 'pack.inviteDay213 = cerDay213b - AWARDS213_LEAD_DAYS' in queue_fn)
chk('1：debug force 跳過窗口（探針／自檢唔郁）', 'forceCeremonyId' in queue_fn)

# --- 2. 預約＋晚間播 ---
chk('2：出席＝預約 attend（唔即播）', 'awards213Book(pack, "attend")' in present_fn)
chk('2：推辭＝預約 decline（唔即播）', 'awards213Book(pack, "decline")' in present_fn)
chk('2：合成 pack（未知 ceremonyId）保留舊即播行為',
    'awardsCeremonyById(pack.ceremonyId)' in present_fn)
chk('2：晨鏈頭掛晚間典禮（播完先行返 step）', 'awards213PlayBookedEvening(step)' in chain_fn)
chk('2：日結續鏈包晚間典禮（nextNbRaw 經 EveningThen）', 'awards213EveningThen(nextNbRaw)' in plan_fn)
chk('2：晚間播 one-shot（播之前清 booking）', 'awards213ClearBooked();' in play_fn)
chk('2：晚間播 log 入面 pack.dayIndex＝典禮日', 'pack.dayIndex = b.ceremonyDay|0' in play_fn)
chk('2：典禮進行中唔重入（CeremonyActive 閘）', 'awards62CeremonyActive()' in play_fn)
chk('2：典禮日係關鍵日（唔靜默加速）', 'awards213BookedForDay' in crit_fn)
chk('2：預約咗 restore 唔重建請柬', 'awards213HasBooked(year, cid)' in restore_fn)
chk('2：預約咗 queueAwardInvite 唔再排', 'awards213HasBooked(pack.year, pack.ceremonyId)' in queue_invite_fn)
chk('2：booking 寫入 S（持久化）＋清 pending', 'S.awardBooked213 = booked' in book_fn and 'S.pendingAwardPack = null' in book_fn)

# --- 3. 報紙翌日規則 ---
chk('3：報紙用典禮日 override（晚間播嗰陣）', '_awardCeremonyDay213' in paper_fn)
chk('3：報紙 publishDay 照舊 day+1（兩條路徑都係）', paper_fn.count('publishDay: day+1') >= 2)
chk('3：冇 override 嗰陣照用 S.dayIndex', '((S && (S.dayIndex|0)) || 0)' in paper_fn)

# --- 4. 請柬文案寫實日期 ---
chk('4：請柬加「典禮夜：日期」行', '典禮夜：${awards213DateLabel(pack.ceremonyDay213)}' in invite_fn)
chk('4：gallery 獎項行有 stamp 寫實日期', 'awards213DateLabelShort(pack.ceremonyDay213) + "獎項："' in invite_fn)
chk('4：gallery 獎項行冇 stamp 跌返「今晚獎項：」（舊測試逐字期望唔郁）',
    '"今晚獎項："' in invite_fn)
chk('4：閘句有 stamp 寫實日期', 'awards213DateLabelShort(pack.ceremonyDay213) + "席位：觀禮。"' in gate_fn)
chk('4：閘句冇 stamp 跌返「今晚席位：觀禮。」', '"今晚席位：觀禮。"' in gate_fn)

# --- 5. 唔郁嘅嘢 ---
chk('唔郁：贏線 0.875', 'AWARDS62_WIN_LINE = 0.875' in src)
chk('唔郁：典禮本身逐格流程（awards62PlayCeremony 仲在）', 'function awards62PlayCeremony(pack, doneFn)' in src)
chk('唔郁：SAVE key', 'starVolunteer_map_v19w' in src)
chk('唔郁：softRev s107', 'softRev:"s107"' in src)
chk('唔郁：?v=v20a10', 'version:"v20a10"' in src)
chk('唔郁：C10 anti-stack 函數本身唔郁（49–52 週）',
    'wkInYear < 49 || wkInYear > 52' in src)
chk('唔郁：請柬掣仲係「出席／推辭」', '"出席"' in present_fn and '"推辭"' in present_fn)

print('\nFAILED: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
