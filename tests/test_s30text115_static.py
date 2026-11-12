# v20a115 S-30 TEXT115・靜態守門測試：通告詳情卡混亂文字重寫（《賀歲特輯》用戶實玩反饋）。
# 用法：python3 tests/test_s30text115_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」（舊寫法出現即 FAIL）。
# 只改文字，唔郁 v111 版式；數字（片酬／簽約金／違約金／日數／期限）一律唔變。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def body_of(fname, span=12000):
    i = html.find(fname)
    return html[i:i + span] if i >= 0 else ''

b = body_of('function castingNoticeDetailHtml', 12000)

# --- 1. 檔期行：一個概念（label 用值入面嘅動詞，值刪前綴）---
ok('T1 檔期行 label 係「預計播出」', '<span class="k">${relMatch115 ? "預計"+relMatch115[1] : "預計播出"}</span>' in b)
ok('T1 舊寫法「檔期」label 唔再喺 releaseRow88', '<span class="k">檔期</span><span class="v">${release88}</span>' not in b)
ok('T1 值刪「預計播出：」前綴（regex 拆 verb＋值）', 'match(/^預計(播出|上映|推出)：(.*)$/)' in b)
ok('T1 gigReleaseLine88 本身唔郁（seasonTipHtml 括號仲要前綴）',
   'function gigReleaseLine88(g)' in html and 'return "預計"+verb+"："+y+" 年"+seasonWord;' in html)
ok('T1 檔期行唔同通告期間重複：期間行仍係「通告期間」',
   '<span class="k">通告期間</span>' in b)

# --- 2. var-note：拆做三行短句，一行一個概念 ---
ok('T2 新 var-note 三行在', '成數受表現／壓力／信用影響。<br>片酬牌面係約數，實收按合約。<br>獲聘先收三成簽約金，餘額殺青先收。' in b)
ok('T2 舊四合一長句唔在', '成數受表現／壓力／信用影響；片酬牌面為約酬區間，試鏡後要等劇組回音，獲聘簽約先收三成簽約金，餘額殺青按合約實收。' not in b)
ok('T2 「成數」原句保留（test_terms57 B7 計數仍係 2；v128 A4 N9 刪咗落選 modal 嗰份）', html.count('成數受表現／壓力／信用影響') == 2)

# --- 3. 等回音只留一個版本（底部 note）---
ok('T3 底部 note「去試鏡要用一日，結果等何生通知。」仍在',
   '去試鏡要用一日，結果等何生通知。' in html)
ok('T3 段嘢入面「試鏡後要等劇組回音」已刪', '試鏡後要等劇組回音' not in html)

# --- 4. 簽約金時點：機制核查反證＋行字 ---
ok('T4 機制：簽約金只喺公佈獲聘嗰刻入帳', '簽約金＝合約額三成，公佈嗰刻即付' in html)
ok('T4 機制：doAudition 接通告嗰刻唔入帳（body 無 apply({money／S.money）',
   (lambda _b: ('apply({money' not in _b) and ('S.money' not in _b))(html[html.find('function doAudition('):html.find('function rarityDot(', html.find('function doAudition('))]))
ok('T4 摘要行寫「獲聘後即收」', '（獲聘後即收）' in b)
ok('T4 舊寫法「接通告後即收」全檔清零', '（接通告後即收）' not in html)
ok('T4 詳細區「簽約即付」已隨詳細區刪除（v20a117 S-30 DEDUP117：嗰句同 var-note 第三行「獲聘先收三成簽約金，餘額殺青先收」重複，成段刪除係應有之義；摘要保留同一時點，機制不變）', '簽約即付，餘額殺青入帳' not in b and '獲聘先收三成簽約金，餘額殺青先收。' in b)

print('---')
print('PASS' if not fails else 'FAIL: ' + '; '.join(fails))
sys.exit(1 if fails else 0)
