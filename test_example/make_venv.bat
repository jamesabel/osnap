REM point this to your python 3
set MYPYTHONHOME="c:\Program Files\Python36"
echo %MYPYTHONHOME%
%MYPYTHONHOME%\python.exe -m venv --clear venv
.\venv\Scripts\pip.exe install -U pip
.\venv\Scripts\pip.exe install -U -r requirements.txt
REM install osnap
pushd .
cd ..
rm -r build
.\test_example\venv\Scripts\python.exe setup.py install
popd
