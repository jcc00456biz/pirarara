#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler


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
