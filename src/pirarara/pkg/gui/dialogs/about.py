#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import os

from pkg.const import __appname__, __version__
from pkg.translation import Translate
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCloseEvent, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel


class AboutDialog(QDialog):
    """
    アプリケーションの情報を表示するダイアログクラス。

    Args:
        parent (QWidget, optional): 親ウィジェット。デフォルトはNone。
    """

    def __init__(self, parent=None):
        """
        AboutDialogクラスのコンストラクタ。

        Args:
            parent (QWidget, optional): 親ウィジェット。デフォルトはNone。
        """

        super().__init__(parent)

        # 翻訳クラスを生成
        self.tr = Translate()

        # 画面タイトルの設定
        self.setWindowTitle(f"{__appname__} {__version__}")

        # ウインドウサイズ
        self.setFixedSize(QSize(380, 120))

        # ベースのレイアウト
        self.formLayout = QFormLayout(self)

        # 表示するアイコン
        self.app_icon = QLabel(self)
        self.app_icon.setText("")
        icon_dir = os.path.join(os.getcwd(), "icon")
        icon_file = os.path.join(icon_dir, "pirarara.svg")
        if os.path.exists(icon_file):
            pixmap = self.renderer_svg(icon_file, 64)
            self.app_icon.setPixmap(pixmap)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.app_icon)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.buttonBox)

        self.about_text = QLabel(self)
        self.about_text.setTextFormat(Qt.TextFormat.PlainText)
        self.about_text.setWordWrap(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.about_text)

        # シグナルにスロットを接続
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # 表示する文言
        description = f"{__appname__} {__version__}"
        description += "\n"
        description += self.tr.tr(
            self.__class__.__name__, "pirarara Multimedia Content Manager."
        )
        self.about_text.setText(description)

    def closeEvent(self, event: QCloseEvent):
        """
        ウィンドウが閉じられたときのイベントハンドラ。

        Args:
            event (QCloseEvent): ウィンドウが閉じられるイベント。
        """
        gc.collect()
        event.accept()

    def renderer_svg(self, file_path: str, size: int) -> QPixmap:
        """
        SVGファイルを指定されたサイズのQPixmapにレンダリングする。

        Args:
            file_path (str): SVGファイルのパス。
            size (int): レンダリングするサイズ。

        Returns:
            QPixmap: レンダリングされたQPixmapオブジェクト。
        """
        renderer = QSvgRenderer(file_path)
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap
