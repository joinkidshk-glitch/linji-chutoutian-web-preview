# v20a188 頒獎獎項改名＋提名掛鈎 static tests：
# 新獎項表 15 個（覆寫表 AWARDS188_CATEGORIES，唔郁 content pack JSON）；舊 10 個 label／
# 舊 category id 喺 index.html 零殘留（TEXTFIX55 遷移表 keys 除外——嗰啲係舊文案對照鍵，
# 唔係玩家面獎項名，留返做舊檔遷移）；報紙模板兩款 win dek 已改新獎項名（VENUE99），
# 另加 AWARDS188_NP_WIN 覆寫表蓋晒 pack 8 款 win 模板嘅 headline／dek／clipLabel；
# 角色閘接線齊（awardsEvalTier／buildAwardResultPack／awardsMvpCategories／awardsStubCategory）；
# 唔郁嘅嘢：SAVE key、softRev s107、?v=v20a10、贏線 0.875、典禮 id／名、提名門檻數字。
# 反證: run against pristine main index -> 覆寫表／閘全部未入 -> FAIL（唔 crash）。
# 用法：python3 tests/test_awards188_static.py [path-to-index.html]
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

OLD_LABELS = ['年度廣告新面孔', '街外最記得住嘅一鏡', '街外最記得住的一鏡', '年度新人碟緣', '最受歡迎出鏡嗓',
              '影壇新面孔', '年度票房話題綠葉', '最佳電視新人', '最受歡迎螢幕面孔',
              '綜藝閃光綠葉', '最佳班底']
OLD_IDS = ['cat_newcomer_ad', 'cat_street_recall', 'cat_newcomer_disc', 'cat_popular_voice',
           'cat_newcomer_film', 'cat_box_talk', 'cat_newcomer_tv', 'cat_popular_face',
           'cat_variety_spark', 'cat_ensemble']
NEW_LABELS = ['最佳廣告男主角', '最佳廣告女主角', '最佳廣告男配角', '最佳廣告女配角',
              '最佳男歌手', '最佳女歌手', '最佳新人獎',
              '最佳男主角', '最佳女主角', '最佳男配角', '最佳女配角']
NEW_IDS = ['cat_ad_lead_m', 'cat_ad_lead_f', 'cat_ad_support_m', 'cat_ad_support_f',
           'cat_music_singer_m', 'cat_music_singer_f', 'cat_music_newcomer',
           'cat_film_lead_m', 'cat_film_lead_f', 'cat_film_support_m', 'cat_film_support_f',
           'cat_tv_lead_m', 'cat_tv_lead_f', 'cat_tv_support_m', 'cat_tv_support_f']

table = slice_const('AWARDS188_CATEGORIES')

# --- 新表 15 個 ---
chk('新表：AWARDS188_CATEGORIES 在位', bool(table))
chk('新表：共 15 個獎項 id', table.count('id:"cat_') == 15)
chk('新表：四典禮齊（ad／music／film／tv）',
    all(k in table for k in ['award_harbour_ad', 'award_golddisc_music', 'award_harbour_film', 'award_singho_tv']))
chk('新表：15 個新 id 齊', all(i in table for i in NEW_IDS))
chk('新表：15 個新 label 齊', all(l in table for l in NEW_LABELS))
chk('新表：每獎有 winLine／loseLine／galleryLine（各 15）',
    table.count('winLine:') == 15 and table.count('loseLine:') == 15 and table.count('galleryLine:') == 15)
chk('新表：role 欄齊（lead／support／singer／newcomer）',
    all(r in table for r in ['role:"lead"', 'role:"support"', 'role:"singer"', 'role:"newcomer"']))
chk('新表：gender 欄齊（m／f／空）', 'gender:"m"' in table and 'gender:"f"' in table and 'gender:""' in table)
chk('新表：唔含舊組別後綴／舊人氣獎', '臨記組' not in table and '最受歡迎' not in table)
chk('新表：唔含 10 個舊生造名（＋街外一鏡嘅字變體）', all(o not in table for o in OLD_LABELS))

# --- 舊殘留零（TEXTFIX55 遷移表除外） ---
tf = slice_const('TEXTFIX55_EXACT')
live = src.replace(tf, '') if tf else src
chk('零殘留：舊 label 喺 live code 零（TEXTFIX55 遷移 keys 除外）',
    all(o not in live for o in OLD_LABELS))
chk('零殘留：10 個舊 category id 喺 index.html 零',
    all(i not in src for i in OLD_IDS))
chk('零殘留：舊組別後綴／舊人氣獎喺 live code 零（TEXTFIX55 除外）',
    '臨記組' not in live and '最受歡迎' not in live)

