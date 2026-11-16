# v20a63 頒獎禮群星版 static tests:
# (1) 舊手繪 pixel map 全撤（PAL62／SPR_STAND／SPR_HOLD／DrawSprite／紅呔格 WWRRWW 一律唔准返嚟）。
# (2) sprite 資產：v63 原 AWARDS63_SPRITES（寫實 12 張）；v20a64 起成套換做 AWARDS64_SPRITES Q 版 34 張；
#     v20a181 起 Q 版池成批清走，改做 PixelLab character 幀（assets/story/awards/px_<starId>_<dir>.png，
#     south／east／west；12 人 × 3 向，腳底 y115）。
# (3) 紅線：fellows 唔用冇 sprite 嘅星（程天諾唔入 POSTER59_STAR_IDS）；池抽已刪（D-v2-2）。
# (4) fellows 接線齊：build pack／log／請柬／結果卡／獎項頁／play（作品卡＋glamour＋對手捧杯）。
# (5) 海報唔重複編碼：B3 已刪 POSTER59_DATA（D-12 新庫 posterBrief 出圖先恢復）；
#     新 code 只經 poster59Path 重用（stub 一律回空字串，各顯示位用 CSS 卡降級）。
# (6) 硬規則：SAVE key 不變、v62 評分公式（WIN_LINE）冇郁。
# 反證: run against a pre-v63 index -> AWARDS63 block missing -> FAIL.
import sys, re, os

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

# --- (2) 資產本體 ---
chk('AWARDS63 區塊標記在位', 'v20a63 AWARDS63' in src)
chk('AWARDS64_SPRITES 已撤（v181：改 PixelLab 幀）', 'const AWARDS64_SPRITES' not in src)
chk('AWARDS63_SPRITES 舊寫實資產已撤', 'const AWARDS63_SPRITES' not in src)
chk('AWARDS63_POOL 已刪（D-v2-2，fellows 只讀 cast／singer／host）', 'const AWARDS63_POOL' not in src)
chk('AWARDS63_TIER_WEIGHT 已刪（D-v2-2）', 'const AWARDS63_TIER_WEIGHT' not in src)
chk('awards63WeightedPick 已刪（D-v2-2）', 'function awards63WeightedPick(' not in src)
chk('fellows 函數在位（v20a204：簽名加可選 gender＋catId）', 'function awards63Fellows(ceremony, year, gender, catId)' in src)
chk('focus 函數在位', 'function awards63FocusCat(pack)' in src)
PX_DIR = os.path.join(os.path.dirname(os.path.abspath(idx_path)), 'assets', 'story', 'awards')
PX_IDS = ['awei', 'luk_baakyin', 'liu_bingxing', 'chai_zanhoi', 'mak_zhendong', 'lok_gasing',
          'chung_choning', 'so_jiyan', 'ngai_wingnaam', 'gu_mingfai', 'yip_manji', 'ko_chunkit']
chk('PixelLab 幀齊 36 檔（12 人 × south／east／west）',
    all(os.path.isfile(os.path.join(PX_DIR, 'px_%s_%s.png' % (sid, d))) for sid in PX_IDS for d in ('south', 'east', 'west')))
chk('play 內冇 Q 版 base64 池', 'data:image/png;base64' not in slice_fn('awards62PlayCeremony'))

# --- (1) 舊手繪 map 全撤 ---
chk('舊 PAL62 已撤', 'AWARDS62_PAL62' not in src)
chk('舊 SPR_STAND／SPR_HOLD 已撤', 'AWARDS62_SPR_STAND' not in src and 'AWARDS62_SPR_HOLD' not in src)
chk('舊 DrawSprite 已撤', 'awards62DrawSprite' not in src)
chk('舊手繪格（含紅呔 WWRRWW）已撤', 'WWRRWW' not in src)

# --- (3) 紅線：fellows 唔用冇 sprite 嘅星；池抽已刪 ---
fellows_fn63 = slice_fn('awards63Fellows')
star_ids63 = slice_const('POSTER59_STAR_IDS')
chk('紅線：程天諾唔入 POSTER59_STAR_IDS（1988 零出場紅線）', 'ching_tinlok' not in star_ids63)
chk('fellows 按格讀 cast／singer／host（awards63CatSlot＋slot.kind）',
    'function awards63CatSlot(' in src and 'awards63CatSlot' in fellows_fn63 and 'slot.kind' in fellows_fn63)
