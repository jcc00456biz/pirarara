#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys

from my_log import my_logging_setup
from pkg.config import AppConfig
from pkg.gui import app_run

logger = logging.getLogger(__name__)

DEBUG = 1


def get_exec_path() -> str:
    """
    PyInstallerで作成されたexeがあるフォルダを取得する関数。

    Returns:
        str: exeが存在するフォルダのパス。
    """
    if DEBUG:
        exec_path = os.getcwd()
        return exec_path
    if getattr(sys, "frozen", False):
        # PyInstallerでバンドルされている場合
        exec_path = os.path.dirname(sys.executable)
    else:
        # 通常のスクリプト実行時
        exec_path = os.path.dirname(os.path.abspath(__file__))
    return exec_path


def main() -> int:
    # 先にアプリ構成ファイル制御クラスを生成
    _ = AppConfig()

    # カレントディレクトリでログファイル作成
    current_path = os.getcwd()
    my_logging_setup(current_path, "my.log", 100, 4)

    # GUI起動
    return app_run()


if __name__ == "__main__":
    sys.exit(main())
