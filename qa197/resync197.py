# v20a197 resync：將舊釘行（pristine 2760680 嘅 1-based 行號）對位到新 index.html。
# 用法：python3 qa197/resync197.py <old1> <old2> ...（唔畀就印全部測試要嘅釘）
# 做法：difflib SequenceMatcher 對位 equal 區直接映射；replace／delete 區內嘅行
# 按內容逐字喺新檔搵（前後 ±200 行窗口），搵唔到就報 UNMAPPED，唔好估。
import difflib, sys
old = open('/tmp/pristine197.html', encoding='utf-8').read().split('\n')
new = open('index.html', encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
# equal 區映射表
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
def map_line(n):
    if n in mapping:
        return mapping[n], 'equal'
    # 內容搜尋：舊行內容喺新檔出現嘅位置（預期漂移 ±200 行窗口優先）
    content = old[n - 1]
    if not content.strip():
        return None, 'blank'
    cands = [i + 1 for i, l in enumerate(new) if l == content]
    if len(cands) == 1:
        return cands[0], 'unique-content'
    if cands:
        return cands, 'multi-content'
    return None, 'UNMAPPED'
pins = [int(x) for x in sys.argv[1:]] or [
    25659, 26000, 26003, 26004, 26005, 26048, 26267, 27213, 27246, 31020, 31028, 31029, 31071,
    6072, 31583, 53416, 53784, 54923, 55017,
    25819, 31502, 31646,  # tang152：lines()[25818] 等係 0-based index → 1-based 行號 +1
    53961, 4862,
]
for n in pins:
    m, how = map_line(n)
    print(f"old {n} -> new {m} [{how}] | {old[n-1].strip()[:80]}")
print(f"total lines: old {len(old)} new {len(new)} net {len(new)-len(old):+d}")
