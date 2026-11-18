# qa305/resync305.py — v20a305 resync：index.html 淨 +35 行
#   Q18 五線 warm finale：
#     (a) ngai_finale 對白 ＋9 行 @舊 L36873 後（ngai_patron 塊尾）
#     (b) lok_finale 對白 ＋9 行 @舊 L37537 後（lok_patron 塊尾）
#     (c) chai_finale 對白 ＋10 行 @舊 L37843 後（chai_patron 塊尾）
#     (d) enc79BuildScript 齊尾句分流 ＋4 行 @舊 L40171 後（ngai_repay 冷版塊後）
#     (e) ngai_finale registry ＋1 行 @舊 L41711 後（ngai_patron 行後）
#     (f) lok_finale registry ＋1 行 @舊 L41732 後（lok_patron 行後）
#     (g) chai_finale registry ＋1 行 @舊 L41740 後（chai_patron 行後）
#     (h) chung registry 調序（farewell 由 patron 之前移到之後）淨 0 行
#   漂移規則（舊行號 → 新行號，difflib 對位核實，見下 shift()）：
#     ＜36874 唔郁；36874–37537 ＋9；37538–37843 ＋18；37844–40171 ＋28；
#     40172–41711 ＋32；41712–41732 ＋33；41733–41740 ＋34；≥41741 ＋35。
#   例外：chung 三行調序（舊 41798 farewell→新 41835、舊 41799 patron_cold→新 41833、
#     舊 41800 patron→新 41834），淨 0 行；今次無釘行命中呢三行，CHUNG_MOVE 只作防禦檢查。
#   方法：先對 pristine main（常駐 clone）逐行核實純漂移（內容逐字相同），然後每檔單次掃描
#   dict 查表改 pin（唔用逐對 re.sub，唔會撞值／重複；歷史 resync 註解入面嘅舊行號唔郁）。
#   ok() 名入面嘅 L 號係歷史標籤，唔郁；每檔頂加一行 v305 resync 註解。
#   另：enc83／enc84／sideline278 嘅 EXPECT 節拍表順序係內容斷言，唔係行號 pin——
#   v305 故意改咗順序（三線加 finale、鍾提攜排送別之前），按新順序更新期望值。
# 用法：python3 qa305/resync305.py [--check-only]
#   預設：pristine = ~/workspace/linji-repo/index.html；work = 同目錄上一層 index.html。
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRISTINE = os.environ.get("RESYNC305_PRISTINE", os.path.expanduser("~/workspace/linji-repo/index.html"))
WORK = os.environ.get("RESYNC305_WORK", os.path.join(ROOT, "index.html"))
CHECK_ONLY = "--check-only" in sys.argv


def shift(old):
    if old <= 36873:
        return old
    if old <= 37537:
        return old + 9
    if old <= 37843:
        return old + 18
    if old <= 40171:
        return old + 28
    if old <= 41711:
        return old + 32
    if old <= 41732:
        return old + 33
    if old <= 41740:
        return old + 34
    return old + 35


# chung 調序三行（淨 0 行；今次無釘行命中，防禦檢查用）
CHUNG_MOVE = {41798: 41835, 41799: 41833, 41800: 41834}


def new_line(old):
    return CHUNG_MOVE.get(old, shift(old))


# ---- (1) 行號 pin：(舊行, 錨點字串)；新行由 new_line() 計，逐行核實 pristine 舊行內容 == work 新行內容 ----
LINE_PINS = {
    "tests/test_rom176_static.py": [
        (40638, "/* ===== v20a176 ROM176"),
        (40988, "function rom176ApplyGiftOverrides()"),
        (42288, "function addLocTalkGiftActs(add, L, npcId)"),
        (42444, "rom176TryIntercept(id)"),
    ],
}

