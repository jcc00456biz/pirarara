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

    def __init__(
        self,
        name_filters: list | None = None,
        file_mode: QFileDialog.FileMode | None = None,
        parent=None,
    ):
        """
        コンストラクタ。

        ダイアログのタイトル、ファイルモード、初期ディレクトリを設定します。

        Args:
            name_filters (QObject, optional): ファイルフィルタ。デフォルトはNone。
            file_mode (QObject, optional): ファイルモード。デフォルトはNone。
            parent (QObject, optional): 親ウィジェット。デフォルトはNone。
        """
        super().__init__(parent)

        # 画面タイトルの設定
        self.setWindowTitle(f"{__appname__} {__version__}")

        # ファイルフィルタの設定
        if isinstance(name_filters, list):
            self.setNameFilters(name_filters)

        # ファイル選択モードを設定します
        if file_mode is None:
            self.setFileMode(QFileDialog.FileMode.ExistingFiles)
        else:
            self.setFileMode(file_mode)

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
