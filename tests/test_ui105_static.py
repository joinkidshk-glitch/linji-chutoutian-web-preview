# v20a105 UI105 版面＋文字硬傷組・靜態守門測試（工人 C 範圍 23 項）。
# 用法：python3 tests/test_ui105_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」（舊寫法出現即 FAIL）。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def body_of(fname, span=3000):
    i = html.find(fname)
    return html[i:i + span] if i >= 0 else ''

# S-48 設定頁：三行「未推出」死掣收起，只剩一行「即將推出」
ok('S-48 音效／音樂行存在', '音效／音樂' in html)
ok('S-48 即將推出只出現一次', html.count('即將推出') == 1)
ok('S-48 冇「未推出 未推出」雙重字樣', '未推出 未推出' not in html)

# S-43 記數簿：屬性唔顯示 /999 上限，壓力保留 /100
b = body_of('function ledgerStatsParts', 1600)
ok('S-43 ledgerStatsParts 喺度', bool(b))
ok('S-43 非壓力屬性只出數值', '`${n}`' in b and 'k==="stress"' in b)
_vt = [ln for ln in b.split('\n') if 'const vTxt' in ln]
ok('S-43 vTxt 渲染行冇 999', bool(_vt) and '999' not in _vt[0])

# S-39 生活費提示：用完成日計星期（dayIndex-1），平日板唔出
ok('S-39 完成日星期 weekdayIdx((S.dayIndex|0)-1)', 'weekdayIdx((S.dayIndex|0)-1)' in html)

# S-24 事務所信任行：刪結局劇透句，數字＋下一階提示保留
b = body_of('function enc79HoTrustLine', 1500)
ok('S-24 enc79HoTrustLine 喺度', bool(b))
ok('S-24 冇「江湖撈家」劇透', '江湖撈家' not in b)
ok('S-24 冇「信任去到 60」條件句', '信任去到 60' not in b)

# S-28 未達標提示新格式「現值／需 X（差 Y）」
b = body_of('function gigGapLine34', 1200)
ok('S-28 gigGapLine34 喺度', bool(b))
ok('S-28 有（差 N）格式', '（差 ' in html)
ok('S-28 gigGapLine34 冇舊「欠：」前綴', '欠：' not in b)

# S-31 報名截止：獨立一行＋「仲有 N 日截止」
b = body_of('function gigApplyDeadlineText', 600)
ok('S-31 截止句式「仲有 N 日截止」', '仲有 ' in b and '日截止' in b)
ok('S-31 詳情有獨立報名截止行', 'ddlRow105' in html)

# S-32 通告詳情卡高按內容收
i = html.find('#mask.casting-sheet-on .notice_sheet_frame{')
seg = html[i:i + 400] if i >= 0 else ''
ok('S-32 notice_sheet_frame height:auto', 'height:auto' in seg)
ok('S-32 冇舊 height:100%（max-height 除外）', 'height:100%' not in seg.replace('max-height:100%', ''))

# S-44 開局冬季債狀態對齊＋台詞唔重播
i = html.find('card_biao_winter')
seg = html[i:i + 260] if i >= 0 else ''
ok('S-44 阿標冬季卡「就嚟到期」', '就嚟到期' in seg)
ok('S-44 阿標冬季卡冇「已逾期」', '已逾期' not in seg)
b = body_of('function seasonCollectToast', 1500)
ok('S-44 toast 唔再直用 overdue.line', 'overdue.line' not in b)

# S-45 進度頁遠幕合併一行
ok('S-45 farMerged105 合併旗在', 'farMerged105' in html)
ok('S-45 合併句「完成前面幕數後逐幕揭曉」', '完成前面幕數後逐幕揭曉' in html)

# S-10 劇情卡：副行截第一句＋「›」絕對定位唔孤行
ok('S-10 › 釘右邊中線', '.map-hint-story-btn::after{ content:"›"; position:absolute;' in html)
ok('S-10 冇舊孤行寫法 content:" ›"', '.map-hint-story-btn::after{ content:" ›";' not in html)

# D-6 旁白入底部對話框
ok('D-6 旁白 plate class sp-plate-narration105', 'sp-plate-narration105' in html)
ok('D-6 旁白 stage 靠底 override', 'sp-mode-narration' in html)

# D-7 頂部 meta：計數刪走，幕標題只喺幕首句閃現
ok('D-7 sp-head-opening 閃現 class', 'sp-head-opening' in html)
ok('D-7 冇「對白 ${」計數模板', '對白 ${' not in html)

# D-8 隨機事件補場景底（第一階段）
ok('D-8 wf4Scene105 函數在', 'function wf4Scene105' in html)
ok('D-8 wf4-scene105 div 接線', 'class=\\"wf4-scene105\\"' in html or 'wf4-scene105' in html)
ok('D-8 場景底 CSS', '.wf4-scene105{' in html)

# S-3 教學搬去行程編輯頁常駐一行
ok('S-3 plan-teach105 在編輯頁', 'plan-teach105' in html)

# S-19 壓力：行內展開明細＋確定唔再彈 modal
ok('S-19 toggleStressDetail105 在', 'function toggleStressDetail105' in html)
ok('S-19 nb-stress-detail105 盒在', 'nb-stress-detail105' in html)
ok('S-19 壓力文案完整句「屬健康範圍：」', '屬健康範圍：' in html)

# S-21 在場紅星行：頭像＋遠觀標籤
ok('S-21 pres105 行在', 'pres105' in html)
ok('S-21 pres105-av 頭像', 'pres105-av' in html)
ok('S-21 pres105-tag 標籤', 'pres105-tag' in html)

# S-25 醫院：體檢確認先扣錢＋用途說明卡
ok('S-25 buyCheckup105 在', 'function buyCheckup105' in html)
ok('S-25 確認掣「確認付款 $…」', '確認付款 $' in html)
ok('S-25 「醫院有咩用？」說明卡', '醫院有咩用' in html)

# S-35 獲聘 modal：殺青結算標籤對位（舊「先入帳」標籤已改）
ok('S-35 「殺青嗰日先結算」標籤', '殺青嗰日先結算' in html)

# S-37 殺青對帳只講一次：舊重複句只准喺註釋出現一次
ok('S-37 舊句「今次入帳係餘額」最多出現一次（註釋）', html.count('今次入帳係餘額') <= 1)

# S-40 支票插喺殺青行之後、唔再排最尾
ok('S-40 wrapNoteIdx105 插位邏輯', 'wrapNoteIdx105' in html)

# S-6 地圖面板按圖比例收高＋羅盤移走
ok('S-6 polaroid flex 收高', '#app .map-polaroid{ flex:0 1 auto !important; }' in html)
ok('S-6 羅盤冇再喺 center 88% 死位', 'center 88% / 150px 168px' not in html)

# S-16 筆記紙左 inset 加到 46px
ok('S-16 .nb-left/.nb-right padding-left:46px', '.nb-left,.nb-right{ padding-left:46px !important; }' in html)

# 紅線：SAVE key／softRev／產品 ?v= 冇郁
ok('紅線 SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('紅線 softRev s107', 's107' in html)

print()
if fails:
    print('FAILURES:', len(fails))
    sys.exit(1)
print('ALL PASS')
