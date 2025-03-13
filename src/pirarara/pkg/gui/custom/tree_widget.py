#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from pkg.config import AppConfig
from pkg.metadata import MetaDataDB
from pkg.translation import Translate
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem

logger = logging.getLogger(__name__)


class PirararaTreeWidget(QTreeWidget):
    """
    データベース情報を表示するカスタムツリーウィジェットクラス。

    親子関係のデータをツリー形式で表示し、アイテム選択やダブルクリック時に独自シグナルを発信します。
    """

    # 選択されたアイテムとその親アイテムのテキストを渡すシグナル。
    item_selected = Signal(str, str)

    # 初期表示で文字を調整する際の文字数。
    INIT_ADJUST_DISPLAY_CHARS = 4
    # 初期表示で数値を調整する際の桁数。
    INIT_ADJUST_DISPLAY_DIGITS = 4

    # ツリーウィジェットのカラムヘッダー名リスト。
    COLUMN_HEADER = [
        "TAG".ljust(INIT_ADJUST_DISPLAY_CHARS),
        "PCS".rjust(INIT_ADJUST_DISPLAY_DIGITS),
    ]
    # ツリーウィジェットのカラム数。
    COLUMN_HEADER_LEN = len(COLUMN_HEADER)

    def __init__(self, parent=None):
        """
        コンストラクタ。

        ツリーウィジェットを初期化し、データベースからデータを取得して表示します。

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

        # 全アイテム展開
        self.expandAll()

        # スロットを接続
        self.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)

    def _setup(self):
        """
        ツリーウィジェットをセットアップし、データベース情報を表示します。

        Returns:
            None
        """
        self.setColumnCount(self.__class__.COLUMN_HEADER_LEN)
        self.setHeaderLabels(self.__class__.COLUMN_HEADER)
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.setHeaderHidden(True)
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
        for c in self.columns:
            item_data = self.db.get_count(c, c)
            if item_data is not None:
                for index, dat in enumerate(item_data):
                    text_list = [
                        self.tr.tr(self.__class__.__name__, dat[0]),
                        str(dat[1]),
                    ]
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
        """
        カラムの幅を内容に合わせて調整します。

        Returns:
            None
        """
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

    def on_item_selection_changed(self):
        """
        アイテムが選択されたときに呼び出されるメソッド。

        選択されたアイテムのテキストと親アイテムのテキストを取得し、独自シグナルを送信します。

        Returns:
            None
        """
        selected_items = self.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            parent_item = selected_item.parent()
            if parent_item is None:
                index = self.indexOfTopLevelItem(selected_item)
                signal_parent_text = self.columns[index]
                column_text = ""
            else:
                index = self.indexOfTopLevelItem(parent_item)
                signal_parent_text = self.columns[index]
                column_text = selected_item.text(0)
            logger.info(f"{signal_parent_text} {column_text}")
            self.item_selected.emit(column_text, signal_parent_text)

    def on_item_double_clicked(self, item, column):
        """
        アイテムがダブルクリックされたときに処理を実行する。

        指定されたアイテムの選択を解除し、独自のシグナルを発信します。
        主にアイテム選択解除とシグナルの通知を行います。

        Args:
            item (QTreeWidgetItem): ダブルクリックされたアイテム。
            column (int): ダブルクリックされたカラムのインデックス。

        Returns:
            None
        """
        item.setSelected(False)
        # 独自シグナルを発信
        logger.info(f"on_item_double_clicked: {column}")
        self.item_selected.emit("", "")

    def refresh_display(self):
        """
        表示内容をリフレッシュする。

        現在のウィジェットの内容をクリアし、再設定を行います。
        主にビューやデータの更新に使用されます。

        Returns:
            None
        """
        self.clear()
        self._setup()
        self.expandAll()
