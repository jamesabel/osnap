
Related Tools
=============

Several tools already exist in this space, such as:

- `cx_freeze <http://cx-freeze.sourceforge.net/>`_
- `py2exe <http://www.py2exe.org/>`_
- `py2app <https://pythonhosted.org/py2app/>`_
- `briefcase <http://pybee.org/project/projects/tools/briefcase/>`_
- `pyinstaller <http://www.pyinstaller.org/>`_
- `bbfreeze <https://pypi.python.org/pypi/bbfreeze>`_
- `pynsist <https://github.com/takluyver/pynsist>`_
- `pyqtdeploy <https://www.riverbankcomputing.com/software/pyqtdeploy/>`_

However, ``osnap`` provides some specific features not found in these other tools:

- Works on hard-to-freeze packages such as `cryptography <https://cryptography.io>`_.
- Provides an executable file as the application's main invocation.  This way it looks like a traditional native
  application to the OS.
- Provides an installer (some tools only freeze the app and leave it up to the developer to do the installer).
- The self-contained Python environment created for the installer can also be used by the developer during development
  and debug. This can help reduce issues encountered in the final user's machine.
