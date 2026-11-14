# v20a208 頒獎禮逐格宣佈 static tests：
# (1) 新函數在位：awards208CatRank／awards208NightCats／awards208NomineeSlotIdx；
#     beats 帶 catIdx／catId 上下文，player 喺格轉換嗰陣重建（applyCatState208）。
# (2) 格次序：配角先、主角後、男主角壓軸；music 新人獎→女歌手→男歌手。
# (3) beat 規格：catTitle 1200、nominee 2000、suspense 1400、reveal 2100；open／out 成晚一次；
#     enter 只限玩家格之前一次；walkup／glamour／comfort 只限玩家格。
# (4) 逐位宣佈：nominee beat 有 nomineeIdx／slotIdx，卡片只出已宣佈嗰啲（syncCards 閘）；
#     舞台逐格重建唔拆 stage（guard 唔見空隙）；跳過掣 finish() 成晚完。
# (5) 邊界：fellows 空 → 通用提名 beat＋揭曉 fallback；全表空／冇 ceremonyId → 跌返舊單格。
# (6) 唔郁嘅機制：seeded fellows、D4 贏線 0.875、comfort 文案、fanfare 只限玩家格贏嗰格揭曉、
#     結果卡／報紙成晚完先出一次（presentAwardResult／finishSkip 流程不變）。
# (7) 硬規則：SAVE key 不變；softRev／?v= 不變；唔改 content pack JSON。
# 反證：對 pristine main 行 → v208 條款唔存在 → 乾淨 FAIL（exit 1，唔 crash）。
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
rank_fn = slice_fn('awards208CatRank')
slot_fn = slice_fn('awards208NomineeSlotIdx')
play_fn = slice_fn('awards62PlayCeremony')

# --- (1) 新函數在位 ---
chk('v208 標記喺 beats／night 附近', 'v20a208' in src)
chk('awards208CatRank 在位', 'function awards208CatRank(c)' in src)
chk('awards208NightCats 在位', 'function awards208NightCats(pack)' in src)
chk('awards208NomineeSlotIdx 在位', 'function awards208NomineeSlotIdx(' in src)
chk('beats 用 night208 多格分支', 'night208' in beats_fn and 'awards208NightCats(pack)' in beats_fn)
chk('player 喺格轉換嗰陣重建（applyCatState208）',
    'applyCatState208' in play_fn and 'function awards208NightCats' not in play_fn)
chk('__awards 暴露 night208／order208', 'night208: awards208NightCats' in src and 'order208: awards208CatRank' in src)

# --- (2) 格次序 ---
chk('配角先（support rank 0／1）', 'role === "support"' in rank_fn and 'g === "m" ? 0 : 1' in rank_fn)
chk('主角後、男主角壓軸（lead 女 2／男 3）', 'role === "lead"' in rank_fn and 'g === "f" ? 2 : 3' in rank_fn)
chk('music：新人獎先（newcomer 0）、女歌手 1、男歌手 2',
    'role === "newcomer"' in rank_fn and 'role === "singer"' in rank_fn and 'g === "f" ? 1 : 2' in rank_fn)
chk('未知 role 排最後（rank 9）', 'return 9' in rank_fn)
chk('night 按 rank 排序', 'awards208CatRank(a) - awards208CatRank(b)' in night_fn)

# --- (3) beat 規格 ---
chk('格標題 beat（catTitle 1200）', 'id: "catTitle", ms: 1200' in beats_fn)
chk('提名人 beat（nominee 2000）', 'id: "nominee", ms: 2000' in beats_fn)
chk('懸念 1400／揭曉 2100', 'id: "suspense", ms: 1400' in beats_fn and 'id: "reveal", ms: 2100' in beats_fn)
chk('open／out 成晚一次（多格分支各推一次）',
    beats_fn.count('id: "open"') >= 1 and 'id: "out", ms: 500' in beats_fn)
chk('enter 只限玩家格之前一次', 'ci === focusIdx208' in beats_fn and 'id: "enter", ms: 1750' in beats_fn)
chk('walkup／glamour／comfort 只限玩家格（isFocus 閘）',
    'nc.isFocus && best === "won"' in beats_fn and 'nc.isFocus && best === "nominated"' in beats_fn)
chk('舊 names 快閃 beat 唔喺多格分支出現',
    'id: "names"' not in beats_fn.split('if(night208 && night208.length){')[1].split('let focus = null;')[0]
    if 'if(night208 && night208.length){' in beats_fn and 'let focus = null;' in beats_fn else False)
chk('beats 帶 catIdx／catId 上下文', 'catIdx: ci' in beats_fn and 'catId: nc.id' in beats_fn)

# --- (4) 逐位宣佈＋轉格＋跳過 ---
chk('nominee beat 有 nomineeIdx／slotIdx', 'nomineeIdx: ni' in beats_fn and 'slotIdx: awards208NomineeSlotIdx' in beats_fn)
chk('卡片只出已宣佈嗰啲（syncCards nominee 閘）',
    'b.id === "nominee"' in play_fn and 'i <= b.nomineeIdx' in play_fn)
chk('逐位宣佈字幕：入圍名單進度＋獎項名',
    '入圍名單' in play_fn and 'nomineeTotal' in play_fn)
chk('轉格重建 slots／卡片／白牌，唔拆舞台（removeChild 全場只得 cleanup 一處）',
    'buildSlots208' in play_fn and 'cardsInnerHtmlFor208' in play_fn and 'awd181-t' in play_fn and
    play_fn.count('removeChild') == 1)
# v20a212 C1 根因：cardsHtmlFor208 改名 cardsInnerHtmlFor208（只回傳內層卡片，唔包容器）
chk('轉格嗰陣卡片 on 即刻拎走（新格逐張出）', 'classList.remove("on")' in play_fn)
chk('跳過掣 finish() 成晚完（唔係跳格）', 'skipBtn.addEventListener("click"' in play_fn and 'finish()' in play_fn)
chk('全晚 fellows 一次過預載', 'night208.forEach(nc=> (nc.fellows' in play_fn)

# --- (5) 邊界 ---
chk('fellows 空 → 通用提名 beat', '入圍名單逐個唱出……' in beats_fn)
chk('fellows 空 → 揭曉 fallback 文案', '今晚嘅得獎者誕生' in beats_fn)
chk('非玩家格得主＝fellows[0]', 'winner = fellows[0]' in night_fn)
chk('玩家格贏 → winner null（得主係阿偉）', 'pc.outcome === "won") winner = null' in night_fn)
chk('全表空／冇 ceremonyId → night 回 null（跌返舊單格）',
    'if(!pack || !pack.ceremonyId) return null' in night_fn and
    '!Array.isArray(table) || !table.length) return null' in night_fn)

# --- (6) 唔郁嘅機制 ---
chk('D4 贏線 0.875 唔郁', 'const AWARDS62_WIN_LINE = 0.875' in src)
chk('comfort 文案不變（何生安慰＋阿偉回應）', '何生拍拍你膊頭' in beats_fn)
chk('fanfare 只限玩家格贏嗰格揭曉', 'curOutcome208 === "won"' in play_fn)
chk('結果卡流程不變（presentAwardResult 照舊）',
    'awards62PlayCeremony(pack, ()=>presentAwardResult(pack, cont))' in src)
chk('推辭 finishSkip 流程不變', 'finishSkip' in src and 'declined:true' in src)

# --- (7) 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變（s107）', 's107' in src)
chk('?v= 不變（v20a10）', 'v20a10' in src)
chk('唔改 content pack JSON（新 code 唔掂 content/）',
    'content/' not in night_fn and 'content/' not in beats_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
