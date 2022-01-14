# /hive/miners/custom/test_build/miner/
# /hive/miners/custom/tonminer_cuda_hiveos_x86_64/assets
# ~/hive/miners/custom/test_build/miner/build_minner/builder.sh

VERTION=0.1.0
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
    pip3 install "numpy<1.15"
    pip3 install "pyopencl<2018.3"
}

run_py() {
    python3 miner.py ${URL} ${WALLET}
    # python3 miner.py https://mining-mission.rich-thinking.com EQB6UzwFx-gZTIZmJmiFWZ7_qTIZ9RwBaR1_2IPtKR4UuAoJ --debug
    # python3 miner.py https://next.ton-pool.com EQB6UzwFx-gZTIZmJmiFWZ7_qTIZ9RwBaR1_2IPtKR4UuAoJ --debug
}

run_bin() {
    ./bin/miner-linux ${URL} ${WALLET}
}

run_build() {
    rm -rf ./bin ./dist ./build
    mkdir ./bin
    cp ./config/* ./bin/

    # git clone https://github.com/TON-Pool/miner.git
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