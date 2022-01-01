@echo off
echo Building project...
python.exe -m PyQt5.uic.pyuic ./window.ui -o options_staged.py
echo Project compiled. Check options_staged.py