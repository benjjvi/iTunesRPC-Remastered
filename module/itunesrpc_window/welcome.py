# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './welcome.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import ast
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets


def get_logger(log):
    global logger
    logger = log


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(523, 145)
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 521, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.dont_show_on_startup = QtWidgets.QCheckBox(self.centralwidget)
        self.dont_show_on_startup.setGeometry(QtCore.QRect(320, 110, 191, 21))
        self.dont_show_on_startup.setObjectName("dont_show_on_startup")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 521, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.ok = QtWidgets.QPushButton(self.centralwidget)
        self.ok.setGeometry(QtCore.QRect(14, 110, 301, 23))
        self.ok.setObjectName("ok")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Welcome to iTunesRPC-Remastered")
        )
        self.label.setText(_translate("MainWindow", "Welcome to iTunesRPC-Remastered"))
        self.dont_show_on_startup.setText(
            _translate("MainWindow", "Don't show this window at start up.")
        )
        self.label_2.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:14pt;">To access the main options window, right click on the <br>Apple Music icon in your system tray.</span></p></body></html>',
            )
        )
        self.ok.setText(_translate("MainWindow", "OK, Thank You! :)"))


class Logic(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        proc = subprocess.Popen("cd", shell=True, stdout=subprocess.PIPE)
        self.get_to_root_dir = proc.stdout.read().decode("utf-8").replace("\r\n", "")
        logger("[WELCOME-GUI] Root Directory: " + self.get_to_root_dir)

        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.ok.clicked.connect(self.close_win_welcome)
        self.dont_show_on_startup.stateChanged.connect(self.toggle_dont_show_on_startup)

    def toggle_dont_show_on_startup(self):
        path_to_config = self.get_to_root_dir + "\\config"
        path_to_config = path_to_config.replace("\\\\", "\\")
        logger("[WELCOME-GUI] Reading config file.")
        f = open(path_to_config, "r")
        conf = ast.literal_eval(f.read())
        f.close()
        logger("[WELCOME-GUI] Config Info: " + str(conf))

        conf[
            "show_msg"
        ] = (
            not self.dont_show_on_startup.isChecked()
        )  # if the checkmark is checked we want
        # slow mode to be enabled, so we can just use the value that isChecked returns.
        logger(
            '[WELCOME-GUI] Key Stored: conf["show_msg"] = '
            + str(not self.dont_show_on_startup.isChecked())
        )

        conf_str = str(conf)
        logger("[WELCOME-GUI] New Config File: " + conf_str)

        logger("[WELCOME-GUI] Writing config file.")
        f = open(path_to_config, "w")
        f.write(conf_str)
        f.close()
        logger("[WELCOME-GUI] Written config file.")

    def close_win_welcome(self):
        logger("[WELCOME-GUI] Closing Welcome GUI.")
        self.close()
