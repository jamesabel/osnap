#!/usr/bin/env bash
#
python3 -m venv --clear venv
./venv/bin/pip3 install -U pip
./venv/bin/pip3 install -U setuptools
./venv/bin/pip3 install -U -r requirements.txt
