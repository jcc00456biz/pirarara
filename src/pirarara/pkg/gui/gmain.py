#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.const import __appname__, __version__
from pkg.gui.custom import (
    PirararaComboBox,
    PirararaTableWidget,
    PirararaToolButton,
    PirararaTreeWidget,
)
from pkg.gui.dialogs import AboutDialog, ImportFileDialog
from pkg.metadata import set_media_info
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

        # ツールボタン定義
        self.tool_button_define = (
            ("IMPORT", "import.svg", self.show_import_file_dialog),
            ("|", "", None),
            (f"{__appname__} ", "pirarara.svg", self.show_about_dialog),
        )
        # ツールボタン
        self.tool_buttons = []
        for title, icon_file_name, slot in self.tool_button_define:
            if title == "|":
                self.toolbar.addSeparator()
                continue
            # アイコン
            icon_dir = os.path.join(os.getcwd(), "icon")
            icon_file_path = os.path.join(icon_dir, icon_file_name)
            self.tool_buttons.append(PirararaToolButton(title, icon_file_path))
            # スロット
            if slot is not None:
                self.tool_buttons[-1].clicked.connect(slot)
            # ツールバーにツールボタンを配置
            self.toolbar.addWidget(self.tool_buttons[-1])

        # コンボボックス
        self.comboBox = PirararaComboBox(self.centralwidget)
        self.verticalLayout.addWidget(self.comboBox)

        # スプリッター
        self.splitter_1 = QSplitter(self.centralwidget)
        self.splitter_1.setOrientation(Qt.Orientation.Horizontal)

        # ツリーウィジェット
        self.treeWidget = PirararaTreeWidget(self.splitter_1)
        self.splitter_1.addWidget(self.treeWidget)

        # テーブルウィジェット
        self.tableWidget = PirararaTableWidget(self.splitter_1)
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

        # コンボボックスのシグナルにスロットを割り当て
        self.comboBox.item_edited.connect(self.on_combo_box_editing)

        # ツリーウィジェットのシグナルにスロットを割り当て
        self.treeWidget.item_selected.connect(
            self.on_tree_widget_item_selected
        )

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def show_import_file_dialog(self):
        dialog = ImportFileDialog(self)
        selected_files = dialog.get_selected_file()
        print(selected_files)

        for fname in selected_files:
            print(fname)
            ret = set_media_info(fname)
            print(ret)

    def on_combo_box_editing(self, text: str):
        if len(text) == 0:
            self.tableWidget.get_form_db("", "")
        else:
            self.tableWidget.get_form_db("title", text)

    def on_tree_widget_item_selected(self, column_text, parent_text):
        # 選択したもので表示
        self.tableWidget.get_form_db(parent_text, column_text)

    def show_message(self, message):
        # メッセージボックスでメッセージを表示
        QMessageBox.information(self, "情報", message)
