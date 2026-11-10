# -*- coding: utf-8 -*-
# v20a83 ENC83 靜態測試：紅星巧遇 Phase 2＋T4 提攜——
# 一、基線不變（SAVE key／softRev／?v=）＋NOTES 在位
# 二、註冊在位（四星 DLG／FRAME const、ENC83 模組標記、advanceDay 借錢 tick 掛點）
# 三、接線在位（借錢入帳本／結算登記 favorDueSettled、提攜八星 grants、E4 時間閘、歌藝閘）
# 四、紅線：ENC83 新增段冇真人名／冇關海媚名／冇 1989 指向；借錢台詞唔寫死金額（gu_loan 段冇 $ 數字）
# 反證：喺 v20a82 index 上行會 FAIL（冇 ENC83 標記／對白）。
# 用法：python3 tests/test_enc83_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def seg(a, b, span=8000):
    i = src.find(a)
    if i < 0: return ''
    j = src.find(b, i + len(a)) if b else -1
    return src[i:j] if j > i else src[i:i + span]

P2 = ['ngai_wingnaam', 'gu_mingfai', 'lok_gasing', 'chai_zanhoi']

# --- 一、基線 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('NOTES_V20A83 在位', (p.parent / 'NOTES_V20A83_ENCOUNTER_P2.md').exists())

# --- 二、註冊 ---
ok('ENC83 對話數據標記在位', 'v20a83 ENC83 對話數據：紅星巧遇 Phase 2 四星' in src)
ok('ENC83 模組標記在位', 'v20a83 ENC83：紅星巧遇 Phase 2' in src and '/* ===== ENC83 模組完 ===== */' in src)
for sid in P2:
    ok('對白 const 在位：' + sid, ('const ENC83_DLG_' + sid + ' =') in src and ('const ENC83_FRAME_' + sid + ' =') in src)
    ok('註冊入 ENC79_DIALOG／PILOT：' + sid, ('ENC79_DIALOG.' + sid + ' = ENC83_DLG_' + sid) in src and ('ENC79_PILOT.' + sid + ' = 1') in src)
ok('advanceDay 掛 enc83GuLoanTick（同 favorDueTick 並列）', 'enc83GuLoanTick();' in src)

# --- 三、接線 ---
mod = seg('/* ===== v20a83 ENC83：紅星巧遇 Phase 2', '/* ===== ENC83 模組完 ===== */', 300000)
ok('模組段抽取成功（>8KB）', len(mod) > 8000)
ok('借錢：入 mockCredits 帳本（credit_enc83_gu_loan）＋身家比例金額', 'credit_enc83_gu_loan' in mod and 'enc79GrantCredit' in mod and 'Math.min(5000' in mod)
ok('借錢：到期結算記入 favorDueSettled（ensureFavorDueSettled）', 'ensureFavorDueSettled()' in mod and 'repaid_loan' in mod and 'void_loan' in mod)
ok('借錢：冇另起 mockDebts 債系統（模組冇寫 mockDebts）', 'mockDebts' not in mod)
ok('提攜：八星 patron 節拍＋引薦債權齊', all(('credit_enc83_' + k + '_patron') in mod for k in ['luk','liu','mak','yip','ngai','gu','lok','chai']))
ok('提攜：Phase 1 四星專屬段 merge 入對白 beats', all((k + '_patron') in mod for k in ['luk','liu','mak','yip']))
ok('駱 E4 時間閘：lok_e4grudge 以 enc83NewsOut("E4") 為閘', 'lok_e4grudge' in mod and 'enc83NewsOut("E4")' in mod)
ok('駱和音閘：lok_help 歌藝 >= 35', 'lok_help' in mod and '>= 35' in mod)
ok('顧 N10 閘：gu_tease／gu_n10after 以 C9 為界', 'enc83NodeDone("C9")' in mod)
ok('齊回收閘：站隊旗 flag_side_*', 'flag_side_film' in mod and 'flag_side_tv' in mod and 'flag_side_undecided' in mod)

# --- 四、對白量同紅線 ---
dlg_blocks = []
for sid in P2:
    i = src.index('const ENC83_DLG_' + sid + ' =')
    j = src.index('\nconst ', i + 10)
    dlg_blocks.append(src[i:j])
counts = [(b.count('["S",') + b.count('["A",') + b.count('["N",')) for b in dlg_blocks]
print('Phase 2 四星對白句數（靜態計）:', counts, '總數', sum(counts))
ok('四星對白每星 >= 100 句', all(c >= 100 for c in counts))
ok('四星對白總數 >= 470', sum(counts) >= 470)
new_text = ''.join(dlg_blocks) + mod
ok('紅線：冇關海媚個名', '關海媚' not in new_text)
ok('紅線：冇 1989 年指向', '1989' not in new_text)
ok('紅線：冇真人名（抽查常見真名）', not any(n in new_text for n in ['周潤發','劉德華','張國榮','梅艷芳','成龍','周星馳','王祖賢','林青霞','張曼玉','梁朝偉','劉嘉玲','郭富城','黎明','張學友','譚詠麟','陳百強','黃家駒','無綫','TVB','邵逸夫','方逸華']))
# 借錢段台詞唔寫死金額：gu_loan beat 段內冇 $ 符號數字
i = src.index('gu_loan: {')
gu_loan_seg = src[i:i + 6000]
ok('借錢台詞唔寫死金額（gu_loan 段冇 $）', '$' not in gu_loan_seg)

print('\n' + ('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
