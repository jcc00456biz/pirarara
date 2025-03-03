#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide6.QtGui import QFont


def qfont_to_stylesheet(font: QFont) -> str:
    """
    QFontオブジェクトをスタイルシート形式に変換します。

    Args:
        font (QFont): QFontオブジェクト。

    Returns:
        str: スタイルシート形式のフォント設定。
    """
    font_family = font.family()
    font_size = font.pointSize()
    font_weight = font.weight()
    font_italic = "italic" if font.italic() else "normal"

    stylesheet = (
        f"font-family: '{font_family}';"
        + f" font-size: {font_size}px;"
        + f" font-weight: {font_weight};"
        + f" font-style: {font_italic};"
    )

    return stylesheet
