set -e

TMP_DIR=$(mktemp -d)
cp tauphi.py $TMP_DIR/
cp tauphi_config.json $TMP_DIR/
cp -r $VIRTUAL_ENV/lib/python2.7/site-packages/* $TMP_DIR/
pushd $TMP_DIR
zip -r lambda ./*
popd
cp $TMP_DIR/lambda.zip ./
