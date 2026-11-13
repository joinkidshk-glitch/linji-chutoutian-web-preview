# v20a63 頒獎禮群星版 static tests:
# (1) 舊手繪 pixel map 全撤（PAL62／SPR_STAND／SPR_HOLD／DrawSprite／紅呔格 WWRRWW 一律唔准返嚟）。
# (2) sprite 資產：v63 原 AWARDS63_SPRITES（寫實 12 張）；v20a64 起成套換做 AWARDS64_SPRITES Q 版 34 張；
#     v20a181 起 Q 版池成批清走，改做 PixelLab character 幀（assets/story/awards/px_<starId>_<dir>.png，
#     south／east／west；12 人 × 3 向，腳底 y115）。
# (3) 紅星池冇程天諾（1988 零出場紅線）。
# (4) fellows 接線齊：build pack／log／請柬／結果卡／獎項頁／play（作品卡＋glamour＋對手捧杯）。
# (5) 海報唔重複編碼：POSTER59_DATA 只得一份 const；新 code 只經 poster59Path 重用。
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
chk('AWARDS63_POOL 在位', 'const AWARDS63_POOL' in src)
chk('fellows 函數在位', 'function awards63Fellows(ceremony, year)' in src)
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

# --- (3) 紅線 ---
pool = slice_const('AWARDS63_POOL')
chk('紅星池冇程天諾 id', 'tinok' not in pool)
chk('池按四媒介齊（film/tv/music/ad）', all((m + ':') in pool for m in ['film', 'tv', 'music', 'ad']))

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
chk('對手加權：AWARDS63_TIER_WEIGHT＋seeded RNG＋weighted pick（v20a147）', 'AWARDS63_TIER_WEIGHT' in src and 'awards63SeededRng' in src and 'awards63WeightedPick' in src)
chk('對手加權：第二輪唔用裸 Math.random（seeded draw）', 'awards63SeededRng(awards63KeySeed' in src)

# --- (5) 海報唔重複編碼 ---
chk('POSTER59_DATA 只得一份', src.count('const POSTER59_DATA') == 1)
chk('海報全經 poster59Path 取用（新 code 冇另嵌海報圖）', src.count('poster59Path') >= 6)

# --- (6) 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('v62 贏線 v147 重做校準值 0.875（唔係舊 0.90）', 'const AWARDS62_WIN_LINE = 0.875' in src)
chk('v62 評分 parts 冇郁', 'function awards62ScoreParts(cat, ceremony, year)' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
