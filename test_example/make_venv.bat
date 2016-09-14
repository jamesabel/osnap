REM point this to your python 3
set MYPYTHONHOME=c:\Users\james\AppData\Local\Programs\Python\Python35
echo %MYPYTHONHOME%
%MYPYTHONHOME%\python.exe %MYPYTHONHOME%\Tools\scripts\pyvenv.py --clear venv
.\venv\Scripts\pip.exe install requests
.\venv\Scripts\pip.exe install jinja2
REM install osnap
pushd .
cd ..
rm -r build
.\test_example\venv\Scripts\python.exe setup.py install
popd