# ---- (2) travel114：COUNT／FREE／DEF／WRAPPER——set 內逐行 shift（只改行首數字，註解唔郁）----
TRAVEL114_PINS = [
    ("COUNT", 15363), ("COUNT", 18672), ("COUNT", 20882), ("COUNT", 22085),
    ("COUNT", 22525), ("COUNT", 22528), ("COUNT", 22559), ("COUNT", 28534),
    ("COUNT", 45679), ("COUNT", 45887), ("COUNT", 46045), ("COUNT", 46066),
    ("FREE", 6525), ("FREE", 6526), ("FREE", 8217), ("FREE", 14215), ("FREE", 14216),
    ("FREE", 14228), ("FREE", 14229), ("FREE", 14240), ("FREE", 14241), ("FREE", 14341),
    ("FREE", 24721), ("FREE", 26065), ("FREE", 26066), ("FREE", 26142), ("FREE", 28342),
    ("FREE", 28375), ("FREE", 40436), ("FREE", 40555), ("FREE", 40630), ("FREE", 40830),
    ("FREE", 40874), ("FREE", 40880), ("FREE", 40947), ("FREE", 40949), ("FREE", 40952),
    ("FREE", 40979), ("FREE", 42251), ("FREE", 42298), ("FREE", 42668), ("FREE", 42690),
    ("FREE", 42842), ("FREE", 42847), ("FREE", 43772), ("FREE", 45249), ("FREE", 45556),
    ("FREE", 45557), ("FREE", 45601), ("FREE", 45602), ("FREE", 45627), ("FREE", 46516),
    ("DEF", 42403), ("WRAPPER", 29103),
]

