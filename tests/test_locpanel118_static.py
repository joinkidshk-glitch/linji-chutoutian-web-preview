# v20a118 LOCPANEL118 靜態守門：地點面板重設計（15 地點全量，純呈現層）。
# 覆蓋：① HTML 元素齊（pill／負責人／名牌／名牌列）② 15 地點負責人覆蓋——11 間
#       機構老闆經 GIG_ISSUER_FIGURE_MAP30V2 對照表（唔 hardcode boss 檔路徑）＋何生
#       （S-30 fallback 同一來源）＋霞姐／禮品檔名牌＋醫院 null ③ 唔用何生頂替任何
#       地點負責人 ④ 額度 pill 文案逐字＋扣後數字＋「已到埗」行只喺扣數嗰陣出
#       ⑤ openLoc 接線：render 喺 ux68 之後、closeSheet 收返面板 ⑥ 選項圖標行
#       iconHtml112（v112 手繪圖，唔用 emoji）＋圖檔實存 ⑦ 冇圖地點素底態
#       （gift_shop／hospital 唔喺 LOC_SHEET_BG）⑧ 390px 尺寸上限
#       ⑨ v114 計數邏輯／LOCS 數據零改動（唔加 residentNpc、唔改 SAVE key／softRev／?v=）
# 反證：pristine main（v117）跑呢檔要 FAIL（locpanel118 元素／函數全部唔存在）。
# 用法：python3 tests/test_locpanel118_static.py [path-to-index.html]
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()
lines = src.split("\n")

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

def extract_fn(name):
    i = src.find("function %s(" % name)
    assert i >= 0, "fn not found: " + name
    depth, j = 0, src.find("{", i)
    for k in range(j, len(src)):
        if src[k] == "{": depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0: j = k; break
    return src[i:j + 1]

