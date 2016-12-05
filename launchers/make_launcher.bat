REM you may want to turn off your virus scanner for this
REM for some reason I have seen py2exe fail if the virus scanner is running
del /Q /S launchwin
REM assumes python is in the path
REM create the windows app using py2exe
venv\Scripts\python.exe setup.py py2exe
REM put the app in a zip
venv\Scripts\python.exe dist2zip.py
REM copy over to the test app so we can test the launcher out
REM del /Q /S ..\test_example\launchwin
REM mkdir ..\test_example\launchwin
REM xcopy /S launchwin\*.* ..\test_example\launchwin
del /Q ..\osnap\launchwin-amd64-window.zip
move launchwin.zip ..\osnap\launchwin-amd64-window.zip