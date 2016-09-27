#!/usr/bin/env bash
set -x
/usr/local/bin/pyvenv --clear venv
./venv/bin/pip3 install requests
./venv/bin/pip3 install jinja2
# install osnap
pushd .
cd ..
rm -r build
./test_example/venv/bin/python3 setup.py install
popd