def extract_const_obj(name):
    i = src.find("const %s" % name)
    assert i >= 0, "const not found: " + name
    j = src.find("{", i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == "{": depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0: j = k; break
    return src[i:j + 1]

# ---------- 0. 紀律 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- 1. HTML 元素 ----------
for eid in ("loc-quota118", "loc-owner118", "loc-owner-img118", "loc-owner-tag118",
            "loc-tagrow118", "loc-tagrow-tag118"):
    ck("HTML 有 #%s" % eid, ('id="%s"' % eid) in src)
ck("pill／負責人／名牌列預設 hidden", all(
    ('id="%s" hidden' % e) in src for e in ("loc-quota118", "loc-owner118", "loc-tagrow118")))
# v20a118 實駕捉到：三個元素嘅 author display 規則（flex）會蓋過 UA [hidden]{display:none}，
# hidden 咗都照顯示——冇 src 嘅負責人圖會出破圖 icon＋殘留 alt 字。必須有 [hidden] 明寫覆寫。
ck("[hidden] 覆寫：三元素 hidden 嗰陣 display:none（唔好俾 author display 蓋過）",
   bool(re.search(r"\.locpanel118-quota\[hidden\][^{]*,\s*#loc-sheet\s+\.locpanel118-owner\[hidden\][^{]*,\s*#loc-sheet\s+\.locpanel118-tagrow\[hidden\]\s*\{\s*display:\s*none\s*!important", src)) or
   all(("[hidden]" in src and "display:none !important" in src and
        (".locpanel118-%s[hidden]" % n) in src)
       for n in ("quota", "owner", "tagrow")))
ck("新元素喺 #loc-sheet 入面",
   src.find('id="loc-quota118"') > src.find('id="loc-sheet"') and
   src.find('id="loc-tagrow118"') < src.find('id="loc-acts"'))
ck("新元素唔喺 #loc-acts 入面（ux68 重排唔會掂佢哋）",
   src.find('id="loc-owner118"') < src.find('id="loc-acts"'))

# ---------- 2. 15 地點負責人覆蓋 ----------
LOCS15 = ["film_lion", "rec_hk", "tvb_longmen", "tvb_kowloon", "tvb_harbour",
          "film_cotton", "film_harbour", "ad_central", "ad_adm", "rec_wanchai",
          "rec_star", "cafe_cha", "agency_ho", "gift_shop", "hospital"]
for lid in LOCS15:
    ck("LOCS 有 %s" % lid, ('id:"%s"' % lid) in src)
owner_src = extract_fn("locpanel118OwnerFor")
map_src = extract_const_obj("GIG_ISSUER_FIGURE_MAP30V2")
ORGS11 = ["film_lion", "rec_hk", "tvb_longmen", "tvb_kowloon", "tvb_harbour",
          "film_cotton", "film_harbour", "ad_central", "ad_adm", "rec_wanchai", "rec_star"]
for lid in ORGS11:
    ck("對照表有 %s" % lid, ('"%s"' % lid) in map_src)
ck("負責人函數讀對照表（GIG_ISSUER_FIGURE_MAP30V2[locId]）",
   "GIG_ISSUER_FIGURE_MAP30V2[locId]" in owner_src)
ck("負責人函數唔 hardcode boss 檔路徑（v116 換入後自動跟新檔）",
   "boss_" not in owner_src and "assets/story/fullbody/boss" not in owner_src)
ck("agency_ho 分支在（何生）", 'locId==="agency_ho"' in owner_src)
ck("agency_ho 經 gigIssuerFigure30v2 fallback 攞圖（S-30 同一來源）",
   "gigIssuerFigure30v2({loc:\"agency_ho\"})" in owner_src)
ck("cafe_cha 分支：霞姐名牌、noFig", 'locId==="cafe_cha"' in owner_src
   and "金龍茶餐廳老闆娘" in owner_src and "noFig:true" in owner_src)
ck("gift_shop 分支：老闆娘名牌、noFig、唔憑空起名",
   'locId==="gift_shop"' in owner_src and "廟街禮品檔" in owner_src
   and "noFig:true" in owner_src)
ck("hospital 分支：return null（唔出人、連名牌都唔出）",
   'locId==="hospital"' in owner_src and "return null" in owner_src)
ck("gigIssuerFigure30v2 呼叫只喺 agency_ho 分支出現（唔用何生頂替其他地點）",
   owner_src.count("gigIssuerFigure30v2(") == 1
   and owner_src.find("gigIssuerFigure30v2(") > owner_src.find('locId==="agency_ho"'))
ck("老闆名牌唔寫「今日喺度」／「駐場」", "今日喺度" not in owner_src and "駐場" not in owner_src)
ck("負責人函數唔讀 residentNpc（cafe_cha 唔加 residentNpc）",
   "residentNpc" not in owner_src)
ck("LOCS cafe_cha 冇 residentNpc",
   "residentNpc" not in lines[[n for n, l in enumerate(lines) if 'id:"cafe_cha"' in l][0]])
ck("全庫 residentNpc 只得 agency_ho 一處（LOCS 定義）",
   sum(1 for l in lines if "residentNpc" in l and 'id:"agency_ho"' in l) == 1)

# ---------- 3. 額度 pill ----------
quota_src = extract_fn("locpanel118QuotaHtml")
ck("pill 有「今日出行：已用 N / 2」", "今日出行：" in quota_src and "已用 " in quota_src)
ck("pill 有「仲可以去 N 個地方」", "仲可以去 " in quota_src and "個地方" in quota_src)
ck("pill 有「✓ 已到埗，扣咗 1 次出行額度」", "✓ 已到埗，扣咗 1 次出行額度" in quota_src)
ck("pill 已到埗行只喺 spent 先出（if(spent)）", "if(spent)" in quota_src)
ck("pill 讀 TRAVEL114_DAILY_CAP（唔 hardcode 2）", "TRAVEL114_DAILY_CAP" in quota_src)
ck("pill 有兩粒點（dots loop＋used 填金）",
   "lp118-dot" in quota_src and '" used"' in quota_src)
render_src = extract_fn("locpanel118Render")
ck("render 讀 travel114State／travel114Remain（扣後數字）",
   "travel114State()" in render_src and "travel114Remain()" in render_src)
ck("render 按 LOC_SHEET_BG 有無切換素底態（locpanel118-nobg）",
   "locpanel118-nobg" in render_src and "LOC_SHEET_BG[L.id]" in render_src)
ck("render 有圖負責人先加 locpanel118-has-owner（文字收窄避開人物）",
   "locpanel118-has-owner" in render_src)
ck("render 圖缺失 onerror 收起負責人（唔出爛圖）",
   "onerror" in render_src and "owner.hidden=true" in render_src)
ck("render 叫 locpanel118AnchorOwner（腳部錨定選項卡頂）",
   "locpanel118AnchorOwner()" in render_src)
ck("render 經 locpanel118ArrivedNow 決定已到埗行（同探訪免費返嚟都出）",
   "locpanel118ArrivedNow(L, !!spent)" in render_src)
arrived_src = extract_fn("locpanel118ArrivedNow")
ck("locpanel118ArrivedNow：spent 即出；否則認探訪記憶（同地點＋同日）",
   "if(spent) return true" in arrived_src and "v.loc===L.id && v.day===day" in arrived_src)
ck("探訪記憶係 transient（let 變量，唔入 S／唔入 save）",
   "let locpanel118SpentVisit = null;" in src and "S.locpanel118SpentVisit" not in src)
anchor_src = extract_fn("locpanel118AnchorOwner")
ck("錨定：腳部收 120px 入選項卡（遮腿，跟樣本；v120-fix1，舊 8px 已改）", "- 120" in anchor_src)
# v20a120 LOCFULL120：全屏幕之後 sheet 高變咗（~844px），人物高度上限 230→400（貼近
# Phase 1 樣本 400px）；下限 120 不變。舊 230 斷言由呢條取代。
ck("錨定：人物高度上限 400、下限 120（唔頂穿 sheet 頂）",
   "Math.min(400" in anchor_src and "Math.max(120" in anchor_src)

# ---------- 4. openLoc／closeSheet 接線 ----------
i = src.find("function openLoc(id, opts){")
assert i >= 0
depth, j = 0, src.find("{", i)
for k in range(j, len(src)):
    if src[k] == "{": depth += 1
    elif src[k] == "}":
        depth -= 1
        if depth == 0: j = k; break
openloc = src[i:j + 1]
ck("openLoc 有 spent118（travel114IsFree 判斷，唔改數）",
   "const spent118 = !(typeof travel114IsFree" in openloc)
ck("openLoc 扣數嗰陣寫探訪記憶（locpanel118SpentVisit）",
   "locpanel118SpentVisit = { loc:id, day:" in openloc)
ck("spent118 喺額度閘之後、enc79 攔截之前定義",
   openloc.find("travel114TrySpend(opts, id)") < openloc.find("const spent118")
   < openloc.find("enc79TryIntercept"))
ck("openLoc 尾段呼叫 locpanel118Render(L, spent118)",
   "locpanel118Render(L, spent118)" in openloc)
ck("render 喺 ux68OrganizeLocSheet 之後（選項砌好先渲染面板）",
   openloc.find("ux68OrganizeLocSheet(L)") < openloc.find("locpanel118Render(L, spent118)"))
ck("render 喺尾段 paintBar 之前（面板齊先畫狀態列）",
   openloc.find("locpanel118Render(L, spent118)") < openloc.rfind("paintBar()"))
ck("closeSheet 收返面板（locpanel118Hide）", "locpanel118Hide()" in src)
hide_src = extract_fn("locpanel118Hide")
ck("locpanel118Hide 清三個 class＋收起三個元素",
   all(x in hide_src for x in ("locpanel118-nobg", "locpanel118-has-owner", "loc-quota118",
                               "loc-owner118", "loc-tagrow118")))

# ---------- 5. 選項圖標 ----------
icon_src = extract_fn("locpanel118ActIcon")
ck("圖標函數經 iconHtml112（v112 手繪圖標）", "iconHtml112(" in icon_src)
ck("圖標函數揀唔到就回空字串（唔用 emoji 頂替）",
   'return ""' in icon_src)
for em, stem in (("🎭", "mask"), ("📰", "news"), ("👥", "people"), ("🎁", "gift"),
                 ("💼", "briefcase"), ("🎬", "clapper"), ("💪", "fitness"),
                 ("😴", "sleep"), ("🏥", "hospital"), ("📖", "book"),
                 ("📻", "radio"), ("📞", "phone")):
    ck("圖標對照 %s → icon_%s.png 實存" % (em, stem),
       em in icon_src and os.path.isfile(os.path.join(ROOT, "assets", "icons", "icon_%s.png" % stem)))
ck("openLoc add() 掣用 locpanel118ActIcon＋act-txt118",
   "locpanel118ActIcon(title, cls)" in openloc and "act-txt118" in openloc)
ck("劇情已完成灰掣都有圖標＋act-txt118", 'locpanel118ActIcon("", "act-story")' in openloc)
ck("CSS 有 .act-ic118＋.act-txt118 規則（v17k first-child 規則失效後補位）",
   ".act-ic118" in src and ".act-txt118" in src)

# ---------- 6. 場景圖 15/15 齊晒（v118 補埋 gift_shop／hospital；素底留做後備機制） ----------
bg_src = extract_const_obj("LOC_SHEET_BG")
ck("LOC_SHEET_BG 有 15 張（v118 補齊 gift_shop／hospital）",
   len(re.findall(r'^\s*(\w+):"assets/story/locs/bg_loc_', bg_src, re.M)) == 15)
for lid in LOCS15:
    ck("LOC_SHEET_BG 有 %s" % lid, ('%s:"assets/story/locs/bg_loc_%s.jpg?v=20a104"' % (lid, lid)) in bg_src)
    ck("場景圖檔實存 assets/story/locs/bg_loc_%s.jpg（720×1280）" % lid,
       os.path.isfile(os.path.join(ROOT, "assets", "story", "locs", "bg_loc_%s.jpg" % lid)))
ck("CSS 有 locpanel118-nobg 素底後備規則（將來有地點冇圖即自動行素底）",
   "locpanel118-nobg" in src)
ck("render 仍按 LOC_SHEET_BG 有無切換素底態（後備機制唔刪）",
   "locpanel118-nobg" in render_src and "LOC_SHEET_BG[L.id]" in render_src)

# ---------- 7. 390px 尺寸上限 ----------
css118 = src[src.find("v20a118 LOCPANEL118"):src.find("v20a118 LOCPANEL118") + 6000]
ck("負責人闊 120px（390px 下唔遮選項）", "width:120px" in css118)
ck("pill 闊上限 252px（唔俾人物遮）", "max-width:252px" in css118)
ck("有負責人嗰陣標題／描述收窄 128px", "calc(100% - 128px)" in css118)
ck("選項卡有實底＋z-index 4（腳部收喺卡後面）",
   "z-index:4" in css118 and "background:#f8f1de" in css118)
ck("負責人 pointer-events:none（唔擋選項點擊）", "pointer-events:none" in css118)

# ---------- 8. v114 計數邏輯／LOCS 零改動 ----------
for fn in ("travel114State", "travel114Remain", "travel114IsFree", "travel114TrySpend"):
    ck("v114 %s 源碼唔含 locpanel118（計數零改動）" % fn,
       "locpanel118" not in extract_fn(fn))
ck("openLoc 額度閘原文不變（travel114TrySpend＋被擋 toast）",
   'travel114TrySpend(opts, id)' in openloc and
   'toast("今日出行額度用完——今日已經去咗 2 個地方，聽日再去。")' in openloc)
ck("openLoc 入面冇寫入 residentNpc（舊註解提及唔計，只禁賦值）",
   "residentNpc:" not in openloc and "residentNpc =" not in openloc)

print("RESULT " + ("FAIL (%d)" % len(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
