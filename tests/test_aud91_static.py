# v20a91 AUD91 試鏡流程改版・靜態測試：接線標記／紅線／玩家面文案／NOTES。
# 用法：python3 tests/test_aud91_static.py [path-to-index.html]
# 反證：v90 index 冇 AUD91 標記、doAudition 仲係即場 scheduleShoot → 多項 FAIL。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end):
    i = html.index(start)
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

# ---- 紅線：SAVE key／softRev／?v= 不變 ----
ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('?v= 冇變', 'v=20a10' in html or '?v=20a10' in html or '20a10&softBehaviorGate' in html)

# ---- AUD91 模組在位 ----
ok('AUD91 模組標記', 'v20a91 AUD91' in html)
ok('AUD91 上限常量', 'const AUD91_CAP = 3' in html)
ok('pendingAud 新檔預設', 'pendingAud:[]' in html)
ok('aud91Log 新檔預設', 'aud91Log:[]' in html)
ok('舊檔載入安全預設', 'if(!Array.isArray(S.pendingAud)) S.pendingAud=[]' in html)

# ---- doAudition 已改：入 pending、唔再即場開 shoot ----
da = seg('function doAudition(gig, L){', 'function aud91PresentOne')
ok('doAudition 入 pending', 'aud91CreatePending' in da)
ok('doAudition 唔再即場 scheduleShoot', 'scheduleShoot(' not in da)
ok('doAudition 有上限閘', 'AUD91_CAP' in da and '等緊消息' in da)
ok('doAudition 試鏡日文案係等消息', '返去等消息啦' in da)

# ---- 公佈呈現接線 ----
ok('公佈呈現函數在位', 'function aud91PresentDue' in html and 'function aud91PresentOne' in html)
ok('簽約金三成', 'Math.round(pay*0.3)' in html and 'shoot.signedPaid = signPay' in html)
gtm = seg('function goToMapForBrowse(){', 'function nudgeRegionForToday')
ok('地圖落點有公佈 hook', 'aud91PresentDue' in gtm)
rs = seg('function runScheduleFromToday(){', 'function resolvePlannedDay')
ok('排程落點有公佈 hook', 'aud91PresentDue' in rs)
ok('公佈唔卡結局（presentDue 有結局鎖檢查）', 'ending78Locked' in seg('function aud91PresentDue', 'function aud91PresentOne'))

# ---- 殺青只入餘額 ----
rp = seg('function resolvePlannedDay(id){', 'function shootDailyDelta')
ok('殺青入餘額（wrapPay91）', 'wrapPay91' in rp and 'signedPaid' in rp)
ok('殺青文案講明冇縮水', '兩筆加埋' in html and '冇縮水' in html)
ok('payWrapNote 新制分支', '實收餘額' in html)

# ---- 等消息防返板 ----
ok('isGigConsumed 擋 pending 返板', 'pendingAud' in seg('function isGigConsumed(g){', 'function gigLifecycleStatus'))
ok('gigLifecycleStatus 有 pending 狀態', 'key:"pending"' in html and '等消息' in html)

# ---- 手帳：等消息清單＋留底 ----
j72 = seg('function jobs72SectionHtml(){', 'function showJobs()')
ok('拍攝簿有等消息段', '等消息（已試鏡，未有回音）' in j72)
ok('拍攝簿有試鏡消息留底段', '試鏡消息（何生通知留底）' in j72)

# ---- 詳情頁：簽約金行＋時序文案 ----
ok('詳情頁有簽約金行', '簽約金' in html and '合約額三成' in html and '餘額殺青入帳' in html)
ok('詳情頁摘要講等回音', '試鏡後要等劇組回音' in html)

# ---- 玩家面唔准系統味詞（AUD91 玩家文案段落） ----
mod = seg('/* ===== v20a91 AUD91', 'function promptAudition')
import re
def literal_texts(chunk):
    # 模板字串剝走 ${...} 程式插值後，剩低嘅先係玩家真係會見到嘅文字
    out = []
    for s in re.findall(r'`[^`]*`', chunk, re.S):
        out.append(re.sub(r'\$\{[^{}]*\}', '', s))
    for s in re.findall(r'"[^"\n]*"|\'[^\'\n]*\'', chunk):
        out.append(s)
    return out
lits = literal_texts(mod)
for bad_word in ['pendingAud', 'revealDay', 'signedPaid', 'pending', 'reveal']:
    ok('玩家面字串冇系統味詞 ' + bad_word, not any(bad_word in t for t in lits))
ok('玩家面有等通知講法', '等消息' in mod and '何生' in mod)

# ---- NOTES 在位 ----
notes_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'NOTES_V20A91_AUDFLOW.md')
ok('NOTES_V20A91 在位', os.path.exists(notes_path))
if os.path.exists(notes_path):
    notes = open(notes_path, encoding='utf-8').read()
    for kw in ['簽約金', '等消息', '明星志願', '違約']:
        ok('NOTES covers ' + kw, kw in notes)

print('\nAUD91 STATIC: ' + (str(len(fails)) + ' FAIL -> ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
