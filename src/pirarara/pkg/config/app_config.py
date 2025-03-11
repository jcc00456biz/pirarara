#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import configparser
import os
import platform

from pkg.const import __appname__
from PySide6.QtCore import QByteArray

DEBUG = False


class AppConfig:

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

        # 構成ファイルのパス
        cfg_fname = f"{__appname__}.ini"
        if DEBUG:
            self.cfg_path = os.path.join(os.getcwd(), cfg_fname)
        else:
            os_type = platform.system()
            if os_type == "Windows":
                app_dir = os.path.join(
                    os.path.join(os.environ["APPDATA"]), __appname__
                )
                self.cfg_path = os.path.join(app_dir, cfg_fname)
            else:
                raise RuntimeError(
                    "An unverified operating system has been detected."
                )

        # ConfigParserを生成
        self.config = configparser.ConfigParser()

        # アプリケーション情報（デフォルト値）
        cfg_dir = os.path.dirname(self.cfg_path)

        self.config["APP_INFO"] = {
            "log_dir": os.path.join(cfg_dir, "log"),
            "log": __appname__ + ".log",
            "db_dir": os.path.join(cfg_dir, "db"),
            "db": "metadata.db",
        }
        self.config["APP_GUI"] = {
            "font_size": "14",
            "main_window": "",
            "splitter1": "",
            "splitter2": "",
        }

        # 設定ファイルがない場合は新規で作成する
        if not os.path.exists(self.cfg_path):
            dir_list = [
                os.path.dirname(self.cfg_path),
                self.config["APP_INFO"]["log_dir"],
                self.config["APP_INFO"]["db_dir"],
            ]
            for d in dir_list:
                os.makedirs(d, exist_ok=True)
            self.write_config()
            self.isdefault = True
        else:
            self.read_config()
            self.isdefault = False

    def write_config(self) -> None:
        # 設定ファイルに書き込む
        with open(
            self.cfg_path, "w", encoding="utf-8", newline="\n"
        ) as configfile:
            self.config.write(configfile)

    def read_config(self) -> None:
        with open(
            self.cfg_path, "r", encoding="utf-8", newline="\n"
        ) as configfile:
            self.config.read_file(configfile)

    def q_bytearray_to_str(self, value: QByteArray) -> str:
        return str(value)

    def str_to_q_bytearray(self, value: str) -> QByteArray:
        try:
            return QByteArray(ast.literal_eval(value))
        except (ValueError, SyntaxError):
            return QByteArray(b"0")

    def get_log_dir(self):
        return self.config["APP_INFO"]["log_dir"]

    def get_log_file(self):
        return self.config["APP_INFO"]["log"]

    def get_db_dir(self):
        return self.config["APP_INFO"]["db_dir"]

    def get_db_file(self):
        return self.config["APP_INFO"]["db"]

    def get_db_path(self):
        return os.path.join(self.get_db_dir(), self.get_db_file())
