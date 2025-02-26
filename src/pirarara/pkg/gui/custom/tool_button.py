#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton


class PirararaToolButton(QToolButton):
    """カスタムツールボタン。

    テキストとアイコンのオプションを指定できます。

    Args:
        text (str | None): ボタンに表示するテキスト。
        icon_file_path (str | None): アイコン画像のファイルパス。
        parent (QWidget | None): 親ウィジェット。
    """

    def __init__(
        self,
        text: str | None = None,
        icon_file_path: str | None = None,
        parent=None,
    ):
        super().__init__(parent)

        if text:
            self.setText(text)

        if icon_file_path and os.path.exists(icon_file_path):
            self.setIcon(QIcon(icon_file_path))
            # ツールボタンスタイルを設定
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
