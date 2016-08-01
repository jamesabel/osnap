# osnap - Overly Simplistic Native Application tool for Python #

----------

## Introduction ##
`osnap` is a way to deliver self-contained Python applications to end users for Windows and (soon) OSX/MacOS.  This process
is known as 'freezing' and installing.  Examples include delivering Python applications to Windows PCs (both laptops and desktops), MacBooks, and iMacs.

## Related Tools ##

Several tools already exist in this space, such as [cx_freeze](http://cx-freeze.sourceforge.net/), [py2exe](http://www.py2exe.org/), [py2app](https://pythonhosted.org/py2app/), 
[briefcase](http://pybee.org/project/projects/tools/briefcase/), [pyinstaller](http://www.pyinstaller.org/), and [pynsist](https://github.com/takluyver/pynsist).  However, `osnap` provides some specific features not found in these other 
tools:

- Works on hard-to-freeze packages such as [cryptography](https://cryptography.io).
- Provides an executable file as the application's main invocation.  This way it looks like a traditional native application 
  to the OS.
- Binary files are encoded in `osnap` into Python files so that the osnap distribution itself is pure Python (not
  a collection of Python and non-Python files, which can be problematic).
- Provides an installer (some tools only freeze the app and leave it up to the developer to do the installer).
- The self-contained Python environment created for the installer can also be used by the developer during development and debug. This can help reduce issues encountered in the final user's machine.

## Limitations/Inefficiencies ##

- Requires Python 3.5 and after (`osnap` uses the [embedded Python](https://docs.python.org/3.5/using/windows.html#embedded-distribution) 
  for Windows, first provided in Python 3.5)
- Since `osnap` includes everything a package installs, the resultant installation may be larger than is actually required 
  by the application.
- The user has to specify all the required packages.  There is no 'auto discovery'.  Since auto discovery can be a source 
  of issues, this is actually more of a feature.
- There is no command line interface capability - it's all in Python.  This strategy was chosen since usually the usage of
  the tool is too complex for a command line.

## Setup ##

`osnap` is not yet on [PyPI](https://pypi.python.org), so for now download the [zip](https://github.com/jamesabel/osnap/archive/master.zip) and do a `python setup.py install` (this python should be from your [venv](https://docs.python.org/3/library/venv.html)).

## Usage ##

In general, there are 2 phases:

1. Creation of the Python environment (this will be in the `osnappython` folder)
2. Creation of the installer

The `osnap` Python environment may be created during development.  Alternatively, the developer can use their own Python environment (e.g. a [venv](https://docs.python.org/3/library/venv.html)), but eventually an `osnap` Python environment will 
have to be created as this is the one that ships with the application.

See the [test_example](https://github.com/jamesabel/osnap/blob/master/test_example/test_osnap.py) for example usage.

## Requirements ##

- For Windows, [NSIS](http://nsis.sourceforge.net/) must be installed on the development machine.  As of this writing,
  Version 3 is used.