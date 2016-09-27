#!/usr/bin/env bash
#
# I'd like to use the venv python, but py2app doesn't seem to work with a venv version
# LOCALPYTHON=./venv/bin/python3
LOCALPYTHON=/usr/local/bin/python3
# and in case we don't already have appdirs, install it (yes I know this messes up the main python ... but it's
# only on osnap developer's machines)
pip3 install -U appdirs
#
rm -r build/
rm -r launchmac/
#
# create the macos app using py2app
$LOCALPYTHON setup.py py2app
#
# put the app into a zip
$LOCALPYTHON dist2zip.py
#
mv -f *.zip ../osnap
