del /S /Q /F dist
del /S /Q /F installers
del /S /Q /F venv
del /S /Q /F osnapy
call make_venv.bat
call install_osnap.bat
call make_osnapy.bat
call make_installer.bat
