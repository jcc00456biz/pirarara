#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import json
import os


class Translate:
    """
    Singletonクラスを使用して翻訳機能を提供するクラス。

    Attributes:
        locale_path (str): 翻訳ファイルが格納されているディレクトリのパス。
        select_language (str): 現在選択されている言語のコード。
        language_files (list): 言語ファイルのリスト。
        language_lists (list): 言語コードのリスト。
        translate_dic (dict): 翻訳データを格納する辞書。

    Methods:
        get_language_lists() -> list: 利用可能な言語リストを取得する。
        change_language(language: str) -> None: 言語を変更し、新しい言語の翻訳データを読み込む。
        trans(text: str) -> str: 与えられたテキストを翻訳する。
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singletonのインスタンスを作成するメソッド。

        Returns:
            Translate: Translateクラスの唯一のインスタンス。
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        locale_path: str | None = None,
        language: str = "ja_JP",
    ):
        """
        Translateクラスの初期化メソッド。

        Args:
            locale_path (str | None): 翻訳ファイルが格納されているディレクトリのパス。
            language (str): 現在選択されている言語のコード。デフォルトは"ja_JP"。
        """
        if not hasattr(self, "_initialized"):
            if locale_path is None:
                raise RuntimeError("Incorrect method usage.")
            self._initialized = True
        else:
            return

        # 選択中の言語
        self._select_language = language

        # 言語ファイルリスト
        self._full_path_language_files = glob.glob(
            os.path.join(locale_path, "*.json")
        )

        # パスを除いた言語ファイルリスト
        self._language_files = []
        for f in self._full_path_language_files:
            self._language_files.append(os.path.basename(f))

        # ファイル名から言語リストを作成
        self._language_lists = []
        for lang in self._language_files:
            self._language_lists.append(lang.replace(".json", ""))

        # 選択中の言語に対応するものがあるか？
        self._translate_dic = {}
        if language in self._language_lists:
            index = self._language_lists.index(language)
            # 存在すれば翻訳データを読み込む
            with open(
                self._full_path_language_files[index], "r", encoding="utf-8"
            ) as file:
                json_data = file.read()
            self._translate_dic = json.loads(json_data)

    def get_language_lists(self) -> list:
        """
        利用可能な言語リストを取得するメソッド。

        Args:
            language (str): 言語コード。

        Returns:
            list: 利用可能な言語リスト。
        """
        return self._language_lists

    def change_language(self, language: str) -> None:
        """
        言語を変更し、新しい言語の翻訳データを読み込むメソッド。

        Args:
            language (str): 設定する新しい言語のコード。
        """
        self._translate_dic = {}
        if language in self._language_lists:
            index = self._language_lists.index(language)
            # 存在すれば翻訳データを読み込む
            with open(
                self._full_path_language_files[index], "r", encoding="utf-8"
            ) as file:
                json_data = file.read()
            self._translate_dic = json.loads(json_data)

    def trans(self, selected_section: str, text: str) -> str:
        """
        与えられたテキストを翻訳するメソッド。

        Args:
            selected_section (str): セクション。
            text (str): 翻訳するテキスト。

        Returns:
            str: 翻訳後のテキスト。翻訳が見つからなければ元のテキストを返す。
        """
        if not selected_section:
            return text
        # パラメータが無効または有効なデータが読み出せていない場合
        if not text or not self._translate_dic:
            return text
        try:
            section_dic = self._translate_dic[selected_section]
            case_insensitive = section_dic.get("#case_insensitive#", 0)

            if case_insensitive:
                text = text.lower()
                section_dic = {
                    k.lower(): v
                    for k, v in section_dic.items()
                    if k != "#case_insensitive#"
                }

            return section_dic.get(text, text)

        except KeyError:
            return text

    def tr(self, selected_section: str, text: str) -> str:
        """
        与えられたテキストを翻訳するメソッド。(短縮版)

        Args:
            selected_section (str): セクション。
            text (str): 翻訳するテキスト。

        Returns:
            str: 翻訳後のテキスト。翻訳が見つからなければ元のテキストを返す。
        """
        return self.trans(selected_section, text)
