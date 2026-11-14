# v20a182 修 v178 設計 review B1＋C1＋C2 static tests：
# B1：獎項頁「同屆提名」行被裁切（fellows 行 scrollW 494 vs 卡 340，成行 31% 唔見）——
#     提名行獨立 class .awd62-fellows 准換行；日期行繼續用 .awd62-when（nowrap）唔郁。
# C1：提名卡列三張 CSS 卡一模一樣——卡面改做 fellow 專屬（大字首字＋全名＋媒介細行，
#     底色按星名 hash 揀 tint）；卡片數據／判定唔郁，只改呈現。
# C2：請柬 modal 下方大片黑空——根源係請柬喺 N1 開場故事 modal 仲開緊嗰陣 present，
#     #mask 留返 story-play-on，modal 變 height:100% 全黑（實量 932px）；修法係
#     presentAwardInvite 開請柬前落返個 class（唔郁請柬邏輯），另加一行今晚獎項填補內容。
# 反證: run against pristine main (4475564) index -> B1/C1/C2 全部未入 -> FAIL（唔 crash）。
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

def rule(sel):
    i = src.find(sel + '{')
    if i < 0: return ''
    j = src.find('}', i)
    return src[i:j + 1] if j > i else ''

pane_fn = slice_fn('renderAwardsPane62')
play_fn = slice_fn('awards62PlayCeremony')
present_fn = slice_fn('presentAwardInvite')
invite_fn = slice_fn('renderAwardInviteHtml')
modal_fn = slice_fn('modal')

# --- B1：提名行准換行 ---
chk('B1 提名行獨立 class .awd62-fellows 在位', '.awd62-fellows' in src)
_fel_rule = rule('.awd62-item .awd62-fellows')
chk('B1 .awd62-fellows 准換行（white-space:normal）', 'white-space:normal' in _fel_rule)
chk('B1 .awd62-fellows 另起一行（flex-basis:100%）', 'flex-basis:100%' in _fel_rule)
chk('B1 獎項頁提名行用新 class', 'awd62-fellows' in pane_fn)
chk('B1 獎項頁只剩日期行用 .awd62-when（提名行唔再用）', pane_fn.count('awd62-when') == 1)
chk('B1 日期行繼續 nowrap（唔郁）', 'white-space:nowrap' in rule('.awd62-item .awd62-when'))

# --- C1：CSS 卡面 fellow 專屬 ---
chk('C1 CSS 卡仍在 play 內（通用跌返規則唔郁）', 'awd63-csscard' in play_fn)
chk('C1 卡面有大字首字 span', 'awd63-cssmono' in play_fn and '.awd63-cssmono' in src)
chk('C1 卡面有全名 span', 'awd63-cssstar' in play_fn and '.awd63-cssstar' in src)
chk('C1 卡面有媒介細行 span', 'awd63-cssmed' in play_fn and '.awd63-cssmed' in src)
chk('C1 首字取自星名（charAt(0)）', "charAt(0)" in play_fn)
_pal = re.search(r'AWDS63_TINTS182 = \[[^\]]*\]', play_fn)
chk('C1 底色 tint palette 在位（≥3 色）', bool(_pal) and len(re.findall(r'"#[0-9a-f]{6}"', _pal.group(0))) >= 3)
chk('C1 底色 tint 按卡位 index 揀（保證同場唔撞）', 'AWDS63_TINTS182[ci % AWDS63_TINTS182.length]' in play_fn)
chk('C1 卡面唔再印典禮名（medName149／cssname 已撤）', 'medName149' not in play_fn and 'awd63-cssname' not in src)
chk('C1 卡片 builder 通用路徑唔郁（v20a208：搬入 buildCardsData208／cardsHtmlFor208，變數名 fl／cd）', 'fl.forEach(f=> cd.push' in play_fn)
chk('C1 CSS 卡仍係 2:3 框', 'aspect-ratio:2/3' in rule('.awd63-csscard'))
chk('C1 得主／玩家角標 CSS 唔郁', '.awd63-card.me' in src and '.awd63-card.win' in src)

# --- C2：請柬唔行 story 全屏舞台 ---
chk('C2 presentAwardInvite 開請柬前落 story-play-on', 'classList.remove("story-play-on")' in present_fn)
chk('C2 同步清 story-play lock', 'setStoryPlayLock(false)' in present_fn)
chk('C2 modal() 本身唔郁 story-play-on（唔影響 StoryPlay）', 'story-play-on' not in modal_fn)
chk('C2 請柬加今晚獎項行（真實 categories 數據）', '今晚獎項' in invite_fn and 'pack.categories' in invite_fn)
chk('C2 請柬接線唔郁（細海報＋同屆提名）', 'awards63InviteBitHtml' in invite_fn)
chk('C2 請柬邏輯唔郁（出席／推辭＋dismiss 即推辭）', '"出席"' in present_fn and '"推辭"' in present_fn and 'onDismiss: skip' in present_fn)
chk('C2 出席先播動畫再入結果卡', 'awards62PlayCeremony' in present_fn and 'presentAwardResult' in present_fn)

# --- 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變（s107）', 's107' in src)
chk('產品 ?v 不變（v20a10）', 'v20a10' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
