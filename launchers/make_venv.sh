#!/usr/bin/env bash
set -x
/usr/local/bin/pyvenv --clear venv
./venv/bin/pip3 install -U pip
./venv/bin/pip3 install -U setuptools
./venv/bin/pip3 install -U appdirs
./venv/bin/pip3 install -U py2app
# install osnap from current source
pushd .
cd ..
launchers/venv/bin/python3 setup.py install
popd
