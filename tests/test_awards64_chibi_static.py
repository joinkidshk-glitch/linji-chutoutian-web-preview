# v20a181：Q 版池成批清走 static tests（原 v20a64「Q版群星」檔成份改寫）。
# v181 起人物改用 PixelLab character 幀（assets/story/awards/px_<starId>_<dir>.png，south 企立／
# east／west 行入場跟方向；12 人 × 3 向，全部腳底 y115 對齊 v180 錨；dispH 112，人物約 89px）。
# AWARDS64_SPRITES（34 張 base64）＋loadSpr／drawSpr 路徑一併刪，唔留 fallback；載唔到畫中性剪影。
# (1) Q 版資產已撤：AWARDS64_SPRITES const 唔存在、play 內冇 base64 池。
# (2) v63 寫實 sprite 繼續撤走（AWARDS63_SPRITES const 唔存在）。
# (3) 走路入場接線：entryPlan（左右兩流）＋east／west 幀引用＋reveal 行前 fwd64。
# (4) 渲染尺度 v181：FLOOR=262、slotCx 置中 240／間距 120、人物高 112（玩家 116）。
# (5) 提名卡統一規則仲喺度（v64 B 部分，同 test_awards64_static.py 互補抽查）。
# 反證：run against pristine main 91f264a -> 「已撤」斷言全部 FAIL（Q 版池仲在），唔 crash；
#   接線／尺度新斷言同樣 FAIL；卡片守衛 pristine 應 PASS。
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

# --- (1) Q 版資產已撤 ---
play_fn = slice_fn('awards62PlayCeremony')
chk('AWARDS64_SPRITES 常數已撤', 'const AWARDS64_SPRITES' not in src)
chk('Q 版 base64 池已撤（play 內冇 data:image/png）', 'data:image/png;base64' not in play_fn)
chk('loadSpr／drawSpr 路徑已撤（play 範圍；退役註解提及除外）', 'loadSpr' not in play_fn and 'drawSpr' not in play_fn)
chk('舊 walkA／walkB 幀值已撤', '"walkA"' not in src and '"walkB"' not in src)
chk('Q 版標記剩低只係退役註解（v20a64 AWARDS64 一詞只出現喺註解）',
    src.count('AWARDS64') <= 3)

# --- (2) v63 寫實資產繼續撤走 ---
chk('AWARDS63_SPRITES 已撤', 'const AWARDS63_SPRITES' not in src)
chk('舊衍生標記（縮 72px）已撤', '縮 72px' not in src)

# --- (3) 走路接線（PixelLab 幀） ---
chk('play 載入 PixelLab 幀（loadPx）', 'loadPx' in play_fn and 'px_" + starId' in play_fn)
chk('入場計劃 entryPlan（兩流深位先行）', 'entryPlan' in play_fn and 'rank * 380' in play_fn)
chk('east／west 行幀有被引用', '"east"' in play_fn and '"west"' in play_fn and 'o.frame' in play_fn)
chk('enter beat 用側面幀行入', 'id === "enter"' in play_fn and 'frame: (p.side < 0) ? "east" : "west"' in play_fn)
chk('reveal 得獎者行前（fwd64）', 'fwd64' in play_fn and 'moving' in play_fn)
chk('中性剪影降級保留（唔係 Q 版比例）', '中性剪影' in play_fn and 'Q 版比例' not in play_fn)
chk('跳過掣保留', 'awd62-skip' in play_fn)

# --- (4) 渲染尺度（v181） ---
chk('地板線 FLOOR=262（木地板 y200–334）', 'const FLOOR = 262' in play_fn)
chk('slotCx 置中 240／間距 120', '240 + (i - (slots.length - 1) / 2) * 120' in play_fn)
chk('人物高度 112／玩家 116', '? 116 : 112' in play_fn)

# --- (5) 卡片統一規則抽查 ---
chk('唱名卡海報 2:3 框', 'aspect-ratio:2/3' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
