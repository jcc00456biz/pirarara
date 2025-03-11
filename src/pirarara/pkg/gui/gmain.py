#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.config import AppConfig
from pkg.const import __appname__, __version__
from pkg.gui.custom import (
    PirararaImageViewer,
    PirararaComboBox,
    PirararaTableWidget,
    PirararaToolButton,
    PirararaTreeWidget,
)
from pkg.gui.dialogs import AboutDialog, ImportFileDialog
from pkg.metadata import set_media_info
from PySide6.QtCore import QRect, QSize, Qt

# from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGraphicsView,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class MWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # アプリケーション構成ファイルアクセスクラス
        self.app_config = AppConfig()

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
        self.graphicsView = PirararaImageViewer(self.splitter_2)
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

        # ウインドウ位置、サイズなどを設定
        self._setup()

        # コンボボックスのシグナルにスロットを割り当て
        self.comboBox.item_edited.connect(self.on_combo_box_editing)

        # ツリーウィジェットのシグナルにスロットを割り当て
        self.treeWidget.item_selected.connect(
            self.on_tree_widget_item_selected
        )

        # テーブルウィジェットのシグナルにスロットを割り当て
        self.tableWidget.item_selected.connect(
            self.on_table_widget_item_selected
        )

    def _setup(self):
        """
        アプリケーション構成ファイルがデフォルト値であれば
        フォントサイズ以外は設定されていないので設定して保存
        """
        if self.app_config.isdefault:
            self.app_config.config["APP_GUI"]["main_window"] = (
                self.app_config.q_bytearray_to_str(self.saveGeometry())
            )
            self.app_config.config["APP_GUI"]["splitter1"] = (
                self.app_config.q_bytearray_to_str(self.splitter_1.saveState())
            )
            self.app_config.config["APP_GUI"]["splitter2"] = (
                self.app_config.q_bytearray_to_str(self.splitter_2.saveState())
            )
            self.app_config.write_config()
        else:
            self.restoreGeometry(
                self.app_config.str_to_q_bytearray(
                    self.app_config.config["APP_GUI"]["main_window"]
                )
            )
            self.splitter_1.restoreState(
                self.app_config.str_to_q_bytearray(
                    self.app_config.config["APP_GUI"]["splitter1"]
                )
            )
            self.splitter_2.restoreState(
                self.app_config.str_to_q_bytearray(
                    self.app_config.config["APP_GUI"]["splitter2"]
                )
            )

    def closeEvent(self, event):
        self.app_config.config["APP_GUI"]["main_window"] = (
            self.app_config.q_bytearray_to_str(self.saveGeometry())
        )
        self.app_config.config["APP_GUI"]["splitter1"] = (
            self.app_config.q_bytearray_to_str(self.splitter_1.saveState())
        )
        self.app_config.config["APP_GUI"]["splitter2"] = (
            self.app_config.q_bytearray_to_str(self.splitter_2.saveState())
        )
        self.app_config.write_config()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.tableWidget.hasFocus():
            reply = QMessageBox.question(
                self,
                "message",
                "Is it okay to delete this?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
            # 表の選択されているデータを削除
            self.tableWidget.delete_selected_items()
            # データ削除に伴い表示を更新
            self.graphicsView.clear_image()
            self.treeWidget.refresh_display()
            self.tableWidget.get_form_db("", "")

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def show_import_file_dialog(self):
        dialog = ImportFileDialog(self)
        selected_files = dialog.get_selected_file()

        for fname in selected_files:
            set_media_info(fname)

        self.treeWidget.refresh_display()
        self.tableWidget.get_form_db("", "")

    def on_combo_box_editing(self, text: str):
        if len(text) == 0:
            self.tableWidget.get_form_db("", "")
        else:
            self.tableWidget.get_form_db("title", text)

    def on_tree_widget_item_selected(self, column_text: str, parent_text: str):
        # 選択したもので表示
        self.tableWidget.get_form_db(parent_text, column_text)

    def on_table_widget_item_selected(self, db_id: int):
        self.graphicsView.show_image(db_id)
