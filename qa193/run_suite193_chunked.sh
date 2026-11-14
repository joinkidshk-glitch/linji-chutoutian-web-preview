#!/bin/bash
# v20a193 第二次重驗：分塊全套＋逐項覆驗。
# 背景：間歇性寫入 EPERM 風暴（見 MEMORY.md v146 教訓）——風暴期間測試嘅
# stdout redirect 失敗，測試未跑就計 FAIL（119/166 假失敗），連 OUT 寫入都 EPERM。
# 單次跑全套要 2.5 分鐘無風暴窗口，好難一次過撞正；改為分塊跑：
#   (1) 全部測試分塊（每塊 40 個），每塊跑完即寫結果；
#   (2) 一塊 FAIL >10 就當撞正風暴，瞓 45 秒重跑成塊（最多 3 次），取最少 FAIL 嗰次；
#   (3) 跑完之後，逐個 FAIL 單獨重跑一次——單獨跑一直穩定，覆跑 PASS 嘅就係風暴假失敗，
#       轉做 PASS(retry)；覆跑都 FAIL 嘅先算真 FAIL。
# 用法：bash qa193/run_suite193_chunked.sh <repo-root> <outfile>
ROOT="$1"; OUT="$2"
cd "$ROOT" || exit 1
TMPLOG="$ROOT/qa193/suite_one193.log"
: > "$OUT"
CHUNK=40
i=0; chunk_no=0
FILES=$(ls tests/test_*.js tests/test_*.py)
TOTAL_N=$(echo "$FILES" | wc -l)
echo "total tests: $TOTAL_N"
# 實跑：逐塊做
for f in $FILES; do
  echo "$f" >> "$ROOT/qa193/.chunk_cur.txt"
  i=$((i+1))
  if [ $i -eq $CHUNK ] || [ "$f" = "$(echo "$FILES" | tail -1)" ]; then
    chunk_no=$((chunk_no+1))
    best_fail=999
    attempt=0
    while [ $attempt -lt 3 ]; do
      attempt=$((attempt+1))
      : > "$ROOT/qa193/.chunk_tmp.txt"
      cfail=0
      while read -r t; do
        case "$t" in
          *.js) if node "$t" > "$TMPLOG" 2>&1; then echo "PASS $t" >> "$ROOT/qa193/.chunk_tmp.txt"; else echo "FAIL $t" >> "$ROOT/qa193/.chunk_tmp.txt"; cfail=$((cfail+1)); fi ;;
          *.py) if python3 "$t" > "$TMPLOG" 2>&1; then echo "PASS $t" >> "$ROOT/qa193/.chunk_tmp.txt"; else echo "FAIL $t" >> "$ROOT/qa193/.chunk_tmp.txt"; cfail=$((cfail+1)); fi ;;
        esac
      done < "$ROOT/qa193/.chunk_cur.txt"
      echo "chunk $chunk_no attempt $attempt: FAIL $cfail"
      if [ $cfail -lt $best_fail ]; then cp "$ROOT/qa193/.chunk_tmp.txt" "$ROOT/qa193/.chunk_best.txt"; best_fail=$cfail; fi
      if [ $cfail -le 10 ]; then break; fi
      echo "chunk $chunk_no: FAIL $cfail > 10，疑似風暴，瞓 45 秒重跑"
      sleep 45
    done
    cat "$ROOT/qa193/.chunk_best.txt" >> "$OUT"
    echo "chunk $chunk_no done: best FAIL $best_fail"
    : > "$ROOT/qa193/.chunk_cur.txt"
    i=0
  fi
done
# 逐個 FAIL 單獨覆跑
FAILS=$(grep '^FAIL ' "$OUT" | sed 's/^FAIL //')
if [ -n "$FAILS" ]; then
  echo "solo re-checking $(echo "$FAILS" | wc -l) FAILs"
  for t in $FAILS; do
    case "$t" in
      *.js) runner=node ;;
      *.py) runner=python3 ;;
    esac
    if $runner "$t" > "$TMPLOG" 2>&1; then
      sed -i "s|^FAIL $t\$|PASS(retry) $t|" "$OUT"
      echo "RETRY-PASS $t"
    else
      echo "REAL-FAIL $t"
    fi
  done
fi
P=$(grep -c '^PASS' "$OUT"); F=$(grep -c '^FAIL ' "$OUT")
echo "TOTAL PASS $P FAIL $F" >> "$OUT"
echo "TOTAL PASS $P FAIL $F"
rm -f "$ROOT/qa193/.chunk_cur.txt" "$ROOT/qa193/.chunk_tmp.txt" "$ROOT/qa193/.chunk_best.txt"
