#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pkg.metadata import set_media_info

from .base import PirararaBasePlugin


class ImportFilePlugin(PirararaBasePlugin):
    def __init__(self, files: list):
        if not isinstance(files, list):
            raise TypeError("The parameters must be list type")

        self.action_counts = len(files)
        if self.action_counts == 0:
            raise ValueError("There are no valid values")

        # 処理するファイルのリストを保持
        self.files = files

        super().__init__(self.action_counts)

    def do_action(self):
        fname = self.files[self.current_count]
        self.msg_label.setText(os.path.basename(fname))
        set_media_info(fname)
        super().do_action()
