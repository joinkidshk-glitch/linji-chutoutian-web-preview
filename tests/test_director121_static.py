# v20a121 DIRECTOR121・靜態守門測試：職銜關鍵字規則取代 v117 窮舉 Set。
# 用法：python3 tests/test_director121_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」——喺 pristine main（v118，
# 仲係 GIG_DIRECTOR_GENERIC117 Set）跑，全檔必須 FAIL（見底註）。
# 只改導演欄判定：唔改 SAVE key／softRev／?v=／content pack；S-30 卡渲染路徑不變。
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

b = body_of('function castingNoticeDetailHtml', 14000)

# --- 1. 舊窮舉已刪，新關鍵字規則在 ---
ok('R1 舊 GIG_DIRECTOR_GENERIC117 Set 已刪', 'GIG_DIRECTOR_GENERIC117' not in html)
ok('R1 舊 Set 字面 new Set([副導…]) 已刪', 'new Set(["副導"' not in html)
ok('R1 新關鍵字表 GIG_DIRECTOR_ROLE_KEYWORDS121 在', 'const GIG_DIRECTOR_ROLE_KEYWORDS121' in html)
ok('R1 新判定 gigDirectorIsRoleValue121 在', 'function gigDirectorIsRoleValue121' in html)
ok('R1 判定用子串（indexOf）唔係全等', 'indexOf(GIG_DIRECTOR_ROLE_KEYWORDS121[i])' in html)
ok('R1 helper 名 gigDirectorRealName117 保留（舊測試／S-30 卡沿用）',
   'function gigDirectorRealName117' in html)
ok('R1 helper 行新判定（唔再讀舊 Set）', 'gigDirectorIsRoleValue121(s)' in html)
ok('R1 gigDirectorLabel fallback「組製未公開」保留', 'return "組製未公開";' in html)

# --- 2. 25 個關鍵字齊晒（按工種分組，註解列明） ---
KW = ["副導","助導","導演",
      "監製","製片","製作","組製","統籌",
      "場務","場記","武指","武術","指導",
      "攝影","燈光","收音","剪接","後期",
      "編劇","宣傳","客戶",
      "助理","幕後","未公開","待定"]
ok('R2 25 個關鍵字全部喺表入面', all('"%s"' % k in html for k in KW))
ok('R2 註解列明分組＋點解揀呢啲字（維護說明）',
   '職銜關鍵字規則' in html and '點解揀呢啲字' in html)
ok('R2 註解更正 v117 普查數字（137 真名／46 職銜值）',
   '137 張真名' in html and '46 職銜值' in html)
ok('R2 註解寫明誤殺檢查方法（對住實池真名逐個子串碰撞）',
   '子串碰撞檢查' in html)
ok('R2 註解寫明已知限制（混合值「導演陳大文」會成個濾走）',
   '混合值' in html)

# --- 3. 顯示路徑：S-30 卡仍然係唯一導演顯示路，經 helper ---
ok('R3 詳情卡仍然用 directorRow117', 'const directorRow117' in b and '${directorRow117}' in b)
ok('R3 directorRow117 仍然讀 gigDirectorRealName117',
   'gigDirectorRealName117(g)' in b)
ok('R3 詳情卡冇第二條直接讀 director 顯示嘅路（舊寫法「導演：${dir}」仍清零）',
   '導演：${dir}' not in html)
ok('R3 導演行仍然係 cn-sum-row（版式不變）',
   '<div class="cn-sum-row"><span class="k">導演</span>' in b)

# --- 4. 紀律：紅線不變 ---
ok('R4 SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('R4 softRev s107 不變', 's107' in html)
ok('R4 產品 ?v= v20a10 不變', 'v=20a10' in html)

print('---')
print('PASS' if not fails else 'FAIL: ' + '; '.join(fails))
sys.exit(1 if fails else 0)
