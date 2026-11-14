# v20a166 頒獎禮 glamour 並置＋空字幕框隱藏 static tests：
# B1（海報縮細並置）：
# (1) glamour overlay 由 stage 全幅改做只冚 canvas：absolute＋top:0／left:0／width:100%／aspect-ratio:480/432（v20a181：canvas 480×360；v20a207 B2：480×432），唔再 inset:0；
#     overlay 本身冇 0.93 暗底（暗層搬去右邊 panel），pointer-events:none（撳掣／elementFromPoint 照通 canvas）。
# (2) 右邊暗 panel：.awd63-glamour-panel flex:0 0 44%（左邊 56% 透明留位畀燕尾服；
#     燕尾服 4 slots 時 cx=180、dispH 112 → 右緣 (180+56)/480＝49.2%＜56%，喺 panel 左緣之外，v20a181 幾何），
#     暗底 rgba(10,6,18,.93) 留喺 panel；海報縮細（max-width:88%／max-height:60%，舊 76vw／330px／60vh 唔見）。
# (3) glamHtml 包 panel div；glamour 層搬入 .awd62-frame（canvas 之後、skip 掣之前），唔再係 stage 尾段全幅。
# C1（空 caption 隱藏字幕框）：
# (4) setCaption 單一 choke point：innerHTML 之後按 textContent.trim() 切換 style.display（空→none，有字→""）。
# (5) 空 caption beats 齊：walkup／glamour／won-out 係 ""；有字 beats（open／reveal／comfort）＋names（lines 填字）唔受影響。
# 反證：run against pristine main (276ffa1) -> B1／C1 斷言全部 FAIL（唔 crash）。
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

# --- B1 (1)：overlay 只冚 canvas ---
glam_css = css_rule('.awd63-glamour')
chk('B1 glamour overlay 在場', bool(glam_css))
chk('B1 overlay absolute＋top:0／left:0／width:100%', 'position:absolute' in glam_css and 'top:0' in glam_css and 'left:0' in glam_css and 'width:100%' in glam_css)
chk('B1 overlay aspect-ratio:480/432（對齊 canvas，v181；v20a207 B2）', 'aspect-ratio:480/432' in glam_css)
chk('B1 overlay 唔再 inset:0 全幅', 'inset:0' not in glam_css)
chk('B1 overlay 本身冇 0.93 暗底（暗層搬去 panel）', 'background:rgba(10,6,18,.93)' not in glam_css)
chk('B1 overlay pointer-events:none', 'pointer-events:none' in glam_css)
chk('B1 overlay 係 row 並置（flex-direction:row＋靠右）', 'flex-direction:row' in glam_css and 'justify-content:flex-end' in glam_css)
chk('B1 舊全幅置中 CSS 唔見', '.awd63-glamour{position:absolute;inset:0' not in src)

# --- B1 (2)：右邊暗 panel＋海報縮細 ---
panel_css = css_rule('.awd63-glamour-panel')
chk('B1 panel 在場', bool(panel_css))
chk('B1 panel 闊 44%（左邊 56% 透明留位畀燕尾服）', 'flex:0 0 44%' in panel_css)
chk('B1 0.93 暗層留喺 panel', 'background:rgba(10,6,18,.93)' in panel_css)
chk('B1 panel 係 column（海報上、cap 下）', 'flex-direction:column' in panel_css)
panel_img = css_rule('.awd63-glamour-panel>img')  # v20a174 A1：裱框規則收窄到直屬海報 img（>）
chk('B1 panel 海報 rule 在場（直屬 img，v174 A1）', bool(panel_img))
chk('B1 海報縮細（max-width:88%／max-height:calc(40cqh - 8px)，v20a190 新 C1 panel 縮短貼底；舊 40% 已由等價 cqh 式取代）', 'max-width:88%' in panel_img and 'max-height:calc(40cqh - 8px)' in panel_img and 'max-height:40%' not in panel_img)
chk('B1 舊大海報尺寸唔見（76vw／330px／60vh）', 'max-width:min(76vw,330px)' not in src and 'max-height:60vh' not in src)
chk('B1 海報金框＋光暈保留', 'border:4px solid #f2c14e' in panel_img and 'box-shadow:0 0 34px rgba(242,193,78,.45)' in panel_img)

# --- B1 (3)：glamHtml 包 panel＋搬入 frame ---
play_fn = slice_fn('awards62PlayCeremony')
chk('B1 glamHtml 包 .awd63-glamour-panel', '<div class="awd63-glamour"><div class="awd63-glamour-panel">' in play_fn)
chk('B1 glamHtml 仍有海報 img＋cap', 'posterOf(pack.repGigId63)' in play_fn and 'awd63-glamour' in play_fn)
inner_i = play_fn.find("stage.innerHTML = '<div class=\"awd62-frame\">'")
inner_block = play_fn[inner_i:inner_i+700] if inner_i >= 0 else ''
chk('B1 glamour 層喺 frame 入面（canvas 之後；v20a197 B3：skip 掣搬入 canvaswrap，喺 glamHtml 之前）',
    inner_block.find('awd62-canvas') < inner_block.find('awd62-skip') < inner_block.find('+ glamHtml'))
chk('B1 glamHtml 新位置（canvaswrap 閂標記之後；v20a197 B3：skip 掣搬入 wrap，喺閂標記之前）', 'awd62-skip">跳過 ⏩</button>\' + "</div>" + glamHtml' in play_fn)
chk('B1 walkup GIF 層已撤（v181：改由 canvas 畫，唔再係 stage 尾段 overlay）', '"</div>" + walkupHtml' not in play_fn and '.awd62-walkup160' not in src)
chk('B1 reveal／glamour／walkup／out 燕尾服唔郁（共 5 處，v187 C3 out 加一處）', play_fn.count('tuxedo: true') == 5)

# --- C1 (4)：setCaption 隱藏空框 ---
sc_i = play_fn.find('const setCaption')
sc_line = play_fn[sc_i:play_fn.find('\n', sc_i)] if sc_i >= 0 else ''
chk('C1 setCaption 在場', bool(sc_line))
chk('C1 setCaption 按 textContent 切換 display', 'style.display' in sc_line and 'textContent' in sc_line and 'trim()' in sc_line)
chk('C1 空→display:none，有字→display:""', '? "" : "none"' in sc_line)

# --- C1 (5)：空／有字 beats ---
beats_fn = slice_fn('awards62CeremonyBeats')
chk('C1 walkup beat caption 係空', 'id: "walkup", ms: 2200, caption: ""' in beats_fn)
chk('C1 glamour beat caption 係空', 'id: "glamour", ms: 1800, caption: ""' in beats_fn)
chk('C1 won-out beat caption 係空', 'id: "out", ms: 500, caption: ""' in beats_fn)
chk('C1 open beat 有字（唔會俾人隱藏）', 'id: "open", ms: 1200, caption: "' in beats_fn)
chk('C1 reveal 用 revealCap（有字）', 'caption: revealCap' in beats_fn)
chk('C1 comfort 有字', '差少少啫' in beats_fn)
chk('C1 names 經 lines 填字（唔係空 caption）', 'applyBeatCaption' in play_fn and '入圍名單' in play_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
