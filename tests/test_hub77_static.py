# -*- coding: utf-8 -*-
# v20a77 HUB77 靜態測試：劇情／進度全套整合（用戶 2026-11-10 17:51 拍板）——
# 一、大地圖常駐「進度」掣（任何 hint 狀態都撳得）直達手帳進度頁
# 二、☰ 選單「劇情」掣＋徽章＋handler 分支移除；paintStoryEntryHints badge 更新安全降級
# 三、頂欄 #chip-story 改指進度頁＋標籤/title 改「主線進度」語系
# 四、進度頁做播放門口：在場（picker 同一套 evalNode）先出「播呢幕」掣；
#    播完畫面掣、劇情提示 modal、手帳提示 fallback 全部改指進度頁；
#    playOpenPicker 保留做死碼（只剩 ?debug 接線面板引用），玩家入口清零。
#    【v20a165 STORY165 取代】用戶 2026-11-13 09:24 拍板劇情強制播放：首播唔再經掣，
#    條件滿足嘅幕返地圖嗰陣即播——進度頁「播呢幕」掣＋委派一併拎走，進度頁只做紀錄；
#    v155 B1 三態根因就係呢個掣嘅有無取決於 soft 路徑 atLoc。以下斷言按 v165 新規格。
# 反證：喺 v20a76 index 上行會 FAIL（冇 map-progress-btn、選單仲有劇情掣、
# chip 仲開 picker、進度頁冇播掣）。
# 用法：python3 tests/test_hub77_static.py [path-to-index.html]
import re
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def seg(a, b, span=6000):
    i = src.find(a)
    if i < 0: return ''
    j = src.find(b, i + len(a)) if b else -1
    return src[i:j] if j > i else src[i:i + span]

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('NOTES_V20A77 在位', (p.parent / 'NOTES_V20A77_HUB.md').exists())

# --- 一、大地圖「進度」掣 ---
# v20a128 A1（計劃 §5／§7 mockup）：進度只留一個入口（頂欄 chip），地圖浮 pill 取消
# （N19 一併解決；反轉 v108 S-8「chip 只係徽章、入口係 pill」嗰個決定）。
# 舊 HUB77 浮 pill 斷言按新規格改寫——pill 唔見，chip 係入口（見第三節）。
i_vm = src.find('<section id="v-map" class="view">')
i_vh = src.find('<section id="v-home" class="view">')
vmap = src[i_vm:i_vh] if 0 <= i_vm < i_vh else ''
ok('地圖浮 pill 已取消（A1：進度入口只留頂欄 chip）',
   'id="map-progress-btn"' not in vmap and 'id="map-progress-btn" aria-label="主線進度">進度</button>' not in vmap)
ok('地圖浮 pill CSS 已取消', '#map-progress-btn{ position:absolute;' not in src)
ok('地圖浮 pill 開 sheet 隱藏規則已取消', '.map-wrap.sheet-open #map-progress-btn{ display:none; }' not in src)
w = seg('const _mapProg77 = document.getElementById("map-progress-btn");', '/* v20a165 STORY165：進度頁「播呢幕」掣已拎走')
ok('地圖浮 pill 舊接線留 null guard（元素缺席唔 crash）', '_mapProg77' in src and 'if(_mapProg77)' in w)
ok('地圖 hint 掣行為保留（data-prog71 委派入進度頁）', '_mapHint71' in src and 'data-prog71' in src)

# --- 二、選單刪劇情掣 ---
ok('選單：story-play 掣全域移除', 'data-m="story-play"' not in src)
ok('選單：menu-story-badge 元素移除', 'id="menu-story-badge"' not in src.replace('getElementById("menu-story-badge")', ''))
h = seg('document.getElementById("menu").onclick', '', 3000)
ok('選單 handler：在位且冇 story-play 分支（註解提及唔計）',
   bool(h) and 'm==="story-play"' not in h and 'StoryPlay.playOpenPicker()' not in h)
ps = seg('function paintStoryEntryHints(){', 'function storyOpenSnapshot', 4000)
ok('paintStoryEntryHints：badge 更新保留 if 守衛（元素缺席安全降級）',
   'const badge = document.getElementById("menu-story-badge");' in ps and 'if(badge){' in ps)

