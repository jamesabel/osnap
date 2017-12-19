echo on
REM currently 3.5 is not working for me for the launcher so use 3.4
\Python34\python.exe \Python34\Tools\Scripts\pyvenv.py --clear venv
venv\Scripts\pip3.exe install -U pip
venv\Scripts\pip3.exe install -U setuptools
venv\Scripts\pip3.exe install -U -r requirements.txt
REM install osnap from current source
pushd .
cd ..
launchers\venv\Scripts\python.exe setup.py install
popd
