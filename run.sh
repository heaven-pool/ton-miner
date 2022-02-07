VERTION=0.2.5
URL=https://ton-dev.heaven-pool.com
WALLET=EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq

MINNER=ton-heaven-pool-miner
OS_VERSION=hiveos
FOLDER_NAME=${MINNER}-${VERTION}
ZIP_NAME=${FOLDER_NAME}-${OS_VERSION}
# need to mapping hive os folder definition - so use one more append name -${OS_VERSION}

hiveos_env() {
    apt install -y python3-pip git
    pip3 install requests pyinstaller
}

run_build() {
    rm -rf ${FOLDER_NAME} ${ZIP_NAME}
}

zip () {
    mkdir -p ${FOLDER_NAME}
    cp -r ./${MINNER}/ ${FOLDER_NAME}
    tar -zcv --exclude='.DS_Store' -f ${ZIP_NAME}.tar.gz ${FOLDER_NAME}
}

run_pak() {
    run_build
    zip
}

qq (){
    run_pak
    release
}

release(){
    gh release create ${VERTION} \
    --notes "regular release" \
    -t ${ZIP_NAME}-release \
    ${ZIP_NAME}.tar.gz \
    -R git@github.com:qwedsazxc78/ton-heaven-pool-miner.git
}

bin() {
    ./bin/hiveos/miner --pool ${URL} ${WALLET}
}

py() {
    poetry run python ./app/main.py --pool ${URL} --debug ${WALLET}
}

"$@"