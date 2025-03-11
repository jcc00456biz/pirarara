#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import shutil

from pkg.config import AppConfig
from .db import MetaDataDB
from .hash import get_file_hash
from .media_info import (
    capture_frame,
    get_media_info,
    get_media_type,
    is_ffmpeg_installed,
)

logger = logging.getLogger(__name__)


def set_media_info(file_path: str) -> int:
    # 動画以外は処理しなし
    if get_media_type(file_path) != "movie":
        return 0

    # FFmpegのインストール確認
    if not is_ffmpeg_installed():
        return 0

    # メディア情報を取得
    file_hash_data = get_file_hash(file_path)
    media_info = get_media_info(file_path, file_hash_data)
    # 辞書をリストに変換
    columns = list(media_info.keys())
    values = list(media_info.values())

    # DBファイル名
    app_config = AppConfig()
    db_file_path = app_config.get_db_path()
    # DBクラスを生成
    db = MetaDataDB(db_file_path)

    # 存在する場合はスキップ
    if db.exists("file_hash_data", file_hash_data):
        return 0

    # DBに追加
    ret_id = db.insert(columns, values)
    if ret_id is None:
        return 0

    # 保存先ディレクトリ作成
    save_dir = os.path.dirname(db_file_path)
    save_path = os.path.join(save_dir, f"id{ret_id}")
    os.makedirs(save_path, exist_ok=True)

    # 動画から静止画をキャプチャ
    capture_file_path = os.path.join(save_path, "capture.jpg")
    if capture_frame(file_path, capture_file_path):
        copy_file_to_directory(file_path, save_path)

    # インポートした先のフォルダ、ファイル名をDBに登録
    update_columns = [
        "save_dir_path",
        "file_name",
    ]
    update_values = [save_path, os.path.basename(file_path)]
    db.update(ret_id, update_columns, update_values)

    return ret_id


def copy_file_to_directory(src_file_path, dest_directory) -> bool:
    try:
        # 目的ディレクトリが存在しない場合は作成
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory, exist_ok=True)

        # 目的ディレクトリのパスにファイル名を追加
        dest_file_path = os.path.join(
            dest_directory, os.path.basename(src_file_path)
        )

        # ファイルをコピー
        shutil.copy(src_file_path, dest_file_path)
        return True
    except Exception as e:
        logger.error(f"Error copy file: {e}")
        return False
