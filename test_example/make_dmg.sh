#!/usr/bin/env bash
rm text_example.dmg
hdiutil create -volname test_example -srcfolder /Users/james/projects/osnap/test_example/dist -ov -format UDZO test_example.dmg
