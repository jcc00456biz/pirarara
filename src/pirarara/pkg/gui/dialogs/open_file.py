#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.const import __appname__, __version__
from PySide6.QtWidgets import QFileDialog


class OpenFileDialog(QFileDialog):
    """
    ファイルオープン用のカスタムダイアログクラス。

    既存のファイルを選択するダイアログを提供します。
    """

    def __init__(self, parent=None):
        """
        コンストラクタ。

        ダイアログのタイトル、ファイルモード、初期ディレクトリを設定します。

        Args:
            parent (QObject, optional): 親ウィジェット。デフォルトはNone。
        """
        super().__init__(parent)

        # 画面タイトルの設定
        self.setWindowTitle(f"{__appname__} {__version__}")

        # ファイル選択モードを設定します
        self.setFileMode(QFileDialog.FileMode.ExistingFiles)

        # カレントディレクトリを初期ディレクトリに設定します
        self.setDirectory(os.getcwd())

    def get_selected_file(self):
        """
        ユーザーが選択したファイルを取得します。

        ダイアログが実行され、ファイルが選択された場合にそのファイルパスを返します。

        Returns:
            list[str] | None: 選択されたファイルのリスト。何も選択されなかった場合はNoneを返します。
        """
        if self.exec():
            return self.selectedFiles()
        return None
