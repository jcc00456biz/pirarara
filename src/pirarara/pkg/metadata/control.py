#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from .db import MetaDataDB
from .hash import get_file_hash
from .media_info import get_media_info, get_media_type, is_ffmpeg_installed


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
    db_file_path = os.path.join(os.getcwd(), "metadata.db")
    # DBクラスを生成
    db = MetaDataDB(db_file_path)

    # 存在する場合はスキップ
    if db.exists("file_hash_data", file_hash_data):
        return 0

    # DBに追加
    ret_id = db.insert(columns, values)
    if ret_id is None:
        return 0
    return ret_id
