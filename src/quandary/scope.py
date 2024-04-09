class Scope(dict):
    default = None

    def __init__(self, contents={}, functions={}, default=None):
        super().__init__(contents)
        self.default = default
        self.functions = functions
