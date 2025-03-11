#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

logger = logging.getLogger(__name__)


class PirararaComboBox(QComboBox):
    """
    カスタムコンボボックスクラス。

    履歴機能を備えた編集可能なコンボボックスで、新しい項目が追加されるたびに独自シグナルを発信します。
    """

    # 新しいアイテムが編集されたときに発信されるシグナル。編集されたテキストを渡します。
    item_edited = Signal(str)

    # 記憶する履歴の最大数。
    HISTORY_COUNT = 10

    def __init__(self, parent=None, history: int | None = None):
        """
        コンストラクタ。

        コンボボックスを初期化し、スタイルの設定や編集終了イベントのハンドラを設定します。

        Args:
            parent (QObject, optional): 親ウィジェット。デフォルトはNone。
            history (int | None, optional): 記憶する履歴数。指定がない場合はデフォルト値。
        """
        super().__init__(parent)

        # 編集可能とする
        self.setEditable(True)

        # スタイル設定
        self._setup()

        # イベントハンドラを設定
        self.line_edit = self.lineEdit()
        if self.line_edit is not None:
            self.line_edit.editingFinished.connect(self.on_editing_finished)

    def _setup(self):
        """
        コンボボックスのスタイルを設定します。

        Returns:
            None
        """
        self.setStyleSheet(
            """
            QComboBox {
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                font-size: 14px;
            }
            """
        )

    def on_editing_finished(self):
        """
        編集が終了した際に呼び出されるイベントハンドラ。

        新しいアイテムを履歴に追加し、必要に応じて古いアイテムを削除します。
        また、独自シグナル `item_edited` を発信します。

        Returns:
            None
        """
        new_text = self.currentText()
        if new_text not in [self.itemText(i) for i in range(self.count())]:
            if self.count() >= self.__class__.HISTORY_COUNT:
                # 古いアイテムのテキスト
                old_text = self.itemText(0)
                # 古いアイテムを削除
                self.removeItem(0)
                logger.info(f"remove item {old_text}")
            # 新しいアイテム追加
            self.addItem(new_text)
            logger.info(f"add new item {new_text}")

        # 独自シグナルを発信
        logger.info(f"New item {new_text}")
        self.item_edited.emit(new_text)
