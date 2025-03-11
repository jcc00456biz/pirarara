#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

from pkg.config import AppConfig
from pkg.metadata import MetaDataDB
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
)

logger = logging.getLogger(__name__)


class PirararaImageViewer(QGraphicsView):
    """
    画像表示機能を提供するカスタムQGraphicsViewクラス。

    データベースに保存された情報をもとに画像を読み込み、QGraphicsView上に表示します。
    """

    def __init__(self, parent=None):
        """
        コンストラクタ。

        画像表示ビューを初期化し、データベースとグラフィックスシーンをセットアップします。

        Args:
            parent (QObject, optional): 親ウィジェット。デフォルトはNone。
        """
        super().__init__(parent)

        # 構成情報からDBファイル名取得
        app_config = AppConfig()
        db_file_path = app_config.get_db_path()
        # DBクラスを生成
        self.db = MetaDataDB(db_file_path)

        self.graphics_scene = QGraphicsScene()
        self.setScene(self.graphics_scene)
        self.image_item = None

    def show_image(self, db_id: int):
        """
        指定されたデータベースIDに基づいて画像を表示します。

        データベースから画像データを取得し、QGraphicsViewに追加します。

        Args:
            db_id (int): 画像データを取得するためのデータベースID。

        Returns:
            None
        """
        self.graphics_scene.clear()

        data = self.db.get_data(db_id)
        if data is not None:
            img_dir = data.get("save_dir_path", "")
            if img_dir:
                img_path = os.path.join(img_dir, "capture.jpg")
                pixmap = QPixmap(img_path)
                self.image_item = QGraphicsPixmapItem(pixmap)
                self.graphics_scene.addItem(self.image_item)
                self.setSceneRect(pixmap.rect())
                self.fit_in_view()

    def clear_image(self):
        """
        表示中の画像をクリアします。

        Returns:
            None
        """
        self.graphics_scene.clear()

    def fit_in_view(self):
        """
        現在表示中の画像をビュー内に収まるようにスケール調整します。

        Returns:
            None
        """
        if self.image_item is not None:
            rect = self.image_item.boundingRect()
            self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        """
        ウィジェットのリサイズイベントを処理します。

        ウィジェットのサイズ変更時に画像の表示を調整します。

        Args:
            event (QResizeEvent): リサイズイベント。

        Returns:
            None
        """
        super().resizeEvent(event)
        self.fit_in_view()
