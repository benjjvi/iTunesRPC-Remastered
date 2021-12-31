# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os

def get_logger(log):
    #get logger for window
    global logger
    logger = log
    logger("module.itunesrpc_window.window_test logger active.")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(671, 165)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\../../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_logs = QtWidgets.QPushButton(self.centralwidget)
        self.open_logs.setGeometry(QtCore.QRect(20, 114, 151, 41))
        self.open_logs.setObjectName("open_logs")
        self.slow_connection = QtWidgets.QCheckBox(self.centralwidget)
        self.slow_connection.setGeometry(QtCore.QRect(20, 40, 151, 71))
        self.slow_connection.setObjectName("slow_connection")
        self.settings_label = QtWidgets.QLabel(self.centralwidget)
        self.settings_label.setGeometry(QtCore.QRect(20, 10, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.settings_label.setFont(font)
        self.settings_label.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.settings_label.setTextFormat(QtCore.Qt.PlainText)
        self.settings_label.setScaledContents(True)
        self.settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_label.setObjectName("settings_label")
        self.current_info = QtWidgets.QLabel(self.centralwidget)
        self.current_info.setGeometry(QtCore.QRect(200, 10, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.current_info.setFont(font)
        self.current_info.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.current_info.setTextFormat(QtCore.Qt.PlainText)
        self.current_info.setScaledContents(True)
        self.current_info.setAlignment(QtCore.Qt.AlignCenter)
        self.current_info.setObjectName("current_info")
        self.song = QtWidgets.QLabel(self.centralwidget)
        self.song.setGeometry(QtCore.QRect(200, 40, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.song.setFont(font)
        self.song.setObjectName("song")
        self.artist = QtWidgets.QLabel(self.centralwidget)
        self.artist.setGeometry(QtCore.QRect(200, 60, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.artist.setFont(font)
        self.artist.setObjectName("artist")
        self.album = QtWidgets.QLabel(self.centralwidget)
        self.album.setGeometry(QtCore.QRect(200, 80, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.album.setFont(font)
        self.album.setObjectName("album")
        self.song_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.song_bar.setEnabled(True)
        self.song_bar.setGeometry(QtCore.QRect(200, 120, 321, 23))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.song_bar.setFont(font)
        self.song_bar.setProperty("value", 24)
        self.song_bar.setInvertedAppearance(False)
        self.song_bar.setFormat("")
        self.song_bar.setObjectName("song_bar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(530, 10, 131, 141))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(".\\../../icon.ico"))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "iTunesRPC Remastered"))
        self.open_logs.setText(_translate("MainWindow", "Open the log file \n" "in Windows Notepad."))
        self.slow_connection.setText(_translate("MainWindow", "Tick this if your computer\n" "is below the minimum \n" "recommended specs to \n" "run iTunesRPC\n" "Remastered."))
        self.settings_label.setText(_translate("MainWindow", "SETTINGS"))
        self.current_info.setText(_translate("MainWindow", "Currently Playing"))
        self.song.setText(_translate("MainWindow", "Song: "))
        self.artist.setText(_translate("MainWindow", "Artist: "))
        self.album.setText(_translate("MainWindow", "Album: "))

class Logic(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.open_logs.clicked.connect(self.open_log)

    def open_log(self):
        cmd = "C:\\Windows\\System32\\notepad.exe "
        cmd = cmd + (os.path.dirname(os.path.realpath(__file__)))
        cmd = cmd + "\\log"
        logger("Running command: " + cmd)
        os.system(cmd)
