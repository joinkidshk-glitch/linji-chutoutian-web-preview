# v20a55 TEXTFIX static tests: cleaner block + call sites wired, and the
# audited display strings are gone from player-facing source positions.
# Block-aware: strings that legitimately remain are match patterns inside
# the TEXTFIX55 tables (code), QA ban-lists, or speaker registries.
# 反證: run against a pre-v55 index -> TEXTFIX55 block missing -> FAIL.
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
block = src[a:b] if 0 <= a < b else ''
outside = (src[:a] + src[b:]) if 0 <= a < b else src
# v20a297：ROM176 段再無關海媚；下面剔走段邏輯留返（無害，A5／A6／C10 掃描範圍不變）。
_rs = outside.find('/* ===== v20a176 ROM176')
_re = outside.find('/* ---------- 殺青回望', _rs) if _rs >= 0 else -1
if _rs >= 0 and _re > _rs:
    outside = outside[:_rs] + outside[_re:]

# call sites
chk('call: copy packs cleaned', 'textfix55SimplePack(giftItems)' in src and 'TEXTFIX55_OPTS_GIFT' in src)
chk('call: story packs cleaned', 'textfix55StoryPack(main)' in src and 'textfix55RivalSpeakers(rival)' in src)
chk('v267 call: tutorial overlay call 已隨傳聞教學一併刪', 'textfix55SimplePack(TUTORIAL_PHASE2_STEPS56_OVERLAY)' not in src and 'TUTORIAL_PHASE2_STEPS56_OVERLAY' not in src)
chk('call: freeplay cleaned', 'textfix55Freeplay(FREEPLAY_FW)' in src)
chk('RW-7: gig clean fn removed', 'textfix55GigRecord(o)' not in src and 'textfix55GigField' not in src and 'textfix55DropSents' not in src)
chk('call: phase3 star sightings looks', 'textfix55SimplePack(data)' in src and 'TEXTFIX55_STAR_LOOKS[st.starId]' in src)

# A1/A2: journal dev text
# v20a162：dev 分支空狀態「暫時未有選角標籤。」隨閘一併刪除；真空狀態留返
# 「暫時未有選角印象。」嗰句（renderCastingTagsPane 玩家分支原有文案）。
chk('A1 journal empty-state natural', '暫時未有選角印象' in src and '[DEV] 選角標籤' not in src)
chk('A1 dev label gone everywhere', src.count('[DEV]') == 0)
# A6: trial-gate wording out of display source (patterns may remain in tables)
chk('A6 no trial-gate outside tables', '試玩閘' not in outside)
chk('A6 start-screen li natural', '試玩閘：' not in src and '不計日子（茶錢另計）' in src)
# A5: gift placeholder fallback
chk('A5 gift fallback de-placeholdered', '（佔位）' not in outside)
# A9/C10: screenshot strings out of display source
chk('C10 debt toast natural', '請截圖回報' not in src)
chk('C10 press headline natural', '俾人截圖' not in outside)
# favor-debt fallback placeholder
chk('debt fallback natural', 'line || "（文案待補）"' not in src and 'line || "人情一筆"' in src)
# KHM (v297)：Vera／關海媚成個移除——全檔只剩 v151 歷史註解一句關海媚（見 test_kwan151_static A0）。
chk('KHM v297：全檔只剩 v151 歷史註解一句', src.count('關海媚') == 1 and 'v151 退役：關海媚名禁令已撤' in src)
chk('KHM cleaner pattern removed (v151)', '"關海媚", "當紅花旦"' not in block)
# A8: undefined jargon in story hint overrides replaced
chk('A8 hint overrides natural', outside.count('雙軌總和夠數') == 0 and '聲望和信用總和足夠' in src)
# item name unified
chk('item name unified outside tables', '淡香氛樣品瓶' not in outside and '淡香水試用裝' in outside)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
