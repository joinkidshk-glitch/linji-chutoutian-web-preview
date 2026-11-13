# -*- coding: utf-8 -*-
# v20a79 ENC79 靜態測試：紅星巧遇 Phase 1——
# 一、框架在位（出沒盤／S.stars／風聲／攔截掛點／降格描寫／人脈頁紅星段）
# 二、處置表（刪後巷食煙＋打招呼、執漏改真功能、聽風聲改真資訊、事務所信任進度護欄）
# 三、遠觀掣退場（openLoc 唔再呼叫 addStarSighting 出掣）
# 四、紅線：新對白＋框架冇真人名／冇關海媚名／冇 1989 指向；SAVE key／softRev／?v= 不變
# 反證：喺 v20a78 index 上行會 FAIL（冇 ENC79 標記、遠觀掣仲喺度、死掣仲喺度）。
# 用法：python3 tests/test_enc79_static.py [path-to-index.html]
import re
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

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('NOTES_V20A79 在位', (p.parent / 'NOTES_V20A79_ENCOUNTER.md').exists())

# --- 一、框架 ---
ok('ENC79 模組標記在位', 'v20a79 ENC79：紅星巧遇系統 Phase 1' in src)
ok('名冊 12 星＋主場副場表', 'const ENC79_STARS =' in src and 'ching_tinlok' in src and 'chai_zanhoi' in src)
ok('S.stars lazy-init', 'function enc79EnsureStars()' in src and 'S.starDay' in src)
ok('出沒盤：日種子＋冷卻＋上限常數', 'ENC79_COOLDOWN = 3' in src and 'ENC79_DAILY_CAP = 1' in src and 'ENC79_WEEKLY_CAP = 2' in src and 'function enc79EnsureDay()' in src)
ok('好感：五段＋級數上限＋週軟頂', 'ENC79_FAV_CAPS = [30,55,80,100]' in src and 'ENC79_WEEK_SOFT_CAP = 10' in src and 'function enc79AddFav(' in src)
ok('風聲：grant＋傳聞頁來源「風聲」', 'function enc79GrantWhisper(' in src and 'source:"風聲"' in src)
ok('攔截掛點：openLoc 入面 encDone 繞過＋先行', 'opts.encDone' in src and 'enc79TryIntercept(id)' in src)
ok('主線壓制：storyPending 檢查在位', 'function enc79StoryPendingAt(' in src)
ok('初遇保底：主場 5 日計數', 'homeVisits' in src and '>=5' in src)
ok('對話殼：全屏 overlay＋企立候補＋場景底', 'enc79-overlay' in src and 'function enc79StandCandidates(' in src and 'function enc79SceneSrc(' in src)
ok('殺青掛點：resolvePlannedDay 入面 enc79OnWrap', 'enc79OnWrap(sh)' in src)
ok('人脈頁：紅星段＋未遇剪影＋範疇（唔畀名）', 'function enc79PeopleHtml()' in src and '？？？' in src and '常喺' in src)
ok('報紙花邊 → 風聲掛點', 'enc79PaperWhisper(row.id)' in src)

