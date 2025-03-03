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

    def get_table_columns(self) -> dict:
        """
        データベースのテーブルカラム情報を返します。

        Returns:
            dict: カラム定義情報
        """
        return self.table_columns

    def insert(self, columns: list, values: list) -> int | None:
        """
        指定されたカラムと値を使用してデータベースに新しいレコードを挿入します。

        Args:
            columns (list): 挿入するカラムのリスト。
            values (list): 挿入する値のリスト。各値の型は対応するカラムの型と一致する必要があります。

        Raises:
            TypeError: `columns`または`values`がリストでない場合、または各値の型がカラムの型と一致しない場合。
            ValueError: `columns`と`values`の長さが一致しない場合、または`columns`に無効な値が
            含まれている場合。

        Returns:
            int | None: 挿入された行のID。挿入が失敗した場合は`None`。
        """
        if not isinstance(columns, list):
            raise TypeError("columns must be of type list")
        if not isinstance(values, list):
            raise TypeError("values must be of type list")
        if len(columns) != len(values):
            raise ValueError("columns and number of values do not match")
        if not all(item in self.table_columns for item in columns):
            raise ValueError("columns contains invalid values")
        for index, c in enumerate(columns):
            t = self.table_columns[c]
            if "INTEGER" in t:
                if not isinstance(values[index], int):
                    raise TypeError("values must be of type int")
            if "TEXT" in t:
                if not isinstance(values[index], str):
                    raise TypeError("values must be of type str")

        sql_values = ", ".join(["?" for _ in values])
        sql = (
            f"INSERT INTO {self.table_name} "
            + f"({', '.join(columns)}) VALUES ({sql_values});"
        )

        with sqlite3.connect(self.db_file_path, isolation_level=None) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(values))
            return cursor.lastrowid

    def update(self, id: int, columns: list, values: list) -> None:
        """
        指定されたIDを持つレコードを更新します。

        Args:
            id (int): 更新する行のID。
            columns (list): 更新するカラムのリスト。
            values (list): 更新する値のリスト。各値の型は対応するカラムの型と一致する必要があります。

        Raises:
            TypeError: `id` が整数型でない場合、`columns` または `values` が
            リストでない場合、または各値の型がカラムの型と一致しない場合。
            ValueError: `columns` と `values` の長さが一致しない場合、
            または `columns` に無効な値が含まれている場合。

        Returns:
            None
        """
        if not isinstance(id, int):
            raise TypeError("id must be of type int")
        if not isinstance(columns, list):
            raise TypeError("columns must be of type list")
        if not isinstance(values, list):
            raise TypeError("values must be of type list")
        if len(columns) != len(values):
            raise ValueError("columns and number of values do not match")
        if not all(item in self.table_columns for item in columns):
            raise ValueError("columns contains invalid values")
        for index, c in enumerate(columns):
            t = self.table_columns[c]
            if "INTEGER" in t:
                if not isinstance(values[index], int):
                    raise TypeError("values must be of type int")
            if "TEXT" in t:
                if not isinstance(values[index], str):
                    raise TypeError("values must be of type str")

        wk_columns = [f"{c}=?" for c in columns]
        wk_values = values + [id]

        sql = (
            f"UPDATE {self.table_name} "
            + f"SET {','.join(wk_columns)} "
            + "WHERE id=?;"
        )
        with sqlite3.connect(self.db_file_path, isolation_level=None) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(wk_values))

    def delete(self, id: int) -> None:
        """
        指定されたIDに基づいてテーブルからレコードを削除するメソッド。
        削除後テーブルにデータが存在しなくなった場合に自動更新値をリセットする

        Args:
            db_id (int): 対象の一意の識別子。
        """
        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT protection FROM {self.table_name} WHERE id=?;", (id,)
            )
            result = cursor.fetchone()
        if result and result[0] == 1:
            return

        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id=?;", (id,))

        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            row_count = cursor.fetchone()[0]

        if row_count == 0:
            with sqlite3.connect(self.db_file_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM sqlite_sequence WHERE name=?;",
                    (f"{self.table_name}",),
                )

    def get_data(self, id: int) -> dict | None:
        """
        指定されたIDに基づいてテーブルからレコードを取得するメソッド。

        Args:
            db_id (int): データを取得する対象の一意の識別子。

        Returns:
            dict | None: 取得したデータを格納した辞書。データが存在しない場合はNone。

        このメソッドは、指定されたIDに基づいてデータベース内の特定のテーブルからデータを取得します。
        まず、テーブルの構造情報を取得し、その後、IDに基づいてデータを選択します。
        取得したデータが存在しない場合はNoneを返します。存在する場合は、テーブルの列名をキーとして
        データを辞書形式で返します。
        """
        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA TABLE_INFO ({self.table_name});")
            table_columns = cursor.fetchall()
            cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE id=?;", (id,)
            )
            data = cursor.fetchone()

        if data is None:
            return None

        ret_data = {}
        for index, col in enumerate(table_columns):
            ret_data[col[1]] = data[index]

        return ret_data

    def get_all_data(self) -> list | None:
        """
        データベースからすべてのデータを取得し、フォーマットされたリストを返します。

        このメソッドは、指定されたデータベースファイルとテーブルからすべてのデータを取得し、
        各レコードを辞書としてフォーマットし、それらの辞書をリストとして返します。

        Returns:
            list | None: データベースから取得したデータのリスト。
            データが存在しない場合はNoneを返します。

        Raises:
            sqlite3.Error: データベース操作中にエラーが発生した場合。
        """
        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA TABLE_INFO ({self.table_name});")
            table_columns = cursor.fetchall()
            cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY id ASC;")
            data = cursor.fetchall()

        if data is None:
            return None

        ret_data = []
        for d in data:
            dict_data = {}
            for index, col in enumerate(table_columns):
                if isinstance(d[index], str):
                    dict_data[col[1]] = d[index]
                if isinstance(d[index], int):
                    dict_data[col[1]] = str(d[index])
            ret_data.append(dict_data)
        return ret_data

    def exists(self, column: str, check_data: str) -> bool:
        """
        指定されたカラムに特定のデータが存在するかを確認するメソッド。

        Args:
            column (str): 検索対象のカラム名。
            check_data (str): 検索するデータ。

        Returns:
            bool: データが存在する場合はTrue、存在しない場合はFalse。
        """
        # 指定のカラムから検索する
        sql = f"SELECT * FROM {self.table_name} " + f"WHERE {column}=?;"

        with sqlite3.connect(self.db_file_path, isolation_level=None) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (check_data,))
            data = cursor.fetchone()

        return data is not None

    def get_count(self, total_text: str, column: str) -> list | None:
        """
        指定されたcolumnに基づいてテーブルからデータ数を取得するメソッド。

        Args:
            column (str): データ数を集計するカラム名。

        Returns:
            list | None: 取得したデータを格納したリスト。データが存在しない場合はNone。

        取得したデータは初めはレコード全体の数。
        2つ目の要素以降にソートされたデータの個数が並ぶ。
        データはすべて文字列型となる。
        """
        # 各要素の個数を取得
        sql = (
            f"SELECT {column}, COUNT(*) FROM {self.table_name} "
            + "WHERE (deletion_mark IS NULL OR deletion_mark != 1) AND "
            + f"{column} IS NOT NULL AND {column}!='' "
            + f"GROUP BY {column} "
            + f"ORDER BY {column} ASC;"
        )

        data = []
        with sqlite3.connect(self.db_file_path, isolation_level=None) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()

        total_count = 0
        ret_data: list[tuple[str, int]] = []
        if data is not None:
            for items in data:
                if (
                    isinstance(items, tuple)
                    and len(items) == 2
                    and isinstance(items[0], str)
                    and isinstance(items[1], int)
                ):
                    ret_data.append((items[0], items[1]))
                    total_count += items[1]

        ret_data.insert(0, (total_text, total_count))
        return ret_data
