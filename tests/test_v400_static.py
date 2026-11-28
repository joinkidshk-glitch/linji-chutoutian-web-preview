# v424 意圖更新：日期行收空格令 14px 一行入鏡，總數資訊不變。
# v20a400 細改 1–3 靜態釘：預設唔再自動揀課／唔再因壓力靜靜換休息；建議列＋成本行接線在位。
# 內容錨點（唔釘行號，免漂移）；行為驗證見 tests/test_v400_logic.js＋真駕。
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

# ① 預設：訓練位預填自由日，自動揀課＋壓力靜靜換休息已刪
dwp = slice_fn('defaultWeekPlan')
chk('① 訓練位預填自由日', 'plan[1] = "scout_all"' in dwp)
chk('① 自動揀課已刪（pick360／acting<2 分支）', 'pick360' not in dwp and 'actingN' not in dwp)
chk('① 壓力靜靜換休息已刪', 'stress384' not in dwp and 'stress379' not in dwp and '>= 60' not in dwp)
chk('① 第 1 週返 base', 'if(w<=1) return base;' in dwp)
chk('① 人情債留位維持', 'plan[4] = "scout_all"' in dwp)
chk('① 週日休息維持', 'plan[6] = "rest"' in dwp)

# ② 建議 helper：lowestStatTrain400（只限已報名課）＋weekStressPeak400（峰值計法保留）
low = slice_fn('lowestStatTrain400')
chk('② lowestStatTrain400 在位', 'function lowestStatTrain400' in low)
chk('② 建議候選只限已報名課', 'en[cid]' in low)
chk('② 建議唔再無條件包演技／歌藝', 'cid==="train_vocal"' not in low and 'cid==="train_acting"' not in low)
chk('② 建議鍵：最低屬性＋最少堂數', 'stat*1000 + cnt' in low)
chk('② 未報任何課 → null', 'return null' in low)
pk = slice_fn('weekStressPeak400')
chk('② weekStressPeak400 在位（峰值計法保留）', 'previewWeekStress' in pk and 'lockShootsIntoDraft' in pk)
chk('② 峰值預覽唔留 daysLeft 副作用', 'daysLeft = snap400' in pk)

# ③ 建議列＋成本行 HTML／CSS
chk('③ #nb-suggest400 在位', 'id="nb-suggest400"' in src)
chk('③ #nb-cost400 在位', 'id="nb-cost400"' in src)
chk('③ 建議列／成本行 CSS 在位', '.nb-suggest400' in src and '.nb-cost400' in src)
rs = slice_fn('renderSuggest400')
chk('③ renderSuggest400 在位', 'function renderSuggest400' in rs)
chk('③ 訓練建議：第 2 週起＋訓練位自由日', 'w400>=2' in rs and 'isMapDay(planDraft[1])' in rs)
chk('③ 沿用上次用 S.lastTrain400（舊檔無即隱藏）', 'S.lastTrain400' in rs)
chk('③ 補最低屬性用 helper', 'lowestStatTrain400()' in rs)
chk('③ 壓力建議：峰值 ≥60／≥80 兩粒掣', 'peak400>=60' in rs and 'peak400>=80' in rs)
chk('③ 壓力建議目標日＝第一個未鎖定自由日', 'freeDays400()' in rs)
chk('③ 建議掣套用先換（唔自動換）', 'planDraft[1] = last400' in rs and 'planDraft[t400] = "rest"' in rs)
chk('③ 建議掣唔郁拍攝鎖位', 'dayPlanLocked(planDraft[1])' in rs and 'dayPlanLocked(planDraft[t400])' in rs)
rn = slice_fn('renderNotebook')
chk('③ renderNotebook 掛建議列', 'renderSuggest400(editable)' in rn)
chk('③ renderNotebook 唔清成本行（唔寫 #nb-cost400）', 'getElementById("nb-cost400")' not in rn)

# ④ 改格記錄 lastTrain＋成本行
th = slice_fn('train71HandleClick')
chk('④ 訓練揀課記 lastTrain400', 'S.lastTrain400 = cid' in th)
chk('④ 訓練揀課出成本行', 'showCost400(from400, cid, planSelDay)' in th)
chk('④ 通用改格記 lastTrain400', 'S.lastTrain400 = it.id' in rn)
chk('④ 通用改格出成本行', 'showCost400(from400, it.id, planSelDay)' in rn)
cl = slice_fn('costLine400')
chk('④ 成本行文案在位（失去／得到）', 'costLose400' in cl and 'costGain400' in cl)
chk('④ 成本行：街演 $35–60／咖啡 $45–75', '"失去約 $35–60 收入"' in src and '"失去約 $45–75 收入"' in src)
chk('④ 成本行：休息壓力清零', '"得到壓力清零"' in src)
chk('④ 成本行：訓練學費 $20', '學費 $20' in src)
sc = slice_fn('showCost400')
chk('④ showCost400 寫 #nb-cost400', 'getElementById("nb-cost400")' in sc)

# ⑤ 日格 hint＋細行進度
chk('⑤ 日格 hint 用 nbDayHint400', 'nbDayHint400(i, meta, editable, locked)' in rn)
nh = slice_fn('nbDayHint400')
chk('⑤ 訓練格 hint：再 N 堂升 X 級／已到三級', '再 " + nx400.left + " 堂升' in nh and '已到三級' in nh)
chk('⑤ 外出日 hint：本週外出機會剩X日', '本週外出機會剩" + n423 + "日' in slice_fn('nbMapTotal400'))
mini = slice_fn('train71CourseMini')
chk('⑤ 細行加升下一級進度', 't70-mprog' in mini and 'prog75m' in mini)

# ⑥ save 跟走＋新週清成本行
sq = slice_fn('saveQ')
chk('⑥ saveQ 全 S 序列化（lastTrain400 跟 save 走）', 'JSON.stringify(S)' in sq)
eh = slice_fn('enterHome')
chk('⑥ 新一週新底稿清成本行', 'getElementById("nb-cost400")' in eh)

print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
