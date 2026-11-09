# v20a58 休息加體能 bug 修復 static tests: 四條休息系路徑 apply 唔再含 stamina、
# 提示文案改減壓向、目標建議 stamina 唔再指 rest、硬規則（SAVE key）冇郁。
# 反證: run against a pre-v58 (v20a56) index -> stamina 仍喺 rest 路徑 -> FAIL.
import sys, re

src = open(sys.argv[1] if len(sys.argv) > 1 else 'index.html', encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def fn_body(name):
    i = src.find('function ' + name + '(')
    if i < 0:
        return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{':
            depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    return ''

# --- 四條路徑：apply 入面唔准再有 stamina ---
rp = fn_body('resolvePlannedDay')
chk('resolvePlannedDay present', bool(rp))
m = re.search(r'id==="rest"\)\{\s*notes=apply\(\{([^}]*)\}\)', rp)
chk('rest 日 apply 只減壓（冇 stamina）', bool(m) and 'stamina' not in m.group(1) and 'stress:-' in m.group(1))
m = re.search(r'id==="home_chore"\)\{\s*notes=apply\(\{([^}]*)\}\)', rp)
chk('home_chore apply 冇 stamina（money/stress 保留）', bool(m) and 'stamina' not in m.group(1) and 'money:R(0,200)' in m.group(1) and 'stress:-' in m.group(1))

dr = fn_body('doRest')
m = re.search(r'apply\(\{([^}]*)\}\)', dr)
chk('doRest apply 冇 stamina（只減壓）', bool(m) and 'stamina' not in m.group(1) and 'stress:-' in m.group(1))

eb = fn_body('endBrowseDayGoHome')
m = re.search(r'apply\(\{([^}]*)\}\)', eb)
chk('提早休息 apply 冇 stamina（只減壓）', bool(m) and 'stamina' not in m.group(1) and 'stress:-' in m.group(1))

# --- 文案：減壓向 ---
chk('休息睡覺 hint 改減壓向', 'name:"休息睡覺", hint:"瞓足一日 · 大減壓"' in src)
chk('收拾房間 hint 改減壓向', 'name:"收拾房間", hint:"執屋 · 小減壓"' in src)
chk('舊 hint「大回復體能」已清', '大回復體能' not in src)
chk('doRest 掣標籤改「減壓」', 'add("休息室歇陣","減壓","+1日"' in src)

# --- 目標建議映射 ---
chk('courseForStatKey: stamina 指去武師班（v58 擴展：有真課程，唔再係 rest/null）', 'stamina:"train_stamina"' in src)
chk('courseForStatKey: stress 保留 rest', 'stress:"rest"' in src)
chk('preferredLocForTrainTarget: stamina 唔再入 rest 分支', 'if(stat==="stress" || courseId==="rest")' in src)

# --- 週結 flavor：v58 擴展經用戶拍板已收走三處 stamina 暗加（細節鎖喺 test_stamina58_static） ---
chk('週結 flavor 暗加已收（v58 擴展裁定）', 'pushFlavor(apply({stamina:8, stress:-6}))' not in src and 'pushFlavor(apply({stress:-6}))' in src)

# --- 硬規則 ---
chk('SAVE key unchanged', 'starVolunteer_map_v19w' in src)

if fails:
    print('FAILURES:', ' | '.join(fails))
    sys.exit(1)
print('ALL PASS')