# ---- (3) 字串 pin：(檔, 舊片段, 新片段)——每段喺檔內唯一，先驗證 count == 1 ----
STR_PINS = {
    "tests/test_rom176_static.py": [
        ("line(40638).startswith('/* ===== v20a176 ROM176')", "line(40670).startswith('/* ===== v20a176 ROM176')"),
        ("line(40988).startswith('function rom176ApplyGiftOverrides()')", "line(41020).startswith('function rom176ApplyGiftOverrides()')"),
        ("line(42288).startswith('function addLocTalkGiftActs(add, L, npcId)')", "line(42323).startswith('function addLocTalkGiftActs(add, L, npcId)')"),
        ("'rom176TryIntercept(id)' in line(42444)", "'rom176TryIntercept(id)' in line(42479)"),
    ],
    "tests/test_gift185_static.py": [
        ("總行數 47194（v193 61167", "總行數 47229（v193 61167"),
        ("== 47194)", "== 47229)"),
        ("＋v304 +38）", "＋v304 +38＋v305 +35）"),
    ],
    "tests/test_tang171_static.py": [
        ("總行數 47194（v193 61167", "總行數 47229（v193 61167"),
        ("== 47194)", "== 47229)"),
        ("＋v304 +38）", "＋v304 +38＋v305 +35）"),
        ("openLoc DEF 行 42403（", "openLoc DEF 行 42438（"),
        ("＋v304 +38，travel114", "＋v304 +38＋v305 +35，travel114"),
        (">= 42409", ">= 42444"),
        ("lines[42402]", "lines[42437]"),
    ],
    "tests/test_tang173_static.py": [
        ("總行數 47194（v193 61167", "總行數 47229（v193 61167"),
        ("== 47194)", "== 47229)"),
        ("＋v304 +38）", "＋v304 +38＋v305 +35）"),
        ("openLoc DEF 行 42403（", "openLoc DEF 行 42438（"),
        ("＋v304 +38，travel114", "＋v304 +38＋v305 +35，travel114"),
        (">= 42409", ">= 42444"),
        ("lines[42402]", "lines[42437]"),
    ],
    # EXPECT 節拍表順序（內容斷言，唔係行號 pin；v305 故意改順序，按新順序更新）
    "tests/test_enc83_logic.js": [
        ("['ngai_intel','ngai_help','ngai_repay','ngai_rain','ngai_patron_cold','ngai_patron'], /* v20a278：新 beat ngai_rain（repay 之後）＋冷版 patron（暖版前） */",
         "['ngai_intel','ngai_help','ngai_repay','ngai_rain','ngai_patron_cold','ngai_patron','ngai_finale'], /* v20a278：新 beat ngai_rain（repay 之後）＋冷版 patron（暖版前）；v20a305：暖版收科 ngai_finale（提攜之後） */"),
        ("['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge','lok_patron_cold','lok_patron_cover','lok_patron'], /* v20a278：新 beat lok_cover（help 之後）＋冷版／翻唱收尾（暖版前） */",
         "['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge','lok_patron_cold','lok_patron_cover','lok_patron','lok_finale'], /* v20a278：新 beat lok_cover（help 之後）＋冷版／翻唱收尾（暖版前）；v20a305：暖版收科 lok_finale（提攜之後） */"),
        ("['chai_intel','chai_fear','chai_choice','chai_repay','chai_patron_cold','chai_patron'], /* v20a278：新 beat chai_fear（intel 之後）＋冷版 patron（暖版前） */",
         "['chai_intel','chai_fear','chai_choice','chai_repay','chai_patron_cold','chai_patron','chai_finale'], /* v20a278：新 beat chai_fear（intel 之後）＋冷版 patron（暖版前）；v20a305：暖版收科 chai_finale（提攜之後） */"),
    ],
    "tests/test_enc84_logic.js": [
        ("['chung_review','chung_intel','chung_f_clue','chung_farewell','chung_patron_cold','chung_patron'], /* v20a278：冷版 patron（暖版前） */",
         "['chung_review','chung_intel','chung_f_clue','chung_patron_cold','chung_patron','chung_farewell'], /* v20a278：冷版 patron（暖版前）；v20a305：提攜排送別之前（送別後出沒 P=0，遲到 T4 會永失提攜） */"),
    ],
    "tests/test_sideline278_logic.js": [
        ("ok('(4) 新 beats 順序：駱 cover 排 help 之後、patron 冷版排暖版前', JSON.stringify((ENC79_BEATS.lok_gasing||[]).map(b=>b.id))===JSON.stringify(['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge','lok_patron_cold','lok_patron_cover','lok_patron']));",
         "ok('(4) 新 beats 順序：駱 cover 排 help 之後、patron 冷版排暖版前、finale 排提攜之後', JSON.stringify((ENC79_BEATS.lok_gasing||[]).map(b=>b.id))===JSON.stringify(['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge','lok_patron_cold','lok_patron_cover','lok_patron','lok_finale']));"),
        ("ok('(4) 新 beats 順序：魏 rain 排 repay 之後、patron 冷版排暖版前', JSON.stringify((ENC79_BEATS.ngai_wingnaam||[]).map(b=>b.id))===JSON.stringify(['ngai_intel','ngai_help','ngai_repay','ngai_rain','ngai_patron_cold','ngai_patron']));",
         "ok('(4) 新 beats 順序：魏 rain 排 repay 之後、patron 冷版排暖版前、finale 排提攜之後', JSON.stringify((ENC79_BEATS.ngai_wingnaam||[]).map(b=>b.id))===JSON.stringify(['ngai_intel','ngai_help','ngai_repay','ngai_rain','ngai_patron_cold','ngai_patron','ngai_finale']));"),
        ("ok('(4) 新 beats 順序：齊 fear 排 intel 之後、patron 冷版排暖版前', JSON.stringify((ENC79_BEATS.chai_zanhoi||[]).map(b=>b.id))===JSON.stringify(['chai_intel','chai_fear','chai_choice','chai_repay','chai_patron_cold','chai_patron']));",
         "ok('(4) 新 beats 順序：齊 fear 排 intel 之後、patron 冷版排暖版前、finale 排提攜之後', JSON.stringify((ENC79_BEATS.chai_zanhoi||[]).map(b=>b.id))===JSON.stringify(['chai_intel','chai_fear','chai_choice','chai_repay','chai_patron_cold','chai_patron','chai_finale']));"),
        ("ok('(4) 新 beats 順序：鍾／程冷版 patron 排暖版前', JSON.stringify((ENC79_BEATS.chung_choning||[]).map(b=>b.id))===JSON.stringify(['chung_review','chung_intel','chung_f_clue','chung_farewell','chung_patron_cold','chung_patron']) && JSON.stringify((ENC79_BEATS.ching_tinlok||[]).map(b=>b.id))===JSON.stringify(['ching_e4','ching_rival','ching_after_train','ching_after_polish','ching_patron_cold','ching_patron']));",
         "ok('(4) 新 beats 順序：鍾提攜排送別之前、程冷版 patron 排暖版前', JSON.stringify((ENC79_BEATS.chung_choning||[]).map(b=>b.id))===JSON.stringify(['chung_review','chung_intel','chung_f_clue','chung_patron_cold','chung_patron','chung_farewell']) && JSON.stringify((ENC79_BEATS.ching_tinlok||[]).map(b=>b.id))===JSON.stringify(['ching_e4','ching_rival','ching_after_train','ching_after_polish','ching_patron_cold','ching_patron']));"),
    ],
}

