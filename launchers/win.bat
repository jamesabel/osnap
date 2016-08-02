del /Q /S launchwin
REM assumes python is in the path
python setup.py py2exe
python dist2py.py
REM copy over to the test app so we can test the launcher out
del /Q /S ..\test_example\launchwin
mkdir ..\test_example\launchwin
xcopy /S launchwin\*.* ..\test_example\launchwin