#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.config import AppConfig
from pkg.translation import Translate
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class SettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # アプリケーション構成ファイルアクセスクラス
        self.app_config = AppConfig()

        # 翻訳クラスを生成
        self.tr = Translate()

        # 画面タイトルの設定
        self.setWindowTitle(self.tr.tr(self.__class__.__name__, "SETTING"))

        # ウインドウサイズ
        self.resize(800, 260)

        # フォントサイズ設定
        self.setFont(self.app_config.get_app_font())

        # ベースのレイアウト
        self.formLayout = QVBoxLayout(self)

        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        # グリッド
        self.gridLayout = QGridLayout()

        # 1行目
        self.label_l = QLabel(self)
        text = self.tr.tr(self.__class__.__name__, "Current library:")
        self.label_l.setText(text)
        self.label_l.setSizePolicy(size_policy)
        self.label_l.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_l, 0, 0, 1, 1)
        self.label_2 = QLabel(self)
        self.label_2.setText(self.app_config.get_db_path())
        self.label_2.setSizePolicy(size_policy)
        self.label_2.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        # 2行目
        self.label_3 = QLabel(self)
        text = self.tr.tr(self.__class__.__name__, "Select new location:")
        self.label_3.setText(text)
        self.label_3.setSizePolicy(size_policy)
        self.label_3.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        # エディット
        self.lineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 4)
        # ボタン
        self.pushButton = QPushButton(self)
        text = self.tr.tr(self.__class__.__name__, "select")
        self.pushButton.setText(text)
        self.gridLayout.addWidget(self.pushButton, 1, 5, 1, 1)

        # 3行目
        self.label_4 = QLabel(self)
        text = self.tr.tr(self.__class__.__name__, "Language:")
        self.label_4.setText(text)
        self.label_4.setSizePolicy(size_policy)
        self.label_4.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        # コンボボックス
        self.comboBox_1 = QComboBox(self)
        self.comboBox_1.addItems(self.tr.get_language_lists())
        self.comboBox_1.setCurrentText(self.app_config.get_language())
        self.gridLayout.addWidget(self.comboBox_1, 2, 1, 1, 1)

        # 4行目
        self.label_5 = QLabel(self)
        text = self.tr.tr(self.__class__.__name__, "Font size:")
        self.label_5.setText(text)
        self.label_5.setSizePolicy(size_policy)
        self.label_5.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.addItems(self.app_config.get_app_font_sizes())
        self.comboBox_2.setCurrentText(self.app_config.get_font_size())
        self.gridLayout.addWidget(self.comboBox_2, 3, 1, 1, 1)

        # スペーサー
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.formLayout.addLayout(self.gridLayout)

        # ボタンボックス
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        btn = self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)
        btn.setText(self.tr.tr(self.__class__.__name__, "ok"))
        btn = self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel)
        btn.setText(self.tr.tr(self.__class__.__name__, "cancel"))
        btn = self.buttonBox.button(QDialogButtonBox.StandardButton.Apply)
        btn.setText(self.tr.tr(self.__class__.__name__, "apply"))
        self.formLayout.addWidget(self.buttonBox)

        self.buttonBox.clicked.connect(self.handle_button_clicked)
        self.pushButton.clicked.connect(self.select_dir)

    def handle_button_clicked(self, button):
        standard_button = self.buttonBox.standardButton(button)
        if standard_button == QDialogButtonBox.StandardButton.Apply:
            self.update_setting()
            self.accept()
        elif standard_button == QDialogButtonBox.StandardButton.Cancel:
            self.reject()
        elif standard_button == QDialogButtonBox.StandardButton.Ok:
            self.accept()

    def select_dir(self):
        text = self.tr.tr(self.__class__.__name__, "Select Directory")
        directory = QFileDialog.getExistingDirectory(self, text)
        if directory:
            self.lineEdit.setText(os.path.normpath(directory))

    def update_setting(self):
        chg = False
        if self.lineEdit.text():
            self.app_config.config["APP_INFO"]["db_dir"] = self.lineEdit.text()
            chg = True
        if (
            self.app_config.config["APP_INFO"]["language"]
            != self.comboBox_1.currentText()
        ):
            self.app_config.config["APP_INFO"][
                "language"
            ] = self.comboBox_1.currentText()
            chg = True

        if (
            self.app_config.config["APP_GUI"]["font_size"]
            != self.comboBox_2.currentText()
        ):
            self.app_config.config["APP_GUI"][
                "font_size"
            ] = self.comboBox_2.currentText()
            chg = True

        if chg:
            self.app_config.write_config()
        return
