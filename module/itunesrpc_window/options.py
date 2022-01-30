# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import os, subprocess, time, threading, ast


def get_logger(log):
    # get logger for window
    global logger
    logger = log
    logger("module.itunesrpc_window.window_test logger active.")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(516, 238)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 160, 491, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "iTunesRPC-Remastered Settings")
        )
        self.open_logs.setText(
            _translate("MainWindow", "Open the log file \n" "in Windows Notepad.")
        )
        self.slow_connection.setText(
            _translate(
                "MainWindow",
                "Tick this if your computer\n"
                "is below the minimum \n"
                "recommended specs to \n"
                "run iTunesRPC\n"
                "Remastered.",
            )
        )
        self.settings_label.setText(_translate("MainWindow", "SETTINGS"))
        self.current_info.setText(_translate("MainWindow", "Currently Playing"))
        self.song.setText(_translate("MainWindow", "Song: "))
        self.artist.setText(_translate("MainWindow", "Artist: "))
        self.album.setText(_translate("MainWindow", "Album: "))
        self.label.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>CHANGES MADE <b>WILL NOT</b> TAKE EFFECT UNTIL </p><p><i>iTunesRPC-Remastered</i> IS RESTARTED.</p></body></html>",
            )
        )

    def closeEvent(self, event):
        logger("[GUI] CLOSING WINDOW")

        proc = subprocess.Popen("cd", shell=False, stdout=subprocess.PIPE)
        get_to_root_dir = proc.stdout.read().decode("utf-8").replace("\r\n", "")

        path_to_config = get_to_root_dir + "\\config"
        path_to_config = path_to_config.replace("\\\\", "\\")

        p = open(path_to_config, "r")
        prev = ast.literal_eval(p.readline())
        p.close()
        prev["gui_window_isOpen"] = False
        update = open(path_to_config, "w")
        update.write(str(prev))
        update.close()

        logger("[GUI] SAVED gui_window_isOpen AS FALSE.")

        event.accept()


class Logic(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, app, parent=None):
        logger("[GUI] OPENING WINDOW")

        self.app = app
        self._translate = QtCore.QCoreApplication.translate

        proc = subprocess.Popen("cd", shell=True, stdout=subprocess.PIPE)
        self.get_to_root_dir = proc.stdout.read().decode("utf-8").replace("\r\n", "")
        logger("[GUI] Root Directory: " + self.get_to_root_dir)

        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.open_logs.clicked.connect(self.open_log)
        self.slow_connection.stateChanged.connect(self.toggle_slow_connection)

        # code used to determine window state
        # this function (__init__) gets ran every time the window opens
        # closeEvent from the mainwindow class gets ran every time the window closes
        # below code allows to set the self.to_update var to true
        # this is used in the update definition
        self.path_to_config = self.get_to_root_dir + "\\config"
        self.path_to_config = self.path_to_config.replace("\\\\", "\\")

        p = open(self.path_to_config, "r")
        prev = ast.literal_eval(p.readline())
        p.close()
        prev["gui_window_isOpen"] = True
        update = open(self.path_to_config, "w")
        update.write(str(prev))
        update.close()
        self.to_update = True

        logger("[GUI] SAVED gui_window_isOpen AS TRUE.")

        # start new thread calling self.update()
        update_thread = threading.Thread(target=self.update, args=())
        update_thread.start()

    def update(self):
        _translate = self._translate
        while self.to_update:
            x = open("config", "r")
            conf_file = ast.literal_eval(x.readline())
            x.close()
            self.to_update = conf_file["gui_window_isOpen"]

            try:
                # read in current song info
                path = self.get_to_root_dir + "\\current_song_info"
                x = open(path, "r")
                curr = ast.literal_eval(x.readline())
                x.close()

                # format strings
                song_format = "Song: " + curr["song"]
                artist_format = "Artist: " + curr["artist"]
                album_format = "Album: " + curr["album"]

                # push strings
                self.song.setText(_translate("MainWindow", song_format))
                self.artist.setText(_translate("MainWindow", artist_format))
                self.album.setText(_translate("MainWindow", album_format))
            except Exception as e:
                logger("[GUI] ERROR: " + e)
                logger("[GUI] ASSUMING WINDOW IS CLOSED. STOPPING LOOP.")
                self.to_update = False

            logger("[GUI] Update ran.")
            time.sleep(1)
        logger("[GUI] Stopping update loop.")

    def open_log(self):
        cd_cmd = "C:\\Windows\\System32\\notepad.exe " + self.get_to_root_dir + "\\log"
        logger("[GUI] Running command: " + cd_cmd)
        os.system(cd_cmd)

    def toggle_slow_connection(self):
        path_to_config = self.path_to_config

        logger("[GUI] Reading config file.")
        f = open(path_to_config, "r")
        conf = ast.literal_eval(f.read())
        f.close()
        logger("[GUI] Config Info: " + str(conf))

        conf[
            "slow_mode"
        ] = self.slow_connection.isChecked()  # if the checkmark is checked we want
        # slow mode to be enabled, so we can just use the value that isChecked returns.
        logger(
            '[GUI] Key Stored: conf["slow_mode"] = '
            + str(self.slow_connection.isChecked())
        )

        conf_str = str(conf)
        logger("[GUI] New Config File: " + conf_str)

        logger("[GUI] Writing config file.")
        f = open(path_to_config, "w")
        f.write(conf_str)
        f.close()
        logger("[GUI] Written config file.")
