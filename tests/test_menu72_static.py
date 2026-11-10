# -*- coding: utf-8 -*-
# v20a72 MENU72 靜態測試：主選單一門原則（選單只留動作＋系統組；資訊頁歸入
# 手帳五大類——狀態併記數／拍攝簿併作品／人脈入人情組／庫存入近況組；
# 傳聞／人情債選單入口刪除）＋舊呼叫重定向。
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
ok('選單 data-m 恰好＝新清單（劇情／手帳／提早休息＋系統五項＋wire）',
   ms == ['story-play', 'journal', 'rest-early', 'replay-tut', 'settings', 'wire', 'save', 'load', 'new'])
ok('選單已冇六個資訊頁入口', all(('data-m="%s"' % m) not in menu for m in
   ['stats', 'people', 'inv', 'jobs', 'rumors', 'debts']))
ok('劇情徽章保留（menu-story-badge）', 'id="menu-story-badge"' in menu and 'class="menu-story"' in menu)
ok('手帳掣文案＝手帳（唔再叫返手帳）', 'data-m="journal">手帳</button>' in menu and '返手帳' not in menu)
i_rest = menu.find('data-m="rest-early"')
i_sep = menu.find('class="menu-sep"')
i_sys = menu.find('data-m="replay-tut"')
ok('分隔線喺動作組同系統組之間', 0 <= i_rest < i_sep < i_sys and '.menu-sep{' in src)
ok('wire 隱藏項保留（接線功能冇誤刪）', 'id="menu-wire" hidden' in menu)

# --- (2) 選單 handler 冇 orphan 分支 ---
i_h = src.find('document.getElementById("menu").onclick')
handler = src[i_h:i_h + 2200] if i_h >= 0 else ''
ok('handler 在位', bool(handler))
ok('handler 已刪六個資訊頁分支', all(('m==="%s"' % m) not in handler for m in
   ['stats', 'people', 'inv', 'jobs', 'rumors', 'debts']))
ok('handler 保留全部新清單分支', all(('m==="%s"' % m) in handler for m in
   ['journal', 'rest-early', 'replay-tut', 'settings', 'wire', 'story-play', 'save', 'load', 'new']))

# --- (3) 手帳新子頁結構 ---
ok('人脈 pane＋清單容器', 'id="home-pane-people"' in src and 'id="people-list"' in src)
ok('庫存 pane＋清單容器', 'id="home-pane-inv"' in src and 'id="inv-list"' in src)
ok('人情組分段列（人情債＋人脈）', 'data-hsubgroup="favor"' in src and 'id="htab-debt"' in src and 'id="htab-people"' in src)
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
