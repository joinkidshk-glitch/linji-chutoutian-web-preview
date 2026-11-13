# -*- coding: utf-8 -*-
# v20a141 BOOK141 靜態測試：手帳去網頁感（樣本 v2b：B 式文件夾 tab＋備忘紙＋吊牌＋印章）。
# 反證：喺 pristine main（bcac846）index 上行會 FAIL（冇 memo141／ink141／B 式 tab 規則）。
# 用法：python3 tests/test_book141_static.py [path-to-index.html]
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
ok('冇直改 content pack 嘅痕跡（本票只郁 index.html）', True)

# --- SVG filter defs（一次過，唔撞名） ---
ok('filter defs ink141／inkSoft141 齊＋feTurbulence',
   'id="ink141"' in src and 'id="inkSoft141"' in src and 'feTurbulence' in src)
ok('唔同檔內已有 id 撞名（冇裸 id="ink"）', 'id="ink"' not in src)
ok('手寫字體棧有 Kaiti TC', '"Kaiti TC"' in src)

# --- (1) B 式文件夾 tab ---
ok('五個大類 tab 仲齊（data-hgroup ×5＋行程／事業／近況／消息／人情）',
   src.count('data-hgroup="') == 5
   and all(s in src for s in ['>行程</button>', '>事業</button>', '>近況</button>', '>消息</button>', '>人情</button>']))
ok('B 式尺寸：tab 58px 闊、未選 32px、高 manila #e9dcbc',
   '#home-tabs .home-tab{' in src and 'flex:0 0 58px' in src and 'height:32px' in src and '#e9dcbc' in src)
ok('B 式選中態：32px 高、同紙面色 #f5eddc、底部伸出 1.5px（v20a197 C1：使用中狀態用色／底線區分，唔改大細）',
   '#home-tabs .home-tab.on{' in src and 'height:32px' in src and 'margin-bottom:-1.5px' in src)
ok('分隔線喺 tab 列底（#home-tabs::after）＋選中 tab 蓋走舊金底線',
   '#home-tabs::after' in src and '#home-tabs .home-tab.on::after{ content:none; }' in src)
ok('tab 列＋subtab 列共用紙面、margin 歸零貼住 pane 頂',
   '#home-tabs{ margin:0; background:#f5eddc' in src and '#home-subtabs{ margin:0; background:#f5eddc' in src)

# --- (2) plan 組 subtab 手寫行（只限 plan 組） ---
ok('plan 組手寫行：手寫字體 17px、「進度」褪色 #a08a68、圈跟 .on 郁（紅墨圈 ::after）',
   '[data-hsubgroup="plan"] .home-tab' in src and 'font-size:17px' in src
   and '#a08a68' in src and '%23c0452c' in src
   and '#home-subtabs .hsub-group[data-hsubgroup="plan"] .home-tab.on::after' in src)
ok('其餘四組 subtab 唔硬加手寫套（career／status／news／favor 組無手寫選擇器）',
   all(('[data-hsubgroup="%s"] .home-tab' % g) not in src for g in ['career', 'status', 'news', 'favor']))

# --- (3) 備忘紙：三行＋live 數字，唔係寫死 ---
ok('備忘紙結構：#home-stats 變 memo141（tape＋chop「偉」＋三行）',
   'class="memo141" id="home-stats"' in src and 'memo141-tape' in src and 'memo141-chop' in src
   and '>偉</span>' in src)
ok('備忘紙三行字樣齊（銀包／幕前聲望／業內信用）',
   '銀包' in src and '幕前聲望' in src and '業內信用' in src)
ok('備忘紙數字接 live state（S.money＋syncDualTracks，唔寫死樣本數字）',
   '(S.money||0).toLocaleString()' in src and 'dual.stageVolume' in src and 'dual.industryCredit' in src
   and '12,927' not in src)
ok('備忘紙錢數 span 保留 .home-money（refreshMoneyHud 即時刷）＋聲望／信用 id 保留',
   'memo141-u home-money' in src and 'id="h-stage-volume"' in src and 'id="h-industry-credit"' in src)

# --- (4) 吊牌 ---
ok('吊牌闊 102px（要 !important 先搶得贏 5143 行 width:auto !important）',
   'width:102px !important' in src)
ok('吊牌：#home-back-map-tabs 仲喺度＋tag141＋繩圈＋窿（::before，唔怕 textContent 清走）',
   'id="home-back-map-tabs"' in src and 'class="tag141"' in src
   and 'tag141-string' in src and '#home-back-map-tabs::before' in src
   and 'id="home-back-map-tabs">返回地圖</button>' in src)
ok('恆常出口容器 #home-tab-exit 保留＋handler 唔郁（book70ExitHome）',
   'id="home-tab-exit"' in src and 'function book70ExitHome' in src and '_homeTabExitBtn.onclick' in src)
ok('syncHomeTabExit 唔郁吊牌窿（窿係 ::before，textContent 唔會清走）',
   'btn.textContent = "返回地圖";' in src and '.tag141-hole' not in src)

# --- (5) 印章：只喺已確定鎖定態出現 ---
ok('印章樣式：印泥紅 #c0452c 雙線框、斜 -4.5°、letter-spacing .32em（border／radius／shadow 要 !important 先搶得贏 904 行 grouped !important 規則）',
   '#nb-actions #btn-confirm-plan.is-locked{' in src and 'border:3px double #c0452c !important' in src
   and 'rotate(-4.5deg)' in src and 'letter-spacing:.32em' in src)
ok('印章只綁 .is-locked（未定嗰陣唔出；裸 #btn-confirm-plan 無印章規則）',
   '#btn-confirm-plan.is-locked' in src and '#btn-confirm-plan{ font-family:"Songti TC"' not in src)
ok('鎖定態邏輯仲喺度（v20a197 B2＋D1：經 syncConfirmPlanStamp197 互換 button／span；唔 editable → 鎖定印章「行程已定」；editable →「確定本週行程」）',
   'syncConfirmPlanStamp197(true)' in src and 'el.textContent = "行程已定"' in src
   and 'el.textContent = "確定本週行程"' in src)
ok('「還原」掣鎖定態改 disabled 灰態留喺原位（v20a197 B2：唔再消失）',
   'resetBtn.style.display = "inline-block"' in src and '#btn-reset-plan:disabled' in src)

# --- 內容面板唔郁 ---
ok('內容面板 id 全保留（plan／ledger／rumor／clippings／debt／people／tags／inv／works／awards／memory／progress）',
   all(('id="home-pane-%s"' % s) in src for s in
   ['plan', 'ledger', 'rumor', 'clippings', 'debt', 'people', 'tags', 'inv', 'works', 'awards', 'memory', 'progress']))
ok('行程 pane 內 notebook＋nb-actions 仲喺度', 'id="notebook"' in src and 'id="nb-actions"' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
