# v406：選單刪「返回」列（有意圖改動），data-m 清單去 back。
# v404 意圖更新：選單 6→3（返回／設定／存檔管理＋隱藏 wire）——重看教學入設定頁、存檔／讀檔／新遊戲入存檔管理共用槽位清單；斷言同步。
# -*- coding: utf-8 -*-
# v20a72 MENU72 靜態測試：主選單一門原則（選單只留動作＋系統組；資訊頁歸入
# 手帳五大類——狀態併記數／拍攝簿併作品／人脈入人情組／庫存入近況組；
# 傳聞／人情債選單入口刪除）＋舊呼叫重定向。
# v20a77 HUB77 原位改版：用戶 2026-11-10 17:51 拍板刪選單「劇情」掣——
# 選單清單／handler 期望同步移除 story-play，徽章斷言改為「已移除」。
# 反證：喺 v20a71 index 上行會 FAIL（選單仲有 14 項、冇 people／inv 子頁、
# showJobs／showPeople／showInventory 仲開 modal）。
# 用法：python3 tests/test_menu72_static.py [path-to-index.html]
import re
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('NOTES_V20A72 在位', (p.parent / 'NOTES_V20A72_MENU.md').exists())

# --- (1) 選單只剩新清單 ---
i_menu = src.find('<div class="menu" id="menu">')
i_after = src.find('<div class="map-wrap">', i_menu)
menu = src[i_menu:i_after] if 0 <= i_menu < i_after else ''
ok('選單容器搵到', bool(menu))
ms = re.findall(r'data-m="([^"]+)"', menu)
# v20a108 TEXT108 S-49：選單項舊名「提早休息」改「過一日」；data-m 值 rest-early 不變，只係測試名跟改
# v20a397 UI397-5：「過一日」由選單移除（地圖入口保留），選單得返系統五項＋wire
ok('選單 data-m 恰好＝新清單（系統五項＋wire；手帳掣 v389 已刪改拉柄；過一日 v397 已刪）',
   ms == ['settings', 'wire', 'slots'])
ok('選單已冇六個資訊頁入口', all(('data-m="%s"' % m) not in menu for m in
   ['stats', 'people', 'inv', 'jobs', 'rumors', 'debts']))
ok('劇情掣＋徽章已移除（v20a77 HUB77）', 'id="menu-story-badge"' not in menu and 'menu-story' not in menu)
ok('手帳掣已刪、拉柄在位（v389）', 'data-m="journal"' not in menu and 'id="book389-handle"' in src)
i_sys = menu.find('data-m="settings"')
ok('選單得返系統組，唔再分組（過一日＋分隔線 v397 一併移除）',
   'data-m="rest-early"' not in menu and 'menu-sep' not in menu and i_sys >= 0)
ok('wire 隱藏項保留（接線功能冇誤刪）', 'id="menu-wire" hidden' in menu)

# --- (2) 選單 handler 冇 orphan 分支 ---
i_h = src.find('document.getElementById("menu").onclick')
handler = src[i_h:i_h + 2200] if i_h >= 0 else ''
ok('handler 在位', bool(handler))
ok('handler 已刪六個資訊頁分支', all(('m==="%s"' % m) not in handler for m in
   ['stats', 'people', 'inv', 'jobs', 'rumors', 'debts']))
ok('handler 保留新清單分支（v404 選單 6→3：返回／設定／存檔管理＋wire；replay-tut 入設定頁、save／load／new 入存檔管理）', all(('m==="%s"' % m) in handler for m in
   ['settings', 'wire', 'slots'])
   and 'm==="replay-tut"' not in handler and 'm==="save"' not in handler and 'm==="load"' not in handler and 'm==="new"' not in handler
   and 'm==="story-play"' not in handler and 'm==="rest-early"' not in handler)
ok('重看教學入設定頁（v404）', 'id="set-replay-tut"' in src)
ok('存檔管理共用槽位清單＋新遊戲（v404）', 'openSaveSlotsModal("manage")' in src and 'data-slot-save404' in src and 'data-slot-load404' in src and 'label:"新遊戲", role:"g", on:()=>openSaveSlotsModal("new")' in src)

