#!/usr/bin/env bash

VERSION=0.1.0
URL=https://ton-dev.heaven-pool.com
WALLET=EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq
MINNER=ton-heaven-pool-miner
OS_VERSION=hiveos
FOLDER_NAME=${MINNER}-${VERSION}
# need to mapping hive os folder definition - so use one more append name -${OS_VERSION}

hiveos_env() {
    apt install -y curl
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
}

build() {
    pushd app/

    rm -rf ../bin ./dist ./build

    mkdir -p ../bin/hiveos/ ../bin/ubuntu18/ ../bin/ubuntu20/
    cp -r ../config/* ../bin/

    poetry run pyinstaller --clean --onefile \
        --add-data "libs/*:libs" --add-data "assets/*:assets" \
        --name miner main.py
    cp ./dist/miner ../bin/hiveos/miner
    cp ./dist/miner ../bin/ubuntu18/miner
    cp ./dist/miner ../bin/ubuntu20/miner

    popd
}

zip () {
    rm -rf ${FOLDER_NAME}*
    mkdir -p ${FOLDER_NAME}
    cp -r ./bin/hiveos ${FOLDER_NAME}-hiveos
    cp -r ./bin/ubuntu18 ${FOLDER_NAME}-ubuntu18
    cp -r ./bin/ubuntu20 ${FOLDER_NAME}-ubuntu20
    pushd ${FOLDER_NAME}-hiveos
    tar -zcv -f ../${FOLDER_NAME}-hiveos.tar.gz *
    popd
    pushd ${FOLDER_NAME}-ubuntu18
    tar -zcv -f ../${FOLDER_NAME}-ubuntu18.tar.gz *
    popd
    pushd ${FOLDER_NAME}-ubuntu20
    tar -zcv -f ../${FOLDER_NAME}-ubuntu20.tar.gz *
    popd
}

pak() {
    build
    zip
}

release(){
    gh release create ${VERSION} \
        --notes "regular release" \
        -t ${FOLDER_NAME}-release \
        ${FOLDER_NAME}-hiveos.tar.gz \
        ${FOLDER_NAME}-ubuntu18.tar.gz \
        ${FOLDER_NAME}-ubuntu20.tar.gz \
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
    poetry run python ./app/main.py --debug --pool ${URL} ${WALLET}
}

"$@"
