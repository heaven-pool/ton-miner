# TON Pool - Hive OS 設定流程

## 飛行儀表板設定步驟

![alt text](https://github.com/heaven-pool/ton-miner/blob/0.1.0/docs/img/flightsheet.png)

1. COIN: ton
2. 錢包: 選擇你的對應貨幣錢包
3. 礦池: 選擇在礦機中設定
4. 礦機: 客製化設定
   - 安裝網址: 複製後貼上 hiveos 礦機設定
      ```sh
      https://github.com/qwedsazxc78/ton-heaven-pool-miner/releases/download/0.2.4/ton-heaven-pool-miner-0.2.4-hiveos.tar.gz
      ```
   - 礦機名稱: 輸入安裝網址後自動帶入
   - 演算法: 不輸入，留預設值
   - 錢包與模板: 輸入
      ```sh
      %WAL%.%WORKER_NAME%
      ```
   - 礦池網址: 請輸入
      ```sh
      https://ton.rich-thinking.com
      ```
   - 點選保存設定
5. 名稱：ton-heaven-pool

   ![alt text](https://github.com/heaven-pool/ton-miner/blob/0.1.0/docs/img/flightsheet-configuration.png)
