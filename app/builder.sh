#!/usr/bin/env bash

cd app/

rm -rf ../bin
rm -rf ./dist ./build

mkdir -p ../bin/hiveos/assets/ ../bin/ubuntu18/assets/ ../bin/ubuntu20/assets/
cp -r ../config/* ../bin/


poetry run pyinstaller --clean --onefile --name miner-linux miner.py
cp ./dist/miner-linux ../bin/hiveos/miner-linux
cp ./dist/miner-linux ../bin/ubuntu18/miner-linux
cp ./dist/miner-linux ../bin/ubuntu20/miner-linux
cp ./assets/ubuntu18* ../bin/hiveos/assets
cp ./assets/ubuntu18* ../bin/ubuntu18/assets
cp ./assets/ubuntu20* ../bin/ubuntu20/assets