RESYNC_NOTE = {
    "tests/test_rom176_static.py": "# v20a305 resync：index.html 淨 +35 行（Q18：ngai finale 對白 ＋9／lok finale ＋9／chai finale ＋10／齊尾句分流 ＋4／registry 三行 ＋3，插入點全部喺釘行之前）；釘行按段重算（40638→40670、40988→41020 各 ＋32，42288→42323、42444→42479 各 ＋35），內容逐字相同，純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。\n",
    "tests/test_gift185_static.py": "# v20a305 resync：index.html 淨 +35 行；總行數 47194→47229（鏈尾加 ＋v305 +35）。\n",
    "tests/test_tang171_static.py": "# v20a305 resync：index.html 淨 +35 行；總行數 47194→47229、openLoc DEF 42403→42438（鏈尾加 ＋v305 +35；DEF guard 42409→42444、index 42402→42437）。\n",
    "tests/test_tang173_static.py": "# v20a305 resync：index.html 淨 +35 行；總行數 47194→47229、openLoc DEF 42403→42438（鏈尾加 ＋v305 +35；DEF guard 42409→42444、index 42402→42437）。\n",
    "tests/test_travel114_static.py": "# v20a305 resync：index.html 淨 +35 行（Q18，插入點見 qa305/resync305.py）；COUNT／FREE／DEF／WRAPPER 按段重算（＜36874 唔郁、36874–37537 ＋9、37538–37843 ＋18、37844–40171 ＋28、40172–41711 ＋32、41712–41732 ＋33、41733–41740 ＋34、≥41741 ＋35；DEF 42403→42438、WRAPPER 29103 唔郁），內容逐行核實純漂移；openLoc( 呼叫點總數不變。\n",
    "tests/test_enc83_logic.js": "// v20a305 resync：EXPECT_BEATS 三線加暖版收科 beat（ngai_finale／lok_finale／chai_finale，排提攜之後）。\n",
    "tests/test_enc84_logic.js": "// v20a305 resync：EXPECT_BEATS 鍾提攜排送別之前（送別後出沒 P=0，遲到 T4 會永失提攜）。\n",
    "tests/test_sideline278_logic.js": "// v20a305 resync：(4) 節拍表順序——三線加 finale（排提攜之後）、鍾提攜排送別之前。\n",
}


