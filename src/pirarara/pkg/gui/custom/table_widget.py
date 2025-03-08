#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import shutil
from datetime import datetime

from pkg.metadata import MetaDataDB
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

logger = logging.getLogger(__name__)


class PirararaTableWidget(QTableWidget):

    # 独自シグナル
    item_selected = Signal(int)

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
        self.cellChanged.connect(self.on_changed)
        # 選択が変わった時のシグナルにスロット割当
        self.itemSelectionChanged.connect(self.on_selection_changed)

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

    def on_changed(self, row: int, column: int):
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

    def on_selection_changed(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            db_id = int(item.text())
            break
        self.item_selected.emit(db_id)

    def get_form_db(
        self, column: str | None = None, keyword: str | None = None
    ):
        self.blockSignals(True)

        # 表示内容をクリア
        self.clearContents()
        self.setRowCount(0)

        # データべーースからデータを取得
        if not column or not keyword:
            data = self.db.get_all_data()
        elif isinstance(column, str) and isinstance(keyword, str):
            data = self.db.get_all_data_by_column(column, keyword)
        else:
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
                    cell_data.setFlags(
                        cell_data.flags() & ~Qt.ItemFlag.ItemIsEditable
                    )
                self.setItem(row_index, column_index, cell_data)
        self.resizeColumnsToContents()
        self.blockSignals(False)

    def delete_selected_items(self):
        selected_items = self.selectedItems()
        id_column_to_check = 0

        for item in selected_items:
            if item.column() == id_column_to_check:
                db_id = int(item.text())
                self.force_delete_db(db_id)

    def force_delete_db(self, id: int):
        # 対象のデータを取得
        tgt_data = self.db.get_data(id)
        if tgt_data is None:
            return
        src_folder = tgt_data.get("save_dir_path", "")
        if len(src_folder) == 0:
            return

        files = os.listdir(src_folder)
        if len(files) != 0:
            trash_box_basename = os.path.join(
                os.path.dirname(self.db.db_file_path), ".trash_box"
            )
            trash_box = self.create_timestamped_folder(trash_box_basename)
        try:
            for file in files:
                src_file = os.path.join(src_folder, file)
                base_dir = os.path.basename(src_folder)
                base_dir_sub = os.path.join(trash_box, base_dir)
                if not os.path.exists(base_dir_sub):
                    os.makedirs(base_dir_sub, exist_ok=True)
                dest_file = os.path.join(base_dir_sub, file)
                shutil.move(src_file, dest_file)
            shutil.rmtree(src_folder)
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception:
            raise Exception
        # DB内のデータ削除
        self.db.delete(id)

    def create_timestamped_folder(self, base_path: str):
        # 現在の年月日時分秒を取得
        now = datetime.now()
        folder_name = now.strftime("%Y%m%d_%H%M%S")

        # フォルダのフルパスを作成
        full_path = os.path.join(base_path, folder_name)

        # フォルダを作成
        os.makedirs(full_path, exist_ok=True)

        return full_path
