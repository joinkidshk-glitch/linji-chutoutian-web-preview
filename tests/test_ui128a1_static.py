# v20a128 A1 地圖一屏包・靜態守門測試。
# 用法：python3 tests/test_ui128a1_static.py [path-to-index.html]
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

# 標籤座標微調（§7 建議稿；金禧 3% 會因 translate(-50%,-50%) 出界，實測改 11%）
ok('標籤 星河電視台', 'left:26%;top:2%">星河電視台' in html)
ok('標籤 金禧大酒店', 'left:11%;top:32%">金禧大酒店' in html)
ok('標籤 薄扶林', 'left:34%;top:50%">薄扶林' in html)
ok('標籤 灣仔', 'left:56%;top:68%">灣仔' in html)
ok('標籤 銅鑼灣', 'right:6%;top:66%">銅鑼灣' in html)
ok('標籤 舊座標唔見（星河 14%／金禧 44.5%）', 'top:calc(14% - 50%)">星河電視台' not in html and 'top:44.5%">金禧大酒店' not in html)

# 浮「進度」掣取消，進度入口只留頂欄 chip（計劃 §5／§7 mockup；反轉 v108 S-8）
ok('浮進度掣 HTML 已刪', 'id="map-progress-btn"' not in html)
ok('進度入口：頂欄 chip 恢復做 button', '<button type="button" class="chip chip-story" id="chip-story"' in html)
ok('進度入口：chip 有 click 接線入進度頁', 'cs.addEventListener("click"' in html)
# 全部地點掣搬入底部卡（paintBar 模板 map-hint-top128 入面，唔再喺 HUD bar-secondary）
_i = html.find('map-hint-top128"><span')
_tpl = html[_i:_i + 600] if _i >= 0 else ''
ok('全部地點掣搬入底部卡', 'map-hint-top128' in html and 'id="map-show-all-locs"' in _tpl)

# 壓力 bar 加粗＋數字加粗
ok('壓力 track 12px', '#app .hud-stress-track{ height:12px; }' in html)
ok('壓力數字 .94rem', '#app .hud-stress-val{ font-size:.94rem; }' in html)

# 底部卡改米紙卡
ok('底部卡米紙＋金邊', '#v-map .map-hint{\n  background:#fffdf6 !important; border:2px solid #c97f1f !important;' in html)
ok('過一日全寬金掣', '.map-hint .map-start-today{\n  display:block !important; width:100% !important;' in html)

# N11：toast-up 嗰陣底部卡唔再隱藏
ok('N11 toast-up 底部卡保持可見', '#app.toast-up:has(#v-map.view.on) #map-hint{' in html and 'visibility:visible !important' in html)

# 劇情卡 2 行截斷（內層 span 做 clamp，button 本身唔食）
ok('劇情卡內層 span 2 行截斷', 'map-hint-story-in128' in html and '-webkit-line-clamp:2 !important;' in html)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
