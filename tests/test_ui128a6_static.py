# v20a128 A6 設定／選單收尾包・靜態守門測試（對白速度紙掣／S-20）。
# 用法：python3 tests/test_ui128a6_static.py [path-to-index.html]
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

# 對白速度：系統 <select> 改紙掣式四格選擇
ok('速度 紙掣容器在', 'class="set-speed128"' in html)
ok('速度 四格掣在（慢／中／快／即出）', 'data-v="slow"' in html and 'data-v="normal"' in html and 'data-v="fast"' in html and 'data-v="instant"' in html)
ok('速度 隱藏欄位 #set-speed 在（關閉 handler 照讀 .value）', 'type="hidden" id="set-speed"' in html)
ok('速度 舊 <select id="set-speed"> 已刪', '<select id="set-speed">' not in html)
ok('速度 紙掣 CSS 在（米紙底＋金邊＋選中金底）', '.set-speed128 .set-speed-btn.on{ background:#c97f1f' in html)
ok('速度 撳掣同步隱藏欄位＋on 態', 'hid.value = b.getAttribute("data-v")' in html)

# S-20：返回地圖搬去手帳頂部，底部只留主 CTA＋細還原
ok('S-20 返回地圖容器搬去頂部（喺 home-tabs 之前）',
   'id="home-tab-exit"' in html and html.find('id="home-tab-exit"') < html.find('id="home-tabs"'))
ok('S-20 返回地圖頂部行唔再係 sticky 底部 bar', '#home-tab-exit{ position:static;' in html)
ok('S-20 還原收細做次要掣', '#nb-actions #btn-reset-plan{ min-height:34px;' in html)
ok('S-20 返回掣本身仍係細掣（舊規則保留）', '#home-tab-exit #home-back-map-tabs{ flex:0 0 auto !important; width:auto !important;' in html)
ok('S-20 返回掣文字不變', 'id="home-back-map-tabs">返回地圖</button>' in html)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
