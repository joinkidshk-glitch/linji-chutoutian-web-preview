# v20a184 修 v182 設計 review 新 C1＋C2 static tests：
# C1：三張提名卡漸變第二 stop 全場同一隻 #241736，卡面下半（約 40% 面積）三張一模一樣——
#     每隻 tint 配返同色系深色第二 stop（按 index 對位，紫卡 keep #241736），成張卡面都帶 tint；
#     色板數量／第一 stop／卡面文字唔郁；得主標記（win 金框＋🏆角標）唔郁。
# C2：同一場 pack 獎項次序兩次實駕唔同——根源係 buildAwardResultPack 每次 build 都
#     Fisher-Yates shuffle 啲 categories 再 slice。修法係呈現層固定排序（按獎項 id，
#     awardsCatsSorted184，slice  copy 唔郁原 pack），請柬「今晚獎項」行＋結果卡同用；
#     pack 數據／content JSON／判定一字唔郁。
# 反證: run against pristine main (6ed68f8) index -> C1/C2 全部未入 -> FAIL（唔 crash）。
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

def hexes(text):
    return re.findall(r'"(#[0-9a-f]{6})"', text)

def lum(h):
    r, g, b = (int(h[i:i+2], 16) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

play_fn = slice_fn('awards62PlayCeremony')
invite_fn = slice_fn('renderAwardInviteHtml')
result_fn = slice_fn('renderAwardResultHtml')
sorted_fn = slice_fn('awardsCatsSorted184')
build_fn = slice_fn('buildAwardResultPack')

# --- C1：同色系深色第二 stop ---
_tints = re.search(r'AWDS63_TINTS182 = \[[^\]]*\]', play_fn)
_deeps = re.search(r'AWDS63_DEEPS184 = \[[^\]]*\]', play_fn)
chk('C1 深色 palette AWDS63_DEEPS184 在位（6 色，對位 tints）', bool(_deeps) and len(hexes(_deeps.group(0))) == 6)
chk('C1 tint palette 唔郁（仍係原 6 色）', bool(_tints) and hexes(_tints.group(0)) == ['#3a2a4a', '#274a3a', '#4a2a2e', '#2a3a4a', '#4a3a20', '#33355e'])
if _tints and _deeps:
    tints = hexes(_tints.group(0))
    deeps = hexes(_deeps.group(0))
    chk('C1 三張實駕卡第二 stop 各不相同（紫 #241736／綠深綠／酒紅深紅）', len(set(deeps[:3])) == 3)
    chk('C1 紫卡第二 stop keep #241736', deeps[0] == '#241736')
    chk('C1 綠／酒紅卡第二 stop 唔再係 #241736', deeps[1] != '#241736' and deeps[2] != '#241736')
    chk('C1 六隻 deep 全部各不相同', len(set(deeps)) == 6)
    chk('C1 每隻 deep 都比對位 tint 深（同色系暗版，唔係另一隻淺色）', all(lum(d) < lum(t) for d, t in zip(deeps, tints)))
chk('C1 漸變用 deep 變量（唔再寫死 #241736）', "linear-gradient(160deg,' + tint182 + ',' + deep184" in play_fn)
chk('C1 deep 按卡位 index 揀（同 tint 對位）', 'AWDS63_DEEPS184[ci % AWDS63_DEEPS184.length]' in play_fn)
chk('C1 卡面文字唔郁（首字＋全名＋媒介細行）', 'awd63-cssmono' in play_fn and 'awd63-cssstar' in play_fn and 'awd63-cssmed' in play_fn)
chk('C1 得主標記 CSS 唔郁（win 金框＋me）', '.awd63-card.me' in src and '.awd63-card.win' in src)

# --- C2：呈現層固定排序 ---
chk('C2 排序 helper awardsCatsSorted184 在位', bool(sorted_fn))
chk('C2 helper 按獎項 id 排序', '.id' in sorted_fn and 'localeCompare' in sorted_fn)
chk('C2 helper slice copy、唔郁原 pack', '.slice()' in sorted_fn and 'pack.categories' in sorted_fn)
chk('C2 請柬「今晚獎項」行用固定排序', '今晚獎項' in invite_fn and 'awardsCatsSorted184(pack)' in invite_fn)
chk('C2 結果卡同用固定排序', 'awardsCatsSorted184(pack)' in result_fn)
chk('C2 請柬獎項集合／文案唔郁（label 照 join）', '.label' in invite_fn and '、' in invite_fn)
chk('C2 build 層評估次序唔郁（shuffle 段原封，淨呈現層排）', 'shuffled' in build_fn and 'Math.random()' in build_fn)
chk('C2 唔直改 content pack（index 無 content/ 寫入）', 'content/STUB_AWARDS' not in src and 'content/SCHEMA_AWARDS' not in src)

# --- 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變（s107）', 's107' in src)
chk('產品 ?v 不變（v20a10）', 'v20a10' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
