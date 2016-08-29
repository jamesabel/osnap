#!/usr/bin/env bash
#
# point this to your python 3
# we had multiples on our system so we had to be very specific
if [ -z "$MYPYTHONHOME" ]; then
    export MYPYTHONHOME=/usr/local/Cellar/python3/3.5.2_1
fi
echo ${MYPYTHONHOME}
${MYPYTHONHOME}/bin/pyvenv --clear venv
./venv/bin/pip3 install sphinx
