#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

from pkg.metadata import MetaDataDB
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem

logger = logging.getLogger(__name__)


class PirararaTreeWidget(QTreeWidget):

    INIT_ADJUST_DISPLAY_CHARS = 4
    INIT_ADJUST_DISPLAY_DIGITS = 4

    # カラムヘッダー
    COLUMN_HEADER = [
        "TAG".ljust(INIT_ADJUST_DISPLAY_CHARS),
        "PCS".rjust(INIT_ADJUST_DISPLAY_DIGITS),
    ]
    COLUMN_HEADER_LEN = len(COLUMN_HEADER)

    def __init__(self, parent=None):
        super().__init__(parent)

        # DBファイル名
        db_file_path = os.path.join(os.getcwd(), "metadata.db")
        # DBクラスを生成
        self.db = MetaDataDB(db_file_path)

        self.columns = [
            "author",
            "brand",
            "category",
            "club",
            "company",
            "publisher",
        ]

        # 選択した子アイテムインデックス
        self._selected_child_item_index = -1

        # カラム設定
        self._setup()

        # スロットを接続
        # self.itemSelectionChanged.connect(self.on_item_selection_changed)

        # 全アイテム展開
        self.expandAll()

    def _setup(self):
        # テーブルヘッダ構築
        # カラム数
        self.setColumnCount(self.__class__.COLUMN_HEADER_LEN)
        # カラムヘッダ
        self.setHeaderLabels(self.__class__.COLUMN_HEADER)
        # カラムのリサイズ設定
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        # ヘッダ非表示
        self.setHeaderHidden(True)
        # スタイルシート設定
        self.setStyleSheet(
            """
            QTreeView {
                font-size: 14pt;
                border: none;
                padding: 0;
                outline: none;
            }
            QTreeView::item {
                border: none;
                padding: 0;
                outline: none;
            }
            QTreeView::item:hover {
                border: none;
                padding: 0;
                outline: none;
                background-color: lightblue;
                color: black;
            }
            QTreeView::item:selected {
                border: none;
                padding: 0;
                outline: none;
                background-color: #3399ff;
                color: black;
            }
            """
        )
        # 表示内容を構築
        for c in self.columns:
            item_data = self.db.get_count(c, c)
            if item_data is not None:
                for index, dat in enumerate(item_data):
                    text_list = [
                        dat[0],
                        str(dat[1]),
                    ]
                    # 親アイテム
                    if index == 0:
                        parent_item = QTreeWidgetItem(text_list)
                        parent_item.setTextAlignment(
                            0, Qt.AlignmentFlag.AlignLeft
                        )
                        parent_item.setTextAlignment(
                            1, Qt.AlignmentFlag.AlignRight
                        )
                        self.addTopLevelItem(parent_item)
                        self.resize_me()

                    else:
                        # 子アイテム
                        child_item = QTreeWidgetItem(text_list)
                        child_item.setTextAlignment(
                            0, Qt.AlignmentFlag.AlignLeft
                        )
                        child_item.setTextAlignment(
                            1, Qt.AlignmentFlag.AlignRight
                        )
                        parent_item.addChild(child_item)
                        self.resize_me()

    def resize_me(self):
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
