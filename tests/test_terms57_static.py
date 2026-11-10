# v20a57 TERMS static tests: player-facing source strings in index.html must be
# free of the audited A-class terms after the v57 pass. Block-aware:
# - the TEXTFIX55/57 cleaning region is excluded (its table KEYS legitimately
#   hold the old pack strings; values are checked by the logic test);
# - JS comments are skipped by the tokenizer;
# - legit remaining literals are whitelisted explicitly: QA ban-probes
#   ("聲量" inside indexOf checks), the fame-source alias ("幕前聲量"), the
#   speaker-registry legacy key ("周刊編輯", kept as alias), and the tutorial
#   provenance string (hard-gate／事態入口, metadata, never displayed).
# 反證: run against a pre-v57 index -> TEXTFIX57 missing + terms present -> FAIL.
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else 'index.html', encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

a = src.find('/* ==== v20a55 TEXTFIX')
b = src.find('async function refreshCopyPacksFromDisk(){')
chk('TEXTFIX55 block present', 0 <= a < b)
region = src[a:b] if 0 <= a < b else ''
outside = (src[:a] + src[b:]) if 0 <= a < b else src

chk('TEXTFIX57 tables present in region', 'TEXTFIX57_EXACT' in region and 'TEXTFIX57_PHRASES' in region and 'TEXTFIX57_GIG_REQ' in region and 'TEXTFIX57_KEY_RENAME' in region)
chk('TEXTFIX57 hooks wired', 'TEXTFIX57_EXACT, t' in region and 'TEXTFIX57_PHRASES' in region and 'FW.castingTagsReg' in region)

# ---- compact JS string tokenizer (skips // and /* */ comments) ----
def string_contents(text):
    out = []
    i, n = 0, len(text)
    prev = ''
    stack = []
    mode = 'code'
    tstart = 0
    while i < n:
        c = text[i]
        if mode == 'code':
            two = text[i:i+2]
            if two == '//':
                j = text.find('\n', i)
                i = n if j < 0 else j + 1
                continue
            if two == '/*':
                j = text.find('*/', i + 2)
                i = n if j < 0 else j + 2
                continue
            if c in ("'", '"'):
                j = i + 1
                while j < n:
                    if text[j] == '\\':
                        j += 2
                        continue
                    if text[j] == c:
                        break
                    j += 1
                out.append(text[i+1:j])
                prev = c
                i = j + 1
                continue
            if c == '`':
                mode = 'tpl'
                tstart = i + 1
                i += 1
                continue
            if c == '/' and prev in ('', '=', '(', ',', '+', '!', '&', '|', '?', ':', ';', '{', '[', '}', 'return', 'case'):
                j = i + 1
                incls = False
                while j < n:
                    ch = text[j]
                    if ch == '\\':
                        j += 2
                        continue
                    if ch == '[':
                        incls = True
                    elif ch == ']':
                        incls = False
                    elif ch == '/' and not incls:
                        break
                    elif ch == '\n':
                        break
                    j += 1
                i = j + 1
                while i < n and text[i].isalpha():
                    i += 1
                prev = '/'
                continue
            if c == '{':
                if stack and stack[-1][0] == 'tpl':
                    stack[-1] = ('tpl', stack[-1][1] + 1)
                prev = '{'
                i += 1
                continue
            if c == '}':
                if stack and stack[-1][0] == 'tpl':
                    if stack[-1][1] == 0:
                        stack.pop()
                        mode = 'tpl'
                        tstart = i + 1
                        i += 1
                        continue
                    stack[-1] = ('tpl', stack[-1][1] - 1)
                prev = '}'
                i += 1
                continue
            if not c.isspace():
                if c.isalpha():
                    j = i
                    while j < n and (text[j].isalnum() or text[j] == '_'):
                        j += 1
                    prev = text[i:j] if text[i:j] in ('return', 'case', 'typeof') else 'x'
                    i = j
                    continue
                prev = c
            i += 1
            continue
        else:
            if c == '\\':
                i += 2
                continue
            if c == '`':
                out.append(text[tstart:i])
                mode = 'code'
                prev = '`'
                i += 1
                continue
            if c == '$' and text[i:i+2] == '${':
                out.append(text[tstart:i])
                stack.append(('tpl', 0))
                mode = 'code'
                prev = '{'
                i += 2
                continue
            i += 1
            continue
    return out

strings = string_contents(outside)

def bad(term, whitelist):
    return [s for s in strings if term in s and not whitelist(s)]

chk('A1 zero 事態 in player strings',
    not bad('事態', lambda s: '事態入口' in s and 'PLAN_GIG_CARD' in s))
chk('A2 zero 聲量 in player strings',
    not bad('聲量', lambda s: s.strip() in ('聲量', '幕前聲量')))
chk('A3 zero 刷新 in player strings', not bad('刷新', lambda s: False))
chk('A4 zero 點擊 in player strings', not bad('點擊', lambda s: False))
chk('B1 zero 解鎖 in player strings', not bad('解鎖', lambda s: False))
chk('B6 zero 周刊 in player strings',
    not bad('周刊', lambda s: s == '周刊編輯'))

# ---- HTML chrome (text nodes are not JS strings) ----
chk('A1 chip label', 'title="有可播劇情">劇情<span class="chip-story-n"' in src)
chk('A1 menu label', 'class="menu-story">劇情 <span class="menu-badge"' in src)
chk('A1 no 事態 text node', '>事態<' not in src and '>事態 <' not in src)

# ---- spot outcomes ----
chk('A3 board toast', '廣告通告欄更新咗：有新通告' in src and '通告欄更新咗' in src)
chk('B5 deposit wording', '"存款不足 $"+fee+"——債項未清。"' in src and '存款亦不足 $200' in src)
chk('B7 成數 note x3', src.count('成數受表現／壓力／信用影響') == 3)
chk('B7 success-rate labels kept', '成功率約' in src)
chk('B2 gate/tag values renamed', src.count('"身手好"') >= 6)
chk('B2 ending neg tags', '["八卦", "耍大牌", "高冷", "爛片"]' in src)
chk('B2 legacy save migration', '舊存檔標籤改名遷移' in src)
chk('B6 speaker alias kept+added', '"周刊編輯":"generic_mag_editor","週刊編輯":"generic_mag_editor"' in src)
# v20a75 改版：進階課已併入級別，舊 unlock 句『進階演技課開放咗』唔再存在——
# 改驗 v75 升級提示句『升到二級』（措辭跟用戶拍板）。
chk('B1 journal unlock wording', '手帳「訓練」開放咗' in src and '升到${LEVELS75_NAMES' in src and '進階演技課開放咗' not in src)
chk('B3 romance ladder wording', '（關係約到2）' in src)
chk('B3 /100 好感 kept', '點好感就開到「' in src)

# ---- C-class vocabulary untouched (spot presence) ----
for w in ['拼合', '人情債', '手帳', '殺青', '通告', '主線', '相遇', '剛聽聞']:
    chk('C kept: ' + w, w in src)

print('FAILURES: ' + ', '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
