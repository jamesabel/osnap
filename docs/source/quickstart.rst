
OSNAP Quick Start
=================

If you haven't done so already, create a `virtualenv <https://docs.python.org/3/library/venv.html>`_ for your Python
project.  We will refer to your Python virtual environment directory as ``venv``.

Install osnap from PyPI by executing ``pip install osnap``.  Alternatively you can get osnap
from `github <https://github.com/jamesabel/osnap>`_ and install it into your ``venv`` by executing
``python setup.py install`` from the osnap directory.

Create a `requirements.txt <https://pip.pypa.io/en/stable/user_guide/#requirements-files>`_ file for your project.
You can add to this as you go, but make sure you keep this up to date with all the packages you need for your project.

Run ``venv/bin/python -m osnap.osnapy`` (or equivalent for the OS you're on).  This should create an osnapy directory,
which contains a complete stand-alone Python environment for your project.  If you want a Python version different than
the default, use the ``--python <version>`` switch.

Develop your Python application.

Run ``venv/bin/python -m osnap.installer --author <author name> --app <your app name>`` .  This will
create an installer for your application for the OS that you are running on.  ``Author`` may be your name or your
company's name.  If you have spaces in a name, put the name in double quotes.

