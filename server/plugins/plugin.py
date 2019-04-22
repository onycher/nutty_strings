
plugin_name = 'Plugin'


class Plugin:
    def __init__(self):
        self.driver = None
        self.name = 'Choose test suite...'

    def setup(self):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError


