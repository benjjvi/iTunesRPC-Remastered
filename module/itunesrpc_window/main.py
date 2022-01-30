# encoding: utf-8
# wrapper for the window.py app
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import module.itunesrpc_window.options as options
import module.itunesrpc_window.welcome as welcome


def get_logger(log):
    # get logger for wrapper
    global logger
    logger = log
    logger("module.itunesrpc_window.main logger active.")


def send_logger():
    options.get_logger(logger)  # pass logger onto the real window
    welcome.get_logger(logger)  # pass logger onto the first open window


def start_welcome():
    welc_app = QtWidgets.QApplication(sys.argv)
    welc = welcome.Logic()
    welc.show()
    welc_app.exec_()


def start(self):
    app = QtWidgets.QApplication(sys.argv)
    win = options.Logic(app=app)
    win.show()
    app.exec_()
