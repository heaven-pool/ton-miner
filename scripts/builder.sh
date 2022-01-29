#!/usr/bin/env bash

rm -rf ../bin
mkdir ../bin
cp ../config/* ../bin/

rm -rf ./dist ./build

pyinstaller --clean --onefile --name miner-linux miner.py
cp ./dist/miner-linux ../bin/miner-linux
