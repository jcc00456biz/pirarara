#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import configparser
import os
import platform

from pkg.const import __appname__
from PySide6.QtCore import QByteArray
from PySide6.QtGui import QFont, QFontDatabase

DEBUG = False


class AppConfig:
    """
    アプリケーションの設定を管理するクラス。

    このクラスはシングルトンパターンを用いて実装されています。
    設定ファイルの読み書きや、アプリケーションの情報を提供します。
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        クラスの唯一のインスタンスを生成または取得します。

        Returns:
            AppConfig: クラスの唯一のインスタンス。
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        AppConfigオブジェクトを初期化します。

        設定ファイルが存在しない場合、新しい設定ファイルを作成します。
        """
        if not hasattr(self, "_initialized"):
            self._initialized = True
        else:
            return

        # 構成ファイルのパスを決定
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
                    "An unidentified operating system was detected."
                )

        # ConfigParserの設定とデフォルト値の構成
        self.config = configparser.ConfigParser()
        cfg_dir = os.path.dirname(self.cfg_path)

        self.config["APP_INFO"] = {
            "log_dir": os.path.join(cfg_dir, "log"),
            "log": __appname__ + ".log",
            "db_dir": os.path.join(cfg_dir, "db"),
            "db": "metadata.db",
            "language": "ja_JP",
        }
        self.config["APP_GUI"] = {
            "font_size": "14",
            "main_window": "",
            "splitter1": "",
            "splitter2": "",
        }

        # 設定ファイルの存在確認と作成
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
        """
        設定ファイルに現在の設定を保存します。

        Returns:
            None
        """
        with open(
            self.cfg_path, "w", encoding="utf-8", newline="\n"
        ) as configfile:
            self.config.write(configfile)

    def read_config(self) -> None:
        """
        設定ファイルを読み込み、設定をロードします。

        Returns:
            None
        """
        with open(
            self.cfg_path, "r", encoding="utf-8", newline="\n"
        ) as configfile:
            self.config.read_file(configfile)

    def q_bytearray_to_str(self, value: QByteArray) -> str:
        """
        QByteArrayを文字列に変換します。

        Args:
            value (QByteArray): 変換するQByteArray。

        Returns:
            str: 変換後の文字列。
        """
        return str(value)

    def str_to_q_bytearray(self, value: str) -> QByteArray:
        """
        文字列をQByteArrayに変換します。

        Args:
            value (str): 変換する文字列。

        Returns:
            QByteArray: 変換後のQByteArray。
        """
        try:
            return QByteArray(ast.literal_eval(value))
        except (ValueError, SyntaxError):
            return QByteArray(b"0")

    def get_log_dir(self) -> str:
        """
        ログディレクトリのパスを取得します。

        Returns:
            str: ログディレクトリのパス。
        """
        return self.config["APP_INFO"]["log_dir"]

    def get_log_file(self) -> str:
        """
        ログファイル名を取得します。

        Returns:
            str: ログファイル名。
        """
        return self.config["APP_INFO"]["log"]

    def get_db_dir(self) -> str:
        """
        データベースディレクトリのパスを取得します。

        Returns:
            str: データベースディレクトリのパス。
        """
        return self.config["APP_INFO"]["db_dir"]

    def get_db_file(self) -> str:
        """
        データベースファイル名を取得します。

        Returns:
            str: データベースファイル名。
        """
        return self.config["APP_INFO"]["db"]

    def get_db_path(self) -> str:
        """
        データベースの完全なパスを取得します。

        Returns:
            str: データベースのパス。
        """
        return os.path.join(self.get_db_dir(), self.get_db_file())

    def get_language(self) -> str:
        """
        言語を取得します。

        Returns:
            str: ja_JP：日本語、en_US：英語
        """
        return self.config["APP_INFO"]["language"]

    def get_font_size(self) -> str:
        """
        フォントサイズを取得します。

        Returns:
            str: フォントサイズ
        """
        return self.config["APP_GUI"]["font_size"]

    def get_app_font(self) -> QFont:
        """
        Qフォントクラスを生成します。

        Returns:
            QFont: QFontクラスインスタンス
        """
        font = QFont()
        font.setPointSize(int(self.get_font_size()))
        return font

    def get_app_font_sizes(self) -> list:
        """
        フォントサイズリストの取得。

        Returns:
            list: フォントサイズのリスト
        """
        font = QFont()
        font_db = QFontDatabase()
        return list(map(str, font_db.pointSizes(font.family())))
