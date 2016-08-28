#!/usr/bin/env bash
#
# copy over the files that are used for other repos to formats that setup wants
cp readme.md readme
python3 setup.py sdist