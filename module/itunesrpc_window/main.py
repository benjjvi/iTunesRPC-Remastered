#wrapper for the window.py app
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import module.itunesrpc_window.window_test as window

def get_logger(log):
    #get logger for wrapper
    global logger
    logger = log
    logger("module.itunesrpc_window.main logger active.")

def send_logger():
    window.get_logger(logger) #pass logger onto the real window

def start():
    app = QtWidgets.QApplication(sys.argv)
    win = window.Logic()
    win.show()
    sys.exit(app.exec_())