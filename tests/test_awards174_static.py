# v20a211 B1 resync：雙幾何（矮 480×432／高 480×540，HS211／HSC211＝×1.25）——短基準值不變，高 viewport 按比例換算；見 NOTES_V20A211。
# v20a174：修 v170 review A1＋B1＋B2＋C1＋C2 static tests。
# A1 獎盃圖標喺深色底失效：(a) .awd63-glamour-panel img 裱框規則收窄到直屬海報 img（>），
#     唔再套落 .cap 內 22px 獎盃；(b) glamour cap＋reveal 字幕嘅獎盃 img 加金底 chip（background #f2c14e，
#     22px），深啡線稿喺金底上面 1x 睇得清；圖標資產本身唔改（成套 26 隻風格唔郁）。
# B1 舞台做大：canvas 424×240→424×360（底圖垂直拉伸 1.5×，吊燈／幕布邊完整保留，唔用 cover-crop——
#     cover 1.5× 會裁走兩盞吊燈 x26–83／340–397，見 NOTES §2）；FLOOR 193→290，人仔 48／50／64→72／75／96，
#     slotCx 間距 72→80，行前 y＋7→＋10，光池 66→99，glyph 21×12→31×18，後備舞台 H-47→H-70。
#     v20a177 resync：FLOOR 290→250（底圖重構，地板深 110px）、slotCx 間距 80→100／置中 202→212、
#     後備舞台 H-70→H-110／H-76→H-116、gallery 中央唔再 −36（改 [82,162,262]），見 NOTES_V20A177.md。
#     v20a181 resync：舞台橫向重建 480×360（4:3）／backing 720×540；FLOOR 250→262（木地板 y200–334，
#     深 134px）；slotCx 間距 100→120／置中 212→240；人物改 PixelLab 幀 112／116／112；獎盃 glyph
#     −96／−39→−112／−52；後備舞台改 delegate 去 awards181DrawBase；講台／圓台成批消失（C1 作廢）。
#     v20a174 rebase 上 main a500536（v149 已落地）：合併後 backing 636×540（邏輯 424×360 ×1.5，
#     setTransform 1.5 均勻），見 NOTES §9；B1 斷言跟合併態，舊「636 唔入呢票」守衛已作廢。
# B2 names 卡列跳位＋逐張淡入：(a) 卡列預留高度——.awd63-cards 常駐 flex＋visibility:hidden，
#     .on 先可見，names 開場 frame 高唔跳；(b) stagger 200＋i*380 → 60＋i*180，第 4 張 600ms 出齊。
# C1 gallery 中央提名人俾講台遮：v20a181 起舞台冇圓台／講台，呢節作廢——gallery 企位改 [75,240,405]
#     （左／中／右分開企，罅 165px）；won 路 slot 公式置中 240／間距 120。舊 −36 移位繼續唔出現。
# C2 glamour 174px 隱藏卡列空帶：glamour-hide 由 visibility:hidden 改 display:none，frame 收短，死位取消。
# 唔郁守衛：cardsData／cardsHtml 唔掂（提名卡人像未拍板）、SAVE key、softRev、?v=。
# 反證：run against pristine main a500536 -> A1／B1／B2／C1／C2 斷言全部 FAIL（唔 crash）；唔郁守衛 pristine 應 PASS。
# （舊反證基底 e8c3a73；rebase 後改用 a500536——pristine 嗰陣已有 v149 636×360 backing＋M5 彩紙，
#  所以合併態斷言（636×540＋H=360）對佢要乾淨 FAIL。）
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
fb_fn = slice_fn('awards62FallbackStage')

# --- A1：獎盃圖標喺深色底失效 ---
panel_img = css_rule('.awd63-glamour-panel>img')
chk('A1 海報裱框規則收窄到直屬 img（>）', bool(panel_img))
chk('A1 裱框唔再套落 panel 內全部 img（舊 .awd63-glamour-panel img 規則消失）',
    '.awd63-glamour-panel img{' not in src)
chk('A1 海報金框＋光暈保留', 'border:4px solid #f2c14e' in panel_img and 'box-shadow:0 0 34px rgba(242,193,78,.45)' in panel_img)
chip_rule = css_rule('.awd63-glamour .cap img.ic112,.awd62-caption img.ic112,.psr-fellows63 img.ic112') # v20a207 C2：同一 rule 擴到結果卡同屆提名行
chk('A1 獎盃金底 chip 規則在場（glamour cap＋reveal 字幕）', bool(chip_rule))
chk('A1 chip 係金底（#f2c14e）', 'background:#f2c14e' in chip_rule)
chk('A1 chip 22px 見方（1x 睇得清）', 'width:22px' in chip_rule and 'height:22px' in chip_rule)
chk('A1 chip 唔帶金邊裱框（唔會再變空心方框）', 'border:4px' not in chip_rule)
chk('A1 glamour cap 仍然用獎盃圖標（唔係刪圖標了事）', 'iconHtml112("🏆")' in play_fn)
chk('A1 reveal 字幕仍然用獎盃圖標', 'iconHtml112("🏆")' in slice_fn('awards62CeremonyBeats'))
chk('A1 圖標資產本身唔改（trophy 仍經 iconHtml112，唔改成套風格）',
    '"🏆":"trophy"' in src and 'icon_trophy' not in play_fn)

