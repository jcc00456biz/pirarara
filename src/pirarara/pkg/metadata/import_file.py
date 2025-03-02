#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from .db import MetaDataDB


def get_title_from_filename(file_path: str) -> int:
    if not os.path.exists(file_path):
        return 0

    # ファイル名をタイトルで採用
    title_value = os.path.basename(file_path)

    columns = [
        "title"
    ]
    values = [
        title_value
    ]
    # DBファイル名
    db_file_path = os.path.join(os.getcwd(), "metadata.db")
    # DBクラスを生成
    db = MetaDataDB(db_file_path)
    # DBに追加
    ret_id = db.insert(columns, values)
    if ret_id is None:
        return 0
    return ret_id
