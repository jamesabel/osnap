
User Guide
==========

Introduction
------------
`OSNAP` essentially has two phases - the development phase and the installer phase.  Freezing and installing
applications can run into issues and it's best to proceed step by step.  This is handy in case there are problems so
that debugging is a more reasonable task.

Development Phase
^^^^^^^^^^^^^^^^^
In the development phase you create the Python environment that you use to run your code.  You first create a
traditional virtual Python environment.  We use `venv` for this Python environment directory name.
This is separate from using `OSNAP`, but it allows the programmer to first develop and test their application in the
traditional way.

The `OSNAP` package is installed into this `venv`. ::

    pip install osnap

Once some basic application functionality is achieved it is recommended that `OSNAP` be used to create the
`OSNAP` Python environment.  This this is done by: ::

    venv/bin/python3 -m osnap.osnapy   # e.g. for OSX

This Python environment is in the `osnapy` directory (note the 'y' - osnapy is short for `OSNAP Python`).
The `osnapy` directory is a separate and stand-alone Python environment that will be packaged up as part of the
application delivered to end users.  `requirements.txt` is used to determine what Python packages are installed
into osnapy.  The Python interpreter in `osnapy` should be used for testing to ensure functionality.

Installation Phase
^^^^^^^^^^^^^^^^^^
In this phase we create the installer that you will deliver to end users. This is where your application,
the `osnapy` Python environment, and the OS-specific launcher are combined into a complete application for a
specific OS.

Since there are several parameters given to the installer, you must create a small Python program like this: ::

    import osnap.installer
    import test_example

    APPLICATION_NAME = 'test_example'
    AUTHOR = 'test'

    def make_installer(verbose):
        osnap.installer.make_installer(AUTHOR, APPLICATION_NAME, 'this is my test example', 'www.mydomain.com',
                                       [APPLICATION_NAME], test_example.__version__, verbose=verbose)

    if __name__ == '__main__':
        make_installer(True)

Run this program to create the appropriate installer for the OS you are running on.

Application Layout
------------------

Lay out your Python application like this: ::

  - < project root >
    - main.py
    - my_project
      - < project files ... >

At a minimum `main.py` must have this structure: ::

    def main():
        < your code >

    if __name__ == '__main__':
        main()

Typically your code will be contained in a separate package, so it will look more like: ::

    import my_application.my_module

    def main():

        # initialization or argument processing code can go here ...

        my_application.my_module.run()

    if __name__ == '__main__':
        main()

See the test_example code for a more complete example.
