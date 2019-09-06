# Stock_K_line_and_Volume
股票 K 線圖
====
服務內容
---
輸入股票代號，起始時間和結束時間，即可呈現該時段之 K 線圖和交易量\<br>
未來希望加入像是可以在圖上做個人備註、預測未來股市走向和判斷買賣時機點

開發動機
----
因本人有在小玩股票，又因電腦作業系統關係，無法使用看盤軟體看個股 K 線和交易量，所以著手自己寫程式，以幫助我看過去的價量關係學習股市相關知識

操作方式
----
1. 先選擇要查詢國內股票還是國外股票，國內股票者按1，國外股票者按2（國外股票目前未寫
2. 選擇要查詢的起始時間與結束時間（目前未寫）
3. 輸入股票代號
4. 跑出 html 檔

技術要求
----
1. python 3.7
2. pyecharts
3. pandas

待解決程式問題
----
1. 將使用 function 功能簡化程式
2. 還未寫出如使用者輸入錯誤會跳出錯誤訊息
3. 目前交易量無法隨著收盤價關係變成紅色或綠色