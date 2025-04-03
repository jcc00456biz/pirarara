#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkg.gui.plugins import PirararaExternalPluginInterface


class ExternalPlugin(PirararaExternalPluginInterface):
    def do_action(self):
        print("do_action")

    def setting(self):
        print("setting")
