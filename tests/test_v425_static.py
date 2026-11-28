# -*- coding: utf-8 -*-
# v425 UI27：篩選明示／金額對齊／試鏡語意與底部層級（只改呈現層，玩法數值不變）
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
fails = []
def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)

# 篩選明示
ok("板頭狀態行 data-board-state425", "data-board-state425" in html)
ok("狀態行出排序與媒介", "排序：" in html and "媒介：全部" in html)
ok("篩選生效出媒介紙籤", "board-media-tag425" in html and "媒介：${filter392}" in html)
ok("解除篩選掣與 handler", "data-clear-filter425" in html and '_boardFilter392 = "all"' in html)
ok("整理掣改名排序與篩選", "排序與篩選 ▾" in html and "整理 · " not in html)
ok("選項 aria-pressed", 'aria-pressed="${_boardSort392===k}"' in html and 'aria-pressed="${filter392===m}"' in html)
ok("返回地點書面語", 'label:"返回地點"' in html and "返去地點" not in html)
ok("細板承接篩選出狀態行", "board-state-small425" in html)

# 金額對齊
ok("範圍用預計片酬範圍", "預計片酬範圍 $" in html)
ok("合約主金額/附註分層", "cn-money-main425" in html and "cn-money-note425" in html)
ok("簽約金主金額與即收分層", "獲聘後即收</span>" in html)
ok("金額寫法無 $ 空格", "$ ${" not in html and '"$ "+' not in html)
ok("預期日薪值不疊約", '<span class="v">$${Math.round(e424)}／日</span>' in html)

# 試鏡語意與底部層級
ok("主掣報名試鏡", 'readyLabel:"報名試鏡"' in html)
ok("印章可報名試鏡", 'readyTag:"可報名試鏡"' in html)
ok("鎖定印章試鏡報名未開放", 'lockedTag:"試鏡報名未開放"' in html)
ok("返回通告欄", 'leaveLabel:"返回通告欄"' in html)
ok("底部成本句常駐", "試鏡需用 1 日，能否獲聘視乎試鏡結果。" in html)
ok("確認標題與主掣", 'title:"報名試鏡"' in html and 'confirmLabel:"確認報名"' in html)
ok("取消/dismiss 重開詳情", "onCancel:()=>openCastingNoticeDetail(g, L)" in html and "onDismiss:()=>openCastingNoticeDetail(g, L)" in html)
ok("ready 人情為次操作", '{label:"用人情免試鏡", role:"g", cls:"btn_favor425"' in html)
ok("鎖定人情升主操作", '{label:"用人情免試鏡", role:"p", cls:"btn_favor425"' in html)
ok("鎖定修正去向降次操作", 'ch158Locked ? "btn_train_second425"' in html)

# 不變量
ok("SAVE key 不變", "starVolunteer_map_v19w" in html)
ok("頒獎贏線 0.875 不變", "AWARDS62_WIN_LINE = 0.875" in html)

print("TOTAL", "FAIL" if fails else "PASS", len(fails))
sys.exit(1 if fails else 0)
