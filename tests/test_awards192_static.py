# v20a192 修 v188 設計 review B1＋C1–C4・static tests：
# B1：AWARDS188_NP_WIN＋VENUE99_NP_DEK 生效文案零舊前提（8 款逐款掃描）；
#     music_02 唔郁；nominee 模板唔入覆寫表。
# C1：tv lead_m loseLine「還有」→「仲有」；全表 45 行再無「還有」。
# C2：awards62GateLineHtml 音樂分支刪走（「未唱過歌」唔再出現）；電影／電視閘句在位。
# C3：renderAwardResultHtml 用 focus 行先（awards63FocusCat＋移頭），其餘格維持
#     v184 id 固定排序（awardsCatsSorted184 仲在位）。
# C4：renderAwardInviteHtml gallery 分支列全 slate（AWARDS188_CATEGORIES＋觀禮標記）；
#     nominee 路徑仲用固定排序出 pack 類別。
# 唔郁嘅嘢：SAVE key、softRev s107、?v=v20a10、贏線 0.875、15 個獎項名／id、典禮 id。
# 反證: run against pristine main b7ca827 index -> v192 文案／邏輯未入 -> FAIL（唔 crash）。
# 用法：python3 tests/test_awards192_static.py [path-to-index.html]
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
        if ch in '{[':
            depth += 1; started = True
        elif ch in '}]':
            depth -= 1
            if started and depth == 0: return src[i:k+1]
        elif ch == ';' and not started:
            return src[i:k+1]
    return ''

# --- 反證守衛：v192 標記唔在就乾淨 FAIL，唔好逐項誤判 ---
NEED192 = ['阿偉憑實力跑出', '仲有下一場', '阿偉奪獎贏街坊票']
missing192 = [s for s in NEED192 if s not in src]
if missing192:
    for m in missing192:
        chk('反證：%s 唔存在（pristine main 預期，v192 未入）' % m, False)
    print('\nFAILED: %d' % len(fails))
    sys.exit(1)

# --- B1：贏獎報紙 8 款（覆寫表＋VENUE99 dek 兩行） ---
NP_WIN_IDS = ['np_win_film_01', 'np_win_film_02', 'np_win_tv_01', 'np_win_tv_02',
              'np_win_music_01', 'np_win_music_02', 'np_win_ad_01', 'np_win_ad_02']
np_table = slice_const('AWARDS188_NP_WIN')
venue_dek = slice_const('VENUE99_NP_DEK')
chk('B1：AWARDS188_NP_WIN 在位，覆蓋 pack 8 款 win 模板',
    bool(np_table) and all(i in np_table for i in NP_WIN_IDS))
BANNED = ['三句對白', '茶餐廳食面', '臨記生涯', '不殺之恩', '一句收工了', '綠葉',
          '和音', '合唱單曲', '涼茶', '跌低眼鏡', '特別獎']
chk('B1：NP 覆寫表零舊前提', all(b not in np_table for b in BANNED))
chk('B1：VENUE99 報紙 dek（film_02／ad_02）零舊前提',
    all(b not in venue_dek for b in BANNED))
chk('B1：music_01 唔寫「新人」（headline＋dek 都唔可以有新人二字）',
    '新人奪獎' not in np_table and '新人' not in
    np_table[np_table.find('np_win_music_01'):np_table.find('np_win_music_02')])
chk('B1：music_02 唯一乾淨款唔郁', '金碟夜 阿偉奪獎 樂壇多把靚聲' in np_table)
chk('B1：film_02／ad_02 dek 仲喺 VENUE99 嗰邊（奪得演員獎／奪得廣告獎）',
    '奪得演員獎' in venue_dek and '奪得廣告獎' in venue_dek)
chk('B1：nominee 模板唔入覆寫表（np_nom_* 零出現）', 'np_nom_' not in np_table)
chk('B1：8 款 clipLabel 全部「・得獎」新名', np_table.count('・得獎') == 8)

# --- C1 ---
cat_table = slice_const('AWARDS188_CATEGORIES')
chk('C1：cat_tv_lead_m loseLine 改「仲有下一場」',
    '名單滑過你個名——入圍咗，未抱盃。仲有下一場。' in cat_table)
chk('C1：全表 45 行再無書面語「還有」', '還有' not in cat_table)

# --- C2 ---
gate_fn = slice_fn('awards62GateLineHtml')
chk('C2：音樂閘句「嗰年未唱過歌」刪走', '未唱過歌' not in gate_fn)
chk('C2：電影／電視版閘句仲在位', '嗰年未做過主角／配角級作品，入圍唔到演員獎' in gate_fn)
chk('C2：音樂嗰陣唔推角色閘（medium music 守衛）',
    'music' in gate_fn and '坐觀禮席睇全場' in gate_fn)

# --- C3 ---
result_fn = slice_fn('renderAwardResultHtml')
chk('C3：結果卡用舞台 focus 行先（awards63FocusCat＋移頭）',
    'awards63FocusCat(pack)' in result_fn and 'unshift' in result_fn)
chk('C3：其餘格維持 v184 id 固定排序（awardsCatsSorted184 仲在位）',
    'awardsCatsSorted184(pack)' in result_fn)
chk('C3：同屆提名行邏輯唔郁（取第一個有 fellows63 嘅類別）',
    'felCat186' in result_fn and 'fellows63' in result_fn)

# --- C4 ---
invite_fn = slice_fn('renderAwardInviteHtml')
chk('C4：gallery 分支列全 slate（AWARDS188_CATEGORIES 表內次序＋觀禮標記）',
    'AWARDS188_CATEGORIES[pack.ceremonyId]' in invite_fn and '（觀禮）' in invite_fn)
chk('C4：gallery 分支只喺 tier gallery 先行（nominee 唔郁）',
    'pack.tier === "gallery"' in invite_fn)
chk('C4：nominee 路徑仲用固定排序出 pack 類別',
    'awardsCatsSorted184(pack)' in invite_fn)

# --- 唔郁嘅嘢 ---
chk('唔郁：SAVE key（starVolunteer_map_v19w）', 'starVolunteer_map_v19w' in src)
chk('唔郁：softRev s107', 's107' in src)
chk('唔郁：產品 ?v=v20a10', 'v20a10' in src)
chk('唔郁：贏線 0.875', 'AWARDS62_WIN_LINE = 0.875' in src)
chk('唔郁：15 個獎項 id 齊', all(i in cat_table for i in
    ['cat_ad_lead_m', 'cat_ad_lead_f', 'cat_ad_support_m', 'cat_ad_support_f',
     'cat_music_singer_m', 'cat_music_singer_f', 'cat_music_newcomer',
     'cat_film_lead_m', 'cat_film_lead_f', 'cat_film_support_m', 'cat_film_support_f',
     'cat_tv_lead_m', 'cat_tv_lead_f', 'cat_tv_support_m', 'cat_tv_support_f']))
chk('唔郁：四典禮 id 齊', all(i in src for i in
    ['award_harbour_ad', 'award_golddisc_music', 'award_harbour_film', 'award_singho_tv']))
chk('唔郁：唔直改 content pack（index 無 content/ 寫入）',
    'content/STUB_AWARDS' not in src and 'content/SCHEMA_AWARDS' not in src)

print('\nFAILED: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