# --- 二、處置表 ---
i_ask = src.find('const MOCK_ASK =')
i_ask_end = src.find('let mockMergePick', i_ask)
ask = src[i_ask:i_ask_end]
ok('刪掣：後巷食煙／打招呼唔喺 MOCK_ASK', 'act_cha_alley_smoke' not in ask and 'act_ho_greet' not in ask)
ok('執漏：改真功能（冇假壓力、文案改幫手人情）', '壓力上升' not in ask and 'title:"幫手執漏"' in ask)
ok('執漏：冇幫忙嗰日唔出掣（mockAskDefs 過濾）', 'enc79HelpAvailable()' in seg('function mockAskDefs(', 'function journalText'))
ok('聽風聲：改名＋每日真資訊分支', 'title:"聽風聲"' in ask and 'function enc79AgencyWind(' in src and 'enc79AgencyWindDay' in src)
ok('飲茶：未持有保底分支', 'function enc79TeaListen(' in src and '未持有保底' in src)
# v20a105 統籌裁決：S-24（審計 A）刪事務所板結局配方句，同本護欄原意（信任進度要標明通去邊，否則 E5 行唔到）
# 分工調和——事務所只留信任數字＋下一階提示；「通去邊」改喺人情頁定性承載（renderDebtPane 江湖路指向）。
ok('護欄：事務所 loc-who 有何生信任進度（數字＋下一階提示）', 'enc79HoTrustLine()' in src and '何生信任：' in seg('function enc79HoTrustLine(', '/* ---------- 處置表', 3000))
ok('S-24 護欄：事務所信任行唔再攤結局配方（冇「江湖撈家」字樣）', '江湖撈家' not in seg('function enc79HoTrustLine(', '/* ---------- 處置表', 3000))
ok('護欄（105 裁決）：E5 指向喺人情頁定性承載（江湖路＋信任/清債/債權方向）', '江湖路' in seg('function renderDebtPane(', '', 6000) and '信任儲得夠深' in seg('function renderDebtPane(', '', 6000))
ok('護欄：聽風聲保留何生人情增益（bumpNpc agent）', 'bumpNpc("agent", 3+R(0,2))' in seg('function enc79AgencyWind(', '/* ----------', 4000))
ok('閘匙保留：茶餐廳三粒＋事務所采兒／守則', ask.count('grantsRumorId:') >= 5 and 'choi_recent_news' in ask and 'hau_ching_recent_news' in ask and 'gao_steal_spotlight' in ask)

# --- 三、遠觀退場 ---
ok('openLoc 唔再出遠觀掣', 'addStarSighting(L.id, add);' not in src)
ok('降格描寫掛點在位', 'enc79SheetPresence(L.id)' in src)

# --- 四、對白量同紅線（只掃 ENC79 新增段：四星 DLG＋模組） ---
dlg_blocks = []
for sid in ['luk_baakyin', 'liu_bingxing', 'mak_zhendong', 'yip_manzi']:
    i = src.index('const ENC79_DLG_' + sid + ' =')
    j = src.index('\nconst ', i + 10)
    dlg_blocks.append(src[i:j])
total_lines = sum(b.count('["S",') + b.count('["A",') + b.count('["N",') for b in dlg_blocks)
print('四星對白句數（靜態計）:', total_lines)
ok('四星對白在位（每星 >= 90 句）', all((b.count('["S",') + b.count('["A",') + b.count('["N",') >= 90) for b in dlg_blocks))
ok('四星對白總數 >= 430', total_lines >= 430)
mod_seg = seg('/* ===== v20a79 ENC79', '/* ===== ENC79 模組完 ===== */', 300000)
# v20a176：ROM176 block 插喺 ENC79 模組段中間（殺青回望之前），入面有意寫關海媚（女角 prefs／對白），
# 唔係 ENC79 對白——紅線掃描要剔走 ROM176 段（ROM176 內容由 test_rom176_static 覆），頭尾兩截照掃。
_rom176_start = mod_seg.find('/* ===== v20a176 ROM176')
_rom176_end = mod_seg.find('/* ---------- 殺青回望', _rom176_start)
if _rom176_start >= 0 and _rom176_end > _rom176_start:
    mod_seg = mod_seg[:_rom176_start] + mod_seg[_rom176_end:]
ok('模組結束標記在位', len(mod_seg) > 20000)
new_text = ''.join(dlg_blocks) + mod_seg
ok('紅線：冇關海媚個名', '關海媚' not in new_text)
ok('紅線：冇 1989 年指向', '1989' not in new_text)
ok('紅線：冇真人名（抽查常見真名）', not any(n in new_text for n in ['周潤發','劉德華','張國榮','梅艷芳','成龍','周星馳','王祖賢','林青霞','張曼玉','梁朝偉','劉嘉玲','郭富城','黎明','張學友','譚詠麟','陳百強','黃家駒','無綫','TVB','邵逸夫','方逸華']))

print('\n' + ('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
