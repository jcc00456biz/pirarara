#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkg.const import __appname__
from PySide6.QtWidgets import QMessageBox


def info_message_box(message: str, parent=None) -> None:
    _ = QMessageBox.information(
        parent,
        f"{__appname__} : Information",
        message,
        QMessageBox.Ok,  # type: ignore
    )
    return


def warning_message_box(message: str, parent=None) -> None:
    _ = QMessageBox.warning(
        parent,
        f"{__appname__} : Warning",
        message,
        QMessageBox.Ok,  # type: ignore
    )
    return


def critical_message_box(message: str, parent=None) -> None:
    _ = QMessageBox.critical(
        parent,
        f"{__appname__} : Critical",
        message,
        QMessageBox.Ok,  # type: ignore
    )
    return


def question_message_box(message: str, parent=None) -> bool:
    reply = QMessageBox.question(
        parent,
        f"{__appname__} : Question",
        message,
        QMessageBox.Yes | QMessageBox.No,  # type: ignore
    )
    if reply == QMessageBox.Yes:  # type: ignore
        return True
    return False
