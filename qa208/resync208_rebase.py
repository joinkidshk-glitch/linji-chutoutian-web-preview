import difflib, sys
old = open('/tmp/pristine208b.html', encoding='utf-8').read().split('\n')
new = open('/home/hatch/workspace/linji-work208/index.html', encoding='utf-8').read().split('\n')
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new)-len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2-i1):
            mapping[i1+k+1] = j1+k+1
print('non-equal opcodes:', [(t, i2-i1, j2-j1) for t,i1,i2,j1,j2 in sm.get_opcodes() if t!='equal'])
import json
json.dump(mapping, open('/tmp/map208.json','w'))
# lookup helper
def look(nums):
    for n in nums:
        m = mapping.get(n)
        same = m is not None and old[n-1]==new[m-1]
        print(f'  {n} -> {m} {"SAME" if same else "DIFF!!"}  {old[n-1].strip()[:60]}')
print('rom176 pins (HEAD base):'); look([6151,31712,54393,54761,55900,55994])
print('openLoc DEF:'); look([55963])
print('travel114 WRAPPER:'); look([45180])
print('travel114 COUNT (HEAD base):'); look([32313,35813,37964,39134,39566,39569,39600,44611,60044,60222,60368,60389])
print('travel114 FREE (HEAD base):'); look([24765,30980,30981,30993,30994,31005,31006,31109,41554,44268,44291,54216,54335,54385,54608,54647,54653,54720,54722,54725,54752,55863,56237,56259,56410,58047,59812,59930,59931,59966,59967,59992,60839])
