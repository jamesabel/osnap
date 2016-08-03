#!/usr/bin/env bash
python3 create_installer.py
hdiutil create -volname test_example -srcfolder /Users/james/projects/osnap/test_example/dist -ov -format UDZO test_example.dmg