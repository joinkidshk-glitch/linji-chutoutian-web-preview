# v20a212 頒獎禮逐格流程修復 static tests：
# (A1) glamour 期間收起跳過掣（唔遮 cap 作品名尾段），下一格即刻返嚟。
# (B1) 得主跨格去重（used212／key212／fallback）＋懸念句輪換（SUSPENSE212 三句循環）。
# (C1) 格標題嗰陣卡列預先淡入剪影（preview212），frame 唔留黑洞。根因追加：格轉換
# applyCatState208 舊 code 將成個 <div class="awd63-cards"> 容器塞入 cardsEl.innerHTML，
# 巢狀第二層冇 .on／.preview212，base rule visibility:hidden 令第 2 格起全部卡片隱形
# （外層 probe 顯示 visible，截圖卡列區全空 mean 17.6／max 19）——改做只換內層卡片。
# (C2) advance() 嗰刻即刻 syncCards——卡片同字幕同步出，唔等下一個 rAF tick。
# (C3) 提名 beat 宣佈嗰位改用 reveal 級 spotlight207 光柱＋行前 10→16。
# (C4) walkup 行緊嗰陣，行經路線上嘅提名人向後褪半步＋淡少少。
# (C5) 得 2 位提名人嗰陣置中收窄企位（200／280）。
# 反證：對 pristine main 行 → v212 條款唔存在 → 乾淨 FAIL（exit 1，唔 crash）。
import sys, os

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0: return src[i:k+1]
    return ''

beats_fn = slice_fn('awards62CeremonyBeats')
night_fn = slice_fn('awards208NightCats')
play_fn = slice_fn('awards62PlayCeremony')

# --- (A1) glamour 期間收起跳過掣 ---
chk('A1：跳過掣有 glamour-hide 隱藏規則（display:none）',
    '.awd62-skip.glamour-hide{display:none}' in src)
chk('A1：syncGlamour 按 glamour beat 開／閂跳過掣',
    'skipBtn.classList.toggle("glamour-hide"' in play_fn)
chk('A1：glamour 期間卡列照舊隱藏（choke point 未郁）',
    'cardsEl.classList.toggle("glamour-hide"' in play_fn)
chk('A1：cap 文字唔郁（唔係靠縮短文字避遮擋）',
    'glamRep208' in play_fn and '：《" + glamRep208 + "》' in play_fn)

# --- (B1) 得主跨格去重＋懸念輪換 ---
chk('B1：used212／key212（星＋作品）在位',
    'const used212 = {}' in night_fn and 'key212' in night_fn)
chk('B1：後格排除已贏組合，揀第一位未贏過嘅提名人',
    'fellows.find(f=> f && !used212[key212(f)])' in night_fn)
chk('B1：fallback 沿用 fellows[0]（唔死局）',
    'winner = fellows[0]' in night_fn)
chk('B1：玩家格 won 得主 null 唔入 used、winner63 豁免（預先登記）',
    'focusPc212' in night_fn and 'winner63' in night_fn)
chk('B1：懸念句三句輪換（SUSPENSE212，第一格沿用舊句）',
    'SUSPENSE212' in beats_fn and 'SUSPENSE212[ci % SUSPENSE212.length]' in beats_fn and
    '"得獎者是……"' in beats_fn and '"今晚呢個獎，屬於……"' in beats_fn and
    '"結果揭曉——得獎者是……"' in beats_fn)
chk('B1：懸念時長唔郁（1400ms）', 'id: "suspense", ms: 1400' in beats_fn)

# --- (C1) 格標題卡列剪影 ---
chk('C1：preview212 剪影 CSS 在位（dimmed 0.22）',
    '.awd63-cards.preview212' in src and 'opacity:.22' in src)
chk('C1：syncCards 格標題分支加 on＋preview212',
    'b.id === "catTitle"' in play_fn and 'classList.add("preview212")' in play_fn)
chk('C1：提名 beat 嗰陣除返 preview212（上色上名）',
    'classList.remove("preview212")' in play_fn)
chk('C1 根因：格轉換只換內層卡片（唔巢狀容器）',
    'cardsEl.innerHTML = cardsData.length ? cardsInnerHtmlFor208(cardsData) : ""' in play_fn)
chk('C1 根因：內層 builder 唔包容器（回傳淨係卡片）',
    'const cardsInnerHtmlFor208 = (cd)=>{' in play_fn and 'return cd.map((c, ci)=>{' in play_fn)
chk('C1 根因：建台嗰陣先包容器外殼（唔係格轉換嗰陣）',
    '\'<div class="awd63-cards">\' + cardsInnerHtmlFor208(cardsData) + "</div>"' in play_fn)
chk('C1 根因：冇殘留成個容器塞入 innerHTML',
    'cardsEl.innerHTML = cardsData.length ? cardsHtmlFor208(cardsData)' not in play_fn)

# --- (C2) 卡片同字幕同步出 ---
chk('C2：advance() 嗰刻即刻 syncCards（唔等下一個 rAF tick）',
    'syncCards(beats[beatIdx], 0)' in play_fn)
chk('C2：loop 入面 syncCards 照舊（逐 tick 跟進）',
    'syncCards(b, elapsed)' in play_fn)

# --- (C3) 提名 spotlight 加強 ---
chk('C3：提名 beat 宣佈嗰位用 spotlight207 光柱（唔再係淡 lightPool）',
    'spotlight207(slotCx(i)' in play_fn)
chk('C3：行前幅度加大（10→16）', '16 * fwd208' in play_fn)
chk('C3：懸念 beat 照舊 lightPool（唔郁）',
    'lightPool(slotCx(i)' in play_fn)

# --- (C4) walkup 讓路 ---
chk('C4：walkup 行經路線上嘅提名人向後褪半步＋淡少少',
    'inPath212' in play_fn and 'slotCx(i) < targetX' in play_fn and 'y: inPath212 ? -10 : 0' in play_fn)
chk('C4：行到埗即刻還原（wp＝1 嗰陣唔褪唔淡）',
    'wp < 1' in play_fn)

# --- (C5) 2 位提名人置中收窄 ---
chk('C5：slots 得 2 位嗰陣置中收窄企位（200／280）',
    'if(slots.length === 2) return [200, 280][i]' in play_fn)
chk('C5：3 位企位唔郁（75／240／405）',
    'if(slots.length === 3) return [75, 240, 405][i]' in play_fn)

# --- 唔郁嘅機制 ---
chk('唔郁：舊單格 fallback（冇 ceremonyId）懸念照舊「得獎者是……」',
    beats_fn.count('caption: "得獎者是……"') >= 1)
chk('唔郁：fellows 池本身唔改（night 只係改得主揀選）',
    'fellows = (fellows || []).slice(0, 3)' in night_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