# --- (3) 手帳新子頁結構 ---
ok('人脈清單容器喺人情合併頁（v389）', 'id="home-pane-favor389"' in src and 'id="people-list"' in src)
ok('庫存 pane＋清單容器', 'id="home-pane-inv"' in src and 'id="inv-list"' in src)
ok('人情組單頁分段掣（人情債｜人脈；v389）', 'id="favor389-seg-debt"' in src and 'id="favor389-seg-people"' in src)
ok('庫存子掣喺近況組', 'id="htab-inv"' in src and 'data-htab="inv">庫存</button>' in src)
ok('分組映射：people→favor、inv→status、人情組預設 debt',
   'people:"favor"' in src and 'inv:"status"' in src and 'favor:"debt"' in src)

# --- (4) setHomeTab 接線 ---
i_sht = src.find('function setHomeTab(tab){')
i_sync = src.find('function syncHomeTabExit', i_sht)
sht = src[i_sht:i_sync] if 0 <= i_sht < i_sync else ''
ok('setHomeTab allow 含 people／inv', 'people:1' in sht and 'inv:1' in sht)
ok('setHomeTab pane 切換列含 people／inv', '"people"' in sht and '"inv"' in sht)
ok('setHomeTab 渲染分派 people／inv', 'renderPeoplePane()' in sht and 'renderInvPane()' in sht)

# --- (5) 內容產生器＋作品頁合併 ---
for fn in ['function jobs72SectionHtml()', 'function jobs72GoBoard()', 'function jobs72GoLoc()',
           'function people72Html()', 'function renderPeoplePane()',
           'function inv72Html()', 'function renderInvPane()']:
    ok('存在 ' + fn, fn in src)
i_rw = src.find('function renderWorksPane(){')
rw = src[i_rw:i_rw + 900] if i_rw >= 0 else ''
ok('作品頁＝拍攝簿段＋作品牆（jobs72SectionHtml＋worksWallHtml59）',
   'jobs72SectionHtml()' in rw and 'worksWallHtml59()' in rw)
ok('作品頁綁返拍攝簿導航掣', 'jobs72-goboard' in rw and 'jobs72-goloc' in rw and 'jobs72GoBoard()' in rw and 'jobs72GoLoc()' in rw)
ok('人脈頁綁返「去找」掣', 'people72GoLoc' in src and 'people-go' in src)
ok('庫存頁綁返「去小賣」掣', 'inv72-goshop' in src and 'inv72GoShop' in src)

# --- (6) 舊 modal 已拆、舊呼叫改重定向 ---
ok('拍攝簿唔再開 modal', 'modal(`<h3>拍攝簿</h3>' not in src)
ok('人脈唔再開 modal', 'modal(`<h3>人脈</h3>' not in src)
ok('庫存唔再開 modal', 'modal(`<h3>庫存</h3>' not in src)
def fnseg(marker, nxt):
    a = src.find(marker)
    b = src.find(nxt, a) if a >= 0 else -1
    return src[a:b] if 0 <= a < b else ''
ok('showJobs 重定向去作品頁', 'setHomeTab("works")' in fnseg('function showJobs(){', '\n}\n'))
ok('showPeople 重定向去人脈頁', 'setHomeTab("people")' in fnseg('function showPeople(){', '\n}\n'))
ok('showInventory 重定向去庫存頁', 'setHomeTab("inv")' in fnseg('function showInventory(){', '\n}\n'))
ok('showStats 維持記數重定向（v20a6 既有）', 'setHomeTab("ledger")' in fnseg('function showStats(){', '\n}\n'))

# --- (7) 外觀修正（用戶 2026-11-10 14:46 追加） ---
ok('子頁掣 active 態明文啡底白字', '#home-subtabs .home-tab.on{ background:#6b4e2e; color:#fff8e8;' in src)
ok('手帳 view toast slab 隱藏規則', '#app.toast-up:has(#v-home.view.on)::after{ display:none !important; }' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
