$URL = "https://ton-dev.heaven-pool.com"
$WALLET = "EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq"
$VERTION  = "0.1.0"
$MINNER = "ton-heaven-pool-miner"
$OS_VERSION = "window"
$FOLDER_NAME = "$MINNER-$VERTION"
$ZIP_NAME = "$FOLDER_NAME-$OS_VERSION"

# need to mapping hive os folder definition - so use one more append name -${OS_VERSION}

# function build {
#     cd app/

#     rm -r ../bin ./dist ./build
#     rm -r $FOLDER_NAME $ZIP_NAME

#     mkdir -p ../bin/window/assets/
#     cp -r ../config/* ../bin/

#     poetry run pyinstaller --clean --onefile \
#         --add-data "libs/*:libs" --add-data "assets/*:assets" \
#         --name miner main.py
#     cp ./dist/miner ../bin/window/assets/s
# }

# function zip () {
#     mkdir -p ${FOLDER_NAME}
#     cp -r ./${MINNER}/ ${FOLDER_NAME}
#     tar -zcv --exclude='.DS_Store' -f ${ZIP_NAME}.tar.gz ${FOLDER_NAME}
# }

function pak() {
    build
    zip
}

function release(){
    gh release create $VERTION -n regular release -t $ZIP_NAME-release $ZIP_NAME.zip -R git@github.com:heaven-pool/ton-miner.git
}

function pak_release (){
    pak
    release
}

function py {
    poetry run python ./app/main.py --debug --pool $URL $WALLET
}

function bin {
    ./bin/hiveos/miner --pools $URL $WALLET
}

release