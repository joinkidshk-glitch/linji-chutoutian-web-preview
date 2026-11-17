#!/usr/bin/env python3
"""v20a268 通用釘行 resync：用 git show HEAD:index.html 做舊版＋工作樹做新版，
difflib SequenceMatcher(autojunk=False) 對位，輸出舊行號 -> 新行號映射。
用法：python3 qa268/resync_generic.py <old1> [old2 ...]（1-based 行號）。
只印映射，唔改任何檔；改測試嗰陣逐個核實內容逐字相同先填。
"""
import subprocess
import sys
from difflib import SequenceMatcher

ROOT = '/home/hatch/workspace/linji-work268'


def main():
    old = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:index.html'],
                         capture_output=True, text=True, check=True).stdout.split('\n')
    new = open(ROOT + '/index.html', encoding='utf-8').read().split('\n')
    print('old %d 行 -> new %d 行，淨 %+d 行' % (len(old), len(new), len(new) - len(old)))
    sm = SequenceMatcher(a=old, b=new, autojunk=False)
    mapping = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                mapping[i1 + k + 1] = j1 + k + 1
    for arg in sys.argv[1:]:
        n = int(arg)
        m = mapping.get(n)
        if m is None:
            print('舊 L%d：唔喺 equal 區（被刪／被改），要人手核實' % n)
        else:
            same = old[n - 1] == new[m - 1]
            print('舊 L%d -> 新 L%d（%+d），內容%s：%s' % (
                n, m, m - n, '逐字相同' if same else '唔同！！', old[n - 1][:80]))


if __name__ == '__main__':
    main()
