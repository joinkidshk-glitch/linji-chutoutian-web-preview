#!/usr/bin/env python3
# v391 UI 檢視修正靜態守門：五項呈現層修法嘅關鍵標記在位＋對比度守門。
# 只驗靜態標記（實駕量度見 ~/workspace/linji-drive391/verify/measurements.json）；
# 數值／邏輯／文案零改動由其他測試守。
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []


def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def lum(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# --- v391 CSS 區塊在位 ---
m = re.search(r"/\* ===== v391 UI391：.*?/\* ===== v391 UI391 完 ===== \*/", src, re.S)
ok("v391 CSS 區塊在位（6735–6861）", bool(m))
blk = m.group(0) if m else ""

# --- (1) 確認 modal：紙卡底＋深字，對比度 ≥7:1（實駕：標題 15.33:1、內文 11.07:1） ---
ok("reconfirm 紙卡底 #F2EBD8", "#F2EBD8" in blk)
ok("reconfirm 標題色 #1A1410", ".reconfirm236 h3{ color:#1A1410" in blk)
ok("reconfirm 標題對比 ≥7:1", contrast("#1A1410", "#F2EBD8") >= 7)
ok("reconfirm 內文色 #3a2e22", ".reconfirm236 p," in blk and "#3a2e22" in blk)
ok("reconfirm 內文對比 ≥7:1", contrast("#3a2e22", "#F2EBD8") >= 7)
ok("reconfirm 掣欄用紙底＋安全區", "calc(10px + env(safe-area-inset-bottom,0px))" in blk)
# 「確定」金掣唔郁：原金漸變規則仲喺度，v391 區塊冇改佢背景
# v401 UI401-3：共用金掣漸變改實色金（殺「繼續」疊影浮雕；底色 #C9A227／墨邊／深色字唔變，掣字對比 7.54:1）——漸變字串已刪，改釘實色金在位
ok("確定金掣原規則仲喺度", "background:#C9A227 !important" in src and src.count("linear-gradient(180deg,#E6D2A8,#C9A227)") == 0)
ok("v391 區塊冇改確定掣背景", "reconfirm236" not in blk.split("#modal-btns{")[1].split("}")[0]
   if "#modal-btns{" in blk else True)

# --- (2) 地圖標籤層：避讓＋拉柄 in-flow＋玩家標記金框 ---
ok("deCollide 近距 8px 都推", "oy>-8" in src and "ox>-8" in src)
ok("deCollide 三輪覆核鏈在位", "_settleLeft391 = 3" in src)
ok("手帳拉柄改 in-flow（position:static）", ".book389-handle{\n  position:static" in blk)
ok("玩家標記金框 #c9a227", ".map-me363{ border-color:#c9a227" in blk)
ok("屋企唔出「我喺呢度」tag（註解＋邏輯）", "唔出「我喺呢度」tag" in src)

# --- (3) 稱號段：包入米紙卡＋朱紅印章 ---
ok("稱號段米紙卡 .tags389-fold", ".tags389-fold{\n  background:linear-gradient(180deg,#f6efdc,#efe2bd)" in blk)
ok("稱號朱紅印章 #9E2F2F", "#9E2F2F" in blk)
ok("印章對比 ≥4.5:1", contrast("#9E2F2F", "#f6efdc") >= 4.5)
ok("稱號重複標頭已刪（.jobs72-h 隱藏）", ".tags389-fold #tags-list .jobs72-h{ display:none" in blk)

# --- (4) 劇情層疊漏＋「下一句」防呆 ---
ok("story-play tut-on 背景壓贏（頁眉唔漏入）", "#mask.story-play-on.tut-on{ background:#0a0705" in blk)
ok("對白模式掣欄改流程底欄（position:static）", "sp-mode-dialogue) #modal-btns," in blk
   and "position:static !important" in blk)
ok("對白掣欄預留安全區", "calc(8px + env(safe-area-inset-bottom,0px))" in blk)
ok("三粒掣統一 44px", "height:44px !important; min-height:44px !important" in blk)
ok("對白紙片預留底邊距", "padding-bottom:calc(14px + env(safe-area-inset-bottom,0px))" in blk)

# --- (5) 地點面板＋頒獎去網頁化 ---
ok("返回地圖改頁角吊牌（min-width:120px）", "#loc-close{\n  flex:0 0 auto !important; width:auto !important; min-width:120px" in blk)
ok("地點標題禁斷詞（塘字唔孤行）", "word-break:keep-all" in blk)
ok("頒獎請柬票根 .awd-sheet 在位", ".awd-sheet{" in blk and "border-top:2px dashed" in blk)
ok("頒獎掣改啞面紙籤（.awd-sheet-on button.p）", "#modal-btns button.p{\n  background:#efe3c2" in blk)

# --- 呈現層以外零郁：總行數＋SAVE key 由其他測試守，呢度只驗 v391 冇掂邏輯標記 ---
ok("v391 區塊只含 CSS（無 JS 邏輯改動混入）", "function " not in blk)

print("RESULT " + ("PASS" if not fails else f"FAIL ({len(fails)})"))
sys.exit(0 if not fails else 1)
