#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

from pkg.gui.PySideHelper import qfont_to_stylesheet
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QToolButton

logger = logging.getLogger(__name__)


class PirararaToolButton(QToolButton):
    """
    カスタムツールボタンクラス。

    テキスト、アイコン、サブメニューを設定可能なツールボタンを作成します。
    """

    def __init__(
        self,
        text: str | None = None,
        icon: str | QIcon | None = None,
        action_list: list[QAction] | None = None,
        parent=None,
    ):
        """
        コンストラクタ。

        ツールボタンを初期化し、テキスト、アイコン、サブメニューを設定します。

        Args:
            text (str | None, optional): ボタンに表示するテキスト。デフォルトはNone。
            icon (str | QIcon | None, optional): ボタンに表示するアイコン。
            文字列（パス）またはQIconインスタンスを指定可能。デフォルトはNone。
            action_list (list[QAction] | None, optional): サブメニューに追加する
            QActionのリスト。デフォルトはNone。
            parent (QObject, optional): 親ウィジェット。デフォルトはNone。

        Raises:
            FileNotFoundError: 指定されたアイコンファイルが存在しない場合に発生。
            TypeError: `icon`引数が`str`または`QIcon`型以外の場合、または`action_list`内の
            要素が全て`QAction`型でない場合に発生。
        """
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
        """
        サブメニューを作成し、ツールボタンに追加します。

        Args:
            action_list (list[QAction]): サブメニューに追加するQActionのリスト。

        Returns:
            None
        """
        self._menu = QMenu(self)
        stylesheet = qfont_to_stylesheet(self.font())
        self._menu.setStyleSheet(stylesheet)
        for action in action_list:
            if self.icon() is not None:
                action.setIcon(self.icon())
            self._menu.addAction(action)
        self.setMenu(self._menu)
        self.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
