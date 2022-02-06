#!/usr/bin/env bash

cd app/

rm -rf ../bin
rm -rf ./dist ./build

mkdir -p ../bin/hiveos/assets/ ../bin/ubuntu18/assets/ ../bin/ubuntu20/assets/
cp -r ../config/* ../bin/


poetry run pyinstaller --clean --onefile --name miner miner.py
cp ./dist/miner ../bin/hiveos/miner
cp ./dist/miner ../bin/ubuntu18/miner
cp ./dist/miner ../bin/ubuntu20/miner
cp ./assets/ubuntu18* ../bin/hiveos/assets
cp ./assets/ubuntu18* ../bin/ubuntu18/assets
cp ./assets/ubuntu20* ../bin/ubuntu20/assets