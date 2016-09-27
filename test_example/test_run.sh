#!/usr/bin/env bash
set -x
rm -rf .eggs build dist logs venv || { echo 'could not rm -rf : re-run with sudo' ; exit 1;  }
set +x
./make_venv.sh
./install_osnap.sh
./make_osnapy.sh
./make_installer.sh
