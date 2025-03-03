#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.gui.PySideHelper import qfont_to_stylesheet
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QToolButton


class PirararaToolButton(QToolButton):
    """
    カスタムツールボタン。

    テキスト、アイコン、およびサブメニューのオプションを指定できます。

    Args:
        text (str | None): ボタンに表示するテキスト。
        icon (str | QIcon | None): アイコン画像のファイルパスまたはQIconオブジェクト。
        action_list (list[QAction] | None): サブメニューのアクションリスト。
        parent (QWidget | None): 親ウィジェット。
    """

    def __init__(
        self,
        text: str | None = None,
        icon: str | QIcon | None = None,
        action_list: list[QAction] | None = None,
        parent=None,
    ):
        super().__init__(parent)

        # テキストの設定
        if text:
            self.setText(text)

        # アイコンの設定
        if icon:
            if isinstance(icon, str):
                if os.path.exists(icon):
                    self.setIcon(QIcon(icon))
                    self.setToolButtonStyle(
                        Qt.ToolButtonStyle.ToolButtonTextUnderIcon
                    )
                else:
                    raise FileNotFoundError(
                        f"The specified icon file does not exist: {icon}"
                    )
            elif isinstance(icon, QIcon):
                self.setIcon(icon)
                self.setToolButtonStyle(
                    Qt.ToolButtonStyle.ToolButtonTextUnderIcon
                )
            else:
                raise TypeError(
                    "The icon argument must be of type str or QIcon"
                )
        # サブメニューの設定
        if action_list:
            if not all(isinstance(a, QAction) for a in action_list):
                raise TypeError(
                    "All elements in action_list must be of type QAction"
                )
            self._create_menu(action_list)

    def _create_menu(self, action_list: list[QAction]):
        self._menu = QMenu(self)
        stylesheet = qfont_to_stylesheet(self.font())
        self._menu.setStyleSheet(stylesheet)
        for action in action_list:
            if self.icon() is not None:
                action.setIcon(self.icon())
            self._menu.addAction(action)
        self.setMenu(self._menu)
        self.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
