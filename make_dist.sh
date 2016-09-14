#!/usr/bin/env bash
#
# copy over the files that are used for other repos to formats that setup wants
pandoc --from=rst --to=markdown --output=readme.md readme.rst
pandoc --from=rst --to=plain --output=readme.txt readme.rst
cp LICENSE LICENSE.txt
python3 setup.py sdist
#
