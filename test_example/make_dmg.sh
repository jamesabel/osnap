#!/usr/bin/env bash
rm myapp.dmg
hdiutil create -volname myapp -srcfolder /Users/james/projects/osnap/test_example -ov -format UDZO myapp.dmg
