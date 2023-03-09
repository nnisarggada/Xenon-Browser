#!/bin/sh

python -m pip install pyinstaller
python -m pip install PySide6
python -m pip install requests
python -m pip install pyqtdarktheme
python -m pip install pyqtdarktheme
python -m PyInstaller Xenon-Browser.spec
mkdir /usr/lib/Xenon-Browser
cp $PWD/dist/Xenon-Browser /usr/lib/Xenon-Browser/Xenon-Browser
cp $PWD/xenon-white.png /usr/lib/Xenon-Browser/
cp Xenon.desktop /usr/share/applications/
