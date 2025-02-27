#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import os
import sqlite3


class MetaDataDB:
    """
    データベースへの接続とメタデータテーブルの操作を管理するクラス。

    Attributes:
        db_file_path (str): データベースファイルのパス。
        table_name (str): テーブル名。
        table_columns (dict): テーブルカラムの定義を格納する辞書。
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        シングルトンインスタンスを生成するメソッド。

        Returns:
            MetaDataDB: MetaDataDBクラスの唯一のインスタンス。
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_file_path: str | None = None):
        """
        MetaDataDBクラスの初期化メソッド。

        Args:
            db_file_path (str): データベースファイルのパス。
        """
        if not hasattr(self, "_initialized"):
            if db_file_path is None:
                raise ValueError("Invalid value")
            self._initialized = True
        else:
            return

        # DBファイル
        self.db_file_path = db_file_path
        # テーブル名
        # self.table_name = self.__class__.__name__
        self.table_name = "MetaDataTbl"

        # テーブルカラム定義
        self.table_columns = {
            "id": "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
            "protection": "INTEGER",
            "deletion_mark": "INTEGER",
            #
            "title": "TEXT",
            #
            "author": "TEXT",
            "series": "TEXT",
            "series_index": "TEXT",
            "category": "TEXT",
            #
            "brand": "TEXT",
            "publisher": "TEXT",
            "company": "TEXT",
            "club": "TEXT",
            #
            "description": "TEXT",
            "release_date": "TEXT",
            "price": "TEXT",
            "product_number": "TEXT",
            "jancode": "TEXT",
            #
            "media_type": "TEXT",
            #
            "rating": "TEXT",
            #
            "still_width": "TEXT",
            "still_height": "TEXT",
            #
            "video_codec_name": "TEXT",
            "video_width": "TEXT",
            "video_height": "TEXT",
            #
            "audio_codec_name": "TEXT",
            "audio_sample_rate": "TEXT",
            #
            "duration": "TEXT",
            #
            "save_dir_path": "TEXT",
            "file_name": "TEXT",
            "file_hash_algorithm": "TEXT",
            "file_hash_data": "TEXT",
            #
            "updated_at": (
                "TEXT NOT NULL " "DEFAULT (DATETIME('now', 'localtime'))"
            ),
            "created_at": (
                "TEXT NOT NULL " "DEFAULT (DATETIME('now', 'localtime'))"
            ),
        }

        # テーブルが存在しない場合は作成
        if not os.path.exists(self.db_file_path) or not self._table_exists():
            self._create_table()

    def _table_exists(self) -> bool:
        """
        テーブルがデータベースに存在するかを確認するメソッド。

        Returns:
            bool: テーブルが存在する場合はTrue、存在しない場合はFalse。
        """
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (self.table_name,))
            result = cursor.fetchone()
            return result is not None

    def _create_table(self) -> None:
        """
        テーブルを生成するメソッド。
        """
        columns = ", ".join(
            [
                f"{col} {attributes}"
                for col, attributes in self.table_columns.items()
            ]
        )
        sql = (
            f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns});\n"
            + "CREATE TRIGGER IF NOT EXISTS trigger_updated_at "
            + f"AFTER UPDATE ON {self.table_name} "
            + "BEGIN "
            + f"UPDATE {self.table_name} SET updated_at = "
            + "DATETIME('now', 'localtime') WHERE rowid = NEW.rowid; "
            + "END;"
        )
        with sqlite3.connect(self.db_file_path, isolation_level=None) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql)

        gc.collect()
