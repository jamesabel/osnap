rmdir /Q /S venv
"C:\Program Files\Python37\python.exe" -m venv --clear venv
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\pip3 install -U setuptools
venv\Scripts\pip3 install -r requirements.txt
