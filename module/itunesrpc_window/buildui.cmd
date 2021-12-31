@echo off
echo Building project...
python.exe -m PyQt5.uic.pyuic ./window.ui -o window_test.py
echo Project compiled. Check window_test.py