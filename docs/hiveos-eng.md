# TON Heaven Pool - Hive OS setting process

## 飛行儀表板設定步驟

![alt text](https://github.com/qwedsazxc78/ton-heaven-pool-miner/blob/main/image/%E9%A3%9B%E8%A1%8C%E5%84%80%E8%A1%A8%E6%9D%BF%E8%A8%AD%E5%AE%9A.png?raw=true)

1. COIN: TON
2. Wallet: Select your toncoin wallet
3. Pool: Select Configure in miner
4. Miner: Setup Miner Config
   - Installation URL: copy and paste below url
      ```sh
      https://github.com/qwedsazxc78/ton-heaven-pool-miner/releases/download/0.2.4/ton-heaven-pool-miner-0.2.4-hiveos.tar.gz
      ```
   - Miner Name: auto input after typing Installation URL
   - Hash algorithm: keep default value
   - Wallet and worker template: input
      ```sh
      %WAL%.%WORKER_NAME%
      ```
   - Pool URL: input
      ```sh
      https://ton.heaven-pool.com
      ```
   - Apply Changes
5. Name：ton-heaven-pool

   ![alt text](https://github.com/qwedsazxc78/ton-heaven-pool-miner/blob/main/image/%E9%A3%9B%E8%A1%8C%E5%84%80%E8%A1%A8%E6%9D%BF%E8%A8%AD%E5%AE%9A-%E5%AE%A2%E8%A3%BD%E5%8C%96%E8%A8%AD%E5%AE%9A.png?raw=true)

## Notice

1. 安裝版本的版號**一定要一樣**，否則會安裝失敗，或是跑起來有問題
   https://github.com/qwedsazxc78/ton-heaven-pool-miner/releases/download/0.2.4/ton-heaven-pool-miner-0.2.4-hiveos.tar.gz
2. 網址尾碼不可以有 "/" ，否則跑起來會有問題。
   例如下面例子，最後有多斜線會導致礦機辨認失誤
   https://ton.rich-thinking.com/
3. 最新礦機下載網址： https://github.com/qwedsazxc78/ton-heaven-pool-miner/releases?page=1
