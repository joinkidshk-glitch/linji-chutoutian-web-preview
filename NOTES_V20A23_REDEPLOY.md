# v20a23 重新部署觸發（無程式變更）

- 背景：PR #119（v20a23，commit 15c0aa3）已合併入 main，但 GitHub Pages 部署 run #243 實際 **failure**（04:21–04:32 UTC，deploy 逾時；與早前 #230/#231 同一故障模式）。當時經 Actions 網頁介面讀到的狀態不準確，誤判為成功。
- 證據：線上實際 serve 的 index.html 為 2,170,054 bytes（v20a22／ecc9891 版本，含 `addLocTalkGiftActs`、無 `locPanelNpcId`／`residentNpc`）；main 的 index.html 為 2,171,602 bytes。即「v20a23 實機覆檢無傾談掣」實為測到舊版部署，非程式問題（全保真 harness 亦證 v20a23 程式在所有可達狀態下均渲染傾談掣）。
- 本 commit 只新增此 NOTES 檔，目的為重新觸發 Pages 部署。部署後須以線上 serve 檔案的 byte 數與標記字串核實，不單靠 Actions 頁面狀態。
