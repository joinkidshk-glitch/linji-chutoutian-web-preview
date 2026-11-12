#!/usr/bin/env python3
# qa147/resync_travel114.py — v20a147 D4 重做校準後 travel114 行號再實量（修正版）。
# 上一版錯將測試釘行（上一手工作副本行號）當 HEAD 行號餵入 HEAD→現版映射。
# 正確做法：將我嘅 4 處改動反向還原，得出上一手工作副本，再同現版 difflib 對位；
# 每個釘行由 equal-block 映射去新行號，逐行驗內容逐字相同，唔係得個常數偏移。
# 用法：python3 qa147/resync_travel114.py（在 ~/workspace/linji-work147 執行）
import difflib
import re
import sys

with open("index.html", encoding="utf-8") as f:
    new_src = f.read()

# (new_text, old_text) — 我嘅 4 處改動（D4 重做校準），逐字照抄 muse.edit 嗰陣嘅字串。
EDITS = [
    ("     評審口味只 ±0.05（AWARDS62_TASTE），唔主導結果；到贏線 0.875 就贏。 */",
     "     評審口味只 ±0.05（AWARDS62_TASTE），唔主導結果；到贏線 0.90 就贏。 */"),
    ("""const AWARDS62_WIN_LINE = 0.875; /* v20a147 D4 重做校準：0.90→0.875——校準見 qa147/CALIBRATION_D4.md §5。
   0.90 嗰版只對理論檔有效（擔正檔 32%），觀測到嘅真實全弧最佳 base 0.748 喺 0.82／0.90 之下
   贏率都係 0%，唔符合「等正常實玩贏得到先至算驗到」。重做同期修咗計分樽頸（窗口 30→90＋
   計分年份改用殺青日曆年），觀測最佳 base 0.694→0.879；新線下觀測期望贏場 0.54／9 場、
   頂級檔 57%、Y1 強 0%。可行窗好窄（頂級 ≤60% 要 L≥0.872；期望 ≥0.5 要 L≤0.879），0.875 係中點。 */""",
     """const AWARDS62_WIN_LINE = 0.90; /* v20a147 D4：0.82→0.90——校準見 qa147/CALIBRATION_D4.md。
   公式天花板（無 tag）係 0.90；擔正級檔案 base 0.882 喺新線下贏率 32%（目標 25–40%），
   Y1 強／Y2 中／專攻／全弧真實最佳全部 0%，第一年贏唔到。權重唔郁。 */"""),
    ("""          if(S.wrapHistory.length>90) S.wrapHistory.length=90; /* v20a147 D4 重做校準：上限 30→90——全弧 arcN 單年最多 79 部（1991 年）、任何 365 日窗口最多 79 部，30 條連一年都冚唔晒，day 609 三部 0.74 代表作俾擠出窗口（base 0.694，見 qa147/CALIBRATION_D4.md §5）；90 條冚得晒一年份量兼有裕。作品牆／ladder95／人情／對手等讀取逐個核過：只會更準，詳見 CALIBRATION_D4.md §5 讀取審計。舊檔已截斷嘅歷史救唔返，新殺青先累積到 90。 */""",
     """          if(S.wrapHistory.length>30) S.wrapHistory.length=30; /* v20a65 FIX65-3：上限 20→30——高產多元玩家嘅舊作品俾其他媒介新作擠出窗口，頒獎每桶深度被斬（BUG-3 另一半機制）；作品牆同受惠。舊檔唔使遷移，上限只喺新殺青嗰刻截斷。 */"""),
    ("""/* v20a147 D4 重做校準：計分年份改用殺青日曆年（wrappedDay）——同 countYearMediumWraps
   （入圍計數）同一個口徑，兩邊終於一致。舊版用 h.year（gig pack 年份＋2 remap）：
   全弧 138 部入面 35 部 pack 年 ≠ 殺青日曆年（全部係 soft-bridge 臨記工，pack 1990 但
   1991 年先殺青），佢哋計數嗰陣入 1991 桶、計分嗰陣入 1990 桶（嗰年典禮早已完結）——
   計分桶永遠見唔到佢哋，day 609「計數 6、計分桶 2」就係咁嚟。改口徑後呢 35 部歸返
   殺青嗰年（窗口 30 下 day 609 base 0.694→0.778 獨立證據；窗口 90 下佢哋唔入頭四名，
   base 唔變）。冇 wrappedDay 嘅舊式記錄（例如遷移補入）照舊跌返 h.year／id 年份。 */
function awards62YearOf(h){
  try{ if(h && h.wrappedDay != null){ const y = awardsYearFromDay(h.wrappedDay); if(y) return y; } }catch(_e){}
  if(h && h.year) return Number(h.year) || 0;
  const m = String((h && h.gigId) || "").match(/(\\d{4})/);
  if(m){ const y66 = Number(m[1]); return (y66>=1988 && y66<=1992) ? y66+2 : y66; } /* v20a66：id 內嵌年份係舊曆編碼 */
  return 0;
}""",
     """function awards62YearOf(h){
  if(h && h.year) return Number(h.year) || 0;
  const m = String((h && h.gigId) || "").match(/(\\d{4})/);
  if(m){ const y66 = Number(m[1]); return (y66>=1988 && y66<=1992) ? y66+2 : y66; } /* v20a66：id 內嵌年份係舊曆編碼 */
  try{ if(h && h.wrappedDay != null) return awardsYearFromDay(h.wrappedDay) || 0; }catch(_e){}
  return 0;
}"""),
]
prev_src = new_src
for new_text, old_text in EDITS:
    n = prev_src.count(new_text)
    assert n == 1, "reverse edit not unique: %d matches for %.60s" % (n, new_text)
    prev_src = prev_src.replace(new_text, old_text)

old_lines = prev_src.split("\n")
new_lines = new_src.split("\n")
print("prev-hand lines: %d  new lines: %d  net: %+d" % (len(old_lines), len(new_lines), len(new_lines) - len(old_lines)))

sm = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
    else:
        print("CHANGE %s prev %d-%d -> new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))

test_src = open("tests/test_travel114_static.py", encoding="utf-8").read()


def parse_set(name):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", test_src, re.S)
    return sorted(int(x) for x in re.findall(r"\d+", m.group(1)))


count_old = parse_set("COUNT_LINES")
free_old = parse_set("FREE_LINES")
def_old = int(re.search(r"DEF_LINE = (\d+)", test_src).group(1))
wrap_old = int(re.search(r"WRAPPER_LINE = (\d+)", test_src).group(1))

fail = 0
for label, pins in (("COUNT", count_old), ("FREE", free_old), ("DEF", [def_old]), ("WRAP", [wrap_old])):
    for ln in pins:
        nl = mapping.get(ln)
        ok = nl is not None and old_lines[ln - 1] == new_lines[nl - 1]
        if not ok:
            fail += 1
        print("%s %d -> %s %s" % (label, ln, nl, "OK" if ok else "MISMATCH"))

# 全部 openLoc( 呼叫點序列逐字一致（44 處）
def calls(lines):
    return [(i + 1, l.strip()) for i, l in enumerate(lines) if "openLoc(" in l]


oc, nc = calls(old_lines), calls(new_lines)
print("openLoc call sites: prev %d new %d" % (len(oc), len(nc)))
seq_ok = len(oc) == len(nc) and all(a[1] == b[1] for a, b in zip(oc, nc))
print("call-site content sequence identical:", seq_ok)
if not seq_ok:
    fail += 1
print("RESULT " + ("FAIL (%d)" % fail if fail else "PASS"))
sys.exit(1 if fail else 0)
