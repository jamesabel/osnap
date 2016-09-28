
Example
=======

See `test_example <https://github.com/jamesabel/osnap/tree/master/test_example>`_ for an example.  Look over
the make_*.* files.  These should be used in this order:

- make_venv.[sh | bat] - makes your Python virtual environment.  This is typical Python usage and is **not**
  specific to ``OASNAP``.
- make_osnapy.[sh | bat] - make the osnapy Python environment that will be bundled with your installation.
- make_installer.[sh | bat] - makes the installer for the OS that it's running on.  This is the final step in the
  process.

