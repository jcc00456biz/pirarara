#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide6.QtCore import (
    QMetaObject,
    QRect,
    Qt,
)

from PySide6.QtWidgets import (
    QComboBox,
    QGraphicsView,
    QMainWindow,
    QMenuBar,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)


class MWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(784, 564)
        self.centralwidget = QWidget(self)

        self.verticalLayout = QVBoxLayout(self.centralwidget)

        self.comboBox = QComboBox(self.centralwidget)

        self.verticalLayout.addWidget(self.comboBox)

        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.treeWidget = QTreeWidget(self.splitter_2)
        self.splitter_2.addWidget(self.treeWidget)
        self.tableWidget = QTableWidget(self.splitter_2)
        self.splitter_2.addWidget(self.tableWidget)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.graphicsView = QGraphicsView(self.splitter)
        self.splitter.addWidget(self.graphicsView)
        self.plainTextEdit = QPlainTextEdit(self.splitter)
        self.splitter.addWidget(self.plainTextEdit)
        self.splitter_2.addWidget(self.splitter)

        self.verticalLayout.addWidget(self.splitter_2)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 784, 33))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(self)
