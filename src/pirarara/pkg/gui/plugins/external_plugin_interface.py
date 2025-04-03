class PirararaExternalPluginInterface:
    def setting(self):
        raise NotImplementedError

    def do_action(self):
        raise NotImplementedError
