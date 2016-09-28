
OS Support
==========

Background
----------
The philosophy around ``OSNAP`` is to bundle an embedded Python environment (interpreter) with your application.
Windows and OSX/MacOS [1]_ are supported.  However, currently the
support for embedded Python for each OS is quite different from each other (hopefully in the future these
will converge).

Windows
-------
In Python 3.5, `Steve Dower added an embedded Python zip <https://blogs.msdn.microsoft.com/pythonengineering/2016/04/26/cpython-embeddable-zip-file/>`_
to the general distribution on python.org.  This makes embedding Python in an application fairly straightforward.
So, this is used directly by ``OSNAP``.

OSX/MacOS
---------
As of this writing there is no embedded Python for Mac in the general distribution.  ``OSNAP`` has two techniques
to fill this, each with their pros and cons:

Compilation
^^^^^^^^^^^
This technique compiles Python as part of the creation of the Python environment (what's in the ``osnapy``
directory).  Mac compliation of Python requires absolute path names, so we predetermine the path that ``osnapy``
will be on the end user's system - i.e. ``/Applications/<application name>.app/Contents/MacOS/osnapy/`` - and
compile and "install" into that location.  The pros/cons are:

Pros:

- This should be a complete solution since we have a regular Python environment : the Python interpreter, pip, etc.
- All the tools are generally available and free.

Cons:

- We have to compile.
- We need to install tools/libraries like XCode and OpenSSL.
- There is always a chance that compilation doesn't work for some reason.
- It's compiling (actually installing) into the /Applications directory, which requires root (sudo) for part of it.

eGenix™ PyRun™
^^^^^^^^^^^^^^
This uses `eGenix PyRun <http://www.egenix.com/products/python/PyRun/>`_, which is essentially an embedded
Python environment.  The pros/cons are:

Pros:

- Prebuilt
- Compact
- Easy to use (like the Windows Embedded Python)

Cons:

- Is not necessarily 100% compatible with the general Python distribution.  May not work with all packages.

Current Default
^^^^^^^^^^^^^^^
In order to support the widest range of end user applications, currently the compilation technique is the default.

.. [1] Here we are using OSX and MacOS interchangeably.