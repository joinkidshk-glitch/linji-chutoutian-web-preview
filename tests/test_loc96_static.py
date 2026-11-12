# -*- coding: utf-8 -*-
"""v20a96 LOC96 地點整理 — 靜態回歸測試
鎖：LOC96 模組在位／新地點＋標籤登記／禮物店正規化接線（pack JSON 冇改、shopId 不變、
舊寄生文案清零）／通告欄掣收返工作地點／醫院三功能接線（治療 gate 三守衛、體檢 tick
接入、探病 hook）／CONSEQ61 本體參數冇郁／SAVE key・softRev・?v= 紀律。
對 v20a95 index 行會 FAIL（反證）。"""
import sys, os, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
fails = []
def ok(cond, msg):
    if not cond: fails.append(msg)

ok("v20a96 LOC96" in src, "LOC96 模組標記在位")
ok("const LOC96_CFG = { treatFee:600, checkupFee:500, checkupDays:28, checkupShield:10 }" in src,
   "LOC96 數字定案（治療 600／體檢 500・28 日・寬容 10）")

# --- 新地點登記 ---
ok('id:"gift_shop", name:"廟街禮品", area:"油麻地", type:"shop"' in src and "x:43, y:35" in src,
   "gift_shop 登記（廟街夜市排檔位 43,35）")
ok('id:"hospital", name:"仁康醫院", area:"薄扶林", type:"med"' in src and "x:43, y:73" in src,
   "hospital 登記（白十字大樓位 43,73）")
ok('<div class="mn68" style="left:28.4%;top:calc(35% - 104px)">廟街禮品</div>' in src, "廟街禮品墨字標籤在位（v20a142 B1：44%→28.4%／-44px→-104px，避開紅白格花紋底）")
ok("海傍禮品" not in src, "舊稱「海傍禮品」已清零（落位跟地圖審計 A11/B5 對位廟街夜市）")
ok('<div class="mn68" style="left:43%;top:calc(73% + 52px)">仁康醫院</div>' in src, "仁康醫院墨字標籤在位")

# --- 禮物店正規化（行覆寫／正規化，唔直改 pack）---
ok('sh.shopId==="shop_street_mk"' in src and 'sh.locId = "gift_shop"' in src and 'sh.name = "廟街禮品檔"' in src,
   "正規化：shop_street_mk 搬去 gift_shop＋改名")
i_assign = src.find("GIFT_SHOPS = giftShops")
i_remap = src.find('if(typeof loc96RemapGiftShop==="function") loc96RemapGiftShop();')
ok(0 <= i_assign < i_remap, "正規化喺 pack 賦值之後即刻行")
shops = json.load(open(os.path.join(ROOT, "content", "shops.json"), encoding="utf-8"))
ok(shops["shops"][0]["locId"] == "rec_hk", "pack shops.json 原封不動（locId 仍係 rec_hk，搬遷靠正規化）")
ok('add("買禮物"' in src, "新店 sheet 出「買禮物」掣")
ok('add("小賣／禮品"' not in src, "舊「小賣／禮品」掣已清走（唱片公司唔再賣禮物）")
for dead in ["附設於香江唱片", "去香江唱片小賣", "旺角唱片旁小賣", "先去旺角小賣看看", 'openLoc("rec_hk"); }catch(_e){ toast("請去旺角香江唱片")']:
    ok(dead not in src, "舊寄生文案清零：" + dead)
ok('openLoc("gift_shop")' in src, "庫存頁「去小賣」掣改指 gift_shop")
ok("廟街禮品檔換了一批貨" in src, "週結補貨旁白改指廟街禮品檔")
ok("油麻地廟街夜市" in src, "禮物店副題用廟街夜市定性（對位地圖審計）")

# --- 通告欄掣收返工作地點 ---
ok("LOC96：通告欄只出喺有通告板嘅工作地點" in src, "通告欄掣 gating 註記在位")
seg = src[src.find("LOC96：通告欄只出喺有通告板嘅工作地點"):][:300]
ok('add("只查看通告欄"' in seg and "L.type" in seg, "通告欄掣跟 type gating（shop/med 唔出空板掣）")

# --- 醫院三功能接線 ---
ok(src.count("hosp96TreatGate(") >= 4, "治療 gate：定義＋三個病日守衛接線齊")
ok("hosp96EffStress(s, stRaw)" in src, "體檢：conseq61DailyTick 接咗有效壓力")
ok("hosp96VisitNote(dayNo)" in src, "探病：conseq61ResolveSickDay 接咗探病 hook")
ok("loc96AddSheetActs(add, L)" in src, "醫院 sheet：openLoc 接咗 loc96AddSheetActs")
ok("hosp96State" in src and "checkupUntil" in src, "體檢狀態 S.hosp96.checkupUntil 在位")

# --- 本體紀律 ---
ok("sickStreak: 2" in src and "sickRelief: 35" in src and "sickCooldownDays: 14" in src,
   "CONSEQ61 病倒本體參數冇郁（streak 2／relief 35／冷卻 14）")
ok("starVolunteer_map_v19w" in src, "SAVE key 冇變")
ok("s107" in src, "softRev 冇變")
ok("v20a10" in src, "產品 ?v= 冇變")

print("FAILURES: " + " | ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
