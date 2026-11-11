#!/bin/bash
# v20a108 全套測試 A/B runner
# 用法：qa108a/run_suite.sh <index.html 路徑> <輸出檔>
# 每個 tests/test_* 檔跑一次，以 exit code 記 PASS/FAIL（同 qa106 做法）。
set -u
IDX="$1"
OUT="$2"
cd "$(dirname "$0")/.." || exit 1
: > "$OUT"
for f in $(ls tests/test_* | sort); do
  case "$f" in
    *.js) timeout 120 node "$f" "$IDX" > /tmp/suite108_one.log 2>&1 ;;
    *.py) timeout 120 python3 "$f" "$IDX" > /tmp/suite108_one.log 2>&1 ;;
    *) echo "SKIP $f" >> "$OUT"; continue ;;
  esac
  if [ $? -eq 0 ]; then echo "PASS $f" >> "$OUT"; else echo "FAIL $f" >> "$OUT"; fi
done
echo "PASS: $(grep -c '^PASS' "$OUT") / FAIL: $(grep -c '^FAIL' "$OUT") / TOTAL: $(wc -l < "$OUT")" >> "$OUT"
