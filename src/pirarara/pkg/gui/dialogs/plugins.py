#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import logging
import os
import shutil
import zipfile

from pkg.config import AppConfig
from pkg.gui.custom import (
    critical_message_box,
    info_message_box,
    question_message_box,
)
from pkg.translation import Translate
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCloseEvent, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)

from .open_file import OpenFileDialog

logger = logging.getLogger(__name__)


class PluginsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # アプリケーション構成ファイルアクセスクラス
        self.app_config = AppConfig()

        # 翻訳クラスを生成
        self.tr = Translate()

        # 画面タイトルの設定
        self.setWindowTitle(self.tr.tr(self.__class__.__name__, "PLUGINS"))

        # ウインドウサイズ
        self.resize(800, 260)

        # フォントサイズ設定
        self.setFont(self.app_config.get_app_font())

        # ベースのレイアウト
        self.formLayout = QVBoxLayout(self)

        # 横レイアウト
        self.horizontalLayout = QHBoxLayout()
        # リスト
        self.plugins_list = QListWidget(self)
        self.horizontalLayout.addWidget(self.plugins_list)

        # 縦レイアウト
        self.verticalLayout = QVBoxLayout()
        # プラグイン追加
        self.add_plugins = QPushButton(self)
        self.add_plugins.setText(
            self.tr.tr(self.__class__.__name__, "Add plugins")
        )
        self.verticalLayout.addWidget(self.add_plugins)
        # プラグイン削除
        self.remove_plugins = QPushButton(self)
        self.remove_plugins.setText(
            self.tr.tr(self.__class__.__name__, "Remove plugins")
        )
        self.verticalLayout.addWidget(self.remove_plugins)
        # スペーサー
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(self.verticalSpacer)
        # 横レイアウトに追加
        self.horizontalLayout.addLayout(self.verticalLayout)

        # ベースレイアウトに設定
        self.formLayout.addLayout(self.horizontalLayout)

        # ボタンボックス
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        btn = self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)
        btn.setText(self.tr.tr(self.__class__.__name__, "ok"))
        btn = self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel)
        btn.setText(self.tr.tr(self.__class__.__name__, "cancel"))
        self.formLayout.addWidget(self.buttonBox)

        # インストール済プラグインリスト表示
        self.build_plugins_list()

        # シグナルにスロット割当
        self.add_plugins.clicked.connect(self.add_plugins_clicked)
        self.remove_plugins.clicked.connect(self.remove_plugins_clicked)
        self.buttonBox.clicked.connect(self.handle_button_clicked)

    def handle_button_clicked(self, button):
        standard_button = self.buttonBox.standardButton(button)
        if standard_button == QDialogButtonBox.StandardButton.Cancel:
            self.reject()
        elif standard_button == QDialogButtonBox.StandardButton.Ok:
            self.accept()

    def add_plugins_clicked(self):
        dialog = OpenFileDialog(
            ["zip (*.zip)"], QFileDialog.FileMode.ExistingFile, self
        )
        selected_files = dialog.get_selected_file()

        # 選択されたファイルが無い場合
        if len(selected_files) == 0:
            return

        # プラグインファイル名からインストール
        select_file_path = selected_files[0]
        plugin_fname = os.path.splitext(os.path.basename(select_file_path))[0]

        # プラグインディレクトリ
        plugin_dir = self.app_config.get_plugins_dir()

        # ラグインファイルパス
        plugin_path = os.path.join(plugin_dir, plugin_fname)
        if os.path.exists(plugin_path):
            info_message_box(
                self.tr.tr(
                    self.__class__.__name__, "The plugin is already installed."
                ),
                self,
            )
            return

        # ZIP ファイルを展開
        try:
            with zipfile.ZipFile(select_file_path, "r") as zip_ref:
                # 出力フォルダを作成（存在しない場合）
                os.makedirs(plugin_path, exist_ok=True)
                # ZIP ファイルを展開
                zip_ref.extractall(plugin_path)
        except zipfile.BadZipFile:
            critical_message_box(
                self.tr.tr(self.__class__.__name__, "Invalid ZIP file."),
                self,
            )
        except Exception:
            critical_message_box(
                self.tr.tr(
                    self.__class__.__name__, "An unexpected error occurred."
                ),
                self,
            )
        else:
            # インストール済プラグインリスト表示
            self.build_plugins_list()

    def remove_plugins_clicked(self):
        selected_item = self.plugins_list.currentItem()
        if not selected_item:
            return

        ret = question_message_box(
            self.tr.tr(
                self.__class__.__name__, "Deletes the selected plugin."
            ),
            self,
        )
        if not ret:
            return

        # 選択したプラグインを削除
        plugin_dir = self.app_config.get_plugins_dir()
        target_path = os.path.join(plugin_dir, selected_item.text())
        if not os.path.exists(target_path):
            return
        try:
            shutil.rmtree(target_path)
        except Exception:
            critical_message_box(
                self.tr.tr(
                    self.__class__.__name__, "An unexpected error occurred."
                ),
                self,
            )
        else:
            # インストール済プラグインリスト表示
            self.build_plugins_list()

        return

    def build_plugins_list(self):
        # プラグインディレクトリを探索
        plugin_dir = self.app_config.get_plugins_dir()
        target_path = os.path.join(plugin_dir, "*")
        # ディレクトリのみを取得
        directories = [d for d in glob.glob(target_path) if os.path.isdir(d)]
        # ディレクトリをソート（アルファベット順）
        sorted_directories = sorted(directories)
        # リストに積み込む
        self.plugins_list.clear()
        for item in sorted_directories:
            self.plugins_list.addItem(os.path.basename(item))