chk('fellows 有 sprite 閘（awards63HasSprite）', 'awards63HasSprite' in fellows_fn63)

# --- (4) 接線 ---
build_fn = slice_fn('buildAwardResultPack')
chk('build pack 衍生 fellows＋winner63', 'awards63Fellows' in build_fn and 'fellows63' in build_fn and 'winner63' in build_fn)
chk('build pack 有 repGigId63', 'repGigId63' in build_fn)
log_fn = slice_fn('commitAwardToLog')
chk('awardsLog 只加 fellows63／winner63 欄', 'fellows63' in log_fn and 'winner63' in log_fn)
invite_fn = slice_fn('renderAwardInviteHtml')
chk('請柬用 awards63InviteBitHtml（細海報＋同屆提名）', 'awards63InviteBitHtml' in invite_fn)
inv_bit = slice_fn('awards63InviteBitHtml')
chk('請柬細海報經 poster59Path 重用＋84px class', 'poster59Path' in inv_bit and 'awd63-invite-poster' in inv_bit and '.awd63-invite-poster{width:84px' in src)
result_fn = slice_fn('renderAwardResultHtml')
chk('結果卡有同屆提名行', 'awards63FellowsHtml' in result_fn)
pane_fn = slice_fn('renderAwardsPane62')
chk('獎項頁顯示同屆提名', 'fellowsTxt' in pane_fn and 'fellows63' in pane_fn)
play_fn = slice_fn('awards62PlayCeremony')
chk('動畫載 PixelLab 幀（loadPx）', 'loadPx' in play_fn and 'px_" + starId' in play_fn)
chk('動畫有中性剪影降級', 'drawPx' in play_fn and '中性剪影' in play_fn)
chk('唱名作品卡列（DOM）', 'awd63-cards' in play_fn and 'awd63-card' in play_fn)
chk('玩家卡有金框「你」標記 CSS', '.awd63-card.me' in src and 'content:"你"' in src)
chk('glamour 海報層', 'awd63-glamour' in play_fn and '.awd63-glamour' in src)
chk('對手捧杯（trophy glyph）', 'drawTrophyGlyph' in play_fn)
chk('懸念掃光（suspense lit slot）', 'lightPool' in play_fn and 'lit' in play_fn)
beats_fn = slice_fn('awards62CeremonyBeats')
chk('beats：入圍唱得主、glamour 只限有海報得獎', 'winner63' in beats_fn and 'glamour' in beats_fn and 'poster59Path' in beats_fn)
chk('beats：旁聽用 pan 群星鏡頭', '"pan"' in beats_fn)
chk('beats：旁聽行埋宣佈弧（names/suspense/reveal，v20a147）', 'gLines' in beats_fn and 'gReveal' in beats_fn)
chk('beats：入圍落選有 comfort 安慰 beat（v20a147）', '"comfort"' in beats_fn and '何生拍拍你膊頭' in beats_fn)
chk('對手唔再加權（fellows 入面無 AWARDS63_TIER_WEIGHT／awards63WeightedPick／seeded draw）',
    'AWARDS63_TIER_WEIGHT' not in fellows_fn63 and 'awards63WeightedPick' not in fellows_fn63 and 'awards63SeededRng' not in fellows_fn63)
chk('fellows 確定性：唔用裸 Math.random（按片酬序，唔係 seeded draw）', 'Math.random' not in fellows_fn63)

# --- (5) 海報唔重複編碼 ---
chk('B3 POSTER59_DATA 已刪（0 份，D-12 先恢復）', src.count('const POSTER59_DATA') == 0)
chk('海報全經 poster59Path 取用（新 code 冇另嵌海報圖）', src.count('poster59Path') >= 6)

# --- (6) 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('v62 贏線 v147 重做校準值 0.875（唔係舊 0.90）', 'const AWARDS62_WIN_LINE = 0.875' in src)
chk('v62 評分 parts 冇郁', 'function awards62ScoreParts(cat, ceremony, year)' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
