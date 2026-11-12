# v20a62 頒獎優化包 static tests: A 評分改版接線齊（新公式／代表作／門檻行／弱瓣／季前提示／獎項頁）、
# B 8-bit 像素動畫三路齊（序列／跳過／降級）、舊運氣骰同隱形壓分清零、插畫版 B 已全撤、硬規則（SAVE key）冇郁。
# 反證: run against a pre-v62 index -> AWARDS62 block missing -> FAIL.
import sys, re

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0: return src[i:k+1]
    return ''

# --- 區塊本體 ---
chk('AWARDS62 block present', '/* ===== v20a62 AWARDS62' in src)
chk('WIN_LINE const 0.875（v20a147 D4 重做校準：0.90→0.875，見 qa147/CALIBRATION_D4.md §5）', 'const AWARDS62_WIN_LINE = 0.875' in src)
chk('TASTE const 0.05', 'const AWARDS62_TASTE = 0.05' in src)
chk('ROLE_Q const', 'const AWARDS62_ROLE_Q' in src and 'film_lead_big: 1.00' in src)
chk('scoreParts defined', 'function awards62ScoreParts(cat, ceremony, year)' in src)
chk('standing defined', 'function awards62Standing(ceremony, year)' in src)
chk('weakHint defined', 'function awards62WeakHint(parts, cat)' in src)
chk('seasonHints defined', 'function awards62SeasonHints(st, w)' in src)
chk('renderAwardsPane62 defined', 'function renderAwardsPane62()' in src)
chk('beats defined', 'function awards62CeremonyBeats(pack)' in src)
chk('playCeremony defined', 'function awards62PlayCeremony(pack, doneFn)' in src)

# --- A1/A3: 運氣骰同隱形壓分清零 ---
chk('18% 贏獎骰全檔消失', 'Math.random() < 0.18' not in src)
score_fn = slice_fn('awardsScoreCategory')
chk('score fn 行新公式（awards62ScoreParts）', 'awards62ScoreParts' in score_fn)
chk('score fn 冇 firstYearSoftBias', 'firstYearSoftBias' not in score_fn)
chk('score fn 冇 ×0.72 壓分', '0.72' not in score_fn)
chk('score fn 用贏線判定', 'AWARDS62_WIN_LINE' in score_fn)

# --- A2/A4/A5: pack／log／卡片接線 ---
build_fn = slice_fn('buildAwardResultPack')
chk('build pack 計代表作', 'awards62RepWork' in build_fn and 'repWorkTitle' in build_fn)
chk('build pack 弱瓣', 'weakHint62' in build_fn and 'awards62WeakHint' in build_fn)
chk('build pack standing 快照', 'standing62' in build_fn and 'awards62Standing' in build_fn)
commit_fn = slice_fn('commitAwardToLog')
chk('log 只加欄位：displayName', 'displayName: pack.displayName' in commit_fn)
chk('log 只加欄位：repTitle', 'repTitle: c.repWorkTitle' in commit_fn)
invite_fn = slice_fn('renderAwardInviteHtml')
chk('請柬出代表作行', 'repWork62' in invite_fn and 'psr-rep62' in invite_fn)
chk('請柬出門檻行', 'awards62GateLineHtml' in invite_fn)
result_fn = slice_fn('renderAwardResultHtml')
chk('結果卡出代表作行', 'repWorkTitle' in result_fn and 'psr-rep62' in result_fn)
chk('結果卡出弱瓣行', 'weakHint62' in result_fn and 'psr-weak62' in result_fn)

# --- A6: 季前提示接 settleWeek 既有渠道 ---
settle_fn = slice_fn('settleWeek')
chk('settleWeek 接 awards62SeasonHints', 'awards62SeasonHints' in settle_fn and 'pushFlavor' in settle_fn)

# --- A7: 手帳獎項頁 ---
chk('手帳 tab：獎項', 'data-htab="awards"' in src and 'id="htab-awards"' in src)
chk('手帳 pane：獎項', 'id="home-pane-awards"' in src and 'id="awards-list"' in src)
tab_fn = slice_fn('setHomeTab')
chk('setHomeTab 接 awards 頁', 'awards' in tab_fn and 'renderAwardsPane62' in tab_fn)

# --- B: 像素動畫三路（序列／跳過／降級） ---
m = re.search(r'const AWARDS62_STAGE_PX = "data:image/webp;base64,([A-Za-z0-9+/=]+)"', src)
chk('像素舞台底圖在位（WebP data URI）', m is not None)
chk('底圖 base64 ≤150KB 目標（實際約 25KB）', m is not None and len(m.group(1)) <= 150 * 1024)
chk('阿偉精靈圖（v64 起改 Q 版 AWARDS64_SPRITES；舊手繪 map 已撤）', 'const AWARDS62_SPR_STAND' not in src and 'const AWARDS64_SPRITES' in src)
chk('canvas 像素呈現（pixelated）', 'image-rendering:pixelated' in src and 'awd62-canvas' in src)
chk('跳過掣存在', 'awd62-skip' in src and '跳過' in src)
chk('撳畫面推進存在', 'addEventListener("click"' in slice_fn('awards62PlayCeremony'))
chk('降級舞台函數存在', 'function awards62FallbackStage(ctx, W, H)' in src)
play_fn = slice_fn('awards62PlayCeremony')
chk('play 有完成 guard（doneFn 只行一次）', 'finished' in play_fn)
present_fn = slice_fn('presentAwardInvite')
chk('出席先播動畫再入結果卡', 'awards62PlayCeremony' in present_fn and 'presentAwardResult' in present_fn)
chk('插畫版 B 已全撤（冇殘留）', 'AWARDS62_STAGE_IMG' not in src and 'awd62-confetti' not in src and 'awd62LineIn' not in src)

# --- 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('CALIB60 冇被郁（遞減帶在位）', 'const CALIB60_FAME_BANDS' in src)
chk('CONSEQ61 冇被郁（後果包在位）', 'conseq61SettleEval' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
