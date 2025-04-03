#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import inspect
import logging
import os
import sys

from pkg.config import AppConfig

logger = logging.getLogger(__name__)


class ExternalPlugins:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
        else:
            return

        # アプリケーション構成ファイルアクセスクラス
        self.app_config = AppConfig()
        # プラグインディレクトリ
        plugin_dir = self.app_config.get_plugins_dir()

        # sys.pathにプラグインディレクトリを追加
        if plugin_dir not in sys.path:
            sys.path.append(plugin_dir)

        # プラグインディレクトリ直下のディレクトリをリスト化
        plugin_dir = self.app_config.get_plugins_dir()
        if os.path.exists(plugin_dir):
            self.plugins_list = [
                d
                for d in os.listdir(plugin_dir)
                if os.path.isdir(os.path.join(plugin_dir, d))
            ]

    def load_plugins(self):
        # リストが空なら処理しない
        if not self.plugins_list:
            return None
        # プラグインのロード
        for plugin_name in self.plugins_list:
            try:
                # プラグインロード
                load_plugin = plugin_name + ".plugin"
                # 既にロード済かを確認
                if load_plugin in sys.modules:
                    logger.info(
                        f"The {plugin_name} has already been loaded."
                    )
                    plugin = sys.modules[load_plugin]
                    return plugin.ExternalPlugin()

                plugin = importlib.import_module(load_plugin)
                logger.info(
                    f"I was able to import this {plugin} successfully."
                )
                # ロードしたプラグインに指定クラスがあるかを確認
                classes = [
                    name
                    for name, _ in inspect.getmembers(
                        plugin, inspect.isclass
                    )
                ]
                if "ExternalPlugin" in classes:
                    return plugin.ExternalPlugin()
                return None
            except ImportError:
                logger.error(f"Failed to import {plugin}.")
                return None
