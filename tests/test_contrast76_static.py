# v20a76 CONTRAST76 static tests：手帳對比度普查修正規則齊（深底亮字組／
# 紙面加深組／金錢晶片／jobs72 inline 副行）、故意淡化項冇被誤改、
# 紅線（SAVE key／softRev／?v=）冇郁。
# 反證：喺 v75 index 上行 → CONTRAST76 block 全缺 → FAIL。
# 量度證據：verify76/audit_before.json／audit_after.json（computed 對比度前後）。
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else 'index.html', encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- block 在位 ---
chk('CONTRAST76 block 在位', 'v20a76 CONTRAST76 手帳對比度普查修正' in src
    and 'v20a76 CONTRAST76 完' in src)

# --- (A) 深底亮字組：修前比值 1.14–2.49 ---
chk('進度標題＋引言提亮', '.prog71-h{ color:#ecdfc2; }' in src
    and '.prog71-intro{ color:#c3b096; }' in src)
chk('拍攝簿／庫存／人脈標題提亮', '.jobs72-h{ color:#ecdfc2; }' in src)
chk('作品牆／回憶（空＋錯過態）標題提亮',
    '.works-empty59 h3, .mem-empty60 h3, .mem-head60 h3{ color:#ecdfc2; }' in src)
chk('拍攝簿條目 .req 提亮（限作品頁）', '#home-pane-works .req{ color:#d9c9a3; }' in src)
chk('記數簿報名行提亮', '#home-pane-ledger .ledger-enroll{ color:#c3b096; }' in src)
chk('人脈提示提亮', '#home-pane-people .people-next{ color:#c3b096; }' in src)
chk('人情債引言提亮（v48 留低嗰頁）', '#home-pane-debt .pane-intro{ color:#e6d7ae; }' in src)
chk('傳聞鬼影字提亮（保 opacity .45 淡化）', '.weak-whisper{ color:#e0d3ac; }' in src)
chk('jobs72 副行 inline 色改淺（4 處）', src.count('color:#b3a284') >= 4)

# --- (C) 金錢晶片：提亮＋狀態色排除 ---
chk('手帳頂金錢晶片提亮＋:not 狀態排除',
    '.home-money:not(.money-warn):not(.money-critical):not(.money-broke)' in src
    and 'color:#e3c565 !important' in src)
chk('money 狀態色原規則冇郁', '.home-money.money-warn{ color:#b86a00 !important; }' in src
    and '.home-money.money-critical{ color:#c0392b !important; }' in src)

# --- (B) 紙面加深組：修前比值 2.89–4.42 ---
chk('行程 hint 加深', '.day-row .nm .plan-hint{ color:#59452a; }' in src)
chk('.act-item .ah 加深＋disabled 額外加深保地板',
    '.act-item .ah{ color:#59452a; }' in src and '.act-item:disabled .ah{ color:#241a10; }' in src)
chk('picker 格標籤＋指南附註加深', '.t70-cell span{ color:#6b5636; }' in src
    and '.guide68-note{ color:#6b5636; }' in src)
chk('壓力綠字加深', '#v-home .home-summary .good, #v-home .nb-live-stress .good{ color:#19684d !important; }' in src)

# --- (D) 故意淡化：原淡化機制冇被誤改 ---
chk('進度 far/missed 行 opacity .62 保留', '.prog71-row.far' in src and 'opacity:.62' in src)
chk('.weak-whisper opacity .45 保留', 'color:#6b4e2e; opacity:.45;' in src)
chk('.act-item:disabled opacity .55 保留', '.act-item:disabled{opacity:.55}' in src)
chk('確定掣 is-locked 樣式冇郁（disabled 判斷項）', 'is-locked' in src)

# --- 紅線 ---
chk('SAVE key 冇郁', 'starVolunteer_map_v19w' in src)
chk('softRev 冇郁', 's107' in src)
chk('產品 ?v= 冇郁', 'v20a10' in src)

print('---')
print(('ALL PASS' if not fails else 'FAILURES: %d' % len(fails)))
sys.exit(1 if fails else 0)