# --- B1：舞台做大 ---
chk('B1 canvas backing 720×648（v181：邏輯 480×432 ×1.5；v20a207 B2）', 'Math.round(HS211 * 1.5)' in src)
chk('B1 draw() 用橫向 480×432（10:9；v20a207 B2）', 'const W = 480, H = HS211' in play_fn)
chk('B1 FLOOR＝314（v20a207 B2：木地板 y274–372，深 98px）', 'const FLOOR = Math.round(314 * HSC211)' in play_fn)
chk('B1 人物 px 幀（136／140／燕尾服 136；v20a207 B2）', 'Math.round(140 * HSC211)' in play_fn and 'dispH: Math.round(136 * HSC211)' in play_fn)
chk('B1 slotCx 間距 120、置中 240（v181）', '240 + (i - (slots.length - 1) / 2) * 120' in play_fn)
chk('B1 glamour overlay aspect 跟 canvas（480/432；v20a207 B2）', 'aspect-ratio:480/432' in src)
chk('B1 行前 y＋10（腳 324；v20a207 B2）', 'y: Math.round(10 * p)' in play_fn)
chk('B1 光池高 120（v20a207 B2）', 'F - Math.round(120 * HSC211)' in play_fn)
chk('B1 獎盃 glyph（−129／−61，v20a187 C6；v20a207 B2；舊 −112）', 'FLOOR + fp.y - Math.round(129 * HSC211)' in play_fn and 'FLOOR + fp.y - Math.round(61 * HSC211)' in play_fn)
chk('B1 彩紙底界跟新高（436；v20a207 B2）', 'p.y > HS211 + 4' in play_fn)
chk('B1 後備舞台 delegate 去程式舞台（H-110 舊平台頂消失）', 'awards181DrawBase(ctx, W, H, 0)' in fb_fn and 'H - 110' not in fb_fn)
chk('B1 合併態釘死：backing 720×648＋setTransform 1.5＋邏輯 480×432（v181；v20a207 B2）',
    'Math.round(HS211 * 1.5)' in src
    and 'ctx.setTransform(1.5, 0, 0, 1.5, 0, 0);' in play_fn
    and 'const W = 480, H = HS211' in play_fn)
chk('B1 舊 canvas 高 240 唔再出現（play 範圍）', 'H = 240' not in play_fn and 'height="240"' not in play_fn)

# --- B2：names 卡列跳位＋逐張淡入 ---
cards_css = css_rule('.awd63-cards')
chk('B2 卡列預留高度（常駐 flex）', 'display:flex' in cards_css)
chk('B2 卡列未開嗰陣 visibility 隱藏（唔係 display:none）',
    'visibility:hidden' in cards_css and 'display:none' not in cards_css)
chk('B2 .on 先可見（visibility:visible）', css_rule('.awd63-cards.on') == '.awd63-cards.on{visibility:visible}')
chk('B2 stagger 縮短（60＋i*180）', 'elapsed > 60 + i * 180' in play_fn)
chk('B2 舊 stagger 唔再出現（200＋i*380）', 'elapsed > 200 + i * 380' not in play_fn)
chk('B2 卡列 beat 清單唔變（names／suspense／reveal／comfort）',
    'b.id === "names"' in play_fn and 'b.id === "suspense"' in play_fn
    and 'b.id === "reveal"' in play_fn and 'b.id === "comfort"' in play_fn)

# --- C1：gallery 中央提名人俾講台遮 ---
chk('C1 gallery 3 slots 用 [75, 240, 405]（v181：講台已撤，左／中／右分開企）',
    '[75, 240, 405]' in play_fn)
chk('C1 舊中央 −36 移位唔再出現', 'cx -= 36' not in play_fn)
chk('C1 won 路 slot 公式置中 240／間距 120（v181）',
    '240 + (i - (slots.length - 1) / 2) * 120' in play_fn)
chk('C1 won 路 slot 唔受中央移位影響（只喺 3 slots 先減）',
    'slots.length === 3' in play_fn)

# --- C2：glamour 174px 隱藏卡列空帶 ---
hide_css = css_rule('.awd63-cards.glamour-hide')
chk('C2 glamour-hide 改 display:none（frame 收短）', 'display:none' in hide_css)
chk('C2 唔再 visibility:hidden 留位', 'visibility:hidden' not in hide_css)
chk('C2 syncGlamour 仍然係單一 choke point（跟 overlay 同條件）',
    'classList.toggle("glamour-hide", !!(b && b.id === "glamour"))' in play_fn)
chk('C2 下一 beat 恢復機制仲在（toggle，唔係單向加）',
    play_fn.count('syncGlamour(beats[') == 2)

# --- 唔郁守衛 ---
chk('提名卡人像唔掂（cardsData／cardsHtml 仲在）', 'cardsData' in play_fn and 'cardsHtml' in play_fn)
chk('提名卡結構唔變（awd63-card／me 標記仲在）', 'awd63-card' in play_fn)
chk('SAVE key 唔變（starVolunteer_map_v19w）', 'starVolunteer_map_v19w' in src)
chk('softRev 唔變', 'softRev' in src)
chk('掌聲 MP3 唔喺呢票（M9 觸發點仲在）', 'awards160PlayWinAudio' in play_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
