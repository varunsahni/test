#!/usr/bin/env bash

run_pyinstaller() {
    mode=$1
    module=$2
    SRC="/opt/ir-sources/${mode}/${module}"
    /usr/bin/sudo rm -Rf $SRC
    /usr/bin/sudo mkdir -p $SRC
    /usr/bin/sudo cp -Rf $DIR/* $SRC
    /usr/bin/sudo rm "${SRC}/config/global_config.py"
    /usr/bin/sudo cp "${SRC}/config/${mode}/global_config.py" "${SRC}/config/"
    /usr/bin/sudo rm -Rf "${SRC}/config/debug" "${SRC}/config/release"

    /usr/bin/sudo rm -Rf $BIN_PATH/$mode/$module $BIN_PATH/$mode/$module.spec
    /usr/bin/sudo rm -Rf $DIST_PATH/$mode/$module
    /usr/bin/sudo rm -Rf $BIN_PATH/$mode/$module.log
    /usr/bin/sudo mkdir -p $BIN_PATH/$mode
    /usr/bin/sudo touch $BIN_PATH/$mode/$module.log
    echo "/usr/bin/sudo pyinstaller --name=$module --console $SRC/$module.py -y --paths=$SRC --key=$KEY --clean --onefile --distpath $DIST_PATH/$mode/bin/ --workpath $BIN_PATH/$mode/$module --specpath $BIN_PATH/$mode/$module >> $BIN_PATH/$mode/$module.log 2>&1 &"
    /usr/bin/sudo pyinstaller --name=$module --console $SRC/$module.py -y --paths=$SRC --key=$KEY --clean --onefile --distpath $DIST_PATH/$mode/bin/ --workpath $BIN_PATH/$mode/$module --specpath $BIN_PATH/$mode/$module >> $BIN_PATH/$mode/$module.log 2>&1 &
}

SAMPLE_COMMAND='`sh create-binaries.sh debug all`'

if [ "$#" -ne 2 ]
then
    echo "Invalid arguments passed"
    echo 'Sample Command :'$SAMPLE_COMMAND
    exit
fi

MODE=$1
MODULE=$2

DIST_PATH="/opt/ir-binaries"
KEY='alfaonepython'
/usr/bin/sudo mkdir -p /opt/ir-sources

if [ "$MODE" != 'debug' -a "$MODE" != 'release' -a "$MODE" != 'both' ]
then
    echo "Argument should be from 'debug', 'release', 'both"
    echo 'Sample Command :'$SAMPLE_COMMAND
    exit
fi

/usr/bin/sudo mkdir -p "${DIST_PATH}/debug/bin"
/usr/bin/sudo mkdir -p "${DIST_PATH}/release/bin"

DIR="/opt/ir-receiver-src"
BIN_PATH=/tmp

/usr/bin/sudo rm -Rf $BIN_PATH/debug $BIN_PATH/release
/usr/bin/sudo mkdir -p $BIN_PATH/ir-debug
/usr/bin/sudo mkdir -p $BIN_PATH/ir-release

if [ "$MODULE" = 'all' -o "$MODULE" = 'listenLIRC' ]
then
    module="listenLIRC"
    if [ "$MODE" = 'both' -o "$MODE" = 'debug' ]
    then
        mode="debug"
        run_pyinstaller $mode $module
    fi

    if [ "$MODE" = 'both' -o "$MODE" = 'release' ]
    then
        mode="release"
        run_pyinstaller $mode $module
    fi

fi

if [ "$OSTYPE" = "darwin"* ]
then
    /usr/bin/sudo chown -Rf Avinash:staff $DIST_PATH/
fi

/bin/sleep 2
pscount=$(/bin/ps aux|/bin/grep /usr/local/bin/pyinstaller | /usr/bin/wc -l)
pscount=$((pscount-1))
while [ $pscount -gt 0 ]
do
        /bin/sleep 1
        pscount=$(/bin/ps aux|/bin/grep /usr/local/bin/pyinstaller | /usr/bin/wc -l)
        pscount=$((pscount-1))
        echo -ne "\e[0K\rPyinstaller running processes : $pscount"
done

echo ""
echo "Binaries are created successfully. Now archiving binaries."

if [ "$MODE" = 'both' -o "$MODE" = 'debug' ]
then
    mode="debug"
    cd "${DIST_PATH}/${mode}/"
    /usr/bin/sudo rm -Rf *.tar.gz
    /usr/bin/sudo cp -Rf $DIST_PATH/$mode/bin/* /opt/bin
    /usr/bin/sudo tar -zcf "skybot_ir_${mode}.tar.gz" . >>/dev/null 2>&1
    /usr/bin/sudo mv "skybot_ir_${mode}.tar.gz" /tmp
    echo "/tmp/skybot_ir_${mode}.tar.gz file created successfully"
fi

if [ "$MODE" = 'both' -o "$MODE" = 'release' ]
then
    mode="release"
    cd "${DIST_PATH}/${mode}/"
    /usr/bin/sudo rm -Rf *.tar.gz
    /usr/bin/sudo tar -zcf "skybot_ir_${mode}.tar.gz" . >>/dev/null 2>&1
    /usr/bin/sudo mv "skybot_ir_${mode}.tar.gz" /tmp
    echo "/tmp/skybot_ir_${mode}.tar.gz file created successfully"
fi