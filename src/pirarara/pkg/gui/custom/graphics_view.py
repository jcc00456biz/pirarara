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
    def __init__(self, parent=None):
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
        self.graphics_scene.clear()

    def fit_in_view(self):
        if self.image_item is not None:
            rect = self.image_item.boundingRect()
            self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_in_view()
