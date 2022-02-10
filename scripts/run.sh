#!/usr/bin/env bash

VERTION=0.1.0
URL=https://ton-dev.heaven-pool.com
WALLET=EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq
MINNER=ton-heaven-pool-miner
OS_VERSION=hiveos
FOLDER_NAME=${MINNER}-${VERTION}
ZIP_NAME=${FOLDER_NAME}-${OS_VERSION}
# need to mapping hive os folder definition - so use one more append name -${OS_VERSION}

hiveos_env() {
    apt install -y curl
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
}

build() {
    cd app/

    rm -rf ../bin ./dist ./build
    rm -rf ${FOLDER_NAME} ${ZIP_NAME}

    mkdir -p ../bin/hiveos/assets/ ../bin/ubuntu18/assets/ ../bin/ubuntu20/assets/
    cp -r ../config/* ../bin/

    poetry run pyinstaller --clean --onefile \
        --add-data "libs/*:libs" --add-data "assets/*:assets" \
        --name miner main.py
    cp ./dist/miner ../bin/hiveos/miner
    cp ./dist/miner ../bin/ubuntu18/miner
    cp ./dist/miner ../bin/ubuntu20/miner
}

zip () {
    mkdir -p ${FOLDER_NAME}
    cp -r ./${MINNER}/ ${FOLDER_NAME}
    tar -zcv --exclude='.DS_Store' -f ${ZIP_NAME}.tar.gz ${FOLDER_NAME}
}

pak() {
    build
    zip
}

release(){
    gh release create ${VERTION} \
    --notes "regular release" \
    -t ${ZIP_NAME}-release \
    ${ZIP_NAME}.tar.gz \
    -R git@github.com:heaven-pool/ton-miner.git
}

pak_release (){
    pak
    release
}

bin() {
    ./bin/hiveos/miner --pool ${URL} ${WALLET}
}

py() {
    poetry run python ./app/main.py --pool ${URL} --debug ${WALLET}
}

"$@"