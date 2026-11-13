# v20a178 高俊傑上頒獎禮 static tests（淨入池邏輯；sprite 衍生已按用戶 2026-11-13 15:11 方向剝走，
# 舞台圖由 v180 接手「全部換做 PixelLab character 直接用」）：
# (1) v178 條款喺 awards63Fellows 入面：v178 標記＋1991 年閘＋ko_chunkit＋「高俊傑」直接寫名。
# (2) 池／權重唔郁：AWARDS63_POOL、AWARDS63_TIER_WEIGHT 入面冇 ko_chunkit。
# (3) 上限唔郁：awards63Fellows 入面仲有 out.length >= 3 兩輪封頂。
# (4) 舞台＋卡片行現行通用路徑，唔另起一套：舞台 loadPx(f.starId, d) 逐個 fellow 載 PixelLab 幀
#     （south／east／west 三向；v20a181 起 Q 版 loadSpr／walkA／walkB 成批退役）；
#     卡片 cardsData 用 fellows.forEach 通用 builder（poster 有就用 poster，冇就 CSS 卡）。
# v20a181 rebase 上 main 9640c6f（v183）更新：(4) 兩項由 loadSpr／walkA／walkB 改做 loadPx 三向幀，
# 其餘 v178 條款（入池／權重／上限／硬規則）唔郁。
# (5) 硬規則：SAVE key 不變；POSTER59_STAR_IDS 唔加高俊傑（嗰個 map 係海報／主演邏輯，唔係提名池）。
# 反證：對 pristine main 行 → v178 條款唔存在 → 乾淨 FAIL（exit 1，唔 crash）。
# Sprite 檢查已刪（用戶 2026-11-13 15:11：舞台直接用 PixelLab character，唔衍生 Q 版；
# 本票 sprite 三項檢查剝走，AWARDS64_SPRITES 返返 34 張基線，見 test_awards64_chibi_static.py）。
# 舞台人物圖由 v180 接手，唔喺本票驗。
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

fellows_fn = slice_fn('awards63Fellows')
play_fn = slice_fn('awards62PlayCeremony')
pool = slice_const('AWARDS63_POOL')
weights = slice_const('AWARDS63_TIER_WEIGHT')
star_ids = slice_const('POSTER59_STAR_IDS')

# --- (1) v178 條款在位 ---
chk('v178 標記喺 awards63Fellows 入面', 'v20a178' in fellows_fn)
chk('1991 年閘（year >= 1991）', '1991' in fellows_fn)
chk('特別名額 starId ko_chunkit', 'ko_chunkit' in fellows_fn)
chk('星名直接寫「高俊傑」', '高俊傑' in fellows_fn)

# --- (2) 池／權重唔郁 ---
chk('佢唔入 AWARDS63_POOL', 'ko_chunkit' not in pool)
chk('AWARDS63_TIER_WEIGHT 冇佢', 'ko_chunkit' not in weights)

# --- (3) 上限唔郁 ---
chk('兩輪封頂 out.length >= 3 仲喺度', 'out.length >= 3' in fellows_fn)

# --- (4) 舞台＋卡片行現行通用路徑 ---
chk('舞台逐個 fellow 載 PixelLab 幀（loadPx(f.starId, d) 通用）', 'loadPx(f.starId, d)' in play_fn)
chk('舞台載埋三向幀（south 企立／east／west 行，通用）', '["south", "east", "west"].forEach(d=> loadPx(f.starId, d))' in play_fn)
chk('卡片用 fellows 通用 builder（唔按 starId 分流）', 'fellows.forEach(f=> cardsData.push' in play_fn)
chk('卡片冇 poster 嗰陣跌返 CSS 卡（通用規則）', 'awd63-csscard' in play_fn)

# --- (5) 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('POSTER59_STAR_IDS 唔加高俊傑（海報／主演邏輯唔郁）', '高俊傑' not in star_ids)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
