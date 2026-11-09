# v20a50 存檔槽顯示診斷靜態測試：鎖死「槽位顯示冇遷移時序問題」嘅結構證據＋紅線。
# 查證結論（詳見 NOTES_V20A50_SLOT.md）：槽位顯示全部喺渲染嗰刻即時讀 localStorage；
# 存檔遷移 normalizeSaveObj 只喺 loadFromSlot 記憶體內行、唔寫回；摘要欄位對遷移不變。
# 用法：python3 tests/test_slot50_static.py [path-to-index.html]
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def fn_body(sig, maxlen=4000):
    try:
        i = html.index(sig)
    except ValueError:
        return ''
    j = html.find('\nfunction ', i + 1)
    if j < 0 or j - i > maxlen:
        j = i + maxlen
    return html[i:j]

# ---- 遷移唔寫回：loadFromSlot 全函數冇 setItem ----
lf = fn_body('function loadFromSlot(')
ok('loadFromSlot present', bool(lf))
ok('loadFromSlot normalizes in memory only (no setItem)', 'setItem' not in lf)
ok('loadFromSlot routes through normalizeSaveObj', 'normalizeSaveObj' in lf)

# ---- 槽位顯示即時讀：開 modal 先 listSaveSlots、標題掣用 hasSave ----
osm = fn_body('function openSaveSlotsModal(', 6000)
ok('openSaveSlotsModal reads listSaveSlots() at open time', 'listSaveSlots()' in osm)
ptb = fn_body('(function paintTitleSaveBtns(){', 2000)
ok('paintTitleSaveBtns derives from hasSave()', 'hasSave()' in ptb)
lss = fn_body('function listSaveSlots(){')
ok('listSaveSlots reads every slot live via readSlotRaw', 'readSlotRaw' in lss)
rsr = fn_body('function readSlotRaw(')
ok('readSlotRaw is a direct localStorage read', 'localStorage.getItem(saveKeyForSlot(slot))' in rsr)

# ---- 遷移規則原樣（冇俾人順手改） ----
nso = fn_body('function normalizeSaveObj(', 3000)
ok('normalizeSaveObj still clamps stress to STRESS_MAX', 'STRESS_MAX' in nso)
ok('normalizeSaveObj still fills newspaperQueue', 'newspaperQueue' in nso)
ssf = fn_body('function saveSummaryFrom(', 2000)
ok('summary week derives from dayIndex', 'dayIndex' in ssf)
ok('summary stage derives via readDualTracks', 'readDualTracks' in ssf)

# ---- 紅線 ----
ok('SAVE key intact', html.count('starVolunteer_map_v19w') == 10)
ok('product ?v= intact', html.count('"v20a10"') == 7)
ok('softRev marker intact', 's109' in html)
style = html.split('<style', 1)[1].split('</style>', 1)[0]
ok('style braces balanced', style.count('{') == style.count('}'))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
