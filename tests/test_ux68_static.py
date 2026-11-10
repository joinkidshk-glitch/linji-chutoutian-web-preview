# -*- coding: utf-8 -*-
# v20a68 UX68 靜態測試：訓練指南頁接線／地圖墨字地名（方案 B 定版）／sheet 分組接線／重量紓緩結果。
# 反證：喺 v20a67 index 上行會 FAIL（冇 UX68 block、冇 .mn68、hero_awi 仍 191KB）。
# 用法：python3 tests/test_ux68_static.py [path-to-index.html]
import re, sys, base64
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- (1) 訓練指南／選擇器 ---
# v20a71 PART3B 改版：renderGuidePane68（指南渲染）已隨「訓練一覽」段移除，
# 數據衍生層保留、呈現改入排程選擇器 train71PickerHtml。本斷言跟新正確行為改。
ok('UX68 block 存在（數據衍生層保留＋v71 選擇器）', '/* ===== v20a68 UX68' in src and 'function train71PickerHtml' in src
   and 'function ux68ParseGainTable' in src and 'function ux68OrganizeLocSheet' in src)
# v20a70 BOOK70 改版：訓練指南取消獨立頁，拼入行程頁「訓練」段。本斷言由「有 guide tab＋pane」
# 改為新正確行為；喺 v69 index 上行會 FAIL（嗰陣仲係獨立頁，係反證）。
ok('手帳冇獨立「訓練指南」tab／pane（v70 拼入行程頁）',
   'data-htab="guide"' not in src and 'id="home-pane-guide"' not in src and 'id="htab-guide"' not in src and 'id="guide-list"' not in src)
# v20a71 PART3B 改版：「訓練一覽」段（home-train70）成段移除——訓練資訊改入
# 排程選擇器 panel（nb-train71-wrap／train71-picker）。本斷言跟新正確行為改。
ok('訓練一覽段已移除、選擇器 panel 喺行程頁（v71 PART3B）',
   'id="home-train70"' not in src and 'id="train70-list"' not in src and 'id="train70-toggle"' not in src
   and 'id="nb-train71-wrap"' in src and 'id="train71-picker"' in src)
m = re.search(r'function setHomeTab\(tab\)\{(.*?)\n\}', src, re.S)
body = m.group(1) if m else ''
# v20a71 PART3B 改版：guide／train 舊入口只去 plan（唔再展開已刪嘅訓練段）、
# allow 冇 guide、唔再呼叫 renderGuidePane68；progress 分支渲染進度頁。
ok('setHomeTab v71 接線（guide／train 改落 plan／冇已刪段呼叫／progress 渲染／分組同步）',
   'if(tab === "guide" || tab === "train")' in body and 'guide:1' not in body
   and 'renderGuidePane68' not in body and 'book70OpenTrainSection' not in body
   and 'renderProgressPane71()' in body and 'book70SyncTabGroups(tab)' in body)
# v20a70 BOOK70 改版：恆常出口——syncHomeTabExit 唔再計 journalTab、唔再睇 #home-back-map
# 可見與否，永遠顯示＋標籤恆定。喺 v69 index 上行會 FAIL（反證）。
ok('syncHomeTabExit v70 恆常出口（永遠顯示＋標籤恆定「返回地圖」）',
   '|| tab==="guide"' not in src and 'exit.hidden = false' in src and 'btn.textContent = "返回地圖"' in src)
# v20a75 改版：增益改按級數據衍生——ux68ParseGainTable 行 TRAIN75_SPEC＋現級
# （levels75GainRange），同實際上堂共用同一張表，唔再解析源碼字面量。
ok('v75：增益表由 TRAIN75_SPEC 按現級衍生（同上堂共用數據）',
   'levels75GainRange(cid, levels75Level(oo, cid))' in src and 'const TRAIN75_SPEC' in src)
# v20a74 改版：主攻目標（目標數值）成個移除（用戶 2026-11-10 16:06 拍板）——
# 舊斷言「目標數值存 prefs」改為「全檔冇目標功能殘留」；喺 v73 index 上行會 FAIL（反證）。
ok('v74：目標數值功能全清（冇讀寫函數／冇 prefs 鍵／冇「主攻」字樣）',
   'ux68TargetStat' not in src and 'ux68SetTargetStat' not in src and '主攻' not in src)
ok('指南有「前往」真跳轉（leaveHomeFromNotebook＋openLoc）',
   'function ux68GoLoc' in src and 'leaveHomeFromNotebook("map")' in src and 'openLoc(locId)' in src)

