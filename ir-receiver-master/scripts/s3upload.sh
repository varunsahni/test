#!/usr/bin/env bash

s3upload() {
    mode=$1
    file=$2

    bucket="skybot-ir-binaries"

    sudo aws s3 cp $file "s3://${bucket}/${mode}/build_ir.tar.gz" --acl public-read

}

SAMPLE_COMMAND='`sh s3upload.sh both`'

if [ "$#" -ne 1 ]
then
    echo "Invalid arguments passed"
    echo 'Sample Command :'$SAMPLE_COMMAND
    exit
fi
MODE=$1
DEST_PATH="/Users/Avinash/Documents/opt/work/lotus/"

if [ "$MODE" != 'debug' -a "$MODE" != 'release' -a "$MODE" != 'both' ]
then
    echo "Argument should be from 'debug', 'release', 'both'"
    echo 'Sample Command :'$SAMPLE_COMMAND
    exit
fi

if [ "$MODE" = 'both' -o "$MODE" = 'debug' ]
then
    mod="debug"
    filename="skybot_ir_${mod}.tar.gz"
    path="/tmp/$filename"
    cd $DEST_PATH
    scp -i ~/.ssh/dev_pi root@dev_pi:$path ./
    /usr/bin/sudo mv $filename "build_ir.tar.gz"
    s3upload $mod "${DEST_PATH}build_ir.tar.gz"
    /usr/bin/sudo mv "build_ir.tar.gz" "${filename}.old"
fi

if [ "$MODE" = 'both' -o "$MODE" = 'release' ]
then
    mod="release"
    filename="skybot_ir_${mod}.tar.gz"
    path="/tmp/$filename"
    cd $DEST_PATH
    scp -i ~/.ssh/dev_pi root@dev_pi:$path ./
    /usr/bin/sudo mv $filename "build_ir.tar.gz"
    s3upload $mod "${DEST_PATH}build_ir.tar.gz"
    /usr/bin/sudo mv "build_ir.tar.gz" "${filename}.old"
fi

echo "Files uploaded to s3 successfully"