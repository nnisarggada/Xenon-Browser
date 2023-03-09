#!/bin/sh

python -m pip install pyinstaller
python -m PyInstaller Xenon-Browser.spec
mkdir /usr/lib/Xenon-Browser
cp $PWD/dist/Xenon-Browser /usr/lib/Xenon-Browser/Xenon-Browser
cp $PWD/xenon-white.png /usr/lib/Xenon-Browser/
cp Xenon.desktop /usr/share/applications/
