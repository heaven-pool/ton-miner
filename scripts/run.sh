VERTION=0.1.0
URL=https://mining-mission.rich-thinking.com
WALLET=EQB6UzwFx-gZTIZmJmiFWZ7_qTIZ9RwBaR1_2IPtKR4UuAoJ
MINNER=ton-heaven-pool-miner
OS_VERSION=hiveos
FOLDER_NAME=${MINNER}-${VERTION}
ZIP_NAME=${FOLDER_NAME}-${OS_VERSION}
# need to mapping hive os folder definition - so use one more append name -${OS_VERSION}

run_py() {
    cd src/app
    python3 miner.py ${URL} ${WALLET}
}

run_bin() {
    cd src/app
    ./bin/miner-linux ${URL} ${WALLET}
}

run_build() {
    rm -rf ./bin ./dist ./build
    mkdir ./bin
    cp ./config/* ./bin/

    pyinstaller --clean --onefile --add-data "hash_solver.cl:." --add-data "sha256.cl:." --name miner-linux miner.py
    cp ./dist/miner-linux ./bin/miner-linux
}

zip_bin () {
    mkdir -p ${FOLDER_NAME}
    cp -a ./bin/. ./${FOLDER_NAME}/
    tar -zcv --exclude='.DS_Store' -f ${ZIP_NAME}.tar.gz ${FOLDER_NAME}
}

zip () {
    mkdir -p ${FOLDER_NAME}
    cp -a ./bin/. ./${FOLDER_NAME}/
    cp ./ton-pool.com-miner-0.3.2/miner-linux ./${FOLDER_NAME}/miner-linux
    tar -zcv --exclude='.DS_Store' -f ${ZIP_NAME}.tar.gz ${FOLDER_NAME}
}

run_pak() {
    run_build
    zip
}

copy(){
    scp x9HJxXms2odJnRmFF7YELrjzE0A4xQAD8ph76qFI@shell.hiveos.farm:/hive/miners/custom/test_build/miner/ton-heaven-pool* .
}

"$@"