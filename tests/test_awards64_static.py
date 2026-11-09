# v20a64 提名作品卡尺寸統一 static tests:
# 用戶原話：「作品提名圖，應該大家尺寸是一樣的」。
# (1) 唱名卡列：海報圖固定 2:3 框 object-fit:cover 裁切，唔再 height:auto 跟原圖尺寸。
# (2) CSS 片名卡同框同高（aspect-ratio:2/3），唔再 min-height:100px。
# (3) 卡內文字行鎖高（片名 2 行高、星名 1 行高），長片名唔會撐高張卡。
# (4) 請柬細海報同樣 2:3 定框（84x126）。
# (5) 玩家卡金框只用 border-color/box-shadow，唔影響尺寸（原 v63 規則保留）。
# 反證: run against a pre-v64 (v63) index -> 上述規則未入 -> FAIL.
import sys

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def rule(sel):
    i = src.find(sel + '{')
    if i < 0: return ''
    j = src.find('}', i)
    return src[i:j + 1] if j > i else ''

img_rule = rule('.awd63-card img')
chk('唱名卡海報固定 2:3 框', 'aspect-ratio:2/3' in img_rule)
chk('唱名卡海報 cover 裁切', 'object-fit:cover' in img_rule)
chk('唱名卡海報唔再 height:auto', 'height:auto' not in img_rule)

css_rule = rule('.awd63-csscard')
chk('片名卡同框 2:3', 'aspect-ratio:2/3' in css_rule)
chk('片名卡唔再 min-height:100px', 'min-height:100px' not in css_rule)

t_rule = rule('.awd63-card .t')
chk('片名行鎖高（2 行）', 'height:30px' in t_rule and 'overflow:hidden' in t_rule)
s_rule = rule('.awd63-card .s')
chk('星名行鎖高（1 行）', 'height:15px' in s_rule and 'overflow:hidden' in s_rule)

inv_rule = rule('.awd63-invite-poster')
chk('請柬細海報 2:3 定框', 'width:84px' in inv_rule and 'height:126px' in inv_rule and 'object-fit:cover' in inv_rule)

me_rule = rule('.awd63-card.me')
chk('玩家卡金框唔改尺寸（只 border/box-shadow）', 'width' not in me_rule and 'height' not in me_rule and 'box-shadow' in me_rule)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
