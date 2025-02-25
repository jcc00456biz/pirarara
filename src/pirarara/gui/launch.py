#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

from .gmain import MWindow


def app_run() -> int:
    """
    アプリケーションを実行する関数。

    この関数はQApplicationを初期化し、メインウィンドウを作成して表示します。

    Args:
        app_config (AppConfig): アプリケーションの設定を含むAppConfigオブジェクト。

    Returns:
        int: アプリケーションの終了コード。
    """
    app = QApplication(sys.argv)
    _ = MWindow()
    return app.exec()
