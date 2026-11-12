#!/bin/bash
# 全套測試：$1=repo 目錄，$2=輸出檔（絕對路徑）。JS 用 node，PY 用 python3，各 120s timeout。
cd "$1" || exit 1
: > "$2"
for t in tests/test_*.js; do
  if timeout 120 node "$t" >/dev/null 2>&1; then echo "PASS $t" >> "$2"; else echo "FAIL $t" >> "$2"; fi
done
for t in tests/test_*.py; do
  if timeout 120 python3 "$t" >/dev/null 2>&1; then echo "PASS $t" >> "$2"; else echo "FAIL $t" >> "$2"; fi
done
echo "TOTAL PASS $(grep -c '^PASS' "$2") FAIL $(grep -c '^FAIL' "$2")" >> "$2"
