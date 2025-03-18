#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import logging

from pkg.config import AppConfig
from pkg.translation import Translate
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

logger = logging.getLogger(__name__)


class PirararaBasePlugin(QDialog):
    def __init__(self, action_count: int, parent=None):
        super().__init__(parent)

        # アプリケーション構成ファイルアクセスクラス
        self.app_config = AppConfig()

        # 翻訳クラスを生成
        self.trans = Translate()

        # ウインドウサイズ
        self.setFixedSize(640, 128)

        # 画面タイトルの設定
        self.setWindowTitle(
            self.trans.tr(self.__class__.__name__, "Under processing")
        )

        # フォントサイズ設定
        self.setFont(self.app_config.get_app_font())

        self.formLayout = QVBoxLayout(self)

        # メッセージ
        self.msg_label = QLabel(self)
        self.msg_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.formLayout.addWidget(self.msg_label)

        # プログレスバー
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid black;
                border-radius: 0px;
            }
            QProgressBar::chunk {
                background-color: lightgray;
            }
            """
        )
        self.progress_bar.setRange(0, action_count)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setFormat("%p%")
        self.formLayout.addWidget(self.progress_bar)

        # ボタンボックス
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
        )
        btn = self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel)
        btn.setText(self.trans.tr(self.__class__.__name__, "cancel"))
        self.formLayout.addWidget(self.buttonBox)

        self.buttonBox.clicked.connect(self.handle_button_clicked)
        self.action_count = action_count
        self.current_count = 0
        self.was_canceled = False
        # シングルショットタイマを実行
        QTimer.singleShot(1, self.do_action)

    def _close(self):
        gc.collect()
        self.close()

    def handle_button_clicked(self, button):
        standard_button = self.buttonBox.standardButton(button)
        if standard_button == QDialogButtonBox.StandardButton.Cancel:
            if not self.was_canceled:
                self.was_canceled = True

    def do_action(self):
        """
        do_actionは派生クラスでオーバーライトし処理をした後に
        基底クラスのこのメソッドを呼び出すこと。
        また基底クラスではラベルに文字を設定しない。
        派生クラスでdo_actionメソッドをオーバーライトして
        self.msg_labelを設定すること。
        """
        # プログレスバーに値を設定
        self.current_count += 1
        self.progress_bar.setValue(self.current_count)

        # 予定処理数に達した？
        if self.current_count >= self.action_count:
            self._close()
        # キャンセルされた？
        if self.was_canceled:
            self._close()

        # シングルショットタイマを実行
        QTimer.singleShot(0, self.do_action)
