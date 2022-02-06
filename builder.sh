#!/usr/bin/env bash

cd app/

rm -rf ../bin
rm -rf ./dist ./build

mkdir -p ../bin/hiveos/assets/ ../bin/ubuntu18/assets/ ../bin/ubuntu20/assets/
cp -r ../config/* ../bin/


poetry run pyinstaller --onefile \
    --add-data "libs/*:libs" --add-data "assets/*:assets" \
    --name miner main.py
cp ./dist/miner ../bin/hiveos/miner
cp ./dist/miner ../bin/ubuntu18/miner
cp ./dist/miner ../bin/ubuntu20/miner
# cp ./assets/ubuntu18* ../bin/hiveos/assets
# cp ./assets/ubuntu18* ../bin/ubuntu18/assets
# cp ./assets/ubuntu20* ../bin/ubuntu20/assets