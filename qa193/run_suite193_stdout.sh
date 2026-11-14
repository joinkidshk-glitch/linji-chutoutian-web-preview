#!/bin/bash
# v20a193 第二次重驗：全套跑、結果印 stdout（唔寫 OUT 檔）。
# 背景：間歇性寫入 EPERM 風暴——結果寫入檔案（>> OUT）會成批失敗，連 TOTAL 都寫唔到，
# 但測試本身嘅執行（stdout redirect 去 TMPLOG）多數行得通，stdout 回傳亦穩定。
# 所以結果唔經檔案：每項 PASS/FAIL 印 stdout，尾行 TOTAL；跑完之後逐個 FAIL 單獨覆跑
# （單獨跑一直穩定），覆跑 PASS 嘅係風暴假失敗。
# 用法：bash qa193/run_suite193_stdout.sh <repo-root>
ROOT="$1"
cd "$ROOT" || exit 1
TMPLOG="$ROOT/qa193/suite_one193.log"
pass=0; fail=0
for f in tests/test_*.js; do
  if node "$f" > "$TMPLOG" 2>&1; then echo "PASS $f"; pass=$((pass+1)); else echo "FAIL $f"; fail=$((fail+1)); fi
done
for f in tests/test_*.py; do
  if python3 "$f" > "$TMPLOG" 2>&1; then echo "PASS $f"; pass=$((pass+1)); else echo "FAIL $f"; fail=$((fail+1)); fi
done
echo "TOTAL PASS $pass FAIL $fail"
