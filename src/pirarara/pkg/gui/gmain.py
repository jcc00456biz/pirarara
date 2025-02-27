#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.const import __appname__, __version__
from pkg.gui.custom import PirararaToolButton
from pkg.gui.dialogs import AboutDialog
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QGraphicsView,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QToolBar,
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
        # QActionの作成
        action_list = []
        for i in range(4):
            action = QAction(f"アクション{i}", self)
            action.triggered.connect(
                lambda: self.show_message(f"アクション{i}が選択されました")
            )
            action_list.append(action)
        icon_dir = os.path.join(os.getcwd(), "icon")
        icon_file = os.path.join(icon_dir, "pirarara.svg")
        if os.path.exists(icon_file):
            self.tool_button = PirararaToolButton(
                __appname__, icon_file, action_list
            )
        else:
            self.tool_button = PirararaToolButton(__appname__)

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

    def show_message(self, message):
        # メッセージボックスでメッセージを表示
        QMessageBox.information(self, "情報", message)
