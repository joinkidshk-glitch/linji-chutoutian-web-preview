#!/bin/bash
cd "$1" || exit 1
: > "$2"
for t in tests/test_*.js; do
  if timeout 120 node "$t" >/dev/null 2>&1; then echo "PASS $t" >> "$2"; else echo "FAIL $t" >> "$2"; fi
done
for t in tests/test_*.py; do
  if timeout 120 python3 "$t" >/dev/null 2>&1; then echo "PASS $t" >> "$2"; else echo "FAIL $t" >> "$2"; fi
done