# --- (2) 地點選項整理 ---
ok('openLoc 尾有 organizer 呼叫', 'ux68OrganizeLocSheet(L)' in src)
ok('分組標籤齊（要事／接工／訓練／社交・劇情／休息・雜項／未開放）',
   all(t in src for t in ['"要事"', '"接工"', '"訓練"', '"社交・劇情"', '"休息・雜項"', '未開放（']))
ok('分類覆蓋主要掣型（通告欄／試鏡／報名／傾談／打聽／休息）',
   all(t in src for t in ['只查看通告欄', '試鏡入口', '報名：', '傾談', 'act-ask', '休息室歇陣']))
ok('要事訊號用既有數據（favorDue／deadlineDay／CALIB60_NODE_WINDOWS／季尾）',
   all(t in src for t in ['favorDueDebt', 'deadlineDay', 'CALIB60_NODE_WINDOWS', 'ux68SeasonEndLeft']))
# v20a74 改版：目標標示隨主攻目標功能移除——舊斷言「▲ 用 STAT_LABEL」改為驗全清。
ok('v74：目標標示已移除（冇 badges 函數／冇 .ux68-tgt）', 'ux68ApplyTargetBadges' not in src and 'ux68-tgt' not in src)
ok('sheet 標題加地區、desc 唔重複', '${L.name}${L.area ? " · " + L.area : ""}' in src
   and 'textContent=`${descShort}`' in src)

# --- (3) 地圖墨字地名（方案 B 定版：index-alt-b.html） ---
labels = re.findall(r'<div class="mn68" style="left:([0-9.]+)%;top:calc\((\d+)% ([+-]) (\d+)px\)">([^<]+)</div>', src)
ok('地圖有 13 個墨字標籤', len(labels) == 13)
lm = re.search(r'const LOCS = \[(.*?)\n\];', src, re.S)
locs = re.findall(r'\{ id:"(\w+)", name:"([^"]+)"', lm.group(1) if lm else '')
loc_names = [n for _, n in locs]
ok('標籤文字同 LOCS 地點名逐個對得上', sorted(t[4] for t in labels) == sorted(loc_names) and len(loc_names) == 13)
spec = {
    '獅子山製片': ('54', '12', '-', '52'), '香江唱片': ('28', '24', '+', '26'),
    '星河電視台': ('33', '14', '-', '50'), '九龍電視台': ('36', '45', '-', '52'),
    '海港廣播': ('88', '15', '+', '16'), '紅棉影業': ('74', '11', '-', '44'),
    '維港電影': ('76', '18', '+', '44'), '中環廣告': ('60', '57', '+', '30'),
    '金鐘創意': ('85', '60', '+', '28'), '灣仔唱片': ('68', '77', '+', '34'),
    '天星音樂': ('86', '82', '+', '30'), '金龍茶餐廳': ('11', '16', '-', '56'),
    '何生事務所': ('15', '86', '-', '20'),
}
got = {t[4]: (t[0], t[1], t[2], t[3]) for t in labels}
ok('標籤位置同定版樣板（v4 貼建築位）逐個一致', got == spec)
ok('墨字 CSS 定版（#43301c／12.5px／紙色光暈／無底框）',
   '.mn68{' in src and 'color:#43301c' in src and 'font-size:12.5px' in src
   and 'text-shadow:0 0 3px #f3e7c8' in src)
ok('標籤層 pointer-events:none（唔擋熱區）', '.map-names68{ position:absolute; inset:0; pointer-events:none;' in src)
ok('冇用返小木牌款（冇 .lbl／木框牌 CSS）', 'class="lbl"' not in src and 'map-names68' in src)

# --- (4) 重量紓緩結果 ---
def raw_of(pat):
    m = re.search(pat, src)
    return len(base64.b64decode(m.group(1))) if m else -1
hero = raw_of(r'"hero_awi":\s*"data:image/jpeg;base64,([A-Za-z0-9+/=]+)')
guide = raw_of(r'start_guide:\s*"data:image/jpeg;base64,([A-Za-z0-9+/=]+)')
mapimg = raw_of(r'const MAP_IMG = "data:image/jpeg;base64,([A-Za-z0-9+/=]+)')
ok('hero_awi 已再壓縮（191,434 → <100,000）', 0 < hero < 100000)
ok('start_guide 已再壓縮（201,839 → <160,000）', 0 < guide < 160000)
ok('MAP_IMG 保留原圖（核心視覺唔硬減；q82 試壓冇收益）', mapimg > 370000)
ok('主檔總量 < 5,075,000 bytes（v83 ENC83 巧遇 Phase 2 四星對白＋提攜模組有意增長至 ~5,047,816；v82 為 ~4,974,159）', len(src.encode('utf-8')) < 5075000)
ok('海報圖已有 loading="lazy"（v59 既有，冇倒退）', 'loading="lazy"' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
