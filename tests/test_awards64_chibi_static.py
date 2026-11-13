# v20a64「Q版群星」整合 static tests:
# (1) Q 版資產在場：AWARDS64_SPRITES 共 34 張（企姿 11＋阿偉捧杯 1＋全員行 A/B 22），base64 ≤130KB。
# (2) v63 寫實 sprite 成套撤走：AWARDS63_SPRITES const 唔存在、舊衍生標記（縮 72px）已改。
# (3) 走路入場接線：entryPlan（左右兩流）＋walkA/walkB 幀引用＋reveal 行前 fwd64。
# (4) 渲染尺度跟 mock v3：FLOOR=290（v20a174 B1：canvas 高 240→360，底圖垂直拉伸 1.5×，舞台頂線 193×1.5＝289.5→290；v20a170 P2 舊值 193）、slotCx 置中 202／間距 80＋gallery 中央 −36（C1）、人仔高 72（玩家 75）。
# (5) 提名卡統一規則仲喺度（v64 B 部分，同 test_awards64_static.py 互補抽查）。
# 反證: run against a pre-v64 index -> AWARDS64 block missing -> FAIL.
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

def slice_const(name):
    i = src.find('const ' + name + ' =')
    if i < 0: return ''
    depth = 0
    started = False
    for k in range(i, len(src)):
        ch = src[k]
        if ch in '{[': depth += 1; started = True
        elif ch in '}]':
            depth -= 1
            if started and depth == 0: return src[i:k+1]
        elif ch == ';' and not started:
            return src[i:k+1]
    return ''

# --- (1) Q 版資產 ---
chk('AWARDS64 區塊標記在位', 'v20a64 AWARDS64' in src)
spr = slice_const('AWARDS64_SPRITES')
STARS = ['luk_baakyin', 'liu_bingxing', 'chai_zanhoi', 'mak_zhendong', 'lok_gasing',
         'chung_choning', 'so_jiyan', 'ngai_wingnaam', 'gu_mingfai', 'yip_manji']
chk('企姿齊（阿偉＋捧杯＋10 星）', all(('"' + k + '":') in spr for k in ['awei', 'awei_hold'] + STARS))
chk('行幀齊（全員 walkA/walkB）', all(('"' + k + suf + '":') in spr for k in ['awei'] + STARS for suf in ('_walkA', '_walkB')))
chk('sprite 共 34 張', spr.count('data:image/png;base64') == 34)
b64len = sum(len(m) for m in re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)', spr))
chk('sprite base64 總量 ≤130KB（實際約 28KB）', 0 < b64len <= 130 * 1024)

# --- (2) v63 寫實資產全撤 ---
chk('AWARDS63_SPRITES 已撤', 'const AWARDS63_SPRITES' not in src)
chk('舊衍生標記（縮 72px）已撤', '縮 72px' not in src)

# --- (3) 走路接線 ---
play_fn = slice_fn('awards62PlayCeremony')
chk('play 載入 AWARDS64_SPRITES', 'AWARDS64_SPRITES' in play_fn)
chk('入場計劃 entryPlan（兩流深位先行）', 'entryPlan' in play_fn and 'rank * 380' in play_fn)
chk('walkA/walkB 幀有被引用', '_walkA' in play_fn and '_walkB' in play_fn and 'o.frame' in play_fn)
chk('enter beat 用 walk 幀行入', 'id === "enter"' in play_fn and 'frame: (tick % 2)' in play_fn)
chk('reveal 得獎者行前（fwd64）', 'fwd64' in play_fn and 'moving' in play_fn)
chk('剪影降級保留', '剪影降級（Q 版比例' in play_fn)
chk('跳過掣保留', 'awd62-skip' in play_fn)

# --- (4) 渲染尺度（mock v3） ---
chk('地板線 FLOOR=250（v20a177：拉伸後舞台頂線，底圖重構）', 'const FLOOR = 250' in play_fn)
chk('slotCx 置中 212／間距 100（v177）', '212 + (i - (slots.length - 1) / 2) * 100' in play_fn)
chk('人仔高度 72／玩家 75', '? 75 : 72' in play_fn)

# --- (5) 卡片統一規則抽查 ---
chk('唱名卡海報 2:3 框', 'aspect-ratio:2/3' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
