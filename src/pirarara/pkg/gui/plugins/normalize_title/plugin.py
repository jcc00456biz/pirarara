#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkg.config import AppConfig
from pkg.gui.plugins import PirararaBasePlugin
from pkg.metadata import MetaDataDB


class NormalizeTitle(PirararaBasePlugin):
    def __init__(self, selected_items: list):
        if not isinstance(selected_items, list):
            raise TypeError("The parameters must be list type")

        self.action_counts = len(selected_items)
        if self.action_counts == 0:
            raise ValueError("There are no valid values")

        # 構成情報からDBクラスインスタンスを取得
        self.db = MetaDataDB(AppConfig().get_db_path())

        """
        処理するアイテムリストの中身は
        IDとTitleをリストにもつネストしたリスト
        """
        self.selected_items = selected_items

        super().__init__(self.selected_items)

    def do_action(self):
        item = self.selected_items[self.current_count]
        if isinstance(item, list):
            current_id = item[0]
            title = item[1]

            self.msg_label.setText(title)

            columns = ["title"]
            values = [self.normalize(title)]
            self.db.update(current_id, columns, values)

        super().do_action()
