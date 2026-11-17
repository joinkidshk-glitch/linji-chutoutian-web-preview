# NOTES_V20A270 — 修復首頁底漏出 JS 碎片

## 問題（用戶實機截圖捉到，2026-11-17）

首頁最底見到一行 code：`1; } refreshCopyPacksFromDisk(); })();`。
成因：live `index.html` 檔尾有重複內容。第一個 `</html>` 之後仲有一段 stray 碎片，
瀏覽器將 `</html>` 之後嘅內容當可見文字 render。

## 根源（已核實，唔係 v268 引入）

逐個 main commit 數 `</html>` 出現次數：

- `6e051e7`（v261）×1、 `32d613d`（v163）×1、 `846e952`（v154）×1——乾淨。
- `9b1e6f0`（**v159**，parent `846e952`）×2——**重複由 v159 引入**。
  `git diff 846e952 9b1e6f0 -- index.html` 最後一個 hunk 顯示：喺原本已經完整嘅
  `</script> / </body> / </html>` 之後，追加咗 `+1; +} +refreshCopyPacksFromDisk(); +})(); +</script> +</body> +</html>`。
  即係 v159 工作副本嘅檔尾本身已經重複咗一次（最後 8 行被複製多一份貼喺 `</html>` 之後），
  再經 squash merge 入 main，之後 v139／v262／v263／v264／v158／v162／v265／v266／v267／v268
  全部原樣繼承，無人掂過檔尾，所以一路留到而家。
- 遊戲本身行得（main script 喺第一個 `</script>` 正常閂，首頁正常 render），只係檔尾漏 code，
  屬外觀＋檔案結構缺陷。

## 修復（手術式，只郁檔尾）

工作副本 `linji-work270`（分支 `v20a270`，基底 `e1bf9cc` v269——v269 喺工作期間平行落地，已 rebase 上新 main 再做一次，行號以下列新 main 為準；舊基底 `3ab2e22` v268 嗰份已驗證過，見下）：
刪走第一個 `</html>`（L45372）之後嘅全部 stray 內容，即係原 L45373–L45380 共 8 行：

```
1;
}
refreshCopyPacksFromDisk();
})();

</script>
</body>
</html>
```

保留合法檔尾（第一個出現嗰套）：`return 1;` → `}` → `refreshCopyPacksFromDisk();` →
`})();` → `</script>` → `</body>` → `</html>`。檔案而家 45,372 行，以單一 `</html>\n` 結尾。（舊基底嗰份係 45,299 行，同一段碎片，行號唔同而已。）

修復後核實：
- `</html>` ×1（L45299）、`</body>` ×1、`<script` ×2＝`</script>` ×2（平衡）。
- `refreshCopyPacksFromDisk();` 全檔只出現一次（檔尾合法嗰次）。
- repo 其餘 HTML 檔（`qa108d/fit_test.html`、`qa149/pristine_index.html`、`sample_liao_card.html`、
  `ui-prototype/index.html`）`</html>` 全部 ×1，無同類問題。
- `node --check` 主 script 通過。

## 測試

新 `tests/test_tail270_static.py`，18 項 ALL PASS：
`</html>` 恰好一次且係檔案最後一個非空標記、檔尾零 stray code、
`<script`＝`</script>`＝2、合法檔尾完整（`return 1;`／`refreshCopyPacksFromDisk();`／
`})();`／`</script>`／`</body>`／`</html>`）、`refreshCopyPacksFromDisk();` 只出現一次、
`node --check` 主 script、紅線（SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=v20a10` 不變）。

## Suite

全套 `bash qa131/run_suite.sh`：
- 第一輪（舊基底 `3ab2e22` v268，基線 333／9）：TOTAL PASS 331 FAIL 12——3 項新 FAIL 全部係
  總行數釘行測試（gift185／tang171／tang173），佢哋嘅「零行數漂移」鏈未計 v270 −8；
  已將三檔鏈尾補上「＋v270 −8」，期望總行數 45307→45299，三檔逐個重跑全部 PASS
  （純行數 resync，內容零改動）。第二輪（同一基底，resync 後）：**TOTAL PASS 334 FAIL 9**，
  9 項 FAIL 全部係已知 pre-existing，零回歸。
- **v269 平行落地**（`e1bf9cc`，新基線 334／9）：工作已 rebase 上新 main 再做一次
  （檔尾同一段碎片，行號 45372／45380；三檔鏈期望總行數 45380→45372，鏈尾「＋v269 +73＋v270 −8」）。
- 第三輪（新基底 `e1bf9cc` v269，基線 334／9）：**TOTAL PASS 335 FAIL 9**（335 檔；基線 334＋新檔 1）。
  9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／
  weave43_static／weave44_static／weave49_static／wf5_87／wrap38，零回歸。

## 落地

待填（main HEAD、Pages 核實）。

## 實機驗證

修完之後請用戶自己 refresh 睇下首頁底嗰行 code 仲喺唔喺度（瀏覽器死，parent 唔可以直接實駕）。