# --- 報紙模板 remap ---
chk('報紙：np_win_film_02 唔再寫舊獎名，改演員獎',
    '年度票房話題綠葉' not in src and '奪得演員獎' in src)
chk('報紙：np_win_music_02 唔再寫舊獎名，改憑歌聲奪獎',
    '最受歡迎出鏡嗓' not in src and '憑歌聲奪獎' in src)
# --- 報紙 win 模板覆寫表（pack 8 款，headline／dek／clipLabel） ---
NP_WIN_IDS = ['np_win_film_01', 'np_win_film_02', 'np_win_tv_01', 'np_win_tv_02',
              'np_win_music_01', 'np_win_music_02', 'np_win_ad_01', 'np_win_ad_02']
np_table = slice_const('AWARDS188_NP_WIN')
chk('報紙：AWARDS188_NP_WIN 在位，覆蓋 pack 8 款 win 模板',
    bool(np_table) and all(i in np_table for i in NP_WIN_IDS))
chk('報紙：NP 覆寫值唔含舊名／舊後綴／舊人氣獎',
    all(o not in np_table for o in OLD_LABELS)
    and '臨記組' not in np_table and '最受歡迎' not in np_table)
chk('報紙：NP 覆寫有 headline＋clipLabel（每款至少一個新 headline）',
    np_table.count('headline:') == 8 and np_table.count('clipLabel:') == 8)
chk('接線：load 嗰陣行 awards188ApplyNpOverlay（textfix55＋venue99 之後）',
    'awards188ApplyNpOverlay(FREEPLAY_FW)' in src
    and 'function awards188ApplyNpOverlay(' in src
    and 'award_win' in slice_fn('awards188ApplyNpOverlay'))

# --- 角色閘接線 ---
eval_fn = slice_fn('awardsEvalTier')
build_fn = slice_fn('buildAwardResultPack')
mvp_fn = slice_fn('awardsMvpCategories')
stubcat_fn = slice_fn('awardsStubCategory')
gate_fn = slice_fn('awards62GateLineHtml')
chk('接線：awardsEvalTier 提名分支過角色閘（awards188EligibleCats）',
    'awards188EligibleCats' in eval_fn and 'roleOk188' in eval_fn)
chk('接線：buildAwardResultPack 提名池用 eligible（pool188）',
    'pool188' in build_fn and 'awards188EligibleCats' in build_fn)
chk('接線：awardsMvpCategories 覆寫表優先', 'AWARDS188_CATEGORIES' in mvp_fn)
chk('接線：awardsStubCategory 覆寫表優先（label／lines 由新表出）',
    'AWARDS188_CATEGORIES' in stubcat_fn)
chk('接線：角色閘函數齊（WorkRole／IsLead／IsSupport／HadEarlierWork／CatEligible／EligibleCats）',
    all(n in src for n in ['function awards188WorkRole(', 'function awards188IsLead(',
                           'function awards188IsSupport(', 'function awards188HadEarlierWork(',
                           'function awards188CatEligible(', 'function awards188EligibleCats(']))
chk('接線：主角判準沿用既有 helper（end95IsLead＋awards65IsLeadWork，唔另起一套）',
    'end95IsLead' in slice_fn('awards188IsLead') and 'awards65IsLeadWork' in slice_fn('awards188IsLead'))
chk('接線：替身 guard 在位（替身唔係主角／配角）',
    slice_fn('awards188IsLead').count('替身') >= 2 and '替身' in slice_fn('awards188IsSupport'))
chk('接線：請柬門檻行講明角色閘原因', '未做過主角／配角級作品' in gate_fn and '未唱過歌' in gate_fn)
chk('接線：__awards 暴露 table188／eligible188（實駕探針用）',
    'table188' in src and 'eligible188' in src)

# --- 唔郁嘅嘢 ---
chk('唔郁：SAVE key（starVolunteer_map_v19w）', 'starVolunteer_map_v19w' in src)
chk('唔郁：softRev s107', 's107' in src)
chk('唔郁：產品 ?v=v20a10', 'v20a10' in src)
chk('唔郁：贏線 0.875', 'AWARDS62_WIN_LINE = 0.875' in src)
chk('唔郁：四典禮 id 齊', all(i in src for i in
    ['award_harbour_ad', 'award_golddisc_music', 'award_harbour_film', 'award_singho_tv']))
chk('唔郁：唔直改 content pack（index 無 content/ 寫入）',
    'content/STUB_AWARDS' not in src and 'content/SCHEMA_AWARDS' not in src)
chk('唔郁：提名門檻數字在位（yearMediumWrapsMin／stageVolumeMin 10／industryCreditMin 12）',
    'yearMediumWrapsMin' in eval_fn and 'stageVolumeMin:10' in src and 'industryCreditMin:12' in src)

print('\nFAILED: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
