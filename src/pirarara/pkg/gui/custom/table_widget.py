#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import shutil
from datetime import datetime

from pkg.config import AppConfig
from pkg.metadata import MetaDataDB
from pkg.translation import Translate
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

logger = logging.getLogger(__name__)


class PirararaTableWidget(QTableWidget):
    """
    カスタムテーブルウィジェットクラス。

    データベースの情報を表示・編集し、選択や変更時に独自シグナルを発信します。
    """

    # アイテムが選択された際に発信されるシグナル。選択された項目のデータベースIDを渡します。
    item_selected = Signal(int)
    # アイテムが変更された際に発信されるシグナル。
    item_changed = Signal()

    def __init__(self, parent=None):
        """
        コンストラクタ。

        テーブルウィジェットを初期化し、データベース接続やカラム情報を設定します。

        Args:
            parent (QObject, optional): 親ウィジェット。デフォルトはNone。
        """
        super().__init__(parent)

        # 構成情報からDBファイル名取得
        app_config = AppConfig()
        db_file_path = app_config.get_db_path()
        # DBクラスを生成
        self.db = MetaDataDB(db_file_path)

        # 翻訳クラスを生成
        self.tr = Translate()

        # テーブルウィジェットのカラム定義を設定
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

        # キーのリストを設定
        self.columns_keys = list(self.table_widget_columns.keys())
        # 翻訳したものを用意
        self.columns_tr_keys = []
        for k in self.table_widget_columns.keys():
            self.columns_tr_keys.append(self.tr.tr(self.__class__.__name__, k))

        # テーブルの初期セットアップ
        self._setup()
        # データベースからデータを取得して設定
        self.get_form_db()
        # シグナルとスロットを接続
        self.cellChanged.connect(self.on_changed)
        self.itemSelectionChanged.connect(self.on_selection_changed)

    def _setup(self):
        """
        テーブルウィジェットの初期スタイルと設定を適用します。

        Returns:
            None
        """
        self.setColumnCount(len(self.columns_tr_keys))
        self.setHorizontalHeaderLabels(self.columns_tr_keys)
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSortingEnabled(True)
        self.setStyleSheet(
            "QTableWidget { font-size: 14pt; font-weight: bold;}"
            + "QTableWidget::item:selected { background-color: #3399ff; }"
            + "QHeaderView::section { font-size: 14pt; font-weight: bold; "
            + "background-color: #333; color: white;}"
        )

    def on_changed(self, row: int, column: int):
        """
        セルが変更されたときに呼び出されるスロット。

        データベースの該当する値を更新します。

        Args:
            row (int): 変更されたセルの行番号。
            column (int): 変更されたセルの列番号。

        Returns:
            None
        """
        db_column = [self.columns_keys[column]]
        item = self.item(row, column)
        if item is None:
            return
        db_value = [item.text()]
        item = self.item(row, 0)
        if item is None:
            return
        db_id = int(item.text())
        self.db.update(db_id, db_column, db_value)
        self.item_changed.emit()

    def on_selection_changed(self):
        """
        アイテムが選択されたときに呼び出されるスロット。

        選択されたアイテムのデータベースIDを独自シグナル `item_selected` として発信します。

        Returns:
            None
        """
        selected_items = self.selectedItems()
        for item in selected_items:
            db_id = int(item.text())
            if db_id > 0:
                self.item_selected.emit(db_id)
            break

    def get_form_db(
        self, column: str | None = None, keyword: str | None = None
    ):
        """
        データベースからデータを取得してテーブルに表示します。

        Args:
            column (str | None, optional): 検索対象のカラム名。デフォルトはNone。
            keyword (str | None, optional): 検索キーワード。デフォルトはNone。

        Returns:
            None
        """
        self.blockSignals(True)
        self.clearContents()
        self.setRowCount(0)

        if not column or not keyword:
            data = self.db.get_all_data()
        elif isinstance(column, str) and isinstance(keyword, str):
            data = self.db.get_all_data_by_column(column, keyword)
        else:
            data = self.db.get_all_data()

        for row_index, d_item in enumerate(data):
            deletion_mark = d_item.get("deletion_mark", "0")
            if deletion_mark == "1":
                continue
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
        """
        選択されたアイテムをデータベースから削除します。

        Returns:
            None
        """
        selected_items = self.selectedItems()
        id_column_to_check = 0
        for item in selected_items:
            if item.column() == id_column_to_check:
                db_id = int(item.text())
                self.force_delete_db(db_id)

    def force_delete_db(self, id: int):
        """
        指定したIDのデータを強制的に削除します。

        Args:
            id (int): 削除対象のデータベースID。

        Returns:
            None
        """
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
        self.db.delete(id)

    def create_timestamped_folder(self, base_path: str) -> str:
        """
        タイムスタンプ付きのフォルダを作成します。

        Args:
            base_path (str): ベースとなるフォルダのパス。

        Returns:
            str: 作成されたフォルダのフルパス。
        """
        now = datetime.now()
        folder_name = now.strftime("%Y%m%d_%H%M%S")
        full_path = os.path.join(base_path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        return full_path
