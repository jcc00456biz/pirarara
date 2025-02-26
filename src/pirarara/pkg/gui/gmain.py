#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.const import __appname__, __version__
from pkg.gui.dialogs import AboutDialog
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QGraphicsView,
    QMainWindow,
    QMenuBar,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QToolBar,
    QToolButton,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)


class MWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 画面タイトルの設定
        self.setWindowTitle(f"{__appname__} {__version__}")

        # ウインドウサイズ設定
        self.resize(1280, 640)

        self.centralwidget = QWidget(self)

        # 垂直レイアウト
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # ツールバー
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(48, 48))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)
        # ツールボタン
        self.tool_button = QToolButton()
        # ツールボタンテキスト
        self.tool_button.setText(f"{__appname__}")
        # ツールボタンアイコン設定
        icon_dir = os.path.join(os.getcwd(), "icon")
        icon_file = os.path.join(icon_dir, "pirarara.svg")
        if os.path.exists(icon_file):
            self.tool_button.setIcon(QIcon(icon_file))
        # ツールボタンスタイル
        self.tool_button.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )
        # クリック時シグナルを受けるスロットと接続
        self.tool_button.clicked.connect(self.show_about_dialog)
        # ツールバーにツールボタンを配置
        self.toolbar.addWidget(self.tool_button)

        # コンボボックス
        self.comboBox = QComboBox(self.centralwidget)
        self.verticalLayout.addWidget(self.comboBox)

        # スプリッター
        self.splitter_1 = QSplitter(self.centralwidget)
        self.splitter_1.setOrientation(Qt.Orientation.Horizontal)

        # ツリーウィジェット
        self.treeWidget = QTreeWidget(self.splitter_1)
        self.splitter_1.addWidget(self.treeWidget)

        # テーブルウィジェット
        self.tableWidget = QTableWidget(self.splitter_1)
        self.splitter_1.addWidget(self.tableWidget)

        # スプリッター
        self.splitter_2 = QSplitter(self.splitter_1)
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)

        # グラフィックスビュー
        self.graphicsView = QGraphicsView(self.splitter_2)
        self.splitter_2.addWidget(self.graphicsView)

        # プレインテキストエディット
        self.plainTextEdit = QPlainTextEdit(self.splitter_2)
        self.splitter_2.addWidget(self.plainTextEdit)

        self.splitter_1.addWidget(self.splitter_2)
        self.verticalLayout.addWidget(self.splitter_1)

        self.setCentralWidget(self.centralwidget)
        # メニューバー
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 784, 33))
        self.setMenuBar(self.menubar)

        # ステータスバー
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        # dialog.exec()
        dialog.show()
