Limitations/Inefficiencies
==========================

- Requires Python 3.5 and after. (``osnap`` uses the
  `embedded Python <https://docs.python.org/3.5/using/windows.html#embedded-distribution>`_ for Windows, first
  provided in Python 3.5)
- Since ``osnap`` includes everything a package installs, the resultant installation will generally be larger than the
  minimum actually required by the application.
- The user has to specify all the required packages.  There is no 'auto discovery'.  Since auto discovery can be a
  source of issues, this is actually more of a feature.  Also, this is derived from ``requirements.txt``, so the
  user should have this already anyway.
