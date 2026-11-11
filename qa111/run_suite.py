# v20a111 全套測試 A/B runner：逐檔 node / python3，exit 0 = PASS，否則 FAIL。
# 用法：bash qa109b/run_suite.sh [index.html所在目錄] [輸出txt]
import os, subprocess, sys, glob
root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "suite_work111.txt")
tests = sorted(glob.glob(os.path.join(root, "tests", "test_*.js")) + glob.glob(os.path.join(root, "tests", "test_*.py")))
lines, npass, nfail = [], 0, 0
for t in tests:
    name = "tests/" + os.path.basename(t)
    cmd = (["node", t] if t.endswith(".js") else ["python3", t])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=root)
        ok = (r.returncode == 0)
    except Exception as e:
        ok, r = False, None
        lines.append("FAIL %s (runner error %s)" % (name, e))
    if ok:
        npass += 1; lines.append("PASS " + name)
    else:
        nfail += 1
        if not any(name in l for l in lines):
            lines.append("FAIL " + name)
print("PASS %d / FAIL %d / TOTAL %d" % (npass, nfail, npass + nfail))
for l in lines:
    print(l)
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\nTOTAL PASS %d FAIL %d\n" % (npass, nfail))