# --- 三、chip 改指進度頁 ---
# v20a128 A1（計劃 §5／§7 mockup）：進度只留一個入口——頂欄 chip。chip 恢復做掣
# （反轉 v108 S-8「chip 只係數字徽章、入口係 pill」；浮 pill 已取消，chip 唔做掣就冇入口）。
ok('chip：標籤改「進度」＋title 改「主線進度」',
   'id="chip-story" title="主線進度">進度<span class="chip-story-n"' in src)
ok('chip：恢復做 button（唯一進度入口）',
   '<button type="button" class="chip chip-story" id="chip-story"' in src
   and '<span class="chip chip-story" id="chip-story"' not in src)
ok('chip：有 click 接線入進度頁（enterHome progress）', 'cs.addEventListener("click"' in src and 'enterHome(null, false, "progress")' in src)
ok('chip：cursor pointer（係掣，唔係徽章）', '#app #chip-story{ cursor:pointer; }' in src)
ok('chip title 四態改主線進度語系',
   '主線進度 · 有 ' in ps and '主線內容載入中' in ps and '主線進度（暫無可播）' in ps and '主線內容載入唔到' in ps)
ok('chip 舊 title 文案清零', '有可播劇情 · ' not in src and '"劇情（暫無可播）"' not in src and '"劇情內容載入中"' not in src)

# --- 四、進度頁播放門口（v20a165 STORY165 取代：掣拎走，首播改強制播） ---
rp = seg('function renderProgressPane71(){', '/* === v20a71', 9000)
ok('進度頁：已開放行唔再出「播呢幕」掣（v165：首播唔經掣）',
   'data-prog77-play="' not in rp and '>播呢幕</button>' not in rp and 'here77' not in rp)
ok('進度頁：已開放行寫「返地圖嗰陣就會播出」', '返地圖嗰陣就會播出' in rp)
ok('進度頁：舊「去 X 就會觸發」／「你而家喺」文案清零',
   '"去"+prog71Esc(r.locName)+"就會觸發。"' not in rp and '你而家喺' not in rp)
ok('進度頁：舊「開劇情列表播」提示已改寫', '開劇情列表播' not in rp and '劇情列表' not in rp)
ok('播掣委派已拎走：closest data-prog77-play／_progList77 清零',
   'closest("[data-prog77-play]")' not in src and '_progList77' not in src)
ok('強制播掛點在位（goToMapForBrowse 尾段 story165TryForcedPlay）',
   'story165TryForcedPlay()' in src and 'function story165TryForcedPlay(){' in src)

# --- 五、播完掣／提示改指進度頁、picker 玩家入口清零 ---
ok('播完畫面：冇「劇情列表」掣', 'label:"劇情列表"' not in src)
ok('播完畫面：兩粒「進度」掣改指進度頁', src.count('label:"進度", role:"g"') == 2
   and src.count('enterHome(null, false, "progress")') >= 5)
n = seg('function maybeNudgeStoryEntry(reason){', '', 3000)
ok('劇情提示 modal：掣改「睇進度」＋落點進度頁＋文案唔再提選單劇情',
   'label:"睇進度"' in n and 'enterHome(null, false, "progress")' in n and '打開劇情' not in n and '選單「劇情」' not in n)
wh = seg('function wireHomeStoryHint(){', '', 2500)
ok('手帳提示 fallback：改去進度頁', 'enterHome(null, false, "progress")' in wh and 'StoryPlay.playOpenPicker()' not in wh)
calls = [m.start() for m in re.finditer(r'StoryPlay\.playOpenPicker\(\)', src)]
ok('picker 玩家入口清零：StoryPlay.playOpenPicker() 只剩 debug 接線一處',
   len(calls) == 1 and 'act==="picker"' in src[max(0, calls[0] - 200):calls[0] + 60] if calls else False)
ok('picker 本體保留做死碼＋HUB77 註明', 'function playOpenPicker(){' in src and 'playOpenPicker 已冇玩家入口' in src)
ok('教學文案唔再叫人開選單劇情（舊句清零＋新句在位）',
   '再打開選單「劇情」' not in src and '再撳地圖上嘅「進度」掣' in src and '通告欄／劇情' not in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
