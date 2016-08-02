#!/usr/bin/env bash
mkdir circle.iconset
sips -z 16 16     circle.png --out circle.iconset/icon_16x16.png
sips -z 32 32     circle.png --out circle.iconset/icon_16x16@2x.png
sips -z 32 32     circle.png --out circle.iconset/icon_32x32.png
sips -z 64 64     circle.png --out circle.iconset/icon_32x32@2x.png
sips -z 128 128   circle.png --out circle.iconset/icon_128x128.png
sips -z 256 256   circle.png --out circle.iconset/icon_128x128@2x.png
sips -z 256 256   circle.png --out circle.iconset/icon_256x256.png
sips -z 512 512   circle.png --out circle.iconset/icon_256x256@2x.png
sips -z 512 512   circle.png --out circle.iconset/icon_512x512.png
cp circle.png circle.iconset/icon_512x512@2x.png
iconutil -c icns circle.iconset
rm -R circle.iconset