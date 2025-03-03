#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from pkg.metadata import MetaDataDB
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

logger = logging.getLogger(__name__)


class PirararaTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # DBファイル名
        db_file_path = os.path.join(os.getcwd(), "metadata.db")
        # DBクラスを生成
        self.db = MetaDataDB(db_file_path)

        """
        データベースのカラム情報を取得を取得してテーブルウィジェットでのカラムヘッダー定義を作る
        作成するのは辞書型で値は
        テーブルウィジェットのヘッダーに表示するテキスト。
        テーブルウィジェットに表示する際の書式。
        テーブルウィジェットで変更の可否の定義。
        をもつタプル。
        """
        db_table_columns = self.db.get_table_columns()
        self.table_widget_columns = {}
        exclude_keys = {
            "protection",
            "deletion_mark",
            "description",
            "save_dir_path",
            "file_hash_algorithm",
            "file_hash_data",
        }
        non_editable_keys = {
            "id",
            "media_type",
            "still_width",
            "still_height",
            "video_codec_name",
            "video_width",
            "video_height",
            "audio_codec_name",
            "audio_sample_rate",
            "duration",
            "file_name",
        }
        date_keys = {"updated_at", "created_at"}
        for key in db_table_columns.keys():
            if key in exclude_keys:
                continue
            if key in non_editable_keys:
                fmt = "s"
                edit = False
            elif key in date_keys:
                fmt = "%Y-%m-%d"
                edit = False
            else:
                fmt = "s"
                edit = True
            self.table_widget_columns[key] = (fmt, edit)

        # キーだけのリスト
        self.columns_keys = list(self.table_widget_columns.keys())
        # 表示内容のセットアップ
        self._setup()
        self.get_form_db()
        # 変更時のシグナルにスロット割当
        self.cellChanged.connect(self._on_changed)

    def _setup(self):
        # カラム数設定
        self.setColumnCount(len(self.columns_keys))
        # カラムヘッダ設定
        self.setHorizontalHeaderLabels(self.columns_keys)
        # 行、カラムサイズをコンテンツに応じてリサイズ
        self.resizeColumnsToContents()
        # 行選択モード
        self.setSelectionBehavior(QTableWidget.SelectRows)
        # ソートを有効に
        self.setSortingEnabled(True)
        # スタイルシート設定
        self.setStyleSheet(
            "QTableWidget { font-size: 14pt; font-weight: bold;}"
            + "QTableWidget::item:selected { background-color: #3399ff; }"
            + "QHeaderView::section { font-size: 14pt; font-weight: bold; "
            + "background-color: #333; color: white;}"
        )

    def _on_changed(self, row: int, column: int):
        # 更新するDB上のカラム名を特定
        db_column = [self.columns_keys[column]]
        # 更新するデータを取得
        item = self.item(row, column)
        if item is None:
            return
        db_value = [item.text()]
        # id
        item = self.item(row, 0)
        if item is None:
            return
        db_id = int(item.text())
        # DB上の値を更新
        self.db.update(db_id, db_column, db_value)

    def get_form_db(self):
        self.blockSignals(True)

        # 表示内容をクリア
        self.clearContents()
        self.setRowCount(0)

        # データべーースからデータを取得
        data = self.db.get_all_data()

        # データベース取得したデータを表示
        for row_index, d_item in enumerate(data):
            # 削除されたデータ？
            deletion_mark = d_item.get("deletion_mark", "0")
            if deletion_mark == "1":
                continue
            # 表示するデータ
            self.setRowCount(row_index + 1)
            for column_index, (column, items) in enumerate(
                self.table_widget_columns.items()
            ):
                fmt, edit = items
                item_value = d_item.get(column, "")

                if item_value:
                    try:
                        if fmt == "%Y-%m-%d":
                            value = datetime.strptime(
                                item_value, "%Y-%m-%d %H:%M:%S"
                            ).strftime(fmt)
                        else:
                            value = f"{item_value:{fmt}}"
                    except ValueError:
                        value = str(item_value)
                else:
                    value = ""

                cell_data = QTableWidgetItem(value)
                if not edit:
                    cell_data.setFlags(cell_data.flags() & ~Qt.ItemIsEditable)
                self.setItem(row_index, column_index, cell_data)
        self.resizeColumnsToContents()
        self.blockSignals(False)
