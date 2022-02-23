$URL = "https:\\ton-dev.heaven-pool.com"
$WALLET = "EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq"
$VERTION = "0.1.0"
$MINNER = "ton-heaven-pool-miner"
$OS_VERSION = "windows"
$FOLDER_NAME = "$MINNER-$VERTION"
$ZIP_NAME = "$FOLDER_NAME-$OS_VERSION"
# need to mapping hive os folder definition - so use one more append name -${OS_VERSION}

function build {
    Push-Location -Path .\app\

    Remove-Item -Recurse -Force -Path ..\bin .\dist .\build

    New-Item -ItemType Directory -Path ..\bin\windows\
    Copy-Item -Recurse -Path .\config -Destination .\bin

    poetry run pyinstaller --clean --onefile `
        --add-data "libs\*:libs" --add-data "assets\*:assets" `
        --name miner main.py
    Copy-Item -Recurse -Path .\dist\miner -Destination ..\bin\windows\
}

function zip {
    Remove-Item -Recurse -Path ".\$FOLDER_NAME" ".\$ZIP_NAME.zip"
    New-Item -ItemType Directory -Path ".\$FOLDER_NAME"

    Copy-Item -Recurse -Path ".\$MINNER" -Destination ".\$FOLDER_NAME"
    Compress-Archive -Path $(Get-ChildItem $FOLDER_NAME | ForEach-Object { $_.FullName }) -DestinationPath "$ZIP_NAME.zip"
}

function pak {
    build
    zip
}

function release {
    gh release create $VERTION -n regular release -t $ZIP_NAME-release $ZIP_NAME.zip -R git@github.com:heaven-pool\ton-miner.git
}

function pak_release {
    pak
    release
}

function py {
    poetry run python .\app\main.py --debug --pool $URL $WALLET
}

function bin {
    .\bin\windows\miner --pools $URL $WALLET
}

& $args[0]
