#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from pkg.config import AppConfig
from pkg.gui import app_run

logger = logging.getLogger(__name__)

DEBUG = 1


def my_logging_setup(
    log_path: str,
    log_file: str,
    log_size: int | str,
    log_backup_count: int | str,
) -> None:
    """ロギング設定を初期化する関数。

    Args:
        log_path (str): ログファイルを保存するディレクトリのパス。
        log_file (str): ログファイルの名前。
        log_size (int | str): ログファイルの最大サイズ（MB単位）。整数または文字列で指定。
        log_backup_count (int | str): ログファイルのバックアップの数。整数または文字列で指定。

    Returns:
        None
    """
    formatter = Formatter(
        "%(asctime)s : %(levelname)s : %(filename)s - %(message)s"
    )

    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    log_fname = os.path.join(log_path, log_file)

    size = int(log_size) if isinstance(log_size, (int, str)) else 100
    size *= 1024 * 1024

    backup_count = (
        int(log_backup_count)
        if isinstance(log_backup_count, (int, str))
        else 4
    )

    file_handler = RotatingFileHandler(
        log_fname,
        maxBytes=size,
        backupCount=backup_count,
        encoding="utf-8",
    )

    logging.basicConfig(
        level=logging.NOTSET, handlers=[stream_handler, file_handler]
    )


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
    app_config = AppConfig()

    my_logging_setup(
        app_config.get_log_dir(), app_config.get_log_file(), 100, 4
    )

    # GUI起動
    return app_run()


if __name__ == "__main__":
    sys.exit(main())
