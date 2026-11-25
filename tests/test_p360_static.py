# v20a360 P0 三修靜態釘：① aud91PresentDue 自癒 ② genre 標籤授予＋舊檔回填 ③ defaultWeekPlan 輪替保底。
# 內容錨點（唔釘行號，免漂移）；行為驗證見 qa360/qa360_harness.js（28 項）＋真駕 qa360_drive3/5。
import re, sys

src = open('index.html', encoding='utf-8').read()
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    m = re.search(r'function ' + name + r'\s*\(', src)
    if not m:
        return ''
    i = src.index('{', m.start())
    d, j = 0, i
    while j < len(src):
        if src[j] == '{':
            d += 1
        elif src[j] == '}':
            d -= 1
            if d == 0:
                break
        j += 1
    return src[m.start():j + 1]

# ① 自癒：旗真＋mask 關 → 清旗；PresentOne 拋錯 → 剔單續呈現；done 冪等
apd = slice_fn('aud91PresentDue')
chk('① aud91PresentDue 自癒清旗在位', '_maskOn360' in apd and '_aud91Presenting = false;' in apd)
chk('① PresentOne 拋錯剔單續呈現', 'catch(_e360b)' in apd and 'filter(p=>p!==list[0])' in apd)
chk('① done 冪等守衛', '_done360' in apd)

# ② genre 授予表＋授予路＋回填
chk('② GIG_GENRE_TAG360 映射齊', '"喜劇":"tag_comedy"' in src and '"動作":"tag_action"' in src and '"武俠":"tag_action"' in src)
chk('② 動作替身授予 tag_action', 'g.roleLabel==="動作替身"' in src)
agt = slice_fn('applyGigTagOnComplete')
chk('② applyGigTagOnComplete 行 genre 授予', 'gigGenreTag360(g)' in agt)
bf = slice_fn('castingTagGenreBackfill360')
chk('② 回填函數在位（wrapHistory＋done_ 旗）', 'o.wrapHistory' in bf and 'done_' in bf)
chk('② 回填唔套雙軌（無 applyCastingTags／industryCreditDelta 寫入）',
    'applyCastingTags' not in bf and 'industryCreditDelta' not in bf)
chk('② normalizeSaveObj 掛回填', src.count('castingTagGenreBackfill360(o)') >= 1)
chk('② enterHome 懶掃掛回填', src.count('castingTagGenreBackfill360(S)') >= 1)

# ③ v20a400：輪替保底退役——defaultWeekPlan 唔再自動揀課，建議邏輯抽去 lowestStatTrain400（只限已報名課）。
dwp = slice_fn('defaultWeekPlan')
chk('③ v400 訓練位預填自由日', 'plan[1] = "scout_all"' in dwp)
chk('③ v400 自動揀課已刪（pick360）', 'pick360' not in dwp)
chk('③ v400 壓力靜靜換休息已刪', 'stress384' not in dwp and '>= 60' not in dwp)
low400 = slice_fn('lowestStatTrain400')
chk('③ v400 建議 helper 在位（只限已報名課）', 'en[cid]' in low400 and 'cid==="train_vocal"' not in low400)
chk('③ v400 最低屬性＋最少堂數鍵', 'stat*1000 + cnt' in low400)

print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
