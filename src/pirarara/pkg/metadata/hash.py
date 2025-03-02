#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib


def get_file_hash(file_path: str, algo: str = "sha256") -> str:
    """
    指定されたファイルのハッシュ値を計算して返す関数。

    この関数は、指定されたファイルの内容に基づいてハッシュ値を計算し、そのハッシュ値を文字列として返します。
    デフォルトのハッシュアルゴリズムは "sha256" です。

    Args:
        file_path (str): ハッシュ値を計算するファイルのパス
        algo (str): 使用するハッシュアルゴリズム（デフォルトは 'sha256'）

    Returns:
        str: ファイルの内容に基づくハッシュ値（16進数の文字列）

    Raises:
        FileNotFoundError: 指定されたファイルが存在しない場合
    """
    h_obj = hashlib.new(algo)
    block_size = 8192

    with open(file_path, "rb") as file:
        while chunk := file.read(block_size):
            h_obj.update(chunk)
    return h_obj.hexdigest()


def comp_file_hash(file_path: str, hash_code: str) -> bool:
    """
    指定されたファイルのハッシュ値が指定されたハッシュコードと一致するかを確認します。

    この関数は、ファイルのハッシュ値を計算し、指定されたハッシュコードと比較して、
    一致する場合はTrueを返し、それ以外の場合はFalseを返します。

    Args:
        file_path (str): ハッシュ値を計算して比較するファイルのパス
        hash_code (str): 比較対象のハッシュコード

    Returns:
        bool: ファイルのハッシュ値が指定されたハッシュコードと一致する場合はTrue、それ以外はFalse
    """
    file_hash_code = get_file_hash(file_path)
    return file_hash_code == hash_code
