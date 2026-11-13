# v20a135 MAP135 地圖底部卡收細・靜態守門測試。
# 用法：python3 tests/test_ui135_mapcard_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → 舊寫法在／新寫法缺席 → 乾淨 FAIL（唔 crash）。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- 模板段：paintBar 計劃行起，到 paintStoryEntryHints 止（含合併行＋卡模板）---
_i = html.find('const planName135')
if _i < 0:
    _i = html.find('document.getElementById("map-hint").innerHTML')
_j = html.find('paintStoryEntryHints', _i) if _i >= 0 else -1
tpl = html[_i:_j] if _i >= 0 and _j > _i else ''
ok('模板段抽得到', bool(tpl))

# 1. 灰色說明行唔再喺地圖卡模板出現（連同 seenMapHelp128 旗標邏輯）
ok('灰色說明行字串唔喺模板', '通告欄／打聽不耗日' not in tpl and '通告欄／打聽／傾談' not in tpl)
ok('灰色說明行 class 唔喺模板', 'map-hint-help' not in tpl)
ok('seenMapHelp128 旗標唔喺模板', 'seenMapHelp128' not in tpl and 'helpFirst128' not in tpl)

# 2. 「全部地點」掣唔再喺地圖卡模板出現（追加指示 19:51：地圖熱區已夠，掣係多餘嘅）
ok('全部地點掣 id 唔喺模板', 'id="map-show-all-locs"' not in tpl)
ok('全部地點掣字唔喺模板', '全部地點' not in tpl)
ok('頂行 flex 包裝唔喺模板', 'map-hint-top128' not in tpl)

# 3. 藍色劇情卡唔再由地圖卡出（模板唔計 storyMapHintHtml；v198 C1 已成個拎走，另驗 §6／§7）
ok('劇情卡唔喺模板', 'storyMapHintHtml' not in tpl and 'map-hint-story' not in tpl)

# 4. 合併行在：計劃＋出行同一行，兩個動態位齊全；額度用完變體同樣併入
ok('合併行：今日＋計劃名', '今日：<b>${planName135}</b>' in tpl)
ok('合併行：仲可以去 N 個地方', '仲可以去 ${rem135} 個地方' in tpl)
ok('合併行：額度用完變體', '出行額度已用完，聽日再去' in tpl)
ok('合併行：舊分行寫法唔見', '今日計劃：' not in tpl and '今日出行：' not in tpl)

# 5. 保留嘅嘢：日期＋週數、audLine108、過一日掣（行為唔變）
ok('日期行保留（fmtDate 含週數）', 'fmtDate()' in tpl)
ok('audLine108 保留（有等緊先顯示）', 'map-hint-aud108' in tpl)
ok('過一日掣保留', '過一日' in tpl and 'id="map-end-day"' in tpl)

# 6. v20a198 C1：refreshMapHintStory 已成個拎走（死 code）——地圖卡模板唔再有 hint 插入口
ok('refreshMapHintStory 宣告已拎走（v198 C1 死 code 清除）', 'function refreshMapHintStory(){' not in html)
ok('refreshMapHintStory 呼叫點已拎走', 'refreshMapHintStory();' not in html)

# 7. v20a198 C1：storyMapHintHtml() 已成個拎走（死 code）——「三處同一來源」只剩兩處玩家面見到嘅
ok('storyMapHintHtml 函數已拎走（v198 C1 死 code 清除）', 'function storyMapHintHtml()' not in html)
ok('storyMainProgressLine 保留（「下一幕」句式規格）', 'function storyMainProgressLine(){' in html)

# 8. CSS：卡內死規則清走（top128／卡內 show-all／卡內 help）；出行 span 行內顯示
ok('CSS：死咗嘅 top128 規則清走', '.map-hint-top128' not in html)
ok('CSS：死咗嘅卡內 show-all 規則清走', '#v-map .map-hint #map-show-all-locs' not in html)
ok('CSS：死咗嘅卡內 help 規則清走', '#v-map .map-hint .map-hint-help' not in html)
ok('CSS：合併行出行 span 行內顯示', '#v-map .map-hint .map-hint-plan .map-hint-travel' in html
   and 'display:inline !important' in html)

# 9. 地圖維持闊度-bound（v19z20 polaroid padding:0，圖已經係最闊；唔加紙邊去縮細舞台）
ok('地圖舞台維持最闊（polaroid padding 0）', 'padding: 0 !important;' in html
   and '#app .map-polaroid{ padding:' not in html)

# 10. 靜態佔位文案唔好留低已刪嘅灰字（TEXTFIX55 舊文案對照表有「點地點」三字，唔計；淨驗佔位嗰句）
ok('佔位文案灰字清走', '<b>點地點</b>' not in html)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
