# v20a207 resync：index.html 淨 +34 行（C3 .awd-sheet block +12 @~4128／
# #mask.awd-sheet-on cap +5 @~5254／modal() toggle +1 @39675／closeModal +1 @39695／
# awards181DrawBase 重寫 +7 @47453／spotlight207 helper +8 @47805；其餘同行改動 0 行）。
# 釘行按段重算（舊行號，-U0 插入點：4130 +12／5256 +5／39677 +1／39697 +1／47462 +7／47810 +8）：
# <4130 +0／4130–5256 +12／5256–39677 +17／39677–39697 +18／39697–47462 +19／47462–47810 +26／>47810 +34。全部錨點對位核實：pristine 行內容
# 逐字等於新行內容（純漂移，零內容改動）；C5／B3 嗰兩處係刻意改動，另見下文。
import subprocess, sys

pris = subprocess.run(['git', 'show', 'HEAD:index.html'], capture_output=True, text=True,
                      cwd='/home/hatch/workspace/linji-work207').stdout.split('\n')
cur = open('/home/hatch/workspace/linji-work207/index.html', encoding='utf-8').read().split('\n')

# (test, old 1-based, new 1-based)
PINS = [
    # kwan151 (+17)
    ('kwan151', 25721, 25738), ('kwan151', 26062, 26079), ('kwan151', 26065, 26082),
    ('kwan151', 26066, 26083), ('kwan151', 26067, 26084), ('kwan151', 26110, 26127),
    ('kwan151', 26329, 26346), ('kwan151', 27322, 27339), ('kwan151', 27355, 27372), ('kwan151', 31132, 31149),
    ('kwan151', 31140, 31157), ('kwan151', 31141, 31158), ('kwan151', 31183, 31200),
    # tang152 (+17, 0-based 25880/31621/31765 -> 1-based)
    ('tang152', 25881, 25898), ('tang152', 31622, 31639), ('tang152', 31766, 31783),
    # text125 (+17, 0-based 27846/27975/33683 -> 1-based)
    ('text125', 27847, 27864), ('text125', 27976, 27993), ('text125', 33684, 33701),
    # rom176 (+17 / +34)
    ('rom176', 6134, 6151), ('rom176', 31695, 31712), ('rom176', 54334, 54368),
    ('rom176', 54702, 54736), ('rom176', 55841, 55875), ('rom176', 55935, 55969),
    # travel114 COUNT (+17 / +19 / +34)
    ('travel114-COUNT', 32296, 32313), ('travel114-COUNT', 35796, 35813),
    ('travel114-COUNT', 37947, 37964), ('travel114-COUNT', 39117, 39134),
    ('travel114-COUNT', 39549, 39566), ('travel114-COUNT', 39552, 39569),
    ('travel114-COUNT', 39583, 39600), ('travel114-COUNT', 44567, 44586),
    ('travel114-COUNT', 59985, 60019), ('travel114-COUNT', 60163, 60197),
    ('travel114-COUNT', 60309, 60343), ('travel114-COUNT', 60330, 60364),
    # travel114 FREE (+17 / +19 / +34)
    ('travel114-FREE', 24748, 24765), ('travel114-FREE', 30963, 30980),
    ('travel114-FREE', 30964, 30981), ('travel114-FREE', 30976, 30993),
    ('travel114-FREE', 30977, 30994), ('travel114-FREE', 30988, 31005),
    ('travel114-FREE', 30989, 31006), ('travel114-FREE', 31092, 31109),
    ('travel114-FREE', 41510, 41529), ('travel114-FREE', 44224, 44243),
    ('travel114-FREE', 44247, 44266), ('travel114-FREE', 54157, 54191),
    ('travel114-FREE', 54276, 54310), ('travel114-FREE', 54326, 54360),
    ('travel114-FREE', 54549, 54583), ('travel114-FREE', 54588, 54622),
    ('travel114-FREE', 54594, 54628), ('travel114-FREE', 54661, 54695),
    ('travel114-FREE', 54663, 54697), ('travel114-FREE', 54666, 54700),
    ('travel114-FREE', 54693, 54727), ('travel114-FREE', 55804, 55838),
    ('travel114-FREE', 56178, 56212), ('travel114-FREE', 56200, 56234),
    ('travel114-FREE', 56351, 56385), ('travel114-FREE', 57988, 58022),
    ('travel114-FREE', 59753, 59787), ('travel114-FREE', 59871, 59905),
    ('travel114-FREE', 59872, 59906), ('travel114-FREE', 59907, 59941),
    ('travel114-FREE', 59908, 59942), ('travel114-FREE', 59933, 59967),
    ('travel114-FREE', 60780, 60814),
    # travel114 DEF/WRAPPER
    ('travel114-DEF', 55904, 55938), ('travel114-WRAPPER', 45136, 45155),
    # tang173 L4862 anchor (1-based 4942, +12)
    ('tang173', 4942, 4954),
]
bad = 0
for t, old, new in PINS:
    ok = pris[old - 1] == cur[new - 1]
    if not ok:
        bad += 1
        print(f'MISMATCH {t} {old}->{new}:')
        print(f'  pris: {pris[old-1][:100]!r}')
        print(f'  cur : {cur[new-1][:100]!r}')
print(f'PINS {len(PINS)} checked, {bad} mismatch; total lines pris={len(pris)-1} cur={len(cur)-1}')
sys.exit(1 if bad else 0)
