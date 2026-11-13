# v20a200 修 v194 設計 review C1＋C2・static tests：
# C1：gap 句加「今年」——邀請函閘句（awards62GateLineHtml）＋季前提示（awards62SeasonHints）
#     兩邊一齊加；計數規則本身唔郁（countYearMediumWraps 繼續按 wrappedDay 曆法年計入嗰屆，
#     gapWorks＝wrapMin－wraps；跨年唔計係既定口徑）。
# C2：旁聽請柬 rep 行分流——awards63InviteBitHtml 按 pack.tier === "gallery" 改「入場觀禮」，
#     nominee／won 照舊「爭獎」；renderAwardInviteHtml 嘅 fallback 同樣分流。
# v192 殘留（對過）：nominee「今晚獎項」行改標籤做「你爭嘅獎項」，slate 唔郁；
#     gallery 嗰邊「今晚獎項」＋（觀禮）全 slate 唔郁。
# 唔郁嘅嘢：SAVE key、softRev s107、?v=v20a10、8 款贏獎報紙 headline（v192 已驗逐字）。
# 反證: run against pristine main a1a6681 index -> v200 標記未入 -> FAIL（唔 crash）。
# 用法：python3 tests/test_awards200_static.py [path-to-index.html]
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


# --- 反證守衛：v200 標記唔在就乾淨 FAIL，唔好逐項誤判 ---
NEED200 = ['今年仲差 ', '入場觀禮', '你爭嘅獎項']
missing200 = [s for s in NEED200 if s not in src]
if missing200:
    for m in missing200:
        chk('反證：%s 唔存在（pristine main 預期，v200 未入）' % m, False)
    print('\nFAILED: %d' % len(fails))
    sys.exit(1)

gate_fn = slice_fn('awards62GateLineHtml')
hint_fn = slice_fn('awards62SeasonHints')
invite_fn = slice_fn('renderAwardInviteHtml')
rep_fn = slice_fn('awards63InviteBitHtml')

# --- C1：兩邊 gap 句都有「今年」，舊無年份寫法清走 ---
chk('C1：邀請函閘句 gap 句加「今年」', '今年仲差 " + st.gapWorks' in gate_fn)
chk('C1：邀請函閘句無年份舊寫法清走', '"仲差 " + st.gapWorks' not in src)
chk('C1：季前提示 gap 句加「今年」', '今年仲差 " + sd.gapWorks' in hint_fn)
chk('C1：季前提示無年份舊寫法清走', '：仲差 " + sd.gapWorks' not in src)
chk('C1：兩邊 gap 句寫法一致（同一個「今年仲差 N 部 X 作品先夠入圍」句式）',
    gate_fn.count('今年仲差') == 1 and hint_fn.count('今年仲差') == 1)

# --- C1：計數規則本身唔郁 ---
count_fn = slice_fn('countYearMediumWraps')
chk('C1：計數繼續按 wrappedDay 曆法年計入嗰屆（跨年唔計，口徑唔郁）',
    'awardsYearFromDay(h.wrappedDay!=null ? h.wrappedDay : h.dayIndex)' in count_fn)
chk('C1：gapWorks 定義唔郁（wrapMin－wraps）',
    'gapWorks: Math.max(0, wrapMin - wraps)' in src)
chk('C1：nominee 分支「嗰年 N 部…爭獎」唔郁',
    '入圍門檻已達標：嗰年 " + st.wraps' in gate_fn)
chk('C1：角色閘句「嗰年未做過主角／配角級作品」唔郁',
    '嗰年未做過主角／配角級作品，入圍唔到演員獎' in gate_fn)

# --- C2：rep 行按 tier 分流 ---
chk('C2：rep 行按 pack.tier === "gallery" 分流', 'pack.tier === "gallery"' in rep_fn)
chk('C2：gallery 嗰陣寫「入場觀禮」', '入場觀禮' in rep_fn)
chk('C2：nominee／won 照舊寫「爭獎」', '爭獎' in rep_fn)
def strip_comments(s):
    return re.sub(r'/\*.*?\*/', '', s, flags=re.S)


chk('C2：rep 行「爭獎」喺函數內恰好 1 處（淨係非 gallery 分支；註解唔計）',
    strip_comments(rep_fn).count('爭獎') == 1)
chk('C2：fallback 行同樣分流（唔會兜返舊寫法）',
    '入場觀禮' in invite_fn and '爭獎' in invite_fn)
chk('C2：閘句「爭獎」淨係 nominee 分支有（gallery 閘句零爭獎；註解唔計）',
    strip_comments(gate_fn).count('爭獎') == 1)
chk('C2：海報＋同屆提名照留（改寫法唔係刪行）',
    'awd63-invite-poster' in rep_fn and '同屆提名' in rep_fn)

# --- v192 殘留：nominee 行改標籤唔改 slate；gallery 唔郁 ---
chk('殘留：nominee 行標籤改做「你爭嘅獎項」', '你爭嘅獎項：' in invite_fn)
chk('殘留：gallery 行仲係「今晚獎項」＋（觀禮）全 slate', '今晚獎項：' in invite_fn and '（觀禮）' in invite_fn)
chk('殘留：非 gallery 分支唔再用「今晚獎項」做標籤',
    invite_fn.count('今晚獎項：') == 1)

# --- 唔郁嘅嘢 ---
chk('唔郁：SAVE key', 'starVolunteer_map_v19w' in src)
chk('唔郁：softRev s107', 'softRev:"s107"' in src)
chk('唔郁：?v=v20a10', 'version:"v20a10"' in src)
WIN8 = ['維港影藝獎揭曉 阿偉 奪演員獎', '影藝獎夜 阿偉奪獎成焦點',
        '星河台慶夜 演員獎爆冷由阿偉奪得', '台慶夜 阿偉奪獎贏街坊票',
        '星河金碟夜 阿偉奪獎跑出', '金碟夜 阿偉奪獎 樂壇多把靚聲',
        '維港街招賞 阿偉跑出', '街外一鏡 阿偉奪獎贏掌聲']
chk('唔郁：8 款贏獎報紙 headline 逐字不變（v192 已驗；模板用 {playerName} 代位）',
    all((h in src) or (h.replace('阿偉', '{playerName}') in src) for h in WIN8))

print('\nFAILED: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
