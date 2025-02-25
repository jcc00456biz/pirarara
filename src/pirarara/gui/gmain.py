#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PySide6 import QtUiTools


class MWindow:
    def __init__(self):

        aUILoader = QtUiTools.QUiLoader()

        ui_file_path = os.path.join(os.getcwd(), "main_window.ui")
        self.main_window = aUILoader.load(ui_file_path)
        self.main_window.show()
