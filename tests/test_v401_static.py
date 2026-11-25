# v20a401 UI401（第八輪 GPT 頭五項）靜態釘：modal 實物紙卡／教學遮罩挖空／金掣清陰影／
# 35c 主標對調＋小檔案旁註／通告欄索引紙＋合約紙。
# 內容錨點（唔釘行號，免漂移）；行為驗證見 tests/test_v401_logic.js＋真駕。
import re, sys

src = open('index.html', encoding='utf-8').read()
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    m = re.search(r'function ' + name + r'\s*\(', src)
    if not m:
        return ''
    i = src.index('{', m.start())
    d, j = 0, i
    while j < len(src):
        if src[j] == '{':
            d += 1
        elif src[j] == '}':
            d -= 1
            if d == 0:
                break
        j += 1
    return src[m.start():j + 1]

def css_block(selector):
    # 攞 selector 規則塊——有覆寫嗰陣取最後一個匹配（後出先贏，同 CSS 層疊一致）
    pat = re.escape(selector) + r'\s*\{'
    ms = list(re.finditer(pat, src))
    if not ms:
        return ''
    m = ms[-1]
    i = src.index('{', m.start())
    d, j = 0, i
    while j < len(src):
        if src[j] == '{':
            d += 1
        elif src[j] == '}':
            d -= 1
            if d == 0:
                break
        j += 1
    return src[m.start():j + 1]

# ===== (1) scenePaper401：共用 modal opt＋實物紙卡 CSS＋各呼叫點 =====
modal = slice_fn('modal')
chk('① modal() 掛 scene-paper401（opt）', 'scenePaper401' in modal and 'scene-paper401' in modal)
chk('① modal() scenePaper401 同樣掛 scene398 漸變 dim', 'opts.keepScene397 || scene401' in modal or 'keepScene397 || scene401' in modal)
chk('① modal() scenePaper401 同樣留場景（setUnderlyingInert）', 'setUnderlyingInert(true, !!(opts.keepScene397 || scene401))' in modal)
chk('① closeModal() 清 scene-paper401', 'scene-paper401' in slice_fn('closeModal'))
chk('① 紙卡 CSS：細圓角＋墨線邊＋米紙底', '#mask.scene-paper401 .modal' in src and 'border-radius:8px' in css_block('#mask.scene-paper401 .modal'))
chk('① 紙卡 CSS：頂部膠紙貼', '#mask.scene-paper401 .modal::before' in src)
chk('① 紙卡 CSS：掣列透明底去分隔線', '#mask.scene-paper401 #modal-btns' in src and 'background:transparent' in css_block('#mask.scene-paper401 #modal-btns'))
chk('① 紙卡 CSS：主掣啞金＋次掣素紙', '#d8c49a' in css_block('#mask.scene-paper401 #modal-btns button.p') and '#fbf4dd' in css_block('#mask.scene-paper401 #modal-btns button.g'))
chk('① 43b 等消息卡掛 scenePaper401', 'keepScene397:true, scenePaper401:true' in src)
chk('① 43d／43f 電話卡掛 scenePaper401', src.count('scenePaper401:true') >= 8)
chk('① 46b confirmChoice236 有 passthrough', 'scenePaper401' in slice_fn('confirmChoice236'))
chk('① 46d afterDayModal 有 passthrough', 'scenePaper401: !!opts.scenePaper401' in slice_fn('afterDayModal'))
chk('① 46d 病假路徑傳入 scenePaper401', 'still374: "sick", scenePaper401:true' in src)
chk('① B01 教學完結卡掛 scenePaper401', 'goPlan, scenePaper401:true' in src)

