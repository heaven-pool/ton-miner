# TON Heaven Pool - Hive OS setting process

## Flightsheet setup

![alt text](https://github.com/heaven-pool/ton-miner/blob/0.1.0/docs/img/flightsheet.png)

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

   ![alt text](https://github.com/heaven-pool/ton-miner/blob/0.1.0/docs/img/flightsheet-configuration.png)
