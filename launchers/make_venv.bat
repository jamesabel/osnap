echo on
REM currently 3.5 is not working for me for the launcher so use 3.4
REM \Users\james\AppData\Local\Programs\Python\Python35\python.exe \Users\james\AppData\Local\Programs\Python\Python35\Tools\scripts\pyvenv.py --clear venv
\Python34\python.exe \Python34\Tools\Scripts\pyvenv.py --clear venv
venv\Scripts\pip3.exe install -U pip
venv\Scripts\pip3.exe install -U setuptools
venv\Scripts\pip3.exe install -U appdirs
venv\Scripts\pip3.exe install -U py2exe
REM install osnap from current source
pushd .
cd ..
launchers\venv\Scripts\python.exe setup.py install
popd
