#!/usr/bin/env bash
set -x
/usr/local/bin/pyvenv --clear venv
./venv/bin/pip3 install -U pip
./venv/bin/pip3 install -U setuptools
./venv/bin/pip3 install -U -r requirements.txt
# install osnap
pushd .
cd ..
rm -r build
./test_example/venv/bin/python3 setup.py install
popd
