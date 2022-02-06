VERTION=0.2.5
URL=https://mining-mission.rich-thinking.com
# URL=https://next.ton-pool.com
WALLET=EQB6UzwFx-gZTIZmJmiFWZ7_qTIZ9RwBaR1_2IPtKR4UuAoJ
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
    curl https://newton-blockchain.github.io/global.config.json ./ton-heaven-pool-miner/config/global.config.json
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
    ./bin/hiveos/miner --pool https://ton-dev.heaven-pool.com EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq
}

py() {
    poetry run python ./app/main.py --pool https://ton-dev.heaven-pool.com EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq
}

"$@"