def main():
    with open(PRISTINE, encoding="utf-8") as f:
        pris = f.read().split("\n")
    with open(WORK, encoding="utf-8") as f:
        work = f.read().split("\n")
    print("pristine %s：%d 行；work %s：%d 行；淨 %s%d 行"
          % (PRISTINE, len(pris) - 1, WORK, len(work) - 1,
             "+" if len(work) >= len(pris) else "", len(work) - len(pris)))
    assert len(work) - len(pris) == 35, "淨行數唔係 +35，停低檢查"
    fails = []

    # ---- (1) LINE_PINS：逐行核實 pristine 舊行內容 == work 新行內容 ----
    for fname, pins in LINE_PINS.items():
        for old, anchor in pins:
            new = new_line(old)
            p = pris[old - 1] if 0 < old <= len(pris) else ""
            w = work[new - 1] if 0 < new <= len(work) else ""
            if p != w or anchor not in w:
                fails.append("%s：pin %d→%d 內容唔同／錨點唔見（pristine=%r work=%r）" % (fname, old, new, p[:80], w[:80]))
            else:
                print("  pin ok %s %d→%d（%s）" % (fname, old, new, anchor[:40]))

    # ---- (2) travel114 pins：逐行核實純漂移 ----
    for kind, old in TRAVEL114_PINS:
        new = new_line(old)
        p = pris[old - 1] if 0 < old <= len(pris) else ""
        w = work[new - 1] if 0 < new <= len(work) else ""
        if p != w:
            fails.append("travel114 %s pin %d→%d 內容唔同（pristine=%r work=%r）" % (kind, old, new, p[:80], w[:80]))
    print("  travel114 pins 核實完：%d 處" % len(TRAVEL114_PINS))
    if fails:
        print("FAILURES:\n" + "\n".join(fails))
        sys.exit(1)
    if CHECK_ONLY:
        print("CHECK-ONLY PASS：全部釘行純漂移核實通過，未寫檔")
        return

    # ---- (3) travel114：set 內逐行 shift（單次掃描，只改行首數字）----
    tpath = os.path.join(ROOT, "tests/test_travel114_static.py")
    with open(tpath, encoding="utf-8") as f:
        tlines = f.read().split("\n")
    pmap = {old: new_line(old) for _, old in TRAVEL114_PINS}
    # 只喺 COUNT_LINES／FREE_LINES set 區內改行首數字；DEF／WRAPPER 用整行匹配
    in_set = None
    changed = 0
    for i, ln in enumerate(tlines):
        if ln.startswith("COUNT_LINES = {"):
            in_set = "COUNT"
            continue
        if ln.startswith("FREE_LINES = {"):
            in_set = "FREE"
            continue
        if in_set and ln.strip() == "}":
            in_set = None
            continue
        if in_set:
            m = re.match(r"^(\s*)(\d+)(,.*)$", ln)
            if m:
                old = int(m.group(2))
                if old in pmap:
                    tlines[i] = m.group(1) + str(pmap[old]) + m.group(3)
                    changed += 1
                else:
                    print("  警告：travel114 %s 區有未列入 pmap 嘅行號 %d（%s），唔郁" % (in_set, old, ln.strip()[:60]))
        elif ln.startswith("DEF_LINE = "):
            m = re.match(r"^DEF_LINE = (\d+)(.*)$", ln)
            if m and int(m.group(1)) in pmap:
                tlines[i] = "DEF_LINE = " + str(pmap[int(m.group(1))]) + m.group(2)
                changed += 1
    print("  travel114 改咗 %d 處（預期 %d）" % (changed, len(TRAVEL114_PINS) - 1))  # WRAPPER 29103 唔郁，唔計
    assert changed == len(TRAVEL114_PINS) - 1, "travel114 改動數唔啱"
    with open(tpath, "w", encoding="utf-8") as f:
        f.write("\n".join(tlines))

    # ---- (4) STR_PINS：每段檔內唯一，先驗證 count == 1 再換 ----
    for fname, pairs in STR_PINS.items():
        fpath = os.path.join(ROOT, fname)
        with open(fpath, encoding="utf-8") as f:
            txt = f.read()
        for old, new in pairs:
            c = txt.count(old)
            if c != 1:
                print("FAILURES：%s 旧片段出現 %d 次（預期 1）：%r" % (fname, c, old[:70]))
                sys.exit(1)
            txt = txt.replace(old, new)
            print("  str ok %s：%r → %r" % (fname, old[:50], new[:50]))
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(txt)

    # ---- (5) 每檔頂加 v305 resync 註解 ----
    for fname, note in RESYNC_NOTE.items():
        fpath = os.path.join(ROOT, fname)
        with open(fpath, encoding="utf-8") as f:
            txt = f.read()
        assert "v20a305 resync" not in txt, "%s 已經有 v305 註解，唔重加" % fname
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(note + txt)
        print("  note ok %s" % fname)

    print("RESYNC305 DONE")


if __name__ == "__main__":
    main()
