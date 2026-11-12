# v20a128 A4 通告欄＋文字清理・靜態守門測試（N1／N15-1／🔒／N14／N18／N12／N9／N10／S-44）。
# 用法：python3 tests/test_ui128a4_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → 新寫法缺席 → 乾淨 FAIL。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# N1：主頁底 dev 字「本頁修訂 s107。」清走
ok('N1 dev 修訂字已刪', '本頁修訂 s107' not in html)
ok('N1 #start-soft-tip 元素保留（有真玩家內容）', 'id="start-soft-tip"' in html)

# N15-1：通告詳情「💡 有情報」改手繪 sparkle 圖標
ok('N15-1 有情報用 sparkle 手繪圖', 'iconHtml112("✨")' in html and '💡 有情報' not in html)

# 🔒：冇 lock 線圖標，用 CSS 畫鎖
# （舊版已有 .sp-lock-ico class，但係包住 🔒 emoji；新版 span 掏空＋CSS 畫鎖身＋鎖扣。）
ok('🔒 CSS 畫鎖在（鎖身＋::before 鎖扣）', '.sp-lock-ico::before' in html and '.sp-lock-ico{ display:inline-block; width:11px; height:8px;' in html)
ok('🔒 進度頁掣用畫鎖唔用 emoji（span 掏空）', '<span class="sp-lock-ico" aria-hidden="true"></span>劇情未開放' in html)
ok('🔒 舊 🔒 emoji 包喺 span 入面已清', '<span class="sp-lock-ico" aria-hidden="true">🔒</span>' not in html)

# N14：通告列表膠囊改印章／紙籤
# （舊版已有 .gt-pill／.gt-badge selector，斷言要指明新嘅紙籤／印章屬性。）
ok('N14 類型籤米紙＋虛線邊', 'border:1px dashed #a98d4f; box-shadow:0 1px 2px rgba(60,40,10,.25);' in html)
ok('N14 可接印章紅邊＋斜放', 'border:2px solid #b3261e; outline:1px solid #b3261e; outline-offset:2px;\n  letter-spacing:.14em; transform:rotate(-3deg);' in html)
ok('N14 舊藍膠囊唔見', 'background:#3a6ea5; border-radius:999px' not in html)

# N18：通告詳情「劇情簡介」白底 inset 改米紙；老闆 hero 唔裁 bust
ok('N18 簡介框米紙＋虛線邊', 'background:#fbf4dd; border:1px dashed #a98d4f;' in html)
# v20a132 resync：v128 以為老闆圖係 240×312 bust，先將 hero 改 auto「唔裁 46px」；
# 實情 11 張老闆圖全部係全身（480×1424 起，比例 ~3.0），auto 令全身圖 609px 擠壓卡面，
# 真機上標題被切、摘要隱形（v132 回歸）。還原 240px＝v116 胸口以上 crop 原設計。
ok('N18 老闆 hero height 240px（胸口以上 crop；v116 原設計）', 'cn-issuer30v2{ flex:0 0 auto; position:relative; height:240px;' in html)

# N12：壓力明細「而家壓力」vs 高峰打架——改叫「高峰壓力」
ok('N12 高峰壓力 label', '"高峰壓力"' in html)

# N9：落選 modal 刪「成功率約」行（連 var-note 孤兒一併刪）
ok('N9 落選 modal 冇成功率行', '成功率約 ${rec.chancePct}%' not in html)

# N10：週結算文案矛盾句重寫
ok('N10 新句在', '阿媽冇提過半句' in html)
ok('N10 舊矛盾句唔見', '冇打電話嚟催' not in html)

# S-44：人情卡狀態講一次（DEBT_FUZZY 頭三句改純指引）
ok('S-44 未到期純指引', '"未到期":"唔使太急，慢慢還得。"' in html)
ok('S-44 絕響句不變（測試釘死前綴）', '"絕響":"人已不在香港' in html)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
