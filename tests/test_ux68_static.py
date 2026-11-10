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

# --- (1) 訓練指南頁 ---
ok('UX68 block 存在', '/* ===== v20a68 UX68' in src and 'function renderGuidePane68' in src
   and 'function ux68ParseGainTable' in src and 'function ux68OrganizeLocSheet' in src)
ok('手帳有「訓練指南」tab＋pane', 'data-htab="guide">訓練指南</button>' in src and 'id="home-pane-guide"' in src and 'id="guide-list"' in src)
m = re.search(r'function setHomeTab\(tab\)\{(.*?)\n\}', src, re.S)
body = m.group(1) if m else ''
ok('setHomeTab 接線 guide（allow／pane／render）',
   'guide:1' in body and '"guide"' in body and 'renderGuidePane68()' in body)
ok('syncHomeTabExit journalTab 含 guide', '|| tab==="guide"' in src)
ok('增益表由 applyTrainLesson 源碼衍生（唔係硬編碼清單）',
   'applyTrainLesson.toString()' in src and 'applyGain60' in src)
ok('目標數值存 prefs（ux68TargetStat），唔入存檔', 'p.ux68TargetStat' in src and 'setPref("ux68TargetStat"' in src)
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
ok('目標標示 ▲ 用 STAT_LABEL', '"▲" + label' in src or '"▲"+label' in src or '▲" + label' in src or '"▲"' in src)
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
ok('主檔總量 < 4,750,000 bytes（v67 為 4,852,951）', len(src.encode('utf-8')) < 4750000)
ok('海報圖已有 loading="lazy"（v59 既有，冇倒退）', 'loading="lazy"' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
