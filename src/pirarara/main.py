#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from pkg.config import AppConfig
from pkg.gui import app_run
from pkg.translation import Translate

logger = logging.getLogger(__name__)

DEBUG = True


def my_logging_setup(
    log_path: str,
    log_file: str,
    log_size: int | str,
    log_backup_count: int | str,
) -> None:
    """
    ログ設定を行います。ローテーティングファイルハンドラとストリームハンドラを使用してログを構成します。

    Args:
        log_path (str): ログファイルを作成するディレクトリへのパス。
        log_file (str): ログファイル名。
        log_size (int | str): ログファイルの最大サイズ（MB単位）。
        log_backup_count (int | str): 保存するバックアップログファイルの数。

    Returns:
        None: この関数は戻り値を持ちません。
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
    スクリプトの実行パスを取得します。

    Returns:
        str: スクリプトが実行されているディレクトリのパス。
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
    """
    アプリケーションのメインエントリーポイント。

    Returns:
        int: アプリケーションの終了ステータス。
    """
    # アプリケーション構成ファイル制御クラスを生成
    app_config = AppConfig()

    # 翻訳クラスを生成
    _ = Translate(os.path.join(os.getcwd(), "lang"))

    my_logging_setup(
        app_config.get_log_dir(), app_config.get_log_file(), 100, 4
    )

    # GUI起動
    return app_run()


if __name__ == "__main__":
    sys.exit(main())
