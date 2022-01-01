@echo off
echo Building project...
python.exe -m PyQt5.uic.pyuic ./welcome.ui -o welcome.py
echo Project compiled. Check welcome.py