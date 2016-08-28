del /Q /S launchwin
REM assumes python is in the path
REM create the windows app using py2exe
python setup.py py2exe
REM put the app in a zip
python dist2zip.py
REM copy over to the test app so we can test the launcher out
REM del /Q /S ..\test_example\launchwin
REM mkdir ..\test_example\launchwin
REM xcopy /S launchwin\*.* ..\test_example\launchwin