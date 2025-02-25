#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide6.QtCore import QMetaObject, QRect
from PySide6.QtWidgets import QMainWindow, QMenuBar, QStatusBar, QWidget


class MWindow(QMainWindow):
    def setupUi(self, MainWindow):

        MainWindow.resize(415, 263)

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 415, 33))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(MainWindow)
