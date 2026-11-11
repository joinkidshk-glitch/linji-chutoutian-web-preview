# -*- coding: utf-8 -*-
# v20a77 HUB77 靜態測試：劇情／進度全套整合（用戶 2026-11-10 17:51 拍板）——
# 一、大地圖常駐「進度」掣（任何 hint 狀態都撳得）直達手帳進度頁
# 二、☰ 選單「劇情」掣＋徽章＋handler 分支移除；paintStoryEntryHints badge 更新安全降級
# 三、頂欄 #chip-story 改指進度頁＋標籤/title 改「主線進度」語系
# 四、進度頁做播放門口：在場（picker 同一套 evalNode）先出「播呢幕」掣；
#    播完畫面掣、劇情提示 modal、手帳提示 fallback 全部改指進度頁；
#    playOpenPicker 保留做死碼（只剩 ?debug 接線面板引用），玩家入口清零。
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
i_vm = src.find('<section id="v-map" class="view">')
i_vh = src.find('<section id="v-home" class="view">')
vmap = src[i_vm:i_vh] if 0 <= i_vm < i_vh else ''
ok('地圖掣：#map-progress-btn 喺 v-map 內、文案「進度」',
   'id="map-progress-btn"' in vmap and 'id="map-progress-btn" aria-label="主線進度">進度</button>' in vmap)
ok('地圖掣：CSS 絕對定位浮掣（紙底金框）', '#map-progress-btn{ position:absolute;' in src and 'border:1px solid var(--gold-seal)' in src)
ok('地圖掣：開 sheet 時隱藏（跟 map-hint 一致，唔遮地點面板）', '.map-wrap.sheet-open #map-progress-btn{ display:none; }' in src)
w = seg('const _mapProg77 = document.getElementById("map-progress-btn");', '/* v20a77 HUB77：進度頁「播呢幕」掣')
ok('地圖掣：click 直達進度頁（enterHome progress）', 'enterHome(null, false, "progress")' in w)
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
# v20a108 UI108 S-8（審計 B 項）：頂欄 chip 改做純數字徽章，唔再做掣——進度唯一入口係
# 地圖 pill（#map-progress-btn）。舊 HUB77「chip click 落點進度頁」斷言按新規格改寫。
ok('chip：標籤改「進度」＋title 改「主線進度」',
   'id="chip-story" title="主線進度">進度<span class="chip-story-n"' in src)
ok('chip：改做 span 純徽章（唔係 button）',
   '<span class="chip chip-story" id="chip-story"' in src
   and '<button type="button" class="chip chip-story" id="chip-story"' not in src)
ok('chip：冇 click 接線（唔再入進度頁）', 'cs.addEventListener("click"' not in src)
ok('chip：地圖 pill 留唯一進度入口', 'id="map-progress-btn"' in src)
ok('chip title 四態改主線進度語系',
   '主線進度 · 有 ' in ps and '主線內容載入中' in ps and '主線進度（暫無可播）' in ps and '主線內容載入唔到' in ps)
ok('chip 舊 title 文案清零', '有可播劇情 · ' not in src and '"劇情（暫無可播）"' not in src and '"劇情內容載入中"' not in src)

# --- 四、進度頁播放門口 ---
rp = seg('function renderProgressPane71(){', '/* === v20a71', 9000)
ok('進度頁：在場判定用 picker 同一套 evalNode（checkNodePhase＋player）',
   'StoryOC.evalNode(node77, { checkNodePhase:true, player:true })' in rp and 'StoryOC.findNodeRaw(r.id)' in rp)
ok('進度頁：在場先出「播呢幕」掣（data-prog77-play）',
   'data-prog77-play="' in rp and '>播呢幕</button>' in rp and 'here77' in rp)
ok('進度頁：唔在場維持「去 X 就會觸發」文字', '"去"+prog71Esc(r.locName)+"就會觸發。"' in rp)
ok('進度頁：舊「開劇情列表播」提示已改寫', '開劇情列表播' not in rp and '劇情列表' not in rp)
pw = seg('const _progList77 = document.getElementById("progress-list");', 'bind global buttons', 2500)
ok('播掣委派：closest data-prog77-play', 'closest("[data-prog77-play]")' in pw)
ok('播掣：開播前 ensureWeekPlanCommittedForStory＋StoryPlay.start(id)',
   'ensureWeekPlanCommittedForStory' in pw and 'StoryPlay.start(id)' in pw)

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