# ===== (2) 教學遮罩：挖空＋頂欄同步降亮＋卡邊背景字＋窄紙條 =====
chk('② 遮罩全幅均勻 dim（頂欄同步降亮）', '#mask.tut-on{ background:rgba(0,0,0,.78) !important; }' in src)
chk('② 遮罩挖空 radial-gradient 規則', '#mask.tut-on.tut-hole401' in src and 'radial-gradient' in css_block('#mask.tut-on.tut-hole401'))
chk('② refreshTutSpotlight398 寫入挖空變數', '--tut-hole-x' in slice_fn('refreshTutSpotlight398') and 'tut-hole401' in slice_fn('refreshTutSpotlight398'))
chk('② 教學完咗清走挖空（setTutMask）', 'tut-hole401' in slice_fn('setTutMask'))
chk('② 教學期間隱去地圖提示列／圖例（卡邊半截字）', '#app.tut-stage397 .map-hint' in src and 'display:none' in css_block('#app.tut-stage397 .map-hint, #app.tut-stage397 .map-legend'))
chk('② 教學卡收窄做紙條（330px）', 'min(330px,calc(100% - 32px))' in src)
chk('② 「下一步」做右下頁籤（降飽和啞金）', '#mask.tut-on #modal-btns button.p' in src and '#d8c49a' in css_block('#mask.tut-on #modal-btns button.p'))
chk('② 「跳過教學」降為卡內次要文字掣', 'tut-skip' in src and 'text-decoration:underline' in src)

# ===== (3) 金掣「繼續」疊影：共用 button.p 規則 =====
gold = css_block('button.p, .start button.p, .gig-actions button.p, .nb-actions button.ink')
chk('③ 金掣改實色金（唔再漸變）', 'background:#C9A227' in gold and 'linear-gradient' not in gold)
chk('③ 金掣清 inset 高光', 'inset 0 1px 0' not in gold)
chk('③ 金掣清掣字陰影', 'text-shadow:none' in gold)
chk('③ 金掣深色實字（--ink #1A1410）', 'color:var(--ink)' in gold)

# ===== (4) 35c：dual 組裝＋主標對調＋小檔案旁註 =====
awd = slice_fn('renderAwardResultHtml')
chk('④ 35c dual 逐項組裝（dualParts401）', 'dualParts401' in awd)
chk('④ 35c 主標「陳偉翔散場」（metricHead401）', 'metricHead401' in awd and '"陳偉翔散場"' in awd)
chk('④ 35c 奪獎行降小標（metricSub401／np214-subhead401）', 'metricSub401' in awd and 'np214-subhead401' in src)
chk('④ 35c 小標樣式在位', '.np214-subhead401' in src)
chk('④ 35c lead 唔再以奪獎行開頭', '散場報道的觀察對象，是憑《' in awd)
chk('④ 35c 小檔案改剪報旁註（只限 .awd-result396）', '.awd-result396 .np214-factbox' in src and 'border-top:1px dashed' in css_block('.awd-result396 .np214-factbox'))
chk('④ 殺青獎勵卡同一 dual 組裝', 'dualParts401' in slice_fn('renderPostShootRewardHtml'))

# ===== (5) 通告欄：索引紙＋合約紙＋手寫備註＋捲底留白 =====
chk('⑤ 整理選單改索引紙（紙底＋微斜）', '.board-menu397' in src and 'rotate(-.6deg)' in css_block('.board-menu397'))
chk('⑤ 選中用紅筆剔號', '.board-chip392.on::after' in src and 'content:"✓"' in src)
chk('⑤ 選項改文字行（唔再膠囊掣）', 'background:transparent' in css_block('.board-menu397 .board-chip392'))
chk('⑤ 詳情三行錢包合約紙（castingNoticeDetailHtml）', 'cn-contract401' in slice_fn('castingNoticeDetailHtml'))
chk('⑤ 合約紙 CSS（「合約」印章）', '.cn-contract401::before' in src and 'content:"合約"' in src)
chk('⑤ 預期日薪算式改手寫備註', 'var(--hand363' in css_block('.board-calc397'))
chk('⑤ 詳情頁捲底留白 28px（陣容最後一行捲得出）', 'padding-bottom:28px' in src)
chk('⑤ v399 釘死嘅三條原規則保留', '.board-ctl397{ display:flex; justify-content:flex-end; margin-top:4px; }' in src and '.board-menu397{ display:flex; flex-direction:column; gap:4px; margin-top:4px; width:200px; align-self:flex-end; }' in src)

print()
if fails:
    print('FAILED: %d' % len(fails))
    sys.exit(1)
print('ALL PASS')
