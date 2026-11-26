# v417 意圖更新：推介卡欄名統一「片酬」（同普通卡同一欄），斷言同步。
# v20a403 UI403（第十輪頭五項＋暗角 dismiss）靜態釘。
# 內容錨點（唔釘行號）；行為驗證見實駕 linji-drive403。
import re, sys
src = open('index.html', encoding='utf-8').read()
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)
def slice_fn(name):
    m = re.search(r'function ' + name + r'\s*\(', src)
    if not m: return ''
    i = src.index('{', m.start()); d, j = 0, i
    while j < len(src):
        if src[j] == '{': d += 1
        elif src[j] == '}':
            d -= 1
            if d == 0: break
        j += 1
    return src[m.start():j + 1]
# (1) 地圖錨點：靜態常數、唔讀 live style、範圍驗證、offsetTop、venue 入 deCollide、paintBar 守門
pos = slice_fn('positionMapLabels137')
chk('① 靜態錨點常數 MAP403_ANCHORS', 'MAP403_ANCHORS' in src and '"何生事務所":[29,84,-42]' in src)
chk('① position 唔再由 live style 擷取錨點', 'el.getAttribute("style")' not in pos and 'map403AnchorFor' in pos)
chk('① 錨點範圍驗證 ay∈[0,100]', 'ay>=0 && ay<=100' in src)
chk('① 推撞用 offsetTop（map403CurTop）', 'map403CurTop' in slice_fn('clampMapLabels397') and 'map403CurTop' in slice_fn('deCollideLabels363'))
chk('① deCollide 包 venue99', '#map-districts97 .md97-venue99' in slice_fn('deCollideLabels363'))
chk('① paintBar 定位前唔推撞（map403LabelsReady 守門）', 'map403LabelsReady()' in slice_fn('paintBar'))
# (2) 截字收尾
chk('② modal 抬頭固定＋捲動安全區', 'scroll-padding-top:12px' in src and '#modal-inner > h3:first-child' in src)
chk('② 捲底頂沿對齊（align403ScrollEdges）', 'align403ScrollEdges' in src)
chk('② 教學舞台卡收窄置中', '.tut-board-stage .gig-board-list{ max-width:300px' in src)
chk('② 支票 memo 上移 80.5%', '.ck-memo{left:6%;top:80.5%' in src)
# (3) fade 改版
chk('③ 26px mask 已拆', 'calc(100% - 26px),transparent 100%)' not in src)
chk('③ 紙邊下接提示', 'awd-next403' in src and 'awd403FoldAndHint' in src)
# (4) 通告欄
chk('④ 推介真劇照（場景圖）', 'gt-still403-img' in src and 'assets/story/locs/bg_loc_' in src)
chk('④ 推介卡片酬第一眼', '片酬 ${payTxt}' in src)
chk('④ 整理索引紙籤去方框', '.board-menu397 .board-chip392::before{ display:none' in src)
chk('④ 詳情合約紙去框', '.cn-req-cell{ border:0' in src)
# (5) 里程碑
chk('⑤ 結局紙加高 94dvh', '#mask:has(.ending375-sheet) .modal{ max-height:min(94dvh' in src)
chk('⑤ 人情頁弱印唔疊字', '#home-pane-favor389.on) .weak-seals{ display:none' in src)
chk('⑤ 資料卡手寫卡', '#home-pane-stats389 .stats-grid{ grid-template-columns:1fr' in src)
# (6) 暗角 dismiss
_mi = src.find('getElementById("mask").addEventListener("click"')
chk('⑥ 通告欄暗角 dismiss（board-tall 例外＋modal 框）', _mi >= 0 and 'board-tall392' in src[_mi:_mi+700] and 'e.target.id!=="modal"' in src[_mi:_mi+700])
# 不變量
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
print(f"\n{len(fails)} failed" if fails else "\nall passed")
sys.exit(1 if fails else 0)
