#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .about import AboutDialog
from .open_file import OpenFileDialog
from .plugins import PluginsDialog
from .setting import SettingDialog

__all__ = [
    "OpenFileDialog",
    "SettingDialog",
    "PluginsDialog",
    "AboutDialog",
]
