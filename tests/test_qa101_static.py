# v20a101 QA101 靜態測試：第 0 部分 GH key 修復在位、駱家聲 bust 入庫、CHK101 支票三接入點、
# SAVE/softRev/?v= 冇變、NOTES 在位。
# 反證：v20a100 index 讀錯 key（pang_siu_kei）＋冇 lok bust／冇 CHK101 → FAIL。
import io, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('產品 ?v= 冇變', 'v20a10' in html)
ok('NOTES_V20A101 文件在位', any(f.startswith('NOTES_V20A101') for f in os.listdir(ROOT)))

# 第 0 部分：GH 好感 key
i = html.find('function end95PangProgress(')
seg = html[i:i+1600] if i >= 0 else ''
ok('end95PangProgress 在位', i >= 0)
ok('end95PangProgress 讀正確星 id pang_siuki', 'pang_siuki' in seg)
ok('end95PangProgress 冇再讀錯 key pang_siu_kei', 'pang_siu_kei' not in seg)

# 第一部分：駱家聲 bust 入庫（源圖早已出好，一直冇入 assets）
lok = os.path.join(ROOT, 'assets', 'story', 'era_stars', 'lok_gasing_bust_default.png')
ok('駱家聲 bust 已入庫', os.path.exists(lok) and os.path.getsize(lok) > 100_000)

# 第一部分（空板修復）：開板路徑快取空補生成
ok('QA101-BOARD 補生成標記在位', 'v20a101 QA101-BOARD' in html)
i2 = html.find('v20a101 QA101-BOARD')
seg2 = html[i2:i2+900] if i2 >= 0 else ''
ok('補生成用 gigsForLocSeasonBoard 同源生成', 'gigsForLocSeasonBoard(L.id, calendarSeason())' in seg2)
ok('補生成只喺快取空先觸發', '!(S.board[L.id]||[]).length' in seg2)

# 第三部分：CHK101 支票
chk = os.path.join(ROOT, 'assets', 'cheque101_base.jpg')
ok('CHK101 支票底圖已入庫', os.path.exists(chk) and os.path.getsize(chk) > 50_000)
j = html.find('const CHK101_BANK')
bank_seg = html[j:j+60] if j >= 0 else ''
ok('CHK101 虛構銀行名在位', '港城商業銀行' in bank_seg)
for real_bank in ('匯豐', '恒生', '渣打', '東亞銀行', '中國銀行'):
    ok('CHK101 銀行名唔含真銀行 ' + real_bank, real_bank not in bank_seg)
# v20a101 定稿架構：簽約支票喺 aud91PresentOne 內先防禦式砌好（chk101SignHtml），兩個公佈 modal 共用；殺青直接呼叫。
ok('CHK101 接入點（簽約砌圖＋兩 modal 引用＋殺青）', html.count('chk101Html({') >= 2 and html.count('chk101SignHtml') >= 3)
ok('CHK101 抬頭用全名陳偉翔', 'const CHK101_PAYEE = "陳偉翔"' in html)


# 第二部分：UI 文案精煉守門（系統味舊句已清、新句在位）
for gone in ('試玩規則：', '免費（試玩）', '試玩不耗日', '工程標籤表', '確認耗日', '後果講明：',
             '估清', '預覽說明（唔清債）', '還款失敗', '僅遠望 · 無互動', '點開查看通告',
             '點此改行程', '仍要試玩進行', '暫時去不成', '劇情進行中，完結後再返屋企', '第2幕條件接近'):
    ok('精煉：舊句已清「' + gone + '」', gone not in html)
for new_s in ('呢步要用一日', '通告欄 · ${L.name}', '沽清', '好感夠就傾多啲：閒談 10 · 忠告 25 · 情報 40',
              '提早休息（過一日）', '劇情進行中，完成對白先可以繼續。', '去試鏡要用一日，結果等何生通知。'):
    ok('精煉：新句在位「' + new_s[:18] + '」', new_s in html)

print()
print('qa101 static: %d fails' % len(fails))
sys.exit(1 if fails else 0)
