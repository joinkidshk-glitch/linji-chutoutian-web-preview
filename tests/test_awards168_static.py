# v20a168 頒獎禮 glamour 期間提名卡列隱藏 static tests（v166 review C1）：
# 修法（v168 原版）：glamour beat 期間將提名卡列一併隱藏——揀「隱藏」唔係「壓暗」：
#   壓暗會留低同一張海報嘅鬼影（缺陷本身就係「同一張海報出現兩次」），只有隱藏先徹底消除；
#   v168 用 visibility:hidden，卡列留位、frame 高度／字幕／tap 行唔跳動。
# v20a174 C2 改法：visibility:hidden → display:none——frame 收短，嗰 174px 死位取消
#   （glamour 入段／出段 frame 會 recentre，係 C2 接受咗嘅 trade-off；見 test_awards174）。
# 機制：syncGlamour 係單一 choke point（init＋advance 兩處 call），跟 overlay 同一條件開／閂——
#   glamour beat 入段加 .glamour-hide，下一 beat（out）即刻除返，恢復自動；跳過／完結拆成個舞台，唔使另行恢復。
# 斷言：
# (1) CSS：.awd63-cards.glamour-hide 規則在場，display:none（v174 C2：收短 frame，唔再留位）。
# (2) JS：syncGlamour 入面 cardsEl 同條件 toggle glamour-hide（glamour 先加，其他 beats 除返＝恢復）。
# (3) syncCards "on" beat 清單唔郁：卡列 "on" 邏輯不變（names／suspense／reveal／comfort 先加 on，glamour 唔入 list——
#     卡列 glamour 期間仍然係 "on" 態，只係俾 display:none 隱藏，恢復嗰陣唔使重新唱名）；
#     但 stagger 時序 v174 B2 改咗（200＋i*380 → 60＋i*180，見 test_awards174）。
# (4) v166 並置佈局唔變：overlay 只冚 canvas（aspect-ratio 424/360，v174 B1）、右 panel 44%＋0.93 暗底、海報縮細 88%／60%。
# (5) beats 唔變：won 順序 reveal→walkup→glamour→out，glamour 1800ms；syncGlamour 兩個 call 位（init＋advance）齊。
# 反證：run against pristine main (60b0a8f) -> (1)(2) 斷言全部 FAIL（唔 crash）；(3)(4)(5) 係回歸守衛，pristine 應 PASS。
import os, sys

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(idx_path))
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

def css_rule(selector):
    i = src.find(selector + '{')
    if i < 0: return ''
    j = src.find('}', i)
    return src[i:j+1] if j >= 0 else ''

play_fn = slice_fn('awards62PlayCeremony')

# --- (1) CSS：glamour-hide 規則 ---
hide_css = css_rule('.awd63-cards.glamour-hide')
chk('C1 glamour-hide CSS 規則在場', bool(hide_css))
chk('C1 卡列隱藏用 display:none（v174 C2：收短 frame）', 'display:none' in hide_css)
chk('C1 唔再 visibility:hidden 留位（174px 死位取消）', 'visibility:hidden' not in hide_css)
chk('C1 .awd63-cards.on 規則跟 v174 B2（常駐 flex＋visibility）', css_rule('.awd63-cards.on') == '.awd63-cards.on{visibility:visible}')

# --- (2) JS：syncGlamour 同條件 toggle ---
sg_i = play_fn.find('const syncGlamour')
sg_block = play_fn[sg_i:play_fn.find('const syncWalkup', sg_i)] if sg_i >= 0 else ''
chk('C1 syncGlamour 在場', bool(sg_block))
chk('C1 syncGlamour toggle 卡列 glamour-hide', 'cardsEl.classList.toggle("glamour-hide"' in sg_block)
chk('C1 卡列 toggle 同 overlay 同條件（淨係 glamour beat）',
    'classList.toggle("on", !!(b && b.id === "glamour"))' in sg_block
    and 'classList.toggle("glamour-hide", !!(b && b.id === "glamour"))' in sg_block)
chk('C1 cardsEl 有 null guard（gallery 冇卡列唔會爆）', 'if(cardsEl)' in sg_block)
chk('C1 syncGlamour 註解寫明恢復機制（下一 beat 即恢復）', '下一 beat' in sg_block and '恢復' in sg_block)
chk('C1 syncGlamour 兩個 call 位齊（init＋advance）', play_fn.count('syncGlamour(beats[') == 2)

# --- (3) syncCards 唔郁 ---
sc_i = play_fn.find('const syncCards')
sc_block = play_fn[sc_i:play_fn.find('const syncGlamour', sc_i)] if sc_i >= 0 else ''
chk('C1 syncCards 在場', bool(sc_block))
chk('C1 syncCards 只喺 names／suspense／reveal／comfort 加 on',
    'b.id === "names"' in sc_block and 'b.id === "suspense"' in sc_block
    and 'b.id === "reveal"' in sc_block and 'b.id === "comfort"' in sc_block)
chk('C1 syncCards 唔掂 glamour（卡列 glamour 期間繼續 "on"，只係俾 display:none 隱藏）',
    'b.id === "glamour"' not in sc_block and 'glamour-hide' not in sc_block)
chk('C1 syncCards 唔會除 "on"（恢復唔使重新唱名）', 'classList.remove("on")' not in sc_block)

# --- (4) v166 並置佈局唔變 ---
glam_css = css_rule('.awd63-glamour')
chk('C1 v166 overlay 唔變（absolute＋424/360 對齊 canvas，v174 B1）',
    'position:absolute' in glam_css and 'aspect-ratio:424/360' in glam_css and 'inset:0' not in glam_css)
panel_css = css_rule('.awd63-glamour-panel')
chk('C1 v166 右 panel 唔變（44%＋0.93 暗底）',
    'flex:0 0 44%' in panel_css and 'background:rgba(10,6,18,.93)' in panel_css)
panel_img = css_rule('.awd63-glamour-panel>img')  # v20a174 A1：裱框規則收窄到直屬海報 img（>）
chk('C1 v166 海報縮細唔變（88%／60%）', 'max-width:88%' in panel_img and 'max-height:60%' in panel_img)
chk('C1 v166 glamour 層仲喺 frame 入面', '+ glamHtml' in play_fn and 'awd62-canvas' in play_fn)

# --- (5) beats 唔變 ---
beats_fn = slice_fn('awards62CeremonyBeats')
chk('C1 glamour beat 仲係 1800ms', 'id: "glamour", ms: 1800, caption: ""' in beats_fn)
chk('C1 won 順序唔變（reveal→walkup→glamour→out）',
    beats_fn.find('id: "reveal"') < beats_fn.find('id: "walkup"') < beats_fn.find('id: "glamour"')
    < beats_fn.rfind('id: "out"'))
chk('C1 walkup／out 時長唔變', 'id: "walkup", ms: 2200' in beats_fn and 'id: "out", ms: 500' in beats_fn)
chk('C1 setCaption 空框隱藏唔郁（v166 C1）', 'style.display' in play_fn and 'textContent' in play_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
