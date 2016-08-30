#!/usr/bin/env bash
#
# copy over the files that are used for other repos to formats that setup wants
pandoc --from=markdown --to=rst --output=README.rst readme.md
cp LICENSE LICENSE.txt
python3 setup.py sdist
#
