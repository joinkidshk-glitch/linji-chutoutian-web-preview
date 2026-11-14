# v20a215 推出日提及 static tests：
# (1) source "release" 入 enqueue 正規化白名單（唔跌返 wrap）
# (2) buildNewspaperEdition 排序：release 永遠排最後
# (3) 掛點：advanceDay tick（跟 news82Tick 同位）＋ pullDue 開頭懶掃
# (4) 觸發規則：只限 base 級、wrappedDay < releaseDay、releaseDay <= today、去重 key release:<gigId>
# (5) 文案：季節寫法（春季／夏季／秋季／冬季＋上映／播出／推出），唔讀 releaseLabel
# (6) 唔郁：SAVE key、softRev、?v=、見報門檻、聲望幅度、剪報上限 40、content pack JSON
# 反證：對 pristine main 行 → v215 條款唔存在 → 乾淨 FAIL（exit 1，唔 crash）。
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

enq_fn = slice_fn('enqueueNewspaperItem')
build_fn = slice_fn('buildNewspaperEdition')
pull_fn = slice_fn('pullDueNewspaperEdition')
adv_fn = slice_fn('advanceDay')
rel_fn = slice_fn('release215EnqueueDue')
copy_fn = slice_fn('release215CopyFor')
day_fn = slice_fn('release215ReleaseDay')

# --- (1) source "release" 正規化 ---
chk('source：enqueue 正規化認 "release"（唔跌返 wrap）',
    'srcRaw==="release" ? "release"' in enq_fn)
chk('source：未知 source 照舊跌返 wrap',
    ': "wrap"' in enq_fn)

# --- (2) 排序排最後 ---
chk('排序：buildNewspaperEdition 有 release 排最後規則',
    'a.source==="release"' in build_fn and 'b.source==="release"' in build_fn)
chk('排序：release 排最後行喺 award 規則之後',
    build_fn.find('source==="award"') < build_fn.find('source==="release"'))
chk('排序：release 唔係靠 fameDelta 排（fameDelta 0 照排最後）',
    'return ra-rb' in build_fn)

# --- (3) 掛點 ---
chk('掛點：advanceDay 行 release215EnqueueDue（跟 news82Tick 同位）',
    'release215EnqueueDue' in adv_fn)
chk('掛點：advanceDay 嘅 release tick 喺 news82Tick 之後',
    adv_fn.find('news82Tick') < adv_fn.find('release215EnqueueDue'))
chk('掛點：pullDue 開頭懶掃（計到期之前）',
    'release215EnqueueDue' in pull_fn and
    pull_fn.find('release215EnqueueDue') < pull_fn.find('newspaperDueItems'))
chk('掛點：兩處呼叫都有 typeof＋try 守衛（舊環境唔 crash）',
    'typeof release215EnqueueDue' in adv_fn and 'typeof release215EnqueueDue' in pull_fn)

# --- (4) 觸發規則 ---
chk('規則：掃 wrapHistory',
    'S.wrapHistory' in rel_fn)
chk('規則：只限 base 級（press94IsBaseRole／press94RoleClass）',
    'press94IsBaseRole' in rel_fn and 'press94RoleClass' in rel_fn)
chk('規則：推出日當日／之後先殺青唔出（wrappedDay >= releaseDay 即 skip）',
    'wrappedDay' in rel_fn and '>= relDay' in rel_fn)
chk('規則：未到推出日唔出（releaseDay > today 即 skip）',
    'relDay > today' in rel_fn)
chk('規則：去重 key 係 release:<gigId>',
    '"release:"+String(entry.gigId)' in rel_fn)
chk('規則：fameDelta 0、唔點名（唔傳玩家名入 headline／dek）',
    'fameDelta: 0' in rel_fn and 'clipLabel: "娛樂版・推出"' in rel_fn)
chk('規則：enqueuedDay＝publishDay - 1（同日到期先併到同一批）',
    'enqueuedDay: today-1' in rel_fn and 'publishDay: relDay' in rel_fn)
chk('規則：入隊唔即刻存檔（persist:false，靠晨報 commit／日結存檔）',
    'persist:false' in rel_fn)

# --- (5) 文案 ---
chk('文案：季節詞表齊四季（春季／夏季／秋季／冬季）',
    '"春季"' in src and '"夏季"' in src and '"秋季"' in src and '"冬季"' in src)
chk('文案：動詞按媒介（電影上映／電視播出／其餘推出）',
    '"上映"' in copy_fn and '"播出"' in copy_fn and '"推出"' in copy_fn)
chk('文案：release215 成段唔讀 releaseLabel（賀歲檔 label 唔會漏入）',
    'releaseLabel' not in rel_fn and 'releaseLabel' not in copy_fn)
chk('文案：headline 係《作品》＋季節＋動詞',
    '"《"+work+"》"+seasonWord+verb' in copy_fn)
chk('觸發日：季首日對照表春 3／夏 6／秋 9／冬 12',
    '"春":3' in src and '"夏":6' in src and '"秋":9' in src and '"冬":12' in src)
chk('觸發日：1990-01-01 起計（Date.UTC(1990, 0, 1)）',
    'Date.UTC(1990, 0, 1)' in day_fn)

# --- (6) 唔郁 ---
chk('唔郁：SAVE key 照舊 starVolunteer_map_v19w',
    'const SAVE = "starVolunteer_map_v19w"' in src)
chk('唔郁：剪報上限 40 照舊',
    'if(clips.length>40) clips.length = 40;' in src)
chk('唔郁：wrapHistory 上限 90 照舊',
    'if(S.wrapHistory.length>90) S.wrapHistory.length=90;' in src)
chk('唔郁：殺青報入隊（enqueueNewspaperFromWrap）原封不動',
    'function enqueueNewspaperFromWrap' in src and 'eventKey: "wrap:"+subject.gigId+":"+shootDay' in src)
chk('唔郁：頒獎報入隊（enqueueNewspaperFromAward）原封不動',
    'function enqueueNewspaperFromAward' in src and 'publishDay: day+1' in src)

print()
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
