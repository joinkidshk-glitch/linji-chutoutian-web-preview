# -*- coding: utf-8 -*-
"""全套測試 in-memory runner（v20a199 沙箱寫入限制下用）：
逐個跑 tests/test_*.js（node）＋test_*.py（python3），output 全捉喺記憶體，
唔寫任何檔（run_suite.sh 嘅 >> 寫檔喺寫入封鎖下會整出假 FAIL）。
用法：python3 qa199/run_suite_mem.py [repo-root]
印每檔 PASS/FAIL 一行＋尾行 TOTAL＋FAIL 清單。exit 1 當有 FAIL。
"""
import glob, os, subprocess, sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(glob.glob(os.path.join(root, "tests", "test_*.js")) +
               glob.glob(os.path.join(root, "tests", "test_*.py")))
passed, failed = [], []
for f in files:
    cmd = (["node", f] if f.endswith(".js") else ["python3", f])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=root)
        ok = (r.returncode == 0)
    except Exception as e:
        ok = False
        r = None
        print("ERROR %s: %r" % (os.path.basename(f), e))
    print(("PASS " if ok else "FAIL ") + os.path.basename(f))
    (passed if ok else failed).append(os.path.basename(f))
print("TOTAL PASS %d FAIL %d" % (len(passed), len(failed)))
if failed:
    print("FAILURES:")
    for n in failed:
        print(" - " + n)
sys.exit(1 if failed else 0)
