#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pkg.const import __appname__, __version__
from PySide6.QtWidgets import QFileDialog


class ImportFileDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 画面タイトルの設定
        self.setWindowTitle(f"{__appname__} {__version__}")

        # ファイル選択モードを設定します。
        self.setFileMode(QFileDialog.FileMode.ExistingFile)

        # カレントディレクトリを初期ディレクトリに設定します。
        self.setDirectory(os.getcwd())

    def get_selected_file(self):

        if self.exec():
            return self.selectedFiles()
        return None
