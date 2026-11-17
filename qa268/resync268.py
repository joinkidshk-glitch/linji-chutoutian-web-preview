#!/usr/bin/env python3
# v20a268 resync：index.html 淨 −236 行（WF2 Vera 覆寫 −233 @舊 L6897–7129／
#   STORY_MEET_SOFT −1 @舊 L7806／SCENE_OVERRIDE154 −1 @舊 L11240／CONTRA98 R_tang_push2／crisis 行 −1 @舊 L14684／
#   CONTRA98 Vera 段刪 0 行（行內段刪，行數不變）／tang 註解改字 0 行）。
# 釘行按 difflib 映射重寫，內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。
# 用法：python3 qa268/resync268.py
import difflib, subprocess
ROOT = '/home/hatch/workspace/linji-work268'
old = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:index.html'],
                     capture_output=True, text=True).stdout.split('\n')
new = open(f'{ROOT}/index.html', encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}  # old 0-based -> new 0-based
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k] = j1 + k
print(f'old {len(old)} 行 -> new {len(new)} 行，淨 {len(new)-len(old)} 行')

def check(old1, frag, label):
    # old1：舊 1-based 行號
    o = old1 - 1
    n = mapping.get(o)
    assert n is not None, f'{label}：舊 L{old1} 唔喺 equal 區（內容改咗？）'
    assert frag in new[n], f'{label}：新 L{n+1} 內容不符：{new[n][:100]!r}（預期含 {frag[:40]!r}）'
    assert frag in old[o], f'{label}：舊 L{old1} 本身已不符（基底唔啱）'
    print(f'{label}：舊 L{old1} -> 新 L{n+1}（0-based idx {n}），內容逐字相同')
    return n  # 0-based 新索引

print('--- test_tang152_static.py（lines() 0-based 索引） ---')
check(9522, '  const HELD = ["R_tang_push1","R_tang_push2","R_tang_crisis"];', 'HELD')
check(14976, 'function normaliseTangStub152(pack){', 'normaliseTangStub152')
check(15103, 'try{ normaliseTangStub152(rom2);', 'stub 呼叫行')
print('--- test_rom159_static.py（line_has 1-based 行號） ---')
check(25431, 'v20a159 ROM159 Phase 1', 'ROM159 block 頭')
check(8480, 'rom159GainAllowed(k)', 'bumpRel 凍結鉤')
check(26265, 'COMMIT48_NODES.CMT_lan_commit', 'CMT_lan_commit')
check(10950, 'rom159PrepareNode(node)', 'StoryPlay 預備鉤')
check(15050, 'rom159ApplyGiftOverrides()', '載入覆寫呼叫')
check(26180, 'function rom159SoMeetGate', 'rom159SoMeetGate')
check(25459, '查實', '全佳註解行')
