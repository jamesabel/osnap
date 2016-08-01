#!/usr/bin/env bash
#
# use full path to python
# links seem to cause problems with py2app
LOCALPYTHON=/usr/local/Cellar/python3/3.5.2/Frameworks/Python.framework/Versions/3.5/bin/python3.5
#
rm -r build/
rm -r launchmac/
#
# create the macos app using py2app
$LOCALPYTHON setup.py py2app
#
# put the app (as a zip) into a .py file so the user of osnap can get to it easily
$LOCALPYTHON dist2py.py
#
# copy over the launcher to the test app so we can test the launcher out
#rm -r ../test_example/launch.app
#cp -r launchmac/launch.app/ ../test_example/launch.app
